---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.1 Pandas Series

Aus der Qualitätssicherung kommt ein Messprotokoll: Zehn Wellen wurden auf einer
Drehmaschine gefertigt, der Solldurchmesser beträgt 20.0 mm. Für jede Welle
liegt der gemessene Ist-Durchmesser vor. Bevor wir entscheiden können, ob die
Charge in Ordnung ist, brauchen wir ein Werkzeug, das solche Messreihen
effizient verwaltet. Bisher haben wir Daten in Listen gespeichert. In dieser
Sektion lernen wir, warum Listen für Messreihen nicht ausreichen und wie die
Datenstruktur **Series** aus dem Python-Modul Pandas dieses Problem löst.

## Lernziele

```{admonition} Lernziele
:class: attention
- [ ] Sie können das Modul **Pandas** mit seiner üblichen Abkürzung **pd**
  importieren.
- [ ] Sie kennen die Pandas-Datenstruktur **Series**.
- [ ] Sie wissen, was ein **Index** ist.
- [ ] Sie können aus Listen ein Series-Objekt erzeugen und mit einem Index
  versehen.
- [ ] Sie können mit Series-Objekten rechnen.
- [ ] Sie können die Elemente eines Series-Objektes mit **sort_values()**
  aufsteigend und absteigend sortieren lassen.
```

## Die Datenstruktur Series

Einfache Listen reichen nicht aus, um größere Datenmengen effizient zu speichern
und zu analysieren. Listen haben mehrere Nachteile: Sie speichern keine
Information über den Datentyp ihrer Elemente, bieten keine Möglichkeit,
Metadaten wie beschreibende Labels zu hinterlegen, und sind bei großen
Datenmengen ineffizient. Dazu benutzen Data Scientists die Datenstrukturen
`Series` oder `DataFrame` aus dem Pandas-Modul. Dabei wird **Series** für
Datenreihen genommen. Damit sind Vektoren gemeint, wenn alle Elemente der
Datenreihe aus Zahlen bestehen, oder eindimensionale Arrays. Die Datenstruktur
**DataFrame** wiederum dient zum Speichern und Verarbeiten von tabellierten
Daten, also Matrizen, wenn alle Elemente Zahlen sind, oder zweidimensionale
Arrays.

