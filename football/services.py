from collections import namedtuple
from dataclasses import dataclass
from football.models import LeagueSettings, MultiplePositionRosterSpot, Position, Projections, Team
from math import ceil, floor
from operator import attrgetter


@dataclass
class Player:
    name: str
    position: str
    team: str
    bye_week: int
    projected_points: float
    projections: Projections
    value: float = 0
    position_rank: int = 0


@dataclass
class PositionValues:
    quarterbacks: float = 10000
    running_backs: float = 10001
    wide_receivers: float = 10002
    tight_ends: float = 10003
    kickers: float = 10004
    team_defense_special_teams: float = 10005


@dataclass
class PositionsUsed:
    quarterbacks: float = 0
    running_backs: float = 0
    wide_receivers: float = 0
    tight_ends: float = 0
    flex_running_back_wide_receiver: float = 0
    flex_wide_receiver_tight_end: float = 0
    flex_running_back_wide_receiver_tight_end: float = 0
    offensive_players: float = 0
    kickers: float = 0
    team_defense_special_teams: float = 0


ProjectedGames = namedtuple('ProjectedGames', [
    'very_low',
    'low',
    'normal',
    'high',
    'very_high',
    ])

# set for use during fantasheet calculations
_roster_spots_not_used_for_starter_calculations = [
    'kickers',
    'punters',
    'team_defense_special_teams',
    'bench_spots',
    'injured_reserve_spots',
]


def calculate_fantaSheet(league_settings):
    
    projections = Projections.objects.all()

    players = []

    for player_projections in projections:
        bye_week = _get_bye_week(player_projections.team)
        projected_player_points = _calculate_projected_points(player_projections, league_settings)
        player = Player(
            name=player_projections.player,
            team=player_projections.team,
            bye_week=bye_week,
            position=player_projections.position,
            projected_points=projected_player_points,
            projections=player_projections)
        players.append(player)

    ranked_and_sorted_players = _rank_and_sort_players(players, league_settings)

    return ranked_and_sorted_players

def _calculate_dst_points_for_yards_or_points(setting_value, low, high, projected_games, projected_year: bool):
    
    if (setting_value == 0):
        return 0

    if (low == 0):
        low = -100 # some standard deviations will be below zero, necessary for comparisons

    if (not projected_year):
        if (projected_games.normal >= low and projected_games.normal <= high):
            return setting_value
        else:
            return 0 

    # games calculations based on normal deviation of 16 games
    normal_games = 10.912
    high_or_low_games = 2.176
    extreme_games = .336

    points = 0.0

    if (projected_games.very_low >= low and projected_games.very_low <= high):
        points += setting_value * extreme_games

    if (projected_games.low >= low and projected_games.low <= high):
        points += setting_value * high_or_low_games

    if (projected_games.normal >= low and projected_games.normal <= high):
        points += setting_value * normal_games

    if (projected_games.high >= low and projected_games.high <= high):
        points += setting_value * high_or_low_games

    if (projected_games.very_high >= low and projected_games.very_high <= high):
        points += setting_value * extreme_games

    return points

def _calculate_projected_points(player_projections, league_settings):
    
    # passing
    # projected_player_points += player_projections.passing_attempts * league_settings.
    # projected_player_points += player_projections.passing_completions * league_settings.
    projected_player_points = player_projections.passing_yards * league_settings.passing_yards
    # projected_player_points = player_projections.passing_yards * league_settings.passing_yards
    projected_player_points += player_projections.passing_touchdowns * league_settings.passing_touchdowns
    projected_player_points += player_projections.passing_interceptions * league_settings.passing_interceptions
    
    # rushing
    # projected_player_points += player_projections.rushing_attempts * league_settings.
    projected_player_points += player_projections.rushing_yards * league_settings.rushing_yards
    projected_player_points += player_projections.rushing_touchdowns * league_settings.rushing_touchdowns

    # receiving
    projected_player_points += player_projections.receiving_receptions * league_settings.receiving_receptions
    projected_player_points += player_projections.receiving_yards * league_settings.receiving_yards
    projected_player_points += player_projections.receiving_touchdowns * league_settings.receiving_touchdowns
    projected_player_points += player_projections.player_fumbles_lost * league_settings.individual_player_fumbles_lost

    # kicking
    projected_player_points += _get_kicker_points(player_projections, league_settings)

    # defense/special teams
    projected_player_points += _get_dst_points(player_projections, league_settings)

    return projected_player_points

