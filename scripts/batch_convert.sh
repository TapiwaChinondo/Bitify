#!/bin/bash

set -e

STYLE=${1:-mixed}

INPUT_DIR="audio"
OUTPUT_DIR="audio/output/batch_${STYLE}"

mkdir -p "$OUTPUT_DIR"

echo "Batch converting MP3 files in: $INPUT_DIR"
echo "Style: $STYLE"
echo "Output: $OUTPUT_DIR"
echo

for INPUT_FILE in "$INPUT_DIR"/*.mp3
do
    if [ ! -f "$INPUT_FILE" ]; then
        echo "No MP3 files found in $INPUT_DIR"
        exit 0
    fi

    BASENAME=$(basename "$INPUT_FILE")
    SONG_NAME="${BASENAME%.*}"

    SAFE_NAME=$(echo "$SONG_NAME" | tr ' ' '_' | tr -cd '[:alnum:]_-')

    OUTPUT_FILE="$OUTPUT_DIR/${SAFE_NAME}_${STYLE}.wav"

    echo "========================================"
    echo "Processing: $BASENAME"
    echo "Output: $OUTPUT_FILE"
    echo "========================================"

    scripts/bitify_direct.sh \
        "$INPUT_FILE" \
        "$OUTPUT_FILE" \
        "$STYLE"

    echo "Done: $OUTPUT_FILE"
    echo
done

echo "All MP3 files processed."
echo "Results saved in: $OUTPUT_DIR"