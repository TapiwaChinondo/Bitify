#!/bin/bash

set -e

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install librosa numpy scipy soundfile streamlit
pip install pretty_midi mido
pip install basic-pitch
pip install demucs
pip install torchcodec
#brew install ffmpeg
pip install mt3-infer

echo "complete"
echo "run source .venv/bin/activate"  