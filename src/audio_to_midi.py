from pathlib import Path
import argparse
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict_and_save

parser = argparse.ArgumentParser(
    description="Convert audio files into MIDI."
)

parser.add_argument(
    "input_file",
    help="Input audio file, for example audio/song.mp3"
)

parser.add_argument(
    "-o",
    "--output_dir",
    default="audio/output",
    help="Folder to save MIDI output"
)

args = parser.parse_args()

input_path = Path(args.input_file)
output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

predict_and_save(
    [args.input_file],
    str(output_dir),
    save_midi=True,
    sonify_midi=False,
    save_model_outputs=False,
    save_notes=False,
    model_or_model_path=ICASSP_2022_MODEL_PATH
)

print(f"Saved MIDI to {output_dir}")