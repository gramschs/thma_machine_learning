---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: chapter07_sec03.md
    title: chapter07_sec03.md
---

# 7.3 Polynomiale Regression

In den letzten beiden Kapiteln haben wir die lineare Regression kennengelernt,
mit einem Merkmal und mit mehreren Merkmalen. In diesem Kapitel erweitern wir sie
zu quadratischen, kubischen und allgemein polynomialen Modellen. Am Bremsweg
eines Autos sehen wir dabei, dass ein hoher R²-Score auf den Trainingsdaten
allein noch nicht bedeutet, dass ein Modell gut ist. Wir lernen drei Kriterien
kennen, mit denen sich ein Modell beurteilen lässt, und wenden sie an. Overfitting
und Underfitting sind uns schon bei den Entscheidungsbäumen begegnet (Kapitel
6.3), hier treffen wir sie bei der Regression wieder.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können eine **polynomiale Regression** mit `PolynomialFeatures`
  durchführen.
* [ ] Sie können ein Modell anhand von drei Kriterien beurteilen: **Anpassung**
  an die Trainingsdaten, **Generalisierung** auf unabhängige Daten und
  **Plausibilität** von Verlauf und Prognosen.
* [ ] Sie können die **Plausibilität** eines Regressionsmodells anhand von
  Kurvenverlauf und Prognosen prüfen.
* [ ] Sie wissen, dass ein hoher R²-Score auf den Trainingsdaten allein noch kein
  gutes Modell bedeutet.
* [ ] Sie erkennen **Underfitting** und **Overfitting** am Kurvenverlauf und
  wissen, dass der **Polynomgrad** ein **Hyperparameter** ist.
```

## Polynomiale Regression durchführen

### Ein Experiment zum Bremsweg

Ausnahmsweise beschäftigen wir uns in diesem Kapitel nicht mit dem Verkauf von
Autos, sondern mit ihrem Bremsweg. Die Faustformel zur Berechnung des Bremsweges
$s$ in Metern (ohne Reaktionszeit) lautet

$$s = \frac{1}{100} \cdot v^2,$$

wobei die Geschwindigkeit $v$ des Autos in km/h angegeben wird. Natürlich
variiert der tatsächliche Bremsweg abhängig von der Straßenoberfläche (trocken /
nass / vereist) oder dem Fahrzeugtyp (insbesondere Leistung der Bremse). Wird die
Bremsung aufgrund eines plötzlich auftauchenden Hindernisses eingeleitet, kommt
zum Bremsweg noch der Reaktionsweg hinzu. Mehr Details finden Sie auf den
Internetseiten des ADAC unter [Bremsweg berechnen: Mit dieser Formel
geht's](https://www.adac.de/verkehr/rund-um-den-fuehrerschein/erwerb/bremsweg-berechnen/).

Wir erzeugen nun künstliche Daten, die ein Experiment simulieren: Bremswege von
Autos in Abhängigkeit von der Geschwindigkeit. In einem ersten Schritt
generieren wir zufällig 50 Geschwindigkeiten zwischen 30 km/h und 150 km/h.
Gemäß der obigen Faustformel lassen wir zunächst die dazugehörigen Bremswege
berechnen, addieren dann aber noch zufällige Schwankungen.

```{code-cell} python
import numpy as np 
import pandas as pd 

np.random.seed(0)
anzahl_experimente = 50
v_min = 30
v_max = 151

v = np.floor( np.random.uniform(v_min, v_max, anzahl_experimente) )
zufaellige_schwankungen = 3 * np.random.normal(0, 1, anzahl_experimente)
bremsweg = 1/100 * v**2 

daten = pd.DataFrame({
    'Geschwindigkeit [km/h]': v,
    'Bremsweg [m]': bremsweg + zufaellige_schwankungen,
    })
```

Als nächstes lassen wir die künstlich erzeugten Bremsweg-Experimente visualisieren.

```{code-cell} python
import plotly.express as px 

fig = px.scatter(daten, x = 'Geschwindigkeit [km/h]', y = 'Bremsweg [m]',
    title='Künstliche Daten: Bremsweg eines Autos')
fig.show()
```

### Erster Versuch: eine Gerade

Als erstes verwenden wir die lineare Regression. Wenn wir die Geschwindigkeit mit
$x$ bezeichnen und den Bremsweg mit $y$, dann lautet das lineare
Regressionsmodell

$$y = w_0 + w_1 \cdot x.$$

```{code-cell} python
from sklearn.linear_model import LinearRegression

