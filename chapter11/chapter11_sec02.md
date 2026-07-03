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

# 11.2 Gittersuche

Die Kreuzvalidierung wird selten isoliert verwendet. Sie ist jedoch ein
unverzichtbares Werkzeug, wenn es darum geht, die Hyperparameter eines Modells
zu optimieren. In diesem Kapitel vertiefen wir daher zunächst das Verständnis
der Kreuzvalidierung, bevor wir sie im Rahmen der Gittersuche anwenden.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie verstehen, dass Daten für die Modellauswahl in Trainingsdaten,
  **Validierungsdaten** und Testdaten unterteilt werden.
* Sie sind in der Lage, Hyperparameter mittels Gittersuche und Kreuzvalidierung
  mithilfe von **GridSearchCV** zu optimieren.
```

## Kreuzvalidierung zur Modellauswahl

Im letzten Kapitel haben wir die Kreuzvalidierung eingeführt. Ihr Ziel ist es,
eine robustere Bewertung der Modellleistung zu ermöglichen. Besonders bei der
Beurteilung und der Verbesserung der Verallgemeinerungsfähigkeit eines Modells
(Reduktion von Overfitting), ist die Kreuzvalidierung ein wertvolles Werkzeug.
In diesem Abschnitt nutzen wir die Kreuzvalidierung, um zwischen zwei Modellen
zu wählen.

Aus didaktischen Gründen verwenden wir weiterhin künstliche Daten, die mit der
Funktion `make_moons()` aus dem Modul `sklearn.datasets` erzeugt werden. Diese
speichern wir in einem Pandas DataFrame und visualisieren sie anschließend mit
Plotly Express.

```{code-cell}
import pandas as pd
import plotly.express as px
from sklearn.datasets import make_moons

X_array, y_array = make_moons(noise = 0.5, n_samples=100, random_state=3)
daten = pd.DataFrame({
    'Merkmal 1': X_array[:,0],
    'Merkmal 2': X_array[:,1],
    'Wirkung': y_array
})
daten['Wirkung'] = daten['Wirkung'].astype('bool')

fig = px.scatter(daten, x = 'Merkmal 1', y = 'Merkmal 2', color='Wirkung',
    title='Künstliche Daten')
fig.show()
```

Als nächstes trainieren wir einen Entscheidungsbaum. Da Entscheidungsbäume
häufig zur Überanpassung (Overfitting) neigen, entscheiden wir uns, die
Baumtiefe zu begrenzen. Aber welche Baumtiefe ist optimal? Die Baumtiefe ist ein
Hyperparameter, der vor dem Training des Modells festgelegt wird. Mithilfe der
Kreuzvalidierung können wir untersuchen, wie sich die Baumtiefe auf die
Modellqualität auswirkt. Wir testen die Baumtiefen 3, 4, 5 und 6 und geben die
Scores auf den Testdaten aus, wobei wir uns mit einer for-Schleife die Arbeit
erleichtern.

```{code-cell}
from sklearn.model_selection import cross_validate, KFold
from sklearn.tree import DecisionTreeClassifier

# Adaption der Daten
X = daten[['Merkmal 1', 'Merkmal 2']]
y = daten['Wirkung']

# Vorbereitung der Kreuzvalidierung mit 10 Splits
kfold = KFold(n_splits=10)

# wiederholte Kreuzvalidierung für Baumtiefe 3, 4, 5 und 6
for max_tiefe in [3, 4, 5, 6]:
    modell = DecisionTreeClassifier(max_depth=max_tiefe)
    cv_results = cross_validate(modell, X,y, cv=kfold)
    test_scores = cv_results['test_score']
    print(f'Testscores: {test_scores}')
```

Die Ausgabe von 10 Testscores ist jedoch unübersichtlich. Stattdessen berechnen
wir besser den Mittelwert (Mean) und die Standardabweichung (Standard Deviation)
der Scores. Dazu importieren wir `mean()` und `std()` aus dem NumPy-Modul und
passen die `print()`-Anweisung entsprechend an.

```{code-cell}
from numpy import mean, std

for max_tiefe in [3, 4, 5, 6]:
    modell = DecisionTreeClassifier(max_depth=max_tiefe)
    cv_results = cross_validate(modell, X,y, cv=kfold)
    test_scores = cv_results['test_score']
    print(f'Mittelwert Testscores: {mean(test_scores):.2f}, Standardabweichung: {std(test_scores):.2f}')
