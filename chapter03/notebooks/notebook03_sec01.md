---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.1 Pandas Series

Ein Autohaus bietet derzeit 10 Autos zum Verkauf an und wir wollen die
Verkaufspreise der Autos analysieren. Bisher haben wir Daten in Listen
gespeichert. In diesem Abschnitt lernen wir, warum Listen für Datenreihen nicht
ausreichen und wie die Datenstruktur **Series** aus dem Python-Modul Pandas
dieses Problem löst.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie kennen die Pandas-Datenstruktur **Series** und können erklären, worin
  sie sich von Python-Listen unterscheidet.
* [ ] Sie erzeugen eine Series aus einer **Liste** oder einem **Dictionary**.
* [ ] Sie vergeben beim Erzeugen einer Series einen eigenen **Index** und kennen
  den Default-Index.
* [ ] Sie fragen die Attribute **values**, **index**, **dtype** und **name**
  einer Series ab und interpretieren deren Bedeutung.
```

## Die Datenstruktur Series

Einfache Listen reichen nicht aus, um größere Datenmengen effizient zu speichern
und zu analysieren. Listen haben mehrere Nachteile: Sie erzwingen keinen
gemeinsamen Datentyp ihrer Elemente (in einer Liste dürfen Zahlen und Texte bunt
gemischt sein), sie bieten keine Möglichkeit, Metadaten wie beschreibende Labels
zu hinterlegen, und sie sind bei großen Datenmengen ineffizient. Data Scientists
benutzen daher die Datenstrukturen `Series` oder `DataFrame` aus dem
Pandas-Modul. Dabei wird **Series** für Datenreihen genommen, also für
eindimensionale Daten wie eine Messreihe oder eben unsere Verkaufspreise. Die
Datenstruktur **DataFrame** wiederum dient zum Speichern und Verarbeiten von
tabellierten Daten, also Tabellen mit Zeilen und Spalten.

Der entscheidende Unterschied zur Liste ist der **Index**: Bei einer Liste
werden die Elemente ausschließlich über ihre Position 0, 1, 2, ... angesprochen.
Eine Series erlaubt zusätzlich einen *expliziten Index* mit selbst gewählten
Beschriftungen, den sogenannten Labels. Wir können uns eine Series daher als
eine Kombination aus Liste und Dictionary vorstellen: Die Daten haben wie in
einer Liste eine feste Reihenfolge und gleichzeitig können wir wie bei einem
Dictionary über Labels auf sie zugreifen. Dazu kommt, dass eine Series anders
als eine Liste einen gemeinsamen Datentyp für alle Elemente erzwingt und dadurch
große Datenmengen deutlich effizienter verarbeiten kann.

Bereitgestellt werden die Datenstrukturen Series und DataFrame vom Modul Pandas.
Ein Modul ist eine Sammlung von fertigem Python-Code zu einem bestimmten Thema,
hier zur Verarbeitung und Analyse von Daten. Es ist üblich, das Modul `pandas`
mit der Abkürzung `pd` zu importieren, damit wir nicht immer `pandas` schreiben
müssen. Ausführliche Beschreibungen aller Funktionen finden wir in der
offiziellen
[Pandas-Dokumentation](https://pandas.pydata.org/docs/user_guide/index.html).

```{code-cell} ipython3
# Lücke: Importieren Sie das Pandas-Modul mit der üblichen Abkürzung
import ____ as ____
```

## Series erzeugen

Wir starten mit der einfachsten Möglichkeit, eine Series zu erzeugen, der
**Erzeugung aus einer Liste**. Als Beispiel betrachten wir die Verkaufspreise
(in Euro) von zehn Autos. Die Daten stammen von der Internetplattform
[Autoscout24](https://www.autoscout24.de). Die Preise kommen zunächst in eine
Liste (erkennbar an den eckigen Klammern), aus der dann ein Series-Objekt
erzeugt wird.

```{code-cell} ipython3
preisliste = [1999, 35990, 17850, 46830, 27443, 14240, 19950, 15950, 21990, 50000]

