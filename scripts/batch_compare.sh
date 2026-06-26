#!/bin/bash

set -e

STYLE=${1:-nes}
KEEP_FILES=${2:-false}

INPUT_DIR="audio"
OUTPUT_DIR="audio/output/batch_compare"

mkdir -p "$OUTPUT_DIR"

echo "Batch comparing MP3 files in: $INPUT_DIR"
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

    DIRECT_OUTPUT="$OUTPUT_DIR/${SAFE_NAME}_direct_${STYLE}.wav"
    DEMUCS_OUTPUT="$OUTPUT_DIR/${SAFE_NAME}_demucs_dynamic_${STYLE}.wav"

    echo "========================================"
    echo "Processing: $BASENAME"
    echo "========================================"

    echo
    echo "Running direct conversion..."
    scripts/bitify_direct.sh \
        "$INPUT_FILE" \
        "$DIRECT_OUTPUT" \
        "$STYLE"

    echo
    echo "Running Demucs dynamic conversion..."
    scripts/bitify_demucs_dynamic.sh \
        "$INPUT_FILE" \
        "$DEMUCS_OUTPUT" \
        "$STYLE" \
        "$KEEP_FILES"

    echo
    echo "Done with: $BASENAME"
    echo "Direct: $DIRECT_OUTPUT"
    echo "Demucs dynamic: $DEMUCS_OUTPUT"
    echo
done

echo "All MP3 files processed."
echo "Results saved in: $OUTPUT_DIR"