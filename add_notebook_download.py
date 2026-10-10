#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import sys
from pathlib import Path

DOWNLOADS_RE = re.compile(r'^downloads:\s*$')


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Ergänzt im YAML-Header einer MyST-Markdown-Datei '
                    'chapterNN/name.md einen Download-Eintrag für das '
                    'Notebook ../notebooks/chapterNN/name.ipynb. Ist der '
                    'Eintrag schon vorhanden, bleibt die Datei unverändert.')
    parser.add_argument('filename', type=str)

    if len(sys.argv) == 1:
        print('Bitte eine Datei angeben: add_notebook_download.py chapterNN/name.md')
        sys.exit(1)

    return parser.parse_args()


def find_header_end(lines):
    if not lines or lines[0].strip() != '---':
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == '---':
            return index
    return None


def add_notebook_download(filename):
    path = Path(filename)
    notebook = f'../notebooks/{path.parent.name}/{path.stem}.ipynb'
    entry = [f'  - file: {notebook}\n',
             f'    title: {path.stem}.ipynb\n']

    with open(filename) as file:
        lines = file.readlines()

    end = find_header_end(lines)
    if end is None:
        print(f'warning {filename}: kein YAML-Header, Download-Eintrag fehlt')
        return

    if any(line.strip() == f'- file: {notebook}' for line in lines[1:end]):
        return  # Eintrag schon vorhanden

    downloads = None
    for index in range(1, end):
        if DOWNLOADS_RE.match(lines[index]):
            downloads = index
            break

    if downloads is None:
        lines[end:end] = ['downloads:\n'] + entry
    elif lines[downloads + 1].startswith('  - '):
        lines[downloads + 1:downloads + 1] = entry
    else:
        print(f'warning {filename}: downloads ist keine Liste der Form '
              f'"  - file: ...", Download-Eintrag fehlt')
        return

    with open(filename, 'w') as file:
        file.writelines(lines)
    print(f'Download-Eintrag ergänzt: {filename}')


def main():
    args = parse_command_line_arguments()
    add_notebook_download(args.filename)


if __name__ == "__main__":
    main()
