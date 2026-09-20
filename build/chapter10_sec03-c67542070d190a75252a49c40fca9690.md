---
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 10.3 Gütemaße für Klassifikation und Regression

```{admonition} Warnung
:class: warning
Dieses Kapitel befindet sich derzeit im Umbau und wird rechtzeitig vor der
Vorlesung im WiSe 2026/27 zur Verfügung stehen.
```

Geplante Einleitung:

* Anknüpfung an den Ausblick von 10.2: Bei 2 % Ausschuss erreicht ein Modell,
  das immer "in Ordnung" vorhersagt, bereits 98 %.
* Bisher haben wir Modelle nur mit dem Standard-Score von Scikit-Learn bewertet:
  bei Klassifikation mit der Genauigkeit, bei Regression mit dem
  Bestimmtheitsmaß R².
* In diesem Kapitel lernen wir Gütemaße kennen, die zeigen, welche Fehler ein
  Modell macht und wie groß diese Fehler sind.

## Lernziele

* Entwurf, ein Lernziel pro Abschnitt:
  * Sie können eine Konfusionsmatrix erstellen und ablesen und erklären, warum
    die Accuracy bei unausgewogenen Klassen täuschen kann.
  * Sie können Precision, Recall und F1-Score berechnen und begründen, welches
    Gütemaß für eine Anwendung wichtig ist.
  * Sie können die Gütemaße MAE, MSE und RMSE für Regressionsmodelle berechnen
    und in der Einheit der Zielgröße deuten.

## Konfusionsmatrix und Accuracy

* Kernbeispiel: Fehldrucke vorhersagen mit dem 3D-Druck-Datensatz
  `3ddruck_kodierung.csv` aus Kapitel 8.2 (200 Druckaufträge, davon 14 %
  Fehldrucke). Merkmale Drucktemperatur, Betttemperatur und
  Druckgeschwindigkeit, Entscheidungsbaum der Tiefe 3.
* Zielgröße so kodieren, dass ein Fehldruck die 1 ist. Die Klasse, die wir
  finden wollen, heißt positive Klasse. In der Qualitätskontrolle ist das der
  Fehler, nicht das Gutteil.
* Aufteilung in Trainings- und Testdaten mit `stratify` (bekannt aus 8.3),
  damit die wenigen Fehldrucke in beiden Teilen gleich stark vertreten sind.
* Den bisherigen Standard-Score benennen: Accuracy (bisher Genauigkeit) ist der
  Anteil der richtig klassifizierten Datenpunkte.
* Accuracy-Falle: Der Baum erreicht 0.86, genau so viel wie ein Modell, das
  immer "Erfolg" vorhersagt. Vergleich mit diesem einfachen Referenzmodell.
* Konfusionsmatrix mit `confusion_matrix()` aus `sklearn.metrics`: tatsächliche
  gegen prognostizierte Klasse. Vier Felder: richtig positiv, falsch positiv,
  falsch negativ, richtig negativ (englisch TP, FP, FN, TN).
* Reihenfolge in Scikit-Learn: Zeilen sind die tatsächlichen, Spalten die
  prognostizierten Klassen, jeweils zuerst 0, dann 1.
* Ablesen: Der Baum erkennt keinen einzigen der 7 Fehldrucke in den Testdaten.
* Accuracy aus der Konfusionsmatrix berechnen: richtige Prognosen (Diagonale)
  geteilt durch alle Prognosen.
* Mini-Übung: dasselbe für `3ddruck_gittersuche.csv` (41 % Fehldrucke, bekannt
  aus 10.2) mit Referenzmodell und Konfusionsmatrix. Erkenntnis: Je
  ausgewogener die Klassen, desto weniger täuscht die Accuracy.

## Precision, Recall und F1-Score

* Fragen aus der Praxis: Welcher Anteil der Fehldrucke wird gefunden? Wie viele
  Alarme sind berechtigt?
* Recall (Trefferquote): richtig positiv geteilt durch alle tatsächlichen
  Fehldrucke. "Wie viel Ausschuss fangen wir ab?"
* Precision (Präzision): richtig positiv geteilt durch alle gemeldeten
  Fehldrucke. "Wie oft schlagen wir unnötig Alarm?"
