import serial
import pygame
import time
import keyboard

pygame.mixer.init()

beep = pygame.mixer.Sound('beep.wav')

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
            
        if keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
            break
        