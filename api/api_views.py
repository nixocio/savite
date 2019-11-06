from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from api.serializers import CategorySerializer, SiteSerializer
from core.models import Category, Site, default_date

# GET Return all categories
# POST Category, URL
#
#  Return all categories


@api_view(["GET"])
def categories_list(request, format=None):
    if request.method == "GET":
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data)


@api_view(["POST"])
def create_site(request):
    if request.method == "POST":
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            Site(
                category=Category.objects.get(name=serializer.data["category"]),
                deadline=default_date(),
                image_path="123.png",
                url=serializer.data["url"],
                user=request.user,
            ).save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
