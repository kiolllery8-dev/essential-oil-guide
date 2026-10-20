"""Draft exact Cloudflare reconstruction, preserving the original raw checker.

Only a pinned beacon insertion and reversible, HTML-context email protection
are permitted. Every other byte must equal the original guarded artifact.
This module never executes Cloudflare, site scripts, analytics or chat.
"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import re
from html.parser import HTMLParser
from pathlib import Path

spec = importlib.util.spec_from_file_location('raw_public', Path(__file__).with_name('verify-public-deployment.py'))
raw = importlib.util.module_from_spec(spec); spec.loader.exec_module(raw)
POLICY = 'intelliverse-cloudflare-exact-v1-draft'
BEACON_SHA256 = '161f2cbf38dc2d029b6223cae09efb59c27edd57a3932b62c320ce014c213795'
BEACON_BYTES = 367
DECODER = b'<script data-cfasync="false" src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>'
HEX = rb'([0-9a-f]{4,512})'
SPAN = re.compile(rb'<span class="__cf_email__" data-cfemail="'+HEX+rb'">\[email&#160;protected\]</span>')
PLAIN = re.compile(rb'<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="'+HEX+rb'">\[email&#160;protected\]</a>')
HREF_VALUE = re.compile(rb'/cdn-cgi/l/email-protection#'+HEX)


def href_edit(token, start):
    """Locate actual attributes without scanning inside quoted attribute values."""
    if not token.startswith(b'<a'):
        return None
    position = 2; hrefs = []
    while position < len(token):
        whitespace = re.match(rb'\s*', token[position:]); position += whitespace.end()
        if token[position:] in (b'>', b'/>'):
            break
        name = re.match(rb'[A-Za-z_:][A-Za-z0-9_.:-]*', token[position:])
        if not name:
            raise ValueError('Unsupported attribute syntax')
        name_start = position; position += name.end()
        key = name.group().lower()
        whitespace = re.match(rb'\s*', token[position:]); position += whitespace.end()
        value_start = value_end = None; quote = None
        if token[position:position+1] == b'=':
            position += 1
            whitespace = re.match(rb'\s*', token[position:]); position += whitespace.end()
            quote = token[position:position+1]
            if quote in (b'"', b"'"):
                value_start = position+1; value_end = token.find(quote, value_start)
                if value_end < 0: raise ValueError('Unclosed attribute value')
                position = value_end+1
            else:
                value_start = position
                value = re.match(rb'[^\s>]+', token[position:])
                if not value: raise ValueError('Missing attribute value')
                position += value.end(); value_end = position
        if key == b'href':
            hrefs.append((name_start, value_start, value_end, quote))
    if len(hrefs) > 1:
        raise ValueError('Duplicate actual href attributes')
    if not hrefs or hrefs[0][1] is None:
        return None
    name_start, value_start, value_end, quote = hrefs[0]
    value = token[value_start:value_end]
    match = HREF_VALUE.fullmatch(value)
    if match:
        if quote != b'"' or token[name_start:value_end+1] != b'href="'+value+b'"':
            raise ValueError('Unknown protected href template')
        return (start+value_start, start+value_end, b'mailto:'+decode_email(match.group(1)))
    return None


def decode_email(encoded):
    if len(encoded) % 2:
        raise ValueError('Odd email encoding')
    value = bytes.fromhex(encoded.decode('ascii'))
    decoded = bytes(byte ^ value[0] for byte in value[1:])
    # This first policy only covers plain ASCII addresses seen in artifacts.
    # Queries, HTML entities, Unicode and new encoding forms fail closed.
    if not re.fullmatch(rb'[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63}', decoded):
        raise ValueError('Unsupported protected email address')
    return decoded


class EmailReconstructor(HTMLParser):
    def __init__(self, body):
        super().__init__(convert_charrefs=False)
        self.body = body; self.edits = []; self.emails = []; self.scripts = []
        self.blocked = []; self.body_ends = []
        self.lines = [0]
        for match in re.finditer(b'\n', body): self.lines.append(match.end())
        self.feed(body.decode('latin1')); self.close()

    def handle_starttag(self, tag, attrs):
        line, column = self.getpos(); start = self.lines[line-1] + column
        token = self.get_starttag_text().encode('latin1')
        if self.blocked:
            if self.blocked[-1] in ('template', 'noscript') and tag == self.blocked[-1]:
                self.blocked.append(tag)
            return
        if tag == 'script':
            self.scripts.append(start)
        if tag in ('script', 'style', 'textarea', 'title', 'xmp', 'iframe',
                   'noembed', 'noframes', 'plaintext', 'noscript', 'template'):
            self.blocked.append(tag)
            return
        expression = SPAN if tag == 'span' else PLAIN if tag == 'a' else None
        match = expression.match(self.body, start) if expression else None
        if match:
            self.edits.append((start, match.end(), decode_email(match.group(1))))
            self.emails.append(match.end())
        elif tag == 'a':
            edit = href_edit(token, start)
            if edit:
                self.edits.append(edit)
                self.emails.append(start+len(token))

    def handle_endtag(self, tag):
        if self.blocked:
            if tag == self.blocked[-1]: self.blocked.pop()
        elif tag == 'body':
            line, column = self.getpos(); self.body_ends.append(self.lines[line-1]+column)


def reconstruct(original, public):
    if original == public:
        return {'mode': 'exact', 'beaconInsertions': 0, 'emailRewrites': 0}
    if len(public) > 4_000_000 or len(original) > 4_000_000:
        raise ValueError('HTML exceeds limit')
    if b'data-cfemail=' in original or DECODER in original:
        raise ValueError('Original contains pre-existing edge email markup')
    close = public.rfind(b'</body>')
    if close < BEACON_BYTES:
        raise ValueError('Missing expected pinned beacon position')
    insertion = public[close-BEACON_BYTES:close]
    if hashlib.sha256(insertion).hexdigest() != BEACON_SHA256:
        raise ValueError('Unknown beacon bytes, configuration or position')
    structure = EmailReconstructor(public)
    if close-BEACON_BYTES not in structure.scripts or structure.body_ends != [close]:
        raise ValueError('Pinned beacon is not an HTML script before the actual body close')
    body = public[:close-BEACON_BYTES] + public[close:]
    parser = EmailReconstructor(body)
    decoder_positions = [position for position in parser.scripts if body.startswith(DECODER, position)]
    if parser.emails:
        if len(decoder_positions) != 1:
            raise ValueError('Email rewrites require exactly one pinned decoder')
        decoder = decoder_positions[0]
        following = [position for position in parser.scripts if position > decoder]
        if (decoder < max(parser.emails) or not following or
                min(following) != decoder+len(DECODER) or
                any(max(parser.emails) <= position < decoder for position in parser.scripts)):
            raise ValueError('Decoder is not immediately before the first script after email rewrites')
        parser.edits.append((decoder, decoder+len(DECODER), b''))
    elif decoder_positions:
        raise ValueError('Unexpected decoder without a reversible email rewrite')
    rebuilt = []; end = 0
    for start, stop, replacement in sorted(parser.edits):
        if start < end:
            raise ValueError('Overlapping edge rewrites')
        rebuilt.extend((body[end:start], replacement)); end = stop
    rebuilt.append(body[end:])
    if b''.join(rebuilt) != original:
        raise ValueError('Bytes outside the exact reversible transforms differ')
    return {'mode': 'exact-cloudflare-reconstruction', 'beaconInsertions': 1,
            'emailRewrites': len(parser.emails)}


def verify(output, sha, run_id, attempt, get=raw.fetch):
    marker, pages = raw.inspect_export(output, sha, run_id, attempt)
    if json.loads(get(raw.MARKER, run_id, attempt, 4096)) != marker:
        raise ValueError('Public marker differs from exact artifact')
    def check(item):
        path, _ = item
        filename = path+'index.html' if not path or path.endswith('/') else path
        try:
            original = (Path(output)/filename).read_bytes()
            public = get(path, run_id, attempt, 4_000_000)
            result = reconstruct(original, public)
            return {'path': '/'+path, 'passed': True, **result,
                    'originalSha256': hashlib.sha256(original).hexdigest(),
                    'publicSha256': hashlib.sha256(public).hexdigest()}
        except Exception as error:
            return {'path': '/'+path, 'passed': False, 'error': type(error).__name__+': '+str(error)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, pages))
    stable = json.loads(get(raw.MARKER, run_id, attempt, 4096)) == marker
    return {'scope': 'all-exported-html-exact-cloudflare-reconstruction',
            'policy': POLICY, 'sourceSha': sha, 'runId': run_id, 'runAttempt': attempt,
            'checkedPages': len(pages), 'passed': stable and all(row['passed'] for row in results),
            'markerStable': stable, 'pages': results, 'browserUiVerified': False,
            'independentReviewVerified': False, 'productionRollbackVerified': False,
            'automaticPublicationAuthorized': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--expected-source-sha', required=True)
    parser.add_argument('--expected-run-id', required=True)
    parser.add_argument('--expected-run-attempt', required=True)
    parser.add_argument('--report', type=Path, default=Path('cloudflare-verification.json'))
    args = parser.parse_args()
    try:
        report = verify(args.out, args.expected_source_sha, args.expected_run_id, args.expected_run_attempt)
    except Exception as error:
        report = {'passed': False, 'policy': POLICY, 'error': type(error).__name__+': '+str(error),
                  'automaticPublicationAuthorized': False}
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='pages'}, indent=2))
    if not report['passed']: raise SystemExit(1)
