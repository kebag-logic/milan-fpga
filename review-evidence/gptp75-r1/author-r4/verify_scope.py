"""Verify the round changes only the specified statements' organization."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

out = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve()
base = json.loads((out / "baseline-source-sha256.json").read_text())
changed = [path for path, digest in base["files"].items()
           if hashlib.sha256((repo / path).read_bytes()).hexdigest() != digest]
assert sorted(changed) == ["scripts/check_source_evidence.py", "tb/verilator/engine/sim_main.cpp"]
path = "tb/verilator/engine/sim_main.cpp"
before = subprocess.run(["git", "show", base["head"] + ":" + path], cwd=repo, capture_output=True, text=True, check=True, timeout=60).stdout
after = (repo / path).read_text()
pattern = r"  void exercise_the_slew_level_contract\(\) \{\n(.*?)\n  \}"
old = re.search(pattern, before, re.S)
new = re.search(pattern, after, re.S)
phases = re.findall(r"^    (\w+)\(\);$", new.group(1), re.M)
assert len(phases) == 8
expanded = []
lengths = {"exercise_the_slew_level_contract": len(new.group().splitlines())}
for name in phases:
    match = re.search(r"  void " + name + r"\(\) \{\n(.*?)\n  \}", after, re.S)
    assert match
    expanded.extend(match.group(1).splitlines())
    lengths[name] = len(match.group().splitlines())
assert all(length < 100 for length in lengths.values())
assert [line for line in old.group(1).splitlines() if line.strip()] == [line for line in expanded if line.strip()]
comment = "  // Each phase continues from the state left by its predecessor.\n"
assert before[:old.start()] == after[:new.start()].removesuffix(comment)
end = after.index("\n  void slew_probe_unconsumed()", new.end())
assert before[old.end():] == after[end - 1:]
result = {"changed_files": changed, "unchanged_files": len(base["files"]) - len(changed),
          "phase_lines": lengths, "expanded_phase_statements_identical": True,
          "code_outside_split_identical": True}
(out / "scope-verification.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
