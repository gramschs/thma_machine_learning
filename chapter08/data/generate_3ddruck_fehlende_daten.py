"""
Generator fuer den 3D-Druck-Datensatz mit ABSICHTLICH FEHLENDEN DATEN.

Dieser Datensatz wird in Kapitel 8.1 (Fehlende Daten) fuer die Mini-Uebungen
verwendet. Waehrend der Vorlesungsstoff am Autoscout24-Datensatz demonstriert
wird, ueben die Studierenden dieselben Schritte am 3D-Druck-Beispiel ein.

Die Basislogik (nichtlineare, interaktive Zusammenhaenge) ist eine Kopie aus
chapter04/data/generate_3ddruck_daten.py. Sie ist hier bewusst dupliziert, damit
dieser Datensatz stabil bleibt, auch wenn der Kapitel-4-Generator spaeter
veraendert wird.

Nach dem Erzeugen des vollstaendigen Datensatzes werden gezielt Luecken und ein
problematischer Datenpunkt eingebaut:

  - Oberflaechenguete:     ~30 % der Eintraege fehlen. Das Merkmal laesst sich
                            ausserdem direkt aus der Schichthoehe ableiten und
                            ist damit redundant -> Merkmal loeschen.
  - Farbe:                 ~12 % der Eintraege fehlen (kategorial ->
                            Imputation mit 'keine Angabe').
  - Druckzeit (min):       ~12 % der Eintraege fehlen (numerisch, rechtsschief
                            verteilt -> Imputation mit Median statt Mittelwert).
  - Wandstaerke (mm):      genau ein fehlender Eintrag, und zwar beim
                            problematischen Datenpunkt (analog zum
                            Kilometerstand im Autoscout24-Beispiel).
  - Ein Datenpunkt (Druck Nr. 47) ist fehlerhaft erfasst:
      * Drucktemperatur (C) enthaelt den Text '250 C' statt einer Zahl, wodurch
        die komplette Spalte beim Import als Object (statt Integer) gelesen wird.
      * Betttemperatur (C) ist mit 5 technisch gueltig, aber voellig unplausibel.
      * Wandstaerke (mm) fehlt.

Aufruf:
    python generate_3ddruck_fehlende_daten.py --n 200 --seed 8 --out ../3ddruck_fehlende_daten.csv
"""

import argparse

import numpy as np
import pandas as pd

MATERIALIEN = {
    "PLA":  {"opt_nozzle": 205, "opt_bed": 55,  "base_strength": 52, "warp_risk": 0.15},
    "PETG": {"opt_nozzle": 235, "opt_bed": 75,  "base_strength": 46, "warp_risk": 0.35},
    "ABS":  {"opt_nozzle": 245, "opt_bed": 100, "base_strength": 38, "warp_risk": 0.90},
    "ASA":  {"opt_nozzle": 255, "opt_bed": 100, "base_strength": 40, "warp_risk": 0.85},
}
MATERIAL_NAMEN = list(MATERIALIEN.keys())
MATERIAL_GEWICHTE = [0.35, 0.30, 0.20, 0.15]

FARBEN = ["schwarz", "weiß", "grau", "rot", "blau", "orange", "transparent", "gelb"]
INFILL_MUSTER = ["Gitter", "Waben", "Linear", "Gyroid"]
INFILL_STUFEN = [10, 15, 20, 25, 30, 40, 50, 60, 80, 100]
SCHICHTHOEHEN = [0.10, 0.15, 0.20, 0.25, 0.30]
WANDSTAERKEN = [0.8, 1.2, 1.6, 2.0, 2.4]

OBERFLAECHENGUETE_NACH_SCHICHTHOEHE = {
    0.10: "fein",
    0.15: "fein",
    0.20: "mittel",
    0.25: "grob",
    0.30: "grob",
}

BEMERKUNGEN_POOL = [
    "Erstversuch",
    "Nachbearbeitet, Stuetzstruktur entfernt",
    "Referenzdruck fuer Serie",
    "Toleranzpruefung durchgefuehrt",
    "Oberflaeche leicht rau",
    "Kunde: Musterbauteil, Rueckmeldung ausstehend",
    "Zweitdruck nach Fehlversuch",
    "keine besonderen Vorkommnisse",
]


