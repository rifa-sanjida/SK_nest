from django import forms
from .models import Message


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body', 'attachment']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your message...'
            }),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }