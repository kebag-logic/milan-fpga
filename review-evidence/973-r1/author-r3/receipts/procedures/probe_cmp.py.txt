#!/usr/bin/env python3
"""probe_cmp.py BASE_RESULTS_JSON HEAD_RESULTS_JSON: every graded probe of the CPU budget harness (run.py's
results.json) on the base image against the head image's: its figure (ms) and bound (bound_ms) each side, the
difference, the verdict each side (within_budget), and its pass's instructions each side (pass_instr: equal is the
same code path). Then a summary: the probes paired, the verdicts that changed, the largest differences, and the probes
whose pass ran another instruction count. Prints a Markdown table and the summary."""
import json
import sys


def probes(path: str) -> dict[str, dict]:
    r = json.load(open(path))
    out = {}
    for g in r['results']:
        for p in g.get('probes', []):
            out[f"{g['group']}/{p['probe']}"] = p
    return out


b, h = probes(sys.argv[1]), probes(sys.argv[2])
both = sorted(set(b) & set(h))
rows, changed, instr_differ, deltas = [], [], [], []
for k in both:
    x, y = b[k], h[k]
    if x.get('status') != 'measured' or y.get('status') != 'measured':
        rows.append(f'| `{k}` | {x.get("status")} | {y.get("status")} | | | |')
        continue
    d = y['ms'] - x['ms']
    deltas.append((abs(d), d, k, x['ms'], y['ms'], x['budget_ms']))
    vb, vh = x['within_budget'], y['within_budget']
    if vb != vh:
        changed.append(k)
    ib, ih = x.get('pass_instr'), y.get('pass_instr')
    if ib != ih:
        instr_differ.append((k, ib, ih))
    rows.append(f'| `{k}` | {x["ms"]:.3f} | {y["ms"]:.3f} | {d:+.3f} | {x["budget_ms"]:g} | '
                f'{"fits" if vb else "MISS"} / {"fits" if vh else "MISS"} | {ib} / {ih} |')
print('| Probe | base ms | head ms | head-base | budget ms | verdict base / head | pass instructions base / head |')
print('|---|---:|---:|---:|---:|---|---|')
print('\n'.join(rows))
deltas.sort(reverse=True)
print(f'\nprobes: base {len(b)}, head {len(h)}, paired {len(both)}, only base {len(set(b) - set(h))}, '
      f'only head {len(set(h) - set(b))}')
print(f'verdicts changed: {len(changed)}' + (f' ({", ".join(changed)})' if changed else ''))
print(f'misses each side: base {sum(1 for k in both if not b[k].get("within_budget", True))}, '
      f'head {sum(1 for k in both if not h[k].get("within_budget", True))}')
print('largest differences: ' + '; '.join(f'{k} {d:+.3f} ms ({x:.3f} -> {y:.3f}, budget {bud:g})'
                                         for _, d, k, x, y, bud in deltas[:5]))
print(f'passes with another instruction count: {len(instr_differ)} of {len(deltas)}' +
      ('' if not instr_differ else ' (' + '; '.join(f'{k} {i} -> {j}' for k, i, j in instr_differ[:12]) + ')'))
