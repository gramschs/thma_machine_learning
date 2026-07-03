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

# 2.1 Datentypen, Variablen und print()

Beim maschinellen Lernen geht es um Daten und Algorithmen. Dabei können die
Daten alles Mögliche umfassen, beispielsweise Zahlen oder Texte. Daher
beschäftigen wir uns zuerst mit Datentypen. Dann geht es um Variablen und deren
Ausgabe auf dem Bildschirm.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie kennen die einfachen Datentypen:
    * **Integer**
    * **Float**
    * **String**
* Sie wissen, was eine **Variable** ist und kennen den **Zuweisungsoperator**.
* Sie können die **print()**-Funktion zur Ausgabe auf dem Bildschirm anwenden.
```

## Einfache Datentypen

Beim maschinellen Lernen geht es um die Sammlung, Erkundung und Analyse von
Daten, um Antworten auf vorgegebene Fragen zu finden.  Der Computer kann
Informationen aber nur als 0 und 1 verarbeiten. Auf dem Speichermedium oder im
Speicher selbst werden Daten daher als eine Folge von 0 und 1 gespeichert. Damit
es für uns Programmierinnen und Programmierer einfacher wird, Daten zu speichern
und zu verarbeiten, wurden Datentypen eingeführt.  

**Datentypen** fassen gleichartige Objekte zusammen und stellen den
Programmiererinnen und Programmierern passende Operationen zur Verfügung. Mit
Operationen sind die Aktionen gemeint, die mit diesen Datenobjekten durchgeführt
werden dürfen. Zahlen dürfen beispielsweise addiert werden, Buchstaben aber
nicht. Es hängt von der Programmiersprache ab, welche Datentypen zur Verfügung
stehen, wie diese im Hintergrund gespeichert werden und welche Operationen
möglich sind.

In diesem Kapitel beschäftigen wir uns mit den einfachen Datentypen

* Integer,
* Float und
* String.

### Integer und Float

In der Programmierung unterscheidet man grundsätzlich zwischen zwei Zahlenarten,
den **ganzen Zahlen** und den Fließkommazahlen. In der Informatik wird jedoch
der englische Begriff dafür verwendet: **Integer**.

Mit Integern können wir ganz normal rechnen, also arithmetische Operationen
ausführen:

```{code-cell}
2+3
```

```{code-cell}
2*3
```

```{code-cell}
6-7
```

```{code-cell}
3*(4+7)
```

```{code-cell}
25/5
```

```{code-cell}
4**2
```

Mit einer Operation verlassen wir aber bereits den Bereich der ganzen Zahlen,
den Bereich der Integer. `25/5` ist wieder eine ganze Zahl, nicht jedoch
`25/3`. Damit sind wir bei den Fließkommazahlen. Auch hier wird üblicherweise
der englische Begriff **Float** für **Fließkommazahl** verwendet.

```{code-cell}
2.3 + 4.5
```

```{code-cell}
5.6 - 2.1
```

```{code-cell}
2.1 * 3.5
```

```{code-cell}
3.4 / 1.7
```

```{code-cell}
3.4 ** 2
```

```{code-cell}
3.5 * (2.6 - 3.8 / 1.9)
```

```{admonition} Hinweis
:class: warning
Verwenden Sie stets einen Punkt als Dezimaltrennzeichen, nicht ein
Komma!
```

Das folgende Video gibt eine Einführung in das Thema »Zahlen mit Python«.

```{dropdown} Video zu "Zahlen in Python" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/VtiDkRDPA_c" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

### String

Daten sind aber sehr oft keine Zahlen. Beispielsweise könnte man sich
vorstellen, eine Einkaufsliste zu erstellen und diese im Computer oder in einer
Notiz-App auf dem Handy zu speichern. Eine solche **Zeichenkette** heißt in der
Informatik **String**. Mit Zeichen meint man dabei Zahlen, Buchstaben oder
andere Zeichen wie beispielsweise !"§$%&/()=?.

Strings werden in Python durch einfache Hochkomma oder Anführungszeichen
definiert.

```{code-cell}
'Dies ist ein String!'
```

Mit Strings kann man ebenfalls "rechnen", nur ist das Ergebnis vielleicht anders
als erwartet.

```{code-cell}
2 * 'Dies ist ein String!'
```

```{code-cell}
'String 1 ' + 'String 2' 
```

Das folgende Video gibt eine Einführung zum Thema »Strings in Python«.

