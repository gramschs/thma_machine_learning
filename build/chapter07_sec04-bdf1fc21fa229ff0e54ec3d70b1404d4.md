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

## Aufgabe 7.1 Bevölkerungszahlen in Deutschland

In dieser Aufgabe betrachten wir den Datensatz `population_germany.csv`. Führen
Sie zuerst eine explorative Datenanalyse durch. Geben Sie dann mit Hilfe eines
Entscheidungsbaumes (Decision Tree) und eines linearen Regressionsmodells
jeweils eine Prognose ab, wie viele Menschen in Deutschland im Jahr 2100 leben
werden. Unterscheiden sich die beiden Prognosen?

```{admonition} Überblick über die Daten
:class: tip 

Laden Sie die csv-Datei `population_germany.csv`. Welche Daten enthält die
Datei? Wie viele Datenpunkte sind vorhanden? Wie viele und welche Merkmale gibt
es? Sind die Daten vollständig? Welche Datentypen haben die Merkmale?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd

daten = pd.read_csv('population_germany.csv')
daten.info()
```

Es liegen 222 Einträge vor und 4 Merkmale: Region, Code, Jahr, Population. Die
ersten beiden Eigenschaften Region und Code sind Objects. Die Eigenschaften Jahr
und Population sind Integer.
````

```{admonition} Statistik der numerischen Daten
:class: tip 

Erstellen Sie eine Übersicht der statistischen Kennzahlen für die numerischen
Daten. Visualisieren Sie anschließend die statistischen Kennzahlen mit Boxplots.
Interpretieren Sie die statistischen Kennzahlen. Gibt es Ausreißer? Sind die
Werte plausibel?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
daten.describe()
```

Das erste Merkmal ist das Jahr. Wir erhalten zwar eine Statistik für die
Jahreszahlen und können ablesen, dass 50 % der Jahre vor 1910 liegen, aber
sinnvoll ist die Statistik für die Jahreszahlen nicht. Eigentlich sind die
Jahreszahlen für diese Fragestellung ein Index und werden daher nicht weiter
betrachtet.

Das zweite numerische Merkmal sind die Bevölkerungszahlen. Die minimale
Population sind 18 Mio. Einwohner, die maximale Einwohnerzahl 83.9 Mio.
Einwohner. Der Mittelwert von 55.4 Mio. Einwohner ist deutlich unter dem Median
von 62.4 Mio. Einwohner. Es gibt einige Jahre mit hohen Bevölkerungszahlen, die 
den Mittelwert nach oben ziehen. Die Verteilung könnte rechtsschief sein. Das
bestätigt auch der Boxplot.

```python
import plotly.express as px 

fig = px.box(daten['Population'],
    labels={'variable':'', 'value': 'Einwohnerzahl'},
    title='Population in Deutschland')
fig.show()
```

Der Boxplot zeigt keine Ausreißer. Insgesamt erscheinen die Werte plausibel.
````

```{admonition} Statistik der kategorialen Daten
:class: tip 

Erstellen Sie eine Übersicht der Häufigkeiten für die kategorialen Daten.
Visualisieren Sie anschließend die Häufigkeiten mit Barplots. Interpretieren Sie
die Häufigkeiten. Sind die Werte plausibel?
```

````{admonition} Lösung
:class: tip
:class: dropdown

Als erstes schauen wir uns an, was sich hinter den Objekten verbirgt.

```python
daten.head(10)
```

Bei Region scheinen Länderbezeichnungen (Strings) aufgelistet zu werden und der
Code scheint ein Länderkürzel (String) zu beinhalten. Bei den ersten 10
Einträgen findet sich bei Region nur `'Germany'` und bei Code nur `'DEU'`. Mit
`.unique()` überprüfen wir, wie viele verschiedene Einträge es überhaupt gibt.
Sind diese Werte als kategoriale Daten einzuordnen?

```python
for merkmal in ['Region', 'Code']:
    einzigartige_werte = daten[merkmal].unique()
    anzahl = len(einzigartige_werte)
    print(f'Das Merkmal {merkmal} hat {anzahl} einzigartige Einträge.')
```

