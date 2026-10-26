---
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
Gini-Impurity-Kriterium ist und welche weiteren Einstellmöglichkeiten es für
Entscheidungsbäume in Scikit-Learn gibt.

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

# Daten ins richtige Format bringen
X = daten[['Kilometerstand [km]', 'Preis [EUR]']]
y = daten['verkauft']

# Training des Modells
modell.fit(X,y)
```

Nun können wir die Funktion `plot_tree` importieren und ihr das trainierte
Modell `modell` übergeben, um es visualisieren zu lassen.

```{code-cell} ipython3
from sklearn.tree import plot_tree

# TODO: ???  (trainiertes Modell zeichnen)
```

`plot_tree` produziert eine Textausgabe und ein Diagramm. Die Textausgabe kann
unterdrückt werden, indem hinter den Funktionsaufruf `plot_tree(modell)` ein
Semikolon `;` gesetzt wird. Das Diagramm zeichnet wie erwartet die Baumstruktur
vom Wurzelknoten über die Knoten und Zweige bis hin zu den Blättern. Die
Entscheidungsfragen stehen in der ersten Zeile der Knoten. Danach folgen weitere
Angaben wie `gini`, `samples` und `value`. Um diese Angaben zu erklären,
ergänzen wir zunächst weitere Angaben. Mit der Option `feature_names=` wird eine
Liste mit den Eigenschaften ergänzt, die Option `class_names=` ergänzt die
Klassenbezeichnungen. Die Klassennamen müssen in der Reihenfolge stehen, in der
Scikit-Learn die Klassen sortiert. Bei `False` und `True` kommt `False` zuerst,
also zuerst "nicht verkauft" und dann "verkauft". So erhalten wir folgendes
Diagramm:

```{code-cell} ipython3
plot_tree(modell, 
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    # TODO: ???  (Namen der beiden Klassen ergänzen)
);
```

Was `gini` bedeuten könnte, erschließt sich so immer noch nicht, aber die
Angaben `samples` und `value` können so leichter von ihrer Bedeutung her
eingeordnet werden. `samples` gibt die Anzahl der Datenobjekte an, die sich in
diesem Knoten befinden. `value` listet auf, wie viele Datenobjekte die
Zielgröße `nicht verkauft` (= False bzw. 0) haben und wie viele zu der Klasse
`verkauft` (= True bzw. 1) gehören.

Weitere Details zu den Optionen der `plot_tree`-Funktion stehen in der
[Dokumentation Scikit-Learn →
plot_tree](https://scikit-learn.org/stable/modules/generated/sklearn.tree.plot_tree.html).

Als Nächstes widmen wir uns der Bedeutung von `gini`.

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

wenn $p$ der Anteil der verkauften Autos ist (das gilt natürlich
allgemein für binäre Klassifikationsaufgaben und nicht nur das
Autohaus-Beispiel).

Die folgende Abbildung zeigt die konkreten Werte des Gini-Impurity-Kriteriums
für den Anteil an verkauften Autos.

```{code-cell} ipython3
from numpy import linspace

p = linspace(0,1)
gini = # TODO: ???  (Gini-Impurity-Kriterium für alle Anteile p berechnen)

import plotly.express as px

fig = px.line(x = p, y = gini,
        title='Gini-Impurity-Kriterium',
        labels={'x': 'Anteil der verkauften Autos', 'y': 'Wert des Gini-Impurity-Kriteriums'})
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

## Entscheidungsbäume trainieren

Der Entscheidungsbaum-Klassifikationsalgorithmus von Scikit-Learn bietet noch
weitere Optionen an, wie in der [Dokumentation Scikit-Learn →
DecisionTreeClassifier()](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier)
nachgelesen werden kann.

Parameter können wir sowohl bei der Initialisierung des Entscheidungsbaumes
setzen als auch beim Aufruf der verschiedenen Methoden. Tatsächlich haben
wir bereits weiter oben den Parameter `random_state=0` bei der Initialisierung
gesetzt. Das dient der Reproduzierbarkeit: Immer wenn es beim Training mehrere
gleich gute Splits zur Auswahl gibt (siehe oben), sorgt ein fester
`random_state` dafür, dass bei jedem Durchlauf derselbe Entscheidungsbaum
entsteht. In einem echten Projekt nutzen wir diesen Parameter aber nicht, um
ein Wunschergebnis zu erzwingen.

Probieren wir verschiedene Werte für `random_state` aus (z.B. 0, 1, 2, 3), dann
ändert sich die Baumstruktur vor allem dort, wo es mehrere gleich gute Splits
gab. Die Accuracy auf den Trainingsdaten bleibt dagegen meist gleich. Ebenso
können wir die Splitting-Kriterien `criterion='gini'` und `criterion='entropy'`
vergleichen. Im folgenden Beispiel verwenden wir `criterion='entropy'` und
`random_state=3`.

```{code-cell} ipython3
modell = # TODO: ???  (Entscheidungsbaum mit der Entropie als Kriterium erzeugen, Zufallszahlen auf 3 fixieren)
modell.fit(X,y)

plot_tree(modell, 
    feature_names=['Kilometerstand [km]', 'Preis [EUR]'],
    class_names=['nicht verkauft', 'verkauft']);
```

Durch die Verwendung von `entropy` als Kriterium kann sich die Struktur des
Entscheidungsbaums ändern. Statt `gini=...` wird nun `entropy=...` im Diagramm
angezeigt. Die grundlegende Funktionsweise bleibt jedoch gleich: Der Algorithmus
wählt die Splits, die die Unreinheit am stärksten reduzieren.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir das Training von Entscheidungsbäumen mit Hilfe der
Bibliothek Scikit-Learn vertieft. Im nächsten Kapitel widmen wir uns den Vor-,
aber auch den Nachteilen von Entscheidungsbäumen.

## Mini-Übungen

### Mini-Übung 1

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

```{code-cell}
# Code-Zelle
```

### Mini-Übung 2

Nutzen Sie den Wurzelknoten aus der vorherigen Mini-Übung: Von den vier
Druckversuchen waren zwei erfolgreich und zwei nicht erfolgreich.

1. Berechnen Sie das Gini-Impurity-Kriterium dieses Knotens von Hand.
2. Vergleichen Sie Ihr Ergebnis mit dem `gini`-Wert im Wurzelknoten aus der
   vorherigen Visualisierung.
3. Warum ist das Gini-Impurity-Kriterium in den beiden Blattknoten jeweils 0?

### Mini-Übung 3

Verwenden Sie erneut die Druckversuch-Daten aus den vorherigen Mini-Übungen.

1. Trainieren Sie einen Entscheidungsbaum mit `criterion='entropy'` und
   `random_state=42`.
2. Visualisieren Sie den Baum mit aussagekräftigen Feature- und Klassennamen.
3. Vergleichen Sie die Struktur und die angezeigten Werte mit dem Baum aus der
   ersten Mini-Übung dieses Kapitels. Was ist gleich, was ist anders?

```{code-cell}
# Code-Zelle
```
