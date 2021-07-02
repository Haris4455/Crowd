from django import forms
from comment.models import Comment
from django.forms import Textarea

class CommentForm(forms.ModelForm):
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea', 'cols': 35, 'rows': 3,'position':'fixed'}), required=True)

	class Meta:
		model = Comment
		fields = ('body',)