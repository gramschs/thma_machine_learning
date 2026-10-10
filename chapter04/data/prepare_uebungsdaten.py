"""
Aufbereitung der Datensaetze fuer die Uebungen in Kapitel 4.4.

Die Rohdaten werden nicht veraendert, nur Spaltennamen (und bei Pokemon die
Typ-Bezeichnungen) ins Deutsche uebersetzt und Fehlwerte als leere Zellen
gespeichert. Spaltennamen enthalten keine Umlaute (ae, oe, ue, ss), damit sie
sich im Code leicht tippen lassen.

Quellen der Rohdaten:

  - Pokemon with stats (Alberto Barradas), Kaggle, Lizenz CC0
    https://www.kaggle.com/datasets/abcsds/pokemon  -> Pokemon.csv
  - Deutscher Wetterdienst, Climate Data Center, Tageswerte Klima,
    Station Mannheim (ID 05906), Lizenz CC BY 4.0
    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/
    -> produkt_klima_tag_17810101_20251231_05906.txt
  - AI4I 2020 Predictive Maintenance Dataset (Stephan Matzka, HTW Berlin),
    UCI Machine Learning Repository, Lizenz CC BY 4.0,
    https://doi.org/10.24432/C5HS5C  -> ai4i2020.csv

Aufruf:
    python prepare_uebungsdaten.py --pokemon Pokemon.csv \
        --dwd produkt_klima_tag_17810101_20251231_05906.txt \
        --ai4i ai4i2020.csv --out ..
"""

import argparse
import os

import pandas as pd


POKEMON_SPALTEN = {
    '#': 'Nr.',
    'Name': 'Name',
    'Type 1': 'Typ 1',
    'Type 2': 'Typ 2',
    'Total': 'Gesamt',
    'HP': 'KP',
    'Attack': 'Angriff',
    'Defense': 'Verteidigung',
    'Sp. Atk': 'Spezial-Angriff',
    'Sp. Def': 'Spezial-Verteidigung',
    'Speed': 'Initiative',
    'Generation': 'Generation',
    'Legendary': 'Legendaer',
}

# offizielle deutsche Typ-Bezeichnungen
POKEMON_TYPEN = {
    'Bug': 'Käfer', 'Dark': 'Unlicht', 'Dragon': 'Drache',
    'Electric': 'Elektro', 'Fairy': 'Fee', 'Fighting': 'Kampf',
    'Fire': 'Feuer', 'Flying': 'Flug', 'Ghost': 'Geist', 'Grass': 'Pflanze',
    'Ground': 'Boden', 'Ice': 'Eis', 'Normal': 'Normal', 'Poison': 'Gift',
    'Psychic': 'Psycho', 'Rock': 'Gestein', 'Steel': 'Stahl',
    'Water': 'Wasser',
}

DWD_SPALTEN = {
    'TMK': 'Mitteltemperatur (C)',
    'TXK': 'Hoechsttemperatur (C)',
    'TNK': 'Tiefsttemperatur (C)',
    'RSK': 'Niederschlag (mm)',
    'SDK': 'Sonnenscheindauer (h)',
    'NM': 'Bewoelkung (Achtel)',
    'UPM': 'Luftfeuchte (%)',
    'FM': 'Windgeschwindigkeit (m/s)',
    'FX': 'Windspitze (m/s)',
}

# meteorologische Jahreszeiten
JAHRESZEITEN = {
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Frühling', 4: 'Frühling', 5: 'Frühling',
    6: 'Sommer', 7: 'Sommer', 8: 'Sommer',
    9: 'Herbst', 10: 'Herbst', 11: 'Herbst',
}

AI4I_SPALTEN = {
    'UDI': 'Nr.',
    'Product ID': 'Produkt-ID',
    'Type': 'Qualitaet',
    'Air temperature [K]': 'Lufttemperatur (K)',
    'Process temperature [K]': 'Prozesstemperatur (K)',
    'Rotational speed [rpm]': 'Drehzahl (1/min)',
    'Torque [Nm]': 'Drehmoment (Nm)',
    'Tool wear [min]': 'Werkzeugverschleiss (min)',
    'Machine failure': 'Ausfall',
    'TWF': 'Ausfall Werkzeug',
    'HDF': 'Ausfall Waermeabfuhr',
    'PWF': 'Ausfall Leistung',
    'OSF': 'Ausfall Ueberlast',
    'RNF': 'Ausfall zufaellig',
}


def pokemon(pfad_roh, pfad_ziel):
    daten = pd.read_csv(pfad_roh)
    daten['Type 1'] = daten['Type 1'].map(POKEMON_TYPEN)
    daten['Type 2'] = daten['Type 2'].map(POKEMON_TYPEN)
    daten['Legendary'] = daten['Legendary'].map({True: 'ja', False: 'nein'})
    daten = daten.rename(columns=POKEMON_SPALTEN)
    daten.to_csv(pfad_ziel, index=False)


def wetter(pfad_roh, pfad_ziel, jahr=2025):
    daten = pd.read_csv(pfad_roh, sep=';', skipinitialspace=True,
                        na_values=[-999])
    daten.columns = daten.columns.str.strip()
    daten = daten[daten['MESS_DATUM'] // 10000 == jahr]
    datum = pd.to_datetime(daten['MESS_DATUM'].astype(str), format='%Y%m%d')
    ergebnis = daten[list(DWD_SPALTEN)].rename(columns=DWD_SPALTEN)
    ergebnis.insert(0, 'Datum', datum.dt.strftime('%Y-%m-%d'))
    ergebnis['Jahreszeit'] = datum.dt.month.map(JAHRESZEITEN)
    ergebnis.to_csv(pfad_ziel, index=False)


def ai4i(pfad_roh, pfad_ziel):
    daten = pd.read_csv(pfad_roh, encoding='utf-8-sig')
    daten = daten.rename(columns=AI4I_SPALTEN)
    daten.to_csv(pfad_ziel, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pokemon', required=True)
    parser.add_argument('--dwd', required=True)
    parser.add_argument('--ai4i', required=True)
    parser.add_argument('--out', default='..')
    args = parser.parse_args()

    pokemon(args.pokemon, os.path.join(args.out, 'pokemon_DE.csv'))
    wetter(args.dwd, os.path.join(args.out, 'wetter_mannheim_2025.csv'))
    ai4i(args.ai4i, os.path.join(args.out, 'ai4i2020_DE.csv'))
