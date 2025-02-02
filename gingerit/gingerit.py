# -*- coding: utf-8 -*-
import requests

URL = 'https://services.gingersoftware.com/Ginger/correct/jsonSecured/GingerTheTextFull'  # noqa
API_KEY = '6ae0c3a0-afdc-4532-a810-82ded0054236'


class GingerIt(object):
    def __init__(self):
        self.url = URL
        self.api_key = API_KEY
        self.api_version = '2.0'
        self.lang = 'US'

    def parse(self, text):
        session = requests.Session()
        request = session.get(
            self.url,
            params={
                'lang': self.lang,
                'apiKey': self.api_key,
                'clientVersion': self.api_version,
                'text': text
            },
        )
        data = request.json()
        return self._process_data(text, data)

    @staticmethod
    def change_char(original_text, from_position, to_position, change_with):
        return original_text[:from_position] + change_with + original_text[to_position + 1:]


    @staticmethod
    def _process_data(text, data):
        result = text
        corrections = []

        for suggestion in reversed(data['Corrections']):
            start = suggestion["From"]
            end = suggestion["To"]

            if suggestion['Suggestions']:
                suggest = suggestion['Suggestions'][0]
                result = GingerIt.change_char(result, start, end, suggest['Text'])

                corrections.append({
                    'text': text[start:end],
                    'correct': suggest.get('Text', None),
                    'definition': suggest.get('Definition', None)
                })
        return {'text': text, 'result': result, 'corrections': corrections}
