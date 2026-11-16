---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 9.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 9.1 bis 9.3. Rechnen Sie mit gut eineinhalb Stunden
Bearbeitungszeit. Die Übung besteht aus zwei Projekten. In Projekt 9.1 lernen
Sie einen neuen Datensatz kennen und vergleichen Schritt für Schritt einen
Entscheidungsbaum, einen Random Forest und XGBoost bei einer
Klassifikationsaufgabe. In Projekt 9.2 kehren Sie zum Beton aus den Projekten
7.2 und 8.2 zurück und übertragen die Ensemble-Methoden auf eine
Regressionsaufgabe. Dabei treffen Sie mehr Entscheidungen selbst.

Bei den meisten Teilen finden Sie einen Kontrollwert. Damit können Sie prüfen,
ob Ihr Zwischenergebnis stimmt, bevor Sie weiterarbeiten. Die Kontrollwerte
gelten nur für die angegebenen Werte von `random_state`. Für beide Projekte
brauchen Sie XGBoost.

Beide Datensätze stehen über das Download-Symbol rechts oben zur Verfügung.
Speichern Sie sie in denselben Ordner wie dieses Jupyter Notebook.

* `waldtypen_colorado.csv`: Stichprobe von 20 000 Waldflächen im Roosevelt
  National Forest in Colorado, Spaltennamen und Einträge ins Deutsche
  übersetzt (Quelle: [J. Blackard, Covertype, UCI Machine Learning
  Repository](https://doi.org/10.24432/C50K5N), Lizenz CC BY 4.0)
* `beton_DE.csv`: 1030 Laborversuche zur Druckfestigkeit von Beton,
  Spaltennamen ins Deutsche übersetzt (Quelle: [I-C. Yeh, Concrete Compressive
  Strength, UCI Machine Learning Repository](https://doi.org/10.24432/C5PK67),
  Lizenz CC BY 4.0)

## Projekt 9.1: Welcher Wald wächst hier?

In den Rocky Mountains im Norden von Colorado hat die US-Forstverwaltung für
sehr viele Flächen von 30 m × 30 m erfasst, welcher Waldtyp dort wächst. Jede
Fläche zu begehen ist aufwendig. Kartendaten wie die Höhe, die Hangneigung oder
der Abstand zum nächsten Gewässer liegen dagegen für jede Fläche vor. Lässt sich
der Waldtyp aus diesen Kartendaten prognostizieren? Wir lassen also einen
Random Forest einen echten Wald vorhersagen.

Die Datei `waldtypen_colorado.csv` enthält 20 000 Flächen aus vier
Schutzgebieten. Zu jeder Fläche gibt es sieben Messgrößen:

* die Höhe über dem Meeresspiegel in m,
* die Ausrichtung, also die Himmelsrichtung, in die der Hang zeigt, in Grad
  (0 für Norden, 90 für Osten, 180 für Süden, 270 für Westen),
* die Hangneigung in Grad,
* den waagerechten Abstand und den Höhenunterschied zum nächsten Gewässer in m,
* den Abstand zur nächsten Straße in m,
* den Abstand zur nächsten Stelle, an der ein Waldbrand ausgebrochen ist, in m.

Dazu kommen das Schutzgebiet (`Gebiet`) und der Waldtyp. Es gibt sieben
Waldtypen: Fichte/Tanne, Drehkiefer, Gelbkiefer, Pappel/Weide, Espe, Douglasie
und Krummholz. Rechnen Sie mit etwa 50 Minuten.

### Teil 1: Daten erkunden

Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein und verschaffen
Sie sich einen Überblick.

1. Wie oft kommt jeder Waldtyp vor? Welche Accuracy erreicht ein Modell, das
   immer den häufigsten Waldtyp prognostiziert?
2. Stellen Sie die Höhe für jeden Waldtyp in einem Boxplot dar. Welche
   Waldtypen wachsen weit oben, welche weiter unten? Reicht die Höhe allein, um
   die Waldtypen zu unterscheiden?

Zur Kontrolle: Auf 9760 Flächen wächst Drehkiefer.

```{code-cell} python
# Code-Zelle
```

### Teil 2: Entscheidungsbaum gegen Random Forest

Kodieren Sie das Gebiet mit der One-Hot-Kodierung. Teilen Sie die Daten in
Trainings- und Testdaten auf, mit 20 % Testdaten und `random_state=0`. Sorgen
Sie dafür, dass die Anteile der Waldtypen in beiden Teilen gleich bleiben,
denn manche Waldtypen sind sehr selten.

Trainieren Sie einen Entscheidungsbaum ohne Begrenzung der Tiefe und einen
Random Forest mit 100 Bäumen, beide mit `random_state=0`.

1. Vergleichen Sie die Accuracy auf den Trainings- und Testdaten. Bei welchem
   Modell sehen Sie Overfitting?
2. Wie viel besser als das Modell aus Teil 1, das immer Drehkiefer
   prognostiziert, sind die beiden Modelle?

Zur Kontrolle: Der Entscheidungsbaum hat die Tiefe 29.

```{code-cell} python
# Code-Zelle
```

### Teil 3: Feature Importance

Stellen Sie die Feature Importance des Random Forests als Balkendiagramm dar,
sortiert nach ihrer Größe.

1. Welches Merkmal ist am wichtigsten? Passt das zu Ihrem Boxplot aus Teil 1?
2. Auf den Plätzen zwei und drei liegen der Abstand zur nächsten Straße und
   der Abstand zur nächsten Brandstelle. Wächst eine Fichte, weil die Straße
   weit weg ist? Was zeigt die Feature Importance, und was zeigt sie nicht?

Zur Kontrolle: Die Höhe hat eine Feature Importance von 0.329.

```{code-cell} python
# Code-Zelle
```

### Teil 4: XGBoost

XGBoost erwartet die Klassen als ganze Zahlen von 0 bis 6. Kodieren Sie den
Waldtyp in den Trainings- und Testdaten entsprechend. Welcher Waldtyp welche
Zahl bekommt, spielt keine Rolle.

Trainieren Sie dann ein XGBoost-Modell mit 200 Boosting-Runden und
`random_state=0`. Lassen Sie dabei den Log Loss für die Trainings- und
Testdaten mitprotokollieren. Bei mehr als zwei Klassen heißt diese Maßzahl in
XGBoost `'mlogloss'`.

1. Vergleichen Sie die Accuracy auf den Testdaten mit dem Random Forest.
2. Stellen Sie den Log Loss in jeder Boosting-Runde dar. Ab etwa welcher Runde
   ändert sich der Log Loss auf den Testdaten kaum noch? Würde frühes Stoppen
   hier helfen?

Zur Kontrolle: Auf den Trainingsdaten erreicht XGBoost eine Accuracy von
0.991.

```{code-cell} python
# Code-Zelle
```

### Abschlussfrage

Welches der drei Modelle würden Sie der Forstverwaltung empfehlen?

## Projekt 9.2: Beton, die dritte Runde

In Projekt 8.2 haben wir verschiedene Modelle für die Druckfestigkeit von Beton
mit Testdaten geprüft. Am besten schnitten das Polynom 3. Grades und der
Entscheidungsbaum ab. Jetzt treten die Ensemble-Methoden gegen sie an. Rechnen
Sie mit etwa 40 Minuten.

### Teil 1: Random Forest und XGBoost

Lesen Sie die Datei `beton_DE.csv` mit der Spalte `Nr.` als Zeilenindex ein und
teilen Sie die Daten wie in Projekt 8.2 auf, mit 20 % Testdaten und
`random_state=0`. Nur dann ist der Vergleich fair. Verwenden Sie die sieben
Bestandteile und das Alter als Merkmale.

Für Regressionsaufgaben gibt es den `RandomForestRegressor`. Er wird ebenfalls
aus `sklearn.ensemble` importiert und genauso verwendet wie der
`RandomForestClassifier`. Bei XGBoost heißt das Gegenstück `XGBRegressor`.

Trainieren Sie einen Random Forest und ein XGBoost-Modell, beide mit
`random_state=0` und sonst mit den voreingestellten Werten. Vergleichen Sie die
R²-Scores auf den Trainings- und Testdaten mit den Modellen aus Projekt 8.2.

Zur Kontrolle: Der Random Forest erreicht auf den Trainingsdaten einen
R²-Score von 0.98.

```{code-cell} python
# Code-Zelle
```

### Teil 2: Was zählt für die Druckfestigkeit?

Stellen Sie die Feature Importance des Random Forests als Balkendiagramm dar.

Bei den standardisierten Koeffizienten der linearen Regression lag der Zement
vorn, gefolgt von Hüttensand und Alter. Welche Rangfolge ergibt die Feature
Importance? Haben Sie eine Erklärung für den Unterschied? Denken Sie daran, wie
die Druckfestigkeit mit dem Alter ansteigt.

Zur Kontrolle: Der Zement hat eine Feature Importance von 0.280.

```{code-cell} python
# Code-Zelle
```

### Teil 3: Prognose für eine Rezeptur

Wir betrachten die Rezeptur mit 540 kg Zement, 173 kg Wasser, 1125 kg
Grobzuschlag und 613 kg Feinzuschlag pro Kubikmeter, ohne Hüttensand,
Flugasche und Fließmittel. Für ein Alter von zwei Jahren lieferten die
linearen Modelle aus Projekt 7.2 dafür 131.5 MPa und -133.1 MPa.

Prognostizieren Sie die Druckfestigkeit dieser Rezeptur jetzt mit dem Random
Forest und dem XGBoost-Modell aus Teil 1, und zwar nur für ein Alter von 28,
365 und 730 Tagen.

1. Nach 28 Tagen wurden 67.3 MPa gemessen. Wie gut treffen die beiden Modelle
   diesen Wert?
2. Vergleichen Sie die Prognosen nach einem Jahr und nach zwei Jahren. Was fällt
   Ihnen auf? Woran liegt das?

Zur Kontrolle: Für ein Alter von 28 Tagen prognostiziert der Random Forest
66.9 MPa.

```{code-cell} python
# Code-Zelle
```

### Abschlussfrage

Stellen Sie die R²-Scores auf den Testdaten aller Betonmodelle aus den
Projekten 8.2 und 9.2 in einer Tabelle zusammen. Welches Modell würden Sie
dem Betonwerk jetzt empfehlen?

Probekörper derselben Rezeptur landen teils in den Trainings- und teils in den
Testdaten. Für ganz neue Rezepturen ist der Testscore deshalb zu optimistisch.
Was bedeutet das für Ihre Empfehlung?
