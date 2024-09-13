# SRT Generator ft. Whisper
A Python script that generates an SRT file for your MP4 files, ft. Whisper.

To run the code snippet you provided, you'll need to install the following Python packages:

1. **Streamlit**: For building the web app interface.
2. **MoviePy**: For video editing and processing.
3. **Whisper**: For transcribing audio (assuming you're using OpenAI's Whisper model).
4. **Tempfile**: This is a built-in Python module, so you don't need to install it separately.
5. **OS**: This is also a built-in Python module and does not require installation.

You can install the necessary packages using pip:

```bash
pip install streamlit moviepy openai-whisper
```

Make sure you have the appropriate version of `whisper` (if it's the OpenAI model) and any dependencies that might be required for `moviepy`, such as `ffmpeg`. You can install `ffmpeg` with:

```bash
pip install imageio[ffmpeg]
```

If you encounter any issues with specific versions or dependencies, you might need to check the documentation for each package or adjust the versions accordingly.

### Run the Streamlit app:

```bash
streamlit run app.py
```

This will launch a local Streamlit web interface where you can upload MP4 files and download the converted MP3s.
