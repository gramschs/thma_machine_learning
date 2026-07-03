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

# 8.1 Fehlende Daten

Realistische Datensätze sind oft unvollständig. In einer Umfrage hat eine Person
mit einer Frage nichts anfangen können und daher nichts angekreuzt. Oder ein
Messsensor an der Produktionsanlage ist abends ausgefallen, was erst am nächsten
Morgen bemerkt wird. Es gibt viele Gründe, warum Datensätze unvollständig sind.
In diesem Abschnitt beschäftigen wir uns damit, fehlende Daten aufzuspüren und
lernen einfache Methoden kennen, damit umzugehen.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können in einem Datensatz mit **isnull()** fehlende Daten aufspüren und
  analysieren.
* Sie kennen die beiden grundlegenden Strategien, mit fehlenden Daten umzugehen:
  * **Elimination** (Löschen) und
  * **Imputation** (Vervollständigen).
* Sie können Daten gezielt mit **drop()** löschen.
* Sie können fehlende Daten mit **fillna()** vervollständigen.
```

## Fehlende Daten aufspüren mit isnull()

Wir arbeiten im Folgenden mit einem echten Datensatz der Verkaufsplattform
[Autoscout24.de](https://www.autoscout24.de), der Verkaufsdaten zu 1000 Autos
enthält.

```{code-cell}
import pandas as pd

url = 'https://raw.githubusercontent.com/gramschs/assets/refs/heads/main/ml4ing/data/autoscout24_fehlende_daten.csv'
daten = pd.read_csv(url)

daten.info()
```

Der Datensatz enthält 1000 Autos, also 1000 Zeilen bzw. 1000 Datenpunkte, und 14
Merkmale. Wir hatten bereits festgestellt, dass die Anzahl der
`non-null`-Einträge für die verschiedenen Merkmale unterschiedlich ist.
Offensichtlich ist nur bei 963 Autos eine »Farbe« eingetragen und die »Leistung
(PS)« ist nur bei 987 Autos gültig. Am wenigsten gültige Einträge hat das
Merkmal »Verbrauch (l/100 km)«, wohingegen bei der Eigenschaft »Kilometerstand
(km)« nur ein ungültiger Eintrag auftaucht. Welche Einträge ungültig sind,
können wir mit der Methode `isnull()` bestimmen. Die Methode liefert ein
Pandas-DataFrame zurück, das True/False-Werte enthält. True steht dabei dafür,
dass ein Wert fehlt bzw. mit dem Eintrag `NaN` gekennzeichnet ist (= not a
number). Weitere Details finden Sie in der [Pandas-Dokumentation →
isnull()](https://pandas.pydata.org/docs/reference/api/pandas.isnull.html).

```{code-cell}
daten.isnull()
```

Bereits in der zweiten Zeile befindet sich ein Auto, bei dem das Merkmal
»Verbrauch (l/100 km)« nicht gültig ist (ggf. müssen Sie weiter nach rechts
scrollen), denn dort steht `True`. Wir betrachten uns diesen Eintrag:

```{code-cell}
daten.loc[1]
```

Bei dem Auto handelt es sich um ein Hybrid-Fahrzeug, vielleicht wurde deshalb
der »Verbrauch (l/100 km)« nicht angegeben? Ist das vielleicht auch bei den
anderen Autos der Grund? Wir speichern zunächst die `isnull()`-Datenstruktur in
einer eigenen Variable ab und ermitteln, wie viele Autos keinen gültigen Eintrag
bei diesem Merkmal haben. Dazu nutzen wir aus, dass der boolesche Wert `False`
bei Rechnungen als 0 interpretiert wird und der boolesche Wert `True` als 1. Die
Methode `.sum()` summiert pro Spalte alle Werte, so dass sie direkt die Anzahl
der ungültigen Werte pro Spalte liefert.

```{code-cell}
fehlende_daten = daten.isnull()

