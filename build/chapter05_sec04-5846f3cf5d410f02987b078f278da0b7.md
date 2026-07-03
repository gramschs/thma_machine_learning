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

# Übungen

```{admonition} Hinweis
:class: warning
Die in dieser Übung verwendeten csv-Dateien können Studierende der Frankfurt UAS
über meinen campUAS-Kurs herunterladen. Für Externe sind die Quellen verlinkt,
jedoch werden ein Kaggle- bzw. ein Statista-Account benötigt.
```

```{admonition} Übung 5.1
:class: tip
Schauen Sie sich die Datei 'kaggle_germany-wind-energy.csv' im Texteditor bzw.
im JupyterLab an. Welche Spalte könnte als Zeilenindex dienen? Importieren Sie
passend die Daten.

Verschaffen Sie sich einen Überblick über die Daten. Welche Messwerte stehen in
den Spalten? Weitere Informationen erhalten Sie hier:
https://www.kaggle.com/datasets/aymanlafaz/wind-energy-germany

Ermitteln Sie die statistischen Kennzahlen und visualisieren Sie die
statistischen Kennzahlen als Boxplot. Ist es sinnvoll, einen gemeinsamen Boxplot
zu verwenden? Interpretieren Sie die statistischen Kennzahlen.

Visualisieren Sie die drei Eigenschaften als Scatterplots. Welche
Schlussfolgerungen ziehen Sie aus den Plots?

Visualisieren Sie drei Eigenschaften als Scattermatrix. Gibt es Abhängigkeiten?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

data = pd.read_csv('kaggle_germany-wind-energy.csv', index_col=0)
data.info()
```

Die erste Spalte enthält Datumsangaben (vermutlich in UTC) und bietet sich daher
als Zeilenindex an. Der Zeilenindex reicht dann vom 01.01.2017 bis zum
30.12.2019.

Insgesamt sind es dann drei Spalten mit Angaben zu

* wind_generation_actual,
* wind_capacity, 
* temperature.

Die Quelle der Daten verrät, dass sich dahinter die 

* tägliche produzierte Windenergie in MW,
* elektrische Windkapaität in MW und
* Temperatur in Grad Celsius

verbergen.

Alle Spalten enthalten 1094 gültige Einträge. Alle Spalten enthalten Floats.

```python
data.describe()
```

```python
import plotly.express as px

fig = px.box(data, title='Windenergie in Deutschland von 2017 bis 2019')
fig.show()
```

Es nicht sinnvoll, einen gemeinsamen Boxplot zu verwenden. Die Unterschiede der
Messwerte sind zu groß. Beispielsweise kann die Temperatur gar nicht mehr
abgelesen werden. Außerdem haben die Spalten verschiedene Einheiten und sind
daher gar nicht direkt vergleichbar.

Im Folgenden werden daher die statistischen Kennzahlen der drei Eigenschaften
einzeln visualisiert.

```python
fig = px.box(data, y = 'wind_generation_actual', title='Windenergie in Deutschland von 2017 bis 2019')
fig.show()
```

Der Median liegt einigermaßen mittig zwischen dem Q1 und dem Q3-Quartil, jedoch gibt es einige Ausreißer nach oben. Die Ausreißer führen auch dazu, dass der Mittelwert 305819 MW über dem Median von 254332 MW liegt.

```python
fig = px.box(data, y = 'wind_capacity', title='Windenergie in Deutschland von 2017 bis 2019')
fig.show()
```

Bei der Windkapazität gibt es keine Ausreißer. Der Median ist nicht mittig zwischen Q1 und Q3, stimmt aber ganz gut mit dem Mittelwert von 45066 MW überein.

```python
fig = px.box(data, y = 'temperature', title='Windenergie in Deutschland von 2017 bis 2019')
fig.show()
```

Die Temperatur ist gleichmäßig verteilt, der Median liegt mittig zwischen Q1 und
Q3 und passt auch sehr gut zum Mittelwert 10.5 Grad Celsius.

Als nächstes visualisieren wir den zeitlichen Verlauf der drei Eigenschaften.

