---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 8.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 8.1 bis 8.3. Rechnen Sie mit gut eineinhalb Stunden
Bearbeitungszeit. Wie in Kapitel 7.4 besteht die Übung aus zwei Projekten.
Projekt 8.1 führt Sie in kleinen Schritten von unvollständigen Rohdaten zu
einem Modell, das fehlende Werte schätzt. In Projekt 8.2 testen Sie die
Betonmodelle aus Projekt 7.2 mit Testdaten und treffen dabei mehr
Entscheidungen selbst.

Bei den meisten Teilen finden Sie einen Kontrollwert. Damit können Sie prüfen,
ob Ihr Zwischenergebnis stimmt, bevor Sie weiterarbeiten. Die Kontrollwerte
gelten nur für die angegebenen Werte von `random_state`.

Beide Datensätze kennen Sie bereits aus früheren Kapiteln. Sie stehen über das
Download-Symbol rechts oben zur Verfügung. Speichern Sie sie in denselben
Ordner wie dieses Jupyter Notebook.

* `olympia_rio2016.csv`: Athletinnen und Athleten der Olympischen
  Sommerspiele 2016 in acht Sportarten, ohne Namen, Spaltennamen und Einträge
  ins Deutsche übersetzt (Quelle: [R. H. Griffin, 120 years of Olympic
  history: athletes and results,
  Kaggle](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results),
  Lizenz CC0)
