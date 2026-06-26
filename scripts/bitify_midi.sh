#!/bin/bash

set -e

INPUT_FILE=${1:-audio/Mario.mid}
OUTPUT_FILE=${2:-audio/output/output.wav}
MODE=${3:-nes}

mkdir -p "$(dirname "$OUTPUT_FILE")"

python src/midi_bitify.py \
    "$INPUT_FILE" \
    --mode "$MODE" \
    -o "$OUTPUT_FILE"

echo "Saved: $OUTPUT_FILE"