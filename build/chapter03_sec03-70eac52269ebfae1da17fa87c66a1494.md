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

# 3.3 Boxplots mit Plotly

Die wichtigsten statistischen Kennzahlen lassen sich mit einem Diagramm
visualisieren, das Boxplot genannt wird. Gelegentlich wird auch der deutsche
Begriff Kastendiagramm dafür gebraucht. In diesem Kapitel visualisieren wir nur
einen Datensatz. Die große Stärke der Boxplots ist normalerweise, die
statistischen Kennzahlen von verschiedenen Datensätzen nebeneinander zu
visualisieren, um so leicht einen Vergleich der Datensätze zu ermöglichen.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können **Plotly Express** mit der typischen Abkürzung **px** importieren.
* Sie können mit **px.box()** einen Boxplot eines Pandas-Series-Objektes
  visualisieren.
* Sie können die Beschriftung eines Boxplots verändern. Dazu gehört die
  Beschriftung der Achsen und der Titel.
* Sie können die Datenpunkte neben einem Boxplot anzeigen lassen.
* Sie wissen, was ein **Ausreißer** ist und können Ausreißer im Boxplot anzeigen
  lassen.
```

## Plotly

Es gibt zahlreiche Python-Module zur Visualisierung von Daten. In dieser
Vorlesung verwenden wir **Plotly**, das im Gegensatz zu anderen Bibliotheken wie
Matplotlib interaktive Diagramme erstellt. Mit **Plotly Express** steht uns eine
einfach zu bedienende Schnittstelle zur Erstellung verschiedenster Diagrammtypen
zur Verfügung.

Üblicherweise wird Plotly Express als `px` abgekürzt.

```{code-cell}
import plotly.express as px
```

Sollte eine Fehlermeldung auftreten, kann Plotly mit `!pip install plotly` oder
`!conda install plotly` nachinstalliert werden.

## Boxplots mit Plotly Express

Wir greifen erneut unser Autoscout24-Beispiel mit den 10 Autos auf.

```{code-cell}
import pandas as pd

preisliste = [1999, 35990, 17850, 46830, 27443, 14240, 19950, 15950, 21990, 12450]
preise = pd.Series(preisliste, index=[
  'Audi Nr. 1', 'Audi Nr. 2', 'Audi Nr. 3',
  'BMW Nr. 1', 'BMW Nr. 2', 
  'Citroen Nr. 1', 'Citroen Nr. 2', 'Citroen Nr. 3', 'Citroen Nr. 4', 'Citroen Nr. 5'
  ])

print(preise)
```

Um einen Boxplot zu erstellen, nutzen wir die Funktion `box()` von Plotly
Express. Wir speichern das Diagramm, das durch diese Funktion erstellt wird, in
der Variablen `diagramm`. Um es dann auch nach seiner Erzeugung tatsächlich
anzeigen zu lassen, verwenden wir die Methode `.show()`. Zusammen sieht der
Python-Code zur Erzeugung eines Boxplots folgendermaßen aus:

```{code-cell}
diagramm = px.box(preise)
diagramm.show()
```

Bewegen wir die Maus über dem Diagramm, sehen wir verschiedene interaktive Funktionen:

* Hover-Informationen zeigen die genauen Werte an.
* Rechts oben erscheinen Buttons zum Zoomen, Verschieben und Herunterladen.
* Mit der Maus können wir in das Diagramm hineinzoomen.

Die untere Antenne (Whisker) zeigt das Minimum an, die obere Antenne das Maximum
der Daten. Der Kasten (Box) wird durch das untere Quartil Q1 und das obere
Quartil Q3 begrenzt. Oder anders formuliert: In der Box liegen 50 % aller
Datenpunkte. Der Median wird durch die horizontale Linie in der Box dargestellt.

```{admonition} Mini-Übung
:class: tip
Erstellen Sie einen Boxplot der Autopreise und beantworten Sie anhand des 
Diagramms:
1. Was ist der Median (die mittlere Linie in der Box)?
2. Zwischen welchen beiden Werten liegen 50 % aller Autos?

