from rest_framework import serializers
from products.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    phone = serializers.IntegerField()
    role = serializers.IntegerField()
    #user = serializers.IntegerField()
    #class Meta:
    #    model = UserProfile
    #    feilds = ['phone', 'user','role']