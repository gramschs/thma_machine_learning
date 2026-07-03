---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 12.3 Neuronale Netze mit Scikit-Learn

```{admonition} Lernziele
:class: attention
* Sie wissen, was die **Architektur** eines neuronalen Netzes ist.
* Sie können mit Scikit-Learn ein neuronales Netz zur Klassifikation trainieren.
* Sie wissen, dass neuronale Netze sensitiv auf unskalierte Daten reagieren
  und daher skaliert werden müssen.
* Sie können neuronale Netze mit Gittersuche und Kreuzvalidierung trainieren.
```

+++

## Neuronale Netze zur Klassifikation

Schauen wir uns an, wie das Training eines neuronalen Netzes in Scikit-Learn
funktioniert. Dazu erzeugen wir zunächst künstliche Daten für eine binäre
Klassifikationsaufgabe, splitten sie in Trainings- und Testdaten und lassen sie
visualisieren.

```{code-cell} ipython3
import pandas as pd
import plotly.express as px
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split

# Generiere künstliche Daten
X, y = make_circles(noise=0.2, factor=0.5, random_state=1)

# Split Trainings- / Testdaten
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=0)

# Konvertierung in ein DataFrame-Objekt für Plotly Express
df = pd.DataFrame({
    'Feature 1': X[:, 0],
    'Feature 2': X[:, 1],
    'Category': pd.Series(y, dtype='category')
})

# Visualisierung
fig = px.scatter(df, x='Feature 1', y='Feature 2', color='Category',
                 title='Künstliche Daten')
fig.show()
```

Die neuronalen Netze sind in dem Untermodul `sklearn.neural_network`. Da es sich
um eine Klassifikationsaufgabe handelt, laden wir das Multilayer-Perzeptron mit
`MLPClassifier`. Mehr Details dazu können wir in der Dokumentation

> [https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier)

nachlesen. Wir lassen das neuronale Netz mit `.fit()` trainieren und geben die
Scores für die Trainings- und Testdaten mit `.score()` aus. Aus didaktischen
Gründen fixieren wir den Zufallsseed mit `random_state=0`.

```{code-cell} ipython3
from sklearn.neural_network import MLPClassifier

# Auswahl des Modells
neuronales_netz = MLPClassifier(random_state=0)

# Training
neuronales_netz.fit(X_train, y_train)

# Validierung 
score_train = neuronales_netz.score(X_train, y_train)
score_test = neuronales_netz.score(X_test, y_test)
print(f'Score für Trainingsdaten: {score_train:.2f}')
print(f'Score für Testdaten: {score_test:.2f}')
```

Beim Training des neuronalen Netzes erscheint die Warnung: `Stochastic
Optimizer: Maximum iterations (200) reached and the optimization hasn't
converged yet.`. Zum Bestimmen der Gewichte des neuronalen Netzes wird ein
iteratives Verfahren verwendet, das Schritt für Schritt die optimalen Gewichte
berechnet. Iterative Verfahren können in eine Endlosschleife geraten. Um das zu
verhindern, wird in der Regel die Anzahl der Schritte (Iterationen) begrenzt.
Die Warnung besagt, dass in unserem Beispiel die Suche nach den optimalen
Gewichten des neuronalen Netzes nach der fest eingestellten Anzahl von 200
Schritten eingestellt wurde. Wir erhöhen diese Zahl auf 2000 mit dem optionalen
Argument `max_iter=2000` und wiederholen das Training.

```{code-cell} ipython3
# Auswahl des Modells mit maximal 2000 Iterationen
neuronales_netz = MLPClassifier(max_iter=2000, random_state=0)

# Training
neuronales_netz.fit(X_train, y_train)

# Validierung 
score_train = neuronales_netz.score(X_train, y_train)
score_test = neuronales_netz.score(X_test, y_test)
print(f'Score für Trainingsdaten: {score_train:.2f}')
print(f'Score für Testdaten: {score_test:.2f}')
```

