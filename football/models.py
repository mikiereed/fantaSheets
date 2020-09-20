from django.db import models
from django.contrib.auth.models import User


class LeagueSettings(models.Model):
    LEAGUE_SITES = (
        ('espn', 'ESPN'),
        ('yahoo', 'Yahoo'),
        ('other', 'Other'),
    )
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,)
    league_hosting_site = models.CharField(
        'Hosting Site', max_length=20, choices=LEAGUE_SITES)
    number_of_teams = models.IntegerField('Number of Teams')
    title = models.CharField('fantaSheet Name', max_length=50)

    # roster settings
    roster_quarterbacks = models.PositiveIntegerField('Quarterbacks')
    roster_team_quarterbacks = models.PositiveIntegerField('Team Quarterbacks')
    roster_running_backs = models.PositiveIntegerField('Running Backs')
    roster_wide_receivers = models.PositiveIntegerField('Wide Receivers')
    roster_tight_ends = models.PositiveIntegerField('Tight Ends')
    roster_flex_running_back_wide_receiver = models.PositiveIntegerField('Flex RB/WR')
    roster_flex_wide_receiver_tight_end = models.PositiveIntegerField('Flex WR/TE')
    roster_flex_running_back_wide_receiver_tight_end = models.PositiveIntegerField(
        'Flex RB/WR/TE')
    roster_offensive_players = models.PositiveIntegerField('Offensive Players')
    roster_defensive_tackles = models.PositiveIntegerField('Defensive Tackles')
    roster_defensive_ends = models.PositiveIntegerField('Defensive Ends')
    roster_linebackers = models.PositiveIntegerField('Linebackers')
    roster_edge_rushers = models.PositiveIntegerField('Edge Rushers')
    roster_defensive_lines = models.PositiveIntegerField('Defensive Lines')
    roster_cornerbacks = models.PositiveIntegerField('Cornerbacks')
    roster_safeties = models.PositiveIntegerField('Safeties')
    roster_defensive_backs = models.PositiveIntegerField('Defensive Backs')
    roster_defensive_players = models.PositiveIntegerField('Defensive Players')
    roster_team_defense_special_teams = models.PositiveIntegerField(
        'Defense / Special Teams')
    roster_kickers = models.PositiveIntegerField('Kickers')
    roster_punters = models.PositiveIntegerField('Punters')
    roster_head_coaches = models.PositiveIntegerField('Head Coaches')
    roster_bench_spots = models.PositiveIntegerField('Bench Spots')
    roster_injured_reserve_spots = models.PositiveIntegerField('Injured Reserve Spots')
    # passing settings
    passing_yards = models.FloatField('Points Per Passing Yard')
    passing_touchdowns = models.FloatField('Points Per Passing Touchdown')
    passing_interceptions = models.FloatField('Points Per Interception')
    passing_two_point_conversions = models.FloatField(
        'Points Per Passing Two Point Conversion')
    # rushing settings
    rushing_yards = models.FloatField('Points Per Rushing Yard')
    rushing_touchdowns = models.FloatField('Points Per Rushing Touchdown')
    rushing_two_point_conversions = models.FloatField(
        'Points Per Rushing Two Point Conversion')
    # receiving settings
    receiving_receptions = models.FloatField()
    receiving_yards = models.FloatField()
    receiving_touchdowns = models.FloatField()
    receiving_two_point_conversions = models.FloatField()
    # kicking settings
    kicking_point_after_touchdowns = models.FloatField()
    kicking_missed_point_after_touchdowns = models.FloatField()
    kicking_field_goal_0_to_39 = models.FloatField()
    kicking_missed_field_goal_0_to_39 = models.FloatField()
    kicking_field_goal_40_to_49 = models.FloatField()
    kicking_missed_field_goal_40_to_49 = models.FloatField()
    kicking_field_goal_50_to_59 = models.FloatField()
    kicking_missed_field_goal_50_to_59 = models.FloatField()
    kicking_field_goal_60_or_more = models.FloatField()
    kicking_missed_field_goal_60_or_more = models.FloatField()
    # defense / special teams settings
    dst_kickoff_return_touchdowns = models.FloatField()
    dst_punt_return_touchdowns = models.FloatField()
    dst_interception_return_touchdowns = models.FloatField()
    dst_fumble_return_touchdowns = models.FloatField()
    dst_blocked_punt_or_field_goal_return_touchdowns = models.FloatField()
    dst_extra_points_returned = models.FloatField()
    dst_sacks = models.FloatField()
    dst_blocked_punt_point_after_touchdown_field_goal = models.FloatField()
    dst_interceptions = models.FloatField()
    dst_fumbles_recovered = models.FloatField()
    dst_safeties = models.FloatField()
    dst_0_points_allowed = models.FloatField()
    dst_1_to_6_points_allowed = models.FloatField()
    dst_7_to_13_points_allowed = models.FloatField()
    dst_14_to_17_points_allowed = models.FloatField()
    dst_14_to_20_points_allowed = models.FloatField()
    dst_18_to_21_points_allowed = models.FloatField()
    dst_21_to_27_points_allowed = models.FloatField()
    dst_22_to_27_points_allowed = models.FloatField()
    dst_28_to_34_points_allowed = models.FloatField()
    dst_35_to_45_points_allowed = models.FloatField()
    dst_46_or_more_points_allowed = models.FloatField()
    # TODO add yardage points
    # individual miscellaneous settings
    individual_player_kickoff_return_touchdowns = models.FloatField()
    individual_player_punt_return_touchdowns = models.FloatField()
    individual_player_fumble_recovered_touchdowns = models.FloatField()
    individual_player_fumbles_lost = models.FloatField()

    class Meta:
        ordering = ('title',)
        verbose_name_plural = "League Settings"

    def __str__(self):
        return self.title
