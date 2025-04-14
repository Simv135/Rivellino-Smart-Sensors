import serial
import csv
import os
import time

porta_seriale = 'COM9'  # Cambia con la tua porta seriale
baudrate = 115200
timeout = 1

# Mappa: tipo di pacchetto → (file CSV, intestazioni, modulo associato)
pacchetti = {
    'a': ('batteria.csv',     ['timestamp', 'modulo', 'batteria (%)'], 'b'),
    'b': ('batteria.csv',     ['timestamp', 'modulo', 'batteria (%)'], 'c'),
    'c': ('temperatura.csv',  ['timestamp', 'modulo', 'temperatura (°C)'], 'a'),
    'd': ('temperatura.csv',  ['timestamp', 'modulo', 'temperatura (°C)'], 'b'),
    'e': ('temperatura.csv',  ['timestamp', 'modulo', 'temperatura (°C)'], 'c'),
    'f': ('umidita.csv',      ['timestamp', 'modulo', 'umidita (%)'], 'a'),
    'g': ('umidita.csv',      ['timestamp', 'modulo', 'umidita (%)'], 'b'),
    'h': ('umidita.csv',      ['timestamp', 'modulo', 'umidita (%)'], 'c'),
    'i': ('qualita_aria.csv', ['timestamp', 'modulo', 'CO (ppm)'], 'a'),
    'j': ('qualita_aria.csv', ['timestamp', 'modulo', 'NO2 (ppm)'], 'b'),
    'k': ('vibrazioni.csv',   ['timestamp', 'modulo', 'frequenza (Hz)'], 'a'),
    'l': ('vibrazioni.csv',   ['timestamp', 'modulo', 'vibrazione (m/s^2)'], 'a'),
    'm': ('allagamento.csv',  ['timestamp', 'modulo', 'stato_allagamento'], 'b')
}

# Crea file CSV con intestazioni, se non esistono
for chiave, (file, intestazioni, modulo) in pacchetti.items():
    if not os.path.exists(file):
        with open(file, 'w', newline='') as f:
            csv.writer(f).writerow(intestazioni)

# Lettura dalla seriale
with serial.Serial(porta_seriale, baudrate, timeout=timeout) as ser:
    print("🟢 Lettura attiva... (CTRL+C per interrompere)\n")

    while True:
        try:
            riga = ser.readline().decode('utf-8', errors='ignore').strip()
            if not riga or len(riga) < 2:
                continue

            tipo = riga[0]
            valore = riga[1:]

            if tipo not in pacchetti:
                print(f"⚠️ Tipo sconosciuto: {riga}")
                continue

            file_csv, intestazioni, modulo = pacchetti[tipo]
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            dati = [timestamp, modulo.upper(), valore]
            print(f"[{timestamp}] {intestazioni[2]} | Modulo {modulo.upper()} | Valore: {valore}")

            with open(file_csv, 'a', newline='') as f:
                csv.writer(f).writerow(dati)

        except KeyboardInterrupt:
            print("\n🔴 Interrotto manualmente.")
            break
        except Exception as e:
            print(f"❌ Errore: {e}")
