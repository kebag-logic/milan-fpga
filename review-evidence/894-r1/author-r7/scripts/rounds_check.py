"""THE RETRY's rounds and the AECP items of harness logs against the tree's stated costs (round_grade.held,
poll_grade.held), partial logs included: each kind's count, its most and how many over. usage: rounds_check.py TREE N_IF LOG..."""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade, round_grade, poll_grade  # noqa: E402
n_if = int(sys.argv[2])
for p in map(Path, sys.argv[3:]):
    text = p.read_text(errors='replace'); text = text[:text.rfind('\n') + 1]
    log = grade.parse(text, 100_000_000, 100_000_000)
    r = round_grade.held(log, n_if)
    h = poll_grade.held(log, n_if)
    over = [o for o in r.get('over', [])]
    worst = max(over, key=lambda o: o['cycles'] - o['limit'], default=None)
    print(f"{p.stem}: rounds {r.get('rounds', '?')}, over {len(over)}"
          + (f", the worst {worst['cycles']:,} against {worst['limit']:,} ({worst['notices']} notice(s))" if worst else '')
          + f"; aecp item most {h['heaviest'].get('aecp', 0):,} of {h['limits']['aecp']:,}; base most {h['heaviest']['base']:,}")
