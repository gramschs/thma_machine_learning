---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 3.2 Auswählen und Rechnen mit Series

Im letzten Kapitel haben wir die Datenstruktur Series kennengelernt und ihre
Attribute abgefragt. Jetzt fangen wir an, mit den Daten zu arbeiten. Wir greifen
gezielt auf einzelne Elemente und Teilbereiche zu, wir rechnen mit allen Werten
auf einmal und wir filtern die Daten nach Bedingungen. Als Beispiel dient uns
weiterhin das fiktive Autohaus mit seinen zehn Autos.

## Zugriff mit .loc[] und .iloc[]

Zunächst erzeugen wir wieder unser Series-Objekt mit den Verkaufspreisen der
zehn Autos.

```{code-cell} python
import pandas as pd

preisliste = [1999, 35990, 17850, 46830, 27443, 14240, 19950, 15950, 21990, 12450]
autos = ['Audi Nr. 1', 'Audi Nr. 2', 'Audi Nr. 3', 'BMW Nr. 1', 'BMW Nr. 2', 'Citroen Nr. 1', 'Citroen Nr. 2', 'Citroen Nr. 3', 'Citroen Nr. 4', 'Citroen Nr. 5']
preise = pd.Series(preisliste, index=autos, name='Verkaufspreis')
print(preise)
```

Aus dem letzten Kapitel kennen wir bereits den Zugriff über den expliziten
Index, also beispielsweise `preise['Audi Nr. 3']`. Das funktioniert, hat aber
einen Haken. Was wäre, wenn der explizite Index selbst aus Ganzzahlen bestehen
würde? Dann wäre bei einem Ausdruck wie `preise[2]` nicht mehr klar, ob die
Position 2 oder das Label 2 gemeint ist. Um solche Mehrdeutigkeiten zu
vermeiden, stellt Pandas zwei eindeutige Zugriffsarten bereit:

* `.loc[]` greift über das **Label** zu (loc wie location, also der "Ort" im
  expliziten Index),
* `.iloc[]` greift über die **Position** zu (iloc wie integer location, also
  die ganzzahlige Position 0, 1, 2, ...).

Der Preis des dritten Autos lässt sich also auf zwei Arten ermitteln. Einmal
über das Label:

```{code-cell} python
preis_drittes_auto = # TODO: ???  (Preis des dritten Autos über das Label abfragen)
print(f'Preis des dritten Autos: {preis_drittes_auto} EUR')
```

Und einmal über die Position (zur Erinnerung: Python zählt ab 0, das dritte
Auto steht also an Position 2):

```{code-cell} python
preis_drittes_auto = # TODO: ???  (Preis des dritten Autos über die Position abfragen)
print(f'Preis des dritten Autos: {preis_drittes_auto} EUR')
```

Mit beiden Zugriffsarten können wir auch **Teilbereiche** auswählen. Diese
Technik heißt **Slicing** (englisch für "in Scheiben schneiden") und
funktioniert mit einem Doppelpunkt zwischen Start und Ende. Wählen wir alle
Autos von `Audi Nr. 1` bis `BMW Nr. 1` aus:

```{code-cell} python
teilbereich = preise.loc['Audi Nr. 1':'BMW Nr. 1']
print(teilbereich)
```

Wir erhalten vier Autos, denn `BMW Nr. 1` ist in der Auswahl enthalten, also
*inklusiv*. Versuchen wir nun, denselben Teilbereich über die Positionen zu
erhalten. Die vier Autos stehen an den Positionen 0, 1, 2 und 3:

```{code-cell} python
teilbereich = # TODO: ???  (Positionen 0 bis 3 auswählen)
print(teilbereich)
```

Auch hier erhalten wir vier Autos, aber Vorsicht: Wir mussten `0:4` schreiben,
nicht `0:3`. Hier lauert ein beliebter Stolperstein.

**Achtung: Obergrenze beim Slicing**
Beim Slicing mit `.loc[]` ist die Obergrenze **eingeschlossen/inklusiv**, beim
Slicing mit `.iloc[]` ist sie **ausgeschlossen/exklusiv** (wie bei
Python-Listen). Der Ausdruck `preise.loc['Audi Nr. 1':'BMW Nr. 1']` liefert vier
Elemente inklusive `BMW Nr. 1`, der Ausdruck `preise.iloc[0:4]` liefert die
Positionen 0 bis 3.

Die Regel lässt sich gut merken, wenn man sich den Grund überlegt: Bei Labels
wissen wir nicht, welches Label "eins weiter" wäre. Deshalb nimmt Pandas das
Label der Obergrenze noch mit. Bei Positionen dagegen bleibt Pandas bei der
üblichen Python-Konvention.

## Rechnen mit Series

Falls der Datentyp der einzelnen Elemente eines Series-Objektes ein numerischer
Typ ist (Integer oder Float), können wir mit den Einträgen auch rechnen. So
lassen sich beispielsweise die Preise nicht in Euro, sondern in Cent angeben,
wenn wir alle Preise mit 100 multiplizieren.

```{code-cell} python
preise_in_cent = # TODO: ???  (alle Preise in Cent umrechnen)
print(preise_in_cent)
```

Wir könnten auch auf die Idee kommen, das billigste Auto auf den Preis 0 zu
setzen und ausgeben, um wie viel Euro die anderen Autos teurer sind. Oder anders
ausgedrückt, wir subtrahieren von jedem Preis den Preis des billigsten Autos,
also 1999 EUR:

```{code-cell} python
preise_differenz = preise - 1999
print(preise_differenz)
```

