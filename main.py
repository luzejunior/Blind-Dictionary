from Lexical.Lexical import Lexical

def main():
    lexical = Lexical()
    while True:
        palavra = input("Digite uma frase: ")
        if palavra == "exit":
            break
        lexical.analize_phrase(palavra)
        print (lexical.dictionary)

if __name__ == "__main__":
    main()
