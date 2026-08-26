---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: chapter06_sec01.md
    title: chapter06_sec01.md
---

# 6.2 Entscheidungsbäume visualisieren und trainieren

Im letzten Kapitel haben wir gelernt, wie mit Scikit-Learn ein Entscheidungsbaum
für binäre Klassifikationsaufgaben trainiert wird. In diesem Kapitel werden wir
uns damit beschäftigen, den trainierten Entscheidungsbaum von Scikit-Learn
visualisieren zu lassen. Darüber hinaus lernen wir, was das
Gini-Impurity-Kriterium ist und welche weiteren Einstellmöglichkeiten es für
Entscheidungsbäume in Scikit-Learn gibt.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können einen trainierten Entscheidungsbaum mit `plot_tree`
  visualisieren.
* [ ] Sie können Entscheidungsfragen sowie die Angaben `samples` und `value` in
  einer Baumvisualisierung interpretieren.
* [ ] Sie können die Gini-Unreinheit als Maß für die Klassenmischung eines
  Knotens erläutern.
* [ ] Sie können `random_state` und `criterion` beim Training eines
  Entscheidungsbaums verwenden.
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
Angaben `samples` und `value` können so leichter von ihrer Bedeutung her
eingeordnet werden. `samples` gibt die Anzahl der Datenobjekte an, die sich in
diesem Knoten befinden. `value` listet auf, wie viele Datenobjekte die
Zielgröße `nicht verkauft` (= False bzw. 0) haben und wie viele zu der Klasse
`verkauft` (= True bzw. 1) gehören.

