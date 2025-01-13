from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['user', 'event_type', 'relationship', 'gender', 'age_range']

    def validate_relationship(self, value):
        gender = self.initial_data.get('gender')  # Получаем поле gender из данных
        if gender == 'male':
            allowed_relationships = ['father', 'husband', 'son', 'grandfather', 'brother', 'friend', 'teacher',
                                     'colleague', 'other']
        elif gender == 'female':
            allowed_relationships = ['mother', 'wife', 'daughter', 'sister', 'grandmother', 'friend', 'teacher',
                                     'colleague', 'other']

        if value and value not in allowed_relationships:
            raise serializers.ValidationError(
                f"Invalid relationship for gender {gender}. Allowed values: {', '.join(allowed_relationships)}")

        return value
