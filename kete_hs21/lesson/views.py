import uuid
import re
from os import path
import threading
import logging

import requests

from webvtt_utils import create_vtt_from_azure_output

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from course.models import Course, Lesson, Recording
from lesson.forms import LessonForm, RecordingForm, SlideshowForm


logger = logging.getLogger(__name__)

@login_required
def lessons(request, course_id):
    corresponding_course = get_object_or_404(Course, id=course_id)
    corresponding_lessons = Lesson.objects.filter(course=corresponding_course)
    context = {
        "recordings_url": settings.RECORDINGS_URL,
        "lessons": corresponding_lessons,
        "course": corresponding_course,
        "is_teacher": request.user.groups.filter(name="teachers").exists()
    }
    return render(request=request, template_name="lesson/lessons.html", context=context)


@login_required()
def delete(request, course_id, lesson_id, needs_redirect=False):
    obj = get_object_or_404(Lesson, id=lesson_id)
    obj.delete()
    if needs_redirect:
        return redirect(lessons)
    return redirect(lessons, course_id)


def write_uploaded_file_to_storage(upload_file, upload_name):
    with open(path.join(settings.RECORDINGS_ROOT, upload_name), 'wb+') as destination:
        for chunk in upload_file.chunks():
            destination.write(chunk)


def create_audio_track_from_video(recording_object_id):
    import subprocess
    logger.warning(f"Starting create_audio_track_from_video for recording id {recording_object_id}")
    recording = Recording.objects.get(pk=recording_object_id)
    recording.recording_audio_split_task_status = "in progress"
    recording.save()
    ffmpeg_command = [f"{settings.FFMPEG_PATH}", "-i", f"{settings.RECORDINGS_ROOT}/{recording.recording_video_archived_name}",
                      "-ar", "16000", "-b:a", "256k", "-vn", f"{settings.RECORDINGS_ROOT}/{recording.recording_audio_archived_name}"]
    ffmpeg_command_result = subprocess.run(ffmpeg_command, stderr=subprocess.DEVNULL)
    if ffmpeg_command_result.returncode != 0:
        logger.warning(f"ffmpeg failed ({ffmpeg_command}) with result {ffmpeg_command_result}")
        recording.recording_audio_split_task_status = "error"
        recording.save()
        return
    recording.recording_audio_split_task_status = "completed"
    recording.save()
    logger.info(f"Finished create_audio_track_from_video for recording id {recording_object_id}")
    translate_audio_to_text(recording_object_id=recording_object_id)


def fetch_azure_tts_api_token(tts_token_url, tts_token_key):
    headers = {
        'Ocp-Apim-Subscription-Key': tts_token_key
    }
    response = requests.post(tts_token_url, headers=headers)
    return str(response.text)


def upload_audio_data_as_blob(audio_file_path,
                              blob_name,
                              storage_account_container_url,
                              storage_account_sas_query_string):
    if not storage_account_container_url.endswith("/"):
        storage_account_container_url += "/"
    if not storage_account_sas_query_string.startswith("?"):
        storage_account_sas_query_string = "?" + storage_account_sas_query_string
    blob_url = storage_account_container_url + blob_name + storage_account_sas_query_string
    headers = {"x-ms-blob-type": "BlockBlob"}
    with open(audio_file_path, "rb") as audio_file:
        result = requests.put(url=blob_url, data=audio_file, headers=headers)
    if result.status_code > 299:
        raise ValueError(f"Failed to upload blob, status {result.status_code} ({result.text})")
    return blob_url


def initiate_speech_to_text_translation(audio_blob_url, tts_api_key):
    headers = {"Content-type": "application/json",
               "Ocp-Apim-Subscription-Key": tts_api_key}
    body = {
        "contentUrls": [
            audio_blob_url
        ],
        "properties": {
            "wordLevelTimestampsEnabled": True,
            "timeToLive": "PT1H",
            "channels": [0]
        },
        "locale": "de-DE",
        "displayName": "Speech to text"
    }
    tts_api_url = f"https://northeurope.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions"
    result = requests.post(url=tts_api_url, json=body, headers=headers)
    if result.status_code > 299:
        raise ValueError(f"Failed during speech to text translation (status {result.status_code}): {result.text}")
    transcript_url = result.json().get("self")
    logger.info(f"Transcript url is {transcript_url}")
    return transcript_url


def fetch_transcript_content(transcript_url, tts_api_key):
    #try to fetch transcript until its done or we give up ...
    from time import sleep
    run = 0
    transcript_content_url = None
    while run < 60:
        run += 1
        headers = {"Ocp-Apim-Subscription-Key": tts_api_key}
        transcription_hint_url = f"{transcript_url}/files"
        hints_result = requests.get(url=transcription_hint_url, headers=headers)
        for hint in hints_result.json().get("values"):
            if hint.get("kind") == "Transcription":
                transcript_content_url = hint.get("links").get("contentUrl")
                break
        else:
            sleep(10)
    transcript_response = requests.get(transcript_content_url)
    return transcript_response.json()

def write_transcript_to_file(transcript, transcript_file_path):
    import json
    with open(transcript_file_path, "w") as transcript_file:
        json.dump(transcript, transcript_file)

