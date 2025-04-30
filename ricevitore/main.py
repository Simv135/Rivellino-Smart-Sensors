#main.py

import serial
import serial.tools.list_ports
import re
import csv
import os
from datetime import datetime

#importiamo il file di configurazione config.py
from config import BAUD_RATE, CSV_FILES, ID_MAP, CSV_HEADERS, CSV_PATH, LOG_MESSAGES

def init_csv_files():
    if not os.path.exists(CSV_PATH):
        os.mkdir(CSV_PATH)
    for category, filename in CSV_FILES.items():
        # Crea il file solo se non esiste
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS[category])
            print(LOG_MESSAGES['file_created'].format(filename=filename))

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
    return None

def process_data(timestamp, pairs):
    # Struttura temporanea per raccogliere i dati
    temp_data = {}
    
    # Prima elaborazione: raccogli tutti i dati di questa iterazione
    for code, value in pairs:
        if code not in ID_MAP:
            continue
            
        sensor_name, modulo, category = ID_MAP[code]
        
        # Inizializza le strutture dati necessarie
        if category not in temp_data:
            temp_data[category] = {}
        if modulo not in temp_data[category]:
            temp_data[category][modulo] = {}
            
        # Memorizza il valore con il nome del sensore come chiave
        temp_data[category][modulo][sensor_name] = value
    
    # Seconda elaborazione: verifica quali set di dati sono completi
    for category in list(temp_data.keys()):
        for modulo in list(temp_data[category].keys()):
            # Ottieni i parametri attesi dalle intestazioni CSV
            csv_headers = CSV_HEADERS[category][2:]  # Escludi timestamp e modulo
            
            # Mappa i nomi dei sensori (in ID_MAP) ai nomi delle colonne CSV (in CSV_HEADERS)
            sensor_to_csv_map = {}
            for code, (name, mod, cat) in ID_MAP.items():
                if cat == category:
                    # Trova l'intestazione CSV corrispondente
                    for header in csv_headers:
                        # Controllo semplice: il nome del sensore è contenuto nell'intestazione CSV?
                        if name in header:
                            sensor_to_csv_map[name] = header
                            break
            
            # Verifica se sono presenti tutti i sensori necessari per questa categoria
            collected_data = temp_data[category][modulo]
            
            # Se abbiamo tutti i sensori necessari per questa categoria
            if all(sensor in collected_data for sensor in sensor_to_csv_map.keys()):
                # Prepara la riga da scrivere nel CSV
                row = [timestamp, modulo]
                
                # Aggiungi i valori nell'ordine corretto delle intestazioni CSV
                for header in csv_headers:
                    # Trova il sensore corrispondente a questa intestazione
                    for sensor_name, csv_header in sensor_to_csv_map.items():
                        if csv_header == header:
                            row.append(collected_data[sensor_name])
                            break
                
                # Scrivi la riga nel CSV
                write_to_csv(category, row)
                # Rimuovi i dati già scritti
                del temp_data[category][modulo]

def readData(port):
    with serial.Serial(port, BAUD_RATE, timeout=0.5) as ser:
        print(LOG_MESSAGES['port_found'].format(port=port, baud=BAUD_RATE))
        
        while True:
            raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
            if raw_line:
                print(LOG_MESSAGES['data'].format(raw_line=raw_line))
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                pairs = parse_line(raw_line)
                
                if pairs:
                    process_data(timestamp, pairs)

def main():
    init_csv_files()
    port = find_working_port()
    
    if port: 
        readData(port)

if __name__ == '__main__':
    print(LOG_MESSAGES['init_start'])
    while True:
        try:
            main()
        except serial.SerialException:
            print(LOG_MESSAGES['comm_error'])
        except KeyboardInterrupt:
            print(LOG_MESSAGES['terminated'])
            break
