from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [ 'restaurant_id', 'user_id', 'number_of_stars', 'comment', 'visited_date' ]