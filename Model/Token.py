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
from Model.Classification import Classification

class Token:
    def __init__(self):
        self.__init__(['word', ['None'], [[['None', 'None']]], -1])

    def __init__(self, token_dict):
        self._token = token_dict[0]
        self._classification = []
        for i, category in enumerate(token_dict[1]):
            self._classification.append(Classification(category, token_dict[2][i]))
        self._position = token_dict[3]
        self._lenght_classification = len(self._classification)




    def get_token(self):
        return self._token

    def get_classification_by_id(self, id_classification):
        if (id_classification > self._lenght_classification -1) or (id_classification < 0):
            return None
        return self._classification[id_classification]

    def get_classification(self):
        return self._classification

    def get_position(self):
        return self._position

    def get_number_of_classification(self):
        return self._lenght_classification