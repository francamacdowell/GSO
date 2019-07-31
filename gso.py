from __future__ import print_function

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

from  random import random

def GSO(input_number, n_neurons, n_glowworms, fitness_value, max_iter):
    dimension = (input_number * n_neurons) + (2 * n_neurons) + n_neurons
    
    glowworm_dict = {}
    luciferin = {}

    for glow_idx in range(n_glowworms):
        glowworm_dict[glow_idx]['conn_weight_input'] = random()
        glowworm_dict[glow_idx]['conn_weight_hidden'] = random()
        glowworm_dict[glow_idx]['bias'] = random()
        luciferin[glow_idx] = 0
    
    #TODO R(i,d) = r0
    t = 0
    while t < max_iter:
        for glow_idx in range(n_glowworms):
            #TODO: Luciferin update
            pass
        
        for glow_idx in range(n_glowworms):
            #TODO: Movement phase
            pass

        t += 1 



if __name__ == "__main__":
    
    batch_size = 128
    num_classes = 10
    epochs = 20

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
    model.add(Dense(N_NEURONS, activation='relu'))
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
        