Nein, in beiden Fällen gibt es nur einen einzigen Wert, nämlich `'Germany'` und
`'DEU'`. Wir können diese beiden Merkmale im Folgenden ignorieren und brauchen
daher auch keinen Barplot für die Häufigkeiten.
````

```{admonition} Korrelationen
:class: tip
Erstellen Sie einen Scatterplot mit dem Jahr auf der x-Achse und der Population
auf der y-Achse. Beschriften Sie den Scatterplot sinnvoll. Vermuten Sie einen
Zusammenhang zwischen Jahr und Bevölkerung? Was fällt Ihnen generell auf? Können
Sie die Besonderheiten mit Geschichtswissen erklären?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
fig = px.scatter(daten, x = 'Jahr', y = 'Population',
    title='Population in Deutschland')
fig.show()
```

Es scheint einen linearen Zusammenhang zu geben.

Die Bevölkerung ist seit 1800 gewachsen. Zu Beginn der 1910er Jahr gibt es einen
Bevölkerungsrückgang bis 1919/1920, dann steigt die Bevölkerung wieder an. Auch
in den 1940er Jahren kam es zu einem Bevölkerungsrückgang. In beiden Fällen
können wir vermuten, dass diese mit den beiden Weltkriegen zu tun hat. Aber auch
in späteren Zeiten kam es trotz des langfristigen Wachstumstrends immer
wieder zu einem kurzen Bevölkerungsrückgang, z.B. um 1984 oder 2010.
````

```{admonition} Lineares Regressionsmodell
:class: tip

Adaptieren Sie die Daten. Wählen Sie als Input das Jahr und als Output die
Population. Trainieren Sie ein lineares Regressionsmodell und lassen Sie den
R²-Score berechnen und ausgeben.
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
X = daten[['Jahr']]
y = daten['Population']

from sklearn.linear_model import LinearRegression

modell_linear = LinearRegression()
modell_linear.fit(X,y)
r2_score_lineares_modell = modell_linear.score(X,y)
print(f'R2-Score lineares Modell: {r2_score_lineares_modell:.2f}')
```

Der R²-Score ist mit 0.97 sehr gut.
````

```{admonition} Entscheidungsbaum/Decision Tree
:class: tip
Lassen Sie nun einen Entscheidungsbaum/Decision Tree trainieren und den R²-Score
ausgeben. 

Tipp: Das Scikit-Learn-Modell heißt DecisionTreeRegressor.
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
from sklearn.tree import DecisionTreeRegressor

modell_entscheidungsbaum = DecisionTreeRegressor()
modell_entscheidungsbaum.fit(X,y)
r2_score_entscheidungsbaum = modell_entscheidungsbaum.score(X,y)
print(f'R2-Score Entscheidungsbaum: {r2_score_entscheidungsbaum:.2f}')
```
Der R²-Score ist mit 1.0 scheinbar perfekt, aber das ist ein Zeichen für
Overfitting auf den Trainingsdaten.
````

````{admonition} Bewertung und Prognose
:class: tip

Für welches Modell würden Sie sich entscheiden? Begründen Sie Ihre Wahl. 

Lassen Sie dann sowohl das lineare Regressionsmodell als auch den
Entscheidungsbaum die Populationen von 1800 bis 2100 prognostizieren. Verwenden
Sie dazu den folgenden Datensatz:

```python
prognosedaten = pd.DataFrame({
    'Jahr': range(1800, 2101)
})
```

Visualisieren Sie die Prognosen zusammen mit den gemessenen Populationen in
einem gemeinsamen Scatterplot.


Tipp: Mit 

`fig.add_scatter(x = prognosedaten['Jahr'],y = prognose_linear, name='lineare Regression')``

können Sie einen weiteren Scatterplot zu einem schon existierenden (hier in der
Variable `fig` gespeichert) hinzufügen.

Welches Modell würden Sie nach der Visualisierung bevorzugen?
````

````{admonition} Lösung
:class: tip
:class: dropdown
Zunächst einmal erscheint der Entscheidungsbaum besser zu sein als das lineare
Regressionsmodell, da der R²-Score besser ist. Daher könnte man sich für einen
Entscheidungsbaum/Decision Tree entscheiden.

```python
prognosedaten = pd.DataFrame({
    'Jahr': range(1800, 2101)
})

