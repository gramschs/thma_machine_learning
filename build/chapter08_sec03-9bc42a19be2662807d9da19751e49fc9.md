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

# 8.3 Kodierung und Skalierung

ML-Algorithmen können nur Zahlen verarbeiten. In diesem Kapitel werden wir uns
zunächst damit beschäftigen, wie auch kategoriale Daten wie beispielsweise die
Farbe eines Autos verarbeitet werden können. Da viele ML-Modelle empfindlich
darauf reagieren, wenn die numerischen Werte in sehr unterschiedlichen
Größenordnungen liegen, beschäftigen wir uns auch mit der Skalierung von
numerischen Daten.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können geordnete kategoriale (= ordinale) Daten mit Hilfe eines
  Dictionaries und der `replace()`-Methode als Zahlen kodieren.
* Sie können ungeordnete kategoriale (= nominale) Daten mit Hilfe der
  `get_dummies()`-Methode als Zahlen kodieren. Diese Methode nennt man
  **One-Hot-Kodierung**.
* Sie können numerische Daten skalieren, indem Sie 
  * mit dem **MinMaxScaler** die Daten **normieren** oder
  * mit dem **StandardScaler** die Daten **standardisieren**.
```

## Kodierung von kategorialen Daten

Bei den Beispielen zur linearen Regression haben wir zur Prognose des
Verkaufspreises nur numerische Daten genutzt, wie beispielsweise den
Kilometerstand. Es gibt jedoch weitere Merkmale, die die Kaufentscheidung
beeinflussen, wie der Kraftstofftyp (Diesel oder Benzin) und die Marke des
Autos. Diese würden wir ebenfalls gerne in die Prognose des Preises einfließen
lassen. Dazu müssen die kategorialen Daten, die in der Regel durch den Datentyp
String gekennzeichnet sind, vorab in Integer oder Floats umgewandelt werden. Je
nachdem, ob die kategorialen Daten geordnet oder ungeordnet sind, gibt es
verschiedene Vorgehensweisen, wie wir uns im Folgenden anhand eines Beispiels
erarbeiten.

Wir laden einen Datensatz mit Verkaufsdaten der Plattform
[Autoscout24.de](https://www.autoscout24.de). Sie können die csv-Datei hier
herunterladen {download}`Download autoscout24_kodierung.csv
<https://gramschs.github.io/book_ml4ing/data/autoscout24_kodierung.csv>` und in
das Jupyter Notebook importieren. Alternativ können Sie die csv-Datei auch über
die URL importieren, wie es in der folgenden Code-Zelle gemacht wird. Mit der
Methode `.info()` lassen wir uns anzeigen, welchen Datentyp die Merkmale haben.

```{code-cell}
import pandas as pd 

url = 'https://raw.githubusercontent.com/gramschs/assets/refs/heads/main/ml4ing/data/autoscout24_kodierung.csv'
daten = pd.read_csv(url)

daten.info()
```

Wir sehen

- 8 Merkmale mit Datentyp `object`: Marke, Modell, Farbe, Erstzulassung,
  Getriebe, Kraftstoff, Bemerkungen, Zustand,
- 4 Merkmale mit Datentyp `int64`: Jahr, Preis (Euro), Leistung (PS), Leistung
  (kW)
- 2 Merkmale mit Datentyp `float64`: Verbrauch (l/100 km) und Kilometerstand
  (km).

Als erstes betrachten wir geordnete Daten.

### Geordnete kategoriale Daten mit zwei Kategorien (binär ordinale Daten)

Als erstes betrachten wir das Merkmal »Getriebe«. Mit der Methode `.unique()`
ermitteln wir, wie viele verschiedene Kategorien es für dieses Merkmal gibt.

```{code-cell}
daten['Getriebe'].unique()
```

Es gibt nur zwei Kategorien: Automatik und Schaltgetriebe. Diese beiden Werte
wollen wir durch Integer ersetzen:

- Automatik --> 0 und
- Schaltgetriebe --> 1.

0 ist dabei nicht besser als 1, wir wollen nur zwei verschiedene Integer nehmen,
um die beiden Werte 'Automatik' und 'Schaltgetriebe' als Zahlen darzustellen.
Pandas bietet dazu die Methode `replace()` an. Bei der Verwendung dieser Methode
darf sich der Datentyp nicht ändern (in Pandas Version 2 noch erlaubt, ab
Version 3 verboten). Daher kodieren wir zunächst die Strings `'Automatik'` und
`'Schaltgetriebe'` als die Strings `'0'` und `'1'`mit Hilfe eines Dictionaries:

```{code-cell}
getriebe_kodierung = {
  'Automatik': '0',
  'Schaltgetriebe': '1',
}
```

Dann verwenden wir `replace()`, um die Ersetzung vorzunehmen. Zuletzt wandeln
wir die Strings `'0'` und `'1'` noch mit der Methode `astype()` in Integer um:

