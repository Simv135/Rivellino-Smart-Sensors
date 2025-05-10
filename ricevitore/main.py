# main.py

### Librerie necessarie ###
#   la libreria serial è necessario installarla con il comando: "pip install pyserial"
import serial, serial.tools.list_ports
import re, csv, os, logging
from datetime import datetime

### Importazione del file di configurazione ###
from config import PORT, BAUD_RATE, CSV_PATH, CSV_FILES, ID_MAP, CSV_HEADERS
from config import SHOW_DATA, LOG_MESSAGES, LOG_FILE

### Configurazione del logging ###
#   i dati di log vengono salvati in un file 'logfile.log'
#   le informazioni vengono mostrate a schermo se indicato nel file config.py
def printLOG(message_key):
    logging.basicConfig(
        filename=LOG_FILE,
        format='%(asctime)s - %(message)s',
        level=logging.INFO
    )
    if message_key in LOG_MESSAGES:
        logging.info(LOG_MESSAGES[message_key])
        if SHOW_DATA:
            print(LOG_MESSAGES[message_key])
    else:
        if SHOW_DATA:
            print(message_key)

### Ricerca delle porte COM funzionanti ###
#   ricerca e utilizza la porta definita nel file config.py
#   se non è stata definita viene utilizzata la prima porta disponibile
def find_port():
    if PORT:
        return PORT
    else:
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            return port.device
        return None

### Scrittura dei file CSV ###
#   se la cartella in cui sono contenuti i file non esiste viene creata
#   se il file della categoria non esiste viene creato e viene intestato
#   al file della categoria viene aggiunta la riga contenente i dati da scrivere
def write_to_csv(category, row):
    if not os.path.exists(CSV_PATH):
        os.mkdir(CSV_PATH)
        printLOG('dir_created')
    filename = CSV_PATH + "/" + CSV_FILES[category]
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS[category])
        printLOG('file_created')
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

### Elaborazione dei dati ricevuti ###
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
            csv_headers = CSV_HEADERS[category][2:]
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

### Analisi della stringa di dati ricevuta ###
def parse_line(line):
    matches = re.findall(r'([a-z])([-+]?[0-9]+(?:\.[0-9]+)?)', line)
    return matches

### Lettura dei dati sulla porta seriale ###
# la porta trovata in precedenza viene letta ogni 0.5 secondi
# i dati ricevuti vengono decodificati
# viene salvato il momento in cui arrivano i dati
# i dati vengono analizzati e trasformati
# i dati trasformati vengono processati per essere salvati in dei file CSV
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

### Ciclo principale ###
# ricerca del dispositivo, ricezione e salvataggio dei dati
# gestione degli errori
if __name__ == '__main__':
    printLOG('init_start')
    while True:
        try:
            port = find_port()
            if port:
                readData(port)
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
