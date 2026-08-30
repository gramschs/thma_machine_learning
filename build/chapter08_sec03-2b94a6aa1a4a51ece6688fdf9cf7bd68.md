---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: autoscout24_kodierung.csv
    title: autoscout24_kodierung.csv
  - file: 3ddruck_kodierung.csv
    title: 3ddruck_kodierung.csv
  - file: chapter08_sec03.md
    title: chapter08_sec03.md
---

# 8.3 Trainings- und Testdaten

Bei den Entscheidungsbäumen und der linearen Regression haben wir mit der Methode
`.score()` bewertet, wie gut ein Modell zu den Daten passt. Je näher der Wert an
1 liegt, desto besser. Ein hoher Wert allein sagt aber wenig aus. Ein Modell kann
die Trainingsdaten auswendig lernen und bei neuen Daten trotzdem versagen. Diesen
Fehler nennen wir **Overfitting**.

Deshalb teilen wir unsere Daten in **Trainingsdaten** und **Testdaten** auf. Mit
den Testdaten prüfen wir, wie gut ein Modell mit Daten zurechtkommt, die es beim
Training nicht gesehen hat. Zum Schluss schauen wir uns an, wie die Skalierung
aus Kapitel 8.2 mit dieser Aufteilung zusammenpasst.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können erklären, warum ein hoher Score auf den Trainingsdaten kein
  gutes Modell garantiert (**Overfitting**).
* [ ] Sie wissen, warum wir Daten in **Trainingsdaten** und **Testdaten**
  aufteilen.
* [ ] Sie können Daten mit der Funktion `train_test_split()` in Trainings- und
  Testdaten aufteilen.
* [ ] Sie wissen, dass ein Scaler nur an die Trainingsdaten angepasst wird, damit
  kein **Data Leakage** entsteht.
```

## Auswendiglernen nützt nichts

Wir betrachten ein einfaches Beispiel. Angenommen, wir haben die folgenden 20
Messwerte erfasst und wollen ein Regressionsproblem lösen.

```{code-cell} python
import pandas as pd
import plotly.express as px

# Daten erzeugen
daten = pd.DataFrame()
daten['Ursache'] = [1.8681193560547067, 0.18892899670288932, 1.8907374398595373, 0.8592639746974586, 0.7909152983890833, -1.1356420176784945, 1.905097819104967, -1.9750789791816405, -0.9880705504662242, -0.26083387038221684, 1.1175316871750098, -1.2092597015989877, 1.451972942396889, 1.933602708701251, -1.3446310343812051, 0.38933577573143685, -1.96405560932978, -0.45371486942548245, -1.8233597682740017, 1.8266118708569437]
daten['Wirkung'] = [18.06801933135814, 0.09048390063552635, 18.29951272892001, 4.02392603643671, 1.97091878521032, 6.799411114666941, 17.540101218695103, 21.051664199041685, 5.604758672240995, 0.38630710692300024, 5.261393705782588, 7.365977868421521, 10.701020062336028, 17.48514901635516, 11.263523310016517, 1.1522069460363902, 20.979929897937023, -0.08352624016486021, 18.258951764602635, 15.321589041941028]

# Visualisierung
fig = px.scatter(daten, x='Ursache', y='Wirkung', title='Künstlich generierte Messdaten')
fig.show()
```

Jetzt bauen wir ein Modell. Der Name sagt bereits alles. Beim Training speichert
es die Zielwerte. Bei einer Prognose gibt es genau diese gespeicherten Werte
wieder zurück.

```{code-cell} python
from sklearn.metrics import r2_score

class AuswendigLerner:
    def fit(self, X, y):
        self.y = y

    def predict(self, X):
        return self.y
```

Wir trainieren unser Modell und lassen es dann bewerten. Um nicht selbst den
R²-Score implementieren zu müssen, verwenden wir die allgemeine Funktion aus
Scikit-Learn (siehe [Dokumentation Scikit-Learn →
r2_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html)).

```{code-cell} python
# Daten ins richtige Format bringen
X = daten[['Ursache']]
y = daten['Wirkung']

