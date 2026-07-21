---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.3 Kennzahlen, Boxplots und Ausreißer

Pandas dient nicht nur dazu, Daten zu verwalten, sondern ermöglicht auch
statistische Analysen. Die deskriptive Statistik hat zum Ziel, Daten durch
einfache Kennzahlen und Diagramme zu beschreiben. In diesem Kapitel ermitteln
wir zuerst die wichtigsten statistischen Kennzahlen mit Pandas. Danach
visualisieren wir sie mit einem Diagramm, das Boxplot genannt wird.
Gelegentlich wird auch der deutsche Begriff Kastendiagramm dafür gebraucht.
Zum Schluss lernen wir, was ein Ausreißer ist und wie wir Ausreißer im Boxplot
anzeigen lassen.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie berechnen statistische Kennzahlen einer Series mit **.mean()**,
  **.std()**, **.min()**, **.max()**, **.quantile()** und **.describe()**.
* [ ] Sie erstellen mit **.box()** aus Plotly Express einen Boxplot für eine
  Series und beschriften ihn mit **labels=** und **title=**.
* [ ] Sie interpretieren die Elemente eines Boxplots (**Median**, **Quartile**,
  **Whisker**, **Ausreißer**) und ordnen ihnen die entsprechenden statistischen
  Kennzahlen zu, inklusive der IQR-Regel zur Ausreißerdefinition.
* [ ] Sie lassen mit **points='outliers'** die Ausreißer einer Series im Boxplot
  anzeigen und rechnen die Ausreißergrenzen mit **.quantile()** nach.
```

## Statistische Kennzahlen ermitteln

Die Methode `.describe()` aus dem Pandas-Modul (siehe
[Pandas-Dokumentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.describe.html))
liefert eine schnelle Übersicht über viele statistische Kennzahlen. Vor allem,
wenn neue Daten geladen werden, ist diese Methode oft ein guter erster Schritt.
Wir bleiben bei unserem Beispiel mit den zehn Autos und deren Verkaufspreisen.

```{code-cell} ipython3
# Import des Pandas-Moduls
import pandas as pd

