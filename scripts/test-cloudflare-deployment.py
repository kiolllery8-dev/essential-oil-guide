import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


edge = load('edge', 'verify-cloudflare-deployment.py')
writer = load('writer', 'write-deployment-version.py')
BEACON = (Path(__file__).parent/'fixtures/cloudflare-beacon.html').read_bytes()
EMAIL = b'help@example.com'
SHA = 'a'*40


def encoded(value=EMAIL, key=42):
    return bytes([key]+[byte ^ key for byte in value]).hex().encode()


def beacon(body):
    return body.replace(b'</body>', BEACON+b'</body>')


class Tests(unittest.TestCase):
    def setUp(self):
        self.original = '<html><body>原文\n'.encode()+EMAIL+b'<script>original()</script></body></html>'

    def span(self, value=EMAIL):
        return b'<span class="__cf_email__" data-cfemail="'+encoded(value)+b'">[email&#160;protected]</span>'

    def protected(self):
        return beacon(self.original.replace(EMAIL,self.span(),1).replace(b'<script>',edge.DECODER+b'<script>',1))

    def test_exact_artifact_is_preserved(self):
        self.assertEqual(edge.reconstruct(self.original,self.original)['mode'],'exact')

    def test_only_pinned_beacon(self):
        self.assertEqual(edge.reconstruct(self.original,beacon(self.original))['emailRewrites'],0)

    def test_email_span_and_decoder_reconstruct_exact_original(self):
        self.assertEqual(edge.reconstruct(self.original,self.protected())['emailRewrites'],1)

    def test_plain_email_link_wrapper(self):
        value=b'<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="'+encoded()+b'">[email&#160;protected]</a>'
        public=beacon(self.original.replace(EMAIL,value,1).replace(b'<script>',edge.DECODER+b'<script>',1))
        self.assertTrue(edge.reconstruct(self.original,public))

    def test_mailto_href_and_visible_span_with_different_keys(self):
        original=b'<html><body><a href="mailto:'+EMAIL+b'" style="color:red"> '+EMAIL+b'</a><script>x()</script></body></html>'
        public=original.replace(b' href="mailto:'+EMAIL+b'"',b' href="/cdn-cgi/l/email-protection#'+encoded(key=99)+b'"')
        public=public.replace(b'> '+EMAIL,b'> '+self.span()).replace(b'<script>',edge.DECODER+b'<script>',1)
        self.assertEqual(edge.reconstruct(original,beacon(public))['emailRewrites'],2)

    def test_changed_original_text_is_rejected(self):
        with self.assertRaises(ValueError): edge.reconstruct(self.original,self.protected().replace('原文'.encode(),b'changed'))

    def test_wrong_email_address_is_rejected(self):
        public=self.protected().replace(encoded(),encoded(b'evil@example.com'))
        with self.assertRaises(ValueError): edge.reconstruct(self.original,public)

    def test_extra_attribute_or_changed_script_is_rejected(self):
        for public in (self.protected().replace(b'class="__cf_email__"',b'class="__cf_email__" onclick="evil()"'),
                       self.protected().replace(b'original()',b'evil()')):
            with self.subTest(public=public[-100:]), self.assertRaises(ValueError): edge.reconstruct(self.original,public)

    def test_unknown_or_duplicate_beacon_is_rejected(self):
        for public in (self.protected().replace(b'"spa":2',b'"spa":3'), beacon(self.protected())):
            with self.assertRaises(ValueError): edge.reconstruct(self.original,public)

    def test_missing_duplicate_or_changed_decoder_is_rejected(self):
        for public in (self.protected().replace(edge.DECODER,b''),
                       self.protected().replace(edge.DECODER,edge.DECODER*2),
                       self.protected().replace(b'data-cfasync="false"',b'data-cfasync="true"')):
            with self.assertRaises(ValueError): edge.reconstruct(self.original,public)

    def test_decoder_wrong_position_is_rejected(self):
        public=self.protected().replace(edge.DECODER,b'').replace(b'</script>',b'</script>'+edge.DECODER,1)
        with self.assertRaises(ValueError): edge.reconstruct(self.original,public)

    def test_decoder_without_email_is_rejected(self):
        with self.assertRaises(ValueError): edge.reconstruct(self.original,beacon(self.original.replace(b'<script>',edge.DECODER+b'<script>',1)))

    def test_cf_markup_inside_script_is_not_rewritten(self):
        original=b'<html><body><script>"'+EMAIL+b'"</script></body></html>'
        public=beacon(original.replace(EMAIL,self.span()))
        with self.assertRaises(ValueError): edge.reconstruct(original,public)

    def test_cf_markup_inside_comment_is_not_rewritten(self):
        original=b'<html><body><!--'+EMAIL+b'--><script>x()</script></body></html>'
        public=beacon(original.replace(EMAIL,self.span()).replace(b'<script>',edge.DECODER+b'<script>',1))
        with self.assertRaises(ValueError): edge.reconstruct(original,public)

    def test_cf_markup_inside_raw_text_and_inert_containers_is_not_rewritten(self):
        for tag in (b'textarea',b'title',b'xmp',b'iframe',b'noscript',b'template'):
            original=b'<html><body><'+tag+b'>'+EMAIL+b'</'+tag+b'><script>x()</script></body></html>'
            public=beacon(original.replace(EMAIL,self.span()).replace(b'<script>',edge.DECODER+b'<script>',1))
            with self.subTest(tag=tag), self.assertRaises(ValueError): edge.reconstruct(original,public)

    def test_pinned_beacon_cannot_be_removed_from_script_text(self):
        original=b'<html><body><script>"</body>"</script></html>'
        with self.assertRaises(ValueError): edge.reconstruct(original,beacon(original))

    def test_nested_inert_container_stays_blocked(self):
        original=b'<html><body><template><template></template>'+EMAIL+b'</template><script>x()</script></body></html>'
        public=beacon(original.replace(EMAIL,self.span()).replace(b'<script>',edge.DECODER+b'<script>',1))
        with self.assertRaises(ValueError): edge.reconstruct(original,public)

    def test_href_looking_text_inside_another_attribute_is_not_rewritten(self):
        original=b'<html><body><a title=\' href="mailto:'+EMAIL+b'"\'>label</a><script>x()</script></body></html>'
        public=original.replace(b' href="mailto:'+EMAIL+b'"',b' href="/cdn-cgi/l/email-protection#'+encoded()+b'"')
        public=beacon(public.replace(b'<script>',edge.DECODER+b'<script>',1))
        with self.assertRaises(ValueError): edge.reconstruct(original,public)

    def test_actual_href_with_quoted_decoy_still_reconstructs(self):
        original=b'<html><body><a title=\' href="unrelated"\' href="mailto:'+EMAIL+b'">label</a><script>x()</script></body></html>'
        public=original.replace(b'href="mailto:'+EMAIL+b'"',b'href="/cdn-cgi/l/email-protection#'+encoded()+b'"')
        public=beacon(public.replace(b'<script>',edge.DECODER+b'<script>',1))
        self.assertTrue(edge.reconstruct(original,public))

    def test_duplicate_real_href_is_rejected(self):
        original=b'<html><body><a href="other" href="mailto:'+EMAIL+b'">label</a><script>x()</script></body></html>'
        public=original.replace(b'href="mailto:'+EMAIL+b'"',b'href="/cdn-cgi/l/email-protection#'+encoded()+b'"')
        public=beacon(public.replace(b'<script>',edge.DECODER+b'<script>',1))
        with self.assertRaises(ValueError): edge.reconstruct(original,public)

    def test_non_html_whitespace_cannot_create_a_fake_href(self):
        for whitespace in (b'\x0b',b'\x85',b'\xa0'):
            original=b'<html><body><a '+whitespace+b'href="mailto:'+EMAIL+b'">label</a><script>x()</script></body></html>'
            public=original.replace(b'href="mailto:'+EMAIL+b'"',b'href="/cdn-cgi/l/email-protection#'+encoded()+b'"')
            public=beacon(public.replace(b'<script>',edge.DECODER+b'<script>',1))
            with self.subTest(whitespace=whitespace), self.assertRaises(ValueError): edge.reconstruct(original,public)

    def test_html_form_feed_separator_is_accepted(self):
        original=b'<html><body><a\x0chref="mailto:'+EMAIL+b'">label</a><script>x()</script></body></html>'
        public=original.replace(b'href="mailto:'+EMAIL+b'"',b'href="/cdn-cgi/l/email-protection#'+encoded()+b'"')
        public=beacon(public.replace(b'<script>',edge.DECODER+b'<script>',1))
        self.assertTrue(edge.reconstruct(original,public))

    def test_all_exported_html_noindex_and_legacy_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory); (output/'index.html').write_bytes(self.original)
            (output/'legacy.html').write_bytes(b'plain verification')
            (output/'hidden').mkdir(); (output/'hidden/index.html').write_bytes(self.original)
            marker=writer.write_marker(output,SHA,'123','1')
            public={'':self.protected(),'hidden/':beacon(self.original),'legacy.html':b'plain verification',
                    edge.raw.MARKER:json.dumps(marker).encode()}
            calls=[]
            def get(path,*args): calls.append(path); return public[path]
            result=edge.verify(output,SHA,'123','1',get)
            self.assertTrue(result['passed']); self.assertEqual(result['checkedPages'],3)
            self.assertFalse(result['automaticPublicationAuthorized'])
            self.assertEqual(calls.count(edge.raw.MARKER),2)
            public['legacy.html']=b'changed'
            self.assertFalse(edge.verify(output,SHA,'123','1',get)['passed'])


if __name__=='__main__': unittest.main()
