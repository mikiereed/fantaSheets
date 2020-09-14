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
    title = models.CharField(max_length=50)
    number_of_teams = models.IntegerField('Number of Teams')
    # roster settings
    roster_quarterbacks = models.IntegerField('Quarterbacks')
    roster_team_quarterbacks = models.IntegerField('Team Quarterbacks')
    roster_running_backs = models.IntegerField('Running Backs')
    roster_flex_running_back_wide_receiver = models.IntegerField('Flex RB/WR')
    roster_wide_receivers = models.IntegerField('Wide Receivers')
    roster_flex_wide_receiver_tight_end = models.IntegerField('Flex WR/TE')
    roster_tight_ends = models.IntegerField('Tight Ends')
    roster_flex_running_back_wide_receiver_tight_end = models.IntegerField(
        'Flex RB/WR/TE')
    roster_offensive_players = models.IntegerField('Offensive Players')
    roster_defensive_tackles = models.IntegerField('Defensive Tackles')
    roster_defensive_ends = models.IntegerField('Defensive Ends')
    roster_linebackers = models.IntegerField('Linebackers')
    roster_edge_rushers = models.IntegerField('Edge Rushers')
    roster_defensive_lines = models.IntegerField('Defensive Lines')
    roster_cornerbacks = models.IntegerField('Cornerbacks')
    roster_safeties = models.IntegerField('Safeties')
    roster_defensive_backs = models.IntegerField('Defensive Backs')
    roster_defensive_players = models.IntegerField('Defensive Players')
    roster_team_defense_special_teams = models.IntegerField(
        'Defense / Special Teams')
    roster_kickers = models.IntegerField('Kickers')
    roster_punters = models.IntegerField('Punters')
    roster_head_coaches = models.IntegerField('Head Coaches')
    roster_bench_spots = models.IntegerField('Bench Spots')
    roster_injured_reserve_spots = models.IntegerField('Injured Reserve Spots')
    # passing settings
    passing_yards = models.FloatField()
    passing_touchdowns = models.FloatField()
    passing_interceptions = models.FloatField()
    passing_two_point_conversions = models.FloatField()
    # rushing settings
    rushing_yards = models.FloatField()
    rushing_touchdowns = models.FloatField()
    rushing_two_point_conversions = models.FloatField()
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
