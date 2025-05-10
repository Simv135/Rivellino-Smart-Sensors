# Sensori Rivellino
Gestione Sensori del Rivellino degli Invalidi.

Moduli:
- A → tirante (Temperatura e Umidità, Aria, Vibrazioni)
- B → galleria (Batterie, Temperatura e Umidità, Aria, Allagamento)
- C → polveriera (Batterie, Temperatura e Umidità)

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

Programma Ricevitore:

Files CSV all'interno della cartella "DatiSensori", relativi ai dati di ciascun sensore:

| File CSV                   | ID del dato sensore          |
|----------------------------|------------------------------|
| allagamento.csv            | m                            |
| ariaCO.csv                 | i                            |
| ariaNO2.csv                | j                            |
| batterie.csv               | a, b                         |
| vibrazioni.csv             | k, l                         |
| temperatura_umidita.csv    | c, d, e, f, g, h             |

File di configurazione "config.py":
- Selezione della porta di comunicazione
- Selezione della velocità di comunicazione (baud rate)
- Selezione del percorso dei files CSV
- Possibilità di rinominare i files CSV e di inserirne di nuovi
- Possibilità di mappare nuovi sensori
- Possibilità di modificare le colonne dei files CSV
- Possibilità di scegliere se mostrare i dati ricevuti sul terminale
- Personalizzazione dei messaggi di log
