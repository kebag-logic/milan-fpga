"""Print every check from a temporary, otherwise byte-identical harness."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tarfile
import tempfile

repo = Path(sys.argv[1]).resolve()
label = sys.argv[2]
out = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix="gptp75-a281-check-trace-") as td:
    work = Path(td)
    archive = work / "source.tar"
    subprocess.run(["git", "archive", "HEAD", "-o", str(archive)], cwd=repo, check=True, timeout=60)
    tree = work / "tree"
    tree.mkdir()
    with tarfile.open(archive) as source:
        source.extractall(tree, filter="data")
    relative = "tb/verilator/engine/sim_main.cpp"
    original = (repo / relative).read_text()
    marker = "  void expect(const char *what, uint64_t got, uint64_t exp) {\n    checks++;"
    assert original.count(marker) == 1
    traced = original.replace(marker, marker + '\n    printf("CHECK %04d %s\\n", checks, what);')
    (tree / relative).write_text(traced)
    (out / (label + "-trace-instrumentation.diff")).write_text(
        "Added after checks++ in expect():\n" + 'printf("CHECK %04d %s\\n", checks, what);\n')
    env = dict(os.environ)
    env["PATH"] = "$VALIDATION_TOOLS/verilator-v5.050/bin:" + env["PATH"]
    with (out / (label + "-traced-engine.log")).open("w") as log:
        result = subprocess.run(["make", "-C", "tb/verilator/engine", "run"], cwd=tree,
                                env=env, stdout=log, stderr=subprocess.STDOUT, timeout=10800)
    lines = (out / (label + "-traced-engine.log")).read_text().splitlines()
    checks = [line for line in lines if line.startswith("CHECK ")]
    tallies = [line for line in lines if " checks:" in line]
    (out / (label + "-engine-checks.txt")).write_text("\n".join(checks) + "\n")
    (out / (label + "-engine-tallies.txt")).write_text("\n".join(tallies) + "\n")
    print(json.dumps({"returncode": result.returncode, "checks": len(checks), "tallies": tallies}), flush=True)
    assert result.returncode == 0
    assert len(checks) == 1613 * 3
    assert tallies == ["1613 checks: 1613 PASS, 0 FAIL"] * 3
