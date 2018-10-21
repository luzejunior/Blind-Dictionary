from Requests.DictionaryJson import DictionaryJson
import re
import nltk

verbs_list = ['VBD','VBG', 'VBN', 'VBP', 'VBZ']
adverbs_list = ['RB', 'RBR', 'RBS']
adjective_list = ['JJ', 'JJR', 'JJS']
preposition_list = ['IN']
determiner = ['DT']
pronoun_list = ['PRP$', 'PRP']
noun_list = ['NN', 'NNS', 'NNP', 'NNPS']


class Lexical:

    def __init__(self):
        self.word_counter = 1
        self.dictionary = []
        self.dictionaryJson = DictionaryJson()
        self._token_validation = []

    def _change_token_name(self):
        new_list = []
        for i,token in enumerate(self._token_validation):
            lexical_class = token[1]
            if lexical_class in verbs_list:
                self._token_validation[i] = (token[0], 'Verb')
            elif lexical_class in adverbs_list:
                self._token_validation[i] = (token[0], 'Adverb')
            elif lexical_class in adjective_list:
                self._token_validation[i] = (token[0], 'Adjective')
            elif lexical_class in preposition_list:
                self._token_validation[i] = (token[0], 'Preposition')
            elif lexical_class in determiner:
                self._token_validation[i] = (token[0], 'Determiner')
            elif lexical_class in pronoun_list:
                self._token_validation[i] = (token[0], 'Pronoun')
            elif lexical_class in noun_list:
                self._token_validation[i] = (token[0], 'Noun')
            else:
                self._token_validation[i] = (token[0], 'Other')

    def analize_phrase(self, phrase):
        self.dictionary = []
        self.word_counter = 1

        tokens = re.sub(r'(\w*)([.])(\w*)', r'\1 \2 \3', phrase).split()
        self._token_validation = nltk.pos_tag(tokens)
        self._change_token_name()

        # tokens = phrase.split()
        for i, token in enumerate(tokens):
            self.__analize_token(token, i)
            self.word_counter = self.word_counter + 1

    def __analize_token(self, token, index):
        result = self.dictionaryJson.get_definition(token, self._token_validation[index][1])
        self.dictionary.append([result[0], result[1], result[2], self.word_counter])

