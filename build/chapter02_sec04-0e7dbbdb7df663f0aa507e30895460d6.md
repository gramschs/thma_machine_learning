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

# Übungen

```{admonition} Übung 2.1
:class: tip 
Welcher Datentyp liegt vor? Kopieren Sie diesen Text in eine Markdown-Zelle und
schreiben Sie Ihre Antwort hinter den Pfeil.

* 3 -->
* -3 -->
* 'drei'-->
* 3.3 -->
* 3,3 -->
* 3**3 -->
* 3**(1/3) -->

Verwenden Sie anschließend `type()` in einer Code-Zelle, um Ihre Antwort zu
überprüfen.
```

```{admonition} Lösung
:class: tip
:class: dropdown, dropdown
* 3 –> int, also Integer
* -3 –> int, also Integer
* ‘drei’–> str, also String
* 3.3 –> float, also Float
* 3,3 –> Fehlermeldung, das Dezimaltrennzeichen ist der Punkt, nicht das Komma
* 3**3 –> int, also Integer
* 3**(1/3) –> float, also Float
```

```{admonition} Übung 2.2
:class: tip 
Schreiben Sie ein Programm, das die Zahlen von 5 bis 15 mit ihrem Quadrat
ausgibt, also "Das Quadrat von 5 ist 25." usw.
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
for zahl in range(5, 16):
    print(f'Das Quadrat von {zahl} ist {zahl**2}.')
```
````

````{admonition} Übung 2.3
:class: tip 
Schreiben Sie eine For-Schleife, die die Brüche 1/7, 2/7, 3/7, bis 7/7 als
Fließkommazahl gerundet auf 2 Nachkommastellen ausgibt. Beispielausgabe:
```{code}
1/7 = 0.14.
2/7 = 0.29.
3/7 = 0.43.
4/7 = 0.57.
5/7 = 0.71.
6/7 = 0.86.
7/7 = 1.00.
```
````

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
for zahl in range(1, 8):
    print(f'{zahl}/7 = {zahl/7:.2f}.')
```
````

````{admonition} Übung 2.4
:class: tip 
Schreiben Sie ein Programm, das eine Liste von Namen durchläuft und jede Person
begrüßt. Wenn beispielsweise die Namen Alice, Bob und Charlie in der Liste
stehen, lauten die Begrüßungen:

```{code}
Hallo, Alice!
Hallo, Bob!
Hallo, Charlie!
```
````

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
namensliste = ['Alice', 'Bob', 'Charlie']
for name in namensliste:
    print(f'Hallo, {name}!')
```
````

```{admonition} Übung 2.5
:class: tip
Erstellen Sie ein Dictionary für einen Studierenden mit folgenden Informationen:

- vorname: "Max"
- nachname: "Mustermann"
- matrikelnummer: 123456
- studiengang: "Maschinenbau"

Geben Sie dann folgende Information aus: "Max Mustermann (123456) studiert Maschinenbau."
````

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
studierender = {
    "vorname": "Max",
    "nachname": "Mustermann",
    "matrikelnummer": 123456,
    "studiengang": "Maschinenbau"
}

print(f'{studierender["vorname"]} {studierender["nachname"]} ({studierender["matrikelnummer"]}) studiert {studierender["studiengang"]}.')
```
````

```{admonition} Übung 2.6
:class: tip
Gegeben ist die Liste: `zahlen = [5, 12, 3, 8, 1]`

1. Fügen Sie die Zahl 7 am Ende der Liste hinzu.
2. Erstellen Sie einen String `text = "Python Programmierung"` und wandeln Sie ihn in Großbuchstaben um.
3. Geben Sie beide Ergebnisse aus.
```

````{admonition} Lösung
:class: tip
:class: dropdown, dropdown
```python
# Liste bearbeiten
zahlen = [5, 12, 3, 8, 1]
zahlen.append(7)
print(f'Liste: {zahlen}')

# String bearbeiten
text = "Python Programmierung"
text_gross = text.upper()
print(f'Text in Großbuchstaben: {text_gross}')
```
````
