from Requests.DictionaryJson import DictionaryJson

def main():
    dictionary = DictionaryJson()
    while True:
        palavra = input("Digite uma palavra: ")
        if palavra == "exit":
            break
        print (dictionary.get_definition(palavra))

if __name__ == "__main__":
    main()
