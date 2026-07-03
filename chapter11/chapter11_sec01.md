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


# 11.1 Kreuzvalidierung

In der Praxis ist es entscheidend, dass ein ML-Modell nicht nur gute Prognosen
für die Daten liefert, sondern auch für neue, unbekannte Daten zuverlässig
funktioniert. Durch das Aufteilen der Daten in Trainings- und Testdaten können
wir eine erste Einschätzung über die Verallgemeinerungsfähigkeit eines Modells
treffen. Dieser Ansatz weist jedoch einige Schwächen auf, die wir in diesem
Kapitel näher beleuchten. Im Anschluss lernen wir ein fortschrittlicheres
Verfahren kennen: die Kreuzvalidierung, die über die einfache Aufteilung in
Trainings- und Testdaten hinausgeht und eine robustere Bewertung der
Modellleistung ermöglicht.

## Lernziele

```{admonition} Lernziele
:class: attention
- Sie sind in der Lage, das Konzept der **Kreuzvalidierung (Cross Validation)**
  verständlich zu erklären.
- Sie können die Vor- und Nachteile der Kreuzvalidierung aufzählen und bewerten.
- Sie können mit **KFold** einen Datensatz in verschiedene **Teilmengen
  (Folds)** aufteilen.
- Sie beherrschen die Durchführung einer Kreuzvalidierung mithilfe der Funktion
  **cross_validate()**.
```

## Idee der Kreuzvalidierung

Ein zentraler Schritt im ML-Workflow ist die Aufteilung der Daten in einen
Trainings- und einen Testdatensatz. Das Modell wird auf den Trainingsdaten
trainiert und anschließend auf den Testdaten bewertet. Diese Methode hat jedoch
auch Nachteile. Besonders bei kleinen Datensätzen ist es problematisch,
beispielsweise 25 % der Daten für den Test zurückhalten zu müssen, da dies die
Datenmenge für das Training reduziert. Zudem kann eine zufällige Aufteilung der
Daten zu unbalancierten Splits führen, die die Trainings- und Testergebnisse
verfälschen. Eine sinnvolle Alternative zu dieser simplen Aufteilung ist die
**Kreuzvalidierung** (engl. **Cross Validation**).

Bei der Kreuzvalidierung werden die Daten in mehrere **Teilmengen**, sogenannte
**Folds**, aufgeteilt. Beispielsweise können die Daten in fünf Folds unterteilt
werden. Das Modell wird dann fünfmal trainiert und getestet, wobei in jedem
Durchlauf eine andere Teilmenge als Testdaten verwendet wird. Im ersten
Durchlauf wird etwa Fold A für den Test zurückgehalten, während die Folds B, C,
D und E zum Training genutzt werden. Im zweiten Durchlauf wird Fold B als
Testdatensatz verwendet und die restlichen Folds dienen wieder dem Training.
Dieser Prozess wird so lange wiederholt, bis jeder Fold einmal als Testdaten
fungiert hat. Am Ende wird die Modellleistung (Score) als Durchschnitt der
Ergebnisse aus den fünf Durchläufen berechnet.

Es müssen jedoch nicht zwingend fünf Folds verwendet werden. Oftmals werden die
Daten in zehn Folds aufgeteilt, sodass 90 % der Daten zum Training und 10 % für
den Test verwendet werden. Ein weiterer Vorteil ist, dass jeder Datenpunkt im
Laufe der Kreuzvalidierung sowohl im Training als auch im Test berücksichtigt
wird, jedoch nie gleichzeitig. Dies verringert die Gefahr, dass unausgewogene
Daten zu verzerrten Testergebnissen führen, wie es bei einer zufälligen
Aufteilung passieren könnte.

Zusammengefasst bietet die Kreuzvalidierung mehrere Vorteile:

- **Effizientere Datennutzung**: Jeder Datenpunkt wird mindestens einmal als
  Testdatenpunkt verwendet, was besonders bei kleinen Datensätzen wichtig ist,
  da die Daten optimal ausgenutzt werden.
- **Stabilere Schätzung der Modellleistung**: Durch das wiederholte Training und
  Testen auf verschiedenen Daten erhöht sich die Robustheit der geschätzten
  Modellleistung (Score), da zufällige Verzerrungen durch unbalancierte Splits
  minimiert werden.

