#main.py

import serial
import serial.tools.list_ports
import re
import csv
import os
from datetime import datetime

#importiamo il file di configurazione config.py
from config import BAUD_RATE, CSV_FILES, ID_MAP, CSV_HEADERS, LOG_MESSAGES

def init_csv_files():
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
            
        sensor_name, modulo, category, _ = ID_MAP[code]
        
        # Inizializza le strutture dati necessarie
        if category not in temp_data:
            temp_data[category] = {}
        if modulo not in temp_data[category]:
            temp_data[category][modulo] = {}
            
        # Memorizza il valore con il nome del sensore come chiave
        temp_data[category][modulo][sensor_name] = value
    
    # Seconda elaborazione: verifica quali set di dati sono completi e possono essere scritti
    # Per ogni categoria nel dizionario temp_data
    for category in list(temp_data.keys()):
        # Per ogni modulo in questa categoria
        for modulo in list(temp_data[category].keys()):
            # Determina quali parametri sono attesi per questa categoria
            expected_params = get_expected_params(category)
            
            # Se abbiamo tutti i parametri attesi, scriviamo nel CSV
            if all(param in temp_data[category][modulo] for param in expected_params):
                # Prepara la riga da scrivere
                row = [timestamp, modulo] + [temp_data[category][modulo][param] for param in expected_params]
                write_to_csv(category, row)
                # Rimuovi i dati già scritti
                del temp_data[category][modulo]

def get_expected_params(category):
    """
    Determina i parametri attesi per una categoria basandosi sulle intestazioni CSV.
    Restituisce una lista di nomi di parametri.
    """
    # Ottieni le intestazioni per questa categoria
    headers = CSV_HEADERS[category]
    
    # Le prime due colonne sono sempre 'timestamp' e 'modulo'
    # Le colonne successive sono i parametri effettivi
    expected_params = []
    for header in headers[2:]:
        # Estrai il nome del parametro dalla colonna dell'intestazione
        # (rimuovi l'unità di misura tra parentesi, se presente)
        param_name = header.split(' (')[0]
        expected_params.append(param_name)
    
    return expected_params

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
