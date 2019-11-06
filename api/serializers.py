from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from core.models import Category, Site


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ("id", "name")
        model = Category


class SiteSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="ID", read_only=True)
    category = serializers.CharField()
    url = serializers.URLField()

    # def create(self, validated_data):
    #     return Site.objects.create(**validated_data)

    def validate_category(self, value):
        if not Category.objects.filter(name=value):
            raise ValidationError("Invalid Category.")
        return value


# class SiteSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     category = serializers.CharField()

# class ItemSerializer(serializers.ModelSerializer):
#     category_name = serializers.RelatedField(source='category', read_only=True)

#     class Meta:
#         model = Item
#         fields = ('id', 'name', 'category_name
