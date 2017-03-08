import json


class BaseFormatter(object):
    def format(self, data):
        raise NotImplementedError()

    def _parse(self, data):
        alternatives = (obj['alternatives'][0]
                        for obj in data['results'])
        return ({
            'transcript': obj['transcript'],
            'confidence': obj['confidence']
        } for obj in alternatives)


class BaseJsonFormatter(BaseFormatter):
    def __init__(self, indent=2):
        self.indent = indent


class OriginalJsonFormatter(BaseJsonFormatter):
    def format(self, data):
        return json.dumps(data, indent=self.indent)


class SimpleJsonFormatter(BaseJsonFormatter):
    def format(self, data):
        objects = list(self._parse(data))
        return json.dumps(objects, indent=self.indent)


class HTMLFormatter(BaseFormatter):
    def format(self, data):
        results = (obj['transcript']
                   for obj in self._parse(data))
        lines = ("{spaces}<p>{line}</p>\n".format(
            spaces=(' ' * 4), line=line) for line in results)
        return "<html>\n{}</html>".format(''.join(lines))


class MarkdownFormatter(BaseFormatter):
    def format(self, data):
        results = (obj['transcript']
                   for obj in self._parse(data))
        lines = ("{line}\n\n".format(line=line) for line in results)

        return ''.join(lines).rstrip()

FORMATTERS = {
    'html': HTMLFormatter,
    'markdown': MarkdownFormatter,
    'simple': SimpleJsonFormatter,
    'original': OriginalJsonFormatter
}


def get_formatter(formatter_name):
    return FORMATTERS[formatter_name]
