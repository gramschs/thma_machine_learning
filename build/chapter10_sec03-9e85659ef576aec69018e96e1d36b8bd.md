---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: 3ddruck_kodierung.csv
    title: 3ddruck_kodierung.csv
  - file: 3ddruck_gittersuche.csv
    title: 3ddruck_gittersuche.csv
  - file: autoscout24_kodierung.csv
    title: autoscout24_kodierung.csv
  - file: chapter10_sec03.md
    title: chapter10_sec03.md
---

# 10.3 Gütemaße für Klassifikation und Regression

Bei 2 % Ausschuss erreicht eine Prüfung, die jedes Bauteil durchwinkt, bereits
eine Accuracy von 98 %. Trotzdem findet sie kein einziges fehlerhaftes Bauteil.
Bisher haben wir unsere Modelle nur mit dem Standard-Score von Scikit-Learn
bewertet, also mit der Accuracy bei Klassifikation und dem R²-Score bei
Regression. In diesem Kapitel lernen wir Gütemaße kennen, die zeigen, welche
Fehler ein Modell macht und wie groß sie sind.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können eine **Konfusionsmatrix** erstellen und ablesen und mit einem
  **Referenzmodell** begründen, warum die Accuracy bei **unausgewogenen
  Klassen** täuschen kann.
* [ ] Sie können **Precision**, **Recall** und **F1-Score** berechnen und
  begründen, welches Gütemaß für eine Anwendung wichtig ist.
* [ ] Sie können die Gütemaße **MAE**, **MSE** und **RMSE** für
  Regressionsmodelle berechnen und MAE und RMSE in der Einheit der Zielgröße
  deuten.
```

## Konfusionsmatrix und Accuracy

In der Qualitätskontrolle wollen wir Fehldrucke erkennen, bevor ein Druck
startet. Dazu verwenden wir den Datensatz `3ddruck_kodierung.csv`. Diesmal
kodieren wir einen Fehldruck, also ein "nein" in der Spalte `Erfolgreich`, mit
der 1, denn ihn wollen wir finden. Da Fehldrucke selten sind, teilen wir die
Daten mit `stratify` auf.

```{code-cell} python
import pandas as pd
from sklearn.model_selection import train_test_split

# Daten ins richtige Format bringen
daten = pd.read_csv('3ddruck_kodierung.csv', index_col=0)
fehldruck_kodierung = {
    'ja': '0',    # erfolgreich, also kein Fehldruck
    'nein': '1',  # nicht erfolgreich, also Fehldruck
}
daten['Fehldruck'] = daten['Erfolgreich'].replace(fehldruck_kodierung)
daten['Fehldruck'] = daten['Fehldruck'].astype('int')

X = daten[['Drucktemperatur (C)', 'Betttemperatur (C)', 'Druckgeschwindigkeit (mm/s)']]
y = daten['Fehldruck']

# Aufteilung mit gleichem Anteil an Fehldrucken
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, stratify=y)
```

Wir trainieren einen Entscheidungsbaum der Tiefe 2 und bewerten ihn mit den
Testdaten.

```{code-cell} python
from sklearn.tree import DecisionTreeClassifier

modell = DecisionTreeClassifier(max_depth=2, random_state=0)
modell.fit(X_train, y_train)
accuracy_test = modell.score(X_test, y_test)
print(f'Accuracy Testdaten: {accuracy_test:.2f}')
```

Der Baum ordnet 86 % der Testdrucke richtig ein. Das klingt ordentlich. Bevor
wir uns darüber freuen, zählen wir, wie oft jede Klasse in den Testdaten
vorkommt.

<!-- Code-Along-Lücke: `y_test.value_counts()` ersetzen durch
`# TODO: ???  (zählen, wie oft jede Klasse in den Testdaten vorkommt)` -->

```{code-cell} python
y_test.value_counts()
```

