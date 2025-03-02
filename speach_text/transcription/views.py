from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from .serializers import TranscriptionSerializer
from .tasks import process_audio
from concurrent.futures import ThreadPoolExecutor
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TranscribeView(APIView):

    parser_classes = (MultiPartParser, FormParser)
    _executor = ThreadPoolExecutor(max_workers=10)
    
    @swagger_auto_schema(
        operation_description="Upload an audio file for immediate transcription",
        manual_parameters=[
            openapi.Parameter(
                'audio_file',
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='Audio file to transcribe (mp3, wav, m4a)'
            )
        ],
        responses={
            200: openapi.Response(
                description="Transcription completed successfully",
                examples={
                    "application/json": {
                        "text": "Your transcribed text will appear here"
                    }
                }
            ),
            400: "Bad Request - Invalid input data",
            413: "Request Entity Too Large - File size exceeds limit",
            503: "Service Unavailable - Maximum concurrent requests reached"
        },
        operation_summary="Transcribe audio to text"
    )
    def post(self, request):
        try:
            # Check if we can accept more requests
            if self._executor._work_queue.qsize() >= 10:
                msg = ('Maximum concurrent requests reached. '
                      'Please try again later.')
                return Response(
                    {'error': msg},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

            serializer = TranscriptionSerializer(data=request.data)
            if serializer.is_valid():
                transcription_obj = serializer.save()
                
                # Submit task to thread pool
                future = self._executor.submit(
                    process_audio,
                    transcription_obj.id
                )
                
                try:
                    # Wait for transcription with timeout
                    transcribed_text = future.result(timeout=300)
                    
                    # Update the transcription object
                    transcription_obj.transcription_text = transcribed_text
                    transcription_obj.save()
                    
                    return Response(
                        {'text': transcribed_text},
                        status=status.HTTP_200_OK
                    )
                except TimeoutError:
                    future.cancel()
                    msg = ('Transcription timeout. '
                          'File may be too large.')
                    return Response(
                        {'error': msg},
                        status=status.HTTP_408_REQUEST_TIMEOUT
                    )
                
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Transcription failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