*Tipp: Bewegen Sie die Maus über die Box, um die genauen Werte zu sehen.*
```

```{code-cell}
# Hier Ihr Code
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
diagramm = px.box(preise)
diagramm.show()
```

Antworten:
1. Der Median liegt bei ca. 18.900 EUR
2. 50 % der Autos liegen zwischen Q1 (ca. 15.200 EUR) und Q3 (ca. 25.200 EUR)
````

Das folgende Video erklärt, wie der Boxplot zu interpretieren ist.

```{dropdown} Video zu "Boxplot" von Datatab
<iframe width="560" height="315" src="https://www.youtube.com/embed/1I_ma7nvKQw" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
allowfullscreen></iframe>
```

## Beschriftung des Boxplots verändern

Die Achsenbeschriftungen wurden automatisch gesetzt. Die x-Achse ist mit
'variable' und die y-Achse mit 'value' beschriftet. Darüber hinaus ist der Titel
der Box '0'. Der Name wird auch angezeigt, wenn wir die Maus über die Box
bewegen.

Die 0 erscheint, weil Pandas intern 0 als Standardnamen verwendet, wenn kein
Name angegeben wurde. Wir können der Spalte aber auch einen eigenen Namen geben.
Am einfachsten funktioniert das direkt bei der Erzeugung, indem der Parameter
`name=` gesetzt wird.

```{code-cell}
preise_mit_name = pd.Series(preisliste, index=[
  'Audi Nr. 1', 'Audi Nr. 2', 'Audi Nr. 3',
  'BMW Nr. 1', 'BMW Nr. 2', 
  'Citroen Nr. 1', 'Citroen Nr. 2', 'Citroen Nr. 3', 'Citroen Nr. 4', 'Citroen Nr. 5'
  ],
  name='Liste von Autoscout24')

print(preise_mit_name)
```

Der neue Name 'Liste von Autoscout24' wird zusätzlich zur Information
'dtype' angezeigt. Erstellen wir nun den Boxplot mit diesem benannten
Series-Objekt:

```{code-cell}
diagramm = px.box(preise_mit_name)
diagramm.show()
```

Sollen nun auch noch die Achsenbeschriftungen geändert werden, müssen wir die
automatisch gesetzten Beschriftungen durch neue Namen ersetzt werden. Dazu wird
ein Dictionary konfiguriert und dem optionalen Argument `labels=` übergeben. Das
Dictionary wird mit geschweiften Klammern erzeugt. Die Schlüssel vor dem
Doppelpunkt sind die alten Beschriftungen, die Werte nach dem Doppelpunkt die
neuen.

Da wir weiterhin den Variablennamen `diagramm` nutzen, wird das Diagramm aus der
vorherigen Code-Zelle überschrieben.

```{code-cell}
diagramm = px.box(preise_mit_name,
                  labels={'variable': 'Name des Datensatzes', 'value': 'Verkaufspreis [EUR]'})
diagramm.show()
```

Fehlt noch eine Überschrift, ein Titel. Wie das englische Wort 'title' heißt
auch das entsprechende Schlüsselwort zum Erzeugen eines Titels, nämlich
`title=`.

```{code-cell}
diagramm = px.box(preise_mit_name,
                  labels={'variable': 'Name des Datensatzes', 'value': 'Verkaufspreis [EUR]'},
                  title='Statistische Kennzahlen als Boxplot')
diagramm.show()
```

## Datenpunkte im Boxplot anzeigen

Oft ist es wünschenswert die Rohdaten zusammen mit dem Boxplot zu visualisieren.
Das ist mit dem `points=`-Parameter recht einfach, jedoch haben wir zwei mögliche
Optionen. Wir können mit `'all'` alle Punkte anzeigen lassen oder nur die
Ausreißer (`'outliers'`).

Lassen wir zuerst alle Punkte anzeigen und setzen also `points='all'`.

```{code-cell}
diagramm = px.box(preise_mit_name,
                  labels={'variable': 'Name des Datensatzes', 'value': 'Verkaufspreis [EUR]'},
                  points='all')