Unter den 50 Testdrucken sind nur 7 Fehldrucke. Eine Prüfregel, die immer "kein
Fehldruck" sagt, liegt also bei 43 von 50 Drucken richtig. Ihre Accuracy
beträgt ebenfalls 0.86. Ein solches einfaches Vergleichsmodell heißt
**Referenzmodell**. Ist ein trainiertes Modell nicht besser als sein
Referenzmodell, ist das ein Warnsignal.

Welche Drucke ordnet der Baum falsch ein? Das zeigt die **Konfusionsmatrix**
(englisch Confusion Matrix). Sie zählt für jede Kombination aus tatsächlicher
und prognostizierter Klasse, wie viele Datenpunkte dort landen. Scikit-Learn
berechnet sie mit der Funktion `confusion_matrix()` aus dem Modul
`sklearn.metrics`. Als erstes Argument übergeben wir die tatsächlichen Klassen,
als zweites die Prognosen.

<!-- Code-Along-Lücke: `konfusionsmatrix = confusion_matrix(y_test, y_prognose)`
ersetzen durch `konfusionsmatrix = # TODO: ???  (Konfusionsmatrix berechnen,
zuerst die tatsächlichen Klassen, dann die Prognosen)`. Die Reihenfolge der
Argumente ist der Stolperstein, vertauscht kippt die Matrix. -->

```{code-cell} python
from sklearn.metrics import confusion_matrix

y_prognose = modell.predict(X_test)
konfusionsmatrix = confusion_matrix(y_test, y_prognose)
print(konfusionsmatrix)
```

Die Zeilen gehören zu den tatsächlichen Klassen, die Spalten zu den Prognosen,
jeweils zuerst die 0 und dann die 1. Die Klasse, die wir finden wollen, heißt
**positive Klasse**. Bei uns ist das der Fehldruck. Positiv bedeutet hier also
nicht "gut", sondern "die Prüfung schlägt Alarm". Damit bekommt jedes Feld der
Konfusionsmatrix einen Namen.

|                           | Prognose gut (0)     | Prognose Fehldruck (1) |
|---------------------------|----------------------|------------------------|
| tatsächlich gut (0)       | richtig negativ (TN) | falsch positiv (FP)    |
| tatsächlich Fehldruck (1) | falsch negativ (FN)  | richtig positiv (TP)   |

Die Abkürzungen stehen für True Negative, False Positive, False Negative und
True Positive. Auf der Diagonalen stehen die richtigen Prognosen, also **richtig
negativ** und **richtig positiv**. **Falsch positiv** ist ein Fehlalarm: Ein
guter Druck wird unnötig nachgeprüft. **Falsch negativ** ist meist schlimmer:
Der Fehldruck rutscht durch und landet im schlimmsten Fall beim Kunden.

Unsere Matrix zeigt 43 richtig negative und 7 falsch negative Drucke. In der
rechten Spalte stehen nur Nullen. Der Baum meldet also keinen einzigen
Fehldruck. Für die Qualitätskontrolle ist er wertlos.

Auch die Accuracy lesen wir aus der Konfusionsmatrix ab. Sie ist der Anteil der
richtigen Prognosen auf der Diagonalen:

$$
\text{Accuracy} =
\frac{\text{TN} + \text{TP}}{\text{TN} + \text{FP} + \text{FN} + \text{TP}}
$$

Die Accuracy zählt jede richtige Prognose gleich. Deshalb bestimmen die vielen
guten Drucke ihren Wert, und die 7 übersehenen Fehldrucke fallen kaum ins
Gewicht. Kommt eine Klasse viel seltener vor als die andere, sprechen wir von
**unausgewogenen Klassen**. Je unausgewogener die Klassen, desto stärker
täuscht die Accuracy. Deshalb vergleichen wir sie immer mit dem Referenzmodell
und schauen zusätzlich in die Konfusionsmatrix.

