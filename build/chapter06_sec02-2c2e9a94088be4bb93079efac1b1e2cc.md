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

# 6.2 Entscheidungsbäume visualisieren und trainieren

Im letzten Kapitel haben wir gelernt, wie mit Scikit-Learn ein Entscheidungsbaum
für binäre Klassifikationsaufgaben trainiert wird. In diesem Kapitel werden wir
uns damit beschäftigen, den trainierten Entscheidungsbaum von Scikit-Learn
visualisieren zu lassen. Darüber hinaus lernen wir, was das
Gini-Impurity-Kriterion ist und welche weiteren Einstellmöglichkeiten es für
Entscheidungsbäume in Scikit-Learn gibt.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können einen Entscheidungsbaum mit `plot_tree` visualisieren.
* Sie wissen, was die Angaben `samples` und `value` bei der Visualisierung des
  Entscheidungsbaumes bedeuten.
* Sie wissen, was das **Gini-Impurity-Kriterium** ist.
* Sie kennen weitere Parameter für Entscheidungsbäume wie `random_state=` oder
  `criterion=`.
```

## Entscheidungsbäume visualisieren

Im letzten Kapitel haben wir den Entscheidungsbaum für das Autohaus mit Hilfe
des Moduls Scikit-Learn trainiert. Scikit-Learn bietet in dem Untermodul
`sklearn.tree` nicht nur Algorithmen für Entscheidungsbäume an, sondern auch ein
dazu passendes Visualisierungswerkzeug. Die Funktion `plot_tree` zeichnet den
Entscheidungsbaum. Um diese Funktion auszuprobieren, wird zunächst der Datensatz
mit den Autodaten erneut geladen, das Modell Entscheidungsbaum gewählt und
anschließend trainiert.

```{code-cell} ipython3
import pandas as pd 
from sklearn.tree import DecisionTreeClassifier

# Sammlung der Daten 
daten = pd.DataFrame({
    'Kilometerstand [km]': [32908, 20328, 13285, 17162, 27449, 13715, 32889,  3111, 15607, 18295],
    'Preis [EUR]': [15960, 20495, 17227, 17851, 5428, 22772, 13581, 16793, 23253, 11382],
    'verkauft': [False, True, False, True, False, True, False, True, True, False],
    },
    index=['Auto 1', 'Auto 2', 'Auto 3', 'Auto 4', 'Auto 5', 'Auto 6', 'Auto 7', 'Auto 8', 'Auto 9', 'Auto 10'])
daten.head(10)

# Auswahl des Modells: Entscheidungsbaum für Klassifikation
modell = DecisionTreeClassifier(random_state=0)

# Adaption der Daten
X = daten[['Kilometerstand [km]', 'Preis [EUR]']]
y = daten['verkauft']

# Training des Modells
modell.fit(X,y)
```

Nun können wir die Funktion `plot_tree` importieren und das trainierte Modell
visualisieren lassen.

```{code-cell} ipython3
from sklearn.tree import plot_tree

