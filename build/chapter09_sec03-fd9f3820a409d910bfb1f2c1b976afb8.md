---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: chapter09_sec03.md
    title: chapter09_sec03.md
---

# 9.3 XGBoost

In der bisherigen Vorlesung haben wir vor allem Pandas und Scikit-Learn benutzt.
Zwar bietet Scikit-Learn Boosting-Verfahren an, in vielen Wettbewerben hat sich
jedoch eine andere Bibliothek durchgesetzt, die eine besonders leistungsfähige
Umsetzung des Gradient Boosting anbietet: **XGBoost**.

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
* [ ] Sie können XGBoost für Klassifikationsaufgaben einsetzen und wissen, dass
  Regression mit `XGBRegressor` genauso funktioniert.
* [ ] Sie wissen, wie Sie mit Analysen der Maßzahlen Fehler und Log Loss für
  Trainings- und Testdaten beurteilen können, ob Überanpassung (Overfitting)
  vorliegt.
* [ ] Sie kennen die Methode **Frühes Stoppen** zur Reduzierung von Overfitting.
* [ ] Sie wissen, dass XGBoost nicht manuell feinjustiert werden sollte, sondern
  mit Gittersuche oder weiteren Bibliotheken (z.B. Optuna).
```

## XGBoost benutzt Scikit-Learn API

In einem früheren Kapitel haben wir Boosting theoretisch kennengelernt: Dabei
werden sequentiell Modelle trainiert, die jeweils die Fehler des
Vorgängermodells korrigieren. XGBoost ist eine hochoptimierte und regularisierte
Umsetzung des Gradient Boosting.

XGBoost steht für e**X**treme **G**radient **Boost**ing und ist aus
Performancegründen in der Programmiersprache C++ implementiert. Für
Python-Programmierer wurde ein Python-Modul mit dem Ziel geschaffen, die
gleichen Schnittstellen wie Scikit-Learn anzubieten, so dass kaum
Einarbeitungszeit in eine neue Bibliothek erforderlich ist. Vor allem benötigen
Data Scientists auch keine C++\-Programmierkenntnisse, sondern können weiterhin
mit Python arbeiten.

Wir bleiben bei unserem Beispiel mit der Verkaufsaktion im Autohaus aus dem
vorherigen Kapitel.

```{code-cell} python
import pandas as pd 
from sklearn.datasets import make_moons

# Erzeugung künstlicher Daten
X_array, y_array = make_moons(n_samples=120, random_state=0, noise=0.3)

daten = pd.DataFrame({
    'Kilometerstand (km)': 10000 * (X_array[:,0] + 2),
    'Preis (EUR)': 5000 * (X_array[:,1] + 2),
    'verkauft': y_array,
    })
```

Wie bei Scikit-Learn trennen wir die Merkmale von der Zielgröße.

```{code-cell} python
# Daten ins richtige Format bringen
X = daten[['Kilometerstand (km)', 'Preis (EUR)']]
y = daten['verkauft'].values
```

Als nächstes importieren wir XGBoost. Es ist üblich, das ganze Modul zu
importieren und mit `xgb` abzukürzen. Danach initialisieren wir das
Klassifikationsmodell `XGBClassifier` und trainieren es auf den Daten.

```{code-cell} python
import xgboost as xgb 

modell = xgb.XGBClassifier(random_state=0)
modell.fit(X, y)
```

Als nächstes visualisieren wir die Prognose des trainierten
XGBoost-Klassifikators. Wie im vorherigen Kapitel verwenden wir dafür
`DecisionBoundaryDisplay` aus Scikit-Learn. Dieser Code baut auf Matplotlib auf
und ist nicht klausurrelevant. Wichtig ist nur, dass Sie das Bild lesen können.

```{code-cell} python
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay

flaechen_farben = ListedColormap(['#EF553B33', '#636EFA33'])
punkt_farben = ListedColormap(['#EF553B', '#636EFA'])