# Daten ins richtige Format bringen
X = daten[['Geschwindigkeit [km/h]']]
y = daten['Bremsweg [m]']

# Training
modell_linear = LinearRegression()
modell_linear.fit(X, y)

# Anpassung an die Trainingsdaten
r2_training = modell_linear.score(X, y)
print(f'R2-score Trainingsdaten: {r2_training:.4f}')
```

Der R²-Score sieht mit etwa 0.96 sehr gut aus. Um die Prognose beurteilen zu
können, schauen wir sie uns über einen Geschwindigkeitsbereich an, der etwas über
die Trainingsdaten hinausgeht. Weil wir die Daten selbst mit der Faustformel
erzeugt haben, können wir die Prognose zusätzlich mit dieser wahren Kurve
vergleichen.

```{code-cell} python
# Geschwindigkeiten für die Prognosekurve, etwas über den Datenbereich hinaus
neue_daten = pd.DataFrame({
    'Geschwindigkeit [km/h]': np.linspace(30, 180, 200)
    })
faustformel = 1/100 * neue_daten['Geschwindigkeit [km/h]']**2
```

```{code-cell} python
y_prognose = modell_linear.predict(neue_daten)

fig = px.scatter(daten, x = 'Geschwindigkeit [km/h]', y = 'Bremsweg [m]',
    title='Bremsweg eines Autos: lineares Modell')
fig.add_scatter(x = neue_daten['Geschwindigkeit [km/h]'], y = y_prognose,
    mode='lines', name='Prognose')
fig.add_scatter(x = neue_daten['Geschwindigkeit [km/h]'], y = faustformel,
    mode='lines', name='Faustformel')
fig.show()
```

Die Gerade trifft die gekrümmte Punktwolke nur grob. Sie liegt mal über, mal
unter der Faustformel, und im unteren Geschwindigkeitsbereich sagt sie sehr
kleine, bald sogar negative Bremswege voraus. Für den gekrümmten Zusammenhang ist
eine Gerade zu einfach. Wir probieren als nächstes ein quadratisches Modell.

### Der Trick: neue Merkmale erzeugen

Wenn wir in der Dokumentation von Scikit-Learn nach einer Funktion zur
quadratischen Regression suchen, werden wir nicht fündig. Stattdessen nutzen wir
einen Trick und erzeugen neue Merkmale.

Das lineare Regressionsmodell hat nur ein Merkmal $x$, nämlich die
Geschwindigkeit:

$$y = w_0 + w_1 \cdot x.$$

Wenn wir eine quadratische Funktion als Modellfunktion wählen möchten, erzeugen
wir einfach ein zweites Merkmal. Wir nennen die bisherigen x-Werte $x$ jetzt
$x_1$ und fügen als zweites Merkmal die neue Eigenschaft

$$x_2 = \left( x_1 \right)^2$$

hinzu. Damit wird aus dem quadratischen Regressionsmodell

$$y = w_0 + w_1 \cdot x_1 + w_2 \cdot \left( x_1 \right)^2$$

das *multiple* lineare Regressionsmodell

$$y = w_0 + w_1 \cdot x_1 + w_2 \cdot x_2.$$

Scikit-Learn stellt dafür passende Methoden bereit. Aus dem Vorbereitungsmodul
`sklearn.preprocessing` importieren wir `PolynomialFeatures`. Mehr Details dazu
finden Sie in der [Dokumentation Scikit-Learn →
PolynomialFeatures](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html).
Wir erzeugen das PolynomialFeatures-Objekt mit der Option `degree=2` und
transformieren die Input-Daten mit der `fit_transform()`-Methode.

```{code-cell} python
from sklearn.preprocessing import PolynomialFeatures

# Merkmale erzeugen: aus x_1 wird (x_1, x_1 hoch 2)
poly2 = PolynomialFeatures(degree = 2)
X = poly2.fit_transform(daten[['Geschwindigkeit [km/h]']])
y = daten['Bremsweg [m]']
```

Wichtig: `fit_transform()` lernt die Transformation aus den Trainingsdaten und
wendet sie an, `transform()` wendet nur die bereits gelernte Transformation an.

Danach können wir das multiple lineare Regressionsmodell trainieren und bewerten
lassen.

```{code-cell} python
modell_quadratisch = LinearRegression()
modell_quadratisch.fit(X, y)