prognose_linear = modell_linear.predict(prognosedaten)
prognose_entscheidungsbaum = modell_entscheidungsbaum.predict(prognosedaten)

fig = px.scatter(daten, x = 'Jahr', y = 'Population', title='Vergleich der Modelle')
fig.add_scatter(x = prognosedaten['Jahr'],y = prognose_linear, name='lineare Regression')
fig.add_scatter(x = prognosedaten['Jahr'],y = prognose_entscheidungsbaum, name='Entscheidungsbaum')
fig.show()
```

Die Visualisierung der beiden Modelle zeigt zunächst die bessere Performance des
Entscheidungsbaumes. Am Ende lernt der Entscheidungsbaum jeden Punkt auswendig
und liefert daher für die bekannten Daten die perfekte Prognose. Er ist jedoch
nicht in der Lage, auf unbekannte Daten (also Zeitraum 2022 bis 2100) zu
verallgemeinern. Es liegt Overfitting vor. Daher ist das lineare
Regressionsmodell zu bevorzugen.

```python
print(f'Prognose im Jahr 2100: {prognose_linear[-1]:.1f}')
```
````

## Aufgabe 7.2 Marketing-Budget für soziale Medien und Zeitungen

Eine Firma erhebt statistische Daten zu ihren Verkaufszahlen (angegeben in
Tausend US-Dollar) abhängig von dem eingesetzten Marketing-Budget in den
jeweiligen Sozialen Medien (Quelle siehe
<https://www.kaggle.com/datasets/fayejavad/marketing-linear-multiple-regression>).

Erstellen Sie eine explorative Datenanalyse (EDA). Trainieren Sie dann
ML-Modelle und bewerten Sie, bei welchem sozialen Medium sich am ehesten lohnt
zu investieren.

```{admonition} Überblick über die Daten
:class: tip 
Laden Sie die csv-Datei `marketing_data.csv`. Welche Daten enthält die
Datei? Wie viele Datenpunkte sind vorhanden? Wie viele und welche Merkmale gibt
es? Sind die Daten vollständig? Welche Datentypen haben die Merkmale?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
import pandas as pd 

daten = pd.read_csv('marketing_data.csv')
daten.info()
```

Die Daten enthalten 171 Einträge, die von 0 bis 170 indiziert sind. Es gibt vier
Eigenschaften, die alle als Floats gespeichert sind. Alle Einträge sind gültig.
Aufgrund der Aufgabenstellung ist klar, dass die ersten drei Eigenschaften das
investierte Marketing-Budget in die sozialen Medien YouTube, Facebook und
Newspaper darstellen. Die Spalte 'sales' repräsentiert dahingehend die Wirkung
der Marketing-Budgets. Wir werfen noch einen Blick auf die ersten 10 Zeilen der 
Tabelle:

```python
daten.head(10)
```
````

```{admonition} Statistik der numerischen Daten
:class: tip 

Erstellen Sie eine Übersicht der statistischen Kennzahlen für die numerischen
Daten. Visualisieren Sie anschließend die statistischen Kennzahlen mit Boxplots.
Interpretieren Sie die statistischen Kennzahlen. Gibt es Ausreißer? Sind die
Werte plausibel?
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
daten.describe()
```

Als nächstes visualisieren wir die statistischen Kennzahlen des
Marketing-Budgets.

```python
import plotly.express as px

X = daten.loc[:, 'youtube' : 'newspaper']
fig = px.box(X,
             title='Marketing-Budget',
             labels={'variable': 'Kategorie', 'value': 'Tsd. US-Dollar'})

