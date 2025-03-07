import numpy as np
import sounddevice as sd
import scipy.signal as signal
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

# Global variables
fs = 44100  # Sampling rate
recorded_sample = None  # To hold the recorded audio

def record_sample(duration=2.0):
    """Record audio from the microphone for a specified duration."""
    global recorded_sample, fs
    print("Recording... Speak or play a sound into the mic for {} seconds.".format(duration))
    recorded_sample = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording complete!")
    recorded_sample = recorded_sample.flatten()  # Flatten to a 1D array

def pitch_shift(sample, factor):
    """
    Shifts the pitch of the sample by resampling.
    A factor > 1.0 shifts the pitch up (shortening duration),
    a factor < 1.0 shifts it down (lengthening duration).
    """
    n = len(sample)
    new_length = int(n / factor)
    shifted_sample = signal.resample(sample, new_length)
    return shifted_sample

class SynthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Virtual Synthesizer")
        layout = QVBoxLayout()
        
        label = QLabel("Press a button to play the recorded sample at a shifted pitch:")
        layout.addWidget(label)
        
        btn_lower = QPushButton("Pitch Down (0.8x)")
        btn_lower.clicked.connect(self.play_lower)
        layout.addWidget(btn_lower)
        
        btn_original = QPushButton("Original Pitch (1.0x)")
        btn_original.clicked.connect(self.play_original)
        layout.addWidget(btn_original)
        
        btn_higher = QPushButton("Pitch Up (1.2x)")
        btn_higher.clicked.connect(self.play_higher)
        layout.addWidget(btn_higher)
        
        self.setLayout(layout)
    
    def play_lower(self):
        shifted = pitch_shift(recorded_sample, 0.8)
        sd.play(shifted, samplerate=fs)
    
    def play_original(self):
        sd.play(recorded_sample, samplerate=fs)
    
    def play_higher(self):
        shifted = pitch_shift(recorded_sample, 1.2)
        sd.play(shifted, samplerate=fs)
        
if __name__ == "__main__":
    # First, record a sample from the microphone.
    record_sample(duration=2.0)
    
    # Create and show the GUI.
    app = QApplication(sys.argv)
    window = SynthWindow()
    window.show()
    sys.exit(app.exec_())
