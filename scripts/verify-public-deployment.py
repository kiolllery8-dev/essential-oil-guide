"""Compare a guarded export with the public marker and every exported HTML page.

HTTP bytes only: this never executes page scripts, analytics or chat widgets.
Differences fail closed; CDN rewriting is reported, never silently normalized.
"""
import argparse
import concurrent.futures
import hashlib
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import quote

SITE = 'https://intelliverse.tw'
MARKER = 'deployment-version.json'


class RejectRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Public verification refuses redirects')


def fetch(path, run_id, attempt, limit):
    # Callers pass only artifact-derived relative paths; no arbitrary host input.
    if path.startswith('/') or '..' in Path(path).parts or '\\' in path:
        raise ValueError('Unsafe public path')
    url = SITE + '/' + quote(path, safe='/') + '?deployment-check=' + run_id + '-' + attempt
    request = urllib.request.Request(url, headers={
        'User-Agent': 'IntelliverseDeploymentVerification/1.0',
        'Cache-Control': 'no-cache', 'Accept-Encoding': 'identity'})
    with urllib.request.build_opener(RejectRedirect()).open(request, timeout=25) as response:
        if response.status != 200 or response.geturl() != url:
            raise ValueError('Unexpected status or response URL')
        if response.headers.get('Content-Encoding', 'identity') != 'identity':
            raise ValueError('Expected uncompressed response bytes')
        data = response.read(limit + 1)
        if len(data) > limit: raise ValueError('Public response exceeds limit')
        return data


def inspect_export(output, sha, run_id, attempt):
    if not re.fullmatch('[0-9a-f]{40}', sha) or any(
            not re.fullmatch('[1-9][0-9]*', value) for value in (run_id, attempt)):
        raise ValueError('Exact source SHA, run ID and attempt required')
    output = Path(output)
    rows = []; pages = []
    for path in sorted(output.rglob('*'), key=lambda p: p.relative_to(output).as_posix()):
        if path.is_symlink(): raise ValueError('Artifact links are forbidden')
        if not path.is_file(): continue
        name = path.relative_to(output).as_posix()
        if name == MARKER: continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append([name, digest])
        if name.endswith('.html'):
            public_path = name[:-10] if name == 'index.html' or name.endswith('/index.html') else name
            pages.append((public_path, digest))
    digest = hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    expected = {'schemaVersion': 1, 'sourceSha': sha, 'runId': run_id,
                'runAttempt': attempt, 'exportDigest': digest, 'fileCount': len(rows)}
    if not (output/'index.html').is_file() or not pages:
        raise ValueError('Export has no homepage')
    if json.loads((output/MARKER).read_text(encoding='utf-8')) != expected:
        raise ValueError('Artifact marker differs from exact identity or export digest')
    return expected, pages


def verify(output, sha, run_id, attempt, get=fetch):
    marker, pages = inspect_export(output, sha, run_id, attempt)
    public_marker = json.loads(get(MARKER, run_id, attempt, 4096))
    if public_marker != marker:
        raise ValueError('Public marker is stale or does not match the artifact')
    def check(item):
        path, digest = item
        try:
            body = get(path, run_id, attempt, 4_000_000)
            if hashlib.sha256(body).hexdigest() != digest:
                return {'path': '/' + path, 'error': 'HTML bytes differ from guarded artifact'}
        except Exception as error:
            return {'path': '/' + path, 'error': type(error).__name__}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        errors = [result for result in pool.map(check, pages) if result]
    # Recheck marker after all pages; a changed version invalidates the scan.
    if json.loads(get(MARKER, run_id, attempt, 4096)) != marker:
        errors.append({'path': '/' + MARKER, 'error': 'Public version changed during verification'})
    return {'scope': 'public-marker-and-all-exported-html-bytes', 'sourceSha': sha,
            'runId': run_id, 'runAttempt': attempt, 'checkedPages': len(pages),
            'passed': not errors, 'errors': errors, 'browserUiVerified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--expected-source-sha', required=True)
    parser.add_argument('--expected-run-id', required=True)
    parser.add_argument('--expected-run-attempt', required=True)
    parser.add_argument('--report', type=Path, default=Path('public-verification.json'))
    args = parser.parse_args()
    try:
        report = verify(args.out, args.expected_source_sha, args.expected_run_id, args.expected_run_attempt)
    except Exception as error:
        report = {'passed': False, 'scope': 'public-marker-and-all-exported-html-bytes',
                  'error': type(error).__name__ + ': ' + str(error), 'browserUiVerified': False}
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    if not report['passed']: raise SystemExit(1)
