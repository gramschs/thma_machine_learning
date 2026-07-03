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

# 3.2 Statistik mit Pandas

Pandas dient nicht nur dazu, Daten zu sammeln, sondern ermöglicht auch
statistische Analysen. Die deskriptive Statistik hat zum Ziel, Daten durch
einfache Kennzahlen und Diagramme zu beschreiben. In diesem Kapitel geht es
darum, die wichtigsten statistischen Kennzahlen mit Pandas zu ermitteln und zu
interpretieren.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können sich mit **.describe()** eine Übersicht über statistische Kennzahlen
  verschaffen.
* Sie wissen, wie Sie die Anzahl der gültigen Einträge mit **.count()** ermitteln.
* Sie kennen die statistischen Kennzahlen Mittelwert und Standardabweichung und
  wissen, wie diese mit **.mean()** und **.std()** berechnet werden.
* Sie können das Minimum und das Maximum mit **.min()** und **.max()** bestimmen.
* Sie wissen, wie ein Quantil interpretiert wird und wie es mit **.quantile()**
  berechnet wird.
```

## Schnelle Übersicht mit .describe()

Die Methode `.describe()` aus dem Pandas-Modul liefert eine schnelle Übersicht
über viele statistische Kennzahlen. Vor allem, wenn neue Daten geladen werden,
sollte diese Methode direkt am Anfang angewendet werden. Wir bleiben bei unserem
Beispiel mit den zehn Autos und deren Verkaufspreisen.

```{code-cell}
# Import des Pandas-Moduls 
import pandas as pd

# Erzeugung der Daten als Series-Objekt
preisliste = [1999, 35990, 17850, 46830, 27443, 14240, 19950, 15950, 21990, 12450]
autos = ['Audi Nr. 1', 'Audi Nr. 2', 'Audi Nr. 3', 'BMW Nr. 1', 'BMW Nr. 2', 'Citroen Nr. 1', 'Citroen Nr. 2', 'Citroen Nr. 3', 'Citroen Nr. 4', 'Citroen Nr. 5']
preise = pd.Series(preisliste, index = autos)
```

Die Anwendung der `.describe()`-Methode liefert folgende Ausgabe:

```{code-cell}
preise.describe()
```

Die Methode `.describe()` liefert acht statistische Kennzahlen, deren Bedeutung
in der
[Pandas-Dokumentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.describe.html)
erläutert wird. Wir gehen im Folgenden jede Kennzahl einzeln durch.

Was machen wir aber, wenn wir die statistischen Kennzahlen erst später verwenden
wollen? Können wir sie zwischenspeichern? Probieren wir es aus.

```{code-cell}
statistische_kennzahlen = preise.describe()
```

Es kommt keine Fehlermeldung. Und was ist in der Variable
`statistische_kennzahlen` nun genau gespeichert, welcher Datentyp?

```{code-cell}
type(statistische_kennzahlen)
```

Wie wir sehen wird durch das Anwenden der `.describe()`-Methode auf das
Series-Objekt `preise` ein neues Series-Objekt erzeugt, in dem wiederum die
statistischen Kennzahlen von `preise` gespeichert sind. Da wir im letzten
Kapitel schon gelernt haben, dass mit eckigen Klammern und dem Index auf einen
einzelnen Wert zugegriffen werden kann, können wir uns so den minimalen
Verkaufspreis ausgeben lassen:

```{code-cell}
minimaler_preis = statistische_kennzahlen['min']
print(f'Das billigste Auto wird für {minimaler_preis} EUR angeboten.')
```

```{admonition} Mini-Übung
:class: tip
Lassen Sie die Verkaufspreise aufsteigend sortieren und ausgeben. Welches Auto
ist am teuersten und für wie viel EUR wird es angeboten?

Ermitteln Sie dann das Maximum mit `.describe()` und vergleichen Sie beide Werte.

*Zusatzfrage:* Die Spanne (Maximum - Minimum) ist über 44.000 EUR groß. Wie
groß ist die Standardabweichung im Vergleich zur Spanne? Was bedeutet das für
die Streuung der Daten?
```

```{code-cell}
# Hier Ihr Code
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Sortierung und Ausgabe
preise_aufsteigend = preise.sort_values()
print('Preise aufsteigend sortiert: ')
print(preise_aufsteigend)

