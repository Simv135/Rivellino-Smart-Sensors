import serial
import re
import csv
import os
from datetime import datetime

# === Configurazione ===
PORT = 'COM9'
BAUD_RATE = 115200

# === Percorsi dei file CSV ===
CSV_FILES = {
    'env': 'temperatura_umidita.csv',
    'vib': 'vibrazioni.csv',
    'flood': 'allagamento.csv',
    'air': 'aria.csv',
    'battery': 'batterie.csv'
}

# === Mappa identificatori ===
id_map = {
    'a': ('battery', 'b'),
    'b': ('battery', 'c'),
    'c': ('temperatura', 'a', 'env'),
    'd': ('temperatura', 'b', 'env'),
    'e': ('temperatura', 'c', 'env'),
    'f': ('umidità', 'a', 'env'),
    'g': ('umidità', 'b', 'env'),
    'h': ('umidità', 'c', 'env'),
    'i': ('aria (CO)', 'a', 'air'),
    'j': ('aria (NO2)', 'b', 'air'),
    'k': ('vibrazione', 'a', 'vib'),
    'l': ('vibrazione', 'a', 'vib'),
    'm': ('allagamento', 'b', 'flood'),
}

# === Inizializza file CSV se non esistono ===
def init_csv_files():
    for key, file in CSV_FILES.items():
        if not os.path.exists(file):
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                if key == 'vib':
                    writer.writerow(['timestamp', 'modulo', 'vibrazione (m/s^2)', 'frequenza (Hz)'])
                elif key == 'env':
                    writer.writerow(['timestamp', 'modulo', 'temperatura (°C)', 'umidità (%)'])
                elif key == 'air':
                    writer.writerow(['timestamp', 'modulo', 'aria'])
                elif key == 'flood':
                    writer.writerow(['timestamp', 'modulo', 'allagamento'])
                elif key == 'battery':
                    writer.writerow(['timestamp', 'modulo', 'batteria (%)'])

# === Parsing riga ricevuta ===
def parse_line(line):
    return re.findall(r'([a-z])([-+]?[0-9]*\.?[0-9]+)', line)

# === Scrittura nei file CSV ===
def write_to_csv(category, row):
    filename = CSV_FILES[category]
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

# === Funzione per gestire la scrittura sincronizzata della temperatura e umidità ===
def handle_env_data(timestamp, modulo, temperature, humidity):
    # Se ci sono entrambi i valori di temperatura e umidità, li scriviamo sulla stessa riga
    if temperature is not None and humidity is not None:
        write_to_csv('env', [timestamp, modulo, temperature, humidity])

# === Main loop ===
def main():
    init_csv_files()
    temp_data = {}  # Buffer temporaneo per memorizzare i dati

    try:
        with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
            print(f"[INFO] Lettura da {PORT} a {BAUD_RATE} baud...\n")
            while True:
                raw_line = ser.readline().decode('utf-8').strip()
                if raw_line:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    pairs = parse_line(raw_line)

                    for code, value in pairs:
                        if code in id_map:
                            mapping = id_map[code]
                            category = mapping[0]
                            modulo = mapping[1]
                            
                            # Gestione del caso con 3 valori (per vibrazione)
                            if len(mapping) == 3:
                                category = mapping[2]  # Aggiorna la categoria per il caso 'vibrazione'

                            if category == 'vib':
                                # Dati delle vibrazioni (frequenza e intensità)
                                if code == 'k':
                                    temp_data['freq'] = float(value)
                                elif code == 'l':
                                    temp_data['intensity'] = float(value)
                                    if 'freq' in temp_data and 'intensity' in temp_data:
                                        write_to_csv('vib', [timestamp, modulo, temp_data['intensity'], temp_data['freq']])
                                        temp_data.clear()
                            elif category == 'flood':
                                write_to_csv(category, [timestamp, modulo, value])
                            elif category == 'env':
                                # Gestione temperatura e umidità
                                if code == 'c' or code == 'd' or code == 'e':  # Temperature
                                    temp_data['temperature'] = value if value else None
                                elif code == 'f' or code == 'g' or code == 'h':  # Humidity
                                    temp_data['humidity'] = value if value else None
                                    
                                # Quando entrambi i dati sono disponibili, scrivi sulla stessa riga
                                if 'temperature' in temp_data and 'humidity' in temp_data:
                                    handle_env_data(timestamp, modulo, temp_data.get('temperature'), temp_data.get('humidity'))
                                    temp_data.clear()

                            elif category == 'battery':
                                write_to_csv(category, [timestamp, modulo, value])
                            else:
                                write_to_csv(category, [timestamp, modulo, value])
    except serial.SerialException as e:
        print(f"[ERRORE] Errore seriale: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Interrotto dall'utente.")

if __name__ == '__main__':
    main()
