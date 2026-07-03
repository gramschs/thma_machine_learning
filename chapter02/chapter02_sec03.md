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

# 2.3 Dictionaries, Funktionen und Methoden

Sobald die Funktionalitäten komplexer werden, ist es wichtig zu verstehen, wie
wir mit verschiedenen Datenstrukturen arbeiten und wie Code in Python
organisiert ist. In diesem Kapitel lernen wir zunächst mit Dictionaries eine
weitere wichtige Datenstruktur kennen. Anschließend vertiefen wir unser
Verständnis von Funktionen und lernen das Konzept der objektorientierten
Programmierung kennen. Funktionen, die direkt an einen Datentyp gekoppelt sind,
werden **Methoden** genannt.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie kennen den Datentyp **Dictionary** und können Schlüssel-Wert-Paare
erstellen und nutzen.
* Sie verstehen, wie Funktionen aufgerufen werden und können mit Argumenten und
Rückgabewerten arbeiten.
* Sie wissen, was **Methoden** sind und kennen das **Konzept der
objektorientierten Programmierung**.
```

## Dictionaries

Bisher haben wir Listen kennengelernt, um mehrere Daten zu sammeln. Listen haben
jedoch einen Nachteil: Wir müssen uns merken, an welcher Position welche
Information steht. Bei einer Liste `[7900, 200000, 190]` ist nicht sofort klar,
was die einzelnen Zahlen bedeuten. Für solche Fälle gibt es eine Datenstruktur,
die besser geeignet ist, das sogenannte **Dictionary**.

Dictionaries (deutsch: Wörterbücher) speichern Daten in Form von
Schlüssel-Wert-Paaren. Wir können uns ein Dictionary wie ein Wörterbuch
vorstellen: Wir schlagen einen Begriff nach (das ist der Schlüssel) und erhalten
die zugehörige Information (das ist der Wert). Im Gegensatz zu Listen, die über
einen numerischen Index angesprochen werden, erfolgt der Zugriff bei
Dictionaries über aussagekräftige Schlüssel.

Ein Dictionary wird mit geschweiften Klammern `{}` erstellt. Die
Schlüssel-Wert-Paare werden durch Doppelpunkte `:` getrennt, mehrere Paare durch
Kommas `,`. Schauen wir uns dazu ein Beispiel an:

```{code-cell}
person = {
    "name": "Alice",
    "alter": 25,
    "stadt": "Berlin"
}
print(person)
```

Der Zugriff auf einzelne Werte erfolgt über die Angabe des Schlüssels in eckigen
Klammern:

```{code-cell}
print(f'Name: {person["name"]}')
print(f'Alter: {person["alter"]}')
print(f'Stadt: {person["stadt"]}')
```

Wir können auch Werte ändern oder neue Schlüssel-Wert-Paare hinzufügen:

```{code-cell}
# Wert ändern
person["alter"] = 26
print(f'Neues Alter: {person["alter"]}')

# Neues Schlüssel-Wert-Paar hinzufügen
person["beruf"] = "Datenwissenschaftlerin"
print(person)
```

Der Vorteil von Dictionaries gegenüber Listen wird besonders deutlich, wenn wir
die beiden Datenstrukturen vergleichen. In einer Liste müssten wir uns merken,
dass der Name an Position 0 steht, das Alter an Position 1 und so weiter. Bei
einem Dictionary können wir direkt mit aussagekräftigen Begriffen arbeiten.

```{code-cell}
# Als Liste (unübersichtlich)
person_liste = ["Alice", 25, "Berlin"]
print(f'Name (Liste): {person_liste[0]}')  # Was bedeutet Index 0?

# Als Dictionary (selbsterklärend)
person_dict = {"name": "Alice", "alter": 25, "stadt": "Berlin"}
print(f'Name (Dictionary): {person_dict["name"]}')
```

```{admonition} Mini-Übung
:class: tip
Erstellen Sie ein Dictionary für einen Datenpunkt mit folgenden Informationen:
- temperatur: 23.5
- luftfeuchtigkeit: 65
- standort: "Sensor_01"

