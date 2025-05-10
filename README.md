# Sensori Rivellino
Gestione dei sensori all'interno del Rivellino degli Invalidi, facente parte del museo di Pietro Micca.

Moduli:
- A → tirante (Temperatura e Umidità, Aria, Vibrazioni)
- B → galleria (Batterie, Temperatura e Umidità, Aria, Allagamento)
- C → polveriera (Batterie, Temperatura e Umidità)

![Mappa_Rivellino](https://github.com/user-attachments/assets/0eda5039-46fb-40d3-8ec3-fc16ac8c2962)

| ID   | Descrizione                | Valore       | Modulo  |
|------|----------------------------|--------------|---------|
| a    | Batteria                   | %            | B       |
| b    | Batteria                   | %            | C       |
| c    | Temperatura                | °C           | A       |
| d    | Temperatura                | °C           | B       |
| e    | Temperatura                | °C           | C       |
| f    | Umidità                    | %            | A       |
| g    | Umidità                    | %            | B       |
| h    | Umidità                    | %            | C       |
| i    | Aria (CO)                  | ppm          | A       |
| j    | Aria (NO2)                 | ppm          | B       |
| k    | Vibrazioni                 | Hz           | A       |
| l    | Vibrazioni                 | m/s²         | A       |
| m    | Allagamento                | 0 / 1        | B       |

I dati verranno elaborati dal ricevitore e salvati all'interno dei files CSV.

# Ricevitore:

Assicurarsi di avere l'ultima versione di Python3 installata sul dispositivo.

Eseguire "pip install pyserial" nel terminale per installare la libreria pyserial.

Eseguire "Python3 main.py" nel terminale, all'interno della cartella in cui si trova.

Il programma proverà a connettersi alla porta seriale. Quando la connessione sarà stabilita verrà mostrata la porta utilizzata e la velocità di comunicazione impostata.

Il programma riceverà dati periodicamente. Esempio di dati inviati da parte dei moduli:
- moduloA:    c28f58k15.5l1.9i0.07
- moduloB:    a61d27g56j0.06m1
- moduloC:    b62e28h42

I dati verranno salvati nella cartella DatiSensori nei seguenti files:

| File CSV                   | ID del dato         |
|----------------------------|---------------------|
| allagamento.csv            | m                   |
| ariaCO.csv                 | i                   |
| ariaNO2.csv                | j                   |
| batterie.csv               | a, b                |
| vibrazioni.csv             | k, l                |
| temperatura_umidita.csv    | c, d, e, f, g, h    |

Il file di configurazione "config.py" permette di modificare alcuni parametri relativi al programma di ricezione dei dati, tra cui:
- Selezionare la porta di comunicazione
- Selezionare la velocità di comunicazione (baud rate)
- Selezionare il percorso dei files CSV
- Rinominare i files CSV e di inserirne di nuovi
- Mappare nuovi sensori
- Modificare le colonne dei files CSV
- Scegliere se mostrare i dati ricevuti sul terminale
- Personalizzare i messaggi di log

Le informazioni di comunicazione ed eventuali errori saranno salvati all'interno di: "logfile.log"

# moduloA

| ID   | Descrizione                | Valore       |
|------|----------------------------|--------------|
| c    | Temperatura                | °C           |
| f    | Umidità                    | %            |
| i    | Aria (CO)                  | ppm          |
| k    | Vibrazioni                 | Hz           |
| l    | Vibrazioni                 | m/s²         |

# moduloB

| ID   | Descrizione                | Valore       |
|------|----------------------------|--------------|
| a    | Batteria                   | %            |
| d    | Temperatura                | °C           |
| g    | Umidità                    | %            |
| j    | Aria (NO2)                 | ppm          |
| m    | Allagamento                | 0 / 1        |

# moduloC

| ID   | Descrizione                | Valore       |
|------|----------------------------|--------------|
| b    | Batteria                   | %            |
| e    | Temperatura                | °C           |
| h    | Umidità                    | %            |
