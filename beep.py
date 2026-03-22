import serial
import pygame
import numpy as np
import time

pygame.mixer.init(frequency=44100, size=-16, channels=2)

def make_beep(frequency=1000, duration=0.2, volume=0.5):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    wave = np.sin(2 * np.pi * frequency * t)

    # fade (envelope)
    fade_len = int(sample_rate * 0.01)
    envelope = np.ones_like(wave)
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)

    wave *= envelope

    audio = (wave * (2**15 - 1) * volume).astype(np.int16)

    # make it stereo: shape becomes (samples, 2)
    stereo_audio = np.column_stack((audio, audio))

    return pygame.sndarray.make_sound(stereo_audio)

beep = make_beep(1000, 0.15)
interval = .5

with serial.Serial('COM3', 9600, timeout=1) as ser:
    time.sleep(2)

    last_beep_time = 0 

    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue

        level = int(line)
        now = time.time()

        interval = {1 : 1, 2 : .75, 3: .5, 4: .25, 5: .15}

        if level and now - last_beep_time >= interval[level]:
            beep.play()
            last_beep_time = now