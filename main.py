
import random
import re
import unicodedata
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

# Configuración del juego
DURACION = 5
FRECUENCIA = 44100
puntos = 100

# Preguntas y traducciones aceptadas
preguntas = [
    # 1-10: Saludos y presentaciones
    ("en", "Hello, how are you?", ["hola como estas"]),
    ("en", "Good morning", ["buenos dias"]),
    ("en", "Good night", ["buenas noches"]),
    ("en", "My name is Lucas", ["mi nombre es lucas", "me llamo lucas"]),
    ("en", "Nice to meet you", ["encantado de conocerte", "mucho gusto"]),
    ("es", "¿Cómo te llamas?", ["what is your name", "whats your name"]),
    ("es", "Mucho gusto", ["nice to meet you"]),
    ("es", "Hasta mañana", ["see you tomorrow"]),
    ("es", "¿De dónde eres?", ["where are you from"]),
    ("es", "Estoy muy bien", ["i am very well", "im very well"]),

    # 11-20: Familia y personas
    ("en", "My brother is tall", ["mi hermano es alto"]),
    ("en", "I live with my family", ["vivo con mi familia"]),
    ("en", "My mother is a teacher", ["mi madre es profesora", "mi mama es profesora"]),
    ("en", "I have two sisters", ["tengo dos hermanas"]),
    ("en", "This is my best friend", ["este es mi mejor amigo", "esta es mi mejor amiga"]),
    ("es", "Mi padre trabaja mucho", ["my father works a lot", "my dad works a lot"]),
    ("es", "Tengo un hermano menor", ["i have a younger brother"]),
    ("es", "Mi familia es muy grande", ["my family is very big", "my family is very large"]),
    ("es", "Ella es mi prima", ["she is my cousin"]),
    ("es", "Él es mi mejor amigo", ["he is my best friend"]),

    # 21-30: Escuela y estudio
    ("en", "I go to school every day", ["voy a la escuela todos los dias"]),
    ("en", "My favorite subject is math", ["mi materia favorita es matematicas"]),
    ("en", "I have homework today", ["tengo tarea hoy"]),
    ("en", "The teacher is very nice", ["el profesor es muy amable", "la profesora es muy amable"]),
    ("en", "Where is my notebook?", ["donde esta mi cuaderno"]),
    ("es", "Tengo un examen mañana", ["i have a test tomorrow", "i have an exam tomorrow"]),
    ("es", "Me gusta aprender inglés", ["i like learning english", "i like to learn english"]),
    ("es", "La clase empieza a las ocho", ["the class starts at eight"]),
    ("es", "Necesito un lápiz", ["i need a pencil"]),
    ("es", "No entiendo la pregunta", ["i dont understand the question", "i do not understand the question"]),

    # 31-40: Comida y bebida
    ("en", "I am hungry", ["tengo hambre"]),
    ("en", "I would like a glass of water", ["quisiera un vaso de agua", "me gustaria un vaso de agua"]),
    ("en", "My favorite food is pizza", ["mi comida favorita es la pizza"]),
    ("en", "Can I have the menu, please?", ["me puedes traer el menu por favor", "puedo ver el menu por favor"]),
    ("en", "The food is delicious", ["la comida esta deliciosa", "la comida es deliciosa"]),
    ("es", "Quiero comer una manzana", ["i want to eat an apple"]),
    ("es", "Tengo mucha sed", ["i am very thirsty", "im very thirsty"]),
    ("es", "No me gusta el café", ["i dont like coffee", "i do not like coffee"]),
    ("es", "El desayuno está listo", ["breakfast is ready"]),
    ("es", "¿Qué quieres beber?", ["what do you want to drink"]),

    # 41-50: Rutina diaria
    ("en", "I wake up at seven", ["me despierto a las siete"]),
    ("en", "I brush my teeth every morning", ["me cepillo los dientes todas las mananas"]),
    ("en", "I take a shower before school", ["me ducho antes de ir a la escuela"]),
    ("en", "I go to bed at ten", ["me voy a dormir a las diez"]),
    ("en", "I am getting ready", ["me estoy preparando"]),
    ("es", "Me levanto temprano", ["i get up early"]),
    ("es", "Después almuerzo con mi familia", ["then i have lunch with my family"]),
    ("es", "Hoy estoy muy cansado", ["i am very tired today", "im very tired today"]),
    ("es", "Tengo que limpiar mi habitación", ["i have to clean my room"]),
    ("es", "Voy a hacer la tarea", ["i am going to do my homework", "im going to do my homework"]),

    # 51-60: Deportes y tiempo libre
    ("en", "I like playing soccer", ["me gusta jugar al futbol", "me gusta jugar futbol"]),
    ("en", "We won the match", ["ganamos el partido"]),
    ("en", "My favorite team is Argentina", ["mi equipo favorito es argentina"]),
    ("en", "I play video games with my friends", ["juego videojuegos con mis amigos"]),
    ("en", "She can swim very well", ["ella puede nadar muy bien"]),
    ("es", "Me gusta escuchar música", ["i like listening to music", "i like to listen to music"]),
    ("es", "Juego al fútbol los sábados", ["i play soccer on saturdays"]),
    ("es", "Quiero aprender a bailar", ["i want to learn to dance"]),
    ("es", "Él corre muy rápido", ["he runs very fast"]),
    ("es", "Vamos a ver una película", ["we are going to watch a movie", "lets watch a movie"]),

    # 61-70: Lugares y direcciones
    ("en", "Where is the train station?", ["donde esta la estacion de tren", "donde queda la estacion de tren"]),
    ("en", "Turn left at the corner", ["gira a la izquierda en la esquina"]),
    ("en", "The supermarket is near my house", ["el supermercado esta cerca de mi casa"]),
    ("en", "I need to go to the hospital", ["necesito ir al hospital"]),
    ("en", "How can I get to the park?", ["como puedo llegar al parque"]),
    ("es", "¿Dónde está el baño?", ["where is the bathroom", "where is the restroom"]),
    ("es", "El banco está enfrente de la escuela", ["the bank is across from the school"]),
    ("es", "Mi casa está lejos del centro", ["my house is far from downtown"]),
    ("es", "Sigue todo recto", ["go straight ahead", "keep going straight"]),
    ("es", "Estamos en el segundo piso", ["we are on the second floor"]),

    # 71-80: Tecnología y objetos
    ("en", "Where is my phone?", ["donde esta mi telefono", "donde esta mi celular"]),
    ("en", "My computer is very slow", ["mi computadora es muy lenta", "mi ordenador es muy lento"]),
    ("en", "I forgot my password", ["olvide mi contrasena"]),
    ("en", "Can you send me a message?", ["puedes enviarme un mensaje"]),
    ("en", "The internet is not working", ["internet no funciona", "el internet no funciona"]),
    ("es", "Necesito cargar mi teléfono", ["i need to charge my phone"]),
    ("es", "Mi computadora está apagada", ["my computer is turned off", "my computer is off"]),
    ("es", "Voy a abrir el archivo", ["i am going to open the file", "im going to open the file"]),
    ("es", "La pantalla es muy grande", ["the screen is very big", "the screen is very large"]),
    ("es", "No encuentro mis auriculares", ["i cant find my headphones", "i cannot find my headphones"]),

    # 81-90: Clima y naturaleza
    ("en", "It is raining outside", ["esta lloviendo afuera"]),
    ("en", "The weather is very cold today", ["el clima esta muy frio hoy"]),
    ("en", "I love sunny days", ["me encantan los dias soleados"]),
    ("en", "There are many trees in the park", ["hay muchos arboles en el parque"]),
    ("en", "The sky is full of stars", ["el cielo esta lleno de estrellas"]),
    ("es", "Hace mucho calor", ["it is very hot", "its very hot"]),
    ("es", "Está nevando en las montañas", ["it is snowing in the mountains", "its snowing in the mountains"]),
    ("es", "El perro está debajo de la mesa", ["the dog is under the table"]),
    ("es", "Me gusta caminar por la playa", ["i like walking on the beach", "i like to walk on the beach"]),
    ("es", "Hoy hace mucho viento", ["it is very windy today", "its very windy today"]),

    # 91-100: Oraciones variadas
    ("en", "I went to the park yesterday", ["ayer fui al parque", "fui al parque ayer"]),
    ("en", "Tomorrow I will visit my grandmother", ["manana visitare a mi abuela", "manana voy a visitar a mi abuela"]),
    ("en", "I cannot find my keys", ["no puedo encontrar mis llaves"]),
    ("en", "She is reading a very interesting book", ["ella esta leyendo un libro muy interesante"]),
    ("en", "We are learning English together", ["estamos aprendiendo ingles juntos"]),
    ("es", "Tengo catorce años", ["i am fourteen years old", "i am 14 years old"]),
    ("es", "Ayer jugué con mis amigos", ["i played with my friends yesterday"]),
    ("es", "¿Puedes ayudarme, por favor?", ["can you help me please"]),
    ("es", "Quiero viajar por el mundo", ["i want to travel around the world"]),
    ("es", "Mañana será un día mejor", ["tomorrow will be a better day"]),
]


