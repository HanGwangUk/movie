from django import forms
from .models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rank']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'