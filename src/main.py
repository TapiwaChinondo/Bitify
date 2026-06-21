import librosa
import soundfile as sf
from pathlib import Path

audio_path = "audio/sample.mp3"
output_path = Path("audio/output/output.wav")

sample, sample_rate = librosa.load(audio_path)

# calculate the duration of the audio
duration = len(sample) / sample_rate
print(f"Duration: {duration:.2f} seconds")
print(f"Sample rate: {sample_rate} Hz")

# Outputting filie
sf.write(output_path, sample, sample_rate)
print(f"Saved converted audio to {output_path}")