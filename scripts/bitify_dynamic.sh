#!/bin/bash

set -e

INPUT_FILE=${1:-audio/Mario.mid}
OUTPUT_FILE=${2:-audio/output/dynamic_8bit.wav}
STYLE=${3:-nes}

mkdir -p "$(dirname "$OUTPUT_FILE")"

python src/dynamic_midi_bitify.py \
    "$INPUT_FILE" \
    --style "$STYLE" \
    -o "$OUTPUT_FILE"

echo "Saved: $OUTPUT_FILE"