```python
fig = px.scatter(data, y = 'wind_generation_actual')
fig.show()
```

Die Winderzeugung ist starken Schwankungen unterworfen. Dabei sind die
Schwankungen in den Sommermonaten kleiner als in den Wintermonaten.

```python
fig = px.scatter(data, y = 'wind_capacity')
fig.show()
```

Die Windkapazität wurde seit Januar 2017 beständig ausgebaut. Im Januar 2017
betrug sie nur 37149 MW, im Dezember 2019 waren es 50542 MW. Das ist eine
Steigerung um 36 %.

```python
fig = px.scatter(data, y = 'temperature')
fig.show()
```

Wie erwartet schwanken die Temperaturen periodisch mit den Jahreszeiten. In den
Wintermonaten sind die Temperaturen niedrig, in den Monaten Juli / August am
höchsten.

Als nächstes visualisieren wir die Scattermatrix.

```python
fig = px.scatter_matrix(data)
fig.show()
```

Bei der Kombination wind_generation_actual - wind_capacity ist kein funktionaler
Zusammenhang erkennbar. Bei der Kombination wind_capacity - temperature sieht es
nach einem Zusammenhang aus, aber die Temperatur kann nicht vom Ausbau der
Infrastruktur in Deutschland abhängen und umgekehrt. Bleibt noch die Kombination
temperature - wind_generation_actual. Scheinbar wird bei Temperaturen von
ungefähr 5 Grad Celsius am meisten Windenergie erzeugt. Bei kälteren
Temperaturen (Minusgrade) oder höheren Temperaturen (über 20 Grad Celsius) wird
weniger als die Hälfte des Maximalwertes erzeugt. 
````

```{admonition} Übung 5.2
:class: tip

Importieren Sie den Datensatz 'kaggle_ikea.csv' und verschaffen Sie sich einen
Überblick über die Daten (Quelle: [Kaggle](https://www.kaggle.com/datasets/thedevastator/ikea-product)).

In welche verschiedenen Kategorien (category) sind die IKEA-Artikel unterteilt?
Erstellen Sie für jede Kategorie einen Boxplot der Verkaufspreise und ziehen Sie 
Schlussfolgerungen daraus.

Lassen Sie für jede Kategorie den durchschnittlichen Preis dieser Kategorie als
Barplot visualisieren. Lesen Sie danach ab: welche Kategorie hat den geringsten
Durchschnittspreis?

Lassen Sie für diese Kategorie die Anzahl der Artikel bestimmen. Visualisieren
Sie dann den Preis in Abhängigkeit des Namens als Scatterplot. Bei welchem Namen
gibt es die größte Spannweite an Verkaufspreisen? Welches ist der teuerste
Artikel (ID?) in dieser Kategorie und wie wird er beschrieben?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

data = pd.read_csv('kaggle_ikea.csv', index_col=0)
data.info()
```

Die Daten bestehen aus 3694 Einträgen mit Waren, die von Ikea verkauft werden.
Die Gegenstände werden durch 12 Eigenschaften beschrieben. Dabei sind die
meisten Eigenschaften Objekte (name, category, old_price, link, other_colors,
short_description, designer). Numerische Eigenschaften sind price, depth, height
und width. Ob der Gegenstand auch Online gekauft werden kann, verbirgt sich in
der Spalte sellable_online mit boolschen Werten. Nicht alle Einträge sind
gültig. Bei den Eigenschaften depth, height und width fehlen Angaben.

```python
data.head(10)
```

```python
data.describe()
```

Bei den Daten ist vor allem der Preis interessant. Der billigste Artikel kostet
3 Euro, der teuerste Artikel 9585 Euro. Aber 50 % aller Artikel kosten weniger
als 544 Euro. Die Größenangaben sind nicht vollständig und etwas schwieriger zu
interpretieren. Offensichtlich ist 1 cm die kleinste Größenangabe bei allen drei
Angaben und 2.57 m, 7 m und 4.2 m die maximalen Größen bei Tiefe, Höhe und
Breite.

```python
data['category'].unique()
```

Es gibt 17 verschiedene Kategorien. 

Als nächstes werden die Verkaufspreise pro Kategorie statistisch ausgewertet.

