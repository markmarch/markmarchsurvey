from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=25)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Password", min_length=6)
    password_repeat = forms.CharField(widget=forms.PasswordInput, label="Repeat Password" , min_length=6)

    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'%s is already taken.' % username)


class SignInForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)


class UserProfileForm(forms.Form):
    username = forms.CharField(max_length=25)
    email = forms.EmailField()
    last_name = forms.CharField(max_length=25, required=False)
    first_name = forms.CharField(max_length=25, required=False)
    twitter = forms.CharField(max_length=25, required=False)
    github = forms.CharField(max_length=25, required=False)
    website = forms.URLField(required=False)