Jetzt ist die Anzahl der Schritte ausreichend, um das neuronale Netz zu
trainieren.

```{admonition} Hinweis: Daten skalieren
:class: warning
In der Regel ist das Skalieren der Daten besser als das Erhöhen der maximalen
Anzahl an Iterationen. Im Maschinenbau messen wir oft Größen mit sehr
unterschiedlichen Einheiten: Temperaturen (20-100°C), Drücke (1-200 bar) oder
Drehzahlen (0-3000 rpm). Liegen Werte in recht unterschiedlichen Größenordnungen
vor, so wird das Training erschwert. Daher ist es sinnvoll, die Daten auf
ähnliche Größenordnungen zu skalieren.
```

In dem obigen Beispiel sind die künstlichen Daten jedoch bereits in einem
ähnlichen Größenbreich, so dass wir hier keine Skalierung vornehmen müssen.

## Architektur des neuronalen Netzes ändern

Neuronale Netze sind zusammengesetzte künstliche Neuronen. Aber welche
Zusammensetzung liegt hier vor? Wie viele versteckte Schichten gibt es, wie
viele Neuronen sind in den einzelnen versteckten Schichten? Welche
Aktivierungsfunktion wurde verwendet? Die zentralen Bestandteile eines
neuronalen Netzes werden **Architektur** des neuronalen Netzes genannt.

Die Voreinstellung für die Anzahl der versteckten Schichten ist
`hidden_layer_sizes=(100,)`. Dem optionalen Argument `hidden_layer_sizes` wird
ein Tupel mit ganzen Zahlen übergeben, wobei hier das Tupel nur eine Zahl
enthält, nämlich 100. Das bedeutet, dass das neuronale Netz eine versteckte
Schicht hat und diese aus 100 Neuronen besteht. Besteht das Tupel aus mehreren
Zahlen, z.B. `(50, 20, 40)`, dann gibt die die erste Zahl in dem Tupel die
Anzahl der Neuronen in der ersten versteckten Schicht an (also 50), die zweite
Zahl die Anzahl der Neuronen in der zweiten Schicht (also 20) und immer so
weiter.

Jetzt wo wir wissen, dass das neuronale Netz mit der Standardeinstellung
`MLPClassifier()` eine versteckte Schicht mit 100 Neuronen hat, können wir uns
überlegen, wie viele Gewichte das Modell hat. Bei zwei Merkmalen, einer
versteckten Schicht mit 100 Neuronen und einer Ausgabe brauchen wir insgesamt 2
x 100 + 100 + 100 x 1 = 401 Parameter (Gewichte und Bias-Einheiten).
Gleichzeitig haben wir nur 100 Datenpunkte, also nur ein Viertel so viele
Informationen wie Parameter. Damit ist die Gefahr groß, dass Overfitting
vorliegt. Wir wählen zwei versteckte Schichten mit jeweils zwei Neuronen.

```{code-cell} ipython3
# Auswahl des Modells
neuronales_netz = MLPClassifier(max_iter=2000, hidden_layer_sizes=(2,2), random_state=0)

# Training
neuronales_netz.fit(X_train, y_train)

# Validierung 
score_train = neuronales_netz.score(X_train, y_train)
score_test = neuronales_netz.score(X_test, y_test)
print(f'Score für Trainingsdaten: {score_train:.2f}')
print(f'Score für Testdaten: {score_test:.2f}')
```

Die Scores für Trainings- und Testdaten sind schlecht. Wir zeichnen die
Entscheidungsgrenzen ein, um zu sehen, wo das neuronale Netz die Trennlinien
zieht.

