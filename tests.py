import os
import tempfile
import mock
import json
import unittest
from click.testing import CliRunner

from speech_to_text.formatters import (
    HTMLFormatter, SimpleJsonFormatter, MarkdownFormatter)
from speech_to_text.utils import guess_mime_type
from speech_to_text.command import speech_to_text


MOCKED_AUDIO_RESULT = {
    "results": [
        {
            "alternatives": [
                {
                    "confidence": 0.803,
                    "transcript": "this is the first line of test data"
                }
            ],
            "final": True
        },
        {
            "alternatives": [
                {
                    "confidence": 0.981,
                    "transcript": "short line"
                }
            ],
            "final": True
        },
        {
            "alternatives": [
                {
                    "confidence": 0.839,
                    "transcript": "this is the last line of test data"
                }
            ],
            "final": True
        }
    ],
    "result_index": 0
}

MARKDOWN_EXPECTED_RESULT = """
this is the first line of test data

short line

this is the last line of test data
""".strip()

HTML_EXPECTED_RESULT = """
<html>
    <p>this is the first line of test data</p>
    <p>short line</p>
    <p>this is the last line of test data</p>
</html>
""".strip()
JSON_EXPECTED_RESULT_INDENT_2 = """
[
  {
    "transcript": "this is the first line of test data",
    "confidence": 0.803
  },
  {
    "transcript": "short line",
    "confidence": 0.981
  },
  {
    "transcript": "this is the last line of test data",
    "confidence": 0.839
  }
]
""".strip()

JSON_EXPECTED_RESULT_INDENT_4 = """
[
    {
        "transcript": "this is the first line of test data",
        "confidence": 0.803
    },
    {
        "transcript": "short line",
        "confidence": 0.981
    },
    {
        "transcript": "this is the last line of test data",
        "confidence": 0.839
    }
]
""".strip()


class FormattersTestCase(unittest.TestCase):
    def setUp(self):
        with open('./test_data.json', 'r') as f:
            self.data = json.load(f)

    def test_html_formatter_with_test_data(self):
        result = HTMLFormatter().format(self.data)
        self.assertEqual(result, HTML_EXPECTED_RESULT)

    def test_html_formatter_with_test_data(self):
        result = MarkdownFormatter().format(self.data)
        self.assertEqual(result, MARKDOWN_EXPECTED_RESULT)

    def test_json_formatter_with_default_indent(self):
        result = SimpleJsonFormatter().format(self.data)

        result_parsed = json.loads(result)
        expected_prased = json.loads(JSON_EXPECTED_RESULT_INDENT_2)

        self.assertEqual(result_parsed, expected_prased)

    def test_json_formatter_with_custom_indent(self):
        result = SimpleJsonFormatter(indent=4).format(self.data)

        result_parsed = json.loads(result)
        expected_prased = json.loads(JSON_EXPECTED_RESULT_INDENT_4)

        self.assertEqual(result_parsed, expected_prased)


class GuessMimeTypeTestCase(unittest.TestCase):
    def test_known_mime_types(self):
        self.assertEqual(guess_mime_type('audio.flac'), 'audio/x-flac')
        self.assertEqual(guess_mime_type('audio.wav'), 'audio/x-wav')

    def test_force_mime_type(self):
        self.assertEqual(
            guess_mime_type('audio.flac', forced_mime_type='audio/x-wav'),
            'audio/x-wav')
        self.assertEqual(
            guess_mime_type('audio.wav', forced_mime_type='audio/x-flac'),
            'audio/x-flac')


class CommandTestCase(unittest.TestCase):
    def test_command(self):
        """Simple high level test for our command. Needs improvements."""
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(mode='w+b', dir='/tmp',
                                         suffix='.flac') as audio_file:
            with mock.patch('speech_to_text.command.recognize_speech',
                            return_value=MOCKED_AUDIO_RESULT):
                result = runner.invoke(speech_to_text, [
                    '-i{}'.format(audio_file.name),
                    '-u rmotr',
                    '-p s3cret',
                    'final.html'
                ], catch_exceptions=False)

                self.assertEquals(result.output, 'Speech > Text finished.\n')
                self.assertTrue(os.path.exists('final.html'))
                with open('final.html', 'r') as f:
                    content = f.read()
                    self.assertEqual(content, HTML_EXPECTED_RESULT)
                os.remove('final.html')
