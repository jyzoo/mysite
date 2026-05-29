from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError

class NewsForm(forms.ModelForm):

    class Meta:
        model = News

        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category', 'photo']

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),

            'category': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise forms.ValidationError("Название не должно начинаться с цифры")
        return title


class CommentForm(forms.Form):
    author = forms.CharField(
        label='Автор',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    text = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5
            }
        )
    )