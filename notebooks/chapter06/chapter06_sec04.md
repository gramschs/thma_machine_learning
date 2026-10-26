---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
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

## Aufgabe 6.1 (✩) Ein Baum mit einer einzigen Frage

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

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.2 (✩) Hyperparameter vorhersagen

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

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.3 (✩✩) Basketball oder Volleyball?

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

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.4 (✩✩✩) Mini-Projekt: Ausfallregeln wiederentdecken

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

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.4 Fortsetzung (Teil 2)

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

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.4 Fortsetzung (Teil 3)

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

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.4 Fortsetzung (Abschlussfrage)

**Abschlussfrage:** In allen drei Teilen erreichen die Bäume auf den
Trainingsdaten eine Accuracy von 1.0 oder knapp darunter. In Kapitel 6.3 haben
wir gelernt, dass eine so hohe Accuracy auf Overfitting hindeuten kann. Ist das
hier der Fall? Vergleichen Sie dazu die Tiefe der Bäume aus Teil 1 und Teil 2.

## Aufgabe 6.5 (✩✩✩) Mini-Projekt: Regentage erkennen

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

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.5 Fortsetzung (Teil 2)

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

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.5 Fortsetzung (Teil 3)

**Teil 3:** Trainieren Sie mit denselben Merkmalen Bäume mit den maximalen
Tiefen 1, 2, 4 und 6 und einen Baum ohne Begrenzung. Lassen Sie sich für jeden
Baum die Accuracy auf den Trainingsdaten und die Tiefe ausgeben. Welchen Baum
würden Sie nach diesen Zahlen wählen?

Zur Kontrolle: Der Baum ohne Begrenzung hat die Tiefe 12.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.5 Fortsetzung (Teil 4)

**Teil 4:** Lesen Sie die Datei `wetter_mannheim_2024.csv` ein und ergänzen Sie
dieselben Spalten wie in Teil 1. Die Bäume aus Teil 3 haben diese Tage beim
Training nie gesehen. Trainieren Sie die Bäume aus Teil 3 erneut mit den Daten
von 2025 und berechnen Sie jetzt für jeden Baum zusätzlich die Accuracy auf den
Daten von 2024. Welcher Baum schneidet 2024 am besten ab? Vergleichen Sie auch
mit der
Accuracy eines Modells, das für 2024 immer "kein Regentag" prognostiziert.

Zur Kontrolle: 2024 gab es 168 Regentage. Das Jahr hat als Schaltjahr 366
Tage.

```{code-cell} python
# Code-Zelle
```

## Aufgabe 6.5 Fortsetzung (Abschlussfrage)

**Abschlussfrage:** In Aufgabe 6.4 Teil 1 hat eine Accuracy von 1.0 auf den
Trainingsdaten eine echte Regel widergespiegelt, hier nicht. Erklären Sie den
Unterschied. Welche maximale Tiefe würden Sie für die Erkennung von Regentagen
wählen? Ist das Jahr 2024 ein fairer Test für einen Baum, der mit dem Jahr 2025
trainiert wurde?
