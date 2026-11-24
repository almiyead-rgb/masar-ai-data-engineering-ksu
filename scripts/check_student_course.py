"""Validate learner resources without presenting source checks as engine evidence."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import os
import re
import sys

import nbformat
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.sources import verify_manifest

LAB_DAYS = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5}
IGNORED_DIRECTORIES = {
    '.git', '.venv', 'venv', '__pycache__', 'node_modules', 'dist',
    'outputs', 'evidence', '.pytest_cache', '.mypy_cache',
}


def learner_documents(root):
    """Prune dependencies and generated artifacts before descending into them."""
    for current, directories, filenames in os.walk(root, followlinks=False):
        directories[:] = sorted(
            name for name in directories
            if name not in IGNORED_DIRECTORIES
            and not (Path(current) / name).is_symlink()
        )
        for name in sorted(filenames):
            path = Path(current) / name
            if path.suffix in {'.md', '.ipynb'} and not path.is_symlink():
                yield path


def inspect(root=ROOT):
    root = Path(root).resolve()
    errors, links, tables, documents = [], 0, 0, 0
    try:
        verify_manifest(root / 'data/masar-small-v1')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append('Dataset integrity: ' + str(exc))
    for day in range(1, 6):
        for filename in ('README.md', 'CONCEPTS.md', 'GLOSSARY.md', 'PRACTICE.md',
                         'COMPLETION.md', 'SOURCES.md', 'STUDENT.ipynb'):
            if not (root / f'day{day:02}' / filename).is_file():
                errors.append(f'Missing Day {day} resource: {filename}')
    for lab, day in LAB_DAYS.items():
        for name in ('README.md', 'WALKTHROUGH.md'):
            if not (root / f'day{day:02}/labs/lab{lab:02}' / name).is_file():
                errors.append(f'Missing Lab {lab} resource: {name}')
    for path in learner_documents(root):
        documents += 1
        relative = path.relative_to(root)
        try:
            if path.suffix == '.ipynb':
                nb = nbformat.read(path, as_version=4)
                nbformat.validate(nb)
                texts = [c.source for c in nb.cells if c.cell_type == 'markdown']
                for cell in nb.cells:
                    if cell.cell_type == 'code':
                        try:
                            compile(cell.source, str(path), 'exec')
                        except SyntaxError as exc:
                            errors.append(f'{relative}: invalid code: {exc}')
            else:
                texts = [path.read_text(encoding='utf-8')]
        except (OSError, ValueError, nbformat.ValidationError) as exc:
            errors.append(f'{relative}: invalid document: {exc}')
            continue
        for text in texts:
            targets = re.findall(r'href=["\']([^"\']+)["\']', text)
            targets += re.findall(r'\]\(([^)]+)\)', text)
            for target in targets:
                # Markdown permits <path> and an optional quoted link title.
                target = re.split(r'\s+["\']', target, maxsplit=1)[0].strip('<> ')
                try:
                    url = urlsplit(target)
                except ValueError:
                    errors.append(f'{relative}: invalid link {target}')
                    continue
                if url.scheme or url.netloc or not url.path:
                    continue
                links += 1
                resolved = (path.parent / unquote(url.path)).resolve()
                if not resolved.is_relative_to(root) or not resolved.exists():
                    errors.append(f'{relative}: missing link {target}')
            soup = BeautifulSoup(text, 'html.parser')
            for table in soup.find_all('table'):
                cells = table.find_all('td')
                if len(cells) == 2 and all(c.get('lang') for c in cells):
                    tables += 1
                    if [c.get('lang') for c in cells] != ['en', 'ar'] or [c.get('dir') for c in cells] != ['ltr', 'rtl']:
                        errors.append(f'{relative}: reversed language columns')
            if relative.parts[0] in {f'day{n:02}' for n in range(1, 6)}:
                if soup.find(attrs={'lang': 'ar'}):
                    errors.append(f'{relative}: learner instructions must be in English')
                words = soup.get_text(' ', strip=True)
                if re.search(r'ENGINE_NOT_EXECUTED|\bPARTIAL\b|authoring session|current authored build', words):
                    errors.append(f'{relative}: obsolete authoring commentary')
    return {
        'scope': 'FIVE_DAY_LEARNER_LAYOUT', 'days': 5, 'labs': 8,
        'documents_checked': documents, 'internal_links': links,
        'bilingual_tables': tables, 'errors': errors,
        'status': 'PASSED' if not errors else 'FAILED',
        'engine_execution_claim': False,
    }


if __name__ == '__main__':
    result = inspect()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status'] == 'PASSED' else 1)
