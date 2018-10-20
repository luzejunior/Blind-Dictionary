SINGULAR = 1
PLURAL = 2
NOUN = 'Noun'
VERB = 'Verb'
PREPOSITION = 'Preposition'
PRONOUN = 'Pronoun'
ADVERB = 'Adverb'
ADJECTIVE = 'Adjective'
DETERMINER = 'Determiner'
DOT = 'Dot'
NOT = 'not'

class Token:
    def __init__(self, token, classification, position,number):
        self._token = token
        self._classification = classification
        self._position = position
        self._number = number

    def get_token(self):
        return self._token

    def get_classification(self):
        return self._classification

    def get_position(self):
        return self._position

    def get_number(self):
        return self._number