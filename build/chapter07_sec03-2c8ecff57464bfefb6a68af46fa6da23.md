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

In den letzten beiden Kapiteln haben wir uns mit der linearen Regression
befasst, mit einem einzelnen Merkmal und mit mehreren Merkmalen. In diesem
Kapitel erweitern wir die Regression zu quadratischen, kubischen und allgemein
polynomialen Modellen. Außerdem sehen wir, wie man den Polynomgrad geeignet
wählt und warum ein zu hoher Grad die Prognosen außerhalb des Datenbereichs
unbrauchbar macht.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können eine **polynomiale Regression** mit `PolynomialFeatures`
  durchführen.
* [ ] Sie können den **Polynomgrad** geeignet wählen und wissen, dass er ein
  **Hyperparameter** ist.
* [ ] Sie können die **Plausibilität** eines Regressionsmodells anhand von
  Kurvenverlauf und Prognosen prüfen, besonders bei der **Extrapolation** über
  den Datenbereich hinaus.
```

## Künstliches Experiment zu Bremswegen eines Autos

Ausnahmsweise werden wir uns in diesem Kapitel nicht mit dem Verkauf von Autos
beschäftigen, sondern mit dem Bremsweg von Autos. Die Faustformel zur Berechnung
des Bremsweges $s$ in Metern (ohne Reaktionszeit) lautet

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

## Erster Versuch: lineare Regression

Als erstes verwenden wir die lineare Regression, um ein Modell für die Messdaten
zu finden. Wenn wir die Geschwindigkeit mit $x$ bezeichnen und den Bremsweg mit
$y$, dann lautet das lineare Regressionsmodell

$$y = w_0 + w_1 \cdot x.$$

```{code-cell} python
from sklearn.linear_model import LinearRegression

# Daten ins richtige Format bringen
X = daten[['Geschwindigkeit [km/h]']]
y = daten['Bremsweg [m]']

# Training des Modells
modell = LinearRegression()
modell.fit(X, y)

# Bewertung des Modells für die Trainingsdaten
r2_training = modell.score(X, y)
print(f'R2-score Trainingsdaten: {r2_training:.4f}')
```

Der R²-Score sieht mit rund 0.96 gut aus. Um die Prognose zu beurteilen, schauen
wir sie uns über einen Geschwindigkeitsbereich an, der deutlich über die
Trainingsdaten hinausgeht. Weil wir die Daten selbst mit der Faustformel erzeugt
haben, können wir die Prognose zusätzlich mit dieser wahren Kurve vergleichen.

```{code-cell} python
# Geschwindigkeiten für die Prognosekurve, weit über den Datenbereich hinaus
geschwindigkeiten = pd.DataFrame({
    'Geschwindigkeit [km/h]': np.linspace(30, 200, 200)
    })
faustformel = 1/100 * geschwindigkeiten['Geschwindigkeit [km/h]']**2
```

```{code-cell} python
y_prognose = modell.predict(geschwindigkeiten)

fig = px.scatter(daten, x = 'Geschwindigkeit [km/h]', y = 'Bremsweg [m]',
    title='Bremsweg eines Autos: lineares Modell')
fig.add_scatter(x = geschwindigkeiten['Geschwindigkeit [km/h]'], y = y_prognose,
    mode='lines', name='Prognose')
fig.add_scatter(x = geschwindigkeiten['Geschwindigkeit [km/h]'], y = faustformel,
    mode='lines', name='Faustformel')
fig.show()
```

Die Gerade trifft die gekrümmte Punktwolke nur grob. Sie liegt mal über, mal
unter der Faustformel, und im unteren Geschwindigkeitsbereich sagt sie sehr
kleine, unter etwa 39 km/h sogar negative Bremswege voraus. Für den gekrümmten
Zusammenhang ist eine Gerade zu einfach. Wir probieren als nächstes ein
quadratisches Modell.

## Quadratische Regression

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
polynom_transformator = PolynomialFeatures(degree = 2)
X = polynom_transformator.fit_transform(daten[['Geschwindigkeit [km/h]']])
y = daten['Bremsweg [m]']
```

Wichtig: `fit_transform()` lernt die Transformation aus den Trainingsdaten und
wendet sie an, `transform()` wendet nur die bereits gelernte Transformation an.

