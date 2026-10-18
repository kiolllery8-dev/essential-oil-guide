"""Download a verified successful Pages artifact for a non-deploying rehearsal."""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import tarfile
from datetime import datetime
from pathlib import Path

REPO = 'kiolllery8-dev/essential-oil-guide'


def original_build_attempt(output, run, artifact):
    """Bind a marked retained export to its successful original build attempt."""
    latest = str(run['run_attempt'])
    marker = Path(output) / 'deployment-version.json'
    if not marker.exists():
        # Legacy exports remain rehearsal-only; actual restore rejects no marker.
        return latest
    attempt = json.loads(marker.read_text(encoding='utf-8')).get('runAttempt', '')
    if not isinstance(attempt, str) or not re.fullmatch(r'[1-9][0-9]*', attempt) or int(attempt) > int(latest):
        raise ValueError('Invalid original build attempt')
    spec = importlib.util.spec_from_file_location('public_check', Path(__file__).with_name('verify-public-deployment.py'))
    verifier = importlib.util.module_from_spec(spec); spec.loader.exec_module(verifier)
    verifier.inspect_export(output, run['head_sha'], str(run['id']), attempt)
    if artifact is None:
        raise ValueError('Marked draft backups need original artifact timing provenance')
    response = api('actions/runs/' + str(run['id']) + '/attempts/' + attempt + '/jobs?per_page=100')
    jobs = response['jobs']
    if response['total_count'] > len(jobs):
        raise ValueError('Incomplete original build job evidence')
    builds = [job for job in jobs if job['name'] == 'build']
    if len(builds) != 1:
        raise ValueError('Exactly one original build is required')
    build = builds[0]
    required = ('Build Next.js (static export)', 'Preserve the existing numerology SEO fields',
                'Protect every existing page and knowledge algorithms',
                'Bind public version marker to the guarded export', 'Upload artifact')
    if (str(build['run_id']) != str(run['id']) or str(build['run_attempt']) != attempt or
            build['head_sha'] != run['head_sha'] or build['status'] != 'completed' or
            build['conclusion'] != 'success' or any(
                len([step for step in build['steps'] if step['name'] == name and
                     step['conclusion'] == 'success']) != 1 for name in required)):
        raise ValueError('Original build identity or required steps did not pass')
    created = datetime.fromisoformat(artifact['created_at'].replace('Z', '+00:00'))
    started = datetime.fromisoformat(build['started_at'].replace('Z', '+00:00'))
    completed = datetime.fromisoformat(build['completed_at'].replace('Z', '+00:00'))
    origin = artifact.get('workflow_run') or {}
    if (str(origin.get('id')) != str(run['id']) or origin.get('head_sha') != run['head_sha'] or
            origin.get('head_branch') != 'master' or not started <= created <= completed):
        raise ValueError('Artifact does not belong to the original build window')
    return attempt


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', 'repos/' + REPO + '/' + path], text=True))


def current_deployment(expected_master, expected_deployment, current_run_id=None):
    if not re.fullmatch(r'[0-9a-f]{40}', expected_master) or not re.fullmatch(r'[0-9]+', expected_deployment):
        raise ValueError('Exact master SHA and deployment ID are required')
    if api('git/ref/heads/master')['object']['sha'] != expected_master:
        raise ValueError('Master changed; abort recovery and revalidate')
    deployments = api('deployments?environment=github-pages&per_page=2')
    # An environment job creates its own in-progress deployment before steps run.
    # Exclude only the newest one, identified by this run's exact GitHub job URL,
    # SHA and GitHub Actions app. Never skip completed or foreign deployments.
    if deployments and current_run_id and re.fullmatch(r'[0-9]+', current_run_id):
        latest = deployments[0]
        latest_statuses = api('deployments/' + str(latest['id']) + '/statuses?per_page=1')
        status = latest_statuses[0] if latest_statuses else {}
        own_url = r'https://github\.com/' + re.escape(REPO) + r'/actions/runs/' + current_run_id + r'/job/[0-9]+'
        if (latest['sha'] == expected_master and
                (latest.get('performed_via_github_app') or {}).get('slug') == 'github-actions' and
                status.get('state') in ('queued', 'in_progress') and
                re.fullmatch(own_url, status.get('log_url', ''))):
            deployments = deployments[1:]
    if not deployments or str(deployments[0]['id']) != expected_deployment:
        raise ValueError('Later deployment exists; refuse to replace it')
    if deployments[0]['sha'] != expected_master:
        raise ValueError('Deployment does not match the expected master')
    statuses = api('deployments/' + expected_deployment + '/statuses?per_page=1')
    if not statuses or statuses[0]['state'] not in ('success', 'failure', 'error'):
        raise ValueError('Deployment is active or unconfirmed; refuse recovery')


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
    parser.add_argument('--expected-deployment-id', required=True)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9]+', args.run_id) or not re.fullmatch(r'[0-9a-f]{40}', args.expected_master):
        raise ValueError('Exact numeric run ID and master SHA are required')
    if args.backup_release_id and not re.fullmatch(r'[0-9]+', args.backup_release_id):
        raise ValueError('Backup release ID must be numeric')
    current_deployment(args.expected_master, args.expected_deployment_id, os.environ.get('GITHUB_RUN_ID'))
    if args.check_only:
        print('Current master and deployment snapshot still match'); return
    head = api('git/ref/heads/master')['object']['sha']
    if head != args.expected_master:
        raise ValueError('Master changed; abort rehearsal and revalidate')
    run = api('actions/runs/' + args.run_id)
    if run['conclusion'] != 'success' or run['head_branch'] != 'master' or run['path'] != '.github/workflows/deploy.yml':
        raise ValueError('Recovery source must be a successful master Pages workflow')
    if not re.fullmatch(r'[0-9a-f]{40}', run['head_sha']):
        raise ValueError('Invalid source commit')
    source_attempt = str(run.get('run_attempt', ''))
    if not re.fullmatch(r'[1-9][0-9]*', source_attempt):
        raise ValueError('Invalid source run attempt')
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
    source_attempt = original_build_attempt(Path('out'), run, candidates[0] if candidates else None)
    report = {'scope': 'github-actions-artifact-recovery-rehearsal',
              'productionDeploymentPerformed': False, 'sourceRunId': args.run_id,
              'sourceSha': run['head_sha'], 'expectedMaster': head,
              'sourceRunAttempt': source_attempt,
              'expectedDeploymentId': args.expected_deployment_id,
              **source,
              'artifactSha256': hashlib.sha256(archive.read_bytes()).hexdigest()}
    Path('recovery-rehearsal.json').write_text(json.dumps(report, indent=2) + '\n')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
            output.write('source_sha=' + run['head_sha'] + '\n')
            output.write('source_run_attempt=' + source_attempt + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
