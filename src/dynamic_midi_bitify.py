from pathlib import Path
import argparse
import numpy as np
import pretty_midi
import soundfile as sf

from synth import generate_wave, midi_note_to_frequency

parser = argparse.ArgumentParser(
    description="Convert MIDI into arranged 8-bit WAV using melody, bass, arpeggio, and drums roles."
)

parser.add_argument("input_file")
parser.add_argument("-o", "--output", default="audio/output/dynamic_8bit.wav")
parser.add_argument("--style", default="nes", choices=["nes", "gameboy", "genesis"])
parser.add_argument("--sample_rate", type=int, default=44100)
parser.add_argument("--tempo", type=float, default=0.055)
parser.add_argument(
    "--force_role",
    choices=["melody", "arp", "bass", "drums"],
    default=None
)
parser.add_argument("--gain", type=float, default=1.0)
parser.add_argument(
    "--max_note_length",
    type=float,
    default=0.0,
    help="Split notes longer than this many seconds. 0 disables splitting."
)

args = parser.parse_args()

sample_rate = args.sample_rate
output_path = Path(args.output)
output_path.parent.mkdir(parents=True, exist_ok=True)

midi_data = pretty_midi.PrettyMIDI(args.input_file)
duration_seconds = midi_data.get_end_time()
audio_samples = np.zeros(int(duration_seconds * sample_rate) + 1)


def envelope(length):
    env = np.ones(length)

    attack = min(int(0.003 * sample_rate), length // 2)
    release = min(int(0.018 * sample_rate), length // 2)

    if attack > 0:
        env[:attack] = np.linspace(0, 1, attack)

    if release > 0:
        env[-release:] = np.linspace(1, 0, release)

    return env


def noise_burst(length, kind="hat"):
    noise = np.random.uniform(-1, 1, length)

    if kind == "kick":
        decay = np.linspace(1.0, 0.0, length) ** 3
        return noise * decay * 0.6

    if kind == "snare":
        decay = np.linspace(1.0, 0.0, length) ** 2
        return noise * decay

    decay = np.linspace(1.0, 0.0, length) ** 5
    return noise * decay * 0.5


def classify_note(note, instrument):
    if args.force_role is not None:
        return args.force_role

    if instrument.is_drum:
        return "drums"

    if note.pitch < 48:
        return "bass"

    if note.pitch >= 72:
        return "melody"

    return "arp"


def role_wave(role):
    if args.style == "genesis":
        return {
            "melody": "sawtooth",
            "bass": "triangle",
            "arp": "square",
        }.get(role, "square")

    return {
        "melody": "square",
        "bass": "triangle",
        "arp": "square",
    }.get(role, "square")


def add_note(start_sample, end_sample, pitch, velocity, wave_type, volume_scale):
    note_length = max(0, end_sample - start_sample)

    if note_length <= 0:
        return

    time_points = np.arange(note_length) / sample_rate
    frequency_hz = midi_note_to_frequency(pitch)

    wave = generate_wave(frequency_hz, time_points, wave_type)
    wave *= envelope(note_length)

    volume = velocity / 127
    audio_samples[start_sample:end_sample] += wave * volume * volume_scale


def add_split_note(start_sample, end_sample, pitch, velocity, wave_type, volume_scale):
    if args.max_note_length <= 0:
        add_note(start_sample, end_sample, pitch, velocity, wave_type, volume_scale)
        return

    max_samples = int(args.max_note_length * sample_rate)

    if max_samples <= 0:
        add_note(start_sample, end_sample, pitch, velocity, wave_type, volume_scale)
        return

    current = start_sample

    while current < end_sample:
        chunk_end = min(current + max_samples, end_sample)

        add_note(
            current,
            chunk_end,
            pitch,
            velocity,
            wave_type,
            volume_scale,
        )

        current = chunk_end


def add_arpeggio(note_group):
    if not note_group:
        return

    start = min(n.start for n in note_group)
    end = max(n.end for n in note_group)
    velocity = int(np.mean([n.velocity for n in note_group]))
    pitches = sorted({n.pitch for n in note_group})

    current = start
    step_index = 0

    while current < end:
        step_end = min(current + args.tempo, end)
        pitch = pitches[step_index % len(pitches)]

        add_note(
            int(current * sample_rate),
            int(step_end * sample_rate),
            pitch,
            velocity,
            "square",
            0.11,
        )

        current = step_end
        step_index += 1


arp_buckets = {}

for instrument in midi_data.instruments:
    for note in instrument.notes:
        role = classify_note(note, instrument)

        start_sample = int(note.start * sample_rate)
        end_sample = int(note.end * sample_rate)

        if role == "drums":
            drum_kind = "hat"

            if note.pitch in [35, 36]:
                drum_kind = "kick"
            elif note.pitch in [38, 40]:
                drum_kind = "snare"

            length = max(
                1,
                min(end_sample - start_sample, int(0.18 * sample_rate))
            )

            audio_samples[start_sample:start_sample + length] += (
                noise_burst(length, drum_kind)
                * (note.velocity / 127)
                * 0.22
            )

        elif role == "bass":
            add_note(
                start_sample,
                end_sample,
                note.pitch,
                note.velocity,
                role_wave(role),
                0.18,
            )

        elif role == "melody":
            add_split_note(
                start_sample,
                end_sample,
                note.pitch,
                note.velocity,
                role_wave(role),
                0.16,
            )

        else:
            bucket = round(note.start / 0.10) * 0.10
            arp_buckets.setdefault(bucket, []).append(note)


for notes in arp_buckets.values():
    if len(notes) >= 2:
        add_arpeggio(notes)
    else:
        note = notes[0]
        add_split_note(
            int(note.start * sample_rate),
            int(note.end * sample_rate),
            note.pitch,
            note.velocity,
            "square",
            0.10,
        )


audio_samples *= args.gain
audio_samples = np.clip(audio_samples, -1.0, 1.0)

sf.write(output_path, audio_samples, sample_rate)

print(f"Saved dynamic 8-bit audio to {output_path}")