---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: autoscout24_xxs.csv
    title: autoscout24_xxs.csv
  - file: chapter04_sec01.md
    title: chapter04_sec01.md
---

# 4.1 Datenstruktur DataFrame

Bisher haben wir uns mit Datenreihen beschäftigt, sozusagen eindimensionalen
Arrays. Das Modul Pandas stellt zur Verwaltung von Datenreihen die Datenstruktur
Series zur Verfügung. In diesem Kapitel lernen wir die Datenstruktur
**DataFrame** kennen, die die Verwaltung von tabellarischen Daten ermöglicht,
also sozusagen zweidimensionalen Arrays.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie kennen die Datenstruktur **DataFrame**.
* Sie kennen das **csv-Dateiformat**.
* Sie können eine csv-Datei mit **read_csv()** einlesen.
* Sie können die ersten Zeilen eines DataFrames mit **.head()** anzeigen lassen.
* Sie konnen mit **.info()** sich einen Überblick über die importierten Daten
  verschaffen.
* Sie können mit **.describe()** die statistischen Kennzahlen ermitteln.
```

## Was ist ein DataFrame?

Bei Auswertung von Messungen ist der häufigste Fall der, dass Daten in Form
einer Tabelle vorliegen. Ein DataFrame-Objekt entspricht einer Tabelle, wie man
sie beispielsweise von Excel, LibreOffice oder Numbers kennt. Sowohl Zeile als
auch Spalten sind indiziert. Typischerweise werden die Daten in der Tabelle
zeilenweise angeordnet. Damit ist gemeint, dass jede Zeile einen Datensatz
darstellt und die Spalten die Eigenschaften speichern.

Ein DataFrame kann direkt über mehrere Pandas-Series-Objekte oder verschachtelte
Listen erzeugt werden. Da es in der Praxis nur selten vorkommt und nur für sehr
kleine Datenmengen praktikabel ist, Daten händisch zu erfassen, fokussieren wir
gleich auf die Erzeugung von DataFrame-Objekten aus einer Datei.

## Import von Tabellen mit .read_csv()

Tabellen liegen werden oft in dem Dateiformat abgespeichert, das die jeweilige
Tabellenkalkulationssoftware Excel, Numbers oder LibreOffice Calc als Standard
eingestellt hat. Wir betrachten in dieser Vorlesung Tabellen, die in einem
offenen Standardformat vorliegen und damit unabhängig von der verwendeten
Software und dem verwendeten Betriebssystem sind.

Das **Dateiformat CSV** speichert Daten zeilenweise ab. Dabei steht CSV für
"comma separated value". Die Trennung der Spalten erfolgt durch ein
Trennzeichen, normalerweise durch das Komma. Im deutschsprachigen Raum wird
gelegentlich ein Semikolon verwendet, weil im deutschprachigen Raum das Komma
als Dezimaltrennzeichen verwendet wird.

Um Tabellen im csv-Format einzulesen, bietet Pandas eine eigene Funktion namens
`read_csv` an (siehe [Dokumentation →
read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)).
Wird diese Funktion verwendet, um die Daten zu importieren, so wird automatisch
ein DataFrame-Objekt erzeugt. Beim Aufruf der Funktion wird mindestens der
Dateiname übergeben. Zusäztliche Optionen können über optionale Argumente
eingestellt werden. Beispielweise könnte auch das Semikolon als Trennzeichen
eingestellt werden.

Am besten sehen wir uns die Funktionsweise von `read_csv` an einem Beispiel an.
Sollten Sie mit einem lokalen Jupyter Notebook arbeiten, laden Sie bitte die
Datei {download}`autoscout24_xxs.csv` herunter und speichern Sie sie in
denselben Ordner, in dem auch dieses Jupyter Notebook liegt. Alternativ können
Sie die csv-Datei auch über die URL importieren, wie es in der folgenden
Code-Zelle gemacht wird. Die csv-Datei enthält die Angaben zu 10 Autos, die auf
[Autoscout24](https://www.autoscout24.de) zum Verkauf angeboten wurden.

Führen Sie dann anschließend die folgende Code-Zelle aus.

```{code-cell}
import pandas as pd

