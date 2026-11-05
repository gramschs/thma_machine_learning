"""
Aufbereitung des Datensatzes fuer die Uebungen in Kapitel 9.4.

Aus dem Covertype-Datensatz (581 012 Flaechen von je 30 x 30 m im Roosevelt
National Forest, Colorado) wird eine Stichprobe von 20 000 Flaechen gezogen.
Uebernommen werden die sieben anschaulichen Messgroessen, das Schutzgebiet
und der Waldtyp. Die drei Schattenindizes und die 40 Bodentypen entfallen,
damit der Datensatz uebersichtlich bleibt. Die vier One-Hot-Spalten der
Schutzgebiete werden zu einer Textspalte zusammengefasst, damit die
Studierenden die One-Hot-Kodierung aus Kapitel 8.2 selbst anwenden. Die Spalte
Nr. ist die Zeilennummer im Originaldatensatz.

Spaltennamen enthalten keine Umlaute (ae, oe, ue, ss), damit sie sich im Code
leicht tippen lassen.

Quelle der Rohdaten:

  - J. Blackard, Covertype, UCI Machine Learning Repository, Lizenz
    CC BY 4.0, https://doi.org/10.24432/C50K5N
    -> https://archive.ics.uci.edu/static/public/31/covertype.zip
       (darin covtype.data.gz)

Beton: Kapitel 9.4 verwendet ausserdem beton_DE.csv, eine Kopie der Datei aus
Kapitel 7 (erzeugt mit chapter07/data/prepare_uebungsdaten.py).

Aufruf:
    python prepare_uebungsdaten.py --covertype covtype.data.gz --out ..
"""

import argparse
import os

import numpy as np
import pandas as pd


MESSGROESSEN = {
    0: 'Hoehe (m)',
    1: 'Ausrichtung (Grad)',
    2: 'Hangneigung (Grad)',
    3: 'Abstand Wasser horizontal (m)',
    4: 'Abstand Wasser vertikal (m)',
    5: 'Abstand Strasse (m)',
    9: 'Abstand Brandstelle (m)',
}

# Spalten 10 bis 13 im Original, in dieser Reihenfolge
GEBIETE = np.array(['Rawah', 'Neota', 'Comanche Peak', 'Cache la Poudre'])

# Spalte 54 im Original
WALDTYPEN = {
    1: 'Fichte/Tanne',
    2: 'Drehkiefer',
    3: 'Gelbkiefer',
    4: 'Pappel/Weide',
    5: 'Espe',
    6: 'Douglasie',
    7: 'Krummholz',
}

ANZAHL = 20000
SEED = 0


def waldtypen(pfad_roh, pfad_ziel):
    daten = pd.read_csv(pfad_roh, header=None)
    assert daten.shape == (581012, 55)
    gebiet_onehot = daten.iloc[:, 10:14].to_numpy()
    assert (gebiet_onehot.sum(axis=1) == 1).all()

    ergebnis = pd.DataFrame({'Nr.': np.arange(1, len(daten) + 1)})
    for spalte, name in MESSGROESSEN.items():
        ergebnis[name] = daten[spalte]
    ergebnis['Gebiet'] = GEBIETE[gebiet_onehot.argmax(axis=1)]
    ergebnis['Waldtyp'] = daten[54].map(WALDTYPEN)

    stichprobe = ergebnis.sample(ANZAHL, random_state=SEED).sort_values('Nr.')
    stichprobe.to_csv(pfad_ziel, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--covertype', required=True)
    parser.add_argument('--out', default='..')
    args = parser.parse_args()

    waldtypen(args.covertype, os.path.join(args.out, 'waldtypen_colorado.csv'))
