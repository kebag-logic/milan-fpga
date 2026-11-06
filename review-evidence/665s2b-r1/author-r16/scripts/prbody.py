#!/usr/bin/env python3
"""Round 15's PR body: round 14's, its header, roles, references, state, validation, limits and Definition of Done
restated, its rows 1 and 2 marked as restated, and a round 15 section before round 14's.

usage: prbody.py ROUND14.md ROUND15_SECTION.md FIGURES.json OUT.md
FIGURES.json holds the strings the restated parts quote, each measured or derived elsewhere (HANDOFF section 5).
"""
import json
import sys
from pathlib import Path

r14, section, figures, out = (Path(a) for a in sys.argv[1:5])
body = r14.read_text()
f = json.loads(figures.read_text())


def swap(old: str, new: str) -> None:
    """Replace one exact span of the body, which must occur once."""
    global body
    if body.count(old) != 1:
        raise SystemExit(f'not found once: {old[:70]!r}')
    body = body.replace(old, new)


swap('[A683q]\n', '[A683r]\n')
swap('REVIEW READY at the head below: `dev-soft-core` `a68536fa` merged, the split CPU on `sys` at 100 MHz, every '
     'measured row and pass fitting.',
     'REVIEW READY at the head below: `dev-soft-core` `a68536fa` merged, the split CPU on `sys` at 100 MHz, every '
     'measured row and pass fitting, aged windows included.')
start = body.index('## Status\n')
end = body.index('## Linked Issue / roles\n')
body = body[:start] + '## Status\n\n' + f['status'] + '\n\n' + body[end:]
swap('Executor: `[A683q]`', 'Executor: `[A683r]`')
swap('## Description\n\n### Round 14\n', '## Description\n\n' + section.read_text().rstrip('\n') + '\n\n### Round 14\n')
# round 14's rows 1 and 2, restated by round 15 (above)
swap('so no aged step lands among a window\'s records; at one, aged steps would land in 8x8\'s windows, where the least '
     'margin, 0.77 ms, is below a step, 0.96 ms. Every row and every pass fits at this head (below) |',
     'so no aged step lands among the records of a window opened from idle (restated in round 15: one opened at the '
     'age limit takes one, and the least margin is ' + f['least'] + ' ms) |')
swap('A save is durable at most 1,000 ms (DR2a) + S × 3 ticks + 10 ms after its change;',
     'A save is durable at most 1,000 ms (DR2a) + S × 3 ticks + 10 ms after its change with no save in flight '
     '(restated in round 15: a change marked while a save is in flight, 22,150 ms at 8x8/2if, 6,070 ms at 1x1);')
start = body.index('## Authoritative references\n')
end = body.index('- `docs/reference/FR_NFR.md` 3.4.1')
body = body[:start] + '## Authoritative references\n\n' + f['references'] + '\n' + body[end:]
swap('git checkout a3f23bbabdd9800177224432361fcd41b53bf882', 'git checkout ' + f['head'])
swap('python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-store-ageless '
     '--mutation store-step-ageless\n',
     'python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-store-ageless '
     '--mutation store-step-ageless\npython3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir '
     '/tmp/budget-aged-heavier --mutation store-step-aged-heavier\n')
start = body.index('Expected result / pass criteria:')
end = body.index('## Known limitations / out of scope\n')
body = body[:start] + f['expected'] + '\n\n' + f['evidence'] + '\n\n' + body[end:]
start = body.index('## Known limitations / out of scope\n')
end = body.index('- **The three egress-held rows**')
body = body[:start] + '## Known limitations / out of scope\n\n' + f['limits'] + '\n' + body[end:]
out.write_text(body)
print(f'{out}: {len(body):,} bytes')
