from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras import backend as k
from keras.optimizers import SGD
from app.chatbot.preprocessor import *
import tensorflow as tf
import matplotlib.pyplot as plt


global graph
graph = tf.get_default_graph()
a = []
b = []
train_x = []
train_y = []


def plot(history):
    print(history)
    plt.plot(history.history['acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('results/accuracy.png')
    plt.clf()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('results/lost.png')
    plt.clf()


def create_model():
    a, b = procesar()
    train_x = a[0]
    train_y = a[1]
    print(len(train_x))
    print("\n\n\n", len(train_y))
    with graph.as_default():
        model = Sequential()
        model.add(Dense(128, input_shape=(
            len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd, metrics=['accuracy'])
        history = model.fit(np.array(train_x), np.array(
            train_y), epochs=200, batch_size=5, verbose=1)
        history_dict = history.history
        model.save("model/model.h5")
        model.summary()
        scoresTraining = model.evaluate(np.array(train_x),np.array(train_y),verbose=1,batch_size=5)
        print("\n%s: %.2f%%" % (model.metrics_names[1], scoresTraining[1]*100))
        plot(history)


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = tokenizer.tokenize(s.lower())

    s_words = [stemmer.stem(w.lower())
               for w in s_words if w not in list(stop_words)]
    print(s_words)

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
                print("found in bag: %s" % w)

    return np.array(bag)
