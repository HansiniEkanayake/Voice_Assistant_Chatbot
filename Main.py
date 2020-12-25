import os
import playsound
import time
import speech_recognition 
from gtts import gTTS

def AudioOut(text):
    #Transfers the text to an audion file in English
    inText = gTTS(text=text , lang='en')
    voiceFile = "Answer.mp3"
    inText.save(voiceFile)
    playsound.playsound(voiceFile)
    
AudioOut("Hello Mahendra")