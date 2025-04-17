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
    temp_data = {
        'env': {},   # {modulo: {'temp': val, 'hum': val}}
        'vib': {},   # {'freq': val, 'intensity': val}
        'air': {}    # {modulo: {'CO': val, 'NO2': val}}
    }

    for code, value in pairs:
        if code not in ID_MAP:
            continue

        name, modulo, category, _ = ID_MAP[code]
        value = float(value)

        if category == 'env':
            if modulo not in temp_data['env']:
                temp_data['env'][modulo] = {}

            if code in ['c', 'd', 'e']:  # temperatura
                temp_data['env'][modulo]['temp'] = value
            elif code in ['f', 'g', 'h']:  # umidità
                temp_data['env'][modulo]['hum'] = value

            # Scrive se entrambi i dati sono presenti
            data = temp_data['env'][modulo]
            if 'temp' in data and 'hum' in data:
                write_to_csv('env', [timestamp, modulo, data['temp'], data['hum']])
                del temp_data['env'][modulo]

        elif category == 'air':
            if modulo not in temp_data['air']:
                temp_data['air'][modulo] = {}

            if code == 'i':  # CO
                temp_data['air'][modulo]['CO'] = value
            elif code == 'j':  # NO2
                temp_data['air'][modulo]['NO2'] = value

            data = temp_data['air'][modulo]
            if 'CO' in data and 'NO2' in data:
                write_to_csv('air', [timestamp, modulo, data['CO'], data['NO2']])
                del temp_data['air'][modulo]

        elif category == 'vib':
            if code == 'k':  # frequenza
                temp_data['vib']['freq'] = value
            elif code == 'l':  # intensità
                temp_data['vib']['intensity'] = value

            if 'freq' in temp_data['vib'] and 'intensity' in temp_data['vib']:
                write_to_csv('vib', [timestamp, modulo, temp_data['vib']['intensity'], temp_data['vib']['freq']])
                temp_data['vib'].clear()

        elif category in ['flood', 'battery']:
            write_to_csv(category, [timestamp, modulo, value])

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
