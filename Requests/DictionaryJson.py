import json
import requests

class DictionaryJson:
    def __init__(self):
        self.definition_url = "http://www.dicionario-aberto.net/search-json/"
        self.similar_url = "http://www.dicionario-aberto.net/search-json?like="

    def get_definition(self, word):
        temp_word = word
        if word[-2:] == "ou":
            word_list = list(word)
            word_list[-2:] = "ar"
            temp_word = "".join(word_list)
        elif word[-2:] == "eu":
            word_list = list(word)
            word_list[-2:] = "er"
            temp_word = "".join(word_list)

        url_path = self.definition_url + temp_word
        response = requests.get(url_path)
        data = response.json()
        if 'superEntry' in data:
            classification = self.__get_classification(data['superEntry'][0]['entry']['sense'][0]['gramGrp'])
        else:
            classification = self.__get_classification(data['entry']['sense'][0]['gramGrp'])
        return [word, classification]

    def __get_classification(self, response_class):
        if response_class == "f.":
            return "Substantivo Feminino"
        elif response_class == "m.":
            return "Substantivo Masculino"
        elif response_class == "v. t." or response_class == "v. i." or response_class == "v." :
            return "Verbo"
        elif response_class == "pron.":
            return "Pronome"
