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

# Übungen

```{admonition} Aufgabe 1
:class: tip
Eine Abalone oder ein Seeohr ist eine Schnecke mit Schale, die einer Ohrmuschel
ähnelt (siehe https://de.wikipedia.org/wiki/Seeohren). Laden Sie den Datensatz
'abalone_DE.csv'. Ziel dieser Aufgabe ist ein Modell zu trainieren, das aus den
Angaben zu Geschlecht, Größe und Gewicht die Anzahl der Ringe prognostiziert.
Die Anzahl der Ringe +1.5 gibt das Alter der Abalone an. 

1. Führen Sie eine Datenexploration durch. Dazu gehören insbesondere 
   * Übersicht
   * statistische Kennzahlen der Eigenschaften
   * Visualisierungen der Eigenschaften
   * Analyse bzgl. Ausreißer
2. Bereinigen Sie den Datensatz. Dazu gehört insbesondere die Entfernung von
   Ausreißern.  
3. Wählen Sie ein Modell.
4. Bereiten Sie die Daten für das Modell auf. Dazu gehört insbesondere auch der
   Split in Trainings- und Testdaten.
5. Validieren Sie das Modell. Erhöhen Sie die Modellkomplexität und beurteilen
   Sie, ob Over- oder Underfitting vorliegt.
6. Kodieren Sie das Geschlecht mit One-Hot-Kodierung und trainieren Sie das
   Modell erneut. Verbessert sich die Prognose?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

data = pd.read_csv('abalone_DE.csv', skiprows=3)
```

```python
data.head(10)
```

Abalone oder Seeohr: https://de.wikipedia.org/wiki/Seeohren

Der Abalone-Datensatz enthält folgende Variablen:

Sex → Geschlecht
Length → Länge (in Millimetern)
Diameter → Durchmesser (senkrecht zur Länge, in Millimetern)
Height → Höhe (mit Fleisch in der Schale, in Millimetern)
Whole weight → Gesamtgewicht (in Gramm)
Shucked weight → Gewicht geschält (Gewicht Fleisch, in Gramm)
Viscera weight → Gewicht der Eingeweide (in Gramm)
Shell weight → Gewicht der Schale (nach dem Trocknen, in Gramm)
Rings → Ringe (+ 1.5 ergibt das Alter der Abalone)

```python
data.info()
```

Der Abalone-Datensatz enthält 4177 gültige Einträge mit 9 Eigenschaften. Der
Datentyp des Geschlechts ist Object. Die physikalischen Eigenschaften der
Abalonen Größe (Länge, Durchmesser und Höhe) und Gewicht (Gesamtgewicht, Gewicht
geschält, Gewicht der Eingeweide, Gewicht der Schale) sind als Floats gegeben.
Die Anzahl der Ringe wird durch einen Integer repräsentiert. Alle Einträge sind
gültig.

Wir untersuchen nacheinander Geschlecht, Größe, Gewicht und Ringe.

```python
data['Geschlecht'].describe()
```

```python
data['Geschlecht'].value_counts()
```

Das Geschlecht enthält drei einzigartige Werte: männlich, Jungtier und weiblich.
Es sind etwas mehr männliche Abalonen im Datensatz enthalten, Jungtiere und
weibliche Abalonen gibt es ungefähr gleich viele.

```python
import plotly.express as px

fig = px.bar(data['Geschlecht'],
             title='Anzahl der Abalonen nach Geschlecht',
             labels={'value': '', 'count': 'Anzahl', 'variable': 'Legende'})
fig.show()
```

Als nächstes betrachten wir die Größe der Abalonen.

```python
data[['Länge [mm]', 'Durchmesser [mm]', 'Höhe [mm]']].describe()
```

```python
fig = px.box(data[['Länge [mm]', 'Durchmesser [mm]', 'Höhe [mm]']],
             title='Größe der Abalonen',
             labels={'variable': '', 'value': 'Größenangabe in mm'})
fig.show()
```

Bei allen drei Größenangaben gibt es Ausreißer nach unten. Auffällig sind jedoch
die beiden Ausreißer bei der Höhe. Die mittlere Höhe sind 0.139516 mm, der
Median liegt bei 0.14 mm. Die beiden Ausreißer haben mit 0.515 mm und 1.13 mm
mehr als die zehnfache Höhe. Um welche Abalonen handelt es sich? 

