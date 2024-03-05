import pyttsx3

def text_to_speech(text, voice_id, emphasized_word):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.setProperty('rate', 150)  # Adjust the speech rate
    engine.setProperty('volume', 1)  # Adjust the speech volume
    engine.setProperty('pitch', 1000)  # Adjust the speech pitch

    # Convert the text to speech
    for word in text.split():
        if word.lower() == emphasized_word.lower():
            engine.say(word.upper())  # Emphasize the word
        else:
            engine.say(word)  # Normal pronunciation for other words

    # Wait for the speech to finish
    engine.runAndWait()

# Example usage
# text = "The quick brown fox jumps over the lazy dog"
# emphasized_word = "fox" 
# text_to_speech(text, 1, "fox")
# text_to_speech("""Once upon a time in a small village nestled amidst rolling hills and whispering forests, there lived a young girl named Elara. Elara was captivated by the night sky, spending countless hours gazing up at the twinkling stars, each one a beacon of hope and wonder in her eyes.
# One crisp autumn evening, as the moon rose high above the village, Elara slipped out of her cozy cottage and made her way to her favorite spot, a grassy knoll just beyond the outskirts of town. She lay down upon the soft earth, her eyes tracing the constellations above.
# As she watched, a shooting star streaked across the heavens, and Elara closed her eyes, making a wish with all her heart. When she opened them again, she saw something remarkable—a figure standing before her, bathed in the gentle glow of moonlight.
# The figure was that of a young man, tall and handsome, with eyes that sparkled like the stars themselves. He introduced himself as Orion, a celestial being tasked with watching over the night sky.
# Elara was awestruck by the stranger's presence but felt an instant connection to him. They spent the night talking, sharing stories of their lives and dreams. Orion spoke of the wonders of the universe, of galaxies and nebulae beyond imagining, while Elara spoke of her love for her village and her desire to explore the world beyond.
# As the first light of dawn began to creep over the horizon, Orion knew he must return to his celestial duties. With a heavy heart, he bid Elara farewell, promising to visit her again beneath the stars.
# Days turned into weeks, and weeks into months, but Elara never forgot her encounter with Orion. She continued to gaze up at the night sky, searching for any sign of him among the twinkling lights.
# Then, one fateful night, as she lay beneath the stars once more, Orion appeared before her. He took her hand and together they danced across the heavens, a symphony of starlight and magic.
# From that moment on, Elara and Orion shared many more nights together, their bond growing stronger with each passing moment. And though they came from different worlds, their love knew no bounds, transcending time and space itself.
# And so, as the world slumbered beneath a blanket of stars, Elara and Orion danced on, their love shining bright for all eternity.""", 1)


import json
from google.cloud import firestore
print("s")
with open('config.json', 'r') as file:
    config = json.load(file)
FIREBASE_JSON = config['FIREBASE_JSON']
db = firestore.Client.from_service_account_json(FIREBASE_JSON)
all_users = db.collection('users').get()
for user in all_users:
    print(db.collection('users').document(user.id).get().to_dict())
# db_ref = db.collection("users").document("ordado1")
# db_ref.set({
#     "general_information":
#     {
#     "name": "or",
#     "gender": "male",
#     "age": "6",
#     "interests": "footbal"
#     }
# })