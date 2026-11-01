---
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
lineare Regression** in diesem Kapitel im Fokus. Bevor wir das Modell aufstellen,
verschaffen wir uns aber erst einen Überblick über die Zusammenhänge in den
Daten.

## Korrelationsmatrix

Im vorherigen Kapitel haben wir den Zusammenhang des Merkmals `Leistung [PS]` und
der Zielgröße `Preis [EUR]` betrachtet. Nun wollen wir noch das Merkmal `Alter`
gemessen in Jahren hinzunehmen. 0 Jahre meint dabei einen Neuwagen. Aus
didaktischen Gründen werden wir auch hier künstlich erzeugte Daten nutzen. Als
erstes erzeugen wir die Daten, diesmal direkt mit Hilfsmitteln des Moduls NumPy.

```{code-cell} python
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

```{code-cell} python
import plotly.express as px

fig = px.scatter_3d(daten, x = 'Alter', y = 'Leistung [PS]', z = 'Preis [EUR]',
  title='Künstliche Verkaufspreise für Autos')
fig.show()
```

In einem dreidimensionalen Streudiagramm können wir höchstens drei Größen als
Achsen darstellen. Um die paarweisen Zusammenhänge zwischen allen Merkmalen zu
sehen, nutzen wir zusätzlich eine Scattermatrix.

```{code-cell} python
fig = px.scatter_matrix(daten,
    title='Künstliche Daten: Verkaufspreise Autos')
fig.show()
```

Wir betrachten die letzte Zeile, in der der Preis auf der y-Achse aufgetragen
ist. In der ersten Spalte wird der Preis abhängig vom Alter dargestellt. Je
älter das Auto, desto geringer der Preis. In der zweiten Spalte wird der Preis
abhängig von der Leistung gezeigt. Je leistungsstärker ein Auto, desto höher der
Preis. Insbesondere vermittelt das Diagramm den Eindruck, dass durch die
Punktewolke sehr gut eine Regressionsgerade gelegt werden könnte, was beim
Zusammenhang zwischen Alter und Preis eher fraglich ist. Zusätzlich stellen wir
fest, dass die Scattermatrix symmetrisch ist und die Hauptdiagonale die
Verteilung der Datenpunkte visualisiert.

Beim Betrachten der Scattermatrix scheint das Merkmal Leistung stärker linear
mit dem Preis zusammenzuhängen als das Alter. Als Nächstes wollen wir bewerten,
wie stark der lineare Zusammenhang zwischen jedem Merkmal und jedem anderen
Merkmal ist. Dazu betrachten wir die sogenannte **Korrelationsmatrix**. Mit der
Methode `corr()` können wir sie einfach berechnen lassen:

```{code-cell} python
# TODO: ???  (Korrelationsmatrix berechnen)
```

Dabei verwendet Pandas standardmäßig den
[Pearson-Korrelationskoeffizienten](https://de.wikipedia.org/wiki/Korrelationskoeffizient_nach_Bravais-Pearson),
der Werte zwischen -1 und 1 liefert.

In der ersten Zeile "Alter" werden die linearen Korrelationen zwischen dem
Merkmal Alter und den Merkmalen Alter, Leistung und Preis dargestellt. Die
Korrelationsmatrix ist symmetrisch: Die Korrelation zwischen Alter und Preis ist
genauso groß wie die zwischen Preis und Alter. Eine **positive Korrelation**
beschreibt einen Zusammenhang nach dem Prinzip "wenn mehr, dann mehr".
Beispielsweise gehen in diesem Datensatz Fahrzeuge mit höherer Leistung
tendenziell mit höheren Preisen einher. Der umgekehrte Fall ist das Prinzip
"wenn mehr, dann weniger" bzw. "wenn weniger, dann mehr", was wir **negative
Korrelation** nennen. Beispielsweise weisen Fahrzeuge mit höherem Alter in
diesem Datensatz tendenziell niedrigere Preise auf.

Der Wert 1 steht für einen perfekten linearen Zusammenhang, -1 für einen
perfekten gegenläufigen. Auf der Hauptdiagonalen steht daher überall eine 1,
denn dort wird jedes Merkmal mit sich selbst verglichen.

Zwischen Alter und Leistung liegt die Korrelation mit -0.074244 sehr nahe bei 0,
es gibt also so gut wie keinen linearen Zusammenhang. Ein Wert nahe 0 schließt
dabei nur einen linearen Zusammenhang aus, ein nichtlinearer Zusammenhang könnte
trotzdem bestehen. Dass Alter und PS nicht zusammenhängen, passt zu unserem
technischen Verständnis eines Autos. Zwischen Alter und Preis besteht mit
-0.471406 ein mittelstarker negativer Zusammenhang, zwischen Leistung und Preis
mit 0.914003 ein starker positiver. Von allen Merkmalspaaren hängen Leistung und
Preis am stärksten linear zusammen. Das Alter wirkt danach eher unwichtig. Ob
das stimmt, prüfen wir später mit dem Regressionsmodell.

**Warnung: Korrelation ist nicht Kausalität**

Wichtig: wenn zwei Merkmale korreliert sind, heißt das nicht, dass das eine
Merkmal das andere verursacht (Kausalität). Es kann auch eine dritte Variable
beide beeinflussen oder der Zusammenhang kann zufällig sein.

## Heatmap

Es ist üblich, die Korrelationsmatrix als sogenannte **Heatmap** zu
visualisieren. Vor allem wenn die Zusammenhänge zwischen vielen Merkmalen
untersucht werden sollen, wird die Korrelationsmatrix schnell unübersichtlich.
Bei einer Heatmap werden die Zahlenwerte der Matrix durch Farben visualisiert.
Plotly Express bietet dazu die Funktion `imshow()` an.

Damit die Farben die Korrelationswerte gut wiedergeben, legen wir den
Farbbereich fest auf -1 bis 1 (`zmin=-1`, `zmax=1`) und wählen mit
`color_continuous_scale='RdBu_r'` eine Farbskala, bei der negative und positive
Korrelationen unterschiedliche Farben erhalten und der Wert 0 in der Mitte
liegt.

```{code-cell} python
korrelationsmatrix = daten.corr()

