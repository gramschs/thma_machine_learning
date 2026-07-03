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

# 7.2 Multiple lineare Regression

Bisher haben wir nur ein einzelnes Merkmal aus den gesammelten Daten
herausgegriffen und untersucht, ob es zwischen diesem Merkmal und der Zielgröße
einen linearen Zusammenhang gibt. So simpel ist die Welt normalerweise nicht,
oft wirken mehrere Einflussfaktoren gleichzeitig. Daher steht die **multiple
lineare Regression** in diesem Kapitel im Fokus.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie wissen, was eine **multiple lineare Regression** ist und können sie mit
  Scikit-Learn durchführen.
* Sie wissen, was **positive lineare Korrelation** und **negative lineare
  Korrelation** bedeuten.
* Sie können die lineare Korrelation der Merkmale miteinander mit Hilfe der
  **Korrelationsmatrix** beurteilen.
* Sie können die Korrelationsmatrix als **Heatmap** visualisieren, um
  Zusammenhänge zwischen Merkmalen schnell zu erkennen.
```

## Zusammenhänge zwischen Merkmalen

Im vorherigen Kapitel haben wir den Zusammenhang des Merkmals `Leistung [PS]` und
der Zielgröße `Preis [EUR]` betrachtet. Nun wollen wir noch das Merkmal `Alter`
gemessen in Jahren hinzunehmen. 0 Jahre meint dabei einen Neuwagen. Aus
didaktischen Gründen werden wir auch hier künstlich erzeugte Daten nutzen, um
die multiple lineare Regression zu erklären. Als erstes erzeugen wir die Daten,
diesmal direkt mit Hilfsmitteln des Moduls NumPy.

```{code-cell} ipython3
import numpy as np 
import pandas as pd 

np.random.seed(0)
anzahl_autos = 100

x = np.floor( np.random.uniform(0, 11, anzahl_autos) )
y = np.floor( np.random.uniform(50, 301, anzahl_autos) )
z = np.floor( -2000 * x + 200 * y + 500 * np.random.normal(0, 1, anzahl_autos) + 10000 )

daten = pd.DataFrame({
    'Alter': x,
    'Leistung [PS]': y,
    'Preis [EUR]': z
    })
```

Dann visualisieren wir die Daten.

```{code-cell} ipython3
import plotly.express as px

fig = px.scatter_3d(daten, x = 'Alter', y = 'Leistung [PS]', z = 'Preis [EUR]',
  title='Künstliche Verkaufspreise für Autos')
fig.show()
```

Da wir mehr als drei Merkmale nicht gleichzeitig in einem Diagramm darstellen
können, nutzen wir eine Scattermatrix. Sie zeigt paarweise Zusammenhänge
zwischen allen Merkmalen.

```{code-cell} ipython3
fig = px.scatter_matrix(daten,
    title='Künstliche Daten: Verkaufspreise Autos')
fig.show()
```

Wir betrachten die letzte Zeile, in der der Preis auf der y-Achse aufgetragen
ist. In der ersten Spalte wird der Preis abhängig vom Alter dargestellt. Je
älter das Auto, desto geringer der Preis. In der zweiten Spalte wird der Preis
abhängig von der Leistung gezeigt. Je leistungsstärker ein Auto, desto höher der
Preis. Insbesondere vermittelt das Diagramm den Eindruck, dass durch die
Punktewolke sehr gut eine Regressionsgerade gelegt werden könnte, was bei dem
Zusammenhang Alter -- Preis eher fraglich ist. Zusätzlich stellen wir fest, dass
die Scattermatrix symmetrisch ist und die Hauptdiagonale die Verteilung der
Datenpunkte visualisiert.

Wir trainieren jetzt ein lineares Regressionsmodell

$$y = w_0 + w_1 \cdot x_1 + w_2 \cdot x_2.$$

Damit ist gemeint, dass wir die Gewichte $w_0, w_1$ und $w_2$ des Modells so
bestimmen wollen, dass der Preis $y$ möglichst gut durch die beiden Merkmale
Alter $x_1$ und Leistung $x_2$ prognostiziert wird.

In einem ersten Schritt laden wir das lineare Regressionsmodul.

```{code-cell} ipython3
from sklearn.linear_model import LinearRegression

modell = LinearRegression()
```

Dann adaptieren wir die Daten.

```{code-cell} ipython3
# Adaption der Daten
X = daten[['Alter', 'Leistung [PS]']]
y = daten['Preis [EUR]']
```

Jetzt können wir das lineare Regressionsmodell von Scikit-Learn mit der
`.fit()`-Methode trainieren. Wir lassen auch gleich den R²-Score mit ausgeben.

```{code-cell} ipython3
# Training
modell.fit(X, y)

