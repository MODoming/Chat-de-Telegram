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
   git clone https://github.com/MODoming/Chat-de-Telegram.git
   cd ChatBOT-Telegram

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt

3. Configura tu clave de API de Telegram en el archivo main.py:

    ```bash
    API_KEY = "tu_clave_de_API_de_Telegram"
    
    La clave la otorga telegram cuando se configura el nuevo BOT, cada uno tiene una clave única.

## Modificaciones personalizadas:

El Chat BOT fue diseñado con un conjunto de funciones que facilitan la interacción con los usuarios de manera sencilla. Para realizar modificaciones personales, es necesario comprender cómo funciona el Chat BOT. En mi caso, he creado la variable de preguntas con un formato de diccionario. En este diccionario, coloco las preguntas genéricas y las variables que se pueden preguntar para llegar a la genérica. Se pueden agregar a gusto del programador.

En el módulo intents.json se encuentran las respuestas que busca el BOT. Ahí se agregan las posibles respuestas que se quieren otorgar a las preguntas genéricas encontradas.

Se incorporó un sistema de entrenamiento del modelo de clasificación de intenciones que permite adaptarse a diferentes contextos. Es necesario entrenar al chat con las modificaciones que se realicen. Para esto, está el módulo train.py. Lo ideal es ejecutarlo antes de poner en funcionamiento el BOT y, obligatoriamente, después de agregar preguntas y respuestas para que el chat sepa que se le está agregando contenido.

Para adaptar los mensajes del BOT a tus necesidades, puedes editar los textos que están en el archivo intents.json.

En el archivo preguntas.txt, se almacenarán las preguntas que no se encontraron para tener un registro de lo que se pregunta y el chat no obtiene respuesta. Por ejemplo, cuando se escriba "Hola", el chat responderá "¡Hola! Gracias por comunicarte". Sin embargo, si se escribe "hol" u "ola", el chat puede no entender el saludo y contestará que no entiende la pregunta, lo que hará que se guarde la pregunta "hol" u "ola" en la lista de preguntas no encontradas.

## Contribuciones
Siéntete libre de contribuir al desarrollo de este BOT. Puedes crear problemas, enviar solicitudes de extracción y sugerir mejoras.

## Notas adicionales
Este proyecto utiliza el modelo de procesamiento del lenguaje natural (NLP) para interpretar y responder a las consultas del usuario.
El BOT puede detectar preguntas predefinidas y proporcionar respuestas específicas para mejorar la experiencia del usuario.
Este proyecto fue creado como un experimento personal para aprender a programar en Python y utilizar los frameworks de Machine Learning.


Asegúrate de actualizar la información, como el enlace del repositorio, la clave de API de Telegram y cualquier otra información específica de tu proyecto. ¡Espero que esto te sea útil!
