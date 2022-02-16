from os import name
import pdb
from django import forms
from django.core.validators import RegexValidator

from .models import Game
from wordle_word.models import Word

# Basic Version
class AttemptForm(forms.Form):
    char0 = forms.CharField(max_length=1, required=True)
    char1 = forms.CharField(max_length=1, required=True)
    char2 = forms.CharField(max_length=1, required=True)
    char3 = forms.CharField(max_length=1, required=True)
    char4 = forms.CharField(max_length=1, required=True)

    def clean(self):
        cleaned_data = super().clean()
        char0 = cleaned_data.get("char0")
        char1 = cleaned_data.get("char1")
        char2 = cleaned_data.get("char2")
        char3 = cleaned_data.get("char3")
        char4 = cleaned_data.get("char4")

        attempt = char0 + char1 + char2 + char3 + char4

        if len(attempt) < 5:
            raise forms.ValidationError("Word must be length of 5")
        elif not Word.valid_word(attempt):
            raise forms.ValidationError(f"'{attempt}' not in word list")
        else:
            return cleaned_data


# Advanced Version
# Define the widget for MultiValue form to use. Otherwise, default is a single Text Input field
class AttemptMultiValueWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs={"max-length": 1})] * 5
        super().__init__(widgets)

    def decompress(self, value=""):
        if value:
            last_attempt = list(value)
            for i in range(5 - len(last_attempt)):
                last_attempt.append("")
            return last_attempt
        else:
            return [""] * 5


# Aggregates the logic of multiple fields that together produce a single value.
class AttemptMultiValueField(forms.fields.MultiValueField):
    widget = AttemptMultiValueWidget

    def __init__(self, *args, **kwargs):
        input_list = [forms.CharField(max_length=1, required=True)] * 5
        super(AttemptMultiValueField, self).__init__(input_list)

    def compress(self, values):
        return "".join(values).upper()


class AttemptClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop("player")
        self.type = kwargs.pop("type")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # One input has more than 1 char
        characters = cleaned_data.get("attempts")
        attempt = "".join(characters)
        if len(attempt) != 5:
            raise forms.ValidationError("Word must be length of 5")
        elif not Word.valid_word(attempt):
            raise forms.ValidationError(f"'{attempt}' not in word list")

        # instance referring to the Game object in creation!
        if self.type == "create":
            self.instance.word = Word.todays_word()

        self.instance.player = self.player
        # self.instance.word = self.word
        self.instance.tries += 1
        return cleaned_data

    class Meta:
        model = Game
        fields = ["attempts"]
        field_classes = {
            "attempts": AttemptMultiValueField,
        }
