import librosa

audio_path = "audio/sample.mp3"

sample, sample_rate = librosa.load(audio_path)
duration = len(sample) / sample_rate
print(f"Duration: {duration:.2f} seconds")
print(f"Sample rate: {sample_rate} Hz")