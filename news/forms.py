from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'head',
            'text_post',
            'author',

        ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text_post")
        if description is not None and len(description) < 20:
            raise ValidationError({
                "text_post": "Описание не может быть менее 20 символов."
            })

        name = cleaned_data.get("head")
        if name == description:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data