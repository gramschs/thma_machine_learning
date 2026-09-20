#!/usr/bin/env bash
# Baut Jupyter-Notebooks für Studierende aus dem MyST-Markdown-Quellcode eines
# Kapitels.
#
# Aufruf: ./build_notebooks.sh chapter01
#
# Kopiert chapterNN/*.md nach notebooks/chapterNN, bereinigt die Kopien mit
# convert_myst_to_notebook.py (entfernt Lernziele und Lösungen, wandelt
# Übungs-/Aufgaben-Admonitions in einfache Überschriften um, sammelt
# Mini-Übungen am Ende) und kopiert die zugehörigen Bilder (pics/) und
# Datensätze (*.csv) mit. Die bereinigten .md-Dateien müssen noch von Hand um
# die Code-Along-Lücken ergänzt werden, bevor sie mit jupytext (--to ipynb,
# dann --set-formats ipynb) in .ipynb umgewandelt werden.

set -euo pipefail

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate python313

if [ $# -ne 1 ]; then
    echo "Aufruf: $0 <chapterNN>" >&2
    exit 1
fi

chapter="$1"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$script_dir/$chapter"
target_dir="$script_dir/notebooks/$chapter"

if [ ! -d "$source_dir" ]; then
    echo "Kein solches Kapitelverzeichnis: $source_dir" >&2
    exit 1
fi

mkdir -p "$target_dir"
cp "$source_dir"/*.md "$target_dir"/

if [ -d "$source_dir/pics" ]; then
    mkdir -p "$target_dir/pics"
    cp "$source_dir"/pics/* "$target_dir/pics/"
fi

# Datensätze, die die Kapitel direkt per pd.read_csv('name.csv') einlesen,
# liegen als lose Dateien im Kapitelverzeichnis (nicht im data/-Unterordner,
# der nur die Generator-Skripte enthält).
shopt -s nullglob
csv_files=("$source_dir"/*.csv)
shopt -u nullglob
if [ ${#csv_files[@]} -gt 0 ]; then
    cp "${csv_files[@]}" "$target_dir/"
fi

for md_file in "$target_dir"/*.md; do
    python3 "$script_dir/convert_myst_to_notebook.py" "$md_file"
done

echo "Bereinigtes Markdown liegt in $target_dir"
echo "Code-Along-Lücken von Hand ergänzen, dann ausführen:"
echo "  jupytext --to ipynb $target_dir/*.md"
echo "  jupytext --set-formats ipynb $target_dir/*.ipynb"
