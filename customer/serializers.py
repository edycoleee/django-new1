#/customer/serializer.py >>validation dan swagger input
from rest_framework import serializers

class CustomerInputSerializer(serializers.Serializer):
    nm_customer = serializers.CharField()
    alamat = serializers.CharField()
    email = serializers.EmailField()
    nohp = serializers.CharField()

class CustomerOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nm_customer = serializers.CharField()
    alamat = serializers.CharField()
    email = serializers.EmailField()
    nohp = serializers.CharField()