# Erzeugung der Daten als Series-Objekt
preisliste = [1999, 35990, 17850, 46830, 27443, 14240, 19950, 15950, 21990, 12450]
autos = ['Audi Nr. 1', 'Audi Nr. 2', 'Audi Nr. 3', 'BMW Nr. 1', 'BMW Nr. 2', 'Citroen Nr. 1', 'Citroen Nr. 2', 'Citroen Nr. 3', 'Citroen Nr. 4', 'Citroen Nr. 5']
preise = pd.Series(preisliste, index=autos)
```

Die Methode `.describe()` zeigt nicht nur die statistischen Kennzahlen an,
sondern gibt sie auch als Ergebnis zurück. Dieses Ergebnis können wir in einer
Variablen zwischenspeichern und später weiterverwenden.

```{code-cell} ipython3
kennzahlen = preise.describe()
```

Zur Kontrolle lassen wir uns den Inhalt der Variablen ausgeben:

```{code-cell} ipython3
print(kennzahlen)
```

Zusätzlich können wir mit `type()` prüfen, welchen Datentyp dieses Ergebnis hat:

```{code-cell} ipython3
type(kennzahlen)
```

Das Ergebnis ist ein Series-Objekt von Pandas. Die Namen der Kennzahlen wie
`'min'` und `'max'` bilden dabei den Index dieser Series. Deshalb können wir auf
einzelne Kennzahlen genauso zugreifen wie auf andere Elemente einer Series, also
über den Index in eckigen Klammern.

Zum Beispiel erhalten wir so den kleinsten Verkaufspreis:

```{code-cell} ipython3
minimaler_preis = kennzahlen['min']
print(f'Das billigste Auto wird für {minimaler_preis} EUR angeboten.')
```

Neben der Möglichkeit, die statistischen Kennzahlen über `.describe()` berechnen
zu lassen und dann über den Index darauf zuzugreifen, gibt es auch direkt
anwendbare Methoden, um die statistischen Kennzahlen zu ermitteln.

Der **Mittelwert** (engl. Mean) wird mit `.mean()` berechnet. **Minimum** und
**Maximum** erhalten wir über die Methoden `.min()` und `.max()`.

```{code-cell} ipython3
print(f'Mittelwert: {preise.mean()} EUR')
print(f'Minimum: {preise.min()} EUR')
print(f'Maximum: {preise.max()} EUR')
```

Der Mittelwert ist wichtig, aber er erzählt nicht die ganze Geschichte. Die
Spanne zwischen dem billigsten Auto (1999 EUR) und dem teuersten Auto (46830
EUR) beträgt über 44000 EUR. Diese Autos sind also sehr unterschiedlich! Wie
sehr die Werte vom Mittelwert abweichen, beschreibt die **Standardabweichung**
(engl. Standard Deviation), die wir mit `.std()` bestimmen.

```{code-cell} ipython3
print(f'Standardabweichung: {preise.std():.2f} EUR')
```

Was bedeutet das konkret? Eine Standardabweichung von rund 12700 EUR bei einem
Mittelwert von rund 21500 EUR zeigt, dass die Preise stark streuen. Viele
Preise liegen in einer Größenordnung von etwa 12700 EUR um den Mittelwert,
einige aber auch deutlich weiter davon entfernt.

Die Standardabweichung hat dieselbe Einheit wie die Originaldaten (hier: EUR).
Das macht sie direkt interpretierbar im Gegensatz zur Varianz, die in EUR²
gemessen wird.

In der Ausgabe von `.describe()` sind uns außerdem die Zeilen `25%`, `50%` und
`75%` aufgefallen. Diese Kennzahlen heißen **Quantile**. Das $p$-Quantil ist der
Wert, unter dem $p\cdot 100\%$ der Daten liegen. Beim 0.5-Quantil liegen also
$50 \%$ der Werte darunter. Dieses Quantil heißt auch **Median**. Mit der
Methode `.quantile()` können wir diesen Wert leicht aus den Daten holen.

```{code-cell} ipython3
median = preise.quantile(0.5)
print(f'Der Median, d.h. das 0.5-Quantil, liegt bei {median} EUR.')
```

Der Median liegt bei 18900 EUR, d.h. 50 % aller Autos werden zu einem Preis
angeboten, der kleiner oder gleich 18900 EUR ist. Und 50 % aller Autos werden
teurer angeboten. Das 0.25- und das 0.75-Quantil werden uns gleich im Boxplot
wieder begegnen.

```{dropdown} Video zu "Mittelwert" von Datatab
<iframe width="560" height="315" src="https://www.youtube.com/embed/IKfsGPwACnU" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

```{dropdown} Video zu "Standardabweichung" von Datatab
<iframe width="560" height="315" src="https://www.youtube.com/embed/QNNt7BvmUJM" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

```{admonition} Mini-Übung
:class: tip
Arbeiten Sie mit der Series `preise` weiter.

1. Speichern Sie das Ergebnis von `.describe()` in einer Variablen und greifen
   Sie über den Index auf die Standardabweichung zu.
2. Berechnen Sie das 0.1-Quantil der Verkaufspreise. Wie interpretieren Sie
   diesen Wert?
3. Vergleichen Sie Mittelwert und Median der Verkaufspreise. Welcher Wert ist
   größer? Haben Sie eine Vermutung, woran das liegen könnte?
```

```{code-cell} ipython3
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# 1. describe() speichern und auf 'std' zugreifen
kennzahlen = preise.describe()
standardabweichung = kennzahlen['std']
print(f'Standardabweichung: {standardabweichung:.2f} EUR')

# 2. das 0.1-Quantil berechnen
quantil_10 = preise.quantile(0.1)
print(f'0.1-Quantil: {quantil_10} EUR')

