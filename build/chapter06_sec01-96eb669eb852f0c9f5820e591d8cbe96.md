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

# 6.1 Was ist ein Entscheidungsbaum?

Ein beliebtes Partyspiel ist das Spiel "Wer bin ich?". Die Spielregeln sind
simpel. Eine Person wählt eine berühmte Person oder eine Figur aus einem Film
oder Buch, die die Mitspieler:innen erraten müssen. Die Mitspieler:innen
dürfen jedoch nur Fragen stellen, die mit "Ja" oder "Nein" beantwortet werden.

Hier ist ein Beispiel, wie eine typische Runde von "Wer bin ich?" ablaufen
könnte:

* Spieler 1: Bin ich männlich?
* Spieler 2: Ja.
* Spieler 3: Bist du ein Schauspieler?
* Spieler 1: Nein.
* Spieler 4: Bist du ein Musiker?
* Spieler 1: Ja.
* Spieler 5: Bist du Michael Jackson?
* Spieler 1: Ja! Richtig!

Als nächstes wäre jetzt Spieler 5 an der Reihe, sich eine Person oder Figur
auszuwählen, die die anderen Spieler erraten sollen. Vielleicht kennen Sie auch
die umgekehrte Variante. Der Name der zu ratenden Person/Figur wird der Person
mit einem Zettel auf die Stirn geklebt. Und nun muss die Person raten, während
die Mitspieler:innen mit Ja/Nein antworten.

Dieser Partyklassiker lässt sich auch auf das maschinelle Lernen übertragen.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie wissen, was ein **Entscheidungsbaum (Decision Tree)** ist.
* Sie kennen die Bestandteile eines Entscheidungsbaumes:
  * Wurzelknoten (Root Node)
  * Knoten (Node)
  * Zweig oder Kante (Branch)
  * Blatt (Leaf)
* Sie können einen Entscheidungsbaum mit Scikit-Learn trainieren.
* Sie können mit Hilfe eines Entscheidungsbaumes Prognosen treffen.
```

## Ein Entscheidungsbaum im Autohaus

Ein **Entscheidungsbaum** gehört zu den überwachten Lernverfahren (Supervised
Learning). Es ist auch üblich, die englische Bezeichnung **Decision Tree**
anstatt des deutschen Begriffes zu nutzen. Ein großer Vorteil von
Entscheidungsbäumen ist ihre Flexibilität, denn sie können sowohl für
Klassifikations- als auch Regressionsaufgaben eingesetzt werden. Im Folgenden
betrachten wir als Beispiel eine Klassifikationsaufgabe. In einem Autohaus
vereinbaren zehn Personen eine Probefahrt. In der folgenden Tabelle ist für
jedes Auto notiert, welchen

* `Kilometerstand [in km]` und
* `Preis [in EUR]`

es hat. In der dritten Spalte `verkauft` ist vermerkt, ob das Auto nach der
Probefahrt verkauft wurde (`True`) oder nicht (`False`). Diese Information ist
die Zielgröße. Die Tabelle mit den Daten lässt sich effizient mit einem
Pandas-DataFrame organisieren:

```{code-cell}
import pandas as pd 

daten = pd.DataFrame({
      'Kilometerstand [km]': [32908, 20328, 13285, 17162, 27449, 13715, 32889,  3111, 15607, 18295],
      'Preis [EUR]': [15960, 20495, 17227, 17851, 5428, 22772, 13581, 16793, 23253, 11382],
      'verkauft': [False, True, False, True, False, True, False, True, True, False],
    },
    index=['Auto 1', 'Auto 2', 'Auto 3', 'Auto 4', 'Auto 5', 'Auto 6', 'Auto 7', 'Auto 8', 'Auto 9', 'Auto 10'])
daten.head(10)
```

Da in unserem Beispiel von den Autos nur die beiden Eigenschaften
`Kilometerstand [km]` und `Preis [EUR]` erfasst wurden, können wir die
Datenpunkte anschaulich in einem zweidimensionalen Streudiagramm (Scatterplot)
visualisieren. Dabei wird der Kilometerstand auf der x-Achse und der Preis auf
der y-Achse abgetragen. Die Zielgröße `verkauft` kennzeichnen wir durch die
Farbe. Dabei steht die Farbe Rot für »verkauft« (True) und Blau für »nicht
verkauft« (False).

```{code-cell}
import plotly.express as px

fig = px.scatter(daten, x='Kilometerstand [km]', y='Preis [EUR]', 
                 color='verkauft', title='Künstliche Daten: Verkaufsaktion im Autohaus')
