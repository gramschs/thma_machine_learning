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

Der California-Housing-Datensatz ist ein klassischer Datensatz für
Regressionsaufgaben im maschinellen Lernen. Er wurde 1990 aus dem US-Census
extrahiert und enthält Daten zu **Wohnblöcken** in Kalifornien. Ein Wohnblock
ist eine statistische Einheit mit typischerweise 600-3000 Einwohnern. Die
Merkmale sind Durchschnittswerte für alle Haushalte in diesem Block. Das Ziel
ist, den Median-Hauswert (in US-Dollar) vorherzusagen.

```{admonition} Überblick über die Daten
:class: tip
Laden Sie den Datensatz `california_housing_DE.csv`.

* Welche Daten enthält der Datensatz?
* Wie viele Datenpunkte und Merkmale gibt es?
* Sind die Daten vollständig?
* Welche Datentypen haben die Merkmale?
* Gibt es Merkmale mit unerwarteten Datentypen?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import pandas as pd

# Laden der Daten und erste Informationen
daten = pd.read_csv('california_housing_DE.csv')
daten.info()

# Check der Vollständigkeit
print(daten.isnull().sum())

# Inhalt der ersten 10 Zeilen
daten.head(10)
```
Der Datensatz enthält 20.640 Datenpunkte (Wohnblöcke) mit 10 Merkmalen. Die Daten
sind nicht vollständig, denn beim Merkmal Schlafzimmer fehlen 207 Einträge. Die
übrigen Merkmale sind vollständig. Die Datentypen der Merkmale sind wie folgt:

* Laenge --> float64,
* Breite --> float64,
* Alter --> float64,
* Zimmer --> float64,
* Schlafzimmer --> float64,
* Bevoelkerung --> float64,
* Haushalte --> float64,
* Einkommen --> float64,
* Hauswert --> float64 und
* Kuestennaehe --> object.

Die Datentypen sind für die Merkmale angemessen.
````

```{admonition} Datenvorverarbeitung
:class: tip
Der Datensatz enthält fehlende Werte in der Spalte `Schlafzimmer`. Entscheiden
Sie, wie Sie diese behandeln möchten. Begründen Sie Ihre Wahl. Führen Sie die
gewählte Methode durch.
```

````{admonition} Lösung
:class: tip
:class: dropdown
Es fehlen 207 Werte (ca. 1 \% des Datensatzes). Da es sich um eine numerische
Spalte handelt und der Anteil der fehlenden Werte gering ist, ist eine
*Imputation mit dem Median* sinnvoll. Der Median ist robust gegenüber Ausreißern
und verändert die Verteilung der Daten kaum.

Die Imputation führen wir wie folgt durch:

```python
# Median berechnen
median_schlafzimmer = daten['Schlafzimmer'].median()
print(f'Median Schlafzimmer: {median_schlafzimmer:.1f} ')

# fehlende Werte ersetzen
daten['Schlafzimmer'] = daten['Schlafzimmer'].fillna(median_schlafzimmer)

# Überprüfen, ob keine fehlenden Werte mehr vorhanden sind
print(f"Fehlende Werte nach Imputation: {daten['Schlafzimmer'].isna().sum()}")
```
Nach der Imputation sind keine fehlenden Werte mehr in der Spalte `Schlafzimmer`
vorhanden.

Alternativen wären: Zeilen löschen (bei nur 1 % vertretbar), Mittelwert (aber
weniger robust) oder komplexere Imputation mit ML-Modellen (hier übertrieben
aufwendig).
````

```{admonition} Statistik der numerischen Daten
:class: tip 
Erstellen Sie eine Übersicht der statistischen Kennzahlen für die numerischen
Daten. Interpretieren Sie die statistischen Kennzahlen. Gibt es Auffälligkeiten?
Sind die Werte plausibel?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import plotly.express as px

# Laenge, Breite wird weggelassen, da die Positionen weniger gut statistisch
# interpretiert werden kann; Hauswert wird gesondert untersucht, da es die 
# Zielgröße ist 
fig = px.box(daten.loc[:, 'Alter':'Einkommen'],
             labels={'variable': 'Merkmal', 'value': 'Wert'})

fig.show()

# Statistik für alle Merkmale und Zielgröße
daten.describe()
```
Beobachtungen:

