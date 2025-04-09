
from rest_framework import serializers

class ProductInputSerializer(serializers.Serializer):
    kd_product = serializers.CharField()
    nm_product = serializers.CharField()
    price = serializers.FloatField()

class ProductOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    kd_product = serializers.CharField()
    nm_product = serializers.CharField()
    price = serializers.FloatField()
