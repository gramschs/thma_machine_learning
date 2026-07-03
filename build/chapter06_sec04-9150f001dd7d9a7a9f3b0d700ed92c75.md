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

## Aufgabe 6.1

Das Schiff Titanic galt bei seiner Fertigstellung als unsinkbar. 1912
kollidierte die Titanic mit einem Eisberg und sank. Bei dem Unglück kamen 1514
von 2220 Personen ums Leben, so dass der Titanic-Untergang zu den größten
Unglücken der Schifffahrt zählt. Mehr Informationen zu der Titanic finden Sie
bei Wikipedia
[https://de.wikipedia.org/wiki/Titanic_(Schiff)](https://de.wikipedia.org/wiki/Titanic_(Schiff)).

In der folgenden Übung werden Passagierlisten der Titanic benutzt, um die
Überlebenswahrscheinlichkeit zu prognostizieren (0 = gestorben, 1 = überlebt),
deren Quelle hier ist:
[https://www.kaggle.com/c/titanic](https://www.kaggle.com/c/titanic).

Laden sie den Datensatz 'titanic_DE_cleaned.csv'.

### EDA Titanic

Führen Sie eine explorative Datenanalyse (EDA) durch, indem  Sie Python-Code in
Code-Zellen ausführen und schreiben Sie in Markdown-Zellen Ihre Antworten.

```{admonition} Überblick über die Daten
:class: tip
Welche Daten enthält der Datensatz? Wie viele Personen sind in der Tabelle
enthalten? Wie viele Merkmale werden dort beschrieben? Sind die Daten
vollständig?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import pandas as pd 
daten = pd.read_csv('titanic_DE_cleaned.csv')

daten.info()
```

Der Datensatz enthält 183 Einträge, also 183 Personen. Es gibt 11 Merkmale. Die
Daten sind vollständig. Für jedes Merkmal werden 183 non-null Einträge
angezeigt.
````

```{admonition} Datentypen
:class: tip
Welchen Datentyp haben die Merkmale? Welche Merkmale sind numerisch und welche
sind kategorial?
```

````{admonition} Lösung
:class: tip
:class: dropdown
Die Merkmale ueberlebt, Klasse, Anzahl_Geschwister_Partner, Anzahl_Eltern_Kinder sind Integer. Die Merkmale Alter und Ticketpreis sind Floats. Die Merkmale Name, Geschlecht, Ticket, Kabine und Einstiegshafen sind Objekte. Mit `.head()` schauen wir uns die ersten fünf Zeilen an:

```python
daten.head()
```

Name, Tickets und Kabine sind Strings. Geschlecht und Einstiegshafen sind zwar vom Datentyp her Strings, könnten aber hier auch für Klassen stehen.
````

```{admonition} Statistik und Ausreißer
:class: tip

Erstellen Sie eine Übersicht der statistischen Merkmale für die numerischen
Daten. Visualisieren Sie anschließend die statistischen Merkmale mit Boxplots.
Interpretieren Sie die statistischen Merkmale. Gibt es Ausreißer? Sind die Werte
plausibel?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
daten.describe()
```

Die statistischen Daten zu `'ueberlebt'` sind unplausibel. Auch wenn hier Integer verwendet wurden, um überlebt/nicht überlebt zu klassifizieren, sind es eigentlich Klassen und sollten daher nicht statistisch ausgewertet werden.

Auf der Titanic gab es drei Preisklassen von 1 bis 3. Minimum und Maximum sind plausibel, aber dass 75 % der Passagiere in Klasse 1 (der teuersten Klasse) mitgereist sind, erscheint unwahrscheinlich.

Beim Alter fällt auf, dass das minimale Alter 0.92 ist. Da Jahre normalerweise als ganze Zahlen angegeben werden, ist das ungewöhnlich, aber nicht unplausibel. Die älteste Person war 80 Jahre alt. Der Durchschnitt lag bei 35.6 Jahren und der Median bei 36. 75 % der Passagiere waren jünger als 47.5 Jahre. Es erscheint plausibel, dass vor allem jüngere Passagiere die Strapazen der Schifffahrt auf sich genommen haben.  

50 % der Passagiere reisten alleine, nur sehr wenige in Familien.

Offensichtlich wurden Passagiere auch kostenlos mitgenommen, denn der minimale Ticketpreis ist 0. Das Maximum verwundert, vielleicht eine Umrechnung der Währungen, denn normalerweise werden nur 2 Nachkommastellen angegeben.

```python
import plotly.express as px 

kastendiagramm = px.box(daten[['Klasse', 'Alter', 'Anzahl_Geschwister_Partner', 'Anzahl_Eltern_Kinder', 'Ticketpreis']],
                       labels={'value': 'Wert', 'variable': 'Merkmal'},
                       title='Boxplot der numerischen Werte des Titanic-Datensatzes')
kastendiagramm.show()
```

Beim Ticketpreis gibt es deutliche Ausreißer, bei den anderen Merkmalen gibt es vereinzelte Ausreißer.
````

```{admonition} Analyse der kategorialen Daten
:class: tip
Untersuchen Sie die kategorialen Daten. Sind es wirklich kategoriale Daten?
Prüfen Sie für jedes kategoriale Merkmal die Einzigartigkeit der auftretenden
Werte und erstellen Sie ein Balkendiagramm mit den Häufigkeiten.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
merkmale = ['Name', 'Geschlecht', 'Ticket', 'Kabine', 'Einstiegshafen']
for m in merkmale:
    einzigartige_eintraege = daten[m].unique()
    anzahl = len(einzigartige_eintraege)
    print(f'Merkmal {m} hat {anzahl} einzigartige Einträge.')
```

Beim Merkmal Geschlecht gibt es nur zwei verschiedene Einträge, beim Einstiegshafen nur drei verschiedene Einstiegshäfen. Das sind (ungeordnete) kategoriale Daten. Die anderen Merkmale sind zu verschieden und sind damit nicht mehr als kategoriale Daten einzustufen. Es werden daher die Balkendiagramme mit den Häufigkeiten nur für die beiden Merkmale Geschlecht und Einstiegshafen erstellt.

```python
geschlecht = daten['Geschlecht']

balkendiagramm_geschlecht = px.bar(geschlecht.value_counts(),
                                  labels={'value': 'Anzahl', 'variable': 'Geschlecht'},
                                  title='Häufigkeit Geschlecht')
balkendiagramm_geschlecht.show()
```

```python
hafen = daten['Einstiegshafen']

balkendiagramm_hafen = px.bar(hafen.value_counts(),
                                  labels={'value': 'Anzahl', 'variable': 'Hafen'},
                                  title='Häufigkeit Einstiegshafen')
balkendiagramm_hafen.show()
```
````

### ML-Modell Titanic

```{admonition} Entscheidungsbaum
:class: tip
Trainieren Sie mit den numerischen Merkmalen einen Entscheidungsbaum/Decision
Tree. Visualisieren Sie den Entscheidungsbaum.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
X = daten[['Klasse', 'Alter', 'Anzahl_Geschwister_Partner', 'Anzahl_Eltern_Kinder','Ticketpreis']]
y = daten['ueberlebt']

from sklearn.tree import DecisionTreeClassifier

entscheidungsbaum =  DecisionTreeClassifier()
entscheidungsbaum.fit(X,y)
entscheidungsbaum.score(X,y)
score = entscheidungsbaum.score(X,y)
print(f'Score: {score:.2f}')
```

```python
from sklearn.tree import plot_tree

plot_tree(entscheidungsbaum);
```
````

```{admonition} Hyperparameter-Tuning und Interpretation
:class: tip

Spielen Sie mit den Hyperparametern des Entscheidungsbaumes/Decision Trees.
Begrenzen Sie die Baumtiefe auf 2, 3 und 4. Was sind die wichtigsten Merkmale,
die ein Überleben der Passagiere gesichert haben?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
for baumtiefe in [2, 3, 4]:
    baum = DecisionTreeClassifier(max_depth=baumtiefe)
    baum.fit(X,y)
    score = baum.score(X,y)
    print(f'Score für eine Baumtiefe von {baumtiefe}: {score: .2f}')
```

Tatsächlich ist der Entscheidungsbaum/Decision Tree mit einer Baumtiefe von 3
und 4 kaum besser als der mit einer Baumtiefe von 2. Wir werten daher den
Entscheidungsbaum mit einer Baumtiefe von 2 aus:

```python
finales_modell = DecisionTreeClassifier(max_depth=2)
finales_modell.fit(X,y)

plot_tree(finales_modell,
    feature_names=['Klasse', 'Alter', 'Anzahl_Geschwister_Partner', 'Anzahl_Eltern_Kinder','Ticketpreis'],
    class_names=['nicht ueberlebt', 'ueberlebt']);
```

Zunächst einmal scheint ein jüngeres Alter die Überlebenschance erhöht zu haben. Danach wirkt es so, also ob der Ticketpreis eine wichtige Rolle gespielt haben könnte.
````

## Aufgabe 6.2

Der Datensatz 'diabetes.csv' ist eine Sammlung von medizinischen Daten, die vom
National Institute of Diabetes and Digestive and Kidney Diseases, erhoben
wurden, siehe
[https://www.kaggle.com/datasets/whenamancodes/predict-diabities?resource=download](https://www.kaggle.com/datasets/whenamancodes/predict-diabities?resource=download).
Bei Frauen des Pima-Stammes wurden folgende medizinische Daten erhoben:

* Pregnancies: Anzahl der Schwangerschaften
* Glucose: Glukose-Level im Blut
* BloodPressure: Messung des Blutdrucks
* SkinThickness: Dicke der Haut
* Insulin: Messung des Insulinspiegels im Blut
* BMI: Body-Maß-Index (Gewicht geteilt durch Körpergröße ins Quadrat)
* DiabetesPedigreeFunction: Wahrscheinlichkeit von Diabetes aufgrund der Familienhistorie
* Age: Alter

Enthalten ist auch, ob bei der Person Diabetes festgestellt wurde oder nicht.

* Outcome: Diabetes = 1, kein Diabetes = 0

### EDA Diabetes

Führen Sie eine explorative Datenanalyse (EDA) durch, indem  Sie Python-Code in
Code-Zellen ausführen und schreiben Sie in Markdown-Zellen Ihre Antworten.

```{admonition} Überblick
:class: tip

Welche Daten enthält der Datensatz? Wie viele Personen sind in der Tabelle
enthalten? Wie viele Merkmale werden dort beschrieben? Sind die Daten
vollständig?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd 

daten = pd.read_csv('diabetes.csv')
daten.info()
```

Der Datensatz enthält 768 Personen mit insgesamt 9 Merkmalen. Aufgelistet sind die Merkmale Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age und Outcome.

Die Daten sind für jedes Merkmal vollständig. In jeder Spalte gibt es 768 non-null Einträge.
````

```{admonition} Datentyp
:class: tip

Welchen Datentyp haben die Merkmale? Welche Merkmale sind numerisch und welche
sind kategorial?
```

````{admonition} Lösung
:class: tip
:class: dropdown

Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, Age und Outcome sind Integer. BMI und DiabetesPedigreeFunction sind Floats. Kein Merkmal wird als object eingestuft.
````

```{admonition} Statistik
:class: tip

Erstellen Sie eine Übersicht der statistischen Merkmale für die numerischen
Daten. Visualisieren Sie anschließend die statistischen Merkmale mit Boxplots.
Interpretieren Sie die statistischen Merkmale. Gibt es Ausreißer? Sind die Werte
plausibel?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
daten.describe()
```

Die Pregnancies reichen von 0 Schwangerschaften bis hin zu 17 Schwangerschaften,
was ungewöhnlich hoch ist. Der Mittelwert von 3.85 Schwangerschaften erscheint
plausibel, 50 % der Frauen waren maximal dreimal schwanger.

Der Glucose-Wert reicht von 0 bis 199. An der Stelle müsste mit einem Mediziner
Rücksprache gehalten werden, ob ein Glucose-Wert von 0 plausibel ist.

Beim BloodPressure, also den Blutdruck, ist der minimale Wert von 0 jedoch
unplausibel. Eine Person mit einem Blutdruck von 0 ist tot. Diese Null-Werte sind wahrscheinlich fehlende Messwerte, die fälschlicherweise als 0 kodiert wurden. In einer vollständigen Datenanalyse müssten diese Werte entweder durch sinnvolle Methoden ersetzt oder die betroffenen Zeilen entfernt werden.

SkinThickness kann erneut nur von Medizinern korrekt eingeordnet werden. Ob eine
minimale SkinThickness von 0 und eine maximale SkinThickness von 99 sinnvolle
Werte darstellen, können Nichtmediziner nicht sinnvoll beurteilen.

Auch der minimale Insulin-Wert von 0 sowie der Body-Maß-Index BMI wirken seltsam.
Ein BMI von 0 kann nicht sein, denn beim BMI wird das Gewicht einer Person durch
die quadrierte Körpergröße geteilt. Ein BMI von 0 bedeutet ein Gewicht von 0,
was nicht sein kann. Wahrscheinlich wurden hier wiederum Werte nicht erfasst.

Die DiabetesPedigree-Funktion können wir ohne medizinisches Fachwissen nicht
bewerten.

Beim Alter fällt auf, dass keine Kinder dabei waren. Die jüngste Person ist 21,
das mittlere Alter liegt bei 33 Jahren und 75 % aller Personen sind jünger als
41.

Das Outcome darf nicht einfach statistisch interpretiert werden. Das Outcome
gibt an, ob eine Person Diabetes hat (1) oder nicht (0). Auch wenn hier Zahlen
verwendet wurden, ist das Outcome eigentlich ein kategoriales Merkmal. Es ist
sogar die kategoriale Zielgröße unserer Problemstellung.
````

```{admonition} Untersuchung Ursache - Wirkung
:class: tip

Erstellen Sie eine Scatter-Matrix mit Insulin, BMI und Outcome. Welche der
beiden Eigeschaften Insulin oder BMI könnte ehr geeignet sein, Diabetes ja/nein
zu prognostizieren?

Visualisieren Sie Diabetes ja/nein in Abhängigkeit der gewählten Eigenschaft.
Vermuten Sie einen Zusammenhang?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import plotly.express as px 

auswahl = ['Insulin', 'BMI', 'Outcome']
fig = px.scatter_matrix(daten[auswahl],
    title='Wirkung Insulin und BMI auf Diabetes')
fig.show()
```

Beim Insulin kann man kaum eine Wirkung des Insulins auf den Diabeteszustand
erkennen. Beim BMI kann man erkennen, dass ein höherer BMI scheinbar mehr zu
Diabetes führt als ein niedriger BMI.

```python
fig = px.scatter(daten, x = 'BMI', y = 'Outcome',
    title='Wirkung BMI auf Diabetes')
fig.show()
```

Es ist kaum ein Zusammenhang erkennbar außer der Feststellung, dass höherer BMI
anscheinend häufiger mit Diabetes korreliert ist als niedriger BMI.
````

### ML-Modell Diabetes

```{admonition} Entscheidungsbaum
:class: tip

Trainieren Sie mit den numerischen Merkmalen einen Entscheidungsbaum/Decision
Tree. Visualisieren Sie den Entscheidungsbaum.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
X = daten.loc[:, 'Pregnancies' : 'Age']
y = daten['Outcome']
```

```python
from sklearn.tree import DecisionTreeClassifier

modell = DecisionTreeClassifier()
modell.fit(X,y)

score = modell.score(X,y)
print(f'Score: {score:.2f}')
```

```python
from sklearn.tree import plot_tree

plot_tree(modell);
```
````

```{admonition} Hyperparameter und Interpretation
:class: tip

Spielen Sie mit den Hyperparametern des Entscheidungsbaumes/Decision Trees.
Begrenzen Sie die Baumtiefe auf 2, 3 und 4. Was sind die wichtigsten Merkmale,
die Diabetes auslösen können?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
for baumtiefe in [2, 3, 4]:
    baum = DecisionTreeClassifier(max_depth=baumtiefe)
    baum.fit(X,y)
    score = baum.score(X,y)
    print(f'Score für eine Baumtiefe von {baumtiefe}: {score: .2f}')
```

Wieder gibt es kaum Unterschiede im Score für die verschiedenen Baumtiefen. Wir
betrachten nun ein Modell der Baumtiefe 2.

```python
finales_modell = DecisionTreeClassifier(max_depth=2)
finales_modell.fit(X,y)

plot_tree(finales_modell,
    feature_names=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
       'BMI', 'DiabetesPedigreeFunction', 'Age'],
    class_names=['kein Diabetes', 'Diabetes']);
```

Als erstes Entscheidungskriterium wird der Glucose-Wert benutzt. Je nachdem, ob
der Glucose-Wert kleiner 127.5 ist oder nicht, wird danach das Alter (jünger als
28.5 bedeutet dann kein Diabetes) oder der BMI (kleiner als 29.95 kein Diabetes)
als Entscheidungsmerkmal verwendet.
````
