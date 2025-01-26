from rest_framework import serializers
from .models import Recipients


class RecipientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipients
        fields = ['id', 'user', 'relationship', 'event_type', 'gender', 'age_range', 'price']

    def validate(self, attrs):
        # Проверка на обязательность полей
        if attrs.get('gender') not in ['male', 'female']:
            raise serializers.ValidationError("Invalid gender")
        if attrs.get('age_range') not in dict(Recipients.AGE_RANGE_CHOICES):
            raise serializers.ValidationError("Invalid age range")
        return attrs
