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

# 10.2 Training SVM mit Scikit-Learn

Wenn wir in der Dokumentation von Scikit-Learn
[Scikit-Learn/SVM](https://scikit-learn.org/stable/modules/svm.html) die Support
Vector Machines nachschlagen, so finden wir viele Einträge: SVC, NuSVC,
LinearSVC, SVR, NuSVR und LinearSVR. Die Varianten mit "C" stehen für
Klassifikation (englisch Classification) und die Varianten mit "R" für
Regression. Wir benutzen in diesem Kapitel das Modell SVC.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können ein SVM-Modell mit der Klasse SVC erzeugen.
* Sie können den Parameter C zur Steuerung der Margins einsetzen.
```

## Wahl des linearen Kernels

Zuerst importieren wir aus Scikit-Learn das entsprechende Modul 'SVM' und
instantiieren ein Modell. Da wir die etwas allgemeinere Klasse SVC anstatt
LinearSVC verwenden, müssen wir bereits bei der Erzeugung die Option `kernel=`
auf linear setzen, also `kernel='linear'`.

```{code-cell}
from sklearn import svm
svm_modell = svm.SVC(kernel='linear')
```

Wir erzeugen uns erneut künstliche Messdaten.

```{code-cell}
from sklearn.datasets import make_blobs
import matplotlib.pylab as plt; plt.style.use('bmh')

# Erzeugung künstlicher Daten
X, y = make_blobs(n_samples=60, centers=2, random_state=0, cluster_std=0.50)

# Visualisierung künstlicher Daten
import plotly.express as px

fig = px.scatter(x = X[:,0], y = X[:,1],  color=y, color_continuous_scale=['#3b4cc0', '#b40426'],
                 title='Künstliche Daten',
                 labels={'x': 'Feature 1', 'y': 'Feature 2'})
fig.show()
```

```{admonition} Warnung: Datenskalierung für SVM notwendig
:class: warning
SVMs sind empfindlich gegenüber unterschiedlichen Feature-Skalen. Ein Feature mit
Werten von 0-1000 dominiert ein Feature mit Werten 0-1, auch wenn beide gleich
wichtig sind. Daher sollten Features vor dem Training skaliert werden.
```

Eine Skalierung der Daten ist hier nicht erforderlich, da alle Features im
gleichen Wertebereich liegen. Als nächstes teilen wir die Messdaten in
Trainings- und Testdaten auf.

```{code-cell}
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
```

Nun können wir unser SVM-Modell trainieren:

```{code-cell}
svm_modell.fit(X_train, y_train);
```

Und als nächstes analysieren, wie viele der Testdaten mit dem trainierten Modell
korrekt klassifiziert werden.

```{code-cell}
svm_modell.score(X_test, y_test)
```

Ein super Ergebnis! Schön wäre es jetzt noch, die gefundene Trenngerade zu
visualisieren. Dazu modifizieren wir ein Code-Beispiel aus dem Buch: »Data
Science mit Python« von Jake VanderPlas (mitp Verlag 2017), ISBN 978-3-95845-
695-2, siehe
[https://github.com/jakevdp/PythonDataScienceHandbook](https://github.com/jakevdp/PythonDataScienceHandbook).

```{code-cell}
# Quelle: VanderPlas "Data Science mit Python", S. 482
# modified by Simone Gramsch
import numpy as np

def plot_svc_grenze(model):
    # aktuelles Grafik-Fenster auswerten
    ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Raster für die Auswertung erstellen
    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    Y, X = np.meshgrid(y, x)
    xy = np.vstack([X.ravel(), Y.ravel()]).T

    # Abstand zur Trennhyperebene berechnen mit eingebauter 
    # decision_function()
    P = model.decision_function(xy).reshape(X.shape)

    # Entscheidungsgrenzen und Margin darstellen
    ax.contour(X, Y, P, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])

    # Stützvektoren darstellen
    ax.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=300, linewidth=1, facecolors='none', edgecolors='orange');
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
```

```{code-cell}

fig, ax = plt.subplots()
ax.scatter(X[:,0], X[:,1], c=y, cmap='coolwarm')
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
ax.set_title('SVM mit Soft Margin');