* Alter: reicht von 1 bis 52 Jahren, durchschnittlich 28.6 Jahre
* Zimmer: sehr große Spannweite (2 bis 39320), Median (2127) deutlich unter
  Mittelwert (2635), d.h. rechtsschiefe Verteilung, Ausreißer vorhanden
* Schlafzimmer: ähnliches Bild wie bei Zimmer
* Bevoelkerung: Maximum von 35682 deutet auf sehr große Bezirke hin
* Einkommen: reicht von 0.5 bis 15 (Einheit: 10.000 USD)
* Hauswert: Maximum von 500001 ist auffällig, vermutlich werden Werte über
  500.000 USD gekappt

Die Werte erscheinen grundsätzlich plausibel, zeigen aber deutliche Ausreißer.
````

```{admonition} Statistik der kategorialen Merkmale
:class: tip 
Wie viele Beobachtungen gibt es pro Kategorie in Küstennähe? Visualisieren
Sie die Verteilung mit einem Balkendiagramm. Ist der Datensatz ausgewogen?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
haeufigkeiten = daten['Kuestennaehe'].value_counts()
print(haeufigkeiten)

fig = px.bar(x=haeufigkeiten.index, y=haeufigkeiten.values,
             labels={'x': 'Küstennähe', 'y': 'Anzahl'},
             title='Verteilung der Kuestennähe-Kategorien')
fig.show()
```
Der Datensatz ist nicht ausgewogen. Die Kategorie 'weniger_als_1h_zum_Ozean'
dominiert mit über 9000 Einträgen, gefolgt von 'Binnenland' mit über 6000
Einträgen. 'nahe_Bucht' und 'nahe_Ozean' haben deutlich weniger Einträge, und
'Insel' ist mit nur 5 Beobachtungen extrem unterrepräsentiert.
````

```{admonition} Analyse der Zielgröße
:class: tip 
Visualisieren Sie die Verteilung der Zielgröße `Hauswert` mit einem
Histogramm. Ist die Verteilung normalverteilt? Gibt es Auffälligkeiten?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
fig = px.histogram(daten, x='Hauswert', 
                   nbins=50,
                   title='Verteilung der Hauswerte')
fig.update_layout(
    yaxis_title='Anzahl',
    xaxis_title='Hauswert (USD)'
)
fig.show()
```
Die Verteilung ist rechtsschief und nicht normalverteilt. Auffällig ist der
große Balken bei 500.001 USD. Hier wurden offensichtlich alle Werte über 500.000
USD auf diesen Maximalwert gesetzt. Dies ist eine Besonderheit des Datensatzes,
die man bei der Interpretation der Ergebnisse berücksichtigen sollte.
````

```{admonition} Korrelationen
:class: tip
Erstellen Sie eine Korrelationsmatrix für alle numerischen Variablen und
visualisieren Sie diese als Heatmap. Welche Merkmale korrelieren am stärksten
mit dem Hauswert? Gibt es starke Korrelationen zwischen den Merkmalen?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
numerische_daten = daten.loc[:, 'Laenge' : 'Hauswert']
korrelation = numerische_daten.corr()

fig = px.imshow(korrelation, 
                text_auto='.2f',
                aspect='auto',
                labels={'color': 'Korrelation'},
                title='Korrelationsmatrix')
fig.show()
```
Eine häufig verwendete Faustregel für die Interpretation des
Korrelationskoeffizienten r ist

* |r| < 0.3: schwacher Zusammenhang
* 0.3 ≤ |r| < 0.7: mittelstarker Zusammenhang
* |r| ≥ 0.7: starker Zusammenhang

Das Einkommen korreliert am stärksten mit dem Hauswert (r = 0.69). Alle anderen
Merkmale zeigen keine bzw. nur einen sehr schwachen Zusammenhang zum Hauswert
(Werte zwischen -0.14 bis 0.13).

Bei den Merkmalen untereinander gibt es starke Korrelationen zwischen den
Zimmern, Schlafzimmern, Bevölkerung und Haushalten (0.86 bis 0.93).
````

