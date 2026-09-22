"""Re-evaluate all 31 public repositories for each of ten production guard mutations."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent.parent
checkout = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(checkout / "scripts"))
from merge_containment_selftest_mutations import MUTATIONS

checker = checkout / "scripts/check_merge_containment.py"
source = checkout / "scripts/merge_containment_replay.py"
rows = json.loads((root / "receipts/public-matrix.json").read_text())["rows"]

def evaluate(script):
    results = {}
    for i, row in enumerate(rows, 1):
        command = [sys.executable, "-B", "-I", str(script), "--no-fetch", "--base", "main", "pr"]
        p = subprocess.run(command, cwd=root / "public-fixtures" / row["scenario"],
                           capture_output=True, text=True)
        word = p.stdout.strip().split()[0] if p.stdout.strip() else "NO VERDICT"
        results[i] = dict(exit=p.returncode, word=word, stdout=p.stdout, stderr=p.stderr)
    return results

baseline = evaluate(checker)
record = dict(baseline=baseline, mutations=[])
for name, edits, cases in MUTATIONS:
    text = source.read_text()
    for before, after in edits:
        assert text.count(before) == 1
        text = text.replace(before, after)
    with tempfile.TemporaryDirectory(prefix="mutation-", dir=root) as directory:
        target = Path(directory)
        (target / "checker.py").write_bytes(checker.read_bytes())
        (target / "merge_containment_replay.py").write_text(text)
        actual = evaluate(target / "checker.py")
    changed = {i: dict(before=(baseline[i]["exit"], baseline[i]["word"]),
                       after=(actual[i]["exit"], actual[i]["word"]))
               for i in baseline if (actual[i]["exit"], actual[i]["word"]) !=
                                    (baseline[i]["exit"], baseline[i]["word"])}
    assert set(changed) == set(cases), (name, changed, cases)
    for i, expected in cases.items():
        assert (actual[i]["exit"], actual[i]["word"]) == expected
    record["mutations"].append(dict(guard=name, edits=edits, changed=changed, results=actual))
    print("KILLED", name, changed, flush=True)
(root / "receipts/mutations-matrix.json").write_text(json.dumps(record, indent=2) + "\n")
print("PASS: all 31 fixtures evaluated under baseline plus ten guard mutations (341 CLI runs).")
