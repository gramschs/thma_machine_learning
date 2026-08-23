---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: autoscout24_xxs.csv
    title: autoscout24_xxs.csv
  - file: 3ddruck_xxs.csv
    title: 3ddruck_xxs.csv
  - file: chapter04_sec02.md
    title: chapter04_sec02.md
---

# 4.2 Arbeiten mit Tabellendaten

In Tabellenkalkulationssoftware ist es möglich, einzelne Zeilen oder Spalten zu
bearbeiten. Pandas bietet mit der Datenstruktur DataFrame dieselbe Möglichkeit.
Wie auf einzelne Spalten und Zeilen zugegriffen wird und wie die Daten
bearbeitet werden können, zeigt dieses Kapitel.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können mit eckigen Klammern **[]** und dem Spaltenindex auf eine ganze
  Spalte zugreifen.
* [ ] Sie können mit **.loc[]** und dem Zeilenindex auf eine ganze Zeile
  zugreifen.
* [ ] Sie können mit **.loc[zeilenindex, spaltenindex]** auf eine einzelne Zelle
  der Tabelle zugreifen.
* [ ] Sie können mehrere unzusammenhängende Zeilen/Spalten mittels Liste
  auswählen.
* [ ] Sie können zusammenhängende Bereiche mittels **Slicing** auswählen.
* [ ] Sie können eine Tabelle um eine Spalte erweitern.
```

## Zugriff auf Spalten

Bei einer Liste oder der Pandas-Datenstruktur Series haben wir auf ein einzelnes
Element zugegriffen, indem wir eckige Klammern benutzt haben. Bei Tabellen und
damit auch DataFrames ist es üblich, dass die Eigenschaften bzw. Merkmale in den
Spalten stehen und in den Zeilen die einzelnen Datenpunkte. Mit den eckigen
Klammern und dem Spaltennamen greifen wir diesmal also nicht nur ein Element
heraus, sondern gleich eine ganze Spalte.

Um den Zugriff auf eine Spalte eines DataFrames auszuprobieren, brauchen wir
einen DataFrame. Wir verwenden erneut den Datensatz `autoscout24_xxs.csv` und
lesen ihn mit der ersten Spalte ID als Zeilenindex ein. Dann verschaffen wir uns
einen ersten Überblick.

```{code-cell} python
import pandas as pd
tabelle = pd.read_csv('autoscout24_xxs.csv', index_col=0)

print(f'Anzahl Autos: {tabelle.shape[0]}')
print(f'Anzahl Merkmale: {tabelle.shape[1]}')

print('\nAnzeige der Merkmale der ersten fünf Autos:')
tabelle.head()
```

Die Farben der 10 Autos können wir folgendermaßen aus der Tabelle auswählen:

```{code-cell} python
farbe = tabelle['Farbe']
```

Was steckt jetzt in der Variable `farbe`? Ermitteln wir zunächst, welchen
Datentyp das Objekt hat, das in `farbe` gespeichert ist.

```{code-cell} python
type(farbe)
```

Es handelt sich um ein Series-Objekt mit dem Namen Farbe, also dem
ursprünglichen Spaltenlabel. Da wir bereits mit `.shape`, das 10 Autos im
Datensatz sind, können wir das neu erzeugte Series-Objekt mit `.head(10)`
anzeigen lassen:

```{code-cell} python
farbe.head(10)
```

Bei der Auswahl mehrerer Spalten via Liste entsteht wieder ein DataFrame, aber
dazu kommen wir gleich. Zunächst widmen wir uns dem Zugriff auf Zeilen und
Zellen.

```{admonition} Mini-Übung
:class: tip
Verwenden Sie den Datensatz `3ddruck_xxs.csv`, der Angaben zu 18
3D-Druckversuchen enthält.

1. Lesen Sie die Datei ein und verwenden Sie dabei die Nummer als Zeilenindex.
2. Wählen Sie die Spalte `Bauteilvolumen (cm3)` aus und speichern Sie sie in
   einer Variablen `volumen`.
3. Welchen Datentyp hat `volumen`? Stellen Sie zunächst eine Vermutung auf und
   überprüfen Sie diese anschließend.
