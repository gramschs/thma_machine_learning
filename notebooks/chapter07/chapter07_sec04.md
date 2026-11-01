---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 7.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 7.1 bis 7.3. Rechnen Sie mit gut eineinhalb Stunden
Bearbeitungszeit. Diesmal besteht die Übung aus zwei Projekten. Beide folgen
dem Ablauf, den wir auch in größeren ML-Projekten verwenden: Daten erkunden,
Daten ins richtige Format bringen, Modelle trainieren und bewerten, Prognosen
treffen und die Ergebnisse kritisch prüfen. Projekt 7.1 führt Sie in kleinen
Schritten durch diesen Ablauf. In Projekt 7.2 treffen Sie mehr Entscheidungen
selbst.

Bei den meisten Teilen finden Sie einen Kontrollwert. Damit können Sie prüfen,
ob Ihr Zwischenergebnis stimmt, bevor Sie weiterarbeiten.

Beide Datensätze stehen über das Download-Symbol rechts oben zur Verfügung.
Speichern Sie sie in denselben Ordner wie dieses Jupyter Notebook.

* `bevoelkerung_deutschland.csv`: Einwohnerzahl Deutschlands in den Jahren
  1800 bis 2021, Spaltennamen ins Deutsche übersetzt (Quelle: [Our World in
  Data, Population](https://ourworldindata.org/population-sources), Stand 2021,
  bis 1950 nach Gapminder, ab 1950 nach UN World Population Prospects 2019,
  Lizenz CC BY 4.0)
* `beton_DE.csv`: 1030 Laborversuche zur Druckfestigkeit von Beton,
  Spaltennamen ins Deutsche übersetzt (Quelle: [I-C. Yeh, Concrete Compressive
  Strength, UCI Machine Learning Repository](https://doi.org/10.24432/C5PK67),
  Lizenz CC BY 4.0)

## Projekt 7.1: Bevölkerung in Deutschland bis 2100

Wie viele Menschen werden im Jahr 2100 in Deutschland leben? Solche Prognosen
braucht zum Beispiel die Energiewirtschaft, um den Strombedarf der nächsten
Jahrzehnte abzuschätzen. Die Datei `bevoelkerung_deutschland.csv` enthält die
Einwohnerzahl Deutschlands für jedes Jahr von 1800 bis 2021. Wir trainieren
verschiedene Regressionsmodelle mit dem Jahr als Merkmal und vergleichen ihre
Prognosen. Rechnen Sie mit etwa 40 Minuten.

### Teil 1: Daten erkunden

Lesen Sie die Datei ein und verschaffen Sie sich einen Überblick. Wie viele
Datenpunkte gibt es? Welche Spalten und Datentypen enthält die Tabelle? Fehlen
Werte? Welche Spalten sind für unsere Fragestellung überflüssig?

Erweitern Sie die Tabelle um eine Spalte `Einwohner (Mio.)` mit der
Einwohnerzahl in Millionen. Erstellen Sie einen Scatterplot mit dem Jahr auf
der x-Achse und der Einwohnerzahl in Millionen auf der y-Achse. In welchen
Zeiträumen ist die Bevölkerung zurückgegangen? Haben Sie eine Erklärung?

Zur Kontrolle: Im Jahr 1800 lebten 18 Mio. Menschen in Deutschland.

```{code-cell} python
# Code-Zelle
```

### Teil 2: Einfache lineare Regression

Trainieren Sie ein lineares Regressionsmodell mit dem Jahr als Merkmal und der
Einwohnerzahl in Millionen als Zielgröße.

1. Wie gut erklärt das Modell die Daten laut R²-Score?
2. Notieren Sie die Modellgleichung. Um wie viele Menschen wächst die
   Bevölkerung laut Modell pro Jahr? Welche Bedeutung hat der
   y-Achsenabschnitt hier, und ist sein Wert plausibel?
3. Welche Einwohnerzahlen prognostiziert das Modell für die Jahre 2030 und
   2100?

Zur Kontrolle: Der R²-Score beträgt 0.9717.

```{code-cell} python
# Code-Zelle
```

### Teil 3: Polynomiale Regression

Trainieren Sie zusätzlich polynomiale Regressionsmodelle mit den Polynomgraden
2 und 3. Bleiben Sie bei höchstens Grad 3. Bei Jahreszahlen um 2000 werden die
höheren Potenzen so riesig (2000 hoch 4 sind schon 16 Billionen), dass die
Rechnung ungenau wird.

1. Vergleichen Sie die R²-Scores und die Prognosen für 2030 und 2100 der drei
   Modelle mit den Graden 1, 2 und 3.
2. Stellen Sie die Messwerte zusammen mit den Kurven aller drei Modelle für die
   Jahre 1800 bis 2100 in einem gemeinsamen Diagramm dar. Welcher
   Kurvenverlauf nach 2021 erscheint Ihnen plausibel?

Zur Kontrolle: Mit dem Grad 2 beträgt der R²-Score 0.9856.

```{code-cell} python
# Code-Zelle
```

### Teil 4: Entscheidungsbaum zum Vergleich

In Kapitel 6 haben wir Entscheidungsbäume für Klassifikationsaufgaben
kennengelernt. Für Regressionsaufgaben gibt es in Scikit-Learn das Modell
`DecisionTreeRegressor`. Es wird ebenfalls aus `sklearn.tree` importiert und
genauso verwendet wie `DecisionTreeClassifier`. Statt einer Klasse
prognostiziert jedes Blatt eine Zahl, nämlich den Mittelwert der Zielgröße
aller Trainingsdaten in diesem Blatt.

Trainieren Sie einen Entscheidungsbaum ohne Begrenzung der Tiefe mit
`random_state=0`. Welchen R²-Score erreicht er? Welche Einwohnerzahlen
prognostiziert er für 2030 und 2100? Ergänzen Sie seine Kurve im Diagramm aus
Teil 3 und erklären Sie den Verlauf nach 2021.

Zur Kontrolle: Der Baum hat die Tiefe 14.

```{code-cell} python
# Code-Zelle
```

### Abschlussfrage

Sie sollen eine Prognose für die Einwohnerzahl im Jahr 2100 abgeben. Für
welches der vier Modelle würden Sie sich entscheiden? Was sagt der R²-Score
über die Qualität dieser Prognose aus?

## Projekt 7.2: Druckfestigkeit von Beton

Beton ist der meistverwendete Baustoff der Welt, im Maschinenbau zum Beispiel
für Maschinenfundamente. Seine wichtigste Kenngröße ist die Druckfestigkeit.
Sie hängt von der Rezeptur ab und vom Alter, denn Beton härtet über Wochen und
Monate aus. Für die Einteilung in Festigkeitsklassen wird die Druckfestigkeit
nach 28 Tagen geprüft. Ein Betonwerk möchte die Druckfestigkeit neuer
Rezepturen abschätzen, bevor es aufwendige Versuche durchführt.

Die Datei `beton_DE.csv` enthält 1030 Laborversuche. Jede Zeile beschreibt
einen Probekörper: die Mengen der sieben Bestandteile in kg pro Kubikmeter
Beton, das Alter in Tagen bei der Prüfung und die gemessene Druckfestigkeit in
MPa. Neben Zement, Wasser, Grobzuschlag (Kies) und Feinzuschlag (Sand)
enthalten viele Rezepturen drei weitere Bestandteile:

* Hüttensand fällt bei der Roheisenherstellung im Hochofen an und ersetzt
  einen Teil des Zements.
* Flugasche stammt aus Kohlekraftwerken und ersetzt ebenfalls einen Teil des
  Zements.
* Fließmittel macht den frischen Beton flüssiger, ohne dass dafür mehr Wasser
  nötig ist.

Projekt 7.2 ist offener als Projekt 7.1. Sie entscheiden häufiger selbst, wie
Sie vorgehen. Rechnen Sie mit etwa 50 Minuten.

### Teil 1: Daten erkunden und erstes Modell

Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein und verschaffen
Sie sich einen Überblick. Lassen Sie dann die Korrelationsmatrix als Heatmap
anzeigen. Tipp: Mit der Option `text_auto='.2f'` zeigt die Heatmap die Werte
mit zwei Nachkommastellen an.

1. Welches Merkmal hängt am stärksten linear mit der Druckfestigkeit zusammen?
   Welche Merkmale hängen negativ mit ihr zusammen?
2. Trainieren Sie mit dem stärksten Merkmal ein einfaches lineares
   Regressionsmodell. Notieren Sie die Modellgleichung und interpretieren Sie
   die Steigung. Wie gut erklärt das Modell die Druckfestigkeit?

Zur Kontrolle: Im Mittel haben die Probekörper eine Druckfestigkeit von
35.8 MPa.

```{code-cell} python
# Code-Zelle
```

### Teil 2: Multiple lineare Regression

Trainieren Sie ein multiples lineares Regressionsmodell mit allen sieben
Bestandteilen der Rezeptur. Nehmen Sie danach das Alter als achtes Merkmal
hinzu.

1. Wie verändert sich der R²-Score gegenüber Teil 1, erst mit der ganzen
   Rezeptur und dann zusätzlich mit dem Alter?
2. Lassen Sie sich die Koeffizienten des Modells mit acht Merkmalen ausgeben.
   Tipp: Speichern Sie die Koeffizienten in einer Series mit den
   Merkmalsnamen als Index, dann ist die Ausgabe übersichtlicher.
   Interpretieren Sie die Koeffizienten von Wasser und Alter.
3. Die Flugasche hängt laut Korrelationsmatrix negativ mit der
   Druckfestigkeit zusammen. Welches Vorzeichen hat ihr Koeffizient im Modell?
   Erklären Sie den scheinbaren Widerspruch. Tipp: Schauen Sie in der Heatmap
   nach, wie Flugasche und Zement zusammenhängen.

Zur Kontrolle: Mit den sieben Bestandteilen erreicht das Modell einen R²-Score
von 0.45.

```{code-cell} python
# Code-Zelle
```

### Teil 3: Das Alter genauer betrachten

Erstellen Sie einen Scatterplot mit dem Alter auf der x-Achse und der
Druckfestigkeit auf der y-Achse. Beschreiben Sie den Verlauf. Passt dazu ein
Modell, in dem die Druckfestigkeit linear vom Alter abhängt?

Nutzen Sie den Trick aus Kapitel 7.3: Erweitern Sie die Tabelle um eine Spalte
`Alter hoch 2` mit dem Quadrat des Alters. Trainieren Sie das Modell aus Teil 2
mit diesem zusätzlichen Merkmal. Wie verändert sich der R²-Score?

Zur Kontrolle: Versuch Nr. 1 wurde nach 28 Tagen geprüft, in der neuen Spalte
steht dort 784.

```{code-cell} python
# Code-Zelle
```

### Teil 4: Prognose für eine Rezeptur

Für die Rezeptur mit 540 kg Zement, 173 kg Wasser, 1125 kg Grobzuschlag und
613 kg Feinzuschlag pro Kubikmeter, ohne Hüttensand, Flugasche und
Fließmittel, enthält der Datensatz Messungen nach unterschiedlich vielen Tagen.

1. Filtern Sie diese Versuche aus der Tabelle. Tipp: Zement und Wasser reichen
   dafür aus.
2. Lassen Sie die Modelle aus Teil 2 und Teil 3 die Druckfestigkeit dieser
   Rezeptur für ein Alter von 1 bis 730 Tagen prognostizieren. Stellen Sie die
   Messwerte und beide Prognosekurven in einem gemeinsamen Diagramm dar.
   Tipp: Wenn Sie beim Erzeugen eines DataFrames für eine Spalte eine einzelne
   Zahl statt einer Liste angeben, übernimmt Pandas diese Zahl für alle
   Zeilen. Wählen Sie für jedes Modell genau die Spalten aus, mit denen es
   trainiert wurde.
3. Welches Modell beschreibt die Messwerte besser? Lesen Sie im Diagramm ab,
   welche Druckfestigkeit die beiden Modelle nach zwei Jahren prognostizieren.
   Ist das plausibel?

Zur Kontrolle: Die Rezeptur wurde siebenmal geprüft. Nach 28 Tagen erreichte
sie 67.31 MPa.

```{code-cell} python
# Code-Zelle
```

### Abschlussfrage

Fassen Sie zusammen, wie sich der R²-Score von Teil 1 bis Teil 3 entwickelt
hat. Welches Modell würden Sie dem Betonwerk empfehlen, und für welche
Prognosen sollte es nicht eingesetzt werden? Was können Sie über die
Prognosegüte für neue Rezepturen sagen, die nicht im Datensatz enthalten sind?
