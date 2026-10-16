import importlib.util
import json
import hashlib
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('marker',Path(__file__).with_name('write-deployment-version.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.out=Path(self.temp.name);(self.out/'index.html').write_text('<h1>Original</h1>')

    def write(self): return module.write_marker(self.out,'a'*40,'123','1')

    def test_keeps_html_and_binds_file_bytes(self):
        before=(self.out/'index.html').read_bytes();first=self.write()
        self.assertEqual(before,(self.out/'index.html').read_bytes())
        self.assertEqual(first,json.loads((self.out/module.NAME).read_text()))
        (self.out/module.NAME).unlink();(self.out/'index.html').write_text('Changed')
        self.assertNotEqual(first['exportDigest'],self.write()['exportDigest'])

    def test_repeat_refused_without_overwriting(self):
        self.write();before=(self.out/module.NAME).read_bytes()
        with self.assertRaises(ValueError): self.write()
        self.assertEqual(before,(self.out/module.NAME).read_bytes())

    def test_bad_identity_and_incomplete_export(self):
        for sha,run,attempt in [('x','123','1'),('a'*40,'0','1'),('a'*40,'123','')]:
            with self.assertRaises(ValueError): module.write_marker(self.out,sha,run,attempt)
        (self.out/'index.html').unlink()
        with self.assertRaises(ValueError): self.write()

    def test_symlink_refused(self):
        try: (self.out/'alias').symlink_to(self.out/'index.html')
        except OSError: self.skipTest('Symlink privilege unavailable')
        with self.assertRaises(ValueError): self.write()

    def test_digest_uses_posix_string_order(self):
        (self.out/'Z.txt').write_bytes(b'z');(self.out/'a.txt').write_bytes(b'a')
        rows=[[name,hashlib.sha256((self.out/name).read_bytes()).hexdigest()]
              for name in ['Z.txt','a.txt','index.html']]
        expected=hashlib.sha256(json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        self.assertEqual(self.write()['exportDigest'],expected)


if __name__=='__main__': unittest.main()
