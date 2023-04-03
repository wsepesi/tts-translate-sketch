from audiochat import *

if __name__ == "__main__":
    text = record_audio_async()
    print(len(text))