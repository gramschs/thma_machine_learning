---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.3
kernelspec:
  display_name: python312
  language: python
  name: python3
---

# Übungen

Der Datensatz Pinguine stammt von
[HuggingFace](https://huggingface.co/datasets/SIH/palmer-penguins). Der
Datensatz umfasst Daten von Pinguinen, insbesondere die Merkmale

* Art,
* Insel,
* Schnabellaenge und Schnabeltiefe in Millimetern
* Flossenlaenge in Millimetern,
* Koerpergewicht in Gramm,
* Geschlecht und
* Jahr der Geburt.

Laden Sie die deutsche Variante des Datensatzes aus campUAS und führen Sie eine
explorative Datenanalyse durch. Legen Sie 10 % der Daten als Testdaten zurück.
Trainieren Sie dann ML-Modelle ggf. mit Gittersuche und wählen Sie das beste
Modell aus. Welchen Score erreicht Ihr Modell für die Testdaten?

```{admonition} Überblick über die Daten
:class: tip
Welche Daten enthält der Datensatz? Wie viele Pinguine sind in der Tabelle enthalten? Wie viele Merkmale werden dort beschrieben? Sind die Daten vollständig?
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
import pandas as pd 

daten = pd.read_csv('pinguine.csv', skiprows=3)
daten.info()
```

Die Tabelle enthält 344 Pinguine. Es sind 8 Merkmale enthalten, nämlich die Merkmale Art, Insel, Schnabellaenge_mm, Schnabeltiefe_mm, Flossenlaenge_mm, Koerpergewicht_g, Geschlecht, Jahr. Die Merkmale Schnabellaenge_mm, Schnabeltiefe_mm, Flossenlaenge_mm und Geschlecht sind unvollständig.
````

```{admonition} Datentypen
:class: tip
Welchen Datentyp haben die Merkmale? Welche Merkmale sind numerisch und welche sind kategorial?
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
* Art --> object
* Insel --> object
* Schnabellaenge_mm --> float
* Schnabeltiefe_mm --> float
* Flossenlaenge_mm --> float
* Koerpergewicht_g --> float
* Geschlecht --> object
* Jahr --> int

```python
merkmale = daten.columns

for m in merkmale:
    anzahl_einzigartiger_eintraege = len(daten[m].unique())
    print(f'Merkmal {m} hat {anzahl_einzigartiger_eintraege} Einträge.')
```

Die Merkmale Art, Insel, Geschlecht und Jahr sind kategorial. Die Merkmale Schnabellaenge_mm, Schnabeltiefe_mm, Flossenlaenge_mm, Koerpergewicht_g sind numerisch.
````

```{admonition} Fehlende Einträge
:class: tip
In welcher Spalte fehlen am meisten Einträge? Filtern Sie den Datensatz nach den fehlenden Einträgen und geben Sie eine Liste mit den Indizes (Zeilennummern) aus, wo Einträge fehlen. Löschen Sie anschließend diese Zeilen aus dem Datensatz. Sind jetzt alle Einträge gültig?
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
fehlende_geschlechtsangaben = daten[ daten['Geschlecht'].isnull() ].index
print(fehlende_geschlechtsangaben)
```

```python
daten = daten.drop(fehlende_geschlechtsangaben)
daten.info()
```

Jetzt sind alle Einträge gültig.
````

```{admonition} Analyse numerische Daten
:class: tip
Erstellen Sie eine Übersicht der statistischen Merkmale für die numerischen Daten. Visualisieren Sie anschließend die statistischen Merkmale mit Boxplots. Verwenden Sie ein Diagramm für die Merkmale, die in Millimetern gemessen werden und ein Diagramm für das Körpergewicht. Interpretieren Sie die statistischen Merkmale. Gibt es Ausreißer? Sind die Werte plausibel?
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
numerische_merkmale = ['Schnabellaenge_mm', 'Schnabeltiefe_mm', 'Flossenlaenge_mm', 'Koerpergewicht_g']

daten[numerische_merkmale].describe()
```

```python
import plotly.express as px 

fig = px.box(daten[['Schnabellaenge_mm', 'Schnabeltiefe_mm', 'Flossenlaenge_mm']],
    labels={'variable': 'Merkmal', 'value':'Wert'},
    title='Numerische Merkmale der Pinguine (gemessen in Millimetern)')
fig.show()
```

Die Schnabeltiefe ist deutlich kleiner als die Schnabellänge. Bei der Flossenlänge fällt auf, das der Median deutlich kleiner ist als der Mittelwert. Insgesamt gibt es keine Ausreißer.

```python
import plotly.express as px 

fig = px.box(daten[['Koerpergewicht_g']],
    labels={'variable': 'Merkmal', 'value':'Wert'},
    title='Numerische Merkmale der Pinguine (gemessen in Gramm)')
fig.show()
```

Beim Körpergewicht gibt es keine Besonderheiten, die Werte erscheinen plausibel.
````

```{admonition} Analyse der kategorialen Werte
:class: tip
Untersuchen Sie die kategorialen Daten. Sind es wirklich kategoriale Daten? Prüfen Sie für jedes kategoriale Merkmal die Einzigartigkeit der auftretenden Werte und erstellen Sie ein Balkendiagramm mit den Häufigkeiten.

Kommen alle Pinguin-Arten auf allen Inseln vor?
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
kategoriale_merkmale = ['Art', 'Insel', 'Geschlecht', 'Jahr']

for k in kategoriale_merkmale:
    print(daten[k].unique())
```

Es gibt drei Pinguin-Arten: Adelie, Gentoo und Chinstrap. Sie leben auf drei Inseln: Torgersen, Biscoe und Dream. Es gibt zwei Geschlechter (männlich/weiblich) und die Pinguine wurden in den Jahren 2007, 2008 und 2009 geboren. Bei allen Merkmalen handelt es sich tatsächlich um kategoriale Daten.

```python
for k in kategoriale_merkmale:

    fig = px.bar(daten[k].value_counts(),
        labels={'value': 'Anzahl'},
        title=f'Histogramm des Merkmals {k}')
    fig.show()
```

Bei den Jahren und dem Geschlecht gibt es jeweils ungefähr gleich viele
Pinguine, aber die Arten und die Inseln sind nicht gleich häufig.

```python
for art in ['Adelie', 'Gentoo', 'Chinstrap']:
    pinguine_art = daten[ daten['Art'] == art ]
    print(f'\nArt: {art}')
    print(pinguine_art['Insel'].value_counts())

```

Die Pinguin-Art Adelie kommt auf allen drei Inseln vor. Die Pinguin-Art Gentoo ist nur auf der Insel Biscoe zu finden, während Chinstrap-Pinguine nur auf der Insel Dream zu finden sind.
````

```{admonition} ML-Modell
:class: tip

Im Folgenden soll die Art der Pinguine anhand der numerischen Merkmale Schnabellaenge_mm, Schnabeltiefe_mm, Flossenlaenge_mm und Koerpergewicht_g klassifiziert werden.

Trainieren Sie nun drei ML-Modelle:

* Entscheidungsbaum (Decision Tree), 
* Random Forests und 
* SVM. 

Führen Sie dazu vorab einen Split in Trainings- und Testdaten durch. Verwenden Sie Kreuzvalidierung und/oder Gittersuche, um die Hyperparameter zu justieren. Für welches Modell würden Sie sich entscheiden? Begründen Sie Ihre Wahl.
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
X = daten[['Schnabellaenge_mm', 'Schnabeltiefe_mm', 'Flossenlaenge_mm', 'Koerpergewicht_g']]

kodierung = {
  'Adelie': '0',
  'Gentoo': '1', 
  'Chinstrap': '2'
}

daten['Art'] = daten['Art'].replace(kodierung)
daten['Art'] = daten['Art'].astype('int')
y = daten['Art']
```

```python
from sklearn.model_selection import GridSearchCV, KFold, train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y)
```

```python
from sklearn.tree import DecisionTreeClassifier

