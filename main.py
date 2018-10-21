from Lexical.Lexical import Lexical
from Model.Token import Token
from Syntax.Sintax import Syntax

def main():
    lexical = Lexical()

    while True:
        palavra = input("Digite uma frase: ")
        if palavra == "exit":
            break
        lexical.analize_phrase(palavra)
        print(lexical.dictionary)
        syntax = Syntax(lexical_input=lexical.dictionary)
        syntax.start()

        # Tokens = []
        # for i,word in enumerate(lexical.dictionary):
        #     print(word)
        #     Tokens.append(Token(word))
        #
        #     print(str(Tokens[i].get_token()) + str(Tokens[i].get_classification()[0].get_feature_text(1)))

        # print (lexical.dictionary)
        # for word in lexical.dictionary:
        #     print('Word: ' + word[0])
        #     for i,category in enumerate(word[1]):
        #         print('\n\nCategory: ' + category)
        #         print('Features: ')
        #         print(word[2][i])


if __name__ == "__main__":
    main()
