---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: ../notebooks/chapter10/chapter10_sec04.ipynb
    title: chapter10_sec04.ipynb
  - file: pinguine.csv
    title: pinguine.csv
  - file: chapter10_sec04.md
    title: chapter10_sec04.md
---

# 10.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 10.1 bis 10.3. Rechnen Sie mit gut einer Stunde
Bearbeitungszeit. Die Übung besteht aus zwei Projekten mit demselben Datensatz.
In Projekt 10.1 wählen Sie mit Kreuzvalidierung und Gittersuche ein Modell aus
und bewerten es am Ende ehrlich mit Testdaten. In Projekt 10.2 bewerten Sie
Modelle mit den Gütemaßen aus Kapitel 10.3.

Bei den meisten Teilen finden Sie einen Kontrollwert. Damit können Sie prüfen,
ob Ihr Zwischenergebnis stimmt, bevor Sie weiterarbeiten. Die Kontrollwerte
gelten nur für die angegebenen Werte von `random_state`.

Der Datensatz steht über das Download-Symbol rechts oben zur Verfügung.
Speichern Sie ihn in denselben Ordner wie dieses Jupyter Notebook.

* `pinguine.csv`: Messungen an 344 Pinguinen aus der Antarktis, Spaltennamen
  und Einträge ins Deutsche übersetzt (Quelle: [A. M. Horst, A. P. Hill, K. B.
  Gorman, palmerpenguins](https://doi.org/10.5281/zenodo.3960218), Lizenz CC0)

Die Daten stammen von der Forschungsstation Palmer in der Antarktis. Von 2007
bis 2009 haben Forschende dort Pinguine auf drei Inseln vermessen und gewogen.
Zu jedem Pinguin gibt es

* die Art (Adeliepinguin, Eselspinguin oder Zügelpinguin),
* die Insel, auf der er gefunden wurde (Biscoe, Dream oder Torgersen),
* die Länge und die Tiefe, also die Höhe, des Schnabels in mm,
* die Länge der Flosse in mm,
* das Körpergewicht in g,
* das Geschlecht und
* das Jahr der Messung.

## Projekt 10.1: Männchen oder Weibchen?

Bei Pinguinen sehen Männchen und Weibchen fast gleich aus. Die Forschenden auf
Palmer haben das Geschlecht deshalb mit einer Blutprobe bestimmt. Lässt es sich
auch aus den Körpermaßen und der Art vorhersagen? In diesem Projekt gehen Sie
so vor wie in Kapitel 10.2: Zuerst legen Sie Testdaten zur Seite, dann wählen
Sie mit den Validierungsscores ein Modell aus und bewerten nur dieses Modell
einmal mit den Testdaten. Rechnen Sie mit etwa 30 Minuten.

```{admonition} Teil 1: Daten vorbereiten
:class: tip
Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein.

1. In welchen Spalten fehlen Werte, und wie viele? Löschen Sie alle Zeilen, in
   denen mindestens ein Wert fehlt. Das geht mit der Methode `dropna()`.
2. Kodieren Sie die Art mit der One-Hot-Kodierung. Verwenden Sie als
   Eingabedaten die vier Körpermaße und die kodierte Art, als Zielgröße das
   Geschlecht.
3. Legen Sie 20 % der Daten als Testdaten zur Seite, mit `random_state=0`.
   Sorgen Sie dafür, dass das Verhältnis von Männchen und Weibchen in beiden
   Teilen etwa gleich ist. Welche Accuracy erreicht auf den Testdaten ein
   Referenzmodell, das immer das häufigere Geschlecht vorhersagt?

Zur Kontrolle: Nach dem Löschen bleiben 333 Pinguine übrig.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
```python
import pandas as pd
from sklearn.model_selection import train_test_split

pinguine = pd.read_csv('pinguine.csv', index_col=0)
print(pinguine.isnull().sum())

pinguine = pinguine.dropna()
print(f'Anzahl Pinguine: {len(pinguine)}')
```
Ausgabe:
```
Art                     0
Insel                   0
Schnabellaenge (mm)     2
Schnabeltiefe (mm)      2
Flossenlaenge (mm)      2
Koerpergewicht (g)      2
Geschlecht             11
Jahr                    0
dtype: int64
Anzahl Pinguine: 333
```
1. Bei zwei Pinguinen fehlen alle vier Körpermaße. Beim Geschlecht fehlen 11
   Angaben. Die zwei Pinguine ohne Körpermaße gehören zu diesen 11. Nach dem
   Löschen bleiben 333 Pinguine übrig.

```python
# Daten ins richtige Format bringen
pinguine_kodiert = pd.get_dummies(pinguine, columns=['Art'], dtype=int)
X = pinguine_kodiert.drop(columns=['Insel', 'Geschlecht', 'Jahr'])
y = pinguine_kodiert['Geschlecht']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0, stratify=y)
print(f'Trainingsdaten: {len(X_train)}, Testdaten: {len(X_test)}')
print(y_test.value_counts())
```
Ausgabe:
```
Trainingsdaten: 266, Testdaten: 67
Geschlecht
männlich    34
weiblich    33
Name: count, dtype: int64
```
2. Statt die Spalten der Eingabedaten einzeln aufzuzählen, löschen wir die
   Spalten, die wir nicht brauchen. So müssen wir die Namen der kodierten
   Spalten nicht abtippen.
3. In den Testdaten sind 34 Männchen und 33 Weibchen. Ein Referenzmodell, das
   immer "männlich" vorhersagt, erreicht eine Accuracy von 34 / 67 = 0.51. Die
   Klassen sind also ausgewogen, und die Accuracy ist hier ein geeignetes
   Gütemaß.
````

```{admonition} Teil 2: Baumtiefe mit Kreuzvalidierung wählen
:class: tip
Vergleichen Sie Entscheidungsbäume mit den Tiefen 1 bis 8 per
Kreuzvalidierung auf den Trainingsdaten. Verwenden Sie fünf Folds, mischen Sie
die Daten vorher und sorgen Sie dafür, dass das Verhältnis der Geschlechter in
jedem Fold erhalten bleibt. Setzen Sie bei der Aufteilung und beim
Entscheidungsbaum `random_state=0`. Geben Sie für jede Tiefe den Mittelwert und
die Standardabweichung der Validierungsscores sowie den Mittelwert der
Trainingsscores aus.

1. Welche Tiefe erreicht den besten mittleren Validierungsscore? Wie groß ist
   ihr Vorsprung vor der Tiefe 2, verglichen mit der Standardabweichung?
2. Bei welcher Tiefe sehen Sie Underfitting, bei welcher Overfitting? Begründen
   Sie mit den Trainings- und Validierungsscores.

Zur Kontrolle: Bei der Tiefe 1 beträgt der mittlere Validierungsscore 0.628.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.tree import DecisionTreeClassifier

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

for max_tiefe in [1, 2, 3, 4, 5, 6, 7, 8]:
    baum = DecisionTreeClassifier(max_depth=max_tiefe, random_state=0)
    cv_results = cross_validate(baum, X_train, y_train, cv=kfold, return_train_score=True)
    mittelwert = np.mean(cv_results['test_score'])
    streuung = np.std(cv_results['test_score'])
    mittelwert_training = np.mean(cv_results['train_score'])
    print(f'Tiefe {max_tiefe}: Validierung {mittelwert:.3f} (Std. {streuung:.3f}), '
          f'Training {mittelwert_training:.3f}')
```
Ausgabe:
```
Tiefe 1: Validierung 0.628 (Std. 0.025), Training 0.727
Tiefe 2: Validierung 0.846 (Std. 0.037), Training 0.874
Tiefe 3: Validierung 0.842 (Std. 0.043), Training 0.918
Tiefe 4: Validierung 0.857 (Std. 0.048), Training 0.948
Tiefe 5: Validierung 0.857 (Std. 0.052), Training 0.976
Tiefe 6: Validierung 0.876 (Std. 0.033), Training 0.988
Tiefe 7: Validierung 0.850 (Std. 0.042), Training 0.993
Tiefe 8: Validierung 0.842 (Std. 0.030), Training 0.998
```
1. Die Tiefe 6 erreicht mit 0.876 den besten mittleren Validierungsscore. Die
   Tiefe 2 kommt auf 0.846. Der Vorsprung von 0.03 ist kleiner als die
   Standardabweichungen von 0.033 und 0.037. Der viel einfachere Baum der
   Tiefe 2 ist also kaum schlechter.
2. Bei der Tiefe 1 sind Trainings- und Validierungsscore mit 0.727 und 0.628
   beide niedrig. Eine einzige Frage reicht nicht, um das Geschlecht zu
   erkennen. Das deutet auf Underfitting hin. Bei der Tiefe 8 liegt der
   Trainingsscore mit 0.998 fast bei 1, der Validierungsscore mit 0.842 aber
   deutlich darunter. Der Baum lernt die Trainingsdaten fast auswendig. Das
   deutet auf Overfitting hin.
````

```{admonition} Teil 3: Random Forest mit Gittersuche
:class: tip
Stimmen Sie jetzt einen Random Forest mit einer Gittersuche ab. Verwenden Sie
dieselbe Fold-Aufteilung wie in Teil 2 und `random_state=0` für den Random
Forest. Durchsuchen Sie für die maximale Tiefe die Werte 2, 4, 6, 8 und `None`
und für die minimale Anzahl an Datenpunkten pro Blatt die Werte 1, 5 und 10.
`None` steht für eine unbegrenzte Tiefe.

1. Wie viele Kombinationen werden getestet, und wie viele Random Forests werden
   dabei trainiert?
2. Welche Kombination ist am besten? Entscheiden Sie anhand der
   Validierungsscores, ob Sie den besten Entscheidungsbaum aus Teil 2 oder den
   Random Forest einsetzen.
3. Bewerten Sie nur das gewählte Modell einmal mit den Testdaten. Warum
   bewerten Sie nicht beide Modelle mit den Testdaten und nehmen das bessere?

Zur Kontrolle: Der beste Validierungsscore des Random Forests beträgt 0.914.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

parameter_gitter = {
    'max_depth': [2, 4, 6, 8, None],
    'min_samples_leaf': [1, 5, 10]
}

gittersuche = GridSearchCV(RandomForestClassifier(random_state=0), param_grid=parameter_gitter, cv=kfold)
gittersuche.fit(X_train, y_train)
print(gittersuche.best_params_)
print(f'Bester Validierungsscore: {gittersuche.best_score_:.3f}')
```
Ausgabe:
```
{'max_depth': None, 'min_samples_leaf': 1}
Bester Validierungsscore: 0.914
```
1. Das Gitter enthält 5 × 3 = 15 Kombinationen. Bei fünf Folds werden 75
   Random Forests trainiert, jeder mit 100 Bäumen. Dazu kommt ein letzter
   Random Forest, den die Gittersuche mit der besten Kombination auf allen
   Trainingsdaten trainiert.
2. Am besten ist der Random Forest mit unbegrenzter Tiefe und mindestens einem
   Datenpunkt pro Blatt, also mit den voreingestellten Werten. Sein
   Validierungsscore von 0.914 liegt deutlich über dem besten Entscheidungsbaum
   mit 0.876. Wir setzen den Random Forest ein.

```python
accuracy_test = gittersuche.score(X_test, y_test)
print(f'Accuracy Testdaten: {accuracy_test:.3f}')
```
Ausgabe:
```
Accuracy Testdaten: 0.910
```
3. Der Random Forest erreicht auf den Testdaten eine Accuracy von 0.910 und
   bestimmt damit bei gut 9 von 10 Pinguinen das Geschlecht richtig. Würden wir
   beide Modelle mit den Testdaten bewerten und das bessere nehmen, hätten wir
   die Testdaten zur Auswahl benutzt. Dann wäre der Testscore des gewählten
   Modells kein unbefangenes Urteil mehr.
````

## Projekt 10.2: Gütemaße für Pinguine

In diesem Projekt bewerten Sie Modelle mit den Gütemaßen aus Kapitel 10.3. Wie
im Fließtext dienen die Testdaten hier nur dazu, die Gütemaße zu
veranschaulichen. Für eine echte Modellauswahl würden Sie wie in Projekt 10.1
Validierungsdaten verwenden. Verwenden Sie die bereinigten Daten aus Projekt
10.1, Teil 1. Rechnen Sie mit etwa 30 Minuten.

```{admonition} Teil 1: Zügelpinguine erkennen
:class: tip
Zügelpinguine sind im Datensatz die seltenste Art. Ein Modell soll allein aus
den vier Körpermaßen erkennen, ob ein Pinguin ein Zügelpinguin ist. Die Insel
lassen wir weg, denn Zügelpinguine wurden nur auf Dream gefunden.

Kodieren Sie die Zielgröße so, dass ein Zügelpinguin die 1 ist und jede andere
Art die 0. Legen Sie 20 % der Daten als Testdaten zur Seite, mit
`random_state=0` und gleichem Anteil an Zügelpinguinen in beiden Teilen.
Wählen Sie für Daten und Zielgröße andere Namen als in Projekt 10.1.

1. Welche Accuracy erreicht ein Referenzmodell, das nie "Zügelpinguin" sagt?
2. Trainieren Sie einen Entscheidungsbaum der Tiefe 1 mit `random_state=0`.
   Berechnen Sie die Accuracy und die Konfusionsmatrix auf den Testdaten. Wie
   viele Zügelpinguine erkennt der Baum?
3. Trainieren Sie denselben Baum noch einmal, aber so, dass die seltenere Klasse
   beim Training stärker zählt. Berechnen Sie Accuracy, Konfusionsmatrix,
   Precision und Recall. Was hat sich verändert?

Zur Kontrolle: In den Testdaten sind 14 Zügelpinguine.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
```python
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

# Daten ins richtige Format bringen
zuegel_kodierung = {
    'Adeliepinguin': '0',
    'Eselspinguin': '0',
    'Zügelpinguin': '1',
}
y_zuegel = pinguine['Art'].replace(zuegel_kodierung).astype('int')
X_zuegel = pinguine[['Schnabellaenge (mm)', 'Schnabeltiefe (mm)', 'Flossenlaenge (mm)', 'Koerpergewicht (g)']]

X_zuegel_train, X_zuegel_test, y_zuegel_train, y_zuegel_test = train_test_split(
    X_zuegel, y_zuegel, test_size=0.2, random_state=0, stratify=y_zuegel)
print(y_zuegel_test.value_counts())
```
Ausgabe:
```
Art
0    53
1    14
Name: count, dtype: int64
```
1. In den Testdaten sind 53 andere Pinguine und 14 Zügelpinguine. Das
   Referenzmodell erreicht eine Accuracy von 53 / 67 = 0.79.

```python
baum_zuegel = DecisionTreeClassifier(max_depth=1, random_state=0)
baum_zuegel.fit(X_zuegel_train, y_zuegel_train)
accuracy_test = baum_zuegel.score(X_zuegel_test, y_zuegel_test)
print(f'Accuracy Testdaten: {accuracy_test:.2f}')

y_zuegel_prognose = baum_zuegel.predict(X_zuegel_test)
print(confusion_matrix(y_zuegel_test, y_zuegel_prognose))
```
Ausgabe:
```
Accuracy Testdaten: 0.79
[[53  0]
 [14  0]]
```
2. Der Baum erreicht 0.79, genau so viel wie das Referenzmodell. Die
   Konfusionsmatrix zeigt, warum: Die rechte Spalte enthält nur Nullen. Der
   Baum erkennt keinen einzigen Zügelpinguin. Mit einer einzigen Frage lassen
   sich die Zügelpinguine nicht abtrennen. Sie haben zwar lange Schnäbel, die
   Eselspinguine aber auch.

```python
baum_gewichtet = DecisionTreeClassifier(max_depth=1, class_weight='balanced', random_state=0)
baum_gewichtet.fit(X_zuegel_train, y_zuegel_train)
accuracy_test = baum_gewichtet.score(X_zuegel_test, y_zuegel_test)
print(f'Accuracy Testdaten: {accuracy_test:.2f}')

y_zuegel_prognose_gewichtet = baum_gewichtet.predict(X_zuegel_test)
print(confusion_matrix(y_zuegel_test, y_zuegel_prognose_gewichtet))
print(f'Precision: {precision_score(y_zuegel_test, y_zuegel_prognose_gewichtet):.2f}')
print(f'Recall: {recall_score(y_zuegel_test, y_zuegel_prognose_gewichtet):.2f}')
```
Ausgabe:
```
Accuracy Testdaten: 0.55
[[23 30]
 [ 0 14]]
Precision: 0.32
Recall: 1.00
```
3. Der gewichtete Baum erkennt alle 14 Zügelpinguine, der Recall beträgt 1.00.
   Dafür hält er 30 andere Pinguine fälschlich für Zügelpinguine. Von seinen 44
   Meldungen sind nur 14 berechtigt, die Precision beträgt 0.32. Die Accuracy
   sinkt auf 0.55 und liegt damit weit unter dem Referenzmodell. Der Baum fragt
   nur noch, ob der Schnabel länger als 42.35 mm ist. Alle Pinguine mit
   langem Schnabel meldet er als Zügelpinguin, auch die Eselspinguine.
````

```{admonition} Teil 2: Eine zweite Frage
:class: tip
Erlauben Sie dem Baum jetzt eine zweite Frage. Trainieren Sie einen
Entscheidungsbaum der Tiefe 2 ohne Gewichtung, mit `random_state=0`.

1. Berechnen Sie Accuracy, Konfusionsmatrix, Precision, Recall und F1-Score auf
   den Testdaten. Stellen Sie die drei Bäume aus Teil 1 und Teil 2 in einer
   Tabelle gegenüber.
2. Eine Forscherin will Zügelpinguine mit einem Sender ausstatten. Jeder
   Pinguin, den das Modell meldet, wird dafür eingefangen. Welches Gütemaß ist
   für sie besonders wichtig?

Zur Kontrolle: Der Baum der Tiefe 2 erkennt 12 der 14 Zügelpinguine.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
baum_tiefe2 = DecisionTreeClassifier(max_depth=2, random_state=0)
baum_tiefe2.fit(X_zuegel_train, y_zuegel_train)
accuracy_test = baum_tiefe2.score(X_zuegel_test, y_zuegel_test)
print(f'Accuracy Testdaten: {accuracy_test:.2f}')

y_zuegel_prognose_tiefe2 = baum_tiefe2.predict(X_zuegel_test)
print(confusion_matrix(y_zuegel_test, y_zuegel_prognose_tiefe2))
print(f'Precision: {precision_score(y_zuegel_test, y_zuegel_prognose_tiefe2):.2f}')
print(f'Recall: {recall_score(y_zuegel_test, y_zuegel_prognose_tiefe2):.2f}')
print(f'F1-Score: {f1_score(y_zuegel_test, y_zuegel_prognose_tiefe2):.2f}')
```
Ausgabe:
```
Accuracy Testdaten: 0.96
[[52  1]
 [ 2 12]]
Precision: 0.92
Recall: 0.86
F1-Score: 0.89
```
1. Mit der zweiten Frage erkennt der Baum 12 der 14 Zügelpinguine und meldet
   nur einen Pinguin fälschlich. Alle drei Gütemaße liegen jetzt hoch.

   | Modell | Accuracy | Precision | Recall | F1-Score |
   | --- | --- | --- | --- | --- |
   | Tiefe 1 | 0.79 | keine | 0.00 | 0.00 |
   | Tiefe 1, gewichtet | 0.55 | 0.32 | 1.00 | 0.48 |
   | Tiefe 2 | 0.96 | 0.92 | 0.86 | 0.89 |

   Beim ersten Baum lässt sich keine Precision berechnen, weil er nie
   "Zügelpinguin" meldet.
2. Für die Forscherin ist die Precision wichtig. Jeder Fehlalarm bedeutet, dass
   ein Pinguin umsonst eingefangen wird. Der gewichtete Baum der Tiefe 1 wäre
   trotz seines perfekten Recalls ungeeignet, denn mehr als zwei Drittel ihrer
   Fangversuche wären umsonst. Mit dem Baum der Tiefe 2 ist nur einer von 13
   Fangversuchen umsonst.
````

```{admonition} Teil 3: Körpergewicht vorhersagen
:class: tip
Jetzt soll eine lineare Regression das Körpergewicht vorhersagen. Kodieren Sie
die Art und das Geschlecht mit der One-Hot-Kodierung. Legen Sie 20 % der Daten
als Testdaten zur Seite, mit `random_state=0`.

Trainieren Sie zwei Modelle: Modell A verwendet nur die Flossenlänge, Modell B
die drei Maße von Schnabel und Flosse sowie die kodierte Art und das kodierte
Geschlecht.

1. Berechnen Sie für beide Modelle R², MAE und RMSE auf den Testdaten.
   Vergleichen Sie den MAE mit dem mittleren Körpergewicht der Testdaten.
2. Um wie viele Gramm liegt Modell B im Mittel weniger daneben als Modell A?

Zur Kontrolle: Modell A erreicht auf den Testdaten einen R²-Score von 0.79.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Daten ins richtige Format bringen
pinguine_regression = pd.get_dummies(pinguine, columns=['Art', 'Geschlecht'], dtype=int)
X_gewicht = pinguine_regression.drop(columns=['Insel', 'Jahr', 'Koerpergewicht (g)'])
y_gewicht = pinguine_regression['Koerpergewicht (g)']

X_gewicht_train, X_gewicht_test, y_gewicht_train, y_gewicht_test = train_test_split(
    X_gewicht, y_gewicht, test_size=0.2, random_state=0)
print(f'Mittleres Körpergewicht Testdaten: {y_gewicht_test.mean():.0f} g')

# Modell A: nur die Flossenlänge
modell_a = LinearRegression()
modell_a.fit(X_gewicht_train[['Flossenlaenge (mm)']], y_gewicht_train)
y_prognose_a = modell_a.predict(X_gewicht_test[['Flossenlaenge (mm)']])
r2_test_a = modell_a.score(X_gewicht_test[['Flossenlaenge (mm)']], y_gewicht_test)
mae_test_a = mean_absolute_error(y_gewicht_test, y_prognose_a)
rmse_test_a = np.sqrt(mean_squared_error(y_gewicht_test, y_prognose_a))
print(f'Modell A: R² {r2_test_a:.2f}, MAE {mae_test_a:.0f} g, RMSE {rmse_test_a:.0f} g')

# Modell B: alle Merkmale
modell_b = LinearRegression()
modell_b.fit(X_gewicht_train, y_gewicht_train)
y_prognose_b = modell_b.predict(X_gewicht_test)
r2_test_b = modell_b.score(X_gewicht_test, y_gewicht_test)
mae_test_b = mean_absolute_error(y_gewicht_test, y_prognose_b)
rmse_test_b = np.sqrt(mean_squared_error(y_gewicht_test, y_prognose_b))
print(f'Modell B: R² {r2_test_b:.2f}, MAE {mae_test_b:.0f} g, RMSE {rmse_test_b:.0f} g')
```
Ausgabe:
```
Mittleres Körpergewicht Testdaten: 4030 g
Modell A: R² 0.79, MAE 301 g, RMSE 378 g
Modell B: R² 0.89, MAE 221 g, RMSE 275 g
```
1. Modell A erreicht ein R² von 0.79 und liegt im Mittel 301 g daneben. Das
   sind gut 7 % des mittleren Körpergewichts von 4030 g. Modell B erreicht ein
   R² von 0.89 und liegt im Mittel 221 g daneben, also gut 5 %. Bei beiden
   Modellen liegt der RMSE etwa ein Viertel über dem MAE. Das deutet darauf
   hin, dass die Fehler ähnlich groß sind und es kaum grobe Fehlprognosen gibt.
2. Modell B liegt im Mittel 80 g weniger daneben als Modell A. Am MAE sehen wir
   die Verbesserung direkt in Gramm. Das R² zeigt zwar ebenfalls, dass Modell B
   besser ist, aber nicht, um wie viel Gramm.
````
