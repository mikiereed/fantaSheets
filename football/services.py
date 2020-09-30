from operator import attrgetter

from football.models import LeagueSettings, Projections, Team


class Player:
    def __init__(self, name, position, projected_points, projections):
        self.name = name
        self.position = position
        self.projected_points = projected_points
        self.projections = projections

    def __str__(self):
        return self.name


def calculate_fantaSheet(league_settings):
    projections = Projections.objects.all()

    players = []

    for player_projections in projections:
        projected_player_points = calculate_projected_points(player_projections, league_settings)
        player = Player(player_projections.player, player_projections.position, projected_player_points, player_projections)
        players.append(player)
        sorted_players= sorted(players, key= attrgetter('projected_points'), reverse=True)

    return sorted_players


def calculate_projected_points(player_projections, league_settings):
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
    projected_player_points += getKickerPoints(player_projections, league_settings)
    projected_player_points += player_projections.kicking_extra_points_made * league_settings.kicking_point_after_touchdowns

    # defense/special teams
    projected_player_points += getDefenseSpecialTeamsPoints(player_projections, league_settings)

    return projected_player_points


def getDefenseSpecialTeamsPoints(player_projections, league_settings):
    if (player_projections.position != 'dst'):
        return 0

    dst_points = 0

    # updated 9.30.2020
    # based of 2019 season stats
    frequency_kickoff_touchdown = .079545
    frequency_punt_touchdown = .079545
    frequency_interception_touchdown = .397727
    frequency_fumble_touchdown = .386364
    frequency_blocked_kick_or_punt_touchdown = .056819

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
    # TODO dst points against
    # dst_points += player_projections.dst_points_against * league_settings.
    # TODO dst yards against
    # dst_points += player_projections.dst_yards_against * league_settings.

    return dst_points


def getKickerPoints(player_projections, league_settings):
    if (player_projections.position != 'k'):
        return 0

    kicker_points = 0

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

    return kicker_points