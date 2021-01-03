import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import random

class UserInteract:

    def __init__(self , wordList , lables , Dset):
        #self.sentence = sentence
        self.wordList = wordList
        self.lables = lables
        self.Dset = Dset



    def InputSentence(self , sentence , keywords):
        binaryWordList = [0 for _ in range(len(keywords))]

        sentenceWords = nltk.word_tokenize(sentence)
        sentenceWords = [stemmer.stem(root.lower()) for root in sentenceWords]

        for word in sentenceWords:
            for i , rootWord in enumerate(keywords):
                if rootWord == word:
                    binaryWordList[i] = 1
                else:
                    binaryWordList[i] = 0

        return numpy.array(binaryWordList)


    def chat(self , nuralModel , keywords , lables , Dset):
        print("Start talking with the Bot")
        while True:
            sentence = input("You : ")
            if sentence.lower() == "quit":
                break

            result = nuralModel.predict([self.InputSentence(sentence, keywords)])
            resultsIndex = numpy.argmax(result)
            tag = lables[resultsIndex]

            #if result[resultsIndex] > 0.8:
            for Dtag in Dset["intents"]:
                if Dtag["tag"] == tag:
                    response = Dtag["responses"]
            print(result)
            print(random.choice(response))
            #else:
                #print("Sorry I can't recogonize what you entered.")