4. Zeigen Sie sich die ersten fünf Werte der Spalte an.
5. Wie groß ist das durchschnittliche Bauteilvolumen über alle Druckversuche?
```

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

# Einlesen der csv-Datei mit der Spalte Nummer als Zeilenindex
druckversuche = pd.read_csv('3ddruck_xxs.csv', index_col=0)

# Spalte auswählen
volumen = druckversuche['Bauteilvolumen (cm3)']

# Datentyp prüfen
print(type(volumen))

# erste fünf Werte anzeigen
volumen.head()

# Durchschnitt berechnen
durchschnitt = volumen.mean()
print(f'Durchschnittliches Bauteilvolumen: {durchschnitt:.2f} cm3')
```

1. Auch hier muss `index_col=0` gesetzt werden, da die Spalte "Nummer" die
   erste Spalte in der csv-Datei ist.
2. Die Spalte wird mit eckigen Klammern und dem Spaltennamen
   `'Bauteilvolumen (cm3)'` ausgewählt.
3. `volumen` ist ein `pandas.Series`-Objekt.
4. `.head()` zeigt die Werte der ersten fünf Druckversuche an: 121.7, 44.2,
   22.3, 50.2 und 51.7 cm3.
5. Das durchschnittliche Bauteilvolumen über alle 18 Druckversuche liegt bei
   rund 68.71 cm3.
````

## Zugriff auf Zeilen und Zellen mit .loc[]

Natürlich kann es auch Gründe geben, sich einen einzelnen Datenpunkt mit allen
Merkmalen herauszugreifen. Oder anders ausgedrückt, vielleicht möchte man in der
Tabelle eine einzelne **Zeile** auswählen. Dazu gibt es den Indexer `.loc`.
Dabei steht "loc" für "location". Danach werden wieder eckige Klammern benutzt,
wobei diesmal der Zeilenindex und nicht der Spaltenname verwendet wird.

Der folgende Code-Schnipsel speichert die Zeile des 4. Autos (= BMW Nr. 1) in
der Variable `viertes_auto` ab. Wir ermitteln gleich den Datentyp dazu.

```{code-cell} python
viertes_auto = tabelle.loc['BMW Nr. 1']
type(viertes_auto)
```

Auch eine einzelne Zeile ist eine Series-Datenstruktur, die wir mit den
Series-Methoden weiter bearbeiten können. Der Name des Series-Objektes ist
diesmal der ursprüngliche Zeilenindex. Wir lassen den Datensatz mit `print()`
anzeigen.

```{code-cell} python
print(viertes_auto)
```

Es kann auch vorkommen, dass man gezielt auf eine einzelne **Zelle** zugreifen
möchte. Auch dazu benutzen wir den Indexer `.loc[]`. Für eine einzelne Zelle
müssen wir angeben, in welcher Zeile und in welcher Spalte sich diese Zelle
befindet. Der Indexer `.loc[]` ermöglicht auch zwei Angaben, also Zeile und
Spalte, indem beide Werte durch ein Komma getrennt werden.

Wollen wir beispielsweise wissen, wann der Audi Nr. 3 zum ersten Mal zugelassen
wurde, so gehen wir folgendermaßen vor:

```{code-cell} python
erstzulassung_audi3 = tabelle.loc['Audi Nr. 3', 'Erstzulassung']
print(erstzulassung_audi3)
```

Jetzt erhalten wir keine Series-Datenstruktur zurück, sondern direkt den Inhalt
dieser Zelle. In unserem Beispiel ist die Erstzulassung als String gespeichert.
Wir Menschen können diesen String natürlich interpretieren und sehen, dass der
Audi Nr. 3 im November 2018 zum ersten Mal zugelassen wurde.

```{admonition} Mini-Übung
:class: tip
Verwenden Sie erneut den Datensatz `3ddruck_xxs.csv`.

1. Lesen Sie die Datei ein und verwenden Sie dabei die Nummer als Zeilenindex.
2. Wählen Sie die Zeile `Druck Nr. 6` aus und speichern Sie sie in einer
   Variablen `druck6`. Welchen Datentyp hat `druck6`? Stellen Sie zunächst
   eine Vermutung auf und überprüfen Sie diese anschließend.
3. Lassen Sie sich die Zeile vollständig anzeigen.
4. Wie hoch war die Zugfestigkeit von `Druck Nr. 11`? Greifen Sie dazu gezielt
   auf die entsprechende Zelle zu.
5. War `Druck Nr. 7` erfolgreich? Greifen Sie dazu gezielt auf die Zelle in der
   Spalte `Erfolgreich` zu.
```

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