Geben Sie dann die Temperatur und den Standort mit passenden Beschriftungen aus.
```

```{code-cell} ipython3
# Hier Ihr Code:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Dictionary für Datenpunkt erstellen
messwert = {
    "temperatur": 23.5,
    "luftfeuchtigkeit": 65,
    "standort": "Sensor_01"
}

# Zugriff auf spezifische Werte
print(f'Temperatur: {messwert["temperatur"]} °C')
print(f'Standort: {messwert["standort"]}')
```
````

Dictionaries werden uns in späteren Kapiteln häufiger begegnen. Insbesondere bei
der Visualisierung mit Plotly werden wir Dictionaries verwenden, um
Konfigurationen für Diagramme zu definieren.

## Funktionen

Eine Funktion ist eine Zusammenfassung von Code, der eine bestimmte Teilaufgabe
löst. Wir haben bereits verschiedene Funktionen kennengelernt und verwendet. Die
Funktion `print()` gibt Text oder Werte auf dem Bildschirm aus. Die Funktion
`len()` ermittelt die Länge einer Liste oder eines Strings. Die Funktion
`type()` gibt uns den Datentyp einer Variable zurück.

Eine Funktion wird aufgerufen, indem wir den Namen der Funktion hinschreiben und
dann in runden Klammern ihre Argumente übergeben. Welche Argumente eine Funktion
erwartet, hängt von der jeweiligen Funktion ab. Betrachten wir dazu einige
Beispiele:

```{code-cell}
# len() mit verschiedenen Argumenten
print(len('Hallo'))  # String als Argument
print(len([1, 2, 3, 4, 8, 2]))  # Liste als Argument

# type() ermittelt den Datentyp
x = 42
print(type(x))
y = 3.14
print(type(y))
```

Die meisten Funktionen geben ein Ergebnis zurück. Dieses können wir einer
Variable zuweisen, um weiter damit zu arbeiten:

```{code-cell}
wort = 'Maschinelles Lernen'
anzahl_zeichen = len(wort)
print(f'Der Text "{wort}" hat {anzahl_zeichen} Zeichen.')
```

Beim maschinellen Lernen werden wir vor allem Funktionen aus Bibliotheken wie
NumPy, Pandas und scikit-learn verwenden. Diese Funktionen sind bereits fertig
implementiert und wir müssen nur wissen, wie wir sie aufrufen. Das Schreiben
eigener Funktionen ist seltener nötig, weshalb wir uns darauf konzentrieren, wie
wir bestehende Funktionen effektiv nutzen können.

Falls Sie sich dafür interessieren, Funktionen selbst zu definieren, finden Sie
in den drei folgenden Videos weitere Details zur Implementierung von Funktionen.

```{dropdown} Video zu "Funktionen selbst definieren" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/LQCfN5HS9xI" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

```{dropdown} Video zu "Funktionen mit Parametern" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/af9ORp1Pty0" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video zu "Funktionen mit Rückgabewert" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/ehSP-sYoKCY" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

## Objektorientierte Programmierung

Nachdem wir gesehen haben, wie Funktionen aufgerufen werden, schauen wir uns nun
an, wie Python Funktionen und Daten in Objekten organisiert.

Die Idee der objektorientierten Programmierung ist, Daten und die dazugehörigen
Funktionen zusammenzufassen. Bisher haben wir Funktionen und Daten getrennt. Die
Daten werden in Variablen gespeichert und Funktionen verarbeiten diese Daten
nach dem EVA-Prinzip (Eingabe, Verarbeitung, Ausgabe). In der objektorientierten
Programmierung werden Daten und Funktionen zu einem **Objekt** kombiniert. Die
Eigenschaften eines Objekts werden **Attribute** genannt. Funktionen, die zu
einem Objekt gehören, nennen wir **Methoden**.

Tatsächlich haben wir bereits Methoden verwendet, ohne es explizit zu wissen.
Listen sind Objekte und wenn wir `liste.append(4)` schreiben, rufen wir die
Methode `.append()` des Listen-Objekts auf. Auch bei Dictionaries stehen
Methoden wie `.keys()` oder `.values()` zur Verfügung, auch wenn wir diese
bisher nicht verwendet haben.

```{code-cell}
meine_liste = [17, 3.5]
meine_liste.append(4)
print(meine_liste)
```

Sehen wir uns noch ein weiteres Beispiel an. Ein String ist in Python ein
Objekt. Strings haben verschiedene Methoden, die uns die Arbeit erleichtern.

```{code-cell}
text = "Hallo Welt"

