"""Write a small public version marker after build and both original guards."""
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

NAME = 'deployment-version.json'


def write_marker(output, sha, run_id, attempt):
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('Exact source SHA required')
    if any(not re.fullmatch(r'[1-9][0-9]*', value) for value in (run_id, attempt)):
        raise ValueError('Exact positive run ID and attempt required')
    output = Path(output)
    if not output.is_dir() or not (output/'index.html').is_file():
        raise ValueError('A complete static export is required')
    marker = output/NAME
    if marker.exists() or marker.is_symlink():
        raise ValueError('Never overwrite an existing exported route or marker')
    rows = []
    for path in sorted(output.rglob('*'), key=lambda item: item.relative_to(output).as_posix()):
        if path.is_symlink():
            raise ValueError('Export must not contain symlinks')
        if path.is_file():
            rows.append([path.relative_to(output).as_posix(),
                         hashlib.sha256(path.read_bytes()).hexdigest()])
    digest = hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    value = {'schemaVersion': 1, 'sourceSha': sha, 'runId': run_id,
             'runAttempt': attempt, 'exportDigest': digest, 'fileCount': len(rows)}
    # Exclusive creation; the marker identifies the export, never rewrites pages.
    with marker.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n')
    return value


if __name__ == '__main__':
    sha = os.environ['GITHUB_SHA']
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'],text=True).strip()
    if head != sha:
        raise ValueError('Checkout differs from the claimed source SHA')
    print(json.dumps(write_marker('out', sha, os.environ['GITHUB_RUN_ID'],
                                 os.environ['GITHUB_RUN_ATTEMPT']), indent=2))
