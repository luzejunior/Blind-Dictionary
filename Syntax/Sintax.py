from Model.Token import *
from Utils.Logger import Logger
WORD = 0
CLASSIFICATION = 1
LINE = 2
MARK = '$'
TOP = -1
SUBTOP = -2
NUMBER = 'Number'
TENSE = 'Tense'
PERSON = 'Person'
class Syntax:

    def __init__(self, lexical_input=[Token()]):
        self._lexical_input = []
        for lexical_entry in lexical_input:
            self._lexical_input.append(Token(lexical_entry))
        self._lexical_input = self._lexical_input[::-1]

        self.success = False
        self._last_read = Token()
        self._logger = Logger('SyntaxAnalyzer').get_logger()

    def _show_error(self, token=Token(), error_msg=''):
        tk = token
        if not token:
            tk = self._last_read
        self._logger.error('Token_read: ' + tk.get_token() + '. ' + error_msg)

    def _is_list_empty(self):
        return len(self._lexical_input) == 0

    def _get_next_token(self, pop=True):
        if len(self._lexical_input) == 0:
            return None
        if pop:
            self._last_read = self._lexical_input[-1]
            return self._lexical_input.pop()

        else:
            return self._lexical_input[-1]

    def _get_last_token_read(self):
        return self._last_read

    def _noun_validation(self, pronoun_token, noun_token):
        if pronoun_token.get_classification(PRONOUN).get_feature(NUMBER) == noun_token.get_classification(NOUN).get_feature(NUMBER):
            return True
        else:
            return False

    def _match_lexical_category(self, token, expected_category):
        if token.get_classification(expected_category):
            return True
        else:
            return False

    def start(self):
        # print(self._lexical_input)
        self._logger.info('Initiating syntax analysis.')
        self._program_routine()
        if self.success:
            self._logger.info('Your program syntax is correct.')

    def _program_routine(self):
        if self._sentence_routine():

            token = self._get_next_token()
            if (not token) or (token and not self._match_lexical_category(token, DOT)):
                self._show_error(token, 'Missing expected period.')

            if self._is_list_empty:
                self.success = True

    def _sentence_routine(self):
        if self._sintagma_nominal_routine():
            # if self._sintagma_verbal_routine():
            #     return True
            # else:
            #     self._show_error()
            #     return False
            return True
        else:
            self._show_error()
            return False

    def _sintagma_nominal_routine(self):
        if self._is_list_empty():
            return False
        token = self._get_next_token()
        if self._match_lexical_category(token, DETERMINER):
            self._logger.info('Determiner has been read. Token: ' + token.get_token() + '.')

            if self._is_list_empty():
                return False
            token = self._get_next_token()

            if not self._match_lexical_category(token, NOUN):
                self._show_error(token, 'Missing expected Noun.')
                return False
            self._logger.info('Noun has been read. Token: ' + token.get_token() + '.')

        elif self._match_lexical_category(token, PRONOUN):
            self._logger.info('Pronoun has been read. Token: ' + token.get_token() + '.')
            if self._is_list_empty():
                return False
            token_aux = self._get_next_token(pop=False)

            if self._match_lexical_category(token_aux, NOUN):
                self._logger.info('Noun has been read right after Pronoun. Checking Agreement.  Tokens: ' + token.get_token() + ' and ' + token_aux.get_token() + '.')
                self._get_next_token()
                if self._noun_validation(token, token_aux):
                    self._logger.info('Pronoun and Noun match in agreement.')
                    return True
                self._show_error(token, 'Pronoun and Noun don\'t match in agreement.')
                return False

        elif not self._match_lexical_category(token, NOUN):
            self._show_error(token, 'Missing expected Noun.')
            return False
        else:
            self._logger.info('Noun has been read. Token: ' + token.get_token() + '.')

        return True

    def _sintagma_verbal_routine(self):
        if self._is_list_empty():
            return False
        token = self._get_next_token()

        if not self._match_lexical_category(token, VERB):
            self._show_error()
            return False
        else:
            return self._phrase_construction()

    def _phrase_construction(self):
        if self._is_list_empty():
            return False
        token = self._get_next_token(pop=False)

        result = True
        result = self._preposition_construction()
        if not result:
            return result
        result = self._adverb_construction()
        if not result:
            return result
        result = self._adjective_construction()
        if not result:
            return result
        if self._match_lexical_category(token, NOUN) or self._match_lexical_category(token, PRONOUN):
            self._get_next_token()

        return True

    def _preposition_construction(self):
        token = self._get_next_token(pop=False)
        if self._match_lexical_category(token, PREPOSITION):
            self._get_next_token()

            if self._is_list_empty():
                return False
            token = self._get_next_token()

            if not (self._match_lexical_category(token, NOUN) or self._match_lexical_category(token, VERB)):
                self._show_error()
                return False
        return True

    def _adverb_construction(self):
        token = self._get_next_token(pop=False)

        if token.get_token() == NOT:
            self._get_next_token()

            if self._is_list_empty():
                return False
            token = self._get_next_token()

            if not (self._match_lexical_category(token, NOUN) or self._match_lexical_category(token, ADJECTIVE)):
                self._show_error()
                return False
        elif self._match_lexical_category(token, ADVERB):
            self._get_next_token()
            return True

        self._show_error()
        return False

    def _adjective_construction(self):
        token = self._get_next_token(pop=False)
        if not self._match_lexical_category(token, ADJECTIVE):
            return True
        self._get_next_token()

        if self._is_list_empty():
            return True
        token = self._get_next_token(pop=False)
        if not self._match_lexical_category(token, ADJECTIVE):
            return True


        while not self._is_list_empty():
            token = self._get_next_token(pop=False)
            if self._match_lexical_category(token, ADJECTIVE):
                self._get_next_token()
            elif self._match_lexical_category(token, NOUN):
                self._get_next_token()
                break
            else:
                self._show_error()
                return False
        return True