# 3. Mittelwert und Median vergleichen
print(f'Mittelwert: {preise.mean()} EUR')
print(f'Median: {preise.quantile(0.5)} EUR')
```

Antworten:
1. Die Standardabweichung beträgt rund 12686.59 EUR. Der Zugriff erfolgt über
   den Index `'std'` in eckigen Klammern.
2. Das 0.1-Quantil liegt bei 11404.9 EUR, d.h. 10 % der Autos werden zu einem
   Preis von höchstens rund 11405 EUR angeboten. Der Wert muss dabei nicht
   selbst in den Daten vorkommen, Pandas interpoliert zwischen den
   Datenpunkten.
3. Der Mittelwert (21469.2 EUR) ist deutlich größer als der Median
   (18900 EUR). Das sehr teure Auto BMW Nr. 1 zieht den Mittelwert nach oben,
   während der Median davon unbeeindruckt bleibt. Der Median ist robust
   gegenüber extremen Werten. Solche extremen Werte schauen wir uns am Ende
   dieses Kapitels genauer an.
````

## Boxplots mit Plotly Express

Die wichtigsten statistischen Kennzahlen lassen sich mit dem **Boxplot**
visualisieren. Es gibt zahlreiche Python-Module zur Visualisierung von Daten. In
dieser Vorlesung verwenden wir **Plotly**, das im Gegensatz zu anderen
Bibliotheken wie Matplotlib interaktive Diagramme erstellt. Mit **Plotly
Express** steht uns eine einfach zu bedienende Schnittstelle zur Erstellung
verschiedenster Diagrammtypen zur Verfügung.

Üblicherweise wird Plotly Express als `px` abgekürzt.

```{code-cell} ipython3
import plotly.express as px
```

Um einen Boxplot zu erstellen, nutzen wir die Funktion `box()` von Plotly
Express. Wir speichern das Diagramm, das durch diese Funktion erstellt wird, in
der Variablen `diagramm`. Um es dann auch nach seiner Erzeugung tatsächlich
anzeigen zu lassen, verwenden wir die Methode `.show()`. Zusammen sieht der
Python-Code zur Erzeugung eines Boxplots folgendermaßen aus:

```{code-cell} ipython3
diagramm = px.box(preise)
diagramm.show()
```

Bewegen wir die Maus über dem Diagramm, sehen wir verschiedene interaktive
Funktionen:

* Hover-Informationen zeigen die genauen Werte an.
* Rechts oben erscheinen Buttons zum Zoomen, Verschieben und Herunterladen.
* Mit der Maus können wir in das Diagramm hineinzoomen.

Ein Schönheitsfehler fällt allerdings auf: Die Achsenbeschriftungen wurden
automatisch gesetzt. Die x-Achse ist mit `'variable'` und die y-Achse mit
`'value'` beschriftet. Darüber hinaus ist der Titel der Box `'0'`. Der Name wird
auch angezeigt, wenn wir die Maus über die Box bewegen. Die 0 erscheint, weil
Pandas intern 0 als Standardnamen verwendet, wenn beim Erzeugen der Series kein
Name angegeben wurde.

Sollen die Achsenbeschriftungen geändert werden, müssen die automatisch
gesetzten Beschriftungen durch neue Namen ersetzt werden. Dazu wird ein
Dictionary konfiguriert und dem optionalen Argument `labels=` übergeben. Das
Dictionary wird mit geschweiften Klammern erzeugt. Die Schlüssel vor dem
Doppelpunkt sind die alten Beschriftungen, die Werte nach dem Doppelpunkt die
neuen.

Da wir weiterhin den Variablennamen `diagramm` nutzen, wird das Diagramm aus der
vorherigen Code-Zelle überschrieben.

```{code-cell} ipython3
diagramm = px.box(preise,
                  labels={'variable': 'Autoscout24', 'value': 'Verkaufspreis [EUR]'})
diagramm.show()
```

Fehlt noch eine Überschrift, ein Titel. Wie das englische Wort 'title' heißt
auch das entsprechende Schlüsselwort zum Erzeugen eines Titels, nämlich
`title=`.

```{code-cell} ipython3
diagramm = px.box(preise,
                  labels={'variable': 'Autoscout24', 'value': 'Verkaufspreis [EUR]'},
                  title='Statistische Kennzahlen als Boxplot')
