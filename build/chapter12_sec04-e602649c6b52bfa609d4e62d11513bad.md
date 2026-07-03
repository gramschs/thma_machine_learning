---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
    file: ./data/diamonds_DE.csv
    title: diamonds_DE.csv
---

# Übung

Der Datensatz {download}`./data/diamonds_DE.csv` enthält die Preise und Eigenschaften
von Diamanten. Die Eigenschaften sind:

* Karat (Gewicht des Diamanten)
* Schliff (Qualität: befriedigend, gut, sehr gut, erstklassig, ideal)
* Farbe des Diamanten (von J (schlechteste) bis D (beste))
* Reinheit - ein Maß für die Klarheit des Diamanten (I1 (schlechteste), SI2,
  SI1, VS2, VS1, VVS2, VVS1, IF (beste))
* Tiefe (Gesamttiefe in Prozent = z / Mittelwert (x, y) = 2 * z / (x + y))
* Tafel (Breite der Oberseite des Diamanten im Verhältnis zur breitesten Stelle)
* Preis (in US-Dollar)
* x - Länge in mm
* y - Breite in mm
* z - Tiefe in mm

Bearbeiten Sie die folgenden Aufgaben. Vorab können Sie die folgenden Module
importieren. Schreiben Sie Ihre Antworten als Kommentar oder in eine
Markdown-Zelle. Lassen Sie das Jupyter Notebook am Ende noch einmal komplett
ausführen, bevor Sie es abgeben.

```{code-cell}
# import numpy as np
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# from sklearn.linear_model import LinearRegression, LogisticRegression, Perceptron
# from sklearn.model_selection import train_test_split, cross_validate, KFold, GridSearchCV
# from sklearn.neural_network import MLPClassifier, MLPRegressor
# from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler, StandardScaler
# from sklearn.svm  import SVC, SVR
# from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree

# pd.DataFrame.iteritems = pd.DataFrame.items
```

## Explorative Datenanalyse

```{admonition} Import und Bereinigung der Daten
:class: tip
Importieren Sie die Daten 'diamonds_DE.csv'. Verschaffen Sie sich einen
Überblick und beantworten Sie folgende Fragen in einer Markdown-Zelle:

* Wie viele Diamanten enthält die Datei?
* Wie viele Merkmale/Attribute/Eigenschaften/Features sind in den Daten enthalten?
* Sind alle Einträge gültig? Wenn nein, wie viele Einträge sind nicht gültig?
* Welchen Datentyp haben die einzelnen Attribute/Eigenschaften/Features?

Falls der Datensatz ungültige Werte aufweist oder Unstimmigkeiten enthält,
bereinigen Sie ihn.
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
daten = pd.read_csv('diamonds_DE.csv', skiprows=3)
daten.info()
```

```python
daten.head()
```

Der Datensatz enthält 53940 Diamanten mit 11 Attributen/Eigenschaften. Alle
Einträge sind gültige Einträge. Die Eigenschaften 'Unnamed: 0' und 'Preis' sind
Integer. Die Eigenschaften 'Karat', 'Tiefe', 'Tafel', 'x', 'y' und 'z' sind
Floats. Die Eigenschaften 'Schliff', 'Farbe' und 'Reinheit' sind Objekte.

Der Datensatz enthält nur gültige Werte, aber sollte dennoch bereinigt werden,
da die ersten fünf Zeilen des Datensatzes nahelegen, dass die Eigenschaft
'Unnamed: 0' ein Index ist. Wir visualisieren diese Eigeschaft, um die Hypothese
zu überprüfen.

```python
fig = px.scatter(daten, y = 'Unnamed: 0',
                 title='Diamanten')
fig.show()
```

Tatsächlich stimmen (zumindest visuell) der automatisch erzeugte Index des
DataFrame-Objektes und die Werte von 'Unnamed: 0' überein. Die überflüssige
Spalte wird gelöscht.

```python
daten = daten.drop(columns='Unnamed: 0')
daten.info()
```
````

```{admonition} Statistische Kennzahlen der numerischen Eigenschaften
:class: tip
* Ermitteln Sie von den numerischen Eigenschaften die statistischen Kennzahlen
  und visualisieren Sie sie. Verwenden Sie beim Plot eine aussagefähige
  Beschriftung.
* Interpretieren Sie jede Eigenschaft anhand der statistischen Kennzahlen und
  der Plots.
* Bereinigen Sie bei Ungereimtheiten den Datensatz weiter.
* Entfernen Sie Ausreißer.
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
numerische_merkmale = ['Karat', 'Tiefe', 'Tafel', 'Preis', 'x', 'y', 'z']
daten.describe()
```

