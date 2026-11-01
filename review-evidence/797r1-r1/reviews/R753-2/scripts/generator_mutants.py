#!/usr/bin/env python3
"""Apply one generator mutant per scratch tree and run --selftest; a surviving mutant exits 0.
Usage: generator_mutants.py <tree> <mutant-id>"""
import sys
from pathlib import Path
MUTANTS = {
 "range_term": ("scripts/register_decode.py", 'if lo in RANGE_ARRAYS or lo == "A_STRM_SEL" or lo == "A_CHMAP_CTRL":', "if True:"),
 "flop_rom": ("scripts/register_decode.py", "if reset.value != rom.value or reset.unknown:", "if False:"),
 "cell_cap": ("scripts/gen_register_reference.py", "if words > MAX_CELL_WORDS:", "if False:"),
 "fingerprint": ("scripts/gen_register_reference.py", 'FINGERPRINT: fingerprint(model.root, model.soc["shape"])}', 'FINGERPRINT: (model.root / FINGERPRINT).read_text(encoding="utf-8")}'),
}
tree, mid = Path(sys.argv[1]), sys.argv[2]
rel, old, new = MUTANTS[mid]
p = tree / rel; t = p.read_text(encoding="utf-8")
assert old in t, mid
p.write_text(t.replace(old, new), encoding="utf-8")