def _get_bye_week(team_abbreviation: str):
    
    try:
        team = Team.objects.only('abbreviation').get(abbreviation=team_abbreviation)
    except:
        return 0
    else:
        return team.bye_week     

def _get_dst_points(player_projections, league_settings):
    
    if (player_projections.position != 'dst'):
        return 0

    dst_points = 0.0

    # updated 9.30.2020
    # based of 2019 season stats
    frequency_kickoff_touchdown = .079545
    frequency_punt_touchdown = .079545
    frequency_interception_touchdown = .397727
    frequency_fumble_touchdown = .386364
    frequency_blocked_kick_or_punt_touchdown = .056819
    # values for yards and points against found in getDSTPointsForPointsAgainst() and getDSTPointsForYardsAgainst()

    # frequencies should add up to 1
    assert 1 == frequency_kickoff_touchdown + frequency_punt_touchdown + frequency_interception_touchdown + frequency_fumble_touchdown + frequency_blocked_kick_or_punt_touchdown

    dst_points += player_projections.dst_sacks * league_settings.dst_sacks
    dst_points += player_projections.dst_interceptions * league_settings.dst_interceptions
    dst_points += player_projections.dst_fumbles_recovered * league_settings.dst_fumbles_recovered
    dst_points += player_projections.dst_touchdowns * frequency_kickoff_touchdown * league_settings.dst_kickoff_return_touchdowns
    dst_points += player_projections.dst_touchdowns * frequency_punt_touchdown * league_settings.dst_punt_return_touchdowns
    dst_points += player_projections.dst_touchdowns * frequency_interception_touchdown * league_settings.dst_interception_return_touchdowns
    dst_points += player_projections.dst_touchdowns * frequency_fumble_touchdown * league_settings.dst_fumble_return_touchdowns
    dst_points += player_projections.dst_touchdowns * frequency_blocked_kick_or_punt_touchdown * league_settings.dst_blocked_punt_or_field_goal_return_touchdowns
    dst_points += _get_dst_points_for_points_against(player_projections.dst_points_against, league_settings)
    # TODO dst yards against
    # dst_points += player_projections.dst_yards_against * league_settings.

    return dst_points

def _get_dst_points_for_points_against(projected_against, league_settings):
    
    # updated 10.1.2020
    # based on http://archive.advancedfootballanalytics.com/2009/05/are-nfl-coaches-too-timid.html
    points_per_game_standard_deviation = 10.0

    projected_year = False
    if (projected_against > 100): # TODO find a better way
        projected_year = True
        projected_against /= 16.0 # total games in a season
    
    projected_games = _get_projected_games_based_on_std_deviation(
        start=projected_against, 
        standard_deviation=points_per_game_standard_deviation)
    dst_points_against_points = 0.0
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_0_points_allowed,
        low=0,
        high=0,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_1_to_6_points_allowed,
        low=1,
        high=6,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_7_to_13_points_allowed,
        low=7,
        high=13,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_14_to_17_points_allowed,
        low=14,
        high=17,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_14_to_20_points_allowed,
        low=14,
        high=20,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_18_to_21_points_allowed,
        low=18,
        high=21,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_21_to_27_points_allowed,
        low=21,
        high=27,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_22_to_27_points_allowed,
        low=22,
        high=27,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_28_to_34_points_allowed,
        low=28,
        high=34,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_35_to_45_points_allowed,
        low=35,
        high=45,
        projected_games=projected_games,
        projected_year=projected_year)
    dst_points_against_points += _calculate_dst_points_for_yards_or_points(
        setting_value=league_settings.dst_46_or_more_points_allowed,
        low=46,
        high=500,
        projected_games=projected_games,
        projected_year=projected_year)
    
    return dst_points_against_points

def _get_full_position_string(position_abbreviation):

    try:
        position = Position.objects.only('abbreviation').get(abbreviation=position_abbreviation)
    except:
        return 0
    else:
        return position.name 

