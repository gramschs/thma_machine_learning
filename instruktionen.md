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

Jedes Kapitel entspricht einer Vorlesungswoche (Montag + Dienstag im Studio-Format) und besteht aus **fünf Sektionen**. Jede Sektion x.1-x.4 ist Drehbuch für einen 45-min-Zyklus (Input → Notebook-Arbeit → Plenum) und zugleich vollständige Buchseite für Selbstlerner.

### Zuordnung der Sektionen

| Sektion | Session | Rolle |
| --- | --- | --- |
| x.1, x.2 | Montag | Neues Thema, stark gescaffoldet |
| x.3 | Dienstag, Zyklus 1 | Vertiefung, weniger Vorgaben |
| x.4 | Dienstag, Zyklus 2 | Challenge (Transfer, offene Aufgabe, Wochenabgabe) |
| x.5 | Selbststudium | Übungen und Training (Auto-Datensatz) |

### Struktur der Sektionen x.1-x.3

- Kurze **Motivation** am Anfang: startet mit einem **Maschinenbau-Problem**
  (Qualitätskontrolle, Kennfeld/Surrogat, Predictive Maintenance), dann
  Anknüpfung an Bekanntes ("Bisher haben wir… Heute…")
- **Lernziele** als Checkliste mit Checkboxen, direkt nach der Motivation mit
  der H2-Überschrift Lernziele; werden im Plenum am Zyklusende abgehakt
- **Drei Unterabschnitte** (H2-Überschriften), roter Faden je Unterabschnitt:
  **Kernbeispiel** (Code) → Erklärung & Verallgemeinerung → **Mini-Übung** →
  Lösung (Dropdown)
  - Das Kernbeispiel ist die Live-Coding-Vorlage (ca. 5 min pro Unterabschnitt,
    Input gesamt 15-20 min)
  - Der Erklärtext wird **nicht vorgetragen**; er dient dem Nachlesen und den
    Selbstlernern
  - Mathematik nur "on demand" im Erklärtext, mit Anknüpfung an Bekanntes
    (Messtechnik, Schwingungslehre)
- Nach dem dritten Unterabschnitt eine **Kombinationsaufgabe**, die alle drei
  Unterabschnitte verbindet (Puffer für schnelle Paare)
- Die drei Mini-Übungen + Kombinationsaufgabe bilden die Arbeitsphase des Zyklus
  (20-25 min); sie werden als **Lücken-Notebook** für Moodle extrahiert
- **Keine separaten Übungsaufgaben** am Sektionsende (wandern nach x.5)
- Kurze **Zusammenfassung** am Ende mit explizitem Ausblick auf die nächste
  Sektion (Überleitung zum nächsten Zyklus)

### Struktur der Sektion x.4 (Challenge)

Bewusster Strukturbruch - kein Dreier-Aufbau, kein neuer Input:

- **Szenario** mit Ingenieur-Entscheidungsfrage (z. B. "Welche Maschine bekommt
  den Serienauftrag?")
- **Aufgabenstellung** mit klaren Deliverables (Kennzahlen, Plot, begründete
  Empfehlung in Markdown-Zelle) und Vorlagen (z. B. Vergleichstabelle)
- **Datensatz-Links**; in der Session Varianten A/B für Informationsasymmetrie
  (nur Moodle), im Buch eine eigene Variante C für Selbstlerner
- Optionale **Zusatzaufgabe** für schnelle Paare
- Musterlösung wird erst nach der Session ins Repository gepusht
- Das Arbeitsnotebook dieser Sektion ist die **Wochenabgabe** (Paar, Di 23:59,
  bestanden/nicht bestanden)

### Struktur der Sektion x.5 (Selbststudium)

- **Übungsaufgaben** (alphabetisch nummeriert) mit Dropdown-Lösungen, basierend
  auf dem **Autoscout24-Datensatz** (bzw. dem bisherigen Übungsmaterial)
- Rahmung als **Transfer auf eine fachfremde Domäne** ("die Werkzeuge
  funktionieren für jede Tabelle")
- In den Wochen vor einer Projektabgabe: expliziter Hinweis, welche
  Arbeitsschritte das Kriterienraster der Abgabe erwartet

### Durchgehende Konventionen

- Ein Moodle-Notebook pro Session: Mo-Notebook (x.1 + x.2), Di-Notebook (x.3 +
  x.4 = Abgabedatei)
- Zwei bis drei durchgehende Maschinenbau-Erzähllinien über das Semester statt
  wöchentlich neuer Beispiele; frühe Kapitel nutzen synthetische, kontrollierte
  Datensätze, echte Datensätze ab dem Modellblock
- Notation, Datensätze und Rituale (Lernziele-Check, Leaderboard-Einträge)
  konsistent über alle Kapitel

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
