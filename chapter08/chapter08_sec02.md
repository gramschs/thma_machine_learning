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

# 8.2 Trainings- und Testdaten

Bei den Entscheidungsbäumen und der linearen Regression haben wir mit der
`score()`-Methode bewertet, wie viele der Daten durch das Modell korrekt
prognostiziert wurden. Je näher der Score an 1 liegt, desto besser. Doch selbst
ein perfekter Score bedeutet nicht zwangsläufig, dass das Modell optimal ist. Es
könnte überangepasst (overfitted) sein und daher bei neuen, unbekannten Daten
schlechte Prognosen liefern. Im Folgenden beschäftigen wir uns mit der
Aufteilung von Daten in Trainings- und Testdaten.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie verstehen, warum Daten in **Trainingsdaten** und **Testdaten** aufgeteilt
  werden.
* Sie können mit der Funktion **train_test_split()** Pandas-DataFrames in
  Trainings- und Testdaten aufteilen.
* Sie kennen das Konzept der **Kreuzvalidierung**.
```

## Auswendiglernen nützt nichts

Um die Herausforderungen bei der Modellauswahl zu verdeutlichen, betrachten wir
einen künstlich generierten Datensatz. Angenommen, wir hätten die folgenden 20
Messwerte erfasst und möchten ein Regressionsproblem lösen.

```{code-cell}
import pandas as pd 
import plotly.express as px

# Generierung Daten
daten = pd.DataFrame()
daten['Ursache'] = [1.8681193560547067, 0.18892899670288932, 1.8907374398595373, 0.8592639746974586, 0.7909152983890833, -1.1356420176784945, 1.905097819104967, -1.9750789791816405, -0.9880705504662242, -0.26083387038221684, 1.1175316871750098, -1.2092597015989877, 1.451972942396889, 1.933602708701251, -1.3446310343812051, 0.38933577573143685, -1.96405560932978, -0.45371486942548245, -1.8233597682740017, 1.8266118708569437]
daten['Wirkung'] = [18.06801933135814, 0.09048390063552635, 18.29951272892001, 4.02392603643671, 1.97091878521032, 6.799411114666941, 17.540101218695103, 21.051664199041685, 5.604758672240995, 0.38630710692300024, 5.261393705782588, 7.365977868421521, 10.701020062336028, 17.48514901635516, 11.263523310016517, 1.1522069460363902, 20.979929897937023, -0.08352624016486021, 18.258951764602635, 15.321589041941028]

# Visualisierung
fig = px.scatter(daten, x = 'Ursache', y = 'Wirkung', title= 'Künstlich generierte Messdaten')
fig.show()
```

Nun würden wir das folgende Modell implementieren. Der Name des Modells sagt
bereits alles!

```{code-cell}
from sklearn.metrics import r2_score

class AuswendigLerner:
    def __init__(self) -> None:
        self.X = None
        self.y = None

    def fit(self, X,y):
        self.X = X
        self.y = y

    def predict(self, X):
        return self.y
```

Wir trainieren unser Modell und lassen es dann bewerten. Um nicht selbst den
R²-Score implementieren zu müssen, verwenden wir die allgemeine Funktion aus
Scikit-Learn (siehe [Dokumentation Scikit-Learn →
r2_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html)).

```{code-cell}
# Adaption der Daten
X = daten[['Ursache']]
y = daten['Wirkung']

# Auswahl Modell und Training
mein_super_modell = AuswendigLerner()
mein_super_modell.fit(X, y)

# prediction
y_prognose = mein_super_modell.predict(X)