fig = # TODO: ???  (Heatmap der Korrelationsmatrix erzeugen, Farbbereich von -1 bis 1, rot-blaue Farbskala)
fig.show()
```

Es ist hilfreich, die Werte der Korrelationsmatrix direkt in der Heatmap
anzeigen zu lassen. Daher verwenden wir die zusätzliche Option `text_auto=True`.

```{code-cell} python
fig = px.imshow(korrelationsmatrix,
    color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
    # TODO: ???  (Zahlenwerte in den Feldern anzeigen)
)
fig.show()
```

In der Heatmap erkennen wir die stärkste Korrelation (Leistung und Preis) an der
kräftigsten Farbe, während schwache Zusammenhänge blass erscheinen.

Die Heatmap hilft auch dabei, überflüssige Merkmale zu erkennen. Die Leistung
eines Autos lässt sich zum Beispiel auch in Kilowatt statt in PS angeben. Wir
fügen diese Spalte hinzu und schauen noch einmal hin.

```{code-cell} python
daten_erweitert = daten.copy()
daten_erweitert['Leistung [kW]'] = daten_erweitert['Leistung [PS]'] * 0.7355

fig = px.imshow(daten_erweitert.corr(), text_auto=True,
    color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
fig.show()
```

Zwischen `Leistung [PS]` und `Leistung [kW]` steht eine 1, die beiden Merkmale
sind perfekt korreliert. Das ist zu erwarten, denn PS und kW sind nur zwei
Einheiten für dieselbe Größe. Solche Merkmalspaare tragen dieselbe Information,
und wir können eines davon weglassen.

Weitere Optionen zum Stylen der Heatmaps finden Sie in der [Plotly Dokumentation
→ Heatmaps in Plotly](https://plotly.com/python/heatmaps/).

## Multiple lineare Regression

Jetzt stellen wir das Modell auf. In der Korrelationsmatrix haben wir gesehen,
dass die Leistung stark mit dem Preis zusammenhängt und das Alter nur
mittelstark. Trotzdem nehmen wir beide Merkmale in das Modell auf. Wir trainieren
ein lineares Regressionsmodell

$$y = w_0 + w_1 \cdot x_1 + w_2 \cdot x_2.$$

Damit ist gemeint, dass wir die Gewichte $w_0, w_1$ und $w_2$ des Modells so
bestimmen wollen, dass der Preis $y$ möglichst gut durch die beiden Merkmale
Alter $x_1$ und Leistung $x_2$ prognostiziert wird.

In einem ersten Schritt laden wir das lineare Regressionsmodul.

```{code-cell} python
from sklearn.linear_model import LinearRegression

modell = LinearRegression()
```

Dann bringen wir die Daten in das richtige Format.

```{code-cell} python
# Daten ins richtige Format bringen
X = # TODO: ???  (Alter und Leistung als Eingabedaten auswählen)
y = daten['Preis [EUR]']
```

Jetzt können wir das lineare Regressionsmodell von Scikit-Learn mit der
`.fit()`-Methode trainieren. Wir lassen auch gleich den R²-Score mit ausgeben.

```{code-cell} python
# Training
modell.fit(X, y)

# Bewertung auf den Trainingsdaten
r2_training = modell.score(X, y)
print(f'Der R²-Score auf den Trainingsdaten ist: {r2_training:.2f}')
```

Der R²-Score auf den Trainingsdaten ist sehr hoch. Da der Wert auf zwei
Nachkommastellen gerundet ausgegeben wird, bedeutet ein ausgegebener Wert von
`1.00` nicht zwingend, dass das Modell die Daten exakt beschreibt. Der Wert sagt
zunächst nur aus, wie gut das Modell die Daten erklärt, mit denen es trainiert
wurde. Ob das Modell auch für unbekannte Daten gute Prognosen liefert, klären wir
in einem späteren Kapitel.

Betrachten wir nun, welche Koeffizienten von Scikit-Learn für unsere
mehrdimensionale lineare Modellfunktion gefunden wurden.

```{code-cell} python
print(f'Achsenabschnitt w0: {modell.intercept_:.2f}')
print(f'Koeffizienten (Steigungen): {modell.coef_}')
```

Damit lautet unsere Modellfunktion abhängig von Alter und Leistung also

$$y = f(x_1, x_2) = 10168 -2025\cdot x_1 + 199\cdot x_2.$$

Für jedes Jahr, das das Auto altert, sinkt der Preis um 2.025 EUR (bei gleicher
Leistung), wohingegen jedes weitere PS den Preis um 199 EUR steigert (bei
gleichem Alter). Der Zusatz "bei gleicher Leistung" bzw. "bei gleichem Alter" ist
wichtig: In einer multiplen linearen Regression beschreibt ein Koeffizient den
Zusammenhang eines Merkmals mit der Zielgröße, wenn die übrigen Merkmale des
Modells festgehalten werden.

Weil wir die Daten selbst mit der Vorschrift $-2000 \cdot x_1 + 200 \cdot x_2 +
10000$ plus einer zufälligen Schwankung erzeugt haben, kennen wir die wahren
Werte. Mit 10168 statt 10000, -2025 statt -2000 und 199 statt 200 rekonstruiert
Scikit-Learn den Zusammenhang, den wir in die Daten hineingesteckt haben.

In der Korrelationsmatrix wirkte das Alter eher unwichtig, seine Korrelation mit
dem Preis war nur mittelstark. Das Regressionsmodell gewichtet das Alter dagegen
deutlich, mit jedem Jahr sinkt der Preis um rund 2.025 EUR. Der scheinbare
Widerspruch entsteht, weil der Korrelationskoeffizient immer nur zwei Merkmale
allein betrachtet. Die Leistung streut in unseren Daten stark und verursacht
große Preisunterschiede. Diese Streuung überlagert den Alterseffekt, sobald wir
nur Alter und Preis anschauen. Die multiple lineare Regression trennt beide
Merkmale dagegen sauber, weil sie das Alter bei gleicher Leistung bewertet.

Geometrisch wird eine Ebene so an die Datenpunkte angepasst, dass die
Fehlerquadratsumme zwischen den beobachteten und den vorhergesagten Preisen
möglichst klein wird. Die Ebene verläuft also nicht exakt durch alle
Datenpunkte.

## Zusammenfassung

In diesem Kapitel haben wir zuerst die Zusammenhänge zwischen den Merkmalen
untersucht. Die Korrelationsmatrix und ihre Visualisierung als Heatmap zeigen,
wie stark je zwei Merkmale linear zusammenhängen. Eine Korrelation belegt dabei
keinen kausalen Zusammenhang.

Anschließend haben wir die multiple lineare Regression kennengelernt. Dabei wird
eine lineare Modellfunktion verwendet, um eine Zielgröße anhand mehrerer Merkmale
zu beschreiben. Die Koeffizienten der Modellfunktion werden so an die Daten
angepasst, dass die Fehlerquadratsumme zwischen den beobachteten und den
vorhergesagten Werten möglichst klein wird. Der R²-Score beschreibt, wie gut die
Modellfunktion die betrachteten Daten erklärt. Ob ein Modell auch für unbekannte
Daten gute Prognosen liefert, untersuchen wir in einem späteren Kapitel.

## Mini-Übungen

### Mini-Übung 1

Interpretieren Sie die folgenden Korrelationswerte aus der Matrix:
1. Alter vs. Preis -0.471406: Was bedeutet das Vorzeichen? Ist der Zusammenhang
   stark oder schwach?
2. Leistung vs. Preis 0.914: Was sagt dieser Wert über den Zusammenhang aus?
3. Alter vs. Leistung -0.074: Hängen diese beiden Merkmale zusammen?
4. Zusatzfrage: Wenn der Korrelationskoeffizient zwischen zwei Merkmalen bei
   0.95 liegt, bedeutet das, dass das eine das andere verursacht?

### Mini-Übung 2

Verwenden Sie erneut den Datensatz `3ddruck_xxs.csv` mit den 18
3D-Druckversuchen. Diesmal soll die Zugfestigkeit nicht nur von der Infill-Dichte
abhängen, sondern zusätzlich von der Schichthöhe.

1. Lesen Sie die Datei ein und verwenden Sie die Nummer als Zeilenindex.
2. Trainieren Sie ein multiples lineares Regressionsmodell mit den Merkmalen
   `Infill (%)` und `Schichthoehe (mm)` und der Zielgröße `Zugfestigkeit (MPa)`.
   Achten Sie auf das richtige Format der Eingabedaten.
3. Lesen Sie Achsenabschnitt und Koeffizienten aus und notieren Sie die
   Modellgleichung.
4. Interpretieren Sie die beiden Koeffizienten. Denken Sie dabei an den Zusatz
   "bei gleichem anderen Merkmal".
5. Welche Zugfestigkeit prognostiziert das Modell für ein Druckteil mit einem
   Infill von 55 Prozent und einer Schichthöhe von 0.2 mm?
6. In Kapitel 7.1 war der R²-Score mit dem einzelnen Merkmal `Infill (%)` rund
   0.78. Wie verändert er sich, wenn die Schichthöhe als zweites Merkmal
   hinzukommt?

```{code-cell}
# Code-Zelle
```
