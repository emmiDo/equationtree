import json
import logging
import os
import tempfile
import urllib
from urllib.parse import urljoin, urlparse
import requests
from geosolver import settings
from geosolver.database.states import Question

__author__ = 'minjoon'

class GeoserverInterface(object):
    def __init__(self, server_url):
        self.server_url = server_url

    def download_questions(self, *args):
        """
        key='all': download all
        key=[development,test]: download dev and test
        key=[1,2,3]: download questions with id 1, 2, and 3
        :param key:
        :return:
        """
        if len(args) == 0:
            param = 'all'
        else:
            param = "+".join(str(x) for x in args)
        sub_url = "/questions/download/%s" % param
        request_url = urljoin(self.server_url, sub_url)
        print ("accessing: %s" % request_url)
        r = requests.get(request_url)
        data = json.loads(r.text, object_hook=_decode_dict)
        questions = {}
        for pair in data:
            try:
                diagram_url = pair['diagram_url']
                temp_dir = tempfile.mkdtemp()
                temp_name = os.path.basename(urlparse(diagram_url).path)
                temp_filepath = os.path.join(temp_dir, temp_name)
                urllib.request.urlretrieve(diagram_url, temp_filepath)
                choices = {int(key): pair['choices'][key] for key in pair['choices']}
                words = {int(index): {int(index): word for index, word in words.items()} for index, words in pair['words'].items()}
                question = Question(pair['pk'], pair['text'], words, temp_filepath, choices)
                questions[question.key] = question
            except:
                pass
        return questions

    def download_labels(self, key="all/"):
        suburl = "/labels/download/%s" % str(key)
        request_url = urljoin(self.server_url, suburl)
        r = requests.get(request_url)
        data = json.loads(r.text, object_hook=_decode_dict)
        labels = {}
        for pair in data:
            question_pk = pair['question_pk']
            label_data = pair['label_data']
            labels[question_pk] = label_data
        return labels

    def download_semantics(self, key=None):
        param = 'all/'
        if key is None:
            param = 'all/'
            
        suburl = "/semantics/download/%s" % param
        request_url = urljoin(self.server_url, suburl)
        r = requests.get(request_url)
        data = json.loads(r.text, object_hook=_decode_dict)
        processed = {int(pk): {int(idx): {int(num): text
                                          for num, text in parses.items()}
                               for idx, parses in sentences.items()}
                     for pk, sentences in data.items()}
        return processed

    def upload_question(self, text, diagram_path, choices, answer=""):
        """

        :param str text: text describing the question
        :param str diagram_path: path to the diagram image
        :param list choices: ex. ['5', '4', '2', '3', 'Cannot be determined']
        :return:
        """
        suburl = "/questions/upload/"
        request_url = urljoin(self.server_url, suburl)
        if len(choices) > 0:
            has_choices = True
        else:
            has_choices = False
        valid = True

        # Get request
        r = requests.get(request_url)
        csrftoken = r.cookies['csrftoken']

        # Post request
        files = {'diagram': open(diagram_path, 'rb')}
        data = dict(text=text, has_choices=has_choices, answer=answer, valid=valid,
                    csrfmiddlewaretoken=csrftoken, html='false')
        cookies = dict(csrftoken=csrftoken)
        r = requests.post(request_url, files=files, data=data, cookies=cookies)
        if r.text == "-1":
            logging.error("Failed upload question: %s" %text)
            return False
        pk = r.text

        for idx, choice_text in enumerate(choices):
            result = self._upload_choice(idx+1, choice_text, pk)
            if not result:
                logging.error("Failed upload question: %s" %text)
                return False

        return True

    def _upload_choice(self, number, text, question_pk):
        '''
        Upload choice
        '''
        suburl = "/questions/upload/choice"
        request_url = urljoin(self.server_url, suburl)

        # Get request
        r = requests.get(request_url)
        csrftoken = r.cookies['csrftoken']

        # Post request
        data = dict(number=number, text=text, question=question_pk,
                    csrfmiddlewaretoken=csrftoken, html='false')
        cookies = dict(csrftoken=csrftoken)
        r = requests.post(request_url, data=data, cookies=cookies)
        if r.text == "-1":
            logging.error("Failed to upload choice %d: %s" %(number, text))
            return False
        return True


def _decode_list(data):
    rv = []
    for item in data:
        item = str(item, 'utf-8')
        
        if isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.items():
         
        if isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


