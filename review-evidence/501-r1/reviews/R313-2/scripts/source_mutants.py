#!/usr/bin/env python3
"""Reviewer probe (R313-1): disposable source mutants on a COPY of the head tree.

Usage: python3 source_mutants.py <head-tree-copy> <verilator-dir>

Each mutant is one exact-text replacement (asserted unique), applied to the
copy, graded by the named check, then the original bytes are restored and
re-verified by SHA-256. `expect` says whether the check must go red.
Never run against the review clone.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

T = Path(sys.argv[1]).resolve()
VDIR = sys.argv[2]
env = dict(os.environ, PATH=f"{VDIR}:{os.environ['PATH']}")
GATE = ["python3", "scripts/check_nvm_record_space.py"]
FWT = ["python3", "sw/firmware/nvm_hosttest/test_nvm_firmware.py"]
COSIM = ["python3", "-B", "tb/verilator/nvm_cosim/run_cases.py", "--shapes", "8x8",
         "--jobs", "2", "--pool", "4", "--skip-mutants"]
FW = "sw/firmware/milan_baremetal/milan_baremetal.c"
MUTANTS = [
    # (name, file, old, new, [(check, cwd-rel, expect_red, needle)])
    ("gate_accept_oversize", "scripts/nvm_klj2.py",
     "if key is None or key not in expect or expect[key] != plen:",
     "if key is None or key not in expect or expect[key] < plen and False:",
     [(GATE, ".", True, "over-capacity journal was not refused atomically")]),
    ("shape_one_short", "scripts/nvm_shape.py",
     "return max(port[\"clusters\"], shape.dc[\"STREAM_OUTPUT\"] * 8)",
     "return max(port[\"clusters\"], shape.dc[\"STREAM_OUTPUT\"] * 8) - 1",
     [(GATE, ".", True, "cannot save 72 keys in 71 entries")]),
    ("restore_drops_last", "scripts/nvm_map_checks.py",
     "        restored[stream, channel] = (cluster, cluster_channel)\n    return restored",
     "        restored[stream, channel] = (cluster, cluster_channel)\n"
     "    restored.pop(next(reversed(restored)), None)\n    return restored",
     [(GATE, ".", True, "cleared-first map restore lost keys")]),
    ("restore_nothing", "scripts/nvm_map_checks.py",
     "    live.update(_restore(applied[group, port]))",
     "    live.update({})",
     [(GATE, ".", True, "cleared-first map restore lost keys")]),
    ("fw_out_table_uses_in_entries", FW,
     "unsigned int entries = dir ? nvm_mapout_entries[k] :\n\t\t\t\t\t\tnvm_mapin_entries[k];",
     "unsigned int entries = nvm_mapin_entries[k];",
     [(FWT, ".", True, ""), (COSIM, ".", True, "")]),
    ("fw_out_plen_old_nine", FW,
     "\t\treturn NVM_MAP_ENTRY * nvm_mapout_entries[index & 0xfu];",
     "\t\treturn NVM_MAP_ENTRY * 9u;",
     [(FWT, ".", True, "")]),
]

results = []
for name, rel, old, new, checks in MUTANTS:
    path = T / rel
    orig = path.read_bytes()
    text = orig.decode()
    n = text.count(old)
    if n != 1:
        results.append(f"{name}: SETUP FAILED ({n} matches)")
        continue
    path.write_text(text.replace(old, new))
    try:
        for argv, cwd, expect_red, needle in checks:
            r = subprocess.run(argv, cwd=T / cwd, env=env, capture_output=True, text=True)
            outp = r.stdout + r.stderr
            red = r.returncode != 0
            named = (needle in outp) if needle else True
            ok = (red == expect_red) and (named or not expect_red)
            first = next((ln for ln in outp.splitlines()
                          if "FINDING" in ln or "FAIL" in ln or "Error" in ln), "")
            label = " ".join(Path(argv[2 if argv[1] == "-B" else 1]).name.split())
            results.append(f"{name} [{label}]: rc={r.returncode} "
                           f"red={red} expected_red={expect_red} named={named} -> "
                           f"{'AS EXPECTED' if ok else 'UNEXPECTED'}; first: {first[:220]}")
            (T.parent / f"mut_{name}_{len(results)}.log").write_text(outp)
    finally:
        path.write_bytes(orig)
        assert hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(orig).digest()
print("\n".join(results))
print("restored all mutated files to original bytes")
