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
  - file: chapter10_sec03.md
    title: chapter10_sec03.md
---

# 10.3 Gütemaße für Klassifikation und Regression

```{admonition} Warnung
:class: warning
Dieses Kapitel befindet sich derzeit im Umbau und wird rechtzeitig vor der
Vorlesung im WiSe 2026/27 zur Verfügung stehen.
```

Geplante Einleitung:

* Anknüpfung an den Ausblick von 10.2: Bei 2 % Ausschuss erreicht ein Modell,
  das immer "in Ordnung" vorhersagt, bereits 98 %.
* Bisher haben wir Modelle nur mit dem Standard-Score von Scikit-Learn bewertet:
  bei Klassifikation mit der Accuracy, bei Regression mit dem
  Bestimmtheitsmaß R².
* In diesem Kapitel lernen wir Gütemaße kennen, die zeigen, welche Fehler ein
  Modell macht und wie groß diese Fehler sind.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können eine **Konfusionsmatrix** erstellen und ablesen und mit einem
  **Referenzmodell** begründen, warum die Accuracy bei **unausgewogenen
  Klassen** täuschen kann.
```

Entwurf für die Lernziele der weiteren Abschnitte:

* Sie können Precision, Recall und F1-Score berechnen und begründen, welches
  Gütemaß für eine Anwendung wichtig ist.
* Sie können die Gütemaße MAE, MSE und RMSE für Regressionsmodelle berechnen
  und in der Einheit der Zielgröße deuten.

## Konfusionsmatrix und Accuracy

In der Qualitätskontrolle wollen wir Fehldrucke erkennen, bevor ein Druck
startet. Dazu verwenden wir den Datensatz `3ddruck_kodierung.csv` aus Kapitel
8.2. Die Zielgröße `Erfolgreich` kodieren wir diesmal andersherum: Ein
Fehldruck, also ein "nein", bekommt die 1, denn ihn wollen wir finden. Da
Fehldrucke selten sind, teilen wir mit `stratify` aus Kapitel 8.3 auf. So ist
ihr Anteil in Trainings- und Testdaten gleich groß.

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

Wie in Kapitel 10.2 trainieren wir einen Entscheidungsbaum der Tiefe 3 und
bewerten ihn mit den Testdaten.

```{code-cell} python
from sklearn.tree import DecisionTreeClassifier

modell = DecisionTreeClassifier(max_depth=3, random_state=0)
modell.fit(X_train, y_train)
accuracy_test = modell.score(X_test, y_test)
print(f'Accuracy Testdaten: {accuracy_test:.2f}')
```

Bei Klassifikationsmodellen berechnet `.score()` die Accuracy, die wir aus
Kapitel 6.1 kennen. Der Baum ordnet also 86 % der Testdrucke richtig ein. Das
klingt zunächst ordentlich. Bevor wir uns darüber freuen, zählen wir, wie oft
jede Klasse in den Testdaten vorkommt.

<!-- Code-Along-Lücke: `y_test.value_counts()` ersetzen durch
`# TODO: ???  (zählen, wie oft jede Klasse in den Testdaten vorkommt)` -->

```{code-cell} python
y_test.value_counts()
```

Unter den 50 Testdrucken sind 43 erfolgreiche Drucke und nur 7 Fehldrucke.
Stellen wir uns eine Prüfregel vor, die gar nicht auf die Daten schaut und immer
"kein Fehldruck" sagt. Diese Regel liegt bei 43 von 50 Drucken richtig. Das
ergibt eine Accuracy von 43/50 = 0.86, genau so viel wie unser
Entscheidungsbaum. Ein solches einfaches Vergleichsmodell heißt
**Referenzmodell**. Ein trainiertes Modell muss sein Referenzmodell deutlich
übertreffen, sonst bringt es keinen Nutzen.

Die Accuracy verrät uns aber nicht, welche Drucke der Baum falsch einordnet. Hat
er einige Fehldrucke erkannt und dafür gute Drucke aussortiert? Oder hat er gar
keinen Fehldruck erkannt?

