from django import forms
from . models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields=['title','description','release_date','poster','actors','category','trailer_link']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']