```{dropdown} Video zu "Strings in Python" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/sTEf4_mrLvw" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

## Variablen und Zuweisung

**Variablen** sind beschriftete Schubladen. Oder anders formuliert sind
Variablen Objekte, denen man einen Namen gibt. Technisch gesehen sind diese
Schubladen ein kleiner Bereich im Arbeitsspeicher des Computers. Der Inhalt der
Schubladen kann sehr unterschiedlich sein. Beispielsweise können in den
Schubladen die Telefonnummer des ADAC-Pannendienstes, die 10. Nachkommastelle
von $\pi$ oder die aktuelle Position des Mauszeigers enthalten sein.

### Zuweisungen sind keine Gleichungen

Wir verwenden Variablen, um bestimmte Werte oder ein bestimmtes Objekt zu
speichern. Eine Variable wird durch eine **Zuweisung** erzeugt. Damit meinen
wir, dass eine Schublade angelegt wird und die Schublade dann erstmalig gefüllt
wird. Das erstmalige Füllen der Schublade nennt man in der Informatik auch
Initialisieren. Für die Zuweisung wird in Python das `=`-Zeichen verwendet.

```{code-cell}
x = 0.5
```

Sobald die Variable `x` in diesem Beispiel durch eine Zuweisung von 0.5 erstellt
wurde, können wir sie verwenden:

```{code-cell}
x * 3
```

```{code-cell}
x + 17
```

Wichtig ist, dass das `=` in der Informatik eine andere Bedeutung hat als in der
Mathematik. `=` meint nicht das Gleichheitszeichen, sondern den sogenannten
**Zuweisungsoperator**. Das ist in der Programmierung ein Kommando, das eine
Schublade befüllt oder technischer ausgedrückt, ein Objekt einer Variable
zuweist.

Variablen müssen initalisiert (erstmalig mit einem Wert versehen) werden, bevor
sie verwendet werden können, sonst tritt ein Fehler auf.

```{admonition} Mini-Übung
:class: tip
Fügen Sie eine Code-Zelle ein und schreiben Sie in die Code-Zelle einfach nur `n`. Lassen Sie die Code-Zelle ausführen. Was passiert?
```

```{admonition} Lösung
:class: tip
:class: dropdown
Es erscheint eine Fehlermeldung, da eine Variable einen Wert haben muss, bevor
sie das erste Mal benutzt wird.
```

Sehr häufig findet man Code wie

```{code-cell}
x = x + 1
```

Würden wir dies als Gleichung lesen, wie wir es aus der Mathematik gewohnt sind,
x = x + 1, könnten wir x auf beiden Seiten subtrahieren und erhalten 0 = 1. Wir
wissen, dass dies nicht wahr ist, also stimmt hier etwas nicht.

In Python sind Gleichungen keine mathematischen Gleichungen, sondern
Zuweisungen. "=" ist kein Gleichheitszeichen im mathematischen Sinne, sondern
eine Zuweisung. Die Zuweisung muss immer in der folgenden Weise zweistufig
gelesen werden:

1. Berechne den Wert auf der rechten Seite (also x+1).
2. Weise den Wert auf der rechten Seite dem auf der linken Seite stehenden
   Variablennamen zu (in Python-Sprechweise: binde dem Namen auf der linken
   Seite an das auf der rechten Seite angezeigte Objekt).

```{code-cell}
x = 4     
x = x + 1
x
```

### Richtlinien für Variablennamen

Früher war der Speicherplatz von Computern klein, daher wurden häufig nur kurze
Variablennamen wie beispielsweise `i` oder `N` verwendet. Heutzutage ist es
Standard, nur in Ausnahmefällen (z.B. in Schleifen, dazu kommen wir noch) kurze
Variablennamen zu nehmen. Stattdessen werden Namen benutzt, bei denen man
erraten kann, was die Variable für einen Einsatzzweck hat. Beispielsweise lässt
der Code

```{code-cell}
m = 0.19
n = 80
b = n + m*n
b
```

nur schwer vermuten, was damit bezweckt wird. Dagegen erahnt man bei diesem Code
schon eher, was bezweckt wird:

```{code-cell}
mehrwertsteuersatz = 19/100
nettopreis = 80
bruttopreis = nettopreis + mehrwertsteuersatz * nettopreis
bruttopreis
```

Code-Zellen zeigen arithmetische Operationen direkt nach Ausführen der
Code-Zelle an. Wenn allerdings in der Code-Zelle mehrere Python-Anweisungen
sind, müssen wir in die letzte Zeile nochmal die Variable selbst hinschreiben,
deren Wert angezeigt werden soll. Das ist etwas umständlich und funktioniert
auch nur mit Jupyter Notebooks. Normalerweise gibt es dazu eine Python-Funktion
`print()`, auf die wir später noch zurückkommen.

Verwenden Sie für Variablennamen nur ASCII-Zeichen, also keine Umlaute wie ö, ü
oder ß. Python erlaubt es zwar, Umlaute in Variablennamen zu verwenden, es ist
aber gute Praxis, dies nicht zu tun. Zahlen sind erlaubt, aber nicht am Anfang
des Namens. Es ist sinnvoll, lange Variablen durch einen Unterstrich besser
lesbar zu gestalten (sogenannte Snake-Case-Formatierung). Ich empfehle für
Variablennamen beispielsweise

`dateiname_alt` oder `dateiname_neu`

wenn beispielsweise eine Datei umbenannt wird. Sie sind frei in der Gestaltung
der Variablennamen, verboten sind nur die sogannnten Schlüsselwörter.

Die folgenden beiden Videos fassen die beiden Themen Variablen und Zuweisungen
nochmals zusammen.

```{dropdown} Video zu "Variablen in Python" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/jfOLXKPGXJ0" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video zu "Zuweisungen in Python" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/XKFQ2_et5k8" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