Weitere Details zu den Optionen der `plot_tree`-Funktion finden Sie in der
[Dokumentation Scikit-Learn →
plot_tree](https://scikit-learn.org/stable/modules/generated/sklearn.tree.plot_tree.html).

````{admonition} Mini-Übung
:class: tip
Verwenden Sie die Druckversuch-Daten aus Kapitel 6.1:
```python
druck_daten = pd.DataFrame({
    'Betttemperatur [C]': [60, 100, 65, 105],
    'Druckgeschwindigkeit [mm/s]': [40, 90, 45, 85],
    'erfolgreich': [True, False, True, False]
})
```
1. Trainieren Sie einen Entscheidungsbaum auf diesen Daten.
2. Visualisieren Sie den Baum mit aussagekräftigen Feature- und
   Klassennamen.
3. Wie viele Datenobjekte liegen im Wurzelknoten, wie viele in den beiden
   Blättern?
````

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
druck_daten = pd.DataFrame({
    'Betttemperatur [C]': [60, 100, 65, 105],
    'Druckgeschwindigkeit [mm/s]': [40, 90, 45, 85],
    'erfolgreich': [True, False, True, False]
})

# 1. Training
X_druck = druck_daten[['Betttemperatur [C]', 'Druckgeschwindigkeit [mm/s]']]
y_druck = druck_daten['erfolgreich']

modell_druck = DecisionTreeClassifier(random_state=0)
modell_druck.fit(X_druck, y_druck)

# 2. Visualisierung
plot_tree(modell_druck,
    feature_names=['Betttemperatur [C]', 'Druckgeschwindigkeit [mm/s]'],
    class_names=['nicht erfolgreich', 'erfolgreich']);
```
3. Im Wurzelknoten stehen `samples = 4` und `value = [2, 2]` (2 nicht
   erfolgreiche und 2 erfolgreiche Drucke). Der Baum trennt die Daten mit einer
   einzigen Frage vollständig: In beiden Blättern stehen `samples = 2`, einmal
   mit `value = [2, 0]` und einmal mit `value = [0, 2]`.
````

Als nächstes widmen wir uns der Bedeutung von `gini`.

## Was ist das Gini-Impurity-Kriterium?

Das Gini-Impurity-Kriterium ist ein Maß für die Unreinheit eines Datensatzes.
Beim Beispiel mit dem Autohaus sind im Wurzelknoten fünf Autos, die nicht
verkauft wurden, und fünf verkaufte Autos. Bei zwei Klassen mit je 50 % Anteil
ist das die maximale Unreinheit, die auftreten kann. Der Anteil der verkauften
Autos ist genau 50 %. Bei dieser Verteilung beträgt das Gini-Impurity-Kriterium
0.5. Es gibt zwei weitere Extremfälle. Entweder sind nur verkaufte Autos im
Datensatz (100 % verkaufte Autos) oder gar keine verkauften Autos (0 % verkaufte
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
splitten. Zu jedem möglichen Split werden dann die Gini-Impurity-Werte der
beiden neu entstehenden Kindknoten berechnet und je nach Anzahl der
Datenobjekte in jedem Kindknoten zu einer Gesamt-Unreinheit dieses Splits
zusammengefasst. Dann wählt der Algorithmus den Split aus, bei dem diese
Gesamt-Unreinheit am kleinsten ist, also die höchste Reinheit erzielt wird.
Gilt das für mehrere Splits gleichermaßen, dann wird zufällig einer davon
ausgewählt. Jedes Training kann daher zu einem anderen Entscheidungsbaum
führen. Ist dieses Verhalten nicht
gewünscht, kann der optionale Parameter `random_state=` auf einen Integer
gesetzt werden, um die Zufallszahlen zu fixieren. Das haben wir auch bereits im
vorherigen Abschnitt gemacht, damit die Ergebnisse vergleichbar waren.

Neben dem Gini-Impurity-Kriterium gibt es noch weitere Bewertungsmaße, um einen
Entscheidungsbaum zu trainieren. In Scikit-Learn sind die beiden Alternativen
`log_loss` und `entropy` verfügbar, die auf der **Shannon-Entropie** basieren
und den Informationsgewinn durch Splits maximieren. Wir schauen uns im Folgenden
an, wie diese ausgewählt werden können. Wer sich zuvor noch ein wenig mehr mit
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

````{admonition} Mini-Übung
:class: tip
Nutzen Sie den Wurzelknoten aus der vorherigen Mini-Übung: Von den vier
Druckversuchen waren zwei erfolgreich und zwei nicht erfolgreich.

1. Berechnen Sie das Gini-Impurity-Kriterium dieses Knotens von Hand.
2. Vergleichen Sie Ihr Ergebnis mit dem `gini`-Wert im Wurzelknoten aus der
   vorherigen Visualisierung.
3. Warum ist das Gini-Impurity-Kriterium in den beiden Blattknoten jeweils 0?
````

````{admonition} Lösung
:class: tip
:class: dropdown
1. $p = 2/4 = 0.5$, also
   $\text{GI} = 1 - 0.5^2 - 0.5^2 = 1 - 0.25 - 0.25 = 0.5$.
2. Das stimmt mit dem angezeigten Wert `gini = 0.5` im Wurzelknoten überein.
3. In jedem Blatt kommt nur noch eine einzige Klasse vor (entweder nur
   erfolgreiche oder nur nicht erfolgreiche Drucke). Der Datensatz ist dort
   rein, daher ist das Gini-Impurity-Kriterium 0.
````

## Entscheidungsbäume trainieren

Der Entscheidungsbaum-Klassifikationsalgorithmus von Scikit-Learn bietet noch
weitere Optionen an, wie in der [Dokumentation Scikit-Learn →
DecisionTreeClassifier()](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier)
nachgelesen werden kann.

Sowohl bei der Initialisierung des Entscheidungsbaumes können Parameter gesetzt
werden, als auch beim Verwenden der verschiedenen Methoden. Tatsächlich haben
wir bereits weiter oben den Parameter `random_state=0` bei der Initialisierung
gesetzt. Das dient der Reproduzierbarkeit: Immer wenn es beim Training mehrere
gleich gute Splits zur Auswahl gibt (siehe oben), sorgt ein fester
`random_state` dafür, dass bei jedem Durchlauf derselbe Entscheidungsbaum
entsteht. In einem echten Projekt würde man diesen Parameter nicht dazu
nutzen, um ein Wunschergebnis zu erzwingen.

Experimentieren Sie mit verschiedenen Werten für `random_state` (z.B. 0, 1, 2,
3). Sie werden feststellen, dass sich die Baumstruktur vor allem dort ändern
kann, wo es mehrere gleich gute Splits gab, während die Vorhersagegenauigkeit
auf den Trainingsdaten meist gleich bleibt. Testen Sie auch verschiedene
Splitting-Kriterien (`criterion='gini'` vs. `criterion='entropy'`) und
vergleichen Sie die entstehenden Bäume.

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
Verwenden Sie erneut die Druckversuch-Daten aus den vorherigen Mini-Übungen.

1. Trainieren Sie einen Entscheidungsbaum mit `criterion='entropy'` und
   `random_state=42`.
2. Visualisieren Sie den Baum mit aussagekräftigen Feature- und Klassennamen.
3. Vergleichen Sie die Struktur und die angezeigten Werte mit dem Baum aus der
   ersten Mini-Übung dieses Kapitels. Was ist gleich, was ist anders?
````

```{code-cell}
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
druck_daten = pd.DataFrame({
    'Betttemperatur [C]': [60, 100, 65, 105],
    'Druckgeschwindigkeit [mm/s]': [40, 90, 45, 85],
    'erfolgreich': [True, False, True, False]
})

X_druck = druck_daten[['Betttemperatur [C]', 'Druckgeschwindigkeit [mm/s]']]
y_druck = druck_daten['erfolgreich']

# 1. Training
modell_druck = DecisionTreeClassifier(criterion='entropy', random_state=42)
modell_druck.fit(X_druck, y_druck)

# 2. Visualisierung
plot_tree(modell_druck,
    feature_names=['Betttemperatur [C]', 'Druckgeschwindigkeit [mm/s]'],
    class_names=['nicht erfolgreich', 'erfolgreich']);
```
3. Die grundlegende Struktur ist ähnlich: ein Split, danach zwei reine
   Blätter mit je 2 Datenobjekten. Die Splitfrage selbst hat sich aber
   geändert: Statt nach der Druckgeschwindigkeit wird nun nach der
   Betttemperatur getrennt (`Betttemperatur [C] <= 82.50`). Der Grund ist,
   dass beide Merkmale die Daten gleich gut trennen können. Bei einem
   solchen Gleichstand wählt der Algorithmus abhängig vom `random_state`
   eine der gleichwertigen Fragen aus, genau wie es beim Autohaus-Beispiel
   im Abschnitt zum Gini-Impurity-Kriterium beschrieben wurde. Zusätzlich
   ändert sich die angezeigte Kennzahl: Statt `gini = 0.5` steht im
   Wurzelknoten jetzt `entropy = 1.0`, dem für zwei gleich große Klassen
   maximalen Entropie-Wert.
````

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir das Training von Entscheidungsbäumen mit Hilfe der
Bibliothek Scikit-Learn vertieft. Im nächsten Kapitel widmen wir uns den Vor-,
aber auch den Nachteilen von Entscheidungsbäumen.