# Modell wählen und trainieren
mein_super_modell = AuswendigLerner()
mein_super_modell.fit(X, y)

# Prognose
y_prognose = mein_super_modell.predict(X)

# Güte bewerten
r2_training = r2_score(y, y_prognose)
print(f'Der R²-Score auf den Trainingsdaten ist: {r2_training:.2f}')
```

Der R²-Score ist 1, unser Modell scheint perfekt zu funktionieren. Doch wie
prognostiziert es neue Daten? Das Modell funktioniert hervorragend für die schon
bekannten Daten, ist aber **nicht verallgemeinerbar**.

```{code-cell} python
mein_super_modell.predict([[1.3]])
```

Statt einer einzelnen Prognose für die Ursache 1.3 gibt das Modell alle 20
gespeicherten Wirkungen zurück. Es hat die Trainingsdaten auswendig gelernt, aber
keinen Zusammenhang verstanden. Auf den Trainingsdaten sieht das Modell perfekt
aus, für neue Daten ist es unbrauchbar.

## Daten für später aufheben

Wir wollen wissen, ob ein Modell auch mit neuen Daten zurechtkommt. Auf die
nächsten Messungen zu warten, dauert zu lange. Deshalb legen wir schon jetzt
einen Teil der vorhandenen Daten beiseite. Diesen Teil nennen wir **Testdaten**,
den Rest **Trainingsdaten**. Trainiert wird nur mit den Trainingsdaten. Mit den
Testdaten prüfen wir danach, wie gut das Modell bei Daten funktioniert, die es
beim Training nicht gesehen hat.

Für die Aufteilung in Trainings- und Testdaten verwenden wir eine dafür
vorgesehene Funktion von Scikit-Learn namens `train_test_split()` (siehe
[Dokumentation Scikit-Learn →
train_test_split()](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)).
Diese Funktion müssen wir aus dem Modul `sklearn.model_selection` importieren.
Dann übergeben wir `train_test_split()` die Daten, die aufgeteilt werden sollen,
und erhalten als Rückgabe zwei DataFrames: Der erste enthält die Trainingsdaten,
der zweite die Testdaten.

```{code-cell} python
from sklearn.model_selection import train_test_split

daten_train, daten_test = train_test_split(daten)
```

Nun wollen wir sehen, welche Datenpunkte zu den Trainingsdaten und welche zu den
Testdaten gehören. Dazu fügen wir dem Datensatz ein neues Merkmal hinzu und
füllen es mit den Strings `'Trainingsdaten'` bzw. `'Testdaten'`. Anschließend
visualisieren wir die Datenpunkte wie oben, wobei die Punkte entsprechend ihrer
Zugehörigkeit (Trainings- oder Testdaten) eingefärbt werden.

```{code-cell} python
# Datenpunkte nach Splitstatus einfärben
daten.loc[daten_train.index, 'Splitstatus'] = 'Trainingsdaten'
daten.loc[daten_test.index, 'Splitstatus'] = 'Testdaten'

fig = px.scatter(daten, x='Ursache', y='Wirkung', color='Splitstatus',
                 title='Künstlich generierte Messdaten')
fig.show()
```

Standardmäßig hält `train_test_split()` 25 % der Daten als Testdaten zurück, hier
also 5 von 20 Datenpunkten. Die Auswahl ist zufällig, jeder Durchlauf liefert
eine andere Aufteilung.

Die Funktion hat einige nützliche Optionen:

- `test_size`: Anteil oder Anzahl der Testdaten. `test_size=0.1` hält 10 %
  zurück, `test_size=7` genau 7 Datenpunkte.
- `random_state`: Ein fester Wert wie `random_state=0` macht die zufällige
  Aufteilung reproduzierbar. Das ist für Vergleiche und Lehrmaterial nützlich.
- `shuffle`: Ob die Daten vor der Aufteilung gemischt werden. Standard ist
  `True`. Bei sortierten Daten ist das wichtig, sonst landen zum Beispiel nur
  billige Autos in den Trainingsdaten und nur teure in den Testdaten.
- `stratify`: Sorgt dafür, dass eine Klassenverteilung in beiden Teilen gleich
  bleibt. Sind 30 % der Autos Diesel, dann auch in Trainings- und Testdaten.

Alle Optionen stehen in der [Dokumentation Scikit-Learn →
train_test_split()](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html).

Für den weiteren Verlauf teilen wir unsere Daten mit einem festen `random_state`
auf und halten 7 Datenpunkte als Testdaten zurück.

```{code-cell} python
daten_train, daten_test = train_test_split(daten, test_size=7, random_state=0)

