from pathlib import Path
import argparse
import numpy as np
import soundfile as sf

parser = argparse.ArgumentParser(description="Mix multiple WAV files into one WAV.")
parser.add_argument("input_files", nargs="+")
parser.add_argument("-o", "--output", default="audio/output/mixed.wav")
args = parser.parse_args()

tracks = []
sample_rate = None

for input_file in args.input_files:
    path = Path(input_file)
    if not path.exists():
        continue

    audio, sr = sf.read(path)

    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    if sample_rate is None:
        sample_rate = sr
    elif sr != sample_rate:
        raise ValueError(f"Sample rate mismatch: {path} has {sr}, expected {sample_rate}")

    tracks.append(audio)

if not tracks:
    raise ValueError("No WAV files to mix.")

max_length = max(len(track) for track in tracks)
mix = np.zeros(max_length)

for track in tracks:
    mix[:len(track)] += track

# peak = np.max(np.abs(mix))
# if peak > 0:
#     mix = mix / peak * 0.8

output_path = Path(args.output)
output_path.parent.mkdir(parents=True, exist_ok=True)
sf.write(output_path, mix, sample_rate)
print(f"Saved mixed WAV to {output_path}")
