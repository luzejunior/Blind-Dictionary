import json
import requests
from collections import namedtuple

possible_classifications=['Verb', 'Adjective', 'Preposition', 'Noun', 'Pronoun', 'Adverb', 'Determiner']

class DictionaryJson:
    def __init__(self):
        self.app_id = '01993288'
        self.app_key = '54200225d71891a07577574d80ac570c'
        self.language = 'en'
        self.definition_url = 'https://od-api.oxforddictionaries.com:443/api/v1/inflections/'  + self.language + '/'
        self.spelling_mistake_url = 'https://languagetool.org/api/v2/check?language=en-US&text='

    def get_definition(self, word, validation_token):
        if word == '.':
            return [word, {'Dot': 0}, [[{'None': 'None'}]]]
        url_path = self.definition_url + word.lower()
        data = self.__make_request(url_path)
        features = []
        categories = dict()
        if data:

            if 'results' in data:
                lexical_entries = data['results'][0]['lexicalEntries']
                count = 0
                for i in range(0, len(lexical_entries)):
                    lexical_category = lexical_entries[i]['lexicalCategory']
                    if (lexical_category in possible_classifications) and (lexical_category == validation_token) and ( not(lexical_category in categories)):
                        categories[lexical_category] = count
                        count = count + 1
                        if 'grammaticalFeatures' in lexical_entries[i]:
                            feats = dict()
                            for feature in lexical_entries[i]['grammaticalFeatures']:
                                feats[feature['type']] = feature['text']
                                # feats.append([feature['type'], feature['text']])

                            features.append(feats)
                        else:
                            features.append([{'None': 'None'}])

                if len(categories) == 0:
                    categories['None'] = 0
                    features.append([{'None': 'None'}])
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
