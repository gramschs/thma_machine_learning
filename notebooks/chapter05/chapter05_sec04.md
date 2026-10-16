---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 5.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 5.1 bis 5.3. Rechnen Sie mit gut eineinhalb Stunden
Bearbeitungszeit.

Der Schwierigkeitsgrad steht im Titel jeder Aufgabe:

* ✩ Verständnis: Code und Ausgaben vorhersagen und erklären (ca. 5 min)
* ✩✩ Anwendung: eigenen Code schreiben und Ergebnisse interpretieren (ca. 10 min)
* ✩✩✩ Mini-Projekt: mehrere Konzepte des Kapitels kombinieren (ca. 30 min)

Alle Datensätze stehen über das Download-Symbol rechts oben zur Verfügung.
Speichern Sie sie in denselben Ordner wie dieses Jupyter Notebook. Drei der
vier Datensätze kennen Sie bereits aus Kapitel 4.4.

* `pokemon_DE.csv`: Werte von 800 Pokémon aus den Videospielen der
  Generationen 1 bis 6, Spaltennamen und Typen ins Deutsche übersetzt (Quelle:
  [Kaggle, Pokemon with stats](https://www.kaggle.com/datasets/abcsds/pokemon),
  Lizenz CC0)
* `wetter_mannheim_2025.csv`: Tageswerte der Wetterstation Mannheim im Jahr
  2025 (Quelle: [Deutscher Wetterdienst, Climate Data
  Center](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/),
  Lizenz CC BY 4.0)
* `olympia_rio2016.csv`: Athletinnen und Athleten der Olympischen
  Sommerspiele 2016 in acht Sportarten, ohne Namen, Spaltennamen und Einträge
  ins Deutsche übersetzt (Quelle: [R. H. Griffin, 120 years of Olympic
  history: athletes and results,
  Kaggle](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results),
  Lizenz CC0)
* `ai4i2020_DE.csv`: synthetische Prozessdaten einer Werkzeugmaschine,
  Spaltennamen ins Deutsche übersetzt (Quelle: [S. Matzka, AI4I 2020
  Predictive Maintenance Dataset, UCI Machine Learning
  Repository](https://doi.org/10.24432/C5HS5C), Lizenz CC BY 4.0)

## Aufgabe 5.1 (✩)

Gegeben ist folgender Code:

```python
import pandas as pd

pokemon = pd.read_csv('pokemon_DE.csv', index_col=1)

print(pokemon['Legendaer'].unique())
print(len(pokemon['Typ 1'].unique()))
print(len(pokemon['Typ 2'].unique()))
print(pokemon['Typ 2'].mode())
print(pokemon['Generation'].value_counts())
```

Notieren Sie Ihre Vermutung in einer Markdown-Zelle, bevor Sie den Code
ausführen.

1. Was gibt die erste `print()`-Anweisung aus? Welche Kardinalität hat das
   Merkmal `Legendaer`?
2. Es gibt 18 Pokémon-Typen, und jeder davon kommt sowohl als erster als auch
   als zweiter Typ vor. Welche Zahlen geben die zweite und die dritte
   `print()`-Anweisung aus? Denken Sie an Charmander aus Aufgabe 4.1.
3. Der Modus von `Typ 2` ist Flug. Gibt `.mode()` nur das Wort Flug aus oder
   noch mehr? Warum ist das so?
4. Die Spalte `Generation` enthält die ganzen Zahlen 1 bis 6 und gibt an, in
   welcher Spielegeneration ein Pokémon erschienen ist. Ist `Generation` ein
   numerisches oder ein kategoriales Merkmal? Falls kategorial: nominal oder
   ordinal?
5. In welcher Reihenfolge stehen die Generationen in der letzten Ausgabe?
6. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 5.2 (✩)

Gegeben ist folgender Code:

```python
import pandas as pd

pokemon = pd.read_csv('pokemon_DE.csv', index_col=1)

bedingung = pokemon['Legendaer'] == 'ja'
legendaer = pokemon[bedingung]
feuer_wasser = pokemon[pokemon['Typ 1'].isin(['Feuer', 'Wasser'])]
feuer = pokemon[pokemon['Typ 1'] == 'feuer']
stark = pokemon[(pokemon['Gesamt'] > 600) & (pokemon['Legendaer'] == 'nein')]
```

Notieren Sie Ihre Vermutung in einer Markdown-Zelle, bevor Sie den Code
ausführen.

1. Welchen Datentyp hat `bedingung`? Wie viele Einträge enthält es und welche
   Werte kommen darin vor?
2. 65 der 800 Pokémon sind legendär. Was gibt `legendaer.shape` zurück?
3. 52 Pokémon haben den ersten Typ Feuer und 112 den ersten Typ Wasser. Wie
   viele Zeilen haben `feuer_wasser` und `feuer`? Erwarten Sie eine
   Fehlermeldung?
4. Beschreiben Sie in Worten, welche Pokémon in `stark` landen.
5. Was passiert, wenn Sie in der letzten Zeile die runden Klammern um die
   beiden Bedingungen weglassen? Und was passiert bei
   `pokemon[pokemon['Typ 1'] = 'Feuer']`?
6. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 5.3 (✩)

Gegeben ist folgender Code:

```python
import pandas as pd
import plotly.express as px

pokemon = pd.read_csv('pokemon_DE.csv', index_col=1)

anzahl_pro_generation = pokemon['Generation'].value_counts().sort_index()
fig = px.bar(anzahl_pro_generation, title='Anzahl Pokémon pro Generation')
fig.show()

fig = px.histogram(pokemon['Gesamt'], nbins=30, title='Verteilung der Gesamtwerte')
fig.show()

gesamt_pro_typ = pokemon.groupby('Typ 1')['Gesamt'].mean()
fig = px.bar(gesamt_pro_typ.sort_values(), orientation='h',
             title='Durchschnittlicher Gesamtwert pro Typ')
fig.show()
```

Notieren Sie Ihre Vermutung in einer Markdown-Zelle, bevor Sie den Code
ausführen.

1. Wie viele Säulen zeigt das erste Diagramm? Warum passt für `Generation` ein
   Barplot, für `Gesamt` dagegen ein Histogramm?
2. Was gibt im Histogramm die Höhe einer Säule an?
3. Viele Pokémon entwickeln sich weiter, zum Beispiel Bulbasaur über Ivysaur
   zu Venusaur mit den Gesamtwerten 318, 405 und 525. Dazu kommen die
   besonders starken legendären Pokémon und Mega-Entwicklungen. Erwarten Sie
   im Histogramm einen einzigen Gipfel oder mehrere?
4. Wie viele Balken zeigt das dritte Diagramm? Drachen-Pokémon gelten als
   besonders stark. Steht der Balken für Drache oben oder unten?
5. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 5.4 (✩✩)

Der Deutsche Wetterdienst beschreibt das Klima eines Ortes unter anderem mit
Kenntagen:

* Sommertag: Die Höchsttemperatur beträgt mindestens 25 °C.
* heißer Tag: Die Höchsttemperatur beträgt mindestens 30 °C.
* Frosttag: Die Tiefsttemperatur liegt unter 0 °C.
* Eistag: Die Höchsttemperatur liegt unter 0 °C.

Wir verwenden wieder die Datei `wetter_mannheim_2025.csv` aus Kapitel 4.4.

1. Lesen Sie die Datei mit dem Datum als Zeilenindex ein. Wie viele
   Sommertage, heiße Tage, Frosttage und Eistage gab es 2025 in Mannheim?
2. In welche Jahreszeiten fallen die Sommertage, in welche die Frosttage? Was
   überrascht Sie?
3. Berechnen Sie für jede Jahreszeit den durchschnittlichen Niederschlag pro
   Tag. Stellen Sie das Ergebnis als Säulendiagramm in der Reihenfolge Winter,
   Frühling, Sommer, Herbst dar und vergeben Sie einen Titel sowie sinnvolle
   Achsenbeschriftungen. Welche Jahreszeit war am trockensten? Hinweis: Die
   gewünschte Reihenfolge erhalten Sie, indem Sie die Einträge mit einer Liste
   von Zeilennamen auswählen, wie bei den Start-Pokémon in Aufgabe 4.4.
4. Erstellen Sie ein Histogramm des täglichen Niederschlags und beschreiben
   Sie die Form der Verteilung. An wie vielen Tagen hat es gar nicht geregnet?
   Beschreibt der Mittelwert des Niederschlags einen typischen Tag?

```{code-cell} python
# Code-Zelle
```

## Aufgabe 5.5 (✩✩)

Die Datei `olympia_rio2016.csv` enthält alle 2520 Athletinnen und Athleten,
die 2016 bei den Olympischen Sommerspielen in Rio de Janeiro in einer von acht
Sportarten angetreten sind: Basketball, Fußball, Gewichtheben, Handball,
Hockey, Judo, Rhythmische Sportgymnastik und Volleyball. Jede Zeile beschreibt
eine Person mit Geschlecht (w oder m), Alter, Körpergröße, Gewicht, Land,
Sportart und gewonnener Medaille. Das Land ist als Länderkürzel des
Internationalen Olympischen Komitees angegeben, zum Beispiel GER für
Deutschland.

1. Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein. Welche
   Spalten sind numerisch, welche kategorial? Welches kategoriale Merkmal ist
   ordinal? Bei wie vielen Personen fehlt die Körpergröße? Aus wie vielen
   Ländern kommen die Personen?
2. Berechnen Sie die durchschnittliche Körpergröße pro Sportart. Stellen Sie
   das Ergebnis als Balkendiagramm dar, sortiert nach der durchschnittlichen
   Körpergröße. Vergeben Sie einen Titel und sinnvolle Achsenbeschriftungen.
3. Erstellen Sie ein Histogramm der Körpergröße aller Personen mit 10
   Intervallen und ein zweites mit 80 Intervallen. Was fällt Ihnen bei 80
   Intervallen auf? Woran könnte das liegen?
4. Rhythmische Sportgymnastik ist bei Olympia eine reine Frauensportart.
   Wiederholen Sie Teil 2 nur für die Frauen. Werten Sie den Vergleich der
   beiden Balkendiagramme nach Beobachtung, Deutung und Einschränkung aus.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 5.6 (✩✩)

Wir bleiben bei der Datei `olympia_rio2016.csv` und werten die Medaillen aus.

1. Wie viele Personen haben jeweils Gold, Silber und Bronze gewonnen? Warum
   taucht in der Ausgabe keine Zeile für die Personen ohne Medaille auf?
   Stellen Sie die Anzahl als Säulendiagramm in der Reihenfolge Gold, Silber,
   Bronze dar.
2. Es gibt mehr Bronze- als Goldmedaillen. Vergleichen Sie für jede Sportart,
   wie viele Personen Gold und wie viele Bronze gewonnen haben. In welcher
   Sportart liegt die Ursache? Haben Sie eine Erklärung?
3. Filtern Sie alle Personen, die eine Medaille gewonnen haben. Aus welchen
   fünf Ländern kommen die meisten Medaillengewinnerinnen und
   Medaillengewinner? Stellen Sie das Ergebnis als Säulendiagramm dar.
4. Im offiziellen Medaillenspiegel haben die USA in diesen acht Sportarten 7
   Medaillen gewonnen, darunter 3 Goldmedaillen. Deutschland kommt auf 6
   Medaillen, darunter 1 Goldmedaille. Warum liegt Deutschland in Ihrem
   Diagramm trotzdem deutlich vor den USA? Vergleichen Sie dazu, in welchen
   Sportarten die deutschen und die US-amerikanischen Medaillen gewonnen
   wurden.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 5.7 (✩✩✩) Mini-Projekt: Ausfallarten und Qualität

Im Mini-Projekt von Kapitel 4.4 haben wir mit der Datei `ai4i2020_DE.csv`
10000 Bearbeitungsprozesse einer Werkzeugmaschine untersucht. Bei 339
Prozessen (3.39 %) ist die Maschine ausgefallen. Jetzt nutzen wir die
kategorialen Merkmale des Datensatzes. Die Spalte `Qualitaet` gibt an, in
welcher Qualitätsvariante das Produkt gefertigt wird: L (niedrig), M (mittel)
oder H (hoch). Die fünf Spalten nach `Ausfall` geben die Art des Ausfalls an
(1 für ja, 0 für nein):

* `Ausfall Werkzeug`: Das Werkzeug ist verschlissen und versagt.
* `Ausfall Waermeabfuhr`: Die Wärme wird nicht ausreichend abgeführt.
* `Ausfall Leistung`: Die Leistung ist zu klein oder zu groß (siehe Kapitel
  4.4).
* `Ausfall Ueberlast`: Das Werkzeug wird überlastet.
* `Ausfall zufaellig`: Die Maschine fällt ohne erkennbaren Grund aus.

**Teil 1:** Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein. Ist
`Qualitaet` ein nominales oder ein ordinales Merkmal? Wie viele Prozesse gibt
es pro Qualitätsvariante? Berechnen Sie außerdem für jede Qualitätsvariante
die Ausfallquote in Prozent. Stellen Sie beide Ergebnisse als Säulendiagramm
in der fachlich sinnvollen Reihenfolge dar.

**Teil 2:** Ermitteln Sie, wie viele Prozesse von jeder Ausfallart betroffen
sind. Eine for-Schleife über die fünf Spaltennamen spart Tipparbeit. Ist die
Summe gleich der Anzahl aller Ausfälle? Prüfen Sie, bei wie vielen zufälligen
Ausfällen auch in der Spalte `Ausfall` eine 1 steht. Erstellen Sie dann je ein
Histogramm des Werkzeugverschleißes für alle Prozesse und für die Prozesse mit
Werkzeugausfall. Ab welcher Einsatzzeit fällt das Werkzeug aus?

**Teil 3:** Laut Dokumentation des Datensatzes hängt ein Überlastausfall vom
Produkt aus Werkzeugverschleiß und Drehmoment ab. Erweitern Sie die Tabelle um
eine Spalte `Belastung (min Nm)` mit diesem Produkt. Bestimmen Sie für jede
Qualitätsvariante die kleinste Belastung, bei der ein Überlastausfall
auftrat, und die größte Belastung, bei der kein Überlastausfall auftrat.
Welche Grenze vermuten Sie für jede Qualitätsvariante? Wie viele
Überlastausfälle stützen Ihre Vermutung jeweils?

**Abschlussfrage:** Fallen Prozesse der Variante L häufiger aus, weil die
Maschine dabei mit ungünstigeren Prozessgrößen arbeitet? Vergleichen Sie dazu
die durchschnittliche Drehzahl, das durchschnittliche Drehmoment und den
durchschnittlichen Werkzeugverschleiß der drei Varianten. Was bedeutet Ihr
Ergebnis für ein Modell, das Überlastausfälle aus den Daten lernen soll?

```{code-cell} python
# Code-Zelle
```
