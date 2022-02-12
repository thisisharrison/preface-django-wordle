from os import name
import pdb
import re
from django import forms
from django.core.validators import RegexValidator

from .models import Game


class AttemptBasicForm(forms.Form):
    char0 = forms.CharField(max_length=1, required=True)
    char1 = forms.CharField(max_length=1, required=True)
    char2 = forms.CharField(max_length=1, required=True)
    char3 = forms.CharField(max_length=1, required=True)
    char4 = forms.CharField(max_length=1, required=True)


class AttemptClassForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        attempts = cleaned_data.get("attempts")

        if len(attempts) < 5:
            raise forms.ValidationError("must be length of 5")
        else:
            return cleaned_data

    class Meta:
        model = Game
        fields = [
            "attempts",
        ]


# Define the widget for MultiValue form to use. Otherwise, default is a single Text Input field
class AttemptMultiValueWidget(forms.MultiWidget):
    # def __init__(self, attrs=None):
    #     widgets = [forms.TextInput()] * 5
    #     # super().__init__(widgets, attrs)
    #     super(AttemptMultiValueWidget, self).__init__(widgets, attrs)

    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super().__init__(widgets)

    def decompress(self, value=""):
        last_attempt = list(value)
        for i in range(5 - len(last_attempt)):
            last_attempt.append(None)
        return last_attempt


# Aggregates the logic of multiple fields that together produce a single value.
class AttemptMultiValueField(forms.MultiValueField):
    widget = AttemptMultiValueWidget

    def __init__(self, *kwargs):
        input_list = [
            forms.CharField(
                max_length=1,
                required=True,
                validators=[RegexValidator(r"[a-zA-Z]$", "Enter a valid letter")],
            )
        ] * 5
        fields = tuple(input_list)
        error_messages = {"incomplete": "must be length of 5"}
        require_all_fields = True
        super(AttemptMultiValueField, self).__init__(
            fields=fields,
            error_messages=error_messages,
            require_all_fields=require_all_fields,
            *kwargs
        )

    def compress(self, data_list):
        return "".join(data_list).upper()
        # return super().compress("".join(data_list).upper())


class AttemptMultiValueForm(forms.Form):
    # attempts = AttemptMultiValueField()
    attempts = AttemptMultiValueField()

    # forms.CharField(max_length=5, widget=AttemptMultiValueWidget)
