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

# 9.2 Random Forests

Im letzten Kapitel haben wir verschiedene Ensemble-Methoden in der Theorie
kennengelernt: Stacking, Bagging und Boosting. Für die beiden letzteren
Ensemble-Methoden werden besonders häufig Entscheidungsbäume (Decision Trees)
eingesetzt. Daher betrachten wir in diesem Kapitel die praktische Umsetzung von
Bagging mit Entscheidungsbäumen, die sogenannten Random Forests.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können das ML-Modell **Random Forest** in der Praxis anwenden.
* Sie können mit Hilfe der **Feature Importance** bewerten, wie groß der
  Einfluss eines Merkmals auf die Prognosegenauigkeit des Random Forests ist.
```

## Random Forests mit Scikit-Learn

Entscheidungsbäume (Decision Trees) haben wir bereits betrachtet. Sie sind
aufgrund ihrer Einfachheit und vor allem aufgrund ihrer Interpretierbarkeit sehr
beliebt. Allerdings ist ihre Tendenz zum Overfitting problematisch. Daher
kombinieren wir die Ensemble-Methode Bagging mit Entscheidungsbäumen (Decision
Trees). Indem aus den Trainingsdaten zufällig Bootstrap-Stichproben ausgewählt
werden, erhalten wir unterschiedliche Entscheidungsbäume (Decision Trees).
Zusätzlich wird beim Training der Entscheidungsbäume nicht mit allen Merkmalen
(Features) trainiert. Bei jedem Split eines Baumes wird nur eine zufällige
Teilmenge der Merkmale betrachtet, um die beste Trennung zu finden. Durch diese
zwei Maßnahmen wird die Anpassung der Entscheidungsbäume an die Trainingsdaten
(Overfitting) reduziert.

Um den Random Forest von Scikit-Learn praktisch auszuprobieren, erzeugen wir
künstliche Daten. Dazu verwenden wir die Funktion `make_moons` von Scikit-Learn,
die Zufallszahlen generiert und interpretieren die Zufallszahlen als
Kilometerstände und Preise von Autos bei einer fiktiven Verkaufsaktion.
Zusätzlich lassen wir zufällig Nullen und Einsen erzeugen, die wir als
»verkauft« oder »nicht verkauft« interpretieren.

```{code-cell} ipython3
import pandas as pd 
from sklearn.datasets import make_moons

# Erzeugung künstlicher Daten
X_array, y_array = make_moons(n_samples=120, random_state=0, noise=0.3)

daten = pd.DataFrame({
    'Kilometerstand [km]': 10000 * (X_array[:,0] + 2),
    'Preis [EUR]': 5000 * (X_array[:,1] + 2),
    'verkauft': y_array,
    })

# Adaption der Daten
X = daten[['Kilometerstand [km]', 'Preis [EUR]']].values
y = daten['verkauft'].values
```

Diesmal werden in dem Autohaus 120 Autos zum Verkauf angeboten (siehe Option
`n_samples=120`). Nach Aktionsende werden die Merkmale Kilometerstand und Preis
tabellarisch erfasst und notiert, ob das Auto verkauft wurde (True bzw. 1) oder
nicht verkauft wurde (False bzw. 0). Wir visualisieren die Daten.

```{code-cell} ipython3
import plotly.express as px
# plot artificial data
fig = px.scatter(daten, x = 'Kilometerstand [km]', y = 'Preis [EUR]', color=daten['verkauft'].astype(bool),
        title='Künstliche Daten: Verkaufsaktion Autohaus',
        labels = {'x': 'Kilometerstand [km]', 'y': 'Preis [EUR]', 'color': 'verkauft'})
fig.show()
```

Nachdem wir die Vorbereitungen für die Daten abgeschlossen haben, können wir
Scikit-Learn einen Random Forest trainieren lassen. Dazu importieren wir den
Algorithmus aus dem Modul `ensemble`. Da der Random Forest ein Ensemble von
Entscheidungsbäumen (Decision Trees) ist, haben wir nun die Möglichkeit, die
Anzahl der Entscheidungsbäume festzulegen. Voreingestellt sind 100
Entscheidungsbäume. Aus didaktischen Gründen reduzieren wir diese Anzahl auf
vier und setzen das Argument `n_estimators=` auf `4`. Ebenfalls aus didaktischen
Gründen fixieren wir die Zufallszahlen, mit Hilfe derer das Bootstrapping und
die Auswahl der Merkmale (Features) umgesetzt wird, mit `random_state=0`. In
einem echten Projekt würden wir das unterlassen. Zuletzt führen wir das Training
mit der `.fit()`-Methode durch. Weitere Details finden Sie unter [Scikit-Learn
Dokumentation →
RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html).

```{code-cell} ipython3
from sklearn.ensemble import RandomForestClassifier

model_random_forest = RandomForestClassifier(n_estimators=4, random_state=0)
model_random_forest.fit(X,y)
```

Als nächstes lassen wir den Random Forest für jeden Punkt des Gebiets
prognostizieren, ob ein Auto mit diesem Kilometerstand und diese Preis
verkaufbar wäre oder nicht.

```{code-cell} ipython3
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay

