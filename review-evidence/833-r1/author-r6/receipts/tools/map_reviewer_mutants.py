#!/usr/bin/env python3
"""Map each round 5 reviewer mutant to the committed MUTANTS entry with the same mutated product text.

usage: python3 -I -B map_reviewer_mutants.py <tree> <R763-5 add_mutants.py> <R764-5 probe_mutants.py>
Exit 1 if any reviewer mutant has no committed entry with an equal mutated text.
"""
import hashlib
import runpy
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "scripts"))
import process_test_support as pts  # noqa: E402

product = (tree / "scripts/owned_process.py").read_text()


def mutated(edits) -> str:
    """The product with these edits, each required to match once."""
    text = product
    for old, new in edits:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    return hashlib.sha256(text.encode()).hexdigest()


committed = {}
for name, entry in pts.MUTANTS.items():
    committed.setdefault(mutated(entry[2:]), []).append(name)
r763 = runpy.run_path(sys.argv[2], run_name="not-main")["NEW"]
source = Path(sys.argv[3]).read_text()
namespace = {}
exec(source[source.index("OWN = {"):source.index("\npts.MUTANTS.update")], namespace)  # the packet's own table
reviewer = {f"R763-5/{n}": edits for n, edits in r763.items()}
reviewer.update({f"R764-5/{n}": entry[2:] for n, entry in namespace["OWN"].items()})
missing = 0
for name, edits in reviewer.items():
    found = committed.get(mutated(edits))
    print(f"{name} -> {found}")
    missing += not found
print(f"{len(reviewer)} reviewer mutants, {missing} without a committed equal")
sys.exit(1 if missing else 0)
