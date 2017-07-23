from django import forms

class ImportComicForm(forms.Form):
    comics = forms.FileField()

class ReviewForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, min_length=10)

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, min_length=2)
