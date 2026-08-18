---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: autoscout24_xxs.csv
    title: autoscout24_xxs.csv
  - file: 3ddruck_xxs.csv
    title: 3ddruck_xxs.csv
  - file: chapter04_sec01.md
    title: chapter04_sec01.md
---

# 4.1 Datenstruktur DataFrame

Bisher haben wir uns mit Datenreihen beschäftigt. Das Modul Pandas stellt zur
Verwaltung von Datenreihen die Datenstruktur Series zur Verfügung, die wir im
letzten Kapitel kennengelernt haben. In diesem Kapitel lernen wir die
Datenstruktur **DataFrame** kennen, die die Verwaltung von tabellarischen Daten
ermöglicht.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie kennen die Datenstruktur **DataFrame**.
* [ ] Sie kennen das **csv-Dateiformat**.
* [ ] Sie können eine csv-Datei mit **read_csv()** einlesen.
* [ ] Sie können sich mit **.shape**, **.head()**, **.info()** und
  **.describe()** einen ersten Überblick über die importierten Daten
  verschaffen.
```

## Was ist ein DataFrame?

Bei Auswertung von Messungen ist der häufigste Fall der, dass Daten in Form
einer Tabelle vorliegen. Ein DataFrame-Objekt entspricht einer Tabelle, wie man
sie beispielsweise von Excel, LibreOffice oder Numbers kennt. Die Zeilen
besitzen einen Zeilenindex, die Spalten sind über Spaltennamen beziehungsweise
Spaltenlabels beschriftet. Typischerweise werden die Daten in der Tabelle
zeilenweise angeordnet. Damit ist gemeint, dass jede Zeile einen Datenpunkt
enthält und die Spalten die Merkmale speichern.

```{figure} pics/screenshot_libreoffice.png
---
name: chap04_sec01_fig01
---
Screenshot einer Tabellenkalkulationssoftware: die Zeilen sind mit Zahlen
indiziert, die Spalten mit Großbuchstaben beschriftet. Jede Zeile enthält einen
Datenpunkt mit der Beschreibung der Merkmale eines Autos. (Quelle: eigene
Abbildung; Lizenz [CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0))
```

```{admonition} Mini-Übung
:class: tip
Betrachten Sie die folgende kleine Tabelle mit drei 3D-Druckversuchen:

| | Material | Zugfestigkeit (MPa) |
|---|---|---|
| 0 | PLA | 48.3 |
| 1 | PETG | 45.0 |
| 2 | ABS | 24.5 |

1. Was stellt in dieser Tabelle jede Zeile dar, was jede Spalte?
2. Vergleichen Sie mit der Abbildung oben (Screenshot der Tabellenkalkulation):
   Dort sind die Zeilen mit den Zahlen 1 bis 11 indiziert und die Spalten mit
   Buchstaben beschriftet. Wie sind hier die Zeilen indiziert und die Spalten
   beschriftet?
3. Stellen Sie sich einen vierten Druckversuch mit ASA (38.4 MPa) vor. Welchen
   Index würde diese Zeile bekommen?
```

```{admonition} Lösung
:class: tip
:class: dropdown
1. Jede Zeile entspricht einem Druckversuch, also einem Datenpunkt. Jede Spalte
   entspricht einem Merkmal dieses Druckversuchs (Material bzw. Zugfestigkeit).
2. Die Zeilen sind mit 0, 1, 2 durchnummeriert und die Spalten sind mit den
   Labels Material bzw. Zugfestigkeit (MPa) beschriftet.
