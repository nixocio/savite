from django import forms

from core.models import Site, Category


class SiteForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        help_text="Please enter the Category of the Site.",
        empty_label="",
    )
    url = forms.URLField(
        max_length=200,
        help_text="Please enter the URL of the site." "",
        label="Site URL",
    )

    class Meta:
        model = Site
        fields = ("category", "url")

