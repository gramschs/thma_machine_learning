"""
Generator fuer den 3D-Druck-Datensatz fuer die GITTERSUCHE.

Dieser Datensatz wird in Kapitel 10.2 (Gittersuche) fuer die Mini-Uebungen
verwendet. Waehrend der Vorlesungsstoff an kuenstlichen Daten (make_moons)
demonstriert wird, ueben die Studierenden die Suche nach Hyperparametern am
3D-Druck-Beispiel ein.

Unterschied zu 3ddruck_kodierung.csv (Kapitel 8.2): Die Schwelle fuer einen
Fehldruck durch Verzug ist von 1.4 auf 0.6 gesenkt. Dadurch sind rund 40 % der
Druckauftraege nicht erfolgreich statt rund 15 %. Bei nur 15 % Fehldrucken
erreicht schon ein Modell, das immer "ja" vorhersagt, einen Score von 0.85, und
die Entscheidungsbaeume schlagen es kaum. Fuer die Mini-Uebungen soll der
Vergleich verschiedener Baumtiefen aber sichtbare Unterschiede zeigen.

Merkmale, die in den Mini-Uebungen gebraucht werden:

  - Drucktemperatur (C):          verraet indirekt das Material (PLA etwa
                                  205 C, ABS/ASA etwa 245 bis 255 C) und damit
                                  das Verzugsrisiko.
  - Betttemperatur (C):           zu kaltes Druckbett -> Verzug.
  - Druckgeschwindigkeit (mm/s):  ueber 70 mm/s steigt das Verzugsrisiko.
  - Erfolgreich:                  Zielgroesse (ja/nein).

Die Basislogik ist eine Kopie aus chapter08/data/generate_3ddruck_kodierung.py
(und damit aus chapter04/data/generate_3ddruck_daten.py). Sie ist hier bewusst
dupliziert, damit dieser Datensatz stabil bleibt, auch wenn die anderen
Generatoren spaeter veraendert werden.

Aufruf:
    python generate_3ddruck_gittersuche.py --n 300 --seed 1002 --out ../3ddruck_gittersuche.csv
"""

import argparse

import numpy as np
import pandas as pd

# Ab diesem Verzugswert gilt ein Druck als nicht erfolgreich (Kapitel 8.2: 1.4).
FEHLDRUCK_SCHWELLE = 0.6

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
    erfolgreich = np.where(warp_score > FEHLDRUCK_SCHWELLE, "nein", "ja")

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=300)
    parser.add_argument("--seed", type=int, default=1002)
    parser.add_argument("--out", type=str, default="../3ddruck_gittersuche.csv")
    args = parser.parse_args()

    df = erzeuge_datensatz(args.n, args.seed)
    df.to_csv(args.out, index=False)

    print(f"{args.n} Zeilen nach {args.out} geschrieben.")
    print()
    print("Erfolgreich:", df["Erfolgreich"].value_counts().to_dict())
    print("Fehlende Werte pro Spalte:", int(df.isnull().sum().sum()))
