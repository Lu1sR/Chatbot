from chatbot.model_chatbot import *
import os.path
from os import path
import sys



if path.exists("model/model.tflearn.index"):
    model.load("model/model.tflearn")

def init_bot():
    create_model()


def chat(msg):
    results = model.predict([bag_of_words(msg, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[0][results_index] > 0.7:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        return random.choice(responses)
    else:
        return "No logré entenderte! Trata de preguntarme otra vez"
    