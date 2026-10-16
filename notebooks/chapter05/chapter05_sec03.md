---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 5.3 Barplots und Histogramme

Barplots (Balken- oder Säulendiagramme) sind die am häufigsten verwendeten
Visualisierungen für kategoriale Daten. In diesem Kapitel lernen wir, wie mit
Plotly ein Barplot erstellt und von einem Histogramm unterschieden wird.

## Barplots

In den letzten Kapiteln haben wir uns mit kategorialen (qualitativen) Daten
auseinandergesetzt. Um kategoriale Daten zu visualisieren und zu vergleichen,
eignet sich besonders der **Barplot**.

Bei der Visualisierung werden prinzipiell zwei Varianten unterschieden. Zum
einen können die Kategorien entlang der x-Achse aneinandergereiht werden. Die
Höhe der Rechtecke repräsentiert dann den Zahlenwert dieser Kategorie. Da die
Rechtecke an Säulen erinnern, wird diese Variante **Säulendiagramm** genannt.
Die andere Möglichkeit ist, die Kategorien untereinander entlang der y-Achse
aufzuführen. Dann ist die Länge der Rechtecke repräsentativ für den Zahlenwert
dieser Kategorie. Diese Variante wird **Balkendiagramm** genannt.

## Was ist ... ein Barplot?

Ein Barplot ist ein Diagramm, das numerische Werte für verschiedene Kategorien 
visualisiert. Jede Kategorie wird durch die Höhe oder Länge eines Rechtecks 
repräsentiert, das den zugehörigen numerischen Wert darstellt.

Probieren wir Barplots am Beispiel der schon bekannten
AutoScout24-Verkaufspreise (siehe `autoscout24_DE_2020.csv`) für Autos aus.
Zuerst laden wir die Daten und verschaffen uns einen Überblick.

```{code-cell} python
import pandas as pd

data = pd.read_csv('autoscout24_DE_2020.csv')
data.info()
```

Mit der Methode `.value_counts()` lassen wir Python die Anzahl der Autos pro
Marke bestimmen.

```{code-cell} python
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

```{code-cell} python
import plotly.express as px

print('Säulendiagramm')
saeulendiagramm = # TODO: ???  (Säulendiagramm der Anzahl pro Marke erzeugen)
saeulendiagramm.show()

