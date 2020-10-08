from collections import namedtuple
from dataclasses import dataclass
from football.models import LeagueSettings, Projections, Team
from operator import attrgetter


@dataclass
class Player:
    name: str
    position: str
    team: str
    bye_week: int
    projected_points: float
    projections: Projections


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
_positions_to_only_draft_one = [
    'kickers',
    'team_defense_special_teams',
]

# loop object attributes and values
# for attr, value in positions_used.__dict__.items():
#     print(attr, value)


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


def _get_number_of_position_used(position, league_settings):
    
    number_used = 0
    starters = _get_roster_size_minus_k_and_dst(league_settings)
    if (starters != 0):
        number_used = ((((position) / starters) * 
        league_settings.roster_bench_spots * 
        league_settings.number_of_teams) + 
        (league_settings.number_of_teams * (position)))

    return number_used


def _get_positions_used(league_settings):

    positions_used = PositionsUsed()

    positions_used_attributes = [attr for attr in dir(positions_used) if not attr.startswith('__')]
    for attribute in positions_used_attributes:
        if (_positions_to_only_draft_one.__contains__(attribute)):
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
                    league_settings=league_settings))

    return positions_used


def _get_projected_games_based_on_std_deviation(start: float, standard_deviation: float):
    
    projected_games = ProjectedGames(
        very_low=start - standard_deviation * 2, # 2 standard diveations below
        low=start - standard_deviation, # 1 standard diveation below
        normal=start,
        high=start + standard_deviation, # 1 standard diveation above
        very_high=start + standard_deviation * 2) # 2 standard diveations above

    return projected_games


def _get_roster_size_minus_k_and_dst(league_settings):

    roster_spots = [
        league_settings.roster_quarterbacks,
        league_settings.roster_team_quarterbacks,
        league_settings.roster_running_backs,
        league_settings.roster_wide_receivers,
        league_settings.roster_tight_ends,
        league_settings.roster_flex_running_back_wide_receiver,
        league_settings.roster_flex_wide_receiver_tight_end,
        league_settings.roster_flex_running_back_wide_receiver_tight_end,
        league_settings.roster_offensive_players,
        league_settings.roster_defensive_tackles,
        league_settings.roster_defensive_lines,
        league_settings.roster_linebackers,
        league_settings.roster_edge_rushers,
        league_settings.roster_defensive_lines,
        league_settings.roster_cornerbacks,
        league_settings.roster_safeties,
        league_settings.roster_defensive_backs,
        league_settings.roster_defensive_players,
        league_settings.roster_punters,
        league_settings.roster_head_coaches,
        league_settings.roster_bench_spots,
    ]
    
    roster_size_minus_k_and_dst = sum(roster_spots)
    
    return roster_size_minus_k_and_dst


def _rank_and_sort_players(players, league_settings):
    
    sorted_players= sorted(players, key= attrgetter('projected_points'), reverse=True)

    roster_size_minus_k_and_dst = _get_roster_size_minus_k_and_dst(league_settings)

    positions_used = _get_positions_used(league_settings)

    return sorted_players