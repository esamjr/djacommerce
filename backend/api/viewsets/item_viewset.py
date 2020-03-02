from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import viewsets, status

from api.serializers import ItemsSerializer

from core.models import Item
from django.contrib.auth.models import User


class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemsSerializer
