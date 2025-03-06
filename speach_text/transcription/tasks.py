from celery import shared_task
from .models import Transcription
from faster_whisper import WhisperModel
import torch

# Check if CUDA (GPU) is available
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

# Initialize the model with optimized settings
model = WhisperModel(
    model_size_or_path="large-v3",
    device=device,
    compute_type=compute_type,
    cpu_threads=4,
    num_workers=2,
    download_root="/app/models"
)

@shared_task
def process_audio(transcription_id):
    try:
        transcription_obj = Transcription.objects.get(id=transcription_id)
        audio_path = transcription_obj.audio_file.path
        
        # Transcribe with optimized settings
        segments, info = model.transcribe(
            audio_path,
            beam_size=5,          # Increased beam size for accuracy
            best_of=5,            # Number of candidates
            temperature=0.0,       # Focused sampling
            condition_on_previous_text=True,    # Use context
            initial_prompt="",     # Optional prompt
            vad_filter=True,      # Voice detection
            vad_parameters={
                "min_silence_duration_ms": 500,
                "threshold": 0.35
            }
        )
        
        full_text = " ".join([seg.text.strip() for seg in segments])
        transcription_obj.transcription_text = full_text
        transcription_obj.save()
        
        return full_text
        
    except (Transcription.DoesNotExist, RuntimeError):
        raise

