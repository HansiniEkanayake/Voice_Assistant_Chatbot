import os
import playsound
import time
import speech_recognition 
from gtts import gTTS
from tempfile import TemporaryFile
import pyttsx3
import json
import random
#ML libaries
import nltk
#nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
from NuralModel import NuralModel

import numpy
import tensorflow
import tflearn


stemmer = LancasterStemmer()

with open("Dset.json") as DsetFile:
    Dset = json.load(DsetFile)

keyWords = []
tempKeyWords = []
labels = []
patternVals = []
patternKeys = []
identifiedSet = []
output = []

for DataBlock in Dset["intents"]:
    for Q_Pattern in DataBlock["patterns"]:
        #Words in patterns are seperated and store in KeyWords list.
        miniPatternList = nltk.word_tokenize(Q_Pattern)
        keyWords.extend(miniPatternList)
        #Patterns are add into the patternVals List.
        patternVals.append(miniPatternList)
        patternKeys.append(DataBlock["tag"])
        
        if DataBlock["tag"] not in labels:
            labels.append(DataBlock["tag"])
print(keyWords)
labels = sorted(labels)


for word in keyWords:
    if(word != "?"):
        # Stemming converts the words in keyWords list into their root words
        tempKeyWords.append(stemmer.stem(word.lower()))

#Sort the stemmed word list in alphabatic order and remove duplicates
tempKeyWords = sorted(list(set(tempKeyWords)))
keyWords = tempKeyWords

print(keyWords)

outList = [0 for _ in range(len(labels))]

for x,vals in enumerate(patternVals):
    binaryWordList = []

    words = [stemmer.stem(root) for root in vals]

    for word in keyWords:
        if word in words:
            binaryWordList.append(1)
        else:
            binaryWordList.append(0)
            
    binaryOut = outList[:]
    binaryOut[labels.index(patternKeys[x])] = 1
    
    identifiedSet.append(binaryWordList)
    output.append(binaryOut)
    
identifiedSet = numpy.array(identifiedSet)
output = numpy.array(output)



print(patternVals)
print(labels)
print(patternKeys)
print(keyWords)
model = NuralModel(identifiedSet , output)
NuralModel.AddLayers(model)





#Method for audio output using python text to speech
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
#
# text2 = "Hello"
#
# if text == "Hello":
#     print("Hello Again")