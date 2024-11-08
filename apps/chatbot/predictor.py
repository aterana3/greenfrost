import os
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import random

# Definir la ruta base relativa a este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar el archivo intents
intents_path = os.path.join(BASE_DIR, 'intents_tienda.json')
with open(intents_path, 'r', encoding='utf-8') as file:
    intents = json.load(file)

# Inicializar lematizador
lemmatizer = WordNetLemmatizer()

# Cargar las palabras y clases entrenadas
words_path = os.path.join(BASE_DIR, 'words.pkl')
classes_path = os.path.join(BASE_DIR, 'classes.pkl')

with open(words_path, 'rb') as file:
    words = pickle.load(file)

with open(classes_path, 'rb') as file:
    classes = pickle.load(file)

# Cargar el modelo de chatbot entrenado
model_path = os.path.join(BASE_DIR, 'chatbot_model.keras')
model = load_model(model_path)

def clean_up_sentence(sentence):
    """Tokeniza y lematiza la oración de entrada del usuario."""
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    """Convierte la oración de entrada en un 'bag of words' para el modelo."""
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    """Predice la clase (intención) de la oración de entrada."""
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # Ordenar por probabilidad
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]
    return return_list

def get_response(intents_list, intents_json):
    """Obtiene una respuesta de acuerdo con la intención predicha."""
    if intents_list:
        tag = intents_list[0]["intent"]
        for i in intents_json["intents"]:
            if i["tag"] == tag:
                return random.choice(i["responses"])
    return "Lo siento, no entiendo tu pregunta."

# Prueba de funcionamiento en caso de ejecutar directamente
if __name__ == "__main__":
    print("Chatbot listo para responder. Escribe 'salir' para terminar.")
    while True:
        message = input("Tú: ")
        if message.lower() == "salir":
            break
        ints = predict_class(message)
        res = get_response(ints, intents)
        print("Chatbot:", res)