# Maximum ermitteln
statistische_kennzahlen = preise.describe()
maximaler_preis = statistische_kennzahlen['max']
print(f'\nMaximaler Preis mit .describe() ermittelt: {maximaler_preis}')

# Zusatzfrage: Spanne und Standardabweichung
spanne = statistische_kennzahlen['max'] - statistische_kennzahlen['min']
standardabweichung = statistische_kennzahlen['std']
print(f'\nSpanne: {spanne:.2f} EUR')
print(f'Standardabweichung: {standardabweichung:.2f} EUR')
print(f'Die Standardabweichung beträgt ca. {standardabweichung/spanne:.1%} der Spanne.')
```

Interpretation: Das teuerste Auto ist BMW Nr. 1 für 46830 EUR. Die Standardabweichung 
(~13.000 EUR) ist etwa 29 % der Spanne (~44.800 EUR), was auf eine starke, aber nicht 
extreme Streuung hindeutet.
````

Neben der Möglichkeit, die statistischen Kennzahlen über .describe() berechnen
zu lassen und dann mit dem expliziten Index darauf zuzugreifen, gibt es auch
Methoden, um die statistischen Kennzahlen direkt zu ermitteln.

## Anzahl count()

Mit `.count()` wird die Anzahl der Einträge bestimmt, die *nicht* 'NA' sind. Der
Begriff 'NA' ist ein Fachbegriff der Datenanalyse. Gemeint sind fehlende
Einträge, wobei die fehlenden Einträge verschiedene Ursachen haben können:

* NA = not available (der Messsensor hat versagt)
* NA = not applicable (es ist sinnlos bei einem Mann nachzufragen, ob er
  schwanger ist)
* NA = no answer (eine Person hat bei der Umfrage nichts angegeben)

```{code-cell}
anzahl_gueltige_preise = preise.count()
print(f'Im Series-Objekt sind {anzahl_gueltige_preise} nicht NA-Werte, also gültige Datensätze gespeichert.')
```

## Mittelwert mean()

Der Mittelwert ist die Summe aller Elemente geteilt durch ihre Anzahl. Wie
praktisch, dass wir mit .count() schon die Anzahl der gültigen Werte geliefert
bekommen. Rechnen wir zuerst einmal "händisch" nach, was der durchschnittliche
Verkaufspreis der 10 Autos ist.

```{code-cell}
preisliste = [1999, 35990, 17850, 46830, 27443, 14240, 19950, 15950, 21990, 12450]
summe = 1999 + 35990 + 17850 + 46830 + 27443 + 14240 + 19950 + 15950 + 21990 + 12450
print(f'Die Summe ist {summe} EUR.')
mittelwert = summe / 10
print(f'Der durchschnittliche Verkaufspreis ist {mittelwert} EUR.')
```

Mittelwert heißt auf Englisch mean. Daher ist es nicht verwunderlich, dass die
Methode `.mean()` den Mittelwert der Einträge in jeder Spalte berechnet.

```{code-cell}
mittelwert = preise.mean()
print(f'Der mittlere Verkaufspreis beträgt {mittelwert} EUR.')
```

Das folgende Video wiederholt das Konzept des Mittelwerts.

```{dropdown} Video zu "Mittelwert" von Datatab
<iframe width="560" height="315" src="https://www.youtube.com/embed/IKfsGPwACnU" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

## Standardabweichung std()

Der Mittelwert ist wichtig, aber er erzählt nicht die ganze Geschichte. Betrachten wir unsere Autopreise:

```{code-cell}
mittelwert = preise.mean()
print(f'Durchschnittspreis: {mittelwert:.2f} EUR')
print('\nAber schauen wir genauer hin:')
print(f'Günstigstes Auto: {preise.min():.2f} EUR')
print(f'Teuerstes Auto: {preise.max():.2f} EUR')
print(f'Spanne: {preise.max() - preise.min():.2f} EUR')
```

Die Spanne von über 44.000 EUR zeigt: Diese Autos sind sehr unterschiedlich! Die **Standardabweichung** beschreibt diese Streuung in einer einzigen Zahl:

