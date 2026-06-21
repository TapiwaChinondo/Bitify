#!/bin/bash

set -e

echo "Cleaning output directories..."

rm -rf audio/output/*
rm -rf audio/temp_direct
rm -rf audio/temp_demucs
rm -rf audio/separated

echo "Done."