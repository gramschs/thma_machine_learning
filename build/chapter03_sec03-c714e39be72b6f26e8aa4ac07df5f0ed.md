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
Zum Schluss lernen wir, was ein Ausreißer ist und wie wir Ausreißer mit der
booleschen Indizierung aus dem letzten Kapitel aus den Daten herausfiltern.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie berechnen statistische Kennzahlen einer Series mit **.mean()**,
  **.std()**, **.min()**, **.max()**, **.quantile()** und **.describe()**.
* [ ] Sie erstellen mit **.box()** aus Plotly Express einen Boxplot für eine
  Series.
* [ ] Sie interpretieren die Elemente eines Boxplots (**Median**, **Quartile**,
  **Whisker**, **Ausreißer**) und ordnen ihnen die entsprechenden statistischen
  Kennzahlen zu, inklusive der IQR-Regel zur Ausreißerdefinition.
* [ ] Sie filtern Ausreißer aus einer Series mithilfe **boolescher Indizierung**
  basierend auf der IQR-Regel heraus.
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
statistische_kennzahlen = preise.describe()
```

Zur Kontrolle lassen wir uns den Inhalt der Variablen ausgeben:

```{code-cell} ipython3
statistische_kennzahlen
```

Zusätzlich können wir mit `type()` prüfen, welchen Datentyp dieses Ergebnis hat:

```{code-cell} ipython3
type(statistische_kennzahlen)
```

Das Ergebnis ist ein Series-Objekt von Pandas. Die Namen der Kennzahlen wie
`'mean'`, `'std'`, `'min'` und `'max'` bilden dabei den Index dieser Series.
Deshalb können wir auf einzelne Kennzahlen genauso zugreifen wie auf andere
Elemente einer Series, also über den Index in eckigen Klammern.

Zum Beispiel erhalten wir so den kleinsten Verkaufspreis:

```{code-cell} ipython3
minimaler_preis = statistische_kennzahlen['min']
print(f'Das billigste Auto wird für {minimaler_preis} EUR angeboten.')
```

Neben der Möglichkeit, die statistischen Kennzahlen über `.describe()` berechnen
zu lassen und dann mit dem expliziten Index darauf zuzugreifen, gibt es auch
Methoden, um die statistischen Kennzahlen direkt zu ermitteln.

Der Mittelwert ist die Summe aller Elemente geteilt durch ihre Anzahl.
Mittelwert heißt auf Englisch mean, daher ist es nicht verwunderlich, dass die
Methode `.mean()` den Mittelwert berechnet. Die Methoden `.std()`
(Standardabweichung, englisch standard deviation), `.min()` und `.max()` sind
fast schon selbsterklärend:

```{code-cell} ipython3
print(f'Mittelwert: {preise.mean()} EUR')
print(f'Standardabweichung: {preise.std():.2f} EUR')
print(f'Minimum: {preise.min()} EUR')
print(f'Maximum: {preise.max()} EUR')
```

Der Mittelwert ist wichtig, aber er erzählt nicht die ganze Geschichte. Die
Spanne zwischen dem billigsten Auto (1999 EUR) und dem teuersten Auto (46830
EUR) beträgt über 44.000 EUR. Diese Autos sind also sehr unterschiedlich! Die
**Standardabweichung** beschreibt die typische Abweichung vom Mittelwert in
einer einzigen Zahl.

Was bedeutet das konkret? Eine Standardabweichung von rund 12.700 EUR bei einem
Mittelwert von rund 21.500 EUR bedeutet: Die Preise schwanken stark. Wenn wir
ein "durchschnittliches" Auto für 21.500 EUR erwarten, müssen wir mit
Abweichungen von ±12.700 EUR rechnen.

Schauen wir uns das an unseren konkreten Daten an:

* Mittelwert ± Standardabweichung = 21.469 ± 12.687 EUR
* Das ergibt den Bereich: [8.783 EUR, 34.156 EUR].
* Tatsächlich liegen 7 von 10 Autos in diesem Bereich.

Die Standardabweichung hat dieselbe Einheit wie die Originaldaten (hier: EUR).
Das macht sie direkt interpretierbar im Gegensatz zur Varianz, die in EUR²
gemessen wird.

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

In der Ausgabe von `.describe()` sind uns außerdem die Zeilen `25%`, `50%` und
`75%` aufgefallen. Diese Kennzahlen heißen **Quantile**. Das p-Quantil ist der
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

## Boxplots mit Plotly Express

Die wichtigsten statistischen Kennzahlen lassen sich mit einem Diagramm
visualisieren, dem **Boxplot**. Es gibt zahlreiche Python-Module zur
Visualisierung von Daten. In dieser Vorlesung verwenden wir **Plotly**, das im
Gegensatz zu anderen Bibliotheken wie Matplotlib interaktive Diagramme
erstellt. Mit **Plotly Express** steht uns eine einfach zu bedienende
Schnittstelle zur Erstellung verschiedenster Diagrammtypen zur Verfügung.

Üblicherweise wird Plotly Express als `px` abgekürzt.

```{code-cell} ipython3
import plotly.express as px
```

Sollte eine Fehlermeldung auftreten, kann Plotly mit `!pip install plotly` oder
`!conda install plotly` nachinstalliert werden.

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

Jetzt zahlt sich aus, dass wir die Quantile schon kennen. Der Kasten (Box) wird
durch das untere Quartil Q1 (das 25 % Quantil) und das obere Quartil Q3 (das
75 % Quantil) begrenzt. Oder anders formuliert: In der Box liegen 50 % aller
Datenpunkte. Der Median wird durch die horizontale Linie in der Box
dargestellt. Die Antennen (englisch Whisker) zeigen den Bereich der übrigen
Daten an. Bei unseren Daten endet die untere Antenne beim billigsten Auto
(1999 EUR). Die obere Antenne endet allerdings bei 35990 EUR und damit *nicht*
beim teuersten Auto. Warum das so ist, klären wir im nächsten Abschnitt.

```{dropdown} Video zu "Boxplot" von Datatab
<iframe width="560" height="315" src="https://www.youtube.com/embed/1I_ma7nvKQw" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
allowfullscreen></iframe>
```

```{admonition} Mini-Übung
:class: tip
Erstellen Sie einen Boxplot der Autopreise und beantworten Sie anhand des
Diagramms:

