import streamlit as st
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import subprocess
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Voice Cloning App",
    page_icon="🎤",
    layout="wide"
)

# Main title
st.title("🎤 Voice Cloning Application")
st.markdown("""Create your own voice clone using F5-TTS technology. Follow the steps below to record your voice,
train the model, and generate synthesized speech.""")

# Create necessary directories
if not os.path.exists('recordings'):
    os.makedirs('recordings')
if not os.path.exists('output'):
    os.makedirs('output')

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Record Voice", "Train Model", "Generate Speech"]
)

# Recording function
def record_audio(duration, sample_rate=44100):
    recording = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate,
                      channels=1)
    sd.wait()
    return recording

# Record Voice Page
if page == "Record Voice":
    st.header("Record or Upload Your Voice")
    st.markdown("""
    You can either record your voice directly or upload pre-recorded .wav files to create your voice dataset.
    Speak clearly and naturally in a quiet environment for best results.
    """)
    
    # Create tabs for recording and uploading
    record_tab, upload_tab = st.tabs(["Record Voice", "Upload Files"])
    
    with record_tab:
        # Recording controls
        duration = st.slider("Recording Duration (seconds)", 1, 10, 5)
        
        if st.button("Start Recording"):
            with st.spinner(f"Recording for {duration} seconds..."):
                try:
                    # Record audio
                    recording = record_audio(duration)
                    
                    # Generate filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"recordings/recording_{timestamp}.wav"
                    
                    # Save the recording
                    sf.write(filename, recording, 44100)
                    
                    st.success(f"Recording saved as {filename}")
                    
                    # Display audio playback
                    st.audio(filename)
                    
                except Exception as e:
                    st.error(f"Error during recording: {str(e)}")
    
    with upload_tab:
        uploaded_files = st.file_uploader("Upload .wav files", type=["wav"], accept_multiple_files=True)
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    # Generate filename with original name and timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"recordings/{uploaded_file.name.split('.')[0]}_{timestamp}.wav"
                    
                    # Save the uploaded file
                    with open(filename, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    st.success(f"File saved as {filename}")
                    
                    # Display audio playback
                    st.audio(filename)
                    
                except Exception as e:
                    st.error(f"Error processing uploaded file: {str(e)}")

# Train Model Page
elif page == "Train Model":
    st.header("Train Voice Model")
    st.markdown("""
    Train the F5-TTS model using your recorded voice samples. This process may take some time
    depending on your system's capabilities.
    """)
    
    # Get list of recordings
    recordings = [f for f in os.listdir('recordings') if f.endswith('.wav')]
    
    if len(recordings) == 0:
        st.warning("No recordings found. Please record some voice samples first.")
    else:
        st.info(f"Found {len(recordings)} recordings")
        
        if st.button("Start Training"):
            with st.spinner("Training model..."):
                try:
                    # Prepare dataset directory
                    if not os.path.exists('dataset'):
                        os.makedirs('dataset')
                    
                    # Copy recordings to dataset directory
                    for recording in recordings:
                        src = os.path.join('recordings', recording)
                        dst = os.path.join('dataset', recording)
                        if not os.path.exists(dst):
                            os.system(f'cp {src} {dst}')
                    
                    # Run F5-TTS training script
                    training_command = [
                        'python',
                        'F5-TTS/src/f5_tts/train/train.py',
                        '--config', 'F5-TTS/src/f5_tts/configs/F5TTS_Base_train.yaml',
                        '--data_path', 'dataset',
                        '--output_dir', 'output'
                    ]
                    
                    process = subprocess.Popen(
                        training_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    
                    # Stream output to Streamlit
                    # Check if stdout exists before reading
                    if process.stdout:
                        while True:
                            output = process.stdout.readline()
                            if output == b'' and process.poll() is not None:
                                break
                            if output:
                                st.text(output.strip().decode())
                    else:
                        st.warning("No output stream available from the process")
                    
                    if process.returncode == 0:
                        st.success("Training completed successfully!")
                    else:
                        st.error("Training failed. Please check the logs above.")
                        
                except Exception as e:
                    st.error(f"Error during training: {str(e)}")

# Generate Speech Page
elif page == "Generate Speech":
    st.header("Generate Speech")
    st.markdown("""
    Generate speech using your trained voice model. Enter the text you want to convert to speech.
    """)
    
    # Check if model exists
    if not os.path.exists('output/model.pth'):
        st.warning("No trained model found. Please train the model first.")
    else:
        # Text input for speech generation
        text_input = st.text_area("Enter text to convert to speech")
        
        if st.button("Generate Speech") and text_input:
            with st.spinner("Generating speech..."):
                try:
                    # Get a reference audio file
                    ref_audio = os.listdir('recordings')[0]
                    ref_audio_path = os.path.join('recordings', ref_audio)
                    
                    # Generate output filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = f"generated_speech_{timestamp}.wav"
                    
                    # Run F5-TTS inference
                    inference_command = [
                        'python',
                        'F5-TTS/src/f5_tts/infer/infer_cli.py',
                        '--model', 'F5-TTS',
                        '--ckpt_file', 'output/model.pth',
                        '--ref_audio', ref_audio_path,
                        '--ref_text', '',
                        '--gen_text', text_input,
                        '--output_dir', 'output',
                        '--output_file', output_file
                    ]
                    
                    process = subprocess.run(
                        inference_command,
                        capture_output=True,
                        text=True
                    )
                    
                    if process.returncode == 0:
                        output_path = os.path.join('output', output_file)
                        st.success("Speech generated successfully!")
                        st.audio(output_path)
                    else:
                        st.error(f"Speech generation failed: {process.stderr}")
                        
                except Exception as e:
                    st.error(f"Error during speech generation: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit and F5-TTS</p>
    <p>Created by jomangbp</p>
</div>
""", unsafe_allow_html=True)