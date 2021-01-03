import tensorflow
import tflearn


class NuralModel:
    def __init__(self , identifiedSet , output):
        self.identifiedSet = identifiedSet
        self.output = output

    def AddLayers(self):
        nuralNet = tflearn.input_data(shape=[None , len(self.identifiedSet[0])])
        nuralNet = tflearn.fully_connected(nuralNet , 8)
        nuralNet = tflearn.fully_connected(nuralNet , 8)
        nuralNet = tflearn.fully_connected(nuralNet , len(self.output[0]) , activation="softmax")
        nuralNet = tflearn.regression(nuralNet)

        nuralModel = tflearn.DNN(nuralNet)

        try:
            x
            nuralModel.load("BankModel.tflearn")
            return nuralModel
        except :

            nuralModel.fit(self.identifiedSet , self.output , n_epoch=1000 , batch_size=8 , show_metric=True)
            nuralModel.save("BankModel.tflearn")
            return nuralModel
