from Lexical.Lexical import Lexical
from Model.Token import Token
from Syntax.Sintax import Syntax
import Utils.VoiceGenerator as vg

def main():
    lexical = Lexical()

    while True:
        vg.saySomething("You can write now")
        palavra = input("You can write now: ")
        if palavra == "exit":
            goodbye = ["Thanks for using our dictionary", "Hope to see you again soon!"]
            vg.sayLotOfThings(goodbye)
            break
        typed = ["You typed", palavra]
        vg.sayLotOfThings(typed)
        lexical.analize_phrase(palavra)
        print(lexical.get_result())
        syntax = Syntax(lexical_input=lexical.get_result())
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
    greetings = ["Hello, welcome to our visually impaired english dictionary", "You can write whatever phrase you want", "Press enter when you done typing"]
    vg.sayLotOfThings(greetings)
    main()
