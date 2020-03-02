from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from core.models import Item


class ItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'price',
            'description_item',
            'discount_price',
            'category',
            'label',
            'slug',
        ]


class userSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


