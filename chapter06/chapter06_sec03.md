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

# 6.3 Entscheidungsbäume in der Praxis

Entscheidungsbäume bieten viele Vorteile, haben aber auch Nachteile, die wir in
diesem Kapitel diskutieren werden. Darüber hinaus lernen wir Methoden kennen,
um bei Entscheidungsbäumen diese Nachteile zu reduzieren.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können in eigenen Worten erklären, was **Overfitting** (deutsch:
  **Überanpassung**) ist.
* Sie wissen, was **Underfitting** bedeutet.
* Sie wissen, dass Entscheidungsbäume eine Tendenz zu Overfitting haben und
  Maßnahmen zur Reduzierung von Overfitting ergriffen werden müssen.
* Sie wissen, was **Hyperparameter** sind.
* Sie kennen Hyperparameter der Entscheidungsbäume wie beispielsweise
    * maximale Baumtiefe,
    * minimale Anzahl an Datenpunkten in Knoten oder
    * minimale Anzahl an Datenpunkten in Blättern.
* Sie können die Hyperparameter zum **Prä-Pruning** (deutsch: vorab
  Zurechtschneiden) geeignet wählen.
```

## Die Tendenz von Entscheidungsbäumen zum Overfitting

Entscheidungsbaummodelle bieten zahlreiche Vorteile. Ein wesentlicher Vorzug ist
die Möglichkeit, den trainierten Entscheidungsbaum zu visualisieren, wodurch es
leicht nachvollziehbar wird, welche Merkmale einen signifikanten Einfluss haben.
Ein weiterer Vorteil ist ihre Effizienz bei heterogenen Daten; sowohl numerische
als auch kategoriale Eigenschaften können problemlos verarbeitet werden.
Entscheidungsbäume sind selbst bei unterschiedlichen Datenskalen robust und
erfordern nur wenig Vorverarbeitung.

Trotz dieser Stärken besitzen Entscheidungsbäume eine Neigung zum
**Overfitting**. Overfitting, auch als Überanpassung bekannt, beschreibt ein
Problem im maschinellen Lernen, bei dem ein Modell die Trainingsdaten zu genau
lernt. Das klingt zunächst gut, aber das Modell kann dadurch seine Fähigkeit
verlieren, Vorhersagen für neue, unbekannte Daten zu treffen. Im Gegensatz dazu
steht das **Underfitting**, das eine zu geringe Anpassung an die Daten bedeutet
und ebenfalls unerwünscht ist.

Um uns das Problem des Overfittings zu veranschaulichen, betrachten wir erneut
das Autohaus-Beispiel, aber diesmal mit mehr Autos. Wir lassen die Autos diesmal
mit einer in Scikit-Learn eingebauten Funktion zur Generierung von künstlichen
Daten erzeugen, der sogenannten `make_moons`-Funktion (siehe [Dokumentation
Scikit-Learn →
make_moons](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_moons.html))
aus dem Module `sklearn.datasets`.

```{code-cell}
from sklearn.datasets import make_moons 

X_array, y_array = make_moons(noise = 0.5, n_samples=50, random_state=3)
```

Damit die künstlichen Daten besser zu dem Autohaus-Beispiel passen,
transformieren wir sie und nutzen die Pandas-Datenstrukturen, um sie effizient
zu verwalten.

```{code-cell}
import numpy as np
import pandas as pd

# Transformation der Merkmalswerte in einen positiven Bereich und 
# Umwandlung in eine Integer-Matrix
X_array = X_array + 1.2 * np.abs(np.min(X_array))
X_array[:,0] = np.ceil(X_array[:,0] * 30000)
X_array[:,1] = np.ceil(X_array[:,1] * 10000)
X = pd.DataFrame(X_array, columns=['Kilometerstand [km]', 'Preis [EUR]'], dtype=(int, int))

# Zuweisung von True/False basierend auf den Kategorien 1 bzw. 0
y_array = (y_array - 1.0) * (-1)
y = pd.Series(y_array, name='verkauft', dtype='bool')
```

Nach der Datenvorbereitung visualisieren wir diese:

```{code-cell}
import plotly.express as px

