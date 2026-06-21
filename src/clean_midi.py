from pathlib import Path
import argparse
import pretty_midi

parser = argparse.ArgumentParser(
    description="Clean noisy transcribed MIDI."
)

parser.add_argument("input_file")
parser.add_argument(
    "-o",
    "--output",
    default="audio/output/cleaned.mid"
)

parser.add_argument(
    "--min_note_length",
    type=float,
    default=0.12,
    help="Remove notes shorter than this many seconds"
)

args = parser.parse_args()

midi = pretty_midi.PrettyMIDI(args.input_file)

for instrument in midi.instruments:
    cleaned_notes = []

    for note in instrument.notes:
        length = note.end - note.start

        if length >= args.min_note_length:
            cleaned_notes.append(note)

    instrument.notes = cleaned_notes

output_path = Path(args.output)
output_path.parent.mkdir(parents=True, exist_ok=True)

midi.write(str(output_path))

print(f"Saved cleaned MIDI to {output_path}")