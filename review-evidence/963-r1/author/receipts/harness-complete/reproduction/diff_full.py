#!/usr/bin/env python3
"""diff_full.py ROOT BASE HEAD OUT: the differential of the full CPU service-budget measurement, base against head,
every (point, arm, group) both ran: ROOT/<tree>/<point>/<arm>/g/<group>/ holds the run's <group>.log and results.json.
For each, what the device made observable, in each one's own order, times aside:
  - every frame on the wire (WIRE lines), per channel and interface, its bytes in order;
  - every write of a publication word (the pass records' W entries in the publication block), per word, in order;
  - the transmit commits per channel (TXC lines), the run's RESULT line, its refusals;
  - each probe's status and whether it is within its budget and its ceiling.
And beside it what the grade holds: the work passes over THE SHARE, and the STATED lines.
Writes OUT/diff.txt (one line a group: SAME or DIFF with the first difference) and OUT/diff.json, and prints a
summary; exit 1 on any difference, any group one side ran alone, or any head pass over THE SHARE. Read only."""
import collections
import json
import re
import sys
from pathlib import Path

root, base, head, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
PUB_LO, PUB_HI = 0x200, 0x200 + 0x80  # the publication block of one interface (the contract's layout)
#: A grandmaster identity of the testbench's flood (sim_main.cpp, flood_gm: 0x0a0b0c0dfffd0000 plus the flood's count,
#: one a pass), which a frame carries as the identity current at its build: it counts the passes before the frame.
FLOOD_GM = re.compile(r'0a0b0c0dfffd[0-9a-f]{4}')


def observe(run: Path, group: str) -> dict:
    wire, pub, txc = collections.defaultdict(list), collections.defaultdict(list), collections.Counter()
    result, refused, stated = None, [], 0
    with open(run / f'{group}.log', errors='replace') as f:
        for line in f:
            if line.startswith('WIRE '):
                _, _, iface, ch, data = line.split()
                wire[(int(ch), int(iface))].append(data)
            elif line.startswith('PASS ') and ' W ' in line:
                for entry in line.split(' W ', 1)[1].split():
                    parts = entry.split(':')
                    if len(parts) == 3 and PUB_LO <= int(parts[1], 16) < PUB_HI:
                        pub[int(parts[1], 16)].append(parts[2])
            elif line.startswith('TXC '):
                txc[int(line.split()[2])] += 1
            elif line.startswith('RESULT'):
                result = line.strip()
            elif line.startswith('REFUSED'):
                refused.append(line.strip())
    res = json.loads((run / 'results.json').read_text())
    g = next(x for x in res['results'] if x['group'] == group)
    probes = {p['probe']: (p.get('status'), p.get('within_budget'), p.get('within_ceiling')) for p in g['probes']}
    share = g.get('passes', {}).get('share', {})
    # the graded costs over their statements (poll_grade, whole_grade, round_grade, slice_grade: each prints STATED
    # and fails the run), and the run's refusals and findings, from its results
    stated = sum(len(g.get('passes', {}).get(k, {}).get('over') or []) for k in ('polls', 'stated', 'rounds', 'slices'))
    # THE SHARE's misses are the over counts reported beside the differential (the change's own target), the rest held
    findings = {k: len(res.get(k) or []) for k in ('refusals', 'misses', 'save_misses', 'notice_misses')}
    return dict(wire=wire, pub=pub, txc=txc, result=result, refused=refused, probes=probes,
                over=share.get('over'), longest=g.get('passes', {}).get('worst', {}).get('cycles'), stated=stated,
                findings=findings,
                rc=(run / 'rc').read_text().strip() if (run / 'rc').is_file() else '?')


def notices_equivalent(x: list, y: list) -> int | None:
    """AECP frames (subtype 0xfb) that differ only in the order the unsolicited notices go out across descriptors:
    every frame but an unsolicited one the same in order, each recipient (controller_entity_id) the same unsolicited
    frames sequence_id aside, and each recipient's sequence_ids consecutive in both. The recipients whose order moved,
    or None where the frames are not so equivalent."""
    def split(frames):
        solicited, per = [], collections.defaultdict(list)
        for f in frames:
            b = bytes.fromhex(f.replace('.', '0'))
            if len(b) < 38 or b[14] != 0xfb:
                return None
            if int.from_bytes(b[36:38], 'big') & 0x8000:
                per[b[26:34]].append((int.from_bytes(b[34:36], 'big'), f[:68] + f[72:]))
            else:
                solicited.append(f)
        return solicited, per
    sx, sy = split(x), split(y)
    if sx is None or sy is None or sx[0] != sy[0] or set(sx[1]) != set(sy[1]):
        return None
    for per in (sx[1], sy[1]):
        for c, fs in per.items():
            if any(s2 != (s1 + 1) & 0xffff for (s1, _), (s2, _) in zip(fs, fs[1:])):
                return None
    if any(sorted(f for _, f in sx[1][c]) != sorted(f for _, f in sy[1][c]) for c in sx[1]):
        return None
    return sum(1 for c in sx[1] if [f for _, f in sx[1][c]] != [f for _, f in sy[1][c]])


