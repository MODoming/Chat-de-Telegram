# librerias
import random
import tensorflow as tf
from keras.layers import Dense, Dropout
from keras.models import load_model
from keras.models import Sequential
import numpy as np
import pickle
import json
import nltk
from nltk.stem import WordNetLemmatizer

# Carga los recursos necesarios para el español
nltk.download('omw-1.4', quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)

# Utiliza el lematizador de nltk para español
lemmatizer = WordNetLemmatizer()

# inicializadores
words = []
classes = []
documents = []
ignore_words = ["?", "!"]
data_file = open("intents.json").read()
intents = json.loads(data_file)

# palabras
for intent in intents["intents"]:
    for pattern in intent["patterns"]:

        # tomar cada palabra y tokenizarla
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # agregar documentos
        documents.append((w, intent["tag"]))

        # agregar clases a nuestra lista de clases
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# lematizador
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

print(len(documents), "documents")

print(len(classes), "classes", classes)

print(len(words), "unique lemmatized words", words)


pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

# inicializador de entrenamiento
# inicializando datos de entrenamiento
training = []
output_empty = [0] * len(classes)
for doc in documents:
    # inicializando bolsa de palabras
    bag = []
    # lista de palabras tokenizadas para el patrón
    pattern_words = doc[0]
    # lematiza cada palabra - crea una palabra base, en un intento de representar palabras relacionadas
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    
# crear nuestra matriz de bolsa de palabras con 1, si se encuentra una coincidencia de palabras en el patrón actual
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # la salida es un '0' para cada etiqueta y un '1' para la etiqueta actual (para cada patrón)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])
# barajar nuestras características y convertirlas en np.array
random.shuffle(training)
training = np.array(training)
# crear listas de entrenamiento y prueba. X - patrones, Y - intenciones
train_x = list(training[:, 0])
train_y = list(training[:, 1])
print("Training data created")

# entrenamiento real
# Crear modelo - 3 capas. La primera capa 128 neuronas, la segunda capa 64 neuronas y la tercera capa de salida contiene varias neuronas
# igual al número de intentos para predecir el intento de salida con softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))
model.summary()

# Compilar modelo. El descenso de gradiente estocástico con gradiente acelerado de Nesterov da buenos resultados para este modelo
sgd = tf.keras.optimizers.legacy.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# para elegir un número óptimo de épocas de entrenamiento para evitar el ajuste insuficiente o el ajuste excesivo use una devolución de llamada de parada temprana a keras
# basado en precisión o monitoreo de pérdidas. Si la pérdida está siendo monitoreada, el entrenamiento se detiene cuando hay un
# incremento observado en los valores de pérdida. O, si se está monitoreando la precisión, el entrenamiento se detiene cuando se observa una disminución en los valores de precisión.

# de las devoluciones de llamada de importación de keras
# detención anticipada = devoluciones de llamada. Detención anticipada (monitor ="pérdida", modo ="min", paciencia = 5, restaurar_mejores_pesos = Verdadero)
# devoluciones de llamada =[parada anticipada]

# ajustando y guardando el modelo
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save("chatbot_model.h5", hist)
print("model created")

