---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: autoscout24_DE_2020.csv
    title: autoscout24_DE_2020.csv
  - file: 3ddruck_xxs.csv
    title: 3ddruck_xxs.csv
  - file: chapter05_sec03.md
    title: chapter05_sec03.md
---

# 5.3 Barplots und Histogramme

Barplots (Balken- oder Säulendiagramme) sind die am häufigsten verwendeten
Visualisierungen für kategoriale Daten. In diesem Kapitel lernen wir, wie mit
Plotly ein Barplot erstellt und von einem Histogramm unterschieden wird.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie kennen **Barplots** zur Visualisierung kategorialer Daten und können
  Säulen- und Balkendiagramme unterscheiden.
* [ ] Sie können mit **px.bar()** Barplots erstellen und anpassen.
* [ ] Sie wissen, wann **Histogramme** statt Barplots verwendet werden.
* [ ] Sie können mit **px.histogram()** Histogramme erstellen und die Anzahl der
  Bins sinnvoll wählen.
```

## Barplots

Im letzten Kapitel haben wir uns mit kategorialen (qualitativen) Daten
auseinandergesetzt. Um kategoriale Daten zu visualisieren und zu vergleichen,
eignet sich besonders der **Barplot**. Ein Barplot zeigt numerische Werte (z.B.
Anzahlen oder Durchschnittswerte) für verschiedene Kategorien an.

Bei der Visualisierung werden prinzipiell zwei Varianten unterschieden. Zum
einen können die Kategorien entlang der x-Achse aneinandergereiht werden. Die
Höhe der Rechtecke repräsentiert dann den Zahlenwert dieser Kategorie. Da die
Rechtecke an Säulen erinnern, wird diese Variante **Säulendiagramm** genannt.
Die andere Möglichkeit ist, die Kategorien untereinander entlang der y-Achse
aufzuführen. Dann ist die Länge der Rechtecke repräsentativ für den Zahlenwert
dieser Kategorie. Diese Variante wird **Balkendiagramm** genannt.

```{admonition} Was ist ... ein Barplot?
:class: note
Ein Barplot ist ein Diagramm, das numerische Werte für verschiedene Kategorien 
visualisiert. Jede Kategorie wird durch die Höhe oder Länge eines Rechtecks 
repräsentiert, das den zugehörigen numerischen Wert darstellt.
```

Probieren wir Barplots am Beispiel der schon bekannten
AutoScout24-Verkaufspreise für Autos aus `autoscout24_DE_2020.csv`. Zuerst laden
wir die Daten und verschaffen uns einen Überblick.

```{code-cell}
import pandas as pd

data = pd.read_csv('autoscout24_DE_2020.csv')
data.info()
```

Mit der Methode `.value_counts()` lassen wir Python die Anzahl der Autos pro
Marke bestimmen.

```{code-cell}
anzahl_pro_marke = data['Marke'].value_counts()
print(anzahl_pro_marke)
```

Die Methode `.value_counts()` sortiert die Einträge standardmäßig von der
höchsten zur niedrigsten Anzahl.

Mit nur wenigen Zeilen Code können wir mit der Funktion `bar()` aus dem
Plotly-Express-Modul eine Visualisierung erstellen. Zuerst importieren wir das
Modul, dann erzeugen wir das Diagramm mit `bar()` und zuletzt lassen wir das
Diagramm mit `show()` anzeigen. Mittels der Option `orientation='h'` erzeugen
wir ein Balkendiagramm mit horizontaler Ausrichtung.

```{code-cell}
import plotly.express as px

saeulendiagramm = px.bar(anzahl_pro_marke)
saeulendiagramm.show()

balkendiagramm = px.bar(anzahl_pro_marke, orientation='h')
balkendiagramm.show()
```

Obwohl Plotly Express bereits eine ansprechende Visualisierung bietet, könnten
die automatisch generierten Beschriftungen "index", "value" und "variable"
verbessert werden. Außerdem sollte ein Diagrammtitel hinzugefügt werden. Der
Titel kann direkt in der `bar()`-Funktion über das `title=` Argument gesetzt
werden. Für die Achsenbeschriftungen und den Legendentitel verwenden wir die
Funktion `update_layout()`. Die Argumente `xaxis_title=` und `yaxis_title=`
modifizieren die Beschriftung der x- und y-Achse. Mit `legend_title=` wird der
Titel der Legende neu beschriftet.

```{code-cell}
fig = px.bar(anzahl_pro_marke, title='AutoScout24 (Zulassungsjahr 2020)')
fig.update_layout(
    xaxis_title='Marke',
    yaxis_title='Anzahl Autos',
    legend_title='Anzahl Autos pro Marke',
)
fig.show()
```

```{admonition} Mini-Übung
:class: tip
Verwenden Sie den Datensatz `3ddruck_xxs.csv` (mit Nummer als Zeilenindex).