```{admonition} Mini-Übung
:class: tip
Übertragen Sie das Vorgehen auf den Datensatz `3ddruck_gittersuche.csv` mit 300
Druckaufträgen. Wählen Sie andere Variablennamen als im Fließtext, damit Sie die
Beispieldaten nicht überschreiben.

1. Kodieren Sie die Zielgröße `Erfolgreich` so, dass ein Fehldruck die 1 ist.
   Eingabedaten sind `Drucktemperatur (C)`, `Betttemperatur (C)` und
   `Druckgeschwindigkeit (mm/s)`.
2. Teilen Sie die Daten so auf, dass der Anteil der Fehldrucke in Trainings- und
   Testdaten gleich ist. Trainieren Sie einen Entscheidungsbaum der Tiefe 2.
   Verwenden Sie für beides `random_state=0`. Vergleichen Sie die Accuracy auf
   den Testdaten mit der des Referenzmodells.
3. Erstellen Sie die Konfusionsmatrix. Wie viele Fehldrucke erkennt der Baum,
   wie viele rutschen durch, und wie viele Fehlalarme gibt es?
4. Warum täuscht die Accuracy hier weniger als im Fließtext?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Daten ins richtige Format bringen
druckversuche = pd.read_csv('3ddruck_gittersuche.csv', index_col=0)
fehldruck_kodierung = {
    'ja': '0',    # erfolgreich, also kein Fehldruck
    'nein': '1',  # nicht erfolgreich, also Fehldruck
}
druckversuche['Fehldruck'] = druckversuche['Erfolgreich'].replace(fehldruck_kodierung)
druckversuche['Fehldruck'] = druckversuche['Fehldruck'].astype('int')

X_druck = druckversuche[['Drucktemperatur (C)', 'Betttemperatur (C)', 'Druckgeschwindigkeit (mm/s)']]
y_druck = druckversuche['Fehldruck']
```

```python
X_druck_train, X_druck_test, y_druck_train, y_druck_test = train_test_split(
    X_druck, y_druck, random_state=0, stratify=y_druck
)

modell_druck = DecisionTreeClassifier(max_depth=2, random_state=0)
modell_druck.fit(X_druck_train, y_druck_train)
accuracy_test_druck = modell_druck.score(X_druck_test, y_druck_test)
print(f'Accuracy Testdaten: {accuracy_test_druck:.2f}')

print(y_druck_test.value_counts())
```

Zu 2. Der Baum erreicht eine Accuracy von 0.79. Die Testdaten enthalten 45 gute
Drucke und 30 Fehldrucke. Das Referenzmodell erreicht also nur 45/75 = 0.60.

```python
from sklearn.metrics import confusion_matrix

y_druck_prognose = modell_druck.predict(X_druck_test)
konfusionsmatrix_druck = confusion_matrix(y_druck_test, y_druck_prognose)
print(konfusionsmatrix_druck)
```

Zu 3. Die Konfusionsmatrix lautet `[[41 4] [12 18]]`. Der Baum erkennt 18 der 30
Fehldrucke, 12 rutschen durch. Dazu kommen 4 Fehlalarme.

Zu 4. Hier sind 40 % der Testdrucke Fehldrucke, im Fließtext nur 14 %. Die
Klassen sind also viel ausgewogener, und das Referenzmodell erreicht nur 0.60.
Eine hohe Accuracy gelingt nur, wenn das Modell auch Fehldrucke erkennt.
````

## Precision, Recall und F1-Score

In der Qualitätskontrolle interessieren uns zwei Fragen. Welchen Anteil der
Fehldrucke finden wir? Und wie viele unserer Alarme sind berechtigt? Dafür
brauchen wir zuerst ein Modell, das überhaupt Fehldrucke meldet.