# Validierung
r2_score = modell.score(X, y)
print(f'Der R2-Score ist: {r2_score:.2f}')
```

Der R²-Score ist perfekt, ob sich das Modell auf neue Daten verallgemeinern
lässt, ist damit noch nicht geklärt. Es könnte Overfitting vorliegen. Betrachten
wir nun, welche Koeffizienten von Scikit-Learn für unsere mehrdimensionale
lineare Modellfunktion gefunden wurden.

```{code-cell} ipython3
print(f'Achsenabschnitt w0: {modell.intercept_:.2f}')
print(f'Koeffizienten (Steigungen): {modell.coef_}')
```

Damit lautet unsere Modellfunktion abhängig von Alter und Leistung also

$$y = f(x_1, x_2) = 10168 -2025\cdot x_1 + 199\cdot x_2.$$

Für jedes Jahr, das das Auto altert, sinkt der Preis um 2.025 EUR (bei gleicher
Leistung), wohingegen jedes weitere PS den Preis um 199 EUR steigert (bei
gleichem Alter). Geometrisch können wir das Ergebnis so interpretieren, dass
eine Ebene durch die Datenpunkte gelegt wird.

## Korrelationsmatrix

Das Prognoseergebnis des multiplen linearen Regressionsmodell ist für die
Trainingsdaten sehr gut. Beim Betrachten der Scattermatrix scheint das Merkmal
Leistung eher einen linearen Einfluss zu haben als das Alter. Als nächstes
wollen wir bewerten, wie stark der lineare Zusammenhang jedes einzelnen Merkmals
auf jedes andere Merkmal ist. Dazu betrachten wir die sogenannte
**Korrelationsmatrix**. Mit der Methode `corr()` können wir sie einfach
berechnen lassen:

```{code-cell} ipython3
daten.corr()
```

Dabei verwendet Pandas standardmäßig den
[Pearson-Korrelationskoeffizienten](https://de.wikipedia.org/wiki/Korrelationskoeffizient_nach_Bravais-Pearson),
der Werte zwischen -1 und 1 liefert.

In der ersten Zeile 'Alter' wird die Stärke der Korrelation von dem Merkmal
Alter auf die Merkmale Alter, Leistung und Preis bewertet. Eine **positive
Korrelation** beschreibt einen Zusammenhang nach dem Prinzip "wenn mehr, dann
mehr". Beispielsweise kann mehr Leistung zu einem höhren Preis führen. Der
umgekehrte Fall ist das Prinzip "wenn mehr, dann weniger" bzw. "wenn weniger,
dann mehr", was wir **negative Korrelation** nennen. Beispielsweise kann ein
höheres Alter zu einem geringeren Preis führen.

Die Zahl 1 drückt dabei aus, dass die beiden Merkmale perfekt linear positiv
korreliert sind. In der ersten Zeile und der ersten Spalte wird der Zusammenhang
zwischen Alter und Alter bewertet. Dort muss eine 1 stehen, denn hier sind ja
beide Merkmale identisch. In der ersten Zeile und der zweiten Spalte wird die
lineare Korrelation zwischen Alter und Leistung bewertet. Die Zahl -0.074244 ist
nahe bei 0 und bedeutet daher, dass es nur einen sehr, sehr schwachen
Zusammenhang zwischen Alter und Leistung gibt, wenn überhaupt. Unser technisches
Verständnis eines Autos bestätigt, dass Alter und PS nicht zusammenhängen
(zumindest, wenn man die Leistung des Autos nimmt, wie sie im Fahrzeugschein
eingetragen ist). Dahingegen scheint es eine schwache negative Korrelation
zwischen Alter und Preis zu geben. Je älter ein Auto ist, desto geringer ist
sein Preis. -1 würde bedeuten, dass die negative Korrelation perfekt ist.

Am stärksten linear scheinen Leistung und Preis zusammenzuhängen. In der zweiten
Zeile und der dritten Spalte findet sich der Eintrag 0.914003. Je größer die
Leistung des Autos, desto höher sein Preis.

```{admonition} Mini-Übung
:class: tip
Interpretieren Sie die folgenden Korrelationswerte aus der Matrix:
1. Alter vs. Preis -0.471406: Was bedeutet das Vorzeichen? Ist der Zusammenhang
   stark oder schwach?
2. Leistung vs. Preis 0.914: Was sagt dieser Wert über den Zusammenhang aus?
3. Alter vs. Leistung -0.074: Hängen diese beiden Merkmale zusammen?
4. Zusatzfrage: Wenn der Korrelationskoeffizient zwischen zwei Merkmalen bei
   0.95 liegt, bedeutet das, dass das eine das andere verursacht?
