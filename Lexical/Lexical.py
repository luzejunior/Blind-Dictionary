from Requests.DictionaryJson import DictionaryJson

class Lexical:

    def __init__(self):
        self.word_counter = 1
        self.dictionary = []
        self.dictionaryJson = DictionaryJson()

    def analize_phrase(self, phrase):
        self.dictionary = []
        self.word_counter = 1
        tokens = phrase.split()
        for token in tokens:
            self.__analize_token(token)
            self.word_counter = self.word_counter + 1

    def __analize_token(self, token):
        result = self.dictionaryJson.get_definition(token)
        self.dictionary.append([result[0], result[1], result[2], self.word_counter])