```{code-cell}
daten['Getriebe'] = daten['Getriebe'].replace(getriebe_kodierung)
daten['Getriebe'] = daten['Getriebe'].astype('int')

# Kontrolle
daten['Getriebe'].unique()
```

### Geordnete kategoriale Daten (ordinale Daten)

Für das Merkmal »Zustand« gibt es vier Kategorien.

```{code-cell}
daten['Zustand'].unique()
```

Die vier Zustände haben eine Ordnung, denn ein Neuwagen ist wertvoller als ein
Jahreswagen. Der Jahreswagen wiederum ist im Allgemeinen wertvoller als der junge
Gebrauchtwagen. Am wenigsten wertvoll ist der Gebrauchtwagen. Durch diese
Ordnung ist es sinnvoll, beim Kodieren der Zustände durch Integer die Ordnung
beizubehalten.

```{code-cell}
zustand_kodierung = {
  'Gebrauchtwagen': '0',
  'junger Gebrauchtwagen': '1', 
  'Jahreswagen': '2',
  'Neuwagen': '3'
}

daten['Zustand'] = daten['Zustand'].replace(zustand_kodierung)
daten['Zustand'] = daten['Zustand'].astype('int')

# Kontrolle
daten['Zustand'].unique()
```

### Ungeordnete kategoriale Daten (nominale Daten): One-Hot-Kodierung

Anders verhält es sich bei den ungeordneten kategorialen Daten wie
beispielsweise den Farben der Autos.

```{code-cell}
daten['Farbe'].unique()
```

14 verschiedene Farben haben die Autos in dem Datensatz. Es wäre jedoch falsch,
nun Integer von 0 bis 13 zu vergeben, denn das würde eine Ordnung der Farben
voraussetzen, die es nicht gibt. Wir verwenden daher das Verfahren der
**One-Hot-Kodierung**. Anstatt einer Spalte mit den Farben führen wir 14 neue
Spalten mit den Farben 'grau', 'grün', 'schwarz', 'blau', usw. ein. Wenn ein
Auto die Farbe 'grau' hat, notieren wir in der Spalte 'grau' in dieser Zeile
eine 1 und in den übrigen 13 Spalten mit den anderen Farben eine 0. So können
wir die Farben numerisch kodieren, ohne eine Ordnung der Farben einzuführen, die
es nicht gibt. Pandas bietet dafür die Methode `get_dummies()`an. Schauen wir
uns zunächst an, was diese Methode bewirkt.

```{code-cell}
pd.get_dummies(daten['Farbe'])
```

Damit haben wir die Spalte »Farbe« nun durch 14 Spalten kodiert. Wir könnten nun
im ursprünglichen Datensatz die Spalte »Farbe« löschen und die neuen 14 Spalten
hinzufügen. Tatsächlich erledigt das Pandas bereits für uns, wenn wir die
Methode etwas modifiziert aufrufen. Mit dem Argument `data=` übergeben wir nun
den kompletten Datensatz und mit dem Argument `columns=` spezifizieren wir die
Liste der ungeordneten kategorialen Daten, die One-Hot-kodiert werden sollen.

```{code-cell}
daten = pd.get_dummies(data=daten, columns=['Farbe'])
daten.head()
```

Die neuen Spaltennamen sind eine Kombination aus dem alten Spaltennamen »Farbe«
und den Kategorien.

## Skalierung von numerischen Daten

Nachdem wir uns intensiv mit den kategorialen Daten beschäftigt haben,
betrachten wir nun die numerischen Daten. Wir laden den Original-Datensatz und
entfernen die kategorialen Daten.

```{code-cell}
url = 'https://raw.githubusercontent.com/gramschs/assets/refs/heads/main/ml4ing/data/autoscout24_kodierung.csv'
daten = pd.read_csv(url)

daten = daten.drop(columns=['Marke', 'Modell', 'Farbe', 'Erstzulassung', 
                            'Getriebe', 'Kraftstoff','Bemerkungen', 'Zustand'])
daten.info()
```

Ein erster Blick auf die Daten zeigt bereits, dass die Eigenschaftswerte in
unterschiedlichen Bereichen liegen.

```{code-cell}
daten.head()
```

Der Verbrauch gemessen in Litern pro 100 Kilometer liegt zwischen 5 und 10,
wohingegen der Kilometerstand die 100000 km übersteigt. Das zeigt auch die
Übersicht der statistischen Kennzahlen:

```{code-cell} ipython3
daten.describe()
```

Damit ist auch der Boxplot nur noch schwer lesbar:

```{code-cell} ipython3
import plotly.express as px 

fig = px.box(daten)
fig.show()
```

Das hat auch Auswirkungen auf das Training der ML-Modelle. Daher beschäftigen
wir uns nun mit der Skalierung von Daten.

