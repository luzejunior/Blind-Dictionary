from Requests.DictionaryJson import DictionaryJson
import re
import nltk
from Utils.Logger import Logger
from stanfordcorenlp import StanfordCoreNLP

verbs_list = ['VBD','VBG', 'VBN', 'VBP', 'VBZ']
adverbs_list = ['RB', 'RBR', 'RBS']
adjective_list = ['JJ', 'JJR', 'JJS']
preposition_list = ['IN']
determiner = ['DT']
pronoun_list = ['PRP$', 'PRP']
noun_list = ['NN', 'NNS', 'NNP', 'NNPS']


class Lexical:

    def __init__(self):
        self._word_counter = 1
        self._dictionary = []
        self._dictionaryJson = DictionaryJson()
        self._logger = Logger('LexicalAnalyzer').get_logger()
        self._nlp = s

    def analize_phrase(self, phrase):
        self._logger.info('Lexical analyzer has been initiated.')
        self._dictionary = []
        self._word_counter = 1

        tokens = re.sub(r'(\w*)([.])(\w*)', r'\1 \2 \3', phrase).split()
        tokens_tag = nltk.pos_tag(tokens)
        # tokens = phrase.split()
        for i, token in enumerate(tokens):
            self._analize_token(token, tokens_tag[i][1])
            self._word_counter = self._word_counter + 1

    def _analize_token(self, token, lexical_class):
        self._logger.info('Analyzing token: ' + token + '.')
        result = self._dictionaryJson.generate_classification(token.lower(), lexical_class)
        self._logger.info('[Token]: ' + token + ' | [Classification]: ' + result[1] + ' | [Features]: ' + str(result[2]))
        self._dictionary.append([result[0], result[1], result[2], self._word_counter])

    def get_result(self):
        return self._dictionary