```

```{admonition} Lösung
:class: tip
:class: dropdown, dropdown
1\. Alter vs. Preis: -0.471406

Das negative Vorzeichen bedeutet, dass ein negativer Zusammenhang besteht:
Je älter das Auto, desto niedriger tendenziell der Preis (und umgekehrt).

Der Betrag von ca. 0.47 deutet auf einen mittelstarken negativen
Zusammenhang hin. Als Faustregel gilt:

* |r| < 0.3: schwacher Zusammenhang
* 0.3 ≤ |r| < 0.7: mittelstarker Zusammenhang
* |r| ≥ 0.7: starker Zusammenhang

2\. Leistung vs. Preis: 0.914

Dieser Wert von 0.914 ist positiv und nahe bei 1, was auf einen sehr starken
positiven linearen Zusammenhang hinweist. Autos mit mehr PS haben tendenziell
einen deutlich höheren Preis. Von allen drei Merkmalen zeigt die Leistung die
stärkste Korrelation mit dem Preis.

3\. Alter vs. Leistung: -0.074

Der Wert von -0.074 liegt sehr nahe bei 0, was bedeutet, dass zwischen Alter und
Leistung praktisch kein linearer Zusammenhang besteht. Das entspricht auch
unserer Erwartung: Die PS-Zahl eines Autos (laut Fahrzeugschein) ändert sich
nicht mit dem Alter des Fahrzeugs.

4\. Zusatzfrage: Korrelation 0.95 → Kausalität?

Nein! Ein Korrelationskoeffizient von 0.95 bedeutet nicht automatisch, dass ein
Merkmal das andere verursacht. Korrelation beschreibt nur, dass zwei Merkmale
gemeinsam variieren. Mögliche Erklärungen für hohe Korrelation ohne Kausalität:

* Eine dritte Variable beeinflusst beide Merkmale.
* Der Zusammenhang ist zufällig (besonders bei kleinen Datensätzen).
* Die Kausalität verläuft in die umgekehrte Richtung als vermutet.
* Es liegt tatsächlich eine kausale Beziehung vor (muss aber separat
  nachgewiesen werden).

Beispiel: Eisverkäufe und Sonnenbrand-Fälle korrelieren stark, aber Eis
verursacht keinen Sonnenbrand. Beide werden durch eine dritte Variable (warmes
Wetter/Sonneneinstrahlung) beeinflusst.
```

```{admonition} Warnung: Korrelation ist nicht Kausalität
:class: warning
Wichtig: wenn zwei Merkmale korreliert sind, heißt das nicht, dass das eine
Merkmal das andere verursacht (Kausalität). Es kann auch eine dritte Variable
beide beeinflussen oder der Zusammenhang kann zufällig sein.
```

## Heatmaps

Es ist üblich, die Korrelationsmatrix als sogenanntes Heatmap-Diagramm zu
visualisieren. Vor allem wenn die Zusammenhänge zwischen vielen Merkmalen
untersucht werden sollen, wird die Korrelationsmatrix schnell unübersichtlich.
Bei einer Heatmap werden die Zahlenwerte der Matrix durch Farben visualisiert.
Plotly Express bietet dazu die Funktion `imshow()` an.

```{code-cell} ipython3
korrelationsmatrix = daten.corr()

fig = px.imshow(korrelationsmatrix)
fig.show()
```

Es ist hilfreich, die Werte der Korrelationsmatrix direkt in der Heatmap
anzeigen zu lassen. Daher verwenden wir die zusätzliche Option `text_auto=True`.

```{code-cell} ipython3
fig = px.imshow(korrelationsmatrix, text_auto=True)
fig.show()
```

Weitere Optionen zum Stylen der Heatmaps finden Sie in der [Plotly Dokumentation
→ Heatmaps in Plotly](https://plotly.com/python/heatmaps/).

## Zusammenfassung

In diesem Kapitel haben wir uns mit der linearen multiplen Regression
beschäftigt. Es wird eine lineare Modellfunktion für einen oder mehrere
Einflussfaktoren gesucht. Die Parameter der Modellfunktion, also die
Koeffizienten der mehrdimensionalen linearen Funktion werden so an die Daten
angepasst, dass die Fehlerquadratsumme möglichst klein wird. Um beurteilen zu
können, ob die beste gefundene Modellfunktion eine gute Prognose liefert, werten
wir den R²-Score aus.

Um zu analysieren, ob einzelne Merkmale miteinander linear korreliert sind,
werden die Korrelationsmatrix und die Heatmap eingesetzt.