Die Antwort liefert die **Konfusionsmatrix** (englisch Confusion Matrix). Sie
zählt für jede Kombination aus tatsächlicher und prognostizierter Klasse, wie
viele Datenpunkte dort landen. Damit zeigt sie, welche Klassen das Modell
miteinander verwechselt. Scikit-Learn berechnet die Konfusionsmatrix mit der
Funktion `confusion_matrix()` aus dem Modul `sklearn.metrics`. Als erstes
Argument übergeben wir die tatsächlichen Klassen, als zweites die Prognosen des
Modells.

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

Um die vier Zahlen zu lesen, brauchen wir die Reihenfolge. Scikit-Learn schreibt
die tatsächlichen Klassen in die Zeilen und die prognostizierten Klassen in die
Spalten, jeweils zuerst die 0 und dann die 1. Die Klasse, die wir finden wollen,
heißt **positive Klasse**. Bei uns ist das der Fehldruck mit der 1. Positiv
bedeutet hier also nicht "gut", sondern "die Prüfung schlägt Alarm". Damit
bekommt jedes Feld der Konfusionsmatrix einen eigenen Namen.

|                           | Prognose gut (0)     | Prognose Fehldruck (1) |
|---------------------------|----------------------|------------------------|
| tatsächlich gut (0)       | richtig negativ (TN) | falsch positiv (FP)    |
| tatsächlich Fehldruck (1) | falsch negativ (FN)  | richtig positiv (TP)   |

* Ein guter Druck, den der Baum als gut einstuft, ist **richtig negativ**.
* Ein guter Druck, den der Baum als Fehldruck meldet, ist **falsch positiv**.
  Das ist ein Fehlalarm, und ein gutes Bauteil wird unnötig nachgeprüft.
* Ein Fehldruck, den der Baum als gut einstuft, ist **falsch negativ**. Der
  Ausschuss rutscht durch und landet im schlimmsten Fall beim Kunden.
* Ein Fehldruck, den der Baum als Fehldruck meldet, ist **richtig positiv**.

Die Abkürzungen kommen aus dem Englischen: True Negative (TN), False Positive
(FP), False Negative (FN) und True Positive (TP).

Jetzt lesen wir unsere Konfusionsmatrix ab. Links oben stehen 43 gute Drucke,
die der Baum richtig als gut einstuft. Links unten stehen 7 falsch negative
Drucke. In der rechten Spalte stehen nur Nullen. Der Baum meldet also keinen
einzigen Fehldruck, und alle 7 Fehldrucke in den Testdaten rutschen durch. Für
die Qualitätskontrolle ist dieses Modell wertlos, obwohl die Accuracy von 0.86
gut klingt.

Auch die Accuracy können wir aus der Konfusionsmatrix ablesen. Die richtigen
Prognosen stehen auf der Diagonalen von links oben nach rechts unten. Wir teilen
sie durch die Anzahl aller Prognosen:

$$
\text{Accuracy} =
\frac{\text{TN} + \text{TP}}{\text{TN} + \text{FP} + \text{FN} + \text{TP}}
$$

In unserem Beispiel ergibt das (43 + 0) / 50 = 0.86. Die Accuracy zählt jede
richtige Prognose gleich. Für die 43 guten Drucke reicht schon die Regel "immer
kein Fehldruck". Diese vielen leichten Fälle bestimmen die Accuracy. Die 7
übersehenen Fehldrucke fallen kaum ins Gewicht. Kommt eine Klasse viel seltener
vor als die andere, sprechen wir von **unausgewogenen Klassen**. Je
unausgewogener die Klassen sind, desto stärker täuscht die Accuracy. Deshalb
vergleichen wir die Accuracy immer mit dem Referenzmodell und schauen zusätzlich
in die Konfusionsmatrix.