fig.show()
```

Als nächstes zeigen wir, wie die Autos anhand von Fragen in die beiden Klassen
»verkauft« und »nicht verkauft« sortiert werden können. Im Streudiagramm
visualisieren wir die Autos mit ihren Eigenschaften `Kilometerstand [km]` und
`Preis [EUR]` als Punkte. Dazu passend werden wir schrittweise den
Entscheidungsbaum entwickeln. Ein Entscheidungsbaum visualisiert
Entscheidungsregeln in Form einer Baumstruktur. Zu Beginn wurde noch keine Frage
gestellt und alle Autos befinden sich gemeinsam in einem **Knoten** (Node) des
Entscheidungsbaumes, der visuell durch einen rechteckigen Kasten symbolisiert
wird. Dieser erste Knoten wird als **Wurzelknoten** (Root Node) bezeichnet, da
er die Wurzel des Entscheidungsbaumes darstellt.

![Entscheidungsbaum - Start](pics/combined_decisiontree00.svg)

![Entscheidungsbaum - Start](pics/scatterplot00.svg)

![Entscheidungsbaum - Start](pics/decisiontree_cars00.svg)

Dann wird eine erste Frage gestellt. *Ist der Verkaufspreis kleiner oder gleich
16376.50 EUR?* Entsprechend dieser Entscheidung werden die Autos in zwei Gruppen
aufgeteilt. Wenn ja, wandern die Autos nach links und ansonsten nach rechts.
Warum wir die Grenze 16376.50 gewählt haben, werden wir in einem späteren
Kapitel besprechen. Im Entscheidungsbaum wird diese Aufteilung durch einen
**Zweig** (Branch) nach links und einen Zweig nach rechts symbolisiert. Ein
alternativer Name für Zweig ist **Kante**. Die Autos »rutschen« die
Zweige/Kanten entlang und landen in zwei separaten Knoten. Im Streudiagramm
(Scatterplot) entspricht diese Fragestellung dem Vergleich mit einer
horizontalen Linie bei y = 16376.5. Da alle Autos mit einem Verkaufspreis
kleiner/gleich 16376.5 EUR blau sind, also »nicht verkauft« wurden, wird im
Streudiagramm (Scatterplot) alles unterhalb der horizontalen Linie blau
eingefärbt.

![Entscheidungsbaum - 1. Entscheidung](pics/combined_decisiontree01.svg)

![Entscheidungsbaum - 1. Entscheidung](pics/scatterplot01.svg)

![Entscheidungsbaum - 1. Entscheidung](pics/decisiontree_cars01.svg)

Bei den Autos mit einem Preis kleiner oder gleich 16376.50 EUR müssen wir nicht
weiter sortieren bzw. weitere Fragen stellen. Da aus diesem Knoten keine Zweige
mehr wachsen, wird dieser Knoten auch **Blatt** (Leaf) genannt. Aber in dem
Knoten des rechten Zweiges befinden sich fünf rote (also verkaufte) Autos und
ein blaues (also nicht verkauftes) Auto. Wir wollen diese Autos durch weitere
Fragen sortieren. Doch obwohl nur ein Auto (nämlich Auto 3) aus dieser Gruppe
separiert werden soll, ist dies nicht durch nur eine einzige Frage möglich.
Lautet die Frage: »Ist der Preis kleiner oder gleich 17300 EUR?«, dann wandern
das rote Auto 8 und das blaue Auto 3 nach links. Wählen wir die Frage: »Ist der
Kilometerstand kleiner oder gleich 13500 km?«, dann wandern ebenfalls Auto 3 und
Auto 8 nach links. Beide Fragen sind also gleichwertig, welche sollen wir
nehmen? In diesem vereinfachten Beispiel wählen wir willkürlich den
Kilometerstand. Der Algorithmus brauchte jedoch Kriterien, um die beste Trennung
zu finden. Darauf gehen wir im nächsten Kapitel ein.

![Entscheidungsbaum - 2. Entscheidung](pics/combined_decisiontree02.svg)

![Entscheidungsbaum - 2. Entscheidung](pics/scatterplot02.svg)

![Entscheidungsbaum - 2. Entscheidung](pics/decisiontree_cars02.svg)

Im Streudiagramm (Scatterplot) wird die noch nicht eingefärbte Fläche rechts der
vertikalen Linie 13500 km rot gefärbt. Im linken Knoten (Node) sind aber nur
noch zwei Autos, so dass diesmal eine weitere Frage ausreicht, die beiden Autos
in zwei Klassen zu sortieren. Wir fragen: *»Ist der Kilometerstand kleiner oder
gleich 8198 km?«*

![Entscheidungsbaum - 3. Entscheidung](pics/combined_decisiontree03.svg)

![Entscheidungsbaum - 3. Entscheidung](pics/scatterplot03.svg)

![Entscheidungsbaum - 3. Entscheidung](pics/decisiontree_cars03.svg)

Alle Autos sind nun durch die Fragen sortiert und befinden sich in Blättern
(Leaves). Im Streudiagramm (Scatterplot) wird dieser Zustand kenntlich gemacht,
indem auch die letzte verbleibende Fläche (oberhalb eines Preises von 16376.50
EUR) links von Kilometerstand 8198 km rot und rechts davon blau eingefärbt wird.

```{admonition} Was ist ... ein Entscheidungsbaum?
:class: note
Ein Entscheidungsbaum (Decision Tree) ist ein Modell zur Entscheidungsfindung,
das Daten mit Hilfe einer Baumstruktur sortiert. Die Datenobjekte beginnen beim
Wurzelknoten (= Ausgangssituation) und werden dann über Knoten (=
Entscheidungsfrage) und Zweige/Kanten (= Ergebnis der Entscheidung) in Blätter
(= Endzustand des Entscheidungsprozesses) sortiert.
```

```{dropdown} Video "Decision Tree Classification Clearly Explained!" von Normalized Nerd
<iframe width="560" height="315" src="https://www.youtube.com/embed/ZVR2Way4nwQ?si=7_of_wa6nrzWIU8g" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "Maschinelles Lernen - Beispiel Entscheidungsbaum"
<iframe width="560" height="315" src="https://www.youtube.com/embed/F9ArN1JIhCY?si=bG0rauYn2XdukIzI" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video zu "Entscheidungsbäume #1" von The Morpheus Tutorials
<iframe width="560" height="315" src="https://www.youtube.com/embed/-YW5s_an4z8?si=PYX24rwrWlYhF9EL" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## Entscheidungsbäume mit Scikit-Learn trainieren