# Lücke: Erzeugen Sie aus der Liste ein Series-Objekt
preise = ____
print(preise)
```

In der linken Spalte der Ausgabe sehen wir die Zahlen 0 bis 9. Das ist der
**Default-Index**: Wenn wir beim Erzeugen keinen eigenen Index angeben,
nummeriert Pandas die Elemente automatisch mit 0, 1, 2, ... durch, genau wie
bei einer Liste. Wenn bei einer Liste auf das dritte Element zugegriffen werden
soll, dann verwenden wir den Index 2 (zur Erinnerung: Python zählt ab 0) und
schreiben

```{code-cell} ipython3
# Lücke: Greifen Sie auf das dritte Element der Liste zu
preis_drittes_auto = preisliste[____]
print(f'Preis des dritten Autos: {preis_drittes_auto} EUR')
```

Die Datenstruktur Series ermöglicht es aber, einen *expliziten Index* zu
setzen. Über den optionalen Parameter `index=` speichern wir als
Zusatzinformation noch ab, von welchem Auto der Verkaufspreis erfasst wurde.
Wir werden diesen Datensatz in den folgenden Kapiteln noch weiter vertiefen. An
dieser Stelle halten wir fest, dass die ersten drei Autos von der Marke Audi
sind, die nächsten sind BMWs und die letzten fünf sind von der Marke Citroën.

```{code-cell} ipython3
autos = ['Audi Nr. 1', 'Audi Nr. 2', 'Audi Nr. 3', 'BMW Nr. 1', 'BMW Nr. 2', 'Citroen Nr. 1', 'Citroen Nr. 2', 'Citroen Nr. 3', 'Citroen Nr. 4', 'Citroen Nr. 5']

# Lücke: Erzeugen Sie die Series erneut, diesmal mit den Autos als explizitem Index
preise = pd.Series(preisliste, ____)
print(preise)
```

Beim ersten Aufruf von `print(preise)` wurden die Zahlen 0, 1, 2, usw.
ausgegeben, weil das Series-Objekt zu dem Zeitpunkt noch den automatisch
generierten Default-Index hatte. Den expliziten Index nutzen wir jetzt, um auf
den Verkaufspreis des dritten Autos zuzugreifen. Das dritte Auto ist `Audi Nr.
3`. Wie bei Listen verwenden wir eckige Klammern:

```{code-cell} ipython3
# Lücke: Greifen Sie über den expliziten Index auf das dritte Auto zu
preis_drittes_auto = preise[____]
print(f'Preis des dritten Autos: {preis_drittes_auto} EUR')
```

Eine Series muss aber nicht aus einer Liste erzeugt werden. Eine zweite, oft
besonders elegante Möglichkeit ist die **Erzeugung aus einem Dictionary**. Ein
Dictionary speichert Schlüssel-Wert-Paare, was perfekt zur Struktur einer Series
passt. Die Schlüssel werden automatisch zum Index, die Werte zu den Daten. Wir
brauchen den Parameter `index=` dann gar nicht mehr:

```{code-cell} ipython3
preis_dictionary = {
    'Audi Nr. 1': 1999,
    'Audi Nr. 2': 35990,
    'Audi Nr. 3': 17850,
    'BMW Nr. 1': 46830,
    'BMW Nr. 2': 27443,
    'Citroen Nr. 1': 14240,
    'Citroen Nr. 2': 19950,
    'Citroen Nr. 3': 15950,
    'Citroen Nr. 4': 21990,
    'Citroen Nr. 5': 50000,
}

