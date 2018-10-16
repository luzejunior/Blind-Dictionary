from Requests.DictionaryJson import DictionaryJson

class Lexical:

    def __init__(self):
        self.word_counter = 1
        self.dictionary = []
        self.dictionaryJson = DictionaryJson()
        self.artigos = ["a", "o", "as", "os", "um", "uma", "uns", "umas"]
        self.preposicao = ["ao","aos","do","dos","da","das","no","nos","na","nas","nele","neles","nela","nelas","dali","dele","deles","dela","delas","à","às","àqueles",
        "àquelas","àquilo","de","como","para","em","por","sem","com"]

    def analize_phrase(self, phrase):
        self.dictionary = []
        self.word_counter = 1
        tokens = phrase.split()
        for token in tokens:
            self.__analize_token(token)
            self.word_counter = self.word_counter + 1

    def __analize_token(self, token):
        if token in self.artigos:
            self.dictionary.append([token, "Artigo", self.word_counter])
        elif token in self.preposicao:
            self.dictionary.append([token, "Preposicao", self.word_counter])
        elif token[0].isupper():
            self.dictionary.append([token, "Substantivo", self.word_counter])
        else:
            result = self.dictionaryJson.get_definition(token)
            self.dictionary.append([result[0], result[1], self.word_counter])
