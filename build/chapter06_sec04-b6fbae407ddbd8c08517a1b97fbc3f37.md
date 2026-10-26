---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
downloads:
  - file: ../notebooks/chapter06/chapter06_sec04.ipynb
    title: chapter06_sec04.ipynb
  - file: pokemon_DE.csv
    title: pokemon_DE.csv
  - file: olympia_rio2016.csv
    title: olympia_rio2016.csv
  - file: ai4i2020_DE.csv
    title: ai4i2020_DE.csv
  - file: wetter_mannheim_2025.csv
    title: wetter_mannheim_2025.csv
  - file: wetter_mannheim_2024.csv
    title: wetter_mannheim_2024.csv
  - file: chapter06_sec04.md
    title: chapter06_sec04.md
---

# 6.4 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 6.1 bis 6.3. Rechnen Sie mit gut eineinhalb Stunden
Bearbeitungszeit. In diesem Kapitel trainieren wir zum ersten Mal echte
ML-Modelle. Deshalb liegt der Schwerpunkt auf zwei Mini-Projekten, die
Aufgaben 6.1 bis 6.3 bereiten darauf vor.

Der Schwierigkeitsgrad steht im Titel jeder Aufgabe:

* ✩ Verständnis: Code und Ausgaben vorhersagen und erklären (ca. 5 min)
* ✩✩ Anwendung: eigenen Code schreiben und Ergebnisse interpretieren (ca. 10 min)
* ✩✩✩ Mini-Projekt: mehrere Konzepte des Kapitels kombinieren (ca. 30 min)

In den Mini-Projekten finden Sie bei einigen Teilen einen Kontrollwert. Damit
können Sie prüfen, ob Ihr Zwischenergebnis stimmt, bevor Sie weiterarbeiten.
Setzen Sie bei allen Entscheidungsbäumen wie in den Kapiteln 6.2 und 6.3
`random_state=0`. Dann stimmen Ihre Ergebnisse mit den Lösungen überein. Mit
einem anderen Wert können sich vor allem Bäume ohne Begrenzung leicht
unterscheiden.

Alle Datensätze stehen über das Download-Symbol rechts oben zur Verfügung.
Speichern Sie sie in denselben Ordner wie dieses Jupyter Notebook. Bis auf
`wetter_mannheim_2024.csv` kennen Sie alle Datensätze bereits aus den Kapiteln
4.4 und 5.4.

