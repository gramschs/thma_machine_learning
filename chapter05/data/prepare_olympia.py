"""
Aufbereitung des Olympia-Datensatzes fuer die Uebungen in Kapitel 5.4.

Aus den Rohdaten werden die Olympischen Sommerspiele 2016 in Rio de Janeiro
und acht Sportarten ausgewaehlt, in denen jede Person nur in einem einzigen
Wettbewerb startet. Damit beschreibt jede Zeile genau eine Person. Namen,
Teamnamen und Wettbewerbe werden entfernt, Spaltennamen, Sportarten,
Geschlecht und Medaillen ins Deutsche uebersetzt. Spaltennamen enthalten keine
Umlaute (ae, oe, ue, ss), damit sie sich im Code leicht tippen lassen.

Quelle der Rohdaten:

  - 120 years of Olympic history: athletes and results (Randi H. Griffin),
    Kaggle, Lizenz CC0,
    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
    -> athlete_events.csv
    Dieselben Daten mit kleingeschriebenen Spaltennamen liegen auch unter
    https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-07-27/olympics.csv

Aufruf:
    python prepare_olympia.py --roh athlete_events.csv --out ..
"""

import argparse
import os

import pandas as pd


SPORTARTEN = {
    'Basketball': 'Basketball',
    'Football': 'Fußball',
    'Handball': 'Handball',
    'Hockey': 'Hockey',
    'Judo': 'Judo',
    'Rhythmic Gymnastics': 'Rhythmische Sportgymnastik',
    'Volleyball': 'Volleyball',
    'Weightlifting': 'Gewichtheben',
}

GESCHLECHT = {'F': 'w', 'M': 'm'}

MEDAILLEN = {'Gold': 'Gold', 'Silver': 'Silber', 'Bronze': 'Bronze'}

SPALTEN = {
    'sex': 'Geschlecht',
    'age': 'Alter',
    'height': 'Groesse (cm)',
    'weight': 'Gewicht (kg)',
    'noc': 'Land',
    'sport': 'Sportart',
    'medal': 'Medaille',
}


def olympia(pfad_roh, pfad_ziel):
    daten = pd.read_csv(pfad_roh)
    daten.columns = daten.columns.str.lower()
    daten = daten[(daten['games'] == '2016 Summer')
                  & daten['sport'].isin(SPORTARTEN)]

    # In den ausgewaehlten Sportarten startet jede Person nur einmal
    assert daten['id'].is_unique

    daten['sport'] = daten['sport'].map(SPORTARTEN)
    daten['sex'] = daten['sex'].map(GESCHLECHT)
    daten['medal'] = daten['medal'].map(MEDAILLEN)
    for spalte in ['age', 'height', 'weight']:
        daten[spalte] = daten[spalte].round().astype('Int64')

    ergebnis = daten[list(SPALTEN)].rename(columns=SPALTEN)
    ergebnis.insert(0, 'Nr.', range(1, len(ergebnis) + 1))
    ergebnis.to_csv(pfad_ziel, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--roh', required=True)
    parser.add_argument('--out', default='..')
    args = parser.parse_args()

    olympia(args.roh, os.path.join(args.out, 'olympia_rio2016.csv'))