Bemerkenswert ist, was hier *nicht* im Code steht: keine Schleife. Bisher
hätten wir mit einer for-Schleife jedes Element einzeln bearbeitet. Pandas
wendet die Rechenoperation dagegen automatisch auf jedes einzelne Element an.
Diese Arbeitsweise nennt man **vektorisiertes Rechnen**. Sie macht den Code
nicht nur kürzer und besser lesbar, sondern bei großen Datenmengen auch
erheblich schneller.

Vektorisiertes Rechnen funktioniert auch zwischen **zwei Series-Objekten**.
Beispielsweise können wir die Kilometerstände der zehn Autos erfassen:

```{code-cell} python
kilometerstand = pd.Series({
    'Audi Nr. 1': 231000,
    'Audi Nr. 2': 2500,
    'Audi Nr. 3': 127800,
    'BMW Nr. 1': 117433,
    'BMW Nr. 2': 19895,
    'Citroen Nr. 1': 57070,
    'Citroen Nr. 2': 81700,
    'Citroen Nr. 3': None,
    'Citroen Nr. 4': 8500,
    'Citroen Nr. 5': 15200,
})
```

Beim dritten Citroën ist der Tachostand nicht eindeutig ablesbar, deswegen
setzen wir `None`. Teilen wir die Preise durch die Kilometerstände, erhalten
wir für jedes Auto den Preis pro gefahrenem Kilometer:

```{code-cell} python
preis_pro_km = preise / kilometerstand
print(preis_pro_km)
```

Pandas verrechnet dabei automatisch die Elemente, die dasselbe Label im Index
tragen. Für `Citroen Nr. 3` kommt `NaN` heraus, was für *Not a Number* steht,
weil der Kilometerstand fehlt. Pandas berücksichtigt also fehlende Werte in der
Rechnung.

Neben den arithmetischen Operationen gibt es noch eine zweite Art von
vektorisierten Operationen, die **Vergleichsoperatoren**. Auch ein Vergleich
wird auf jedes einzelne Element angewendet. Prüfen wir, welche Autos mehr als
20000 EUR kosten:

```{code-cell} python
ist_teuer = preise > 20000
print(ist_teuer)
```

Das Ergebnis ist wieder eine Series, aber eine besondere: Sie enthält für jedes
Auto den Wahrheitswert `True` oder `False` und hat den Datentyp `bool`. Man
spricht von einer **booleschen Series**. Was wir damit anfangen können, sehen
wir im nächsten Abschnitt.

## Series filtern mit boolescher Indizierung

Die boolesche Series aus dem letzten Abschnitt ist mehr als eine Spielerei. Wir
können sie in eckigen Klammern hinter ein Series-Objekt schreiben und erhalten
dann genau die Elemente, bei denen `True` steht. Diese Technik heißt
**boolesche Indizierung** und ist eines der wichtigsten Werkzeuge der
Datenanalyse überhaupt.

```{code-cell} python
teure_autos = # TODO: ???  (Preise über 20000 EUR herausfiltern)
print(teure_autos)
```

Der Ausdruck liest sich am besten von innen nach außen: Der innere Teil
`preise > 20000` erzeugt die boolesche Series, die äußeren eckigen Klammern
wählen dann alle Elemente aus, bei denen `True` steht. In Worten: "Gib mir alle
Preise, für die gilt: Preis größer als 20000 EUR."

Natürlich funktioniert das mit jeder Bedingung. Suchen wir alle Autos, die
weniger als 15000 EUR kosten:

```{code-cell} python
guenstige_autos = preise[preise < 15000]
print(guenstige_autos)
```

Das Ergebnis ist wieder ein ganz normales Series-Objekt, mit dem wir
weiterarbeiten können. Der explizite Index sorgt dafür, dass wir auch nach dem
Filtern noch wissen, um welche Autos es sich handelt.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir gelernt, mit den Daten in einem Series-Objekt zu
arbeiten. Mit `.loc[]` greifen wir über das Label und mit `.iloc[]` über die
Position auf einzelne Elemente und Teilbereiche zu, wobei beim Slicing mit
`.loc[]` die Obergrenze eingeschlossen ist. Arithmetische Operationen und
Vergleiche werden vektorisiert auf jedes Element angewendet, ganz ohne
Schleifen. Mit der booleschen Indizierung filtern wir schließlich alle Elemente
heraus, die eine Bedingung erfüllen. Im nächsten Kapitel lernen wir die
wichtigsten statistischen Kennzahlen kennen und visualisieren sie mit einem
Boxplot.

## Mini-Übungen

### Mini-Übung 1

Erzeugen Sie erneut die Bildschirmzeiten-Series mit den Beispieldaten aus dem
letzten Kapitel (Montag 2.5, Dienstag 3, Mittwoch 4.25, Donnerstag 2.75,
Freitag 3.5, Samstag 6.5, Sonntag 5 Stunden).

1. Greifen Sie auf die Bildschirmzeit von Mittwoch zu, einmal mit `.loc[]` und
   einmal mit `.iloc[]`.
2. Wählen Sie den Teilbereich von Dienstag bis Donnerstag aus, ebenfalls auf
   beide Arten. Achten Sie auf die Obergrenze.

```{code-cell} python
# Code-Zelle
```

### Mini-Übung 2

Verwenden Sie erneut die Bildschirmzeiten-Series.

1. Rechnen Sie die Bildschirmzeiten von Stunden in Minuten um und geben Sie das
   Ergebnis aus.
2. Erzeugen Sie eine boolesche Series, die für jeden Tag angibt, ob Sie mehr
   als 4 Stunden am Bildschirm verbracht haben. An welchen Tagen steht `True`?

```{code-cell} python
# Code-Zelle
```

### Mini-Übung 3

Filtern Sie aus der Bildschirmzeiten-Series alle Tage heraus, an denen Sie mehr
als 6 Stunden Bildschirmzeit hatten. Geben Sie das Ergebnis aus.

```{code-cell} python
# Code-Zelle
```
