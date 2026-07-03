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

# 9.1 Grundideen der Ensemble-Methoden

Eins, zwei, viele ... im Bereich des maschinellen Lernens sind Ensemble-Methoden
leistungsstarke Techniken zur Verbesserung der Modellgenauigkeit und Robustheit.
Diese Methoden kombinieren mehrere Modelle, um die Gesamtleistung zu steigern,
indem sie die individuellen Stärken der Modelle nutzen und deren Schwächen
ausgleichen. In diesem Kapitel werden wir die grundlegenden Konzepte und
Unterschiede zwischen diesen Methoden erläutern, um ein besseres
Verständnis ihrer Funktionsweise und Anwendungen zu vermitteln.

## Lernziele

```{admonition} Lernziele
:class: attention
* Sie können in eigenen Worten erklären, was **Ensemble-Methoden** sind.
* Sie kennen die Grundideen der Ensemble-Methoden
  * **Voting**,
  * **Averaging**,
  * **Stacking**,
  * **Bagging** und 
  * **Boosting**.
```

## Ensemble-Methoden

Der Begriff »Ensemble« wird im Allgemeinen eher mit Musik und Kunst in
Verbindung gebracht als mit Informatik. In der Musik bezeichnet ein Ensemble
eine kleine Gruppe von Musikern, die entweder das gleiche Instrument spielen
oder verschiedene Instrumente kombinieren. Im Theater bezeichnet man eine Gruppe
von Schauspielern ebenfalls als Ensemble, und in der Architektur beschreibt der
Begriff eine Gruppe von Gebäuden, die in einem besonderen Zusammenhang
zueinander stehen.

Auch im Bereich des maschinellen Lernens hat sich der Begriff Ensemble
etabliert. Mit **Ensemble-Methoden** (Ensemble Learning) wird eine Gruppe von
maschinellen Modellen bezeichnet, die zusammen eine Prognose treffen sollen.
Ähnlich wie bei Musik-Ensembles können bei den Ensemble-Methoden entweder
identische Modelle oder verschiedene Modelle kombiniert werden. Diese Modelle
können entweder gleichzeitig eine Prognose treffen, die dann kombiniert wird,
oder nacheinander verwendet werden, wobei ein nachfolgendes Modell die Fehler
des vorherigen korrigiert. Je nach Vorgehensweise unterscheidet man im
maschinellen Lernen zwischen **Voting**, **Averaging**, **Stacking**,
**Bagging** und **Boosting**.