# Datenpunkte nach Splitstatus einfärben
daten.loc[daten_train.index, 'Splitstatus'] = 'Trainingsdaten'
daten.loc[daten_test.index, 'Splitstatus'] = 'Testdaten'

fig = px.scatter(daten, x='Ursache', y='Wirkung', color='Splitstatus',
                 title='Künstlich generierte Messdaten')
fig.show()
```

Damit haben wir das Werkzeug, um **Overfitting** aufzudecken. Ein Modell wird nur
mit den Trainingsdaten trainiert und danach mit den Testdaten bewertet. Der
`AuswendigLerner` aus dem ersten Abschnitt schneidet auf den Trainingsdaten
perfekt ab. Auf den Testdaten würde er durchfallen, denn für neue Ursachen kennt
er keine Wirkung. Ab jetzt teilen wir unsere Daten in jedem Kapitel zuerst auf.

```{admonition} Mini-Übung
:class: tip
Arbeiten Sie mit dem Datensatz `3ddruck_kodierung.csv`. Die Spalte `Nummer` soll
als Zeilenindex dienen.

1. Teilen Sie den Datensatz in Trainings- und Testdaten auf. 20 % der Daten
   sollen Testdaten sein. Legen Sie einen festen Wert für den Zufallsgenerator
   fest.
2. Prüfen Sie, wie viele Druckaufträge in den Trainingsdaten und wie viele in den
   Testdaten sind.
3. Im Merkmal `Erfolgreich` gibt es viel mehr erfolgreiche als nicht erfolgreiche
   Drucke. Teilen Sie erneut auf, diesmal so, dass dieses Verhältnis in beiden
   Teilen erhalten bleibt.
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

druckversuche = pd.read_csv('3ddruck_kodierung.csv', index_col=0)

druckversuche_train, druckversuche_test = train_test_split(
    druckversuche, test_size=0.2, random_state=0
)

print('Trainingsdaten:', len(druckversuche_train))
print('Testdaten:', len(druckversuche_test))
```

Mit `stratify` bleibt die Verteilung von `Erfolgreich` in beiden Teilen erhalten:

```python
druckversuche_train, druckversuche_test = train_test_split(
    druckversuche, test_size=0.2, random_state=0,
    stratify=druckversuche['Erfolgreich']
)

print(druckversuche_train['Erfolgreich'].value_counts(normalize=True))
print(druckversuche_test['Erfolgreich'].value_counts(normalize=True))
```
````

## Skalieren ohne Data Leakage

In Kapitel 8.2 haben wir den kompletten Datensatz auf einmal skaliert. Jetzt
trennen wir vorher in Trainings- und Testdaten. Dabei müssen wir aufpassen.

Wir holen den Autoscout24-Datensatz zurück, behalten die numerischen Merkmale und
teilen auf.

```{code-cell} python
daten = pd.read_csv('autoscout24_kodierung.csv')
daten = daten.drop(columns=['Marke', 'Modell', 'Farbe', 'Erstzulassung',
                            'Getriebe', 'Kraftstoff', 'Bemerkungen', 'Zustand'])

daten_train, daten_test = train_test_split(daten, test_size=0.2, random_state=7)
```

Die Regel lautet: Der Scaler wird nur mit den Trainingsdaten angepasst. Wir rufen
`.fit()` also ausschließlich mit den Trainingsdaten auf. Danach transformieren wir
beide Teile.

```{code-cell} python
from sklearn.preprocessing import MinMaxScaler

normierung = MinMaxScaler()
normierung.fit(daten_train)

