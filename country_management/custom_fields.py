from django.core.exceptions import ValidationError
from markdownx.models import MarkdownxField

class CustomMarkdownxField(MarkdownxField):
    def clean(self, value, model_instance):
        # Call the superclass's clean method to maintain default behaviors
        value = super().clean(value, model_instance)
        
        # Convert both value and the search string to lowercase for case-insensitive comparison
        if "invalid url" in value.lower():
            raise ValidationError("Invalid URL detected in text.")
        
        return value
