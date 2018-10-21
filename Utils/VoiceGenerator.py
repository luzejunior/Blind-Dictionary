import pyttsx3

speak = pyttsx3.init()

def saySomething(something):
    speak.say(something)
    speak.runAndWait()

def sayLotOfThings(lotOfThings):
    for thing in lotOfThings:
        speak.say(thing)
    speak.runAndWait()