Danach können wir das multiple lineare Regressionsmodell trainieren und bewerten
lassen.

```{code-cell} python
# Training des Modells
modell = LinearRegression()
modell.fit(X, y)

# Bewertung des Modells für die Trainingsdaten
r2_training = modell.score(X, y)
print(f'R2-score Trainingsdaten: {r2_training:.4f}')
```

Für die Prognosekurve müssen wir auch die neuen Geschwindigkeiten mit demselben
Transformator umformen. Wir nutzen dazu die `transform()`-Methode.

```{code-cell} python
X_neu = polynom_transformator.transform(geschwindigkeiten)
y_prognose = modell.predict(X_neu)

fig = px.scatter(daten, x = 'Geschwindigkeit [km/h]', y = 'Bremsweg [m]',
    title='Bremsweg eines Autos: quadratisches Modell')
fig.add_scatter(x = geschwindigkeiten['Geschwindigkeit [km/h]'], y = y_prognose,
    mode='lines', name='Prognose')
fig.add_scatter(x = geschwindigkeiten['Geschwindigkeit [km/h]'], y = faustformel,
    mode='lines', name='Faustformel')
fig.show()
```

Prognose und Faustformel sind im gesamten Bereich kaum zu unterscheiden, auch
weit über 150 km/h hinaus. Der R²-Score ist mit rund 0.998 höher als beim
linearen Modell. Das quadratische Modell passt also gut.

## Die Wahl des Polynomgrads

Mit demselben Trick können wir die Merkmale auch mit 3, 4 oder mehr potenzieren
und so Polynome beliebigen Grades trainieren. Ein höherer Grad ist aber nicht
automatisch besser. Wir probieren Grad 6.

```{code-cell} python
# Merkmale bis zur 6. Potenz erzeugen
polynom_transformator = PolynomialFeatures(degree = 6)
X = polynom_transformator.fit_transform(daten[['Geschwindigkeit [km/h]']])
y = daten['Bremsweg [m]']

# Training des Modells
modell = LinearRegression()
modell.fit(X, y)

# Bewertung des Modells für die Trainingsdaten
r2_training = modell.score(X, y)
print(f'R2-score Trainingsdaten: {r2_training:.4f}')

# Prognose bei 200 km/h
prognose_200 = modell.predict(
    polynom_transformator.transform(pd.DataFrame({'Geschwindigkeit [km/h]': [200]})))
print(f'Prognose bei 200 km/h: {prognose_200[0]:.0f} m')
```

```{code-cell} python
X_neu = polynom_transformator.transform(geschwindigkeiten)
y_prognose = modell.predict(X_neu)

fig = px.scatter(daten, x = 'Geschwindigkeit [km/h]', y = 'Bremsweg [m]',
    title='Bremsweg eines Autos: Polynom 6. Grades')
fig.add_scatter(x = geschwindigkeiten['Geschwindigkeit [km/h]'], y = y_prognose,
    mode='lines', name='Prognose')
fig.add_scatter(x = geschwindigkeiten['Geschwindigkeit [km/h]'], y = faustformel,
    mode='lines', name='Faustformel')
# y-Achse begrenzen, damit die Messdaten erkennbar bleiben
fig.update_yaxes(range=[0, 500])
fig.show()
```

Der R²-Score auf den Trainingsdaten ist mit rund 0.998 nicht besser als beim
quadratischen Modell. Im Datenbereich bis 150 km/h liegt die Prognose weiterhin
dicht an der Faustformel. Außerhalb des Datenbereichs verhält sich das Modell
aber ganz anders: Ab etwa 150 km/h weicht die Kurve immer stärker ab, und bei
200 km/h prognostiziert das Polynom 6. Grades einen Bremsweg von rund 835 m,
während die Faustformel 400 m ergibt.

Ein Polynom hohen Grades hat viele Freiheitsgrade. Innerhalb der Daten werden sie
durch die Messpunkte festgelegt, außerhalb nicht. Dort kann die Kurve praktisch
beliebig ausschlagen. Der höhere Grad verbessert die Anpassung an die
Trainingsdaten also kaum, macht die Prognosen außerhalb des Datenbereichs aber
unzuverlässig. Man nennt das die schlechte **Extrapolation** von Polynomen hohen
Grades.

