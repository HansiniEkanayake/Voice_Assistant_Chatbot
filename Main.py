import os
import playsound
import time
import speech_recognition 
from gtts import gTTS
from tempfile import TemporaryFile
import pyttsx3



def AudioOut(text):
    #Transfers the text to an audion file in English using gTTS
    #inText = gTTS(text=text , lang='en')
    ##voiceFile = "Answer.mp3"
    ##inText.save(voiceFile)
    ##playsound.playsound(voiceFile)

    #Using Tempory File
    #file = TemporaryFile()
    #inText.write_to_fp(file)
    #playsound(file)
    #file.close()

    #Using pyttsx3

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate' , 110)
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def AudioIn():
    recognizer = speech_recognition.Recognizer()

    ##Aquire and release the microphone(equals to try and finally)
    with speech_recognition.Microphone() as micIn:
        recognizer.adjust_for_ambient_noise(micIn)
        print("Say Something")
        audio = recognizer.listen(micIn)
        print("Started to listen")
        userWords = ""

        try:
            userWords = recognizer.recognize_google(audio , language='en-IN' )
            print(userWords)
        except  Exception as ex:
            print("Exception Occoured " + ex)

    return userWords


#AudioOut("Hello! How are you")

text = AudioIn()
#
# text2 = "Hello"
#
# if text == "Hello":
#     print("Hello Again")