import json
import requests

class DictionaryJson:
    def __init__(self):
        self.definition_url = "http://www.dicionario-aberto.net/search-json/"
        self.similar_url = "http://www.dicionario-aberto.net/search-json?like="

    def get_definition(self, word, recursive = False):
        url_path = self.definition_url + word
        data = self.__make_request(url_path)

        if data:
            if 'superEntry' in data:
                classification = self.__get_classification(data['superEntry'][0]['entry']['sense'][0]['gramGrp'])
            elif 'entry' in data:
                classification = self.__get_classification(data['entry']['sense'][0]['gramGrp'])
        elif recursive:
            new_word = self.__search_similar_words(word)
            result = self.get_definition(new_word)
            return [new_word, result[1]]
        else:
            temp_word = word
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
            elif word[-2:] == "iu":
                word_list = list(word)
                word_list[-2:] = "ir"
                temp_word = "".join(word_list)
            elif word[-4:] == "indo":
                word_list = list(word)
                word_list[-4:] = "ir"
                temp_word = "".join(word_list)
            recursive = self.get_definition(temp_word, True)
            classification = recursive[1]

        return [word, classification]

    def __make_request(self, url):
        response = requests.get(url)
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return False

    def __search_similar_words(self, word):
        print("A palavra: " + word + " está errada")
        url_path = self.similar_url + word
        data = self.__make_request(url_path)

        if data:
            counter = 1
            print("Você quis dizer: ")
            for token in data["list"]:
                print(str(counter) + " - " + token)
                counter = counter + 1
            selection = input("Escolha um número: ")
            return data["list"][int(selection) - 1]


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
