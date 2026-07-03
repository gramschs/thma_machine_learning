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

# 5.3 Daten filtern und gruppieren

Im vorherigen Kapitel haben wir Autos basierend auf ihrem Kilometerstand
gruppiert und visualisiert. Während diese Gruppierung automatisch im Hintergrund
stattfand, werden wir in diesem Kapitel lernen, wie wir direkt auf die
gruppierten Daten zugreifen und zusätzliche Analysen durchführen können.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie wissen, dass die Wahrheitswerte `True` (wahr)  oder `False` (falsch) in
  dem Datentyp **bool** gespeichert werden.
* Sie kennen die wichtigsten Vergleichsoperatoren (`<`, `<=`, `>`, `>=`, `==`,
  `!=`, `in`, `not in`) in Python.
* Sie können ein Pandas-DataFrame-Objekt nach einem Wert filtern.
* Sie können ein Pandas-DataFrame-Objekt mit den Methoden `groupby()` und
  `get_group()` gruppieren.
```

## Daten filtern

Im vorherigen Kapitel haben wir die Kilometerstände von Autos untersucht, die im
Jahr 2020 zugelassen und Mitte 2023 auf Autoscout24.de angeboten wurden. Bei der
Kategorisierung der Kilometerstände fiel auf, dass Fahrzeuge mit einer
Laufleistung von über 200000 km selten sind. Trotzdem beeinflusste dies die
Aufteilung in zehn gleichmäßige Gruppen, die von 0 km bis 435909 km reichten,
erheblich. Um eine genauere Analyse zu ermöglichen, wäre es sinnvoll, Fahrzeuge
mit einer Laufleistung von bis zu 200.000 km in den Fokus zu nehmen und die
Ausreißer auszuschließen. Daher widmen wir uns in diesem Kapitel der Filterung
von tabellarischen Datensätzen mithilfe von Pandas.

Zuerst laden wir den Datensatz `autoscout24_DE_2020.csv` und überprüfen den
Inhalt.

```{code-cell}
import pandas as pd

url = 'https://raw.githubusercontent.com/gramschs/assets/refs/heads/main/ml4ing/data/autoscout24_DE_2020.csv'
data = pd.read_csv(url)
data.info()
```

Um die Autos mit einem Kilometerstand von bis zu 200000 km zu filtern,
vergleichen wir die entsprechende Spalte mit dem Wert 200000, indem wir den aus
der Mathematik bekannten Kleiner-gleich-Operator `<=` benutzen. Das Ergebnis
dieses Vergleichs speichern wir in der Variable `bedingung_kilometerstand`.

```{code-cell}
bedingung_kilometerstand = data['Kilometerstand (km)'] <= 200000
```

Aber was genau ist in der Variable `bedingung_kilometerstand` enthalten? Schauen
wir uns den Datentyp an:

```{code-cell}
type(bedingung_kilometerstand)
```

Offensichtlich handelt es sich um ein Pandas-Series-Objekt. Für weitere
Informationen können wir die `.info()`-Methode aufrufen:

```{code-cell}
bedingung_kilometerstand.info()
```

In dem Series-Objekt sind 18566 Einträge vom Datentyp `bool` gespeichert. Diesen
Datentyp haben wir bisher nicht kennengelernt. Wir lassen die ersten fünf
Einträge ausgeben:

```{code-cell}
bedingung_kilometerstand.head()
```

Sind alle Einträge mit dem Wert `True` gefüllt? Wie viele und vor allem welche
einzigartige Einträge gibt es in diesem Series-Objekt?

```{code-cell}
bedingung_kilometerstand.unique()
```

Das Series-Objekt enthält nur `True` und `False`, was den Datentyp `bool`
charakterisiert. In diesem Datentyp können nur zwei verschiedene Werte
gespeichert werden, nämlich wahr (True) und falsch (False). Oft sind
Wahrheitswerte das Ergebnis eines Vergleichs, wie das folgende Code-Beispiel
zeigt:

```{code-cell}
x = 19
print(x < 100)
```

In der Python-Programmierung wird der Datentyp `bool` oft verwendet, um
Programmcode zu verzweigen. Damit ist gemeint, dass Teile des Programms nur
durchlaufen und ausgeführt werden, wenn eine bestimmte Bedingung wahr (True)
ist. In dieser Vorlesung benutzen wir `bool`-Werte hauptsächlich zum Filtern von
Daten.

```{admonition} Welche Vergleichsoperatoren kennt Python?
:class: note
In Python können die mathematischen Vergleichsoperatoren in ihrer gewohnten
Schreibweise verwendet werden:
* `<` kleiner als
* `<=` kleiner als oder gleich 
* `>` größer als
* `>=` größer als oder gleich
* `==` gleich (`=` ist der Zuweisungsoperator, nicht mit Gleichheit
  verwechseln!)
