---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 5.1 Was sind kategoriale Daten?

In unserem bisherigen Beispiel zu den Autoverkaufspreisen haben wir bestimmte
Eigenschaften der Autos, wie die Marke oder die Farbe, nicht berücksichtigt. In
den vorherigen Kapiteln konzentrierten sich unsere Analysen hauptsächlich auf
numerische Werte wie den Kilometerstand. Dies liegt daran, dass es für Daten wie
Farben oder Automarken keine Rechenoperationen gibt. In diesem Kapitel werden
wir uns intensiver mit diesen nicht-numerischen Daten auseinandersetzen.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie wissen, was **numerische (metrische oder quantitative) Daten** sind.
* Sie wissen, was **kategoriale (qualitative) Daten** sind.
* Sie können die Methode **.unique()** benutzen, um die eindeutigen Werte eines
  Pandas-Series-Objektes aufzulisten.
* Sie kennen den Unterschied zwischen **ungeordneten** und **geordneten**
  kategorialen Daten.
* Sie können mit der Methode **.value_counts()** die Anzahl der eindeutigen
  Werte eines Pandas-Series-Objektes bestimmen lassen.
* Sie wissen, was der **Modalwert** oder **Modus** eines Datensatzes ist und
  können diesen mit der Methode **.mode()** bestimmen lassen.
