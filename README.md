# Speech to Text Python command

Simple command line tool to create text transcripts out of audio files using [IBM Watson Speech to Text](https://www.ibm.com/watson/developercloud/speech-to-text.html).

## Install

```bash
$ git clone https://github.com/rmotr/speech-to-text
$ mkvirtualenv speech-to-text
$ pip install -r requirements.txt
```

## Usage

The first thing you'll need to do is **get your Bluemix Username and Password**. This is a tedious process and we're writing a blog post that will describe it. Once you have your username and password you can do:

```bash
python main.py -u <MY-USERNAME> -p <MY-PASSWORD> -f html -i <AUDIO-FILE> transcript.html
```

_(You can omit the password option and you'll be prompted to type it in a secure manner.)_

The `-i` option receives the audio file that you want to transcript, and it'll store the text in `transcript.html` in HTML format. To select a different format, see below..

## Formatters

There are currently 4 formatters builtin: `html` (default), `markdown`, `json`, `original`. You can pass the `-f` option with any of those formatters in place.

## Examples

Under the `examples/` directory you can find a short audio file containing the first 30 seconds of [Jacob Kaplan-Moss Keynote from Pycon 2015](https://www.youtube.com/watch?v=hIJdFxYlEKE). There are also the end results of the transcription (_html_ and _markdown_ format).

#### Documentation

https://www.ibm.com/watson/developercloud/speech-to-text/api/v1/#recognize_sessionless_nonmp12

File types supported:

* audio/flac
* audio/l16
* audio/wav
* audio/ogg;codecs=opus
* audio/mulaw