```{code-cell}
standardabweichung = preise.std()
print(f'Standardabweichung: {standardabweichung:.2f} EUR')
```

Was bedeutet das konkret? Eine Standardabweichung von 13.000 EUR bei einem
Mittelwert von 21.500 EUR bedeutet: Die Preise schwanken stark. Wenn wir ein
"durchschnittliches" Auto für 21.500 EUR erwarten, müssen wir mit Abweichungen
von ±13.000 EUR rechnen.

Schauen wir uns das an unseren konkreten Daten an:

* Mittelwert ± Standardabweichung = 21.469 ± 13.000 EUR
* Das ergibt den Bereich: [8.469 EUR, 34.469 EUR]
* Tatsächlich liegen 7 von 10 Autos in diesem Bereich

Die Standardabweichung hat dieselbe Einheit wie die Originaldaten (hier: EUR).
Das macht sie direkt interpretierbar im Gegensatz zur Varianz, die in EUR²
gemessen wird.

```{dropdown} Video zu "Standardabweichung" von Datatab
<iframe width="560" height="315" src="https://www.youtube.com/embed/QNNt7BvmUJM" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

## Minimum und Maximum mit min() und max()

Die Namen der Methoden `.min()` und `max()` sind fast schon wieder
selbsterklärend. Die Methode `.min()` liefert den kleinsten Wert zurück, der
gefunden wird. Umgekehrt liefert `.max()` den größten Eintrag. Wie häufig die
minimalen und maximalen Werte vorkommen, ist dabei egal. Es kann durchaus sein,
dass das Minimum oder das Maximum mehrfach vorkommt.

Schauen wir uns an, was der niedrigste Verkaufspreis ist. Und dann schauen wir
nach, welches Auto am teuersten ist.

```{code-cell}
preis_min = preise.min()
print(f'Das billigste oder die billigsten Autos werden zum Preis von {preis_min} EUR angeboten.')

preis_max = preise.max()
print(f'Das teuerste oder die teuersten Autos werden für {preis_max} EUR angeboten.')
```

## Quantil mit quantile()

Das Quantil $p\%$ ist der Wert, bei dem $p\%$ der Einträge kleiner oder gleich
diesem Wert sind und $100\% - p\%$ sind größer. Meist werden nicht Prozentzahlen
verwendet, sondern p ist zwischen 0 und 1, wobei die 1 für 100 % steht.

Angenommen, wir würden gerne das 0.5-Quantil (auch Median genannt) der Preise
wissen. Mit der Methode `.quantile()` können wir diesen Wert leicht aus den
Daten holen.

```{code-cell}
quantil50 = preise.quantile(0.5)
print(f'Der Median, d.h. das 50 % Quantil, liegt bei {quantil50} EUR.')
```

Das 50 % -Quantil liegt bei 18900 EUR. 50 % aller Autos werden zu einem Preis
angeboten, der kleiner oder gleich 18900 EUR ist. Und 50 % aller Autos werden
teurer angeboten. Wir schauen uns jetzt das 75 % Quantil an.

```{code-cell}
quantil75 = preise.quantile(0.75)
print(f'75 % aller Autos haben einen Preis kleiner gleich {quantil75} EUR.')
```

75 % aller Autos werden günstiger als 26079.75 EUR angeboten. Wir können uns für
jeden beliebigen Prozentsatz zwischen 0 % und 100 % das Quantil ansehen, aber
häufig wird neben dem 75 % Quantil, dem 50 % Quantil noch das 25 % Quantil
betrachtet.

```{code-cell}
quantil25 = preise.quantile(0.25)
print(f'25 % aller Autos haben einen Preis kleiner gleich {quantil25} EUR.')
```

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir uns mit einfachen statistischen Kennzahlen
beschäftigt, die Pandas mit der Methode `.describe()` zusammenfasst, die aber
auch einzeln über

* `.count()`
* `.mean()`
* `.std()`
* `.min()` und `.max()`
* `.quantile()`

berechnet und ausgegeben werden können. Im nächsten Kapitel geht es darum, durch
Diagramme mehr über die Daten zu erfahren.
