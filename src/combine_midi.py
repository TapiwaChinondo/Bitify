from pathlib import Path
import argparse
import pretty_midi

parser = argparse.ArgumentParser(
    description="Combine MIDI files with volume weights."
)

parser.add_argument("input_files", nargs="+")
parser.add_argument("-o", "--output", default="audio/output/combined.mid")

args = parser.parse_args()

combined = pretty_midi.PrettyMIDI()

# Edit these based on what sounds good
volume_weights = {
    "other": 1.0,
    "vocals": 1.6,
    "bass": 0.25,
    "drums": 0.2,
}

for midi_file in args.input_files:
    midi_path = Path(midi_file)
    midi = pretty_midi.PrettyMIDI(str(midi_path))

    weight = 1.0

    for stem_name, stem_weight in volume_weights.items():
        if stem_name in midi_path.stem.lower():
            weight = stem_weight

    for instrument in midi.instruments:
        for note in instrument.notes:
            note.velocity = int(max(1, min(127, note.velocity * weight)))

        combined.instruments.append(instrument)

output_path = Path(args.output)
output_path.parent.mkdir(parents=True, exist_ok=True)
combined.write(str(output_path))

print(f"Saved combined MIDI to {output_path}")