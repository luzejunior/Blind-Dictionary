WORD = 0
CLASSIFICATION = 1
LINE = 2
MARK = '$'
TOP = -1
SUBTOP = -2
from Model.Token import *


class Syntax:
    def __init__(self, lexical_input=[Token('token',NOUN, 0, SINGULAR)]):
        self.lexical_input = lexical_input[::-1]
        self.success = False
        self._last_read = Token('token',NOUN, 0, SINGULAR)
        self._symbols_table = []
        self._symbol_arguments_table = []
        self._types_table = []
        self._current_arithmetic_op = 'none'
        self._arguments = []
        self._current_procedure = []

    def _show_error(self):
        #indicar error e limpar a entradaa

    def _is_list_empty(self):
        return len(self.lexical_input) == 0

    def _get_next_token(self, pop=True):
        if len(self.lexical_input) == 0:
            return -1
        if pop:
            self._last_read = self.lexical_input[-1]
            return self.lexical_input.pop()

        else:
            return self.lexical_input[-1]

    def _get_last_token_read(self):
        return self._last_read

    def _noun_validation(self,pronoun_token, noun_token):
        if pronoun_token.get_number() == noun_token.get_number():
            return True
        else:
            return False

    def start(self):
        # print(self.lexical_input)
        self._program_routine()
        if self.success:
            print('Your program syntax is correct.')

    def _program_routine(self):
        if self._sentence_routine():

            token = self._get_next_token()
            if (token == -1) or (not token.get_classification() == DOT):
                self._show_error()

            if self._is_list_empty:
                self.success = True



    def _sentence_routine(self):
        if self._sintagma_nominal_routine():
            if self._sintagma_verbal_routine():
                return True
            else:
                self._show_error()
                return False
        else:
            self._show_error()
            return False





    def _sintagma_nominal_routine(self):
        if self._is_list_empty():
            return False
        token = self._get_next_token()
        if token.get_classification() == DETERMINER:

            if self._is_list_empty():
                return False

            if self._is_list_empty():
                return False
            token = self._get_next_token()

            if not token.get_classification() == NOUN:
                self._show_error()
                return False

        elif token.get_classification() == PRONOUN:
            if self._is_list_empty():
                return False
            token_aux = self._get_next_token(pop=False)

            if token_aux.get_classification() == NOUN:
                self._get_next_token()
                if self._noun_validation(token, token_aux):
                    return True
                self._show_error()
                return False

        elif not token.get_classification() == NOUN:
            self._show_error()
            return False

        return True

    def _sintagma_verbal_routine(self):
        if self._is_list_empty():
            return False
        token = self._get_next_token()

        if not token.get_classification() == VERB:
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
        if token.get_classification() == NOUN or token.get_classification()==PRONOUN:
            self._get_next_token()

        return True


    def _preposition_construction(self):
        token = self._get_next_token(pop=False)
        if token.get_classification() == PREPOSITION:
            self._get_next_token()

            if self._is_list_empty():
                return False
            token = self._get_next_token()

            if not (token.get_classification() == NOUN or token.get_classification() == VERB):
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

            if not (token.get_classification() == NOUN or token.get_classification() == ADJECTIVE):
                self._show_error()
                return False
        elif token.get_classification() == ADVERB:
            self._get_next_token()
            return True

        self._show_error()
        return False

    def _adjective_construction(self):
        token = self._get_next_token(pop=False)
        if not token.get_classification() == ADJECTIVE:
            return True
        self._get_next_token()

        if self._is_list_empty():
            return True
        token = self._get_next_token(pop=False)
        if token.get_classification() != ADJECTIVE:
            return True


        while not self._is_list_empty():
            token = self._get_next_token(pop=False)
            if token.get_classification() == ADJECTIVE:
                self._get_next_token()
            elif token.get_classification() == NOUN:
                self._get_next_token()
                break
            else:
                self._show_error()
                return False
        return True













