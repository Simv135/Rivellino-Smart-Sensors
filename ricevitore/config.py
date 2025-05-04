# config.py

# Connessione
PORT = None
BAUD_RATE = 115200

# Percorso file CSV
CSV_PATH = "DatiSensori"

# Nome dei file CSV
CSV_FILES = {
    'env': 'temperatura_umidita.csv',
    'vib': 'vibrazioni.csv',
    'flood': 'allagamento.csv',
    'air': 'aria.csv',
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
    'i': ('CO', 'a', 'air'),
    'j': ('NO2', 'b', 'air'),
    'k': ('frequenza', 'a', 'vib'),
    'l': ('vibrazione', 'a', 'vib'),
    'm': ('allagamento', 'b', 'flood')
}

# Inizializza tutti i file CSV con le intestazioni corrette
CSV_HEADERS = {
    'env': ('timestamp', 'modulo', 'temperatura (°C)', 'umidità (%)'),
    'vib': ('timestamp', 'modulo', 'vibrazione (m/s²)', 'frequenza (Hz)'),
    'air': ('timestamp', 'modulo', 'CO (ppm)', 'NO2 (ppm)'),
    'flood': ('timestamp', 'modulo', 'allagamento'),
    'battery': ('timestamp', 'modulo', 'batteria (%)')
}

# Messaggi di LOG
SHOW_LOG = True

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