Bereitgestellt werden beide Datenstrukturen vom **Modul** Pandas. Ein Modul ist
eine Sammlung von fertigem Python-Code zu einem bestimmten Thema, hier zur
Verarbeitung und Analyse von Daten. Es ist üblich, das Modul `pandas` mit der
Abkürzung `pd` zu importieren, damit wir nicht immer `pandas` schreiben müssen.
Ausführliche Beschreibungen aller Funktionen finden wir in der offiziellen
[Pandas-Dokumentation](https://pandas.pydata.org/docs/user_guide/index.html).

```{code-cell} python
import pandas as pd
```

Wir starten mit der Datenstruktur Series. Als Beispiel betrachten wir das
Messprotokoll aus der Qualitätssicherung: die gemessenen Ist-Durchmesser (in mm)
von zehn gefertigten Wellen mit dem Solldurchmesser 20.0 mm. Die Messwerte
kommen zunächst in eine Liste (erkennbar an den eckigen Klammern), aus der dann
ein Series-Objekt erzeugt wird.

```{code-cell} python
messwerte = [20.02, 19.98, 20.05, 19.97, 20.01, 20.00, 19.95, 20.08, 19.99, 20.03]
durchmesser = pd.Series(messwerte)
print(durchmesser)
```

Was ist aber jetzt der Vorteil von Pandas? Warum nicht einfach bei der Liste
bleiben? Der wichtigste Unterschied zwischen Liste und Series ist der **Index**.

Bei einer Liste werden Elemente über ihre Position angesprochen, der Index ist
immer eine Ganzzahl beginnend bei 0. Wenn bei einer Liste auf das dritte Element
zugegriffen werden soll, dann verwenden wir den Index 2 (zur Erinnerung: Python
zählt ab 0) und schreiben

```{code-cell} python
durchmesser_dritte_welle = messwerte[2]
print(f'Durchmesser der dritten Welle: {durchmesser_dritte_welle} mm')
```

Die Datenstruktur Series ermöglicht es aber, einen *expliziten Index* zu setzen.
Über den optionalen Parameter `index=` speichern wir als Zusatzinformation noch
ab, zu welcher Welle der Messwert gehört. Im Messprotokoll ist jede Welle mit
einer Prüfnummer versehen, W01 bis W10. Diesen Datensatz werden wir in den
folgenden Sektionen noch weiter vertiefen.

```{code-cell} python
wellen = ['W01', 'W02', 'W03', 'W04', 'W05', 'W06', 'W07', 'W08', 'W09', 'W10']
durchmesser = pd.Series(messwerte, index = wellen)
print(durchmesser)
```

Beim ersten Aufruf von `print(durchmesser)` wurden die Zahlen 0, 1, 2, usw.
ausgegeben, weil das Series-Objekt zu dem Zeitpunkt noch einen automatisch
generierten ganzzahligen Index hatte. Den expliziten Index nutzen wir jetzt, um
auf den Messwert der dritten Welle zuzugreifen. Die dritte Welle hat die
Prüfnummer `W03`. Wie bei Listen verwenden wir eckige Klammern:

```{code-cell} python
durchmesser_dritte_welle = durchmesser['W03']
print(f'Durchmesser der Welle W03: {durchmesser_dritte_welle} mm')
```

Die Datenstruktur Series hat gegenüber der Liste noch einen weiteren Vorteil. In
der Datenstruktur ist noch eine Zusatzinformation gespeichert, die Eigenschaft
`dtype`. Darin gespeichert ist der Datentyp der Elemente des Series-Objektes.
Auf diese Eigenschaft können wir direkt mit dem sogenannten Punktoperator
zugreifen.

```{code-cell} python
datentyp_durchmesser = durchmesser.dtype
print(f'Die einzelnen Elemente des Series-Objektes "durchmesser" haben den Datentyp {datentyp_durchmesser}.')
```

Offensichtlich sind die gespeicherten Werte Floats. Die Zusatzinformation
`float64` bedeutet, dass es sich um 64-Bit-Gleitkommazahlen handelt.

```{admonition} Mini-Übung
:class: tip
Erzeugen Sie ein Series-Objekt mit den Wochentagen als Index. Verwenden Sie
dabei nur die Werktage und speichern Sie, wie viele Stunden Sie an diesem Tag
schlafen. Welchen Datentyp haben die Elemente?
```

```{code-cell} python
# Hier Ihr Code:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
schlafzeiten = pd.Series([8, 9.5, 7.8, 8.1, 8.3],
  index=['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag'])
print(schlafzeiten)

print(f'Datentyp: {schlafzeiten.dtype}')
```
````

## Arbeiten mit Series-Objekten

Falls der Datentyp der einzelnen Elemente eines Series-Objektes ein numerischer
Typ ist (Integer oder Float), können wir mit den Einträgen auch rechnen. In der
Qualitätskontrolle interessiert uns weniger der absolute Durchmesser als die
**Abweichung vom Sollmaß**. Dazu subtrahieren wir von jedem Messwert den
Solldurchmesser 20.0 mm. Pandas führt die Subtraktion automatisch für alle
Elemente gleichzeitig aus.

```{code-cell} python
abweichung = durchmesser - 20.0
print(abweichung)
```

Die Abweichungen sind sehr kleine Zahlen. In der Fertigungsmesstechnik werden
solche Abweichungen üblicherweise in Mikrometern angegeben. Wir rechnen von
Millimetern in Mikrometer um, indem wir alle Elemente mit 1000 multiplizieren.

```{code-cell} python
abweichung_mikrometer = abweichung * 1000
print(abweichung_mikrometer)
```

Bei zehn Wellen war es relativ einfach, die größte Abweichung zu ermitteln,
indem wir einfach das Messprotokoll durchgeschaut haben. Hilfreicher ist es,
vorher die Werte aufsteigend oder absteigend zu sortieren. Dazu nutzen wir die
Methode `.sort_values()`. Der Name lässt vermuten, dass die Methode die Elemente
nach ihrem Wert sortiert.

```{code-cell} python
abweichung_aufsteigend = abweichung_mikrometer.sort_values()
print(abweichung_aufsteigend)
```

Jetzt zeigt sich auch der Vorteil des expliziten Index, denn auf die
ursprüngliche Reihenfolge kommt es nicht an. Der explizite Index ermöglicht uns,
jede Welle auch in der nach Abweichungen aufsteigend sortierten Messreihe
eindeutig wiederzufinden. Zum Abschluss sortieren wir noch absteigend. Mit dem
optionalen Argument `ascending` wird gesteuert, ob aufsteigend sortiert werden
soll oder nicht. Fehlt das Argument, so nimmt der Python-Interpreter an, dass
`ascending = True` gewünscht wird, also dass `aufsteigend = wahr` sein soll.
Wollen wir absteigend sortieren, müssen wir `aufsteigend = falsch` setzen, also
`ascending = False`.

```{code-cell} python
abweichung_absteigend = abweichung_mikrometer.sort_values(ascending = False)
print(abweichung_absteigend)
```

Die Welle mit der größten Abweichung nach oben steht jetzt am Anfang der
Ausgabe. Wir haben das sortierte Series-Objekt gleich in einer neuen Variable
abgespeichert. Das ist notwendig, wenn die neue Sortierung erhalten bleiben
soll. Standardmäßig wirkt der Sortierungsbefehl nämlich nur einmalig und ändert
die eigentliche Reihenfolge im Original nicht. Auch das lässt sich durch weitere
Parameter ändern (`inplace = True`), wie wir in der [Pandas-Dokumentation →
sort_values()](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_values.html)
nachlesen können.

```{admonition} Mini-Übung
:class: tip
Alice, Bob, Charlie und Dora sind 22, 20, 24 und 22 Jahre alt. Speichern Sie
diese Informationen in einem Series-Objekt und sortieren Sie von alt nach jung.
Zusatzfrage: Was fällt Ihnen bei der Sortierung auf, wenn zwei Personen gleich
alt sind? Bleibt ihre ursprüngliche Reihenfolge erhalten?
```

```{code-cell} python
# Hier Ihr Code:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Erzeugung des Series-Objektes
namen = ['Alice', 'Bob', 'Charlie', 'Dora']
alter = [22, 20, 24, 22]
personen = pd.Series(alter, index = namen)

# Sortierung und Ausgabe
personen_sortiert = personen.sort_values(ascending = False)
print(personen_sortiert)

# Beobachtung: Alice und Dora sind beide 22 Jahre alt.
# In der sortierten Ausgabe erscheint Dora vor Alice,
# obwohl Alice in der ursprünglichen Liste zuerst kam.
# Die Sortierung ist also nicht stabil. Die ursprüngliche
# Reihenfolge bei gleichen Werten wird nicht unbedingt erhalten.
```
````

## Aufgabe

```{admonition} Aufgabe: Bohrungen im Lagerbock
:class: tip
Aus der Fertigung kommt ein zweites Messprotokoll. In acht Lagerböcken wurde
jeweils eine Bohrung mit dem Solldurchmesser 8.5 mm gefertigt. Gemessen wurden
die Ist-Durchmesser 8.52, 8.47, 8.55, 8.49, 8.51, 8.44, 8.53 und 8.50 mm. Die
Prüfnummern lauten B01 bis B08.

1. Erzeugen Sie ein Series-Objekt mit den Prüfnummern als Index.
2. Berechnen Sie die Abweichung vom Sollmaß in Mikrometern.
3. Sortieren Sie die Abweichungen absteigend.
4. Welche Bohrung weicht am stärksten nach oben ab, welche am stärksten nach
   unten?

Zusatzfrage: Welche Bohrung hat die betragsmäßig größte Abweichung? Tipp:
Recherchieren Sie die Methode `.abs()`.
```

```{code-cell} python
# Hier Ihr Code:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# 1. Series-Objekt mit Prüfnummern als Index
bohrungen = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08']
messwerte_bohrungen = [8.52, 8.47, 8.55, 8.49, 8.51, 8.44, 8.53, 8.50]
durchmesser_bohrungen = pd.Series(messwerte_bohrungen, index = bohrungen)

# 2. Abweichung vom Sollmaß in Mikrometern
abweichung_bohrungen = (durchmesser_bohrungen - 8.5) * 1000

# 3. Absteigend sortieren
abweichung_sortiert = abweichung_bohrungen.sort_values(ascending = False)
print(abweichung_sortiert)

# 4. Am stärksten nach oben weicht B03 ab (+50 Mikrometer),
# am stärksten nach unten B06 (-60 Mikrometer).

# Zusatzfrage: Die Methode .abs() liefert die Beträge der Abweichungen.
betraege = abweichung_bohrungen.abs()
print(betraege.sort_values(ascending = False))
# Die betragsmäßig größte Abweichung hat B06 mit 60 Mikrometern.
```
````

## Zusammenfassung und Ausblick

In dieser Sektion haben wir die sehr wichtige Datenstruktur Series aus dem
Pandas-Modul kennengelernt. Am Beispiel des Messprotokolls haben wir Messreihen
mit einem expliziten Index versehen, Abweichungen vom Sollmaß berechnet und die
Werte sortiert. Bei zehn Wellen können wir Auffälligkeiten noch mit bloßem Auge
erkennen. Bei tausend Messwerten funktioniert das nicht mehr. In der nächsten
Sektion lassen wir Pandas deshalb die wichtigsten statistischen Kennzahlen der
Messreihe berechnen: Mittelwert, Standardabweichung, Minimum, Maximum und
Quantile.