3. Der vierte Druckversuch würde den Index 3 bekommen.
```

Ein DataFrame kann direkt über mehrere Pandas-Series-Objekte oder verschachtelte
Listen erzeugt werden. Da dies in der Praxis nur selten vorkommt und nur für sehr
kleine Datenmengen praktikabel ist, Daten händisch zu erfassen, fokussieren wir
gleich auf die Erzeugung von DataFrame-Objekten aus einer Datei.

## Import von Tabellen im csv-Format

Tabellen werden oft in dem Dateiformat abgespeichert, das die jeweilige
Tabellenkalkulationssoftware Excel, Numbers oder LibreOffice Calc als Standard
voreingestellt hat. Wir betrachten in dieser Vorlesung Tabellen, die in einem
offenen Standardformat vorliegen und damit unabhängig von der verwendeten
Software und dem verwendeten Betriebssystem sind.

Das **Dateiformat CSV** speichert Daten zeilenweise ab. Dabei steht CSV für
"comma separated value". Die Trennung der Spalten erfolgt durch ein
Trennzeichen, normalerweise durch das Komma. Im deutschsprachigen Raum wird
gelegentlich ein Semikolon verwendet, weil im Deutschen das Komma als
Dezimaltrennzeichen verwendet wird. In dieser Vorlesung bleiben wir jedoch beim
Komma als Trennzeichen. Sollte es erforderlich sein, das Komma beispielsweise in
einem Text zu verwenden, kann der gesamte Ausdruck in Anführungszeichen gesetzt
werden, damit das Komma nicht als Trennzeichen interpretiert wird (siehe
Bemerkungen Citroen Nr. 4 in dem nachfolgenden csv-Ausschnitt).

```{code} csv
ID,Marke,Modell,Farbe,Erstzulassung,Jahr,Preis (Euro),Leistung (kW),Leistung (PS),Getriebe,Kraftstoff,Verbrauch (l/100 km),Verbrauch (g/km),Kilometerstand (km),Bemerkungen
Audi Nr. 1,Audi,Audi A4,silber,08/1997,1997,1999,66,90,Schaltgetriebe,Diesel,5.4,146,231000,1.9 TDI / AHK / Tüv neu
Audi Nr. 2,Audi,Audi A1,weiß,05/2023,2023,35990,81,110,Automatik,Benzin,6.1,138,2500,S line 30 TFSI 81(110) kW(PS) S tr
Audi Nr. 3,Audi,Audi A3,blau,11/2018,2018,17850,85,116,Automatik,Benzin,6.6,150,127800,Sportback sport 30 TFSI PDC SHZ XENON
BMW Nr. 1,BMW,BMW X3,blau,04/2018,2018,46830,294,400,Automatik,Diesel,5.9,154,117433,M550 d xDrive AHK+HUD+360+SOFT+SITZKLIMA+NAV-PRO
BMW Nr. 2,BMW,BMW X2,gold,07/2020,2020,27443,103,140,Schaltgetriebe,Benzin,5.5,125,19895,sDrive18i Advantage LED.Navi.RüKamera.ParkAss
Citroen Nr. 1,Citroen,C3,beige,03/2021,2021,14240,60,82,Schaltgetriebe,Benzin,4.2,97,57070,Feel PureTech 83 + LED + PDC + DAB + BLUETOOTH
Citroen Nr. 2,Citroen,Citroen Berlingo,blau,07/2020,2020,19950,75,102,Schaltgetriebe,Diesel,4.1,107,81700,HDI 100 Live M Navi Klima PDC
Citroen Nr. 3,Citroen,Citroen Berlingo,blau,12/2019,2019,15950,75,102,Schaltgetriebe,Diesel,4.1,108,98832,Live M/1 Hand/Klima/Tempomat/PDC
Citroen Nr. 4,Citroen,Citroen Berlingo,schwarz,01/2021,2021,21990,96,131,Schaltgetriebe,Diesel,4.4,116,8500,"Club XL Kasten Blue-HDI 130 Mwst.,Navi,DAB,Temp."
Citroen Nr. 5,Citroen,Citroen C1,silber,03/2021,2021,12450,53,72,Schaltgetriebe,Benzin,3.7,85,15200,VTi 72 Shine+KAMERA+SHZ+APP+DAB+KLIMA+BT
```

Um Tabellen im csv-Format einzulesen, bietet Pandas eine eigene Funktion namens
`read_csv` an. Wird diese Funktion verwendet, um die Daten zu importieren, so
wird automatisch ein DataFrame-Objekt für die importierten Daten erzeugt. Beim
Aufruf der Funktion übergeben wir mindestens den Dateinamen. Über zusätzliche
Optionen können wir beispielsweise steuern, ob Zeilen beim Einlesen übersprungen
werden sollen oder dass das Semikolon anstatt des Kommas als Trennzeichen dient.
Weitere Optionen sind in der [Dokumentation →
read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
beschrieben.

Am besten sehen wir uns die Funktionsweise von `read_csv` an einem Beispiel an.
Bitte laden Sie die Datei `autoscout24_xxs.csv` herunter (Moodle oder
Download-Symbol auf dieser Seite rechts oben) und speichern Sie sie in denselben
Ordner, in dem auch dieses Jupyter Notebook liegt. Die csv-Datei enthält Angaben
zu 10 Autos, die auf [Autoscout24](https://www.autoscout24.de) zum Verkauf
angeboten wurden.

Führen Sie dann anschließend die folgende Code-Zelle aus.

```{code-cell} python
import pandas as pd

