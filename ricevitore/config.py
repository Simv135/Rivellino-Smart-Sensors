# config.py

BAUD_RATE = 115200

# Definizione costante dei file CSV
CSV_FILES = {
    'env': 'DatiSensori/temperatura_umidita.csv',
    'vib': 'DatiSensori/vibrazioni.csv',
    'flood': 'DatiSensori/allagamento.csv',
    'air': 'DatiSensori/aria.csv',
    'battery': 'DatiSensori/batterie.csv'
}

# Mappatura completa degli ID dei sensori con relative informazioni
ID_MAP = {
    # ID: (nome, modulo, categoria_file)
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
    'env': ['timestamp', 'modulo', 'temperatura (°C)', 'umidità (%)'],
    'vib': ['timestamp', 'modulo', 'vibrazione (m/s²)', 'frequenza (Hz)'],
    'air': ['timestamp', 'modulo', 'CO (ppm)', 'NO2 (ppm)'],
    'flood': ['timestamp', 'modulo', 'allagamento'],
    'battery': ['timestamp', 'modulo', 'batteria (%)']
}

LOG_MESSAGES = {
    'init_start': "[INFO] Avvio sistema ricevitore...",
    'file_created': "[INFO] Creato file {filename} con intestazioni",
    'port_found': "[INFO] {port} - {baud} baud",
    'data': "[DATA] {raw_line}",
    'comm_error': "[ERROR] Errore di comunicazione",
    'terminated': "[INFO] Programma terminato"
}
