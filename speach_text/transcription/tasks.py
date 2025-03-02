from celery import shared_task
from .models import Transcription
from faster_whisper import WhisperModel


model = WhisperModel("small", device="cpu")


@shared_task
def process_audio(transcription_id):
    transcription_obj = Transcription.objects.get(id=transcription_id)
    audio_path = transcription_obj.audio_file.path
    
    segments, info = model.transcribe(audio_path)
    full_text = " ".join([seg.text for seg in segments])
    
    transcription_obj.transcription_text = full_text
    transcription_obj.save()
    return full_text