# Festlegung des Suchraumes
parameter_gitter = {'max_depth': [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 50]}

# Konfiguration der Kreuzvalidierung
kfold = KFold(n_splits=10)

# Gittersuche mit Kreuzvalidierung
entscheidungsbaum = GridSearchCV(DecisionTreeClassifier(), param_grid=parameter_gitter, cv=kfold)
entscheidungsbaum.fit(X_train, y_train)
print(entscheidungsbaum.score(X_train, y_train))
print(entscheidungsbaum.score(X_test, y_test))

# Bestes Modell
print(entscheidungsbaum.best_params_)
```

```python
from sklearn.ensemble import RandomForestClassifier

# Festlegung des Suchraumes
random_forest_gitter = {'max_depth': [None, 1, 2, 3, 4, 5],
                        'min_samples_leaf': [1, 2, 3, 4, 5],
                        'n_estimators': [50, 100, 200]}

# Konfiguration der Kreuzvalidierung
kfold = KFold(n_splits=10)

# Gittersuche mit Kreuzvalidierung
random_forest_modell = GridSearchCV(RandomForestClassifier(), param_grid=random_forest_gitter, cv=kfold)
random_forest_modell.fit(X_train, y_train)
print(random_forest_modell.score(X_train, y_train))
print(random_forest_modell.score(X_test, y_test))

# Bestes Modell
print(random_forest_modell.best_params_)
```

```python
from sklearn.svm import SVC

svm_gitter = {'kernel': ['linear', 'rbf'],
              'C': [0.1, 1, 10, 1000]
} 

# Konfiguration der Kreuzvalidierung
kfold = KFold(n_splits=10)

# Gittersuche mit Kreuzvalidierung
svm_modell = GridSearchCV(SVC(), param_grid=svm_gitter, cv=kfold)
svm_modell.fit(X_train, y_train)
print(svm_modell.score(X_train, y_train))
print(svm_modell.score(X_test, y_test))

# Bestes Modell
print(svm_modell.best_params_)
```

RandomForest und SVM erzielen gleich gute Scores bei den Testdaten und sind daher beide sehr gut geeignet, als finales Modell verwendet zu werden.
````
