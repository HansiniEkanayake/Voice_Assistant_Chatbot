import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy

class UserInteract:

    def __init__(self , sentence , wordList):
        self.sentence = sentence
        self.wordList = wordList
        self.stemmer = LancasterStemmer()


    def InputSentence(self):
        binaryWordList = [0 for _ in range(len(self.wordList))]

        sentenceWords = nltk.word_tokenize(self.sentence)
        sentenceWords = [self.stemmer.stem(root.lower()) for root in sentenceWords]

        for word in sentenceWords:
            for i , rootWord in enumerate(self.wordList):
                if rootWord == word:
                    binaryWordList[i].append(1)
                else:
                    binaryWordList[i].append(0)

        return numpy.array(binaryWordList)

