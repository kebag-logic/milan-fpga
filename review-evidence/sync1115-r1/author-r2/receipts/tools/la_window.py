#!/usr/bin/env python3
"""la_window.py HARNESS_DIR RESULTS_DIR GROUP AT_MS: what the CPU ran between a LeaveAll run-out near AT_MS and its
first frame: the passes there, their cycles in total and by module (the pass's per-module counter), and the
function entries traced there, by name (the log's entries). An experiment's read-out; it grades nothing."""
import sys
from collections import Counter
from pathlib import Path

harness, results, group, at_ms = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], float(sys.argv[4])
sys.path.insert(0, str(harness))
import grade  # noqa: E402
import mrpdu_grade  # noqa: E402

text = (results / f'{group}.log').read_text(errors='replace')
log = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
entry = min((c for c, n in log.entries if n == 'on_la_timer'), key=lambda c: abs(c / 1e5 - at_ms))
outcome, frames = mrpdu_grade.resolve(log, entry)
end = frames[0][0] if frames else entry
print(f'{group}: LeaveAll run-out at {entry / 1e5:.3f} ms, {outcome}, first frame {(end - entry) / 1e5:.3f} ms after it')
passes = [p for p in log.passes if entry <= p.start_sys < end]
mods, cyc = Counter(), 0
for p in passes:
    cyc += p.cycles
    mods.update(p.modules)
print(f'  {len(passes)} passes between, {cyc:,} CPU cycles in them ({cyc / 1e5:.1f} ms of the {(end - entry) / 1e5:.1f})')
for m, c in mods.most_common(8):
    print(f'    {m}: {c:,}')
names = Counter(n for c, n in log.entries if entry <= c < end)
print('  entries traced between: ' + ', '.join(f'{n} x{k}' for n, k in names.most_common(12)))
big = sorted(passes, key=lambda p: -p.cycles)[:5]
print('  longest passes: ' + '; '.join(f'{p.start_sys / 1e5:.1f} ms {p.cycles:,}' for p in big))
print('  entries in order: ' + '; '.join(f'{n} {(c - entry) / 1e5:+.3f} ms' for c, n in log.entries
                                         if entry - 20_000_000 <= c < end + 100_000 and n in ('on_join_timer', 'on_la_timer', 'on_pt_timer', 'build_mrpdu')))
tx = [(c, i) for c, ch, i, _ in log.tx if entry - 20_000_000 <= c < end + 100_000]
print('  frames sent (all channels) from 200 ms before: ' + '; '.join(f'{(c - entry) / 1e5:+.3f}' for c, _ in tx[:40]))
