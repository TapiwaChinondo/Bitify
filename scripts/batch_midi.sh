#!/bin/bash

set -e

MODE=${1:-nes}

INPUT_DIR="audio"
OUTPUT_DIR="audio/output/batch_midi_${MODE}"

mkdir -p "$OUTPUT_DIR"

echo "Batch converting MIDI files in: $INPUT_DIR"
echo "Mode: $MODE"
echo "Output: $OUTPUT_DIR"
echo

for INPUT_FILE in "$INPUT_DIR"/*.mid "$INPUT_DIR"/*.midi
do
    if [ ! -f "$INPUT_FILE" ]; then
        continue
    fi

    BASENAME=$(basename "$INPUT_FILE")
    SONG_NAME="${BASENAME%.*}"
    SAFE_NAME=$(echo "$SONG_NAME" | tr ' ' '_' | tr -cd '[:alnum:]_-')

    OUTPUT_FILE="$OUTPUT_DIR/${SAFE_NAME}_${MODE}.wav"

    echo "Processing: $BASENAME"

    scripts/bitify_midi.sh \
        "$INPUT_FILE" \
        "$OUTPUT_FILE" \
        "$MODE"

    echo "Saved: $OUTPUT_FILE"
    echo
done

echo "All MIDI files processed."
echo "Results saved in: $OUTPUT_DIR"