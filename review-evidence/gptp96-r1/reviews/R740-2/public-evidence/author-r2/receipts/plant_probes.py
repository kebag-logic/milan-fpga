#!/usr/bin/env python3
"""Planted-defect probes for the docs gate, each in a fresh archive copy.

usage: plant_probes.py <repo> <head> <old-checker-rev> <workdir>
"""
import re
import subprocess
import sys
from pathlib import Path

repo, head, old_rev, work = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4])
work.mkdir(parents=True, exist_ok=True)
old_checker = subprocess.run(
    ["git", "-C", repo, "show", f"{old_rev}:scripts/check_docs.py"],
    check=True, capture_output=True, text=True).stdout
ENV = {"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1",
       "TMPDIR": str(work)}


def fresh(name):
    tree = work / name
    subprocess.run(["rm", "-rf", str(tree)], check=True)
    tree.mkdir()
    archive = subprocess.run(["git", "-C", repo, "archive", head],
                             check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tree)], input=archive, check=True)
    return tree


def edit(tree, rel, old, new, count=1):
    path = tree / rel
    text = path.read_text()
    if text.count(old) < 1:
        raise SystemExit(f"{rel}: anchor not found: {old!r}")
    path.write_text(text.replace(old, new, count))


def run(tree, *args, checker="scripts/check_docs.py"):
    r = subprocess.run([sys.executable, "-B", checker, *args], cwd=tree,
                       capture_output=True, text=True, env=ENV)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()


SYNC_ROW = "| `SYNC_RTO_MS_C` | 375 |"
TREE = [
    ("control", lambda t: None, 0),
    ("const_plain_stale", lambda t: edit(t, "docs/INTEGRATION.md", SYNC_ROW, "| `SYNC_RTO_MS_C` | 376 |"), 1),
    ("const_bold_stale", lambda t: edit(t, "docs/INTEGRATION.md", SYNC_ROW, "| `SYNC_RTO_MS_C` | **376** |"), 1),
    ("const_negative", lambda t: edit(t, "docs/INTEGRATION.md", SYNC_ROW, "| `SYNC_RTO_MS_C` | -1 |"), 1),
    ("const_unit_stale", lambda t: edit(t, "docs/INTEGRATION.md", SYNC_ROW, "| `SYNC_RTO_MS_C` | 376 ms |"), 1),
    ("const_row_deleted", lambda t: edit(t, "docs/INTEGRATION.md", SYNC_ROW + " syncReceiptTimeout, ms | Milan 4.2.6.2.3, Table 4.2 |\n", ""), 1),
    ("const_name_unbackticked", lambda t: edit(t, "docs/INTEGRATION.md", SYNC_ROW, "| SYNC_RTO_MS_C | 376 |"), 1),
    ("code_drift", lambda t: edit(t, "hdl/ucode/gen_gptp_ucode.py", "SYNC_RTO_MS_C = 375", "SYNC_RTO_MS_C = 376"), 1),
    ("rom_formatted_stale", lambda t: edit(t, "docs/MANAGER.md", "| Shipping | 1,022 of 1,024 | 2 |", "| Shipping | **1,021** of 1,024 | 3 |"), 1),
    ("rom_duplicate_row", lambda t: edit(t, "docs/MANAGER.md", "| Shipping | 1,022 of 1,024 | 2 |\n", "| Shipping | 1,022 of 1,024 | 2 |\n| Shipping | 1,022 of 1,024 | 2 |\n"), 1),
    ("copy_hdl_prose", lambda t: edit(t, "docs/HDL_DEVELOPER.md", "Every usable Sync pair restarts it, in either role.\n", "Every usable Sync pair restarts it, in either role.\n\nThat watch lasts 375 ms.\n"), 1),
    ("copy_threshold_table", lambda t: edit(t, "docs/INTEGRATION.md", "| Link-up | [`STEP_LINKUP_NS_C`](#protocol-constants) |", "| Link-up | 20 us |"), 1),
    ("copy_spelled_minutes", lambda t: edit(t, "docs/INTEGRATION.md", "The [`CEASE_MS_C`](#protocol-constants) countdown remains the other exit.", "The five-minute countdown remains the other exit."), 1),
    ("copy_test_ppm", lambda t: edit(t, "docs/TEST_DEVELOPER.md", "- Keeps every written addend inside [`RATE_PPM_C`](INTEGRATION.md#protocol-constants).", "- Keeps every written addend inside 200 ppm."), 1),
    ("copy_band_ns", lambda t: edit(t, "docs/INTEGRATION.md", "Its inclusive tracking band is ±[`SLEW_SETTLED_NS_C`](#protocol-constants) around zero.", "Its tracking band is inclusive: -100 ns through +100 ns."), 1),
    ("status_row_missing", lambda t: edit(t, "docs/README.md", "| `tb/tsngen/README.md` |", "| `tb/tsngen/GONE.md` |"), 1),
]

CHECKER = [
    ("required_set_removed", "        for name in CONSTANTS\n        if name not in seen", "        for name in ()\n        if name not in seen"),
    ("old_numeric_row_regex", 'CONSTANT_ROW_RE = re.compile(r"^\\|\\s*`([A-Za-z_][A-Za-z0-9_]*)`\\s*\\|\\s*([^|]*?)\\s*\\|")', 'CONSTANT_ROW_RE = re.compile(r"^\\|\\s*`([A-Z][A-Z0-9_]*)`\\s*\\|\\s*([0-9][0-9,]*)\\s*\\|")'),
    ("decimal_accepts_markup", '    cell = cell.strip()\n', '    cell = cell.strip().strip("*").split()[0].lstrip("-") if cell.strip() else cell\n'),
    ("home_not_excluded", "            if fenced or home:\n", "            if fenced:\n"),
    ("no_unit_conversion", '        numbers.append((value // 1000, "(?:us|\\u00b5s|\\u03bcs)"))\n', "        pass\n"),
    ("no_minute_words", '        patterns += [rf"\\b{minutes}[\\s-]min", rf"\\b{word}[\\s-]minutes?\\b"]\n', "        pass\n"),
    ("rom_duplicate_ignored", '            findings.append(f"{ROM_PAGE}: duplicate ROM budget row: {image}")\n', "            pass\n"),
]

failures = 0
print(f"head {head}; old checker from {old_rev}")
print("## real-tree defects: new checker rc, old checker rc, first finding")
for name, mutate, want in TREE:
    tree = fresh(name)
    mutate(tree)
    rc, out = run(tree)
    (tree / "old_check_docs.py").write_text(old_checker)
    (tree / "scripts" / "old_check_docs.py").write_text(old_checker)
    old_rc, _ = run(tree, checker="scripts/old_check_docs.py")
    finding = next((line.strip() for line in out if line.startswith("  ")), out[-1] if out else "")
    ok = rc == want
    failures += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {name}: rc {rc} (want {want}); old rc {old_rc}; {finding}")
    subprocess.run(["rm", "-rf", str(tree)], check=True)

print("## checker mutants: --selftest rc and message")
for name, old, new in CHECKER:
    tree = fresh("checker_" + name)
    edit(tree, "scripts/check_docs.py", old, new)
    rc, out = run(tree, "--selftest")
    ok = rc != 0
    failures += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {name}: selftest rc {rc}; {out[-1] if out else ''}")
    subprocess.run(["rm", "-rf", str(tree)], check=True)

print(f"probe failures: {failures}")
sys.exit(1 if failures else 0)