r2_training = modell_quadratisch.score(X, y)
print(f'R2-score Trainingsdaten: {r2_training:.4f}')
```

Für die Prognosekurve müssen wir auch die neuen Geschwindigkeiten mit demselben
Transformator umformen. Wir nutzen dazu die `transform()`-Methode.

```{code-cell} python
X_neu = poly2.transform(neue_daten)
y_prognose = modell_quadratisch.predict(X_neu)

fig = px.scatter(daten, x = 'Geschwindigkeit [km/h]', y = 'Bremsweg [m]',
    title='Bremsweg eines Autos: quadratisches Modell')
fig.add_scatter(x = neue_daten['Geschwindigkeit [km/h]'], y = y_prognose,
    mode='lines', name='Prognose')
fig.add_scatter(x = neue_daten['Geschwindigkeit [km/h]'], y = faustformel,
    mode='lines', name='Faustformel')
fig.show()
```

Prognose und Faustformel sind kaum zu unterscheiden. Der R²-Score ist mit rund
0.998 höher als beim linearen Modell.

Beide Modelle haben also einen ordentlichen R²-Score, das quadratische einen
besseren. Trotzdem haben wir sie unterschiedlich beurteilt, nicht nur über den
Score, sondern auch über den Kurvenverlauf. Das führt uns zu den Kriterien, mit
denen man ein ML-Modell bewertet.

## Drei Kriterien für ein gutes Modell

Schon in Kapitel 7.1 haben wir festgestellt: Selbst wenn die Fehlerquadratsumme
minimal ist, kann das Modell völlig falsch sein, zum Beispiel eine Gerade für
einen sinusförmigen Zusammenhang. Ein kleiner Fehler auf den Trainingsdaten ist
also nur ein Teil der Wahrheit. Ein Modell beurteilt man an drei Kriterien.

```{admonition} Drei Kriterien zur Modellbewertung
:class: note
| Kriterium | Leitfrage |
| --- | --- |
| **Anpassung** | Wie gut beschreibt das Modell die Trainingsdaten? |
| **Generalisierung** | Wie gut funktioniert es auf unabhängigen Daten? |
| **Plausibilität** | Sind Verlauf und Prognosen fachlich sinnvoll? |
```

### Anpassung

Die Anpassung an die Trainingsdaten misst der R²-Score, den wir mit der
`score()`-Methode berechnen. Das lineare Modell erreicht 0.9641, das quadratische
0.9979. Beide beschreiben die Trainingsdaten ordentlich, das quadratische besser.

### Generalisierung

Wichtiger ist meist, wie gut ein Modell für Autos funktioniert, die nicht in den
Trainingsdaten stehen. Diese Frage kann der R²-Score auf den Trainingsdaten nicht
beantworten, denn das Modell wurde ja genau auf diese Daten angepasst.

Ein Gedankenexperiment: Hätten wir von den 50 Autos zehn zurückgehalten und das
Modell nur mit den übrigen 40 trainiert, könnten wir am Schluss prüfen, wie gut
es die Bremswege der zehn zurückgehaltenen Autos trifft. Genau dieses Vorgehen
lernen wir in Kapitel 8.3 mit `train_test_split` kennen. In diesem Kapitel lassen
wir das Kriterium Generalisierung noch offen.

### Plausibilität

Das dritte Kriterium prüft mit Fachwissen, ob Verlauf und Prognosen sinnvoll
sind. Drei Fragen helfen dabei:

* **Wertebereich:** Sind die Prognosen physikalisch überhaupt möglich? Ein
  Bremsweg kann nicht negativ sein.
* **Verlauf:** Passt die Form der Kurve zur Erwartung? Der Bremsweg sollte mit
  der Geschwindigkeit glatt und ohne Sprünge steigen.
* **Extrapolation:** Bleiben die Prognosen auch etwas außerhalb des
  Datenbereichs sinnvoll?

Hier haben wir einen Vorteil: Wir kennen den wahren Zusammenhang, die Faustformel,
und können die Modellkurve direkt mit ihr vergleichen (grüne Linie in den
Abbildungen). Normalerweise kennt man das wahre Gesetz nicht. Dann stützt sich
der Plausibilitäts-Check allein auf Fachwissen und gesunden Menschenverstand.

### Die beiden Modelle im Vergleich

```{code-cell} python
# Prognose der beiden Modelle bei 30 km/h
neuer_wert = pd.DataFrame({'Geschwindigkeit [km/h]': [30]})
print(f'linear:      {modell_linear.predict(neuer_wert)[0]:.1f} m')
print(f'quadratisch: {modell_quadratisch.predict(poly2.transform(neuer_wert))[0]:.1f} m')
```

**Lineares Modell:** Die Anpassung ist ordentlich (R² 0.96). Die Plausibilität
ist aber verletzt: Bei 30 km/h prognostiziert das Modell einen Bremsweg von etwa
$-15$ m, und im ganzen Bereich weicht es systematisch von der Faustformel ab, mal
nach oben, mal nach unten. Die Gerade ist zu starr für den gekrümmten
Zusammenhang. Dieses Fehlerbild, ein zu einfaches Modell, heißt **Underfitting**.

**Quadratisches Modell:** Die Anpassung ist sehr gut (R² 0.998). Die Plausibilität
stimmt ebenfalls: Der Verlauf steigt glatt und monoton, alle Prognosen sind
positiv, und die Kurve liegt dicht an der Faustformel, auch etwas über 150 km/h
hinaus. Von den Kriterien, die wir jetzt prüfen können, erfüllt das quadratische
Modell alle.

## Wenn das Modell zu komplex wird: Overfitting

Das quadratische Modell passt gut. Wäre ein Polynom höheren Grades noch besser?
Mit demselben Trick können wir die Merkmale mit 3, 4 oder mehr potenzieren. Wir
probieren Grad 8.

Bei hohem Grad werden die Merkmalswerte sehr groß ($150^8$ ist eine 18-stellige
Zahl). Damit die Berechnung numerisch zuverlässig bleibt, skalieren wir die
Geschwindigkeit vorher mit dem `MinMaxScaler` auf den Bereich 0 bis 1. Wie
`PolynomialFeatures` wird der Skalierer mit `fit` an die Trainingsdaten angepasst
und mit `transform` angewendet.

```{code-cell} python
from sklearn.preprocessing import MinMaxScaler

