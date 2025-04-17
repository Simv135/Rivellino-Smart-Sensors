# Sensori Rivellino
Gestione sensori rivellino degli invalidi.

Moduli:
- a → tirante (Temperatura e Umidità, Aria, Vibrazioni)
- b → galleria (Batterie, Temperatura e Umidità, Aria, Allagamento)
- c → polveriera (Batterie, Temperatura e Umidità)

| ID   | Descrizione                | Valore       | Modulo  |
|------|----------------------------|--------------|---------|
| a    | Batteria                   | %            | b       |
| b    | Batteria                   | %            | c       |
| c    | Temperatura                | °C           | a       |
| d    | Temperatura                | °C           | b       |
| e    | Temperatura                | °C           | c       |
| f    | Umidità                    | %            | a       |
| g    | Umidità                    | %            | b       |
| h    | Umidità                    | %            | c       |
| i    | Aria (CO)                  | ppm          | a       |
| j    | Aria (NO2)                 | ppm          | b       |
| k    | Vibrazioni                 | Hz           | a       |
| l    | Vibrazioni                 | m/s²         | a       |
| m    | Allagamento                | 0 / 1        | b       |

| File CSV                    | ID del dato corrispondente       |
|----------------------------|----------------------------------|
| allagamento.csv            | m                                |
| aria.csv                   | i, j                             |
| batterie.csv               | a, b                             |
| vibrazioni.csv             | k, l                             |
| temperatura_umidita.csv    | c, d, e, f, g, h                 |
