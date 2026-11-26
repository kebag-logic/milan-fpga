"""Cross-check the published power-cut listings against the board summaries.
usage: python3 -I check_cuts.py <r3 author dir> <r2 author dir>"""
import re, sys
from pathlib import Path
r3, r2 = Path(sys.argv[1]), Path(sys.argv[2])
CUT = re.compile(r'^cut\s+(\d+): off (\S+), ([\d.]+) s after the last BIND_RX \| (.*?) \| STREAM_INPUT (\d+) \| a bind since the previous cut: (True|False) \| hold reading: (yes|no)')
SINK = re.compile(r'sink (\d+): power off ([\d.]+) s after the response; idle at the bind (\w+).*?durable by ([\d.]+) s.*?durable ([\d.]+) s before it \(at least 0.25\) (\w+)')
tot = graded = 0
for shape in ('8x8', '1x1'):
    cuts = [CUT.match(l) for l in (r3 / 'cuts' / f'cuts-{shape}.txt').read_text().splitlines()]
    cuts = [c for c in cuts if c]
    sinks = [SINK.search(l) for l in (r2 / 'board' / f'summary-{shape}.txt').read_text().splitlines()]
    sinks = [s for s in sinks if s]
    g = [c for c in cuts if c.group(6) == 'True' and c.group(7) == 'yes']
    ung = [c for c in cuts if not (c.group(6) == 'True' and c.group(7) == 'yes')]
    mixed = [c for c in cuts if (c.group(6) == 'True') != (c.group(7) == 'yes')]
    print(f'{shape}: cuts {len(cuts)}, graded {len(g)}, ungraded {len(ung)} {[int(c.group(1)) for c in ung]}, bind/hold disagreeing {len(mixed)}')
    print(f'  summary sink lines {len(sinks)}; verdicts {sorted(set(s.group(6) for s in sinks))}; idle {sorted(set(s.group(3) for s in sinks))}')
    offs_c = [float(c.group(3)) for c in g]
    offs_s = [float(s.group(2)) for s in sinks]
    print(f'  graded off-times equal summary off-times in order: {offs_c == offs_s}')
    print(f'  graded inputs in order: {[int(c.group(5)) for c in g] == [int(s.group(1)) for s in sinks]}')
    dur = [float(s.group(4)) for s in sinks]; margin = [float(s.group(5)) for s in sinks]
    print(f'  off after response {min(offs_s):.3f}..{max(offs_s):.3f} s; durable max {max(dur)*1000:.1f} ms; margin before last frame min {min(margin):.3f} s')
    for c in ung:
        print(f'  ungraded cut {c.group(1)}: input {c.group(5)}, {c.group(3)} s after last bind, scenario {c.group(4)[:60]!r}')
    tot += len(cuts); graded += len(g)
print(f'TOTAL cuts {tot}, graded {graded}, ungraded {tot - graded}')