plot_tree(modell)
```

`plot_tree` produziert eine Textausgabe und ein Diagramm. Die Textausgabe kann
unterdrückt werden, indem hinter den Funktionsaufruf `plot_tree(modell)` ein
Semikolon `;` gesetzt wird. Das Diagramm zeichnet wie erwartet die Baumstruktur
vom Wurzelknoten über die Knoten und Zweige bis hin zu den Blättern. Die
Entscheidungsfragen stehen in der ersten Zeile der Knoten. Danach folgen weitere
Angaben wie `gini`, `samples` und `value`. Um diese Angaben zu erklären,
ergänzen wir zunächst weitere Angaben. Mit der Option `feature_names=` wird eine
Liste mit den Eigenschaften ergänzt, die Option `class_names=` ergänzt die
Klassenbezeichnungen. So erhalten wir folgendes Diagramm:

```{code-cell} ipython3
plot_tree(modell, 
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    class_names=['nicht verkauft', 'verkauft']);
```

Was `gini` bedeuten könnte, erschließt sich so immer noch nicht, aber die
Angaben `samples` und `values` können so leichter von ihrer Bedeutung her
eingeordnet werden. `samples` gibt die Anzahl der Datenobjekte an, die sich in
diesem Knoten befinden. `values` listet auf, wie viele Datenobjekte die
Zielgröße `nicht verkauft` (= False bzw. 0) haben und wie viele zu der Klasse
`verkauft` (= True bzw. 1) gehören.

Weitere Details zu den Optionen der `plot_tree`-Funktion finden Sie in der
[Dokumentation Scikit-Learn →
plot_tree](https://scikit-learn.org/stable/modules/generated/sklearn.tree.plot_tree.html).

Als nächstes widmen wir uns der Bedeutung von `gini`.

## Was ist das Gini-Impurity-Kriterium?

Das Gini-Impurity-Kriterium ist ein Maß für die Unreinheit eines Datensatzes.
Beim Beispiel mit dem Autohaus sind im Wurzelknoten fünf Autos, die nicht
verkauft wurden, und fünf verkaufte Autos. Bei zwei Klassen mit je 50 % Anteil
ist das die maximale Unreinheit, die auftreten kann. Der Anteil der verkauften
Autos ist genau 50 %. Bei dieser Verteilung beträgt das Gini-Impurity-Kriterium
0.5. Es gibt zwei weitere Extremfälle. Entweder sind nur verkaufte Autos im
Datensatz (100 % verkaufte Autos) oder gar keine verkaufte Autos (0 % verkaufte
Autos). In beiden Fällen ist der Datensatz rein, das Gini-Impurity-Kriterium ist
0. In allen anderen Fällen liegt das Gini-Impurity-Kriterium zwischen 0 und 0.5.
Die Formel zur Berechnung des genauen Wertes des Gini-Impurity-Kriteriums lautet

$$\text{GI} = 1 - p^2 - (1-p)^2,$$

wenn $p$ der prozentuale Anteil der verkauften Autos ist (das gilt natürlich
allgemein für binäre Klassifikationsaufgaben und nicht nur das
Autohaus-Beispiel).

Die folgende Abbildung zeigt die konkreten Werte des Gini-Impurity-Kriteriums
für den prozentualen Anteil an verkauften Autos.

```{code-cell} ipython3
from numpy import linspace

p = linspace(0,1)
gini = 1 - p**2 - (1-p)**2

import plotly.express as px

fig = px.line(x = p, y = gini,
        title='Gini-Impurity-Kriterium',
        labels={'x': 'prozentualer Anteil', 'y': 'Wert des Gini-Impurity-Kriteriums'})
fig.show()
```

Im Diagramm können wir direkt ablesen, dass bei einem nicht verkauften Auto und
fünf verkauften Autos ($p = 0.8\bar{3}$) das Gini-Impurity-Kriterium den Wert
$0.27\bar{7} \approx 0.278$ hat.

Das Gini-Impurity-Kriterium ist sehr wichtig für das Training eines
Entscheidungsbaumes. Der Algorithmus probiert im Hintergrund verschiedene
Möglichkeiten durch, mit Hilfe der Entscheidungsfragen den Datensatz zu
splitten. Zu jedem Split werden dann die zugehörigen Werte des
Gini-Impurity-Kriteriums berechnet. Dann wählt der Algorithmus den Split aus,
der die höchste Reinheit hat (also den niedrigsten Gini-Impurity-Wert). Gilt das
für mehrere Splits, dann wird zufällig ein Split ausgewählt. Jedes Training kann
daher zu einem anderen Entscheidungsbaum führen. Ist dieses Verhalten nicht
gewünscht, kann der optionale Parameter `random_state=` auf einen Integer
gesetzt werden, um die Zufallszahlen zu fixieren. Das haben wir auch bereits im vorherigen Kapitel gemacht, damit die Ergebnisse vergleichbar waren.

Neben dem Gini-Impurity-Kriterium gibt es noch weitere Bewertungsmaße, um einen
Entscheidungsbaum zu trainieren. In Scikit-Learn sind die beiden Alternativen
`log_loss` und `entropy` verfügbar, die auf der **Shannon-Entropie** basieren
und den Informationsgewinn durch Splits maximieren. Wir schauen uns im Folgenden
an, wie diese ausgewählt werden können. Wer zuvor sich noch ein wenig mehr mit
den Details von Entscheidungsbäumen beschäftigen möchte, kann sich die folgenden
Videos ansehen.

```{dropdown} Optionales Video "Entscheidungsbäume #2 - Der ID3-Algorithmus" von The Morpheus Tutorials
<iframe width="560" height="315" src="https://www.youtube.com/embed/SYyyuHG9qBs?si=MgACjs1hSdFTPu5s" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Optionales Video "Entscheidungsbäume #3 - Entropie und Informationsgewinn" von The Morpheus Tutorials
<iframe width="560" height="315" src="https://www.youtube.com/embed/lg1pb0YaAjI?si=K66tahVdLcI_sEex" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Optionales Video "ID3 Entscheidungsbaum" von 42 Entwickler
<iframe width="560" height="315" src="https://www.youtube.com/embed/FAeVafU7qd8?si=JrDW6mu3v9SVOPAz" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## Entscheidungsbäume trainieren