Ein Nachteil der Kreuzvalidierung ist der erhöhte Rechenaufwand, da das Modell
mehrfach trainiert und getestet wird.

Können wir also auf die Aufteilung in Trainings- und Testdaten verzichten? Nein,
denn für das Hyperparameter-Tuning ist der Split weiterhin notwendig. Mehr dazu
im nächsten Kapitel. Zunächst widmen wir uns der praktischen Umsetzung der
Kreuzvalidierung in Scikit-Learn.

## Kreuzvalidierung mit KFold

Um die Kreuzvalidierung in Scikit-Learn zu demonstrieren, generieren wir
zunächst einen künstlichen Datensatz. Mithilfe der Funktion `make_moons()`
erstellen wir 50 Datenpunkte und speichern sie in einem Pandas-DataFrame. Für
eine einfachere Visualisierung mit Plotly Express wandeln wir die Zielvariable
`'Wirkung'` von den Werten 0/1 in boolesche Werte (False/True) um.

```{code-cell}
import pandas as pd
import plotly.express as px
from sklearn.datasets import make_moons 

X_array, y_array = make_moons(noise = 0.5, n_samples=50, random_state=3)
daten = pd.DataFrame({
    'Merkmal 1': X_array[:,0],
    'Merkmal 2': X_array[:,1],
    'Wirkung': y_array
})
daten['Wirkung'] = daten['Wirkung'].astype('bool')

fig = px.scatter(daten, x = 'Merkmal 1', y = 'Merkmal 2', color='Wirkung',
    title='Künstliche Daten')
fig.show()
```

Als Nächstes laden wir die Klasse `KFold` aus dem Untermodul
`sklearn.model_selection`. Wir instanziieren ein KFold-Objekt mit dem Argument
`n_splits=5`, das die Daten in fünf Teilmengen (Folds) aufteilt. Tatsächlich ist
dies die Standardeinstellung, wie uns die [Dokumentation Scikit-Learn →
KFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html)
zeigt. Das Argument könnte also weggelassen werden.

```{code-cell}
from sklearn.model_selection import KFold

kfold = KFold(n_splits = 5)
```

Im Hintergrund wurde ein Generator erzeugt, mit Hilfe dessen wir Daten in fünf
Teilmengen (Folds) aufteilen können. Dazu benutzen wir die Methode `.split()`
und übergeben ihr die Daten, die gesplittet werden sollen.

```{code-cell}
kfold.split(daten)
```

Zwar wurde hiermit die Aufteilung in fünf Teilmengen vollzogen, doch die
eigentlichen Trainings- und Testdaten wurden noch nicht gespeichert und
weiterverarbeitet. Mithilfe einer for-Schleife greifen wir in jedem Durchgang
auf die Trainings- und Testindizes zu, die die Methode `split()` als Tupel
zurückgibt. Das erste Element enthält die Indizes der Trainingsdaten, das zweite
die der Testdaten.

```{code-cell}
for (train_index, test_index) in kfold.split(daten):
  print(f'Index Trainingsdaten: {train_index}')
  print(f'Index Testdaten: {test_index}')
```

Die Aufteilung der Daten erfolgt hierbei sehr systematisch. Im ersten Durchgang
werden die Datenpunkte 0–9 als Testdaten verwendet, im zweiten Durchgang die
Punkte 10–19 und so weiter. Bei sortierten Daten kann dies ungünstig sein. Um
eine zufällige Aufteilung zu gewährleisten, können wir das Argument
`shuffle=True` verwenden, um die Daten vor dem Split zu mischen.

```{code-cell}
kfold = KFold(n_splits = 5, shuffle=True)

for (train_index, test_index) in kfold.split(daten):
  print(f'Index Trainingsdaten: {train_index}')
  print(f'Index Testdaten: {test_index}')
```

Nun verwenden wir diese fünf Aufteilungen, um einen Entscheidungsbaum zu
trainieren. Dabei begrenzen wir die Baumtiefe auf 3 und bewerten in jedem
Durchgang die Genauigkeit (Score) sowohl auf den Trainings- als auch auf den
Testdaten.

