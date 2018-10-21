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
        if lexical.get_result():
            print(lexical.get_result())
            syntax = Syntax(lexical_input=lexical.get_result())
            syntax.start()
        else:
            vg.saySomething("Please write your phrase again")

if __name__ == "__main__":
    greetings = ["Hello, welcome to our visually impaired english dictionary", "You can write whatever phrase you want", "Press enter when you done typing"]
    vg.sayLotOfThings(greetings)
    main()