fig = DecisionBoundaryDisplay.from_estimator(modell, X,
    cmap=flaechen_farben, grid_resolution=1000)
fig.ax_.scatter(X['Kilometerstand (km)'], X['Preis (EUR)'], c=y, cmap=punkt_farben)
fig.ax_.set_xlabel('Kilometerstand (km)');
fig.ax_.set_ylabel('Preis (EUR)');
fig.ax_.set_title('XGBoost: Entscheidungsgrenzen');
```

Die Entscheidungsgrenzen sehen sehr plausibel aus.

Genau wie beim Random Forest können wir uns die Feature Importance ausgeben
lassen.

```{code-cell} python
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

Der Preis (0.57) hat eine etwas höhere Feature Importance als der Kilometerstand
(0.43). Wie schon beim Random Forest sollten wir diese Werte nicht überbewerten.
Die Berechnung bevorzugt Merkmale mit vielen verschiedenen Werten und gibt eher
eine Tendenz an als eine exakte Rangfolge.

Hier lösen wir eine Klassifikationsaufgabe und verwenden deshalb den
`XGBClassifier`. Für Regressionsaufgaben gibt es die Klasse `XGBRegressor`. Die
Bedienung ist identisch: `XGBRegressor` initialisieren, mit `.fit()` trainieren
und mit `.predict()` prognostizieren.

```{admonition} Mini-Übung
:class: tip
1. XGBoost und Random Forest kombinieren beide viele Entscheidungsbäume. Worin
   unterscheiden sich die beiden Verfahren darin, wie die Bäume entstehen?
2. Warum ist der Umstieg von Scikit-Learn zu XGBoost besonders leicht?
3. Die Feature Importance bei XGBoost zeigt für den Preis 0.57 und für den
   Kilometerstand 0.43. Was bedeutet das, und was bedeutet es nicht?
```

```{admonition} Lösung
:class: tip
:class: dropdown
1. Beim Random Forest werden alle Bäume unabhängig und parallel auf zufälligen
   Stichproben trainiert. Bei XGBoost werden die Bäume nacheinander trainiert.
   Jeder neue Baum korrigiert die Fehler der bisherigen Bäume.
2. XGBoost bietet dieselben Schnittstellen wie Scikit-Learn: `.fit()` zum
   Trainieren, `.predict()` für Prognosen, `.score()` zur Bewertung.
   C++-Kenntnisse sind nicht nötig.
3. Der Preis trägt in diesem Modell etwas mehr zur Prognose bei als der
   Kilometerstand. Es bedeutet nicht, dass der Preis in der realen Welt
   wichtiger ist. Die Werte sind nur eine Tendenz und hängen von den Daten und
   der Berechnungsart ab.
```

## XGBoost kann zu Overfitting neigen

XGBoost hat zwar eine eingebaute Regularisierung, kann aber bei zu vielen
Boosting-Runden überanpassen. Mit jedem zusätzlichen Baum passt sich das
Gesamtmodell etwas stärker an die Trainingsdaten an. Um das an unserem Beispiel
mit der Verkaufsaktion im Autohaus zu zeigen, fügen wir noch neue, unbekannte
Testdaten hinzu. Dazu verdoppeln wir die Anzahl der Autos (`n_samples=2000`).

```{code-cell} python
# Erzeugung künstlicher Daten
X_array, y_array = make_moons(n_samples=2000, random_state=0, noise=0.3)

daten = pd.DataFrame({
    'Kilometerstand (km)': 10000 * (X_array[:,0] + 2),
    'Preis (EUR)': 5000 * (X_array[:,1] + 2),
    'verkauft': y_array,
    })

X = daten[['Kilometerstand (km)', 'Preis (EUR)']]
y = daten['verkauft'].values
```

Anschließend teilen wir die 2000 Autos in zwei Gruppen: Trainings- und
Testdaten.

```{code-cell} python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=0.5, random_state=0)
```