plot_svc_grenze(svm_modell)
```

## Der Parameter C

Im letzten Abschnitt haben wir uns mit dem Parameter `C` beschäftigt, der
Ausnahmen innerhalb des Sicherheitsstreifens erlaubt. Wir können uns den
Parameter `C` als die "Höhe der Mauer" um den Margin vorstellen. Eine hohe Mauer
(großes `C`) schützt den Sicherheitsbereich streng. Praktisch keine Datenpunkte
dürfen hinein. Eine niedrige Mauer (kleines `C`) ist toleranter und lässt mehr
Ausnahmen zu. Als nächstes schauen wir uns an, wie der Parameter `C` gesetzt
wird.  

Die Option zum Setzen des Parameters C lautet schlicht und einfach `C=`. Dabei
muss C immer positiv sein. Der voreingestellte Standardwert ist `C=1`.

Damit aber besser sichtbar wird, wie sich C auswirkt, vermischen wir die
künstlichen Daten stärker. Für die Bewertung der Modelle trennen wir die Daten
in Trainings- und Testdaten.

```{code-cell}
# Erzeugung künstlicher Daten
X, y = make_blobs(n_samples=60, centers=2, random_state=0, cluster_std=0.80)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Visualisierung künstlicher Daten
import plotly.express as px

fig = px.scatter(x = X[:,0], y = X[:,1],  color=y, color_continuous_scale=['#3b4cc0', '#b40426'],
                 title='Künstliche Daten',
                 labels={'x': 'Feature 1', 'y': 'Feature 2'})
fig.show()
```

Zuerst wählen wir ein sehr hohes `C=1000000`. Das ist ein Hard Margin, eine
praktisch nicht durchdringbare Mauer, die keine Datenpunkte in den
Sicherheitsbereich lässt.

```{code-cell}
# Wahl des Modells mit linearem Kern und großem C
svm_modell = svm.SVC(kernel='linear', C=1000000)

# Training und Bewertung
svm_modell.fit(X_train, y_train);
score = svm_modell.score(X_test, y_test)
print(f'Score auf den Testdaten: {score:.2f}')

# Visualisierung
fig, ax = plt.subplots()
ax.scatter(X[:,0], X[:,1], c=y, cmap='coolwarm')
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
ax.set_title('SVM mit Hard Margin');
plot_svc_grenze(svm_modell)
```

Nun reduzieren wir den Wert des Parameters `C` deutlich auf `C=1`. Vereinzelt
liegen Datenpunkte nun im Sicherheitsbereich, d.h. wir haben einen Soft Margin.

```{code-cell}
# Wahl des Modells mit linearem Kern und kleinem C
svm_modell = svm.SVC(kernel='linear', C=1)

# Training und Bewertung
svm_modell.fit(X_train, y_train);
score = svm_modell.score(X_test, y_test)
print(f'Score auf den Testdaten: {score:.2f}')

# Visualisierung
fig, ax = plt.subplots()
ax.scatter(X[:,0], X[:,1], c=y, cmap='coolwarm')
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
ax.set_title('SVM mit Soft Margin');
plot_svc_grenze(svm_modell)
```

Die Visualisierung zeigt, dass bei kleinem `C` mehr Stützvektoren (orange
eingekreist) vorhanden sind, und einige davon innerhalb des Margins liegen oder
die Klassifikationsgrenze verletzen.

Welches `C` sollen wir wählen? Beide Modelle liefern den gleichen Score von 1.0
auf den Testdaten. Das kleinere `C` führt jedoch zu einem robusteren Modell mit
breiterem Margin. In der Praxis wird `C` oft durch Kreuzvalidierung
(Crossvalidation) optimiert, was wir in einem späteren Kapitel aufgreifen
werden.

## Zusammenfassung

Verwenden wir den SVC-Klassifikator aus dem Modul SVM von Scikit-Learn, können
wir mittels der Option `kernel='linear'` eine binäre Klassifikation durchführen,
bei der die Trennungsgerade den größtmöglichen Abstand zwischen den Gruppen von
Punkten erzeugt, also einen möglichst großen Margin. Sind die Daten nicht linear
trennbar, so können wir mit der Option `C=` steuern, wie viele Ausnahmen erlaubt
werden sollen. Mit Ausnahmen sind Punkte innerhalb des Margins gemeint. Im
nächsten Abschnitt betrachten wir nichtlineare Trennungsgrenzen.
