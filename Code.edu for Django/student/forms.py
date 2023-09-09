from django import forms
from django.forms import fields, widgets
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "title",
            "image1",
            "image2",
            "image3",
            "content",
            "viewer",
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "nickname",
            "profile_pic",
            "intro",
            "group_in",
            "email",
        ]
        widgets = {
            "intro": forms.Textarea,
        }
        initial = {
            "group_in": 1
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            "group_name",
            "description",
            "group_pic",
        ]