### Datentypen ermitteln mit type()

Werden zwei Integer geteilt, so wird das Ergebnis automatisch in einen Float
umgewandelt. Mit Hilfe der Funktion `type()` können wir den Python-Interpreter
bestimmen lassen, welcher Datentyp in einer Variable gespeichert ist. Mit
Funktion ist hier keine mathematische Funktion gemeint. Eine **Funktion** sind
viele Anweisungen nacheinander, um eine bestimmte Teilaufgabe zu lösen. Damit
klar ist, dass es sich um eine Funktion und nicht um eine Variable handelt,
werden runde Klammern an den Namen der Funktion gehängt.

In diesem Fall soll der Datentyp eines Objektes ermittelt werden. Damit der
Python-Interpreter weiß, von welcher Variable der Datentyp ermittelt werden
soll, schreiben wir die Variable in runde Klammern.

```{code-cell}
x = 25 * 5
type(x)
```

```{code-cell}
x = 25 / 5
type(x)
```

Nicht immer ist es aber möglich, Datentypen zu mischen. Dann meldet Python einen
Fehler.

Das folgende Video fasst die Datentypen Integer, Float und String nochmal zusammen.

```{dropdown} Video zu "Datentypen in Python" von Programmieren lernen
<iframe width="560" height="315" src="https://www.youtube.com/embed/1WqFJ5wsA4o" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

## Ausgaben mit print()

Jetzt lernen Sie eine weitere Python-Funktion kennen. Bei den obigen
Rechenaufgaben wurde automatisch das Ergebnis der Rechnung angezeigt, sobald die
Code-Zelle ausgeführt wurde. Dies ist eine Besonderheit der Jupyter Notebooks,
würde aber in einem normalen Python-Programm nicht funktionieren. Auch möchte
man vielleicht ein Zwischenergebnis anzeigen lassen. Die interaktive Ausgabe der
Jupyter Notebooks zeigt jedoch immer nur den Inhalt der letzten Zeile an.

Für die Anzeige von Rechenergebnissen oder Texten gibt es in Python die
**print()**-Funktion. Die print()-Funktion in Python gibt den Wert am Bildschirm
aus, der ihr als sogenanntes **Argument** in den runden Klammern übergeben wird.
Das kann zum Beispiel eine Zahl oder eine Rechenaufgabe sein, wie in dem
folgenden Beispiel.

```{code-cell}
print(2)
print(3+3)
```

In der ersten Zeile ist das Argument für die print()-Funktion die Zahl 2. Das
Argument wird in runde Klammern hinter den Funktionsnamen `print` geschrieben.
Ein Argument ist sozusagen der Input, der an die print()-Funktion übergeben
wird, damit der Python-Interpreter weiß, welcher Wert auf dem Bildschirm
angezeigt werden soll.

Das zweite Beispiel in der zweiten Zeile funktioniert genauso. Nur wird diesmal
eine komplette Rechnung als Argument an die print()-Funktion übergeben. In dem
Fall rechnet der Python-Interpreter erst den Wert der Rechnung, also `3+3=6` aus
und übergibt dann die `6` an die print()-Funktion. Die print()-Funktion wiederum
zeigt dann die `6` am Bildschirm an.

```{admonition} Mini-Übung
:class: tip
Lassen Sie Python den Term $3:4$ berechnen und geben Sie das Ergebnis mit der print()-Funktion aus. 
```

```{code-cell} ipython3
# Geben Sie nach diesem Kommentar Ihren Code ein:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
print(3/4)
```
````

Python kann mit der print()-Funktion jedoch nicht nur Zahlen ausgeben, sondern
auch Texte, also Strings.

```{code-cell}
print('Hallo')
```

```{admonition} Mini-Übung
:class: tip
Probieren Sie aus was passiert, wenn Sie die einfachen Anführungszeichen `'`
durch doppelte Anführungszeichen `"` ersetzen. Lassen Sie den Text Hallo Welt
ausgeben :-)
```

```{code-cell} ipython3
# Geben Sie nach diesem Kommentar Ihren Code ein:
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
print("Hallo Welt")
```
````

Zum Schluss behandeln wir noch formatierte Strings, die sogenannten f-Strings.
Seit Python 3.6 erleichtert dieser Typ von String die Programmierung. Falls Sie
Python-Code sehen, in dem Prozentzeichen vorkommen (ganz, ganz alt) oder die
`.format()`-Methode benutzt wird, wundern Sie sich nicht. In dieser Vorlesung
verwenden wir jedoch f-Strings.

**f-Strings** sind die Abkürzung für "formatted string literals". Sie
ermöglichen es, den Wert einer Variable oder einen Ausdruck direkt in den String
einzubetten. Dazu werden geschweifte Klammern verwendet, also `{` und `}` und zu
Beginn des Strings wird ein `f` eingefügt, um aus dem String einen f-String zu
machen. Der Python-Interpreter fügt dann zur Laufzeit des Programms den
entsprechenden Wert der Variable in den String ein.

Hier ein Beispiel:

```{code-cell}
name = 'Alice'
alter = 20
print(f'Mein Name ist {name} und ich bin {alter} Jahre alt.')
```

Insbesondere bei Ausgabe von Zahlen sind f-Strings besonders nützlich. Wenn nach
dem Variablennamen ein Doppelpunkt eingefügt wird, kann danach die Anzahl der
gewünschten Stellen vor dem Komma (hier natürlich ein Punkt) und der
Nachkommastellen festgelegt werden. Zusätzlich setzen wir ein `f` in die
geschweiften Klammern, um einen Float anzeigen zu lassen. Im folgenden Beispiel
geben wir $\pi$ auf zwei Nachkommastellen an.

```{code-cell}
pi = 3.141592653589793238462643383279
print(f'Pi = {pi:1.2f}')
```

Es ist schwierig, sich alle Formatierungsoptionen zu merken. Auf der
Internetseite
[https://cheatography.com/brianallan/cheat-sheets/python-f-strings-basics/](https://cheatography.com/brianallan/cheat-sheets/python-f-strings-basics/)
finden Sie eine umfangreiche Übersicht und können sich zudem ein pdf-Dokument
herunterladen.

```{admonition} Mini-Übung
:class: tip
Schreiben Sie ein Programm, mit dem der Flächeninhalt eines Rechtecks berechnet werden soll. Die beiden Seitenlängen werden jeweils in den Variablen `laenge` und `breite` gespeichert (suchen Sie sich eigene Zahlen aus). Ausgegeben werden soll dann: "Der Flächeninhalt eines Rechtecks mit den Seiten XX und XX ist XX.", wobei XX durch die korrekten Zahlen ersetzt werden und der Flächeninhalt auf eine Nachkommastelle gerundet werden soll.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Eingabe
laenge = 5.5
breite = 6.3

# Verarbeitung
flaeche = laenge * breite

# Ausgabe 
print(f'Der Flächeninhalt eines Rechtecks mit den Seiten {laenge} und {breite} ist {flaeche:.1f}.')
```
````

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir gelernt, was ein Datentyp ist, wie eine Variable mit
einem Wert gefüllt wird und mit der print()-Funktion am Bildschirm ausgegeben
wird. Die einfachsten Datentypen Integer, Float und String reichen allerdings
nicht aus, um z.B. die eine Adresse mit Straße (String), Hausnummer (Integer)
und Postleitzahl (Integer) in einer Variablen gemeinsam zu speichern. Dazu
lernen wir im nächsten Abschnitt den Datentyp Liste kennen.
