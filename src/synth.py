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

# to prevent sudden cuts/static apply a fade in and fade out on every note
# this will make the audio sound more smooth particualrly for triangle notes that have sharp peak.
def apply_envelope(wave, sample_rate, attack_ms=3, release_ms=8):
    attack_samples = int(sample_rate * attack_ms / 1000)
    release_samples = int(sample_rate * release_ms / 1000)

    envelope = np.ones(len(wave))

    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, min(attack_samples, len(wave)))

    if release_samples > 0:
        envelope[-release_samples:] = np.linspace(1, 0, min(release_samples, len(wave)))

    return wave * envelope