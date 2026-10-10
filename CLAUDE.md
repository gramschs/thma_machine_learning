# Schreibstil-Anweisungen für Vorlesungsskripte

## Kontext

Dieses Projekt enthält das Vorlesungsmaterial für das Modul **Maschinelles
Lernen Maschinenbau** an der Technischen Hochschule Mannheim (Prof. Dr. Simone
Gramsch) für Studierende des Bachelor-Studiengangs Maschinenbau. Das Material
wird mit **MyST Markdown** erstellt und ist für **Jupyter Book** konzipiert.

## Format

- Jupyter Book 2 Format = Myst Markdown mit `{code-cell}` und
  `{admonition}`-Blöcken
- Sprache: Deutsch

## Struktur eines Kapitels

- Kurze **Motivation** am Anfang: startet mit einem **Maschinenbau-Problem**
  (Qualitätskontrolle, Kennfeld/Surrogat, Predictive Maintenance), dann
  Anknüpfung an Bekanntes ("Bisher haben wir… Heute…")
- **Lernziele** als Checkliste mit Checkboxen, direkt nach der Motivation mit
  der H2-Überschrift Lernziele
- möglichst **drei Unterabschnitte** (H2-Überschriften), roter Faden je
  Unterabschnitt: **Kernbeispiel** (Code) → Erklärung & Verallgemeinerung →
  **Mini-Übung** → Lösung (Dropdown)
- Kurze **Zusammenfassung** am Ende mit explizitem Ausblick auf das nächste
  Kapitel

## Sprache

- In den **Lernzielen**: "Sie können…", "Sie wissen…" (handlungsorientiert)
- Im **restlichen Text**: "Wir" (kein "man", kein "Sie")
- Kurze, klare Sätze
- Keine Gedankenstriche
- Fachbegriffe werden beim ersten Auftreten **fett** markiert und sofort erklärt
- Kein Lehrbuch-Jargon, sondern pragmatische Erklärungen

## MyST-Formatkonventionen

### Dateianfang

Dateien beginnen immer mit dem YAML-Header:

```yaml
---
kernelspec:
  name: python3
  display_name: 'Python 3'
---
```

## Code-Along-Lücken in Notebooks

- `build_notebooks.sh` kopiert `chapterNN/*.md` nach `notebooks/chapterNN/*.md`
  und bereinigt sie. Nur die Kopien in `notebooks/` bekommen Lücken. In den
  Originalen ergänzt das Skript lediglich im YAML-Header den Download-Eintrag
  `../notebooks/chapterNN/name.ipynb` (über `add_notebook_download.py`, nur
  falls er fehlt).
- Nur `sec01`-`sec03` sind ca. 30-minütige Code-Along-Notebooks und bekommen
  Lücken. `sec04` ist ein Übungs-Notebook fürs Selbststudium (Hausaufgabe) und
  bleibt unverändert. Lücken nur im Hauptteil (vor "## Mini-Übungen"), nie in
  den Mini-Übungen selbst.
- Markierung: `# TODO: ???` ersetzt entfernten Code. Bei Teilzeilen bleibt die
  linke Seite stehen, z.B. `A = # TODO: ???`. Bei mehrzeiligen Blöcken
  (z.B. Matrixzeilen) ein `# TODO: ???` pro Zeile mit kurzem Hinweis, welcher
  Schritt gemeint ist.
- Richtwert 3-5 Lücken pro Notebook. Feine Granularität (pro Zeile) nur beim
  zentralen Lernkonzept der Einheit, sonst grob bzw. einzeilig. Rein
  mechanische Schritte (gegebene Werte, Prints, Unpacking) bleiben ausgefüllt.
- Lücken nur in Code, den der Text unmittelbar davor erklärt. Wer den Absatz
  gelesen hat, muss die Lücke füllen können. Die nötige Syntax (Funktionsname,
  Argument, Klammerschreibweise) muss im Fließtext vor der Zelle stehen oder
  aus früheren Kapiteln bekannt sein. Lernziele zählen nicht, weil der
  Konverter sie entfernt. Fehlt die Syntax im Text, sie im Original
  `chapterNN/*.md` und von Hand in der Kopie `notebooks/chapterNN/*.md`
  ergänzen (ein Neubau würde die Lücken löschen).
- Pro H2-Abschnitt die ein bis zwei Zeilen wählen, die das neue Konzept tragen
  (erstmals eingeführte Methode oder Syntax, z.B. `pd.Series(...)`, `.loc[]`,
  `.describe()`). Lücken über alle H2-Abschnitte verteilen.
- Wiederholungen eines gerade geübten Musters bleiben ausgefüllt (z.B. zweiter
  Filter nach dem ersten, `.loc`-Slicing wenn `.iloc`-Slicing schon Lücke ist),
  ebenso Importe und gegebene Daten.
- Ist ein Stolperstein Thema des Abschnitts, die Stelle bewusst zur Lücke
  machen, damit die Studierenden ihn selbst erleben (z.B. `.iloc[0:4]` wegen
  der exklusiven Obergrenze).
- Hinweis in Klammern beschreibt die Aufgabe in Worten, ganz ohne Syntax:
  keine Funktions- oder Methodennamen, keine Operatoren, keine Index- oder
  Argumentschreibweise, auch keine Begriffe, die das Werkzeug verraten (z.B.
  "per Slicing"). Inhaltliche Angaben wie Spalten-, Datei- und Zeilennamen
  oder Zahlenwerte bleiben stehen, z.B. `(Zeile von BMW Nr. 1 auswählen)`.
- Bei einer Teillücke in einem mehrzeiligen Funktionsaufruf die ganze Zeile
  durch `# TODO: ???` ersetzen und die schließende Klammer in eine eigene Zeile
  setzen.
- Lösung ergibt sich aus den unveränderten Originaldateien außerhalb von
  `notebooks/`.
