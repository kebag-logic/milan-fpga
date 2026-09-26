#!/usr/bin/env python3
"""Reviewer probe for round 3: partial-strength weakenings of the refusals the
round claims (one direction of each uniqueness test, value-deduplication, and
alternative microcode depth derivations). A surviving mutant marks a behaviour
the self-test cannot distinguish; its practical impact is judged in REPORT.md.
usage: delta_probe_mutants.py <path/to/syn/ooc/pp_baseline.py>"""
import ast
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = "        if len(matches) != 1 or len(packages) != 1:\n"
HITS = "    if len(hits) != 1:\n"
MUTANTS = {
    "binding: allow duplicates (len<1 only)": (GUARD, "        if len(matches) < 1 or len(packages) != 1:\n"),
    "binding: allow missing (len>1 only)": (GUARD, "        if len(matches) > 1 or len(packages) != 1:\n"),
    "package: allow duplicates (len<1 only)": (GUARD, "        if len(matches) != 1 or len(packages) < 1:\n"),
    "package: allow missing (len>1 only)": (GUARD, "        if len(matches) != 1 or len(packages) > 1:\n"),
    "package: dedupe by path": (GUARD, "        packages = list(dict.fromkeys(packages))\n" + GUARD),
    "package: dedupe by content": (
        GUARD, "        packages = list({p.read_text(): p for p in packages}.values())\n" + GUARD),
    "binding: dedupe by value": (GUARD, "        matches = list(dict.fromkeys(matches))\n" + GUARD),
    "declaration: allow duplicates (len<1 only)": (HITS, "    if len(hits) < 1:\n"),
    "declaration: allow missing (len>1 only)": (HITS, "    if len(hits) > 1:\n"),
    "declaration: dedupe identical values": (HITS, "    hits = sorted(set(hits))\n" + HITS),
    "declaration: first hit wins": (HITS, "    hits = hits[:1]\n" + HITS),
    "microcode depth: 2*UPC_W_C": ("            count = 1 << count\n", "            count = 2 * count\n"),
    "microcode depth: UPC_W_C+1": ("            count = 1 << count\n", "            count = count + 1\n"),
    "generated ROM: words/width swapped": (
        "inputs.append(image_record(path, int(words), int(width)))",
        "inputs.append(image_record(path, int(width), int(words)))"),
    "generated ROM: skip when name contains rom": (
        '        if name == "sram":\n', '        if name != "rom" and name == "sram":\n'),
    "readmemh: subset instead of equality": (
        '    if expected != {Path(row["path"]).name for row in inputs}:\n',
        '    if not expected <= {Path(row["path"]).name for row in inputs}:\n'),
    "package width read from depth": (
        "                                   package_number(text, width)))\n",
        "                                   package_number(text, width) and None))\n"),
}


def main() -> None:
    source = Path(sys.argv[1]).read_text()
    with tempfile.TemporaryDirectory(prefix="r332-4-delta-") as tmp:
        for index, (name, change) in enumerate([("control", None), *MUTANTS.items()]):
            changed = source
            if change:
                old, new = change
                assert source.count(old) == 1, f"not unique: {name}"
                changed = source.replace(old, new)
            ast.parse(changed)
            target = Path(tmp) / str(index) / "syn/ooc/pp_baseline.py"
            target.parent.mkdir(parents=True)
            target.write_text(changed)
            r = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                               capture_output=True, text=True, timeout=120)
            lines = [line for line in r.stderr.splitlines() if line.strip()]
            last = lines[-1] if lines else ""
            verdict = ("control-pass" if r.returncode == 0 else "CONTROL-FAIL") if change is None \
                else ("killed" if r.returncode != 0 else "SURVIVED")
            print(f"{name}\trc={r.returncode}\t{verdict}\t{last}")


if __name__ == "__main__":
    main()
