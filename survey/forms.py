from django import forms
from django.forms import extras
from survey.models import *
import datetime

class SurveyForm(forms.Form):
    """Survey Form"""
    name = forms.CharField(max_length=100)
    desc = forms.CharField(max_length=500, widget=forms.Textarea)
    expires = forms.BooleanField(required=False)
    expire_date = forms.DateField(required=False, widget=extras.SelectDateWidget())
    visibility_help = """if you choose 'private', only your friends can vote on this survey"""
    visibility = forms.ChoiceField(choices=Survey.VISIBILITY_CHOICE,
        help_text=visibility_help)
    
    def clean_expire_date(self):
        """validate that expire date is in the future"""
        expires = self.cleaned_data['expires']
        expire_date = self.cleaned_data['expire_date']
        if expires and expire_date is not None:
            now = datetime.date.today()
            if now > expire_date:
                raise forms.ValidationError(u'expire date must be in the future')
        return expire_date

        


