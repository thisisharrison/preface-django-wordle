from os import name
import pdb
from django import forms
from django.forms.utils import flatatt
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from django.template import loader

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
# Define the Table Data component (widget) to use in Multi Value Widget
class MyWidget(forms.Widget):
    template_name = "wordle_app/widget_template.html"

    def render(self, name, value, attrs=None):
        super().render(name, value, attrs)
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


# Define the widget for MultiValue form to use. Otherwise, default is a single Text Input field
class AttemptMultiValueWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [MyWidget()] * 5
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
        return "".join(values).lower()


class AttemptClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop("type")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        attempt = cleaned_data.get("attempts")

        if attempt is None:
            raise forms.ValidationError(self.errors.get("attempts"))

        if len(attempt) != 5:
            raise forms.ValidationError("Word must be length of 5")

        if not Word.valid_word(attempt):
            raise forms.ValidationError(f"'{attempt}' not in word list")

        # instance referring to the Game object in creation!
        if self.type == "create":
            self.instance.word = Word.todays_word()

        if self.type == "update":
            previous = self.instance.attempts
            cleaned_data["attempts"] = previous + "," + attempt

        self.instance.tries += 1

        return cleaned_data

    class Meta:
        model = Game
        fields = ["attempts"]
        field_classes = {
            "attempts": AttemptMultiValueField,
        }


class AttemptClassFormBAD(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"
