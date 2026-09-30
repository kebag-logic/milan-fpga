#!/usr/bin/env python3
"""Drive the published usb_frame_words.py with a synthetic capture: frame
1,632 set to the published words after 1,632 silent frames. It must return
those words, their tag/ordinal/low-byte split, previous_frame_silent and
in_order, refuse a wrong SHA-256 and an out-of-range frame, and report a
rotated frame as not in order.
usage: probe_frame_words.py <usb_frame_words.py> <published frame json> <workdir>"""
import array, hashlib, json, subprocess, sys
from pathlib import Path
tool, pub, work = sys.argv[1], json.load(open(sys.argv[2])), Path(sys.argv[3])
words = [int(w['word'], 16) for w in pub['words']]
a = array.array('I', [0] * (8 * 1632) + words + [0x01000000 | (0x6ec9 << 8)] * 8 + words[3:] + words[:3])
raw = work / 'synthetic.raw'; raw.write_bytes(a.tobytes())
h = hashlib.sha256(raw.read_bytes()).hexdigest()
def run(*args):
    return subprocess.run([sys.executable, '-I', tool, str(raw), *args], capture_output=True, text=True)
bad = 0
r = run(h, '1632'); out = json.loads(r.stdout)
got = [w['word'] for w in out['words']]
checks = {
    'rc 0': r.returncode == 0,
    'words equal published': got == [w['word'] for w in pub['words']],
    'split equal published': [(w['tag'], w['ordinal'], w['low_byte']) for w in out['words']] == [(w['tag'], w['ordinal'], w['low_byte']) for w in pub['words']],
    'byte_offset 52224': out['byte_offset'] == 52224,
    'previous_frame_silent': out['previous_frame_silent'] is True,
    'in_order': out['in_order'] is True,
}
r2 = run('0' * 64, '1632'); checks['wrong sha refused'] = r2.returncode != 0 and 'mismatch' in r2.stderr
r3 = run(h, str(len(a) // 8)); checks['out-of-range frame refused'] = r3.returncode != 0
r4 = run(h, '1634'); o4 = json.loads(r4.stdout); checks['rotated frame not in_order'] = o4['in_order'] is False and o4['previous_frame_silent'] is False
for k, v in checks.items():
    bad += not v; print(f'{"PASS" if v else "FAIL"} {k}')
print('RESULT', 'PASS' if not bad else 'FAIL'); sys.exit(1 if bad else 0)