```python
fig = px.box(daten, y = numerische_merkmale,
             title='Diamanten: numerische Eigenschaften',
             labels={'variable': 'Eigenschaft', 'value': 'Wert'})
fig.show()
```

Die Skalen der einzelnen Eigenschaften sind stark verschieden, so dass ein
gemeinsamer Boxplot nicht möglich ist. Daher werden die Eigenschaften einzeln
oder in vergleichbaren Gruppen sortiert.

```python
fig = px.box(daten, y = 'Karat',
             title='Diamanten')
fig.show()
```

75 % der Diamanten haben ein Karat und weniger, wobei der Median bei 0.7 Karat
liegt. Das ist etwas niedriger als der Mittelwert von 0.8 Karat. Der höhere
Mittelwert wird sicherlich bedingt durch die vielen Ausreißer nach oben ab 2 bis
ca. 5 Karat.

Als nächstes werden Tiefe und Tafel untersucht.

```python
fig = px.box(daten, y = ['Tiefe', 'Tafel'],
             title='Diamanten: numerische Eigenschaften',
             labels={'variable': 'Eigenschaft', 'value': 'Größe'})
fig.show()
```

50 % aller Diamanten haben eine Tiefe zwischen 61 % und 62 %. Der Median ist mit
61.8 % mittig zwischen Q1 und Q3 und stimmt mit dem Mittelwert 61.7 % überein.
Es gibt Ausreißer nach oben und unten.

Bei der Breite ist der Median 57 näher am Q1-Wert 56 und und liegt auch etwas
unterhalb des Mittelwertes von 57.4.

```python
fig = px.box(daten, y = ['x', 'y', 'z'],
             title='Diamanten: numerische Eigeschaften',
             labels={'variable': 'Eigenschaft', 'value': 'Wert'})
fig.show()
```

Der Boxplot sowie die statistischen Kennzahlen der Eigenschaften x, y und z
zeigen Ungereimtheiten. Bei allen drei Eigenschaften wird auch der Wert Null
angenommen. Das ist unmöglich, daher müssen diese Diamanten aus dem Datensatz
entfernt werden.

```python
daten[ daten['x'] == 0 ] 
```

```python
daten[ daten['y'] == 0 ]
```

```python
daten[ daten['z'] == 0 ]
```

Es ist mühsam, die Indizes (Zeilennummern) abzuschreiben. Daher benutzen wir das
Attribut `.index`, um die Indizes direkt der drop()-Methode als Argument zu
übergeben.

```python
zeilen = daten[ daten['x'] == 0 ].index
daten = daten.drop(zeilen)

zeilen = daten[ daten['y'] == 0 ].index
daten = daten.drop(zeilen)

zeilen = daten[ daten['z'] == 0 ].index
daten = daten.drop(zeilen)

daten.info()
```

Darüber hinaus gibt es bei der Größe in y-Richtung zwei deutliche Ausreißer mit
31.8 mm und 58.9 mm. Auch bei der Größe in z-Richtung gibt es einen deutlichen
Ausreißer nach oben mit z = 31.8 mm. Diese Diamanten werden ebenfalls entfernt.

```python
zeilen = daten[ daten['y'] > 31.0 ].index
daten = daten.drop(zeilen)

zeilen = daten[ daten['z'] > 31.0 ].index
daten = daten.drop(zeilen)

daten.info()
```

Somit sind es nur 53917 Einträge von ehemals 53940 Einträgen. Es wurden 23
Diamanten entfernt.

Zuletzt betrachten wir noch den Preis.

```python
fig = px.box(daten, y = 'Preis',
             title='Diamanten: numerische Eigenschaften')
fig.show()
```

Der Median von 2401 US-Dollar liegt nicht mittig zwischen Q1 und Q3 und ist
deutlich niedriger als der Mittelwert von 3932 US-Dollar. Die Preise müssen sehr
asymmetrisch verteilt sein.

```python
fig = px.histogram(daten['Preis'],
                   title='Histogramm des Diamantenpreises',
                   labels={'value':'Preis in US-Dollar', 'count': 'Anzahl'})
fig.show()
```

