import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import whisper
import os

def convert_mp4_to_mp3(mp4_bytes):
    try:
        # Use a temporary file to store the uploaded MP4 in memory
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(mp4_bytes)
            temp_video.flush()
            video = VideoFileClip(temp_video.name)
        
        # Create a temporary MP3 file in memory
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            video.audio.write_audiofile(temp_audio.name)
            temp_audio.flush()
            
            # Read the MP3 file back into memory
            with open(temp_audio.name, "rb") as mp3_file:
                mp3_bytes = mp3_file.read()
        
        return mp3_bytes, None
    except Exception as e:
        return None, str(e)

def transcribe_mp3(mp3_bytes):
    try:
        model = whisper.load_model("base")  # Load the Whisper model
        st.text("Whisper model loaded. Starting transcription...")
        
        # Save MP3 bytes to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
            temp_mp3.write(mp3_bytes)
            temp_mp3.flush()
            temp_mp3_path = temp_mp3.name
        
        # Transcribe the audio file
        st.text(f"Transcribing MP3 file: {temp_mp3_path}")
        result = model.transcribe(temp_mp3_path)
        
        # Clean up temporary file
        os.remove(temp_mp3_path)
        
        st.text("Transcription completed.")
        
        # Generate SRT formatted text
        srt_content = ""
        for segment in result["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            srt_content += f"{segment['id'] + 1}\n"
            srt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
            srt_content += f"{text}\n\n"
        
        return srt_content.encode(), None
    except Exception as e:
        return None, str(e)

def format_time(seconds):
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"

def main():
    st.title("MP4 to MP3 Converter and Transcription")
    st.write("Upload an MP4 file to convert it to MP3 and get a transcript.")
    
    # File upload
    uploaded_file = st.file_uploader("Choose an MP4 file", type=["mp4"])
    
    if uploaded_file is not None:
        if st.button("Convert to MP3"):
            st.write("Converting...")
            mp3_bytes, error = convert_mp4_to_mp3(uploaded_file.read())
            
            if mp3_bytes:
                st.success("Conversion successful!")
                
                # Download MP3
                st.download_button(
                    label="Download MP3",
                    data=mp3_bytes,
                    file_name=uploaded_file.name.replace(".mp4", ".mp3"),
                    mime="audio/mp3"
                )
                
                # Transcription
                st.write("Transcribing MP3...")
                srt_bytes, trans_error = transcribe_mp3(mp3_bytes)
                
                if srt_bytes:
                    st.success("Transcription successful!")
                    st.download_button(
                        label="Download SRT",
                        data=srt_bytes,
                        file_name=uploaded_file.name.replace(".mp4", ".srt"),
                        mime="text/plain"
                    )
                else:
                    st.error(f"Transcription error: {trans_error}")
            else:
                st.error(f"Conversion error: {error}")

if __name__ == "__main__":
    main()
