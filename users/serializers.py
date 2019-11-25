from rest_framework import serializers
from .models import Employee, Role, Organization, Token, Application


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class EmployeeSerializer(serializers.ModelSerializer):
    tokens = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='key'
     )
    class Meta:
        model = Employee
        fields = ('id', 'username', 'organization', 'tokens')


class RoleSerializer(serializers.ModelSerializer):
    members = EmployeeSerializer(many=True, read_only=True)
    class Meta:
        model = Role
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    class Meta:
        model = Organization
        fields = '__all__'




class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'applicant', 'organization', 'request_type', 'accepted' )