# Geschwindigkeit auf 0 bis 1 skalieren, dann Merkmale erzeugen
skalierer = MinMaxScaler()
X_skaliert = skalierer.fit_transform(daten[['Geschwindigkeit [km/h]']])

poly8 = PolynomialFeatures(degree = 8)
X = poly8.fit_transform(X_skaliert)
y = daten['Bremsweg [m]']

modell_grad8 = LinearRegression()
modell_grad8.fit(X, y)

r2_training = modell_grad8.score(X, y)
print(f'R2-score Trainingsdaten: {r2_training:.4f}')
```

```{code-cell} python
X_neu = poly8.transform(skalierer.transform(neue_daten))
y_prognose = modell_grad8.predict(X_neu)

fig = px.scatter(daten, x = 'Geschwindigkeit [km/h]', y = 'Bremsweg [m]',
    title='Bremsweg eines Autos: Polynom 8. Grades')
fig.add_scatter(x = neue_daten['Geschwindigkeit [km/h]'], y = y_prognose,
    mode='lines', name='Prognose')
fig.add_scatter(x = neue_daten['Geschwindigkeit [km/h]'], y = faustformel,
    mode='lines', name='Faustformel')
# y-Achse begrenzen, damit die Kurve im Datenbereich erkennbar bleibt
fig.update_yaxes(range=[-50, 400])
fig.show()
```

**Anpassung:** Der R²-Score auf den Trainingsdaten ist mit 0.9986 sogar etwas
höher als beim quadratischen Modell (0.9979). Das ist kein Zufall: Ein Polynom
8. Grades enthält das quadratische als Spezialfall (die höheren Koeffizienten
können null sein), es kann die Trainingsdaten also mindestens so gut anpassen.
Die Prognosekurve zieht sich etwas näher an die einzelnen Punkte.

**Plausibilität:** Hier fällt das Modell durch. Bei 30 km/h liegt die Prognose
schon bei null. Ab etwa 150 km/h biegt die Kurve nach unten ab: Das Modell sagt
für schnellere Autos einen kürzeren Bremsweg voraus, ab ungefähr 170 km/h sogar
einen negativen. Das ist technisch unmöglich. Das Modell hat sich zu stark an die
zufällige Lage der einzelnen Trainingspunkte angepasst und dabei den glatten
Zusammenhang verloren.

Dieses Fehlerbild, ein zu komplexes Modell, heißt **Overfitting**. Von den
Entscheidungsbäumen kennen wir es schon (Kapitel 6.3): Dort hat sich der Baum an
einzelne Ausreißer angepasst.

### Der Polynomgrad ist ein Hyperparameter

Der Polynomgrad wird vor dem Training festgelegt und nicht aus den Daten gelernt.
Solche Werte heißen Hyperparameter, wie schon bei der maximalen Tiefe der
Entscheidungsbäume in Kapitel 6.3.

```{admonition} Was ist ... ein Hyperparameter?
:class: note
Ein Hyperparameter ist ein Parameter, der vor dem Training eines Modells
festgelegt wird und nicht aus den Daten während des Trainings gelernt wird. Die
Hyperparameter steuern den gesamten Lernprozess und haben einen wesentlichen
Einfluss auf die Leistung des Modells.
```

Für ein gutes Modell muss der Polynomgrad passend gewählt werden. Wir fassen die
drei betrachteten Modelle zusammen:

| Polynomgrad | R² (Trainingsdaten) | Plausibilität |
| --- | --- | --- |
| 1 | 0.9641 | negativer Bremsweg unter 39 km/h, Verlauf zu starr — Underfitting |
| 2 | 0.9979 | Verlauf und Prognosen durchweg sinnvoll — gutes Modell |
| 8 | 0.9986 | ab 150 km/h fallender, dann negativer Bremsweg — Overfitting |

Die Anpassung an die Trainingsdaten wird mit steigendem Polynomgrad besser. Das
allein macht ein Modell aber nicht gut. Das quadratische Modell erfüllt alle
Kriterien, die wir jetzt prüfen können, und ist das einfachste solche Modell.
Daher wählen wir für den Bremsweg das quadratische Regressionsmodell.

```{admonition} Mini-Übung
:class: tip
Untersuchen Sie zwei weitere Polynomgrade: Grad 3 und Grad 12.

