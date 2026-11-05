---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: waldtypen_colorado.csv
    title: waldtypen_colorado.csv
  - file: beton_DE.csv
    title: beton_DE.csv
  - file: chapter09_sec04.md
    title: chapter09_sec04.md
---

# 9.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 9.1 bis 9.3. Rechnen Sie mit gut eineinhalb Stunden
Bearbeitungszeit. Wie in den Kapiteln 7.4 und 8.4 besteht die Übung aus zwei
Projekten. In Projekt 9.1 lernen Sie einen neuen Datensatz kennen und
vergleichen Schritt für Schritt einen Entscheidungsbaum, einen Random Forest
und XGBoost bei einer Klassifikationsaufgabe. In Projekt 9.2 kehren Sie zum
Beton aus den Projekten 7.2 und 8.2 zurück und übertragen die Ensemble-Methoden
auf eine Regressionsaufgabe. Dabei treffen Sie mehr Entscheidungen selbst.

Bei den meisten Teilen finden Sie einen Kontrollwert. Damit können Sie prüfen,
ob Ihr Zwischenergebnis stimmt, bevor Sie weiterarbeiten. Die Kontrollwerte
gelten nur für die angegebenen Werte von `random_state`. Für beide Projekte
brauchen Sie XGBoost, siehe Kapitel 9.3.

Beide Datensätze stehen über das Download-Symbol rechts oben zur Verfügung.
Speichern Sie sie in denselben Ordner wie dieses Jupyter Notebook.

