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

# 5.2 Barplots und Histogramme

Barplots (Balken- oder Säulendiagramme) sind die am häufigsten verwendeten
Visualisierungen für kategoriale Daten. In diesem Kapitel lernen wir, wie mit
Plotly ein Barplot erstellt und von einem Histogramm unterschieden wird.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie kennen **Barplots** zur Visualisierung kategorialer Daten und können 
  Säulen- und Balkendiagramme unterscheiden.
* Sie können mit **px.bar()** Barplots erstellen und anpassen.
* Sie wissen, wann **Histogramme** statt Barplots verwendet werden.
* Sie können mit **px.histogram()** Histogramme erstellen und die Anzahl 
  der Bins sinnvoll wählen.
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

Probieren wir Barplots am Beispiel der Autoscout24-Verkaufspreise für Autos aus,
die 2020 zugelassen wurden ({download}`Download autoscout24_DE_2020.csv
<https://gramschs.github.io/book_ml4ing/data/autoscout24_DE_2020.csv>`). Zuerst
laden wir die Daten und verschaffen uns einen Überblick.

```{code-cell}
import pandas as pd

url = 'https://raw.githubusercontent.com/gramschs/assets/refs/heads/main/ml4ing/data/autoscout24_DE_2020.csv'
data = pd.read_csv(url)
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
fig = px.bar(anzahl_pro_marke, title='Autoscout24 (Zulassungsjahr 2020)')
fig.update_layout(
    xaxis_title='Marke',
    yaxis_title='Anzahl Autos',
    legend_title='Anzahl Autos pro Marke',
)
fig.show()
```

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

Mit über 10.000 verschiedenen Kilometerständen wäre eine direkte Visualisierung
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
hohem Kilometerstand (maximaler Kilometerstand 435909 km). Wir können diesen
Bereich in gleichmäßige Intervalle unterteilen. Wählen wir beispielsweise 10
Intervalle, so würde das erste Intervall alle Autos mit einem Kilometerstand von
0 km bis 50000 km umfassen. Das zweite Intervall geht dann von 50000 km bis
100000 km usw. Um jetzt zu ermitteln, wie viele Autos in das jeweilige Intervall
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
Experimentieren Sie mit verschiedenen Werten für `nbins=`. Probieren Sie 
`nbins=5`, `nbins=20` und `nbins=50` aus. Was beobachten Sie? Welche 
Vor- und Nachteile haben wenige vs. viele Bins?
```

```{admonition} Lösung
:class: tip
:class: dropdown
* Mit `nbins=5` sind die Kategorien sehr breit - man erkennt nur grobe Muster.
* Mit `nbins=50` werden viele Kategorien leer oder haben nur wenige Werte - das
Diagramm wird unübersichtlich.
* Mit `nbins=10` bis `nbins=20` entsteht ein guter Kompromiss: Die Verteilung
ist erkennbar, ohne dass das Diagramm überladen wirkt.
```

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
zur Visualisierung numerischer Daten. Im nächsten Kapitel widmen wir uns dem
Thema Datenfilterung.
