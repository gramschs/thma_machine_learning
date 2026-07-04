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

Gegeben sind folgende Daten zu der Verteilung von Studierenden
(männlich/weiblich) auf die Hochschularten Universität und Fachhochschulen
(Hochschulen für angewandte Wissenschaften), Quelle:
[https://www.statistischebibliothek.de/mir/receive/DESerie_mods_00007716]

```python
bundeslaender = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 
                 'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern', 
                 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz',
                 'Saarland', 'Sachsen', 'Sachsen-Anhalt',
                 'Schleswig-Holstein', 'Thüringen']
studierende_universitaeten_maennlich = [85183, 118703, 58682, 15845,
                                        9291, 27444, 68753, 10349, 
                                        62192, 235564, 31487, 7806, 
                                        35826, 15847, 16548, 14350]
studierende_universitaeten_weiblich = [82635, 131158, 65587, 18742,
                                       10181, 28438, 75292, 12821,
                                       69866, 246467, 41755, 8391,
                                       37669, 17061, 22760, 17245]
studierende_fachhochschulen_maennlich = [83058, 81163, 34727, 7778,
                                         8299, 26818, 53998, 7120,
                                         33147, 132976, 21759, 7407,
                                         15497, 12023, 14167, 39330]
studierende_fachhochschulen_weiblich = [65332, 63198, 33333, 6323,
                                        8235, 33558, 47600, 6886,
                                        27157, 106755, 18042, 5767,
                                        11087, 11273, 7943, 63669]
```

```{admonition} Übung 3.1
:class: tip
Speichern Sie die Daten zu den Studentinnen an Fachhochschulen als Pandas-Series.
Verschaffen Sie sich einen Überblick über die statistischen Kennzahlen. Lesen
Sie dann ab: In welchem Bundesland studieren die wenigsten Studentinnen und im
welchem Bundesland die meisten?
```

````{admonition} Lösung
:class: tip
:class: dropdown
Zuerst speichern wir den Datensatz als Pandas-Series in der Variable
`stud_fh_weiblich` und verschaffen uns einen Überblick über die statistischen
Kennzahlen, um Minimum und Maximum zu bestimmen.

```python
import pandas as pd

stud_fh_weiblich = pd.Series(data=studierende_fachhochschulen_weiblich, index=bundeslaender, name='Studentinnen an Fachhochschulen')
stud_fh_weiblich.describe()
```

Die minimale Anzahl an Studentinnen ist 5767, die maximale Anzahl 106755. Mit `print`
lassen wir den kompletten Datensatz anzeigen:

```python
print(stud_fh_weiblich)
```

Wir lesen ab: am wenigsten Studentinnen an Fachhochschulen studieren im Saarland
und am meisten in Nordrhein-Westfalen.
````

```{admonition} Übung 3.2
:class: tip
Wählen Sie **einen** der drei verbleibenden Datensätze aus:

* Studenten an Universitäten
* Studentinnen an Universitäten  
* Studenten an Fachhochschulen

Erstellen Sie ein Series-Objekt für diesen Datensatz und überprüfen Sie, ob auch
dort das Saarland das Minimum und Nordrhein-Westfalen das Maximum hat. Lassen
Sie Minimum und Maximum mit `.min()` und `.max()` ausgeben und kontrollieren Sie
durch Anzeige des Datensatzes, welches Bundesland dazugehört.

Zusatzfrage: Was vermuten Sie für die anderen beiden Datensätze, die Sie nicht
untersucht haben? Begründen Sie Ihre Vermutung.
```

````{admonition} Lösung
:class: tip
:class: dropdown
Beispiel für Studenten an Universitäten:
```python
import pandas as pd

stud_uni_maennlich = pd.Series(data=studierende_universitaeten_maennlich, 
                                index=bundeslaender, 
                                name='Studenten an Universitäten')

print(f'Minimum: {stud_uni_maennlich.min()}, Maximum: {stud_uni_maennlich.max()}')
print(stud_uni_maennlich)
```

Ergebnis: Minimum im Saarland (7806) und Maximum in Nordrhein-Westfalen (235564).

Zusatzfrage: Vermutlich haben auch die anderen beiden Datensätze das Minimum im 
Saarland und das Maximum in Nordrhein-Westfalen. Begründung: Die Studierendenzahlen 
hängen stark von der Größe und Bevölkerungszahl des Bundeslandes ab. Das Saarland 
ist das kleinste Flächenland, Nordrhein-Westfalen das bevölkerungsreichste 
Bundesland Deutschlands.
````

```{admonition} Übung 3.3
:class: tip
Lassen Sie die Datensätze zu Studentinnen an Fachhochschulen und Studenten an
Fachhochschulen durch Boxplots visualisieren.

Teil A: Erstellen Sie den ersten Boxplot für Studentinnen an Fachhochschulen
mit folgenden Eigenschaften:

* Benennen Sie das Series-Objekt mit 'Studentinnen FH'.
* Beschriften Sie die y-Achse mit 'Anzahl Studierende'.
* Setzen Sie den Titel 'Studentinnen an Fachhochschulen'.
* Zeigen Sie alle Datenpunkte neben dem Boxplot an.

Teil B: Erstellen Sie analog einen zweiten Boxplot für Studenten an
Fachhochschulen. Achten Sie darauf, eine andere Variablennamen für das Diagramm
zu verwenden (z.B. `diagramm2` statt `diagramm`), damit der erste Boxplot nicht
überschrieben wird.

Interpretationsfrage: Gibt es Ausreißer? Wenn ja, bei welchem Datensatz und
welches Bundesland ist betroffen?
```

````{admonition} Lösung
:class: tip
:class: dropdown
Teil A: Boxplot für Studentinnen an Fachhochschulen:
```python
import pandas as pd
import plotly.express as px

stud_fh_weiblich = pd.Series(data=studierende_fachhochschulen_weiblich,
                              index=bundeslaender,
                              name='Studentinnen FH')

diagramm1 = px.box(stud_fh_weiblich,
                   labels={'value': 'Anzahl Studierende'},
                   title='Studentinnen an Fachhochschulen',
                   points='all')
diagramm1.show()
```

Teil B: Boxplot für Studenten an Fachhochschulen:
```python
stud_fh_maennlich = pd.Series(data=studierende_fachhochschulen_maennlich,
                               index=bundeslaender,
                               name='Studenten FH')

diagramm2 = px.box(stud_fh_maennlich,
                   labels={'value': 'Anzahl Studierende'},
                   title='Studenten an Fachhochschulen',
                   points='all')
diagramm2.show()
```

Interpretationsfrage: Ja, es gibt einen Ausreißer beim Datensatz "Studenten an 
Fachhochschulen". Das betroffene Bundesland ist Nordrhein-Westfalen mit 132.976 
Studenten. Bei den Studentinnen an Fachhochschulen gibt es keinen Ausreißer.
````

```{admonition} Übung 3.4
:class: tip
Erstellen Sie für alle vier Datensätze Boxplots mit aussagekräftigen 
Beschriftungen:
- Studentinnen an Fachhochschulen
- Studenten an Fachhochschulen
- Studenten an Universitäten
- Studentinnen an Universitäten

Verwenden Sie für jeden Boxplot:
- Einen Namen für das Series-Objekt
- Die Beschriftung `'Anzahl Studierende'` für die y-Achse
- Einen passenden Titel

Hinweis: Die Boxplots müssen nicht einzeln angezeigt werden, speichern Sie 
sie aber in den Variablen `fig1`, `fig2`, `fig3` und `fig4`, damit Sie sie in 
der nächsten Aufgabe vergleichen können.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import pandas as pd
import plotly.express as px

# Series-Objekte erstellen
stud_fh_weiblich = pd.Series(data=studierende_fachhochschulen_weiblich, 
                              index=bundeslaender, 
                              name='Studentinnen FH')
stud_fh_maennlich = pd.Series(data=studierende_fachhochschulen_maennlich, 
                               index=bundeslaender, 
                               name='Studenten FH')
stud_uni_maennlich = pd.Series(data=studierende_universitaeten_maennlich, 
                                index=bundeslaender, 
                                name='Studenten Uni')
stud_uni_weiblich = pd.Series(data=studierende_universitaeten_weiblich, 
                               index=bundeslaender, 
                               name='Studentinnen Uni')

# Boxplots erstellen
fig1 = px.box(stud_fh_weiblich,
              labels={'value': 'Anzahl Studierende'},
              title='Studentinnen an Fachhochschulen')

fig2 = px.box(stud_fh_maennlich,
              labels={'value': 'Anzahl Studierende'},
              title='Studenten an Fachhochschulen')

fig3 = px.box(stud_uni_maennlich,
              labels={'value': 'Anzahl Studierende'},
              title='Studenten an Universitäten')

fig4 = px.box(stud_uni_weiblich,
              labels={'value': 'Anzahl Studierende'},
              title='Studentinnen an Universitäten')

# Optional: Einen oder alle anzeigen
fig1.show()
```
````

```{admonition} Übung 3.5
:class: tip
Vergleichen Sie die vier Boxplots miteinander, indem Sie sie nacheinander mit 
`.show()` anzeigen lassen. Nutzen Sie die Hover-Funktion (Maus über die Box 
bewegen), um die Werte abzulesen.

Teil A: Erstellen Sie eine Vergleichstabelle in einer Markdown-Zelle:

| Datensatz | Median | Q1 (25%) | Q3 (75%) | Ausreißer vorhanden? |
|-----------|--------|----------|----------|----------------------|
| Studentinnen FH | ... | ... | ... | ja/nein |
| Studenten FH | ... | ... | ... | ja/nein |
| Studentinnen Uni | ... | ... | ... | ja/nein |
| Studenten Uni | ... | ... | ... | ja/nein |

Teil B: Beantworten Sie folgende Fragen:
1. An welcher Hochschulart (Uni oder FH) ist die Streuung der Studierendenzahlen 
   größer?
2. Bei welchem Datensatz liegt der Median am weitesten von der Mitte zwischen 
   Q1 und Q3 entfernt? Was bedeutet das?
3. Welche Bundesländer tauchen als Ausreißer auf?
```

````{admonition} Lösung
:class: tip
:class: dropdown
Teil A: Boxplots anzeigen und Werte ablesen:
```python
# Alle vier Boxplots nacheinander anzeigen
fig1.show()  # Studentinnen FH
fig2.show()  # Studenten FH
fig3.show()  # Studenten Uni
fig4.show()  # Studentinnen Uni
```

Vergleichstabelle:

| Datensatz | Median | Q1 (25%) | Q3 (75%) | Ausreißer vorhanden? |
|-----------|--------|----------|----------|----------------------|
| Studentinnen FH | 22599.5| 8162 | 51499.5 | nein |
| Studenten FH | 24288.5 | 11092 | 42997.0 | ja (NRW) |
| Studentinnen Uni | 33053.5 | 17199.0 | 71222.5 | ja (NRW) |
| Studenten Uni | 29465.5 | 15471.25 | 63832.25 | ja (NRW) |

Teil B: Interpretation:

1. *Streuung Uni vs. FH:* Die Streuung ist an Universitäten deutlich größer. Der
   Interquartilabstand (Q3 - Q1) beträgt bei Unis ca. 48000 (Männer) bzw. 54000
   (Frauen), bei FH nur ca. 32000 (Männer) bzw. 43000 (Frauen). Das liegt
   vermutlich daran, dass es in großen Bundesländern mehr Universitäten gibt.

2. *Asymmetrische Verteilung:* Bei Studentinnen an Fachhochschulen liegt der
   Median (22599.5) deutlich näher an Q1 (11092) als an Q3 (51499.5). Das
   bedeutet: Die Mehrzahl der Bundesländer hat wenige Studentinnen an
   Fachhochschulen, aber einige wenige Bundesländer haben sehr viele.

3. *Ausreißer:* Nordrhein-Westfalen taucht bei drei Datensätzen als Ausreißer
   auf (nicht bei Studentinnen FH). Das ist plausibel, da NRW das
   bevölkerungsreichste Bundesland ist.
````
