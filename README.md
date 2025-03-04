# Speech-to-Text API with Parallel Processing

A Django REST API that integrates the Faster Whisper model to transcribe audio files with support for parallel processing.

## Features

- Audio file transcription endpoint
- Support for up to 10 parallel requests
- Asynchronous processing using Celery
- API documentation with Swagger
- PostgreSQL for storing transcription results

## Tech Stack

- Django & Django REST Framework
- Faster Whisper (Speech-to-Text model)
- Celery with Redis for background processing
- PostgreSQL database
- Docker for containerization
- Swagger for API documentation

## Setup Instructions

### Using Docker (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/speech-to-text-api.git
   cd speech-to-text-api
   ```

2. Start the services using Docker Compose:
   ```
   docker-compose up
   ```

3. Access the API at `http://localhost:8000/`

4. Access Swagger documentation at `http://localhost:8000/swagger/`

### Manual Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/speech-to-text-api.git
   cd speech-to-text-api
   ```

2. activate the virtual environment and install dependencies:
   ```
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   cd speach_text
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL and create a database named `stt_db`

4. Install and start Redis server

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Start the Django development server:
   ```
   python manage.py runserver
   ```

7. Start the Celery worker in a separate terminal:
   ```
   celery -A speach_text worker --loglevel=info
   ```

8. Access the API at `http://localhost:8000/`

## API Usage

### Transcribe Audio

**Endpoint:** `POST /transcribe/`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `audio_file`: Audio file (mp3, wav, m4a)

**Response:**
```json
{
  "text": "Your transcribed text will appear here"
}
```

