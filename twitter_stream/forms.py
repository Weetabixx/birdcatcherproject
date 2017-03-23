from django import forms

class searchform(forms.Form):
    group = forms.CharField(label='group', max_length=100)
    search_string = forms.CharField(label='search_string', max_length=100)