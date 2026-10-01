#!/usr/bin/env python3
"""R425-5: withheld every-channel capture sizes, checked without printing them.

Usage: r425_5_withheld.py <repo> <old-rev> <new-rev> <text files...>
From the old page (git show <old-rev>:page) it reads the three every-channel
rows' Bytes cells and derives, in memory, the capture's channel count for
3- and 4-byte samples at 48 kHz from each row's duration. It never prints a
size or the count. It then checks, for the new page and every extra text file:
  W1 no withheld size appears (with or without thousands separators);
  W2 no integer, divided by duration * 48000 * bytes-per-sample for any
     duration stated on the page or in the file and 3 or 4 bytes, gives the
     derived channel count exactly;
  W3 (power check) the same test flags the old page's three rows.
Prints labels and counts only.
"""
import re, subprocess, sys

repo, old, new = sys.argv[1:4]
extra = sys.argv[4:]
PAGE = 'docs/findings/117_AUDIO_CONTINUITY.md'
show = lambda rev: subprocess.run(['git', '-C', repo, 'show', f'{rev}:{PAGE}'],
                                  check=True, capture_output=True, text=True).stdout
old_page, new_page = show(old), show(new)
rows = re.findall(r'^\| [^|]*every channel, (\d+) s \| (\d+) \|', old_page, re.M)
assert len(rows) == 3, 'expected three every-channel rows on the old page'
sizes = {int(b) for _, b in rows}
counts = set()
for dur, b in rows:
    for bps in (3, 4):
        q, r = divmod(int(b), int(dur) * 48000 * bps)
        if r == 0:
            counts.add(q)
print(f'old page: {len(rows)} every-channel rows; derived channel-count candidates: {len(counts)} (not printed)')

def durations(text):
    ds = {float(x) for x in re.findall(r'(\d+(?:\.\d+)?) ?s\b', text)}
    ds |= {3.0, 10.0, 15.0, 25.0, 40.0, 660.0, 660.15, 657.7}
    return {d for d in ds if d > 0}

def ints(text):
    out = set()
    for tok in re.findall(r'\d[\d,]*\d|\d', text):
        t = tok.replace(',', '')
        if t.isdigit():
            out.add(int(t))
    return out

def check(label, text):
    vals = ints(text)
    w1 = sorted(v for v in vals if v in sizes)
    w2 = 0
    for v in vals:
        if v < 48000:
            continue
        for d in durations(text):
            for bps in (3, 4):
                den = d * 48000 * bps
                q = v / den
                if abs(q - round(q)) < 1e-9 and round(q) in counts:
                    w2 += 1
    print(f'{label}: W1 withheld sizes present: {len(w1)}; W2 exact divisions to the channel count: {w2}')
    return len(w1), w2

check('POWER old page (expect W1 3, W2 >= 3)', old_page)
res = [check('new page', new_page)]
for f in extra:
    res.append(check(f, open(f, encoding='utf-8').read()))
bad = sum(a + b for a, b in res)
print('RESULT', 'PASS' if bad == 0 else 'FAIL', f'({bad} hits outside the power check)')