Unser Baum hat zwar ein Blatt für Fehldrucke, doch kein Testdruck landet darin.
In den übrigen Blättern sind die guten Drucke in der Mehrheit. In einem Blatt
liegen zum Beispiel 11 Fehldrucke und 38 gute Drucke, also lautet die Prognose
dort "gut". Mit dem Hyperparameter `class_weight='balanced'` zählt beim Training
jeder Druck umso stärker, je seltener seine Klasse ist. Unsere Trainingsdaten
enthalten fast sechsmal so viele gute Drucke wie Fehldrucke. Ein Fehldruck wiegt
dann also etwa sechsmal so viel wie ein guter Druck, und mehr Blätter melden
Fehldrucke.

```{code-cell} python
modell_gewichtet = DecisionTreeClassifier(max_depth=2, class_weight='balanced', random_state=0)
modell_gewichtet.fit(X_train, y_train)
accuracy_test_gewichtet = modell_gewichtet.score(X_test, y_test)
print(f'Accuracy Testdaten: {accuracy_test_gewichtet:.2f}')

y_prognose_gewichtet = modell_gewichtet.predict(X_test)
print(confusion_matrix(y_test, y_prognose_gewichtet))
```

Die Accuracy sinkt von 0.86 auf 0.80 und liegt jetzt sogar unter dem
Referenzmodell. Dafür erkennt der gewichtete Baum 4 der 7 Fehldrucke, bei 7
Fehlalarmen. Ist er besser oder schlechter als der erste Baum? Die Accuracy kann
das nicht beantworten.

Die erste Frage beantwortet der **Recall** (deutsch Trefferquote). Er gibt an,
welchen Anteil der tatsächlichen Fehldrucke das Modell findet:

$$
\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}
$$

Der gewichtete Baum findet 4 von 7 Fehldrucken, sein Recall ist also 4/7 = 0.57.
Die zweite Frage beantwortet die **Precision** (deutsch Präzision). Sie gibt an,
welcher Anteil der Alarme berechtigt ist:

$$
\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}
$$

Von 11 Alarmen sind 4 berechtigt, die Precision ist also 4/11 = 0.36. Wir
bleiben bei den englischen Begriffen, denn das deutsche Wort "Genauigkeit" steht
mal für die Accuracy und mal für die Precision.

Der **F1-Score** fasst Precision und Recall in einer Zahl zusammen. Er ist ihr
harmonisches Mittel:

$$
\text{F1} =
\frac{2 \cdot \text{Precision} \cdot \text{Recall}}
{\text{Precision} + \text{Recall}}
$$

Anders als der gewöhnliche Mittelwert wird der F1-Score klein, sobald einer der
beiden Werte klein ist. Scikit-Learn berechnet die drei Gütemaße mit den
Funktionen `precision_score()`, `recall_score()` und `f1_score()` aus dem Modul
`sklearn.metrics`. Die Argumente übergeben wir wie bei der Konfusionsmatrix. Als
positive Klasse verwendet Scikit-Learn die 1. Deshalb haben wir den Fehldruck
mit 1 kodiert.

<!-- Code-Along-Lücke: `recall_test = recall_score(y_test, y_prognose_gewichtet)`
ersetzen durch `recall_test = # TODO: ???  (Recall des gewichteten Baums
berechnen)`. -->

```{code-cell} python
from sklearn.metrics import precision_score, recall_score, f1_score

precision_test = precision_score(y_test, y_prognose_gewichtet)
recall_test = recall_score(y_test, y_prognose_gewichtet)
f1_test = f1_score(y_test, y_prognose_gewichtet)
print(f'Precision: {precision_test:.2f}')
print(f'Recall: {recall_test:.2f}')
print(f'F1-Score: {f1_test:.2f}')
```

Der gewichtete Baum erreicht einen F1-Score von 0.44. Der erste Baum findet
keinen Fehldruck. Sein Recall ist 0, und damit ist auch sein F1-Score 0. Nach
der Accuracy liegt also der erste Baum vorn, nach dem F1-Score der gewichtete.