def _deprecated_fetch_via_azure_speech_to_text_api(tts_api_url, tts_api_key, audio_file_path):
    #Cant use this since azure doesnt do audio > 60 sec for this api ...
    api_parameters = {"language": "de-DE",
                      "profanity": "raw", #life is too short for censorship
                      "format": "detailed",
                      "initialSilenceTimeoutMs": "60000",
                      "endSilenceTimeoutMs": "60000"}
    try:
        bearer_token = fetch_azure_tts_api_token(tts_token_url=settings.AZURE_TTS_TOKEN_URL,
                                                 tts_token_key=tts_api_key)
    except (requests.HTTPError, requests.ConnectionError) as err:
        raise ValueError(f"Failed to authenticate with azure (cannot fetch bearer token): {err}")
    try:
        with open(audio_file_path, 'rb') as audio_file:
            response = requests.post(url=tts_api_url,
                                     data=audio_file,
                                     headers={"Content-type": "audio/wav",
                                              "Accept": "application/json",
                                              "Authorization": f"Bearer {bearer_token}"},
                                     params=api_parameters)
    except FileNotFoundError:
        raise ValueError(f"Failed to find audiofile ({audio_file_path})")
    except IOError:
        raise ValueError(f"Failed to read from audiofile ({audio_file_path})")
    except (requests.HTTPError, requests.ConnectionError) as err:
        raise ValueError(f"Failed to translate audio to text for file {audio_file_path}: {err}")
    return str(response.text)


def translate_audio_to_text(recording_object_id):
    recording = Recording.objects.get(pk=recording_object_id)
    if not recording:
        logger.warning(f"Error before audio translation: recording with id {recording_object_id} does not exist")
    recording.recording_audio_to_text_task_status = "in progress"
    recording.save()
    try:
        audio_blob_url = upload_audio_data_as_blob(audio_file_path=path.join(settings.RECORDINGS_ROOT,recording.recording_audio_archived_name),
                                                   blob_name=recording.recording_audio_archived_name,
                                                   storage_account_container_url=settings.AZURE_BLOB_CONTAINER_URL,
                                                   storage_account_sas_query_string=settings.AZURE_STORAGE_ACCOUNT_SAS_QUERY_STRING)
    except ValueError as err:
        logger.warning(f"Error during audio file upload to blobstore: {err}")
        recording.recording_audio_to_text_task_status = "error"
        return
    transcript_url = initiate_speech_to_text_translation(audio_blob_url=audio_blob_url, tts_api_key=settings.AZURE_OCP_APIM_SUBSCRIPTION_KEY)
    transcript_content = fetch_transcript_content(transcript_url=transcript_url, tts_api_key=settings.AZURE_OCP_APIM_SUBSCRIPTION_KEY)
    logger.info(f"Successfully translated audio for recording id {recording_object_id} (lesson: {recording.lesson.id})")
    transcript_file_path = path.join(settings.RECORDINGS_ROOT, recording.recording_text_archived_name)
    try:
        create_vtt_from_azure_output(transcript_content, transcript_file_path)
    except IOError:
        logger.warning(f"Failed to write translated text to file {transcript_file_path}")
        recording.recording_audio_to_text_task_status = "error"
    else:
        recording.recording_audio_to_text_task_status = "completed"
    recording.save()


def run_background_task(task_function, *args, **kwargs):
    logger.info(f"Starting background task")
    t = threading.Thread(target=task_function,args=args,kwargs=kwargs)
    t.setDaemon(True)
    t.start()

@login_required
def create(request, course_id):
    corresponding_course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        lesson_form = LessonForm(request.POST)
        recording_form = RecordingForm(request.POST)
        slideshow_form = SlideshowForm(request.POST)
        if lesson_form.is_valid():
            lesson_formdata = lesson_form.save(commit=False)
            lesson_formdata.created_by = request.user.profile
            lesson_formdata.course_id = corresponding_course.id
            lesson_formdata.save()
            lesson_form.save_m2m()
            messages.success(request, 'Lektion gespeichert.')
            if recording_form.is_valid():
                if recording_form.cleaned_data["recording_name"]:
                    filename_without_filetype = str(uuid.uuid4()) + "_" + \
                               "".join([c for c in recording_form.cleaned_data["recording_name"] if re.match(r'\w', c)])
                    filename_full = filename_without_filetype + "." + str(request.FILES['recording_file']).split(".")[-1]
                    write_uploaded_file_to_storage(request.FILES['recording_file'], filename_full)
                    recording_formdata = recording_form.save(commit=False)
                    recording_formdata.lesson_id = lesson_formdata.id
                    recording_formdata.recording_video_archived_name = filename_full
                    recording_formdata.recording_audio_archived_name = filename_without_filetype + ".wav"
                    recording_formdata.recording_text_archived_name = filename_without_filetype + ".vtt"
                    recording_formdata.save()
                    run_background_task(create_audio_track_from_video, recording_formdata.id)
        else:
            messages.error(request, 'Fehler beim Speichern der Lektion.')
        return redirect(lessons, course_id)
    lesson_form = LessonForm()
    recording_form = RecordingForm()
    slideshow_form = SlideshowForm()
    return render(request=request, template_name="lesson/create.html", context={'lesson_form': lesson_form,
                                                                                "recording_form": recording_form,
                                                                                "slideshow_form": slideshow_form,
                                                                                'course': corresponding_course})
