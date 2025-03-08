import numpy as np
import sounddevice as sd
from pynput import keyboard
import sys

# ----------------------------
# Configuration and Constants
# ----------------------------
SAMPLE_RATE = 44100       # Hz
DURATION = 200.0          # Duration of precomputed waveform (seconds)
FADE_IN_DURATION = 0.05   # seconds
FADE_OUT_DURATION = 0.1   # seconds

# ----------------------------
# Key Mapping (Keyboard Layout)
# ----------------------------
# White keys: lower row from "z" to "/" and upper row from "q" to "["
white_lower_keys = list("zxcvbnm,./")  # 10 keys
white_upper_keys = list("qwertyuiop[]")   # 11 keys

# Frequencies for 21 white keys spanning three octaves (C3 to B5)
white_frequencies = [
    # Octave 1: C3 - B3
    130.81, 146.83, 164.81, 174.61, 196.00, 220.00, 246.94,
    # Octave 2: C4 - B4
    261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88,
    # Octave 3: C5 - B5
    523.25, 587.33, 659.25, 698.46, 783.99, 880.00, 987.77, 1046.50
]

white_keys = {}
white_keys.update(dict(zip(white_lower_keys, white_frequencies[:10])))
white_keys.update(dict(zip(white_upper_keys, white_frequencies[10:])))

# Black keys: groups as specified
black_group1 = list("sd")           # 2 keys: C#3, D#3
black_group2 = list("ghj")          # 3 keys: F#3, G#3, A#3
black_group3 = list("l;")           # 2 keys: C#4, D#4
black_group4 = list("234")          # 3 keys: F#4, G#4, A#4
black_group5 = list("67")           # 2 keys: C#5, D#5
black_group6 = list("90-")          # 3 keys: F#5, G#5, A#5

# Frequencies for 15 black keys spanning three octaves
black_frequencies = [
    # Octave 1: C#3, D#3, F#3, G#3, A#3
    138.59, 155.56, 185.00, 207.65, 233.08,
    # Octave 2: C#4, D#4, F#4, G#4, A#4
    277.18, 311.13, 369.99, 415.30, 466.16,
    # Octave 3: C#5, D#5, F#5, G#5, A#5
    554.37, 622.25, 739.99, 830.61, 932.33
]

black_keys = {}
index = 0
for group in [black_group1, black_group2, black_group3, black_group4, black_group5, black_group6]:
    n = len(group)
    black_keys.update(dict(zip(group, black_frequencies[index:index+n])))
    index += n

# Combine white and black keys
KEY_FREQUENCIES = {}
KEY_FREQUENCIES.update(white_keys)
KEY_FREQUENCIES.update(black_keys)

# ----------------------------
# Waveform Generation
# ----------------------------
def generate_saw_wave(freq, sample_rate, duration, fade_in_duration, fade_out_duration):
    """
    Generate a saw wave with a given frequency and duration.
    The wave ramps up from -0.5 to 0.5.
    Fade-in and fade-out envelopes are applied to smooth the transitions.
    Returns a float32 NumPy array.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Create a saw wave: ramps from -0.5 to 0.5.
    wave = 0.5 * (2 * (t * freq - np.floor(t * freq + 0.5)))
    
    # Apply fade-in
    fade_in_samples = int(fade_in_duration * sample_rate)
    if fade_in_samples > 0:
        fade_in = np.linspace(0, 1, fade_in_samples)
        wave[:fade_in_samples] *= fade_in
    # Apply fade-out
    fade_out_samples = int(fade_out_duration * sample_rate)
    if fade_out_samples > 0:
        fade_out = np.linspace(1, 0, fade_out_samples)
        wave[-fade_out_samples:] *= fade_out
        
    return wave.astype(np.float32)

# Precompute waveforms for every key using saw waves
precomputed_waves = { key: generate_saw_wave(freq, SAMPLE_RATE, DURATION, FADE_IN_DURATION, FADE_OUT_DURATION)
                      for key, freq in KEY_FREQUENCIES.items() }

# ----------------------------
# Active Note Management
# ----------------------------
# For each active key, store the current playback position in its waveform.
active_notes = {}

def on_press(key):
    global active_notes, listener
    # Use ESC to exit the program
    if key == keyboard.Key.esc:
        listener.stop()
        return False
    try:
        if hasattr(key, 'char'):
            k = key.char.lower()
            if k in KEY_FREQUENCIES and k not in active_notes:
                active_notes[k] = 0  # Start playback from the beginning
    except Exception as e:
        print(e)

def on_release(key):
    try:
        if hasattr(key, 'char'):
            k = key.char.lower()
            if k in active_notes:
                del active_notes[k]
    except Exception as e:
        print(e)

# ----------------------------
# Audio Callback and Stream
# ----------------------------
def audio_callback(outdata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    combined = np.zeros(frames, dtype=np.float32)
    note_count = len(active_notes)
    for key in list(active_notes.keys()):
        pos = active_notes[key]
        wave = precomputed_waves[key]
        end = pos + frames
        if end > len(wave):
            end = len(wave)
        n_samples = end - pos
        if n_samples > 0:
            combined[:n_samples] += wave[pos:end]
            active_notes[key] = pos + n_samples
        else:
            del active_notes[key]
    if note_count > 0:
        combined /= np.sqrt(note_count)
    outdata[:] = combined.reshape(-1, 1)

stream = sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype='float32',
    latency='low',
    callback=audio_callback
)
stream.start()

# ----------------------------
# Keyboard Listener and Main Loop
# ----------------------------
listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True)
listener.start()

try:
    listener.join()
except KeyboardInterrupt:
    print("Ctrl+C detected. Exiting program.")
finally:
    stream.stop()
    stream.close()