```{code-cell} ipython3
:tags: ["hide-input"]
import plotly.graph_objects as go
import numpy as np

# Create grid for contour plot
gridX, gridY = np.meshgrid(np.linspace(-1.5, 1.5, 50), np.linspace(-1.5, 1.5, 50))
gridZ = neuronales_netz.predict_proba(np.column_stack([gridX.ravel(), gridY.ravel()]))[:, 1]
Z = gridZ.reshape(gridX.shape)

# Create scatter plot
scatter = go.Scatter(x=df['Feature 1'], y=df['Feature 2'], mode='markers',
                     marker=dict(color=df['Category'], colorscale='BlueRed_r'))

# Create contour plot
contour = go.Contour(x=np.linspace(-1.5, 1.5, 50), y=np.linspace(-1.5, 1.5, 50), z=Z, 
                     opacity=0.2, colorscale='BlueRed_r')

# Create figure and add plots
fig = go.Figure()
fig.add_trace(contour)
fig.add_trace(scatter)
fig.update_layout(title='Künstliche Messdaten und Entscheidungsgrenzen des neuronalen Netzes',
                  xaxis_title='Feature 1',
                  yaxis_title='Feature 2')
fig.show()
```

Dieses neuronale Netz scheint nicht komplex genug zu sein, um die Daten korrekt
zu klassifizieren.

```{admonition} Mini-Übung
:class: tip
Experimentieren Sie mit verschiedenen Architekturen:
1. Testen Sie `hidden_layer_sizes=(20,)`, also eine Schicht mit 20 Neuronen.
2. Testen Sie `hidden_layer_sizes=(15, 10, 5)`, also drei Schichten.
3. Welche Architektur funktioniert am besten?
4. Was passiert mit sehr großen Netzen wie `hidden_layer_sizes=(100, 100)`?
```

Probieren wir zwei versteckte Schichten mit jeweils fünf Neuronen aus.

```{code-cell} ipython3
# Auswahl des Modells
neuronales_netz = MLPClassifier(max_iter=2000, hidden_layer_sizes=(5,5), random_state=0)

# Training
neuronales_netz.fit(X_train, y_train)

# Validierung 
score_train = neuronales_netz.score(X_train, y_train)
score_test = neuronales_netz.score(X_test, y_test)
print(f'Score für Trainingsdaten: {score_train:.2f}')
print(f'Score für Testdaten: {score_test:.2f}')
```

Erneut lassen wir die Entscheidungsgrenzen visualisieren.

```{code-cell} ipython3
:tags: ["hide-input"]
gridZ = neuronales_netz.predict_proba(np.column_stack([gridX.ravel(), gridY.ravel()]))[:, 1]
Z = gridZ.reshape(gridX.shape)

# Create scatter plot
scatter = go.Scatter(x=df['Feature 1'], y=df['Feature 2'], mode='markers',
                     marker=dict(color=df['Category'], colorscale='BlueRed_r'))

# Create contour plot
contour = go.Contour(x=np.linspace(-1.5, 1.5, 50), y=np.linspace(-1.5, 1.5, 50), z=Z, 
                     opacity=0.2, colorscale='BlueRed_r')

# Create figure and add plots
fig = go.Figure()
fig.add_trace(contour)
fig.add_trace(scatter)
fig.update_layout(title='Künstliche Messdaten und Entscheidungsgrenzen des neuronalen Netzes',
                  xaxis_title='Feature 1',
                  yaxis_title='Feature 2')
fig.show()
```

Die Scores für Trainings- und Testdaten sind gut und die Entscheidungsgrenzen
sind plausibel.

## Optimierung mit Gittersuche

Bisher haben wir die Architektur manuell angepasst. Mit der Gittersuche (Grid
Search) können wir diesen Prozess automatisieren. Die Gittersuche testet
systematisch verschiedene Kombinationen von Parametern und findet die beste
Konfiguration. Dabei wird jede Kombination mit Kreuzvalidierung (Cross
Validation) getestet: Die Trainingsdaten werden in 5 Teile aufgeteilt und das
Modell wird 5-mal trainiert, wobei jedes Mal ein anderer Teil zur Validierung
dient. Neben der Anzahl der versteckten Schichten ändern wir auch noch die
Aktivierungsfunktion. Auch wenn es eigentlich nicht nötig ist, skalieren wir die
Daten, so wie es in der Regel notwendig ist.

