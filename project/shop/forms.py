from django import forms
from captcha.fields import CaptchaField

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    captcha = CaptchaField()