my_colormap = ListedColormap(['#EF553B33', '#636EFA33'])
fig = DecisionBoundaryDisplay.from_estimator(model_random_forest, X,  cmap=my_colormap)
fig.ax_.scatter(X[:,0], X[:,1], c=y, cmap=my_colormap)
fig.ax_.set_xlabel('Kilometerstand [km]');
fig.ax_.set_ylabel('Preis [EUR]');
fig.ax_.set_title('Random Forest: Entscheidungsgrenzen');
```

Möchte man die vier Entscheidungsbäume (Decision Trees) analysieren, aus denen
der Random Forest kombiniert wurde, kann man mit dem Attribut `estimators_`
darauf zugreifen. Wir lassen uns jetzt die Entscheidungsgrenzen einzeln für
jeden Entscheidungsbaum anzeigen.

```{code-cell} ipython3
my_colormap = ListedColormap(['#EF553B33', '#636EFA33'])
for (nummer, baum) in zip(range(4), model_random_forest.estimators_):
    fig = DecisionBoundaryDisplay.from_estimator(baum, X,  cmap=my_colormap)
    fig.ax_.scatter(X[:,0], X[:,1], c=y, cmap=my_colormap)
    fig.ax_.set_xlabel('Kilometerstand [km]');
    fig.ax_.set_ylabel('Preis [EUR]');
    fig.ax_.set_title(f'Entscheidungsbaum {nummer+1}');
```

## Feature Importance

Der Random Forest reduziert das Overfitting und ist damit für zukünftige
Prognosen besser gerüstet, verliert aber seine leichte Interpretierbarkeit. Ein
großer Vorteil des Entscheidungsbaumes (Decision Trees) ist ja, dass wir die
Entscheidungen als eine Abfolge von Entscheidungsfragen gut nachvollziehen
können. Jeder der einzelnen Entscheidungsbäume kommt jedoch zu einer anderen
Reihenfolge der Entscheidungsfragen und zu anderen Grenzen. Dafür bietet der
Random-Forest-Algorithmus eine alternative Bewertung, wie wichtig einzelne
Merkmale (Features) sind, die sogenannte **Feature Importance**.

Feature Importance bewertet, wie wichtig der Einfluss eines Merkmals (Features)
auf die Prognoseleistung ist. Ist die Feature Importance eines Merkmals
(Features) höher, so trägt dieses Merkmal (Feature) auch mehr zu der Genauigkeit
der Prognose bei. Bei Entscheidungsbäumen wird für jedes Merkmal (Feature)
berechnet, wie groß die Reduktion der Gini-Impurity ist. Gibt es ein Merkmal,
das eindeutig die Gini-Impurity reduziert, dann hat dieses Merkmal auch einen
großen Einfluss auf die Prognosefähigkeit des Modells. Wir könnten nach dem
Training des Entscheidungsbaumes zusammenfassen, wie oft und wieviel ein
bestimmtes Merkmal zur Reduktion beiträgt. In der Praxis kommt es aber oft vor,
dass bei einem Split mehrere Merkmale gleichermaßen die Gini-Impurity
reduzieren. Dann wird eines der Merkmale zufällig ausgewählt. Daher kann es
schwierig sein, bei einem Entscheidungsbaum die Feature Importance zu bewerten.
Bei einem Random Forest hingegen werden viele Entscheidungsbäume trainiert. Wenn
wir jetzt bei allen Entscheidungsbäumen die Feature Importance berechnen und den
Mittelwert bilden, erhalten wir ein aussagekräftiges Bewertungskriterium, wie
stark einzelne Merkmale die Prognosefähigkeit beeinflussen.

Wir trainieren nun einen Random Forest mit der Standardeinstellung von 100
Entscheidungsbäumen und lassen uns dann die Feature Importance ausgeben.

```{code-cell} ipython3
model = RandomForestClassifier(random_state=0)
model.fit(X,y)

print(model.feature_importances_)
```

Der erste Wert gibt die Feature Importance für das erste Merkmal an und der zweite Wert entsprechend für das zweite Merkmal. Es ist üblich, die Feature Importance als Balkendiagramm zu visualisieren.

```{code-cell} ipython3
feature_importances = pd.Series(model.feature_importances_, index=['Kilometerstand [km]', 'Preis [EUR]'])

fig = px.bar(feature_importances, orientation='h',
  title='Verkaufsaktion im Autohaus', 
  labels={'value':'Feature Importance', 'index': 'Merkmal'})
fig.update_traces(showlegend=False) 
fig.show()
```

Der Preis ist demnach wichtiger als der Kilometerstand (wobei es hier ja ein
künstliches Beispiel ist).

## Zusammenfassung und Ausblick

Random Forests sind einfachen Entscheidungsbäumen vorzuziehen, da sie das
Overfitting reduzieren. Die Erzeugung der einzelnen Entscheidungsbäume kann
parallelisiert werden, so dass das Training eines Random Forests sehr schnell
durchgeführt werden kann. Auch für große Datenmengen mit sehr unterschiedlichen
Eigenschaften arbeitet der Random Forest sehr effizient. Er ermöglicht auch eine
Interpretation, welche Eigenschaften ggf. einen größeren Einfluss haben als
andere Eigenschaften.