* Englische Begriffe beibehalten. Im Deutschen steht "Genauigkeit" mal für
  Accuracy, mal für Precision.
* Kernbeispiel: derselbe Baum mit `class_weight='balanced'`, damit Fehldrucke
  beim Training stärker zählen. Die Accuracy sinkt von 0.86 auf 0.84, aber 3
  von 7 Fehldrucken werden erkannt (Recall 0.43), bei 4 Fehlalarmen (Precision
  0.43). Das Modell mit der schlechteren Accuracy ist für die
  Qualitätskontrolle das bessere.
* Zielkonflikt: Mehr Alarme erhöhen den Recall und senken meist die Precision.
* F1-Score: fasst Precision und Recall in einer Zahl zusammen (harmonisches
  Mittel) und wird klein, sobald einer der beiden Werte klein ist.
* Code: `precision_score()`, `recall_score()` und `f1_score()` aus
  `sklearn.metrics`.
* Welches Gütemaß wann? Sicherheitsbauteil: Recall wichtig, kein Ausschuss darf
  durchrutschen. Teure Nachprüfung oder Produktionsstopp bei jedem Alarm:
  Precision wichtig. Beides gleich wichtig: F1-Score.
* Rückbezug zu 10.2: Mit `scoring='recall'` oder `scoring='f1'` optimieren
  `cross_validate()` und `GridSearchCV` das passende Gütemaß statt der
  Accuracy.
* Mini-Übung: Precision, Recall und F1-Score für das Modell aus der vorherigen
  Mini-Übung berechnen und für zwei Anwendungsfälle das passende Gütemaß
  begründen. Optional eine Gittersuche mit `scoring='recall'`.

## Gütemaße für Regression

* Anknüpfung an Kapitel 7: Bei Regression ist der Standard-Score das
  Bestimmtheitsmaß R². Es zeigt, wie gut das Modell im Vergleich zum Mittelwert
  ist, aber nicht, wie weit die Prognosen danebenliegen.
* Kernbeispiel: Verkaufspreis mit dem Autoscout24-Datensatz vorhersagen
  (Kilometerstand, Leistung, Jahr), lineare Regression. R² liegt bei etwa 0.66.
* MAE (mittlerer absoluter Fehler): Mittelwert der Beträge der Residuen, in
  Euro und damit direkt verständlich: "Im Mittel liegen wir etwa 6000 Euro
  daneben."
* MSE (mittlerer quadratischer Fehler): die Fehlerquadratsumme aus Kapitel 7.1,
  geteilt durch die Anzahl der Datenpunkte. Große Fehler zählen besonders
  stark, die Einheit Euro² ist aber schwer zu deuten.
* RMSE: Wurzel aus dem MSE, wieder in Euro, im Beispiel etwa 9700 Euro. Liegt
  der RMSE deutlich über dem MAE, gibt es einzelne grobe Fehlprognosen.
* Code: `mean_absolute_error()` und `mean_squared_error()` aus
  `sklearn.metrics`, RMSE mit `np.sqrt()`.
* Welches Gütemaß wann? R² zum Einordnen und Vergleichen, MAE zum Kommunizieren,
  RMSE wenn große Abweichungen besonders teuer sind, etwa bei Toleranzen.
* Hinweis für die Gittersuche: `scoring='neg_mean_absolute_error'`.
  Scikit-Learn maximiert immer, deshalb steht der Fehler mit negativem
  Vorzeichen.
* Mini-Übung: Zugfestigkeit mit `3ddruck_gittersuche.csv` vorhersagen, R², MAE
  und RMSE berechnen und in MPa deuten.

## Zusammenfassung und Ausblick

* Die Accuracy täuscht bei unausgewogenen Klassen. Die Konfusionsmatrix zeigt,
  welche Fehler ein Modell macht.
* Precision, Recall und F1-Score beantworten unterschiedliche Fragen. Die Wahl
  hängt davon ab, welcher Fehler teurer ist.
* Bei Regression ergänzen MAE und RMSE das R² um die Größe der Fehler in der
  Einheit der Zielgröße.
* Ausblick auf Kapitel 11 (Neuronale Netze): Die Gütemaße aus diesem Kapitel
  gelten für jedes Modell, auch für neuronale Netze.