```python
categories = data.groupby('category')
categories['price'].describe()
```

```python
import plotly.express as px

fig1 = px.box(data, x = 'category', y = 'price')
fig1.show()
```

Am teuersten sind Artikel in der Kategorie Betten (Beds) und Sofas (Sofas &
Armchairs). Es ist interessant zu sehen, dass in beiden Kategorien der teuerste
Preis 9585 EUR ist. Vielleicht ist das ein Artikel, der sowohl als Bett als auch
Sofa kategorisiert wurde, ein Schlafsofa zum Beispiel. 

```python
fig = px.bar(categories['price'].mean(), title='Durchnittspreis IKEA',
             labels={'value': 'Preis in Euro', 'variable': 'Legende'})
fig.show()
```

Den geringsten Durchschnittspreis hat die Kategorie Kindermöbel (Children's furniture).

```python
children_furnitures = categories.get_group("Children's furniture")
children_furnitures.info()
```

In der Kategorie Kindermöbel werden 124 Artikel verkauft.

```python
fig = px.scatter(children_furnitures, x = 'name', y = 'price')
fig.show()
```

Die größte Spannweite an Preisen gibt es bei Artikel mit dem Namen Stuva bzw.
Fritids. Er kostet 1545 EUR.

```python
most_expensive_children_furniture = children_furnitures[ children_furnitures['price'] == 1545] 
most_expensive_children_furniture.head()
```

Bei dem teuersten Möbel in der Kategorie der Kindermöbel handelt es sich um
einen Schrank mit der Artikel-ID "19275075" und der Beschreibung "Wardrobe,
120x50x192 cm".

```python
print(most_expensive_children_furniture['link'])
```
````

```{admonition} Übung 5.3
:class: tip
Lesen Sie die csv-Datei
'statistic_id1301764_formel1-fahrerwertung-saison-2022.csv' (Formel 1
Fahrerwertung, Stand 30.10.2022, Quelle:
https://de.statista.com/statistik/daten/studie/1301764/umfrage/formel-1-wm-stand/)
ein. 

Führen Sie eine statistische Datenanalyse inklusive Visualisierung durch.
Visualisieren Sie zusätzlich die Fahrerwertung.

Hinweis: Diese Übung ist bewusst offener formuliert. Nutzen Sie die Methoden aus
den vorherigen Kapiteln bzw. Übungen selbstständig.
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

data = pd.read_csv('statistic_id1301764_formel1-fahrerwertung-saison-2022.csv', index_col=0, skiprows=2)
data.info()
```

Die Datei enthält 21 Zeilen mit den Fahrernamen und eine Spalte mit der Wertung. Der Datentyp der Spalte Wertung ist Integer. Alle Einträge sind gültig. 

```python
data.head()
```

Statistische Analyse:

```python
data.describe()
```

```python
import plotly.express as px

fig = px.box(data, title='Formel-1-Saison 2022', labels={'value': 'Punkte', 'variable': ''})
fig.show()
```

Der Mittelwert der erreichten Punkte in der Fahrerwertung liegt bei 100.5
Punkten, der Median jedoch bei 36 Punkten. Es liegt also eine deutlich schiefe
Verteilung der Punkte vor. 50 % der Fahrer haben weniger als 36 Punkte erreicht,
die besten 25 % der Fahrer haben mehr als 213 Punkte. Diese ungleiche Verteilung
der Punkte zeigt sich auch in einer hohen Standardabweichung von 120 Punkten,
die größer als der Mittelwert ist.

Verteilung der Wertung auf die einzelnen Fahrer:

```python
fig = px.bar(data, title='Formel-1-Saison 2022',
             labels={'value':'Punkte', 'variable': 'Legende'})
fig.show()
```

Die Visualisierung der Wertung der Fahrer zeigt, das Max Verstappen mit 416 Punkten die Saison gewonnen hat. Dabei hatte er einen deutlichen Vorsprung vor Sergio Perez, der nur 280 Punkte erreichte. Somit hat der Zweitplatzierte nur ca. 67 % der Punkte von Verstappen erreicht.
````
