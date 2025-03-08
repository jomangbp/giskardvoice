# Giskard Voice - A Foundation for Voice Cloning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Giskard Voice is an open-source voice cloning application inspired by the psychohistorical principles of Isaac Asimov's Foundation series. Just as Hari Seldon could predict the future of humanity, this application allows you to preserve and reproduce your voice using advanced AI technology.

## Features

- **Voice Recording**: Record your voice directly through the application or upload pre-recorded WAV files
- **Model Training**: Train a personalized voice model using F5-TTS technology
- **Speech Generation**: Generate natural-sounding speech from text using your cloned voice
- **User-Friendly Interface**: Simple Streamlit interface for easy interaction

## Installation

### Prerequisites

- Python 3.8 or higher
- A decent GPU for faster training (CPU will work but will be slower)

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/jomangbp/giskard-voice.git
   cd giskard-voice
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Clone the F5-TTS repository if not already included:
   ```
   git clone https://github.com/SWivid/F5-TTS.git
   ```

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Navigate to the provided URL (usually http://localhost:8501)

3. Follow the steps in the application:
   - Record or upload voice samples
   - Train your voice model
   - Generate speech using your cloned voice

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── F5-TTS/               # F5-TTS voice cloning engine
├── recordings/           # Directory for voice recordings
└── output/               # Directory for trained models and generated audio
```

## How It Works

Giskard Voice uses the F5-TTS (Foundation Five Text-to-Speech) system to create a digital replica of your voice. The process involves:

1. **Data Collection**: Recording or uploading voice samples to create a dataset
2. **Model Training**: Training a neural network to learn the characteristics of your voice
3. **Speech Synthesis**: Generating new speech in your voice from any text input

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [SWivid's F5-TTS](https://github.com/SWivid/F5-TTS) for the voice cloning technology
- Inspired by Isaac Asimov's Foundation series and the concept of psychohistory

---

*"The psychohistorians can predict the voice of humanity, but Giskard Voice can preserve yours."*