```

Das beste Ergebnis erzielen wir mit einem Entscheidungsbaum der Tiefe 3. Diesen
könnten wir nun als finales Modell wählen.

Es gibt jedoch ein Problem: Wir haben die Modellauswahl mit den Scores der
Testdaten begründet, wodurch diese in das Modelltraining eingeflossen sind. Daher
benötigen wir einen frischen Datensatz, um die Prognosequalität zu testen. Die
Lösung dafür ist `train_test_split()`.

Zuerst teilen wir die Daten in Trainings- und Testdaten. Dann verwenden wir die
Kreuzvalidierung auf den Trainingsdaten, um die Hyperparameter zu bewerten. Die
Kreuzvalidierung teilt die Trainingsdaten erneut in Trainings- und Testdaten
auf.  Damit diese »internen« Testdaten nicht mit den richtigen Testdaten
verwechselt werden, nennt man sie auch **Validierungsdaten**. Die Mittelwerte
der Scores speichern wir in einem Dictionary, um später das beste Modell zu
ermitteln. Schließlich trainieren wir das beste Modell auf allen Trainingsdaten
und bewerten es mit den Testdaten.

Das Hyperparameter-Tuning bzw. die Modellwahl mit Kreuzvalidierung funktioniert
komplett also wie folgt:

```{code-cell}
from sklearn.model_selection import cross_validate, KFold, train_test_split
from sklearn.tree import DecisionTreeClassifier

X = daten[['Merkmal 1', 'Merkmal 2']]
y = daten['Wirkung']

X_train, X_test, y_train, y_test = train_test_split(X,y)

kfold = KFold(n_splits=10)

mean_scores = {}
for max_tiefe in [3, 4, 5, 6]:
    modell = DecisionTreeClassifier(max_depth=max_tiefe)
    cv_results_modell = cross_validate(modell, X_train, y_train, cv=kfold)
    test_scores = cv_results_modell['test_score']
    mean_scores[max_tiefe] = mean(test_scores)
    print(f'Mittelwert Testscores: {mean(test_scores):.2f}, Standardabweichung: {std(test_scores):.2f}')

# Ermitteln der besten Baumtiefe (argmax o.ä. wäre einfacher)
tiefe = 3
score = mean_scores[3]
for t in [4,5,6]:
    if mean_scores[t] > score:
        tiefe = t
        score = mean_scores[t]
print(f'\nWähle Baumtiefe {tiefe} mit dem besten Score {score:.2f}.')

# Finale Modellauswahl, Training und Bewertung
finales_modell = DecisionTreeClassifier(max_depth=tiefe)
finales_modell.fit(X_train, y_train)
finaler_score = finales_modell.score(X_test, y_test)
print(f'Testscore finales Modell: {finaler_score:.2f}') 
```

Um die Hyperparameter zu optimieren und das beste Modell zu finden, haben wir
eine for-Schleife und manuelle Auswahl verwendet. Scikit-Learn bietet jedoch
eine einfachere Lösung, die wir im nächsten Abschnitt behandeln: die Gittersuche
mit Kreuzvalidierung **GridSearchCV**.

## Gittersuche mit Kreuzvalidierung: GridSearchCV

Die Gittersuche mit Kreuzvalidierung wird als **GridSearchCV** aus dem Modul
`sklearn.model_selection` importiert. Zunächst legen wir fest, welche Parameter
optimiert werden sollen und welche Werte dafür in Betracht kommen. Technisch
benötigen wir dafür ein Dictionary, in dem die Schlüssel die Parameternamen und
die Werte Listen der möglichen Einstellungen sind. In unserem Fall soll die
Baumtiefe `'max_depth'` des Entscheidungsbaums justiert werden. Wie zuvor in der
for-Schleife, untersuchen wir die Baumtiefen 3, 4, 5 und 6, die im folgenden
Dictionary `parameter_gitter` definiert werden.

```{code-cell}
from sklearn.model_selection import GridSearchCV

# Festlegung des Suchraumes
parameter_gitter = {'max_depth': [3, 4, 5, 6]}
```

Nun instanziieren wir ein neues `GridSearchCV`-Modell. Als erstes Argument
übergeben wir das eigentliche Modell, hier also den Entscheidungsbaum, und als
zweites das Dictionary mit den Hyperparametern. Das dritte Argument ist die
Methode zur Kreuzvalidierung. Weitere Details können Sie der [Dokumentation
Scikit-Learn →
GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV)
entnehmen.

```{code-cell}
optimiertes_modell = GridSearchCV(DecisionTreeClassifier(), param_grid=parameter_gitter, cv=kfold)
```

Mit der Methode `.fit()` wird die Gittersuche samt Kreuzvalidierung
durchgeführt. Dabei werden systematisch alle Parameterkombinationen getestet,
und das optimierte Modell wird abschließend erneut auf den gesamten
Trainingsdaten trainiert.

```{code-cell}
optimiertes_modell.fit(X_train, y_train)
```

Mit der Methode `.score()` können wir die Modellgüte sowohl auf den Trainings-
als auch auf den Testdaten bewerten. Auch die Methode `.predict()` funktioniert
wie gewohnt.

```{code-cell}
opt_score_train = optimiertes_modell.score(X_train, y_train)
opt_score_test  = optimiertes_modell.score(X_test, y_test)