```{code-cell} ipython3
import pandas as pd
import plotly.express as px
from sklearn.datasets import make_circles
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler

# Künstliche Daten generieren
X, y = make_circles(noise=0.2, factor=0.5, random_state=1)

# Daten skalieren (wichtig für neuronale Netze!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, random_state=0
)

# Definition des Suchraums
# Wir testen verschiedene Architekturen und Lernraten
gitter = {
    'hidden_layer_sizes': [
        (5,),           # 1 Schicht mit 5 Neuronen
        (10,),          # 1 Schicht mit 10 Neuronen
        (5, 5),        # 2 Schichten mit je 5 Neuronen
        (10, 5),       # 2 Schichten mit 10 und 5 Neuronen
        (10, 10),      # 2 Schichten mit je 10 Neuronen
    ],
    'alpha': [0.0001, 0.001, 0.01],  # Regularisierung (verhindert Overfitting)
    'solver': ['lbfgs', 'adam']      # Solver
}

# Basismodell erstellen
basismodell = MLPClassifier(max_iter=5000, random_state=0)

# Gittersuche mit 5-facher Kreuzvalidierung
gittersuche = GridSearchCV(
    estimator=basismodell,
    param_grid=gitter,
    cv=5  # 5-fache Kreuzvalidierung
)

# Suche starten
print('Starte Gittersuche...')
gittersuche.fit(X_train, y_train)

# Beste Parameter ausgeben
print('Ergebnisse der Gittersuche:')
print(f'beste Parameter: {gittersuche.best_params_}')
print(f'bester Score (Kreuzvalidierung): {gittersuche.best_score_:.2f}')

# Bestes Modell auf Testdaten evaluieren
bestes_modell = gittersuche.best_estimator_
test_score = bestes_modell.score(X_test, y_test)
print(f"Score auf Testdaten: {test_score:.3f}")
```

Für das beste Modell sehen die Entscheidungsgrenzen wie folgt aus.

```{code-cell} ipython3
:tags: ["hide-input"]
gridX, gridY = np.meshgrid(np.linspace(-2.5, 2.5, 100), np.linspace(-2.5, 2.5, 100))
gridZ = bestes_modell.predict_proba(np.column_stack([gridX.ravel(), gridY.ravel()]))[:, 1]
Z = gridZ.reshape(gridX.shape)

# Create scatter plot
scatter = go.Scatter(x=X_scaled[:,0], y=X_scaled[:,1], mode='markers',
                     marker=dict(color=df['Category'], colorscale='BlueRed_r'))

# Create contour plot
contour = go.Contour(x=np.linspace(-2.5, 2.5, 100), y=np.linspace(-2.5, 2.5, 100), z=Z, 
                     opacity=0.2, colorscale='BlueRed_r')

# Create figure and add plots
fig = go.Figure()
fig.add_trace(contour)
fig.add_trace(scatter)
fig.update_layout(title='Künstliche Messdaten und Entscheidungsgrenzen des besten neuronalen Netzes',
                  xaxis_title='Feature 1',
                  yaxis_title='Feature 2')
fig.show()
```

Es ist schwierig, eine gute Architektur des neuronalen Netzes zu finden. Auch
fällt das Ergebnis jedesmal ein wenig anders aus, weil im Hintergrund
stochastische Verfahren für das Trainieren der Gewichte benutzt werden. Aus
diesem Grund sollten neuronale Netze nur eingesetzt werden, wenn sehr große
Datenmengen vorliegen und auch dann noch ist das Finden der besten Architektur
eine große Herausforderung.

## Zusammenfassung und Ausblick

Neuronale Netze sind ein sehr mächtiges Werkzeug, erfordern aber auch große
Datenmengen und ein sorgfältiges Training. In vielen Fällen sollten erst
einfachere ML-Modelle wie beispielsweise das Random-Forest-Modell ausprobiert
werden, das in der Regel einen guten Kompromiss zwischen Geschwindigkeit und
Genauigkeit darstellt, bevor neuronale Netze eingesetzt werden.