# check quality
score = r2_score(y,y_prognose)
print(f'Der R2-Score ist: {score:.2f}')
```

Ein R²-Score von 1, unser Modell scheint perfekt zu funktionieren! Doch wie
prognostiziert es neue Daten? Das Modell funktioniert zwar hervorragend für die
gegebenen Trainingsdaten, ist jedoch **nicht verallgemeinerbar**.

```{code-cell}
mein_super_modell.predict([[1.3]])
```

Anstatt für den x-Wert $1.3$ (Ursache) eine Prognose zu treffen, gibt das Modell
einfach die auswendig gelernten y-Werte (Wirkungen) aus.

## Daten für später aufheben

Bei der Modellauswahl und dem Training des Modells müssen wir zusätzlich
sicherstellen, dass das Modell verallgemeinerbar ist, das heißt, dass es auch
für neue, zukünftige Daten verlässliche Prognosen liefern kann. Da wir jedoch
sofort abschätzen wollen, wie gut das Modell auf neue Daten reagiert, und nicht
warten möchten, bis die nächsten Messungen vorliegen, legen wir jetzt schon
einen Teil der vorhandenen Daten zur Seite. Diese Daten nennen wir
**Testdaten**. Die verbleibenden Daten verwenden wir für das Training des
Modells, sie heißen **Trainingsdaten**. Später nutzen wir die Testdaten, um zu
überprüfen, wie gut das Modell bei Daten funktioniert, die nicht zum Training
verwendet wurden.

Für die Aufteilung in Trainings- und Testdaten verwenden wir eine dafür
vorgesehene Funktion von Scikit-Learn namens `train_test_split()` (siehe
[Dokumentation Scikit-Learn →
train_test_split()](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)).
Diese Funktion müssen wir aus dem Modul `sklearn.model_selection` importieren.
Dann übergeben wir `train_test_split()` die Daten, die aufgeteilt werden sollen,
und erhalten als Rückgabe zwei DataFrames: Der erste enthält die Trainingsdaten,
der zweite die Testdaten.

```{code-cell}
from sklearn.model_selection import train_test_split

daten_train, daten_test = train_test_split(daten)
```

Nun wollen wir sehen, welche Datenpunkte zu den Trainingsdaten und welche zu den
Testdaten gehören. Dazu fügen wir dem Datensatz ein neues Merkmal hinzu und
füllen es mit den Strings `'Trainingsdaten'` bzw. `'Testdaten'`. Anschließend
visualisieren wir die Datenpunkte wie oben, wobei die Punkte entsprechend ihrer
Zugehörigkeit (Trainings- oder Testdaten) eingefärbt werden.

```{code-cell}
# Anreicherung der Daten mit dem Splitstatus
daten.loc[daten_train.index,'Splitstatus'] = 'Trainingsdaten'
daten.loc[daten_test.index, 'Splitstatus'] = 'Testdaten'

# Visualisierung
fig = px.scatter(daten, x = 'Ursache', y = 'Wirkung', color='Splitstatus', 
title='Künstlich generierte Messdaten')
fig.show()
```

Standardmäßig hält die Funktion `train_test_split()` 25 % der Daten als
Testdaten zurück. Ein schnelles Zählen der fünf Testdatenpunkte bestätigt dies.
Die Auswahl der Testdaten erfolgt zufällig, sodass jeder Durchlauf des Codes
eine andere Aufteilung der Daten erzeugt.

Die Funktion bietet aber auch Optionen, um die Aufteilung nach eigenen Wünschen
anzupassen:

- `test_size`: Mit der Option `test_size` kann ein anderer Anteil als 25 % für
  die Testdaten festgelegt werden. Möchte man zum Beispiel nur 10 % der Daten
  als Testdaten zurückhalten, kann man `test_size=0.1` einstellen. Der Anteil
  wird als Float zwischen 0.0 und 1.0 angegeben. Verwendet man stattdessen einen
  Integer, interpretiert Scikit-Learn diesen als Anzahl der Testdatenpunkte.
  `test_size=7` bedeutet also, dass sieben Datenpunkte als Testdaten verwendet
  werden.
- `random_state`: Die zufällige Auswahl der Testdaten erfolgt durch einen
  Zufallszahlengenerator, der bei jedem Durchlauf neu gestartet wird. Wenn wir
  zwar eine zufällige Auswahl wollen, aber den Neustart des
  Zufallszahlengenerators verhindern möchten, können wir den Ausgangszustand des
  Generators mit einem festen Wert (Integer) festlegen. Das ist vor allem für
  Präsentationen oder Lehrmaterialien nützlich.
- `shuffle`: Die Option `shuffle` bestimmt, ob die Daten vor der Aufteilung
  durchmischt werden. Der Standard ist `True`, d.h. die Datenpunkte werden
  zufällig durchmischt, bevor sie aufgeteilt werden. Wird diese Option auf
  `False` gesetzt, behalten die Daten ihre ursprüngliche Reihenfolge. Bei einem
  üblichen Split von 80/20 in Trainingsdaten und Testdaten werden die ersten 80
  \% für die Trainingsdaten genommen und die letzten 20 % für die Testdaten. Sind
  die Daten sortiert, kann es dadurch zu Verzerrungen kommen. Kommen
  beispielsweise erst alle billigen Autos und dann die teuren, lernt das
  ML-Modell mit den billigeren Autos und testet mit den teureren Autos.
- `stratify`: Diese Option ist vor allem wichtig, wenn die Verteilung zwischen
  verschiedenen Klassen erhalten bleiben soll. Sind im gesamten Datensatz 30 \%
  der Autos Diesel-Fahrzeuge, sollen auch in den Trainingsdaten 30 \% der Autos
  Diesel-Fahrzeuge sein. Diese Option erfordert, dass die Option `shuffle` auf
  `True` gesetzt ist. Mehr Informationen zum Gebrauch von `stratify` finden wir
  in der [Dokumentation Scikit-Learn →
  train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html).

Nun verwenden wir `train_test_split` für unsere Daten.

```{code-cell}
daten_train, daten_test = train_test_split(daten, test_size=7, random_state=0)

