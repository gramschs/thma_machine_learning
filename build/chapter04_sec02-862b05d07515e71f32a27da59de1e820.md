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

# 4.2 Arbeiten mit Tabellendaten

In Tabellenkalkulationssoftware ist es möglich, einzelne Zeilen oder Spalten zu
bearbeiten. Pandas mit seiner Dantestruktur DataFrame bietet diese Möglichkeit
ebenfalls. Wie auf einzelne Spalten und Zeilen zugegriffen wird und wie die
Daten bearbeitet werden können, zeigt dieses Kapitel.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können mit eckigen Klammern **[]** und dem Spaltenindex auf eine ganze
  Spalte zugreifen.
* Sie können mit **.loc[]** und dem Zeilenindex auf eine ganze Zeile zugreifen.
* Sie können mit **.loc[zeileindex, spaltenindex]** auf eine einzelne Zelle der
  Tabelle zugreifen.
* Sie können mehrere unzusammenhängende Zeilen/Spalten mittels Liste auswählen.
* Sie können zusammenhängende Bereich mittels **Slicing** auswählen.
* Sie können eine Tabelle um eine Zeile oder Spalte erweitern.
```

## Zugriff auf Spalten

Bei einer Liste oder der Pandas-Datenstruktur Series haben wir auf ein einzelnes
Element zugegriffen, indem wir eckige Klammern benutzt haben. Bei Tabellen und
damit auch DataFrames ist es üblich, dass die Eigenschaften in den Spalten
stehen und in den Zeilen die einzelnen Datensätze. Mit den eckigen Klammern und
dem Indexnamen greifen wir diesmal also nicht nur ein Element heraus, sondern
gleich eine ganze Spalte.

Falls Sie aus dem vorherigen Kapitel den Datensatz {download}`Download
autoscout24_xxs.csv
<https://gramschs.github.io/book_ml4ing/data/autoscout24_xxs.csv>` noch geladen
haben, können Sie sich mit `.info()` die Spaltenüberschriften, also den Index,
direkt anzeigen lassen. Ansonsten importieren Sie zuerst Pandas mit seiner
üblichen Abkürzung pd und laden den Datensatz.

```{code-cell}
import pandas as pd
tabelle = pd.read_csv('autoscout24_xxs.csv', index_col=0)
tabelle.info()
```

Die Farbe der 10 Autos können wir folgendermaßen aus der Tabelle auswählen:

```{code-cell}
farbe = tabelle['Farbe']
```

Was steckt jetzt in der Variable `farbe`? Ermitteln wir zunächst, welchen
Datentyp das Objekt hat, das in `farbe` gespeichert ist.

```{code-cell}
type(farbe)
```

Es ist ein Series-Objekt mit dem Namen Farbe, also dem Spaltenindex. Das neu
erzeugte Series-Objekt kann also beispielsweise mit `.head()` angezeigt werden.

```{code-cell}
farbe.head()
```

Ein DataFrame besteht aus Series-Objekten.

## Zugriff auf Zeilen

Natürlich kann es auch Gründe geben, sich einen einzelnen Datensatz mit allen
Eigenschaften herauszugreifen. Oder anders ausgedrückt, vielleicht möchte man in
der Tabelle eine einzelne Zeile auswählen. Dazu gibt es das Attribut `.loc`.
Danach werden wieder eckige Klammern benutzt, wobei diesmal der Zeilenindex
verwendet wird.

Der folgende Code-Schnippsel speichert die Zeile des 4. Autos (= BMW Nr. 1) in
der Variable `viertes_auto` ab. Wir ermitteln gleich den Datentyp dazu.

```{code-cell}
viertes_auto = tabelle.loc['BMW Nr. 1']
type(viertes_auto)
```

Auch eine einzelne Zeile ist eine Series-Datenstruktur, die wir mit den
Series-Methoden weiter bearbeiten können. Der Name des Series-Objektes ist
diesmal der alte Zeilenindex. Wir lassen den Datensatz mit `.head()` anzeigen.

```{code-cell}
viertes_auto.head()
```

## Zugriff auf Zellen

Es kann auch vorkommen, dass man gezielt auf eine einzelne Zelle zugreifen
möchte. Auch dazu benutzen wir das Attribut `.loc[]`. Für eine einzelne Zelle
müssen wir angeben, in welcher Zeile und in welcher Spalte sich diese Zelle
befindet. Das Attribut `.loc[]` ermöglicht auch zwei Angaben, also Zeile und
Spalte, indem beide Werte durch ein Komma getrennt werden.