```python
data[ data['Höhe [mm]'] > 0.5 ].head(2)
```

Abalone 1417 scheint einfach nur groß zu sein, bei Abalone 2051 passt die Höhe
aber nicht zu den ansonsten eher durchschnittlichen Größenangaben. Im Folgenden
eliminieren wir die beiden Ausreißer aus dem Datensatz.

```python
data = data[ data['Höhe [mm]'] <= 0.5 ]
data.info()
```

```python
data[['Länge [mm]', 'Durchmesser [mm]', 'Höhe [mm]']].describe()
```

```python
fig = px.box(data[['Länge [mm]', 'Durchmesser [mm]', 'Höhe [mm]']],
             title='Größe der Abalonen',
             labels={'variable': '', 'value': 'Größenangabe in mm'})
fig.show()
```

Als nächstes betrachten wir die Gewichtsangaben.

```python
data[['Gesamtgewicht [g]', 'Gewicht geschält [g]', 'Gewicht der Eingeweide [g]', 'Gewicht der Schale [g]']].describe()
```

```python
fig = px.box(data[['Gesamtgewicht [g]', 'Gewicht geschält [g]', 'Gewicht der Eingeweide [g]', 'Gewicht der Schale [g]']],
             title='Gewicht der Abalonen',
             labels={'variable': '', 'value': 'Gewicht in g'})
fig.show()
```

Bei den Gewichtsangaben gibt es einige Ausreißer nach oben, aber keine
offensichtlich herausragenden Ausreißer. 

Zuletzt verschaffen wir uns noch einen Überblick über die statistischen
Kennzahlen der Ringe.

```python
data['Ringe'].describe()
```

```python
fig = px.box(data['Ringe'],
             title='Ringe der Abalonen',
             labels={'variable': '', 'value': 'Anzahl'})
fig.show()
```

```python
fig = px.bar(data['Ringe'].value_counts())
fig.show()
```

Mittelwert 9.9 und Median 9 stimmen praktisch überein. Das Histogramm der Ringe
zeigt aber auch eine ganz leichte Rechtsschiefe.

Als nächstes untersuchen wir, welche Wirkung Größe und Gewicht auf die Ringe haben.

```python
fig = px.scatter_matrix(data[['Länge [mm]', 'Durchmesser [mm]', 'Höhe [mm]', 'Ringe']])
fig.show()
```

Je größer eine Abalone ist, desto mehr Ringe scheint sie zu haben.

```python
fig = px.scatter_matrix(data[['Gesamtgewicht [g]', 'Gewicht geschält [g]', 'Gewicht der Eingeweide [g]', 'Gewicht der Schale [g]', 'Ringe']])
fig.show()
```

Auch bei steigenden Gewicht scheint die Anzahl der Ringe zuzunehmen.

Zuletzt trainieren wir ein multiples lineares Regressionsmodell.

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Split der Daten in Trainingsdaten und Testdaten
data_train, data_test = train_test_split(data, random_state=42)

# Wahl des linearen Regressionsmodells
model = LinearRegression()

# Adaption der Daten für das lineare Regressionsmodell
# Geschlecht wird weggelassen, da kategorial
X_train = data_train.loc[:, 'Länge [mm]' : 'Gewicht der Schale [g]']
y_train = data_train['Ringe']

# Training
model.fit(X_train, y_train)

# Validierung
r2_score_train = model.score(X_train, y_train)

X_test = data_test.loc[:, 'Länge [mm]' : 'Gewicht der Schale [g]']
y_test = data_test['Ringe']

r2_score_test = model.score(X_test, y_test)

print(f'R2-Score Trainingsdaten: {r2_score_train:.2f}')
print(f'R2-Score Testdaten: {r2_score_test:.2f}')
```

Bei den Trainingsdaten und bei den Testdaten erzielen wir R²-Scores von ca. 0.55
(leicht variierend je nach zufälliger Aufteilung in Test- und Trainingsdaten).
Damit scheint die gewählte Modellkomplexität für die Daten zu gering zu sein.
Wir erhöhen die Modellkomplexität, gehen also zu einer polynomialen Regression
über. Zu jedem Polynomgrad betrachten wir den jeweiligen R²-Score für
Trainingsdaten und Testdaten.

```python
from sklearn.preprocessing import PolynomialFeatures