tabelle = pd.read_csv('autoscout24_xxs.csv')
```

Es erscheint keine Fehlermeldung, aber den Inhalt der geladenen Datei sehen wir
trotzdem nicht. Wie wir uns einen ersten Überblick über die importierten Daten
verschaffen, erklärt der nächste Abschnitt.

## Ersten Überblick verschaffen

Wie viele Datenpunkte haben wir denn importiert? Das Attribut `.shape` verrät
die Anzahl der Zeilen und Spalten in Form eines Tupels.

```{code-cell}
print(tabelle.shape)
```

Wir haben 10 Zeilen und 15 Spalten (siehe auch [Dokumentation →
shape](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.shape.html)),
also 10 Datenpunkte mit 15 Merkmalen.

Den Inhalt der Tabelle sehen wir mit der Methode `.head()` (siehe auch
[Dokumentation →
head](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.head.html#pandas.DataFrame.head)).

```{code-cell} python
tabelle.head()
```

Die Methode `.head()` zeigt uns die ersten fünf Zeilen der Tabelle an. Der
Zeilenindex und die Spaltenlabels werden fettgedruckt. Anders als bei der
Tabellenkalulationssoftware übernimmt Pandas hier die erste Zeile als
Beschriftung der Spalten, so dass wir hier ID, Marke, Modell usw. als
Spaltennamen haben.

Wenn wir beispielsweise die ersten 10 Zeilen anzeigen lassen wollen, so
verwenden wir die Methode `.head()` mit dem Argument 10, also `.head(10)`:

```{code-cell} python
tabelle.head(10)
```

Offensichtlich wurde beim Import der Daten wieder ein impliziter Index 0, 1, 2,
usw. für die Datenpunkte (Autos) gesetzt. Das ist nicht weiter verwunderlich,
denn Pandas kann nicht wissen, welche Spalte wir als Index vorgesehen haben. Und
manchmal ist ein automatisch erzeugter impliziter Index auch nicht schlecht. In
diesem Fall würden wir aber gerne die Auto-IDs als Zeilenindex verwenden. Daher
modifizieren wir den Befehl `read_csv` mit dem optionalen Argument `index_col=`.
Die Namen stehen in der 1. Spalte, was in Python-Zählweise einer 0 entspricht,
also setzen wir `index_col=0`. Damit ändern wir die Anzahl der Spalten von 15
auf 14, da die ID-Spalte nun der Index ist und nicht mehr mitgezählt wird.

```{code-cell} python
tabelle = pd.read_csv('autoscout24_xxs.csv', index_col=0)

