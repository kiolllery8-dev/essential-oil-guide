import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


recovery = load('recovery', 'prepare-pages-recovery.py')
writer = load('writer', 'write-deployment-version.py')
SHA = 'a' * 40


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        (self.out / 'index.html').write_bytes(b'original')
        writer.write_marker(self.out, SHA, '123', '1')
        self.run = dict(id=123, run_attempt=2, head_sha=SHA)
        names = ['Build Next.js (static export)', 'Preserve the existing numerology SEO fields',
                 'Protect every existing page and knowledge algorithms',
                 'Bind public version marker to the guarded export', 'Upload artifact']
        self.job = dict(name='build', run_id=123, run_attempt=1, head_sha=SHA,
                        status='completed', conclusion='success',
                        started_at='2026-10-18T02:00:00Z', completed_at='2026-10-18T02:01:00Z',
                        steps=[dict(name=n, conclusion='success') for n in names])
        self.artifact = dict(created_at='2026-10-18T02:00:55Z',
                             workflow_run=dict(id=123, head_sha=SHA, head_branch='master'))

    def check(self, **changes):
        job = copy.deepcopy(self.job); job.update(changes)
        with patch.object(recovery, 'api', return_value=dict(total_count=1, jobs=[job])) as api:
            value = recovery.original_build_attempt(self.out, self.run, self.artifact)
            api.assert_called_once_with('actions/runs/123/attempts/1/jobs?per_page=100')
            return value

    def test_partial_rerun_uses_successful_original_build(self):
        self.assertEqual(self.check(), '1')

    def test_wrong_identity_or_unsuccessful_build_rejected(self):
        for change in [dict(run_attempt=2), dict(run_id=124), dict(head_sha='b'*40),
                       dict(status='in_progress'), dict(conclusion='failure'), dict(steps=[])]:
            with self.subTest(change=change), self.assertRaises(ValueError): self.check(**change)

    def test_artifact_from_other_build_window_rejected(self):
        self.artifact['created_at'] = '2026-10-18T02:02:00Z'
        with self.assertRaises(ValueError): self.check()

    def test_wrong_artifact_source_rejected(self):
        self.artifact['workflow_run']['head_sha'] = 'b'*40
        with self.assertRaises(ValueError): self.check()

    def test_modified_export_rejected_before_api(self):
        (self.out / 'index.html').write_bytes(b'changed')
        with patch.object(recovery, 'api') as api, self.assertRaises(ValueError):
            recovery.original_build_attempt(self.out, self.run, self.artifact)
        api.assert_not_called()

    def test_future_attempt_rejected(self):
        self.run['run_attempt'] = 0
        with self.assertRaises(ValueError): self.check()

    def test_marked_draft_without_timing_evidence_rejected(self):
        with self.assertRaises(ValueError): recovery.original_build_attempt(self.out, self.run, None)

    def test_legacy_no_marker_remains_rehearsal_only(self):
        (self.out / 'deployment-version.json').unlink()
        self.assertEqual(recovery.original_build_attempt(self.out, self.run, None), '2')


if __name__ == '__main__':
    unittest.main()