Die Verteilung der Preise ist rechtsschief (linkssteil).
````

```{admonition} Statistische Kennzahlen (kategoriale Eigenschaften)
:class: tip
* Ermitteln Sie, wie häufig jeder Wert einer Kategorie in der jeweiligen Spalte
  vorkommt.
* Lassen Sie die Anzahl der Werte auch visualisieren. Beschriften Sie die
  Diagramme mit einem aussagefähigen Titel.
* Fassen Sie die Ergebnisse bzw. die Interpretation davon jeweils kurz zusammen
  (in einer Markdown-Zelle).
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
for kategorie in ['Schliff', 'Farbe', 'Reinheit']:
    print(f'Eigenschaft {kategorie}: {daten[kategorie].unique()}')

```

```python
daten['Schliff'].unique()
daten['Schliff'].value_counts()
```

```python
fig = px.bar(daten['Schliff'].value_counts(),
             title='Schliff der Diamanten',
             labels={'value': 'Anzahl', 'index': 'Qualität', 'variable':'Legende'})
fig.show()
```

In dem Datensatz kommen überraschend viele Diamanten der Qualität ideal vor. Die
Anzahl der Diamanten in den einzelnen Qualitätsstufen nimmt immer weiter ab.

```python
fig = px.bar(daten['Farbe'].value_counts(),
             title='Farbe der Diamanten',
             labels={'value': 'Anzahl', 'index': 'Farbname', 'variable':'Legende'})
fig.show()
```

Am häufigsten kommt die Farbe G vor, am seltesten ist Farbe J.

```python
fig = px.bar(daten['Reinheit'].value_counts(),
             title='Reinheit der Diamanten',
             labels={'value': 'Anzahl', 'index': 'Reinheitskategorie', 'variable':'Legende'})
fig.show()
```

I1 ist die schlechteste Reinheit und kommt auch am seltesten vor. IF ist die
beste Reinheitskategorie und kommt am zweitseltesten vor. Die meisten Diamanten
im Datensatz haben eine mittlere Reinheitsstufe SI1.
````

## ML-Modelle

```{admonition} Regression (ohne neuronales Netz)
:class: tip
Ziel der Regressionsaufgabe ist es, den Preis der Diamanten zu prognostizieren.

* Wählen Sie zwei Regressionsmodelle (kein neuronales Netz, das kommt später)
  aus.
* Wählen Sie für jedes der zwei Modelle eine oder mehrere Eigenschaften aus, die
  Einfluss auf den Preis haben könnten. Begründen Sie Ihre Auswahl.
* Adaptieren Sie die Daten jeweils passend zu den von Ihnen gewählten Modellen.
* Falls notwendig, skalieren Sie die Daten.
* Führen Sie einen Split der Daten in Trainings- und Testdaten durch.
* Trainieren Sie jedes ML-Modell.
* Validieren Sie jedes ML-Modell bzgl. der Trainingsdaten und der Testdaten.
* Bewerten Sie abschließend: welches der zwei Modelle würden Sie empfehlen?
  Begründen Sie Ihre Empfehlung.
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
Wahl der Regressionsmodelle: lineare Regression und SVM.

```python
fig = px.scatter_matrix(daten.loc[:, ['Karat', 'Tiefe', 'Tafel', 'x', 'y', 'z', 'Preis']])
fig.show()
```

Karat (Gewicht des Diamanten) scheint von der Größe (x, y und z) abzuhängen. Es
ist zunächst kein linearer Zusammenhang zwischen Tiefe/Tafel und dem Preis
erkennbar. Im Folgenden wird daher für die lineare Regression nur Karat als
Input gewählt.

```python
selected_data = daten.loc[:, ['Karat']]

scaler = StandardScaler()
scaler.fit(selected_data)
input_numerical = scaler.transform(selected_data)

X_train, X_test, y_train, y_test = train_test_split(input_numerical, daten['Preis'], random_state=0)
```

```python
model_linear_regression = LinearRegression()
model_linear_regression.fit(X_train, y_train)

score_train = model_linear_regression.score(X_train, y_train)
score_test = model_linear_regression.score(X_test, y_test)

