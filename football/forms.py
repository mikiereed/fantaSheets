from django import forms
from .models import LeagueSettings


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