# Einlesen der csv-Datei mit der Spalte Nummer als Zeilenindex
druckversuche = pd.read_csv('3ddruck_xxs.csv', index_col=0)

# Zeile auswählen
druck6 = druckversuche.loc['Druck Nr. 6']
print(type(druck6))
print(druck6)

# Einzelne Zelle: Zugfestigkeit von Druck Nr. 11
zugfestigkeit_11 = druckversuche.loc['Druck Nr. 11', 'Zugfestigkeit (MPa)']
print(f'Zugfestigkeit Druck Nr. 11: {zugfestigkeit_11} MPa')

# Einzelne Zelle: Erfolg von Druck Nr. 7
erfolg_7 = druckversuche.loc['Druck Nr. 7', 'Erfolgreich']
print(f'Druck Nr. 7 erfolgreich: {erfolg_7}')
```

1. Auch hier wird `index_col=0` gesetzt, da "Nummer" die erste Spalte ist.
2. `druck6` ist eine Series mit dem Zeilenindex `Druck Nr. 6` als Name.
3. `print(druck6)` zeigt alle 15 Merkmale dieses Druckversuchs an, z. B.
   Material ASA, Farbe transparent, Zugfestigkeit 24.4 MPa.
4. Die Zugfestigkeit von Druck Nr. 11 beträgt 40.9 MPa.
5. Druck Nr. 7 war **nicht** erfolgreich (Eintrag "nein").
````

## Mehrfachauswahl und Tabelle erweitern

Sollen mehrere Zeilen oder Spalten gleichzeitig ausgewählt werden, werden
mehrere Spaltenlabels oder mehrere Zeilenlabels in einer Liste verwendet. Wir
demonstrieren die Mehrfachauswahl hier für Spalten.

Mit einer Liste in eckigen Klammern wählen wir mehrere Spalten auf einmal aus,
in diesem Beispiel sowohl die Erstzulassung als auch den Preis.

```{code-cell} python
mehrere_spalten = tabelle[['Erstzulassung', 'Preis (Euro)']]
mehrere_spalten.head()
```

Wenn Spalten oder Zeilen aufeinanderfolgen, also zusammenhängend sind, brauchen
wir nicht alle Indizes in die Liste zu schreiben. Es genügt, den ersten Index
und den letzten Index zu nehmen und dazwischen einen Doppelpunkt zu setzen.
Diese Art, Zeilen oder Spalten auszuwählen, wird in der Informatik als
**Slicing** bezeichnet. Da die Autos in diesem Datensatz nach Marke sortiert
sind, können wir alle Autos der Marke Citroën per Slicing extrahieren:

```{code-cell} python
citroens = tabelle.loc['Citroen Nr. 1':'Citroen Nr. 5'] 
citroens.head()
```

Wichtig dabei ist, dass beim Slicing mit `.loc[start:ende]` der Endwert im
Gegensatz zu Python-Listen eingeschlossen ist.

Jetzt kann beispielsweise der durchschnittliche Verkaufspreis aller Citroëns
folgendermaßen ermittelt werden:

```{code-cell} python
durchschnittspreis = citroens['Preis (Euro)'].mean()
print(f'Der durchschnittliche Verkaufspreis der Citroens ist {durchschnittspreis:.2f} EUR.')
```

Beim Slicing können wir den Anfangsindex oder den Endindex oder sogar beides
weglassen. Wenn wir den Anfangsindex weglassen, fängt Pandas bei der ersten
Zeile/Spalte an. Lassen wir den Endindex weg, geht der Slice automatisch bis zum
Ende.

Auch das Erweitern der Tabelle funktioniert über denselben Mechanismus: Um eine
neue Spalte einzufügen, wird einfach ein neuer Spaltenname erzeugt.

```{code-cell} python
# Erweiterung der Tabelle um eine neue Spalte
tabelle['Preis pro Leistung'] = tabelle['Preis (Euro)'] / tabelle['Leistung (PS)']

