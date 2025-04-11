import serial
import csv
import time
import re
import os

porta_seriale = 'COM9'  # Cambia se necessario
baudrate = 115200
timeout = 1

# File per ogni tipo di misurazione
file_temp_hum = 'temperatura_umidita.csv'
file_vib_freq = 'vibrazioni.csv'
file_allagamento = 'allagamento.csv'
file_qualita_aria = 'qualita_aria.csv'

# Intestazioni
intestazioni_temp_hum = ['timestamp', 'modulo', 'temperatura (°C)', 'umidità (%)']
intestazioni_vib_freq = ['timestamp', 'modulo', 'vibrazione (m/s^2)', 'frequenza (Hz)']
intestazioni_allagamento = ['timestamp', 'modulo', 'stato_allagamento']
intestazioni_aria = ['timestamp', 'modulo', 'qualita_aria']

# Inizializza i file con intestazioni
for file_name, headers in [
    (file_temp_hum, intestazioni_temp_hum),
    (file_vib_freq, intestazioni_vib_freq),
    (file_allagamento, intestazioni_allagamento),
    (file_qualita_aria, intestazioni_aria)
]:
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

# Variabili
buffer = ''
last_temp = {}
last_hum = {}

with serial.Serial(porta_seriale, baudrate, timeout=timeout) as ser:
    print("🟢 Lettura attiva...")

    while True:
        try:
            data = ser.read(ser.in_waiting or 1).decode('utf-8', errors='ignore')
            buffer += data

            # PACCHETTI VIBRAZIONE/FREQUENZA (es: aa1.23ab19.61)
            pattern_vib = re.compile(r'([a-z])a([0-9.\-]+)\1b([0-9.\-]+)')
            for modulo, vib, freq in pattern_vib.findall(buffer):
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                with open(file_vib_freq, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo.upper(), vib, freq])
                print(f"[{timestamp}] Vibrazione | Modulo {modulo.upper()} | Vib: {vib} | Freq: {freq}")

            buffer = re.sub(r'[a-z]a[0-9.\-]+[a-z]b[0-9.\-]+', '', buffer)

            # PACCHETTI TEMPERATURA/UMIDITÀ (es: ac27.83ad45.20)
            pattern_env = re.compile(r'([a-z])c([0-9]+\.[0-9]+)\1d([0-9]+\.[0-9]+)')
            for modulo, temp, hum in pattern_env.findall(buffer):
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                with open(file_temp_hum, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo.upper(), temp, hum])
                print(f"[{timestamp}] Ambiente | Modulo {modulo.upper()} | Temp: {temp} | Hum: {hum}")

            buffer = re.sub(r'[a-z]c[0-9]+\.[0-9]+[a-z]d[0-9]+\.[0-9]+', '', buffer)

            # TODO: Allagamento (es: ae0 -> nessun allagamento | ae1 -> allagamento)
            pattern_allagamento = re.compile(r'([a-z])e([01])')
            for modulo, stato in pattern_allagamento.findall(buffer):
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                with open(file_allagamento, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo.upper(), 'ALLAGAMENTO' if stato == '1' else 'OK'])
                print(f"[{timestamp}] Allagamento | Modulo {modulo.upper()} | Stato: {'ALLAGAMENTO' if stato == '1' else 'OK'}")

            buffer = re.sub(r'[a-z]e[01]', '', buffer)

            # TODO: Qualità dell'aria (es: af12.5 -> valore qualità)
            pattern_aria = re.compile(r'([a-z])f([0-9]+\.[0-9]+)')
            for modulo, valore in pattern_aria.findall(buffer):
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                with open(file_qualita_aria, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo.upper(), valore])
                print(f"[{timestamp}] Aria | Modulo {modulo.upper()} | Qualità: {valore}")

            buffer = re.sub(r'[a-z]f[0-9]+\.[0-9]+', '', buffer)

        except KeyboardInterrupt:
            print("\n🔴 Interrotto manualmente.")
            break
        except Exception as e:
            print(f"❌ Errore: {e}")