Sind die Bereiche der Daten von ihren Zahlenwerten sehr verschieden, sollten
alle numerischen Werte in dieselbe Größenordnung gebracht werden. Dieser Vorgang
heißt **Skalieren** der Daten. Gebräuchlich sind dabei zwei verschiedene
Methoden:

- **Normierung** und
- **Standardisierung**.

### Normierung

Bei der Normierung wird festgelegt, dass alle Zahlenwerte in einem festen
Intervall liegen. Besonders häufig wird das Intervall $[0,1]$ genommen. Die
Verbrauch (l/100 km), der zwischen 3.5 und 14.9 liegt, würde so transformiert
werden, dass das Minimum 3.5 der 0 entspricht und das Maximum 14.9 der 1.
Genauso würde mit den anderen Eigenschaften verfahren werden. Wir nutzen zur
praktischen Umsetzung Scikit-Learn.

Damit keine Informationen über die Testdaten in das Training des ML-Modells
sickern (Data Leakage), wird die Normierung an das Minimum und das Maximum der
Trainingsdaten angepasst und ggf. für die Testdaten angewendet. Damit können
Testdaten auch außerhalb des Intervalls $[0,1]$ liegen. Wir splitten daher
zunächst unsere Daten in Trainings- und Testdaten.

```{code-cell}
from sklearn.model_selection import train_test_split

daten_train, daten_test = train_test_split(daten, random_state=0)
```

Dann importieren wir die Klasse `MinMaxScaler` aus dem Untermodul
`sklearn.preprocessing` und erzeugen ein MinMaxScaler-Objekt:

```{code-cell}
from sklearn.preprocessing import MinMaxScaler

# Auswahl Skalierungsmethode: Normierung
normierung = MinMaxScaler()
```

Jetzt wird das Minimum/Maximum jeder Spalte bestimmt, also der MinMaxScaler an
die Trainingsdaten angepasst. Daher ist es nicht verwunderlich, dass die Methode
`fit()` genannt wurde. Dem MinMaxScaler werden also die Trainingsdaten
übergeben:

```{code-cell}
normierung.fit(daten_train)
```

Zuletzt erfolgt die Transformation der Daten mit der `transform()`-Methode. Dazu
werden einmal die Trainingsdaten und einmal die Testdaten dem angepassten
MinMaxScaler übergeben und die transformierten Daten in neuen Variablen
gespeichert.

```{code-cell}
# Transformation der Trainings- und Testdaten
X_train_normiert = normierung.transform(daten_train)
X_test_normiert = normierung.transform(daten_test)
```

Wir schauen in 'X_train_normiert' hinein:

```{code-cell} ipython3
print(X_train_normiert)
```

Die Normierung der Daten scheint funktioniert zu haben. Alle Werte liegen
zwischen 0 und 1. Gleichzeitig haben wir aber die Pandas-DataFrame-Datenstruktur
verloren. Die Normierung ist nicht für uns Menschen gedacht, sondern für den
ML-Algorithmus. Daher nutzt Scikit-Learn die Transformation der Daten
gleichzeitig für die Umwandlung in das speichereffizientere NumPy-Array, das für
den ML-Algorithmus gebraucht wird.

### Standardisierung

Oft sind Daten normalverteilt. Die Standardisierung berücksichtigt das und
transformiert nicht auf ein festes Intervall, sondern verschiebt den Mittelwert
auf 0 und die Varianz auf 1. Die normalverteilten Daten werden also
standardnormalverteilt. Auch das lassen wir Scikit-Learn erledigen:

```{code-cell} ipython3
from sklearn.preprocessing import StandardScaler

# Auswahl Skalierungsmethode: Standardisierung
standardisierung = StandardScaler()

# Analyse: jede Spalte wird auf ihr Minimum und ihre Maximum hin untersucht
# es werden immer die Trainingsdaten verwendet
standardisierung.fit(daten_train)

# Transformation der Trainungs- und Testdaten
X_train_standardisiert = standardisierung.transform(daten_train)
X_test_standardisiert = standardisierung.transform(daten_test)

print(X_train_standardisiert)
```

Auch hier geht die Pandas-DataFrame-Struktur verloren.

## Zusammenfassung und Ausblick

Kategoriale Daten müssen kodiert werden, damit sie in einem ML-Algorithmus
verarbeitet werden können. Geordnete kategoriale (ordinale) Daten können dabei
über ein Dictionary und die `replace()`-Methode kodiert werden. Für ungeordnete
kategoriale (nominale) Daten muss die One-Hot-Kodierung verwendet werden.

Auch numerische Daten müssen häufig für ML-Algorithmen aufbereitet werden, vor
allem, wenn die Daten in sehr unterschiedlichen Zahlenbereichen liegen. Bei den
bisher eingeführten ML-Modellen lineare Regression und Entscheidungsbäumen ist
die Skalierung der numerischen Daten nicht notwendig. Erst die nachfolgenden
ML-Modelle werden davon Gebrauch machen.
