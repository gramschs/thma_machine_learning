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

# 4.3 Scatterplots und Scattermatrix

Bei der Datenvisualisierung geht es darum, Daten durch eine Grafik so
aufzubereiten, dass Muster oder Unregelmäßigkeiten in den Daten entdeckt werden
können. Dabei kann die visuelle Darstellung der Daten helfen, Muster in den
Daten zu entdecken, aber sie kann auch irreführend sein. Abhängig davon, wie die
Art der Daten beschaffen ist, die wir visualisieren wollen, gibt es verschiedene
Darstellungsformen, die sogenannten **Diagrammtypen**. Im Folgenden betrachten wir
die Diagrammtypen

* Scatterplot und
* Scattermatrix.

Danach beschäftigen wir uns mit der Gestaltung bzw. dem Styling von Diagrammen.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können mit der Funktion **scatter()** einen **Scatterplot** erzeugen, der
  numerische Daten als Ursache-Wirkungs-Diagramm visualisiert.
* Sie kennen die folgenden Styling-Optionen 
  * Textannotation **text=**, 
  * Farbe **color=** und
  * Größe **size=**.
* Sie können mit **title=** den Titel des Diagramms setzen.
* Sie können eine **Scattermatrix** mit **scatter_matrix()** erzeugen und
  interpretieren. 
```

## Scatterplots

Scatterplots (deutsch: Streudiagramme) werden eingesetzt, wenn der Zusammenhang
zwischen zwei numerischen Größen untersucht werden soll. Das ist vor allem bei
Experimenten häufig der Fall.

Im Folgenden soll der Scatterplot anhand des Autoscout24-Beispiels
{download}`Download autoscout24_xxs.csv
<https://gramschs.github.io/book_ml4ing/data/autoscout24_xxs.csv>` demonstriert
werden. Dazu laden wir die Tabelle wie üblich mit Pandas.

```{code-cell}
import pandas as pd
daten = pd.read_csv('autoscout24_xxs.csv', index_col=0)
daten.info()
```

Uns interessieren zunächst die Verkaufspreise der Autos. Zu jedem Auto soll
entlang der y-Achse der Verkaufspreis aufgetragen werden. Dazu wird zuerst
Plotly Express mit der üblichen Abkürzung px importiert. Danach nutzen wir die
Funktion `scatter()`. Das erste Argument in den runden Klammern ist die
komplette Tabelle, also `daten`. Danach geben wir direkt den Spaltenindex der
Spalte an, die visualisiert werden soll, also `y = 'Preis (Euro)'`. Zuletzt
lassen wir den Scatterplot auch mit `.show()` anzeigen.

```{code-cell}
import plotly.express as px
diagramm = px.scatter(daten, y = 'Preis (Euro)')
diagramm.show()
```

Da wir für die x-Achse keine Angaben gemacht haben, wird automatisch der
Zeilenindex für die x-Achse verwendet.

Der Scatterplot bietet im Vergleich zum Boxplot weitere Informationen.
Beispielsweise erkennen wir nun, dass die Autos der Marke Citroën eher unter dem
Durchschnitt liegen. Scatterplots bieten uns auch die Möglichkeit, Muster zu
visuell zu erkunden, um Abhängigkeiten von Ursache und Wirkung zu erkunden. Wir
könnten beispielsweise auf die Idee kommen, dass der Preis (= Wirkung) auch
abhängig ist von der Anzahl der gefahrenen Kilometer (= Ursache). Wir setzen die
vermutete Ursache auf die x-Achse mit dem Argument `x = 'Kilometerstand (km)'`
und die vermutete Wirkung auf die y-Achse mit `y = 'Preis (Euro)'`.

```{code-cell}
diagramm = px.scatter(daten, x = 'Kilometerstand (km)', y = 'Preis (Euro)')
diagramm.show()
```

Von der Tendenz her scheint unsere Vermutung richtig zu sein. Je mehr Kilometer
ein Auto bereits gefahren wurde, desto günstiger ist sein Verkaufspreis.
Allerdings scheint es zwei Autos zu geben, die nicht ganz in dieses Muster
passen. Ein Auto wird trotz eines Kilometerstandes von 117433 km für 46 TEUR
angeboten, an anderes hat nur 15200 km auf dem Buckel, soll aber trotzdem für
nur 12 TEUR verkauft werden. Aber welche Autos sind die beiden Ausnahmen? Um
mehr Informationen aus den Daten zu holen, beschäftigen wir uns mit dem Styling
von Scatterplots.

## Styling von Scatterplots

Die Voreinstellungen von Plotly sind bereits sehr gut gewählt, so dass ohne
weitere Optionen bereits gut aussehende und informative Diagramme erstellt
werden können. Eine Möglichkeit, durch das Styling der Diagramme
Zusatzinformationen zu visualisieren, bietet die Option `text=`. Wir verwenden
den Zeilenindex als Text, der in dem Attribut `.index` gespeichert ist.

