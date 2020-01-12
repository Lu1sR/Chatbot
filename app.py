from model_chatbot import *
import os.path
from os import path

def chat():
    if path.exists("model/model.tflearn.index"):
        model.load("model/model.tflearn")
        
    else:
        create_model()
    
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        if results[0][results_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            print(random.choice(responses))
        else:
            print("No logré entenderte! Trata de preguntarme otra vez")

chat()