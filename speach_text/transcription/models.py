from django.db import models


class Transcription(models.Model):
    audio_file = models.FileField(upload_to='audios/')
    transcription_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcription {self.id}"
