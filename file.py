import wave
import numpy as np
import pyrubberband as pyrb

# Input / output
input_file = "springchicken-b4.raw"
output_file = "springchicken-b4.wav"

# C64 constants
region = input("Enter region (PAL/NTSC): ").strip().upper()
if region == "PAL":
    sample_rate = 16750
elif region == "NTSC":
    sample_rate = 17430.8943
else:
    raise ValueError("Region must be PAL or NTSC")

print(f"Calculated sample rate: {sample_rate:.2f} Hz")

# Read raw
with open(input_file, "rb") as f:
    raw_bytes = f.read()

# Convert bytes to nibbles
samples = []
for b in raw_bytes:
    upper = (b >> 4) & 0x0F
    lower = b & 0x0F
    samples.append(upper * 17)
    samples.append(lower * 17)

# Convert to numpy array
audio = np.array(samples, dtype=np.float32) / 255.0  # scale 0-1

audio_out = np.clip(audio * 255, 0, 255).astype(np.uint8)

# Write WAV
with wave.open(output_file, "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(1)
    wav_file.setframerate(int(sample_rate))
    wav_file.writeframes(audio_out.tobytes())

print(f"WAV saved: {output_file}")
