#!/usr/bin/env python3
"""Remove only the body/key refusal, run the same probes, then restore it."""
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
out = Path(__file__).resolve().parent
source = root / "hdl/aecp/desc/gen_desc_image.py"
original = source.read_bytes()
text = original.decode()
start = text.index('        body_type = int.from_bytes(body[0:2], "big")\n')
end = text.index('        nidx = _u(desc.get("name_index", NAME_NONE))', start)
removed = text[start:end]
assert removed.count("raise ImageError(") == 1
mutant = text[:start] + text[end:]
(out / "mutant.patch").write_text("".join(difflib.unified_diff(
    text.splitlines(keepends=True), mutant.splitlines(keepends=True),
    fromfile="a/hdl/aecp/desc/gen_desc_image.py",
    tofile="b/hdl/aecp/desc/gen_desc_image.py")))
cases = (
    ("mutant-legal", [sys.executable, "-B", "test_gen_desc_image.py",
                      "BodyKeyTest.test_legal_fields", "BodyKeyTest.test_legal_bytes"], 0),
    ("mutant-type", [sys.executable, "-B", "test_gen_desc_image.py",
                     "BodyKeyTest.test_type_mismatch_fields",
                     "BodyKeyTest.test_type_mismatch_bytes"], 1),
    ("mutant-index", [sys.executable, "-B", "test_gen_desc_image.py",
                      "BodyKeyTest.test_index_mismatch_fields",
                      "BodyKeyTest.test_index_mismatch_bytes"], 1),
    ("mutant-entry", ["make", "generator-check"], 2),
)
results = {}
try:
    source.write_text(mutant)
    for label, command, expected in cases:
        log = out / (label + ".log")
        with log.open("w") as stream:
            result = subprocess.run(command, cwd=root / "tb/desc_store",
                                    stdout=stream, stderr=subprocess.STDOUT,
                                    timeout=7200)
            stream.write(f"\nReturn code: {result.returncode}\n")
        output = log.read_text()
        assert result.returncode == expected, (label, result.returncode, expected)
        if label in ("mutant-type", "mutant-index"):
            assert "FAILED (failures=8)" in output
            assert output.count("AssertionError: ImageError not raised") == 8
        if label == "mutant-entry":
            assert "FAILED (failures=16)" in output
        results[label] = {"command": command, "returncode": result.returncode,
                          "expected": expected}
        print(f"{label}: rc {result.returncode}, expected {expected}")
finally:
    source.write_bytes(original)
assert source.read_bytes() == original
results["source_restored_sha256"] = hashlib.sha256(original).hexdigest()
(out / "mutant-results.json").write_text(json.dumps(results, indent=2) + "\n")
print("Original source restored byte-for-byte")
