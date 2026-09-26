"""Require the resolving-path mutant to fail the full offline self-test."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path.cwd()
out = Path(__file__).resolve().parent
source = (repo / "scripts/act_ci.py").read_text(encoding="utf-8")
before = "return str(pathlib.Path(found).absolute())"
assert source.count(before) == 1
with tempfile.TemporaryDirectory(prefix="milan-532-path-mutant-") as raw:
    mutant = Path(raw) / "act_ci.py"
    mutant.write_text(source.replace(before, "return str(pathlib.Path(found).resolve())", 1), encoding="utf-8")
    with (out / "full-mutant.log").open("w") as stream:
        result = subprocess.run(
            ["rtk", "proxy", "python3", "-I", str(mutant), "--selftest", "--worktree", str(repo)],
            cwd=repo, stdout=stream, stderr=subprocess.STDOUT, timeout=3600, check=False,
        )
text = (out / "full-mutant.log").read_text()
failures = [line.strip() for line in text.splitlines() if line.startswith("  FAIL ")]
expected = [
    "FAIL pasta keeps its absolute SAFE_PATH spelling despite an ambient PATH impostor",
    "FAIL the slot uplink's fake multi-call executable observes the invoked name pasta",
]
report = {"rc": result.returncode, "expected_rc": 1, "failures": failures}
(out / "full-mutant-result.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
assert result.returncode == 1 and failures == expected
assert "selftest: 2 FAILURE(S)" in text
print("PASS: resolving-path mutant exits 1 on exactly the two regression arms")