Welches Gütemaß wichtiger ist, hängt davon ab, welcher Fehler teurer ist.
Meldet ein Modell mehr Alarme, steigt meist der Recall, und die Precision sinkt.
Darf bei einem Sicherheitsbauteil kein Fehldruck durchrutschen, achten wir auf
den Recall. Löst jeder Alarm eine teure Nachprüfung aus, achten wir auf die
Precision. Sollen beide hoch sein, wählen wir den F1-Score.

Streng genommen dürfen wir ein Modell nicht anhand der Testdaten auswählen. Hier
dienen sie nur zur Veranschaulichung. Für eine echte Auswahl verwenden wir wie
in Kapitel 10.2 die Kreuzvalidierung auf den Trainingsdaten. Mit dem Argument
`scoring='recall'` bewertet `cross_validate()` die Modelle mit dem Recall statt
mit der Accuracy. Das funktioniert ebenso mit `scoring='precision'` oder
`scoring='f1'` und auch bei `GridSearchCV`.

```{admonition} Mini-Übung
:class: tip
Setzen Sie die vorherige Mini-Übung fort.

1. Berechnen Sie Precision, Recall und F1-Score für den Entscheidungsbaum aus
   der vorherigen Mini-Übung. Prüfen Sie Precision und Recall von Hand mit der
   Konfusionsmatrix.
2. Trainieren Sie einen zweiten Entscheidungsbaum der Tiefe 2, bei dem die
   seltenere Klasse beim Training stärker zählt. Berechnen Sie für ihn die
   Konfusionsmatrix sowie Precision, Recall und F1-Score. Was hat sich
   verändert?
3. Welchen der beiden Bäume setzen Sie in den folgenden Fällen ein? Begründen
   Sie Ihre Wahl jeweils mit einem Gütemaß.
   * Die Bauteile sind sicherheitsrelevant. Möglichst kein Fehldruck darf
     durchrutschen.
   * Jeder Alarm hält den Druckauftrag an, bis jemand die Einstellungen von Hand
     geprüft hat.
4. Prüfen Sie Ihre Wahl ohne Testdaten. Vergleichen Sie beide Bäume mit einer
   Kreuzvalidierung auf den Trainingsdaten, einmal mit dem Recall und einmal
   mit der Precision als Gütemaß. Verwenden Sie wie in Kapitel 10.2
   `StratifiedKFold` mit 5 Folds, `shuffle=True` und `random_state=0`.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
from sklearn.metrics import precision_score, recall_score, f1_score

precision_test_druck = precision_score(y_druck_test, y_druck_prognose)
recall_test_druck = recall_score(y_druck_test, y_druck_prognose)
f1_test_druck = f1_score(y_druck_test, y_druck_prognose)
print(f'Precision: {precision_test_druck:.2f}')
print(f'Recall: {recall_test_druck:.2f}')
print(f'F1-Score: {f1_test_druck:.2f}')
```

Zu 1. Die Precision beträgt 0.82, der Recall 0.60 und der F1-Score 0.69. Von
Hand: Der Baum meldet 18 + 4 = 22 Alarme, davon sind 18 berechtigt. Das ergibt
eine Precision von 18/22 = 0.82. Von den 18 + 12 = 30 Fehldrucken findet er 18.
Das ergibt einen Recall von 18/30 = 0.60.

```python
modell_druck_gewichtet = DecisionTreeClassifier(max_depth=2, class_weight='balanced', random_state=0)
modell_druck_gewichtet.fit(X_druck_train, y_druck_train)
y_druck_prognose_gewichtet = modell_druck_gewichtet.predict(X_druck_test)
print(confusion_matrix(y_druck_test, y_druck_prognose_gewichtet))

precision_test_druck_gewichtet = precision_score(y_druck_test, y_druck_prognose_gewichtet)
recall_test_druck_gewichtet = recall_score(y_druck_test, y_druck_prognose_gewichtet)
f1_test_druck_gewichtet = f1_score(y_druck_test, y_druck_prognose_gewichtet)
print(f'Precision: {precision_test_druck_gewichtet:.2f}')
print(f'Recall: {recall_test_druck_gewichtet:.2f}')
print(f'F1-Score: {f1_test_druck_gewichtet:.2f}')
```

