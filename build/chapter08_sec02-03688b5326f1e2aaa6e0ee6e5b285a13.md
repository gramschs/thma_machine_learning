---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: autoscout24_kodierung.csv
    title: autoscout24_kodierung.csv
  - file: 3ddruck_kodierung.csv
    title: 3ddruck_kodierung.csv
  - file: chapter08_sec02.md
    title: chapter08_sec02.md
---

# 8.2 Kodierung und Skalierung

Bisher haben wir zur Prognose des Verkaufspreises eines Autos nur numerische
Merkmale wie den Kilometerstand genutzt. Viele Merkmale liegen aber als Text vor,
zum Beispiel die Farbe oder der Kraftstoff. Andere numerische Merkmale liegen in
sehr unterschiedlichen Größenordnungen. Damit ein ML-Modell auch diese Merkmale
nutzen kann, bereiten wir die Daten in zwei Schritten vor: mit der **Kodierung**
von kategorialen Daten und der **Skalierung** von numerischen Daten.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können **geordnete kategoriale Daten** (ordinale Daten) mit Hilfe
  eines Dictionaries und der `.replace()`-Methode als Zahlen kodieren.
* [ ] Sie wissen, dass bei genau zwei Kategorien die Reihenfolge keine Rolle
  spielt.
* [ ] Sie können **ungeordnete kategoriale Daten** (nominale Daten) mit der
  `.get_dummies()`-Methode als Zahlen kodieren. Dieses Verfahren heißt
  **One-Hot-Kodierung**.
* [ ] Sie wissen, dass numerische Merkmale in sehr unterschiedlichen
  Größenordnungen viele ML-Modelle stören.
* [ ] Sie können numerische Merkmale skalieren, indem Sie
  * mit dem `MinMaxScaler()` die Daten **normieren** oder
  * mit dem `StandardScaler()` die Daten **standardisieren**.
```

## Geordnete kategoriale Daten kodieren

Bei den Beispielen zur linearen Regression haben wir zur Prognose des
Verkaufspreises nur numerische Merkmale genutzt, zum Beispiel den Kilometerstand.
Es gibt aber weitere Merkmale, die den Preis beeinflussen, etwa den Kraftstoff
(Diesel oder Benzin) oder den Zustand des Autos. Diese Merkmale liegen als Text
vor, in Pandas erkennbar am Datentyp `object`. Ein ML-Modell kann mit Text nicht
rechnen. Wir müssen die Kategorien vorher in Zahlen übersetzen. Wie wir das tun,
hängt davon ab, ob die Kategorien eine natürliche Reihenfolge haben. In diesem
Abschnitt behandeln wir geordnete Kategorien.

Wir laden einen Datensatz mit Verkaufsdaten der Plattform
[Autoscout24.de](https://www.autoscout24.de). Mit der Methode `.info()` lassen
wir uns anzeigen, welchen Datentyp die Merkmale haben.

```{code-cell} python
import pandas as pd

daten = pd.read_csv('autoscout24_kodierung.csv')
daten.info()
```

Wir sehen

- 8 Merkmale mit Datentyp `object`: Marke, Modell, Farbe, Erstzulassung,
  Getriebe, Kraftstoff, Bemerkungen und Zustand,
- 4 Merkmale mit Datentyp `int64`: Jahr, Preis (Euro), Leistung (PS) und
  Leistung (kW),
- 2 Merkmale mit Datentyp `float64`: Verbrauch (l/100 km) und Kilometerstand
  (km).

Die acht Merkmale vom Typ `object` sind Text und müssen kodiert werden. Wir
beginnen mit dem Merkmal »Zustand«. Mit der Methode `.unique()` sehen wir, welche
Kategorien es gibt.

```{code-cell} python
daten['Zustand'].unique()
```

Es gibt vier Kategorien. Sie haben eine natürliche Reihenfolge, denn ein Neuwagen
ist mehr wert als ein Jahreswagen, dieser mehr als ein junger Gebrauchtwagen und
dieser mehr als ein Gebrauchtwagen. Geordnete Kategorien nennen wir **ordinale
Daten**. Beim Kodieren behalten wir die Reihenfolge bei:

- Gebrauchtwagen wird zu 0,
- junger Gebrauchtwagen wird zu 1,
- Jahreswagen wird zu 2,
- Neuwagen wird zu 3.

Diese Zuordnung schreiben wir in ein **Dictionary**. Ein Dictionary ordnet jedem
Eintrag einen Wert zu, hier also jeder Kategorie eine Zahl. Wir schreiben die
Zahlen zunächst als Text `'0'` bis `'3'`. Den Grund erklären wir gleich.

```{code-cell} python
zustand_kodierung = {
    'Gebrauchtwagen': '0',
    'junger Gebrauchtwagen': '1',
    'Jahreswagen': '2',
    'Neuwagen': '3',
}
```

Mit der Methode `.replace()` ersetzen wir jede Kategorie durch den Wert aus dem
Dictionary. Damit `.replace()` zuverlässig funktioniert, ersetzen wir Text durch
Text. Die Umwandlung in echte Zahlen machen wir danach in einem eigenen Schritt
mit der Methode `.astype()`.

```{code-cell} python
daten['Zustand'] = daten['Zustand'].replace(zustand_kodierung)
daten['Zustand'] = daten['Zustand'].astype('int')

# Kontrolle
daten['Zustand'].unique()
```

Aus den vier Kategorien sind die Zahlen 0 bis 3 geworden. Die Reihenfolge der
Zustände bleibt dabei erhalten.

Manche Merkmale haben nur zwei Kategorien, zum Beispiel »Getriebe« mit den Werten
Automatik und Schaltgetriebe. Hier gibt es keine natürliche Reihenfolge. Bei
genau zwei Kategorien spielt das aber keine Rolle. Wir vergeben einfach 0 und 1
und gehen dabei genauso vor wie beim Zustand.

```{admonition} Mini-Übung
:class: tip
Übertragen Sie das Vorgehen auf einen Datensatz aus der Fertigung. Die Datei
`3ddruck_kodierung.csv` enthält 200 3D-Druckaufträge mit jeweils 15 Merkmalen.

