Build on top of https://github.com/marquisdepolis/audiochat to rework the flow to reesult in a python script that can be run from the CLI. 

Lightweight solution to a realtime conversation translator / language acquisition tool.

`python audiochat.py` opens the system menu, allowing for an input of `j` or `e` to read in Japanese or English speech respectively, transcribe with Whisper, then translate with GPT-3.5-Turbo, then TTS back to the user. `x` closes the stream and makes the calls.

## TODO
- Wrap into real GUI or webapp. Right now just runs on my PC which is not ideal (laptop is large, dinner table is small, etc)
