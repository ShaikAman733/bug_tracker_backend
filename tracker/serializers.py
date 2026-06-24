from rest_framework import serializers
from .models import User, Project, Bug

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'designation', 'is_active']

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