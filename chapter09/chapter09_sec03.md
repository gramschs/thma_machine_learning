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

# 9.3 XGBoost

In der bisherigen Vorlesung haben wir vor allem Pandas und Scikit-Learn benutzt.
Zwar bietet Scikit-Learn Boosting-Verfahren an, in vielen Wettbewerben hat sich
jedoch eine andere Bibliothek durchgesetzt, die eine optimierte Variante des
Stochastic Gradient Boosting anbietet: **XGBoost**.

```{admonition} Warnung
:class: warning
Falls bei Ihnen XGBoost nicht installiert sein sollte, folgen Sie bitte den
Anweisungen auf der Internetseite
[https://xgboost.readthedocs.io](https://xgboost.readthedocs.io/en/stable/install.html)
und installieren Sie XGBoost jetzt nach.
```

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können XGBoost für Regressions- und Klassifikationsaufgaben einsetzen.
* Sie wissen, wie Sie mit Analysen der Maßzahlen Fehler und Log Loss für
  Trainings- und Testdaten beurteilen können, ob Überanpassung (Overfitting)
  vorliegt.
* Sie kennen die Methode **Frühes Stoppen** zur Reduzierung der Überanpassung
  (Overfitting).
* Sie wissen, dass XGBoost nicht manuell feinjustiert werden sollte, sondern mit
  Gittersuche oder weiteren Bibliotheken (z.B. Optuna).
```

## XGBoost benutzt Scikit-Learn API

In einem früheren Kapitel haben wir Stochastic Gradient Boosting theoretisch
kennengelernt: Dabei werden sequentiell Modelle trainiert, die jeweils die
Fehler des Vorgängermodells korrigieren. XGBoost ist eine hochoptimierte und
erweiterte Implementierung dieses Verfahrens.

XGBoost steht für e**X**treme **G**radient **Boost**ing und ist aus
Performancegründen in der Programmiersprache C++ implementiert. Für
Python-Programmierer wurde ein Python-Modul mit dem Ziel geschaffen, die
gleichen Schnittstellen wie Scikit-Learn anzubieten, so dass kaum
Einarbeitungszeit in eine neue Bibliothek erforderlich ist. Vor allem benötigen
Data Scientists auch keine C++\-Programmierkenntnisse, sondern können weiterhin
mit Python arbeiten.

Wir bleiben bei unserem Beispiel mit der Verkaufsaktion im Autohaus aus dem
vorherigen Kapitel.

```{code-cell}
import pandas as pd 
from sklearn.datasets import make_moons

# Erzeugung künstlicher Daten
X_array, y_array = make_moons(n_samples=120, random_state=0, noise=0.3)

daten = pd.DataFrame({
    'Kilometerstand [km]': 10000 * (X_array[:,0] + 2),
    'Preis [EUR]': 5000 * (X_array[:,1] + 2),
    'verkauft': y_array,
    })
```

XGBoost kann Pandas DataFrames nicht verarbeiten, sondern benötigt die reinen
Zahlenwerte in Form von Matrizen. Das ist in der Tat kein Problem, denn die
Datenstruktur DataFrame stellt die reinen Matrizen über die Methode `.values`
direkt zur Verfügung.

```{code-cell}
# Adaption der Daten
X = daten[['Kilometerstand [km]', 'Preis [EUR]']].values
y = daten['verkauft'].values
```

Als nächstes importieren wir XGBoost. Es ist üblich, das ganze Modul zu
importieren und mit `xgb` abzukürzen. Danach initialisieren wir das
Klassifikationsmodell `XGBClassifier` und trainieren es auf den Daten.

```{code-cell}
import xgboost as xgb 

modell = xgb.XGBClassifier()
modell.fit(X,y)
```

Als nächstes visualisieren wir die Prognose des trainierten
XGBoost-Klassifikators.

```{code-cell}
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay

