from __future__ import print_function

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

from  random import random

def GSO(input_number, n_neurons, fitness_value, max_iter, luci_enhancement, luci_decay, neigh_ray):
    dimension = (input_number * n_neurons) + (2 * n_neurons) + n_neurons
    
    glow_input_layer = []
    glow_hidden_layer = []
    glow_bias = []
    luciferin = {}

    luciferin['input'] = []
    luciferin['hidden'] = []
    luciferin['bias'] = []
    
    for glow_idx in range(input_number):
        glow_input_layer.append(random())
        luciferin['input'].append(0)
    
    
    for glow_idx in range(n_neurons):
        glow_hidden_layer.append(random())
        luciferin['hidden'].append(0)

        glow_bias.append(random())
        luciferin['bias'].append(0)

    t = 0

    while t < max_iter:
        print(str(t) + ' ITERATION:')
        # TO INPUT LAYER
        for glow_idx in range(input_number):
            luciferin[glow_idx] = ((1 - luci_decay) * luciferin['input'][glow_idx]) + (luci_enhancement * fitness_value)
        
        for glow_idx in range(input_number):

            neighbours = []

            for glow_i in range(input_number):

                if glow_idx != glow_i:
                    d = abs(glow_input_layer[glow_idx] - glow_input_layer[glow_i])
                    if d <= neigh_ray:
                        neighbours.append([glow_i, luciferin['input'][glow_i]])
            
            major_glow = [-1, -1]
    
            for n in neighbours:
                if n[1] > major_glow[1]:
                    major_glow = n
            
            #Movment phase
            glow_input_layer[glow_idx] += abs(glow_input_layer[glow_idx] - glow_input_layer[major_glow[0]]) / 2

        # TO HIDDEN LAYER
        for glow_idx in range(n_neurons):
            
            luciferin['hidden'][glow_idx] = ((1 - luci_decay) * luciferin['hidden'][glow_idx]) + (luci_enhancement * fitness_value)
            luciferin['bias'][glow_idx] = ((1 - luci_decay) * luciferin['bias'][glow_idx]) + (luci_enhancement * fitness_value)
        

        for glow_idx in range(n_neurons):

            neighbours = []

            for glow_i in range(n_neurons):

                if glow_idx != glow_i:
                    d = abs(glow_hidden_layer[glow_idx] - glow_hidden_layer[glow_i])
                    if d <= neigh_ray:
                        neighbours.append([glow_i, luciferin['hidden'][glow_i]])
            

            major_glow = [-1, -1]
    
            for n in neighbours:
                if n[1] > major_glow[1]:
                    major_glow = n

            #Movment phase
            glow_hidden_layer[glow_idx] += abs(glow_hidden_layer[glow_idx] - glow_hidden_layer[major_glow[0]]) / 2

        t += 1
    return glow_input_layer, glow_hidden_layer, glow_bias


if __name__ == "__main__":
    
    batch_size = 128
    num_classes = 10
    epochs = 1

    INPUT_NUMBER = 784
    N_NEURONS = 512

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(60000, INPUT_NUMBER)
    x_test = x_test.reshape(10000, INPUT_NUMBER)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)


    model = Sequential()
    model.add(Dense(N_NEURONS, activation='relu', input_shape=(INPUT_NUMBER,)))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy',
                optimizer=RMSprop(),
                metrics=['accuracy'])

    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_data=(x_test, y_test))
    
    score = model.evaluate(x_test, y_test, verbose=0)

    accuracy = score[1]

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    
    input_weigth, hidden_weigth, bias = GSO(INPUT_NUMBER, N_NEURONS, score[1], 10, 0.6, 0.4, 0.2)

    model2 = Sequential()
    model2.add(Dense(N_NEURONS, activation='relu', input_shape=(INPUT_NUMBER,)))
    model2.add(Dropout(0.2))
    model2.add(Dense(num_classes, activation='softmax'))

    import numpy
    model2.summary()
    hidden_weigth = numpy.asarray(hidden_weigth)
    bias = numpy.asarray(bias)
    print('Input layer weigths:')
    print(input_weigth)