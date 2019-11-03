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
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the site." "", label="Site URL")
 
    class Meta:
        model = Site
        widgets = {"deadline": DateInput()}
        unique_together = ("user", "url")
        fields = ("category", "url", "deadline")
 
    def __init__(self, user=None, *args, **kwargs):
        if user:
            self.user = user
        super(SiteForm, self).__init__(*args, **kwargs)
 
    def clean_url(self):
        url = self.cleaned_data["url"]
        query = Site.objects.filter(Q(user=self.user) & Q(url=url)).all()
        if query:
            category = Site.objects.filter(
                Q(user=self.user) & Q(url=url) & Q(category=self.cleaned_data["category"])
            ).count()
            if category:
                raise ValidationError("URL already present in the database")
        return url
 
    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        from pprint import pprint
 
        pprint(deadline)
        pprint(timezone.localtime(timezone.now()))
        if deadline < timezone.localtime(timezone.now()):
            raise ValidationError("Not a valid deadline.")
        return deadline