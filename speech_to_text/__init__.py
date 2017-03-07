from watson_developer_cloud import SpeechToTextV1

from .utils import guess_mime_type

__version__ = '0.0.1'
__title__ = 'speech_to_text'
__license__ = 'MIT'
__description__ = "Speech to Text command using IBM Watson API"


def recognize_speech(username, password, audio_file_path,
                     forced_mime_type, audio_model):
    raise ValueError("Hello")
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
    with open(audio_file_path, 'rb') as audio_file:
        return stt.recognize(audio_file, **kwargs)
