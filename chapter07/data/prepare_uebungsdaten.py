"""
Aufbereitung der Datensaetze fuer die Uebungen in Kapitel 7.4.

Die Rohdaten werden nicht veraendert, nur Spaltennamen ins Deutsche
uebersetzt. Beim Beton-Datensatz kommt eine Spalte Nr. als Zeilenindex hinzu.
Spaltennamen enthalten keine Umlaute (ae, oe, ue, ss), damit sie sich im Code
leicht tippen lassen.

Quellen der Rohdaten:

  - Concrete Compressive Strength (I-Cheng Yeh), UCI Machine Learning
    Repository, Lizenz CC BY 4.0, https://doi.org/10.24432/C5PK67
    -> https://archive.ics.uci.edu/static/public/165/data.csv
  - Bevoelkerung Deutschland 1800 bis 2021 aus den aelteren Vorlesungen
    (population_germany.csv). Die Werte entsprechen der Zeitreihe
    "Population" von Our World in Data (Stand 2021, bis 1950 nach Gapminder,
    ab 1950 nach UN World Population Prospects 2019), Lizenz CC BY 4.0,
    https://ourworldindata.org/population-sources

Aufruf:
    python prepare_uebungsdaten.py --beton data.csv \
        --bevoelkerung population_germany.csv --out ..
"""

import argparse
import os

import pandas as pd


BETON_SPALTEN = {
    'Cement': 'Zement (kg/m3)',
    'Blast Furnace Slag': 'Huettensand (kg/m3)',
    'Fly Ash': 'Flugasche (kg/m3)',
    'Water': 'Wasser (kg/m3)',
    'Superplasticizer': 'Fliessmittel (kg/m3)',
    'Coarse Aggregate': 'Grobzuschlag (kg/m3)',
    'Fine Aggregate': 'Feinzuschlag (kg/m3)',
    'Age': 'Alter (Tage)',
    'Concrete compressive strength': 'Druckfestigkeit (MPa)',
}

BEVOELKERUNG_SPALTEN = {
    'Region': 'Land',
    'Code': 'Code',
    'Jahr': 'Jahr',
    'Population': 'Einwohner',
}


def beton(pfad_roh, pfad_ziel):
    daten = pd.read_csv(pfad_roh)
    assert list(daten.columns) == list(BETON_SPALTEN)
    ergebnis = daten.rename(columns=BETON_SPALTEN)
    ergebnis.insert(0, 'Nr.', range(1, len(ergebnis) + 1))
    ergebnis.to_csv(pfad_ziel, index=False)


def bevoelkerung(pfad_roh, pfad_ziel):
    daten = pd.read_csv(pfad_roh)
    assert list(daten.columns) == list(BEVOELKERUNG_SPALTEN)
    ergebnis = daten.rename(columns=BEVOELKERUNG_SPALTEN)
    ergebnis['Land'] = ergebnis['Land'].replace({'Germany': 'Deutschland'})
    ergebnis.to_csv(pfad_ziel, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--beton', required=True)
    parser.add_argument('--bevoelkerung', required=True)
    parser.add_argument('--out', default='..')
    args = parser.parse_args()

    beton(args.beton, os.path.join(args.out, 'beton_DE.csv'))
    bevoelkerung(args.bevoelkerung,
                 os.path.join(args.out, 'bevoelkerung_deutschland.csv'))