def _get_kicker_points(player_projections, league_settings):
    
    if (player_projections.position != 'k'):
        return 0

    kicker_points = 0.0

    # updated 9.30.2020
    # stats from 2018 and 2019 seasons
    frequency_made_0_to_39 = .603326
    frequency_made_40_to_49 = .286486
    frequency_made_50_to_59 = .100187
    frequency_made_60_plus = .010001 # no stats on 60 plus fgs
    frequency_missed_0_to_39 = .145957
    frequency_missed_40_to_49 = .504931
    frequency_missed_50_to_59 = .299112
    frequency_missed_60_plus = .05 # no stats on 60 plus fgs

    # frequencies should add up to 1
    assert 1 == frequency_made_0_to_39 + frequency_made_40_to_49 + frequency_made_50_to_59 + frequency_made_60_plus 
    assert 1 == frequency_missed_0_to_39 + frequency_missed_40_to_49 + frequency_missed_50_to_59 + frequency_missed_60_plus

    # makes
    kicker_points += (player_projections.kicking_field_goals_made * frequency_made_0_to_39) * league_settings.kicking_field_goal_0_to_39
    kicker_points += (player_projections.kicking_field_goals_made * frequency_made_40_to_49) * league_settings.kicking_field_goal_40_to_49
    kicker_points += (player_projections.kicking_field_goals_made * frequency_made_50_to_59) * league_settings.kicking_field_goal_50_to_59
    kicker_points += (player_projections.kicking_field_goals_made * frequency_made_60_plus) * league_settings.kicking_field_goal_60_or_more

    # misses
    projected_missed_field_goals = player_projections.kicking_field_goals_attempted - player_projections.kicking_field_goals_made
    kicker_points += (projected_missed_field_goals * frequency_missed_0_to_39) * league_settings.kicking_missed_field_goal_0_to_39
    kicker_points += (projected_missed_field_goals * frequency_missed_40_to_49) * league_settings.kicking_missed_field_goal_40_to_49
    kicker_points += (projected_missed_field_goals * frequency_missed_50_to_59) * league_settings.kicking_missed_field_goal_50_to_59
    kicker_points += (projected_missed_field_goals * frequency_missed_60_plus) * league_settings.kicking_missed_field_goal_60_or_more

    # extra points
    kicker_points += player_projections.kicking_extra_points_made * league_settings.kicking_point_after_touchdowns
    # TODO calculate extra point misses
    # ex: kickerEPMadePct = .950292M;

    return kicker_points

def _set_player_position_ranks(sorted_players):

    # positions = Position.objects.only('abbreviation')
    positions = Position.objects.values_list('abbreviation', flat=True)

    assert positions

    position_ranks = []

    for position in positions:
        position_rank = {
            'position' : position,
            'rank' : 1
        }
        position_ranks.append(position_rank)

    for player in sorted_players:
        for position in position_ranks:
            if player.position == position['position']:
                player.position_rank = position['rank']
                position['rank'] += 1
                break
        
    return sorted_players

def _get_number_of_position_used(position, league_settings, starters_count_minus_worthless_positions):
    
    number_used = 0

    if (starters_count_minus_worthless_positions != 0):
        number_used = ((((position) / starters_count_minus_worthless_positions) * 
            league_settings.roster_bench_spots * 
            league_settings.number_of_teams) + 
            (league_settings.number_of_teams * (position)))

    return number_used

def _get_position_abbreviation(position):

    try:
        position = Position.objects.only('name').get(name=position)
    except:
        return 0
    else:
        return position.abbreviation 

def _get_position_value(position, number_of_position_used, player_projections):

    if (number_of_position_used <= 0):
        return -1

    position_value = -1
    low_player_value = 0
    high_player_value = 0
    ceiling_player = ceil(number_of_position_used)
    floor_player = floor(number_of_position_used)
    decimal = number_of_position_used - floor(number_of_position_used)
    position_abbreviation = _get_position_abbreviation(position)

    for player in player_projections:
        assert 0 != player.position_rank # players need rankings
        if (player.position.lower() == position_abbreviation):
            if (player.position_rank == ceiling_player):
                low_player_value = player.projected_points
            elif (player.position_rank == floor_player):
                high_player_value = player.projected_points

            # break out for speed, since player is already found
            if (low_player_value > 0 and high_player_value > 0):
                break
            if (low_player_value > 0 or high_player_value > 0):
                if (ceiling_player == floor_player):
                    break

    if (decimal > 0): # combine 2 values
        low_value = low_player_value * decimal
        high_value = high_player_value* (1 - decimal)
        position_value = high_value + low_value
    else:
        position_value = low_player_value

    return position_value

