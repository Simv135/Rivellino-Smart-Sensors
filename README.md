# Rivellino Smart Sensors

## Introduzione

Il sistema **Rivellino Smart Sensors** è progettato per monitorare le condizioni ambientali all'interno del ***Rivellino degli Invalidi***, parte del **Museo Pietro Micca** di Torino.  
I sensori installati nei tre moduli principali **Tirante (A)**, **Galleria (B)** e **Polveriera (C)** raccolgono dati su:

- Temperatura e Umidità  
- Qualità dell’aria (CO e NO₂)  
- Vibrazioni
- Allagamento

Questi dati vengono trasmessi via seriale ad un Raspberry Pi e letti da un ricevitore scritto in Python, che li elabora e li salva automaticamente in file CSV.  
Il sistema garantisce un monitoraggio continuo e affidabile degli ambienti ipogei, contribuendo alla **tutela e alla conservazione del patrimonio storico**.

## I moduli
- [Modulo Ricevitore](#Il-ricevitore) per l'elaborazione dei dati
- [Modulo A](#Modulo-A) → tirante (Temperatura e Umidità, Aria, Vibrazioni)
- [Modulo B](#Modulo-B) → galleria (Batterie, Temperatura e Umidità, Aria, Allagamento)
- [Modulo C](#Modulo-C) → polveriera (Batterie, Temperatura e Umidità)

<img width="1580" height="854" alt="diagramma_funzionale" src="https://github.com/user-attachments/assets/adbd03e2-59d2-45a6-bc90-2eb4d45d66fc" />

<br><br>

## I dati

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

<br><br>

## Posizionamento

<img width="2880" height="1611" alt="Mappa_Rivellino" src="https://github.com/user-attachments/assets/a389c6fa-4961-492c-86c4-1f770559a0b4" />

<br><br>

## Disegno Meccanico

| | |
|:---:|:---:|
| ![ModuloA](https://github.com/user-attachments/assets/4cb3a996-f35a-484c-b502-63b5ccda0648) | ![ModuloB](https://github.com/user-attachments/assets/6e28f377-c215-4d7e-a07a-ac02ab442f20) |
| ModuloA | ModuloB e ModuloC |
| ![ModuloA_Condotto](https://github.com/user-attachments/assets/a95124b8-e612-47c0-9490-474b2da2c831) | ![Coperchio](https://github.com/user-attachments/assets/f67974d0-79c0-44b9-8a58-a31172c024fd) |
| Condotto Aria (ModuloA) | Coperchio (ModuloA, ModuloB e Modulo C) |

<br><br>

## Il ricevitore

Assicurarsi di avere l'ultima versione di Python3 installata sul dispositivo (in questo caso sul Raspberry Pi 5).

Eseguire ```pip install pyserial``` nel terminale per installare la libreria pyserial.

Eseguire ```python3 main.py``` nel terminale, all'interno della cartella in cui si trova il programma ricevitore.

Il programma proverà a connettersi alla porta seriale. Quando la connessione sarà stabilita verrà mostrata la porta utilizzata e la velocità di comunicazione impostata.

Il programma riceverà dati periodicamente. Esempio di dati inviati da parte dei moduli:
- moduloA:    `c28f58j0.06k15.5l1.9i0.07`
- moduloB:    `a61d27g56m1`
- moduloC:    `b62e28h42`

I dati verranno salvati nella cartella DatiSensori nei seguenti files:

| File CSV                   | ID del dato         |
|----------------------------|---------------------|
| allagamento.csv            | m                   |
| ariaCO.csv                 | i                   |
| ariaNO2.csv                | j                   |
| batterie.csv               | a, b                |
| vibrazioni.csv             | k, l                |
| temperatura_umidita.csv    | c, d, e, f, g, h    |

Il file di configurazione `config.py` permette di modificare alcuni parametri relativi al programma di ricezione dei dati, tra cui:
- Selezionare la porta di comunicazione
- Selezionare la velocità di comunicazione (baud rate)
- Selezionare il percorso dei files CSV
- Rinominare i files CSV e di inserirne di nuovi
- Mappare nuovi sensori
- Modificare le colonne dei files CSV
- Scegliere se mostrare i dati ricevuti sul terminale
- Personalizzare i messaggi di log

Le informazioni di comunicazione ed eventuali errori saranno salvati all'interno di: `logfile.log`

## Librerie Arduino
Estrarre `libraries.zip` all'interno della cartella `C:\Users\%USERPROFILE%\Documents\Arduino\`, riavviare eventualmente Arduino IDE.

## Configurazione LoRa
- Lora Modulo A
  - `AT+ADDRESS=1`
  - `AT+NETWORKID=5`
  - `AT+IPR=9600`
- Lora Modulo B
  - `AT+ADDRESS=2`
  - `AT+NETWORKID=5`
  - `AT+IPR=9600`
- Lora Modulo C
  - `AT+ADDRESS=3`
  - `AT+NETWORKID=5`
  - `AT+IPR=9600`

## Modulo A

<img width="602" height="662" alt="ModuloA" src="https://github.com/user-attachments/assets/75a2bb8d-df2d-480f-bab2-1d8166e463b7" />

<br><br>

**Componenti**:
- Arduino Nano 33 BLE Sense Rev2
- Sensore Qualità Aria Mikroe3056
- Modulo LoRa RYLR498

Esempio di dati inviati:
`c28f58j0.06k15.5l1.9i0.07`

| ID   | Descrizione                | Valore       |
|------|----------------------------|--------------|
| c    | Temperatura                | °C           |
| f    | Umidità                    | %            |
| i    | Aria (CO)                  | ppm          |
| j    | Aria (NO2)                 | ppm          |
| k    | Vibrazioni                 | Hz           |
| l    | Vibrazioni                 | m/s²         |

<br><br>

## Modulo B

<img width="901" height="716" alt="ModuloB" src="https://github.com/user-attachments/assets/7d79e3ab-da4b-4317-91d7-e6963c3c493e" />

<br><br>

**Componenti**:
- Arduino Pro Mini
- Sensore Temperatura e Umidità DHT11
- Sensore Allagamento HW-038
- Modulo LoRa RYLR498
- Batterie AA Alcaline x5 (serie)

Esempio di dati inviati:
`a61d27g56m1`

| ID   | Descrizione                | Valore       |
|------|----------------------------|--------------|
| a    | Batteria                   | %            |
| d    | Temperatura                | °C           |
| g    | Umidità                    | %            |
| m    | Allagamento                | 0 / 1        |

<br><br>

## Modulo C

<img width="792" height="723" alt="ModuloC" src="https://github.com/user-attachments/assets/f7f4e038-95c8-4f98-9709-067d31cbaec1" />

<br><br>

**Componenti**:
- Arduino Pro Mini
- Sensore Temperatura e Umidità DHT11
- Modulo LoRa RYLR498
- Batterie AA Alcaline x5 (serie)

Esempio di dati inviati:
`b62e28h42`

| ID   | Descrizione                | Valore       |
|------|----------------------------|--------------|
| b    | Batteria                   | %            |
| e    | Temperatura                | °C           |
| h    | Umidità                    | %            |

<br><br>

***ITS AEROSPAZIO PIEMONTE***

***CORSO EMBT02***

***Rivellino Smart Sensors***

<br><br>
