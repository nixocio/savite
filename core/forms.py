from django import forms

from core.models import Category, Site


class DateInput(forms.DateInput):
    input_type = "date"


class SiteForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        help_text="Pick the category of the site.",
        empty_label="All",
        label="",
    )
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the site." "", label="Site URL")

    class Meta:
        model = Site
        widgets = {"deadline": DateInput()}
        fields = ("category", "url", "deadline")