```{admonition} Analyse der Positionen
:class: tip
Erstellen Sie einen Scatterplot mit Längengrad (x-Achse) und Breitengrad
(y-Achse). Färben Sie die Punkte nach Hauswert ein. Erkennen Sie geografische
Muster?

Tipp: Benutzen Sie das optionale Argument `opacity=0.5`, damit knapp
übereinanderliegende Punkte dennoch sichtbar werden.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
fig = px.scatter(daten, 
                 x='Laenge', 
                 y='Breite',
                 color='Hauswert',
                 labels={'Laenge': 'Längengrad',
                        'Breite': 'Breitengrad',
                        'Hauswert': 'Hauswert (USD)'},
                 title='Geografische Verteilung der Hauswerte',
                 opacity=0.5
                )
fig.show()
```
Die Form von Kalifornien ist deutlich erkennbar. Die höchsten Hauswerte sind in
den Küstenregionen (Vergleich mit Atlas: San Francisco Bay Area und Los
Angeles/San Diego). Im Binnenland sind die Hauswerte niedriger.

Die geografische Lage ist ein wichtiger Einflussfaktor auf den Hauswert. Der
Einfluss ist allerdings nichtlinear, denn sonst hätten wir in der
Korrelationsmatrix nicht r = -0.05 für die Laenge und r = -0.14 für die Breite
erhalten.
````

```{admonition} Neue Merkmale
:class: tip
Wir haben festgestellt, dass die Merkmale Zimmer, Schlafzimmer, Bevölkerung und
Haushalte stark linear korreliert sind.

Erstellen Sie folgende neue Merkmale:
* Zimmer pro Haushalt
* Schlafzimmer pro gesamte Anzahl Zimmer  
* Personen pro Haushalt

Dürfen die drei Divisionen durchgeführt werden? Berechnen Sie die Korrelation
dieser neuen Merkmale mit der Zielgröße.
```

````{admonition} Lösung
:class: tip
:class: dropdown
Die statische Analyse ergab, dass das Minimum der Haushalte 1 ist und die
minimale Anzahl der Zimmer 2. Null kommt nicht vor, so dass alle drei Divisionen
durchgeführt werden können.
```python
# Erstellung neue Merkmale als zusätzliche Spalten
daten['Zimmer_pro_Haushalt'] = daten['Zimmer'] / daten['Haushalte']
daten['Schlafzimmer_Anteil'] = daten['Schlafzimmer'] / daten['Zimmer']
daten['Personen_pro_Haushalt'] = daten['Bevoelkerung'] / daten['Haushalte']

# Auswahl der Merkmale für Korrelationsmatrix
neue_daten = daten.loc[:, ['Zimmer_pro_Haushalt', 'Schlafzimmer_Anteil', 'Personen_pro_Haushalt', 'Hauswert' ]]

# Berechnung und Anzeige Korrelationsmatrix
neue_korrelationen = neue_daten.corr()
print(neue_korrelationen)

# Visualisierung Korrelationsmatrix als Heatmap
fig = px.imshow(neue_korrelationen, 
                text_auto='.2f',
                aspect='auto',
                labels={'color': 'Korrelation'},
                title='Neue Korrelationsmatrix')
fig.show()
```
Die neuen Merkmale zeigen stärkere Korrelationen als die ursprünglichen
Merkmale. Besonders der `Schlafzimmer_Anteil` könnte ein nützliches Merkmal zur
Prognose des Hauswertes sein.
````

```{admonition} Vorbereitung der Daten für das Training
:class: tip
Bereiten Sie die Daten für das maschinelle Lernen vor:

1. Kodieren Sie die kategoriale Variable Küstennähe mit One-Hot-Encoding.
2. Trennen Sie die Merkmale (Input X) und die Zielgröße (Output y).
3. Teilen Sie die Daten in Trainings- und Testdaten im Verhältnis 80:20 auf.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from sklearn.model_selection import train_test_split

# One-Hot-Encoding für Kuestennaehe
daten = pd.get_dummies(data=daten, columns=['Kuestennaehe'])
daten.head()

# Input und Output trennen
X = daten.drop('Hauswert', axis=1)
y = daten['Hauswert']

# Train-Test-Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f'Trainingsdaten: {X_train.shape[0]} Datenpunkte')
print(f'Testdaten: {X_test.shape[0]} Datenpunkte')
print(f'Anzahl Merkmale: {X_train.shape[1]}')
```
````

