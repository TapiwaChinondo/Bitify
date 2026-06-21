import numpy as np
import random


# convert a note number to a real frequency
def midi_note_to_frequency(note_number):
    return 440.0 * (2 ** ((note_number - 69) / 12))


# Generate the specified sound wave
def generate_wave(frequency_hz, time_points, wave_type="square"):

    #  NES sound
    if wave_type == "square":
        return np.sign(
            np.sin(2 * np.pi * frequency_hz * time_points)
        )

    #  Game Boy
    elif wave_type == "triangle":
        return (
            2 * np.abs(
                2 * ((frequency_hz * time_points) % 1) - 1
            ) - 1
        )

    # Smooth
    elif wave_type == "sine":
        return np.sin(
            2 * np.pi * frequency_hz * time_points
        )

    # SEGA Genesis
    elif wave_type == "sawtooth":
        return (
            2 * ((frequency_hz * time_points) % 1)
        ) - 1

    else:
        raise ValueError(f"Unknown wave type: {wave_type}")

def choose_wave_type(mode):
    if mode == "gameboy":
        return "triangle"

    if mode == "nes":
        return "square"
    
    if mode == "genesis":
        return "sawtooth"
    
    if mode == "sine":
        return "sine"

    if mode == "mixed":
        return random.choice([
            "square",
            "triangle",
            "sine",
            "sawtooth"
        ])
        
    return mode