In der Praxis verwenden wir die ML-Bibliothek Scikit-Learn, um einen
Entscheidungsbaum zu trainieren. Das Modul [Scikit-Learn →
Tree](https://scikit-learn.org/stable/modules/tree.html) stellt sowohl einen
Entscheidungsbaum-Algorithmus für Klassifikationsprobleme als auch einen
Algorithmus für Regressionsprobleme zur Verfügung. Für das obige Beispiel
Autohaus importieren wir den Algorithmus für Klassifikationsprobleme namens
`DecisionTreeClassifier`:

```{code-cell}
from sklearn.tree import DecisionTreeClassifier
```

Dann erzeugen wir ein noch untrainiertes Entscheidungsbaum-Modell und weisen es
der Variable `modell` zu:

```{code-cell}
modell = DecisionTreeClassifier()
```

Bei der Erzeugung könnten wir noch verschiedene Optionen einstellen, die in der
[Dokumentation Scikit-Learn →
DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier)
nachgelesen werden können. Zunächst belassen wir es aber bei den
Standardeinstellungen.

Als nächstes adaptieren wir die Daten aus dem Pandas-DataFrame so, dass das
Entscheidungsbaum-Modell trainiert werden kann. Der `DecisionTreeClassifier`
erwartet für das Training zwei Argumente. Als erstes Argument müssen die
Eingabedaten übergeben werden, also die Eigenschaften der Autos. Als zweites
Argument erwartet der `DecisionTreeClassifier` die Zielgröße, also den Status
»nicht verkauft« oder »verkauft«. Wir trennen daher den Pandas-DataFrame `daten`
auf und verwenden die Bezeichnung `X` für die Eingabedaten und `y` für die
Zielgröße.

```{code-cell}
X = daten[['Kilometerstand [km]', 'Preis [EUR]']]
y = daten['verkauft']
```

Als nächstes wird der Entscheidungsbaum trainiert. Dazu wird die Methode
`.fit()` mit den beiden Argumenten `X` und `y` aufgerufen.

```{code-cell}
modell.fit(X,y)
```

Jetzt ist zwar der Entscheidungsbaum trainiert, doch wir sehen nichts. Als
erstes überprüfen wir mit der Methode `.score()`, wie gut die Prognose des
Entscheidungsbaumes ist.

```{code-cell}
score = modell.score(X,y)
print(score)
```

Eine 1 steht für 100 %, also alle 10 Autos werden korrekt klassifiziert. Dazu
hat der `DecisionTreeClassifier` basierend auf den Eingabedaten `X` eine
Prognose erstellt und diese Prognose mit den echten Daten in `y` verglichen. Für
die Trainingsdaten funktioniert der Entscheidungsbaum also perfekt. Ob der
Entscheidungsbaum ein neues, elftes Auto korrekt klassifizieren würde, kann so
erst einmal nicht entschieden werden. Möglicherweise hat der Entscheidungsbaum
die Trainingsdaten auswendig gelernt, anstatt allgemeine Muster zu erkennen. Es
besteht die Gefahr des sogenannten Overfittings, auf die wir im übernächsten
Kapitel noch eingehen werden.

## Prognosen mit Entscheidungsbäumen treffen

Soll für neue Autos eine Prognose abgegeben werden, ob sie sich eher verkaufen
lassen oder nicht, müssen die neuen Daten die gleiche Struktur wie die
Eingangsdaten haben. Wir erzeugen daher einen neuen Pandas-DataFrame, bei dem
die erste Eigenschaft der Kilometerstand der neuen Autos ist und die zweite
Eigenschaft ihr Preis.

```{code-cell}
neue_autos = pd.DataFrame({
    'Kilometerstand [km]': [11300, 20000, 7580],
    'Preis [EUR]': [12000, 14999, 20999]
    },
    index=['Auto 11', 'Auto 12', 'Auto 13']) 
```

Mit Hilfe der `predict()`-Methode kann dann der Entscheidungsbaum
prognostizieren, ob die Autos verkauft werden oder nicht.

```{code-cell}
prognose = modell.predict(neue_autos)
print(prognose)
```

Um für ein neues Auto eine Prognose abzugeben, werden zunächst den Blättern
Klassen zugeordnet. Dazu wird die sogenannte Reinheit der Blätter untersucht.
Befinden sich nur Autos einer einzigen Klasse in einem Blatt, so nennen wir das
Blatt **rein** und es bekommt diese Klasse zugeordnet. Ist ein Blatt nicht rein,
sondern enthält noch Autos mit unterschiedlichen Klassen »verkauft« oder »nicht
verkauft«, so wird diesem Blatt diejenige Klasse zugeordnet, die am häufigsten
auftritt. Um diese Idee zu visualisieren, färben wir im Entscheidungsbaum die
Blätter entsprechend rot und blau ein.

Jedes neue Auto durchläuft jetzt die Entscheidungen, bis es in einem Blatt
angekommen ist. Die Klasse des Blattes ist dann die Prognose für dieses Auto.

![Entscheidungsbaum - Prognose](pics/combined_decisiontree_prediction.svg)

![Entscheidungsbaum - Prognose](pics/scatterplot_prediction.svg)

![Entscheidungsbaum - Prognose](pics/decisiontree_cars_prediction.svg)

Der Entscheidungsbaum prognostiziert, dass Auto 11 und Auto 12 nicht verkauft
werden, aber Auto 13 könnte verkaufbar sein.

````{admonition} Mini-Übung
:class: tip
Trainieren Sie einen Entscheidungsbaum für die folgenden Daten:

```python
test_daten = pd.DataFrame({
    'Kilometerstand [km]': [5000, 25000, 15000, 30000],
    'Preis [EUR]': [18000, 14000, 19000, 12000],
    'verkauft': [True, False, True, False]
})
```

Geben Sie eine Prognose für ein Auto mit 10.000 km und 16.000 EUR ab.
````

```{code-cell}
# Hier Ihr Code
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
test_daten = pd.DataFrame({
    'Kilometerstand [km]': [5000, 25000, 15000, 30000],
    'Preis [EUR]': [18000, 14000, 19000, 12000],
    'verkauft': [True, False, True, False]
})

X_test = test_daten[['Kilometerstand [km]', 'Preis [EUR]']]
y_test = test_daten['verkauft']

modell_test = DecisionTreeClassifier()
modell_test.fit(X_test, y_test)

neues_auto = pd.DataFrame({
    'Kilometerstand [km]': [10000],
    'Preis [EUR]': [16000]
})

prognose = modell_test.predict(neues_auto)
print(f"Prognose für das neue Auto: {prognose[0]}")
```
````

## Zusammenfassung und Ausblick

In diesem Kapitel haben Sie den Entscheidungsbaum (Decision Tree) anhand einer
Klassifikationsaufgabe kennengelernt. Mit Hilfe von Scikit-Learn wurde ein
Entscheidungsbaum trainiert und dazu benutzt, eine Prognose für neue Daten
abzugeben. Im nächsten Kapitel werden wir uns damit beschäftigen, weitere
Einstellmöglichkeiten beim Training des Entscheidungsbaumes zu nutzen und
Entscheidungsbäume durch Scikit-Learn visualisieren zu lassen.
