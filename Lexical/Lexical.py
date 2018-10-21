from Requests.DictionaryJson import DictionaryJson
import re
# import nltk
from Utils.Logger import my_logger
import language_check
from stanfordcorenlp import StanfordCoreNLP
import os


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
        self._logger = my_logger('LexicalAnalyzer')
        self._nlp = StanfordCoreNLP(os.path.join(os.path.expanduser('~'), 'Hacking', 'UFPB', 'Blind-Dictionary', 'stanford-corenlp-full-2018-10-05'))
        self._lang_checker = language_check.LanguageTool('en-US')

    def _show_error(self, word, error_msg):
        self._logger.error('[WORD]: ' + word + ' | ' + error_msg)

    def analize_phrase(self, phrase):
        # matches = self._lang_checker.check(phrase)

        # print(matches)
        self._logger.info('Lexical analyzer has been initiated.')
        self._dictionary = []
        self._word_counter = 1
        tokens = re.sub(r'(\w*)([.])(\w*)', r'\1 \2 \3', phrase)
        tokens_tag = self._nlp.pos_tag(tokens)
        tokens = tokens.split()
        for i, token in enumerate(tokens):
            if self.get_misspelling_error(token):
                self._show_error(token, 'This word might have been incorrectly spelled.')
                break
            self._analize_token(token, tokens_tag[i][1])
            self._word_counter = self._word_counter + 1

    def get_misspelling_error(self, word):
        results = self._lang_checker.check(word.lower().capitalize())
        if len(results) > 0:
            for result in results:
                if result.locqualityissuetype == 'misspelling':
                    return True
        return False

    def _analize_token(self, token, lexical_class):
        self._logger.info('Analyzing token: ' + token + '.')
        result = self._dictionaryJson.generate_classification(token.lower(), lexical_class)
        self._logger.info('[Token]: ' + token + ' | [Classification]: ' + result[1] + ' [NLTK]: ' + lexical_class +' | [Features]: ' + str(result[2]))
        self._dictionary.append([token.lower(), result[1], result[2], self._word_counter])

    def get_result(self):
        return self._dictionary

