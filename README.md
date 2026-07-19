# Task 1: Voice Assistant (Beginner Tier)

A Python-based voice assistant built as part of the Oasis Infobyte Python Development Internship.

## Features Implemented
- Voice Input via speech_recognition
- Text-to-Speech via pyttsx3
- Tells current time and date
- Launches web searches
- Graceful error handling

## Privacy Consideration
All voice data is processed locally. Audio snippets are converted to text using Google's Web Speech API. No data is stored or saved.
python assistant.py

## Privacy & Compliance Considerations
* **Data Collection Scope:** This Voice Assistant operates exclusively via localized triggers. All processed vocal data is routed securely to the Google Web Speech API infrastructure for transcription transiently. No audio recordings are permanently written to long-term physical disks.
* **Audit Logging Transparency:** The system maintains a localized execution log file named `privacy_audit.log` which registers what action intents were identified during runtime. No continuous microphonic surveillance or data sharing operations are active.
* **Network Context:** External internet connectivity is limited exclusively to outbound queries toward the secure OpenWeatherMap API endpoints and explicit user-requested browser redirects.