# Überblick
print(f'Anzahl Autos: {tabelle.shape[0]}')
print(f'Anzahl Merkmale/Spalten: {tabelle.shape[1]}')
tabelle.head()
```

Nach demselben Prinzip lässt sich mit `.loc[]` auch eine neue Zeile einfügen,
indem ein neuer Zeilenindex vergeben wird. Das Einfügen einer neuen Spalte oder
Zeile über einen neuen Index funktioniert allerdings nur, wenn die neuen Daten
das richtige Format haben. Sollen mehrere bereits als DataFrame vorliegende
Zeilen oder Spalten zusammengeführt werden, eignet sich `pd.concat()` (siehe
[Dokumentation →
concat](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html?highlight=concat#pandas.concat)).

```{admonition} Mini-Übung
:class: tip
Verwenden Sie erneut den Datensatz `3ddruck_xxs.csv`.

1. Lesen Sie die Datei ein und verwenden Sie dabei die Nummer als Zeilenindex.
2. Wählen Sie gleichzeitig die Spalten `Material`, `Infill (%)` und
   `Zugfestigkeit (MPa)` aus und speichern Sie das Ergebnis in einer Variablen
   `auswahl`.
3. Wählen Sie alle Druckversuche von `Druck Nr. 5` bis `Druck Nr. 9` als
   zusammenhängenden Bereich aus und speichern Sie das Ergebnis in einer
   Variablen `teilbereich`.
4. Wie hoch ist die durchschnittliche Zugfestigkeit in diesem Teilbereich?
5. Erweitern Sie den Datensatz um eine neue Spalte `Zugfestigkeit pro Infill`,
   die sich aus der Zugfestigkeit geteilt durch den Infill-Anteil berechnet.
```

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

# Einlesen der csv-Datei mit der Spalte Nummer als Zeilenindex
druckversuche = pd.read_csv('3ddruck_xxs.csv', index_col=0)

# Mehrere Spalten gleichzeitig auswählen
auswahl = druckversuche[['Material', 'Infill (%)', 'Zugfestigkeit (MPa)']]
auswahl.head()

# Zusammenhängender Zeilenbereich per Slicing
teilbereich = druckversuche.loc['Druck Nr. 5':'Druck Nr. 9']
teilbereich

# Durchschnittliche Zugfestigkeit im Teilbereich
durchschnitt = teilbereich['Zugfestigkeit (MPa)'].mean()
print(f'Durchschnittliche Zugfestigkeit: {durchschnitt:.2f} MPa')

# Tabelle um eine neue Spalte erweitern
druckversuche['Zugfestigkeit pro Infill'] = druckversuche['Zugfestigkeit (MPa)'] / druckversuche['Infill (%)']
druckversuche.head()
```

1. Auch hier wird `index_col=0` gesetzt, da "Nummer" die erste Spalte ist.
2. `auswahl` ist ein DataFrame mit den drei ausgewählten Spalten.
3. `teilbereich` enthält die fünf Druckversuche Nr. 5 bis Nr. 9 (beim Slicing
   mit `.loc[]` ist der Endindex eingeschlossen).
4. Die durchschnittliche Zugfestigkeit in diesem Teilbereich beträgt rund
   30.92 MPa.
5. Die neue Spalte ergibt sich durch elementweise Division. Da die Spalte
   `Infill (%)` die reinen Zahlenwerte (z. B. 30 statt 0.30) enthält, ergibt
   sich bei Druck Nr. 1 der Wert 28.8 / 30 = 0.96 MPa je Prozentpunkt Infill.
   Diese Kennzahl ist eine vereinfachte, rein beschreibende Größe: Sie belegt
   nicht, dass die Zugfestigkeit linear mit dem Infill-Anteil zunimmt, da
   weitere Einflussgrößen wie Material, Schichthöhe oder Drucktemperatur
   unberücksichtigt bleiben.
````

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir verschiedene Wege kennengelernt, gezielt auf
Ausschnitte eines DataFrames zuzugreifen: mit **[]** auf einzelne Spalten, mit
**.loc[]** auf einzelne Zeilen und Zellen sowie mit Listen und Slicing auf
mehrere Zeilen oder Spalten gleichzeitig. Außerdem haben wir gesehen, wie sich
eine Tabelle über denselben Mechanismus um eine neue Spalte erweitern lässt.

Diese Zugriffsmuster bilden das Handwerkszeug für die weitere Arbeit mit
Tabellendaten. Im nächsten Kapitel nutzen wir sie, um ausgewählte Spalten und
Zeilen gezielt zu visualisieren und so einen besseren Eindruck von den Daten
zu gewinnen.
