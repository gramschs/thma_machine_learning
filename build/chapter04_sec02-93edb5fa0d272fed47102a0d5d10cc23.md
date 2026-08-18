---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: autoscout24_xxs.csv
    title: autoscout24_xxs.csv
  - file: chapter04_sec02.md
    title: chapter04_sec02.md
---

# 4.2 Arbeiten mit Tabellendaten

```{admonition} Warnung
:class: warning
Dieses Kapitel befindet sich derzeit im Umbau und wird rechtzeitig vor der
Vorlesung im WiSe 2026/27 zur Verfügung stehen.
```

In Tabellenkalkulationssoftware ist es möglich, einzelne Zeilen oder Spalten zu
bearbeiten. Pandas mit seiner Datenstruktur DataFrame bietet diese Möglichkeit
ebenfalls. Wie auf einzelne Spalten und Zeilen zugegriffen wird und wie die
Daten bearbeitet werden können, zeigt dieses Kapitel.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können mit eckigen Klammern **[]** und dem Spaltenindex auf eine ganze
  Spalte zugreifen.
* [ ] Sie können mit **.loc[]** und dem Zeilenindex auf eine ganze Zeile
  zugreifen.
* [ ] Sie können mit **.loc[zeileindex, spaltenindex]** auf eine einzelne Zelle
  der Tabelle zugreifen.
* [ ] Sie können mehrere unzusammenhängende Zeilen/Spalten mittels Liste
  auswählen.
* [ ] Sie können zusammenhängende Bereiche mittels **Slicing** auswählen.
* [ ] Sie können eine Tabelle um eine Spalte erweitern.
```

## Zugriff auf Spalten

Bei einer Liste oder der Pandas-Datenstruktur Series haben wir auf ein einzelnes
Element zugegriffen, indem wir eckige Klammern benutzt haben. Bei Tabellen und
damit auch DataFrames ist es üblich, dass die Eigenschaften bzw. Merkmale in den
Spalten stehen und in den Zeilen die einzelnen Datenpunkte. Mit den eckigen
Klammern und dem Spaltennamen greifen wir diesmal also nicht nur ein Element
heraus, sondern gleich eine ganze Spalte.

Um den Zugriff auf eine Spalte eines DataFrames auszuprobieren, brauchen wir
einen DataFrame. Wir verwenden erneut den Datensatz `autoscout24_xxs.csv` und
lesen ihn mit der ersten Spalte ID als Zeilenindex ein. Dann verschaffen uns
einen ersten Überblick.

```{code-cell} python
import pandas as pd
tabelle = pd.read_csv('autoscout24_xxs.csv', index_col=0)

print(f'Anzahl Autos: {tabelle.shape[0]}')
print(f'Anzahl Merkmale: {tabelle.shape[1]}')