def _get_position_values(player_projections, league_settings):

    position_values = PositionValues()  
    positions_used = _get_positions_used(league_settings)

    positions_used = _get_special_roster_type_values(positions_used, player_projections)

    position_values_attributes = [attr for attr in dir(position_values) if not attr.startswith('__')]
    for attribute in position_values_attributes:
        position_value = _get_position_value(
                                    position=attribute,
                                    number_of_position_used=getattr(positions_used, attribute),
                                    player_projections=player_projections,
                                )
        if (position_value > 0):
            setattr(
                position_values,
                attribute,
                position_value
            )

    

    return position_values

def _get_positions_used(league_settings):

    positions_used = PositionsUsed()
    starters_minus_worthless_positions = _get_starters_count_minus_worthless_positions(league_settings)

    positions_used_attributes = [attr for attr in dir(positions_used) if not attr.startswith('__')]
    for attribute in positions_used_attributes:
        if (_roster_spots_not_used_for_starter_calculations.__contains__(attribute)):
            setattr(
            positions_used,
            attribute,
            getattr(
                league_settings,
                ('roster_%s' % attribute)) *
                league_settings.number_of_teams)
        else:
            setattr(
                positions_used,
                attribute,
                _get_number_of_position_used(
                    position=getattr(
                        league_settings,
                        ('roster_%s' % attribute)),
                    league_settings=league_settings,
                    starters_count_minus_worthless_positions=starters_minus_worthless_positions))

    return positions_used

def _get_projected_games_based_on_std_deviation(start: float, standard_deviation: float):
    
    projected_games = ProjectedGames(
        very_low=start - standard_deviation * 2, # 2 standard diveations below
        low=start - standard_deviation, # 1 standard diveation below
        normal=start,
        high=start + standard_deviation, # 1 standard diveation above
        very_high=start + standard_deviation * 2) # 2 standard diveations above

    return projected_games

def _get_special_roster_type_values(positions_used, player_projections):

    special_roster_spots = MultiplePositionRosterSpot.objects.all()
  
    for special_roster_spot in special_roster_spots:
        if (getattr(positions_used, special_roster_spot.title) > 0):
            # print(special_roster_spot, getattr(positions_used, special_roster_spot.title), special_roster_spot.positions.all())
            positions_used = _update_positions_used(positions_used, special_roster_spot, player_projections)

    return positions_used

def _get_starters_count_minus_worthless_positions(league_settings):

    starters_minus_worthless_positions = 0

    league_settings_attributes = [attr for attr in dir(league_settings) if attr.startswith('roster_')]
    for attribute in league_settings_attributes:
        starters_minus_worthless_positions += getattr(league_settings, attribute)

    for worthless_position in _roster_spots_not_used_for_starter_calculations:
        starters_minus_worthless_positions -= getattr(league_settings, f'roster_{worthless_position}')

    return starters_minus_worthless_positions

def _rank_and_sort_players(players, league_settings):
    
    sorted_players = sorted(players, key= attrgetter('projected_points'), reverse=True)

    sorted_players = _set_player_position_ranks(sorted_players)

    position_values = _get_position_values(sorted_players, league_settings)

    sorted_players = _set_player_values(sorted_players, position_values)

    sorted_players = sorted(players, key= attrgetter('value'), reverse=True)

    return sorted_players

def _set_player_values(players, position_values):

    for player in players:
        position = _get_full_position_string(position_abbreviation=player.position)
        position_value = getattr(position_values, position)
        player.value = player.projected_points - position_value
    
    return players

def _update_positions_used(positions_used, special_roster_spot, player_projections):
    
    possible_positions = special_roster_spot.positions.all()
    amount_needed = ceil(getattr(positions_used, special_roster_spot.title)) 
    position_ranges = []
    possible_players = []

    for position in possible_positions:
        position_range = {
            "position_abbreviation" : _get_position_abbreviation(position.name),
            "start_index" : getattr(positions_used, position.name),
            "end_index" : getattr(positions_used, position.name) + amount_needed,
        }
        position_ranges.append(position_range)

    for player in player_projections:
        for position_range in position_ranges:
            if (
                player.position == position_range['position_abbreviation']
                and player.position_rank > position_range['start_index']
                and player.position_rank <= position_range['end_index']
                ):
                possible_players.append(player)

    players_to_use = possible_players[:amount_needed]

    for position in possible_positions:
        position_abbreviation = _get_position_abbreviation(position.name)
        position_count = sum(player.position == position_abbreviation for player in players_to_use)
        setattr(
            positions_used, 
            position.name, 
            getattr(positions_used, position.name) + position_count
            )

    return positions_used
