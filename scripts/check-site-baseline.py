"""Check every existing route's SEO fields and protected knowledge files.

Run after npm run build. --capture is only for the initial approved baseline;
normal CI must never recapture it automatically.
"""
import argparse
import hashlib
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / 'data' / 'maintenance-baseline.json'
PROTECTED = ['scripts/build_numerology_page.py', 'data/oils.json',
             'html-source/numerology.html', 'html-source/safety.html']

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.fields = {'title': '', 'description': '', 'canonical': '', 'robots': ''}
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title': self.in_title = True
        if tag == 'meta' and a.get('name') in ('description', 'robots'):
            self.fields[a['name']] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.fields['canonical'] = a.get('href', '')
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.fields['title'] += data

def snapshot(out):
    routes = {}
    for f in sorted(out.rglob('index.html')):
        rel = f.relative_to(out).as_posix()
        if rel.startswith(('_next/', '_not-found/')): continue
        url = '/' if rel == 'index.html' else '/' + rel[:-len('index.html')]
        p = Metadata(); p.feed(f.read_text(encoding='utf-8'))
        routes[url] = p.fields
    if not routes: raise ValueError('No exported pages; run npm run build first')
    return {'schemaVersion': 1, 'routes': routes, 'protectedFiles': {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in PROTECTED}}

def differences(expected, actual):
    errors = []
    for url, fields in expected['routes'].items():
        if url not in actual['routes']:
            errors.append(f'Missing protected route: {url}'); continue
        for k, v in fields.items():
            if actual['routes'][url][k] != v:
                errors.append(f'Protected {k} changed: {url}')
    for name, digest in expected['protectedFiles'].items():
        if actual['protectedFiles'].get(name) != digest:
            errors.append(f'Protected knowledge/algorithm changed: {name}')
    for url, fields in actual['routes'].items():
        if not fields['title'] or not fields['description'] or not fields['canonical']:
            errors.append(f'Missing required metadata: {url}')
    return errors

def main():
    a = argparse.ArgumentParser(); a.add_argument('--capture', action='store_true')
    a.add_argument('--out', type=Path, default=ROOT / 'out'); args = a.parse_args()
    actual = snapshot(args.out)
    if args.capture:
        if BASELINE.exists(): raise ValueError('Baseline already exists; refusing overwrite')
        BASELINE.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Captured {len(actual["routes"])} existing routes'); return
    expected = json.loads(BASELINE.read_text(encoding='utf-8'))
    errors = differences(expected, actual)
    for e in errors: print(e, file=sys.stderr)
    if errors: sys.exit(1)
    print(f'PASS: {len(expected["routes"])} protected routes; '
          f'{len(actual["routes"])} exported routes; protected knowledge unchanged')

if __name__ == '__main__': main()
