Build on top of https://github.com/marquisdepolis/audiochat to rework the flow to reesult in a python script that can be run from the CLI. All credit to @marquisdepolis for the initial draft

Lightweight solution to a Japanese student who moved in with my host family in Paris for a few weeks, who speaks practically no French or English.

`python audiochat.py` opens the system menu, allowing for an input of `j` or `e` to read in Japanese or English speech respectively, transcribe with Whisper, then translate with GPT-3.5-Turbo, then TTS back to the user. Prefixing the input with a number will set the tool to listen for that long, otherwise defaults to 8 seconds. Prefixing with `c` enters continuous mode, where it will listen for up to a minute or until the user inputs `x` to exit.



## TODO
- Wrap into real GUI or webapp. Right now just runs on my PC which is not ideal (laptop is large, dinner table is small, etc)
