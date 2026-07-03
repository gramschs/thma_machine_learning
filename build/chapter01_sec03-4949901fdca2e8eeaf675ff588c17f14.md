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

# 1.3 Technische Voraussetzungen

Für maschinelles Lernen ist **Python** die Programmiersprache der Wahl. Das
liegt vor allem auch daran, dass Google eine sehr wichtige ML-Bibliothek für
Python zur Verfügung stellt, die sogenannte Bibliothek
[TensorFlow](https://www.tensorflow.org). Glücklicherweise müssen wir die
Algorithmen nicht selbst in Python umsetzen, sondern können schon fertige
Modelle aus Bibliotheken wie beispielsweise
[scikit-learn](https://scikit-learn.org/stable/index.html) verwenden, die wir
dann noch an die Daten anpassen müssen. In diesem Kapitel werden die technischen
Voraussetzungen beschrieben, um maschinelles Lernen mit Python und den
sogenannten **Jupyter Notebooks** umzusetzen.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie haben eine lauffähige **Python-Distribution** installiert.
* Sie können **JupyterLab** starten und ein **Jupyter Notebook** erzeugen.
* Sie kennen den prinzipiellen Aufbau eines Jupyter Notebooks mit
  **Markdown-Zellen** und **Code-Zellen**.
```

## Was sind Jupyter Notebooks?

Die Vorlesung wird in Form von **Jupyter Notebooks** zur Verfügung gestellt.
Jupyter Notebooks sind interaktive digitale Notizbücher, die sowohl Texte,
Bilder oder Videos enthalten können als auch Python-Code, der direkt im
Notizbuch ausführbar ist.

Die Kombination von Text, Python-Code und Visualisierungen macht Jupyter
Notebooks zu einem sehr leistungsstarken Werkzeug für die Datenanalyse. Daten
können direkt in die Jupyter Notebooks eingegeben oder importiert werden.
Fehlende Daten oder Ausreißer können direkt korrigiert werden, ohne dass mit
einer externen Software die Korrektur dokumentiert werden muss. Die Ergebnisse
der Analysen oder ML-Modelle können sofort im Jupyter Notebook dargestellt
werden, ohne dass eine externe Anwendung gestartet werden müssen. Daher sind sie
eine der bekanntesten Anwendungen im Bereich Data Science und werden oft zur
Datenanalyse, maschinellem Lernen und Visualisierung eingesetzt.

## Installation Python

Python wird in der Regel mit dem Betriebsystem ausgeliefert. Für maschinelles
Lernen benötigen wir jedoch weitere **Python-Module**, die die grundlegenden
Funktionalitäten von Python um ML-Funktionalitäten erweitern. Diese sind
normalerweise nicht vorinstalliert, sondern müssen nachinstalliert werden. Bevor
man sich die Module aus verschiedenen Internetquellen zusammensucht, ist es
einfacher, eine sogenannte Python-Distribution zu benutzen.

Eine **Distribution** ist eine Zusammenstellung von Software oder
Bibliotheken/Modulen. Die Firma Anaconda, Inc. wurde 2012 mit dem Ziel
gegründet, Python in Unternehmen speziell für die Geschäftsfeldanalyse (Business
Analytics) einzuführen, was die Open Source Community so nicht leisten konnte.
Daher enthält die Python-Distribution [Anaconda](https://www.anaconda.com) eine
Reihe von nützlichen Paketen und Bibliotheken für wissenschaftliche
Berechnungen, Datenanalyse, maschinelles Lernen und andere Anwendungen. Da sie
eine Benutzeroberfläche beinhaltet, mit der die Python-Bibliotheken verwaltet
werden, ist sie auch gerade für Einsteiger in Python eine gute Wahl.

Die Python-Distribution Anaconda gibt es in verschiedenen Editionen mit
entsprechenden Preismodellen. Für diese Vorlesung ist die sogenannte »Individual
Edition« ausreichend, die von Anaconda kostenlos zur Verfügung gestellt wird.

Hier ist eine Schritt-für-Schritt-Anleitung zum Installieren von Python mit der
Distribution Anaconda für Windows und MacOS:

1. Öffnen Sie die offizielle Anaconda-Website unter
   <https://www.anaconda.com/products/individual> und laden Sie die neueste
   Version von Anaconda für Ihr Betriebssystem herunter.
2. Führen Sie die Installationsdatei aus und folgen Sie den Anweisungen auf dem
   Bildschirm.
3. Öffnen Sie nach der Installation das Anaconda-Navigator-Programm, das im
   Startmenü oder Launchpad verfügbar sein sollte.

## Mit welcher App wird ein Jupyter Notebook bearbeitet?

Es gibt mehrere Applikationen, die Jupyter Notebooks bearbeiten können. Am
bekanntesten ist sicherlich [JupyterLab](https://jupyter.org), das wir auch in
dieser Vorlesung verwenden. Neben JupyterLab gibt es aber auch weitere
Möglichkeiten, um Jupyter Notebooks zu bearbeiten.

Die beiden Entwicklungsumgebungen

* [PyCharm](https://www.jetbrains.com/help/pycharm/jupyter-notebook-support.html)
* [Microsoft Visual Studio Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)

ermöglichen ebenfalls die direkte Bearbeitung von Jupyter Notebooks. Auch
zahlreiche Cloudanbieter bieten direkt das Bearbeiten und Ausführen von Jupyter
Notebooks an, z.B.

* [Google Colab](https://colab.research.google.com/notebook)
* [Microsoft Azure](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks)
* [Deepnote](https://deepnote.com)
* [replit](https://replit.com/template/jupyter-notebook)

Wie bei allen Clouddiensten sollte man sich jedoch eingehend mit den
Datenschutzbestimmungen des Anbieters vertraut machen, bevor man den Dienst in
Anspruch nimmt. Aufgrund des Datenschutzes empfehle ich stets, Python/Anaconda
lokal zu installieren.

## Start von JupyterLab und das erste Jupyter Notebook

Anaconda installiert JupyterLab automatisch mit, so dass wir direkt loslegen
können. Sollte es Probleme geben, finden Sie hier die [Dokumentation von
JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html).

JupyterLab startet im Hintergrund einen sogenannten Jupyter-Kernel, der die
interaktiven Python-Code-Zellen ausführt. Der Client ist in der Regel der
Standard-Browser.

Die folgende Schritt-für-Schritt-Anleitung zeigt, wie ein neues Jupyter Notebook
in JupyterLab erstellt wird.

1. Um ein neues Jupyter Notebook zu erstellen, klicken Sie auf "Home" im
   Anaconda-Navigator und wählen "JupyterLab" aus. Alternativ können Sie
   JupyterLab auch mit dem Befehl "jupyter-lab" aus einem Terminal oder einer
   Konsole starten (Linux oder MacOS).
2. Wählen Sie "Python 3 (ipykernel)" aus, um ein neues Notebook zu erstellen.
3. Sie können jetzt Python-Code in dem Notebook schreiben und ausführen. Wenn
   Sie zusätzliche Pakete benötigen, können Sie diese über den
   "Environments"-Tab im Anaconda-Navigator installieren.

```{figure} pics/fig_chap01_sec02_jupyterlab.png
:name: fig_chap01_sec02_jupyterlab

Startansicht der Software JupyterLab: ein neues Jupyter Notebook wird mit Klick auf den Button Python 3 (ipykernel) erstellt.
```

## Grundlegende Funktionalitäten von Jupyter Notebooks

Ein Jupyter Notebook besteht aus einer Abfolge von Zellen, in denen Text, Code
und Visualisierungen eingebettet werden. Die Zellen können entweder in der
Programmiersprache Python oder in einer Reihe anderer Programmiersprachen wie R,
Julia oder JavaScript geschrieben werden. Erkennbar sind Jupyter Notebooks an
der Dateiendung `ipynb`, die die Abkürzung für »**i**ntelligentes **Py**thon
**N**ote**b**ook« darstellt.

```{figure} pics/fig_chap01_sec03_zellen.png
:name: fig_chap01_sec03_zellen

Screenshot eines Jupyter Notebooks mit einer nicht ausgeführten Markdown-Zelle (1), einer ausgeführten Code-Zelle (2) und dem Run-Button (3)
```

Wie im obigen Screenshot zu sehen, sind Zellen mit einem Rahmen versehen. Eine
Zelle kann entweder eine Text-Zelle (1) oder eine Code-Zelle (2) sein. In
Text-Zellen wird die sogenannte
[Markdown-Formatierung](https://de.wikipedia.org/wiki/Markdown) benutzt, weshalb
sie **Markdown-Zellen** genannt werden. Bei dieser Art, Text zu formatieren,
werden Textzeichen benutzt anstatt auf einen Button zu klicken. Um
beispielsweise ein Wort fettgedruckt anzuzeigen, werden zwei Sternchen `**` vor
und hinter das Wort gesetzt, also ich bin `**fett**` gedruckt.

In **Code-Zellen** (2) können Sie direkt Python-Code eingeben. Sie erkennen eine
Code-Zelle daran, dass eckige Klammern links daneben stehen. Eine Code-Zelle
wird ausgeführt, indem Sie auf "Run" klicken. Der Run-Button verbirgt sich
hinter dem kleinen nach rechts gerichteten Dreick in der Menü-Leiste des Jupyter
Notebooks (3). Danach erscheint die Ausgabe, die der Python-Interpreter ggf.
produziert. Wird eine Code-Zelle ausgeführt, so erscheint eine Zahl in den
eckigen Klammern. Diese Zahl zeigt die Reihenfolge an, in der Code-Zellen
ausgeführt wurden.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir uns mit den technischen Voraussetzungen für
maschinelles Lernen mit Python beschäftigt. Zum Standardwerkzeug im Bereich des
maschinellen Lernens sind die Jupyter Notebooks geworden, die wir in den
nächsten Kapiteln immer besser kennenlernen werden. Im nächsten Part werden wir
im Schnelldurchlauf Python wiederholen.
