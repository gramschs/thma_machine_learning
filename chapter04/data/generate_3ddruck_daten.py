"""
Generator fuer den 3D-Druck-Datensatz (FDM-Druckauftraege).

Erzeugt einen Datensatz mit realistisch eingebauten, NICHT-linearen und
interaktiven Zusammenhaengen, damit spaetere Kapitel (lineare Regression vs.
Decision Trees / Random Forest / XGBoost vs. neuronale Netze) einen echten,
sichtbaren Methodenunterschied zeigen koennen:

  - Zugfestigkeit (MPa):   hat ein Optimum bei materialspezifischer
                            Drucktemperatur (invertierte Parabel), steigt mit
                            Infill nur mit abnehmendem Grenznutzen (log),
                            sinkt bei zu grosser Schichthoehe.
  - Erfolgreich (ja/nein): haengt von einer INTERAKTION aus Material,
                            Betttemperatur und Druckgeschwindigkeit ab
                            (Warping-Risiko) -- ein klassisches
                            Schwellenwert-/Interaktionsmuster, das lineare
                            Modelle nicht gut abbilden koennen, Baeume aber
                            schon.
  - Druckzeit (min):       haengt vom Bauteilvolumen, der Schichthoehe, dem
                            Infill und der Druckgeschwindigkeit ab.

Aufruf:
    python generate_3ddruck_daten.py --n 18 --seed 42 --out 3ddruck_xxs.csv

Fuer spaetere, groessere ML-Kapitel kann derselbe Generator mit hoeherem
--n erneut aufgerufen werden (--seed variieren fuer neue Zufallsstichproben),
sodass Trainings- und Testdaten aus derselben zugrunde liegenden Logik
stammen wie das Einfuehrungsbeispiel in Kapitel 4.1.
"""

import argparse

import numpy as np
import pandas as pd

MATERIALIEN = {
    # opt_nozzle, opt_bed in °C; base_strength in MPa (Grenzwert bei
    # optimaler Temperatur und 100 % Infill); warp_risk: relatives Risiko
    # fuer Warping/Ablösung (0 = gering, 1 = hoch)
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

BEMERKUNGEN_POOL = [
    "Erstversuch",
    "Nachbearbeitet, Stuetzstruktur entfernt",
    "Referenzdruck fuer Serie",
    "Toleranzpruefung durchgefuehrt",
    "Oberflaeche leicht rau",
    "Kunde: Musterbauteil, Rueckmeldung ausstehend",
    "Zweitdruck nach Fehlversuch",
    "",
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

    # --- Zugfestigkeit: nichtlineare Effekte + Interaktionen ---
    # Infill wirkt mit abnehmendem Grenznutzen (Wurzelfunktion), nicht linear
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

    # --- Druckzeit: haengt von Volumen, Schichthoehe, Infill, Speed ab ---
    infill_faktor = 0.5 + 0.008 * infill
    druckzeit = (
        volumen * 1.3 / schichthoehe * infill_faktor / (geschwindigkeit / 50)
    )
    druckzeit = np.round(druckzeit / 10) * 10  # auf 10 min runden
    druckzeit = np.clip(druckzeit, 20, None).astype(int)

    # --- Erfolgreich: Interaktion aus Material, Betttemperatur, Speed ---
    bed_defizit = np.maximum(0, opt_bed - betttemperatur)
    speed_ueberschuss = np.maximum(0, geschwindigkeit - 70)
    warp_score = warp_risk * (0.15 * bed_defizit + 0.05 * speed_ueberschuss)
    warp_score += rng.normal(0, 0.4, size=n)
    erfolgreich = np.where(warp_score > 1.4, "nein", "ja")

    bemerkungen = rng.choice(BEMERKUNGEN_POOL, size=n)

    df = pd.DataFrame({
        "Nummer": [f"Druck Nr. {i+1}" for i in range(n)],
        "Material": material,
        "Farbe": farbe,
        "Infill-Muster": infill_muster,
        "Schichthoehe (mm)": schichthoehe,
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
    parser.add_argument("--n", type=int, default=18)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default="3ddruck_xxs.csv")
    args = parser.parse_args()

    df = erzeuge_datensatz(args.n, args.seed)
    df.to_csv(args.out, index=False)
    print(f"{args.n} Zeilen nach {args.out} geschrieben.")
    print(df["Erfolgreich"].value_counts())
