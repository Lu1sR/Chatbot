from chatbot.model_chatbot import *
from chatbot.preprocessor import *
import os.path
from os import path
import sys
import pandas as pd

a=[]
b=[]
train_x=[]
train_y=[]
labels=[]
words=[]

a,b=procesar()
train_x=a[0]
train_y=a[1]
labels=b[0]
words=b[1]
    
if path.exists("model/model.h5"):
    
    print(train_x)
    print("\n\n\n",train_y)
    model = load_model('model/model.h5')
    model._make_predict_function()
    print("modelo cargado")

else:
    create_model()
    model = load_model('model/model.h5')
    model._make_predict_function()
    print("modelo guardado y cargado")
    

def init_bot():
    create_model()
    print("modelo guardado y cargado")

def clasificar(msg):
    ERROR_THRESHOLD = 0.25
    input_data = pd.DataFrame([bag_of_words(msg, words)], dtype=float, index=['input'])
    results = model.predict([input_data[0:1]])[0]
    print(results)
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((labels[r[0]], str(r[1])))
        print(return_list)
    
    return return_list

def chat(msg):
    results = clasificar(msg)
    if results:
        while results:
            for i in data["intents"]:
                if i["tag"] == results[0][0]:
                        if(float(results[0][1])<0.75):
                            return "Aun no estoy entrenado para responder esa pregunta"
                        return random.choice(i["responses"])
   
    