Diesmal legen wir explizit fest, aus wie vielen Modellen das Boosting-Verfahren
bestehen soll. Dazu setzen wir `n_estimators=200`. Oft wird auch von der Anzahl
der »Boosting-Runden« gesprochen. Das Training auf den Trainingsdaten liefert
ein sehr gutes Ergebnis:

```{code-cell} python
import xgboost as xgb

modell = xgb.XGBClassifier(n_estimators=200, random_state=0)

modell.fit(X_train, y_train)

score_train = modell.score(X_train, y_train)
print(f'Score bezogen auf Trainingsdaten: {score_train:.3f}')
score_test = modell.score(X_test, y_test)
print(f'Score bezogen auf Testdaten: {score_test:.3f}')
```

Die Trainingsdaten werden nahezu perfekt prognostiziert. Auch bei den Testdaten
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

```{code-cell} python
modell = xgb.XGBClassifier(n_estimators=200, eval_metric=['error', 'logloss'], random_state=0)
```

Allerdings ist damit noch nicht festgelegt, auf welchen Daten die Fehler-Maßzahl
und die Log-Loss-Maßzahl berechnet werden. Zunächst sollen beide Maßzahlen für
die Trainingsdaten berechnet werden, dann für die Testdaten. Das erreichen wir
mit dem optionalen Argument `eval_set=`, dem wir folgendermaßen die Trainings-
und Testdaten mitgeben.

```{code-cell} python
modell.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=False)
```

Wir setzen noch `verbose=False`, damit nicht für jedes Modell bzw. jede
Boosting-Runde die vier Maßzahlen auf dem Bildschirm ausgegeben werden. Nach dem
Training können wir die vier Maßzahlen mit der Methode `.evals_result()` aus dem
trainierten Modell extrahieren. Um die Maßzahlen zu visualisieren, packen wir
sie in einen Pandas-DataFrame.

```{code-cell} python
masszahlen = modell.evals_result()
metriken = pd.DataFrame({
    'Fehler Train': masszahlen['validation_0']['error'],
    'Fehler Test': masszahlen['validation_1']['error'],
    'Log Loss Train': masszahlen['validation_0']['logloss'],
    'Log Loss Test': masszahlen['validation_1']['logloss']
    })
```

Wir visualisieren Fehler und Log Loss getrennt voneinander.

```{code-cell} python
import plotly.express as px

# Fehler plotten
fig = px.line(metriken[['Fehler Train', 'Fehler Test']],
    title='Fehler in jeder Boosting-Runde',
    labels={'value': 'Fehler', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()
```

Der Fehler bei den Trainingsdaten wird von Boosting-Runde zu Boosting-Runde
kleiner. Der Fehler der Testdaten sinkt zunächst ebenfalls, erreicht aber schon
nach wenigen Boosting-Runden ein Minimum und steigt danach wieder an. Dieses
Auseinanderlaufen von Training und Test ist typisch für Overfitting. Noch
deutlicher wird es bei der Log-Loss-Maßzahl, die auch bewertet, wie sicher sich
das Modell bei seiner Vorhersage ist.

```{code-cell} python
# Log Loss plotten
fig = px.line(metriken[['Log Loss Train', 'Log Loss Test']],
    title='Log Loss in jeder Boosting-Runde',
    labels={'value': 'Log Loss', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()
```

Auch die Log-Loss-Maßzahl für die Testdaten erreicht nach etwa zehn
Boosting-Runden ihr Minimum und steigt danach an. Nach dieser Analyse wäre es am
besten gewesen, das Training rund um dieses Minimum zu stoppen, bevor die
Überanpassung an die Trainingsdaten einsetzt.

```{admonition} Mini-Übung
:class: tip
1. Im Diagramm sinkt der Fehler auf den Trainingsdaten immer weiter, während der
   Fehler auf den Testdaten ab einem bestimmten Punkt wieder steigt. Wie heißt
   dieses Phänomen, und was sagt es über das Modell aus?
2. Der Fehler und die Log Loss bewerten beide die Klassifikation. Worin
   unterscheiden sich die beiden Maßzahlen?
3. Welche Anzahl an Boosting-Runden wäre für dieses Beispiel eine gute Wahl?
   Begründen Sie mit dem Diagramm.
```