fig = px.scatter(x = X['Kilometerstand [km]'], y = X['Preis [EUR]'], color=y,
    title='Künstliche Daten Autohaus',
    labels={'x': 'Kilometerstand [km]', 'y': 'Preis [EUR]', 'color': 'verkauft'})
fig.show()
```

Das Training des Entscheidungsbaumes und dessen Visualisierung erledigt der
folgende Code.

```{code-cell}
from sklearn.tree import DecisionTreeClassifier, plot_tree

modell = DecisionTreeClassifier(random_state=0)
modell.fit(X,y)

plot_tree(modell,
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    class_names=['nicht verkauft', 'verkauft']);
```

Die Visualisierung offenbart zahlreiche Verzweigungen und eine schwer lesbare
Beschriftung. Die Entscheidungsgrenzen, die im Folgenden mit
`DecisionBoundaryDisplay` visualisiert werden, zeigen eine zu starke Anpassung
an die Trainingsdaten.

```{code-cell}
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay

fig = DecisionBoundaryDisplay.from_estimator(modell, X, cmap=ListedColormap(['#EF553B33', '#636EFA33']), grid_resolution=1000)
fig.ax_.scatter(X['Kilometerstand [km]'], X['Preis [EUR]'], c=y, cmap=ListedColormap(['#EF553B', '#636EFA']))
fig.ax_.set_title('Entscheidungsgrenzen');
```

Es ist fraglich, ob dieser Entscheidungsbaum nicht zu genau an die
Trainingsdaten angepasst wurde. Der dünne blaue vertikale Streifen bei ungefähr
97000 km ist wahrscheinlich keine sinnvolle Entscheidung, sondern eher einem
Ausreißer geschuldet (dem Auto mit einem Kilometerstand von 97098 km und einem
Preis von 28229 EUR). Der Entscheidungsbaum hat sich zu stark an die Daten
angepasst. Es ist wahrscheinlich, dass dieser Entscheidungsbaum für Autos mit
einem Kilometerstand von ungefähr 97000 km falsche Prognosen treffen wird. Wenn
wir mit den gleichen Daten erneut einen Entscheidungsbaum trainieren lassen und
den Zufallszahlengenerator mit dem Zustand `random_state=1` initialisieren,
erhalten wir ein völlig anderes Ergebnis.

```{code-cell}
modell_alternative = DecisionTreeClassifier(random_state=1)
modell_alternative.fit(X,y)

