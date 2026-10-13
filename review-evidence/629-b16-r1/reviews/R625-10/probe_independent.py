#!/usr/bin/env python3
"""Independent whole-check probes, preserving source line numbers.
Usage: locked-python probe_independent.py REPO PACKET OUTPUT
"""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

repo, packet, output = [Path(x).resolve() for x in sys.argv[1:]]
check = packet/'tools/check_b16_figures.py'
doc = repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
base = doc.read_text().splitlines(True)
index = (doc.parent/'README.md').read_text()
target = next(i for i,x in enumerate(base) if x.startswith('| The tone source and the peer\'s path into its talker | None beyond'))
cases = {
    'quoted_unit': ' Extra "7.25 ppm".',
    'linked_unit': ' Extra [7.25 ppm](#b16c-attribution).',
    'decimal_nbsp': ' Extra CLOCK_DOMAIN 7\u00a0ppm.',
    'unlisted_unit': ' Extra CLOCK_DOMAIN 7 furlongs.',
    'exponent': ' Extra -.7e+2ppm.',
    'joined_unit': ' Extra 26s.',
    'raw_tag_split': ' Extra CLOCK_DOMAIN 7<span></span>ppm.',
    'character_reference': ' Extra CLOCK_DOMAIN 7&#32;ppm.',
    'unicode_numeric': ' Extra CLOCK_DOMAIN ٧ ppm.',
    'superscript_numeric': ' Extra CLOCK_DOMAIN ⁷ ppm.',
    'math_text': ' Extra $7$ ppm.',
    'linked_image': ' Extra CLOCK_DOMAIN 7[![](x.png)](#b16c-attribution)ppm.',
    'collapsed_reference_image': ' Extra CLOCK_DOMAIN 7![blank][]ppm.',
    'nul_separator': ' Extra CLOCK_DOMAIN 7\x00ppm.',
    'unicode_keycap': ' Extra CLOCK_DOMAIN 7\ufe0f\u20e3ppm.',
    'zero_width_unit': ' Extra CLOCK_DOMAIN 7\u200bppm.',
    'short_comment': ' Extra CLOCK_DOMAIN 7<!-->ppm<!-- -->.',
    'email_after_code': ' Extra `label` x@example.com 7 ppm.',
    'entity_then_email': ' Extra &amp; x@example.com 7 ppm.',
    'xmpp': ' Extra xmpp:x@example.com 7 ppm.',
    'struck_figure': ' Extra ~~7 ppm~~.',
    'footnote_reference': ' Extra [^7].',
    'allowed_emphasis': ' Extra CLOCK_DOMAIN **7** ppm.',
}

def run(item):
    name, added = item
    folder = output/'scratch/independent'/name
    folder.mkdir(parents=True, exist_ok=True)
    lines = list(base)
    lines[target] = lines[target].rstrip('\n').rstrip('|') + added + ' |\n'
    if name == 'collapsed_reference_image':
        lines.append('\n[blank]: x.png\n')
    if name == 'footnote_reference':
        lines.append('\n[^7]: A note.\n')
    page = folder/doc.name
    page.write_text(''.join(lines))
    (folder/'README.md').write_text(index)
    r = subprocess.run([sys.executable, '-B', str(check), str(page), str(packet), str(folder/'rows.tsv'), str(folder/'coverage.tsv'), '--repo', str(repo), '--show', '100'], capture_output=True, text=True, timeout=120)
    relevant = [x for x in r.stdout.splitlines() if x.startswith(('MARKUP ', 'UNCOVERED '))]
    met = r.returncode == 1 and any(f'{doc.name}:{target+1} ' in x for x in relevant) and not r.stderr
    return dict(case=name, inserted=added, line=target+1, rc=r.returncode, stdout=r.stdout, stderr=r.stderr,
                rows_written=(folder/'rows.tsv').is_file(), coverage_written=(folder/'coverage.tsv').is_file(), met=met)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, cases.items()))
out = dict(head='f1b2489f5b1c929e81eeae79a469b2b27c47e340', cases=len(results), met=sum(x['met'] for x in results), results=results)
(output/'receipts/independent-probes.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k: out[k] for k in ('head','cases','met')}))
sys.exit(0 if all(x['met'] for x in results) else 1)
