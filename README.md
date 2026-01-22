# SmartRise: The AI-Powered Multimedia Alarm System

SmartRise is a voice-controlled, AI-enhanced alarm clock system built on a Raspberry Pi 4. It is designed to help users start and end their days intentionally without needing screentime. Through integrated voice commands, music playback, alarm scheduling, and local AI interaction, SmartRise creates a screen-free, productivity-focused experience.
![IMG_9361](https://github.com/user-attachments/assets/cd908b34-0b94-4731-839e-b3ec3fed2ccd)


## 📸 Demo & Documentation
[Demo Video](https://drive.google.com/file/d/1xjQ_AtIRt9Aot3gjrQRl_ckbW8xgyLdE/view?usp=sharing)


## 🎯 Purpose & Motivation

Modern routines often start and end with distraction-heavy phone use. SmartRise was created as a healthier, distraction-free alternative: a bedside assistant that combines the best features of music, alarms, and AI chat into a single user-friendly system. Beyond solving a personal pain point, it also serves as a project for applying skills in embedded systems, AI/ML, Cloud Integration, and Cyber-Physical Systems.


## ⚙️ Core Components

STT (Speech-to-Text): Uses Whisper on a remote AWS EC2 server instance to transcribe audio commands.

TTS (Text-to-Speech): Uses pyttsx3 for fully offline responses.

Intent Classification: Custom-trained TF-IDF + SVM model to classify commands like "play music", "set alarm", etc.

Parameter Extraction: spaCy NER model trained to extract artist, song, time, label, etc.

Alarm System: SQLite-backed alarm manager that schedules, triggers, and logs custom alarms with Dateparser.

Music Playback: Plays .mp3 files stored locally using Pygame Mixer.

Chatbot: Local/offline LLM integration using Ollama for casual Q&A or fallback support.


### Main Command Loop (Overview)

Continuously checks the alarm database for triggered events.

Waits for wake-word ("smartrise" or "jarvis") via short speech segment.

On detection, prompts user and records main command.

Classifies the intent and extracts relevant parameters.

Executes the associated function: play music, set alarm, stop alarm, etc.

Responds with TTS or executes fallback AI chat if no match found.


## 🧩 Files & Directories

main.py: Entry point. Controls command loop and integration.

alarm/: Alarm logic, SQLite interaction, and trigger handling.

music_player/: Music playback logic with pause/resume/stop.

intent_model/: ML intent classifier and spaCy parameter model.

voice_assistant/:  Audio input/output (STT, TTS) modules.

live_record.py: Real-time audio recording until silence.

utils.py:  Helper for WAV recording.

chatio.py: LLM interface using Ollama.


## 👤 Developer

Alexander Kamil Diab-Liu
[Portfolio](https://alexdiabliu.github.io/) | [GitHub](https://github.com/alexdiabliu) | [LinkedIn](https://www.linkedin.com/in/alexdiabliu/)


## 📬 Questions?
Feel free to reach out via LinkedIn!