```{admonition} ML-Modell: Entscheidungsbaum
:class: tip
Trainieren Sie einen Entscheidungsbaum (DecisionTreeRegressor) auf den
Trainingsdaten. Berechnen Sie den R²-Score auf den Trainings- und Testdaten. Was
fällt Ihnen auf?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from sklearn.tree import DecisionTreeRegressor

modell_baum = DecisionTreeRegressor(random_state=42)
modell_baum.fit(X_train, y_train)

r2_train_baum = modell_baum.score(X_train, y_train)
r2_test_baum = modell_baum.score(X_test, y_test)

print(f'R²-Score Entscheidungsbaum (Training): {r2_train_baum:.2f}')
print(f'R²-Score Entscheidungsbaum (Test): {r2_test_baum:.2f}')
```
Der R²-Score auf den Trainingsdaten ist nahezu perfekt (1.0), während der Score
auf den Testdaten deutlich niedriger ist (0.6). Dies ist ein klares Zeichen für
Overfitting. Das Modell hat die Trainingsdaten auswendig gelernt, kann aber
schlecht auf neue Daten verallgemeinern.
````

```{admonition} ML-Modell: Random Forest
:class: tip

Trainieren Sie nun einen Random Forest (RandomForestRegressor) mit 100 Bäumen
auf denselben Daten. Berechnen Sie wieder die R²-Scores für Training und Test.
Wie unterscheiden sich die Ergebnisse vom einzelnen Entscheidungsbaum?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from sklearn.ensemble import RandomForestRegressor

modell_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modell_rf.fit(X_train, y_train)

r2_train_rf = modell_rf.score(X_train, y_train)
r2_test_rf = modell_rf.score(X_test, y_test)

print(f'R²-Score Random Forest (Training): {r2_train_rf:.2f}')
print(f'R²-Score Random Forest (Test): {r2_test_rf:.2f}')
```
Der Random Forest zeigt weniger Overfitting, er lässt sich besser
verallgemeinern. Der R²-Score für die Trainingsdaten ist etwas geringer (0.97),
aber dafür liegt der R²-Score der Testdaten bei 0.81. Die Differenz zwischen
dem Trainings- und dem Testscore ist kleiner.
````

```{admonition} Feature Importance
:class: tip
Lassen Sie sich die Feature Importance des Random-Forest-Modells ausgeben und
visualisieren Sie die Top 10 wichtigsten Merkmale als Balkendiagramm. Welche
Merkmale sind am wichtigsten für die Vorhersage?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Feature Importance extrahieren
importance = pd.DataFrame({
    'Merkmal': X_train.columns,
    'Feature Importance': modell_rf.feature_importances_
}).sort_values('Feature Importance', ascending=False)

# Top 10 visualisieren
top10 = importance.head(10)
fig = px.bar(top10, x='Feature Importance', y='Merkmal', orientation='h',
             title='Top 10 wichtigste Merkmale im Random Forest')
fig.update_yaxes(autorange="reversed")
fig.show()

print(top10)
```
Das wichtigste Merkmal aus den vorhandenen Merkmalen ist das Einkommen. Mit
etwas Abstand kommen dann die Lage (Küstennähe Binnenland) und die Anzahl der
Personen pro Haushalt.
````

```{admonition} ML-Modell: lineare Regression
:class: tip
Trainieren Sie nun ein lineares Regressionsmodell auf denselben Daten. Berechnen
Sie wieder die R²-Scores für Training und Test. Wie unterscheiden sich die
Ergebnisse vom den beiden vorherigen Modellen?

Wählen Sie dann ein finales Modell.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from sklearn.linear_model import LinearRegression

modell_lr = LinearRegression()
modell_lr.fit(X_train, y_train)

r2_train_lr = modell_lr.score(X_train, y_train)
r2_test_lr = modell_lr.score(X_test, y_test)

print(f'R²-Score lineare Regression (Training): {r2_train_lr:.2f}')
print(f'R²-Score lineare Regression (Test): {r2_test_lr:.2f}')
```
Der R²-Score der Trainingsdaten ist 0.66, für die Testdaten liegt er bei 0.58.
Auch wenn die Differenz zwischen Trainingsscore und Testscore klein ist und wohl
kein Overfitting vorliegt, sind die beiden Scores erheblich schlechter als beim
Random Forest (0.97 und 0.81). Daher verwenden wir den Random Forest als finales
Modell.
````
