import serial
import serial.tools.list_ports
import re
import csv
import os
from datetime import datetime

BAUD_RATE = 115200

# Definizione costante dei file CSV
CSV_FILES = {
    'env': 'temperatura_umidita.csv',
    'vib': 'vibrazioni.csv',
    'flood': 'allagamento.csv',
    'air': 'aria.csv',
    'battery': 'batterie.csv'
}

# Mappatura completa degli ID dei sensori con relative informazioni
id_map = {
    # ID: (nome, modulo, categoria_file, unità_misura)
    'a': ('batteria', 'b', 'battery', '%'),
    'b': ('batteria', 'c', 'battery', '%'),
    'c': ('temperatura', 'a', 'env', '°C'),
    'd': ('temperatura', 'b', 'env', '°C'),
    'e': ('temperatura', 'c', 'env', '°C'),
    'f': ('umidità', 'a', 'env', '%'),
    'g': ('umidità', 'b', 'env', '%'),
    'h': ('umidità', 'c', 'env', '%'),
    'i': ('CO', 'a', 'air', 'ppm'),
    'j': ('NO2', 'b', 'air', 'ppm'),
    'k': ('frequenza', 'a', 'vib', 'Hz'),
    'l': ('vibrazione', 'a', 'vib', 'm/s²'),
    'm': ('allagamento', 'b', 'flood', 'True/False')
}

def init_csv_files():
    #Inizializza tutti i file CSV con le intestazioni corrette
    csv_headers = {
        'env': ['timestamp', 'modulo', 'temperatura (°C)', 'umidità (%)'],
        'vib': ['timestamp', 'modulo', 'vibrazione (m/s²)', 'frequenza (Hz)'],
        'air': ['timestamp', 'modulo', 'CO (ppm)', 'NO2 (ppm)'],
        'flood': ['timestamp', 'modulo', 'allagamento'],
        'battery': ['timestamp', 'modulo', 'batteria (%)']
    }
    
    for category, filename in CSV_FILES.items():
        # Crea il file solo se non esiste
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(csv_headers[category])
            print(f"[INFO] Creato file {filename} con intestazioni")

def parse_line(line):
    #Estrae i dati dalla linea ricevuta dalla porta seriale
    #Trova tutte le coppie ID-valore nella linea
    matches = re.findall(r'([a-z])([-+]?[0-9]*\.?[0-9]+)', line)
    return matches

def write_to_csv(category, row):
    #Scrive una riga di dati nel file CSV appropriato
    filename = CSV_FILES[category]
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def find_working_port():
    #Trova una porta seriale funzionante
    try:
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            try:
                with serial.Serial(port.device, BAUD_RATE, timeout=2) as ser:
                    ser.write(b'\n')
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        return port.device
            except (serial.serialutil.SerialException, UnicodeDecodeError):
                continue
    except Exception as e:
        print(f"[ERRORE] Errore durante la ricerca delle porte: {e}")
    return None

def process_data(timestamp, pairs):
    #Elabora i dati ricevuti e li scrive nei file CSV appropriati
    # Dati temporanei per accoppiare sensori correlati
    temp_data = {
        'env': {},      # Per temperatura e umidità
        'vib': {},      # Per frequenza e intensità vibrazione
        'air': {}       # Per CO e NO2
    }
    
    for code, value in pairs:
        if code in id_map:
            name, modulo, category, _ = id_map[code]
            
            # Gestione diversa in base alla categoria
            if category == 'vib':
                if code == 'k':  # Frequenza
                    temp_data['vib']['freq'] = float(value)
                elif code == 'l':  # Intensità vibrazione
                    temp_data['vib']['intensity'] = float(value)
                
                # Se abbiamo entrambi i valori, salviamo nel CSV
                if 'freq' in temp_data['vib'] and 'intensity' in temp_data['vib']:
                    write_to_csv('vib', [
                        timestamp, 
                        modulo, 
                        temp_data['vib']['intensity'], 
                        temp_data['vib']['freq']
                    ])
                    temp_data['vib'].clear()
            
            elif category == 'env':
                # Identifichiamo se è temperatura o umidità
                if code in ['c', 'd', 'e']:  # Temperature
                    if modulo not in temp_data['env']:
                        temp_data['env'][modulo] = {}
                    temp_data['env'][modulo]['temp'] = value
                elif code in ['f', 'g', 'h']:  # Umidità
                    if modulo not in temp_data['env']:
                        temp_data['env'][modulo] = {}
                    temp_data['env'][modulo]['hum'] = value
                
                # Se abbiamo sia temperatura che umidità per lo stesso modulo, salviamo
                if modulo in temp_data['env'] and 'temp' in temp_data['env'][modulo] and 'hum' in temp_data['env'][modulo]:
                    write_to_csv('env', [
                        timestamp, 
                        modulo, 
                        temp_data['env'][modulo]['temp'], 
                        temp_data['env'][modulo]['hum']
                    ])
                    del temp_data['env'][modulo]
            
            elif category == 'air':
                if code == 'i':  # CO
                    if 'a' not in temp_data['air']:
                        temp_data['air']['a'] = {}
                    temp_data['air']['a']['CO'] = value
                elif code == 'j':  # NO2
                    if 'b' not in temp_data['air']:
                        temp_data['air']['b'] = {}
                    temp_data['air']['b']['NO2'] = value
                
                # Salviamo i dati dell'aria in base al modulo
                if modulo in temp_data['air']:
                    if modulo == 'a' and 'CO' in temp_data['air']['a']:
                        write_to_csv('air', [timestamp, modulo, temp_data['air']['a']['CO'], ''])
                        del temp_data['air']['a']
                    elif modulo == 'b' and 'NO2' in temp_data['air']['b']:
                        write_to_csv('air', [timestamp, modulo, '', temp_data['air']['b']['NO2']])
                        del temp_data['air']['b']
            
            elif category == 'flood':
                # L'allagamento è un dato singolo
                write_to_csv('flood', [timestamp, modulo, value])
            
            elif category == 'battery':
                # La batteria è un dato singolo
                write_to_csv('battery', [timestamp, modulo, value])

def readData(port):
    with serial.Serial(port, BAUD_RATE, timeout=0.5) as ser:
        print(f"[INFO] {port} - {BAUD_RATE} baud\n")
        
        while True:
            raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
            if raw_line:
                print(f"[DATI] {raw_line}")
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                pairs = parse_line(raw_line)
                
                if pairs:
                    process_data(timestamp, pairs)

print("[INFO] Avvio sistema ricevitore...")

def main():
    init_csv_files()

    port = find_working_port()
    
    if port: 
        readData(port)

if __name__ == '__main__':
    while True:
        try:
            main()
        except serial.SerialException as e:
            print(f"[ERRORE] Errore di comunicazione")
        except KeyboardInterrupt:
            print("[INFO] Programma terminato")
            break