print('\nAnzeige der Merkmale der ersten fünf Autos:')
tabelle.head()
```

Die Farbe der 10 Autos können wir folgendermaßen aus der Tabelle auswählen:

```{code-cell} python
farbe = tabelle['Farbe']
```

Was steckt jetzt in der Variable `farbe`? Ermitteln wir zunächst, welchen
Datentyp das Objekt hat, das in `farbe` gespeichert ist.

```{code-cell} python
type(farbe)
```

Es ist ein Series-Objekt mit dem Namen Farbe, also dem ursprünglichen
Spaltenlabel. Das neu erzeugte Series-Objekt kann also beispielsweise mit
`.head()` angezeigt werden.

```{code-cell} python
farbe.head()
```

Bei Auswahl mehrerer Spalten mit einer Liste entsteht wieder ein DataFrame, aber
dazu kommen wir gleich. Zunächst widmen wir uns dem Zugriff auf Zeilen und
Zellen.

## Zugriff auf Zeilen und Zellen mit .loc[]

Natürlich kann es auch Gründe geben, sich einen einzelnen Datenpunkt mit allen
Merkmalen herauszugreifen. Oder anders ausgedrückt, vielleicht möchte man in der
Tabelle eine einzelne **Zeile** auswählen. Dazu gibt es den Indexer `.loc`.
Danach werden wieder eckige Klammern benutzt, wobei diesmal der Zeilenindex und
nicht der Spaltenname verwendet wird.

Der folgende Code-Schnippsel speichert die Zeile des 4. Autos (= BMW Nr. 1) in
der Variable `viertes_auto` ab. Wir ermitteln gleich den Datentyp dazu.

```{code-cell} python
viertes_auto = tabelle.loc['BMW Nr. 1']
type(viertes_auto)
```

Auch eine einzelne Zeile ist eine Series-Datenstruktur, die wir mit den
Series-Methoden weiter bearbeiten können. Der Name des Series-Objektes ist
diesmal der ursprüngliche Zeilenindex. Wir lassen den Datensatz mit `.head()`
anzeigen.

```{code-cell} python
viertes_auto.head()
```

Es kann auch vorkommen, dass man gezielt auf eine einzelne **Zelle** zugreifen
möchte. Auch dazu benutzen wir den Indexer `.loc[]`. Für eine einzelne Zelle
müssen wir angeben, in welcher Zeile und in welcher Spalte sich diese Zelle
befindet. Der Indexer `.loc[]` ermöglicht auch zwei Angaben, also Zeile und
Spalte, indem beide Werte durch ein Komma getrennt werden.

Wollen wir beispielsweise wissen, wann der Audi Nr. 3 zum ersten Mal zugelassen
wurde, so gehen wir folgendermaßen vor:

```{code-cell} python
erstzulassung_audi3 = tabelle.loc['Audi Nr. 3', 'Erstzulassung']
print(erstzulassung_audi3)
```

Jetzt erhalten wir keine Series-Datenstruktur zurück, sondern direkt den Inhalt
dieser Zelle. In unserem Beispiel ist die Erstzulassung als String gespeichert.
Wir Menschen können diesen String natürlich interpretieren und sehen, dass der
Audi Nr. 3 im November 2018 zum ersten Mal zugelassen wurde.

## Mehrfachauswahl und Tabelle erweitern

Sollen mehrere Zeilen oder Spalten gleichzeitig ausgewählt werden, so werden die
entsprechenden Indizes als eine Liste in die eckigen Klammern gesetzt. Wir
demonstrieren die Mehrfachauswahl hier für Spalten.

Mit einer Liste in eckigen Klammern wählen wir mehrere Spalten auf einmal aus,
in diesem Beispiel sowohl die Erstzulassung als auch den Preis.

```{code-cell} python
mehrere_spalten = tabelle[['Erstzulassung', 'Preis (Euro)']]
mehrere_spalten.head()
```

Wenn die Spalten oder Zeilen nacheinander kommen, also zusammenhängend sind,
brauchen wir nicht alle Indizes in die Liste zu schreiben. Es genügt, den ersten
Index und den letzten Index zu nehmen und dazwischen einen Doppelpunkt zu
setzen. Diese Art, Zeilen oder Spalten auszuwählen, wird in der Informatik als
**Slicing** bezeichnet. Da die Autos in diesem Datensatz nach Marke sortiert
sind, können wir alle Autos der Marke Citroën per Slicing extrahieren:

```{code-cell} python
citroens = tabelle.loc[ 'Citroen Nr. 1' : 'Citroen Nr. 5'] 
citroens.head()
```

Wichtig dabei ist, dass beim Slicing mit `.loc[start:ende]` der Endwert
inkludiert ist im Gegensatz zu Python-Listen.

Jetzt kann beispielsweise der durchschnittliche Verkaufspreis aller Citroëns
folgendermaßen ermittelt werden:

```{code-cell} python
durchschnittspreis = citroens['Preis (Euro)'].mean()
print(f'Der durchschnittliche Verkaufspreis der Citroens ist {durchschnittspreis:.2f} EUR.')
```

Beim Slicing können wir den Anfangsindex oder den Endindex oder sogar beides
weglassen. Wenn wir den Anfangsindex weglassen, fängt Pandas bei der ersten
Zeile/Spalte an. Lassen wir den Endindex weg, geht der Slice automatisch bis zum
Ende.

Auch das Erweitern der Tabelle funktioniert über denselben Mechanismus: Um eine
neue Spalte einzufügen, wird einfach ein neuer Spaltenindex erzeugt.

```{code-cell} python
# Erweiterung der Tabelle um eine neue Spalte
tabelle['Preis pro Leistung'] = tabelle['Preis (Euro)'] / tabelle['Leistung (PS)']

# Überblick
print(f'Anzahl Autos: {tabelle.shape[0]}')
print(f'Anzahl Merkmale/Spalten: {tabelle.shape[1]}')
tabelle.head()
```

Nach demselben Prinzip lässt sich mit `.loc[]` auch eine neue Zeile einfügen,
indem ein neuer Zeilenindex vergeben wird. Das Einfügen einer neuen Spalte oder
Zeile über einen neuen Index funktioniert allerdings nur, wenn die neuen Daten
das richtige Format haben. Sollen mehrere bereits als DataFrame vorliegende
Zeilen oder Spalten zusammengeführt werden, eignet sich `pd.concat()`(siehe
[Dokumentation →
concat](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html?highlight=concat#pandas.concat)).

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir uns damit beschäftigt, wie tabellarische Daten
verwaltet werden. Im nächsten Kapitel geht es darum, diese zu visualisieren.
