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

Daten für die Übungen:

* [12612-0001_de.csv](https://nextcloud.frankfurt-university.de/s/bpZ8TZrzafKqAxq)
* [stromverbrauch_hessen.csv](https://nextcloud.frankfurt-university.de/s/ddfDzAAnJtJ4FZQ)

````{admonition} Übung 4.1 - Teilaufgabe a)
:class: tip

Schauen Sie sich die csv-Datei '12612-0001_de.csv' im Texteditor an. Der
Datensatz enthält die Lebendgeburten in Deutschland getrennt nach männlich,
weiblich und insgesamt (Quelle: [Statistisches
Bundesamt](https://www-genesis.destatis.de/datenbank/beta/statistic/12612/table/12612-0001)).

Ab welcher Zeile beginnen die Daten und in welcher Zeile enden sie? Importieren
Sie dann die Daten, wobei Kopf- und Fußzeilen beim Import übersprungen werden
sollen. Schlagen Sie dazu in der Dokumentation nach, wie Zeilen beim Lesen einer
csv-Datei Übersprungen werden. 

Tipp: Importieren Sie pandas mit dem üblichen Alias pd und führen Sie dann die
folgende Code-Zeile in einer Code-Zelle aus:

```none
pd.read_csv?
```

Welches Argument könnte für das Überspringen der Kopfzeilen stehen, welches für 
die Fußzeilen?

Welche Spalte ist als Index-Spalte geeignet? Setzen Sie eine passende
Spalte als Index. Verschaffen Sie sich einen Überblick über die Daten und
erstellen Sie eine Übersicht der statistischen Kennzahlen.
````

````{admonition} Lösung
:class: tip
:class: dropdown

```none
import pandas as pd

pd.read_csv?
```

```python
# 5 Kopfzeilen, 4 Fußzeilen; Jahreszahlen sind der Index
data = pd.read_csv('data/12612-0001_de.csv', skiprows=5, skipfooter=4, index_col=0)
data.info()
```

Der Datensatz enthält 3 Spalten: männlich, weiblich und insgesamt. Jede Spalte enthält 73 gültige Einträge. Jede Spalte enthält Integer.

```python
data.describe()
```
````

````{admonition} Übung 4.1 - Teilaufgabe b)
:class: tip
Kontrollieren Sie, ob die Spalte 'insgesamt' tatsächlich die Summe der beiden
Spalten 'männlich' und 'weiblich' ist. Bilden Sie dazu die Differenz 'insgesamt' - 
'männlich' - 'weiblich' und fügen Sie diese Differenz als neue Spalte dem
DataFrame hinzu. Wie lauten die statistischen Kennzahlen dieser Spalte? Welchen
Schluss ziehen Sie daraus? Haben Sie eine Vermutung, was passiert ist?
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
data['Differenz'] = data['insgesamt'] - data['männlich'] - data['weiblich']
data['Differenz'].describe()
```

Der Mittelwert ist 0.369863 und nicht wie erwartet 0. Das Maximum ist 17 und
nicht wie erwartet 0. Die Spalte 'insgesamt' ist daher nicht die Summe der
beiden Spalten 'männlich' und 'weiblich'. Normalerweise würden wir jetzt nach
den Jahren filtern, bei denen die Differenz nicht Null ist. Da wir das noch
nicht gelernt haben, visualisieren wir die Differenz als Scatterplot.

```python
import plotly.express as px

fig = px.scatter(data['Differenz'], 
                 title='Differenz "insgesamt - männlich - weiblich"',
                 labels={'value': 'Anzahl Geburten', 'variable': 'Legende'})
fig.show()
```

Die Abweichungen treten in den Jahren 2016 und 2017 auf. Das passt zu der
Bemerkung "Ab 2016: Die Gesamtzahl der Lebendgeborenen enthält auch die Fälle
mit unbestimmtem Geschlecht." Vermutlich ist die Zahl der Geburten 'insgesamt'
höher als die Summe der Geburten 'männlich' + 'weiblich', weil das Geschlecht
unbestimmt war.
````

````{admonition} Übung 4.1 - Teilaufgabe c)
:class: tip
Lassen Sie die statistischen Kennzahlen der Lebendgeburten 'männlich' und
'weiblich' als Boxplot visualisieren. Wurden mehr Jungen oder Mädchen geboren?
Liegt der Median mittig zwischen Q1 und Q3?
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import plotly.express as px

fig = px.box(data[['männlich','weiblich']],
             title='Statistische Kennzahlen der Lebendgeburten in Deutschland',
             labels={'value': 'Anzahl Geburten', 'variable': 'Geschlecht'})
fig.show()
```

Es wurden insgesamt mehr Jungen als Mädchen geboren. Bei beiden Geschlechtern
ist auffällig, dass der Median recht nahe bei dem Q1-Quantil liegt. Das deutet
auf eine asymmetrische Verteilung der Geburten über die Jahre hin.
Wahrscheinlich gibt es wenige Ausreißer mit geburtenstarken Jahrgängen.
````

````{admonition} Übung 4.1 - Teilaufgabe d)
:class: tip
Visualisieren Sie die Anzahl der männlichen und weiblichen Lebendgeburten pro
Jahr als Scatterplot. Beschriften Sie auch die Achsen und setzen Sie einen
Titel.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
fig = px.scatter(data[['männlich','weiblich']], 
                 title='Lebendgeborene in Deutschland',
                 labels={'value': 'Anzahl Lebendgeburten', 'variable': 'Geschlecht'})
fig.show()
```
````

````{admonition} Übung 4.2 - Teilaufgabe a)
:class: tip
Schauen Sie sich die csv-Datei 'stromverbrauch_hessen.csv' im Texteditor an.
Welche Daten enthält die Datei? Ab welcher Zeile beginnen die Daten und in
welcher Zeile enden sie? Importieren Sie dann die Daten, wobei Kopf- und
Fußzeilen beim Import übersprungen werden sollen. Welche Spalte ist als
Index-Spalte geeignet? Setzen Sie eine passende Spalte als Index. Verschaffen
Sie sich einen Überblick über die Daten und erstellen Sie eine Übersicht der
statistischen Kennzahlen. Interpretieren Sie den Stromverbrauch der
Verbrauchergruppen.
````

````{admonition} Lösung
:class: tip
:class: dropdown
Die Datei enthält den Stromverbrauch in Hessen 2000 bis 2021 nach
Verbrauchergruppen in Gigawattstunden. Es bietet sich an, das Jahr als Index zu
wählen.

```python
import pandas as pd

data = pd.read_csv('stromverbrauch_hessen.csv', skiprows=4, index_col=0)
```

```python
data.info()
```

Der Datensatz enthält 22 Zeilen mit dem Stromverbrauch von 2000 bis
einschließlich 2021. In den Spalten stehen der Stromverbrauch 

* der Industrie,
* des Verkehrs und
* der Haushalte, etc.
 
Alle Einträge sind gültig.   

```python
data.describe()
```

Der mittlere Stromverbrauch der Industrie ist ungefähr 10x so groß wie der
Stromverbrauch des Verkehrs. Nochmal doppelt soviel Strom verbrauchen aber
Haushalte, Gewerbe, etc.
````

````{admonition} Übung 4.2 - Teilaufgabe b)
:class: tip
Checken Sie, ob die Spalte 'insgesamt' tatsächlich die Summe der anderen Spalten ist. 
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
data['Differenz'] = data['insgesamt'] - data['Industrie'] - data['Verkehr'] - data['Haushalte, Gewerbe, Handel, Dienstleistungen und übrige Verbraucher']
data['Differenz'].describe()
```

Es gibt Abweichungen, Minimum und Maximum weichen jeweils um eine Gigawattstunde
ab. Angesichts der absoluten Werte wird es sich dabei um Rundungsfehler handeln
und bedarf keiner weiteren Maßnahmen.
````

````{admonition} Übung 4.2 - Teilaufgabe c)
:class: tip
Fertigen Sie Boxplots an und interpretieren Sie die statistischen Kennzahlen. 
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import plotly.express as px

