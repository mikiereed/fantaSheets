from operator import attrgetter

from football.models import LeagueSettings, Projections, Team


class Player:
    def __init__(self, name, projected_points, projections):
        self.name = name
        self.projected_points = projected_points
        self.projections = projections

    def __str__(self):
        return self.name


def calculate_fantaSheet(league_settings):
    projections = Projections.objects.all()

    players = []

    for player_projections in projections:
        projected_player_points = calculate_projected_points(player_projections, league_settings)
        player = Player(player_projections.player, projected_player_points, player_projections)
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
    kicks_missed = player_projections.kicking_field_goals_attempted - player_projections.kicking_field_goals_made
    # TODO kicking kicks missed
    # projected_player_points += player_projections.kicking_field_goals_attempted * league_settings.
    # TODO kicking kicks made
    # projected_player_points += player_projections.kicking_field_goals_made
    projected_player_points += player_projections.kicking_extra_points_made * league_settings.kicking_point_after_touchdowns

    # defense/special teams
    projected_player_points += player_projections.dst_sacks * league_settings.dst_sacks
    projected_player_points += player_projections.dst_interceptions * league_settings.dst_interceptions
    projected_player_points += player_projections.dst_fumbles_recovered * league_settings.dst_fumbles_recovered
    # projected_player_points += player_projections.dst_fumbles_forced * league_settings.
    # TODO dst touchdowns
    # projected_player_points += player_projections.dst_touchdowns * league_settings.
    projected_player_points += player_projections.dst_safeties * league_settings.dst_safeties
    # TODO dst points against
    # projected_player_points += player_projections.dst_points_against * league_settings.
    # TODO dst yards against
    # projected_player_points += player_projections.dst_yards_against * league_settings.

    return projected_player_points