* `!=` ungleich 

Darüber hinaus kann mit `in` oder `not in` getestet werden, ob
ein Element in einer Liste ist oder eben nicht.
```

Aber was machen wir jetzt mit diesem Series-Objekt? Wir können es als Index
benutzen für den ursprünglichen Datensatz benutzen. Die Zeilen, in denen `True`
steht, werden übernommen, die anderen verworfen.

```{code-cell}
autos_bis_200000km = data[bedingung_kilometerstand]
autos_bis_200000km.info()
```

Von den 18566 Autos wurden 18525 Autos übernommen. Ist denn die Filterung
geglückt? Wir verschaffen uns mit der `.describe()`-Methode einen schnellen
Überblick.

```{code-cell}
autos_bis_200000km.describe()
```

Der maximale Eintrag für die Spalte `Kilometerstand (km)` ist 199000 km. Mit dem
Tilde-Operator `~` können wir das Pandas-Series-Objekt
`bedingung_kilometerstand` in das Gegenteil umwandeln. Damit können wir also die
Autos mit einem Kilometerstand über 200.000 km herausfiltern.

```{code-cell}
autos_ab_200000km = data[~bedingung_kilometerstand]
autos_ab_200000km.info()
```

41 Autos, die 2020 zugelassen wurden, sollten Mitte 2023 mit einem
Kilometerstand von mehr als 200000 km verkauft werden. Schauen wir uns die
Statistik an.

```{code-cell}
autos_ab_200000km.describe()
```

Und was sind das für Autos?

```{code-cell}
autos_ab_200000km.head(10)
```

```{admonition} Mini-Übung
:class: tip
Filtern Sie den Datensatz so, dass nur Autos mit einem Preis zwischen 
10.000 und 30.000 Euro übrig bleiben. Wie viele Autos erfüllen diese 
Bedingung? Tipp: Sie können zwei Bedingungen mit `&` (und) verknüpfen.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
bedingung_preis = (data['Preis (Euro)'] >= 10000) & (data['Preis (Euro)'] <= 30000)
autos_mittlerer_preis = data[bedingung_preis]
print(f"Anzahl Autos: {len(autos_mittlerer_preis)}")
```
Es gibt 11.793 Autos in dieser Preisklasse.

Wichtig: Die Klammern um die einzelnen Bedingungen sind notwendig!
````

## Daten gruppieren

Eine Filterung nach Kilometerstand ermöglicht es uns, die Autos in zwei
Datensätze zu teilen: Autos mit bis zu 200000 km Laufleistung und jene mit mehr
als 200000 km (hierzu kann der Tilde-Operator (~) verwendet werden).

Wenden wir nun diese Technik an, um die Fahrzeuge basierend auf ihrer Marke zu
trennen. Ein Beispiel: Um alle "Audi"-Fahrzeuge zu extrahieren, verwenden wir
den folgenden Code:

```{code-cell}
bedingung_audi = data['Marke'] == 'audi'
audis = data[bedingung_audi]
audis.info()
```

Diese Bedingung erfüllen 1.190 Autos. Der Gesamtdatensatz enthält jedoch 41
unterschiedliche Automarken. Es wäre ineffizient, für jede Marke eine separate
Filterung durchzuführen. Deshalb bietet Pandas die `.groupby()`-Methode, die es
erlaubt, die Daten automatisch nach den einzigartigen Einträgen einer Spalte zu
gruppieren:

```{code-cell}
autos_nach_marke = data.groupby('Marke')
type(autos_nach_marke)
```

Das Resultat ist eine spezielle Pandas-Datenstruktur namens `DataFrameGroupBy`.
Auf dieses Objekt sind nicht alle bekannten DataFrame-Methoden anwendbar, aber
beispielsweise die `.describe()`-Methode darf verwendet werden:

```{code-cell}
autos_nach_marke.describe()
```

Für jede Automarke werden nun für jede Spalte mit numerischen Informationen die
statistischen Kennzahlen ermittelt. Die entstehende Tabelle ist etwas
unübersichtlich. Besser ist daher, sich die statistischen Kennzahlen einzeln
ausgeben zu lassen. Im Folgenden ermitteln wir die Mittelwerte der numerischen
Informationen nach Automarke. Ohne das Argument `numeric_only=True` würde Pandas
versuchen, auch die nicht-numerischen Spalten (wie 'Marke' oder 'Farbe') zu
mitteln, was zu einer Fehlermeldung führen würde. Mit diesem Argument wird die
Operation nur auf numerische Spalten angewendet.

```{code-cell}
durchschnittspreis_pro_marke = autos_nach_marke['Preis (Euro)'].mean()