Zu 2. Die Konfusionsmatrix des gewichteten Baums lautet `[[23 22] [6 24]]`. Er
findet 24 der 30 Fehldrucke, nur noch 6 statt 12 rutschen durch. Dafür steigt
die Zahl der Fehlalarme von 4 auf 22. Der Recall steigt von 0.60 auf 0.80, die
Precision sinkt von 0.82 auf 0.52. Der F1-Score sinkt leicht von 0.69 auf 0.63.

Zu 3. Bei sicherheitsrelevanten Bauteilen zählt der Recall. Wir wählen den
gewichteten Baum, der 80 % der Fehldrucke findet, und nehmen die Fehlalarme in
Kauf. Ob 6 übersehene Fehldrucke akzeptabel sind, ist allerdings fraglich.
Vermutlich brauchen wir ein besseres Modell oder eine zusätzliche Prüfung. Hält
jeder Alarm den Druckauftrag an, zählt die Precision. Wir wählen den ersten
Baum, denn 82 % seiner Alarme sind berechtigt.

```python
from sklearn.model_selection import cross_validate, StratifiedKFold

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
for guetemass in ['recall', 'precision']:
    cv_erster_baum = cross_validate(modell_druck, X_druck_train, y_druck_train, cv=kfold, scoring=guetemass)
    cv_gewichtet = cross_validate(modell_druck_gewichtet, X_druck_train, y_druck_train, cv=kfold, scoring=guetemass)
    mittel_erster_baum = cv_erster_baum['test_score'].mean()
    mittel_gewichtet = cv_gewichtet['test_score'].mean()
    print(f'{guetemass}: erster Baum {mittel_erster_baum:.2f}, gewichteter Baum {mittel_gewichtet:.2f}')
```

Zu 4. Die Kreuzvalidierung bestätigt die Wahl. Der gewichtete Baum erreicht im
Mittel einen Recall von 0.76, der erste Baum nur 0.36. Bei der Precision liegt
der erste Baum mit 0.63 vor dem gewichteten mit 0.52.
````

## Gütemaße für Regression

Bei Regressionsmodellen berechnet `.score()` das Bestimmtheitsmaß R². Es
vergleicht die Prognosen mit einem Referenzmodell, das immer den Mittelwert
vorhersagt. Wie weit eine Prognose danebenliegt, verrät das R² nicht. Als
Beispiel sagen wir den Preis eines Gebrauchtwagens aus dem
Autoscout24-Datensatz mit einer linearen Regression vorher. Als Merkmale
verwenden wir Kilometerstand, Leistung und Jahr der Erstzulassung.

```{code-cell} python
from sklearn.linear_model import LinearRegression

# Daten ins richtige Format bringen
daten = pd.read_csv('autoscout24_kodierung.csv')
X = daten[['Kilometerstand (km)', 'Leistung (kW)', 'Jahr']]
y = daten['Preis (Euro)']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

modell = LinearRegression()
modell.fit(X_train, y_train)
r2_test = modell.score(X_test, y_test)
print(f'R² Testdaten: {r2_test:.2f}')
```

Das R² von 0.66 sagt uns, dass das Modell deutlich besser ist als der
Mittelwert. Ein Händler möchte aber wissen, um wie viele Euro die Prognose
danebenliegen kann. Dazu betrachten wir die Residuen, also die Differenzen
zwischen tatsächlichem und prognostiziertem Preis. Den Mittelwert ihrer Beträge
nennen wir **mittleren absoluten Fehler** (englisch Mean Absolute Error,
**MAE**):

