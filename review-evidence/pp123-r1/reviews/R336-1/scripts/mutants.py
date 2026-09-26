#!/usr/bin/env python3
"""Mutation probes for the body/key check. Usage: mutants.py <head-tree> <scratch> <receipts>

Each mutant is a copy of the exported head tree with exactly one textual edit
(asserted to apply once). For every mutant the six new tests are run one by one,
and `make generator-check` plus the suite's default `make` target are run as
the repository's entry points. The expectation column says which tests must
fail; a mutant is KILLED when the entry points exit non-zero and exactly the
expected tests fail (legal tests must keep passing unless listed).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HEAD, SCRATCH, RECEIPTS = (Path(a).resolve() for a in sys.argv[1:4])
GEN = "hdl/aecp/desc/gen_desc_image.py"
TESTS = ["test_legal_fields", "test_legal_bytes",
         "test_type_mismatch_fields", "test_type_mismatch_bytes",
         "test_index_mismatch_fields", "test_index_mismatch_bytes"]
CHECK = '''        if (body_type, body_index) != (typ, idx):
            raise ImageError('''
ALL_REFUSALS = TESTS[2:]

MUTANTS = {
    # The author's mutant: remove the comparison and its ImageError.
    "M0-remove-check": (GEN, '''        body_type = int.from_bytes(body[0:2], "big")
        body_index = int.from_bytes(body[2:4], "big")
        if (body_type, body_index) != (typ, idx):
            raise ImageError(
                f"cfg {cfg} directory key type 0x{typ:04X} index {idx} "
                f"disagrees with body type 0x{body_type:04X} "
                f"index {body_index}")
''', "", ALL_REFUSALS),
    "M1-type-only": (GEN, CHECK, '''        if body_type != typ:
            raise ImageError(''', TESTS[4:]),
    "M2-index-only": (GEN, CHECK, '''        if body_index != idx:
            raise ImageError(''', TESTS[2:4]),
    "M3-low-byte-only": (GEN, CHECK, '''        if (body_type & 0xFF, body_index & 0xFF) != (typ & 0xFF, idx & 0xFF):
            raise ImageError(''', ALL_REFUSALS),
    "M4-fields-form-only": (GEN, CHECK, '''        if "bytes" not in desc and (body_type, body_index) != (typ, idx):
            raise ImageError(''', ["test_type_mismatch_bytes", "test_index_mismatch_bytes"]),
    "M5-bytes-form-only": (GEN, CHECK, '''        if "bytes" in desc and (body_type, body_index) != (typ, idx):
            raise ImageError(''', ["test_type_mismatch_fields", "test_index_mismatch_fields"]),
    "M6-message-drops-cfg": (GEN, 'f"cfg {cfg} directory key type', 'f"directory key type', ALL_REFUSALS),
    "M7-wrong-exception": (GEN, CHECK, '''        if (body_type, body_index) != (typ, idx):
            raise ValueError(''', ALL_REFUSALS),
    "M8-type-slice-off-by-one": (GEN, 'body_type = int.from_bytes(body[0:2], "big")',
                                 'body_type = int.from_bytes(body[1:3], "big")',
                                 TESTS),
    "M9-cli-writes-before-build": (GEN, '''    try:
        img, report = build(model, args.line_bytes)''', '''    open(args.out, "wb").close()
    try:
        img, report = build(model, args.line_bytes)''', ALL_REFUSALS),
    "M10-over-strict-cfg0-only": (GEN, CHECK, '''        if (body_type, body_index) != (typ, idx) or cfg != 0:
            raise ImageError(''', TESTS),
}


def run(cmd, cwd, log):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900)
    log.write(f"$ {' '.join(cmd)}  (cwd {cwd.relative_to(SCRATCH)})\n"
              f"{p.stdout}{p.stderr}rc={p.returncode}\n\n")
    return p.returncode


def main():
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, (path, old, new, expect_fail) in MUTANTS.items():
        tree = SCRATCH / f"mut-{name}"
        shutil.rmtree(tree, ignore_errors=True)
        shutil.copytree(HEAD, tree, symlinks=True)
        src = (tree / path).read_text()
        assert src.count(old) == 1, (name, src.count(old))
        (tree / path).write_text(src.replace(old, new))
        tb = tree / "tb/desc_store"
        with open(RECEIPTS / f"mutant-{name}.log", "w") as log:
            per_test = {t: run([sys.executable, "-B", "test_gen_desc_image.py",
                                f"BodyKeyTest.{t}"], tb, log) for t in TESTS}
            gc = run(["make", "generator-check"], tb, log)
            dflt = run(["make"], tb, log)
        failed = sorted(t for t, rc in per_test.items() if rc != 0)
        killed = gc != 0 and dflt != 0 and failed == sorted(expect_fail)
        results[name] = {"failed_tests": failed, "expected_failed": sorted(expect_fail),
                         "generator_check_rc": gc, "make_default_rc": dflt,
                         "verdict": "KILLED as expected" if killed else "UNEXPECTED"}
        print(f"{name:30} {results[name]['verdict']:20} gen-check rc {gc}  "
              f"make rc {dflt}  failed {len(failed)}/6")
    (RECEIPTS / "mutants.json").write_text(json.dumps(results, indent=1) + "\n")
    return 0 if all(r["verdict"].startswith("KILLED") for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