1. Lesen Sie die Datei ein.
2. Ermitteln Sie, wie oft jedes Material im Datensatz vorkommt.
3. Visualisieren Sie die Verteilung der Materialien als Säulendiagramm.
   Vergeben Sie einen Titel sowie sinnvolle Achsenbeschriftungen.
```

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd
import plotly.express as px

# 1. Datei einlesen
druckversuche = pd.read_csv('3ddruck_xxs.csv', index_col=0)

# 2. Anzahl pro Material bestimmen
anzahl_pro_material = druckversuche['Material'].value_counts()
print(anzahl_pro_material)

# 3. Säulendiagramm erstellen
fig = px.bar(anzahl_pro_material, title='Materialverteilung der Druckversuche')
fig.update_layout(
    xaxis_title='Material',
    yaxis_title='Anzahl Druckversuche',
    legend_title='Anzahl Druckversuche pro Material',
)
fig.show()
```

Am häufigsten wurde PETG verwendet (6 von 18 Druckversuchen), gefolgt von ABS
(5), PLA (4) und ASA (3).
````

## Histogramm

Während Barplots in erster Linie kategoriale Daten visualisieren, dienen
Histogramme zur Darstellung numerischer Daten. Ein Barplot zeigt typischerweise
die Anzahl der Werte pro Kategorie. Bei numerischen Daten wäre eine solche
Darstellung oft nicht sinnvoll. Nehmen wir als Beispiel die Kilometerstände von
Autos. Wir lassen zuerst mit der Methode `.unique()` die verschiedenen
Kilometerstände bestimmen. Das Ergebnis ist ein sogenanntes NumPy-Array, das
hier wie eine Liste benutzt werden kann. Mit Hilfe der `len()`-Funktion können
wir die Anzahl der Einträge berechnen.

```{code-cell}
kilometerstaende = data['Kilometerstand (km)'].unique()
anzahl_kilometerstaende = len(kilometerstaende)
print(f'Es gibt {anzahl_kilometerstaende} verschiedene Kilometerstände.')
```

Mit über 10 000 verschiedenen Kilometerständen wäre eine direkte Visualisierung
nicht zielführend. Um dennoch eine sinnvolle Analyse durchzuführen, können wir
den Bereich der Kilometerstände in Intervalle einteilen. Dazu bestimmen wir das
Minimum und das Maximum der Kilometerstände.

```{code-cell}
minimaler_kilometerstand = data['Kilometerstand (km)'].min()
maximaler_kilometerstand = data['Kilometerstand (km)'].max()

print(f'minimaler Kilometerstand: {minimaler_kilometerstand}')
print(f'maximaler Kilometerstand: {maximaler_kilometerstand}')
```

Die Daten reichen von Neuwagen (minimaler Kilometerstand 0 km) bis zu Autos mit
hohem Kilometerstand (maximaler Kilometerstand 435 909 km). Wir können diesen
Bereich in gleichmäßige Intervalle unterteilen. Wählen wir beispielsweise 10
Intervalle, so würde das erste Intervall alle Autos mit einem Kilometerstand von
0 km bis 50 000 km umfassen. Das zweite Intervall geht dann von 50 000 km bis
100 000 km usw. Um jetzt zu ermitteln, wie viele Autos in das jeweilige Intervall
fallen, könnten wir ein kleines Python-Programm schreiben. Tatsächlich brauchen
wir das nicht, denn diese Funktionalität ist bereits in der
`histogram()`-Funktion integriert, die auch die Visualisierung übernimmt.

Wir übergeben der Funktion die Daten als erstes Argument. Als optionales zweites
Argument können wir die gewünschte Anzahl an Intervallen übergeben. Die
künstlich gewählten Intervalle werden auch als Bins bezeichnet. Daher lautet das
Argument zum Setzen der Anzahl der Bins `nbins=`, so wie der englische Begriff
»number of bins«.

