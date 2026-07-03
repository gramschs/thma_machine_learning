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

# 7.1 Einfache lineare Regression

Die lineare Regression gehört zu den überwachten maschinellen Lernverfahren
(Supervised Learning). Meist ist sie das erste ML-Modell, das eingesetzt wird,
um Regressionsprobleme zu lösen. In diesem Kapitel führen wir in das Konzept
und die Umsetzung der einfachen linearen Regression mit Scikit-Learn ein.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie kennen das **lineare Regressionsmodell**.
* Sie können erklären, was die **Fehlerquadratsumme** ist.
* Sie wissen, dass das Training des lineare Regressionsmodells durch die
  **Minimierung** der Fehlerquadratsumme (Kleinste-Quadrate-Schätzer) erfolgt.
* Sie können mit Scikit-Learn ein lineares Regressionsmodell trainieren.
* Sie können mit einem trainierten linearen Regressionsmodell Prognosen treffen.
* Sie können mit dem **Bestimmtheitsmaß** bzw. **R²-Score** beurteilen, ob das
  lineare Regressionsmodell geeignet zur Erklärung der Daten ist.
```

## Regression kommt aus der Statistik

In der Statistik beschäftigen sich Mathematikerinnen und Mathematiker bereits
seit Jahrhunderten damit, Analyseverfahren zu entwickeln, mit denen
experimentelle Daten gut erklärt werden können. Falls wir eine "erklärende”
Variable haben und wir versuchen, die Abhängigkeit einer Messgröße von der
erklärenden Variable zu beschreiben, nennen wir das Regressionsanalyse oder kurz
**Regression**. Bei vielen Problemen suchen wir nach einem linearen Zusammenhang
und sprechen daher von **linearer Regression**. Mehr Details finden wir auch bei
[Wikipedia → Regressionsanalyse](https://de.wikipedia.org/wiki/Regressionsanalyse).

Etwas präziser formuliert ist lineare Regression ein Verfahren, bei dem es eine
Einflussgröße $x$ und eine Zielgröße $y$ gibt. In der ML-Sprechweise wird die
Einflussgröße $x$ typischerweise als **Merkmal** (oder englisch **Input** oder
**Feature**) bezeichnet. Die **Zielgröße** (manchmal auch **Output** oder
**Target** genannt) soll stetig sein (manchmal auch kontinuierlich, metrisch
oder quantitativ genannt). Für das Merkmal (oder die Merkmale) liegen $M$
Datenpunkte mit den dazugehörigen Werten der Zielgröße vor. Diese werden
üblicherweise als Paare (wenn nur ein Merkmal vorliegt) zusammengefasst:

$$(x^{(1)},y^{(1)}), \, (x^{(2)},y^{(2)}), \, \ldots, \, (x^{(M)},y^{(M)}).$$

Ziel der linearen Regression ist es, zwei Parameter $w_0$ und $w_1$ so zu
bestimmen, so dass die lineare Gleichung

$$y^{(i)} \approx w_0 + w_1 x^{(i)}$$

möglichst für alle Datenpunkte $(x^{(i)}, y^{(i)})$ gilt. Geometrisch
ausgedrückt: durch die Daten soll eine Gerade gelegt werden, wie die folgende
Abbildung zeigt. Die Datenpunkte sind blau, die Regressionsgerade rot.

```{figure} pics/Linear_regression.svg
---
name: fig_linear_regression
---
Lineare Regression: die erklärende Variable (= Input oder unabhängige Variable
oder Ursache) ist auf der x-Achse, die abhängige Variable (= Output oder
Wirkung) ist auf der y-Achse aufgetragen, Paare von Messungen sind in blau
gekennzeichnet, das Modell in rot.
(Quelle:[Wikimedia](https://commons.wikimedia.org/wiki/File:Linear_regression.svg)
 von Sewaqu. Lizenz: Public domain))
