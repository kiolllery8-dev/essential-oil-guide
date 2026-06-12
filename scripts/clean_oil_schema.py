# -*- coding: utf-8 -*-
"""2026-06 schema 清理：刪假 aggregateRating、Person#author、MedicalWebPage、
重複 Organization/#organization 與 WebSite/#website 定義；author/reviewedBy 引用改 #organization。
適用：oil-*.html、oils.html、references.html（numerology/blend 由產生器修）。"""
import glob, json, re, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SITE = 'https://intelliverse.tw'
stats = {'files':0,'blocks':0,'dropped':0,'ratings':0,'refs':0}

def clean_block(src):
    try:
        obj = json.loads(src)
    except Exception:
        return None
    def strip_rating(n):
        if isinstance(n, dict) and 'aggregateRating' in n:
            n.pop('aggregateRating'); stats['ratings'] += 1
    if isinstance(obj, dict) and '@graph' in obj:
        keep = []
        for node in obj['@graph']:
            t = node.get('@type'); nid = node.get('@id','')
            types = t if isinstance(t, list) else [t]
            if nid == SITE+'/#author' and 'Person' in types:
                stats['dropped'] += 1; continue
            if 'MedicalWebPage' in types:
                stats['dropped'] += 1; continue
            if nid == SITE+'/#organization' and types == ['Organization']:
                stats['dropped'] += 1; continue
            if nid == SITE+'/#website' and 'WebSite' in types:
                stats['dropped'] += 1; continue
            strip_rating(node)
            if 'Product' in types:
                node.pop('brand', None)
                nt = [x for x in types if x != 'Product'] or ['ChemicalSubstance']
                node['@type'] = nt[0] if len(nt) == 1 else nt
            keep.append(node)
        obj['@graph'] = keep
    else:
        strip_rating(obj)
    out = json.dumps(obj, ensure_ascii=False, indent=2)
    n = out.count('"'+SITE+'/#author"')
    if n:
        out = out.replace('"'+SITE+'/#author"', '"'+SITE+'/#organization"')
        stats['refs'] += n
    return out

targets = sorted(glob.glob('html-source/oil-*.html')) + ['html-source/oils.html', 'html-source/references.html']
for f in targets:
    h = open(f, encoding='utf-8').read()
    changed = False
    def repl(m):
        global changed
        cleaned = clean_block(m.group(1))
        if cleaned is None: return m.group(0)
        changed = True; stats['blocks'] += 1
        return '<script type="application/ld+json">\n' + cleaned + '\n  </script>'
    h2 = re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', repl, h, flags=re.S)
    if changed:
        open(f, 'w', encoding='utf-8').write(h2); stats['files'] += 1
print('清理完成:', stats)
