import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


def module(name, filename):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(filename))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value

writer=module('writer','write-deployment-version.py')
reader=module('reader','verify-public-deployment.py')
SHA='a'*40


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.out=Path(self.temp.name)
        (self.out/'index.html').write_bytes(b'<h1>Home</h1>')
        (self.out/'hidden').mkdir()
        (self.out/'hidden/index.html').write_bytes(b'<meta name="robots" content="noindex"><h1>Hidden</h1>')
        writer.write_marker(self.out,SHA,'123','1')
        self.public={
            '':(self.out/'index.html').read_bytes(),
            'hidden/':(self.out/'hidden/index.html').read_bytes(),
            reader.MARKER:(self.out/reader.MARKER).read_bytes()}
        self.calls=[]
        def get(path,*args): self.calls.append(path);return self.public[path]
        self.get=get

    def verify(self): return reader.verify(self.out,SHA,'123','1',self.get)

    def test_checks_home_and_noindex_then_rechecks_marker(self):
        result=self.verify()
        self.assertTrue(result['passed']);self.assertEqual(result['checkedPages'],2)
        self.assertIn('hidden/',self.calls)
        self.assertEqual(self.calls.count(reader.MARKER),2)
        self.assertIs(result['browserUiVerified'],False)

    def test_stale_public_marker_rejected_before_pages(self):
        changed=json.loads(self.public[reader.MARKER]);changed['runId']='122'
        self.public[reader.MARKER]=json.dumps(changed).encode()
        with self.assertRaises(ValueError): self.verify()
        self.assertEqual(self.calls,[reader.MARKER])

    def test_changed_noindex_html_is_not_ignored(self):
        self.public['hidden/']=b'Changed'
        result=self.verify()
        self.assertFalse(result['passed']);self.assertEqual(result['errors'][0]['path'],'/hidden/')

    def test_artifact_tampering_rejected_before_network(self):
        (self.out/'index.html').write_bytes(b'Tampered')
        with self.assertRaises(ValueError): self.verify()
        self.assertEqual(self.calls,[])

    def test_changed_version_during_scan_fails(self):
        count=0
        def get(path,*args):
            nonlocal count
            if path==reader.MARKER:
                count+=1
                if count==2: return b'{}'
            return self.public[path]
        self.get=get
        self.assertFalse(self.verify()['passed'])

    def test_page_network_error_kept(self):
        def get(path,*args):
            if path=='hidden/': raise TimeoutError()
            return self.public[path]
        self.get=get
        self.assertFalse(self.verify()['passed'])

    def test_wrong_expected_identity_and_legacy_artifact_fail(self):
        with self.assertRaises(ValueError): reader.inspect_export(self.out,SHA,'124','1')
        (self.out/reader.MARKER).unlink()
        with self.assertRaises(FileNotFoundError): self.verify()

    def test_redirect_refused_before_following(self):
        with self.assertRaises(ValueError): reader.RejectRedirect().redirect_request(None)

    def test_direct_html_and_verification_files_are_checked(self):
        (self.out/reader.MARKER).unlink()
        for name in ('atlas.html','oil-detail.html','google-test.html','404.html'):
            (self.out/name).write_bytes(b'Legacy or verification HTML')
            self.public[name]=(self.out/name).read_bytes()
        writer.write_marker(self.out,SHA,'123','1')
        self.public[reader.MARKER]=(self.out/reader.MARKER).read_bytes()
        self.assertEqual(self.verify()['checkedPages'],6)
        self.public['atlas.html']=b'Changed legacy HTML'
        result=self.verify()
        self.assertFalse(result['passed'])
        self.assertTrue(any(row['path']=='/atlas.html' for row in result['errors']))


if __name__=='__main__': unittest.main()