diagramm.show()
```

Kehren wir zur Interpretation des Boxplots zurück. Wofür steht eigentlich die
Box? Die Box zeigt uns die Quantile. Sie wird unten durch das 0.25-Quantil (auch
Q1-Quartil genannt) und oben durch das 0.75-Quantil (auch Q3-Quartil genannt)
begrenzt. Oder anders formuliert: In der Box liegen 50 % aller Datenpunkte. Der
Median wird durch die horizontale Linie in der Box dargestellt. Die Antennen
(englisch Whisker) zeigen den Bereich der übrigen Daten an.

```{dropdown} Video zu "Boxplot" von Datatab
<iframe width="560" height="315" src="https://www.youtube.com/embed/1I_ma7nvKQw" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
allowfullscreen></iframe>
```

## Ausreißer anzeigen

Oft ist es wünschenswert, die Rohdaten zusammen mit dem Boxplot zu
visualisieren. Das ist mit dem `points=`-Parameter recht einfach, jedoch haben
wir zwei mögliche Optionen. Wir können mit `'all'` alle Punkte anzeigen lassen
oder nur die **Ausreißer** `'outliers'`.

Lassen wir zuerst alle Punkte anzeigen und setzen also `points='all'`.

```{code-cell} ipython3
diagramm = px.box(preise,
                  labels={'variable': 'Autoscout24', 'value': 'Verkaufspreis [EUR]'},
                  title='Statistische Kennzahlen als Boxplot',
                  points='all')
diagramm.show()
```

Die Punkte werden links vom Boxplot platziert. Als Nächstes lassen wir uns die
Ausreißer anzeigen.

```{code-cell} ipython3
diagramm = px.box(preise,
labels={'variable': 'Autoscout24', 'value': 'Verkaufspreis [EUR]'},
title='Statistische Kennzahlen als Boxplot',
points='outliers')
diagramm.show()
```

Das Ergebnis wirkt zunächst enttäuschend: Es erscheint kein einziger Punkt. Die
Antennen reichen vom billigsten Auto (1999 EUR) bis zum teuersten Auto
(46830 EUR). Unter unseren zehn Autos gibt es also keinen Ausreißer. Damit wir
trotzdem sehen, wie ein Ausreißer im Boxplot aussieht, erweitern wir das
Angebot des Autohauses um einen Luxuswagen: einen Porsche für 98500 EUR. Dazu
kopieren wir die Series mit `.copy()` und fügen den Porsche über das neue Label
'Porsche Nr. 1' hinzu.

```{code-cell} ipython3
preise_neu = preise.copy()
preise_neu['Porsche Nr. 1'] = 98500
print(preise_neu)
```

Nun erstellen wir den Boxplot mit der erweiterten Series erneut:

```{code-cell} ipython3
diagramm = px.box(preise_neu,
labels={'variable': 'Autoscout24', 'value': 'Verkaufspreis [EUR]'},
title='Statistische Kennzahlen als Boxplot',
points='outliers')
diagramm.show()
```

Ein einzelner Punkt erscheint oberhalb der Antenne: Porsche Nr. 1 mit
98500 EUR. Das wirft zwei Fragen auf. Warum gilt der Porsche als Ausreißer,
das zweitteuerste Auto (BMW Nr. 1 mit 46830 EUR) aber nicht? Und warum endet
die obere Antenne beim BMW, obwohl der Porsche das teuerste Auto ist? Um
beides zu klären, müssen wir definieren, was ein Ausreißer ist.

Die Box im Boxplot enthält 50 % aller Datenpunkte, denn sie ist durch das
untere Quartil Q1 und das obere Quartil Q3 begrenzt. Die Differenz zwischen Q1
und Q3, also IQR = Q3 - Q1, wird **Interquartilsabstand** (manchmal auch kurz
Quartilsabstand) genannt und mit **IQR** (englisch für Interquartile Range)
abgekürzt. In der Statistik werden Punkte als Ausreißer angesehen, die kleiner
als Q1 - 1.5 IQR oder größer als Q3 + 1.5 IQR sind. Dabei ist die Wahl des
Faktors 1.5 eine statistische Konvention, die sich in der Praxis bewährt hat.
Die Antennen des Boxplots reichen jeweils nur bis zum letzten Datenpunkt
*innerhalb* dieser Grenzen. Deshalb endet die obere Antenne bei 46830 EUR:
Das ist der größte Preis, der noch kein Ausreißer ist.

Rechnen wir die Grenzen mit der Methode `.quantile()` selbst nach:

```{code-cell} ipython3
q1 = preise_neu.quantile(0.25)
q3 = preise_neu.quantile(0.75)
iqr = q3 - q1
print(f'Q1: {q1} EUR')
print(f'Q3: {q3} EUR')
print(f'IQR: {iqr} EUR')