```{admonition} Mini-Übung
:class: tip
Übertragen Sie das Vorgehen auf den Datensatz `3ddruck_gittersuche.csv` aus
Kapitel 10.2. Er enthält 300 Druckaufträge. Der Anteil der Fehldrucke ist
deutlich höher als im Fließtext.

1. Lesen Sie die Datei ein und kodieren Sie die Zielgröße `Erfolgreich` so, dass
   ein Fehldruck die 1 ist. Verwenden Sie als Eingabedaten die Merkmale
   `Drucktemperatur (C)`, `Betttemperatur (C)` und
   `Druckgeschwindigkeit (mm/s)`. Wählen Sie für Daten und Zielgröße andere
   Namen als im Fließtext, damit Sie die Beispieldaten nicht überschreiben.
2. Teilen Sie die Daten so in Trainings- und Testdaten auf, dass der Anteil der
   Fehldrucke in beiden Teilen gleich ist. Trainieren Sie einen
   Entscheidungsbaum der Tiefe 3 und berechnen Sie die Accuracy auf den
   Testdaten. Verwenden Sie für die Aufteilung und den Entscheidungsbaum
   `random_state=0`, damit Ihre Ergebnisse mit der Lösung vergleichbar sind.
   Welche Accuracy erreicht das Referenzmodell, das immer "kein Fehldruck"
   vorhersagt?
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

modell_druck = DecisionTreeClassifier(max_depth=3, random_state=0)
modell_druck.fit(X_druck_train, y_druck_train)
accuracy_test_druck = modell_druck.score(X_druck_test, y_druck_test)
print(f'Accuracy Testdaten: {accuracy_test_druck:.2f}')

print(y_druck_test.value_counts())
```

Zu 2. Der Baum erreicht auf den Testdaten eine Accuracy von 0.76. In den
Testdaten sind 45 gute Drucke und 30 Fehldrucke. Das Referenzmodell liegt also
bei 45 von 75 Drucken richtig und erreicht eine Accuracy von 45/75 = 0.60. Der
Baum ist damit deutlich besser als das Referenzmodell.

```python
from sklearn.metrics import confusion_matrix

y_druck_prognose = modell_druck.predict(X_druck_test)
konfusionsmatrix_druck = confusion_matrix(y_druck_test, y_druck_prognose)
print(konfusionsmatrix_druck)
```

Zu 3. Die Konfusionsmatrix lautet `[[34 11] [7 23]]`. Der Baum erkennt 23 der 30
Fehldrucke (richtig positiv). 7 Fehldrucke rutschen durch (falsch negativ).
Dazu kommen 11 Fehlalarme (falsch positiv).

Zu 4. In den Testdaten sind hier 30 von 75 Drucken Fehldrucke, also 40 %. Im
Fließtext waren es nur 7 von 50, also 14 %. Die Klassen sind hier viel
ausgewogener. Das Referenzmodell erreicht deshalb nur 0.60. Eine hohe Accuracy
ist nur möglich, wenn das Modell auch Fehldrucke richtig erkennt. Je
ausgewogener die Klassen, desto weniger täuscht die Accuracy.
````

## Precision, Recall und F1-Score

* Fragen aus der Praxis: Welcher Anteil der Fehldrucke wird gefunden? Wie viele
  Alarme sind berechtigt?
* Recall (Trefferquote): richtig positiv geteilt durch alle tatsächlichen
  Fehldrucke. "Wie viel Ausschuss fangen wir ab?"
* Precision (Präzision): richtig positiv geteilt durch alle gemeldeten
  Fehldrucke. "Wie oft schlagen wir unnötig Alarm?"
* Englische Begriffe beibehalten. Im Deutschen steht "Genauigkeit" mal für
  Accuracy, mal für Precision.
