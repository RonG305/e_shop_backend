from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Role



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={
                                      'input_type': 'password'})
    role = serializers.CharField(write_only=True, required=False, default='user') 

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "password2", "role"]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("the two passords dont match")
        return data 
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        role_name = validated_data.pop('role', 'user') 
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data, password=password)
        role, created = Role.objects.get_or_create(roleName=role_name, user=user)

        return user