for d in [2, 3, 4, 5]:
    polynom_transformator = PolynomialFeatures(degree = d)

    # Adaption der Daten für das lineare Regressionsmodell
    X_train = polynom_transformator.fit_transform(data_train.loc[:, 'Länge [mm]' : 'Gewicht der Schale [g]'])
    y_train = data_train['Ringe']

    # Training
    model.fit(X_train, y_train)

    # Validierung
    r2_score_train = model.score(X_train, y_train)

    X_test = polynom_transformator.transform(data_test.loc[:, 'Länge [mm]' : 'Gewicht der Schale [g]'])
    y_test = data_test['Ringe']

    r2_score_test = model.score(X_test, y_test)

    print(f'Grad: {d} ==> R2-Score Trainingsdaten: {r2_score_train:.2f} | R2-Score Testdaten: {r2_score_test:.2f}')
```

Der Wechsel von einem linearen auf ein quadratisches Regressionspolynom scheint
eine leichte Verbesserung des R2-Wertes zu bringen. Aber bereits bei Grad 3
fällt der R²-Score bei den Testdaten auf 0.25 ab, während er für die
Trainingsdaten auf 0.61 steigt. Damit befinden wir uns bereits im Overfitting. Bei
Grad 4 und 5 sind die R²-Scores sogar negativ. Daher darf allerhöchstens Grad 2
für das Regressionspolynom gewählt werden. Da aber die Verbesserung von Grad 1
auf 2 nur marginal ist, ist weiterhin das lineare multiple Regressionsmodell
empfehlenswert.

Nun beziehen wir noch das Geschlecht ein. Dazu kodieren wir es mit
One-Hot-Kodierung und trainieren dann das lineare multiple Regressionsmodell
erneut.

```python
# One-Hot-Kodierung des Geschlechts
data_kodiert = pd.get_dummies(data, columns=['Geschlecht'])

 # Erneuter Split (mit gleichem random_state für Vergleichbarkeit)
data_train, data_test = train_test_split(data_kodiert, random_state=42)

# Training mit Geschlecht
X_train = data_train.drop(columns=['Ringe'])
y_train = data_train['Ringe']
model.fit(X_train, y_train)

# Validierung
X_test = data_test.drop(columns=['Ringe'])
y_test = data_test['Ringe']
r2_score_test = model.score(X_test, y_test)
print(f'R2-Score mit Geschlecht: {r2_score_test:.2f}')
```

Der R²-Score ist bei den Testdaten minimal von 0.56 auf 0.57 gestiegen. Eine
signifikante Verbesserung des Modells ist es nicht, das Geschlecht mit
hinzuzunehmen.
````

```{admonition} Aufgabe 2
:class: tip
Der Datensatz
'statistic_id226994_annual-average-unemployment-figures-for-germany-2005-2022.csv'
stammt von Statista. Die Daten beschreiben die Entwicklung der
Arbeitslosenzahlen (in Mio.) seit 1991. Im Original-Excel sind einige
Ungereimtheiten, die sich auch so im csv-File befinden.

1. Korrigieren Sie den Datensatz zuerst mit einem Texteditor. 
2. Führen Sie dann eine explorative Datenanalyse durch (Übersicht, statistische
   Kennzahlen, Boxplot und Visualisierung der Arbeitslosenzahlen abhängig vom
   Jahr.)
3. Wählen Sie mehrere ML-Modelle aus. Adaptieren Sie die Daten für das Training
   und lassen Sie die gewählten ML-Modelle trainieren.
4. Validieren Sie Ihr Modell: ist es geeignet? Bewerten Sie die Modelle bzgl.
   Over- und Underfitting.
5. Visualisieren Sie eine Prognose von 1990 bis 2030.
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

data = pd.read_csv('statistic_id226994_korrigiert.csv')
data.info()
```

Der Datensatz enthält 32 Zeilen und zwei Spalten. Das Jahr wird durch Integer repräsentiert, die Arbeitslosenzahl durch Floats.

```python
einzigartige_jahre = len(data['Jahr'].unique())
print(f'Es sind {einzigartige_jahre} verschiedene Jahreszahlen gelistet.')
```

Die Arbeitslosenzahlen sind Floats und alle Einträge sind gültig.

```python
data.describe()
```

```python
import plotly.express as px

