---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 10.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 10.1 bis 10.3. Rechnen Sie mit gut einer Stunde
Bearbeitungszeit. Die Übung besteht aus zwei Projekten mit demselben Datensatz.
In Projekt 10.1 wählen Sie mit Kreuzvalidierung und Gittersuche ein Modell aus
und bewerten es am Ende ehrlich mit Testdaten. In Projekt 10.2 bewerten Sie
Modelle mit den Gütemaßen aus Kapitel 10.3.

Bei den meisten Teilen finden Sie einen Kontrollwert. Damit können Sie prüfen,
ob Ihr Zwischenergebnis stimmt, bevor Sie weiterarbeiten. Die Kontrollwerte
gelten nur für die angegebenen Werte von `random_state`.

Der Datensatz steht über das Download-Symbol rechts oben zur Verfügung.
Speichern Sie ihn in denselben Ordner wie dieses Jupyter Notebook.

* `pinguine.csv`: Messungen an 344 Pinguinen aus der Antarktis, Spaltennamen
  und Einträge ins Deutsche übersetzt (Quelle: [A. M. Horst, A. P. Hill, K. B.
  Gorman, palmerpenguins](https://doi.org/10.5281/zenodo.3960218), Lizenz CC0)

Die Daten stammen von der Forschungsstation Palmer in der Antarktis. Von 2007
bis 2009 haben Forschende dort Pinguine auf drei Inseln vermessen und gewogen.
Zu jedem Pinguin gibt es

* die Art (Adeliepinguin, Eselspinguin oder Zügelpinguin),
* die Insel, auf der er gefunden wurde (Biscoe, Dream oder Torgersen),
* die Länge und die Tiefe, also die Höhe, des Schnabels in mm,
* die Länge der Flosse in mm,
* das Körpergewicht in g,
* das Geschlecht und
* das Jahr der Messung.

## Projekt 10.1: Männchen oder Weibchen?

Bei Pinguinen sehen Männchen und Weibchen fast gleich aus. Die Forschenden auf
Palmer haben das Geschlecht deshalb mit einer Blutprobe bestimmt. Lässt es sich
auch aus den Körpermaßen und der Art vorhersagen? In diesem Projekt gehen Sie
so vor wie in Kapitel 10.2: Zuerst legen Sie Testdaten zur Seite, dann wählen
Sie mit den Validierungsscores ein Modell aus und bewerten nur dieses Modell
einmal mit den Testdaten. Rechnen Sie mit etwa 30 Minuten.

### Teil 1: Daten vorbereiten

Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein.

1. In welchen Spalten fehlen Werte, und wie viele? Löschen Sie alle Zeilen, in
   denen mindestens ein Wert fehlt. Das geht mit der Methode `dropna()`.
2. Kodieren Sie die Art mit der One-Hot-Kodierung. Verwenden Sie als
   Eingabedaten die vier Körpermaße und die kodierte Art, als Zielgröße das
   Geschlecht.
3. Legen Sie 20 % der Daten als Testdaten zur Seite, mit `random_state=0`.
   Sorgen Sie dafür, dass das Verhältnis von Männchen und Weibchen in beiden
   Teilen etwa gleich ist. Welche Accuracy erreicht auf den Testdaten ein
   Referenzmodell, das immer das häufigere Geschlecht vorhersagt?

Zur Kontrolle: Nach dem Löschen bleiben 333 Pinguine übrig.

```{code-cell} python
# Code-Zelle
```

### Teil 2: Baumtiefe mit Kreuzvalidierung wählen

Vergleichen Sie Entscheidungsbäume mit den Tiefen 1 bis 8 per
Kreuzvalidierung auf den Trainingsdaten. Verwenden Sie fünf Folds, mischen Sie
die Daten vorher und sorgen Sie dafür, dass das Verhältnis der Geschlechter in
jedem Fold erhalten bleibt. Setzen Sie bei der Aufteilung und beim
Entscheidungsbaum `random_state=0`. Geben Sie für jede Tiefe den Mittelwert und
die Standardabweichung der Validierungsscores sowie den Mittelwert der
Trainingsscores aus.

1. Welche Tiefe erreicht den besten mittleren Validierungsscore? Wie groß ist
   ihr Vorsprung vor der Tiefe 2, verglichen mit der Standardabweichung?
2. Bei welcher Tiefe sehen Sie Underfitting, bei welcher Overfitting? Begründen
   Sie mit den Trainings- und Validierungsscores.

Zur Kontrolle: Bei der Tiefe 1 beträgt der mittlere Validierungsscore 0.628.

```{code-cell} python
# Code-Zelle
```

### Teil 3: Random Forest mit Gittersuche

Stimmen Sie jetzt einen Random Forest mit einer Gittersuche ab. Verwenden Sie
dieselbe Fold-Aufteilung wie in Teil 2 und `random_state=0` für den Random
Forest. Durchsuchen Sie für die maximale Tiefe die Werte 2, 4, 6, 8 und `None`
und für die minimale Anzahl an Datenpunkten pro Blatt die Werte 1, 5 und 10.
`None` steht für eine unbegrenzte Tiefe.

1. Wie viele Kombinationen werden getestet, und wie viele Random Forests werden
   dabei trainiert?
2. Welche Kombination ist am besten? Entscheiden Sie anhand der
   Validierungsscores, ob Sie den besten Entscheidungsbaum aus Teil 2 oder den
   Random Forest einsetzen.
3. Bewerten Sie nur das gewählte Modell einmal mit den Testdaten. Warum
   bewerten Sie nicht beide Modelle mit den Testdaten und nehmen das bessere?

Zur Kontrolle: Der beste Validierungsscore des Random Forests beträgt 0.914.

```{code-cell} python
# Code-Zelle
```

## Projekt 10.2: Gütemaße für Pinguine

In diesem Projekt bewerten Sie Modelle mit den Gütemaßen aus Kapitel 10.3. Wie
im Fließtext dienen die Testdaten hier nur dazu, die Gütemaße zu
veranschaulichen. Für eine echte Modellauswahl würden Sie wie in Projekt 10.1
Validierungsdaten verwenden. Verwenden Sie die bereinigten Daten aus Projekt
10.1, Teil 1. Rechnen Sie mit etwa 30 Minuten.

### Teil 1: Zügelpinguine erkennen

Zügelpinguine sind im Datensatz die seltenste Art. Ein Modell soll allein aus
den vier Körpermaßen erkennen, ob ein Pinguin ein Zügelpinguin ist. Die Insel
lassen wir weg, denn Zügelpinguine wurden nur auf Dream gefunden.

Kodieren Sie die Zielgröße so, dass ein Zügelpinguin die 1 ist und jede andere
Art die 0. Legen Sie 20 % der Daten als Testdaten zur Seite, mit
`random_state=0` und gleichem Anteil an Zügelpinguinen in beiden Teilen.
Wählen Sie für Daten und Zielgröße andere Namen als in Projekt 10.1.

1. Welche Accuracy erreicht ein Referenzmodell, das nie "Zügelpinguin" sagt?
2. Trainieren Sie einen Entscheidungsbaum der Tiefe 1 mit `random_state=0`.
   Berechnen Sie die Accuracy und die Konfusionsmatrix auf den Testdaten. Wie
   viele Zügelpinguine erkennt der Baum?
3. Trainieren Sie denselben Baum noch einmal, aber so, dass die seltenere Klasse
   beim Training stärker zählt. Berechnen Sie Accuracy, Konfusionsmatrix,
   Precision und Recall. Was hat sich verändert?

Zur Kontrolle: In den Testdaten sind 14 Zügelpinguine.

```{code-cell} python
# Code-Zelle
```

### Teil 2: Eine zweite Frage

Erlauben Sie dem Baum jetzt eine zweite Frage. Trainieren Sie einen
Entscheidungsbaum der Tiefe 2 ohne Gewichtung, mit `random_state=0`.

1. Berechnen Sie Accuracy, Konfusionsmatrix, Precision, Recall und F1-Score auf
   den Testdaten. Stellen Sie die drei Bäume aus Teil 1 und Teil 2 in einer
   Tabelle gegenüber.
2. Eine Forscherin will Zügelpinguine mit einem Sender ausstatten. Jeder
   Pinguin, den das Modell meldet, wird dafür eingefangen. Welches Gütemaß ist
   für sie besonders wichtig?

Zur Kontrolle: Der Baum der Tiefe 2 erkennt 12 der 14 Zügelpinguine.

```{code-cell} python
# Code-Zelle
```

### Teil 3: Körpergewicht vorhersagen

Jetzt soll eine lineare Regression das Körpergewicht vorhersagen. Kodieren Sie
die Art und das Geschlecht mit der One-Hot-Kodierung. Legen Sie 20 % der Daten
als Testdaten zur Seite, mit `random_state=0`.

Trainieren Sie zwei Modelle: Modell A verwendet nur die Flossenlänge, Modell B
die drei Maße von Schnabel und Flosse sowie die kodierte Art und das kodierte
Geschlecht.

1. Berechnen Sie für beide Modelle R², MAE und RMSE auf den Testdaten.
   Vergleichen Sie den MAE mit dem mittleren Körpergewicht der Testdaten.
2. Um wie viele Gramm liegt Modell B im Mittel weniger daneben als Modell A?

Zur Kontrolle: Modell A erreicht auf den Testdaten einen R²-Score von 0.79.

```{code-cell} python
# Code-Zelle
```
