import serial
import serial.tools.list_ports
import re
import csv
import os
from datetime import datetime

BAUD_RATE = 115200

CSV_FILES = {
    'env': 'temperatura_umidita.csv',
    'vib': 'vibrazioni.csv',
    'flood': 'allagamento.csv',
    'air': 'aria.csv',
    'battery': 'batterie.csv'
}

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
                    writer.writerow(['timestamp', 'modulo', 'CO', 'NO2'])
                elif key == 'flood':
                    writer.writerow(['timestamp', 'modulo', 'allagamento'])
                elif key == 'battery':
                    writer.writerow(['timestamp', 'modulo', 'batteria (%)'])

def parse_line(line):
    return re.findall(r'([a-z])([-+]?[0-9]*\.?[0-9]+)', line)

def write_to_csv(category, row):
    filename = CSV_FILES[category]
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def find_working_port():
    try:
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            with serial.Serial(port.device, BAUD_RATE, timeout=2) as ser:
                ser.write(b'\n')
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"[INFO] Dispositivo trovato sulla porta {port.device}")
                    connected = True
                    return port.device
    except serial.serialutil.SerialException:
        pass
    return None

def main():
    init_csv_files()
    temp_data = {}

    connectedPast = True

    while True:
        port = find_working_port()
        connected = bool(port)

        if connected:
            break

        if not connected and connected != connectedPast:
            print("[ERRORE] Nessun dispositivo valido trovato.")

        connectedPast = connected

    with serial.Serial(port, BAUD_RATE, timeout=0.5) as ser:
        print(f"[INFO] Lettura da {port} a {BAUD_RATE} baud...\n")
        while True:
            try:
                raw_line = ser.readline().decode('utf-8').strip()
            except serial.SerialException:
                break
            if raw_line != "":
                print(raw_line)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                pairs = parse_line(raw_line)

                for code, value in pairs:
                    if code in id_map:
                        mapping = id_map[code]
                        category = mapping[0]
                        modulo = mapping[1]

                        if len(mapping) == 3:
                            category = mapping[2]

                        if category == 'vib':
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
                            if code in ['c', 'd', 'e']:
                                temp_data['temperature'] = value
                            elif code in ['f', 'g', 'h']:
                                temp_data['humidity'] = value

                            if 'temperature' in temp_data and 'humidity' in temp_data:
                                temperature = temp_data.get('temperature')
                                humidity = temp_data.get('humidity')
                                if temperature is not None and humidity is not None:
                                    write_to_csv('env', [timestamp, modulo, temperature, humidity])
                                    temp_data.clear()

                        elif category == 'battery':
                            write_to_csv(category, [timestamp, modulo, value])
                        else:
                            write_to_csv(category, [timestamp, modulo, value])

if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Interrotto dall'utente")
            quit()
