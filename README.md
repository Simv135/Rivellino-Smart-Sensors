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
0. [Modulo Ricevitore](#il-ricevitore) per l'elaborazione dei dati
1. [Modulo A](#1-ModuloA) → tirante (Temperatura e Umidità, Aria, Vibrazioni)
2. [Modulo B](#2-ModuloB) → galleria (Batterie, Temperatura e Umidità, Aria, Allagamento)
3. [Modulo C](#3-ModuloC) → polveriera (Batterie, Temperatura e Umidità)

<img width="1071" height="572" alt="schema-moduli" src="https://github.com/user-attachments/assets/4dd5736c-9acb-4d7d-bbe6-4dd24cb1500f"/>

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

<img width="2160" height="1208" alt="Mappa_Rivellino" src="https://github.com/user-attachments/assets/9a15419e-a349-405f-b95e-75f8a2fb708f"/>

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
Estrarre `libraries.zip` e inserire le librerie all'interno della cartella `C:\Users\%USERPROFILE%\Documents\Arduino\libraries`

## 1. ModuloA

<img width="912" height="540" alt="image" src="https://github.com/user-attachments/assets/092ea132-b699-40a9-a8d6-75a042c1687d" />

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

## 2. ModuloB

<img width="986" height="530" alt="image" src="https://github.com/user-attachments/assets/2a0e6bcc-ffef-49de-8ba9-27df456c938a" />

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

## 3. ModuloC

<img width="897" height="520" alt="image" src="https://github.com/user-attachments/assets/401373b9-26b6-440e-ab7c-1bd358575cdf" />

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
