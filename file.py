import wave
import numpy as np
import pyrubberband as pyrb

# input / output
input_file = "springchicken-b4.raw"
output_file = "springchicken-b4.wav"

# commodore 64 constants
region = input("enter region (PAL/NTSC): ").strip().upper()
if region == "PAL":
    sample_rate = 16750
elif region == "NTSC":
    sample_rate = 17430.8943
else:
    raise ValueError("region must be PAL or NTSC")

print(f"calculated de sample rate: {sample_rate:.2f} Hz")

# read raw binary
with open(input_file, "rb") as f:
    raw_bytes = f.read()

# convert bytes to nibbles
samples = []
for b in raw_bytes:
    upper = (b >> 4) & 0x0F
    lower = b & 0x0F
    samples.append(upper * 17)
    samples.append(lower * 17)

# convert to numpy array
audio = np.array(samples, dtype=np.float32) / 255.0  # scale 0-1

audio_out = np.clip(audio * 255, 0, 255).astype(np.uint8)

# write microsoft wave
with wave.open(output_file, "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(1)
    wav_file.setframerate(int(sample_rate))
    wav_file.writeframes(audio_out.tobytes())

print(f"wav saved: {output_file}")

