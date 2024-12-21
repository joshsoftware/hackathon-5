# Hackathon - Team 4 (Scamurai)
Real-Time Scam Detection for Calls

### Introduction

The "Real-Time Scam Detection for Calls" project is designed to safeguard users—particularly vulnerable groups like the elderly—against phone call scams. The mobile app, built using React Native, listens to incoming calls, processes the audio in real time, and uses a Random Forest NLP model to analyze the conversation for scam-related patterns. If a scam is detected, the app alerts the user, advising them on whether the call should be disconnected or if they should avoid sharing sensitive information.

### Problem Statement
Phone scams are a major issue, with fraudsters using sophisticated techniques to deceive people, especially the elderly. These scams frequently involve requests for personal details, financial information, or one-time passwords (OTPs). Detecting these scams in real-time can help users protect themselves before falling victim to fraudulent activities.

### Objectives
Build a real-time mobile app that listens to phone calls and streams the audio to the backend for processing.
Use Natural Language Processing (NLP) and Machine Learning (ML) algorithms, specifically a Random Forest model trained on scam-related data, to identify scam patterns.
Provide real-time alerts to the user, including suggestions like disconnecting the call or avoiding sharing sensitive information.

### Scope
Real-time audio streaming from mobile devices (iOS/Android).
Random Forest NLP model for scam detection.
Integration with mobile apps (built using React Native).
Backend API using FastAPI in Python for real-time audio processing and model inference.

## BAckend Project Setup

### Install Python3
To install python on your system, [refer this.](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/)

### Clone the repo
```
git clone https://github.com/joshsoftware/hackathon-team-4.git
cd service
```

### Required Modules
To install all the required modeules to run project, use this command
```
pip install -r requirement.txt
```
## Run
To run the system, use command
```
uvicorn app:app --reload
```
