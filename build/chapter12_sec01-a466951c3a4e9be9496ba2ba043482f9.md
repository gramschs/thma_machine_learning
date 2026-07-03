---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 12.1 Perzeptron = Grundbaustein neuronaler Netze

Neuronale Netze sind sehr beliebte maschinelle Lernverfahren. Das einfachste
künstliche neuronale Netz ist das **Perzeptron**. In diesem Abschnitt werden wir
das Perzeptron vorstellen.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können das Perzeptron als mathematische Funktion formulieren und in diesem
  Zusammenhang die folgenden Begriffe erklären:
    * **gewichtete Summe** (Weighted Sum),
    * **Bias** oder Bias-Einheit (Bias),
    * **Schwellenwert** (Threshold)  
    * **Heaviside-Funktion** (Heaviside Function) und
    * **Aktivierungsfunktion** (Activation Function).
* Sie können das Perzeptron als ein binäres Klassifikationsproblem des
  überwachten Lernens einordnen.
```

## Die Hirnzelle dient als Vorlage für künstliche Neuronen

1943 haben die Forscher Warren McCulloch und Walter Pitts das erste Modell einer
vereinfachten Hirnzelle präsentiert. Zu Ehren der beiden Forscher heißt dieses
Modell MCP-Neuron. Darauf aufbauend publizierte Frank Rosenblatt 1957 seine Idee
einer Lernregel für das künstliche Neuron. Das sogenannte Perzeptron bildet die
Grundlage der künstlichen neuronalen Netze. Inspiriert wurden die Forscher dabei
durch den Aufbau des Gehirns und der Verknüpfung der Nervenzellen.

```{figure} pics/neuron_wikipedia.svg
---
width: 600px
name: fig_neuron_wikipedia
---
Schematische Darstellung einer Nervenzelle
(Quelle: [Wikimedia](https://commons.wikimedia.org/wiki/File:Neuron_(deutsch)-1.svg);
Lizenz: [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/))
```

Elektrische und chemische Eingabesignale kommen bei den Dendriten an und laufen
im Zellkörper zusammen. Sobald ein bestimmter Schwellwert überschritten wird,
wird ein Ausgabesignal erzeugt und über das Axon weitergeleitet. Mehr Details zu
Nervenzellen finden Sie auf
[Wikipedia/Nervenzelle](https://de.wikipedia.org/wiki/Nervenzelle).

+++

## Von logischem ODER zur mathematischen Ungleichung

Das einfachste künstliche Neuron besteht aus zwei Inputs und einem Output. Dabei
sind für die beiden Inputs nur zwei Zustände zugelassen und auch der Output
besteht nur aus zwei verschiedenen Zuständen. In der Sprache des maschinellen
Lernens liegt also eine **binäre Klassifikationsaufgabe** innerhalb des
**Supervised Learnings** vor.

Beispiel:

* Input 1: Es regnet oder es regnet nicht.
* Input 2: Der Rasensprenger ist an oder nicht.
* Output: Der Rasen wird nass oder nicht.

Den Zusammenhang zwischen Regen, Rasensprenger und nassem Rasen können wir in
einer Tabelle abbilden:

Regnet es? | Ist Sprenger an? | Wird Rasen nass?
-----------|------------------|-----------------
nein       | nein             | nein
ja         | nein             | ja
nein       | ja               | ja
ja         | ja               | ja

+++

```{admonition} Mini-Übung
:class: tip
Schreiben Sie ein kurzes Python-Programm, das abfragt, ob es regnet und ob der
Rasensprenger eingeschaltet ist. Dann soll der Python-Interpreter ausgeben, ob
der Rasen nass wird oder nicht.
```

```{code-cell}
# Ihr Code:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Eingabe
x1 = input('Regnet es (j/n)?')
x2 = input('Ist der Rasensprenger eingeschaltet? (j/n)')

# Verarbeitung
y = (x1 == 'j') or (x2 == 'j')

# Ausgabe
if y == True:
    print('Der Rasen wird nass.')
else:
    print('Der Rasen wird nicht nass.')
```
````

+++

Für das maschinelle Lernen müssen die Daten als Zahlen aufbereitet werden, damit
die maschinellen Lernverfahren in der Lage sind, Muster in den Daten zu
erlernen. Anstatt "Regnet es? Nein." oder Variablen mit True/False setzen wir
jetzt Zahlen ein. Die Eingabewerte bezeichnen wir mit x1 für Regen und x2 für
Rasensprenger. Die 1 steht für ja, die 0 für nein. Den Output bezeichnen wir mit
y. Dann lautet die obige Tabelle für das "Ist-der-Rasen-nass-Problem":

x1 | x2 | y
---|----|---
0  | 0  | 0
1  | 0  | 1
0  | 1  | 1
1  | 1  | 1

+++

```{admonition} Mini-Übung
:class: tip
Schreiben Sie Ihren Programm-Code der letzten Mini-Übung um. Verwenden Sie
Integer 0 und 1 für die Eingaben.
```

```{code-cell}
# Ihr Code:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Eingabe
x1 = int(input('Regnet es (ja = 1 | nein = 0)?'))
x2 = int(input('Ist der Rasensprenger eingeschaltet? (ja = 1 | nein = 0)'))

# Verarbeitung
y = (x1 == 1) or (x2 == 1)

# Ausgabe
if y == True:
    print('Der Rasen wird nass.')
else:
    print('Der Rasen wird nicht nass.')
```
````

+++

Nun ersetzen wir das logische ODER durch ein mathematisches Konstrukt:
Wenn die Ungleichung

\begin{equation*}
x_1 w_1  +  x_2 w_2 \geq \theta
\end{equation*}

erfüllt ist, dann ist $y = 1$ oder anders ausgedrückt, der Rasen wird nass. Und
ansonsten ist $y = 0$, der Rasen wird nicht nass. Allerdings müssen wir noch die
**Gewichte** $w_1$ und $w_2$ (auf Englisch: weights) geschickt wählen. Die Zahl
$\theta$ ist der griechische Buchstabe Theta und steht als Abkürzung für den
sogenannten **Schwellenwert** (auf Englisch: threshold).

Beispielsweise würde $w_1 = 0.3$, $w_2=0.3$ und $\theta = 0.2$ passen:

* $0 \cdot 0.3 + 0 \cdot 0.3 = 0.0 \geq 0.2$ nicht erfüllt
* $0 \cdot 0.3 + 1 \cdot 0.3 = 0.3 \geq 0.2$ erfüllt
* $1 \cdot 0.3 + 0 \cdot 0.3 = 0.3 \geq 0.2$ erfüllt
* $1 \cdot 0.3 + 1 \cdot 0.3 = 0.6 \geq 0.2$ erfüllt

+++

```{admonition} Mini-Übung
:class: tip
Schreiben Sie Ihren Programm-Code der letzten Mini-Übung um. Ersetzen Sie das
logische ODER durch die linke Seite der Ungleichung und vergleichen Sie
anschließend mit $0.2$, um zu entscheiden, ob der Rasen nass wird oder nicht.
```

```{code-cell}
# Ihr Code:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Eingabe
x1 = int(input('Regnet es (ja = 1 | nein = 0)?'))
x2 = int(input('Ist der Rasensprenger eingeschaltet? (ja = 1 | nein = 0)'))

# Verarbeitung
y = 0.3 * x1 + 0.3 * x2

# Ausgabe
if y >= 0.2:
    print('Der Rasen wird nass.')
else:
    print('Der Rasen wird nicht nass.')
```
````

+++

## Die Heaviside-Funktion ersetzt die Ungleichungsprüfung

Noch sind wir aber nicht fertig, denn auch die Frage "Ist die Ungleichung
erfüllt oder nicht?" muss noch in eine mathematische Funktion umgeschrieben
werden. Dazu subtrahieren wir zuerst auf beiden Seiten der Ungleichung den
Schwellenwert $\theta$:

$$-\theta + x_1 w_1  +  x_2 w_2 \geq 0.$$

Damit haben wir jetzt nicht mehr einen Vergleich mit dem Schwellenwert, sondern
müssen nur noch entscheiden, ob der Ausdruck $-\theta + x_1 w_1 + x_2 w_2$
negativ oder positiv ist. Bei negativen Werten, soll $y = 0$ sein und bei
positiven Werten (inklusive der Null) soll $y = 1$ sein. Dafür gibt es in der
Mathematik eine passende Funktion, die sogenannte
[Heaviside-Funktion](https://de.wikipedia.org/wiki/Heaviside-Funktion) (manchmal
auch Theta-, Stufen- oder Treppenfunktion genannt).

```{figure} pics/heaviside_wikipedia.svg
---
name: fig_heaviside_wikipedia
---
Schaubild der Heaviside-Funktion
(Quelle: [Wikimedia](https://commons.wikimedia.org/wiki/File:Heaviside.svg) von
Lennart Kudling; Lizenz: gemeinfrei)
```

Definiert ist die Heaviside-Funktion folgendermaßen:

$$\Phi(x) = \begin{cases}0:&x<0\\1:&x\geq 0\end{cases}$$

In dem Modul NumPy ist die Heaviside-Funktion schon hinterlegt, siehe
> <https://numpy.org/doc/stable/reference/generated/numpy.heaviside.html>

+++

```{admonition} Mini-Übung
:class: tip
Visualisieren Sie die Heaviside-Funktion für das Intervall $[-3,3]$ mit 101
Punkten. Setzen Sie das zweite Argument einmal auf 0 und einmal auf 2. Was
bewirkt das zweite Argument? Sehen Sie einen Unterschied in der Visualisierung?

Erhöhen Sie auch die Anzahl der Punkte im Intervall. Wählen Sie dabei immer eine
ungerade Anzahl an Punkten, damit die 0 dabei ist und der Sprung an der Stelle
$x = 0$ besser sichtbar wird.
```

```{code-cell}
# Ihr Code:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import pandas as pd
import plotly.express as px
import numpy as np

x = np.linspace(-3, 3, 101)
y0 = np.heaviside(x, 0)  # an der Stelle x=0 ist y=0
y1 = np.heaviside(x, 2)  # an der Stelle x=0 ist y=2

# Daten für Plotly Express vorbereiten
df = pd.DataFrame({'x': x, 'y0': y0, 'y1': y1})

# Visualisierung
fig = px.scatter(df, x='x', y=['y0', 'y1'], title='Heaviside-Funktion')
fig.update_layout(
    xaxis_title='x',
    yaxis_title='y'
)
fig.show()
```
````

Das zweite Argument der Heaviside-Funktion `heaviside` in NumPy gibt an, welchen
Funktionswert die Heaviside-Funktion an der Stelle $x=0$ hat. Der Standard ist
$0.5$.

Mit der Heaviside-Funktion können wir nun den Vergleich in der
Programmverzweigung mit $0.2$ durch eine direkte Berechnung ersetzen. Betrachten
wir den folgenden Programm-Code, der zeigt, wie wir ohne logisches Oder bzw.
ohne Programmverzweigung if-else auskommen.

+++

```python
# Import der notwendigen Module
import numpy as np

# Eingabe
x1 = int(input('Regnet es (ja = 1 | nein = 0)?'))
x2 = int(input('Ist der Rasensprenger eingeschaltet? (ja = 1 | nein = 0)'))

# Verarbeitung
y = np.heaviside(-0.2 + 0.3 * x1 + 0.3 * x2, 1.0)

# Ausgabe
ergebnis_als_text = ['Der Rasen wird nicht nass.', 'Der Rasen wird nass.']
print(ergebnis_als_text[int(y)])
```

+++

## Das Perzeptron mit mehreren Eingabewerten

Das Perzeptron für zwei Eingabewerte lässt sich in sehr natürlicher Weise auf
viele Eingabewerte verallgemeinern, die auch mehrere Zustände annehmen können.
Bei den Outputs bleiben wir jedoch dabei, dass nur zwei Zustände angenommen
werden können, die wir mit 0 und 1 bezeichnen. Wir betrachten also weiterhin
binäre Klassifikationsaufgaben.

Wenn wir nicht nur zwei, sondern $n$ Eingabewerte $x_i$ haben, brauchen wir
entsprechend auch $n$ Gewichte $w_i$. Um die Notation zu vereinfachen, fassen
wir die Eingabewerte in einem Spaltenvektor zusammen, also

\begin{equation*}
\mathbf{x} = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{pmatrix}.
\end{equation*}

Auch die Gewichte fassen wir in einem Spaltenvektor zusammen, also

\begin{equation*}
\mathbf{w} =
\begin{pmatrix} w_1 \\ w_2 \\ \vdots \\ w_n\end{pmatrix}.
\end{equation*}

Nun lässt sich die Ungleichung recht einfach durch das Skalarprodukt abkürzen:

\begin{equation*}
\mathbf{x}^{T}\mathbf{w} =
x_1 w_1 +  x_2 w_2 + \ldots + x_n w_n \geq \theta.
\end{equation*}

Wie bei dem Perzeptron mit zwei Eingängen wird der Schwellenwert $\theta$ durch
Subtraktion auf die linke Seite gebracht. Wenn wir jetzt bei dem Vektor
$\mathbf{w}$ mit den Gewichten vorne den Vektor um das Element $w_0 = -\theta$
ergänzen und den Vektor $\mathbf{x}$ mit $x_0 = 1$ erweitern, dann erhalten wir

\begin{equation*}
\mathbf{x}^{T}\mathbf{w} =
1 \cdot (-\theta) + x_1 w_1 + x_2 w_2 + \ldots + x_n w_n \geq 0.
\end{equation*}

Genaugenommen hätten wir jetzt natürlich für die Vektoren $\mathbf{w}$ und
$\mathbf{x}$ neue Bezeichnungen einführen müssen, aber ab sofort gehen wir immer
davon aus, dass ab jetzt immer die erweiterten Vektoren gemeint sind, die um den
negativen Schwellenwert $-\theta$ bzw. die 1 ergänzt wurden. Der negative
Schwellenwert wird in der ML-Community **Bias** oder **Bias-Einheit (Bias
Unit)** genannt.

Um jetzt klassifizieren zu können, wird auf die gewichtete Summe
$\mathbf{x}^{T}\mathbf{w}$ die Heaviside-Funktion angewendet. In späteren
Kapiteln werden wir sehen, dass auch andere Funktionstypen anstatt der
Heaviside-Funktion verwendet werden, die bessere mathematische Eigenschaften
haben. Im Folgenden nennen wir die Funktion, die auf die gewichtete Summe
angewendet wird, **Aktivierungsfunktion**.

```{admonition} Was ist ... ein Perzeptron?
:class: note
Das Perzeptron ist ein Modell, das Eingaben verarbeitet, indem es erst eine
gewichtete Summe der Eingaben bildet und dann darauf eine Aktivierungsfunktion
anwendet.
```

Eine typische Visualisierung des Perzeptrons ist in der folgenden Abbildung
gezeigt. Wir lesen es von links nach rechts und beginnen mit den Eingaben der
Merkmale, die durch (hellblaue) Kreise symbolisiert werden. In manchen
Darstellungen wird die Bias-Einheit ebenfalls durch einen Kreis symbolisiert und
als Eingabe dargestellt. Manchmal wird auf die Darstellung der Bias-Einheit
komplett verzichtet. Als Kompromiss zwischen diesen beiden Ansätzen ist in
dieser Grafik die Bias-Einheit zwar als Kreis symbolisiert, aber der Kreis
befindet sich nicht in einer Reihe mit den Merkmalen, sondern ist etwas nach
rechts eingerückt. Die Multiplikation der Inputs $x_j$ mit den Gewichten $w_j$
wird durch Kanten dargestellt. Die einzelnen Summanden $x_j w_j$ treffen sich
sozusagen im linken, mittleren Kreis, wo die gewichtete Summe $\sum_{j=0}^{n}
x_j w_j$ gebildet wird. Auf die gewichtete Summe wird dann im rechten, mittleren
Kreis eine Aktivierungsfunktion angewendet. Um zu verdeutlichen, dass hier zwei
mathematische Operationen durchgeführt werden, sind die beiden Kreise weiß
eingefärbt. Das Perzeptron berechnet dann die Ausgabe $\hat{y}$ und dieser Wert
wird dann ganz rechts als (dunkelblauer) Kreis dargestellt. Um berechnete
Ausgaben zu kennzeichnen, verwenden wir das $\wedge$-Symbol und setzen es über
das $y$, so dass das Symbol $\hat{y}$ entsteht.

```{figure} pics/fig_12_01_topology_perceptron.svg
---
name: fig_perzeptron
---
Schematische Darstellung eines Perzeptrons (Quelle: eigene Darstellung; Lizenz
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
```

Selbstverständlich können die Farben in anderen Abbildungen anders gewählt sein.
Wichtig ist die Darstellung mit Kreisen und Kanten.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir gelernt, wie ein Perzeptron aufgebaut ist und wie
aus den Daten mit Hilfe von Gewichten und einer Aktivierungsfunktion der binäre
Zustand prognostiziert wird. Im nächsten Kapitel werden wir mehrere Perzeptrons
zu mehrschichtigen Netzen verbinden und erhalten ein neuronales Netz.