```{code-cell}
from sklearn.tree import DecisionTreeClassifier

modell = DecisionTreeClassifier(max_depth=3) 
kfold = KFold(n_splits = 5, shuffle=True, random_state=0)

for (train_index, test_index) in kfold.split(daten):
  X_train = daten.loc[train_index, ['Merkmal 1', 'Merkmal 2']]
  y_train = daten.loc[train_index, 'Wirkung']
  X_test = daten.loc[test_index, ['Merkmal 1', 'Merkmal 2']]
  y_test = daten.loc[test_index, 'Wirkung']
  
  modell.fit(X_train, y_train)
  score_train = modell.score(X_train, y_train)
  score_test = modell.score(X_test, y_test)

  print(f'Score Training: {score_train:.2f}, Score Test: {score_test:.2f}')
```

Die Scores auf den Trainingsdaten könnten den Eindruck erwecken, dass der
Entscheidungsbaum sehr gut funktioniert. Doch die Testdaten zeigen Schwankungen
zwischen 0.4 und 0.8. Hätten wir eine einfache Aufteilung in Trainings- und
Testdaten vorgenommen und zufällig den dritten Split erwischt, hätten wir
wahrscheinlich eine zu optimistische Einschätzung der Modellqualität getroffen.
Aus didaktischen Gründen verwenden wir das Argument `random_state=0`, um die
Ergebnisse mit dem Vorlesungsskript vergleichbar zu machen.

## Automatische Kreuzvalidierung mit cross_validate

Wie so oft bietet Scikit-Learn eine elegantere und einfachere Möglichkeit, die
Kreuzvalidierung (Cross Validation) durchzuführen, ohne manuell eine
for-Schleife programmieren zu müssen. Die Funktion `cross_validate()` übernimmt
die Durchführung der Kreuzvalidierung automatisch. Wir importieren sie aus dem
Untermodul `sklearn.model_selection` und teilen anschließend die Daten in
Eingabedaten `X` und Zielgröße `y` auf.

Die Funktion `cross_validate()` wird mit dem ML-Modell (hier einem
Entscheidungsbaum), den Eingabedaten `X` und der Zielgröße `y` aufgerufen.
Standardmäßig wird eine 5-fache Kreuzvalidierung ohne Mischen durchgeführt. Mit
dem optionalen Argument `cv=` kann jedoch auch ein benutzerdefinierter
Aufteilungsgenerator übergeben werden, wie zum Beispiel `KFold`. Das zusätzliche
Argument `return_train_score=True` sorgt dafür, dass auch die Trainingsscores in
jedem Durchlauf gespeichert werden. Der entsprechende Code sieht folgendermaßen
aus:

```{code-cell}
from sklearn.model_selection import cross_validate

X = daten[['Merkmal 1', 'Merkmal 2']]
y = daten['Wirkung']

cv_results = cross_validate(modell, X,y, cv=kfold, return_train_score=True)
```

Die Funktion `cross_validate()` gibt ein Dictionary zurück, das wie folgt
aufgebaut ist:

```{code-cell}
print(cv_results)
```

In diesem Dictionary sind zunächst die Rechenzeiten für das Training
(`'fit_time'`) und die Prognose (`'score_time'`) gespeichert. Danach folgen die
Scores der Testdaten (`'test_score'`). Falls das Argument
`return_train_score=True` gesetzt wurde, enthält das Dictionary auch die Scores
der Trainingsdaten (`'train_score'`). Die Scores können wir wie folgt anzeigen
lassen:

```{code-cell}
print(cv_results['test_score'])
print(cv_results['train_score'])
```

Weitere Details zu der Funktion `cross_validate()` finden Sie in der
[Dokumentation Scikit-Learn →
cross_validate](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html).

## Zusammenfassung und Ausblick

Die Kreuzvalidierung ist ein wichtiges Werkzeug, insbesondere wenn es um die
Feinjustierung der Hyperparameter geht, also das sogenannte
Hyperparameter-Tuning. Im nächsten Kapitel werden wir uns mit der Kombination
von Kreuzvalidierung (Cross Validation) und einer Gittersuche (Grid Search)
beschäftigen, um die optimalen Hyperparameter für ein Modell zu finden.