1. Was ist der Median (die mittlere Linie in der Box)?
2. Zwischen welchen beiden Werten liegen 50 % aller Autos?
3. Lassen Sie mit dem Parameter `points='all'` zusätzlich alle Datenpunkte
   links neben dem Boxplot anzeigen.

*Tipp: Bewegen Sie die Maus über die Box, um die genauen Werte zu sehen.*
```

```{code-cell} ipython3
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
diagramm = px.box(preise, points='all')
diagramm.show()
```

Antworten:
1. Der Median liegt bei 18.900 EUR.
2. 50 % der Autos liegen zwischen Q1 (14.667,50 EUR) und Q3 (26.079,75 EUR).
   Das sind genau die Werte, die auch `preise.quantile(0.25)` und
   `preise.quantile(0.75)` liefern.
3. Mit `points='all'` werden alle zehn Datenpunkte links neben dem Boxplot
   platziert.
````

## Ausreißer verstehen und herausfiltern

Neben `points='all'` gibt es noch eine zweite Option für den
`points=`-Parameter: Mit `points='outliers'` werden nur die sogenannten
**Ausreißer** angezeigt.

```{code-cell} ipython3
diagramm = px.box(preise, points='outliers')
diagramm.show()
```

Ein einzelner Punkt erscheint oberhalb der Antenne: BMW Nr. 1 mit 46830 EUR.
Das wirft zwei Fragen auf. Warum gilt ausgerechnet das teuerste Auto als
Ausreißer, das zweitteuerste (Audi Nr. 2 mit 35990 EUR) aber nicht? Und warum
endete die obere Antenne im letzten Abschnitt genau bei 35990 EUR? Um beides zu
klären, müssen wir definieren, was ein Ausreißer ist.

Die Box im Boxplot enthält 50 % aller Datenpunkte, denn sie ist durch das
untere Quartil Q1 und das obere Quartil Q3 begrenzt. Die Differenz zwischen Q1
und Q3, also IQR = Q3 - Q1, wird **Interquartilsabstand** (manchmal auch kurz
Quartilsabstand) genannt und mit **IQR** (englisch für Interquartile Range)
abgekürzt. In der Statistik werden Punkte als Ausreißer angesehen, die kleiner
als Q1 - 1.5 IQR oder größer als Q3 + 1.5 IQR sind. Dabei ist die Wahl des
Faktors 1.5 eine statistische Konvention, die sich in der Praxis bewährt hat.
Die Antennen des Boxplots reichen jeweils nur bis zum letzten Datenpunkt
*innerhalb* dieser Grenzen. Deshalb endete die obere Antenne bei 35990 EUR:
Das ist der größte Preis, der noch kein Ausreißer ist.

Rechnen wir die Grenzen mit der Methode `.quantile()` selbst nach:

```{code-cell} ipython3
q1 = preise.quantile(0.25)
q3 = preise.quantile(0.75)
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
nach unten keine Ausreißer geben. Die obere Grenze liegt bei 43198.125 EUR.
Jeder Preis darüber gilt als Ausreißer. Jetzt kommt die boolesche Indizierung
aus dem letzten Kapitel ins Spiel. Mit ihr filtern wir die Ausreißer heraus:

```{code-cell} ipython3
ausreisser = preise[preise > obere_grenze]
print(ausreisser)
```

Wie erwartet ist BMW Nr. 1 mit 46830 EUR der einzige Ausreißer. Genauso können
wir die Daten von den Ausreißern bereinigen, indem wir die Bedingung umdrehen
und alle Preise behalten, die kleiner oder gleich der oberen Grenze sind:

```{code-cell} ipython3
preise_bereinigt = preise[preise <= obere_grenze]
print(preise_bereinigt)
```

Eine Warnung zum Schluss: Ein Ausreißer ist nicht automatisch ein Fehler. Er
kann ein Tippfehler oder ein Sensordefekt sein, dann sollte er entfernt oder
korrigiert werden. Er kann aber auch ein echter, wichtiger Wert sein, hier zum
Beispiel ein tatsächlich sehr teures Auto. Bevor Ausreißer gelöscht werden,
sollte immer geprüft werden, wie sie entstanden sind. Beim maschinellen Lernen
kommen wir auf diese Frage zurück, denn Ausreißer können Modelle stark
verzerren.

## Aufgaben

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
