---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 12.2 Mehrschichtiges Perzeptron

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können das Konzept eines **künstlichen Neurons** erklären.
* Sie wissen, was ein **mehrschichtiges Perzeptron** ist und kennen den
  englischen Begriff **Multilayer Perceptron** (MLP) dafür.
* Sie können den Begriff **Deep Learning** erklären.
```

+++

## Künstliche Neuronen

Im letzten Kapitel haben wir das Perzeptron kennengelernt. Schematisch können
wir es folgendermaßen darstellen:

```{figure} pics/fig_12_02_topology_perceptron.svg
---
name: fig_12_02_topology_perceptron
---
Schematische Darstellung eines Perzeptrons (Quelle: eigene Darstellung; Lizenz:
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
```

Kurz zusammengefasst funktioniert ein Perzeptron ähnlich wie ein biologisches
Neuron. Jedes Eingangssignal wird mit einem Gewicht multipliziert. Anschließend
werden die gewichteten Eingangssignale summiert. Übersteigt die gewichtete Summe
einen Schwellenwert, feuert sozusagen das Neuron. Das Ausgabesignal wird
aktiviert.

Mathematisch gesehen, werden auf die Eingabedaten zwei mathematische Funktionen
angewendet:

1. Übertragungsfunktion (hier die Bildung der gewichteten Summe) und
2. Aktivierungsfunktion (hier die Anwendung der Heaviside-Funktion).

Dieses Prinzip behalten wir bei, erlauben aber eine größere Auswahl an
Übertragungs- und Aktivierungsfunktionen, um das Perzeptron auf das sogenannte
**künstliche Neuron** zu verallgemeinern. Später werden wir die künstlichen
Neuronen in einem Netz zusammensetzen.

```{admonition} Was ist ... ein künstliches Neuron?
:class: note
Ein künstliches Neuron verarbeitet Informationen, indem es

1. Eingaben mit Gewichten multipliziert und zusammenaddiert,
2. eine Aktivierungsfunktion auf die gewichtete Summe anwendet und
3. das Ergebnis ausgibt.
```

Bei neuronalen Netzen werden vor allem die
[ReLU-Funktion](https://de.wikipedia.org/wiki/Rectifier_(neuronale_Netzwerke))
(rectified linear unit) und der [Tangens
hyperbolicus](https://de.wikipedia.org/wiki/Tangens_hyperbolicus_und_Kotangens_hyperbolicus)
als Aktivierungsfunktion verwendet, die im Folgenden dargestellt werden.

ReLU-Funktion:

```{figure} pics/fig_12_02_plot_relu_function.svg
---
name: fig_12_02_plot_relu_function
width: 100%
---
ReLU-Funktion (Quelle: eigene Darstellung; Lizenz:
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
```

Tangens hyperbolicus:

```{figure} pics/fig_12_02_plot_tanh_function.svg
---
name: fig_12_02_plot_tanh_function
width: 100%
---
Tangens hyperbolicus (Quelle: eigene Darstellung; Lizenz:
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
```

Beide Funktionen haben einen glatten Verlauf (keinen harten Sprung wie die
Heaviside-Funktion). Daher können die Gewichte $w_0, w_1, \ldots, w_n$ mit
mathematischen Optimierungsverfahren besser bestimmt werden als beim klassischen
Perzeptron mit der Heaviside-Funktion. Im nächsten Kapitel werden wir sehen, wie
das in der Praxis mit Scikit-Learn funktioniert. Vorher beschäftigen wir uns mit
dem Zusammensetzen von vielen Perzeptronen zu einem neuronalen Netz.

## Aus Neuronen wird ein Netz

Neuronale Netze sind Netze aus einzelnen künstlichen Neuronen. Im Folgenden
werden wir auf eine mathematisch präzise Beschreibung von neuronalen Netzen
verzichten und stattdessen das Konzept eines neuronalen Netzes anhand von
Schemazeichnungen erläutern. Dazu vereinfachen wir zunächst die schematische
Darstellung des künstlichen Neurons. Zunächst fassen wir die beiden
mathematischen Operationen »Übertragungsfunktion« (Bilden der gewichteten Summe)
und »Aktivierungsfunktion« in einem gemeinsamen Kreis in der Mitte zusammen. Die
Bias-Einheit lassen wir in der Darstellung ebenfalls weg.

```{figure} pics/fig_12_02_neuron_with_annotations.svg
---
width: 100%
name: fig_12_02_neuron_with_annotations
---
Vereinfachte schematische Darstellung eines künstlichen Neurons (Quelle: eigene
Darstellung; Lizenz: [CC BY-NC-SA
4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
```

Tatsächlich sind sogar häufig Darstellungen verbreitet, bei denen die
Beschriftungen komplett weggelassen werden.

```{figure} pics/fig_12_02_neuron_without_annotations.svg
---
width: 100%
name: fig_12_02_neuron_without_annotations
---
Symbolbild eines künstlichen Neurons (Quelle: eigene Darstellung;
Lizenz: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
```

Mit Hilfe dieser stark vereinfachten Darstellung eines künstlichen Neurons
zeigen wir nun, wie aus vielen solcher künstlicher Neuronen ein neuronales Netz
zusammengesetzt wird. In einem ersten Schritt werden die Eingaben für jedes
Merkmal (in diesem Beispiel vier Merkmale symbolisiert durch hellblaue Kreise)
gewichtet, aufsummiert und dann wird darauf eine Aktivierungsfunktion angewendet
(weißer Kreis oben). Diesen Vorgang wiederholen wir mit anderen Gewichten oder
einer anderen Aktivierungsfunktion, also mit einem zweiten künstlichen Neuron
(weißer Kreis unten). In einem zweiten Schritt werden die beiden Ergebnisse der
einzelnen künstlichen Neuronen wiederum verrechnet, um daraus die finale Ausgabe
zu prognostizieren (dunkelblauer Kreis). Die folgende Schemazeichnung
verdeutlicht diese Vorgehensweise für vier Merkmale (die Bias-Einheit wurde
wieder weggelassen).

```{figure} pics/fig_12_02_multi_layer_perceptron.svg
---
width: 100%
name: fig_12_02_multi_layer_perceptron
---
Ein mehrschichtiges Perzeptron (Multilayer Perceptron) (Quelle: eigene
Darstellung; Lizenz: [CC BY-NC-SA
4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
```

Bei dieser Architektur unterscheiden wir drei Arten von Schichten.

1. Die **Eingabeschicht** (auf Englisch: Input Layer) nimmt die Eingabedaten
   entgegen. Jedes Neuron in der Eingabeschicht entspricht einem Merkmal oder
   einer Eigenschaft der Eingabedaten.
2. Die **Ausgabeschicht** (auf Englisch: Output Layer) liefert das Ergebnis der
   Berechnung. Bei einer binären Klassifikationsaufgabe besteht die
   Ausgabeschicht beispielsweise aus einem einzigen Neuron.
3. Zwischen Eingabe- und Ausgabeschicht liegen die **versteckten Schichten**
   (auf Englisch: Hidden Layers). Diese Schichten heißen versteckt, weil wir von
   außen nur die Eingabe und die Ausgabe sehen, nicht aber die
   Zwischenergebnisse in diesen Schichten. Die versteckten Schichten ermöglichen
   es dem neuronalen Netz, komplexe nichtlineare Zusammenhänge zwischen Eingabe
   und Ausgabe zu erlernen. Je mehr versteckte Schichten ein neuronales Netz
   hat, desto komplexere Muster kann es prinzipiell erfassen.

Ab etwa 2-3 versteckten Schichten spricht man von **Deep Learning**.

```{admonition} Mini-Übung
:class: tip
Betrachten Sie das mehrschichtige Perzeptron aus der Abbildung oben. Es hat vier
Eingabeneuronen, eine versteckte Schicht mit zwei Neuronen und ein
Ausgabeneuron.

1. Wie viele Gewichte verbinden die Eingabeschicht mit der versteckten Schicht?
2. Wie viele Gewichte verbinden die versteckte Schicht mit der Ausgabeschicht?
3. Wie viele Bias-Einheiten benötigt das Netz insgesamt?
4. Berechnen Sie die Gesamtzahl aller Parameter (Gewichte + Bias-Einheiten) des
   Netzes. Mit 'Parameter' meinen wir alle Zahlen, die das Netz lernen muss,
   also alle Gewichte und Bias-Einheiten zusammen.
```

```{admonition} Lösung
:class: tip
:class: dropdown
1. Jedes der 4 Eingabeneuronen ist mit jedem der 2 Neuronen in der versteckten
   Schicht verbunden: 4 × 2 = 8 Gewichte
2. Jedes der 2 Neuronen der versteckten Schicht ist mit dem 1 Ausgabeneuron
   verbunden: 2 × 1 = 2 Gewichte
3. Jedes Neuron (außer den Eingabeneuronen) benötigt eine Bias-Einheit: 2
   (versteckte Schicht) + 1 (Ausgabeschicht) = 3 Bias-Einheiten
4. Gesamtzahl Parameter: 8 + 2 + 3 = 11 Parameter

*Allgemeine Formel:* Zwischen zwei Schichten mit $n$ und $m$ Neuronen gibt es $n
\times m$ Gewichte plus $m$ Bias-Einheiten.
```

Das folgende Video fasst die Struktur eines neuronalen Netzes noch einmal zusammen.

```{dropdown} Video "Neuronale Netze" von Plattform Lernende Systeme
<iframe width="560" height="315" src="https://www.youtube.com/embed/2dBu9wgW2-s"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write;
encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
```

## Zusammenfassung und Ausblick

Nachdem wir in diesem Kapitel das Konzept eines neuronalen Netzes erklärt haben,
werden wir im nächsten Kapitel ein neuronales Netz mit Scikit-Learn trainieren.
Dabei werden wir lernen, wie das Netz die optimalen Gewichte automatisch findet.