1. Trainieren Sie für beide Grade ein Modell (Geschwindigkeit mit `MinMaxScaler`
   skalieren, Merkmale mit `PolynomialFeatures` erzeugen, `LinearRegression`
   trainieren). Lassen Sie den R²-Score auf den Trainingsdaten ausgeben sowie
   die Prognose bei 30 km/h und bei 200 km/h.
2. Beurteilen Sie für beide Modelle die **Anpassung** (R²-Score) und die
   **Plausibilität** (sind die beiden Prognosen physikalisch möglich?).
3. Welchen Polynomgrad würden Sie für die Prognose von Bremswegen wählen?
```

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

**Zu 1.**

```python
for grad in [3, 12]:
    skalierer = MinMaxScaler()
    X_skaliert = skalierer.fit_transform(daten[['Geschwindigkeit [km/h]']])

    poly = PolynomialFeatures(degree=grad)
    X = poly.fit_transform(X_skaliert)
    y = daten['Bremsweg [m]']

    modell = LinearRegression()
    modell.fit(X, y)

    r2_training = modell.score(X, y)
    test_geschwindigkeiten = pd.DataFrame({'Geschwindigkeit [km/h]': [30, 200]})
    prognose = modell.predict(poly.transform(skalierer.transform(test_geschwindigkeiten)))
    print(f'Grad {grad}: R2 Training {r2_training:.4f}')
    print(f'  Prognose bei 30 km/h:  {prognose[0]:.1f} m')
    print(f'  Prognose bei 200 km/h: {prognose[1]:.1f} m')
```

**Zu 2.**

| Grad | R² Training | Prognose 30 km/h | Prognose 200 km/h |
| --- | --- | --- | --- |
| 3 | 0.9979 | 9.2 m | 386 m |
| 12 | 0.9987 | 3.2 m | 1 841 946 m |

Grad 3: Die Anpassung ist so gut wie beim quadratischen Modell, beide Prognosen
sind plausibel.

Grad 12: Die Anpassung ist minimal besser, aber die Prognose bei 200 km/h ist mit
über einer Million Metern physikalisch unmöglich. Außerhalb des Datenbereichs
versagt das Modell, ein Zeichen von Overfitting.

**Zu 3.** Grad 2. Ein höherer Grad verbessert die Anpassung nur unwesentlich und
verschlechtert die Plausibilität. Man wählt das einfachste Modell, das alle
Kriterien erfüllt.
````

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir die polynomiale Regression mit `PolynomialFeatures`
kennengelernt und drei Kriterien zur Modellbewertung: **Anpassung** an die
Trainingsdaten, **Generalisierung** auf unabhängige Daten und **Plausibilität**
von Verlauf und Prognosen. Ein hoher R²-Score auf den Trainingsdaten allein
genügt nicht. Ein zu niedriger Polynomgrad führt zu Underfitting, ein zu hoher
zu Overfitting; der Polynomgrad ist ein Hyperparameter. Wie man das Kriterium
Generalisierung misst und Hyperparameter systematisch wählt, sehen wir in
Kapitel 8.
