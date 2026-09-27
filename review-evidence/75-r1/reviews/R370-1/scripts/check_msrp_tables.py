"""Cross-check the page's MSRP tables against its per-cycle table and public events.

usage: check_msrp_tables.py <page.md> <packet author dir>
1. Sums per-cycle PDU and LeaveAll pairs and compares them to the sender table.
2. Checks the attribute table's per-type LeaveAll columns against the vectors.
3. Recomputes, for the ten public cycles, the per-cycle row from msrp.tsv
   (declarations, Ready, LeaveAll) and analysis.json (PDUs, sources).
"""
import collections, csv, json, re, sys
from pathlib import Path
page = open(sys.argv[1]).read(); root = Path(sys.argv[2]); bad = []
cyc = {}
for m in re.finditer(r'^\| DUT (listener|talker) \| (\d+) \| ([0-9.]+) \| (\d+) / (\d+) \| (\d+) / (\d+) \| (\d+) / (\d+) \| (\d+) / (\d+) \| (\d+) / (\d+) \| (\w+) \|$', page, re.M):
    g = m.groups(); cyc[(g[0], int(g[1]))] = dict(pdus=(int(g[3]), int(g[4])), la=(int(g[5]), int(g[6])), ta=(int(g[7]), int(g[8])), li=(int(g[9]), int(g[10])), ready=(int(g[11]), int(g[12])))
print('per-cycle rows parsed:', len(cyc))
sender = {(m[1], m[2]): dict(before=float(m[3]), after=float(m[4]), resumed=float(m[5]), pdus=int(m[6]), la=int(m[7]))
          for m in re.finditer(r'^\| DUT (listener|talker) \| (DUT|bridge) \| ([0-9.]+) \| ([0-9.]+) \| ([0-9.]+) \| (\d+) \| (\d+) \|$', page, re.M)}
attr = collections.defaultdict(dict)
for m in re.finditer(r'^\| DUT (listener|talker) \| (DUT|bridge) \| (\w+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$', page, re.M):
    attr[(m[1], m[2])][m[3]] = [int(x) for x in m.groups()[3:]]
for d in ('listener', 'talker'):
    for i, s in enumerate(('DUT', 'bridge')):
        pd = sum(cyc[(d, n)]['pdus'][i] for n in range(1, 101)); la = sum(cyc[(d, n)]['la'][i] for n in range(1, 101))
        t = sender[(d, s)]; a = attr[(d, s)]
        la_types = {k: v[6] for k, v in a.items()}
        ok = pd == t['pdus'] and la == t['la'] and sum(la_types.values()) == la
        print(f'{d} {s}: per-cycle PDU sum {pd} vs table {t["pdus"]}; LeaveAll sum {la} vs table {t["la"]}; per-type LeaveAll {la_types} -> {"OK" if ok else "MISMATCH"}')
        if not ok: bad.append((d, s))
        # per-cycle declaration sums vs attribute table (New+JoinIn+JoinMt)
        ta = sum(cyc[(d, n)]['ta'][i] for n in range(1, 101)); li = sum(cyc[(d, n)]['li'][i] for n in range(1, 101))
        ta_t = a['TalkerAdvertise'][0] + a['TalkerAdvertise'][1] + a['TalkerAdvertise'][3]
        li_t = a['Listener'][0] + a['Listener'][1] + a['Listener'][3]
        print(f'   TA declarations per-cycle sum {ta} vs attribute table {ta_t}; Listener declarations {li} vs {li_t}')
        if ta != ta_t or li != li_t: bad.append((d, s, 'decl'))
DECL = ('New', 'JoinIn', 'JoinMt')
for d in ('listener', 'talker'):
    for n in range(1, 6):
        name = f'{d}-{n:03d}'; ev = list(csv.DictReader(open(root / name / 'msrp.tsv'), delimiter='\t'))
        an = json.loads((root / name / 'analysis.json').read_text())
        row = {}
        for k, fn in (('ta', lambda e: e['type'] == 'TalkerAdvertise' and e['event'] in DECL),
                      ('li', lambda e: e['type'] == 'Listener' and e['event'] in DECL),
                      ('ready', lambda e: e['type'] == 'Listener' and e['event'] in DECL and e['listener'] == '2'),
                      ('la', lambda e: e['event'] == 'LeaveAll')):
            row[k] = tuple(sum(fn(e) and e['sender'] == s for e in ev) for s in ('DUT', 'bridge'))
        row['pdus'] = tuple(an['msrp']['whole'][s]['pdus'] for s in ('DUT', 'bridge'))
        want = cyc[(d, n)]
        same = all(row[k] == want[k] for k in row)
        print(f'{name}: recomputed {row} page {"MATCH" if same else want} distinct MSRP sources per sender { {s: len(v) for s, v in an["msrp_sources"].items()} } parse_errors {len(an["msrp_parse_errors"])}')
        if not same: bad.append(name)
print('MISMATCHES:', bad)
sys.exit(1 if bad else 0)
