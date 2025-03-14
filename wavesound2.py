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

baseFrequency = 16.352

def nF(noteNum):
    freq = baseFrequency*pow(pow(2,(1/12)),noteNum)
    return freq

# White key frequencies (3 octaves, 7 keys per octave = 21 keys)
white_frequencies = [
    # Octave 1 (C3 - B3)
    nF(0), nF(2), nF(4), nF(5), nF(7), nF(9), nF(11),
    # Octave 2 (C4 - B4)
    nF(12), nF(14), nF(16), nF(17), nF(19), nF(21), nF(23),
    # Octave 3 (C5 - B5)zz
    nF(24), nF(26), nF(28), nF(29), nF(31), nF(33), nF(35), nF(36)
]
# White keys: lower row from "z" to "/" (10 keys) and upper row from "q" to "[" (11 keys)
white_lower_keys = list("zxcvbnm,./")  # 10 keys
white_upper_keys = list("qwertyuiop[]")  # 11 keys

white_keys = {}
white_keys.update(dict(zip(white_lower_keys, white_frequencies[:10])))
white_keys.update(dict(zip(white_upper_keys, white_frequencies[10:])))

# Black key frequencies (3 octaves, 5 black keys per octave = 15 keys)
black_frequencies = [
    # Octave 1 (C#3, D#3, F#3, G#3, A#3)
    nF(1), nF(3), nF(6), nF(8), nF(10),
    # Octave 2 (C#4, D#4, F#4, G#4, A#4)
    nF(13), nF(15), nF(18), nF(20), nF(22),
    # Octave 3 (C#5, D#5, F#5, G#5, A#5)
    nF(25), nF(27), nF(30), nF(32), nF(34)
]

# Black keys: groups defined as follows
black_lower_keys = list("sdghjl;") # 7 keys
black_upper_keys = list("2346790-") # 8 keys

black_keys = {}
black_keys.update(dict(zip(black_lower_keys, black_frequencies[:10])))
black_keys.update(dict(zip(black_upper_keys, black_frequencies[7:])))

# Combine all key mappings into one dictionary
Key_FREQUENCIES = {}
Key_FREQUENCIES.update(white_keys)
Key_FREQUENCIES.update(black_keys)

# ----------------------------
# Waveform Generation
# ----------------------------
def generate_cos_wave(freq, sample_rate, duration, fade_in_duration, fade_out_duration):
    """
    Generate a cosine waveform with fade-in and fade-out.
    Returns a float32 NumPy array.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.cos(2 * np.pi * freq * t)
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

# Precompute waveforms for every key

wave_set = {}
for i in range(53):
    for j in Key_FREQUENCIES:
        Key_FREQUENCIES[j] = Key_FREQUENCIES[j]*pow(pow(2,(1/12)),i)
    precomputed_waves = { key: generate_cos_wave(freq, SAMPLE_RATE, DURATION, FADE_IN_DURATION, FADE_OUT_DURATION)
                for key, freq in Key_FREQUENCIES.items() }
    wave_set[i] = precomputed_waves
    print(i)

current_set = {}
current_set_num = 1

# ----------------------------
# Active Note Management
# ----------------------------
# For each active key, store the current playback index in its waveform.
active_notes = {}


def on_press(key):
    global active_notes, listener, baseFrequency, stream, precomputed_waves,Key_FREQUENCIES
    # Allow ESC to exit the program
    if key == keyboard.Key.esc:
        listener.stop()
        return False
    if key == keyboard.Key.up:
        if current_set == 53:
            Print("Highest Bound Reached")
        else:
            current_set += 1
            current_set = wave_set[current_set]
    if key == keyboard.Key.down:
        if current_set == 1:
            Print("Lowest Bound Reached")
        else:
            current_set -= 1
            current_set = wave_set[current_set]
    try:
        if hasattr(key, 'char'):
            k = key.char.lower()
            if k in Key_FREQUENCIES and len(active_notes) < 10 and k not in active_notes:
                active_notes[k] = 0  # Start playing from the beginning
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
    # Prepare an empty buffer for the callback
    combined = np.zeros(frames, dtype=np.float32)
    note_count = len(active_notes)
    # For each active note, add its next segment to the combined buffer.
    for key in list(active_notes.keys()):
        pos = active_notes[key]
        wave = current_set[key]
        end = pos + frames
        if end > len(wave):
            end = len(wave)
        n_samples = end - pos
        if n_samples > 0:
            combined[:n_samples] += wave[pos:end]
            active_notes[key] = pos + n_samples
        else:
            del active_notes[key]
    # Mix the notes without excessive attenuation.
    # Divide by sqrt(note_count) to preserve clarity.
    if note_count > 0:
        combined /= np.sqrt(note_count)
    outdata[:] = combined.reshape(-1, 1)

# Create and start the output stream
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