# Lücke: Erzeugen Sie eine Series aus dem Dictionary. Was wird zum Index?
preise = ____
print(preise)
```

Beide Wege führen zum selben Series-Objekt. Welchen Weg wir wählen, hängt davon
ab, in welcher Form die Daten vorliegen: als Liste oder als Dictionary.

## Attribute einer Series

Ein Series-Objekt speichert neben den eigentlichen Daten noch weitere
Zusatzinformationen, die sogenannten **Attribute**. Auf die Attribute greifen
wir mit dem sogenannten Punktoperator zu. Die vier wichtigsten Attribute sind
`values`, `index`, `dtype` und `name`.

Beginnen wir mit den beiden Bestandteilen, aus denen eine Series besteht: den
Daten und dem Index. Das Attribut `values` liefert die reinen Daten der Series,
also die Verkaufspreise ohne die Beschriftung:

```{code-cell} ipython3
# Lücke: Lassen Sie sich die reinen Daten der Series ausgeben
daten = preise.____
print(daten)
```

Das Attribut `index` liefert entsprechend die Beschriftung, also den Index der
Series:

```{code-cell} ipython3
# Lücke: Lassen Sie sich den Index der Series ausgeben
beschriftung = preise.____
print(beschriftung)
```

Hätten wir beim Erzeugen keinen expliziten Index vergeben, würde hier ein
sogenannter `RangeIndex` ausgegeben. Das ist die Pandas-Bezeichnung für den
Default-Index 0, 1, 2, usw.

Das dritte Attribut ist `dtype`. Darin ist der Datentyp der Elemente des
Series-Objektes gespeichert. Anders als eine Liste erzwingt eine Series einen
gemeinsamen Datentyp für alle Elemente und welcher das ist, verrät uns `dtype`:

```{code-cell} ipython3
# Lücke: Lassen Sie sich den Datentyp der Elemente ausgeben
datentyp_preise = preise.____
print(f'Die einzelnen Elemente des Series-Objektes "preise" haben den Datentyp {datentyp_preise}.')
```

Offensichtlich sind die gespeicherten Werte Integer. Die Zusatzinformation
`int64` bedeutet, dass es sich um einen 64-Bit-Integer handelt. Sind in den
Daten Ganzzahlen und Kommazahlen gemischt, wandelt Pandas beim Erzeugen alle
Elemente in Kommazahlen um und der Datentyp ist `float64`. Tauchen sogar Texte
in den Daten auf, weicht Pandas auf den allgemeinen Datentyp `object` aus. Dann
sind allerdings viele Berechnungen nicht mehr möglich. Ein Blick auf `dtype`
lohnt sich daher immer, um zu prüfen, ob die Daten so gespeichert sind, wie wir
es erwarten.

Zuletzt betrachten wir das Attribut `name`. Damit können wir der Series einen
beschreibenden Namen geben, der bei der Ausgabe mit angezeigt wird. Anders als
die bisherigen Attribute können wir `name` auch direkt setzen:

```{code-cell} ipython3
# Lücke: Geben Sie der Series den Namen 'Verkaufspreis in EUR'
preise.____ = ____
print(preise)
```

Der Name erscheint jetzt in der letzten Zeile der Ausgabe. Im Moment wirkt das
wie eine Kleinigkeit, aber spätestens beim DataFrame im übernächsten Kapitel
wird der Name wichtig, denn dort dient er als Spaltenname.

## Aufgaben

Die folgende Aufgabe bearbeiten Sie zu zweit (Pair Programming): Eine Person
tippt (*Driver*), die andere denkt mit, prüft und schlägt vor (*Navigator*).
Wechseln Sie nach Teilaufgabe 2 die Rollen. **Zeit: 12 Minuten**, danach
besprechen wir die Ergebnisse gemeinsam.

```{admonition} Aufgabe: Kilometerstände im Autohaus
:class: tip
Das Autohaus hat zu den zehn Autos auch die Kilometerstände erfasst. Die Daten
finden Sie bereits als Dictionary in der Code-Zelle unten.

1. Erzeugen Sie aus dem Dictionary eine Series `kilometerstand`.
2. Lassen Sie sich die Attribute `values`, `index` und `dtype` ausgeben.
   Diskutieren Sie mit Ihrer Partnerin / Ihrem Partner: Welchen Datentyp hat die
   Series und warum ist das ein Problem, wenn wir später mit den
   Kilometerständen rechnen wollen?
3. *Rollenwechsel!* Erzeugen Sie die Series erneut, aber ersetzen Sie
   `'unbekannt'` durch den speziellen Python-Wert `None` ("kein Wert
   vorhanden"). Prüfen Sie den Datentyp erneut. Was hat sich geändert und warum
   ist das die bessere Wahl für einen fehlenden Messwert?
4. Geben Sie der Series den Namen `'Kilometerstand'` und greifen Sie über den
   Index auf den Kilometerstand von `BMW Nr. 1` zu.
5. **Zusatzaufgabe:** Die Series `preise` und `kilometerstand` haben denselben
   Index. Überlegen Sie gemeinsam: Wie könnte man wohl den Preis pro gefahrenem
   Kilometer berechnen? Probieren Sie Ihre Idee aus.
```

```{code-cell} ipython3
kilometer_dictionary = {
    'Audi Nr. 1': 165000,
    'Audi Nr. 2': 87500,
    'Audi Nr. 3': 102300,
    'BMW Nr. 1': 21000,
    'BMW Nr. 2': 76900,
    'Citroen Nr. 1': 98000,
    'Citroen Nr. 2': 59000,
    'Citroen Nr. 3': 'unbekannt',
    'Citroen Nr. 4': 45200,
    'Citroen Nr. 5': 12800,
}

# Hier Ihr Code:
```

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir Pandas und die sehr wichtige Datenstruktur Series
kennengelernt. Eine Series kombiniert die feste Reihenfolge einer Liste mit
einem expliziten Index, über den wir Elemente mit sprechenden Labels ansprechen
können. Erzeugen lässt sich eine Series aus einer Liste oder einem Dictionary,
und über die Attribute `values`, `index`, `dtype` und `name` erhalten wir die
wichtigsten Zusatzinformationen. Im nächsten Kapitel geht es darum, die
wichtigsten statistischen Kennzahlen der Daten zu ermitteln, die in dem
Series-Objekt gespeichert sind.
