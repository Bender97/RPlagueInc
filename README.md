# RPlagueInk
To run the codes, we need Python 3.6 and pygame, so:

pip install pygame

<b>STRUCTURE OF FOLDER:</b><br>
    engine.py - location di cui abbiamo parlato, ancora in versione neonato<br>
    Walker.py - le personcine che si muovono<br>
    
    tutti gli altri file: lasciateli perdere per ora, roba vecchia


Further works:
- introdurre tempo di incubazione   ---- fatto
    - dopo quanto tempo sviluppi la malattia?
- introdurre asintomatici
    - probabilità di diventare asintomatico piuttosto che ammalarsi davvero
        - idea: se sai di aver preso il virus, le probabilità di essere asintomatico sono:
            - bambini -> P(asintomatico) = 4/5
            - adulti  -> P(asintomatico) = 2/5
            - anziani -> P(asintomatico) = 1/5
- morte (perché rimuoverli dal gioco non va bene)
    - dopo quanto tempo puoi morire, se muori?
        - if asintomatico: P(morte) = 0
        - elif ammalato: P(morte) = 0.03
    - morte di parente -> malcontento aumenta, e anche la disobbedienza



ROBA IN PIU':
    - aggiungere edificio: ospedale