fig = px.box(data['insgesamt'], 
             title='Stromverbrauch Hessen von 2000 bis 2021 (insgesamt)',
             labels={'value': 'Gigawattstunden', 'variable': ''})
fig.show()
```

Der Median liegt nahe am 25%-Quantil, die Verteilung des Stromverbrauchs der
einzelnen Jahre scheint nicht symmetrisch zu sein. Es gibt einen Ausreißer mit
39351 Gigawattstunden.

```python
fig = px.box(data[['Industrie', 'Verkehr', 'Haushalte, Gewerbe, Handel, Dienstleistungen und übrige Verbraucher']],
            title='Stromverbrauch Hessen von 2000 bis 2021',
            labels={'value': 'Gigawattstunden', 'variable': 'Sektoren'})
fig.show()
```

Eine gemeinsame Visualisierung der drei Kategorien ist hier nicht sinnvoll, da die statistischen Kennzahlen weit auseinander liegen. Daher wird jede Kategorie einzeln untersucht.

```python
fig = px.box(data['Industrie'],
            title='Stromverbrauch Hessen von 2000 bis 2021 (Industrie)',
            labels={'value': 'Gigawattstunden', 'variable': ''})
fig.show()
```

Die Verteilung des Stromverbrauchs ist symmetrisch, der Median liegt ungefähr
mittig zwischen Q1 und Q3. Es gibt zwei Ausreißer nach unten.

```python
fig = px.box(data['Verkehr'],
            title='Stromverbrauch Hessen von 2000 bis 2021 (Verkehr)',
            labels={'value': 'Gigawattstunden', 'variable': ''})
fig.show()
```

Die Verteilung des Stromverbrauchs ist ungefähr symmetrisch, es gibt einen
Ausreißer nach unten und einen Ausreißer nach oben.

```python
fig = px.box(data['Haushalte, Gewerbe, Handel, Dienstleistungen und übrige Verbraucher'],
            title='Stromverbrauch Hessen von 2000 bis 2021 (Haushalte, etc.)',
            labels={'value': 'Gigawattstunden', 'variable': ''})
fig.show()
```

Es gibt keine Ausreißer, der Median ist ungefähr mittig zwischen Q1 und Q3. 
````

````{admonition} Übung 4.2 - Teilaufgabe d)
:class: tip

Visualisieren Sie den Stromverbrauch der drei relevanten Sektoren Industrie,
Verkehr und Haushalte abhängig vom Jahr in einem gemeinsamen Scatterplot. Setzen
Sie einen Titel und beschriften Sie auch die Achsen.

Gibt es Auffälligkeiten?
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
fig = px.scatter(data[['Industrie', 'Verkehr', 'Haushalte, Gewerbe, Handel, Dienstleistungen und übrige Verbraucher']],
                 title='Stromverbrauch Hessen von 2000 bis 2021',
                 labels={'value': 'Gigawattstunden', 'variable': 'Legende'})
fig.show()
```

Der Stromverbrauch der Industrie ist 2009 etwas eingebrochen. Vielleicht hat die
Weltfinanzkrise 2007–2008 dazu geführt, dass 2009 die Industrie in Hessen
weniger produziert hat und daher weniger Strom verbraucht hat. Aber das ist eine
Hypothese, die durch weitere Analysen belegt oder widerlegt werden müsste.
````
