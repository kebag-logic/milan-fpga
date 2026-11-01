#!/usr/bin/env bash
# Disposable probes on an exported copy of the reviewed head; the clone is not modified.
# Usage: PYTHONPATH=<pinned renderer> probe_delta.sh <clone> <scratch-dir>
set -u
clone=$1; work=$2; rm -rf "$work"; mkdir -p "$work"
git -C "$clone" archive HEAD docs scripts CHANGELOG.md | tar -x -C "$work"
cd "$work" || exit 9
export PYTHONDONTWRITEBYTECODE=1
echo "# P1: the R758-10-R4 text as proposed, 12 words, in the guide: the style gate must refuse"
cp docs/guides/gptp/MANAGER.md /tmp/.m.$$
sed -i 's/^This guide covers the fabric plane until F6\.$/This guide covers the fabric plane, which owns product time until F6./' docs/guides/gptp/MANAGER.md
python3 scripts/check_doc_style.py 2>&1 | head -3 | cut -c1-200; echo "rc=${PIPESTATUS[0]}"
cp /tmp/.m.$$ docs/guides/gptp/MANAGER.md
echo "# P2: the two new sentences appended to the 'Use this page' paragraph: the style gate must refuse"
python3 - <<'PY'
import re
p='docs/guides/gptp/MANAGER.md'; t=open(p).read()
t=t.replace("Use this page for delivery decisions.\n\nThis guide","Use this page for delivery decisions.\nThis guide")
open(p,'w').write(t)
PY
python3 scripts/check_doc_style.py 2>&1 | head -3 | cut -c1-200; echo "rc=${PIPESTATUS[0]}"
cp /tmp/.m.$$ docs/guides/gptp/MANAGER.md; rm -f /tmp/.m.$$
echo "# P3: control, the exported copy unmodified"
python3 scripts/check_doc_style.py 2>&1 | head -2 | cut -c1-200; echo "rc=${PIPESTATUS[0]}"
echo "# P4: rendered structure of the ieee8021q clause and the MS and AB sentences"
python3 - <<'PY'
import cmarkgfm, re, html5lib
t=open('docs/traceability/ieee8021q.md',encoding='utf-8').read()
a=t.index('This clause splits cleanly'); b=t.index('Two consequences worth stating')
h=cmarkgfm.github_flavored_markdown_to_html(t[a:b])
d=html5lib.parse(h,namespaceHTMLElements=False)
body=d.find('body')
for el in body:
    if el.tag=='ul':
        print('ul items:',len(el.findall('li')))
        for li in el.findall('li'):
            s=' '.join(''.join(li.itertext()).split()); print('  li:',s[:70],'...','has MRP-1' if 'MRP-1..MRP-8' in s else '')
    else:
        print(el.tag+':',' '.join(''.join(el.itertext()).split())[:110])
a=open('docs/design/AREA_BUDGET.md',encoding='utf-8').read().splitlines()
print('AB sentences after the history marker:')
for l in a[182:186]:
    if l.strip(): print('  ',re.sub(r'\(https?://[^)]*\)','',l)[:90])
PY
