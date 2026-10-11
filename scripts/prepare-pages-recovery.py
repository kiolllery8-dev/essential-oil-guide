"""Download a verified successful Pages artifact for a non-deploying rehearsal."""
import argparse
import hashlib
import json
import re
import subprocess
import tarfile
from pathlib import Path

REPO = 'kiolllery8-dev/essential-oil-guide'


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', 'repos/' + REPO + '/' + path], text=True))


def extract(archive, destination):
    destination.mkdir(exist_ok=False)
    with tarfile.open(archive) as tar:
        members = tar.getmembers()
        if sum(member.size for member in members) > 2 * 1024 ** 3:
            raise ValueError('Artifact exceeds rehearsal limit')
        for member in members:
            target = (destination / member.name).resolve()
            if not target.is_relative_to(destination.resolve()) or ':' in member.name:
                raise ValueError('Unsafe artifact path')
            if not (member.isfile() or member.isdir()):
                raise ValueError('Artifact links and special files are forbidden')
        tar.extractall(destination, filter='data')


def draft_backup(release_id, run, run_id, download):
    release = api('releases/' + release_id)
    if release.get('draft') is not True or release.get('tag_name') != 'maintenance-backup-' + run_id:
        raise ValueError('Backup must remain an unpublished draft for the exact source run')
    for name in ('artifact.tar', 'provenance.json'):
        matches = [asset for asset in release['assets'] if asset['name'] == name]
        if len(matches) != 1:
            raise ValueError('Exactly one backup asset is required: ' + name)
        with (download / name).open('wb') as output:
            subprocess.run(['gh', 'api', 'repos/' + REPO + '/releases/assets/' + str(matches[0]['id']),
                            '-H', 'Accept: application/octet-stream'], stdout=output, check=True)
    provenance = json.loads((download / 'provenance.json').read_text())
    archive = download / 'artifact.tar'
    if (provenance.get('schemaVersion') != 1 or provenance.get('sourceRunId') != run_id or
            provenance.get('sourceSha') != run['head_sha'] or
            provenance.get('artifactSha256') != hashlib.sha256(archive.read_bytes()).hexdigest()):
        raise ValueError('Backup provenance or archive checksum mismatch')
    return archive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--expected-master', required=True)
    parser.add_argument('--backup-release-id', default='')
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9]+', args.run_id) or not re.fullmatch(r'[0-9a-f]{40}', args.expected_master):
        raise ValueError('Exact numeric run ID and master SHA are required')
    if args.backup_release_id and not re.fullmatch(r'[0-9]+', args.backup_release_id):
        raise ValueError('Backup release ID must be numeric')
    head = api('git/ref/heads/master')['object']['sha']
    if head != args.expected_master:
        raise ValueError('Master changed; abort rehearsal and revalidate')
    run = api('actions/runs/' + args.run_id)
    if run['conclusion'] != 'success' or run['head_branch'] != 'master' or run['path'] != '.github/workflows/deploy.yml':
        raise ValueError('Recovery source must be a successful master Pages workflow')
    artifacts = api('actions/runs/' + args.run_id + '/artifacts')['artifacts']
    candidates = [artifact for artifact in artifacts if artifact['name'] == 'github-pages' and not artifact['expired']]
    download = Path('recovery-download')
    download.mkdir(exist_ok=False)
    if len(candidates) == 1:
        subprocess.run(['gh', 'run', 'download', args.run_id, '--repo', REPO,
                        '--name', 'github-pages', '--dir', str(download)], check=True)
        archive = download / 'artifact.tar'
        source = {'artifactId': candidates[0]['id']}
    elif not candidates and args.backup_release_id:
        archive = draft_backup(args.backup_release_id, run, args.run_id, download)
        source = {'draftBackupReleaseId': args.backup_release_id}
    else:
        raise ValueError('Exactly one retained Pages artifact or explicit verified draft backup is required')
    extract(archive, Path('out'))
    report = {'scope': 'github-actions-artifact-recovery-rehearsal',
              'productionDeploymentPerformed': False, 'sourceRunId': args.run_id,
              'sourceSha': run['head_sha'], 'expectedMaster': head,
              **source,
              'artifactSha256': hashlib.sha256(archive.read_bytes()).hexdigest()}
    Path('recovery-rehearsal.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
