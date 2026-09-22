import difflib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
evidence = Path(__file__).parent
parent = Path("$VALIDATION_STORAGE/lanes/trusted-dev-20260922-512")
ref = "483a133ed08867ea0d300d2b4a027b5b48a4282f"
identities = []
for name in ("check_cpp_idiom.py", "code_quality_scope.py"):
    rel = "scripts/" + name
    data = (parent / rel).read_bytes()
    expected = subprocess.check_output(
        ["rtk", "proxy", "git", "-C", str(parent), "show", ref + ":" + rel],
        env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"))
    assert data == expected
    identities.append(dict(path=rel, git_blob=hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
        sha256=hashlib.sha256(data).hexdigest(), size=len(data)))
    (evidence / "context" / name).write_bytes(data)
print("Verified parent inputs:", json.dumps(identities))
(evidence / "context" / "checker-inputs.json").write_text(json.dumps(identities, indent=2) + "\n")
spec = importlib.util.spec_from_file_location("parent_cpp", parent / "scripts/check_cpp_idiom.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
make = Path("tb/pp_top/Makefile").read_text()
before = (evidence / "context/Makefile.before").read_text()
supplementary = '-CFLAGS "-DPP_TOP_SRP_DOM_DEF_VID=0x$(SRP_VID_FIXTURE) -Wall -Wextra"'
assert make.count(supplementary) == 1
assert make == before.replace(supplementary.replace(" -Wall -Wextra", ""), supplementary, 1)
results = []
for label, text, expected in (("original", before, ["-Wall", "-Wextra"]),
                               ("corrected", make, [])):
    result = checker.cflags_missing(text)
    print(label, "cflags_missing =", result)
    assert result == expected
    results.append(dict(case=label, missing=result))
for flag in ("-Wall", "-Wextra"):
    mutant = make.replace(supplementary, supplementary.replace(" " + flag, ""), 1)
    with tempfile.TemporaryDirectory(prefix="pp102-flag-", dir=evidence) as temp:
        copy = Path(temp) / "Makefile"
        copy.write_text(mutant)
        result = checker.cflags_missing(copy.read_text())
        print("removed", flag, "in disposable copy:", result)
        assert result == [flag]
        results.append(dict(case="remove " + flag, missing=result,
                            sha256=hashlib.sha256(copy.read_bytes()).hexdigest()))
        (evidence / "context" / ("Makefile.remove-" + flag[1:])).write_bytes(copy.read_bytes())
        (evidence / "context" / ("remove-" + flag[1:] + ".patch")).write_text(
            "".join(difflib.unified_diff(make.splitlines(True), mutant.splitlines(True),
                                        fromfile="corrected/Makefile", tofile="disposable/Makefile")))
assert Path("tb/pp_top/Makefile").read_text() == make
(evidence / "focused-results.json").write_text(json.dumps(results, indent=2) + "\n")
if "--parent-controls" in sys.argv:
    print("Parent warning-flag selftest controls:")
    tally = checker._Tally()
    checker._selftest_warning_flags(tally)
    print(f"{tally.checks} checks: {tally.checks - tally.failures} PASS, {tally.failures} FAIL")
    assert tally.failures == 0