Der Entscheidungsbaum-Klassifikationsalgorithmus von Scikit-Learn bietet noch
weitere Optionen an, wie in der [Dokumentation Scikit-Learn →
DecisionTreeClassifier()](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier)
nachgelesen werden kann.

Sowohl bei der Initialisierung des Entscheidungsbaumes können Parameter gesetzt
werden, als auch beim Verwenden der verschiedenen Methoden. Tatsächlich haben
wir bereits weiter oben aus didaktischen Gründen den Parameter `random_state=0`
bei der Initialisierung gesetzt, damit immer der gleiche Entscheidungsbaum
entsteht. In einem echten Projekt würde dieser Parameter nie verwendet werden.

Experimentieren Sie mit verschiedenen Werten für `random_state` (z.B. 0, 1, 2,
3). Sie werden feststellen, dass sich die Struktur des Baumes ändern kann,
obwohl die Klassifikationsgenauigkeit oft ähnlich bleibt. Testen Sie auch
verschiedene Splitting-Kriterien (`criterion='gini'` vs. `criterion='entropy'`)
und vergleichen Sie die entstehenden Bäume.

```{code-cell} ipython3
modell = DecisionTreeClassifier(criterion='entropy', random_state=3)
modell.fit(X,y)

plot_tree(modell, 
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    class_names=['nicht verkauft', 'verkauft']);
```

Durch die Verwendung von `entropy` als Kriterium kann sich die Struktur des
Entscheidungsbaums ändern. Statt `gini=...` wird nun `entropy=...` im Diagramm
angezeigt. Die grundlegende Funktionsweise bleibt jedoch gleich: Der Algorithmus
wählt die Splits, die die Unreinheit am stärksten reduzieren.

````{admonition} Mini-Übung
:class: tip
Gegeben sind folgende Trainingsdaten für eine Pflanzenklassifikation:
```python
pflanzen_daten = pd.DataFrame({
    'Blattlaenge [cm]': [2.5, 4.9, 6.3, 7.1, 3.2],
    'Blattbreite [cm]': [0.8, 1.5, 2.1, 2.5, 1.0],
    'giftig': [False, False, True, True, False]
})
```
1. Trainieren Sie einen Entscheidungsbaum mit `random_state=42`.
2. Visualisieren Sie den Baum mit aussagekräftigen Feature- und Klassennamen.
````

```{code-cell}
# Hier Ihr Code
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
pflanzen_daten = pd.DataFrame({
    'Blattlaenge [cm]': [2.5, 4.9, 6.3, 7.1, 3.2],
    'Blattbreite [cm]': [0.8, 1.5, 2.1, 2.5, 1.0],
    'giftig': [False, False, True, True, False]
})

# 1. Training
X_pflanzen = pflanzen_daten[['Blattlaenge [cm]', 'Blattbreite [cm]']]
y_pflanzen = pflanzen_daten['giftig']

modell_pflanzen = DecisionTreeClassifier(random_state=42)
modell_pflanzen.fit(X_pflanzen, y_pflanzen)

# 2. Visualisierung
plot_tree(modell_pflanzen,
    feature_names=['Blattlänge [cm]', 'Blattbreite [cm]'],
    class_names=['nicht giftig', 'giftig']);
```
````

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir das Training von Entscheidungsbäumen mit Hilfe der
Bibliothek Scikit-Learn vertieft. Im nächsten Kapitel widmen wir uns den Vor-,
aber auch den Nachteilen von Entscheidungsbäumen.
