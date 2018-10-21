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
DOT = 'Dot'
NOT = 'not'



class Token:
    def __init__(self, token_dict=None):
        if not token_dict:
            self.__init__(token_dict=['word', {'None': 0}, [[{'None': 'None'}]], -1])
        else:
            self._token = token_dict[0]
            self._categories_index = token_dict[1]
            self._classification = []
            for i, category in enumerate(token_dict[1]):
                self._classification.append(Classification(category, token_dict[2][i]))
            self._position = token_dict[3]
            self._lenght_classification = len(self._classification)

    def get_token(self):
        return self._token

    def _get_classification_id(self, key_category):
        if not (key_category in self._categories_index):
            return None
        return self._categories_index[key_category]

    def get_classification(self, key_category):
        index = self._get_classification_id(key_category)
        if not index and index != 0:
            return None
        return self._classification[index]

    def get_all_classifications(self):
        return self._classification

    def get_position(self):
        return self._position

    def get_number_of_classification(self):
        return self._lenght_classification