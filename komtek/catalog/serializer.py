from rest_framework import serializers
from .models import Handbook, Element, HandbookVersion


class HandbookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handbook
        fields = '__all__'


class ElementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('id', 'code', 'value')


class HandbookVersionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandbookVersion
        fields = '__all__'
