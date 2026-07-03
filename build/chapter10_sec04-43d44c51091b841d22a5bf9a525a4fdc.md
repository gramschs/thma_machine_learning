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

# Übung

Auf der Internetseite
[https://archive.ics.uci.edu/dataset/151/connectionist+bench+sonar+mines+vs+rocks]
finden Sie einen Datensatz mit Sonarsignalen. Die Muster der Signale sind durch
60 Zahlenwerte codiert (es handelt sich um die Energie zu bestimmten Frequenzen,
normalisiert auf \[0,1\]). Darüber hinaus wird angegeben, ob das Sonarsignal
Gestein (= Stein) oder Metall detektiert hat.

Laden Sie nun die Datei 'metall_oder_stein.csv'. Führen Sie eine explorative
Datenanalyse durch. Lassen Sie dann alle Ihnen bekannten Klassifikationsmodelle
trainieren und validieren, um die Materialeigenschaft Stein/Metall auf Basis der
numerischen Werte zu prognostizieren.

```{admonition} Überblick über die Daten
:class: tip
* Welche Daten enthält der Datensatz?
* Wie viele Datenpunkte und Merkmale gibt es?
* Sind die Daten vollständig?
* Welche Datentypen haben die Merkmale?
* Gibt es Merkmale mit unerwarteten Datentypen?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import pandas as pd

# Import der Daten (zwei Kommentarzeilen werden übersprungen)
daten = pd.read_csv('metall_oder_stein.csv', skiprows=2)
daten.info()

# Check der Vollständigkeit:
print(daten.isnull().sum())

# Blick in die Daten:
daten.head(10)
```
Der Datensatz enthält 208 Einträge (Datenpunkte) und 61 Merkmale. Die ersten 60
Merkmale Signal01 bis Signal60 werden durch Floats repräsentiert, das Merkmal
Material wird durch Objekte repräsentiert.

Die Daten sind vollständig.

Die ersten 10 Zeilen zeigen in den Spalten Signal01 bis Signal60 numerische
Werte. In der letzten Spalte Material wird der String 'Stein' aufgelistet. Ein
kurzer Test mit

```python
daten['Material'].unique()
```

zeigt, dass in dieser Spalte lediglich die beiden Einträge 'Stein' und 'Metall'
auftreten. Insgesamt sind die Werte der Merkmale für die Datentypen plausibel.
````

```{admonition} Statistik der numerischen Daten
:class: tip
Erstellen Sie eine Übersicht der statistischen Kennzahlen für die numerischen
Daten. Interpretieren Sie die statistischen Kennzahlen. Gibt es Auffälligkeiten?
Sind die Werte plausibel?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
daten.describe()
```
Die statistischen Kennzahlen lassen sich aufgrund der großen Anzahl an Merkmalen
so kaum interpretieren. Daher hilft hier ein Boxplot der numerischen Daten
weiter.

```python
import plotly.express as px

fig = px.box(daten.drop('Material', axis=1), 
             title='Stein oder Metall',
             labels={'variable': 'Merkmal', 'value':'Wert'})
fig.show()
```
Die Medianwerte scheinen einem Muster zu folgen. Beginnend bei Merkmal Signal01
steigen sie bis zu Signal26, wo der Median den Wert 0.7545 erreicht, um dann
wieder abzufallen. Ab Signal50 liegt der Median unter 0.0179. Bei Eigenschaften
mit einem größeren Median ist auch der Interquartilsabstand (IQR) größer, dafür
gibt es keine Ausreißer. Das Maximum liegt bei 1, was konsistent mit der
Normalisierung auf \[0,1\] ist.
````

```{admonition} Statistik der kategorialen Merkmale
:class: tip
Wie viele Einträge gibt es für Metall oder Stein? Visualisieren Sie die
Verteilung mit einem Balkendiagramm der Klassenverteilung. Ist der Datensatz
ausgewogen?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Berechnung der Anzahl der Einträge
print(daten['Material'].value_counts())

# Visualisierung als Balkendiagramm
fig = px.bar(daten['Material'].value_counts(),
             title='Stein oder Metall')
fig.update_layout(
    yaxis_title='Anzahl',
    xaxis_title='Material',
    showlegend=False
)
fig.show()
```
Im Datensatz sind 111 Proben Metall und 97 Stein. Damit sind 53 % der Proben
Metall und 47 % Stein, was ungefähr gleichverteilt ist.
````

```{admonition} Vorbereitung der Daten für das Training
:class: tip
Bereiten Sie die Daten für das maschinelle Lernen vor:
1. Kodieren Sie die kategoriale Variable Material mit `replace()`.
2. Trennen Sie die Merkmale (Input X) und die Zielgröße (Output y).
3. Teilen Sie die Daten in Trainings- und Testdaten im Verhältnis 80:20 auf.
4. Skalieren Sie - falls notwendig - die Trainingsdaten mit `fit_transform()`
   und die Testdaten mit `transform()`.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from sklearn.model_selection import train_test_split

# Kodierung mit Check (sollte [0 1] ausgeben)
daten['Material'] = daten['Material'].replace({'Stein': '0', 'Metall': '1'}).astype(int)
print(daten['Material'].unique())

# Aufteilung in Input/Output
X = daten.drop('Material', axis=1)
y = daten['Material']

# Split 80:20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Prüfen der Wertebereiche
print(X.min().min(), X.max().max())
```
Da die Signaldaten alle im Intervall \[0,1\] liegen, brauchen wir die Daten
nicht skalieren.
````

```{admonition} ML-Modell Entscheidungsbaum
:class: tip
Trainieren Sie einen Entscheidungsbaum und bewerten Sie das trainierte Modell.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from sklearn.tree import DecisionTreeClassifier

# Instanziierung des Entscheidungsbaums mit Training
modell_baum = DecisionTreeClassifier()
modell_baum.fit(X_train,y_train)

# Bewertung
score_train = modell_baum.score(X_train, y_train)
score_test = modell_baum.score(X_test, y_test)
print(f'Score Trainingsdaten Entscheidungsbaum: {score_train :.2f}')
print(f'Score Testdaten Entscheidungsbaum: {score_test :.2f}')
```
Der Trainingsscore ist 1.00, der Testscore 0.79; ein Zeichen für Overfitting.
````

```{admonition} ML-Modell Random Forest
:class: tip
Trainieren Sie nun einen Random Forest mit 1, 5, 10, 20, 50 und 100 Bäumen auf
denselben Daten. Berechnen Sie wieder die Scores für Training und Test. Wie
unterscheiden sich die Ergebnisse vom einzelnen Entscheidungsbaum? Welches
Random-Forest-Modell würden Sie wählen?

Bewerten Sie darüber hinaus mit der Feature Importance, welche Signale am
wichtigsten sind.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from sklearn.ensemble import RandomForestClassifier

for n in [1, 5, 10, 20, 50, 100]:
    # Instanziierung des Random-Forest-Modells und Training
    modell_rf = RandomForestClassifier(n_estimators=n, random_state=0)
    modell_rf.fit(X_train, y_train)

    # Bewertung
    score_train = modell_rf.score(X_train, y_train)
    score_test = modell_rf.score(X_test, y_test)
    print(f'Anzahl Entscheidungsbäume: {n}')
    print(f'Score Training: {score_train :.2f} | Score Test: {score_test :.2f}')
    print('')

# bestes RF-Modell wählen
modell_rf_final = RandomForestClassifier(n_estimators=50, random_state=0)
modell_rf_final.fit(X_train, y_train)

# Feature Importance extrahieren
importance = pd.DataFrame({
    'Merkmal': X_train.columns,
    'Feature Importance': modell_rf_final.feature_importances_
}).sort_values('Feature Importance', ascending=False)

# die 5 wichtigsten Merkmale anzeigen
importance.head(5)
```
Das Random-Forest-Modell ist besser verallgemeinerbar als der Entscheidungsbaum.
Für einen Random Forest aus 50 Entscheidungsbäumen erhalten wir einen
Trainingsscore von 1.00 und einen Testscore von 0.88. Noch mehr
Entscheidungsbäume führen zu keinem besseren Ergebnis, so dass wir dieses
Modell wählen würden.

Mit dem besten Modell berechnen wir dann die Feature Importance. Am wichtigsten
sind die Signale Signal09 bis Signal12 und Signal52.
````

```{admonition} ML-Modelle SVM und finales Modell
:class: tip
Trainieren Sie nun sowohl eine lineare SVM als auch eine nichtlineare SVM.
Ordnen Sie ein: welches ML-Modell würden Sie final wählen?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from sklearn.svm import SVC

# Instanziierung einer linearen SVM und Training
svm_linear = SVC(kernel='linear', random_state=0)
svm_linear.fit(X_train, y_train)

# Bewertung lineare SVM
score_train = svm_linear.score(X_train, y_train)
score_test = svm_linear.score(X_test, y_test)
print(f'Score Trainingsdaten lineare SVM: {score_train :.2f}')
print(f'Score Testdaten lineare SVM: {score_test :.2f}')

# Instanziierung einer nichtlinearen SVM und Training
svm_rbf = SVC(kernel='rbf', random_state=0)
svm_rbf.fit(X_train, y_train)

# Bewertung nichtlineare SVM
score_train = svm_rbf.score(X_train, y_train)
score_test = svm_rbf.score(X_test, y_test)
print(f'Score Trainingsdaten nichtlineare SVM: {score_train :.2f}')
print(f'Score Testdaten nichtlineare SVM: {score_test :.2f}')
```
Wir erhalten die folgenden Scores (zusammen mit den vorherigen):


| ML-Modell | Score Training | Score Test |
| --- | --- | --- |
| Entscheidungsbaum | 1.00 | 0.79 |
| Random Forest | 1.00 | 0.88 |
| lineare SVM | 0.86 | 0.86 |
| nichtlineare SVM (RBF-Kernel) | 0.88 | 0.79 |

Die lineare SVM generalisiert am besten (gleicher Score auf Train/Test), während
die nichtlineare SVM (mit RBF-Kernel) leichtes Overfitting zeigt (0.88 vs. 0.79)

Obwohl der Random Forest das beste Ergebnis auf den Testdaten erzielt (Testscore
0.88), entscheiden wir uns nicht für dieses Modell. Der Random Forest besteht
aus vielen Entscheidungsbäumen und ist dadurch zwar leistungsstark, aber nur
eingeschränkt interpretierbar.

Die lineare SVM erreicht mit einem Trainings- und Testscore von jeweils 0.86
eine ähnlich gute Prognosegüte wie der Random Forest, zeigt aber keinerlei
Overfitting. Außerdem ist sie deutlich einfacher interpretierbar, da die
Entscheidungsregel auf einem linearen Modell basiert. Die gelernten Gewichte
geben direkt an, wie stark und in welche Richtung jedes Signal die
Klassifikation beeinflusst. Das macht das lineare SVM-Modell transparent.

Daher wählen wir als finales Modell die lineare SVM, da sie stabile Ergebnisse
liefert, gut verallgemeinert und die zugrunde liegende Entscheidungslogik
nachvollziehbar bleibt.
````