```{code-cell}
diagramm = px.scatter(daten, x = 'Kilometerstand (km)', y = 'Preis (Euro)', text=daten.index)
diagramm.show()
```

An jedem Datenpunkt wird nun zusätzlich die Auto-ID eingeblendet. Leider
überschreibt der Text den Datenpunkt selbst. Das kann nachträglich geändert
werden, indem die Textposition relativ zu den Datenpunkten auf einen anderen
Wert gesetzt wird. Die einzelnen Bestandteile eines Plotly-Express-Diagramms
heißen **trace**. Sie werden durch `update_traces()` aktualisiert oder anders
ausgedrückt, die Voreinstellungen werden dadurch überschrieben. Wir möchten,
dass die Position der Texte oberhalb der Datenpunkte ist, aber dennoch zentriert
zum Datenpunkt. Durch das Argument `textposition='top center'` erreichen wir
dieses Ziel, wie der folgende Scatterplot zeigt.

```{code-cell}
diagramm = px.scatter(daten, x = 'Kilometerstand (km)', y = 'Preis (Euro)', text=daten.index)
diagramm.update_traces(textposition='top center')
diagramm.show()
```

Als nächstes möchten wir weitere Zusatzinformationen in das Diagramm packen.
Nicht immer ist es sinnvoll, so viele Zusatzinformationen in ein Diagramm zu
bringen, da damit das Publikum auch schnell überfordert werden kann. Daher
sollte gut überlegt werden, ob die beiden nächsten Möglichkeiten gleichzeitig
genutzt werden sollen.  

Die Farbe ist eine weitere Möglichkeit, Zusatzinformationen zu visualisieren.
Wie alt ist ein Auto? Hat es ebenfalls einen Einfluss auf den Verkaufspreis? Wir
nutzen das Jahr der Erstzulassung, um das Alter der Autos abzuschätzen. Die
Anweisung an Python, die Punkte des Scatterplots nach der Erstzulassung
einzufärben, wird durch das optionale Argument `color='Jahr'` gegeben.

```{code-cell}
diagramm = px.scatter(daten, x = 'Kilometerstand (km)', y = 'Preis (Euro)', text=daten.index, color='Jahr')
diagramm.update_traces(textposition='top center')
diagramm.show()
```

Die Farbe scheint links gelber zu sein als rechts, wo Auto 'Audi Nr. 1' violett
gefärbt ist. Also scheint das Jahr der Erstzulassung und damit das Alter der
Fahrzeuge auch etwas mit dem Kilometerstand zu tun zu haben, der auf der x-Achse
aufgetragen ist. Je jünger das Fahrzeug ist, desto weniger Kilomter wurde es
bisher gefahren.

Als zweite Möglichkeit, Zusatzinformationen direkt mit den Datenpunkten im
Scatterplot zu visualisieren, dient die Größe der Punkte. Mit dem optionalen
Argument `size=` wird sie gesteuert. Wiederum verwenden wir einen Spaltenindex
als Argument. Die Leistung könnte erfahrungsgemäß ebenfalls den Verkaufspreis
beeinflussen. Also setzen wir `size='Leistung (PS)'` und betrachten das so
erweiterte Diagramm.

```{code-cell}
diagramm = px.scatter(daten, x = 'Kilometerstand (km)', y = 'Preis (Euro)', text=daten.index, color='Jahr', size='Leistung (PS)')
diagramm.update_traces(textposition='top center')
diagramm.show()
```

Das Auto 'BMW Nr. 1', das uns schon zuvor aufgefallen ist, weil der Preis recht
hoch ist, obwohl das Auto schon einen mittleren Kilomterstand hat, scheint
besonders viel PS zu haben. Vielleicht erklärt das den hohen Preis?

Als letzte Styling-Möglichkeit betrachten wir den Titel. Im Gegensatz zu den
vorherigen Styling-Möglichkeiten, ist der Titel stets Pflicht. **Jedes Diagramm
muss einen Titel haben!** Der Titel wird mit dem Argument `title=` gesetzt.

```{code-cell}
diagramm = px.scatter(daten, x = 'Kilometerstand (km)', y = 'Preis (Euro)', text=daten.index, color='Jahr', size='Leistung (PS)', title='Verkaufsdaten von 10 Autos (Quelle: Autocout24.de)')
diagramm.update_traces(textposition='top center')
diagramm.show()
```

## Scattermatrix

