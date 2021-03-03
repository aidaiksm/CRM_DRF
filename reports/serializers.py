from rest_framework import serializers

from flights.serializers import FlightSerializer
from .models import *



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'feedback', 'created', 'updated', 'report')

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        comment = Comment.objects.create(**validated_data)
        return comment


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'created_at', 'flight_num', 'body', 'suggestions', 'image', 'evaluation')

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        report = Report.objects.create(**validated_data)
        return report

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comment'] = CommentSerializer(instance.comment.all(), many=True).data
        return representation


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'