def erzeuge_datensatz(n: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    material = rng.choice(MATERIAL_NAMEN, size=n, p=MATERIAL_GEWICHTE)
    farbe = rng.choice(FARBEN, size=n)
    infill_muster = rng.choice(INFILL_MUSTER, size=n)
    schichthoehe = rng.choice(SCHICHTHOEHEN, size=n)
    infill = rng.choice(INFILL_STUFEN, size=n)
    wandstaerke = rng.choice(WANDSTAERKEN, size=n)
    geschwindigkeit = rng.integers(30, 121, size=n)
    volumen = np.round(rng.uniform(15, 140, size=n), 1)

    opt_nozzle = np.array([MATERIALIEN[m]["opt_nozzle"] for m in material])
    opt_bed = np.array([MATERIALIEN[m]["opt_bed"] for m in material])
    base_strength = np.array([MATERIALIEN[m]["base_strength"] for m in material])
    warp_risk = np.array([MATERIALIEN[m]["warp_risk"] for m in material])

    drucktemperatur = np.round(opt_nozzle + rng.normal(0, 7, size=n)).astype(int)
    betttemperatur = np.round(opt_bed + rng.normal(0, 14, size=n)).astype(int)
    betttemperatur = np.clip(betttemperatur, 20, None)

    infill_anteil = 0.3 + 0.7 * np.sqrt(infill / 100)
    temp_abw = drucktemperatur - opt_nozzle
    schicht_strafe = np.maximum(0, schichthoehe - 0.20) * 35
    zugfestigkeit = (
        base_strength * infill_anteil
        - 0.030 * temp_abw ** 2
        - schicht_strafe
        + 1.0 * wandstaerke
        + rng.normal(0, 1.8, size=n)
    )
    zugfestigkeit = np.round(np.clip(zugfestigkeit, 4, None), 1)

    infill_faktor = 0.5 + 0.008 * infill
    druckzeit = (
        volumen * 1.3 / schichthoehe * infill_faktor / (geschwindigkeit / 50)
    )
    druckzeit = np.round(druckzeit / 10) * 10
    druckzeit = np.clip(druckzeit, 20, None).astype(int)

    bed_defizit = np.maximum(0, opt_bed - betttemperatur)
    speed_ueberschuss = np.maximum(0, geschwindigkeit - 70)
    warp_score = warp_risk * (0.15 * bed_defizit + 0.05 * speed_ueberschuss)
    warp_score += rng.normal(0, 0.4, size=n)
    erfolgreich = np.where(warp_score > 1.4, "nein", "ja")

    bemerkungen = rng.choice(BEMERKUNGEN_POOL, size=n)

    oberflaechenguete = np.array(
        [OBERFLAECHENGUETE_NACH_SCHICHTHOEHE[s] for s in schichthoehe]
    )

    df = pd.DataFrame({
        "Nummer": [f"Druck Nr. {i+1}" for i in range(n)],
        "Material": material,
        "Farbe": farbe,
        "Infill-Muster": infill_muster,
        "Schichthoehe (mm)": schichthoehe,
        "Oberflaechenguete": oberflaechenguete,
        "Drucktemperatur (C)": drucktemperatur,
        "Betttemperatur (C)": betttemperatur,
        "Druckgeschwindigkeit (mm/s)": geschwindigkeit,
        "Infill (%)": infill,
        "Wandstaerke (mm)": wandstaerke,
        "Bauteilvolumen (cm3)": volumen,
        "Druckzeit (min)": druckzeit,
        "Zugfestigkeit (MPa)": zugfestigkeit,
        "Erfolgreich": erfolgreich,
        "Bemerkungen": bemerkungen,
    })
    return df


def baue_luecken_ein(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Baut gezielt fehlende Werte und einen fehlerhaften Datenpunkt ein."""
    rng = np.random.default_rng(seed)
    df = df.copy()
    n = len(df)

    # Der fehlerhafte Datenpunkt: Druck Nr. 47 (Zeilenlage 46).
    fehler_pos = 46

    # Spalten als object vorbereiten, damit gemischte Eintraege moeglich sind.
    df["Farbe"] = df["Farbe"].astype("object")
    df["Oberflaechenguete"] = df["Oberflaechenguete"].astype("object")
    df["Drucktemperatur (C)"] = df["Drucktemperatur (C)"].astype("object")

    # Oberflaechenguete: ~30 % fehlend (Merkmal ist redundant zur Schichthoehe).
    anzahl_guete = round(0.30 * n)
    idx_guete = rng.choice(n, size=anzahl_guete, replace=False)
    df.iloc[idx_guete, df.columns.get_loc("Oberflaechenguete")] = np.nan

    # Farbe: ~12 % fehlend.
    anzahl_farbe = round(0.12 * n)
    idx_farbe = rng.choice(n, size=anzahl_farbe, replace=False)
    df.iloc[idx_farbe, df.columns.get_loc("Farbe")] = np.nan

    # Druckzeit (min): ~12 % fehlend, rechtsschief verteilt.
    anzahl_druckzeit = round(0.12 * n)
    idx_druckzeit = rng.choice(n, size=anzahl_druckzeit, replace=False)
    df["Druckzeit (min)"] = df["Druckzeit (min)"].astype("float")
    df.iloc[idx_druckzeit, df.columns.get_loc("Druckzeit (min)")] = np.nan

    # Wandstaerke (mm): genau ein fehlender Wert, beim fehlerhaften Datenpunkt.
    df["Wandstaerke (mm)"] = df["Wandstaerke (mm)"].astype("float")
    df.iloc[fehler_pos, df.columns.get_loc("Wandstaerke (mm)")] = np.nan

    # Fehlerhafte Erfassung beim Datenpunkt Druck Nr. 47.
    df.iloc[fehler_pos, df.columns.get_loc("Drucktemperatur (C)")] = "250 C"
    df.iloc[fehler_pos, df.columns.get_loc("Betttemperatur (C)")] = 5

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=200)
    parser.add_argument("--seed", type=int, default=8)
    parser.add_argument("--out", type=str, default="../3ddruck_fehlende_daten.csv")
    args = parser.parse_args()

    df = erzeuge_datensatz(args.n, args.seed)
    df = baue_luecken_ein(df, args.seed)
    df.to_csv(args.out, index=False)

    print(f"{args.n} Zeilen nach {args.out} geschrieben.")
    print()
    print("Fehlende Werte pro Spalte:")
    print(df.isnull().sum())