```

In der Praxis werden die Daten nicht perfekt auf der Geraden liegen. Die Fehler
zwischen dem echten $y^{(i)}$ und dem Funktionswert der Gerade $f(x^{(i)}) =
w_0 + w_1 x^{(i)}$ werden unterschiedlich groß sein, je nachdem, welche Parameter
$w_0$ und $w_1$ gewählt werden. Wie finden wir jetzt die beste Kombination $w_0$
und $w_1$, so dass diese Fehler möglichst klein sind?

## Wie groß ist der Fehler?

Das Prinzip für das lineare Regressionsmodell und auch die folgenden ML-Modelle
ist jedesmal gleich. Das Modell ist eine mathematische Funktion, die aber noch
Parameter (hier beispielsweise die Koeffizienten der Gerade) enthält. Dann wird
festgelegt, was eine gute Prognose ist, also wie Fehler berechnet und beurteilt
werden sollen. Das hängt jeweils von dem betrachteten Problem ab. Sobald das
sogenannte Fehlermaß feststeht, werden die Parameter der Modellfunktion so
berechnet, dass das Fehlermaß (z.B. Summe der Fehler oder Mittelwert der Fehler)
möglichst klein wird. In der Mathematik sagt man dazu **Minimierungsproblem**.

Für die lineare Regression wird als Fehlermaß die Kleinste-Quadrate-Schätzung
verwendet (siehe [Wikipedia  → Methode der kleinsten
Quadrate](https://de.wikipedia.org/wiki/Methode_der_kleinsten_Quadrate)). Dazu
berechnen wir, wie weit weg die Gerade von den Messpunkten ist. Wie das geht,
veranschaulichen wir uns mit der folgenden Grafik.

```{figure} pics/kq_regression.png
---
width: 600px
name: kq_regression
---
Messpunkte (blau) und der Abstand (grün) zu einer Modellfunktion (rot)
([Quelle:](https://commons.wikimedia.org/wiki/File:MDKQ1.svg) Autor: Christian Schirm, Lizenz: CC0) 
```

Unsere rote Modellfunktion trifft die Messpunkte mal mehr und mal weniger gut.
Wir können jetzt für jeden Messpunkt berechnen, wie weit die rote Kurve von ihm
weg ist (= grüne Strecke), indem wir die Differenz der y-Koordinaten errechnen:
$r = y_{\text{blau}}-y_{\text{rot}}$. Diese Differenz nennt man **Residuum**.
Danach summieren wir die Fehler (also die Residuen) auf und erhalten den
Gesamtfehler. Dabei kann es passieren, dass am Ende als Gesamtfehler 0
herauskommt, weil beispielsweise für den 1. Messpunkt die blaue y-Koordinate
unter der roten y-Koordinate liegt und damit ein negatives Residuum herauskommt,
aber für den 5. Messpunkt ein positives Residuum. Daher quadrieren wir die
Residuen, was noch weitere Vorteile bietet (Differenzierbarkeit, eindeutiges
Minimum). Dann wird diese **Fehlerquadratsumme** minimiert, um die Koeffizienten
des Regressionsmodells zu berechnen.

## Einfache lineare Regression mit Scikit-Learn

Nach diesem theoretischen Exkurs möchten wir Scikit-Learn nutzen, um eine
einfache lineare Regression durchzuführen. Aus didaktischen Gründen erzeugen wir
uns dazu künstliche Daten mit der Funktion `make_regression` des Moduls
`sklearn.datasets`. Wir transformieren die zufällig erzeugten Zahlen und packen
sie in ein Pandas-DataFrame mit den Merkmalen »Leistung \[PS\]« eines Autos und
dem »Preis \[EUR\]« eines Autos.

```{code-cell} ipython3
import numpy as np 
import pandas as pd 
from sklearn.datasets import make_regression

X_array, y_array = make_regression(n_samples=100, n_features=1, noise=10, random_state=0)

daten = pd.DataFrame({
    'Leistung [PS]': np.floor(50*(X_array[:,0] + 3)),
    'Preis [EUR]': 100*(y_array+150)
    })
```

Mehr Details zu der Funktion `make_regression` gibt es in der [Dokumentation
Scikit-Learn →
make_regression](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html#sklearn.datasets.make_regression).
Wir visualisieren nun den Preis in Abhängigkeit von der Leistung des Autos.

```{code-cell} ipython3
import plotly.express as px 

fig = px.scatter(daten, x = 'Leistung [PS]', y = 'Preis [EUR]',
    title='Künstliche Daten: Verkaufspreise Autos')
fig.show()
```

Es drängt sich die Vermutung auf, dass der Preis eines Autos linear von der
Leistung abhängt. Je mehr PS, desto teurer das Auto.

Als nächstes trainieren wir ein lineares Regressionsmodell auf den Daten.
Lineare ML-Modelle fasst Scikit-Learn in einem Untermodul namens `linear_model`
zusammen. Um also das lineare Regressionsmodell `LinearRegression` verwenden zu
können, müssen wir es folgendermaßen importieren und initialisieren:

```{code-cell} ipython3
from sklearn.linear_model import LinearRegression

modell = LinearRegression()
```

Mit der Methode `.fit()` werden die Parameter des linearen Regressionsmodells an
die Daten angepasst. Dazu müssen die Daten in einem bestimmten Format vorliegen.
Bei den Inputs wird davon ausgegangen, dass mehrere Merkmale in das Modell
eingehen sollen. Die Merkmale stehen normalerweise in den Spalten des
Datensatzes. Beim Output erwarten wir zunächst nur ein Merkmal, das durch das
Modell erklärt werden soll. Daher geht Scikit-Learn davon aus, dass der Input
eine Tabelle (Matrix) $X$ ist, die M Zeilen und N Spalten hat. M ist die Anzahl
an Datenpunkten, hier also die Anzahl der Autos, und N ist die Anzahl der
Merkmale, die betrachtet werden sollen. Da wir momentan nur die Abhängigkeit des
Preises von der PS-Zahl analysieren wollen, ist $N=1$. Beim Output geht
Scikit-Learn davon aus, dass eine Datenreihe (eindimensionaler Spaltenvektor)
vorliegt, die natürlich ebenfalls M Zeilen hat. Wir müssen daher unsere
PS-Zahlen noch in das Matrix-Format bringen. Dazu verwenden wir die Tatsache,
dass mit `[ [list] ]` eine Tabelle extrahiert wird.

```{code-cell} ipython3
# Adaption der Daten
X = daten[['Leistung [PS]']]
y = daten['Preis [EUR]']
```

Danach können wir das lineare Regressionsmodell trainieren.

```{code-cell} ipython3
modell.fit(X,y)
```

Es erfolgt keine Ausgabe, aber jetzt ist das lineare Regressionsmodell
trainiert. Die durch das Training bestimmten Parameter des Modells sind im
Modell selbst abgespeichert. Bei dem linearen Regressionsmodell sind das die
beiden Parameter $w_0$ und $w_1$, also Steigung `.coef_` und den
y-Achsenabschnitt `.intercept_`.

```{code-cell} ipython3
print(f'Steigung: {modell.coef_[0]}')
print(f'y-Achsenabschnitt: {modell.intercept_}')
```

Damit lautet das (gerundete) lineare Regressionsmodell, um aus der PS-Zahl eines
Autos $x$ den Verkaufspreis $y$ zu berechnen, folgendermaßen:

$$y = 85.2 \cdot x + 2179.$$

## Prognosen treffen

Wenn wir die Parameter des trainierten Modells ausgeben lassen bzw. die lineare
Funktion $y = 85.2 \cdot x + 2179$ verwenden, können wir mit dem linearen Modell
Prognosen treffen. Den Umweg über das Ausgeben der trainierten Parameter und dem
Basteln einer linearen Funktion können wir uns aber sparen, denn Scikit-Learn
stellt für Prognosen mit dem trainierten Modell direkt eine Methode zur
Verfügung. Mit Hilfe der `predict()`-Methode können für jedes Scikit-ML-Modell
Prognosen getroffen werden.

Wir möchten uns den kompletten Bereich zwischen 20 PS und 270 PS ansehen und
erzeugen daher 100 Punkte in diesem Bereich. Diese transformieren wir in ein
Pandas-DataFrame und verwenden dann die `predict()`-Methode.

```{code-cell}
testdaten = pd.DataFrame({
    'Leistung [PS]': np.linspace(20, 270, 100)
    })
prognose = modell.predict(testdaten[['Leistung [PS]']])   
```

Diese Prognose wird dann zusammen mit den Verkaufsdaten in einem Diagramm
visualisiert. Dazu generieren wir zuerst den Scatter-Plot mit den Verkaufsdaten
und fügen dann mit der Funktion `add_scatter()` einen zweiten Scatter-Plot zu
dem ersten hinzu. In diesem Scatter-Plot sollen die Punkte jedoch durch eine
Linie verbunden werden, weshalb wir die Option `mode='lines'` nutzen. Zusätzlich
kennzeichnen wir die Regressionsgerade noch mit dem Namen `name='Prognose'`.

```{code-cell}
fig = px.scatter(daten, x = 'Leistung [PS]', y = 'Preis [EUR]',
    title='Verkaufspreise von Autos')
fig.add_scatter(x = testdaten['Leistung [PS]'], y = prognose, mode='lines', name='Prognose')
fig.show()
```

Der visuelle Eindruck ist gut, aber ist diese Regressionsgerade wirklich das
beste Modell? Im nächsten Abschnitt sehen wir uns ein statistisches Bewertungsmaß
an, um die Güte des Modells zu beurteilen.

## Ist das beste Modell gut genug? Der R²-Score

Auch wenn wir mit der Minimierung der Fehlerquadratsumme bzw. der
Kleinsten-Quadrate-Methode die besten Parameter für unsere Modellfunktion
gefunden haben, heißt das noch lange nicht, dass unser Modell gut ist. Bereits
die Modellfunktion kann ja völlig falsch gewählt sein. Beispielsweise könnten
wir Messungen rund um eine sinus-förmige Wechselspannung vornehmen und dann wäre
ein lineares Regressionsmodell völlig ungeeignet, auch wenn die
Fehlerquadratsumme minimal wäre.

Wir brauchen daher noch ein Kriterium dafür, ob das trainierte Modell auch
valide ist. Für die lineare Regression nehmen wir das **Bestimmtheitsmaß**, das
in der ML-Community auch **R²-Score** genannt wird. Der R²-Score wird dabei
folgendermaßen interpretiert:

* Wenn $R^2 = 1$  ist, dann gibt es den perfekten linearen Zusammenhang und die
  Modellfunktion ist eine sehr gute Anpassung an die Messdaten.
* Wenn $R^2 = 0$ oder gar negativ ist, dann funktioniert die lineare
  Modellfunktion überhaupt nicht. Dann ist das Modell schlechter als der einfache
  Mittelwert.

Auf der Seite [https://mathweb.de](https://mathweb.de) gibt es eine Reihe von
Aufgaben und interaktiven Demonstrationen rund um die Mathematik. Insbesondere
gibt es dort auch eine interaktive Demonstration des R²-Scores.

```{admonition} Mini-Übung
:class: tip
<iframe width="560" height="315"
src="https://lti.mint-web.de/examples/index.php?id=01010320"  allowfullscreen>
</iframe>

Drücken Sie auf den zwei kreisförmigen Pfeile rechts oben. Dadurch wird ein
neuer Datensatz erzeugt. Die Messdaten sind durch grüne Punkte dargestellt, das
lineare Regressionsmodell durch eine blaue Gerade. Im Titel wird der aktuelle
und der optimale R²-Wert angezeigt. Ziehen Sie an den weißen Punkten, um die
Gerade zu verändern. Schaffen Sie es, den optimalen R²-Score zu treffen?
Beobachten Sie dabei, wie die Fehler (rot) kleiner werden.
```

Wie ist nun der R²-Score für das trainierte lineare Regressionsmodell? Dazu
verwenden wir die `score()`-Methode.

```{code-cell} ipython3
r2_score = modell.score(X,y)
print(f'Der R2-Score für das lineare Regressionsmodell ist: {r2_score:.2f}.')
```

Das lineare Regressionsmodell kann für die Trainingsdaten sehr gut die
Verkaufspreise prognostizieren. Wie gut es allerdings noch unbekannte Daten
prognostizieren könnte, ist ungewiss. Mit dem Thema Validierung werden wir uns
einem späteren Kapitel noch detailliert beschäftigen.

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir das theoretische Modell der linearen Regression
kennengelernt. Das Training eines linearen Regressionsmodells mit Scikit-Learn
erfolgt wie üblich mit der `fit()`-Methode, die Prognose mit der
`predict()`-Methode. Bewerten können wir Prognosequalität mit der
`score()`-Methode. Im nächsten Kapitel betrachten wir die lineare Regression,
bei der die Zielgröße von mehreren Merkmalen abhängt.