print(f'optimierter Entscheidungsbaum Score Trainingsdaten: {opt_score_train:.2f}')
print(f'optimierter Entscheidungsbaum Score Testdaten: {opt_score_test:.2f}')
```

Zusätzlich zu den Standardmethoden wie `.fit()`, `.predict()` und `.score()`
können wir mit dem Attribut `best_params_` herausfinden, welche
Hyperparameter-Kombination am besten abgeschnitten hat.

```{code-cell}
print(optimiertes_modell.best_params_)
```

In diesem Fall ergibt die Gittersuche, dass die optimale Baumtiefe 3 beträgt.

Warum sprechen wir von einer **Gittersuche**? Normalerweise wollen wir nicht nur
einen Hyperparameter optimieren, sondern mehrere gleichzeitig. Beispielsweise
könnten wir neben der Baumtiefe auch die minimale Anzahl an Datenpunkten pro
Blatt (`min_samples_leaf`) optimieren. Dies führt dazu, dass wir jede
Kombination von `max_depth` mit jedem Wert von `min_samples_leaf` testen. So
entsteht ein zweidimensionales Gitter, das die Gittersuche effizient durchläuft.
Wir müssen lediglich das Dictionary entsprechend erweitern. In diesem Beispiel
werden 4 Baumtiefen und 3 Werte für `min_samples_leaf` kombiniert, was zu
insgesamt 4 x 3 = 12 Hyperparameter-Kombinationen führt. Da wir 10-fache
Kreuzvalidierung verwenden, werden insgesamt 120 Modelle trainiert und bewertet.

```{code-cell}
parameter_gitter = {
    'max_depth': [3, 4, 5, 6],
    'min_samples_leaf': [1, 2, 3]
}

optimiertes_modell = GridSearchCV(DecisionTreeClassifier(), param_grid=parameter_gitter, cv=kfold)
optimiertes_modell.fit(X_train, y_train)

opt_score_train = optimiertes_modell.score(X_train, y_train)
opt_score_test  = optimiertes_modell.score(X_test, y_test)

print(f'optimierter Entscheidungsbaum Score Trainingsdaten: {opt_score_train:.2f}')
print(f'optimierter Entscheidungsbaum Score Testdaten: {opt_score_test:.2f}')

print(optimiertes_modell.best_params_)
```

Auch wenn bei diesem einfachen Beispiel die Unterschiede zwischen den Modellen
gering sind und die Vorteile der Gittersuche mit Kreuzvalidierung nicht sofort
ersichtlich werden, ist diese Methode bei größeren Datensätzen und komplexeren
Modellen ein sehr wertvolles Werkzeug zur Modelloptimierung, bei der alle
möglichen Kombinationen von Hyperparametern systematisch getestet werden. Dies
kann jedoch sehr *rechenintensiv* sein, besonders wenn der Suchraum groß ist
oder komplexe Modelle verwendet werden. Daher unterstützt GridSearchCV die
*Parallelisierung* der Berechnungen, indem es mehrere Kerne verwendet, um die
Rechenzeit signifikant zu verkürzen, was besonders bei größeren Datensätzen von
Vorteil ist.

Eine Alternative zu GridSearchCV ist **RandomizedSearchCV**. Dieses Verfahren
testet eine zufällige Auswahl von Parametern testet und spart so Zeit, während
es dennoch gute Ergebnisse liefert. Mehr Details dazu finden Sie in der
[Dokumentation Scikit-Learn →
RandomizedSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html#sklearn.model_selection.RandomizedSearchCV).

```{dropdown} Video "GridSearchCV" von Normalized Nerd
<iframe width="560" height="315" src="https://www.youtube.com/embed/TvB_3jVIHhg?si=s2jDNKOmqBEcJcAd" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir erstmals systematisch Hyperparameter optimiert und
dabei die Gittersuche mit Kreuzvalidierung angewendet. Im nächsten Kapitel
lernen wir ein weiteres Werkzeug kennen, das nicht nur verschiedene Modelle,
sondern auch deren Hyperparameter optimiert und anschließend Modellvorschläge
basierend auf den besten Einstellungen macht.
