import json
import requests

class DictionaryJson:
    def __init__(self):
        self.definition_url = "http://www.dicionario-aberto.net/search-json/"
        self.similar_url = "http://www.dicionario-aberto.net/search-json?like="

    def get_definition(self, word):
        url_path = self.definition_url + word
        data = self.__make_request(url_path)

        if data:
            if 'superEntry' in data:
                classification = self.__get_classification(data['superEntry'][0]['entry']['sense'][0]['gramGrp'])
            elif 'entry' in data:
                classification = self.__get_classification(data['entry']['sense'][0]['gramGrp'])
        else:
            if word[-2:] == "ou":
                word_list = list(word)
                word_list[-2:] = "ar"
                temp_word = "".join(word_list)
            elif word[-4:] == "ando":
                word_list = list(word)
                word_list[-4:] = "ar"
                temp_word = "".join(word_list)
            elif word[-2:] == "eu":
                word_list = list(word)
                word_list[-2:] = "er"
                temp_word = "".join(word_list)
            elif word[-4:] == "endo":
                word_list = list(word)
                word_list[-4:] = "er"
                temp_word = "".join(word_list)
            recursive = self.get_definition(temp_word)
            classification = recursive[1]

        return [word, classification]

    def __make_request(self, url):
        response = requests.get(url)
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return False

    def __get_classification(self, response_class):
        if response_class == "f.":
            return "Substantivo Feminino"
        elif response_class == "m.":
            return "Substantivo Masculino"
        elif "v." in response_class:
            return "Verbo"
        elif "pron." in response_class:
            return "Pronome"
        elif "adj." in response_class:
            return "Adjetivo"
