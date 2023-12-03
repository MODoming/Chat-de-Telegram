import random
import datetime
import numpy as np
import pickle
import json
from keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
import logging
from telegram.ext import *
#-*- coding: utf-8 -*-

name_to_display = ""
fecha_nacimiento = datetime.datetime(year=1984, month=12, day=20)
strftime = datetime.datetime.now()
edad = strftime.year - fecha_nacimiento.year - ((strftime.month, strftime.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
API_KEY = "tu_clave_de_API_de_Telegram" # Configurar la clave Token generada por Telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

# Carga los recursos necesarios para el español
nltk.download('omw-1.4', quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)

# Utiliza el lematizador de nltk para español
lemmatizer = WordNetLemmatizer()

# Lista de preguntas y posibles variantes
preguntas = {
    "Hola, ¿cómo estás?": ["¡Hola!", "hola", "¡Buenos días!"],
    "¿Cómo estás?": ["¿Como estas?", "que tal?", "¿Que tal?", "como va?"],
    "Adiós, nos vemos después": ["¡Hasta luego!", "Chau, hasta la próxima", "Nos vemos pronto", "¡Adiós!"],
    "Te agradezco por tu ayuda": ["Gracias por tu apoyo", "¡Muchas gracias!", "Aprecio tu ayuda", "Gracias por estar ahí"],
    "No entendí lo que dijiste": ["¿Podrías explicar más detalladamente?", "¿Puedes reformular eso?", "Lo siento, no comprendí"],
    "¿Qué puedes hacer por mí?": ["¿En qué áreas puedes ayudarme?", "Explícame tus funciones", "¿Cuáles son tus habilidades?", "Háblame sobre tus capacidades", "¿Que cosas podes hacer?", "en qué me podés ayudar"],
    "¿Quién eres?": ["¿Cuál es tu identidad?", "¿Puedes presentarte?", "Dime un poco sobre ti", "Quien sos", "¿Quién eres?", "quién sos?", "con quién hablo?", "queria saber quién sos"],
    "Me llamo [tu nombre]": ["Hola, mi nombre es", "Mucho gusto, me llamo", "Es un placer conocerte, mi nombre es"],
    "¿Tomas café?": ["¿Eres fanático del café?", "¿Qué opinas del café?", "¿Cuál es tu relación con el café?"],
    "Necesito un favor, ¿puedes ayudarme?": ["¿Podrías echarme una mano?", "¿Podrías hacerme un favor?", "Tengo una solicitud, ¿puedes ayudarme?", "¿Estás disponible para ayudarme con un favor?"],
    "¿Qué es la Inteligencia Artificial?": ["Explícame qué es la IA", "Háblame sobre la IA", "¿Qué significa Inteligencia Artificial?"],
    "¿Eres consciente de ti mismo?": ["¿Tienes autoconciencia?", "¿Eres consciente de lo que haces?", "¿Eres consciente como los humanos?"],
    "¿Eres sabio?": ["¿Tienes sabiduría?", "¿Posees conocimiento profundo?", "¿Eres capaz de tomar decisiones sabias?"],
    "¿En qué lenguaje estás programado?": ["¿Cuál es tu lenguaje de programación?", "¿Qué tecnología utilizas?", "¿En qué idioma funcionas?"],
    "¿Eres inmortal?": ["¿Puedes morir?", "¿Tienes una vida finita?", "¿Eres eterno?"],
    "No entiendo lo que dices": ["¿Puedes explicar de otra manera?", "Necesito más claridad en tus palabras", "No logro comprender lo que dices"],
    "¿Puedes moverte?": ["¿Tienes movimiento físico?", "¿Puedes desplazarte?", "¿Eres capaz de moverte físicamente?"],
    "¿Mienten los robots?": ["¿Pueden los robots ser deshonestos?", "¿Tienen la capacidad de mentir los robots?", "¿Los robots pueden engañar?"],
    "¿Qué es un robot de chat?": ["Explícame sobre los robots de chat", "Háblame sobre los chatbots", "¿Cómo funcionan los chatbots?"],
    "¿En qué sistemas operativos trabajas?": ["¿En qué entornos puedes operar?", "¿Qué sistemas operativos son compatibles contigo?", "Dime sobre tus plataformas de trabajo"],
    "¿Qué tipo de computadora eres?": ["Háblame sobre tu naturaleza como computadora", "¿Qué características tienes como máquina?", "Explícame cómo funcionas como computadora"],
    "¿Quién te creó?": ["Dime sobre tu creador", "Explícame sobre la persona detrás de ti", "¿Quién es responsable de desarrollarte?"],
    "¿Quién eres?": ["¿Cuál es tu identidad?", "¿Puedes presentarte?", "Dime un poco sobre ti"],
    "¿Eres un bot?": ["¿Eres un programa automatizado?", "Háblame sobre tu naturaleza como bot", "¿Eres un robot virtual?", "sos un bot"],
    "¿Qué hay de nuevo?": ["¿Tienes alguna novedad?", "Cuéntame qué estás haciendo actualmente", "Háblame sobre tus últimas actualizaciones"],
    "Cuéntame un chiste": ["¿Tienes algún chiste para compartir?", "Necesito un poco de humor, ¿puedes hacerme reír?", "Dame un chiste para alegrar el día"],
    "¿Qué hora es?": ["¿Puedes decirme la hora actual?", "Necesito saber qué hora es", "Dime la hora, por favor", "Qué hora es"],
    "El clima": ["Que temperatura hay", "Cual es la temperatura actual","como va a estar el clima hoy", "y el clima"],
    "¿Qué música escuchas?": ["¿Tienes algún género musical favorito?", "Háblame sobre tus preferencias musicales", "¿Qué tipo de música te gusta?"],
    "¿Cuál es tu película favorita?": ["¿Tienes una película preferida?", "Háblame sobre tus gustos cinematográficos", "¿Qué películas disfrutas ver?"],
    "¿Te gustan los deportes?": ["¿Eres aficionado a algún deporte?", "Háblame sobre tu relación con los deportes", "¿Qué opinas sobre los eventos deportivos?"],
    "¿Juegas videojuegos?": ["¿Eres fanático de los videojuegos?", "Háblame sobre tus preferencias en juegos", "¿Tienes algún videojuego favorito?"],
    "¿Qué dato interesante me puedes dar?": ["Cuéntame algo interesante", "Dame un dato curioso", "Sorpréndeme con un hecho interesante"],
    "Eso es gracioso": ["Jajaja", "Hahahah", "Kakaka", "Muy divertido", "Muy gracioso", "Que chistoso"],
    "¿Cómo me contacto?": ["¿Cómo puedo comunicarme contigo?", "Dame tus datos de contacto", "Háblame sobre cómo puedo ponerte en contacto"],
    "Fue agradable hablar contigo": ["También disfruté de nuestra conversación", "Me alegra que hayas disfrutado la charla", "Siempre es un placer hablar contigo"],
    "Habilidades de Maximiliano": ["Cuéntame sobre las habilidades de Maximiliano", "Háblame sobre las capacidades de tu creador", "Dime qué cualidades destacan en Maximiliano"],
    "Capacitación en informática": ["que estudios tiene maximiliano?", "Háblame sobre la formación en informática de Maximiliano", "Dime sobre la educación tecnológica de tu creador", "Cuéntame acerca de los estudios informáticos de Maximiliano"],
    "Título docente": ["Explícame sobre la certificación docente de Maximiliano", "Háblame de la especialización en docencia de tu creador", "Dime sobre el título para enseñar de Maximiliano"],
    "Experiencia como docente": ["Cuéntame sobre la experiencia docente de Maximiliano", "Háblame sobre la trayectoria como profesor de tu creador", "Dime sobre la labor educativa de Maximiliano"],
    "Experiencia anterior": ["en qué se especializa?", "Háblame sobre los trabajos anteriores de Maximiliano", "Dime sobre la experiencia laboral previa de tu creador", "Cuéntame acerca de los empleos pasados de Maximiliano"],
    "Proyectos informáticos": ["Explícame sobre los proyectos informáticos de Maximiliano", "Háblame de los trabajos tecnológicos de tu creador", "Dime sobre los proyectos de software de Maximiliano"],
    "Edad": ["Que edad tienen Maximiliano", "Cuantos años tiene", "que tan viejo es maximiliano", "cuando es el cumpleaños de maximiliano?", "cuando es su cumpleaños"]
}

# Chat initialization
model = load_model("chatbot_model.h5")
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

# Funciones del chat
def clean_up_sentence(sentence): 
    """
    Limpia una oración tokenizándola y lematizándola.
    Parameters:
    - sentence (str): La oración a limpiar.
    Returns:
    - list: Lista de palabras lematizadas.
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Crea una bolsa de palabras (Bag of Words) para una oración.
def bow(sentence, words, show_details=True):
    """
    Parameters:
    - sentence (str): La oración para la cual se crea la bolsa de palabras.
    - words (list): Lista de palabras utilizadas en el modelo.
    - show_details (bool): Indica si mostrar detalles durante la creación de la bolsa.
    Returns:
    - np.array: Bolsa de palabras como un array numpy.
    """
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

# Predecir la clase (intención) de una oración utilizando el modelo.
def predict_class(sentence, model):
    """
    Parameters:
    - sentence (str): La oración para la cual predecir la clase.
    - model: El modelo de chatbot.
    Returns:
    - list: Lista de clases predichas con probabilidades asociadas.
    """
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.50
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Obtener la respuesta asociada a las intenciones predichas.
def getResponse(ints, intents_json):
    """
    Parameters:
    - ints (list): Lista de intenciones predichas.
    - intents_json: JSON con las intenciones y respuestas asociadas.
    Returns:
    - str: Respuesta del chatbot.
    """
    if len(ints) > 0:
        tag = ints[0]["intent"]
        list_of_intents = intents_json["intents"]
        for i in list_of_intents:
            if i["tag"] == tag:
                result = random.choice(i["responses"])
                break
        return result
    else:
        return "Lo siento, no entendí tu pregunta."

# Funcioón para agregar una pregunta que no se encuentra en el listado de preguntas sin responder    
def agregar_pregunta_sin_respuesta(pregunta):
    ruta_archivo = ".\preguntas.txt"
    
    # Abre el archivo en modo de anexar ('a') y utiliza un bloque 'with' para garantizar que el archivo se cierre correctamente
    with open(ruta_archivo, 'a') as archivo:
        archivo.write(pregunta.encode('latin-1').decode('utf-8') + '\n')

# Función para detectar preguntas y encontrar la pregunta correspondiente
def detectar_pregunta(texto):
    mejor_pregunta = None
    mejor_similitud = 75
    try:
        # Iterar sobre las preguntas y variantes
        for pregunta, variantes in preguntas.items():
            for variante in variantes:
                similitud = fuzz.ratio(texto.lower(), variante.lower())

                # Actualizar la pregunta y similitud si encontramos una mejor coincidencia
                if similitud > mejor_similitud:
                    mejor_pregunta = pregunta
                    mejor_similitud = similitud
        if mejor_pregunta is None:
            agregar_pregunta_sin_respuesta(texto)
            return ""
        else:
            return mejor_pregunta
    except Exception as e:
        return ""

# Maneja los mensajes enviados al BOT.
def handle_message(update, context):
    """
    Parameters:
    - update: Objeto que representa una actualización en Telegram.
    - context: Objeto que proporciona información adicional.
    Returns:
    - None
    """
    user_input = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {user_input}')

    # Bot response
    chat_response = chatear(user_input)
    if chat_response:
        # Si la respuesta del chat existe, enviarla
        update.message.reply_text(chat_response)
    else:
        # Si no hay respuesta del chat, intentar detectar una pregunta predefinida
        detected_question = detectar_pregunta(user_input)

        if detected_question:
            # Si se detecta una pregunta predefinida, enviar la respuesta predefinida
            predefined_response = preguntas[detected_question][0]
            update.message.reply_text(predefined_response.encode('latin-1').decode('utf-8'))
        else:
            # Si no se detecta una pregunta predefinida, enviar un mensaje predeterminado
            update.message.reply_text("Lo siento, no entendí tu pregunta.")

# Maneja los errores durante la ejecución del BOT.
def error(update, context):
    """
    Parameters:
    - update: Objeto que representa una actualización en Telegram.
    - context: Objeto que proporciona información adicional.
    """
    # Registra errores
    logging.error(f'Update {update} caused error {context.error}')

# Maneja el comando de inicio (/start) enviado al BOT.
def start_command(update, context):
    """
    Parameters:
    - update: Objeto que representa una actualización en Telegram.
    - context: Objeto que proporciona información adicional.
    """
    user_name = update.message.from_user.username
    full_name = update.message.from_user.full_name
    if user_name:
        name_to_display = user_name
    else:
        name_to_display = full_name

    update.message.reply_text(f"Hola {name_to_display}! Soy el bot de Maximiliano!")

# Función principal para procesar y responder a la entrada del usuario.
def chatear(user_input):
    """
    Parameters:
    - user_input (str): Entrada del usuario.
    Returns:
    - str: Respuesta del BOT.
    """
    pregunta=detectar_pregunta(user_input)
    ints = predict_class(pregunta, model)
    response = getResponse(ints, intents)
    try:
        if pregunta=="¿Qué hora es?":
            return "La hora actual es "+ datetime.datetime.now().strftime("%H:%M") +"."
        elif pregunta=="Edad":
            return f"{response.encode('latin-1').decode('utf-8')} Tiene {edad} años."
        else:
            return (response.encode('latin-1').decode('utf-8'))
    except UnicodeDecodeError:
        return response

if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True) # Inicializa el objeto Updater con la clave de la API de Telegram y habilita el uso de contexto.
    
    dp = updater.dispatcher # Obtiene el despachador para registrar manejadores.
    
    dp.add_handler(CommandHandler('start', start_command)) # Agrega un manejador para el comando '/start' que ejecuta la función start_command.

    dp.add_handler(MessageHandler(Filters.text, handle_message)) # Agrega un manejador para los mensajes de texto que ejecuta la función handle_message.

    dp.add_error_handler(error) # Registra un manejador para los errores que ejecuta la función error.

    updater.start_polling(1.0) # Inicia la recepción de actualizaciones del bot con un intervalo de 1 segundo.

    updater.idle() # Permanece en ejecución hasta que se presiona Ctrl+C o se interrumpe la ejecución.