Wollen wir beispielsweise wissen, wann der Audi Nr. 3 zum zugelassen wurde, so
gehen wir folgendermaßen vor:

```{code-cell}
erstzulassung_audi3 = tabelle.loc['Audi Nr. 3', 'Erstzulassung']
type(erstzulassung_audi3)
```

Jetzt erhalten wir keine Series-Datenstruktur zurück, sondern den Datentyp des
Elements in dieser Zelle. In unserem Beispiel ist die Erstzulassung als String
gespeichert, den wir mit der print()-Funktion ausgeben lassen können:

```{code-cell}
print(erstzulassung_audi3 )
```

Wir Menschen können diesen String natürlich interpretieren und sehen, dass der
Audi Nr. 3 im November 2018 zum ersten Mal zugelassen wurde. Für Python ist es
an dieser Stelle aber nicht möglich, eine korrekte Interpretation des Strings zu
bieten.

## Mehrere Zeilen oder Spalten

Sollen mehrere Zeilen oder Spalten gleichzeitig ausgewählt werden, so werden die
entsprechenden Indizes als eine Liste in die eckigen Klammern gesetzt.

Der folgende Code wählt sowohl die Erstzulassung als auch den Preis aus.

```{code-cell}
mehrere_spalten = tabelle[ ['Erstzulassung', 'Preis (Euro)'] ]
mehrere_spalten.head()
```

Wenn die Spalten oder Zeilen nacheinander kommen, also zusammenhängend sind,
brauchen wir nicht alle Indizes in die Liste schreiben. Dann genügt es, den
ersten Index und den letzten Index zu nehmen und dazwischen einen Doppelpunkt zu
setzen. Diese Art, Zeilen oder Spalten auszuwählen, wird in der Informatik als
**Slicing** bezeichnet. Alle Autos der Marke Citroën werden also folgendermaßen
extrahiert:

```{code-cell}
citroens = tabelle.loc[ 'Citroen Nr. 1' : 'Citroen Nr. 5'] 
citroens.head()
```

Jetzt kann beispielsweise der mittlere Verkaufspreis aller Citroëns
folgendermaßen ermittelt werden:

```{code-cell}
mittelwert = citroens['Preis (Euro)'].mean()
print(f'Der mittlere Verkaufspreis der Citroens ist {mittelwert:.2f} EUR.')
```

Beim Slicing können wir den Angangsindex oder den Endindex oder sogar beides
weglassen. Wenn wir den Anfangsindex weglassen, fängt Pandas bei der ersten
Zeile/Spalte an. Lassen wir den Endindex weg, geht der Slice automatisch bis zum
Ende.

## Neue Spalte oder Zeile einfügen

Eine neue Spalte einzufügen, funktioniert recht einfach. Dazu wird ein neuer
Spaltenindex erzeugt.

```{code-cell}
tabelle['Verbrauch pro Leistung'] = tabelle['Verbrauch (l/100 km)'] / tabelle['Leistung (PS)']
tabelle.head(10)
```

Nach demselben Prinzip können wir einen neuen Datensatz aufnehmen und eine neue
Zeile einfügen. Da wir uns auf die Zeilen beziehen, verwenden wir wieder
`loc[]`.

```{code-cell}
tabelle.loc['Dacia Nr. 1'] = ['dacia', 'Dacia Duster', 'orange', '03/2023', 2023, 25749, 84, 114, 'Schaltgetriebe', 'Diesel', 5.3, 140, 5.0, 'Journey Blue dCi 115 4x4', 5.3/114] 
tabelle.head(11)
```

```{admonition} Warnung
:class: warning 
Das oben beschriebene Prinzip, eine neue Spalte oder eine neue Zeile einzufügen,
indem ein neuer Spalten- oder Zeilenindex hinzugefügt wird, funktioniert nur,
wenn die neuen Daten das richtige Format haben. Im Zweifelsfall sollte die
Erweiterung eines DataFrames mit
[concat](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html?highlight=concat#pandas.concat)
durchgeführt werden.
```

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir uns damit beschäftigt, wie tabellarische Daten
verwaltet werden. Im nächsten Kapitel geht es darum, diese zu visualisieren.
