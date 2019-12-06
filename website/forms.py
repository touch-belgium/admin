from django import forms
from dal import autocomplete

from .models import Bonus, Match, Pool

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('__all__')
        widgets = {
            "home_team": autocomplete.ModelSelect2(),
            "away_team": autocomplete.ModelSelect2()
        }

class BonusForm(forms.ModelForm):
    class Meta:
        model = Bonus
        fields = ('__all__')
        widgets = {
            "team": autocomplete.ModelSelect2()
        }


class PoolForm(forms.ModelForm):
    class Meta:
        model = Pool
        fields = ('__all__')
        widgets = {
            "teams": autocomplete.ModelSelect2Multiple()
        }