### Der Polynomgrad ist ein Hyperparameter

Der Polynomgrad wird vor dem Training festgelegt und nicht aus den Daten gelernt.
Solche Werte heißen Hyperparameter, wie schon die maximale Tiefe bei den
Entscheidungsbäumen in Kapitel 6.3.

```{admonition} Was ist ... ein Hyperparameter?
:class: note
Ein Hyperparameter ist ein Parameter, der vor dem Training eines Modells
festgelegt wird und nicht aus den Daten während des Trainings gelernt wird. Die
Hyperparameter steuern den gesamten Lernprozess und haben einen wesentlichen
Einfluss auf die Leistung des Modells.
```

Wir fassen die drei Modelle zusammen. Der wahre Bremsweg bei 200 km/h beträgt
nach der Faustformel 400 m.

| Polynomgrad | R² (Trainingsdaten) | Prognose bei 200 km/h |
| --- | --- | --- |
| 1 | 0.9641 | 288 m |
| 2 | 0.9979 | 396 m |
| 6 | 0.9979 | 835 m |

Grad 1 ist zu einfach: Die Prognose bleibt mit 288 m deutlich unter dem wahren
Wert. Grad 2 trifft mit 396 m fast genau. Grad 6 verbessert die Anpassung nicht
und liefert außerhalb des Datenbereichs mit 835 m einen unrealistischen Wert.

```{admonition} Faustregel: Polynomgrad wählen
:class: tip
* Beginnen Sie mit einem niedrigen Grad (1 oder 2).
* Erhöhen Sie den Grad nur, wenn die Anpassung an die Daten dadurch sichtbar
  besser wird.
* Prüfen Sie den Kurvenverlauf: Bleibt er glatt und plausibel, auch etwas
  außerhalb des Datenbereichs?
* Wählen Sie im Zweifel den niedrigeren Grad, das einfachere Modell.
```

Systematische Methoden, um Hyperparameter wie den Polynomgrad zu wählen, lernen
wir in Kapitel 8 kennen.

```{admonition} Mini-Übung
:class: tip
Trainieren Sie ein polynomiales Regressionsmodell mit Grad 4.

1. Lassen Sie den R²-Score auf den Trainingsdaten ausgeben.
2. Lassen Sie die Prognose für 200 km/h ausgeben.
3. Vergleichen Sie beide Werte mit dem quadratischen Modell (Grad 2). Welchen
   Grad würden Sie für die Prognose von Bremswegen wählen?
```

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
polynom_transformator = PolynomialFeatures(degree=4)
X = polynom_transformator.fit_transform(daten[['Geschwindigkeit [km/h]']])
y = daten['Bremsweg [m]']

modell = LinearRegression()
modell.fit(X, y)

print(f'R2-score Trainingsdaten: {modell.score(X, y):.4f}')

prognose_200 = modell.predict(
    polynom_transformator.transform(pd.DataFrame({'Geschwindigkeit [km/h]': [200]})))
print(f'Prognose bei 200 km/h: {prognose_200[0]:.0f} m')
```

Der Trainings-R² ist mit rund 0.998 praktisch identisch mit dem des
quadratischen Modells. Die Prognose bei 200 km/h ist mit rund 354 m weiter von
der Faustformel (400 m) entfernt als beim quadratischen Modell (396 m). Grad 4
bringt hier keinen Vorteil. Man wählt Grad 2.
````

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir die polynomiale Regression mit `PolynomialFeatures`
kennengelernt. Der Polynomgrad ist ein Hyperparameter, der vor dem Training
festgelegt wird. Ein zu niedriger Grad beschreibt einen gekrümmten Zusammenhang
nicht gut. Ein zu hoher Grad verbessert die Anpassung kaum, macht die Prognosen
außerhalb des Datenbereichs aber unzuverlässig. In der Praxis beginnt man mit
einem niedrigen Grad und erhöht ihn nur, wenn es die Anpassung sichtbar
verbessert und der Kurvenverlauf plausibel bleibt. Systematische Methoden zur
Wahl von Hyperparametern folgen in Kapitel 8.
