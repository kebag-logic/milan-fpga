"""Compare every generated artifact of the five configurations to the base."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile

root = Path.cwd().resolve()
sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb

baseline = json.loads(Path(__file__).with_name("baseline-sha256.json").read_text())
actual = {}
with tempfile.TemporaryDirectory(prefix="582-identity-") as tmp:
    for path in sorted((root / "configs").glob("endstation_*.yaml")):
        result = eb.build(path, tmp, write_fragment=False)
        files = {name: hashlib.sha256(Path(value).read_bytes()).hexdigest()
                 for name, value in sorted(result["paths"].items())}
        digest = hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        actual[path.stem] = {"files": files, "sha256": digest}
        assert actual[path.stem] == baseline[path.stem], f"artifact drift: {path.stem}"
        print(f"IDENTICAL {path.stem}: {len(files)} artifacts; sha256 {digest}")
assert actual == baseline, "configuration set changed"
Path(__file__).with_name("final-sha256.json").write_text(json.dumps(actual, indent=2) + "\n")
print("PASS: all five configuration artifact sets are byte-identical to the base")
