# courses/forms.py
from django import forms
from .models import CourseReview

class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ['rating', 'review_text']