tabelle = pd.read_csv('autoscout24_xxs.csv')
```

Es erscheint keine Fehlermeldung, aber den Inhalt der geladenen Datei sehen wir
trotzdem nicht. Dazu verwenden wir die Methode `.head()`.

## Anzeige der ersten Zeilen mit .head()

Probieren wir einfachmal aus, was die Anwendung der Methode `.head()` bewirkt.

```{code-cell}
tabelle.head()
```

Die Methode `.head()` zeigt uns die ersten fünf Zeilen der Tabelle an. Wenn wir
beispielsweise die ersten 10 Zeilen anzeigen lassen wollen, so verwenden wir die
Methode .head() mit dem Argument 10, also `.head(10)`:

```{code-cell}
tabelle.head(10)
```

Offensichtlich wurde beim Import der Daten wieder ein impliziter Index 0, 1, 2,
usw. gesetzt. Das ist nicht weiter verwunderlich, denn Pandas kann nicht wissen,
welche Spalte wir als Index vorgesehen haben. Und manchmal ist ein automatisch
erzeugter impliziter Index auch nicht schlecht. In diesem Fall würden wir aber
gerne als Zeilenindex die Auto-IDs verwenden. Daher modifizieren wir den Befehl
read_csv mit dem optionalen Argument `index_col=`. Die Namen stehen in der 1.
Spalte, was in Python-Zählweise einer 0 entspricht.

```{code-cell}
tabelle = pd.read_csv('autoscout24_xxs.csv', index_col=0)
tabelle.head(10)
```

## Übersicht verschaffen mit .info()

Das obige Beispiel zeigt uns zwar nun die ersten 10 Zeilen des importierten
Datensatzes, aber wie viele Daten insgesamt enthalten sind, können wir mit der
`.head()`-Methode nicht erfassen. Dafür stellt Pandas die Methode `.info()` zur
Verfügung. Probieren wir es einfach aus.

```{code-cell}
tabelle.info()
```

Mit `.info()` erhalten wir eine Übersicht, wie viele Spalten es gibt und auch
die Spaltenüberschriften werden aufgelistet.

Weiterhin entnehmen wir der Ausgabe von `.info()`, dass in jeder Spalte 10
Einträge sind, die 'non-null' sind. Damit ist gemeint, dass diese Zellen beim
Import nicht leer waren. Zudem wird bei jeder Spalte noch der Datentyp
angegeben. Für die Marke oder das Modell, die als Strings gespeichert sind, wird
der allgemeine Datentyp 'object' angegeben. Beim Jahr oder dem Preis wurden
korrektweise Integer erkannt. Der Verbrauch (Liter pro 100 Kilometer) wird als
Float gespeichert.

## Statistische Kennzahlen mit .describe()

So wie die Methode `.info()` uns einen schnellen Überblick über die Daten eines
DataFrame-Objektes gibt, so liefert die Methode `.describe()` eine schnelle
Übersicht über statistische Kennzahlen.

```{code-cell}
tabelle.describe()
```

Da es sich eingebürgert hat, Daten zeilenweise abzuspeichern und die Eigenschaft
pro einzelnem Datensatz in den Spalten zu speichern, wertet `.describe()` jede
Spalte für sich aus. Für jede Eigenschaft werden dann die statistischen
Kennzahlen

* count
* mean
* std
* min
* max
* Quantile 25 %, 50 % und 75 %
* max

ausgegeben.

Die Bedeutung der Kennzahlen wird in der
[Dokumentation → describe()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
erläutert. Sie entsprechen den statistischen Kennzahlen, die die Methode
.describe() für Series-Objekte liefert. Pandas hat hier auch auf den Datentyp
reagiert. Nur für numerische Werte (Integer oder Float) wurden die statistischen
Kennzahlen ermittelt.

## Zusammenfassung und Ausblick

Mit Hilfe der Datenstruktur DataFrame können tabellarische Daten verwaltet
werden. In den nächsten Kapiteln werden wir uns damit beschäftigen, auf einzelne
Spalten oder Zeilen zuzugreifen und die Datenpunkte als sogenannten Scatterplot
zu visualisieren.