my_colormap = ListedColormap(['#EF553B33', '#636EFA33'])
fig = DecisionBoundaryDisplay.from_estimator(modell, X,  cmap=my_colormap)
fig.ax_.scatter(X[:,0], X[:,1], c=y, cmap=my_colormap)
fig.ax_.set_xlabel('Kilometerstand [km]');
fig.ax_.set_ylabel('Preis [EUR]');
fig.ax_.set_title('XGBoost: Entscheidungsgrenzen');
```

Die Entscheidungsgrenzen sehen sehr plausibel aus.

Genau wie beim Random Forest können wir uns die Feature Importance ausgeben
lassen.

```{code-cell}
# Feature Importance wie bei Random Forest
import plotly.express as px

feature_importance = pd.Series(
    modell.feature_importances_, 
    index=['Kilometerstand', 'Preis']
)

fig = px.bar(feature_importance, orientation='h',
    title='Feature Importance bei XGBoost',
    labels={'value': 'Wichtigkeit', 'index': 'Merkmal'})
fig.update_traces(showlegend=False)
fig.show()
```

Der Preis (0.57) hat eine um den Faktor 1.3 höhere Feature Importance als der
Kilometerstand (0.43). Allerdings liegen hier aus didaktischen Gründen nur
künstliche Daten vor, so dass diese Erkenntnis nicht auf die reale Welt
verallgemeinerbar ist.

## XGBoost neigt stark zur Überanpassung (Overfitting)

XGBoost neigt zu Überanpassung (Overfitting), weil es sehr komplexe Modelle
durch Hinzufügen vieler Bäume erstellt, die sich immer stärker an die
Trainingsdaten anpassen. Um das an unserem Beispiel mit der Verkaufsaktion im
Autohaus zu zeigen, fügen wir noch neue, unbekannte Testdaten hinzu. Dazu
verdoppeln wir die Anzahl der Autos (`n_samples=2000`).

```{code-cell}
# Erzeugung künstlicher Daten
X_array, y_array = make_moons(n_samples=2000, random_state=0, noise=0.3)

daten = pd.DataFrame({
    'Kilometerstand [km]': 10000 * (X_array[:,0] + 2),
    'Preis [EUR]': 5000 * (X_array[:,1] + 2),
    'verkauft': y_array,
    })

X = daten[['Kilometerstand [km]', 'Preis [EUR]']].values
y = daten['verkauft'].values
```

Anschließend teilen wir die 2000 Autos in zwei Gruppen: Trainings- und
Testdaten.

```{code-cell}
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=0.5, random_state=0)
```

Diesmal legen wir explizit fest, aus wie vielen Modellen das Boosting-Verfahren
bestehen soll. Dazu setzen wir `n_estimators=200`. Oft wird auch von der Anzahl
der »Boosting-Runden« gesprochen. Das Training auf den Trainingsdaten liefert
ein sehr gutes Ergebnis:

```{code-cell}
import xgboost as xgb

modell = xgb.XGBClassifier(n_estimators=200)

modell.fit(X_train, y_train)

