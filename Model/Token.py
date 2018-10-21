from Model.Classification import Classification
SINGULAR = 1
PLURAL = 2
NOUN = 'Noun'
VERB = 'Verb'
PREPOSITION = 'Preposition'
PRONOUN = 'Pronoun'
ADVERB = 'Adverb'
ADJECTIVE = 'Adjective'
DETERMINER = 'Determiner'
DOT = 'Period'


class Token:
    def __init__(self, token_dict=None):
        if not token_dict:
            self.__init__(token_dict=['word', 'None', {'None': 'None'}, -1])
        else:
            self._token = token_dict[0]
            self._classification = Classification(token_dict[1], token_dict[2])
            self._position = token_dict[3]

    def get_token(self):
        return self._token

    def get_classification(self):

        return self._classification

    def get_position(self):
        return self._position

