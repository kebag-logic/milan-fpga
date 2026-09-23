"""Kill the ten public #423 guard mutations against production sources.

Each replica changes only the named guard, then runs the real CLI in the
current fixture repository. Both its exit and its verdict word are asserted;
the tree guard's STRANDED-to-UNKNOWN change intentionally keeps exit 1.
"""

import subprocess
import sys
from pathlib import Path

from merge_containment_selftest_scratch import scratch


# (name, exact source edits, public fixture numbers and mutated expectations)
MUTATIONS = (
    ("merge-count", (("if len(rows) != 1:", "if not rows:"),),
     {3: (0, "contained")}),
    ("parent-count", (("if len(fields) != 3:", "if len(fields) < 3:"),
                      ("merge, first, second = fields", "merge, first, second = fields[:3]")),
     {25: (0, "contained")}),
    ("direct-parent", (("if parents[1:] != [first]:", "if False:"),),
     {28: (0, "contained")}),
    ("merge-tree", (("return merge_tree == second_tree", "return True"),),
     {21: (1, "UNKNOWN"), 22: (0, "contained")}),
    ("historical-proof", (("historical, error = replay(branch, base)", "historical, error = True, None"),),
     {index: (1, "UNKNOWN") for index in range(17, 21)}),
    ("retention-proof", (("unproved = _retained_at_tip(branch, base, git)", "unproved = []"),),
     {index: (0, "contained") for index in range(6, 17)}),
    ("exact-only", (("return _merge_is_noop(original, tip, branch)", "return False"),),
     {1: (1, "UNKNOWN"), 2: (1, "UNKNOWN")}),
    ("mode-rule", (("if not (tip[0] == branch[0]\n"
                    "            or (original is not None and original[0] == branch[0])):",
                    "if False:"),),
     {10: (0, "contained")}),
    ("tip-byte-equality", (("return rc == 0 and merged == blobs[0]", "return rc == 0"),),
     {14: (0, "contained")}),
    ("merge-error", (("raise _MeasurementError(f\"raw merge-file failed (exit {rc})\")", "return True"),),
     {11: (0, "contained")}),
)


def mutation_cases(fx: object, index: int) -> None:
    """Run each applicable weakened replica against this public fixture."""
    source_dir = Path(__file__).resolve().parent
    #! Bytes, not text: the checker carries non-ASCII bytes, and a copy must
    #! not depend on the parent's locale encoding (an ASCII parent crashed).
    checker = (source_dir / "check_merge_containment.py").read_bytes()
    original = (source_dir / "merge_containment_replay.py").read_bytes()
    for name, edits, cases in MUTATIONS:
        if index not in cases:
            continue
        mutated = original
        for before, after in edits:
            before, after = before.encode("ascii"), after.encode("ascii")
            if mutated.count(before) != 1:
                raise RuntimeError(f"mutation {name}: guard no longer has one source location")
            mutated = mutated.replace(before, after)
        with scratch(fx.leftovers) as directory:
            target = Path(directory)
            (target / "checker.py").write_bytes(checker)
            (target / "merge_containment_replay.py").write_bytes(mutated)
            result = subprocess.run((sys.executable, "-B", "-I", str(target / "checker.py"),
                                     "--no-fetch", "--base", "main", "pr"),
                                    capture_output=True, text=True,
                                    errors="backslashreplace")
        lines = [line.split() for line in result.stdout.splitlines() if line.strip()]
        actual = (result.returncode, lines[0][0] if lines else result.stderr.strip())
        fx.case(f"mutation-{name}-{index:02d}", actual, cases[index],
                "weakened production guard changes the verdict, including its words")