score_train = modell.score(X_train, y_train)
print(f'Score bezogen auf Trainingsdaten: {score_train:.2f}')
score_test = modell.score(X_test, y_test)
print(f'Score bezogen auf Testdaten: {score_test:.2f}')
```

Die Trainingsdaten werden perfekt prognostiziert. Auch bei den Testdaten
erhalten wir ein gutes Ergebnis, das aber im Vergleich zu dem sehr guten Score
bei den Trainingsdaten abfällt. Es fällt schwer, zu entscheiden, ob eine
Überanpassung (Overfitting) vorliegt. XGBoost ist ein iteratives Verfahren.
Zunächst wird Modell Nr. 1 trainiert, darauf aufbauend Modell Nr. 2 usw. Wir
wiederholen jetzt das Training des XGBoost-Klassifikators, aber lassen durch ein
weiteres Argument mitprotokollieren, was in den einzelnen Boosting-Runden (=
Iterationen) passiert.

Zuerst legen wir fest, welche internen Bewertungskennzahlen (= Metrik, Maßzahl)
mitprotokolliert werden sollen. Wir wählen als erste Maßzahl den Fehler, also
die relative Anzahl der falsch klassifizierten Autos. Die zweite Maßzahl ist die
Log Loss, die nicht nur bewertet, ob die Klassifikation richtig ist, sondern
auch wie sicher das Modell bei seiner Vorhersage ist.

Technisch setzen wir dies um, indem wir bei der Initialisierung des
XGBoost-Modells das optionale Argument `eval_metric=['error', 'logloss']`
setzen.

```{code-cell}
modell = xgb.XGBClassifier(n_estimators=200, eval_metric=['error', 'logloss'])
```

Allerdings ist damit noch nicht festgelegt, auf welchen Daten die Fehler-Maßzahl
und die Log-Loss-Maßzahl berechnet werden. Zunächst sollen beide Maßzahlen für
die Trainingsdaten berechnet werden, dann für die Testdaten. Das erreichen wir
mit dem optionalen Argument `eval_set=`, dem wir folgendermaßen die Trainings-
und Testdaten mitgeben.

```{code-cell}
modell.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=False)
```

Wir setzen noch `verbose=False`, damit nicht für jedes Modell bzw. jede
Boosting-Runde die vier Maßzahlen auf dem Bildschirm ausgegeben werden. Nach dem
Training können wir die vier Maßzahlen mit der Methode `.evals_result()` aus dem
trainierten Modell extrahieren. Um die Maßzahlen zu visualisieren, packen wir
sie in einen Pandas-DataFrame.

```{code-cell} ipython3
masszahlen = modell.evals_result()
metriken = pd.DataFrame({
    'Fehler Train': masszahlen['validation_0']['error'],
    'Fehler Test': masszahlen['validation_1']['error'],
    'Log Loss Train': masszahlen['validation_0']['logloss'],
    'Log Loss Test': masszahlen['validation_1']['logloss']
    })
```

Wir visualisieren Fehler und Log Loss getrennt voneinander.

```{code-cell}
import plotly.express as px