```{admonition} Lösung
:class: tip
:class: dropdown
1. Overfitting (Überanpassung). Das Modell lernt die Trainingsdaten immer
   genauer auswendig, verliert dabei aber die Fähigkeit, gut auf neue Daten zu
   übertragen.
2. Der Fehler zählt nur, ob die Klasse richtig ist (verkauft oder nicht). Die
   Log Loss bewertet zusätzlich, wie sicher sich das Modell war. Eine falsche,
   aber sehr selbstsichere Prognose wird bei der Log Loss stärker bestraft.
3. Etwa die Runde, in der der Fehler bzw. die Log Loss auf den Testdaten ihr
   Minimum erreichen, hier rund 7 bis 10 Runden. Danach verbessert sich nur noch
   die Leistung auf den Trainingsdaten, nicht mehr auf neuen Daten.
```

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

```{code-cell} python
modell = xgb.XGBClassifier(n_estimators=200, early_stopping_rounds=10, eval_metric=['error', 'logloss'], random_state=0)
modell.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=False)
```

Visualisiert sieht die Log-Loss-Statistik für das obige Beispiel so aus:

```{code-cell} python
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

print(f'Training gestoppt nach {modell.best_iteration + 1} Boosting-Runden')
print(f'Kleinste Log-Loss-Maßzahl auf den Testdaten: {modell.best_score:.2f}')
```

Eine weitere Möglichkeit, Überanpassung (Overfitting) zu reduzieren, besteht
darin, die Tiefe der Entscheidungsbäume zu begrenzen. Wir benutzen
Entscheidungsbaum-Stümpfe, die nur einen Split haben. Das erreichen wir mit dem
optionalen Argument `max_depth=1`.

```{code-cell} python
modell = xgb.XGBClassifier(max_depth=1, n_estimators=200, eval_metric=['error', 'logloss'], random_state=0)
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

```{admonition} Mini-Übung
:class: tip
1. Beim frühen Stoppen bricht XGBoost das Training vorzeitig ab. Nach welchem
   Kriterium entscheidet das Verfahren, wann Schluss ist?
2. Warum sollte das frühe Stoppen in einem echten Projekt nicht anhand der
   Testdaten entschieden werden?
3. Nennen Sie zwei Stellschrauben von XGBoost, mit denen sich Overfitting
   verringern lässt, und beschreiben Sie kurz ihre Wirkung.
```

```{admonition} Lösung
:class: tip
:class: dropdown
1. XGBoost beobachtet die Bewertungsmaßzahl auf den Übergabedaten. Wenn sich
   diese Maßzahl über eine festgelegte Anzahl von Boosting-Runden nicht mehr
   verbessert, wird das Training gestoppt und das Modell aus der besten Runde
   verwendet. Technisch: das Argument `early_stopping_rounds=`.
2. Wenn wir die Testdaten schon zum Stoppen verwenden, fließen sie indirekt in
   die Modellwahl ein. Der Testfehler ist dann zu optimistisch (Data Leakage).
   Besser ist ein separates Validierungsset.
3. Frühes Stoppen (`early_stopping_rounds=`) begrenzt die Anzahl der
   Boosting-Runden. `max_depth=` begrenzt die Tiefe der einzelnen Bäume. Sehr
   flache Bäume, zum Beispiel Stümpfe mit `max_depth=1`, können sich weniger
   stark an die Trainingsdaten anpassen.
```

## Vergleich: Random Forest vs. XGBoost

Zum Abschluss dieses Kapitels beschäftigen wir uns noch mit einem Vergleich der
beiden Verfahren Random Forest und XGBoost.

| Aspekt | Random Forest | XGBoost |
| -------- | --------------- | --------- |
| Training | parallel | sequentiell |
| Overfitting | wenig anfällig | anfällig bei zu vielen Runden |
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