daten_train_normiert = normierung.transform(daten_train)
daten_test_normiert = normierung.transform(daten_test)
```

Warum nur die Trainingsdaten? Berechnet der Scaler Minimum und Maximum aus allen
Daten, fließt Wissen über die Testdaten in die Vorbereitung ein. Der Testscore
wäre dann zu gut. Diesen schleichenden Informationsfluss nennen wir **Data
Leakage**. Die Testdaten sollen neue, ungesehene Daten nachstellen, deshalb
halten wir sie aus jeder Vorbereitung heraus.

Eine Folge davon: Testwerte können nach der Normierung auch außerhalb von 0 bis
1 liegen. Das passiert, wenn ein Testauto extremer ist als alle Trainingsautos.

```{code-cell} python
daten_test_normiert = pd.DataFrame(daten_test_normiert, columns=daten.columns)
daten_test_normiert.describe()
```

Bei der Leistung und beim Kilometerstand liegt der größte Testwert über 1. In den
Testdaten steht ein Auto mit mehr PS als jedes Auto in den Trainingsdaten. Das
ist kein Fehler, sondern richtig so.

Dasselbe Prinzip gilt für andere Vorbereitungsschritte, die etwas aus den Daten
berechnen, zum Beispiel das Ersetzen fehlender Werte durch den Mittelwert aus
Kapitel 8.1. Auch dieser Mittelwert wird nur aus den Trainingsdaten gebildet.

```{admonition} Mini-Übung
:class: tip
Arbeiten Sie mit dem Datensatz `3ddruck_kodierung.csv`. Die Spalte `Nummer` soll
als Zeilenindex dienen. Behalten Sie nur die numerischen Merkmale.

1. Teilen Sie den Datensatz in Trainings- und Testdaten auf. 20 % sollen
   Testdaten sein, mit festem Wert für den Zufallsgenerator.
2. Normieren Sie beide Teile auf das Intervall von 0 bis 1. Passen Sie die
   Normierung dabei nur an die Trainingsdaten an.
3. Prüfen Sie über die statistischen Kennzahlen, ob Testwerte außerhalb von 0 bis
   1 liegen.
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
from sklearn.preprocessing import MinMaxScaler

druckversuche = pd.read_csv('3ddruck_kodierung.csv', index_col=0)
druckversuche = druckversuche.drop(
    columns=['Material', 'Farbe', 'Infill-Muster', 'Oberflaechenguete',
             'Erfolgreich', 'Bemerkungen']
)

druckversuche_train, druckversuche_test = train_test_split(
    druckversuche, test_size=0.2, random_state=0
)

normierung = MinMaxScaler()
normierung.fit(druckversuche_train)

druckversuche_train_normiert = normierung.transform(druckversuche_train)
druckversuche_test_normiert = normierung.transform(druckversuche_test)
```

Die Kennzahlen der normierten Testdaten:

```python
druckversuche_test_normiert = pd.DataFrame(
    druckversuche_test_normiert, columns=druckversuche.columns
)
druckversuche_test_normiert.describe()
```

Bei der Drucktemperatur liegt der kleinste Testwert leicht unter 0. In den
Testdaten gibt es einen Druck mit niedrigerer Temperatur als in allen
Trainingsdaten.
````

## Zusammenfassung und Ausblick

Wir haben unsere Daten in **Trainingsdaten** und **Testdaten** aufgeteilt. Mit
der Funktion `train_test_split()` geht das in einer Zeile. Trainiert wird nur mit
den Trainingsdaten, bewertet wird mit den Testdaten. So erkennen wir
**Overfitting**. Auch einen Scaler passen wir nur an die Trainingsdaten an, sonst
entsteht **Data Leakage**.

Ein einzelner Split hat einen Nachteil. Er hängt vom Zufall ab, und ein Teil der
Daten steht nicht für das Training zur Verfügung. Bei der **Kreuzvalidierung**
teilt man die Daten in mehrere Teile und trainiert und testet das Modell
mehrmals. Wir behandeln sie ausführlich in Kapitel 10.
