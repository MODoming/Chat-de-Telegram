# Chat BOT de Telegram

Este proyecto consiste en un Chat BOT desarrollado en Python que funciona en la plataforma de Telegram. El BOT es capaz de mantener conversaciones simples, responder preguntas predefinidas y realizar algunas funciones básicas.

## Características

- **Conversación Interactiva:** El BOT puede mantener conversaciones simples y responder a preguntas comunes.
- **Funciones Específicas:** Ofrece funciones específicas, como proporcionar la hora actual y la edad del creador del BOT, Maximiliano.
- **Preguntas Predefinidas:** Incluye un conjunto de preguntas predefinidas y respuestas asociadas para mejorar la interactividad.

## Requisitos

- Python 3.x
- Bibliotecas requeridas: nltk, fuzzywuzzy, numpy, tensorflow, telegram, python-telegram-bot
- Se debe obtener una clave de API de Telegram para la configuración.

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/TuUsuario/ChatBOT-Telegram.git
   cd ChatBOT-Telegram

2. Instala las dependencias:

    pip install -r requirements.txt

3. Configura tu clave de API de Telegram en el archivo main.py:

    API_KEY = "tu_clave_de_API_de_Telegram"
    La clave la otorga telegram cuando se configura el nuevo BOT, cada uno tiene una clave única.

## Modificaciones personalizadas:

El chat bot fue diseñado con un conjunto de funciones que permiten interactuar con los usuarios de manera sencilla
Para realizar modificaciónes personales es necesario entender cómo funciona el chat bot. En mi caso, he creado la variable de prefuntas con un formato de Diccionario, ahi coloco las preguntas genericas y las fariables que se puede preguntar para llegar a la generica. Se pueden agregar a gusto del programador. 
En el módulo intents.json se encuentran las respuestas que busca el BOT. Ahí se agregan las posibles respuestas que se quieren otorgar a las preguntas genéricas encontradas. 
Se agregó un sistema de entrenamiento del modelo de clasificación de intenciones que permite adaptarse a diferentes contextos. Hay que entrenar al chat con las modificaciones que se realizen, para esto esta el Módulo train.py, lo ideal es ejecutarlo antes de poner en funcionamiente el BOT y si o si despues de agregar preguntas y respuestas para que el chat sepa que se le está agregando contenido.
Para adaptar los mensajes del bot a tus necesidades, puedes editar los textos que están en el archivo intents.json
En el archivo preguntas.txt se van a almacenar las preguntas que no se encontraron para tener un registro de lo que se pregunta y el chat no obtiene respuesta. Un ejemplo, cuando se escriba "Hola", el chat va a responder "¡Hola! Gracias por comunicarte", pero si se escribe "hol" u "ola" el chat puede no entender el saludo y va a contestar que no entiende la pregunta, esto hará que se guarde la pregunta "hol" u "ola" en la lista de preguntas no encontradas. 

## Contribuciones
Siéntete libre de contribuir al desarrollo de este BOT. Puedes crear problemas, enviar solicitudes de extracción y sugerir mejoras.

## Notas adicionales
Este proyecto utiliza el modelo de procesamiento del lenguaje natural (NLP) para interpretar y responder a las consultas del usuario.
El BOT puede detectar preguntas predefinidas y proporcionar respuestas específicas para mejorar la experiencia del usuario.
Este proyecto fue creado como un experimento personal para aprender a programar en Python y utilizar los frameworks de Machine Learning.

## Licencia
Este proyecto está bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.


Asegúrate de actualizar la información, como el enlace del repositorio, la clave de API de Telegram y cualquier otra información específica de tu proyecto. ¡Espero que esto te sea útil!
