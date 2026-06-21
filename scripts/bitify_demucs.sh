#!/bin/bash

set -e

INPUT_FILE=${1:-audio/sample.mp3}
OUTPUT_FILE=${2:-audio/output/demucs_8bit.wav}
MODE=${3:-mixed}
KEEP_FILES=${4:-false}

TEMP_DIR="audio/temp_demucs"
SEPARATED_DIR="$TEMP_DIR/separated"
MIDI_DIR="$TEMP_DIR/midi"

SONG_NAME=$(basename "$INPUT_FILE")
SONG_NAME="${SONG_NAME%.*}"

mkdir -p "$SEPARATED_DIR"
mkdir -p "$MIDI_DIR"
mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "Separating audio with Demucs..."
demucs "$INPUT_FILE" -o "$SEPARATED_DIR"

STEM_DIR="$SEPARATED_DIR/htdemucs/$SONG_NAME"

if [ ! -d "$STEM_DIR" ]; then
    echo "Could not find stem directory: $STEM_DIR"
    exit 1
fi

echo "Converting stems to MIDI..."

for STEM in vocals other bass drums
do
    STEM_FILE="$STEM_DIR/$STEM.wav"

    if [ -f "$STEM_FILE" ]; then
        echo "Converting $STEM..."
        mkdir -p "$MIDI_DIR/$STEM"
        python src/audio_to_midi.py "$STEM_FILE" -o "$MIDI_DIR/$STEM"
    fi
done

echo "Combining MIDI files..."

python src/combine_midi.py \
    "$MIDI_DIR/vocals"/*.mid \
    "$MIDI_DIR/other"/*.mid \
    "$MIDI_DIR/bass"/*.mid \
    "$MIDI_DIR/drums"/*.mid \
    -o "$TEMP_DIR/combined.mid"

echo "Converting combined MIDI to 8-bit..."
python src/midi_bitify.py "$TEMP_DIR/combined.mid" --mode "$MODE" -o "$OUTPUT_FILE"

if [ "$KEEP_FILES" != "true" ]; then
    echo "Cleaning temporary files..."
    rm -rf "$TEMP_DIR"
else
    echo "Kept temporary files in: $TEMP_DIR"
fi

echo "Saved: $OUTPUT_FILE"