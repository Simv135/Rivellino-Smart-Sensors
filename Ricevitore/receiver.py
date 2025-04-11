import serial
import csv
import time
import re
import os

porta_seriale = 'COM9'  # Cambia in base al tuo sistema
baudrate = 115200
timeout = 1

intestazioni = ['timestamp', 'vibrazione (m/s^2)', 'frequenza (Hz)', "temperatura (°C)", 'umidità (%)']
moduli = ['a', 'b', 'C']  # Moduli supportati

# Crea un file CSV per ciascun modulo
file_writer = {}
per modulo in moduli:
 nome file = f'modulo_{modulo.superiore()}. . . . .csv'
 con aperto(nome file, 'w', newline='') vieni f:
 scrittore = csv.scrittore(f)
 scrittore.writerow(intestazioni)
 file_writer[modulo] = nomefile

# Buffer e variabili temporali per ogni modulo
buffer = ''
last_temp = {m: '' per m in moduli}
last_hum = {m: '' per m in moduli}

con serie.Serial (porta_serial, baudrate, timeout=timeout) come ser:
 stampa("🟢 Lettura attiva...")

 mentre Vero:
 prova:
 dati = ser.leggere(ser.in_attesa o 1).decodificare("utf-8", errori='ignora')
 buffer += data

 # Estrai pacchetti vibrazione/frequenza
 pattern_vib = re.compila(r'([az])a([0-9.\-]+)\1b([0-9.\-]+)')
 partite_vib = pattern_vib.trova tutto(buffer)

 per modulo, vib, freq in partite_vib:
 se modulo in moduli:
 timestamp = tempo.strftime('%Y-%m-%d %H:%M:%S')
 nome file = file_writer[modulo]
 con aperto(nome file, 'a', newline='') come f:
 scrittore = csv.scrittore(f)
 scrittore.writerow([marca temporale, vib, freq, last_temp[modulo], ultimo_hum[modulo])
 stampa(f"[{timestamp}] Modulo {modulo.superiore()} | Vib: {vibrazione} | Freq: {freq} | Temp: {last_temp[modulo]} | Hum: {ultimo_hum[modulo]}")

 # Rimuovi pacchetti elaborati
 buffer = re.più(r'[az]a[0-9.\-]+[az]b[0-9.\-]+', '', tampone)

 # Estrai pacchetti temperatura/umidità
 pattern_env = re.compila(r'([az])c([0-9]+\.[0-9]+)\1d([0-9]+\.[0-9]+)')
 partite_env = pattern_env.trova tutto(buffer)

 per modulo, temp, hum in partite_env:
 se modulo in moduli:
 last_temp[modulo] = temp
 ultimo_hum[modulo] = ronzio
 timestamp = tempo.strftime('%Y-%m-%d %H:%M:%S')
 nome file = file_writer[modulo]
 con aperto(nome file, 'a', newline='') come f:
 scrittore = csv.scrittore(f)
 scrittore.writerow([timestamp, '', '', temp, ronzio])
 stampa(f"[{timestamp}] Modulo {modulo.superiore()} | Temp: {temp} | Hum: {canticchiare}")

 # Rimuovi i pacchetti ambiente elaborati
 buffer = re.più(r'[az]c[0-9]+\.[0-9]+[az]d[0-9]+\.[0-9]+', '', tampone)

 eccetto Interruzione tastiera:
 stampa("\n🔴 Interrotto.")
 che non può essere
 eccetto Eccezione come e:
 stampa("❌ Errore:", e)