# Fehler plotten
fig = px.line(metriken[['Fehler Train', 'Fehler Test']],
    title='Fehler in jeder Boosting-Runde',
    labels={'value': 'Fehler', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()

# Log Loss plotten
fig = px.line(metriken[['Log Loss Train', 'Log Loss Test']],
    title='Log Loss in jeder Boosting-Runde',
    labels={'value': 'Log Loss', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()
```

Der Fehler bei den Trainingsdaten wird von Boosting-Runde zu Boosting-Runde
kleiner, aber der Fehler der Testdaten wächst. Zunächst wird der Fehler der
Testdaten kleiner, erreicht in Minimum in der 6. Boosting-Runde, um dann wieder zu
steigen. Dieses Verhalten ist typisch für Überanpassung (Overfitting). Etwas
deutlicher wird dieses Phänomen, wenn wir uns die (transformierte) Differenz
der Wahrscheinlichkeiten ansehen, die Log-Loss-Maßzahl.

Am kleinsten ist die Log-Loss-Maßzahl für die Boosting-Runde 9, danach steigt
die Log-Loss-Maßzahl wieder an. Am besten wäre es nach dieser Analyse gewesen,
nach der 6. oder 9. Boosting-Runde aufzuhören, da dann die Überanpassung
(Overfitting) an die Trainingsdaten einsetzt.

## Bekämpfen von Überanpassung (Overfitting)

Es gibt einige Hyperparameter von XGBoost, die helfen, Überanpassung
(Overfitting) zu reduzieren. Eine Möglichkeit ist es, früher zu stoppen und
nicht die voreingestellte Anzahl an Modellen bzw. Boosting-Runden (Iterationen)
zu durchlaufen. Das wird durch das optionale Argument `early_stopping_rounds=`
im Konstruktor ermöglicht. Die Zahl, die diesem Parameter übergeben wird, gibt
die Anzahl der Boosting-Runden vor, nach denen gestoppt wird, falls sich kaum
etwas an der Maßzahl geändert hat.

Wichtig: In der Praxis sollte early stopping nicht auf den Testdaten erfolgen,
sondern auf einem separaten Validierungsset, um Data Leakage zu vermeiden. Für
dieses didaktische Beispiel verwenden wir vereinfacht die Testdaten.

```{code-cell}
modell = xgb.XGBClassifier(n_estimators=200, early_stopping_rounds=10, eval_metric=['error', 'logloss'])
modell.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=False)
```

Visualisiert sieht die Log-Loss-Statistik für das obige Beispiel so aus:

```{code-cell}
masszahlen = modell.evals_result()
metriken = pd.DataFrame({
    'Fehler Train': masszahlen['validation_0']['error'],
    'Fehler Test': masszahlen['validation_1']['error'],
    'Log Loss Train': masszahlen['validation_0']['logloss'],
    'Log Loss Test': masszahlen['validation_1']['logloss']
    })

fig = px.line(metriken[['Fehler Train', 'Fehler Test']],
    title='Frühes Stoppen: Fehler',
    labels={'value': 'Fehler', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()

fig = px.line(metriken[['Log Loss Train', 'Log Loss Test']],
    title='Frühes Stoppen: Log Loss',
    labels={'value': 'Log Loss', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()

print(f'Training gestoppt nach {modell.best_iteration + 1} Boosting-Runde(n)')
print(f'Bester Score auf Testdaten: {modell.best_score}')
```

Eine weitere Möglichkeit, Überanpassung (Overfitting) zu reduzieren, besteht
darin, die Tiefe der Entscheidungsbäume zu begrenzen. Wir benutzen
Entscheidungsbaum-Stümpfe, die nur einen Split haben. Das erreichen wir mit dem
optionalen Argument `max_depth=1`.

```{code-cell}
modell = xgb.XGBClassifier(max_depth=1, n_estimators=200, eval_metric=['error', 'logloss'])
modell.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=False)

masszahlen = modell.evals_result()
metriken = pd.DataFrame({
    'Fehler Train': masszahlen['validation_0']['error'],
    'Fehler Test': masszahlen['validation_1']['error'],
    'Log Loss Train': masszahlen['validation_0']['logloss'],
    'Log Loss Test': masszahlen['validation_1']['logloss']
    })

fig = px.line(metriken[['Fehler Train', 'Fehler Test']],
    title='Begrenzte Entscheidungsbäume: Fehler',
    labels={'value': 'Fehler', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()

fig = px.line(metriken[['Log Loss Train', 'Log Loss Test']],
    title='Begrenzte Entscheidungsbäume: Log Loss',
    labels={'value': 'Log Loss', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()
```

Es gibt noch einige weitere Hyperparameter, die für "das" beste Modell
feinjustiert werden können. Händisch gelingt es kaum, alle Hyperparameter
optimal einzustellen, so dass hier eine Gittersuche oder gar eine Bibliothek wie
[Optuna](https://github.com/optuna/optuna) eingesetzt werden sollte. Das
übersteigt jedoch den zeitlichen Rahmen dieser Vorlesung und wird daher hier
nicht behandelt.

### Vergleich: Random Forest vs. XGBoost

Zum Abschluss dieses Kapitels beschäftigen wir uns noch mit einem Vergleich der beiden Verfahren Random Forest und XGBoost.

| Aspekt | Random Forest | XGBoost |
| -------- | --------------- | --------- |
| Training | parallel | sequentiell |
| Overfitting | weniger anfällig | stark anfällig |
| Hyperparameter-Tuning | wenig nötig | intensiv nötig |
| Geschwindigkeit | schnell | langsamer |
| Typische Genauigkeit | gut | sehr gut |

Random Forests eignen sich gut für einen schnellen ersten Ansatz, während
XGBoost durch sorgfältiges Tuning oft bessere Ergebnisse liefert, aber mehr
Aufwand erfordert.

## Zusammenfassung und Ausblick

Mit XGBoost haben Sie ein ML-Modell für das überwachte Lernen kennengelernt, das
in den vergangenen Jahren sehr viele Wettbewerbe beispielsweise auf der
Plattform Kaggle gewonnen hat. Die Mächtigkeit der Algorithmen führt aber häufig
zur Überanpassung (Overfitting), so dass die sorgsame Feinjustierung der
Hyperparameter besonders wichtig ist.
