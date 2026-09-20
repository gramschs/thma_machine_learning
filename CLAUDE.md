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
  und bereinigt sie. Die Originale außerhalb von `notebooks/` bleiben
  unangetastet, nur die Kopien in `notebooks/` bekommen Lücken.
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
- Lösung ergibt sich aus den unveränderten Originaldateien außerhalb von
  `notebooks/`.