# Methode upper(): wandelt alle Buchstaben in Großbuchstaben um
text_gross = text.upper()
print(text_gross)

# Methode lower(): wandelt alle Buchstaben in Kleinbuchstaben um
text_klein = text.lower()
print(text_klein)

# Methode replace(): ersetzt Teile des Strings
text_neu = text.replace("Welt", "Python")
print(text_neu)
```

Das nächste Beispiel zeigt den Einsatz von Methoden bei Dictionaries:

```{code-cell}
# Dictionary-Methoden
person = {"name": "Alice", "alter": 25}
print(person.keys())    # dict_keys(['name', 'alter'])
print(person.values())  # dict_values(['Alice', 25])
```

Methoden werden also aufgerufen, indem wir die Variable (das Objekt)
hinschreiben, dann einen Punkt setzen und dann den Methodennamen mit runden
Klammern anfügen. Falls die Methode Argumente benötigt, werden diese in die
runden Klammern geschrieben.

In den kommenden Kapiteln werden wir viele Bibliotheken für maschinelles Lernen
verwenden. Diese Bibliotheken arbeiten mit Objekten und Methoden. Beispielsweise
werden wir später mit scikit-learn arbeiten. Dort erstellen wir ein
Modell-Objekt und rufen dann Methoden wie `fit()` auf, um das Modell zu
trainieren, oder `predict()`, um Vorhersagen zu machen. Das Prinzip ist immer
das gleiche wie bei `liste.append()` oder `text.upper()`.

Python ermöglicht es uns auch, eigene Objekte zu definieren. Dazu verwenden wir
das Schlüsselwort `class`. In diesem Einführungskurs werden wir jedoch keine
eigenen Klassen erstellen, sondern nur die Klassen und Methoden verwenden, die
uns die verschiedenen Bibliotheken zur Verfügung stellen. Die folgenden Videos
geben einen vertieften Einblick in die Objektorientierung mit Python für alle,
die mehr darüber erfahren möchten.

```{dropdown} Video zu "Konzept der Objektorientierung" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/46yolPy-2VQ" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video zu "Klassen und Objekte" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/XxCZrT7Z3G4" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video zu "Der self Parameter" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/CLoK-_qNTnU" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video zu "Methoden in Klassen" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/58IjjwHs_4A" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir drei wichtige Konzepte kennengelernt. Zunächst haben
wir mit Dictionaries eine Datenstruktur gesehen, die uns erlaubt, Daten über
aussagekräftige Schlüssel statt über numerische Indizes anzusprechen.
Anschließend haben wir vertieft, wie wir Funktionen aufrufen und mit ihren
Rückgabewerten arbeiten. Zum Schluss haben wir einen ersten Einblick in die
objektorientierte Programmierung erhalten und verstehen nun, was Methoden sind
und wie sie sich von normalen Funktionen unterscheiden.

Oft ist es aber praktischer, Funktionen und Klassen zu nutzen, die bereits
implementiert sind, anstatt das Rad neu zu erfinden. Vor allem bei der
Datenexploration und den maschinellen Lernalgorithmen werden wir die
vorgefertigten Funktionsbausteine nutzen, wie wir in den nächsten Kapiteln sehen
werden.
