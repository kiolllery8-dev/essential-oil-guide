"""Loopback-only transport tests; no production traffic or browser execution."""
import importlib.util
import json
import tempfile
import threading
import unittest
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


def load(name,file):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(file))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value

reader=load('reader_http','verify-public-deployment.py')
writer=load('writer_http','write-deployment-version.py')


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.out=Path(self.temp.name)
        (self.out/'index.html').write_bytes(b'<h1>Home</h1>')
        (self.out/'hidden').mkdir();(self.out/'hidden/index.html').write_bytes(b'<meta name="robots" content="noindex">')
        writer.write_marker(self.out,'a'*40,'123','1')
        self.mode='normal';self.target_requests=0
        test=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args): pass
            def do_GET(self):
                path=urlsplit(self.path).path
                if path=='/redirect-target': test.target_requests+=1
                if test.mode=='redirect' and path=='/'+reader.MARKER:
                    self.send_response(302);self.send_header('Location','/redirect-target');self.end_headers();return
                target=test.out/path.lstrip('/')
                if path.endswith('/'): target=target/'index.html'
                if not target.is_file(): self.send_error(404);return
                body=target.read_bytes();self.send_response(200)
                self.send_header('Content-Length',str(len(body)))
                self.end_headers();self.wfile.write(body)
        self.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.previous=reader.SITE
        reader.SITE='http://127.0.0.1:'+str(self.server.server_address[1])
        self.addCleanup(self.close)

    def close(self):
        self.server.shutdown();self.server.server_close();self.thread.join()
        reader.SITE=self.previous

    def test_actual_transport_checks_noindex(self):
        result=reader.verify(self.out,'a'*40,'123','1')
        self.assertTrue(result['passed']);self.assertEqual(result['checkedPages'],2)

    def test_actual_redirect_does_not_request_target(self):
        self.mode='redirect'
        with self.assertRaises(ValueError): reader.verify(self.out,'a'*40,'123','1')
        self.assertEqual(self.target_requests,0)

    def test_response_size_is_bounded(self):
        with self.assertRaises(ValueError): reader.fetch('','123','1',4)


if __name__=='__main__': unittest.main()