untere_grenze = q1 - 1.5 * iqr
obere_grenze = q3 + 1.5 * iqr
print(f'Untere Grenze: {untere_grenze} EUR')
print(f'Obere Grenze: {obere_grenze} EUR')
```

Die untere Grenze ist negativ, negative Preise gibt es nicht, also kann es
nach unten keine Ausreißer geben. Die obere Grenze liegt bei 56648.75 EUR.
Jeder Preis darüber gilt als Ausreißer. Von unseren elf Autos liegt nur
Porsche Nr. 1 mit 98500 EUR über dieser Grenze. BMW Nr. 1 mit 46830 EUR bleibt
darunter und markiert deshalb das Ende der oberen Antenne. Damit sind beide
Fragen beantwortet.

```{admonition} Hinweis: Quartile sind Konventionssache
:class: note
Statistiksoftware berechnet Quartile nicht einheitlich, es gibt mehrere
gebräuchliche Rechenverfahren. Plotly verwendet eine etwas andere Konvention
als die Pandas-Methode `.quantile()`. Die Hover-Werte für Q1 und Q3 im Boxplot
können deshalb leicht von den selbst berechneten Werten abweichen. Liegt ein
Datenpunkt sehr nahe an einer Ausreißergrenze, kann er je nach Software einmal
als Ausreißer eingestuft werden und einmal nicht. An der Interpretation des
Boxplots ändert das nichts.
```

Eine Warnung zum Schluss: Ein Ausreißer ist nicht automatisch ein Fehler. Er
kann ein Tippfehler oder ein Sensordefekt sein, dann sollte er entfernt oder
korrigiert werden. Er kann aber auch ein echter, wichtiger Wert sein, hier zum
Beispiel ein tatsächlich sehr teures Auto. Bevor Ausreißer gelöscht werden,
sollte immer geprüft werden, wie sie entstanden sind. Beim maschinellen Lernen
kommen wir auf diese Frage zurück, denn Ausreißer können Modelle stark
verzerren.

Wie Ausreißer mit der booleschen Indizierung aus dem letzten Kapitel
tatsächlich aus den Daten herausgefiltert werden, sehen wir in Kapitel 5 an
einem echten Datensatz mit mehr als 18000 Autos.

<!-- ## Aufgaben

Zum Abschluss wenden wir alle Techniken dieses Kapitels in einer
zusammenhängenden Aufgabe an.

```{admonition} Aufgabe: Ausreißerjagd im Autohaus
:class: tip
Verwenden Sie die Series `preise` und `kilometerstand` aus diesem Kapitel.

1. Wenden Sie `.describe()` auf die Kilometerstände an. An welcher Kennzahl
   erkennen Sie, dass ein Wert fehlt?
2. Ersetzen Sie den fehlenden Kilometerstand mit `.fillna()` durch den
   Mittelwert. Vergleichen Sie Mittelwert und Standardabweichung vor und nach
   dem Ersetzen. Was fällt auf?
3. Berechnen Sie für die Verkaufspreise Q1, Q3, den Interquartilsabstand und
   die obere Ausreißergrenze. Filtern Sie die Ausreißer mit boolescher
   Indizierung heraus und erzeugen Sie eine bereinigte Series
   `preise_bereinigt` ohne die Ausreißer.