diagramm.show()
```

Die Punkte werden links vom Boxplot platziert. Als nächstes lassen wir uns die
Ausreißer anzeigen.

```{code-cell}
diagramm = px.box(preise_mit_name,
                  labels={'variable': 'Name des Datensatzes', 'value': 'Verkaufspreis [EUR]'},
                  points='outliers')
diagramm.show()
```

Es sind keine Punkte zu sehen, was ist falsch? Nun, um das zu klären, müssen wir
erst einmal definieren, was ein Ausreißer ist.

## Ausreißer berechnen und visualisieren

Die Box im Boxplot enthält 50 % aller Datenpunkte, denn sie ist durch das untere
Quartil Q1 und das obere Quartil Q3 begrenzt. Die Differenz zwischen Q1 und Q3,
also IQR = Q3 - Q1, wird **Interquartilsabstand** (manchmal auch kurz
Quartilsabstand) genannt und mit **IQR** (englisch für Interquartile Range)
abgekürzt. In der Statistik werden Punkte als Ausreißer angesehen, die kleiner
als Q1 - 1.5 IQR oder größer als Q3 + 1.5 IQR sind. Dabei ist die Wahl des
Faktors 1.5 eine statistische Konvention, die sich in der Praxis bewährt hat.

In unserem Beispiel mit den Autopreisen kommen keine Ausreißer vor, weil Minimum
und Maximum noch innerhalb dieses Bereichs liegen. Wir fügen daher noch ein
neues, teureres Auto ein. Jetzt sehen wir einen Ausreißer.

```{code-cell}
preise_mit_name['BMW Nr. 3'] = 62999
diagramm = px.box(preise_mit_name, 
              labels={'variable': 'Name des Datensatzes', 'value': 'Verkaufspreis [EUR]'},
              points='outliers')
diagramm.show()
```

Wir beenden dieses Kapitel mit einer Mini-Übung.

```{admonition} Mini-Übung
:class: tip
Erstellen Sie einen Boxplot mit folgenden Eigenschaften:
1. Benennen Sie das Series-Objekt mit dem Namen "Gebrauchtwagen"
2. Beschriften Sie die y-Achse mit "Preis [EUR]"
3. Fügen Sie den Titel "Gebrauchtwagen-Analyse" hinzu
4. Zeigen Sie alle Datenpunkte an

*Zusatzfrage:* Welche Autos liegen preislich am weitesten auseinander?
```

```{code-cell}
# Hier Ihr Code
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
preise_benannt = pd.Series(preisliste, 
                           index=['Audi Nr. 1', 'Audi Nr. 2', 'Audi Nr. 3',
                                  'BMW Nr. 1', 'BMW Nr. 2', 
                                  'Citroen Nr. 1', 'Citroen Nr. 2', 'Citroen Nr. 3',
                                  'Citroen Nr. 4', 'Citroen Nr. 5'],
                           name='Gebrauchtwagen')

diagramm = px.box(preise_benannt,
                  labels={'value': 'Preis [EUR]'},
                  title='Gebrauchtwagen-Analyse',
                  points='all')
diagramm.show()
```

Zusatzfrage: Audi Nr. 1 (1.999 EUR, günstigstes) und BMW Nr. 1 (46.830 EUR,
teuerstes) liegen am weitesten auseinander.
````

## Zusammenfassung und Ausblick

Der Boxplot ermöglicht eine einfache Visualisierung der wichtigsten
statistischen Kennzahlen eines Datensatzes. Seine Stärke zeigt sich besonders,
sobald mehrere Datensätze miteinander verglichen werden sollen. Daher werden wir
im nächsten Kapitel uns mit Tabellen beschäftigen.