print(f'Score Trainingsdaten: {score_train:.2f}')
print(f'Score Testdaten: {score_test:.2f}')
```

Support Vector Machines beherrschen auch nichtlineare Zusammenhänge. Es werden
daher alle Features verwendet.

```python
selected_data = daten.loc[:, ['Karat', 'Tiefe', 'Tafel', 'x', 'y', 'z']]

scaler = StandardScaler()
scaler.fit(selected_data)
input_numerical = scaler.transform(selected_data)

X_train, X_test, y_train, y_test = train_test_split(input_numerical, daten['Preis'], random_state=0)
```

```python
model_svr = SVR()
model_svr.fit(X_train, y_train)

score_train = model_svr.score(X_train, y_train)
score_test = model_svr.score(X_test, y_test)

print(f'Score Trainingsdaten: {score_train:.2f}')
print(f'Score Testdaten: {score_test:.2f}')
```

Zusammenfassung der Scores für die Testdaten:

lineare Regression: 0.85
Support Vector Machines: 0.55

Die lineare Regression erreicht bessere Testscores als die SVM, daher ist dieses
Modell zu bevorzugen.
````

```{admonition} Regression mit neuronalem Netz
:class: tip
* Trainieren Sie ein `MLPRegressor` mit den numerischen Eigenschaften (Karat,
   Tiefe, Tafel, x, y, z).
* Skalieren Sie die Daten mit `StandardScaler`.
* Setzen Sie `max_iter=2000` und `random_state=0`, um konsistente Ergebnisse zu
  erhalten.
* Experimentieren Sie manuell mit verschiedenen Architekturen:
   * `hidden_layer_sizes=(10,)`
   * `hidden_layer_sizes=(20, 10)`
   * `hidden_layer_sizes=(50, 25, 10)`
* Notieren Sie für jede Architektur die Scores für Trainings- und Testdaten.
* Verwenden Sie dann Gittersuche, um systematisch die beste Architektur zu
  finden. Testen Sie dabei:
   * `hidden_layer_sizes`: [(10,), (20,), (10, 10), (20, 10)]
   * `alpha`: [0.001, 0.01]
* Vergleichen Sie das beste neuronale Netz mit der linearen Regression aus der
  vorherigen Aufgabe.
* Bewerten Sie: Wann lohnt sich der Einsatz eines neuronalen Netzes?
```

````{admonition} Lösung
:class: tip
:class: dropdown

**Datenvorbereitung**

```python
# Auswahl der numerischen Eigenschaften
selected_data = daten.loc[:, ['Karat', 'Tiefe', 'Tafel', 'x', 'y', 'z']]

# Skalierung (wichtig für neuronale Netze!)
scaler = StandardScaler()
scaler.fit(selected_data)
input_numerical = scaler.transform(selected_data)

# Train-Test-Split
X_train, X_test, y_train, y_test = train_test_split(
    input_numerical, daten['Preis'], random_state=0
)
```

**Manuelle Experimente mit verschiedenen Architekturen**

```python
from sklearn.neural_network import MLPRegressor

# Architektur 1: Eine Schicht mit 10 Neuronen
model_nn1 = MLPRegressor(hidden_layer_sizes=(10,), max_iter=2000, random_state=0)
model_nn1.fit(X_train, y_train)

score_train = model_nn1.score(X_train, y_train)
score_test = model_nn1.score(X_test, y_test)
print('Architektur (10,):')
print(f'  Score Trainingsdaten: {score_train:.2f}')
print(f'  Score Testdaten: {score_test:.2f}')
```

Mit `max_iter=2000` erscheint eine Konvergenz-Warnung. Wenn wir `max_iter`
erhöhen (z.B. auf 10000), konvergiert der Algorithmus und liefert einen Score
von 0.88.

```python
# Architektur 2: Zwei Schichten mit 20 und 10 Neuronen
model_nn2 = MLPRegressor(hidden_layer_sizes=(20, 10), max_iter=2000, random_state=0)
model_nn2.fit(X_train, y_train)

