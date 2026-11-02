#!/usr/bin/env python3
"""Undo each round-3 fix in its own scratch copy, regenerate so freshness cannot
mask it, and run --selftest or --check. Usage: mutants.py <base> <python> <work> <out.tsv>"""
import json, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
base, py, work, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
GEN = "scripts/gen_register_reference.py"
PAGE = "scripts/register_page.py"
NEW_ROWS = '''    rows = [[model.wording.conditions(term) or "every case", value]
            for value, terms in values.items() if value != other for term in terms]
    if other is not None:
        rows.append(["any other case", other])
'''
def sub(old, new):
    def f(root):
        p = root / PAGE; t = p.read_text(encoding="utf-8"); assert t.count(old) == 1, old
        p.write_text(t.replace(old, new), encoding="utf-8")
    return f
def undo_read_value_table(root):
    p = root / PAGE; t = p.read_text(encoding="utf-8")
    a = t.index("    live = [leaf for _, leaf in reg.views if not leaf_constant(leaf, model)]")
    b = t.index('    return table(["When", "A read returns"], rows)')
    t = t[:a] + ("    rows = []\n    live = [leaf for _, leaf in reg.views if not leaf_constant(leaf, model)]\n"
                 "    for conds, leaf in reg.views:\n"
                 "        rows.append([model.wording.conditions(conds), leaf_text(leaf, len(live) == 1, model)])\n") + t[b:]
    p.write_text(t, encoding="utf-8")
def desc(change):
    def f(root):
        p = root / "scripts/register_descriptions.json"; d = json.loads(p.read_text(encoding="utf-8")); change(d)
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return f
def reserved(d):
    d["registers"]["PP_NVM_STAT"]["split"]["PP_NVM_CSR_RDATA"][-2:] = [["1:0", "RESERVED", ""]]
def table_note(d):
    d["registers"]["ETH_GUARD"]["notes"] = ["| Note |\n|---|\n| " + "word " * 25 + "end. |"]
# name, plant, regenerate first, command, what undoing it must do
M = [
 ("U1_refusal_reserved_off", sub('if fl.name == "RESERVED" and "W" in fl.access and any(note.startswith("writes:") for note in fl.notes):', "if False:"), True, "--selftest"),
 ("U2_refusal_table_off", sub("    if TABLE_DELIMITER_RE.search(text):\n", "    if False:\n"), True, "--selftest"),
 ("U3_read_table_exact_undo", undo_read_value_table, True, "--selftest"),
 ("U4_no_merge", sub("if care & bit and not value & bit and (value | bit, care) in current:", "if False:"), True, "--selftest"),
 ("U5_negated_spellings_apart", sub('NEGATED = {"!=": "==", ">=": "<", "<=": ">"}', "NEGATED = {}"), True, "--selftest"),
 ("U6_priority_reversed", sub("leaf = next(leaf for conds, leaf in views if", "leaf = next(leaf for conds, leaf in reversed(views) if"), True, "--selftest"),
 ("U7_exclusive_off", sub("""            if equal.setdefault(signal, unparse(node[3])) != unparse(node[3]):
                return True
""", "            equal.setdefault(signal, unparse(node[3]))\n"), True, "--selftest"),
 ("D1_reserved_row_back_in_data", desc(reserved), False, "--check"),
 ("D2_table_note_in_data", desc(table_note), False, "--check"),
 ("X1_other_case_row_dropped", sub('        rows.append(["any other case", other])\n', "        pass\n"), True, "--selftest"),
 ("X2_other_case_wrong_value", sub('        rows.append(["any other case", other])\n', '        rows.append(["any other case", "`0xDEADDEAD`"])\n'), True, "--selftest"),
 ("X3_only_first_term_kept", sub("if value != other for term in terms]", "if value != other for term in terms[:1]]"), True, "--selftest"),
]
def run(m):
    name, plant, regen, cmd = m
    root = work / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(base, root)
    plant(root)
    w = subprocess.run([py, "-B", GEN, "--write"], cwd=root, capture_output=True, text=True) if regen else None
    t = subprocess.run([py, "-B", GEN, cmd], cwd=root, capture_output=True, text=True)
    out_text = t.stdout + t.stderr
    failed = [l.strip()[:100] for l in t.stdout.splitlines() if l.startswith("  FAIL")]
    if cmd == "--check":
        failed = [l.strip()[:150] for l in out_text.splitlines() if "REFUSED" in l or "stale" in l][:2]
    (work / f"{name}.log").write_text((w.stdout + w.stderr if w else "") + out_text, encoding="utf-8")
    shutil.rmtree(root)
    return f"{name}\twrite_rc={w.returncode if w else 'n/a'}\t{cmd}_rc={t.returncode}\t{failed[:4]}"
with ThreadPoolExecutor(12) as ex:
    res = list(ex.map(run, M))
out.write_text("\n".join(res) + "\n", encoding="utf-8")
print("\n".join(res))
