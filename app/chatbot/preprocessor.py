from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os.path
from os import path
import numpy as np
import random
import json

stop_words = set(stopwords.words('spanish'))
stemmer = SnowballStemmer("spanish")

properties_tags = []

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, 'intents.json')
data = json.load(open(json_url))
property_data = json.load(
    open(os.path.join(SITE_ROOT, 'properties_intents.json')))


for property_intent in property_data['intents']:
    data['intents'].append(property_intent)
    properties_tags.append(property_intent['tag'])

tokenizer = RegexpTokenizer(r'\w+')


def procesar():

    data = json.load(open(json_url))
    property_data = json.load(
        open(os.path.join(SITE_ROOT, 'properties_intents.json')))

    properties_tags.clear()
    for property_intent in property_data['intents']:
        data['intents'].append(property_intent)
        properties_tags.append(property_intent['tag'])

    words = []
    labels = []
    documents = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = tokenizer.tokenize(pattern.lower())
            words.extend(wrds)
            documents.append((wrds, intent["tag"]))
            print(wrds)
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower())
             for w in words if w not in list(stop_words)]
    words = sorted(list(set(words)))

    print("vocabulario: ", len(words), words)

    labels = sorted(labels)

    print("etiquetas:", len(labels), labels)

    training = []
    output_empty = [0] * len(labels)

    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[labels.index(doc[1])] = 1

        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    return [(train_x, train_y), (labels, words)]
