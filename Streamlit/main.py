import streamlit as st
import sounddevice as sd
import soundfile as sf
import numpy as np

recording = False

def record_audio(file_path, duration):
    global recording

    # Callback function to record audio
    def callback(indata, frames, time, status):
        if status:
            print('Recording error:', status)

        # Reshape the audio data if needed
        if indata.ndim > 1:
            indata = np.squeeze(indata)

        # Save recorded audio to file
        with sf.SoundFile(file_path, mode='w', samplerate=48000, channels=1) as file:
            file.write(indata)

    # Start audio recording
    recording = True
    with sd.InputStream(callback=callback, device = 4):
        dev = sd.query_devices()[4]
        print(dev['default_samplerate'])
        print(dev['max_input_channels'])
        st.write('Recording audio...')
        sd.sleep(int(duration * 1000))

    st.write('Finished recording audio.')
    recording = False

def main():
    global recording
    st.title('Audio Recorder')

    print(sd.query_devices())

    # Button to start or stop recording audio
    if not recording and st.button('Record'):
        # Specify the output file path and duration
        file_path = 'recorded_audio.wav'
        duration = 5  # in seconds

        record_audio(file_path, duration)
    elif recording and st.button('Stop'):
        recording = False
    

if __name__ == '__main__':
    main()