fig.show()
```

Mit großem Abstand wird am meisten in das Marketing bei YouTube investiert. Im
Mittel 178 Tsd. US-Dollar, wohingegen nur 27 Tsd. US-Dollar in Facebook und 35
Tsd. US-Dollar in Zeitungen (Newspaper) investiert werden. Bei allen drei
Kategorien ist der Median ungefähr mittig zwischen Q1 und Q3. Bei der Kategorie
Newspaper gibt es einen Ausreißer.

Zuletzt betrachten wir noch den Boxplot der Wirkung 'sales'.

```python
import plotly.express as px

y = daten['sales']
fig = px.box(y,
             title='Verkäufe',
             labels={'variable': 'Kategorie', 'value': 'Tsd. US-Dollar'})

fig.show()
```

Auch bei den Verkäufen gibt es keine Ausreißer. Der Median liegt näher an Q1 als
an Q3 und unterhalb des Mittelwertes von 16 Tsd. US-Dollar.
````

```{admonition} Korrelationen
:class: tip
Erstellen Sie zuerst eine Scattermatrix, um Zusammenhänge zwischen den Merkmalen
zu analysieren. Lassen Sie dann die Korrelationsmatrix als Heatmap anzeigen und
interpretieren Sie das Ergebnis.
```

````{admonition} Lösung
:class: tip
:class: dropdown

Alle drei Merkmale YouTube, Facebook und Newspaper könnten eine Wirkung auf die
Verkaufszahlen haben. Am einfachsten ist zunächst die Visualisierung als
Scattermatrix.

```python
fig = px.scatter_matrix(daten)
fig.show()
```

YouTube und Facebook scheinen eine stärke lineare Wirkung auf die Verkaufszahlen
zu haben als die Zeitungen. Genaueres zeigt uns die Korrelationsmatrix:

```python
korrelationsmatrix = daten.corr()

fig = px.imshow(korrelationsmatrix, text_auto=True)
fig.show()
```

Alle drei sozialen Medien sind positiv korreliert, also je mehr
Marketing-Budget, desto höhere Verkaufszahlen. Am stärksten korreliert YouTube
gefolgt von Facebook. Newspaper haben den geringsten Einfluss.
````

```{admonition} Lineares Regressionsmodell
:class: tip

Trainieren Sie drei lineare Regressinsmodelle, jeweils mit einem anderen Merkmal
als Input, d.h. mit jeweils `youtube`, `facebook`, `newspaper`. Adaptieren Sie
dazu passend die Daten. Lassen Sie jeweils den R²-Score berechnen und ausgeben.
```

````{admonition} Lösung
:class: tip
:class: dropdown

Wir trainieren zunächst drei einzelne lineare
Regressionsmodelle und bestimmen den jeweiligen R²-Score.

```python
from sklearn.linear_model import LinearRegression

y = daten['sales']
for merkmal in ['youtube', 'facebook', 'newspaper']:
    X = daten[[merkmal]]
    modell = LinearRegression()
    modell.fit(X,y)
    r2_score = modell.score(X,y)
    print(f'Input: {merkmal}, R2-Score = {r2_score:.2f}')
```

Wie erwartet sind die R²-Scores bei YouTube besser als bei Facebook und den
Newspapern, da dort ein lineares Modell besser passt.
````

```{admonition} Finales Modell
:class: tip
Trainieren Sie nun als finales Modell ein multiples Regressionsmodell und
stellen Sie mit den Koeffizienten (Gewichten) und dem Achsenabschnitt (Bias) die
dazugehörige Modellfunktion auf.
```

````{admonition} Lösung
:class: tip
:class: dropdown

```python
X = daten[['youtube', 'facebook', 'newspaper']]
y = daten['sales']

modell_multiple_regression = LinearRegression()
modell_multiple_regression.fit(X,y)
r2_score = modell_multiple_regression.score(X,y)

print(f'R2-Score multiples Regressionsmodell: {r2_score:.2f}')

print(f'Koeffizienten: {modell_multiple_regression.coef_}')
print(f'Achsenabschnitt: {modell_multiple_regression.intercept_:.4f}')
```

Modellfunktion: 

$$y = 0.0452\cdot x_{\text{youtube}} + 0.1884\cdot x_{\text{facebook}}
+ 0.0043\cdot x_{\text{newspaper}} + 3.5059.$$
````
