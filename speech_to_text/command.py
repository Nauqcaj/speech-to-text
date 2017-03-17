"""Main commands speech2text.

# $ speech2text -i input.mp3 -f html (default) -o output.html
# optional: content type, formatters?
"""

import click
import progressbar

from .config import SUPPORTED_AUDIO_MODELS, SUPPORTED_CONTENT_TYPES
from . import recognize_speech
from .formatters import get_formatter


@click.command()
@click.option('-i', '--input', type=click.Path(exists=True), required=True)
@click.option('-u', '--username', envvar='IBM_USERNAME', required=True)
@click.option('-p', '--password', prompt=True,
              hide_input=True, envvar='IBM_PASSWORD')
@click.option('-f', '--formatter',
              type=click.Choice(['html', 'markdown', 'json', 'original']),
              default='html')
@click.option('-c', '--content-type',
              type=click.Choice(SUPPORTED_CONTENT_TYPES), required=False)
@click.option('-m', '--audio-model',
              type=click.Choice(SUPPORTED_AUDIO_MODELS), required=False)
@click.option('--progress/--no-progress', default=True)
@click.argument('output', type=click.Path(exists=False), required=True)
def speech_to_text(input, username, password, formatter,
                   content_type, audio_model, progress, output):

    APP = {
        'progress_bar': None
    }

    def progress_callback(data, progress, total_size):
        if not data and APP['progress_bar'] is None:
            return

        if APP['progress_bar'] is None:
            click.echo("Starting Upload.")
            APP['progress_bar'] = progressbar.ProgressBar(
                maxval=total_size,
                widgets=[progressbar.Bar('=', '[', ']'), ' ',
                         progressbar.Percentage()])
            APP['progress_bar'].start()
        APP['progress_bar'].update(progress)
        if not data:
            APP['progress_bar'].finish()
            click.echo("Upload finished. Waiting for Transcript")

    _callback = progress_callback if progress else None

    result = recognize_speech(username, password, audio_file_path=input,
                              forced_mime_type=content_type,
                              audio_model=audio_model,
                              progress_callback=_callback)

    FormatterClass = get_formatter(formatter)
    formatted_output = FormatterClass().format(result)

    with open(output, 'w') as output_file:
        output_file.write(formatted_output)

    click.echo('Speech > Text finished.')