print(f'Anzahl Spalten: {tabelle.shape[1]}')
tabelle.head(10)
```

Das obige Beispiel zeigt uns zwar nun die ersten 10 Zeilen des importierten
Datensatzes, aber welcher Datentyp gesetzt ist und ob die Daten vollständig
sind, zeigen uns `.shape` und `.head()` nicht. Dafür stellt Pandas die Methode
`.info()` zur Verfügung. Probieren wir es einfach aus.

```{code-cell} python
tabelle.info()
```

Mit `.info()` erhalten wir den Datentyp der Variablen `tabelle` (hier ein
DataFrame) und Informationen zum Index (hier 10 Einträge, der erste Eintrag ist
`Audi Nr. 1` und der letzte `Citroen Nr. 5`). Dann wird die Anzahl der Spalten
angegeben (hier 14). Weiterhin entnehmen wir der Ausgabe von `.info()`, dass in
jeder Spalte 10 Einträge sind, die 'non-null' sind. Damit ist gemeint, dass
diese Zellen beim Import nicht leer im Sinne von `NaN` oder `None` waren. Zudem
wird bei jeder Spalte noch der Datentyp angegeben. Für die Marke oder das
Modell, die als Strings gespeichert sind, wird der allgemeine Datentyp
`'object'` angegeben. Beim Jahr oder dem Preis wurden korrekterweise Integer
erkannt. Der Verbrauch (Liter pro 100 Kilometer) wird als Float gespeichert.

So wie die Methode `.info()` uns einen schnellen Überblick über die prinzipielle
Struktur eines DataFrame-Objektes gibt, so liefert die Methode `.describe()`
eine schnelle Übersicht über statistische Kennzahlen.

```{code-cell} python
tabelle.describe()
```

Da es sich eingebürgert hat, Daten zeilenweise und die Merkmale der Datenpunkte
spaltenweise zu speichern, wertet `.describe()` jede Spalte für sich aus. Für
jedes Merkmal werden dann die statistischen Kennzahlen

* count
* mean
* std
* min
* Quantile 25 %, 50 % und 75 %
* max

berechnet und ausgegeben. Die Bedeutung der Kennzahlen wird in der
[Dokumentation →
describe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
erläutert. Sie entsprechen den statistischen Kennzahlen, die die Methode
`.describe()` für Series-Objekte liefert. Eine Bemerkung zum Schluss: Pandas hat
hier auch auf den Datentyp reagiert und nur für die numerischen Werte (Integer
oder Float) die statistischen Kennzahlen ermittelt. Spalten wie beispielsweise
Farbe oder Getriebe wurden ignoriert.

```{admonition} Mini-Übung
:class: tip
Verwenden Sie den Datensatz `3ddruck_xxs.csv`, der Angaben zu 18 3D-Druckversuchen
enthält.

1. Lesen Sie die Datei ein und verwenden Sie dabei die Nummer als Zeilenindex.
2. Wie viele Druckversuche (Zeilen) und wie viele Merkmale (Spalten) enthält
   der Datensatz? Verschaffen Sie sich einen ersten Eindruck des Tabelleninhalts.
3. Gibt es eine Spalte mit fehlenden Werten? Welche, und bei wie vielen
   Druckversuchen fehlt der Eintrag?
4. Wie hoch ist die durchschnittliche Zugfestigkeit über alle Druckversuche?
   Wie groß ist die Spannweite (Maximum minus Minimum) der Druckzeit?
```

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

# Einlesen der csv-Datei mit der Spalte Nummer als Zeilenindex
druckversuche = pd.read_csv('3ddruck_xxs.csv', index_col=0)

# Anzahl und Inhalt
print(druckversuche.shape)
druckversuche.head()

# Fehlende Einträge und Datentypen
druckversuche.info()

# Statistische Kennzahlen
druckversuche.describe()
```

1. Ein Blick auf die csv-Daten zeigt, dass die Spalte "Nummer" die erste Spalte
   ist und daher `index_col=0` gesetzt werden muss.
2. Der Datensatz enthält 18 Zeilen und 14 Spalten.
3. Die Spalte `Bemerkungen` hat nur 16 von 18 non-null-Einträgen, bei 2
   Druckversuchen fehlt hier also der Eintrag. Alle anderen Spalten sind
   vollständig.
4. Wir ermitteln die statistischen Kennzahlen und lesen dann ab. Die
   durchschnittliche Zugfestigkeit liegt bei rund 33.7 MPa. Die Druckzeit reicht
   von 60 bis 1030 Minuten, die Spannweite beträgt also 970 Minuten.
````

## Zusammenfassung und Ausblick

Mit Hilfe der Datenstruktur DataFrame können tabellarische Daten effizient in
Python verwaltet werden. In den nächsten Kapiteln werden wir uns damit
beschäftigen, auf einzelne Spalten oder Zeilen zuzugreifen und die Datenpunkte
der Tabelle als sogenannten Scatterplot zu visualisieren.
