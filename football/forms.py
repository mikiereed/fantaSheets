from django import forms
from .models import LeagueSettings


class LeagueSettingsGeneralForm(forms.ModelForm):
    class Meta:
        model = LeagueSettings
        fields = ('title', 'league_hosting_site', 'number_of_teams')

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
