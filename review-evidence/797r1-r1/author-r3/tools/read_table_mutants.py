#!/usr/bin/env python3
"""Plant one generator mutant per run, regenerate the page so freshness cannot
mask it, and run --selftest. A surviving mutant exits 0.
Usage: read_table_mutants.py <clone> <python> <log dir>"""
import subprocess
import sys
from pathlib import Path

PAGE = "scripts/register_page.py"
MUTANTS = {
    "no_grouping": (PAGE, '''    rows = [[model.wording.conditions(term) or "every case", value]
            for value, terms in values.items() if value != other for term in terms]
    if other is not None:
        rows.append(["any other case", other])
''', '''    rows = [[model.wording.conditions(conds), leaf_text(leaf, len(live) == 1, model)] for conds, leaf in reg.views]
'''),
    "no_merge": (PAGE, "if care & bit and not value & bit and (value | bit, care) in current:", "if False:"),
    "polarity_inverted": (PAGE, "rows[value] = [[(found[name], bool(term >> n & 1))", "rows[value] = [[(found[name], not bool(term >> n & 1))"),
    "exclusive_compare_off": (PAGE, '''            if equal.setdefault(signal, unparse(node[3])) != unparse(node[3]):
                return True
''', "            equal.setdefault(signal, unparse(node[3]))\n"),
    "reserved_on_strobe_word": (PAGE, 'if fl.name == "RESERVED" and "W" in fl.access and any(note.startswith("writes:") for note in fl.notes):', "if False:"),
    "table_in_note": (PAGE, "    if TABLE_DELIMITER_RE.search(text):\n", "    if False:\n"),
}
clone, python, logs = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
logs.mkdir(parents=True, exist_ok=True)
GEN = "scripts/gen_register_reference.py"
survivors = 0
for name, (rel, old, new) in MUTANTS.items():
    path = clone / rel
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, name
    path.write_text(text.replace(old, new), encoding="utf-8")
    write = subprocess.run([python, "-B", GEN, "--write"], cwd=clone, capture_output=True, text=True)
    test = subprocess.run([python, "-B", GEN, "--selftest"], cwd=clone, capture_output=True, text=True)
    (logs / f"{name}.log").write_text(write.stdout + write.stderr + test.stdout + test.stderr, encoding="utf-8")
    failed = [ln.strip()[:90] for ln in test.stdout.splitlines() if ln.startswith("  FAIL")]
    print(f"{name}\twrite_rc={write.returncode}\tselftest_rc={test.returncode}\t{failed[:3]}", flush=True)
    survivors += test.returncode == 0
    subprocess.run(["git", "checkout", "-q", "--", "."], cwd=clone, check=True)
    subprocess.run(["git", "clean", "-qfd", "docs/diagrams/regmap"], cwd=clone, check=True)
print(f"survivors {survivors} of {len(MUTANTS)}", flush=True)
raise SystemExit(1 if survivors else 0)