Unsere Tabelle hat sieben Spalten mit numerischen Werten: Jahr, Preis (Euro),
Leistung (kW), Leistung (PS), Verbrauch (l/100 km), Verbrauch (g/km) und
Kilometerstand (km). Damit können sieben Eigenschaften als Ursache interpretiert
werden und auf der x-Achse aufgetragen werden. Zu jeder dieser sieben
Eigenschaften können dann die verbleibenden sechs Eigenschaften als Wirkung
interpretiert werden und auf der y-Achse dargestellt werden. Also müssten wir 42
Scatterplots untersuchen. Die Scattermatrix vereinfacht das Zusammenstellen
dieser Kombinationen. Dazu legen wir erst eine Liste mit den Spaltenindizes an,
die in die Scattermatrix aufgenommen werden sollen. Danach erzeugen wir mit der
Funktion `scatter_matrix()` die gewünschten Kombinationen. Als erstes Argument
werden die Daten aus der Tabelle übergeben, dann folgt die Liste der
ausgewählten Spalten als Argument für den Parameter `dimensions=`.

```{code-cell}
auswahl = ['Jahr', 'Preis (Euro)', 'Leistung (kW)', 'Leistung (PS)', 'Verbrauch (l/100 km)', 'Verbrauch (g/km)', 'Kilometerstand (km)']
diagramm = px.scatter_matrix(daten, dimensions=auswahl)
diagramm.show()
```

Es werden 49 Diagramme angezeigt, die allerdings kaum lesbar sind. Warum 49 und
nicht 42? Tatsächlich wird auch jede Eigenschaft als Ursache mit ihrer Wirkung
auf sich selbst dargestellt. Da das Diagramm so kaum lesbar ist, reduzieren wir
die Auswahl weiter und nehmen nur die ersten vier Eigenschaften.

```{code-cell}
auswahl = ['Jahr', 'Preis (Euro)', 'Leistung (kW)', 'Leistung (PS)']
diagramm = px.scatter_matrix(daten, dimensions=auswahl)
diagramm.show()
```

Auf der Diagonalen befinden sich die Scatterplots, bei denen dieselbe
Eigenschaft auf der x- und auf der y-Achse aufgetragen ist. Daher müssen diese
Punkte immer auf der Winkelhalbierenden liegen. Diese Darstellung zeigt uns
schnell, dass die Auswahl der Autos nicht gleichmäßig bezogen auf das Jahr der
Erstzulassung erfolgt ist. Im Scatterplot Jahr - Jahr ist ein Punkt (1997) sehr
weit von den restlichen Autos entfernt. Beim Preis hingegen sieht es besser aus,
diese Punkte sind entlang der Winkelhalbierenden relativ gleichmäßig verteilt.
Allerdings zeigen beide Scatterplots für die Leistung wiederum, dass ein Auto
(kW = 294 bzw. PS = 400) von den anderen Autos entfern ist. Bei beiden Autos
könnte man argumentieren, dass sie nicht repräsentativ für den Datensatz sind,
sondern als Ausreißer betrachtet werden müssen. Es stellt sich die Frage, ob sie
für die weitere Datenverarbeitung aus dem Datensatz gelöscht werden sollen.  

Betrachten wir den Scatterplot Leistung (kW) vs. Leistung (PS), so stellen wir
fest, dass die Punkte ebenfalls auf der Winkelhalbierenden liegen. Tatsächlich
ist das nicht verwunderlich, da die Leistung ja nur eine einzige Eigenschaft
darstellt, aber in zwei verschiedenen Einheiten angegeben wird. 1 Watt (W) sind
ungefähr 0,00136 Pferdestärken (PS). Die Scattermatrix zeigt uns nun (wenn wir
es nicht schon vorher wussten), dass wir nur eine der beiden Spalten brauchen.
Diese Spalte könnte für die weitere Datenexploration gelöscht werden.

```{code-cell}
auswahl = ['Jahr', 'Preis (Euro)', 'Leistung (kW)']
diagramm = px.scatter_matrix(daten, dimensions=auswahl)
diagramm.show()
```

Als letztes Interpretationsbeispiel betrachten wir die zweite Zeile der Matrix,
wo der Preis (Euro) auf der y-Achse aufgetragen ist. Betrachten wir den ersten
Scatterplot der zweiten Zeile, so scheint das Jahr keinen besonderen Einfluss
auf den Verkaufspreis zu haben. Beim dritten Scatterplot in der zweiten Zeile,
scheint es aber ein Muster zu geben. Mit wachsender Leistung scheint auch der
Verkaufspreis zu steigen. Die Scattermatrix hilft also gerade zu Beginn der
Datenexploration schnell, interessante Zusammenhänge zwischen einzelnen
Eigenschaften aufzudecken, die dann durch einzelne Scatterplots näher untersucht
werden können.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir uns mit der Visualisierung von numerischen Werten
beschäftigt. Die Scattermatrix ordnet alle Kombinationen von einzelnen
Scatterplots in einer Matrix an. Damit können schnell Muster in den Daten
gefunden werden, deren Abhängigkeiten dann wiederum durch einzelne Scatterplots
detaillierter beleuchtet werden können. Bisher haben wir aber nur die
numerischen Werte untersucht. Wie auch die nicht-numerischen Werte wie
beispielsweise die Farbe der Autos mit in die Visualisierung einbezogen werden
können, sehen wir im nächsten Kapitel.