1. Lesen Sie die Datei ein. Die Spalte `Nummer` soll als Zeilenindex dienen.
   Verschaffen Sie sich mit `.info()` einen Überblick über die Datentypen.
2. Das Merkmal `Oberflaechenguete` ist geordnet: grob ist schlechter als mittel,
   mittel schlechter als fein. Kodieren Sie es mit einem Dictionary und
   `.replace()` als 0, 1 und 2. Wandeln Sie die Spalte anschließend mit
   `.astype()` in Ganzzahlen um.
3. Das Merkmal `Erfolgreich` hat nur zwei Kategorien: ja und nein. Kodieren Sie
   es als 0 und 1.
4. Kontrollieren Sie jeweils mit `.unique()`, ob die Kodierung geklappt hat.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

druckversuche = pd.read_csv('3ddruck_kodierung.csv', index_col=0)
druckversuche.info()
```

Das geordnete Merkmal `Oberflaechenguete` kodieren:

```python
guete_kodierung = {
    'grob': '0',
    'mittel': '1',
    'fein': '2',
}

druckversuche['Oberflaechenguete'] = druckversuche['Oberflaechenguete'].replace(guete_kodierung)
druckversuche['Oberflaechenguete'] = druckversuche['Oberflaechenguete'].astype('int')

druckversuche['Oberflaechenguete'].unique()
```

Das Merkmal `Erfolgreich` hat nur zwei Kategorien. Wir vergeben 0 und 1:

```python
erfolg_kodierung = {
    'nein': '0',
    'ja': '1',
}

druckversuche['Erfolgreich'] = druckversuche['Erfolgreich'].replace(erfolg_kodierung)
druckversuche['Erfolgreich'] = druckversuche['Erfolgreich'].astype('int')

druckversuche['Erfolgreich'].unique()
```
````

## Ungeordnete kategoriale Daten kodieren

Anders verhält es sich bei den ungeordneten kategorialen Daten wie
beispielsweise den Farben der Autos.

```{code-cell} python
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

```{code-cell} python
pd.get_dummies(daten['Farbe'])
```

Damit haben wir die Spalte »Farbe« nun durch 14 Spalten kodiert. Wir könnten nun
im ursprünglichen Datensatz die Spalte »Farbe« löschen und die neuen 14 Spalten
hinzufügen. Tatsächlich erledigt das Pandas bereits für uns, wenn wir die
Methode etwas modifiziert aufrufen. Mit dem Argument `data=` übergeben wir nun
den kompletten Datensatz und mit dem Argument `columns=` spezifizieren wir die
Liste der ungeordneten kategorialen Daten, die One-Hot-kodiert werden sollen.

```{code-cell} python
daten = pd.get_dummies(data=daten, columns=['Farbe'])
daten.head()
```

Die neuen Spaltennamen sind eine Kombination aus dem alten Spaltennamen »Farbe«
und den Kategorien.

## Skalierung von numerischen Daten

Nachdem wir uns intensiv mit den kategorialen Daten beschäftigt haben,
betrachten wir nun die numerischen Daten. Wir laden den Original-Datensatz und
entfernen die kategorialen Daten.

```{code-cell} python
daten = pd.read_csv('autoscout24_kodierung.csv')

daten = daten.drop(columns=['Marke', 'Modell', 'Farbe', 'Erstzulassung', 
                            'Getriebe', 'Kraftstoff','Bemerkungen', 'Zustand'])
daten.info()
```

Ein erster Blick auf die Daten zeigt bereits, dass die Eigenschaftswerte in
unterschiedlichen Bereichen liegen.

```{code-cell} python
daten.head()
```

Der Verbrauch gemessen in Litern pro 100 Kilometer liegt zwischen 5 und 10,
wohingegen der Kilometerstand die 100000 km übersteigt. Das zeigt auch die
Übersicht der statistischen Kennzahlen:

```{code-cell} python
daten.describe()
```

Damit ist auch der Boxplot nur noch schwer lesbar:

```{code-cell} python
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

```{code-cell} python
from sklearn.model_selection import train_test_split

daten_train, daten_test = train_test_split(daten, random_state=0)
```

Dann importieren wir die Klasse `MinMaxScaler` aus dem Untermodul
`sklearn.preprocessing` und erzeugen ein MinMaxScaler-Objekt:

```{code-cell} python
from sklearn.preprocessing import MinMaxScaler

# Auswahl Skalierungsmethode: Normierung
normierung = MinMaxScaler()
```

Jetzt wird das Minimum/Maximum jeder Spalte bestimmt, also der MinMaxScaler an
die Trainingsdaten angepasst. Daher ist es nicht verwunderlich, dass die Methode
`fit()` genannt wurde. Dem MinMaxScaler werden also die Trainingsdaten
übergeben:

```{code-cell} python
normierung.fit(daten_train)
```

Zuletzt erfolgt die Transformation der Daten mit der `transform()`-Methode. Dazu
werden einmal die Trainingsdaten und einmal die Testdaten dem angepassten
MinMaxScaler übergeben und die transformierten Daten in neuen Variablen
gespeichert.

```{code-cell} python
# Transformation der Trainings- und Testdaten
X_train_normiert = normierung.transform(daten_train)
X_test_normiert = normierung.transform(daten_test)
```

Wir schauen in 'X_train_normiert' hinein:

```{code-cell} python
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

```{code-cell} python
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