# Aktualisierung des Splitstatus
daten.loc[daten_train.index,'Splitstatus'] = 'Trainingsdaten'
daten.loc[daten_test.index, 'Splitstatus'] = 'Testdaten'

# Visualisierung
fig = px.scatter(daten, x = 'Ursache', y = 'Wirkung', color='Splitstatus', 
title='Künstlich generierte Messdaten')
fig.show()
```

## Idee der Kreuzvalidierung

Das Zurückhalten eines Teils der Daten als Testdaten hat den Nachteil, dass
weniger Daten für das Training zur Verfügung stehen. Besonders bei kleinen
Datensätzen kann dies dazu führen, dass das Modell ungenau oder schlecht
trainiert wird. Hier kommt die Kreuzvalidierung ins Spiel.

Die Idee der **Kreuzvalidierung** ist, die Daten in mehrere Teilmengen zu
unterteilen und das Modell mehrmals zu trainieren und zu testen, um die Leistung
besser beurteilen zu können. Schauen wir uns zunächst die zweifache
Kreuzvalidierung an:

Bei der zweifachen Kreuzvalidierung teilen wir die Daten in zwei Teilmengen, A
und B. Das Modell wird dann zweimal trainiert und getestet: einmal mit A als
Trainingsdaten und B als Testdaten, und einmal umgekehrt. Die endgültige
Modellbewertung ergibt sich aus dem Durchschnitt der beiden Testergebnisse.

Die dreifache Kreuzvalidierung funktioniert ähnlich, mit dem Unterschied, dass
die Daten in drei Teilmengen A, B und C aufgeteilt werden. In drei Durchläufen
wird jeweils mit zwei der Teilmengen trainiert und mit der dritten getestet:

- Im ersten Durchlauf wird mit A und B trainiert und mit C getestet.
- Im zweiten Durchlauf wird mit B und C trainiert und mit A getestet.
- Im dritten Durchlauf wird mit A und C trainiert und mit B getestet. Am Ende
wird der Durchschnitt der drei Testergebnisse als Maß für die Modellleistung
verwendet.

Dieses Verfahren lässt sich auf beliebig viele Teilmengen erweitern.
Scikit-Learn bietet dafür auch spezielle Funktionen zur effizienten Umsetzung
der Kreuzvalidierung. Eine detailliertere Betrachtung dieser Techniken erfolgt
jedoch in einem späteren Kapitel. An dieser Stelle soll lediglich das Konzept
der Kreuzvalidierung eingeführt werden.

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir die Aufteilung von Daten in Trainings- und
Testdaten kennengelernt und die Funktion `train_test_split()` verwendet. Diese
Funktion wird uns in zukünftigen Kapiteln und Projekten begleiten. Zudem haben
wir eine erste Einführung in die Kreuzvalidierung erhalten, die wir später
ausführlicher behandeln werden.
