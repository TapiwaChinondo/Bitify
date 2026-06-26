#!/bin/bash

set -e

INPUT_FILE=${1:-audio/sample.mp3}
OUTPUT_FILE=${2:-audio/output/demucs_dynamic_8bit.wav}
STYLE=${3:-nes}
KEEP_FILES=${4:-false}

TEMP_DIR="audio/temp_demucs_dynamic"
SEPARATED_DIR="$TEMP_DIR/separated"
MIDI_DIR="$TEMP_DIR/midi"
WAV_DIR="$TEMP_DIR/wav"

SONG_NAME=$(basename "$INPUT_FILE")
SONG_NAME="${SONG_NAME%.*}"

rm -rf "$TEMP_DIR"

mkdir -p "$SEPARATED_DIR"
mkdir -p "$MIDI_DIR"
mkdir -p "$WAV_DIR"
mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "Separating audio with Demucs..."
demucs "$INPUT_FILE" -o "$SEPARATED_DIR"

STEM_DIR="$SEPARATED_DIR/htdemucs/$SONG_NAME"

if [ ! -d "$STEM_DIR" ]; then
    echo "Could not find stem directory: $STEM_DIR"
    exit 1
fi

echo "Mixing raw Demucs stems for comparison..."
python src/mix_wavs.py \
    "$STEM_DIR/vocals.wav" \
    "$STEM_DIR/other.wav" \
    "$STEM_DIR/bass.wav" \
    "$STEM_DIR/drums.wav" \
    -o "$TEMP_DIR/raw_demucs_recombined.wav"

echo "Converting stems to MIDI..."

for STEM in vocals other bass drums
do
    STEM_FILE="$STEM_DIR/$STEM.wav"

    if [ -f "$STEM_FILE" ]; then
        echo "Converting $STEM stem to MIDI..."
        mkdir -p "$MIDI_DIR/$STEM"

        python src/audio_to_midi.py "$STEM_FILE" -o "$MIDI_DIR/$STEM"

        RAW_MIDI=$(find "$MIDI_DIR/$STEM" -name "*.mid" | head -n 1 || true)

        if [ -n "$RAW_MIDI" ]; then
            echo "Cleaning $STEM MIDI..."
            python src/clean_midi.py "$RAW_MIDI" \
                -o "$MIDI_DIR/$STEM/cleaned.mid" \
                --min_note_length 0.00
        fi
    fi
done

echo "Rendering each stem as dynamic 8-bit WAV..."

WAV_FILES=()

render_stem () {
    STEM=$1
    ROLE=$2
    GAIN=$3
    MAX_NOTE_LENGTH=${4:-0.0}

    MIDI_FILE="$MIDI_DIR/$STEM/cleaned.mid"

    if [ ! -f "$MIDI_FILE" ]; then
        echo "Skipping $STEM: no cleaned MIDI found."
        return
    fi

    STEM_WAV="$WAV_DIR/$STEM.wav"

    echo "Rendering $STEM as $ROLE..."
    python src/dynamic_midi_bitify.py "$MIDI_FILE" \
        --style "$STYLE" \
        --force_role "$ROLE" \
        --gain "$GAIN" \
        --max_note_length "$MAX_NOTE_LENGTH" \
        -o "$STEM_WAV"

    WAV_FILES+=("$STEM_WAV")
}

render_stem vocals melody 1.2 0.12
render_stem other arp 0.5 0.0
render_stem bass bass 1.0 0.0
render_stem drums drums 0.8 0.0

if [ ${#WAV_FILES[@]} -eq 0 ]; then
    echo "No stem WAV files were created."
    exit 1
fi

echo "Mixing rendered stem WAVs..."
python src/mix_wavs.py "${WAV_FILES[@]}" -o "$OUTPUT_FILE"

if [ "$KEEP_FILES" != "true" ]; then
    echo "Cleaning temporary files..."
    rm -rf "$TEMP_DIR"
else
    echo "Kept temporary files in: $TEMP_DIR"
    echo "Raw Demucs recombined file:"
    echo "$TEMP_DIR/raw_demucs_recombined.wav"
fi

echo "Saved: $OUTPUT_FILE"