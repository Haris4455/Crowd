from django import forms
from django.forms import ModelForm, Textarea
from askcrowd.models import Question, Answer
class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('details',)
        widgets = {'details': Textarea(attrs={'cols': 100, 'rows': 20}),}

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'detail', 'tags', 'image',)
        widgets = {'detail': Textarea(attrs={'cols': 100, 'rows': 10}),}