fig = DecisionBoundaryDisplay.from_estimator(modell_alternative, X, cmap=ListedColormap(['#EF553B33', '#636EFA33']), grid_resolution=1000)
fig.ax_.scatter(X['Kilometerstand [km]'], X['Preis [EUR]'], c=y, cmap=ListedColormap(['#EF553B', '#636EFA']))
fig.ax_.set_title('Entscheidungsgrenzen des alternativen Modells');
```

Eine Möglichkeit, das Overfitting (Überanpassung) an die Daten zu bekämpfen, ist
das Zurechtschneiden (Pruning) der Entscheidungsbäume. Eine andere ist, aus
mehreren Entscheidungbäumen einen »durchschnittlichen« Entscheidungsbaum zu
bilden. Dieses Verfahren heißt Zufallswald (Random Forest) und wird ausführlich
in einem eigenen Kapitel behandelt werden. In diesem Kapitel betrachten wir nur
das Zurechtschneiden der Entscheidungsbäume.

## Zurechtschneiden von Entscheidungsbäumen

Eine effektive Strategie zur Bekämpfung des Overfittings bei Entscheidungsbäumen
ist das sogenannte **Pruning**, also das Beschneiden des Baumes. Pruning hilft,
die Komplexität des Modells zu reduzieren, indem weniger relevante
Entscheidungszweige nach bestimmten Kriterien entfernt werden. Im Kontext
unseres Autohaus-Beispiels würde dies bedeuten, dass Entscheidungszweige, die
beispielsweise aufgrund von Ausreißern entstanden sind, abgeschnitten werden.
Dies könnte beispielsweise den zuvor erwähnten dünnen blauen Streifen bei einem
Kilometerstand von ungefähr 97000 km betreffen, der wahrscheinlich durch einen
Ausreißer entstanden ist. Durch das Entfernen solcher spezifischen Anpassungen
kann der Entscheidungsbaum besser verallgemeinern und wird robuster gegenüber
neuen, unbekannten Daten. Das Ergebnis ist ein Modell, das eine bessere Balance
zwischen Anpassung an die Trainingsdaten und Generalisierungsfähigkeit aufweist.

Für Entscheidungsbäume gibt es prinzipiell zwei Methoden des Prunings:
**Prä-Pruning** und **Post-Pruning**. Das Prä-Pruning findet *vor* dem Training
des Entscheidungsbaumes statt, das Post-Pruning *nach* dem Training. Die beiden
wichtigsten Prä-Pruning-Maßnahmen sind

* die Begrenzung der maximalen Tiefe des Baumes und
* die Forderung nach einer Mindestanzahl von Datenpunkten (entweder pro Knoten
  oder pro Blatt).

Beim Post-Pruning werden im Nachhinein Knoten mit wenig Informationen aus dem
Entscheidungsbaum entfernt oder es werden Knoten zusammengelegt. Scikit-Learn
hat nur Prä-Pruning implementiert, so dass wir hier nicht weiter auf
Post-Pruning eingehen.

### Prä-Pruning: Baumtiefe

Wir schauen uns zunächst an, wie bei Scikit-Learn-Entscheidungsbäumen die
maximale Tiefe festgelegt wird. Bisher haben wir das Modell ohne weitere
Parameter initialisiert (einzige Ausnahme: wir haben ggf. den
Zufallszahlengenerator aus didaktischen Gründen fixiert, damit die Ergebnisse
vergleichbar sind). Nun verwenden wir bei der Initialisierung des
DecisionTreeClassifiers das optionale Argument `max_depth=` und setzen es auf
`1`.

```{code-cell}
modell_tiefe1 = DecisionTreeClassifier(random_state=0, max_depth=1)
modell_tiefe1.fit(X,y)

plot_tree(modell_tiefe1,
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    class_names=['nicht verkauft', 'verkauft']);
```

Eine Tiefe von 1 bedeutet, dass nur noch eine einzige Entscheidungsfrage
gestellt wird. Das reicht nicht mehr, um die Autos in reine Blätter zu
sortieren. Im linken Blatt sind 13 nicht verkaufte Autos und 24 verkaufte Autos,
weshalb diesem Blatt die Kategorie »verkauft« zugeordnet wird. Im rechten Blatt
sind 12 nicht verkaufte Autos und ein verkauftes Auto, so dass dieses Blatt
insgesamt als »nicht verkauft« gilt. Die Visualisierung der Entscheidungsgrenzen
zeigt, um welche Autos es sich handelt.

```{code-cell}
fig = DecisionBoundaryDisplay.from_estimator(modell_tiefe1, X, cmap=ListedColormap(['#EF553B33', '#636EFA33']), grid_resolution=1000)
fig.ax_.scatter(X['Kilometerstand [km]'], X['Preis [EUR]'], c=y, cmap=ListedColormap(['#EF553B', '#636EFA']))
fig.ax_.set_title('Entscheidungsgrenzen');
```

Insbesondere die Visualisierung der Entscheidungsgrenzen zeigt aber auch, dass
dieser Entscheidungsbaum nicht besonders gut die Daten erklärt. Der Score ist
mit

```{code-cell}
print(f'Score des Entscheidungsbaumes mit Tiefe 1: {modell_tiefe1.score(X,y)}')
```

auch nicht so gut. Daher verwenden wir nun als maximale Tiefe des Entscheidungsbaumes einen Wert von 2.

```{code-cell}
modell_tiefe2 = DecisionTreeClassifier(random_state=0, max_depth=2)
modell_tiefe2.fit(X,y)

plot_tree(modell_tiefe2,
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    class_names=['nicht verkauft', 'verkauft']);

