from rest_framework import serializers
from .models import Transcription


class TranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = ['id', 'audio_file', 'transcription_text', 'created_at']
        read_only_fields = ['transcription_text', 'created_at']
