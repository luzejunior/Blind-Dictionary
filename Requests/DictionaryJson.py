import json
import requests
from Utils.Logger import my_logger

verbs_list = ['VB','VBD','VBG', 'VBN', 'VBP', 'VBZ']
adverbs_list = ['RB', 'RBR', 'RBS']
adjective_list = ['JJ', 'JJR', 'JJS']
preposition_list = ['IN']
determiner = ['DT']
pronoun_list = ['PRP$', 'PRP']
noun_list = ['NN', 'NNS', 'NNP', 'NNPS']

third_person_pronoun = [['she', 'her', 'he', 'him', 'it'],['they', 'them']]
first_person_pronoun = [['i','me'],['we', 'us']]
second_person_pronoun = [['you'],['you']]
possessive_pronouns = [['my', 'your', 'his', 'her', 'its'], ['our','your', 'their']]


possible_classifications=['Verb', 'Adjective', 'Preposition', 'Noun', 'Pronoun', 'Adverb', 'Determiner']

class DictionaryJson:
    def __init__(self):
        self.app_id = '01993288'
        self.app_key = '54200225d71891a07577574d80ac570c'
        self.language = 'en'
        self.definition_url = 'https://od-api.oxforddictionaries.com:443/api/v1/inflections/'  + self.language + '/'
        self.spelling_mistake_url = 'https://languagetool.org/api/v2/check?language=en-US&text='
        self._logger = my_logger('LexicalAnalyzer')

    def _generate_noun_features(self, lexical_class):
        feature = dict()
        number = None
        if lexical_class == 'NN' or lexical_class == 'NNP':
            number = 'Singular'
        else:
            number = 'Plural'
        feature['Number'] = number

        return feature

    def _generate_verb_features(self, lexical_class):
        tense = None
        number = None
        person = None
        features = dict()
        if lexical_class == 'VBD':
            tense = 'Past'
        elif lexical_class == 'VB':
            tense = 'Present'
            person = 'non-3d'
            number = 'Singular'
        elif lexical_class == 'VBG':
            tense = 'Present'
        elif lexical_class == 'VBN':
            tense = 'Past'
        elif lexical_class == 'VBP':
            tense = 'Present'
            person = 'non-3d'
        elif lexical_class == 'VBZ':
            tense = 'Present'
            person = '3d'
            number = 'Singular'
        if tense:
            features['Tense'] = tense
        if number:
            features['Number'] = number
        if person:
            features['Person'] = person

        return features

    def _generate_adverbs_adjectives_features(self, lexical_class):
        feat = None
        features = dict()
        if lexical_class == 'RB' or lexical_class == 'JJ':
            feat = 'Standard'
        elif lexical_class == 'RBR' or lexical_class == 'JJR':
            feat = 'Comparative'
        else:
            feat = 'Superlative'

        features['Type'] = feat
        return features

    def _generate_none_features(self):
        feature = dict()
        feature['Type'] = None
        return feature

    def _generate_pronoun_features(self, word, lexical_class):
        feature = dict()
        number = None
        person = None

        if lexical_class == 'PRP':
            if word in first_person_pronoun[0] or word in first_person_pronoun[1]:
                person = 'First'
            elif word in second_person_pronoun[0] or word in second_person_pronoun[1]:
                person = 'Second'
            else:
                person = 'Third'

            if word in first_person_pronoun[0] or word in second_person_pronoun[0] or word in third_person_pronoun[0]:
                number = 'Singular'
            else:
                number = 'Plural'
        else:
            if word in possessive_pronouns[0]:
                number = 'Singular'
            else:
                number = 'Plural'

        if number:
            feature['Number'] = number
        if person:
            feature['Person'] = person

        return feature


    def generate_classification(self, word, lexical_class):
        if word == '.':
            return [word, 'Period', {'Type':None}]

        lexical_tag = None
        features = None
        if lexical_class in verbs_list:
            lexical_tag = 'Verb'
            features = self._generate_verb_features(lexical_class)
        elif lexical_class in adverbs_list:
            lexical_tag = 'Adverb'
            features = self._generate_adverbs_adjectives_features(lexical_class)
        elif lexical_class in adjective_list:
            lexical_tag = 'Adjective'
            features = self._generate_adverbs_adjectives_features(lexical_class)
        elif lexical_class in preposition_list:
            lexical_tag = 'Preposition'
            features = self._generate_none_features()
        elif lexical_class in determiner:
            lexical_tag = 'Determiner'
            features = self._generate_none_features()
        elif lexical_class in pronoun_list:
            lexical_tag = 'Pronoun'
            features = self._generate_pronoun_features(word, lexical_class)
        elif lexical_class in noun_list:
            lexical_tag = 'Noun'
            if not self._search_for_word(word):
                self._logger.error('This word wasn\'t found in the database. Token: ' + word + '.')
            features = self._generate_noun_features(lexical_class)
        else:
            lexical_tag = 'Other'
            features = self._generate_none_features()

        return[word,lexical_tag, features]

    def _search_for_word(self, word):
        url_path = self.definition_url + word.lower()
        data = self.__make_request(url_path)
        if data:
            return True
        else:
            return False
    # def get_definition(self, word, validation_token):
    #     if word == '.':
    #         return [word, {'Dot': 0}, [[{'None': 'None'}]]]
    #     url_path = self.definition_url + word.lower()
    #     data = self.__make_request(url_path)
    #     features = []
    #     categories = dict()
    #     if data:
    #
    #         if 'results' in data:
    #             lexical_entries = data['results'][0]['lexicalEntries']
    #             count = 0
    #             for i in range(0, len(lexical_entries)):
    #                 lexical_category = lexical_entries[i]['lexicalCategory']
    #                 if (lexical_category in possible_classifications) and (lexical_category == validation_token) and ( not(lexical_category in categories)):
    #                     categories[lexical_category] = count
    #                     count = count + 1
    #                     if 'grammaticalFeatures' in lexical_entries[i]:
    #                         feats = dict()
    #                         for feature in lexical_entries[i]['grammaticalFeatures']:
    #                             feats[feature['type']] = feature['text']
    #                             # feats.append([feature['type'], feature['text']])
    #
    #                         features.append(feats)
    #                     else:
    #                         features.append([{'None': 'None'}])
    #
    #             if len(categories) == 0:
    #                 categories['None'] = 0
    #                 features.append([{'None': 'None'}])
    #             # for i in range(0,len(data['results'][0]['lexicalEntries'])):
    #             #     #print (i)
    #             #     found = False
    #             #     if 'grammaticalFeatures' in data['results'][0]['lexicalEntries'][i]:
    #             #         feature = data['results'][0]['lexicalEntries'][i]['grammaticalFeatures'][0]['text']
    #             #         classification = data['results'][0]['lexicalEntries'][i]['lexicalCategory']
    #             #         break
    #             #
    #             #     if not found:
    #             #         feature = ""
    #             #         classification = data['results'][0]['lexicalEntries'][i]['lexicalCategory']
    #             #else:
    #             #    feature = data['results'][0]['lexicalEntries'][1]['grammaticalFeatures'][0]['text']
    #             #    classification = data['results'][0]['lexicalEntries'][1]['lexicalCategory']
    #     else:
    #
    #         temp_word = self.__search_similar_words(word)
    #         return self.get_definition(temp_word)
    #
    #     return [word, categories, features]

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
