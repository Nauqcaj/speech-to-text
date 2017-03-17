import os
from watson_developer_cloud import SpeechToTextV1

from .utils import guess_mime_type
from .formatters import get_formatter

__version__ = '0.0.1'
__title__ = 'speech_to_text'
__license__ = 'MIT'
__description__ = "Speech to Text command using IBM Watson API"

_4K = 1024 * 4


def chunked_upload(audio_file_path, buffer_size, callback=None):
    def _callback(data, progress, total_size):
        if callback:
            callback(data, progress, total_size)

    total_size = os.path.getsize(audio_file_path)
    progress = 0
    with open(audio_file_path, 'rb') as audio_file:
        while True:
            data = audio_file.read(buffer_size)
            progress += len(data or [])
            _callback(data, progress, total_size)
            if not data:
                break
            yield data


def recognize_speech(username, password, audio_file_path,
                     forced_mime_type, audio_model=None,
                     progress_callback=None, buffer_size=_4K):
    stt = SpeechToTextV1(username=username, password=password)
    content_type = guess_mime_type(audio_file_path, forced_mime_type)
    kwargs = {
        'content_type': content_type,
        'continuous': True,
        'timestamps': False,
        'max_alternatives': 1
    }
    if audio_model:
        kwargs['model'] = audio_model
    return stt.recognize(
        chunked_upload(audio_file_path, buffer_size, progress_callback),
        **kwargs)
