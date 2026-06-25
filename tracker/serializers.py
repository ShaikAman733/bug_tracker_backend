from rest_framework import serializers
from .models import User, Project, Bug

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'designation', 'is_active', 'password']

    def validate(self, data):
        # Password mandatory sirf create pe, edit pe optional
        if self.instance is None and not data.get('password'):
            raise serializers.ValidationError(
                {'password': 'Password is required when creating a new account.'}
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = '__all__'

    def validate(self, data):
        # Validation: Due date cannot be in the past
        from datetime import date
        if 'due_date' in data and data['due_date'] and data['due_date'] < date.today():
            raise serializers.ValidationError({"due_date": "Due date cannot be in the past."})
        
        # Validation: Closed bugs must contain a resolution comment
        if data.get('status') == 'Closed' and not data.get('resolution_comment'):
            raise serializers.ValidationError({"resolution_comment": "Closed bugs must contain a resolution comment."})
        
        return data