def normalizar(texto):
    # Ignora mayúsculas, tildes y signos de puntuación
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto


def escuchar(idioma):
    recognizer = sr.Recognizer()

    input("Presiona ENTER para empezar a hablar...")

    try:
        print("\n🎙️ Habla ahora...")

        grabacion = sd.rec(
            int(DURACION * FRECUENCIA),
            samplerate=FRECUENCIA,
            channels=1,
            dtype="int16",
        )
        sd.wait()

        wav.write("respuesta.wav", FRECUENCIA, grabacion)
        print("🔎 Reconociendo tu voz...")

        with sr.AudioFile("respuesta.wav") as fuente:
            audio = recognizer.record(fuente)

        # Reconoce español o inglés según la pregunta
        codigo = "es-ES" if idioma == "en" else "en-US"

        texto = recognizer.recognize_google(
            audio,
            language=codigo,
        )

        print("📝 Dijiste:", texto)
        return texto

    except sr.UnknownValueError:
        print("😕 No pude entender lo que dijiste.")
        return None

    except sr.RequestError as error:
        print("❌ Error del reconocimiento:", error)
        return None

    except Exception as error:
        print("❌ Error:", error)
        return None


def jugar():
    global puntos

    random.shuffle(preguntas)

    print("=" * 40)
    print("       🎮 JUEGO DE TRADUCCIÓN")
    print("=" * 40)
    print("Empezás con", puntos, "puntos.")
    print("Correcta: +10 | Incorrecta: -5")
    print("Escribí S para salir del juego.\n")

    for numero, pregunta in enumerate(preguntas, start=1):
        print("-" * 40)
        print(f"Pregunta {numero} de {len(preguntas)}")
        print("Puntos actuales:", puntos)

        if pregunta[0] == "en":
            print("\n🌎 Traduce al ESPAÑOL:")
        else:
            print("\n🌎 Traduce al INGLÉS:")

        print(pregunta[1])

        opcion = input(
            "\nENTER para responder con el micrófono o S para salir: "
        ).strip().lower()

        if opcion == "s":
            break

        respuesta = escuchar(pregunta[0])

        if respuesta is None:
            print("No se pudo evaluar esta respuesta.")
            print("No se suman ni se restan puntos.")
            continue

        respuesta_limpia = normalizar(respuesta)

        respuestas_correctas = [
            normalizar(r) for r in pregunta[2]
]

        if respuesta_limpia in respuestas_correctas:
            puntos += 10
            print("\n✅ ¡CORRECTO! +10 puntos")
        else:
            puntos -= 5
            print("\n❌ Incorrecto. -5 puntos")
            print("Una respuesta válida era:")
            print(pregunta[2][0])

        print("⭐ Puntos actuales:", puntos)

    print("\n" + "=" * 40)
    print("          🏆 FIN DEL JUEGO")
    print("Puntuación final:", puntos)
    print("=" * 40)


if __name__ == "__main__":
    jugar()