print('Balkendiagramm')
balkendiagramm = # TODO: ???  (Balkendiagramm der Anzahl pro Marke erzeugen)
balkendiagramm.show()
```

Obwohl Plotly Express bereits eine ansprechende Visualisierung bietet, könnten
die automatisch generierten Beschriftungen "value", "variable" und "count"
verbessert werden. Außerdem sollte ein Diagrammtitel hinzugefügt werden. Der
Titel kann direkt in der `bar()`-Funktion über das `title=` Argument gesetzt
werden. Für die Achsenbeschriftungen verwenden wir die Funktion
`update_layout()`. Die Argumente `xaxis_title=` und `yaxis_title=` modifizieren
die Beschriftung der x- und y-Achse. Die automatisch erzeugte Legende zeigt hier
nur einen einzigen, redundanten Eintrag und liefert keinen zusätzlichen
Informationsgewinn. Mit `showlegend=False` blenden wir sie aus.

```{code-cell} python
fig = px.bar(anzahl_pro_marke, title='AutoScout24 (Zulassungsjahr 2020)')
fig.update_layout(
    xaxis_title='Marke',
    # TODO: ???  (y-Achse mit Anzahl Autos beschriften)
    showlegend=False,
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

```{code-cell} python
kilometerstaende = data['Kilometerstand (km)'].unique()
anzahl_kilometerstaende = len(kilometerstaende)
print(f'Es gibt {anzahl_kilometerstaende} verschiedene Kilometerstände.')
```

Mit über 10 000 verschiedenen Kilometerständen wäre eine direkte Visualisierung
nicht zielführend. Um dennoch eine sinnvolle Analyse durchzuführen, können wir
den Bereich der Kilometerstände in Intervalle einteilen. Dazu bestimmen wir das
Minimum und das Maximum der Kilometerstände.

```{code-cell} python
minimaler_kilometerstand = data['Kilometerstand (km)'].min()
maximaler_kilometerstand = data['Kilometerstand (km)'].max()

print(f'minimaler Kilometerstand: {minimaler_kilometerstand}')
print(f'maximaler Kilometerstand: {maximaler_kilometerstand}')
```

Die Daten reichen von Neuwagen (minimaler Kilometerstand 0 km) bis zu Autos mit
hohem Kilometerstand (maximaler Kilometerstand 435 909 km). Wir können diesen
Bereich in Intervalle unterteilen, um zu zählen, wie viele Autos in welches
Intervall fallen. Die Intervallgrenzen von Hand zu berechnen, indem wir die
Spannweite einfach durch die gewünschte Anzahl an Intervallen teilen, wäre
mühsam und würde selten auf runde Zahlen führen. Tatsächlich brauchen wir das
nicht, denn diese Funktionalität ist bereits in der `histogram()`-Funktion
integriert, die auch die Visualisierung übernimmt.

Wir übergeben der Funktion die Daten als erstes Argument. Als optionales zweites
Argument können wir die gewünschte Anzahl an Intervallen übergeben. Die
gewählten Intervalle werden auch als Bins bezeichnet. Daher lautet das Argument
zum Setzen der Anzahl der Bins `nbins=`, so wie der englische Begriff »number of
bins«. Plotly wählt dabei automatisch runde Intervallgrenzen in der Nähe der
gewünschten Anzahl, sodass die tatsächlich angezeigte Anzahl an Intervallen von
`nbins=` leicht abweichen kann.

```{code-cell} python
fig = px.histogram(data['Kilometerstand (km)'],
    # TODO: ???  (Anzahl der Intervalle auf 10 setzen)
    title='Histogramm des Kilometerstandes (km)')
fig.update_layout(
    xaxis_title='Intervalle der Kilometerstände (km)',
    yaxis_title='Anzahl Autos',
    showlegend=False,
)
fig.show()
```

Die meisten Autos haben weniger als 200 000 km auf dem Kilometerzähler. Das
Histogramm zeigt eine hohe Häufigkeit bei niedrigen Kilometerständen und
deutlich weniger Fahrzeuge bei sehr hohen Kilometerständen. Die Verteilung ist
damit rechtsschief: Viele Fahrzeuge liegen im unteren Wertebereich, während
wenige Fahrzeuge sehr hohe Kilometerstände aufweisen.

Die Anzahl der Bins ist ein sehr wichtiger Faktor bei der Visualisierung. Werden
zu wenige Bins gewählt, werden Unterschiede nicht sichtbar. Werden zu viele Bins
gewählt, können einzelne Bins leer bleiben oder nur wenige Datenpunkte
enthalten. Dadurch können zufällige Schwankungen stärker hervortreten und die
Verteilung schwerer interpretierbar werden.

Zusammenfassend wird ein Histogramm folgendermaßen beschrieben.

## Was ist ... ein Histogramm?

Ein Histogramm ist eine grafische Darstellung der Häufigkeitsverteilung 
numerischer Daten. Dabei wird der Wertebereich in gleich große Intervalle 
(sogenannte Bins oder Klassen) eingeteilt. Die Höhe jeder Säule zeigt, wie 
viele Datenpunkte in das jeweilige Intervall fallen. Ein charakteristisches 
Merkmal: Die Säulen liegen ohne Lücken aneinander, da sie eine kontinuierliche 
Skala repräsentieren.

## Wann Barplot, wann Histogramm?

Wir nutzen einen *Barplot*, wenn wir kategoriale Daten wie die Automarke
darstellen wollen. Für numerische Daten wie den Kilometerstand, die wir dafür
in Intervalle einteilen, verwenden wir stattdessen ein *Histogramm*.

| Frage | Diagrammtyp | Beispiel |
| --- | --- | --- |
| Wie oft kommt jede Marke vor? | Barplot | `px.bar(anzahl_pro_marke)` |
| Verteilung der Kilometerstände? | Histogramm | `px.histogram(..., nbins=10)` |

## Zusammenfassung und Ausblick

In diesem Kapitel wurden zwei wichtige Diagrammtypen vorgestellt: der Barplot
und das Histogramm. Obwohl beide mit Rechtecken arbeiten, haben sie
unterschiedliche Anwendungsbereiche und sollten nicht verwechselt werden.
Während der Barplot ideal für kategoriale Daten ist, eignet sich das Histogramm
zur Visualisierung numerischer Daten. Damit schließen wir die Kapitel zur
Datenexploration ab. Im nächsten Kapitel beginnt der Teil zum maschinellen
Lernen mit den Entscheidungsbäumen.

## Mini-Übungen

### Mini-Übung 1

Verwenden Sie den Datensatz `3ddruck_xxs.csv` (mit Nummer als Zeilenindex).

1. Lesen Sie die Datei ein.
2. Ermitteln Sie, wie oft jedes Material im Datensatz vorkommt.
3. Visualisieren Sie die Verteilung der Materialien als Säulendiagramm.
   Vergeben Sie einen Titel sowie sinnvolle Achsenbeschriftungen.

```{code-cell}
# Code-Zelle
```

### Mini-Übung 2

Verwenden Sie den Datensatz `3ddruck_xxs.csv` (mit Nummer als Zeilenindex).

1. Lesen Sie die Datei ein.
2. Visualisieren Sie die Verteilung der Spalte `Zugfestigkeit (MPa)` als
   Histogramm mit 3 Intervallen.
3. Probieren Sie anschließend 5 und 10 Intervalle aus. Was beobachten Sie
   bei 10 Intervallen? Woran liegt das, wenn Sie an die Anzahl der
   Druckversuche in diesem Datensatz denken?

```{code-cell}
# Code-Zelle
```
