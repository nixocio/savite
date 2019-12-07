from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from core.models import Category, Site


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ("id", "name")
        model = Category


class SiteSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="ID", read_only=True)
    category = serializers.CharField()
    url = serializers.URLField()

    # def validate_category(self, value):
    #     if not Category.objects.filter(name=value):
    #         raise ValidationError("Invalid Category.")
    #     return value