fig = px.box(data['Arbeitslosenzahl'],
             title='Arbeitslosenzahlen in Deutschland von 1991 bis 2022',
             labels={'variable':'', 'value': 'Mio. Personen'})
fig.show()
```

Der Median liegt mittig zwischen Q1 und Q3, aber insgesamt gibt es mehrere
Jahre, bei denen mehr als 4 Mio. Arbeitslose (Q3) gibt. Es gibt keine Ausreißer.

+++

Als nächstes visualisieren wir die Arbeitslosenzahlen abhängig vom Jahr.

```python
fig = px.scatter(data, x = 'Jahr', y = 'Arbeitslosenzahl',
             title='Arbeitslosenzahlen in Deutschland von 1991 bis 2022')
fig.show()
```

Aufgrund der Visualisierung ist abzusehen, dass das lineare Regressionsmodell
kein gutes Modell sein wird. Wir probieren polynomiale Regression für Grad 1 bis
10 und notieren den jeweiligen R²-Score.

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures


# Auswahl des Modells
model = LinearRegression()


# Adaption der Daten
data_train, data_test = train_test_split(data, random_state=42)

X_train = data_train[['Jahr']]
y_train = data_train['Arbeitslosenzahl']

X_test = data_test[['Jahr']]
y_test = data_test['Arbeitslosenzahl']

# Training für Polynomgrad 1 bis 5
for grad in [1, 2, 3, 4, 5]:
    polynom_transformator = PolynomialFeatures(degree = grad)

    X_train_transformiert =  polynom_transformator.fit_transform(X_train)
    model.fit(X_train_transformiert, y_train)

    # Validierung mit Testdaten
    r2_score_train = model.score(X_train_transformiert, y_train)
    X_test_transformiert = polynom_transformator.transform(X_test)
    r2_score_test  = model.score(X_test_transformiert, y_test)

    # Vergleich der Modelle
    print(f'Grad {grad}: R2-Score Trainingsdaten: {r2_score_train:.2f} \t R2-Score Testdaten: {r2_score_test}')
```

Ab Grad 3 gibt es keine Veränderung mehr. Der R²-Score für die Testdaten ist
deutlich kleiner als für die Trainingsdaten.  Dies deutet darauf hin, dass das Modell bereits anfängt zu overfitten. Dennoch wählen wir Grad 3, da höhere Grade zu noch schlechteren Testscores führen.

```python

# Wähle Grad 3
polynom_transformator = PolynomialFeatures(degree = 3)

X_train_transformiert =  polynom_transformator.fit_transform(X_train)
model.fit(X_train_transformiert, y_train)

# Validierung mit Testdaten
r2_score_train = model.score(X_train_transformiert, y_train)
X_test_transformiert = polynom_transformator.transform(X_test)
r2_score_test  = model.score(X_test_transformiert, y_test)

# Vergleich der Modelle
print(f'Grad 3: R2-Score Trainingsdaten: {r2_score_train:.2f} \t R2-Score Testdaten: {r2_score_test}')
```

```python
import numpy as np
import plotly.graph_objects as go

# Prognose für die Jahre 1990 bis 2030
prognose = pd.DataFrame()
prognose['Jahr'] = np.arange(1990, 2031)

X_prognose = polynom_transformator.transform(prognose[['Jahr']])
prognose['Arbeitslosenzahl'] = model.predict(X_prognose)

```

```python

fig1 = px.scatter(data, x = 'Jahr', y = 'Arbeitslosenzahl')
fig2 = px.line(prognose, x = 'Jahr', y = 'Arbeitslosenzahl')

fig = go.Figure(fig1.data + fig2.data)
fig.show()
```

Da das von uns gewählte Modell ein Polynom dritten Grades ist, schwingt es für
Jahre nach 2020 wieder nach oben. Dieses Verhalten wird nicht von den
Trainingsdaten gestützt. Daher sollte das Modell nicht für eine Prognose in die
Zukunft genutzt werden.
````