fehlende_daten.sum()
```

Jetzt lassen wir uns diese 109 Autos anzeigen, bei denen ungültige Werte beim
»Verbrauch (l/100 km)« angegeben wurden. Dazu nutzen wir die True-Werte in der
Spalte `Verbrauch (l/100 km)` als Filter für den ursprünglichen Datensatz.
Zumindest die ersten 20 Autos lassen wir uns dann mit der `.head(20)`-Methode
anzeigen.

```{code-cell}
autos_mit_fehlendem_verbrauch_pro_100km = daten[ fehlende_daten['Verbrauch (l/100 km)'] == True ]
autos_mit_fehlendem_verbrauch_pro_100km.head(20)
```

Bemerkung: Der Vergleich `== True` ist redundant und kann auch weggelassen werden.

Beim Kraftstoff werden alle möglichen Angaben gemacht: Hybrid, Benzin, Diesel
und Elektro. Wir müssten jetzt systematisch den fehlenden Angaben nachgehen. Für
Elektrofahrzeuge und ggf. Hybridautos ist die Angabe »Verbrauch (l/100 km)«
unsinnig. Aber das zweite Auto mit der Nr. 5 wird mit Benzin betrieben, da
scheint Nachlässigkeit beim Ausfüllen der Merkmale vorzuliegen. Beim fünften
Auto mit der Nr. 77 ist zwar der »Verbrauch (l/100 km)« nicht angegeben, aber
dafür der »Verbrauch (g/km)«. Daraus könnten wir den »Verbrauch (l/100 km)«
abschätzen und den fehlenden Wert ergänzen. Es gibt verschiedene Strategien, mit
fehlenden Daten umzugehen. Die beiden wichtigsten Verfahren zum Umgang mit
fehlenden Daten sind

1. Löschen (Elimination) und
2. Vervollständigung (Imputation).

Bei Elimination werden Datenpunkte (Autos) und/oder Merkmale gelöscht. Bei
Imputation (Vervollständigung) werden die fehlenden Werte ergänzt. Beide
Verfahren werden wir nun etwas detaillierter betrachten.

## Löschen (Elimination) mit drop()

Bei der Elimination (Löschen) können wir filigran vorgehen oder die
Holzhammer-Methode verwenden. Beispielsweise können wir entscheiden, das Merkmal
»Verbrauch (l/100 km)« komplett zu löschen und einfach nur den »Verbrauch
(g/km)« zu berücksichtigen. Aber ein kurzer Blick auf die Daten hatte ja bereits
gezeigt, dass diese Werte auch nur unzuverlässig gefüllt waren, auch wenn sie
technisch gültig sind. Wir löschen beide Merkmale. Dazu benutzen wir die Methode
`drop()` mit dem zusätzlichen Argument `columns=['Verbrauch (l/ 100 km)',
'Verbrauch (g/km)']`. Da wir gleich zwei Spalten auf einmal eliminieren möchten,
müssen wir die Spalten (Columns) als Liste übergeben. Danach überprüfen wir mit
der Methode `.info()`, ob das Löschen geklappt hat.

```{code-cell}
daten.drop(columns=['Verbrauch (l/100 km)', 'Verbrauch (g/km)'])
daten.info()
```

Leider hat der Befehl `drop()` nicht funktioniert! Was ist da los? Python
verfolgt das Programmierparadigma »Explizit ist besser als implizit!« Daher
werden zwar durch den `drop()`-Befehl die beiden Spalten gelöscht, aber der
Datensatz `daten` selbst bleibt aus Sicherheitsgründen unverändert. Möchten wir
den Datensatz mit den gelöschten Merkmalen weiter verwenden, müssen wir ihn in
einer neuen Variable speichern oder die alte Variable `daten` damit
überschreiben. Wir nehmen eine neue Variable namens `daten_ohne_verbrauch`.

```{code-cell}
daten_ohne_verbrauch = daten.drop(columns=['Verbrauch (l/100 km)', 'Verbrauch (g/km)'])
daten_ohne_verbrauch.info()
```

Ein weiterer Datenpunkt weist einen ungültigen Eintrag für den »Kilometerstand
(km)« auf. Schauen wir zunächst nach, um welches Auto es sich handelt.

```{code-cell}
daten_ohne_verbrauch[ daten_ohne_verbrauch['Kilometerstand (km)'].isnull() ]
```

Bei den Einträgen des Autos sind noch mehr Probleme ersichtlich. Die
Erstzulassung war sicherlich nicht bei 37.500 km und das Jahr ist nicht 12/2020.
Wir können jetzt diesen Datenpunkt löschen oder den Datenpunkt reparieren.
Zunächst einmal der Code zum Löschen des Datenpunktes. Standardmäßig löscht die
`drop()`-Methode ohnehin Zeilen, also Datenpunkte, so dass wir ohne weitere
Optionen den Index der zu löschenden Datenpunkte angeben. Diesmal verwenden wir
die alte Variable um den reduzierten Datensatz zu speichern.

```{code-cell}
daten_ohne_verbrauch = daten_ohne_verbrauch.drop(708)
daten_ohne_verbrauch.info()
```

Wie wir in der [Dokumentation Pandas →
drop()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html)
nachlesen können, gibt es zum expliziten Überschreiben der alten Variable auch
die Alternative, die Option `inplace=True` zu setzen. Welche Option genutzt
wird, ist Geschmackssache.

Ob alle Angaben plausibel sind, ist nicht gesagt. Bei dem Peugeot mit dem Index
708 hatten wir ja gesehen, dass bei der Erstzulassung eine Kilometerangabe
stand. Tatsächlich gab es bereits erste Hinweise darauf, dass manche Werte
technisch gültig, aber nicht plausibel sind. Die Spalte mit dem Jahr
beispielsweise wurde beim Import als Datentyp Object klassifiziert. Zu erwarten
wäre jedoch der Datentyp Integer gewesen. Schauen wir noch einmal in den
ursprünglichen Datensatz hinein.

```{code-cell}
daten['Jahr'].unique()
```

Da bei dem Peugeot mit dem Index 708 das Jahr fälschlicherweise mit `12/2020`
angegeben wurde, hat dieser eine Text-Eintrag dazu geführt, dass die komplette
Spalte als Object klassifiziert wurde und nicht als Integer. Daher müssen stets
weitere Plausibilitätsprüfungen durchgeführt werden, bevor die Daten genutzt
werden, um statistische Aussagen zu treffen oder ein ML-Modell zu trainieren.

## Vervollständigung (Imputation) mit fillna()

Auch bei den Angaben zur Farbe fehlen Einträge. Zum Beispiel die Zeile mit
dem Index 2 ist unvollständig.

```{code-cell}
daten_ohne_verbrauch.loc[2]
```

Diesmal entscheiden wir uns dazu, diese Eigenschaft nicht wegzulassen.
ML-Verfahren brauchen immer einen gültigen Wert und nicht `NaN`. Wir müssen
daher den fehlenden Wert ersetzen. Eine Möglichkeit ist, eine Farbe zu erfinden,
z.B. 'bunt', oder die fehlenden Werte explizit durch einen Eintrag 'keine
Angabe' zu vervollständigen. Dazu benutzen wir die Methode `fillna()` (siehe
[Pandas-Dokumentation →
fillna()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)).
Die Vervollständigung soll nur die NaN-Werte der Spalte »Farbe« füllen. Daher
filtern wir zuerst diese Spalte und wenden darauf die `fillna()`-Methode an. Das
erste Argument der `fillna()`-Methode ist der Wert, durch den die NaN-Werte
ersetzt werden sollen (hier `'keine Angabe'`). Damit die Vervollständigung
explizit gespeichert wird, überschreiben wir die Spalte.

```{code-cell}
daten_ohne_verbrauch['Farbe'] = daten_ohne_verbrauch['Farbe'].fillna('keine Angabe')

