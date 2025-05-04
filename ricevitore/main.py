import serial, serial.tools.list_ports  # pip install pyserial
import re, csv, os, logging
from datetime import datetime

# Importiamo il file di configurazione config.py
from config import BAUD_RATE, CSV_FILES, ID_MAP, CSV_HEADERS, CSV_PATH
from config import LOG_MESSAGES, SHOW_LOG

# Configurazione del logging
def printLOG(message_key):
    logging.basicConfig(
        filename='logfile.log',
        format='%(asctime)s - %(message)s',
        level=logging.INFO
    )
    if message_key in LOG_MESSAGES:
        logging.info(LOG_MESSAGES[message_key])
        if SHOW_LOG:
            print(LOG_MESSAGES[message_key])
    else:
        if SHOW_LOG:
            print(message_key)

def init_csv_files():
    if not os.path.exists(CSV_PATH):
        os.mkdir(CSV_PATH)
        printLOG('dir_created')
    for category, filename in CSV_FILES.items():
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS[category])
            printLOG('file_created')

def parse_line(line):
    matches = re.findall(r'([a-z])([-+]?[0-9]*\.?[0-9]+)', line)
    return matches

def write_to_csv(category, row):
    filename = CSV_FILES[category]
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def find_working_port():
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
    temp_data = {}

    for code, value in pairs:
        if code not in ID_MAP:
            continue
        sensor_name, modulo, category = ID_MAP[code]
        if category not in temp_data:
            temp_data[category] = {}
        if modulo not in temp_data[category]:
            temp_data[category][modulo] = {}
        temp_data[category][modulo][sensor_name] = value

    for category in list(temp_data.keys()):
        for modulo in list(temp_data[category].keys()):
            csv_headers = CSV_HEADERS[category][2:]  # Escludi timestamp e modulo
            sensor_to_csv_map = {}

            for code, (name, mod, cat) in ID_MAP.items():
                if cat == category:
                    for header in csv_headers:
                        if name.lower() in header.lower():
                            sensor_to_csv_map[name] = header
                            break

            collected_data = temp_data[category][modulo]
            row = [timestamp, modulo]

            for header in csv_headers:
                value = ''
                for sensor_name, csv_header in sensor_to_csv_map.items():
                    if csv_header == header and sensor_name in collected_data:
                        value = collected_data[sensor_name]
                        break
                row.append(value)

            write_to_csv(category, row)

def readData(port):
    with serial.Serial(port, BAUD_RATE, timeout=0.5) as ser:
        printLOG('port_found')
        printLOG(f'[INFO] {port} - {BAUD_RATE}')
        while True:
            raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
            if raw_line:
                printLOG(f'[DATA] {raw_line}')
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
    printLOG('init_start')
    while True:
        try:
            main()
        except serial.SerialException:
            printLOG('comm_error')
        except FileNotFoundError:
            printLOG('dir_error')
        except KeyboardInterrupt:
            printLOG('terminated')
            logging.shutdown()
            break
        except Exception as e:
            printLOG(e)