$$
\text{MAE} = \frac{1}{M} \sum_{i=1}^{M} \left| y^{(i)} - \hat{y}^{(i)} \right|
$$

Scikit-Learn berechnet ihn mit der Funktion `mean_absolute_error()` aus dem
Modul `sklearn.metrics`. Wie bei der Konfusionsmatrix übergeben wir zuerst die
tatsächlichen Werte und dann die Prognosen.

<!-- Code-Along-Lücke: `mae_test = mean_absolute_error(y_test, y_prognose)`
ersetzen durch `mae_test = # TODO: ???  (mittleren absoluten Fehler auf den
Testdaten berechnen)`. -->

```{code-cell} python
from sklearn.metrics import mean_absolute_error

y_prognose = modell.predict(X_test)
mae_test = mean_absolute_error(y_test, y_prognose)
print(f'MAE Testdaten: {mae_test:.0f} Euro')
print(f'Mittlerer Preis Testdaten: {y_test.mean():.0f} Euro')
```

Im Mittel liegt das Modell rund 6100 Euro daneben, bei einem mittleren Preis von
rund 21500 Euro. Diese Aussage verstehen auch Personen ohne ML-Kenntnisse.

Die lineare Regression minimiert allerdings nicht den MAE, sondern die
Fehlerquadratsumme. Teilen wir sie durch die Anzahl der Datenpunkte, erhalten
wir den **mittleren quadratischen Fehler** (englisch Mean Squared Error,
**MSE**). Seine Einheit Euro² ist schwer zu deuten. Deshalb ziehen wir die
Wurzel und erhalten die **Wurzel des mittleren quadratischen Fehlers**
(englisch Root Mean Squared Error, **RMSE**), wieder in Euro:

$$
\text{RMSE} = \sqrt{\text{MSE}} =
\sqrt{\frac{1}{M} \sum_{i=1}^{M} \left( y^{(i)} - \hat{y}^{(i)} \right)^2}
$$

Den MSE berechnet die Funktion `mean_squared_error()`, die Wurzel ziehen wir
mit `np.sqrt()`. Zum Vergleich geben wir auch das betragsmäßig größte Residuum
aus.

```{code-cell} python
import numpy as np
from sklearn.metrics import mean_squared_error

mse_test = mean_squared_error(y_test, y_prognose)
rmse_test = np.sqrt(mse_test)
residuen = y_test - y_prognose
print(f'MSE Testdaten: {mse_test:.0f} Euro²')
print(f'RMSE Testdaten: {rmse_test:.0f} Euro')
print(f'Größtes Residuum (Betrag): {residuen.abs().max():.0f} Euro')
```

Der RMSE ist mit rund 9700 Euro deutlich größer als der MAE. Durch das
Quadrieren zählen große Fehler besonders stark. Deshalb ist der RMSE nie kleiner
als der MAE, und ein großer Abstand deutet auf einzelne grobe Fehlprognosen hin.
Das größte Residuum bestätigt das: Bei einem Auto liegt das Modell rund 56800
Euro daneben, mehr als das Neunfache des MAE.

Das R² eignet sich zum Einordnen und Vergleichen von Modellen, der MAE zum
Erklären der Prognosegüte. Der RMSE ist wichtig, wenn große Abweichungen
besonders teuer sind, etwa wenn ein Bauteil eine Toleranz einhalten muss. Auch
in Kreuzvalidierung und Gittersuche können wir einen Fehler verwenden, zum
Beispiel mit `scoring='neg_mean_absolute_error'`. Scikit-Learn sucht dort immer
den größten Wert. Ein Fehler soll aber klein sein, deshalb steht er mit
negativem Vorzeichen.

