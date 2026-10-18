#!/usr/bin/env python3
"""Independently audit the pinned public packet and falsify its index checks."""
import hashlib
import importlib.util
import json
import pathlib
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
out = pathlib.Path(__file__).resolve().parents[1]
source = pathlib.Path(sys.argv[1]).resolve()
public = out / "scratch/public"
author = public / "author-r3"
assert author.is_dir(), "run fetch_packet.py first"
manifest = json.loads((public / "MANIFEST.json").read_text())
rows = [r for r in manifest if r["file"].startswith("author-r3/")]
assert len(rows) == 313
for row in rows:
    assert hashlib.sha256((public / row["file"]).read_bytes()).hexdigest() == row["published_sha256"], row["file"]
print("PASS publication manifest: 313 exact published hashes")

fixture = out / "scratch/index-fixture"
if fixture.exists():
    shutil.rmtree(fixture)
shutil.copytree(author, fixture)
target = fixture / "receipts/r3/gates/head/bench.rc"
original = target.read_bytes()
for verifier in ["receipts/scripts/verify_receipts.py", "receipts/r3/scripts/verify_receipts.py"]:
    for case, expected in [("clean", 0), ("changed", 1), ("missing", 1), ("extra", 1)]:
        target.write_bytes(original)
        extra = fixture / "unexpected-file"
        extra.unlink(missing_ok=True)
        if case == "changed":
            target.write_bytes(b"1\n")
        elif case == "missing":
            target.unlink()
        elif case == "extra":
            extra.write_text("unexpected\n")
        result = subprocess.run([sys.executable, str(author / verifier), str(fixture)], capture_output=True, text=True)
        assert result.returncode == expected, (verifier, case, result.stdout, result.stderr)
        print(verifier, case, "rc=" + str(result.returncode), result.stdout.strip().replace("\n", "; "))
    target.write_bytes(original)
    extra.unlink(missing_ok=True)

spec = importlib.util.spec_from_file_location("engine_mutants", source / "tb/verilator/engine/mutants.py")
mutants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutants)
gates = author / "receipts/r3/gates/head"
logs = "\n".join(p.read_text() for p in sorted(gates.glob("engine-mutants-s*.log")))
assert logs.count("[PASS] the unmutated engine still passes the harness") == 18
caught = re.findall(r"^\[PASS\] mutant caught: (.*?) - breaks ", logs, re.M)
assert len(caught) == len(set(caught)) == len(mutants.MUTATIONS) == 58
assert set(caught) == {m[0] for m in mutants.MUTATIONS}
for name, file, pattern, replacement, breaks in mutants.MUTATIONS:
    assert (source / "hdl" / file).read_text().count(pattern) == 1, name
print("PASS all 58 current mutation names caught exactly once; 18 clean shard controls; all source anchors unique")
for tag, expected in [("drop_keeps_flags", ["the drop commit's flags are gmPresent alone"]),
                      ("held_no_rearm", ["once capable, with no Announce, master in 3 s", "that mastership names thisClock, {thisClock}"])]:
    text = (author / f"receipts/r3/controls/reviewer-probe-{tag}.log").read_text()
    assert f"probe={tag} harness_rc=1" in text
    for name in expected:
        assert any(line.startswith("FAIL #82 Pdelay loss: ") and name in line for line in text.splitlines())
    print("PASS named failing public probe", tag)
engine = (gates / "engine.log").read_text()
assert engine.count("1642 checks: 1642 PASS, 0 FAIL") == 3
assert "46 checks: 46 PASS, 0 FAIL" in engine
assert engine.count("the fall commits flags 9") == 4
assert engine.count("1970 cycles later with flags 1") == 3
assert engine.count("mastership commits 2000682 cycles") == 3
print("PASS exact-head engine: 1642 x 3 and 46; sync-ok at all four falls; correct self flags and recovery timing")

summary = {}
for directory in ["receipts/r3/gates/head", "receipts/r3/pgates/head", "receipts/r3/gates/base", "receipts/pgates/base"]:
    values = {p.name: int(p.read_text().strip()) for p in sorted((author / directory).glob("*.rc"))}
    summary[directory] = values
    nonzero = {k: v for k, v in values.items() if v}
    print(directory, "exit receipts", len(values), "nonzero", nonzero)
    if directory.endswith("gates/head") and "/pgates/" not in directory:
        assert not nonzero
    if directory == "receipts/r3/pgates/head":
        assert nonzero == {"milan_dp-gptp-dev-tests.rc": 2}
(out / "receipts/gate-exit-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print("PASS packet audit and all falsification cases")
