#!/usr/bin/env python3
"""Mutation probe for check_baremetal_only.py's HOST_MEMORY_READS declarations.

Usage: python3 baremetal_mask_probe.py <checkout> <python>
Each mutant rewrites the gate in place, runs --check and --selftest, and restores
the exact original bytes. Prints one result line per mutant.
"""
import pathlib
import subprocess
import sys

checkout = pathlib.Path(sys.argv[1])
python = sys.argv[2]
gate = checkout / "scripts" / "check_baremetal_only.py"
original = gate.read_bytes()
ANCHOR = "HOST_RUNTIME_MASKS = with_declared_lines(HOST_RUNTIME_MASKS, HOST_MEMORY_READS)\n"

MUTANTS = {
    # every declared line accepted in every declared file, not only its own
    "lines pooled across the declared files":
        (ANCHOR, "HOST_RUNTIME_MASKS = with_declared_lines(HOST_RUNTIME_MASKS, {p: tuple(l for ls in "
                 "HOST_MEMORY_READS.values() for l in ls) for p in HOST_MEMORY_READS})\n"),
    # the declared lines accepted in any file at all
    "declared lines accepted in every file":
        ("        runtime_mask = HOST_RUNTIME_MASKS.get(path)\n",
         "        runtime_mask = HOST_RUNTIME_MASKS.get(path) or re.compile(declared_line_mask("
         "tuple(l for ls in HOST_MEMORY_READS.values() for l in ls)))\n"),
    # the declaration also copied onto the first product document
    "declared lines accepted in a product document":
        (ANCHOR, "HOST_RUNTIME_MASKS = with_declared_lines(HOST_RUNTIME_MASKS, {**HOST_MEMORY_READS, "
                 "PRODUCT_DOCS[0]: tuple(l for ls in HOST_MEMORY_READS.values() for l in ls)})\n"),
    # only the first path on each declared line is bound; a second is masked anywhere
    "second path on a line masked unbound":
        ("        for line in lines for m in TARGET_OS_PATH_RE.finditer(line))\n",
         "        for line in lines for m in TARGET_OS_PATH_RE.finditer(line)) + '|/sys(?=/fs/cgroup)'\n"),
    # the runner's earlier masks dropped when the declarations merge
    "earlier per-file mask replaced, not extended":
        ('        merged[path] = re.compile(("" if known is None else known.pattern + "|") + declared_line_mask(lines))\n',
         '        merged[path] = re.compile(declared_line_mask(lines))\n'),
}


def run(*args: str) -> tuple[int, str]:
    done = subprocess.run([python, str(gate), *args], cwd=checkout, capture_output=True, text=True, check=False)
    out = (done.stdout + done.stderr).strip().splitlines()
    return done.returncode, (out[0] if out else "")[:160] + f" ({len(out)} line(s))"


try:
    for name, (old, new) in MUTANTS.items():
        text = original.decode()
        assert text.count(old) == 1, name
        gate.write_text(text.replace(old, new))
        check = run("--check")
        selftest = run("--selftest")
        caught = check[0] != 0 or selftest[0] != 0
        print(f"{'CAUGHT' if caught else 'SURVIVED'}: {name}")
        print(f"  --check rc {check[0]}: {check[1]}")
        print(f"  --selftest rc {selftest[0]}: {selftest[1]}")
finally:
    gate.write_bytes(original)
print("restored:", gate.read_bytes() == original)