print(f'Score des Entscheidungsbaumes mit Tiefe 2: {modell_tiefe2.score(X,y)}')
```

Mit einem Score von 0.78 ist der Entscheidungsbaum mit einer maximalen Tiefe von
2 zwar besser als der Baum mit einer maximalen Tiefe von 1, aber deutlich
entfernt von dem Score 1.0 bei einer Baumtiefe von 7. Die Entscheidungsgrenzen
sehen folgendermaßen aus:

```{code-cell}
fig = DecisionBoundaryDisplay.from_estimator(modell_tiefe2, X, cmap=ListedColormap(['#EF553B33', '#636EFA33']), grid_resolution=1000)
fig.ax_.scatter(X['Kilometerstand [km]'], X['Preis [EUR]'], c=y, cmap=ListedColormap(['#EF553B', '#636EFA']))
fig.ax_.set_title('Entscheidungsgrenzen');
```

Was ist jetzt besser, eine maximale Tiefe von 1 oder 2? Oder doch 3 vielleicht?
Die Einführung der maximalen Tiefe bietet den Vorteil, das Overfitting zu
bekämpfen. Der Nachteil davon ist, dass wir jetzt einen neuen Parameter haben,
der das Training und die Prognose des Modells bestimmt. Und für diesen Parameter
muss ein passender Wert eingestellt werden. Solche Parameter nennt man
**Hyperparameter**.

```{admonition} Was ist ... ein Hyperparameter?
:class: note
Ein Hyperparameter ist ein Parameter, der vor dem Training eines Modells
festgelegt wird und nicht aus den Daten während des Trainings gelernt wird. Die
Hyperparameter steuern den gesamten Lernprozess und haben einen wesentlichen
Einfluss auf die Leistung des Modells.
```

Ein Score von 1.0 auf den Trainingsdaten deutet auf Overfitting hin, d.h. das
Modell hat die Daten auswendig gelernt. Ein sehr niedriger Score (z.B. 0.72)
deutet auf Underfitting hin, d.h. das Modell ist zu einfach. Das Ziel ist ein
Gleichgewicht: ein Score, der hoch genug ist, um die Daten gut zu beschreiben,
aber nicht 1.0, um Generalisierung zu ermöglichen. Werte zwischen 0.8 und 0.95
sind oft ein guter Kompromiss, aber dies muss mit separaten Testdaten validiert
werden.

Kommen wir nun zu einem anderen Hyperparameter der Entscheidungsbäume, der
Mindestanzahl von Datenpunkten.

### Prä-Pruning: Mindestanzahl Datenpunkte

Genau wie der Hyperparameter zur Begrenzung der Baumtiefe wird die Mindestanzahl
der Datenpunkte vorab bei der Initialisierung des Entscheidungsbaumes
festgelegt. Scikit-Learn bietet wiederum zwei Möglichkeiten, über die minimale
Anzahl von Datenpunkten den Entscheidungsbaum zurechtzuschneiden. Zum einen kann
für die *Knoten* eine minimal erforderliche Anzahl von Datenpunkten festgelegt
werden, ab der es erlaubt ist, durch Entscheidungsfragen weiter zu verzweigen.
Zum anderen kann eine minimale Anzahl an Datenpunkten für jedes *Blatt*
festgelegt werden, das am Ende der Verzweigungen erreicht werden muss.

Wir probieren beide Möglichkeiten aus und vergleichen die Ergebnisse
miteinander. Die Option zur Einstellung der Mindestanzahl pro Knoten heißt
`min_samples_split` und die Option zur Einstellung des Mindestanzahl Datenpunkte
pro Blatt heißt `min_samples_leaf`. Beiden optionalen Argumenten kann entweder
ein Integer übergeben werden oder ein Float. Wird ein Integer übergeben, so ist
damit die tatsächliche minimale Anzahl an Datenpunkten gemeint. Ein Float wird
als Bruch interpretiert und meint die relative Anzahl der Datenpunkte. Der Bruch
wird mit der Gesamtzahl der Datenpunkte multipliziert und dann wird auf die
nächste ganze Zahl aufgerundet.

Schauen wir uns beide Varianten an. Zunächst begrenzen wir die Knoten und
fordern, dass sich in jedem Entscheidungsknoten mindestens sechs Datenpunkte
befinden müssen.

```{code-cell}
modell_knotenbegrenzung = DecisionTreeClassifier(random_state=0, min_samples_split=6)
modell_knotenbegrenzung.fit(X,y)

