import serial
import csv
import time
import re
import os

porta_seriale = 'COM9'  # Cambia in base al tuo sistema
baudrate = 115200
timeout = 1

intestazioni = ['timestamp', 'vibrazione (m/s^2)', 'frequenza (Hz)', 'temperatura (°C)', 'umidità (%)']
moduli = ['a', 'b', 'c']  # Moduli supportati

# Crea un file CSV per ciascun modulo
file_writer = {}
for modulo in moduli:
    filename = f'modulo_{modulo.upper()}.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(intestazioni)
    file_writer[modulo] = filename

# Buffer e variabili temporanee per ogni modulo
buffer = ''
last_temp = {m: '' for m in moduli}
last_hum = {m: '' for m in moduli}

with serial.Serial(porta_seriale, baudrate, timeout=timeout) as ser:
    print("🟢 Lettura attiva...")

    while True:
        try:
            data = ser.read(ser.in_waiting or 1).decode('utf-8', errors='ignore')
            buffer += data

            # Estrai pacchetti vibrazione/frequenza
            pattern_vib = re.compile(r'([a-z])a([0-9.\-]+)\1b([0-9.\-]+)')
            matches_vib = pattern_vib.findall(buffer)

            for modulo, vib, freq in matches_vib:
                if modulo in moduli:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    filename = file_writer[modulo]
                    with open(filename, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp, vib, freq, last_temp[modulo], last_hum[modulo]])
                    print(f"[{timestamp}] Modulo {modulo.upper()} | Vib: {vib} | Freq: {freq} | Temp: {last_temp[modulo]} | Hum: {last_hum[modulo]}")

            # Rimuovi pacchetti elaborati
            buffer = re.sub(r'[a-z]a[0-9.\-]+[a-z]b[0-9.\-]+', '', buffer)

            # Estrai pacchetti temperatura/umidità
            pattern_env = re.compile(r'([a-z])c([0-9]+\.[0-9]+)\1d([0-9]+\.[0-9]+)')
            matches_env = pattern_env.findall(buffer)

            for modulo, temp, hum in matches_env:
                if modulo in moduli:
                    last_temp[modulo] = temp
                    last_hum[modulo] = hum
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    filename = file_writer[modulo]
                    with open(filename, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp, '', '', temp, hum])
                    print(f"[{timestamp}] Modulo {modulo.upper()} | Temp: {temp} | Hum: {hum}")

            # Rimuovi i pacchetti ambiente elaborati
            buffer = re.sub(r'[a-z]c[0-9]+\.[0-9]+[a-z]d[0-9]+\.[0-9]+', '', buffer)

        except KeyboardInterrupt:
            print("\n🔴 Interrotto.")
            break
        except Exception as e:
            print("❌ Errore:", e)
