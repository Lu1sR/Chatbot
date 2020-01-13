from chatbot.model_chatbot import *
import os.path
from os import path


def init_bot():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    model_url = os.path.join(SITE_ROOT,'model/model.tflearn.index')
    if path.exists(model_url):
        model.load(model_url)
        
    else:
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
    