def first_diff(a: dict, b: dict, reordered: list | None = None) -> str | None:
    for ch in sorted(set(a['wire']) | set(b['wire'])):
        x, y = a['wire'].get(ch, []), b['wire'].get(ch, [])
        if reordered is not None and x != y:
            moved = notices_equivalent(x, y)
            if moved is not None:
                reordered.append((ch, moved))
                continue
        for k, (u, v) in enumerate(zip(x, y)):
            if u != v:
                return f'channel {ch[0]} if{ch[1]} frame {k}: {u[:48]}.. against {v[:48]}..'
        if len(x) != len(y):
            return f'channel {ch[0]} if{ch[1]}: {len(x)} frames against {len(y)}'
    for w in sorted(set(a['pub']) | set(b['pub'])):
        if a['pub'].get(w, []) != b['pub'].get(w, []):
            return f'publication word {w:#x}: {len(a["pub"].get(w, []))} writes against {len(b["pub"].get(w, []))}'
    for key in ('txc', 'result', 'refused', 'probes', 'findings'):
        if a[key] != b[key]:
            return f'{key}: {a[key]} against {b[key]}'
    return None


out.mkdir(parents=True, exist_ok=True)
lines, rows, bad = [], [], 0
for run in sorted((root / base).glob('*/*/g/*')):
    point, arm, group = run.parts[-4], run.parts[-3], run.parts[-1]
    other = root / head / point / arm / 'g' / group
    if not (run / 'results.json').is_file() or not (other / 'results.json').is_file():
        continue
    a, b = observe(run, group), observe(other, group)
    d = first_diff(a, b)
    masked = 0
    if d is not None and 'flood gm 1' in (run / f'{group}.txt').read_text():
        # the flood's identities masked: a frame that differs only in them differs in the passes before its build
        for x in (a, b):
            x['wire_raw'] = x['wire']
            x['wire'] = {ch: [FLOOD_GM.sub('0a0b0c0dfffd....', f) for f in fs] for ch, fs in x['wire'].items()}
        masked = sum(1 for ch in a['wire_raw'] for u, v in zip(a['wire_raw'][ch], b['wire_raw'].get(ch, [])) if u != v)
        d = first_diff(a, b)
    reordered = []
    if d is not None:
        d = first_diff(a, b, reordered)
    frames = sum(len(v) for v in a['wire'].values())
    tag = f'{point} {arm} {group}'
    flood = f'{masked} differing only in the flood\'s grandmaster identity, ' if masked else ''
    flood += ''.join(f'AECP channel {ch} if{i}\'s notices in another order across descriptors for {n} recipients, each '
                     'the same notices with its sequence_ids consecutive, ' for (ch, i), n in reordered)
    lines.append(f'{"SAME" if d is None else "DIFF"} {tag}: {frames} frames, {flood}'
                 f'{sum(len(v) for v in a["pub"].values())} publication writes; over THE SHARE {a["over"]} -> {b["over"]}'
                 f', longest {a["longest"]} -> {b["longest"]}; STATED {a["stated"]} -> {b["stated"]}; rc {a["rc"]} -> '
                 f'{b["rc"]}' + (f'; {d}' if d else ''))
    rows.append(dict(point=point, arm=arm, group=group, same=d is None, first_difference=d, frames=frames,
                     flood_gm_masked=masked, notices_reordered=[[ch, i, n] for (ch, i), n in reordered],
                     over=[a['over'], b['over']], longest=[a['longest'], b['longest']],
                     stated=[a['stated'], b['stated']], rc=[a['rc'], b['rc']]))
    bad += d is not None or bool(b['over']) or b['stated'] != 0 or b['rc'] != '0'
(out / 'diff.txt').write_text('\n'.join(lines) + '\n')
(out / 'diff.json').write_text(json.dumps(rows, indent=1) + '\n')
same = sum(r['same'] for r in rows)
print(f'{len(rows)} groups compared: {same} SAME, {len(rows) - same} DIFF; head passes over THE SHARE in '
      f'{sum(1 for r in rows if r["over"][1])} groups (base {sum(1 for r in rows if r["over"][0])}); '
      f'{bad} groups with a difference or a head finding')
sys.exit(1 if bad else 0)
