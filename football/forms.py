from django import forms
from .models import LeagueSettings


class AnonymousLeagueSettingsForm(forms.ModelForm):
    class Meta:
        model = LeagueSettings
        exclude = ('league_hosting_site',
                   'title',
                   'roster_team_quarterbacks',
                   'roster_defensive_tackles',
                   'roster_defensive_ends',
                   'roster_linebackers',
                   'roster_edge_rushers',
                   'roster_defensive_lines',
                   'roster_cornerbacks',
                   'roster_safeties',
                   'roster_defensive_backs',
                   'roster_defensive_players',
                   'roster_team_defense_special_teams',
                   'roster_kickers',
                   'roster_punters',
                   'roster_head_coaches',
                   'roster_bench_spots',
                   'roster_injured_reserve_spots',
                   'passing_yards',
                   'passing_interceptions',
                   'passing_two_point_conversions',
                   'rushing_yards',
                   'rushing_touchdowns',
                   'rushing_two_point_conversions',
                   'receiving_yards',
                   'receiving_touchdowns',
                   'receiving_two_point_conversions',
                   'individual_player_fumbles_lost',
                   'individual_player_kickoff_return_touchdowns',
                   'individual_player_punt_return_touchdowns',
                   'individual_player_fumble_recovered_touchdowns',
                   'kicking_point_after_touchdowns',
                   'kicking_missed_point_after_touchdowns',
                   'kicking_field_goal_0_to_39',
                   'kicking_missed_field_goal_0_to_39',
                   'kicking_field_goal_40_to_49',
                   'kicking_missed_field_goal_40_to_49',
                   'kicking_field_goal_50_to_59',
                   'kicking_missed_field_goal_50_to_59',
                   'kicking_field_goal_60_or_more',
                   'kicking_missed_field_goal_60_or_more',
                   'dst_kickoff_return_touchdowns',
                   'dst_punt_return_touchdowns',
                   'dst_interception_return_touchdowns',
                   'dst_fumble_return_touchdowns',
                   'dst_blocked_punt_or_field_goal_return_touchdowns',
                   'dst_extra_points_returned',
                   'dst_sacks',
                   'dst_blocked_punt_point_after_touchdown_field_goal',
                   'dst_interceptions',
                   'dst_fumbles_recovered',
                   'dst_safeties',
                   'dst_0_points_allowed',
                   'dst_1_to_6_points_allowed',
                   'dst_7_to_13_points_allowed',
                   'dst_14_to_17_points_allowed',
                   'dst_14_to_20_points_allowed',
                   'dst_18_to_21_points_allowed',
                   'dst_21_to_27_points_allowed',
                   'dst_22_to_27_points_allowed',
                   'dst_28_to_34_points_allowed',
                   'dst_35_to_45_points_allowed',
                   'dst_46_or_more_points_allowed',)

    def __init__(self, *args, **kwargs):
        super(AnonymousLeagueSettingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class LeagueSettingsForm(forms.ModelForm):
    class Meta:
        model = LeagueSettings
        # fields = ('title', 'league_hosting_site', 'number_of_teams')
        exclude = ('owner',
                   'roster_defensive_tackles',
                   'roster_defensive_ends',
                   'roster_defensive_lines',
                   'roster_defensive_players',
                   'roster_linebackers',
                   'roster_edge_rushers',
                   'roster_defensive_backs',
                   'roster_cornerbacks',
                   'roster_safeties',
                   'roster_punters',
                   'roster_head_coaches',
                   'roster_team_quarterbacks',
                   'roster_injured_reserve_spots',)

    def __init__(self, *args, **kwargs):
        super(LeagueSettingsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



    # def clean(self):
    #     # change all nulls to 0s
    #     for key, value in self.cleaned_data.items():
    #         print(f'{key} : {value}')
    #         # if value is None:
    #             # filter[key] = 0

        # def clean_url(self):
        # url = self.cleaned_data['url']
        # valid_extensions = ['jpg', 'jpeg']
        # extension = url.rsplit('.', 1)[1].lower()
        # if extension not in valid_extensions:
        #     raise forms.ValidationError('The given URL does not ' \
        #                                 'match valid image extensions.')
        # return url
        
        # def save(self, force_insert=False,
        #          force_update=False,
        #          commit=True):
        # league_settings = super().save(commit=False)
        # image_url = self.cleaned_data['url']
        # name = slugify(image.title)
        # extension = image_url.rsplit('.', 1)[1].lower()
        # image_name = f'{name}.{extension}'
        # # download image from the given URL
        # response = request.urlopen(image_url)
        # image.image.save(image_name,
        #                  ContentFile(response.read()),
        #                  save=False)
        # if commit:
        #     league_settings.save()
        # return league_settings
