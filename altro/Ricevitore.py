import serial
import csv
import time

porta_seriale = 'COM9'  # Modifica se necessario
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

# Inizializza i file con intestazioni se non esistono
for file_name, headers in [
    (file_temp_hum, intestazioni_temp_hum),
    (file_vib_freq, intestazioni_vib_freq),
    (file_allagamento, intestazioni_allagamento),
    (file_qualita_aria, intestazioni_aria)
]:
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

# Inizio lettura dalla seriale
with serial.Serial(porta_seriale, baudrate, timeout=timeout) as ser:
    print("🟢 Lettura attiva... (Premi CTRL+C per uscire)")

    while True:
        try:
            riga = ser.readline().decode('utf-8', errors='ignore').strip()
            if not riga:
                continue

            parti = riga.split(',')

            if len(parti) < 3:
                print(f"⚠️ Riga ignorata: {riga}")
                continue

            modulo = parti[0].strip().upper()
            tipo = parti[1].strip().lower()
            valori = parti[2:]

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            if tipo == 'ambiente' and len(valori) == 2:
                temp, hum = valori
                with open(file_temp_hum, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo, temp, hum])
                print(f"[{timestamp}] Ambiente | Modulo {modulo} | Temp: {temp} | Hum: {hum}")

            elif tipo == 'vibrazione' and len(valori) == 2:
                vib, freq = valori
                with open(file_vib_freq, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo, vib, freq])
                print(f"[{timestamp}] Vibrazione | Modulo {modulo} | Vib: {vib} | Freq: {freq}")

            elif tipo == 'allagamento' and len(valori) == 1:
                stato = 'ALLAGAMENTO' if valori[0] == '1' else 'OK'
                with open(file_allagamento, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo, stato])
                print(f"[{timestamp}] Allagamento | Modulo {modulo} | Stato: {stato}")

            elif tipo == 'aria' and len(valori) == 1:
                qualita = valori[0]
                with open(file_qualita_aria, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, modulo, qualita])
                print(f"[{timestamp}] Aria | Modulo {modulo} | Qualità: {qualita}")

            else:
                print(f"⚠️ Formato sconosciuto: {riga}")

        except KeyboardInterrupt:
            print("\n🔴 Interrotto manualmente.")
            break
        except Exception as e:
            print(f"❌ Errore: {e}")
