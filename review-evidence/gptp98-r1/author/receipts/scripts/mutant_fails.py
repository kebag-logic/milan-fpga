"""Run the #98 parser mutants through the arm's own code and keep every
FAIL line each one produces (the arm itself prints only its verdict).

usage: mutant_fails.py <parser tb dir> <work dir> <out.md>
"""
import sys
from pathlib import Path

tb = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tb))
import mutants  # noqa: E402

work = Path(sys.argv[2]); work.mkdir(parents=True, exist_ok=True)
out = ["# #98 parser mutants: named checks and every FAIL line", ""]
for idx, (name, edits, breaks) in enumerate(m for m in mutants.MUTATIONS if "(#98)" in m[0]):
    exe = mutants.build(mutants.stage(work, f"m{idx}", edits), work, f"m{idx}")
    rc, output = mutants.run_harness(exe)
    fails = [l for l in output.splitlines() if l.startswith("FAIL ")]
    missed = [b for b in breaks if not any(b in l for l in fails)]
    tally = [l for l in output.splitlines() if "checks:" in l]
    out += [f"## {name}", "", f"rc {rc}; {tally[-1] if tally else 'no tally'}; named {len(breaks)}, missed {len(missed)}", ""]
    out += ["Named: " + "; ".join(f"`{b}`" for b in breaks), "", "```"] + fails + ["```", ""]
    print(name, rc, len(fails), "missed", missed)
Path(sys.argv[3]).write_text("\n".join(out) + "\n")