* `beton_DE.csv`: 1030 Laborversuche zur Druckfestigkeit von Beton,
  Spaltennamen ins Deutsche übersetzt (Quelle: [I-C. Yeh, Concrete Compressive
  Strength, UCI Machine Learning Repository](https://doi.org/10.24432/C5PK67),
  Lizenz CC BY 4.0)

## Projekt 8.1: Fehlende Gewichte schätzen

In Aufgabe 5.5 haben wir festgestellt, dass im Olympia-Datensatz bei 13
Personen das Gewicht fehlt. In Kapitel 8.1 haben wir fehlende Zahlenwerte durch
den Mittelwert oder den Median ersetzt. Als bessere Alternative haben wir dort
ein Regressionsmodell genannt, das die fehlenden Werte aus den übrigen
Merkmalen schätzt. Genau das probieren wir jetzt aus. Dasselbe Vorgehen hilft
auch in der Produktion: Fällt ein Sensor aus, lassen sich seine Messwerte oft
aus den Werten der anderen Sensoren schätzen. Rechnen Sie mit etwa 40 Minuten.

### Teil 1: Fehlende Werte untersuchen

Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein.

1. Ermitteln Sie, wie viele Werte pro Merkmal fehlen.
2. In der Spalte `Medaille` fehlen die meisten Einträge. Aus Aufgabe 5.5
   wissen Sie, dass das kein Datenfehler ist. Vervollständigen Sie die Spalte
   mit einem passenden Ersatzwert.
3. Lassen Sie sich alle Personen anzeigen, bei denen das Gewicht fehlt. Bei
   wie vielen von ihnen fehlt auch die Körpergröße? Welche Sportart fällt auf?

Zur Kontrolle: Insgesamt fehlen im Datensatz 1986 Werte, davon 1963 in der
Spalte `Medaille`.

```{code-cell} python
# Code-Zelle
```

### Teil 2: Kategoriale Merkmale kodieren

Bringen Sie die kategorialen Merkmale in eine Form, mit der ein ML-Modell
rechnen kann.

1. Kodieren Sie das Geschlecht mit 0 für w und 1 für m.
2. Die Medaille ist ein geordnetes Merkmal. Kodieren Sie sie so, dass die
   Reihenfolge erhalten bleibt, von 0 für keine Medaille bis 3 für Gold.
3. Kodieren Sie die Sportart mit der One-Hot-Kodierung. Die neuen Spalten
   sollen Nullen und Einsen enthalten.
4. Das Land kodieren wir nicht. Wie viele neue Spalten würde die
   One-Hot-Kodierung des Landes erzeugen? Warum ist das ungünstig?

Zur Kontrolle: Die Summe der kodierten Spalte `Medaille` beträgt 1100. Der
Datensatz hat nach der Kodierung 14 Spalten.

```{code-cell} python
# Code-Zelle
```

### Teil 3: Ein Modell für das Gewicht

Für das Training brauchen wir Personen, bei denen Körpergröße und Gewicht
bekannt sind.

1. Entfernen Sie alle Personen, bei denen das Gewicht oder die Körpergröße
   fehlt. Speichern Sie das Ergebnis unter einem neuen Namen, denn die
   Personen ohne Gewicht brauchen wir in Teil 4 noch. Tipp: Sie können der
   Methode `drop()` statt eines einzelnen Zeilenindex auch den Zeilenindex
   eines gefilterten DataFrames übergeben. Dann löscht sie alle diese Zeilen
   auf einmal.
2. Teilen Sie die vollständigen Daten in Trainings- und Testdaten auf, mit
   20 % Testdaten und `random_state=0`.
3. Trainieren Sie lineare Regressionsmodelle mit dem Gewicht als Zielgröße und
   vergleichen Sie jeweils die R²-Scores auf den Trainings- und Testdaten.
   Beginnen Sie mit der Körpergröße als einzigem Merkmal. Nehmen Sie dann das
   Geschlecht hinzu, danach die Sportart und zum Schluss auch Alter und
   Medaille. Tipp: Mit `drop()` erhalten Sie schnell alle Spalten außer
   denen, die Sie nicht als Merkmal verwenden wollen.
4. Zum Vergleich: Ersetzen wir jedes fehlende Gewicht durch den Median wie in
   Kapitel 8.1, prognostizieren wir für alle Personen dasselbe Gewicht.
   Welchen R²-Score erreicht diese Prognose auf den Testdaten? Berechnen Sie
   den Median nur aus den Trainingsdaten. Tipp: Die Funktion `r2_score()` aus
   Kapitel 8.3 bewertet auch Prognosen, die nicht von einem Scikit-Learn-Modell
   stammen. Wenn Sie beim Erzeugen eines DataFrames für eine Spalte eine
   einzelne Zahl angeben, übernimmt Pandas diese Zahl für alle Zeilen.
5. Welches Modell würden Sie zum Schätzen der fehlenden Gewichte verwenden?

Zur Kontrolle: Es bleiben 2504 vollständige Datenpunkte. Mit der Körpergröße
allein erreicht das Modell auf den Testdaten einen R²-Score von 0.55.

```{code-cell} python
# Code-Zelle
```

### Teil 4: Fehlende Gewichte schätzen

Schätzen Sie mit dem Modell aus Körpergröße, Geschlecht und Sportart das
Gewicht aller Personen, bei denen nur das Gewicht fehlt, die Körpergröße aber
bekannt ist. Tragen Sie die Schätzwerte in den Datensatz ein. Tipp: Wie in
Kapitel 8.3 beim Einfärben nach Splitstatus können Sie mit `.loc[]` und einem
Zeilenindex mehrere Zeilen auf einmal beschreiben.

1. Bei wie vielen Personen fehlt das Gewicht danach noch?
2. Sind die Schätzwerte plausibel? Beim Judo treten die Männer in sieben
   Gewichtsklassen an, von bis 60 kg bis über 100 kg.

Zur Kontrolle: Für die Basketballerin mit der Nr. 262 schätzt das Modell ein
Gewicht von 51.2 kg.

```{code-cell} python
# Code-Zelle
```

### Abschlussfrage

Bei 7 Personen fehlt das Gewicht weiterhin. Warum hilft unser Modell hier
nicht, und was würden Sie mit diesen Personen machen? Vergleichen Sie außerdem
die beiden Strategien aus Kapitel 8.1, den Median und das Regressionsmodell.
Wann lohnt sich der Aufwand für ein Modell?

## Projekt 8.2: Betonmodelle fair testen

In Projekt 7.2 haben wir Modelle für die Druckfestigkeit von Beton trainiert
und mit dem R²-Score bewertet. Dabei haben wir den R²-Score auf denselben
Daten berechnet, mit denen wir die Modelle trainiert haben. Ob die Modelle
auch für neue Probekörper taugen, wissen wir deshalb nicht. Das holen wir
jetzt nach. Wir halten einen Teil der Laborversuche als Testdaten zurück,
vergleichen verschiedene Modelle und entscheiden, welches wir dem Betonwerk
empfehlen. Projekt 8.2 ist offener als Projekt 8.1. Rechnen Sie mit etwa 50
Minuten.

### Teil 1: Die Modelle aus Projekt 7.2 fair testen

Lesen Sie die Datei `beton_DE.csv` mit der Spalte `Nr.` als Zeilenindex ein und
ergänzen Sie wie in Projekt 7.2 die Spalte `Alter hoch 2`. Teilen Sie die Daten
in Trainings- und Testdaten auf, mit 20 % Testdaten und `random_state=0`.

Trainieren Sie die beiden Modelle aus Projekt 7.2 erneut, diesmal nur mit den
Trainingsdaten: die multiple lineare Regression mit den sieben Bestandteilen
und dem Alter sowie dasselbe Modell mit dem zusätzlichen Merkmal `Alter hoch 2`.

1. Vergleichen Sie für beide Modelle die R²-Scores auf den Trainings- und
   Testdaten. Liegt Overfitting vor?
2. In Projekt 7.2 erreichten die beiden Modelle R²-Scores von 0.62 und 0.74.
   Passen die neuen Werte dazu?

Zur Kontrolle: Die Testdaten enthalten 206 Probekörper.

```{code-cell} python
# Code-Zelle
```

### Teil 2: Welcher Bestandteil wirkt am stärksten?

Lassen Sie sich die Koeffizienten des Modells mit acht Merkmalen aus Teil 1
ausgeben. Das Fließmittel hat den größten Koeffizienten. Ist es deshalb der
wichtigste Bestandteil? Vergleichen Sie dazu die Wertebereiche der Merkmale in
den Trainingsdaten.

Standardisieren Sie die acht Merkmale und trainieren Sie das Modell erneut.
Passen Sie die Standardisierung nur an die Trainingsdaten an. Nach dem
Standardisieren gibt jeder Koeffizient an, um wie viel MPa sich die
Druckfestigkeit ändert, wenn das Merkmal um eine Standardabweichung zunimmt.
Damit lassen sich die Koeffizienten direkt vergleichen.

1. Welcher Bestandteil wirkt jetzt am stärksten, welcher am schwächsten?
2. Wie verändert sich der R²-Score auf den Testdaten durch die
   Standardisierung?

Zur Kontrolle: In den Trainingsdaten hat das Fließmittel eine
Standardabweichung von 6.0 kg/m³.

```{code-cell} python
# Code-Zelle
```

### Teil 3: Polynome höheren Grades

In Kapitel 7.3 haben wir mit `PolynomialFeatures` aus den Merkmalen Potenzen
und Produkte erzeugt. Damit die höheren Potenzen nicht riesig werden,
normieren Sie die acht Merkmale aus Teil 1 zuerst auf das Intervall von 0 bis
1. Passen Sie die Normierung nur an die Trainingsdaten an. Trainieren Sie
danach polynomiale Regressionsmodelle mit den Graden 1 bis 4.

1. Notieren Sie für jeden Grad die Anzahl der Spalten nach der Transformation
   sowie die R²-Scores auf den Trainings- und Testdaten.
2. Welcher Grad ist am besten? Was passiert beim Grad 4, und woran liegt das?
   Vergleichen Sie die Anzahl der Spalten mit der Anzahl der Trainingsdaten.

Zur Kontrolle: Mit dem Grad 2 entstehen aus den acht Merkmalen 45 Spalten.

```{code-cell} python
# Code-Zelle
```

### Teil 4: Entscheidungsbaum

Trainieren Sie einen `DecisionTreeRegressor` mit `random_state=0` und den acht
Merkmalen aus Teil 1, zunächst ohne Begrenzung der Tiefe. Eine Skalierung ist
für Entscheidungsbäume nicht nötig.

1. Wie tief wird der Baum? Vergleichen Sie die R²-Scores auf den Trainings-
   und Testdaten.
2. Begrenzen Sie die Tiefe auf 4 und auf 8. Verbessert sich der R²-Score auf
   den Testdaten?

Zur Kontrolle: Der Baum ohne Begrenzung hat die Tiefe 20.

```{code-cell} python
# Code-Zelle
```

### Abschlussfrage

Stellen Sie die R²-Scores aller Modelle auf den Trainings- und Testdaten in
einer Tabelle zusammen. Welches Modell würden Sie dem Betonwerk empfehlen?

Wiederholen Sie danach die Aufteilung mit `random_state=1` und führen Sie alle
Teile erneut aus. Bleibt Ihre Empfehlung dieselbe?

Was sagt der Testscore über die Prognosegüte für ganz neue Rezepturen aus?
Tipp: Denken Sie an Teil 4 von Projekt 7.2. Dort wurde dieselbe Rezeptur
siebenmal geprüft, nach unterschiedlich vielen Tagen.