```{admonition} Mini-Übung
:class: tip
Jetzt soll ein Modell die Zugfestigkeit der Bauteile aus
`3ddruck_gittersuche.csv` vorhersagen.

1. Verwenden Sie als Eingabedaten die Merkmale `Schichthoehe (mm)`,
   `Infill (%)`, `Wandstaerke (mm)`, `Drucktemperatur (C)`,
   `Betttemperatur (C)` und `Druckgeschwindigkeit (mm/s)`. Die Zielgröße ist
   `Zugfestigkeit (MPa)`. Teilen Sie die Daten mit `random_state=0` in
   Trainings- und Testdaten auf und trainieren Sie eine lineare Regression.
2. Berechnen Sie R², MAE, RMSE und das betragsmäßig größte Residuum auf den
   Testdaten.
3. Deuten Sie MAE und RMSE in MPa, auch im Vergleich zur mittleren
   Zugfestigkeit der Testdaten. Gibt es grobe Fehlprognosen wie beim
   Autopreis?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Daten ins richtige Format bringen
druckversuche = pd.read_csv('3ddruck_gittersuche.csv', index_col=0)
X_zug = druckversuche[['Schichthoehe (mm)', 'Infill (%)', 'Wandstaerke (mm)',
                       'Drucktemperatur (C)', 'Betttemperatur (C)', 'Druckgeschwindigkeit (mm/s)']]
y_zug = druckversuche['Zugfestigkeit (MPa)']
X_zug_train, X_zug_test, y_zug_train, y_zug_test = train_test_split(X_zug, y_zug, random_state=0)

modell_zug = LinearRegression()
modell_zug.fit(X_zug_train, y_zug_train)
r2_test_zug = modell_zug.score(X_zug_test, y_zug_test)

y_zug_prognose = modell_zug.predict(X_zug_test)
mae_test_zug = mean_absolute_error(y_zug_test, y_zug_prognose)
rmse_test_zug = np.sqrt(mean_squared_error(y_zug_test, y_zug_prognose))
residuen_zug = y_zug_test - y_zug_prognose

print(f'R² Testdaten: {r2_test_zug:.2f}')
print(f'MAE Testdaten: {mae_test_zug:.1f} MPa')
print(f'RMSE Testdaten: {rmse_test_zug:.1f} MPa')
print(f'Größtes Residuum (Betrag): {residuen_zug.abs().max():.1f} MPa')
print(f'Mittlere Zugfestigkeit Testdaten: {y_zug_test.mean():.1f} MPa')
```

Zu 2. Das R² beträgt 0.82, der MAE 3.0 MPa, der RMSE 3.9 MPa und das größte
Residuum 9.7 MPa.

Zu 3. Im Mittel liegt die Prognose der Zugfestigkeit 3.0 MPa daneben. Bei einer
mittleren Zugfestigkeit von 32.0 MPa sind das knapp 10 %. Der RMSE liegt nur
wenig über dem MAE, und der größte Fehler ist gut dreimal so groß wie der MAE.
Grobe Ausreißer wie beim Autopreis, wo der größte Fehler mehr als das Neunfache
des MAE beträgt, gibt es hier nicht.
````

## Zusammenfassung und Ausblick

Eine hohe Accuracy kann täuschen. Bei unausgewogenen Klassen erreicht schon ein
Referenzmodell, das immer die häufige Klasse vorhersagt, eine hohe Accuracy. Die
Konfusionsmatrix zeigt, welche Fehler ein Modell tatsächlich macht. Recall und
Precision beantworten zwei verschiedene Fragen: Wie viele Fehldrucke finden wir,
und wie viele Alarme sind berechtigt? Welches Gütemaß wichtiger ist, hängt davon
ab, welcher Fehler teurer ist. Bei Regression ergänzen MAE und RMSE das R² um
die Größe der Fehler in der Einheit der Zielgröße.

Im nächsten Kapitel lernen wir mit den neuronalen Netzen eine neue Art von
Modellen kennen. Die Gütemaße aus diesem Kapitel gelten für jedes Modell, also
auch für neuronale Netze.