4. Erstellen Sie einen Boxplot von `preise_bereinigt` mit `points='outliers'`.
   Was beobachten Sie? Überlegen Sie: Was bedeutet Ihre Beobachtung für das
   blinde Entfernen von Ausreißern?
```

```{code-cell} ipython3
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Teilaufgabe 1: describe auf die Kilometerstände
print(kilometerstand.describe())
```

An der Kennzahl `count` erkennen wir den fehlenden Wert: Sie zeigt 9 statt 10,
denn `.describe()` ignoriert `NaN`-Einträge und rechnet nur mit den gültigen
Werten.

```python
# Teilaufgabe 2: fehlenden Wert ersetzen und Kennzahlen vergleichen
print(f'Mittelwert vorher: {kilometerstand.mean():.2f} km')
print(f'Standardabweichung vorher: {kilometerstand.std():.2f} km')

kilometerstand_gefuellt = kilometerstand.fillna(kilometerstand.mean())
print(f'Mittelwert nachher: {kilometerstand_gefuellt.mean():.2f} km')
print(f'Standardabweichung nachher: {kilometerstand_gefuellt.std():.2f} km')
```

Der Mittelwert bleibt exakt gleich (74188.89 km), denn wir haben ja genau den
Mittelwert eingesetzt. Die Standardabweichung wird dagegen kleiner (von
46713.37 auf 44041.78 km), weil der neue Wert genau in der Mitte liegt und
damit die Streuung rechnerisch verringert. Das ist ein bekannter Nebeneffekt
dieser Ersetzungsstrategie.

```python
# Teilaufgabe 3: Ausreißergrenze berechnen und filtern
q1 = preise.quantile(0.25)
q3 = preise.quantile(0.75)
iqr = q3 - q1
obere_grenze = q3 + 1.5 * iqr
print(f'Obere Ausreißergrenze: {obere_grenze} EUR')

ausreisser = preise[preise > obere_grenze]
print(ausreisser)

preise_bereinigt = preise[preise <= obere_grenze]
print(preise_bereinigt)
```

Die obere Grenze liegt bei 43198.125 EUR, einziger Ausreißer ist BMW Nr. 1 mit
46830 EUR. Die bereinigte Series enthält noch neun Autos.

```python
# Teilaufgabe 4: Boxplot der bereinigten Daten
diagramm = px.box(preise_bereinigt, points='outliers')
diagramm.show()
```

Überraschung: Es erscheint wieder ein Ausreißer, diesmal Audi Nr. 2 mit
35990 EUR! Durch das Entfernen von BMW Nr. 1 haben sich die Quartile
verschoben (Q1 = 14240 EUR, Q3 = 21990 EUR) und die obere Grenze liegt jetzt
bei nur noch 33615 EUR. Die 1.5-IQR-Regel ist eben relativ zu den Daten: Wer
Ausreißer entfernt und die Regel erneut anwendet, findet unter Umständen immer
wieder neue. Das zeigt, warum Ausreißer nicht blind und schon gar nicht
wiederholt entfernt werden sollten, sondern immer mit Blick auf ihre Ursache.
```` 
-->

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir gelernt, was die Daten uns erzählen. Die Methode
`.describe()` liefert die wichtigsten statistischen Kennzahlen auf einen
Blick, die auch einzeln über `.mean()`, `.std()`, `.min()`, `.max()` und
`.quantile()` berechnet werden können. Fehlende Werte spüren wir mit `.isna()`
auf und behandeln sie mit `.dropna()` oder `.fillna()`. Der Boxplot
visualisiert die Kennzahlen: Die Box reicht von Q1 bis Q3, die Linie darin ist
der Median, die Antennen zeigen den Bereich der übrigen Daten und Punkte
außerhalb sind Ausreißer nach der 1.5-IQR-Regel. Mit der booleschen
Indizierung haben wir diese Ausreißer schließlich aus den Daten
herausgefiltert. Die Stärke des Boxplots zeigt sich besonders, sobald mehrere
Datensätze miteinander verglichen werden sollen. Daher werden wir uns im
nächsten Kapitel mit Tabellen beschäftigen.
