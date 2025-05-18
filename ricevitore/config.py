# config.py

# Connessione porta COM
# PORT = None    →  Selezione automatica della prima porta disponibile
# oppure
# PORT = "<nome_della_porta>"  →  Consigliato se si utilizza più di una porta seriale
PORT = None

BAUD_RATE = 9600

# Percorso file CSV
CSV_PATH = "DatiSensori"

# Nome dei file CSV
CSV_FILES = {
    'env': 'temperatura_umidita.csv',
    'vib': 'vibrazioni.csv',
    'flood': 'allagamento.csv',
    'airCO': 'ariaCO.csv',
    'airNO2': 'ariaNO2.csv',
    'battery': 'batterie.csv'
}

# Mappatura degli ID dei sensori con le relative informazioni
#    ID: (nome, modulo, categoria_file)
ID_MAP = {
    'a': ('batteria', 'b', 'battery'),
    'b': ('batteria', 'c', 'battery'),
    'c': ('temperatura', 'a', 'env'),
    'd': ('temperatura', 'b', 'env'),
    'e': ('temperatura', 'c', 'env'),
    'f': ('umidità', 'a', 'env'),
    'g': ('umidità', 'b', 'env'),
    'h': ('umidità', 'c', 'env'),
    'i': ('CO', 'a', 'airCO'),
    'j': ('NO2', 'b', 'airNO2'),
    'k': ('frequenza', 'a', 'vib'),
    'l': ('vibrazione', 'a', 'vib'),
    'm': ('allagamento', 'b', 'flood')
}

# Inizializza tutti i file CSV con le intestazioni corrette
CSV_HEADERS = {
    'env': ('timestamp', 'modulo', 'temperatura (°C)', 'umidità (%)'),
    'vib': ('timestamp', 'modulo', 'vibrazione (m/s²)', 'frequenza (Hz)'),
    'airCO': ('timestamp', 'modulo', 'CO (ppm)'),
    'airNO2': ('timestamp', 'modulo', 'NO2 (ppm)'),
    'flood': ('timestamp', 'modulo', 'allagamento'),
    'battery': ('timestamp', 'modulo', 'batteria (%)')
}

# Messaggi di LOG
SHOW_DATA = True

LOG_FILE = 'logfile.log'

LOG_MESSAGES = {
    'init_start': '[INFO] Avvio ricevitore...',
    'file_created': '[INFO] File CSV creato',
    'dir_created': f'[INFO] Cartella {CSV_PATH} creata',
    'port_found': '[INFO] Connesso alla porta seriale',
    'dir_error': f'[ERROR] Cartella {CSV_PATH} non trovata',
    'comm_error': '[ERROR] Errore di comunicazione',
    'terminated': "[INFO] Programma terminato dall'utente"
}