* Kernbeispiel: derselbe Baum mit `class_weight='balanced'`, damit Fehldrucke
  beim Training stärker zählen. Die Accuracy sinkt von 0.86 auf 0.84, aber 3
  von 7 Fehldrucken werden erkannt (Recall 0.43), bei 4 Fehlalarmen (Precision
  0.43). Das Modell mit der schlechteren Accuracy ist für die
  Qualitätskontrolle das bessere.
* Zielkonflikt: Mehr Alarme erhöhen den Recall und senken meist die Precision.
* F1-Score: fasst Precision und Recall in einer Zahl zusammen (harmonisches
  Mittel) und wird klein, sobald einer der beiden Werte klein ist.
* Code: `precision_score()`, `recall_score()` und `f1_score()` aus
  `sklearn.metrics`.
* Welches Gütemaß wann? Sicherheitsbauteil: Recall wichtig, kein Ausschuss darf
  durchrutschen. Teure Nachprüfung oder Produktionsstopp bei jedem Alarm:
  Precision wichtig. Beides gleich wichtig: F1-Score.
* Rückbezug zu 10.2: Mit `scoring='recall'` oder `scoring='f1'` optimieren
  `cross_validate()` und `GridSearchCV` das passende Gütemaß statt der
  Accuracy.
* Mini-Übung: Precision, Recall und F1-Score für das Modell aus der vorherigen
  Mini-Übung berechnen und für zwei Anwendungsfälle das passende Gütemaß
  begründen. Optional eine Gittersuche mit `scoring='recall'`.

## Gütemaße für Regression

* Anknüpfung an Kapitel 7: Bei Regression ist der Standard-Score das
  Bestimmtheitsmaß R². Es zeigt, wie gut das Modell im Vergleich zum Mittelwert
  ist, aber nicht, wie weit die Prognosen danebenliegen.
* Kernbeispiel: Verkaufspreis mit dem Autoscout24-Datensatz vorhersagen
  (Kilometerstand, Leistung, Jahr), lineare Regression. R² liegt bei etwa 0.66.
* MAE (mittlerer absoluter Fehler): Mittelwert der Beträge der Residuen, in
  Euro und damit direkt verständlich: "Im Mittel liegen wir etwa 6000 Euro
  daneben."
* MSE (mittlerer quadratischer Fehler): die Fehlerquadratsumme aus Kapitel 7.1,
  geteilt durch die Anzahl der Datenpunkte. Große Fehler zählen besonders
  stark, die Einheit Euro² ist aber schwer zu deuten.
* RMSE: Wurzel aus dem MSE, wieder in Euro, im Beispiel etwa 9700 Euro. Liegt
  der RMSE deutlich über dem MAE, gibt es einzelne grobe Fehlprognosen.
* Code: `mean_absolute_error()` und `mean_squared_error()` aus
  `sklearn.metrics`, RMSE mit `np.sqrt()`.
* Welches Gütemaß wann? R² zum Einordnen und Vergleichen, MAE zum Kommunizieren,
  RMSE wenn große Abweichungen besonders teuer sind, etwa bei Toleranzen.
* Hinweis für die Gittersuche: `scoring='neg_mean_absolute_error'`.
  Scikit-Learn maximiert immer, deshalb steht der Fehler mit negativem
  Vorzeichen.
* Mini-Übung: Zugfestigkeit mit `3ddruck_gittersuche.csv` vorhersagen, R², MAE
  und RMSE berechnen und in MPa deuten.

## Zusammenfassung und Ausblick

* Die Accuracy täuscht bei unausgewogenen Klassen. Die Konfusionsmatrix zeigt,
  welche Fehler ein Modell macht.
* Precision, Recall und F1-Score beantworten unterschiedliche Fragen. Die Wahl
  hängt davon ab, welcher Fehler teurer ist.
* Bei Regression ergänzen MAE und RMSE das R² um die Größe der Fehler in der
  Einheit der Zielgröße.
* Ausblick auf Kapitel 11 (Neuronale Netze): Die Gütemaße aus diesem Kapitel
  gelten für jedes Modell, auch für neuronale Netze.
