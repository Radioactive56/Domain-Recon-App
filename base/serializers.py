from .models import Domain , SubDomain
from rest_framework import serializers


class Domain_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'

class SubDomain_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SubDomain
        fields = '__all__'