```

## Was wir bisher hatten: numerische Daten

In den bisherigen Kapiteln lag unser Fokus auf den Verkaufspreisen von Autos.
Die Methode `.describe()` in Pandas bietet eine schnelle Möglichkeit, einen
Überblick über die statistischen Kennzahlen eines Datensatzes zu erhalten.
Interessanterweise berücksichtigt die `describe()`-Methode nur numerische Werte
(also Zahlen wie Integer und Floats) für die Auswertung. Dennoch bestimmen auch
die nicht-numerischen Eigenschaften eines Autos den Verkaufspreis. Die Farbe
eines Autos beispielsweise beeinflusst häufig die Kaufentscheidung und damit den
Preis.

Bevor wir uns den nicht-numerischen Daten widmen, vertiefen wir unser
Verständnis für numerische Daten. Diese werden oft auch als **metrische oder
quantitative Daten** bezeichnet.

```{admonition} Was sind ... metrische/quantitative/numerische Daten?
:class: note
Metrische Daten sind Informationen, die gemessen werden können. Daher können sie
durch Zahlen (ganze Zahlen, rationale oder reelle Zahlen) auf einer Skala
dargestellt werden und werden numerische Daten genannt. Ein anderer Name für
metrische Daten ist der Begriff quantitative Daten. 
```

Wir betrachten den Datensatz {download}`Download autoscout24_DE_2020.csv
<https://gramschs.github.io/book_ml4ing/data/autoscout24_DE_2020.csv>` mit
Autoverkaufspreises von [Autoscout24.de](https://www.autoscout24.de), der alle
Autos enthält, die im Jahr 2020 zugelassen wurden. Ein kurzer Überblick über den
Datensatz hilft uns, die Art der Daten besser zu verstehen.

```{code-cell}
import pandas as pd

url = 'https://raw.githubusercontent.com/gramschs/assets/refs/heads/main/ml4ing/data/autoscout24_DE_2020.csv'
data = pd.read_csv(url)
data.info()
```

```{admonition} Mini-Übung
:class: tip

Welche Eigenschaften der Autos sind numerisch (metrisch/quantitativ)? Würden Sie
bei anderen Eigenschaften ebenfalls einen metrischen Datentyp erwarten?
```

```{admonition} Lösung
:class: tip
:class: dropdown
Das Jahr und der Preis (Euro) sind ganze Zahlen (Integer). Die Leistung der
Autos wird als Fließkommazahl (Float) angegeben, unabhängig von der Einheit kW
oder PS. Auch der Kilometerstand wird durch eine Fließkommazahl (Float)
repräsentiert. Das hätte man auch für den Verbrauch in Spalte 10 oder 11
erwarten können. Die Angabe der Einheit l/100 km oder g/km in den Zellen hat
verhindert, dass Pandas diese Informationen als Zahl interpretiert.
```

Mit numerischen Daten können wir umfangreiche Datenanalysen durchführen. Wir
können vergleichen, ob zwei Messwerte gleich oder ungleich sind. Wir können
beurteilen, ob ein Messwert kleiner oder größer als ein anderer ist oder sogar
das Minimum und das Maximum aller Messwerte bestimmen. Und vor allem können wir
mit metrischen Daten rechnen. Erst dadurch ist es möglich, einen Mittelwert zu
bilden oder Streuungsmaße wie Spannweite, Standardabweichung und
Interquartilsabstand zu berechnen. Solche detaillierten Berechnungen sind nur
bei metrischen (quantitativen) Daten möglich.

## Das Gegenteil von numerischen Daten: kategoriale Daten

Während numerische Daten messbare Informationen darstellen, sind **kategoriale
Daten** durch ihre Zugehörigkeit zu bestimmten Kategorien oder Gruppen
definiert. Ein weiterer Begriff für kategoriale Daten ist **qualitative Daten**.
Ein gutes Beispiel für kategoriale Daten ist die Farbe eines Autos. Oft gibt der
Datentyp einer bestimmten Eigenschaft in einem Datensatz bereits Hinweise
darauf, ob es sich um kategoriale oder numerische Daten handelt.

Die obige Ausführung der Anweisung `data.info()` hat gezeigt, dass einige Daten
als `objects` gespeichert sind, was oft auf kategoriale Daten hinweist. Ein
Blick in die Spalte »Marke« gibt uns weitere Einblicke.

```{code-cell}
data['Marke'].head(10)
```

Die ersten 10 Autos sind offensichtlich Alfa Romeos. Sind vielleicht nur Alfa
Romeos in der Tabelle enthalten? Wir schauen uns die letzten 10 Einträge an.

```{code-cell}
data['Marke'].tail(10)
```

Die letzten Einträge sind Volvos. Vielleicht sind die Autos nach Marken
alphabetisch geordnet? Es wäre schön zu wissen, welche verschiedenen Marken im
Datensatz enthalten sind. Dazu gibt es die Methode `.unique()`. Sie gehört zu
der Datenstruktur Pandas-Series. Wenn wir eine einzelne Spalte eines
Pandas-DataFrames herausgreifen, liegt automatisch ein Pandas-Series-Objekt vor,
so dass wir diese Methode hier benutzen können.

```{code-cell}
data['Marke'].unique()
```

Obwohl der Datensatz insgesamt 18566 Autos umfasst, gibt es nur 41 verschiedene
Marken. Allgemein gesagt, gibt es für die Eigenschaft »Marke« 41 Kategorien.
Eine nicht-metrische Eigenschaft, die nur eine begrenzte Anzahl von Werten
annehmen kann, wird als kategoriale Variable bezeichnet. Ihre konkreten Werte
werden als kategoriale Daten oder qualitative Daten bezeichnet.

```{admonition} Was sind ... kategoriale/qualitative Daten?
:class: note
Kategoriale Daten sind Informationen, die nicht gemessen werden können.
Stattdessen werden sie durch die Zugehörigkeit zu einer Kategorie dargestellt.
Sie bekommen ein Etikett. Kategoriale Daten nehmen nur eine begrenzte Anzahl
von verschiedenen Werten an. Oft bezeichnet man kategoriale Daten auch als
qualitative Daten.
```

Diese Definition ist nicht präzise. Der Begriff 'begrenzte Anzahl' von Werten
ist etwas schwammig. Sind damit 10 Kategorien gemeint oder 100 oder 1000? Welche
Eigenschaften des Auto-Datensatzes sind kategorial? In der Praxis spricht man
von kategorialen Daten, wenn die Anzahl der Kategorien deutlich kleiner als die
Anzahl der Datenpunkte ist (oft als Faustregel: < 5-10 % der Beobachtungen).

```{admonition} Mini-Übung
:class: tip
Suchen Sie sich drei nicht-metrische Eigenschaften aus und bestimmen Sie
die Anzahl der einzigartigen Einträge dieser Eigenschaft.

Tipp: Die Methode `.unique()` liefert ein sogenanntes NumPy-Array zurück, das
hier wie eine Liste benutzt werden kann. Die Python-Funktion `len()` kann die
Länge einer Liste, also die Anzahl der Elemente der Liste, bestimmen.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
anzahl_einzigartige_werte = len(data['Modell'].unique())
print(f'Die Spalte/Eigenschaft Modell hat {anzahl_einzigartige_werte} einzigartige Werte.')
```

Offensichtlich gibt es 561 einzigartige Werte für die Spalte/Eigenschaft Modell.

Mit einer for-Schleife können wir auch alle Eigenschaften durchgehen, indem wir
das Attribut `.columns` nutzen, in dem alle Spaltenüberschriften gespeichert
sind. Damit betrachten wir natürlich auch die metrischen/quantitativen
Eigenschaften.

```python
for col in data.columns:
    anzahl_einzigartige_werte = len(data[col].unique())
    print(f'Die Spalte/Eigenschaft {col} hat {anzahl_einzigartige_werte} einzigartige Werte.')
```

Damit erhalten wir folgende Ausgabe:
```{code}
Die Spalte/Eigenschaft Marke hat 41 einzigartige Werte.
Die Spalte/Eigenschaft Modell hat 561 einzigartige Werte.
Die Spalte/Eigenschaft Farbe hat 15 einzigartige Werte.
Die Spalte/Eigenschaft Erstzulassung hat 12 einzigartige Werte.
Die Spalte/Eigenschaft Jahr hat 1 einzigartige Werte.
Die Spalte/Eigenschaft Preis (Euro) hat 4926 einzigartige Werte.
Die Spalte/Eigenschaft Leistung (kW) hat 260 einzigartige Werte.
Die Spalte/Eigenschaft Leistung (PS) hat 260 einzigartige Werte.
Die Spalte/Eigenschaft Getriebe hat 4 einzigartige Werte.
Die Spalte/Eigenschaft Kraftstoff hat 10 einzigartige Werte.
Die Spalte/Eigenschaft Verbrauch (l/100 km) hat 238 einzigartige Werte.
Die Spalte/Eigenschaft Verbrauch (g/km) hat 616 einzigartige Werte.
Die Spalte/Eigenschaft Kilometerstand (km) hat 10730 einzigartige Werte.
Die Spalte/Eigenschaft Bemerkungen hat 16547 einzigartige Werte.
```
````

Bei unserem Beispiel sind die Eigenschaften Marke, Modell, Farbe, Getriebe,
Kraftstoff und Bemerkungen nicht-numerische Eigenschaften. Allerdings hat die
Eigenschaft Bemerkungen 16547 verschiedene Werte. Ein Merkmal von kategorialen
bzw. qualitativen Daten ist aber, dass nur eine begrenzte Anzahl von
verschiedenen Werten angenommen wird. Das ist hier nicht mehr der Fall, so dass
wir die Eigenschaft Bemerkung nicht als kategoriale/qualitative Eigenschaft
einstufen. Die kategorialen Eigenschaften in dem Beispiel sind also Marke,
Modell, Farbe, Getriebe und Kraftstoff.

## Kategoriale Daten: ungeordnet oder geordnet?

Innerhalb der kategorialen bzw. qualitativen Daten gibt es wiederum zwei Arten
von Datentypen:

* ungeordnete kategoriale Daten und
* geordnete kategoriale Daten.

Ungeordnete kategoriale Daten werden in der Statistik auch **nominalskalierte
Daten** genannt, während die geordneten kategorialen Daten auch als
**ordinalskalierte Daten** bezeichnet werden.

Ein typisches Beispiel für ungeordnete kategoriale Daten sind die Farben der
Autos. Es gibt keine natürliche Reihenfolge für Farben. Wir könnten die Farbe
alphabetisch anordnen, doch sobald wir eine andere Sprache benutzen, wäre auch
die Reihenfolge anders. Farben sind ungeordnete Kategorien. Für statistische
Analysen heißt das, dass nur bestimmt werden kann, ob die Farbe eines Autos in
eine bestimmte Kategorie fällt oder nicht. Entweder das Auto ist gelb oder es
ist nicht gelb. Mathematisch gesehen können wir also nur auf Gleichheit oder
Ungleichheit prüfen. Es gibt keine Vergleiche bzgl. der Reihenfolge und auch
kein Minimum oder Maximum. Auch sämtliche Rechenoperationen entfallen und daher
können auch nicht Mittelwerte oder Streuungsmaße bestimmt werden. Stattdessen
wird der **Modus** oder **Modalwert** bestimmt.

```{admonition} Was ist ... der Modus (Modalwert)?
:class: note
Der Modus, auch Modalwert genannt, ist der häufigste auftretende Wert in dem
Datensatz. Er gehört zu den Lageparametern in der Statistik. Er existiert sowohl
für ungeordnete und geordnete kategoriale Daten als auch für metrische Daten.
Ein Datensatz kann auch mehrere Modi haben, wenn mehrere Werte gleich häufig
vorkommen.
```

Pandas bietet eine Methode zur Bestimmung des Modus namens `.mode()`. Diese
Methode funktioniert wieder nur für ein Pandas-Series-Objekt, so dass zuerst
eine einzelne Spalte aus der Tabelle herausgeschnitten wird. Auf diese Spalte
wird dann die Methode angewendet. Gibt es mehrere Modi, so werden alle
zurückgegeben.

```{code-cell}
modus_farben = data['Farbe'].mode()
print(f'Die häufigste Farbe ist {modus_farben}.')
```

Und wie häufig kommen die anderen Farben vor? Die Methode `.value_counts()`
zählt die Anzahl an Autos mit einer bestimmten Farbe.

```{code-cell}
data['Farbe'].value_counts()
```

## Der Mehrwert geordneter kategorialer Daten

Was macht geordnete kategoriale Daten besonders? Bei ungeordneten kategorialen
Daten wie Farben gibt es keine sinnvolle Reihenfolge. Bei geordneten
kategorialen Daten wie Monaten dagegen schon:

```{code-cell}
# Bei Farben: Sortierung ist willkürlich (alphabetisch)
print("Farben alphabetisch:")
print(data['Farbe'].value_counts())

# Bei Monaten: Sortierung ist sinnvoll (chronologisch)
print("\nMonate chronologisch:")
print(data['Erstzulassung'].value_counts().sort_index())
```

Jetzt können wir erkennen: Im ersten Quartal (01/2020, 02/2020, 03/2020) wurden
deutlich mehr Autos zugelassen als im letzten Quartal. Diese Aussage setzt
voraus, dass die Kategorien eine **Reihenfolge** haben.

Bei Farben wäre die Aussage "Im ersten Drittel der Farben wurden mehr Autos
verkauft" sinnlos, denn was ist das "erste Drittel" von Farben?

Das ist der entscheidende Unterschied: Bei nominalen Daten können wir nur
Häufigkeiten zählen. Bei ordinalen Daten können wir zusätzlich die Reihenfolge
nutzen, um Aussagen wie 'im ersten Quartal' oder 'mehr als in der zweiten
Hälfte' zu treffen.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir uns mit dem Unterschied zwischen numerischen
(metrischen bzw. quantitativen) und kategorialen (qualitativen) Daten
beschäftigt. Dabei wird bei kategorialen Daten noch zwischen ungeordneten und
geordneten Kategorien unterschieden. Je nach Art der Daten können
unterschiedliche statistische Kennzahlen erhoben werden. Bei ungeordneten
kategorialen Daten kann nur der Modus (Modalwert) berechnet werden. Bei
geordneten kategorialen Daten können zusätzlich noch Quantile (insbesondere der
Median) berechnet werden. Nur bei numerischen (metrischen bzw. quantitativen)
Daten ist es möglich, den Mittelwert und zusätzlich die Streuungsmaße
(Spannbreite, Standardabweichung und Interquartilsabstand) zu bestimmen. Im
nächsten Kapitel werden wir uns mit der Visualisierung der kategorialen Daten
beschäftigen.