# Kontrolle der Vervollständigung
daten_ohne_verbrauch.isnull().sum()
```

Wenn wir uns jetzt noch einmal die dritte Zeile ansehen, sehen wir, dass
`fillna()` funktioniert hat.

```{code-cell} ipython3
daten_ohne_verbrauch.loc[2,:]
```

Bei den PS-Zahlen haben wir ebenfalls keine vollständigen Daten. Diesmal haben
wir nicht kategoriale Daten wie die Farben, sondern numerische Werte. Daher
bietet es sich hier eine zweite Methode der Ersetzung (Imputation) an. Wenn wir
überall da, wo keine PS-Zahlen vorliegen, den Mittelwert der vorhandenen
PS-Zahlen einsetzen, verändern wir zumindest den Mittelwert des gesamten
Datensatzes nur wenig. Wir berechnen daher zuerst den Mittelwert mit der Methode
`.mean()` und nutzen dann die `fillna()`-Methode.

```{code-cell}
mittelwert = daten_ohne_verbrauch['Leistung (PS)'].mean()
print(f'Der Mittelwert der vorhandenen Einträge »Leistung (PS)« ist: {mittelwert:.2f}')

daten_ohne_verbrauch['Leistung (PS)'] = daten_ohne_verbrauch['Leistung (PS)'].fillna(mittelwert)
```

Noch einmal die Kontrolle, ob jetzt alle NaN-Werte eliminiert oder
vervollständigt wurden:

```{code-cell}
daten_ohne_verbrauch.isnull().sum()
```

Der Mittelwert der »Leistung (PS)« ist sehr hoch. Vielleicht haben wir doch den
Datensatz eher verschlechtert, indem wir fehlende Werte durch den Mittelwert
ersetzt haben. Mit großer Wahrscheinlichkeit haben wir die Varianz im Datensatz
reduziert und es könnte auch sein, dass wir Korrelationen verfälscht haben.
Vielleicht wäre der Median eine bessere Alternative. Auch könnten wir zunächst
die Autos mit fehlenden PS-Zahlen weglassen, für die übrigen Autos ein lineares
Regressionsmodell oder einen Entscheidungsbaum trainieren und damit die
fehlenden PS-Zahlen abschätzen. Bei diesem Beispiel wäre die beste Lösung zur
Imputation der ungültigen Werte »Leistung (PS)« die Umrechung der vorhandenen,
gültigen Werte der Spalte »Leistung (kW)«. Tatsächlich sind die beiden Merkmale
redundant, da es sich um dasselbe Merkmal in zwei verschiedenen Einheiten
handelt, so dass wir die Spalte »Leistung (PS)« auch entfernen könnten.

## Zusammenfassung und Ausblick

Ein wichtiger Teil eines ML-Projektes beschäftigt sich mit der Aufbereitung der
Daten für die ML-Algorithmen. Dabei ist es nicht nur wichtig, in großen
Datensammlungen fehlende Einträge aufspüren zu können, sondern ein Gespür dafür
zu entwickeln, wie mit den fehlenden Daten umgegangen werden soll. Die
Strategien hängen dabei von der Anzahl der fehlenden Daten und ihrer Bedeutung
ab. Häufig werden unvollständige Daten aus der Datensammlung gelöscht
(Elimination) oder numerische Einträge durch den Mittelwert der vorhandenen
Daten ersetzt (Imputation). Wie kategoriale Daten für ML-Algorithmen aufbereitet
werden müssen, wird im nächsten Kapitel erklärt.
