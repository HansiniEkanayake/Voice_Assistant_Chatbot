import json
import pickle
import random
#ML libaries
import nltk
#nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer

from NuralModel import NuralModel
from UserInteract import UserInteract

import numpy
from tensorflow.python.framework import ops
import tflearn



stemmer = LancasterStemmer()

with open("Dset.json") as DsetFile:
    Dset = json.load(DsetFile)

try:
    x
    with open("ProcessedData.pickle", "rb") as file:
        keyWords, labels, identifiedSet, output =  pickle.load(file)

except:
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

    with open("ProcessedData.pickle", "wb") as file:
        pickle.dump((keyWords , labels , identifiedSet , output) , file)


ops.reset_default_graph()

nuralNet = tflearn.input_data(shape=[None , len(identifiedSet[0])])
nuralNet = tflearn.fully_connected(nuralNet , 8)
nuralNet = tflearn.fully_connected(nuralNet , 8)
nuralNet = tflearn.fully_connected(nuralNet , len(output[0]) , activation="softmax")
nuralNet = tflearn.regression(nuralNet)

nuralModel = tflearn.DNN(nuralNet)

try:
    x5
    nuralModel.load("BankModel.tflearn")
except :

    nuralModel.fit(identifiedSet , output , n_epoch=1000 , batch_size=8 , show_metric=True)
    nuralModel.save("BankModel.tflearn")


def bag_of_words(s, keyWords):
    bag = [0 for _ in range(len(keyWords))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(keyWords):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = nuralModel.predict([bag_of_words(inp, keyWords)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in Dset["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        print(random.choice(responses))


chat()


# model = NuralModel(identifiedSet , output)
# nuralModel = model.AddLayers()
#
#
# userInteract = UserInteract(keyWords , labels , Dset)
# userInteract.chat(nuralModel , keyWords , labels , Dset)