```{code-cell}
fig = px.histogram(data['Kilometerstand (km)'], nbins=10, 
    title='10 künstlich gewählte Intervalle bzgl. des Kilometerstandes (km)')
fig.update_layout(
    xaxis_title='Kategorien der Kilometerstände (km)',
    yaxis_title='Anzahl Autos',
    legend_title='Anzahl Autos pro Kategorie',
)
fig.show()
```

Die meisten Autos haben weniger als 200000 km auf dem Kilometerzähler.

Ein charakteristisches Merkmal von Histogrammen ist, dass die Balken ohne Lücke
aneinander liegen, was die kontinuierliche Natur der numerischen Daten
widerspiegelt. Die Anzahl der Kategorien (Bins) beeinflusst die Darstellung
maßgeblich und sollte sorgfältig gewählt werden.

Die Anzahl der Kategorien ist ein sehr wichtiger Faktor bei der Visualisierung.
Werden zu wenige Kategorien gewählt, werden auch nicht die Unterschiede
sichtbar. Werden zu viele Kategorien gewählt, sind ggf. einige Kategorien leer.

```{admonition} Mini-Übung
:class: tip
Verwenden Sie den Datensatz `3ddruck_xxs.csv` (mit Nummer als Zeilenindex).

1. Lesen Sie die Datei ein.
2. Visualisieren Sie die Verteilung der Spalte `Zugfestigkeit (MPa)` als
   Histogramm mit 3 Intervallen.
3. Probieren Sie anschließend 5 und 10 Intervalle aus. Was beobachten Sie
   bei 10 Intervallen? Woran liegt das, wenn Sie an die Anzahl der
   Druckversuche in diesem Datensatz denken?
```

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd
import plotly.express as px

# 1. Datei einlesen
druckversuche = pd.read_csv('3ddruck_xxs.csv', index_col=0)

# 2./3. Histogramm mit unterschiedlicher Anzahl an Intervallen
fig = px.histogram(druckversuche['Zugfestigkeit (MPa)'], nbins=10,
    title='Zugfestigkeit der Druckversuche')
fig.update_layout(
    xaxis_title='Zugfestigkeit (MPa)',
    yaxis_title='Anzahl Druckversuche',
    legend_title='Anzahl Druckversuche pro Kategorie',
)
fig.show()
```

* Mit `nbins=3` entstehen breite Intervalle (20 MPa), in denen jeweils mehrere
  Druckversuche liegen, aber nur grobe Muster erkennbar sind.
* Mit `nbins=5` wird die Verteilung schon etwas genauer sichtbar, ohne dass
  Intervalle leer bleiben.
* Bei `nbins=10` bleibt eines der Intervalle leer, da der Datensatz nur 18
  Druckversuche enthält. Bei so kleinen Datensätzen sind wenige, breite
  Intervalle daher meist sinnvoller als bei dem großen AutoScout24-Datensatz.
````

Zusammenfassend wird ein Histogramm folgendermaßen beschrieben.

```{admonition} Was ist ... ein Histogramm?
:class: note
Ein Histogramm ist eine grafische Darstellung der Häufigkeitsverteilung 
numerischer Daten. Dabei wird der Wertebereich in gleich große Intervalle 
(sogenannte Bins oder Klassen) eingeteilt. Die Höhe jedes Balkens zeigt, wie 
viele Datenpunkte in das jeweilige Intervall fallen. Ein charakteristisches 
Merkmal: Die Balken liegen ohne Lücken aneinander, da sie eine kontinuierliche 
Skala repräsentieren.
```

## Zusammenfassung und Ausblick

In diesem Kapitel wurden zwei wichtige Diagrammtypen vorgestellt: der Barplot
und das Histogramm. Obwohl beide mit Rechtecken arbeiten, haben sie
unterschiedliche Anwendungsbereiche und sollten nicht verwechselt werden.
Während der Barplot ideal für kategoriale Daten ist, eignet sich das Histogramm
zur Visualisierung numerischer Daten. Damit schließen wir die Kapitel zur
Datenexploration ab. Im nächsten Kapitel beginnt der Teil zum maschinellen
Lernen mit den Entscheidungsbäumen.
