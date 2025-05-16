from machine import I2S, Pin
import array
import time

# === Pin config (adjust if you used different ones) ===
BCLK_PIN = 12   # Bit clock
WS_PIN   = 15   # Word select (LRCL)
SD_PIN   = 13   # Serial data from mic

# === I2S Config ===
i2s = I2S(
    0,                              # I2S peripheral ID
    sck=Pin(BCLK_PIN),              # BCLK
    ws=Pin(WS_PIN),                 # LRCL / Word Select
    sd=Pin(SD_PIN),                 # Serial data input
    mode=I2S.RX,                    # Receive mode
    bits=32,                        # 32-bit samples (SPH0645 outputs 24-bit in 32-bit frames)
    format=I2S.MONO,                # Mono channel
    rate=48000,                     # Sample rate in Hz
    ibuf=4096                       # Internal buffer size
)

# === Allocate buffer for 100 samples (100 * 4 bytes = 400 bytes) ===
buf = bytearray(400)

print("Reading I2S mic data...")
time.sleep(1)

# === Read samples ===
num_bytes = i2s.readinto(buf)
print(f"Read {num_bytes} bytes from mic")

# === Convert to integers and print a few ===
samples = array.array("i", buf[:num_bytes])

print("First 10 audio samples:")
print(samples[:10])

# === Cleanup ===
i2s.deinit()