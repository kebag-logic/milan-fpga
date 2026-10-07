#!/usr/bin/env python3
"""Reviewer-planted mutants of the #654 validation, graded by the PR's own refusal bank.

Usage: mutation_probes.py PYTHON TREE OUT_DIR
TREE is a disposable checkout at the head under review. For each mutant the
recipe sw/litex/milan_soc.py is rewritten in TREE (anchor must match exactly
once), sw/builder/test_soc_options.py is run with PYTHON, and the original
bytes are restored. A mutant is KILLED when the bank exits non-zero; the log
records which assertion fired. Exit 0 only when every mutant is killed and
the recipe bytes are restored to their original digest.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

py, tree, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
soc = tree / "sw/litex/milan_soc.py"
orig = soc.read_bytes()
digest = hashlib.sha256(orig).hexdigest()
CTOR = "        _validate_cpu_options(cpu, with_fpu, l2_bytes)\n"
BIOS = "        # BIOS ROM is always integrated."
CLI = ("    try:\n        _validate_cpu_options(args.cpu, args.with_fpu, args.l2_bytes)\n"
       "    except ValueError as exc:\n        ap.error(str(exc))\n")
PROFILE = ('        ap.error("--software-profile baremetal requires no FPU, --l2-bytes 0, "\n'
           '                 "and no --scala-args overrides")\n')
MUTANTS = [
    ("K1 constructor validation moved after CPU setup",
     [(CTOR, ""), (BIOS, CTOR + BIOS)]),
    ("K2 CLI validation moved after the profile refusals",
     [(CLI, ""), (PROFILE, PROFILE + CLI)]),
    ("K3 CLI raises ValueError instead of a parser exit",
     [("        ap.error(str(exc))\n    if args.cpu", "        raise\n    if args.cpu")]),
    ("K4 finiteness check removed", [("(not math.isfinite(l2_bytes) or", "(False or")]),
    ("K5 negative check removed", [("l2_bytes < 0 or int(l2_bytes)", "False or int(l2_bytes)")]),
    ("K6 whole-number check removed", [("int(l2_bytes) != l2_bytes)", "False)")]),
    ("K7 VexiiRiscv L2 refusal only above 64 KiB",
     [("        if l2_bytes:\n            raise", "        if l2_bytes and l2_bytes > 65536:\n            raise")]),
    ("K8 NaxRiscv zero refusal only with FPU",
     [('if cpu == "naxriscv" and l2_bytes == 0:', 'if cpu == "naxriscv" and l2_bytes == 0 and with_fpu:')]),
    ("K9 over-refusal: NaxRiscv FPU refused",
     [('    if cpu == "naxriscv" and l2_bytes == 0:',
       '    if cpu == "naxriscv" and with_fpu:\n        raise ValueError("planted")\n'
       '    if cpu == "naxriscv" and l2_bytes == 0:')]),
    ("K10 over-refusal: VexiiRiscv explicit zero refused",
     [("        if l2_bytes:\n            raise", "        if l2_bytes is not None:\n            raise")]),
    ("K11 CLI validates the default CPU, not the selected one",
     [("_validate_cpu_options(args.cpu, args.with_fpu", '_validate_cpu_options("vexiiriscv", args.with_fpu')]),
    ("K12 constructor validates as NaxRiscv always",
     [("        _validate_cpu_options(cpu, with_fpu, l2_bytes)", '        _validate_cpu_options("naxriscv", with_fpu, l2_bytes)')]),
]
results, ok = [], True
try:
    for label, edits in MUTANTS:
        text = orig.decode()
        for old, new in edits:
            assert text.count(old) == 1, (label, old, text.count(old))
            text = text.replace(old, new)
        soc.write_text(text)
        run = subprocess.run([py, "sw/builder/test_soc_options.py"], cwd=tree,
                             capture_output=True, text=True, timeout=900)
        soc.write_bytes(orig)
        tag = label.split()[0]
        (out / f"{tag}.log").write_text(run.stdout + run.stderr)
        last = [l for l in (run.stdout + run.stderr).splitlines() if l.strip()][-1:]
        killed = run.returncode != 0
        ok &= killed
        results.append(dict(mutant=label, rc=run.returncode,
                            verdict="KILLED" if killed else "SURVIVED", last_line=last))
        print(f"{'KILLED  ' if killed else 'SURVIVED'} rc={run.returncode} {label} :: {last}", flush=True)
finally:
    soc.write_bytes(orig)
restored = hashlib.sha256(soc.read_bytes()).hexdigest() == digest
print("recipe restored:", restored, digest)
(out / "mutation-results.json").write_text(json.dumps(dict(results=results, restored=restored,
                                                           recipe_sha256=digest), indent=1) + "\n")
sys.exit(0 if ok and restored else 1)