* `pokemon_DE.csv`: Werte von 800 Pokémon aus den Videospielen der
  Generationen 1 bis 6, Spaltennamen und Typen ins Deutsche übersetzt (Quelle:
  [Kaggle, Pokemon with stats](https://www.kaggle.com/datasets/abcsds/pokemon),
  Lizenz CC0)
* `olympia_rio2016.csv`: Athletinnen und Athleten der Olympischen
  Sommerspiele 2016 in acht Sportarten, ohne Namen, Spaltennamen und Einträge
  ins Deutsche übersetzt (Quelle: [R. H. Griffin, 120 years of Olympic
  history: athletes and results,
  Kaggle](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results),
  Lizenz CC0)
* `ai4i2020_DE.csv`: synthetische Prozessdaten einer Werkzeugmaschine,
  Spaltennamen ins Deutsche übersetzt (Quelle: [S. Matzka, AI4I 2020
  Predictive Maintenance Dataset, UCI Machine Learning
  Repository](https://doi.org/10.24432/C5HS5C), Lizenz CC BY 4.0)
* `wetter_mannheim_2025.csv` und `wetter_mannheim_2024.csv`: Tageswerte der
  Wetterstation Mannheim in den Jahren 2025 und 2024 (Quelle: [Deutscher
  Wetterdienst, Climate Data
  Center](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/),
  Lizenz CC BY 4.0)

````{admonition} Aufgabe 6.1 (✩) Ein Baum mit einer einzigen Frage
:class: tip
Wir verwenden wieder die Datei `pokemon_DE.csv`. 65 der 800 Pokémon sind
legendär. Gegeben ist folgender Code:

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree

pokemon = pd.read_csv('pokemon_DE.csv', index_col=1)

X = pokemon[['Gesamt']]
y = pokemon['Legendaer']

modell = DecisionTreeClassifier(max_depth=1, random_state=0)
modell.fit(X, y)

plot_tree(modell, feature_names=['Gesamt'], class_names=['ja', 'nein']);

accuracy_training = modell.score(X, y)
print(f'Accuracy Trainingsdaten: {accuracy_training:.3f}')

neue_pokemon = pd.DataFrame({'Gesamt': [300, 680]},
                            index=['Pokémon A', 'Pokémon B'])
print(modell.predict(neue_pokemon))
```

Notieren Sie Ihre Vermutung in einer Markdown-Zelle, bevor Sie den Code
ausführen.

1. Welche Werte stehen im Wurzelknoten bei `samples` und `value`? In
   `class_names` steht `'ja'` vor `'nein'`. Warum? Was würde passieren, wenn
   wir `class_names=['nein', 'ja']` schreiben?
2. Berechnen Sie das Gini-Impurity-Kriterium des Wurzelknotens von Hand.
3. Der Baum stellt die Frage `Gesamt <= 579.5`. Alle legendären Pokémon haben
   einen höheren Gesamtwert, außerdem 48 nicht legendäre Pokémon, vor allem
   Mega-Entwicklungen. Welche Werte stehen in den beiden Blättern bei
   `samples` und `value`? Welche Klasse bekommt jedes Blatt?
4. Berechnen Sie die Accuracy aus den Angaben in den Blättern.
5. Welche Prognose gibt der Baum für Pokémon A und Pokémon B ab?
6. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
Der Code ist vollständig gegeben. Zusätzlich lassen wir uns die Reihenfolge
der Klassen ausgeben:

```python
print(modell.classes_)
```

Ausgabe:
```
Accuracy Trainingsdaten: 0.940
['nein' 'ja']
['ja' 'nein']
```
1. Im Wurzelknoten stehen alle Pokémon, also `samples = 800` und
   `value = [65, 735]`. Scikit-Learn sortiert die Klassen der Zielgröße, bei
   Text alphabetisch. So wie im Autohaus-Beispiel `False` vor `True` stand,
   steht hier `'ja'` vor `'nein'`. Das zeigt `modell.classes_`. Die Liste
   `class_names` vergibt nur Namen in dieser Reihenfolge. Mit
   `class_names=['nein', 'ja']` wären alle Klassen im Diagramm falsch
   beschriftet, und Python würde keine Fehlermeldung ausgeben.
2. Der Anteil der legendären Pokémon ist $p = 65/800 = 0.08125$. Damit ist
   $\text{GI} = 1 - 0.08125^2 - 0.91875^2 \approx 0.149$. Der Wert ist klein,
   weil fast alle Pokémon zur Klasse "nein" gehören.
3. Im linken Blatt (`Gesamt <= 579.5`) stehen `samples = 687` und
   `value = [0, 687]`. Das Blatt ist rein und bekommt die Klasse "nein". Im
   rechten Blatt stehen `samples = 113` und `value = [65, 48]`. Die Mehrheit
   ist legendär, daher bekommt das Blatt die Klasse "ja".
4. Richtig sind die 687 Pokémon im linken Blatt und die 65 legendären Pokémon
   im rechten Blatt, also $752/800 = 0.94$.
5. Pokémon A landet im linken Blatt und wird als "nein" prognostiziert,
   Pokémon B im rechten Blatt als "ja".
````

````{admonition} Aufgabe 6.2 (✩) Hyperparameter vorhersagen
:class: tip
Jetzt verwenden wir die sechs Kampfwerte als Merkmale. Gegeben ist folgender
Code:

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

pokemon = pd.read_csv('pokemon_DE.csv', index_col=1)

kampfwerte = ['KP', 'Angriff', 'Verteidigung', 'Spezial-Angriff',
              'Spezial-Verteidigung', 'Initiative']
X = pokemon[kampfwerte]
y = pokemon['Legendaer']

modell_a = DecisionTreeClassifier(random_state=0)
modell_b = DecisionTreeClassifier(max_depth=2, random_state=0)
modell_c = DecisionTreeClassifier(min_samples_leaf=401, random_state=0)
modell_d = DecisionTreeClassifier(random_state=1)

modell_a.fit(X, y)
modell_b.fit(X, y)
modell_c.fit(X, y)
modell_d.fit(X, y)

print(f'A: Accuracy {modell_a.score(X, y):.3f}, Tiefe {modell_a.get_depth()}')
print(f'B: Accuracy {modell_b.score(X, y):.3f}, Tiefe {modell_b.get_depth()}')
print(f'C: Accuracy {modell_c.score(X, y):.3f}, Tiefe {modell_c.get_depth()}')
print(f'D: Accuracy {modell_d.score(X, y):.3f}, Tiefe {modell_d.get_depth()}')
```

Notieren Sie Ihre Vermutung in einer Markdown-Zelle, bevor Sie den Code
ausführen.

1. Ordnen Sie die Modelle A, B und C nach ihrer Accuracy auf den
   Trainingsdaten.
2. Modell C verlangt mindestens 401 Pokémon in jedem Blatt. Wie viele Fragen
   kann dieser Baum stellen? Welche Accuracy erwarten Sie?
3. Modell A ist nicht begrenzt. Erreicht es eine Accuracy von 1.0? Die sechs
   Pokémon Mew, Celebi, Jirachi, Manaphy, Shaymin (Land-Form) und Victini
   haben in allen sechs Kampfwerten den Wert 100. Nur Jirachi, Shaymin und
   Victini sind legendär.
4. Modell D unterscheidet sich von Modell A nur im `random_state`. Ändert sich
   die Accuracy?
5. Welches Modell zeigt die stärkste Tendenz zum Overfitting?
6. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
Der Code ist vollständig gegeben. Zusätzlich lassen wir uns die Prognose von
Modell A für Mew und Jirachi ausgeben:

```python
print(modell_a.predict(pokemon.loc[['Mew', 'Jirachi'], kampfwerte]))
```

Ausgabe:
```
A: Accuracy 0.996, Tiefe 10
B: Accuracy 0.940, Tiefe 2
C: Accuracy 0.919, Tiefe 0
D: Accuracy 0.996, Tiefe 10
['ja' 'ja']
```
1. Modell A hat die höchste Accuracy, dann folgen B und C.
2. Ein Baum mit einer Frage teilt die 800 Pokémon in zwei Blätter auf. Dann
   kann nicht in beiden Blättern mindestens 401 Pokémon liegen. Modell C
   stellt also keine einzige Frage, der Baum besteht nur aus dem
   Wurzelknoten. Er hat die Tiefe 0 und prognostiziert für jedes Pokémon die
   häufigste Klasse "nein". Die Accuracy ist der Anteil der nicht legendären
   Pokémon, $735/800 \approx 0.919$.
3. Nein. Die sechs Pokémon mit identischen Kampfwerten landen im selben Blatt,
   egal welche Fragen der Baum stellt. Das Blatt enthält 3 legendäre und 3
   nicht legendäre Pokémon. Bei diesem Gleichstand wählt Scikit-Learn die
   erste Klasse, hier "ja". Mew, Celebi und Manaphy werden daher falsch
   klassifiziert, die Accuracy ist $797/800 \approx 0.996$. Wenn sich
   Datenpunkte mit gleichen Merkmalen in der Zielgröße unterscheiden, kann
   kein Entscheidungsbaum alle richtig klassifizieren.
4. Nein. Der `random_state` entscheidet nur, welcher von mehreren gleich guten
   Splits gewählt wird. Accuracy und Tiefe bleiben hier gleich.
5. Modell A (und ebenso D). Es braucht 10 Ebenen, um gerade einmal 5.6
   Prozentpunkte mehr Accuracy als Modell B mit 2 Ebenen zu erreichen. Eine
   hohe Accuracy, die nur ein deutlich komplexeres Modell erreicht, ist ein
   Warnsignal für Overfitting.
````

````{admonition} Aufgabe 6.3 (✩✩) Basketball oder Volleyball?
:class: tip
In Aufgabe 5.5 haben wir gesehen, dass die Basketballerinnen und Basketballer
in Rio 2016 im Durchschnitt nur knapp 2 cm größer waren als die
Volleyballerinnen und Volleyballer. Kann ein Entscheidungsbaum die beiden
Sportarten trotzdem an den Körpermaßen unterscheiden?

1. Lesen Sie die Datei `olympia_rio2016.csv` mit der Spalte `Nr.` als
   Zeilenindex ein und behalten Sie nur die Personen, die Basketball oder
   Volleyball spielen. Bei einer Person fehlt das Gewicht. Entfernen Sie
   diese Person, indem Sie nur Personen mit einem Gewicht über 0 kg behalten.
   Wie wir systematisch mit fehlenden Werten umgehen, lernen wir in Kapitel
   8.1. Wie viele Personen bleiben übrig? Welche Accuracy erreicht ein Modell,
   das immer die häufigere Sportart prognostiziert?
2. Trainieren Sie mit den Merkmalen Körpergröße und Gewicht einen
   Entscheidungsbaum mit der maximalen Tiefe 2 und einen ohne Begrenzung.
   Vergleichen Sie Accuracy und Tiefe der beiden Bäume. Lassen Sie sich den
   Baum mit der Tiefe 2 anzeigen und deuten Sie ihn.
3. Auch ohne Begrenzung erreicht der Baum keine Accuracy von 1.0. Woran liegt
   das? Denken Sie an die Histogramme der Körpergröße aus Aufgabe 5.5.
4. Nehmen Sie das Alter als drittes Merkmal hinzu und trainieren Sie erneut
   einen Baum ohne Begrenzung. Hat der Baum jetzt mehr über Basketball und
   Volleyball gelernt?
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree

olympia = pd.read_csv('olympia_rio2016.csv', index_col=0)

# Nur Basketball und Volleyball, nur Personen mit Gewichtsangabe
auswahl = olympia[olympia['Sportart'].isin(['Basketball', 'Volleyball'])]
auswahl = auswahl[auswahl['Gewicht (kg)'] > 0]
print(f'Anzahl Personen: {len(auswahl)}')
print(auswahl['Sportart'].value_counts())

# Körpergröße und Gewicht als Merkmale
X = auswahl[['Groesse (cm)', 'Gewicht (kg)']]
y = auswahl['Sportart']

modell_tiefe2 = DecisionTreeClassifier(max_depth=2, random_state=0)
modell_tiefe2.fit(X, y)
print(f'Tiefe 2: Accuracy {modell_tiefe2.score(X, y):.3f}')

modell_unbegrenzt = DecisionTreeClassifier(random_state=0)
modell_unbegrenzt.fit(X, y)
accuracy_training = modell_unbegrenzt.score(X, y)
print(f'ohne Begrenzung: Accuracy {accuracy_training:.3f}, Tiefe {modell_unbegrenzt.get_depth()}')

# Personen mit 193 cm und 82 kg
gleiche_masse = auswahl[(auswahl['Groesse (cm)'] == 193) & (auswahl['Gewicht (kg)'] == 82)]
print(gleiche_masse['Sportart'].value_counts())

# Alter als drittes Merkmal
X_alter = auswahl[['Groesse (cm)', 'Gewicht (kg)', 'Alter']]
modell_alter = DecisionTreeClassifier(random_state=0)
modell_alter.fit(X_alter, y)
accuracy_training = modell_alter.score(X_alter, y)
print(f'mit Alter: Accuracy {accuracy_training:.3f}, Tiefe {modell_alter.get_depth()}')

plot_tree(modell_tiefe2, feature_names=['Groesse (cm)', 'Gewicht (kg)'],
          class_names=['Basketball', 'Volleyball']);
```
Ausgabe:
```
Anzahl Personen: 563
Sportart
Volleyball    283
Basketball    280
Name: count, dtype: int64
Tiefe 2: Accuracy 0.599
ohne Begrenzung: Accuracy 0.906, Tiefe 18
Sportart
Volleyball    2
Basketball    2
Name: count, dtype: int64
mit Alter: Accuracy 0.993, Tiefe 23
```
1. Es bleiben 563 Personen übrig, 283 im Volleyball und 280 im Basketball.
   Ein Modell, das immer Volleyball prognostiziert, erreicht
   $283/563 \approx 0.503$. Das ist kaum besser als Raten mit einer Münze.
2. Der Baum mit der Tiefe 2 erreicht nur 0.599. Er fragt zuerst nach dem
   Gewicht: Personen über 101.5 kg ordnet er dem Basketball zu, alle anderen
   dem Volleyball. Die Blätter sind aber stark gemischt. Im größten Blatt
   stehen 178 Basketballerinnen und Basketballer neben 196 Volleyballerinnen
   und Volleyballern. Der Baum ohne Begrenzung erreicht 0.906, braucht dafür
   aber 18 Ebenen. Viele seiner Blätter enthalten nur wenige Personen.
3. Viele Personen haben genau dieselbe Körpergröße und dasselbe Gewicht, weil
   die Angaben auf ganze Zentimeter und Kilogramm gerundet sind. Zum Beispiel
   sind 4 Personen 193 cm groß und 82 kg schwer, 2 davon spielen Basketball
   und 2 Volleyball. Solche Personen landen immer im selben Blatt, und der
   Baum kann nicht alle richtig einordnen. Bei 241 der 563 Personen gibt es
   mindestens eine weitere Person mit denselben Maßen.
4. Mit dem Alter steigt die Accuracy auf 0.993 bei einer Tiefe von 23. Gelernt
   hat der Baum dabei nichts über die Sportarten. Mit dem Alter kann er auch
   Personen mit gleichen Maßen voneinander unterscheiden und so einzelne
   Personen auswendig lernen. Das ist Overfitting. Ob Körpergröße und Gewicht
   wenigstens ein bisschen über die Sportart verraten, können wir erst mit
   Daten prüfen, die der Baum beim Training nicht gesehen hat. Genau das
   machen wir im zweiten Mini-Projekt.
````

````{admonition} Aufgabe 6.4 (✩✩✩) Mini-Projekt: Ausfallregeln wiederentdecken
:class: tip
In den Mini-Projekten der Kapitel 4.4 und 5.4 haben wir in der Datei
`ai4i2020_DE.csv` nach den Regeln gesucht, nach denen die Werkzeugmaschine
ausfällt. Die Grenzen für den Leistungsausfall haben wir im Scatterplot
abgelesen, die Grenzen für den Überlastausfall haben wir mit `.groupby()`
eingegrenzt. Jetzt soll ein Entscheidungsbaum diese Arbeit übernehmen. Zur
Erinnerung: Die Spalten `Ausfall Leistung` und `Ausfall Waermeabfuhr` enthalten
eine 1, wenn die Maschine aus diesem Grund ausgefallen ist, sonst eine 0.

**Teil 1:** Lesen Sie die Datei mit der Spalte `Nr.` als Zeilenindex ein und
erweitern Sie die Tabelle wie in Aufgabe 4.7 um die Spalte `Leistung (W)`.
Trainieren Sie einen Entscheidungsbaum mit der maximalen Tiefe 2, der aus der
Leistung prognostiziert, ob ein Leistungsausfall vorliegt. Lassen Sie sich den
Baum anzeigen. Bei welchen Leistungen liegen die Grenzen? Vergleichen Sie mit
Ihrem Ergebnis aus Aufgabe 4.7. Welche Accuracy erreicht der Baum, und was
ändert sich ohne Begrenzung der Tiefe?

Zur Kontrolle: Prozess Nr. 51 hat eine Leistung von rund 1378 W.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
```python
import pandas as pd
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier, plot_tree

maschinendaten = pd.read_csv('ai4i2020_DE.csv', index_col=0)
maschinendaten['Leistung (W)'] = maschinendaten['Drehmoment (Nm)'] * 2 * 3.1416 * maschinendaten['Drehzahl (1/min)'] / 60
print(f"Leistung Prozess Nr. 51: {maschinendaten.loc[51, 'Leistung (W)']:.0f} W")

X_leistung = maschinendaten[['Leistung (W)']]
y_leistung = maschinendaten['Ausfall Leistung']

modell = DecisionTreeClassifier(max_depth=2, random_state=0)
modell.fit(X_leistung, y_leistung)
print(f'Tiefe 2: Accuracy {modell.score(X_leistung, y_leistung):.4f}')

modell_unbegrenzt = DecisionTreeClassifier(random_state=0)
modell_unbegrenzt.fit(X_leistung, y_leistung)
accuracy_training = modell_unbegrenzt.score(X_leistung, y_leistung)
print(f'ohne Begrenzung: Accuracy {accuracy_training:.4f}, Tiefe {modell_unbegrenzt.get_depth()}')

plot_tree(modell, feature_names=['Leistung (W)'],
          class_names=['kein Ausfall', 'Ausfall']);
```
Ausgabe:
```
Leistung Prozess Nr. 51: 1378 W
Tiefe 2: Accuracy 1.0000
ohne Begrenzung: Accuracy 1.0000, Tiefe 2
```
Der Baum fragt zuerst `Leistung (W) <= 9001.25` und im linken Zweig danach
`Leistung (W) <= 3496.145`. Alle drei Blätter sind rein: 31 Prozesse mit sehr
kleiner und 64 Prozesse mit sehr großer Leistung sind ausgefallen, die übrigen
9905 Prozesse nicht. Die Grenzen liegen also bei rund 3500 W und 9000 W. Das
passt zu dem, was wir in Aufgabe 4.7 im Scatterplot abgelesen haben, und genau
diese Grenzen nennt die Dokumentation des Datensatzes. Der Baum erreicht eine
Accuracy von 1.0. Ohne Begrenzung ändert sich nichts. Weil alle Blätter schon
rein sind, gibt es nichts weiter aufzuteilen, und der Baum hört bei der Tiefe 2
auf.
````

```{admonition} Aufgabe 6.4 Fortsetzung (Teil 2)
:class: tip
**Teil 2:** Ein Entscheidungsbaum stellt immer Fragen der Form "Ist ein
Merkmal kleiner oder gleich einer Grenze?". Was passiert, wenn wir ihm die
Leistung nicht verraten? Trainieren Sie für dieselbe Zielgröße Bäume, die nur
die Drehzahl
und das Drehmoment kennen, mit den maximalen Tiefen 2 und 4 und ohne
Begrenzung. Hinweis: `max_depth=None` steht für "ohne Begrenzung" und ist die
Standardeinstellung. Damit können Sie alle drei Bäume in einer for-Schleife
über eine Liste trainieren. Vergleichen Sie Accuracy und Tiefe mit Teil 1.

Erstellen Sie dann einen Scatterplot mit der Drehzahl auf der x-Achse und dem
Drehmoment auf der y-Achse, eingefärbt nach `Ausfall Leistung`. Warum braucht
der Baum ohne die Leistung so viel mehr Fragen?

Zur Kontrolle: Mit der Tiefe 2 erreicht der Baum eine Accuracy von 0.9962.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
X_antrieb = maschinendaten[['Drehzahl (1/min)', 'Drehmoment (Nm)']]

for tiefe in [2, 4, None]:
    modell = DecisionTreeClassifier(max_depth=tiefe, random_state=0)
    modell.fit(X_antrieb, y_leistung)
    accuracy_training = modell.score(X_antrieb, y_leistung)
    print(f'max_depth={tiefe}: Accuracy {accuracy_training:.4f}, Tiefe {modell.get_depth()}')

fig = px.scatter(maschinendaten, x='Drehzahl (1/min)', y='Drehmoment (Nm)',
                 color='Ausfall Leistung',
                 title='Leistungsausfälle in Abhängigkeit von Drehzahl und Drehmoment')
fig.show()
```
Ausgabe:
```
max_depth=2: Accuracy 0.9962, Tiefe 2
max_depth=4: Accuracy 0.9984, Tiefe 4
max_depth=None: Accuracy 1.0000, Tiefe 10
```
Mit der Tiefe 2 erreicht der Baum 0.9962, mit der Tiefe 4 schon 0.9984. Für
eine Accuracy von 1.0 braucht er aber 10 Ebenen statt 2 wie in Teil 1.

Im Scatterplot liegen die Leistungsausfälle an zwei Rändern der Punktwolke:
rechts unten bei hoher Drehzahl und kleinem Drehmoment (Leistung zu klein)
und links oben bei kleiner Drehzahl und großem Drehmoment (Leistung zu groß).
Die Grenzen sind gekrümmte Kurven. Bei konstanter Leistung
$P = M \cdot 2 \pi n / 60$ halbiert sich das Drehmoment, wenn sich die Drehzahl
verdoppelt. Jede Frage des Baums entspricht im Scatterplot aber einer
waagerechten oder senkrechten Linie, wie wir es in Kapitel 6.1 beim Autohaus
gesehen haben. Eine gekrümmte Grenze kann der Baum nur mit vielen kleinen
Stufen annähern. Kennt er die Leistung, reicht eine einzige Frage pro Grenze.
Ein Merkmal, das wir aus physikalischem Wissen berechnen, erspart dem Baum
also viel Arbeit und macht ihn leichter verständlich.
````

```{admonition} Aufgabe 6.4 Fortsetzung (Teil 3)
:class: tip
**Teil 3:** Ein Ausfall der Wärmeabfuhr hängt von der Differenz zwischen
Prozess- und Lufttemperatur und von der Drehzahl ab. Erweitern Sie die Tabelle
um eine Spalte `Temperaturdifferenz (K)`. Trainieren Sie zwei Bäume, die mit der
Temperaturdifferenz und der Drehzahl prognostizieren, ob die Wärmeabfuhr
ausfällt, einen mit der maximalen Tiefe 1 und einen mit der maximalen Tiefe 2.
Lassen Sie sich beide Bäume in getrennten Code-Zellen anzeigen.

1. Wie viele Ausfälle der Wärmeabfuhr erkennt der Baum mit der Tiefe 1?
   Vergleichen Sie seine Accuracy mit dem Anteil der Prozesse, bei denen die
   Wärmeabfuhr nicht ausgefallen ist.
2. Beide Blätter dieses Baums gehören zur selben Klasse. Warum stellt der Baum
   die Frage trotzdem? Berechnen Sie dazu aus den Angaben im Diagramm die
   Gesamt-Unreinheit der beiden Blätter. Gewichten Sie dafür den Gini-Wert
   jedes Blatts mit seinem Anteil an allen Prozessen.
3. Welche Regel hat der Baum mit der Tiefe 2 gefunden? Formulieren Sie sie in
   Worten.

Zur Kontrolle: Bei 115 Prozessen ist die Wärmeabfuhr ausgefallen.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
maschinendaten['Temperaturdifferenz (K)'] = maschinendaten['Prozesstemperatur (K)'] - maschinendaten['Lufttemperatur (K)']

X_waerme = maschinendaten[['Temperaturdifferenz (K)', 'Drehzahl (1/min)']]
y_waerme = maschinendaten['Ausfall Waermeabfuhr']
print(y_waerme.value_counts())

modell_tiefe1 = DecisionTreeClassifier(max_depth=1, random_state=0)
modell_tiefe1.fit(X_waerme, y_waerme)
print(f'Tiefe 1: Accuracy {modell_tiefe1.score(X_waerme, y_waerme):.4f}')

plot_tree(modell_tiefe1, feature_names=['Temperaturdifferenz (K)', 'Drehzahl (1/min)'],
          class_names=['kein Ausfall', 'Ausfall']);
```
Ausgabe:
```
Ausfall Waermeabfuhr
0    9885
1     115
Name: count, dtype: int64
Tiefe 1: Accuracy 0.9885
```
In einer neuen Code-Zelle:
```python
modell_tiefe2 = DecisionTreeClassifier(max_depth=2, random_state=0)
modell_tiefe2.fit(X_waerme, y_waerme)
print(f'Tiefe 2: Accuracy {modell_tiefe2.score(X_waerme, y_waerme):.4f}')

plot_tree(modell_tiefe2, feature_names=['Temperaturdifferenz (K)', 'Drehzahl (1/min)'],
          class_names=['kein Ausfall', 'Ausfall']);
```
Ausgabe:
```
Tiefe 2: Accuracy 0.9985
```
1. Der Baum mit der Tiefe 1 fragt `Temperaturdifferenz (K) <= 8.65`. Beide
   Blätter bekommen die Klasse "kein Ausfall", der Baum erkennt also keinen
   einzigen Ausfall. Trotzdem erreicht er eine Accuracy von 0.9885. Das ist
   genau der Anteil der Prozesse ohne Ausfall der Wärmeabfuhr,
   $9885/10000$. Wenn eine Klasse sehr selten ist, sagt eine hohe Accuracy
   wenig aus. Gütemaße, die das berücksichtigen, lernen wir in Kapitel 10.3
   kennen.
2. Im Wurzelknoten ist der Gini-Wert 0.023. Das linke Blatt enthält 805
   Prozesse mit dem Gini-Wert 0.245, das rechte Blatt 9195 Prozesse ohne
   Ausfall mit dem Gini-Wert 0. Die Gesamt-Unreinheit der beiden Blätter ist
   $\frac{805}{10000} \cdot 0.245 + \frac{9195}{10000} \cdot 0 \approx 0.020$.
   Sie ist kleiner als im Wurzelknoten. Der Baum wählt seine Fragen nach der
   Reinheit, nicht nach der Accuracy. Die Frage sortiert alle Ausfälle in das
   linke Blatt, auch wenn dort die Prozesse ohne Ausfall noch in der Mehrheit
   sind.
3. Der Baum mit der Tiefe 2 fragt im linken Zweig zusätzlich
   `Drehzahl (1/min) <= 1380.0`. Die Regel lautet: Die Wärmeabfuhr fällt aus,
   wenn die Temperaturdifferenz höchstens 8.65 K und die Drehzahl höchstens
   1380 1/min beträgt. Laut Dokumentation lautet die Regel "Differenz unter
   8.6 K und Drehzahl unter 1380 1/min". In dem Blatt mit allen 115 Ausfällen
   stehen noch 15 Prozesse ohne Ausfall. Bei ihnen beträgt die
   Temperaturdifferenz genau 8.6 K, sie liegen also genau auf der Grenze. Die
   Temperaturen sind auf 0.1 K gerundet, daher lässt sich an dieser Grenze
   nicht sauber trennen. Die Accuracy steigt auf 0.9985.
````

```{admonition} Aufgabe 6.4 Fortsetzung (Abschlussfrage)
:class: tip
**Abschlussfrage:** In allen drei Teilen erreichen die Bäume auf den
Trainingsdaten eine Accuracy von 1.0 oder knapp darunter. In Kapitel 6.3 haben
wir gelernt, dass eine so hohe Accuracy auf Overfitting hindeuten kann. Ist das
hier der Fall? Vergleichen Sie dazu die Tiefe der Bäume aus Teil 1 und Teil 2.
```

````{admonition} Lösung Abschlussfrage
:class: tip
:class: dropdown
Beim Baum aus Teil 1 nicht. Er stellt nur zwei Fragen und findet genau die
Regel, mit der das Programm die Leistungsausfälle erzeugt hat. Die Daten sind
synthetisch und folgen festen Regeln ohne zufällige Abweichungen. Eine
Accuracy von 1.0 bedeutet hier, dass das Modell die Daten wirklich erklärt.

Anders sieht es beim Baum ohne Begrenzung aus Teil 2 aus. Er braucht 10
Ebenen und nähert die gekrümmten Grenzen mit vielen Stufen an, die genau zu
diesen 10000 Prozessen passen. Ein neuer Prozess, der nahe an der Grenze
zwischen zwei Stufen liegt, könnte falsch eingeordnet werden. Eine hohe
Accuracy, die nur ein deutlich komplexeres Modell erreicht, ist das
Warnsignal aus Kapitel 6.3. Im nächsten Mini-Projekt sehen wir, was mit
einem solchen Baum bei echten, verrauschten Daten passiert.
````

````{admonition} Aufgabe 6.5 (✩✩✩) Mini-Projekt: Regentage erkennen
:class: tip
Die Wetterstation Mannheim misst jeden Tag die Sonnenscheindauer und die
Temperaturen. Lässt sich daraus ablesen, ob es an diesem Tag geregnet hat?
Eine Wettervorhersage ist das nicht, denn die Messwerte stehen erst am Ende
des Tages fest. Die Frage ist aber ein gutes Beispiel für echte Daten, die
nicht nach festen Regeln entstehen. Wir trainieren mit dem Jahr 2025 und
prüfen am Ende mit dem Jahr 2024, ob der Baum auch für ein Jahr funktioniert,
das er beim Training nie gesehen hat.

**Teil 1:** Lesen Sie die Datei `wetter_mannheim_2025.csv` mit dem Datum als
Zeilenindex ein. Erweitern Sie die Tabelle um die Spalte `Tagesspanne (C)` wie
in Aufgabe 4.5 und um eine Spalte `Regentag`, die für jeden Tag angibt, ob
Niederschlag gefallen ist (`True`) oder nicht (`False`). Wie viele Regentage
gab es 2025? Welche Accuracy erreicht ein Modell, das immer "kein Regentag"
prognostiziert?

Zur Kontrolle: An 233 Tagen fiel kein Niederschlag, siehe Aufgabe 5.4.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree

wetter_2025 = pd.read_csv('wetter_mannheim_2025.csv', index_col=0)
wetter_2025['Tagesspanne (C)'] = wetter_2025['Hoechsttemperatur (C)'] - wetter_2025['Tiefsttemperatur (C)']
wetter_2025['Regentag'] = wetter_2025['Niederschlag (mm)'] > 0
print(wetter_2025['Regentag'].value_counts())
```
Ausgabe:
```
Regentag
False    233
True     132
Name: count, dtype: int64
```
Ein Vergleich wie `wetter_2025['Niederschlag (mm)'] > 0` liefert eine Series
mit den Werten `True` und `False`, wie wir sie in Kapitel 5 zum Filtern
verwendet haben. Diese Series speichern wir als neue Spalte. 2025 gab es 132
Regentage. Ein Modell, das immer "kein Regentag" prognostiziert, liegt an 233
der 365 Tage richtig und erreicht eine Accuracy von $233/365 \approx 0.638$.
Diesen Wert muss ein Entscheidungsbaum deutlich übertreffen.
````

```{admonition} Aufgabe 6.5 Fortsetzung (Teil 2)
:class: tip
**Teil 2:** Verwenden Sie als Merkmale die Sonnenscheindauer, die Tagesspanne
und die Mitteltemperatur. Die Bewölkung wäre ebenfalls naheliegend, sie hat
aber fehlende Werte. Trainieren Sie einen Entscheidungsbaum mit der maximalen
Tiefe 2 und lassen Sie sich den Baum anzeigen.

1. Welche Frage stellt der Baum zuerst?
2. Beschreiben Sie in Worten, an welchen Tagen der Baum einen Regentag
   prognostiziert. Welche Rolle spielt die Temperatur? Haben Sie eine
   Erklärung?
3. Welche Prognose gibt der Baum für die folgenden drei Tage ab?
   * Tag A: 11 h Sonne, Tagesspanne 14 °C, Mitteltemperatur 20 °C
   * Tag B: 0.5 h Sonne, Tagesspanne 3 °C, Mitteltemperatur 8 °C
   * Tag C: 0.2 h Sonne, Tagesspanne 2 °C, Mitteltemperatur 1 °C

Zur Kontrolle: Der Baum erreicht eine Accuracy von 0.784.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
merkmale = ['Sonnenscheindauer (h)', 'Tagesspanne (C)', 'Mitteltemperatur (C)']
X_2025 = wetter_2025[merkmale]
y_2025 = wetter_2025['Regentag']

modell = DecisionTreeClassifier(max_depth=2, random_state=0)
modell.fit(X_2025, y_2025)
print(f'Tiefe 2: Accuracy {modell.score(X_2025, y_2025):.3f}')

neue_tage = pd.DataFrame({
    'Sonnenscheindauer (h)': [11.0, 0.5, 0.2],
    'Tagesspanne (C)': [14.0, 3.0, 2.0],
    'Mitteltemperatur (C)': [20.0, 8.0, 1.0]
    },
    index=['Tag A', 'Tag B', 'Tag C'])
print(modell.predict(neue_tage))

plot_tree(modell, feature_names=merkmale,
          class_names=['kein Regentag', 'Regentag']);
```
Ausgabe:
```
Tiefe 2: Accuracy 0.784
[False  True False]
```
1. Der Baum fragt zuerst `Sonnenscheindauer (h) <= 5.55`.
2. An Tagen mit mehr als 5.55 h Sonne prognostiziert der Baum immer "kein
   Regentag". Die zweite Frage nach der Sonnenscheindauer in diesem Zweig
   ändert die Prognose nicht, sie macht die Blätter nur reiner, wie in
   Aufgabe 6.4 Teil 3. Einen Regentag prognostiziert der Baum nur für trübe
   Tage mit höchstens 5.55 h Sonne und einer Mitteltemperatur über
   3.05 °C. Von diesen 167 Tagen waren 110 Regentage. Trübe Tage mit
   höchstens 3.05 °C sind dagegen meist trocken, nur an 5 von 31 solchen
   Tagen hat es geregnet. Vermutlich handelt es sich um kalte Wintertage mit
   Hochnebel, an denen die Sonne zwar nicht durchkommt, aber kein Niederschlag
   fällt.
3. Tag A bekommt die Prognose "kein Regentag", weil die Sonne lange scheint.
   Tag B ist trüb und mild, der Baum prognostiziert einen Regentag. Tag C ist
   trüb und kalt, der Baum prognostiziert keinen Regentag.
````

```{admonition} Aufgabe 6.5 Fortsetzung (Teil 3)
:class: tip
**Teil 3:** Trainieren Sie mit denselben Merkmalen Bäume mit den maximalen
Tiefen 1, 2, 4 und 6 und einen Baum ohne Begrenzung. Lassen Sie sich für jeden
Baum die Accuracy auf den Trainingsdaten und die Tiefe ausgeben. Welchen Baum
würden Sie nach diesen Zahlen wählen?

Zur Kontrolle: Der Baum ohne Begrenzung hat die Tiefe 12.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
for tiefe in [1, 2, 4, 6, None]:
    modell = DecisionTreeClassifier(max_depth=tiefe, random_state=0)
    modell.fit(X_2025, y_2025)
    accuracy_2025 = modell.score(X_2025, y_2025)
    print(f'max_depth={tiefe}: Accuracy 2025 {accuracy_2025:.3f}, Tiefe {modell.get_depth()}')
```
Ausgabe:
```
max_depth=1: Accuracy 2025 0.726, Tiefe 1
max_depth=2: Accuracy 2025 0.784, Tiefe 2
max_depth=4: Accuracy 2025 0.841, Tiefe 4
max_depth=6: Accuracy 2025 0.910, Tiefe 6
max_depth=None: Accuracy 2025 1.000, Tiefe 12
```
Die Accuracy steigt mit jeder zusätzlichen Ebene. Der Baum ohne Begrenzung
klassifiziert alle 365 Tage richtig. Nach diesen Zahlen allein wäre er die
beste Wahl. Allerdings braucht er dafür 12 Ebenen und 73 Blätter, im Mittel
also ein Blatt für jeweils 5 Tage. Ob er wirklich etwas über Regentage
gelernt hat oder die Tage des Jahres 2025 nur auswendig kennt, zeigt Teil 4.
````

```{admonition} Aufgabe 6.5 Fortsetzung (Teil 4)
:class: tip
**Teil 4:** Lesen Sie die Datei `wetter_mannheim_2024.csv` ein und ergänzen Sie
dieselben Spalten wie in Teil 1. Die Bäume aus Teil 3 haben diese Tage beim
Training nie gesehen. Trainieren Sie die Bäume aus Teil 3 erneut mit den Daten
von 2025 und berechnen Sie jetzt für jeden Baum zusätzlich die Accuracy auf den
Daten von 2024. Welcher Baum schneidet 2024 am besten ab? Vergleichen Sie auch
mit der
Accuracy eines Modells, das für 2024 immer "kein Regentag" prognostiziert.

Zur Kontrolle: 2024 gab es 168 Regentage. Das Jahr hat als Schaltjahr 366
Tage.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 4
:class: tip
:class: dropdown
```python
wetter_2024 = pd.read_csv('wetter_mannheim_2024.csv', index_col=0)
wetter_2024['Tagesspanne (C)'] = wetter_2024['Hoechsttemperatur (C)'] - wetter_2024['Tiefsttemperatur (C)']
wetter_2024['Regentag'] = wetter_2024['Niederschlag (mm)'] > 0
print(wetter_2024['Regentag'].value_counts())

X_2024 = wetter_2024[merkmale]
y_2024 = wetter_2024['Regentag']

for tiefe in [1, 2, 4, 6, None]:
    modell = DecisionTreeClassifier(max_depth=tiefe, random_state=0)
    modell.fit(X_2025, y_2025)
    accuracy_2025 = modell.score(X_2025, y_2025)
    accuracy_2024 = modell.score(X_2024, y_2024)
    print(f'max_depth={tiefe}: Accuracy 2025 {accuracy_2025:.3f}, Accuracy 2024 {accuracy_2024:.3f}')
```
Ausgabe:
```
Regentag
False    198
True     168
Name: count, dtype: int64
max_depth=1: Accuracy 2025 0.726, Accuracy 2024 0.672
max_depth=2: Accuracy 2025 0.784, Accuracy 2024 0.716
max_depth=4: Accuracy 2025 0.841, Accuracy 2024 0.721
max_depth=6: Accuracy 2025 0.910, Accuracy 2024 0.661
max_depth=None: Accuracy 2025 1.000, Accuracy 2024 0.645
```
2024 war deutlich nasser als 2025. Ein Modell, das immer "kein Regentag"
prognostiziert, erreicht nur $198/366 \approx 0.541$. Alle Bäume liegen
darüber, sie haben also etwas Echtes über Regentage gelernt. Auf den Daten von
2024 schneiden sie aber durchweg schlechter ab als auf den Trainingsdaten von
2025.

Am besten ist 2024 der Baum mit der Tiefe 4 (0.721), dicht gefolgt vom Baum
mit der Tiefe 2 (0.716). Der Baum ohne Begrenzung fällt von 1.000 auf 0.645
zurück. Er ist 2024 sogar schlechter als der Baum mit nur einer Frage. Das ist
Overfitting: Je tiefer der Baum, desto besser passt er zu den Trainingsdaten.
Ab einer gewissen Tiefe lernt er aber die Zufälligkeiten des Jahres 2025 mit
und wird für neue Tage schlechter.

Mit einem anderen `random_state` oder einer anderen Reihenfolge der Merkmale
liegt die Accuracy des Baums ohne Begrenzung für 2024 etwa zwischen 0.63 und
0.67. Bei gleich guten Splits wählt der Baum dann andere Fragen, wie beim
Autohaus in Kapitel 6.3. An der Aussage ändert das nichts: Der Baum ohne
Begrenzung bleibt 2024 schlechter als der Baum mit nur einer Frage.
````

```{admonition} Aufgabe 6.5, Abschlussfrage
:class: tip
In Aufgabe 6.4 Teil 1 hat eine Accuracy von 1.0 auf den Trainingsdaten eine
echte Regel widergespiegelt, hier nicht. Erklären Sie den Unterschied. Welche
maximale Tiefe würden Sie für die Erkennung von Regentagen wählen? Ist das
Jahr 2024 ein fairer Test für einen Baum, der mit dem Jahr 2025 trainiert
wurde?
```

````{admonition} Lösung Abschlussfrage
:class: tip
:class: dropdown
Die Maschinendaten aus Aufgabe 6.4 sind nach festen Regeln erzeugt. Gleiche
Leistung bedeutet immer dasselbe Ergebnis, und ein Baum, der die Regel findet,
liegt auch bei neuen Prozessen richtig. Beim Wetter gibt es keine solche
Regel. Zwei Tage mit gleicher Sonnenscheindauer und Temperatur können
verschieden ausgehen, weil viele Einflüsse fehlen, zum Beispiel die
Bewölkung, der Luftdruck oder die Uhrzeit des Regens. Ein unbegrenzter Baum
lernt diese Zufälligkeiten mit. Seine Accuracy von 1.0 sagt dann nur, dass er
die Trainingsdaten auswendig kennt.

Sinnvoll ist eine Tiefe von 2 bis 4. Der Baum mit der Tiefe 4 ist 2024 am
besten. Der Baum mit der Tiefe 2 ist kaum schlechter, lässt sich aber auf
einen Blick verstehen.

Das Jahr 2024 ist ein fairer Test, weil der Baum diese Tage nie gesehen hat.
Allerdings ist jedes Jahr anders, 2024 hatte zum Beispiel 36 Regentage mehr
als 2025. Ein einzelnes Testjahr gibt also nur einen ersten Eindruck. Wie wir
einen Datensatz gezielt in Trainings- und Testdaten aufteilen, lernen wir in
Kapitel 8.3. Wie wir die Hyperparameter systematisch wählen, sehen wir in
Kapitel 10.2 bei der Gittersuche.
````
