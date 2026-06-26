#!/bin/bash

set -e

INPUT_FILE=${1:-audio/sample.mp3}
OUTPUT_FILE=${2:-audio/output/direct_8bit.wav}
MODE=${3:-nes}

TEMP_DIR="audio/temp_direct"

mkdir -p "$TEMP_DIR"
mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "Converting audio to MIDI..."
python src/audio_to_midi.py "$INPUT_FILE" -o "$TEMP_DIR"

MIDI_FILE=$(find "$TEMP_DIR" -name "*.mid" | head -n 1)

if [ -z "$MIDI_FILE" ]; then
    echo "No MIDI file created."
    exit 1
fi

echo "Converting MIDI to 8-bit..."
python src/midi_bitify.py "$MIDI_FILE" --mode "$MODE" -o "$OUTPUT_FILE"

echo "Cleaning temporary files..."
rm -rf "$TEMP_DIR"

echo "Saved: $OUTPUT_FILE"