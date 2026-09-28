"""Plant one defect at a time in the composed milan_soc.py of a disposable tree
and require the composed builder gates for BOTH predecessor (#577) and this PR
(#395) to catch the defect in their own half, while the other half stays green.

Usage: python3 -B probe_mutations.py <disposable repository root>

Each arm restores the file from git and verifies the tree is clean before the
next arm. The disposable tree must not be the review clone.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
target = root / "sw/litex/milan_soc.py"
RUNNER = """
import sys
sys.path.insert(0, 'sw/builder')
import test_builder as t
fn = getattr(t, sys.argv[1])
fn()
print('RESULT', sys.argv[1], 'PASS', 'skipped:', [s[0] for s in t.SKIPPED])
"""
GATES = ("test_soc_shipping_image_contract", "test_commercial_timing_grade")

CHECK = ("    try:\n        aem_image_checks.validate_shipping_image(blob)\n"
         "    except aem_image_checks.ImageCheckError as exc:\n"
         "        raise RuntimeError(f\"aem_desc.bin: {exc}\") from exc\n")
PLL = 'S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))'
MUTATIONS = {
    "control": None,
    "577_image_check_removed": (CHECK, ""),
    "395_pll_grade_literal": (PLL, "S7PLL(speedgrade=-2)"),
    "both_removed": [(CHECK, ""), (PLL, "S7PLL(speedgrade=-2)")],
}
EXPECT = {
    "control": {GATES[0]: 0, GATES[1]: 0},
    "577_image_check_removed": {GATES[0]: 1, GATES[1]: 0},
    "395_pll_grade_literal": {GATES[0]: 0, GATES[1]: 1},
    "both_removed": {GATES[0]: 1, GATES[1]: 1},
}


def clean() -> None:
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=root,
                            capture_output=True, text=True, check=True).stdout
    assert status == "", status


assert root != Path("$REVIEWS/r373-4-395").resolve(), "refusing the review clone"
clean()
original = target.read_text()
failures = []
for label, edits in MUTATIONS.items():
    text = original
    for old, new in ([edits] if isinstance(edits, tuple) else edits or []):
        assert text.count(old) == 1, (label, old)
        text = text.replace(old, new)
    target.write_text(text)
    try:
        for gate in GATES:
            r = subprocess.run([sys.executable, "-B", "-c", RUNNER, gate], cwd=root,
                               capture_output=True, text=True, timeout=900)
            got = 0 if r.returncode == 0 else 1
            tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
            verdict = "as expected" if got == EXPECT[label][gate] else "UNEXPECTED"
            print(f"[{label}] {gate}: rc={r.returncode} ({'pass' if got == 0 else 'fail'}; {verdict})")
            for line in tail:
                print(f"    {line[:300]}")
            if got != EXPECT[label][gate]:
                failures.append((label, gate))
    finally:
        subprocess.run(["git", "checkout", "--", str(target)], cwd=root, check=True)
        clean()
print("MUTATION PROBE", "PASS" if not failures else f"FAIL {failures}")
sys.exit(1 if failures else 0)
