---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 4.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 4.1 bis 4.3. Rechnen Sie mit gut eineinhalb Stunden
Bearbeitungszeit.

Der Schwierigkeitsgrad steht im Titel jeder Aufgabe:

* ✩ Verständnis: Code und Ausgaben vorhersagen und erklären (ca. 5 min)
* ✩✩ Anwendung: eigenen Code schreiben und Ergebnisse interpretieren (ca. 10 min)
* ✩✩✩ Mini-Projekt: mehrere Konzepte des Kapitels kombinieren (ca. 30 min)

Alle Datensätze stehen über das Download-Symbol rechts oben zur Verfügung.
Speichern Sie sie in denselben Ordner wie dieses Jupyter Notebook.

* `pokemon_DE.csv`: Werte von 800 Pokémon aus den Videospielen der
  Generationen 1 bis 6, Spaltennamen und Typen ins Deutsche übersetzt (Quelle:
  [Kaggle, Pokemon with stats](https://www.kaggle.com/datasets/abcsds/pokemon),
  Lizenz CC0)
* `wetter_mannheim_2025.csv`: Tageswerte der Wetterstation Mannheim im Jahr
  2025 (Quelle: [Deutscher Wetterdienst, Climate Data
  Center](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/),
  Lizenz CC BY 4.0)
* `stromverbrauch_hessen.csv`: Stromverbrauch in Hessen 2000 bis 2021 nach
  Verbrauchergruppen
* `ai4i2020_DE.csv`: synthetische Prozessdaten einer Werkzeugmaschine,
  Spaltennamen ins Deutsche übersetzt (Quelle: [S. Matzka, AI4I 2020
  Predictive Maintenance Dataset, UCI Machine Learning
  Repository](https://doi.org/10.24432/C5HS5C), Lizenz CC BY 4.0)

## Aufgabe 4.1 (✩)

Die Datei `pokemon_DE.csv` enthält 800 Pokémon und beginnt mit folgenden
Zeilen:

```none
Nr.,Name,Typ 1,Typ 2,Gesamt,KP,Angriff,Verteidigung,Spezial-Angriff,Spezial-Verteidigung,Initiative,Generation,Legendaer
1,Bulbasaur,Pflanze,Gift,318,45,49,49,65,65,45,1,nein
2,Ivysaur,Pflanze,Gift,405,60,62,63,80,80,60,1,nein
3,Venusaur,Pflanze,Gift,525,80,82,83,100,100,80,1,nein
3,VenusaurMega Venusaur,Pflanze,Gift,625,80,100,123,122,120,80,1,nein
4,Charmander,Feuer,,309,39,52,43,60,50,65,1,nein
```

Gegeben ist folgender Code:

```python
import pandas as pd

pokemon = pd.read_csv('pokemon_DE.csv', index_col=1)
```

Notieren Sie Ihre Vermutung in einer Markdown-Zelle, bevor Sie den Code
ausführen.

1. Welche Spalte wird zum Zeilenindex? Was gibt `pokemon.shape` zurück?
2. Warum wäre die Spalte `Nr.` als Zeilenindex ungeeignet?
3. Bei Charmander fehlt der zweite Typ. Insgesamt haben 386 Pokémon nur einen
   Typ. Wie viele non-null-Einträge zeigt `pokemon.info()` für die Spalte
   `Typ 2` an?
4. Für wie viele Spalten berechnet `pokemon.describe()` statistische
   Kennzahlen? Sind alle diese Kennzahlen sinnvoll?
5. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 4.2 (✩)

Gegeben ist folgender Code:

```python
import pandas as pd

pokemon = pd.read_csv('pokemon_DE.csv', index_col=1)

a = pokemon['Angriff']
b = pokemon.loc['Pikachu']
c = pokemon.loc['Pikachu', 'Initiative']
d = pokemon[['Angriff', 'Verteidigung']]
e = pokemon.loc['Bulbasaur':'Charmander']
```

Notieren Sie Ihre Vermutung in einer Markdown-Zelle, bevor Sie den Code
ausführen.

1. Welchen Datentyp haben `a`, `b`, `c` und `d`: Series, DataFrame oder ein
   einzelner Wert?
2. Wie viele Einträge hat `b`?
3. Wie viele Zeilen hat `e`? Schauen Sie dazu noch einmal auf den Dateianfang
   in Aufgabe 4.1.
4. Was passiert bei `pokemon['Pikachu']`?
5. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 4.3 (✩)

Gegeben ist folgender Code:

```python
import pandas as pd
import plotly.express as px

pokemon = pd.read_csv('pokemon_DE.csv', index_col=1)

auswahl = ['KP', 'Angriff', 'Verteidigung', 'Spezial-Angriff',
           'Spezial-Verteidigung', 'Initiative']
diagramm = px.scatter_matrix(pokemon, dimensions=auswahl, color='Legendaer')
diagramm.show()

diagramm = px.scatter(pokemon, x='Angriff', y='Verteidigung',
                      color='Gesamt', size='KP')
diagramm.show()
```

Notieren Sie Ihre Vermutung in einer Markdown-Zelle, bevor Sie den Code
ausführen.

1. Aus wie vielen Einzeldiagrammen besteht die Scattermatrix? Wie viele
   verschiedene Paare aus zwei unterschiedlichen Merkmalen zeigt sie?
2. Die Scattermatrix ist nach `Legendaer` eingefärbt, der Scatterplot nach
   `Gesamt`. Wie unterscheiden sich die beiden Farbdarstellungen und warum?
3. Was bedeutet im Scatterplot ein besonders großer Kreis?
4. Legendaere Pokémon gelten als besonders stark. In welchem Bereich der
   Einzeldiagramme erwarten Sie die legendären Pokémon?
5. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 4.4 (✩✩)

Wir bleiben bei den Pokémon. Lesen Sie die Datei `pokemon_DE.csv` mit dem
Namen als Zeilenindex ein.

1. Die Spalte `Gesamt` soll die Summe der sechs Werte KP, Angriff,
   Verteidigung, Spezial-Angriff, Spezial-Verteidigung und Initiative sein.
   Prüfen Sie das: Erweitern Sie die Tabelle um eine Spalte `Kontrolle` mit
   der Differenz und lassen Sie sich die statistischen Kennzahlen dieser
   Spalte ausgeben.
2. Vergleichen Sie die drei Start-Pokémon Bulbasaur, Charmander und Squirtle.
   Wählen Sie dazu gleichzeitig diese drei Zeilen und die Spalten `Typ 1`,
   `Gesamt`, `Angriff`, `Verteidigung` und `Initiative` aus. Welches der drei
   Pokémon ist am schnellsten, hat also die höchste Initiative?
3. Erstellen Sie einen Scatterplot mit dem Angriff auf der x-Achse und der
   Verteidigung auf der y-Achse. Färben Sie die Punkte danach ein, ob ein
   Pokémon legendär ist, und setzen Sie einen Titel.
4. Werten Sie den Scatterplot nach Beobachtung, Deutung und Einschränkung aus.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 4.5 (✩✩)

Die Datenreihe der Wetterstation Mannheim beginnt im Jahr 1781 und gehört
damit zu den ältesten der Welt. Die Datei `wetter_mannheim_2025.csv` enthält
die Tageswerte des Jahres 2025. Die Spalte `Jahreszeit` haben wir ergänzt
(meteorologische Jahreszeiten, z. B. Winter = Dezember bis Februar).

1. Lesen Sie die Datei mit dem Datum als Zeilenindex ein. Wie viele Tage
   enthält der Datensatz? In welchen Spalten fehlen Werte und wie viele?
2. Berechnen Sie die durchschnittliche Mitteltemperatur im Januar und im Juli.
   Wählen Sie dazu jeden Monat als zusammenhängenden Bereich aus.
3. Erweitern Sie die Tabelle um eine Spalte `Tagesspanne (C)`, die Differenz
   aus Höchst- und Tiefsttemperatur.
4. Erstellen Sie einen Scatterplot mit der Sonnenscheindauer auf der x-Achse
   und der Tagesspanne auf der y-Achse. Färben Sie die Punkte nach der
   Jahreszeit ein und setzen Sie einen Titel.
5. Werten Sie den Scatterplot nach Beobachtung, Deutung und Einschränkung aus.
   Gibt es ein Merkmal im Datensatz, das beide Größen gleichzeitig
   beeinflussen könnte?

```{code-cell} python
# Code-Zelle
```

## Aufgabe 4.6 (✩✩)

Die Datei `stromverbrauch_hessen.csv` enthält den Stromverbrauch in Hessen
von 2000 bis 2021 nach Verbrauchergruppen in Gigawattstunden (GWh).

1. Schauen Sie sich die Datei zunächst im Texteditor an. In welcher Zeile
   beginnen die Daten? Lesen Sie die Datei mit dem Jahr als Zeilenindex ein
   und überspringen Sie dabei die Beschreibungszeilen am Dateianfang. Schlagen
   Sie dazu in der Dokumentation von `read_csv()` nach, mit welchem Argument
   sich Zeilen überspringen lassen.
2. Prüfen Sie mit einer Kontrollspalte, ob die Spalte `insgesamt` die Summe
   der drei Verbrauchergruppen ist. Wie erklären Sie die Abweichungen?
3. Erweitern Sie die Tabelle um eine Spalte `Anteil Industrie (%)` und lassen
   Sie sich diese Spalte für die Jahre 2007 bis 2010 anzeigen.
4. Erstellen Sie einen Scatterplot mit dem Jahr auf der x-Achse und dem
   Stromverbrauch der Industrie auf der y-Achse. Hinweis: Das Jahr ist der
   Zeilenindex und keine Spalte. Übergeben Sie für die x-Achse deshalb wie bei
   `text=` in Kapitel 4.3 den Zeilenindex selbst. Werten Sie den Scatterplot
   nach Beobachtung, Deutung und Einschränkung aus.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 4.7 (✩✩✩) Mini-Projekt: Predictive Maintenance

Bei der vorausschauenden Wartung (Predictive Maintenance) werten wir
Maschinendaten aus, um Ausfälle zu erkennen, bevor sie passieren. Die Datei
`ai4i2020_DE.csv` enthält 10000 Bearbeitungsprozesse einer Werkzeugmaschine.
Die Daten sind synthetisch, also von einem Programm erzeugt, das realen
Industriedaten nachempfunden ist. Jede Zeile beschreibt einen Prozess mit
folgenden Merkmalen:

* `Qualitaet`: Qualitätsvariante des Produkts (L, M oder H für niedrig, mittel
  oder hoch)
* `Lufttemperatur (K)` und `Prozesstemperatur (K)` in Kelvin
* `Drehzahl (1/min)` und `Drehmoment (Nm)` des Antriebs
* `Werkzeugverschleiss (min)`: bisherige Einsatzzeit des Werkzeugs in Minuten
* `Ausfall`: 1, wenn die Maschine ausgefallen ist, sonst 0. Die fünf Spalten
  danach geben an, welche Art von Ausfall vorlag.

**Teil 1:** Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein und
verschaffen Sie sich einen Überblick. Fehlen Werte? Wie viel Prozent der
Prozesse endeten mit einem Ausfall? Hinweis: Was bedeutet der Mittelwert einer
Spalte, die nur die Werte 0 und 1 enthält?

**Teil 2:** Erzeugen Sie eine Scattermatrix der fünf Prozessgrößen
Lufttemperatur, Prozesstemperatur, Drehzahl, Drehmoment und
Werkzeugverschleiß. Färben Sie die Punkte nach `Ausfall` ein. Welche zwei
Merkmalspaare zeigen einen deutlichen Zusammenhang? In welchen Bereichen
häufen sich die Ausfälle?

**Teil 3:** Die mechanische Leistung des Antriebs ist $P = M \cdot \omega$ mit
dem Drehmoment $M$ in Nm und der Winkelgeschwindigkeit
$\omega = 2 \pi \cdot n / 60$ in 1/s, wobei $n$ die Drehzahl in 1/min ist.
Erweitern Sie die Tabelle um eine Spalte `Leistung (W)` (verwenden Sie
$\pi \approx 3.1416$) und lassen Sie sich die statistischen Kennzahlen der
Leistung ausgeben. Erstellen Sie dann einen Scatterplot mit der Drehzahl auf
der x-Achse und der Leistung auf der y-Achse, eingefärbt nach `Ausfall`.
Unterhalb welcher und oberhalb welcher Leistung fällt die Maschine immer aus?
Schauen Sie sich zur Kontrolle die Prozesse Nr. 51 und Nr. 70 an.

**Abschlussfrage:** Die Daten sind synthetisch. Was bedeutet das für die
Erkenntnisse aus Teil 3? Was wäre bei echten Maschinendaten anders?

```{code-cell} python
# Code-Zelle
```

