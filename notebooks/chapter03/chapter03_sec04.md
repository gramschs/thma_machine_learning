---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 3.4 Übungen

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

## Übung 3.1

Speichern Sie die Daten zu den Studentinnen an Fachhochschulen als Pandas-Series.
Verschaffen Sie sich einen Überblick über die statistischen Kennzahlen. Lesen
Sie dann ab: In welchem Bundesland studieren die wenigsten Studentinnen und im
welchem Bundesland die meisten?

```{code-cell} python
# Code-Zelle
```

## Übung 3.2

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

```{code-cell} python
# Code-Zelle
```

## Übung 3.3

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

```{code-cell} python
# Code-Zelle
```

## Übung 3.4

Erstellen Sie für alle vier Datensätze Boxplots mit aussagekräftigen
Beschriftungen:

* Studentinnen an Fachhochschulen
* Studenten an Fachhochschulen
* Studenten an Universitäten
* Studentinnen an Universitäten

Verwenden Sie für jeden Boxplot:

* Einen Namen für das Series-Objekt
* Die Beschriftung `'Anzahl Studierende'` für die y-Achse
* Einen passenden Titel

Hinweis: Die Boxplots müssen nicht einzeln angezeigt werden, speichern Sie
sie aber in den Variablen `fig1`, `fig2`, `fig3` und `fig4`, damit Sie sie in
der nächsten Aufgabe vergleichen können.

```{code-cell} python
# Code-Zelle
```

## Übung 3.5

Vergleichen Sie die vier Boxplots miteinander, indem Sie sie nacheinander mit
`.show()` anzeigen lassen. Nutzen Sie die Hover-Funktion (Maus über die Box
bewegen), um die Werte abzulesen.

Teil A: Erstellen Sie eine Vergleichstabelle in einer Markdown-Zelle:

| Datensatz | Median | Q1 (25%) | Q3 (75%) | Ausreißer vorhanden? |
| ----------- | -------- | ---------- | ---------- | ---------------------- |
| Studentinnen FH | ... | ... | ... | ja/nein |
| Studenten FH | ... | ... | ... | ja/nein |
| Studentinnen Uni | ... | ... | ... | ja/nein |
| Studenten Uni | ... | ... | ... | ja/nein |

Teil B: Beantworten Sie folgende Fragen:

1. An welcher Hochschulart (Uni oder FH) ist die Streuung der Studierendenzahlen
   größer?
2. Bei welchem Datensatz liegt der Median am weitesten von der Mitte zwischen Q1
   und Q3 entfernt? Was bedeutet das?
3. Welche Bundesländer tauchen als Ausreißer auf?

```{code-cell} python
# Code-Zelle
```
