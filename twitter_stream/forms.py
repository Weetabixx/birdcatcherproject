from django import forms

class searchform(forms.Form):
    group = forms.CharField(label='group', max_length=100, widget=forms.HiddenInput())
    search_string = forms.CharField(label='', max_length=100)