In dieser Vorlesung konzentrieren wir uns auf Bagging und Boosting mit ihren
bekanntesten Vertretern, den Random Forests und XGBoost. Die Konzepte Voting und
Averaging sowie Stacking werden hier nur kurz ohne weitere Details vorgestellt.
Eine allgemeine Einführung in Ensemble-Methoden mit Scikit-Learn findet sich in
der [Dokumentation Scikit-Learn →
Ensemble](https://scikit-learn.org/stable/modules/ensemble.html).

## Voting, Averaging und Stacking

```{figure} pics/concept_voting.svg
---
width: 100%
---
Die Prognosen von mehreren *unterschiedlichen* ML-Modellen werden zu einer
finalen Prognose kombiniert. Die Kombination kann beispielsweise durch
Mehrheitsentscheidung (Voting), aber auch Mittelwertbildung (Averaging)
erfolgen.
```

In einem ersten Schritt werden mehrere ML-Modelle unabhängig voneinander auf den
Trainingsdaten trainiert. Jedes dieser Modelle liefert eine Prognose, die dann
auf verschiedene Arten miteinander kombiniert werden können. Bei
Klassifikationsaufgaben ist **Voting**, also die Wahl durch
Mehrheitsentscheidung, eine beliebte Methode, um die Einzelprognosen zu
kombinieren. Wurden beispielsweise drei ML-Modelle gewählt, die jeweils ja oder
nein prognostizieren, dann wird für die finale Prognose das Ergebnis genommen,
das die Mehrheit der einzelnen Modelle vorausgesagt hat. Scikit-Learn bietet
dafür einen Voting Classifier an, siehe [Dokumentation Scikit-Learn → Voting
Classifier](https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier).

Bei Regressionsaufgaben werden die einzelnen Prognosen häufig gemittelt. Beim
**Averaging** kann entweder der übliche arithmetische Mittelwert verwendet
werden oder ein gewichteter Mittelwert, was als Weighted Averaging bezeichnet
wird. Dennoch wird die Mittelwertbildung bei Regressionsaufgaben von
Scikit-Learn ebenfalls als Voting bezeichnet, siehe [Dokumentation Scikit-Learn
→ Voting
Regressor](https://scikit-learn.org/stable/modules/ensemble.html#voting-regressor).

Eine alternative Kombinationsmethode ist die Verwendung eines weiteren
ML-Modells. In diesem Fall werden die Modelle, die die einzelnen Prognosen
liefern, als Basismodelle bezeichnet. Die Basismodelle liefern Features für ein
weiteres ML-Modell, das als Meta-Modell bezeichnet wird. Diese Ensemble-Methode
wird **Stacking** genannt. Weitere Informationen liefert die [Scikit-Learn
Dokumentation → Stacked
Generalization](https://scikit-learn.org/stable/modules/ensemble.html#stacked-generalization).

Stacking bietet viele Vorteile. Der wichtigste Vorteil ist, dass die
Prognosefähigkeit des Gesamtmodells in der Regel deutlich besser ist als die der
einzelnen Basismodelle. Die Stärken der Basismodelle werden kombiniert und die
Schwächen ausgeglichen. Allerdings erfordert Stacking sehr viel Feinarbeit. Auch
steigt die Trainingszeit für das Gesamtmodell, selbst wenn die Basismodelle bei
genügend Rechenleistung parallel trainiert werden können. Aus diesem Grund
werden wir in dieser Vorlesung kein Stacking verwenden.

## Bagging

```{figure} pics/concept_bagging.svg
---
width: 100%
---
Beim Bagging wird das gleiche ML-Modell auf *unterschiedlichen* Stichproben der
Trainingsdaten trainiert (Bootstrapping). Die Einzelprognosen der Modelle werden
dann zu einer finalen Prognose kombiniert (Aggregating).
```

Bagging ist eine Ensemble-Methode, bei der stets dasselbe Modell für die
Einzelprognosen verwendet wird. Die Unterschiede in den Einzelprognosen
entstehen dadurch, dass für das Training der einzelnen Modelle unterschiedliche
Daten verwendet werden.

Im ersten Schritt werden zufällige Datenpunkte aus den Trainingsdaten ausgewählt
und in einen neuen Datensatz, „Stichprobe 1“, aufgenommen. Nachdem ein
Datenpunkt ausgewählt wurde, kehrt er in die ursprüngliche Menge der
Trainingsdaten zurück und kann erneut ausgewählt werden. Dieser Prozess wird in
der Mathematik als **Ziehen mit Zurücklegen** bezeichnet, auf Englisch
**Bootstrapping**. Durch Bootstrapping werden dann noch weitere Stichproben
gebildet, wobei jede Stichprobe üblicherweise die gleiche Anzahl an Datenpunkten
wie der ursprüngliche Datensatz enthält.

Im zweiten Schritt wird ein ML-Modell gewählt und für jede Bootstrap-Stichprobe
trainiert. Da die Stichproben unterschiedliche Trainingsdaten enthalten,
entstehen unterschiedlich trainierte Modelle, die für neue Daten verschiedene
Einzelprognosen liefern. Diese Einzelprognosen werden kombiniert bzw. nach
festgelegten Regeln zu einer finalen Prognose zusammengefasst. In der Statistik
wird die Zusammenfassung von Daten als Aggregation bezeichnet. Auf Englisch
heißt der Vorgang des Zusammenfassens **Aggregating**.

Die beiden wesentlichen Schritte der Bagging-Methode sind also **B**ootstrapping
und **Agg**regat**ing**, woraus sich die Abkürzung »Bagging« ableitet.
Scikit-Learn bietet sowohl für Klassifikations- als auch für Regressionsaufgaben
eine allgemeine Implementierung der Bagging-Methode an (siehe [Dokumentation
Scikit-Learn →
Bagging](https://scikit-learn.org/stable/modules/ensemble.html#bagging-meta-estimator)).
Die bekannteste Bagging-Methode ist **Random Forests**, bei dem
Entscheidungsbäume (Decision Trees) auf unterschiedlichen Stichproben trainiert
und aggregiert werden. Random Forests werden wir im nächsten Kapitel
detaillierter betrachten. Vorab beschäftigen wir uns noch mit dem Konzept der
Boosting-Methoden.

## Boosting

```{figure} pics/concept_boosting.svg
---
width: 100%
---
Der Fehler in der Prognose wird benutzt, um das nächste Modell zu trainieren.
Beim hier gezeigten Adaboost-Verfahren werden die Daten neu gewichtet, beim
(Stochastic) Gradient Boosting werden Modelle zur Fehlerkorrektur trainiert.
```

Das englische Verb „to boost sth.“ hat viele Bedeutungen. Insbesondere wird es
im Deutschen mit „etwas verstärken“ übersetzt. Im Kontext des maschinellen
Lernens bezeichnet **Boosting** eine Ensemble-Methode, bei der mehrere ML-Modelle
hintereinander geschaltet werden, um die Genauigkeit der Prognose zu verstärken.
Die Idee des Boosting besteht darin, dass jedes Modell die Fehler des
Vorgängermodells reduziert. Es gibt mehrere Varianten zur Fehlerreduktion, aus
denen sich unterschiedliche Boosting-Methoden ableiten. Die wichtigsten
Varianten sind:

* Adaboost,
* Gradient Boosting und
* Stochastic Gradient Boosting.

Beim **Adaboost**-Verfahren wird im ersten Schritt ein Modell (z.B. ein
Entscheidungsbaum) auf den Trainingsdaten trainiert. Anschließend werden die
Prognosen dieses Modells mit den tatsächlichen Werten verglichen. Im zweiten
Schritt wird ein neuer Datensatz erstellt, wobei die falsch prognostizierten
Datenpunkte ein größeres Gewicht erhalten. Nun wird erneut ein Modell trainiert;
und dessen Prognosen werden wieder mit den echten Werten verglichen. Dieser
Vorgang wird mehrfach wiederholt. Das Training der Modelle erfolgt sequentiell,
da jedes Vorgängermodell die neue Gewichtung der Trainingsdaten liefert. Am Ende
werden alle Einzelprognosen gewichtet zu einer finalen Prognose kombiniert.
Weitere Details finden sich in der [Dokumentation Scikit-Learn →
Adaboost](https://scikit-learn.org/stable/modules/ensemble.html#adaboost).

Beim **Gradient Boosting** wird ebenfalls ein sequentieller Ansatz verfolgt,
aber der Fokus liegt auf der Minimierung der Fehler. Im ersten Schritt wird ein
ML-Modell (häufig ein Entscheidungsbaum) trainiert. Danach wird für jeden
Datenpunkt der Fehler des Modells, das sogenannte **Residuum**, berechnet, indem
die Differenzen zwischen dem tatsächlichen Wert und den Prognosen bestimmt wird.
Im nächsten Schritt wird ein neues Modell trainiert, das darauf abzielt, diese
Residuen vorherzusagen. Dieses neue Modell wird dann zu dem vorherigen Modell
hinzugefügt, um die Gesamtprognose zu verbessern. Dieser Prozess wird
wiederholt, wobei in jeder Iteration ein neues Modell trainiert wird, das die
Fehler der bisherigen Modelle reduziert (mit Hilfe einer Verlustfunktion und
eines Gradientenverfahrens). Am Ende ergibt sich eine starke Vorhersage, indem
alle Modelle kombiniert werden. Da häufig Entscheidungsbäume als Modell gewählt
werden, bietet Scikit-Learn eine Implementierung der sogenannten
**Gradient-Boosted Decision Trees** an, siehe [Dokumentation Scikit-Learn →
Gradient-boosted
trees](https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosted-trees).

**Stochastic Gradient Boosting** ist eine Erweiterung des Gradient Boosting, bei
der zusätzlich Stochastik eingeführt wird. Hierbei wird in jedem Schritt nur
eine zufällige Stichprobe der Trainingsdaten verwendet, um ein Modell zu
trainieren. Der Trainingsprozess ähnelt dem von Gradient Boosting, wobei in
jeder Runde ein neues Modell trainiert wird, das die Fehler der vorherigen
Modelle korrigiert. Durch die zufällige Auswahl der Trainingsdaten in jeder
Iteration wird eine höhere Robustheit gegenüber Overfitting (Überanpassung)
erreicht. Stochastic Gradient Boosting wird von Scikit-Learn nicht direkt
unterstützt. Eine sehr bekannte Implementierung davon ist XGBoost (siehe
[https://xgboost.readthedocs.io/](https://xgboost.readthedocs.io/en/stable/)),
die wir in einem der nächsten Kapitel noch näher betrachten werden.

## Zusammenfassung und Ausblick

In diesem Kapitel haben Sie die Konzepte Voting, Averaging, Stacking, Bagging
und Boosting kennengelernt. Alle Methoden sind Ensemble-Methoden, bei denen
mehrere ML-Modelle parallel oder sequentiell kombiniert werden. Obwohl diese
Ensemble-Methoden allgemein für verschiedene ML-Modelle eingesetzt werden
können, haben sich vor allem Random Forests (Bagging für Entscheidungsbäume) und
Stochastic Gradient Boosting als besonders effektiv erwiesen. Letztere sind
nicht in Scikit-Learn implementiert, sondern werden durch eine eigene Bibliothek
namens XGBoost bereitgestellt. In den nächsten beiden Kapiteln werden wir beide
auch mit praktischen Beispielen vertiefen.
