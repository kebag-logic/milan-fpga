#!/usr/bin/env python3
"""The six R699-1 reviewer mutants whose round-1 anchors the rewrite removed,
re-anchored on the same defect in the new code, through the reviewer's own
unchanged runner (r699_reviewer_mutants.run: self-test and plan feature).

Usage: python3 -I r699_equivalents.py <pristine export root> <work dir>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r699_reviewer_mutants as reviewer  # noqa: E402

EQUIVALENTS = [
    ("G01 bit-flip resolution removed (a lone corrupted word stays a slip pair)",
     'if span[0][0] == "bad" or _audio_duplicate(track, labels, k):', "if True:"),
    ("G03 inserted silence never detected",
     "inserted = None if current is None or ahead[k] is None else ahead[k] == current - extra",
     "inserted = None if current is None or ahead[k] is None else False"),
    ("G04 swap detection removed", "        elif partner is not None:\n", "        elif False:\n"),
    ("G05 both-ends rule removed",
     'if any(end != {"dropped", "repeated", "bit-flip"} for end in ends):', "if False:"),
    ("G08 arm tolerance widened by 100",
     'or event["channel"] not in want or not _audio_at(event, arm["index"], tolerance)):',
     'or event["channel"] not in want or not _audio_at(event, arm["index"], tolerance + 100)):'),
    ("G09 fast path compares one frame",
     "and column.tobytes() == _audio_expected_bytes(slot.tag, slot.position, count)):",
     "and column[:1].tobytes() == _audio_expected_bytes(slot.tag, slot.position, 1)):"),
]
root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
results = [reviewer.run(root, work, 50 + k, mutant) for k, mutant in enumerate(EQUIVALENTS)]
for name, verdict, why in results:
    print(f"{verdict}: {name} ({why})")
print(f"SUMMARY: {sum(v == 'KILLED' for _, v, _ in results)} of {len(results)} killed")
