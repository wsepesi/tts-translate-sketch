# %%
import os
import openai
import wave
import logging
import warnings
import tempfile
from callgpt import Chatbot
# import tkinter as tk
# from tkinter import filedialog
from gtts import gTTS
import os
import dotenv
import sounddevice as sd

logger = logging.getLogger(__name__)

# Catch warnings


def fxn():
    warnings.warn("deprecated", DeprecationWarning)


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


#directory = filedialog.askdirectory()
#os.chdir(directory)
# os.environ["OPENAI_API_KEY"] = open_file('openai_api_key.txt')
openai.api_key = dotenv.get_key(".env", "OPENAI_API_KEY")
openai_api_key = openai.api_key

# Configure audio settings
# FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
# RECORD_SECONDS = 5

# Initialize PyAudio
# audio = pyaudio.PyAudio()


def record_audio(seconds=8):
    print("Recording...")
    myrecording = sd.rec(int(seconds * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    print("Done recording.")
    return myrecording


def transcribe_audio(audio_data, jp=False, manual_jp=False):
    # save sd recording to a temporary wav file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(RATE)
            wf.writeframes(audio_data)

        # Transcribe the temporary file
        with open(temp_file.name, 'rb') as file:
            if jp:
                transcript = openai.Audio.translate(
                    "whisper-1",
                    file,
                    sample_rate=RATE,
                    encoding="LINEAR16",
                )
            elif manual_jp:
                transcript = openai.Audio.transcribe(
                    "whisper-1",
                    file,
                    sample_rate=RATE,
                    encoding="LINEAR16",
                    language="ja"
                )
            else:
                transcript = openai.Audio.transcribe(
                    "whisper-1",
                    file,
                    sample_rate=RATE,
                    encoding="LINEAR16",
                    language="en"
                )

    # Delete the temporary file
    os.unlink(temp_file.name)

    if transcript["text"]:
        return transcript["text"]
    else:
        return None


def synthesize_speech_with_whisper(text, jp=False):
    if not text:
        return None

    if jp:
        tts = gTTS(text, lang='ja')
    else:
        tts = gTTS(text, lang='en', tld='us')
    tts.save("output.mp3")
    os.system("afplay output.mp3")


def get_translation(text, jp=False):
    if not text:
        return None
    
    chatbot = Chatbot()

    if jp:
        prompt = f"Translate the following into English: '{text}'"
        response = chatbot.translate_prompt_jp_en(prompt)

    else:
        prompt = f"Translate this to Japanese: '{text}'"
        response = chatbot.translate_prompt_en_jp(prompt)
        # trim the romanized Japanese from the response, which is in parantheses
        response = response.split('(')[0]

    return response

# def play_audio(audio_data):
#     # play audio using sounddevice
#     print("Playing audio...")
#     sd.play(audio_data, 16000)
#     # sd.wait()
#     print("Done playing audio.")

if __name__ == "__main__":
    DIRECT = False
    while(True):
        try:
            # branch on whether the user inputs 'j' or 'e'
            user_input = input("Japanese or English? (j/e): ")
            selection = user_input[-1]
            time = user_input[:-1]
            print(selection, time)

            if selection == 'j':
                print("Japanese mode selected.")
                audio_data = record_audio(seconds=time)
                if DIRECT:
                    translation = transcribe_audio(audio_data, jp=True)
                else:
                    transcription = transcribe_audio(audio_data, manual_jp=True)
                    print(f"Transcription: {transcription}")
                    translation = get_translation(transcription, jp=True)
                print(f"Translation: {translation}")
                synthesized_speech = synthesize_speech_with_whisper(translation, jp=False)
                # play_audio(synthesized_speech)
            elif selection == 'e':
                print("English mode selected.")
                audio_data = record_audio(seconds=time)
                transcription = transcribe_audio(audio_data)
                print(f"Transcription: {transcription}")
                translation = get_translation(transcription)
                print(f"Translation: {translation}")
                synthesized_speech = synthesize_speech_with_whisper(translation, jp=True)
                # play_audio(synthesized_speech)
            else:
                print("Exiting...")
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            # break
        except Exception as e:
            print(f"Error: {e}")