* `waldtypen_colorado.csv`: Stichprobe von 20 000 Waldflächen im Roosevelt
  National Forest in Colorado, Spaltennamen und Einträge ins Deutsche
  übersetzt (Quelle: [J. Blackard, Covertype, UCI Machine Learning
  Repository](https://doi.org/10.24432/C50K5N), Lizenz CC BY 4.0)
* `beton_DE.csv`: 1030 Laborversuche zur Druckfestigkeit von Beton,
  Spaltennamen ins Deutsche übersetzt (Quelle: [I-C. Yeh, Concrete Compressive
  Strength, UCI Machine Learning Repository](https://doi.org/10.24432/C5PK67),
  Lizenz CC BY 4.0)

## Projekt 9.1: Welcher Wald wächst hier?

In den Rocky Mountains im Norden von Colorado hat die US-Forstverwaltung für
sehr viele Flächen von 30 m × 30 m erfasst, welcher Waldtyp dort wächst. Jede
Fläche zu begehen ist aufwendig. Kartendaten wie die Höhe, die Hangneigung oder
der Abstand zum nächsten Gewässer liegen dagegen für jede Fläche vor. Lässt sich
der Waldtyp aus diesen Kartendaten prognostizieren? Wir lassen also einen
Random Forest einen echten Wald vorhersagen.

Die Datei `waldtypen_colorado.csv` enthält 20 000 Flächen aus vier
Schutzgebieten. Zu jeder Fläche gibt es sieben Messgrößen:

* die Höhe über dem Meeresspiegel in m,
* die Ausrichtung, also die Himmelsrichtung, in die der Hang zeigt, in Grad
  (0 für Norden, 90 für Osten, 180 für Süden, 270 für Westen),
* die Hangneigung in Grad,
* den waagerechten Abstand und den Höhenunterschied zum nächsten Gewässer in m,
* den Abstand zur nächsten Straße in m,
* den Abstand zur nächsten Stelle, an der ein Waldbrand ausgebrochen ist, in m.

Dazu kommen das Schutzgebiet (`Gebiet`) und der Waldtyp. Es gibt sieben
Waldtypen: Fichte/Tanne, Drehkiefer, Gelbkiefer, Pappel/Weide, Espe, Douglasie
und Krummholz. Rechnen Sie mit etwa 50 Minuten.

```{admonition} Teil 1: Daten erkunden
:class: tip
Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein und verschaffen
Sie sich einen Überblick.

1. Wie oft kommt jeder Waldtyp vor? Welche Accuracy erreicht ein Modell, das
   immer den häufigsten Waldtyp prognostiziert?
2. Stellen Sie die Höhe für jeden Waldtyp in einem Boxplot dar. Welche
   Waldtypen wachsen weit oben, welche weiter unten? Reicht die Höhe allein, um
   die Waldtypen zu unterscheiden?

Zur Kontrolle: Auf 9760 Flächen wächst Drehkiefer.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
```python
import pandas as pd
import plotly.express as px

flaechen = pd.read_csv('waldtypen_colorado.csv', index_col=0)
flaechen.info()
print(flaechen['Waldtyp'].value_counts())
```
Ausgabe:
```
<class 'pandas.core.frame.DataFrame'>
Index: 20000 entries, 24 to 580973
Data columns (total 9 columns):
 #   Column                         Non-Null Count  Dtype 
---  ------                         --------------  ----- 
 0   Hoehe (m)                      20000 non-null  int64 
 1   Ausrichtung (Grad)             20000 non-null  int64 
 2   Hangneigung (Grad)             20000 non-null  int64 
 3   Abstand Wasser horizontal (m)  20000 non-null  int64 
 4   Abstand Wasser vertikal (m)    20000 non-null  int64 
 5   Abstand Strasse (m)            20000 non-null  int64 
 6   Abstand Brandstelle (m)        20000 non-null  int64 
 7   Gebiet                         20000 non-null  object
 8   Waldtyp                        20000 non-null  object
dtypes: int64(7), object(2)
memory usage: 1.5+ MB
Waldtyp
Drehkiefer      9760
Fichte/Tanne    7308
Gelbkiefer      1170
Krummholz        719
Douglasie        592
Espe             346
Pappel/Weide     105
Name: count, dtype: int64
```
1. Es fehlen keine Werte. Die sieben Messgrößen sind ganze Zahlen, das Gebiet
   und der Waldtyp sind Text. Drehkiefer und Fichte/Tanne wachsen zusammen auf
   gut 85 % der Flächen. Pappel/Weide kommt nur auf 105 Flächen vor. Ein
   Modell, das immer Drehkiefer prognostiziert, erreicht eine Accuracy von
   9760 / 20000 = 0.488. Daran messen wir alle weiteren Modelle.

```python
fig = px.box(flaechen, x='Waldtyp', y='Hoehe (m)',
             title='Höhenlage der Waldtypen')
fig.show()
print(flaechen.groupby('Waldtyp')['Hoehe (m)'].median().sort_values())
```
Ausgabe:
```
Waldtyp
Pappel/Weide    2227.0
Gelbkiefer      2411.0
Douglasie       2420.0
Espe            2782.5
Drehkiefer      2939.0
Fichte/Tanne    3147.0
Krummholz       3367.0
Name: Hoehe (m), dtype: float64
```
2. Die Waldtypen wachsen in unterschiedlichen Höhenstufen. Pappel und Weide,
   Gelbkiefer und Douglasie wachsen unten, im Median zwischen gut 2200 und gut
   2400 m.
   Darüber folgen Espe und Drehkiefer, dann Fichte/Tanne. Am höchsten liegt
   das Krummholz mit einem Median von fast 3400 m, also an der Baumgrenze. Die
   Boxen überlappen sich aber stark, vor allem bei den beiden häufigsten
   Waldtypen Drehkiefer und Fichte/Tanne. Die Höhe allein reicht deshalb nicht
   aus.
````

```{admonition} Teil 2: Entscheidungsbaum gegen Random Forest
:class: tip
Kodieren Sie das Gebiet mit der One-Hot-Kodierung. Teilen Sie die Daten in
Trainings- und Testdaten auf, mit 20 % Testdaten und `random_state=0`. Sorgen
Sie dafür, dass die Anteile der Waldtypen in beiden Teilen gleich bleiben,
denn manche Waldtypen sind sehr selten.

Trainieren Sie einen Entscheidungsbaum ohne Begrenzung der Tiefe und einen
Random Forest mit 100 Bäumen, beide mit `random_state=0`.

1. Vergleichen Sie die Accuracy auf den Trainings- und Testdaten. Bei welchem
   Modell sehen Sie Overfitting?
2. Wie viel besser als das Modell aus Teil 1, das immer Drehkiefer
   prognostiziert, sind die beiden Modelle?

Zur Kontrolle: Der Entscheidungsbaum hat die Tiefe 29.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Daten ins richtige Format bringen
flaechen_kodiert = pd.get_dummies(flaechen, columns=['Gebiet'], dtype=int)
X = flaechen_kodiert.drop(columns=['Waldtyp'])
y = flaechen_kodiert['Waldtyp']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0, stratify=y)

baum = DecisionTreeClassifier(random_state=0)
baum.fit(X_train, y_train)
accuracy_training = baum.score(X_train, y_train)
accuracy_test = baum.score(X_test, y_test)
print(f'Baum (Tiefe {baum.get_depth()}): Training {accuracy_training:.3f}, Test {accuracy_test:.3f}')

wald = RandomForestClassifier(random_state=0)
wald.fit(X_train, y_train)
accuracy_training = wald.score(X_train, y_train)
accuracy_test = wald.score(X_test, y_test)
print(f'Wald: Training {accuracy_training:.3f}, Test {accuracy_test:.3f}')
```
Ausgabe:
```
Baum (Tiefe 29): Training 1.000, Test 0.742
Wald: Training 1.000, Test 0.827
```
1. Der Entscheidungsbaum wird 29 Ebenen tief und lernt die Trainingsdaten
   auswendig. Auf den Testdaten erreicht er nur 0.742. Diese große Lücke ist
   das typische Zeichen für Overfitting. Auch der Random Forest erreicht auf
   den Trainingsdaten 1.000, denn er besteht aus 100 unbegrenzten Bäumen. Auf
   den Testdaten liegt er mit 0.827 aber deutlich über dem einzelnen Baum.
   Das Mitteln vieler Bäume gleicht einen Teil ihrer zufälligen Fehler aus,
   wie in Kapitel 9.2.
2. Das Modell, das immer Drehkiefer prognostiziert, erreicht 0.488. Der Baum
   liegt gut 25 Prozentpunkte darüber, der Random Forest fast 34
   Prozentpunkte.
````

```{admonition} Teil 3: Feature Importance
:class: tip
Stellen Sie die Feature Importance des Random Forests als Balkendiagramm dar,
sortiert nach ihrer Größe.

1. Welches Merkmal ist am wichtigsten? Passt das zu Ihrem Boxplot aus Teil 1?
2. Das Gebiet ist durch die One-Hot-Kodierung auf vier Spalten verteilt. Wie
   wichtig ist das Gebiet insgesamt?
3. Auf den Plätzen zwei und drei liegen der Abstand zur nächsten Straße und
   der Abstand zur nächsten Brandstelle. Wächst eine Fichte, weil die Straße
   weit weg ist? Was zeigt die Feature Importance, und was zeigt sie nicht?

Zur Kontrolle: Die Höhe hat eine Feature Importance von 0.329.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
feature_importances = pd.Series(wald.feature_importances_, index=X.columns)

fig = px.bar(feature_importances.sort_values(), orientation='h',
             title='Feature Importance: Waldtypen',
             labels={'value': 'Feature Importance', 'index': 'Merkmal'})
fig.update_traces(showlegend=False)
fig.show()
print(feature_importances.sort_values(ascending=False).round(3))
```
Ausgabe:
```
Hoehe (m)                        0.329
Abstand Strasse (m)              0.136
Abstand Brandstelle (m)          0.127
Ausrichtung (Grad)               0.105
Abstand Wasser horizontal (m)    0.088
Abstand Wasser vertikal (m)      0.083
Hangneigung (Grad)               0.068
Gebiet_Cache la Poudre           0.033
Gebiet_Rawah                     0.014
Gebiet_Comanche Peak             0.011
Gebiet_Neota                     0.006
dtype: float64
```
1. Die Höhe ist mit 0.329 mit Abstand am wichtigsten. Das passt zu den
   Höhenstufen im Boxplot aus Teil 1.
2. Zusammen kommen die vier Gebietsspalten auf 0.033 + 0.014 + 0.011 + 0.006 =
   0.064. Das Gebiet ist also weniger wichtig als jede einzelne Messgröße. Ein
   Grund: Die Gebiete liegen unterschiedlich hoch, und diese Information
   steckt schon in der Höhe.
3. Nein. Die Feature Importance zeigt nur, welche Merkmale der Random Forest
   für seine Prognosen nutzt. Über Ursachen sagt sie nichts. Straßen und
   Brandstellen liegen an bestimmten Orten. Ihre Abstände verraten deshalb
   ungefähr, wo im Gebiet eine Fläche liegt, und Waldtypen wachsen oft in
   zusammenhängenden Bereichen. Außerdem haben die Abstände sehr viele
   verschiedene Werte. Wie in Kapitel 9.2 beschrieben, bevorzugt die
   Feature Importance solche Merkmale.
````

```{admonition} Teil 4: XGBoost
:class: tip
XGBoost erwartet die Klassen als ganze Zahlen von 0 bis 6. Kodieren Sie den
Waldtyp in den Trainings- und Testdaten entsprechend. Welcher Waldtyp welche
Zahl bekommt, spielt keine Rolle.

Trainieren Sie dann ein XGBoost-Modell mit 200 Boosting-Runden und
`random_state=0`. Lassen Sie dabei wie in Kapitel 9.3 den Fehler und den Log
Loss für die Trainings- und Testdaten mitprotokollieren. Bei mehr als zwei
Klassen heißen diese Maßzahlen in XGBoost `'merror'` und `'mlogloss'`.

1. Vergleichen Sie die Accuracy auf den Testdaten mit dem Random Forest.
2. Stellen Sie den Fehler und den Log Loss in jeder Boosting-Runde dar. Nach
   wie vielen Runden erreichen die beiden Maßzahlen auf den Testdaten ihr
   Minimum? Vergleichen Sie mit dem Beispiel aus Kapitel 9.3. Würde frühes
   Stoppen hier helfen?

Zur Kontrolle: Auf den Trainingsdaten erreicht XGBoost eine Accuracy von
0.991.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 4
:class: tip
:class: dropdown
```python
import xgboost as xgb

# XGBoost erwartet die Klassen als Zahlen 0 bis 6
waldtyp_kodierung = {
    'Fichte/Tanne': '0',
    'Drehkiefer': '1',
    'Gelbkiefer': '2',
    'Pappel/Weide': '3',
    'Espe': '4',
    'Douglasie': '5',
    'Krummholz': '6',
}
y_train_kodiert = y_train.replace(waldtyp_kodierung).astype('int')
y_test_kodiert = y_test.replace(waldtyp_kodierung).astype('int')

modell = xgb.XGBClassifier(n_estimators=200, eval_metric=['merror', 'mlogloss'], random_state=0)
modell.fit(X_train, y_train_kodiert,
           eval_set=[(X_train, y_train_kodiert), (X_test, y_test_kodiert)], verbose=False)
accuracy_training = modell.score(X_train, y_train_kodiert)
accuracy_test = modell.score(X_test, y_test_kodiert)
print(f'XGBoost: Training {accuracy_training:.3f}, Test {accuracy_test:.3f}')
```
Ausgabe:
```
XGBoost: Training 0.991, Test 0.817
```
1. XGBoost erreicht auf den Testdaten 0.817 und liegt damit knapp hinter dem
   Random Forest mit 0.827.

In einer neuen Code-Zelle stellen wir die Maßzahlen dar:
```python
masszahlen = modell.evals_result()
metriken = pd.DataFrame({
    'Fehler Train': masszahlen['validation_0']['merror'],
    'Fehler Test': masszahlen['validation_1']['merror'],
    'Log Loss Train': masszahlen['validation_0']['mlogloss'],
    'Log Loss Test': masszahlen['validation_1']['mlogloss']
    })

fig = px.line(metriken[['Fehler Train', 'Fehler Test']],
    title='Fehler in jeder Boosting-Runde',
    labels={'value': 'Fehler', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()

fig = px.line(metriken[['Log Loss Train', 'Log Loss Test']],
    title='Log Loss in jeder Boosting-Runde',
    labels={'value': 'Log Loss', 'index': 'Boosting-Runde', 'variable': 'Legende'})
fig.show()
```
2. Der Fehler auf den Trainingsdaten sinkt bis auf knapp 0.01. Der Fehler auf
   den Testdaten sinkt fast bis zur letzten Runde und erreicht sein Minimum
   von 0.181 erst in Runde 196. Der Log Loss auf den Testdaten erreicht sein
   Minimum von 0.467 nach rund 150 Runden und steigt danach nur ganz leicht
   an. Im Beispiel aus Kapitel 9.3 lag das Minimum schon bei etwa 10 Runden.
   Hier setzt Overfitting viel später ein, denn es gibt 16 000 Trainingsdaten
   statt 1000. Frühes Stoppen hilft hier kaum, wie die folgende Rechnung
   zeigt. Wie in Kapitel 9.3 verwenden wir dafür vereinfacht die Testdaten.

```python
modell_stopp = xgb.XGBClassifier(n_estimators=200, early_stopping_rounds=10,
                                 eval_metric=['merror', 'mlogloss'], random_state=0)
modell_stopp.fit(X_train, y_train_kodiert,
                 eval_set=[(X_train, y_train_kodiert), (X_test, y_test_kodiert)], verbose=False)
print(f'Training gestoppt nach {modell_stopp.best_iteration + 1} Boosting-Runden')
print(f'Accuracy Test: {modell_stopp.score(X_test, y_test_kodiert):.3f}')
```
Ausgabe:
```
Training gestoppt nach 151 Boosting-Runden
Accuracy Test: 0.812
```
Das frühe Stoppen orientiert sich an der letzten Maßzahl in der Liste, hier
also am Log Loss. Das Modell aus Runde 151 ist auf den Testdaten sogar etwas
schlechter als nach 200 Runden.
````

```{admonition} Abschlussfrage
:class: tip
Welches der drei Modelle würden Sie der Forstverwaltung empfehlen?

Wie gut erkennt der Random Forest die einzelnen Waldtypen? Berechnen Sie die
Accuracy getrennt für die Testflächen jedes Waldtyps. Tipp: Wenden Sie die
Methode `.score()` nur auf die Testflächen eines einzelnen Waldtyps an. Was
verrät die gesamte Accuracy über die seltenen Waldtypen?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Abschlussfrage
:class: tip
:class: dropdown
| Modell | Accuracy Training | Accuracy Test |
| --- | --- | --- |
| immer Drehkiefer | 0.488 | 0.488 |
| Entscheidungsbaum | 1.000 | 0.742 |
| Random Forest | 1.000 | 0.827 |
| XGBoost mit 200 Runden | 0.991 | 0.817 |

Wir würden den Random Forest empfehlen. Er erreicht die höchste Accuracy auf
den Testdaten und funktioniert ohne jede Feinjustierung. XGBoost liegt knapp
dahinter. Wie die Tabelle in Kapitel 9.3 sagt, kann XGBoost mit sorgfältig
eingestellten Hyperparametern oft noch zulegen. Das ist aber Aufwand, und wie
wir Hyperparameter systematisch suchen, lernen wir erst in Kapitel 10.

```python
for waldtyp in y_test.value_counts().index:
    auswahl = y_test == waldtyp
    anzahl = len(y_test[auswahl])
    accuracy_waldtyp = wald.score(X_test[auswahl], y_test[auswahl])
    print(f'{waldtyp}: {anzahl} Testflächen, Accuracy {accuracy_waldtyp:.2f}')
```
Ausgabe:
```
Drehkiefer: 1952 Testflächen, Accuracy 0.88
Fichte/Tanne: 1462 Testflächen, Accuracy 0.83
Gelbkiefer: 234 Testflächen, Accuracy 0.83
Krummholz: 144 Testflächen, Accuracy 0.69
Douglasie: 118 Testflächen, Accuracy 0.45
Espe: 69 Testflächen, Accuracy 0.28
Pappel/Weide: 21 Testflächen, Accuracy 0.48
```
Die häufigen Waldtypen erkennt der Random Forest gut, die seltenen schlecht.
Von den Espen-Flächen ordnet er nicht einmal jede dritte richtig ein. Die
gesamte Accuracy von 0.827 verdeckt das, denn sie wird von den vielen Flächen
mit Drehkiefer und Fichte/Tanne bestimmt. Wer sich gerade für Espen oder
Douglasien interessiert, darf sich auf diese Zahl nicht verlassen. Mit welchen
Gütemaßen wir solche Schwächen sichtbar machen, lernen wir in Kapitel 10.3.
````

## Projekt 9.2: Beton, die dritte Runde

In Projekt 7.2 haben wir lineare Modelle für die Druckfestigkeit von Beton
trainiert, in Projekt 8.2 haben wir sie und weitere Modelle mit Testdaten
geprüft. Am besten schnitten dort das Polynom 3. Grades und der
Entscheidungsbaum ab. Jetzt treten die Ensemble-Methoden gegen sie an. Damit
der Vergleich fair ist, verwenden wir dieselbe Aufteilung in Trainings- und
Testdaten wie in Projekt 8.2. Projekt 9.2 ist offener als Projekt 9.1. Rechnen
Sie mit etwa 40 Minuten.

```{admonition} Teil 1: Random Forest und XGBoost
:class: tip
Lesen Sie die Datei `beton_DE.csv` mit der Spalte `Nr.` als Zeilenindex ein und
teilen Sie die Daten wie in Projekt 8.2 auf, mit 20 % Testdaten und
`random_state=0`. Verwenden Sie die sieben Bestandteile und das Alter als
Merkmale.

Für Regressionsaufgaben gibt es den `RandomForestRegressor`. Er wird ebenfalls
aus `sklearn.ensemble` importiert und genauso verwendet wie der
`RandomForestClassifier`. Bei XGBoost heißt das Gegenstück `XGBRegressor`.

Trainieren Sie einen Random Forest und ein XGBoost-Modell, beide mit
`random_state=0` und sonst mit den voreingestellten Werten. Vergleichen Sie die
R²-Scores auf den Trainings- und Testdaten mit den Modellen aus Projekt 8.2.

Zur Kontrolle: Der Random Forest erreicht auf den Trainingsdaten einen
R²-Score von 0.98.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
```python
import pandas as pd
import plotly.express as px
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

beton = pd.read_csv('beton_DE.csv', index_col=0)
beton_train, beton_test = train_test_split(beton, test_size=0.2, random_state=0)

merkmale = ['Zement (kg/m3)', 'Huettensand (kg/m3)', 'Flugasche (kg/m3)',
            'Wasser (kg/m3)', 'Fliessmittel (kg/m3)',
            'Grobzuschlag (kg/m3)', 'Feinzuschlag (kg/m3)', 'Alter (Tage)']
X_train = beton_train[merkmale]
X_test = beton_test[merkmale]
y_train = beton_train['Druckfestigkeit (MPa)']
y_test = beton_test['Druckfestigkeit (MPa)']

wald_beton = RandomForestRegressor(random_state=0)
wald_beton.fit(X_train, y_train)
r2_training = wald_beton.score(X_train, y_train)
r2_test = wald_beton.score(X_test, y_test)
print(f'Random Forest: Training {r2_training:.2f}, Test {r2_test:.2f}')

boosting_beton = xgb.XGBRegressor(random_state=0)
boosting_beton.fit(X_train, y_train)
r2_training = boosting_beton.score(X_train, y_train)
r2_test = boosting_beton.score(X_test, y_test)
print(f'XGBoost: Training {r2_training:.2f}, Test {r2_test:.2f}')
```
Ausgabe:
```
Random Forest: Training 0.98, Test 0.93
XGBoost: Training 1.00, Test 0.93
```
Beide Ensemble-Methoden erreichen auf den Testdaten einen R²-Score von 0.93.
Das ist deutlich mehr als bei allen Modellen aus Projekt 8.2. Dort lag das
Polynom 3. Grades mit 0.81 vorn, der einzelne Entscheidungsbaum erreichte 0.78.
Beim Random Forest liegen Training und Test nah beieinander. XGBoost passt
sich den Trainingsdaten fast perfekt an und ist auf den Testdaten trotzdem
genauso gut.
````

```{admonition} Teil 2: Was zählt für die Druckfestigkeit?
:class: tip
Stellen Sie die Feature Importance des Random Forests als Balkendiagramm dar.

In Projekt 8.2 haben wir die Merkmale mit den standardisierten Koeffizienten
der linearen Regression verglichen. Dort lag der Zement vorn, gefolgt von
Hüttensand und Alter. Welche Rangfolge ergibt die Feature Importance? Haben
Sie eine Erklärung für den Unterschied? Denken Sie an den Scatterplot von
Alter und Druckfestigkeit aus Projekt 7.2.

Zur Kontrolle: Der Zement hat eine Feature Importance von 0.280.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
feature_importances = pd.Series(wald_beton.feature_importances_, index=merkmale)

fig = px.bar(feature_importances.sort_values(), orientation='h',
             title='Feature Importance: Druckfestigkeit von Beton',
             labels={'value': 'Feature Importance', 'index': 'Merkmal'})
fig.update_traces(showlegend=False)
fig.show()
print(feature_importances.sort_values(ascending=False).round(3))
```
Ausgabe:
```
Alter (Tage)            0.345
Zement (kg/m3)          0.280
Wasser (kg/m3)          0.106
Fliessmittel (kg/m3)    0.106
Huettensand (kg/m3)     0.071
Feinzuschlag (kg/m3)    0.042
Grobzuschlag (kg/m3)    0.029
Flugasche (kg/m3)       0.021
dtype: float64
```
Für den Random Forest ist das Alter am wichtigsten, knapp vor dem Zement. In
der linearen Regression lag das Alter nur auf Platz drei. Der Scatterplot aus
Projekt 7.2 zeigt den Grund: In den ersten Wochen steigt die Druckfestigkeit
steil an, danach nur noch wenig. Eine lineare Regression kann im Alter nur
eine Gerade abbilden und nutzt deshalb nur einen Teil dieser Information. Die
Bäume des Random Forests teilen das Alter dagegen in Abschnitte ein und bilden
so auch den gekrümmten Verlauf ab.

Beide Verfahren sind sich einig, dass der Zement eine große Rolle spielt und
Grobzuschlag und Feinzuschlag eine kleine. Ganz vergleichen lassen sich die
Zahlen aber nicht. Ein standardisierter Koeffizient gibt an, wie stark sich die
Prognose ändert, wenn ein Merkmal um eine Standardabweichung steigt. Die
Feature Importance misst dagegen, wie oft und wie erfolgreich die Bäume mit
einem Merkmal trennen. Und wie in Kapitel 9.2 gilt: Sie gibt eher eine Tendenz
an als eine exakte Rangfolge.
````

```{admonition} Teil 3: Prognose für die Rezeptur aus Projekt 7.2
:class: tip
In Projekt 7.2 Teil 4 haben wir die Druckfestigkeit der Rezeptur mit 540 kg
Zement, 173 kg Wasser, 1125 kg Grobzuschlag und 613 kg Feinzuschlag pro
Kubikmeter, ohne Hüttensand, Flugasche und Fließmittel, für ein Alter von 1 bis
730 Tagen prognostiziert. Nach zwei Jahren lieferten die linearen Modelle dort
131.5 MPa und -133.1 MPa.

Wiederholen Sie diese Prognose mit dem Random Forest und dem XGBoost-Modell
aus Teil 1. Stellen Sie die Messwerte der Rezeptur und beide Prognosekurven in
einem gemeinsamen Diagramm dar.

1. Wie gut folgen die Kurven den Messwerten?
2. Was prognostizieren die beiden Modelle nach zwei Jahren? Warum verlaufen die
   Kurven ab einem bestimmten Alter waagerecht?
3. Fünf der sieben Probekörper dieser Rezeptur liegen in den Trainingsdaten.
   Was bedeutet das für die Güte der Kurven?

Zur Kontrolle: Für ein Alter von 28 Tagen prognostiziert der Random Forest
66.9 MPa.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
messungen = beton[(beton['Zement (kg/m3)'] == 540) & (beton['Wasser (kg/m3)'] == 173)]

# Einzelwerte gelten für alle Zeilen, das Alter läuft von 1 bis 730 Tage
rezeptur = pd.DataFrame({
    'Zement (kg/m3)': 540,
    'Huettensand (kg/m3)': 0,
    'Flugasche (kg/m3)': 0,
    'Wasser (kg/m3)': 173,
    'Fliessmittel (kg/m3)': 0,
    'Grobzuschlag (kg/m3)': 1125,
    'Feinzuschlag (kg/m3)': 613,
    'Alter (Tage)': range(1, 731)
    })
rezeptur['Random Forest'] = wald_beton.predict(rezeptur[merkmale])
rezeptur['XGBoost'] = boosting_beton.predict(rezeptur[merkmale])

fig = px.scatter(messungen, x='Alter (Tage)', y='Druckfestigkeit (MPa)',
                 title='Rezeptur mit 540 kg Zement: Messwerte und Prognosen')
fig.add_scatter(x=rezeptur['Alter (Tage)'], y=rezeptur['Random Forest'],
                mode='lines', name='Random Forest')
fig.add_scatter(x=rezeptur['Alter (Tage)'], y=rezeptur['XGBoost'],
                mode='lines', name='XGBoost')
fig.show()
```
1. Beide Kurven verlaufen in Stufen und folgen den Messwerten sehr eng. Nach
   28 Tagen wurden 67.3 MPa gemessen. Der Random Forest prognostiziert
   66.9 MPa, XGBoost 67.6 MPa. Die linearen Modelle aus Projekt 7.2 lagen hier
   noch rund 15 MPa zu niedrig.
2. Nach zwei Jahren prognostiziert der Random Forest 73.2 MPa und XGBoost
   74.2 MPa. Das ist plausibel, ganz anders als die 131.5 MPa und -133.1 MPa
   der linearen Modelle. Spätestens ab einem Alter von 270 Tagen verlaufen
   beide Kurven waagerecht. Beide Modelle bestehen aus Entscheidungsbäumen,
   und ein Baum kann nur Werte prognostizieren, die in seinen Blättern stehen.
   Wie der Baum in Projekt 7.1 setzt er keinen Trend über den Datenbereich
   hinaus fort. Dass echter Beton auch nach einem Jahr noch langsam fester wird,
   bilden die Modelle deshalb nicht ab.
3. Die Kurven sehen besser aus, als die Modelle für eine ganz neue Rezeptur
   wären. Die Modelle kennen fünf Messwerte genau dieser Rezeptur aus dem
   Training. Auch die beiden Probekörper in den Testdaten, nach 3 und nach
   7 Tagen, haben Nachbarn derselben Rezeptur in den Trainingsdaten, zum
   Beispiel den Probekörper nach 14 Tagen.
````

```{admonition} Abschlussfrage
:class: tip
Stellen Sie die R²-Scores auf den Testdaten aller Betonmodelle aus den
Projekten 8.2 und 9.2 in einer Tabelle zusammen. Welches Modell würden Sie
dem Betonwerk jetzt empfehlen?

In der Abschlussfrage von Projekt 8.2 haben wir gesehen, dass der Testscore für
ganz neue Rezepturen zu optimistisch ist. Was bedeutet das für Ihre
Empfehlung?
```

````{admonition} Lösung Abschlussfrage
:class: tip
:class: dropdown
| Modell | Projekt | R²-Score Test |
| --- | --- | --- |
| linear mit Alter | 8.2 | 0.64 |
| linear mit Alter und Alter hoch 2 | 8.2 | 0.72 |
| Polynom Grad 3 | 8.2 | 0.81 |
| Entscheidungsbaum ohne Begrenzung | 8.2 | 0.78 |
| Random Forest | 9.2 | 0.93 |
| XGBoost | 9.2 | 0.93 |

Wir würden den Random Forest empfehlen. Er ist so gut wie XGBoost, braucht
aber keine Feinjustierung und neigt weniger zu Overfitting. Wie alle Modelle
aus Bäumen taugt er nur für ein Alter innerhalb des Datenbereichs, also bis
365 Tage.

Für ganz neue Rezepturen ist auch der Wert 0.93 zu optimistisch. Teilen wir
die Daten so auf, dass alle Probekörper einer Rezeptur gemeinsam in den
Trainings- oder in den Testdaten landen, sinkt der R²-Score des Random
Forests. In zehn solchen Aufteilungen liegt er zwischen 0.79 und 0.89, im
Mittel bei 0.85. Selbst dann liegt er im Mittel noch über dem besten Modell
aus Projekt 8.2, das ja ebenfalls von der zufälligen Aufteilung profitiert
hat. An der Empfehlung ändert sich also nichts. Für das Betonwerk ist aber
0.85 die ehrlichere Zahl.

Bisher haben wir jedes Modell mit einer einzigen zufälligen Aufteilung
bewertet. In Kapitel 10 lernen wir mit der Kreuzvalidierung, Modelle
zuverlässiger zu vergleichen, und mit der Gittersuche, Hyperparameter
systematisch einzustellen.
````
