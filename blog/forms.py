from django import forms

class PostForm(forms.Form):
	fields = ('content', 'text',)