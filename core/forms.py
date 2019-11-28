from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db.models import Q
from django.utils import timezone

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

    url = forms.URLField(
        max_length=200,
        initial="https://",
        help_text="Please enter the URL of the site." "",
        label="Site URL",
    )

    class Meta:
        model = Site
        widgets = {"deadline": DateInput()}
        unique_together = ("user", "url")
        fields = ("category", "url", "deadline")

    def __init__(self, user=None, *args, **kwargs):
        if user:
            self.user = user
        super().__init__(*args, **kwargs)

    def clean_url(self):
        url = self.cleaned_data["url"]
        if Site.objects.filter(Q(user=self.user) & Q(url=url)):
            raise ValidationError("URL already present in the database")
        return url

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.localtime(timezone.now()):
            raise ValidationError("Not a valid deadline.")
        return deadline


class SiteEditForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        help_text="Pick the category of the site.",
        empty_label="All",
        label="",
    )

    class Meta:
        model = Site
        widgets = {"deadline": DateInput()}
        unique_together = ("user", "url")
        fields = ("category", "url", "deadline")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["url"].disabled = True

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.localtime(timezone.now()):
            raise ValidationError("Not a valid deadline.")
        return deadline


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Add a category")

    class Meta:
        model = Category
        fields = ("name",)

    def __init__(self, user=None, *args, **kwargs):
        if user:
            self.user = user
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Category.objects.filter(Q(user=self.user) & Q(name=name)):
            raise ValidationError("Name already present in the database")
        return name

