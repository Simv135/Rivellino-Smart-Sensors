# config.py

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
ID_MAP = {
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