score_train = model_nn2.score(X_train, y_train)
score_test = model_nn2.score(X_test, y_test)
print('Architektur (20, 10):')
print(f'  Score Trainingsdaten: {score_train:.2f}')
print(f'  Score Testdaten: {score_test:.2f}')
```

Ein Trainingsscore von 0.88 und ein Testscore von 0.88 sind gute Ergebnisse.
Dabei mussten wir die Anzahl der Iterationen nicht hochsetzen und der
Algorithmus berechnete die Parameter des neuronalen Netzes deutlich schneller
(ca. 15 s) als bei Fall 1 (ca. 1 min 30 s).

```python
# Architektur 3: Drei Schichten mit 50, 25 und 10 Neuronen
model_nn3 = MLPRegressor(hidden_layer_sizes=(50, 25, 10), max_iter=2000, random_state=0)
model_nn3.fit(X_train, y_train)

score_train = model_nn3.score(X_train, y_train)
score_test = model_nn3.score(X_test, y_test)
print('Architektur (50, 25, 10):')
print(f'  Score Trainingsdaten: {score_train:.2f}')
print(f'  Score Testdaten: {score_test:.2f}')
```

Erneut erhalten wir einen Trainings- und Testscore von 0.88. Die Rechenzeit ist
vergleichbar mit Fall 2 und liegt bei ca. 20 s. Eine Erhöhung der maximalen
Anzahl von Iterationen ist nicht notwendig.

**Systematische Optimierung mit Gittersuche**

```python
from sklearn.model_selection import GridSearchCV

# Definition des Suchraums
gitter = {
    'hidden_layer_sizes': [(10,), (20,), (10, 10), (20, 10)],
    'alpha': [0.001, 0.01]  # Regularisierung
}

# Basismodell
basismodell = MLPRegressor(max_iter=2000, random_state=0)

# Gittersuche mit 5-facher Kreuzvalidierung
# Hinweis: Die Gittersuche kann je nach Computer mehr als 15 Minuten dauern,
# da 8 Konfigurationen mit jeweils 5-facher Kreuzvalidierung getestet werden.
gittersuche = GridSearchCV(
    estimator=basismodell,
    param_grid=gitter,
    cv=5,
    verbose=1  # Zeigt Fortschritt
)

print('Starte Gittersuche...')
gittersuche.fit(X_train, y_train)

# Beste Parameter
print('Ergebnisse der Gittersuche:')
print(f'   beste Architektur: {gittersuche.best_params_["hidden_layer_sizes"]}')
print(f'   bester Alpha-Wert: {gittersuche.best_params_["alpha"]}')
print(f'   bester Score (Kreuzvalidierung): {gittersuche.best_score_:.2f}')

# Test auf ungesehenen Daten
bestes_modell = gittersuche.best_estimator_
test_score = bestes_modell.score(X_test, y_test)
print(f'Score auf Testdaten: {test_score:.2f}')
```

**Vergleich mit linearer Regression**

Aus der vorherigen Aufgabe:
- Lineare Regression (nur Karat): Score Testdaten = 0.85
- Support Vector Machine (alle Features): Score Testdaten = 0.55

Neuronales Netz (alle numerischen Features): Score Testdaten = 0.88

Das neuronale Netz erreicht mit allen Features den besten Score!

**Interpretation und Bewertung**

Das neuronale Netz kann die komplexen nichtlinearen Zusammenhänge zwischen den
Eigenschaften (Karat, Abmessungen, Tiefe, Tafel) und dem Preis etwas besser
erfassen als die lineare Regression. Das neuronale Netz verbessert die
Vorhersagegenauigkeit um 3 Prozentpunkte (von 0.85 auf 0.88).

Wann lohnt sich der Einsatz eines neuronalen Netzes?

Pro neuronales Netz:
- Bei komplexen, nichtlinearen Zusammenhängen
- Wenn ausreichend Daten vorhanden sind (hier: >50.000 Datenpunkte)
- Wenn höchste Genauigkeit wichtig ist
- Wenn Rechenzeit keine große Rolle spielt

Contra neuronales Netz:
- Training dauert länger als bei linearer Regression
- Schwieriger zu interpretieren ("Black Box")
- Architektur muss aufwändig optimiert werden
- Bei kleinen Datenmengen (<1000 Punkte) oft Overfitting

Fazit: Für diesen Datensatz ist das neuronale Netz die beste Wahl. Allerdings
ist der Vorteil gegenüber der linearen Regression (0.88 vs 0.85) relativ gering.
In der Praxis müsste abgewogen werden, ob der Mehraufwand (längere Rechenzeit,
schwierigere Interpretation, aufwändige Architektur-Optimierung) den geringen
Genauigkeitsgewinn rechtfertigt.
````