# Visualisierung
import plotly.express as px
fig = px.bar(durchschnittspreis_pro_marke, 
             title='Durchschnittlicher Preis pro Automarke',
             labels = {'value': 'Preis [EUR]'})
fig.show()
```

Eine sehr wichtige Methode der GroupBy-Datenstruktur ist die
`get_group()`-Methode. Damit können wir ein bestimmtes DataFrame-Objekt aus dem
GroupBy-Objekt extrahieren:

```{code-cell}
audis_alternativ = autos_nach_marke.get_group('audi')
audis_alternativ.info()
```

In der Variablen `audis_alternativ` steckt nun der gleiche Datensatz wie in der
Variablen `audis`, den wir bereits durch das Filtern des ursprünglichen
Datensatzes extrahiert haben. Beide Methoden führen zum gleichen Ergebnis. Die
Filterung mit Bedingungen ist direkter und oft intuitiver. Die Gruppierung mit
`.groupby()` und `.get_group()` ist besonders nützlich, wenn wir mehrere Gruppen
nacheinander untersuchen möchten, da wir die Gruppierung nur einmal durchführen
müssen.

```{admonition} Mini-Übung
:class: tip
Gruppieren Sie die Autos nach 'Kraftstoff' und berechnen Sie den 
durchschnittlichen Preis für jede Kraftstoffart. Welche Kraftstoffart 
ist im Durchschnitt am teuersten?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
autos_nach_kraftstoff = data.groupby('Kraftstoff')
durchschnittspreis = autos_nach_kraftstoff['Preis (Euro)'].mean()
print(durchschnittspreis.sort_values(ascending=False))
```
Die teuerste Kraftstoffart im Durchschnitt ist Hybrid (Elektro/Diesel). Einträge
ohne Angabe vernachlässigen wir hier.
````

## Wann filtern, wann gruppieren?

Wir *filtern*, wenn wir einen Ausschnitt der Daten analysieren wollen. Zum
Beispiel könnten wir nur die Audis untersuchen wollen. Das Ergebnis ist ein
neuer DataFrame mit den gefilterten Zeilen. Wenn wir jedoch alle Kategorien
vergleichen wollen, nutzen wir die *Gruppierung*. Beispielsweise könnten wir die
Durchschnittpreise pro Marke berechnen wollen.

Beide Methoden können auch kombiniert werden. Wir können auch erst gruppieren
und dann eine spezifische Gruppe mit `.get_group()` extrahieren. Dies ist
besonders nützlich, wenn wir die Gruppierung für mehrere Analysen
wiederverwenden möchten.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir die Technik des Datenfilterns kennengelernt. Um
spezifische Einträge aus einem Datensatz basierend auf einem bestimmten Wert zu
extrahieren, nutzen wir Vergleichsoperationen und verwenden das resultierende
Series-Objekt als Index. Wenn das Ziel darin besteht, Daten anhand der
einzigartigen Werte einer Spalte zu gruppieren, dann ist die Kombination von
`.groupby()` und `.get_group()` oft der effizienteste Weg. Damit haben wir
unsere Einführung in die Datenexploration abgeschlossen, obwohl es noch viele
weitere Möglichkeiten gibt, die Daten zu erkunden. Im nächsten Kapitel beginnen
wir mit den Grundlagen des maschinellen Lernens und beschäftigen uns mit
Entscheidungsbäumen.
