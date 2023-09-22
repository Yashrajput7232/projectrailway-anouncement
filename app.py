# from flask import Flask, render_template, request
# from googletrans import Translator
# from google.cloud import texttospeech
# import os

# app = Flask(__name__)
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your-credentials-file.json'

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     translated_text = ''
#     audio_url = None
#     target_language = 'mr'  # Default to Marathi

#     if request.method == 'POST':
#         text_to_translate = request.form['text_to_translate']
#         target_language = request.form['target_language']

#         # Translate the text
#         translator = Translator()
#         translated_text = translator.translate(text_to_translate, dest=target_language).text

#         # Initialize Google Cloud Text-to-Speech client
#         client = texttospeech.TextToSpeechClient()

#         # ... (rest of your code to generate audio and URL)

#     return render_template('index.html', translated_text=translated_text, audio_url=audio_url, target_language=target_language)

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for
from googletrans import Translator
from google.cloud import texttospeech
import os
import pygame

app = Flask(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'erudite-river-393013-36e232235c42.json'

# Initialize Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

pygame.mixer.pre_init()
pygame.mixer.init()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    translated_text = ''
    audio_url = None
    target_language = 'mr'  # Default to Marathi

    if request.method == 'POST':
        text_to_translate = request.form['text_to_translate']
        target_language = request.form['target_language']

        # Translate the text
        translator = Translator()
        translated_text = translator.translate(text_to_translate, dest=target_language).text

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code=target_language,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the translated text
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=translated_text),
            voice=voice,
            audio_config=audio_config
        )

        # Save the speech as an audio file
        audio_file_name = 'translation.mp3'
        with open(audio_file_name, 'wb') as out:
            out.write(response.audio_content)

        audio_url = url_for('static', filename=audio_file_name)

    return render_template('translate.html', translated_text=translated_text, audio_url=audio_url, target_language=target_language)

@app.route('/announce', methods=['GET', 'POST'])
def announce():
    if request.method == 'POST':
        text_to_announce = request.form['text_to_announce']
        target_language = request.form['target_language']

        # Translate the text
        translator = Translator()
        translated_text = translator.translate(text_to_announce, dest=target_language).text

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code=target_language,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the translated text
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=translated_text),
            voice=voice,
            audio_config=audio_config
        )

        # Save the speech as an audio file
        audio_file_name = 'announcement.mp3'
        with open(audio_file_name, 'wb') as out:
            out.write(response.audio_content)

        # Play the audio using pygame
        pygame.mixer.music.load(audio_file_name)
        pygame.mixer.music.play()

    return render_template('announce.html')

if __name__ == '__main__':
    app.run(debug=True)
