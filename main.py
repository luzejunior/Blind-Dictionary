from Lexical.Lexical import Lexical
from Model.Token import Token
from Syntax.Sintax import Syntax

def main():
    lexical = Lexical()

    while True:
        palavra = input("Type in a phrase: ")
        if palavra == "exit":
            break
        lexical.analize_phrase(palavra)
        if lexical.get_result():
            syntax = Syntax(lexical_input=lexical.get_result())
            syntax.start()
        else:
            print('Try again...')

if __name__ == "__main__":
    main()
