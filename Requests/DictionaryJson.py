import json
import requests
from collections import namedtuple

possible_classifications=['Verb', 'Adjective', 'Preposition', 'Noun', 'Pronoun', 'Adverb']
class DictionaryJson:
    def __init__(self):
        self.app_id = '01993288'
        self.app_key = '54200225d71891a07577574d80ac570c'
        self.language = 'en'
        self.definition_url = 'https://od-api.oxforddictionaries.com:443/api/v1/inflections/'  + self.language + '/'
        self.spelling_mistake_url = 'https://languagetool.org/api/v2/check?language=en-US&text='

    def get_definition(self, word, recursive = False):
        url_path = self.definition_url + word.lower()
        data = self.__make_request(url_path)
        features = []
        categories = []
        if data:
            lexical_entries = data['results'][0]['lexicalEntries']
            # print(data)
            if 'results' in data:
                for i in range(0, len(lexical_entries)):
                    lexical_category = lexical_entries[i]['lexicalCategory']
                    if lexical_category in possible_classifications:
                        categories.append(lexical_category)
                        if 'grammaticalFeatures' in lexical_entries[i]:
                            feats = []
                            for feature in lexical_entries[i]['grammaticalFeatures']:
                                feats.append([feature['type'], feature['text']])

                            features.append(feats)
                        else:
                            features.append([['None', 'None']])
                    else:
                        categories.append('None')
                        features.append([['None', 'None']])
                # for i in range(0,len(data['results'][0]['lexicalEntries'])):
                #     #print (i)
                #     found = False
                #     if 'grammaticalFeatures' in data['results'][0]['lexicalEntries'][i]:
                #         feature = data['results'][0]['lexicalEntries'][i]['grammaticalFeatures'][0]['text']
                #         classification = data['results'][0]['lexicalEntries'][i]['lexicalCategory']
                #         break
                #
                #     if not found:
                #         feature = ""
                #         classification = data['results'][0]['lexicalEntries'][i]['lexicalCategory']
                #else:
                #    feature = data['results'][0]['lexicalEntries'][1]['grammaticalFeatures'][0]['text']
                #    classification = data['results'][0]['lexicalEntries'][1]['lexicalCategory']
        else:
            temp_word = self.__search_similar_words(word)
            return self.get_definition(temp_word)

        return [word, categories, features]

    def __make_request(self, url):
        response = requests.get(url, headers = {'app_id' : self.app_id, 'app_key' : self.app_key})
        # print(response.text)
        try:
            # print(response.text)
            return json.loads(response.text)
            # return json.loads(response.text, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        except json.JSONDecodeError:
            return False

    def __search_similar_words(self, word):
        print("We found a spelling mistake in word: " + word)
        url_path = self.spelling_mistake_url + word
        data = self.__make_request(url_path)
        if data:
            counter = 1
            print("Did you mean: ")
            for token in data['matches'][0]['replacements']:
                print(str(counter) + " - " + token['value'])
                counter = counter + 1
            selection = input("Choose a number: ")
            return data['matches'][0]['replacements'][int(selection) - 1]['value']
