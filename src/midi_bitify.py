from pathlib import Path
import argparse

# Adavcned math needed for sound waves
import numpy as np
import pretty_midi
import soundfile as sf

from synth import generate_wave, midi_note_to_frequency, choose_wave_type, apply_envelope

parser = argparse.ArgumentParser(
    description="Convert MIDI files into 8-bit WAV audio."
)

parser.add_argument(
    "input_file",
    help="Input MIDI file"
)

parser.add_argument(
    "-o",
    "--output",
    default="audio/output/output.wav",
    help="Output WAV file"
)

parser.add_argument(
    "-m",
    "--mode",
    default="nes",
    choices=[
        "nes",
        "gameboy",
        "mixed",
        "genesis",
        "sine"
    ],
    help="Wave mode"
)

args = parser.parse_args()

input_path = args.input_file
output_path = Path(args.output)
mode = args.mode


# Input and output files

# Choose the wave type: "square" or "triangle"
# Suqare is 8bit, Triangle is Gameboy
wave_type = choose_wave_type(mode)

# Set the sample rate --> Standard CD-quality
sample_rate = 44100
output_path.parent.mkdir(parents=True, exist_ok=True)

# Load the MIDI file
midi_data = pretty_midi.PrettyMIDI(input_path)
duration_seconds = midi_data.get_end_time()

# Empty audio track to be filled later / bitified
audio_samples = np.zeros(int(duration_seconds * sample_rate))


# Main loop for every instrument and every note,
# find the start and end times of the note and convert the frequency
for instrument in midi_data.instruments:
    for note in instrument.notes:

        # Starting time and ending time
        start_sample = int(note.start * sample_rate)
        end_sample = int(note.end * sample_rate)

        frequency_hz = midi_note_to_frequency(note.pitch)
        note_length = end_sample - start_sample

        # length in samples
        time_points = np.arange(note_length) / sample_rate

        # bitify it --> Create a wave
        wave_type = choose_wave_type(mode)
        
        wave = generate_wave(
            frequency_hz,
            time_points,
            wave_type
        )
        
        wave = apply_envelope(wave, sample_rate)

        volume = note.velocity / 127

        # adds note to the song
        audio_samples[start_sample:end_sample] += wave * volume * 0.2


peak = np.max(np.abs(audio_samples))

# Normalise audio volume
if peak > 0:
    audio_samples = audio_samples / peak * 0.8

sf.write(output_path, audio_samples, sample_rate)

print(f"Saved {output_path}")