plot_tree(modell_knotenbegrenzung,
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    class_names=['nicht verkauft', 'verkauft']);

print(f'Score des Entscheidungsbaumes mit Prä-Pruning Mindestanzahl Datenpunkte pro Knoten: {modell_knotenbegrenzung.score(X,y)}')
```

Der Score ist 0.92. Nun fordern wir, dass in jedem Blatt mindestens sechs
Datenpunkte verbleiben müssen.

```{code-cell}
modell_blattbegrenzung = DecisionTreeClassifier(random_state=0, min_samples_leaf=6)
modell_blattbegrenzung.fit(X,y)

plot_tree(modell_blattbegrenzung,
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    class_names=['nicht verkauft', 'verkauft']);

print(f'Score des Entscheidungsbaumes mit Prä-Pruning Mindestanzahl Datenpunkte pro Blatt: {modell_blattbegrenzung.score(X,y)}')
```

In diesem Fall erhalten wir einen Entscheidungsbaum mit einem Score von 0.82.
Was jetzt die bessere Wahl ist -- Begrenzung der Baumtiefe oder Festlegung einer
Mindestanzahl von Datenpunkten Knoten/Blatt -- und vor allem welchen Wert der
Hyperparameter haben soll, ist eine zentrale Herausforderung im maschinellen
Lernen. In späteren Kapiteln werden wir systematische Methoden wie Grid Search
und Cross-Validation kennenlernen, um die besten Hyperparameter-Werte zu finden.

```{admonition} Mini-Übung
:class: tip
Welcher Entscheidungsbaum zeigt vermutlich die stärkste Tendenz zum Overfitting?
Stellen Sie eine Vermuting an und überprüfen Sie Ihre Vermutung durch Ausprobieren.

A) `DecisionTreeClassifier(max_depth=2)`  
B) `DecisionTreeClassifier(max_depth=10)`  
C) `DecisionTreeClassifier(min_samples_leaf=20)`
```

```{code-cell}
# Hier Ihr Code
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
Antwort B, denn eine große maximale Tiefe erlaubt sehr komplexe Bäume.

Überprüfung durch Code:
```python
# Die drei Modelle trainieren und Scores vergleichen
modell_a = DecisionTreeClassifier(max_depth=2, random_state=0)
modell_a.fit(X, y)
print(f'Score A (max_depth=2): {modell_a.score(X, y):.3f}')

modell_b = DecisionTreeClassifier(max_depth=10, random_state=0)
modell_b.fit(X, y)
print(f'Score B (max_depth=10): {modell_b.score(X, y):.3f}')

modell_c = DecisionTreeClassifier(min_samples_leaf=20, random_state=0)
modell_c.fit(X, y)
print(f'Score C (min_samples_leaf=20): {modell_c.score(X, y):.3f}')

# Modell B hat vermutlich den höchsten Score (nahe 1.0) → Overfitting!
```
````

```{dropdown} Video "How to Implement Decision Trees in Python / Scikit-Learn" von Misra Turp
<iframe width="560" height="315" src="https://www.youtube.com/embed/wxS5P7yDHRA?si=rawkRWRmUi0ZZAub" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir die Tendenz der Entscheidungsbäume zum Overfitting
diskutiert. Um dem Problem des Overfittings zu begegnen, bietet Scikit-Learn die
Möglichkeit des Prä-Prunings. Durch die Begrenzung der maximalen Baumtiefe oder
die Festlegung einer Mindestanzahl von Datenpunkten in Knoten oder Blättern kann
Overfitting reduziert werden. Diese zusätzlichen Parameter des
Entscheidungsbaums werden Hyperparameter genannt und müssen angepasst werden.
Eine weitere Alternative, das Overfitting von Entscheidungsbäumen zu minimieren,
bieten die Random Forests, die wir in einem späteren Kapitel kennenlernen
werden.
