"""
Aufbereitung des Datensatzes fuer die Uebungen in Kapitel 10.4.

Der Datensatz Palmer Penguins enthaelt Messungen an 344 Pinguinen dreier Arten,
die von 2007 bis 2009 auf drei Inseln des Palmer-Archipels in der Antarktis
erfasst wurden. Spaltennamen und Eintraege werden ins Deutsche uebersetzt. Die
fehlenden Werte bleiben erhalten, damit die Studierenden sie selbst entfernen.
Die Spalte Nr. ist die Zeilennummer im Originaldatensatz.

Spaltennamen enthalten keine Umlaute (ae, oe, ue, ss), damit sie sich im Code
leicht tippen lassen. Die Eintraege behalten ihre Umlaute.

Quelle der Rohdaten:

  - A. M. Horst, A. P. Hill, K. B. Gorman, palmerpenguins: Palmer Archipelago
    (Antarctica) penguin data, https://doi.org/10.5281/zenodo.3960218,
    Lizenz CC0
    -> https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv

Aufruf:
    python prepare_uebungsdaten.py --penguins penguins.csv --out ..
"""

import argparse
import os

import numpy as np
import pandas as pd


SPALTEN = {
    'species': 'Art',
    'island': 'Insel',
    'bill_length_mm': 'Schnabellaenge (mm)',
    'bill_depth_mm': 'Schnabeltiefe (mm)',
    'flipper_length_mm': 'Flossenlaenge (mm)',
    'body_mass_g': 'Koerpergewicht (g)',
    'sex': 'Geschlecht',
    'year': 'Jahr',
}

ARTEN = {
    'Adelie': 'Adeliepinguin',
    'Gentoo': 'Eselspinguin',
    'Chinstrap': 'Zügelpinguin',
}

GESCHLECHTER = {
    'female': 'weiblich',
    'male': 'männlich',
}


def pinguine(pfad_roh, pfad_ziel):
    daten = pd.read_csv(pfad_roh)
    assert daten.shape == (344, 8)

    daten = daten.rename(columns=SPALTEN)
    daten['Art'] = daten['Art'].map(ARTEN)
    daten['Geschlecht'] = daten['Geschlecht'].map(GESCHLECHTER)
    assert daten['Art'].notnull().all()

    daten.insert(0, 'Nr.', np.arange(1, len(daten) + 1))
    daten.to_csv(pfad_ziel, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--penguins', required=True)
    parser.add_argument('--out', default='..')
    args = parser.parse_args()

    pinguine(args.penguins, os.path.join(args.out, 'pinguine.csv'))
