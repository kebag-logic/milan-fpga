#!/usr/bin/env python3
"""R363-3: my round-2 mutants whose anchors changed at 7a051e61, re-anchored to the
head code implementing the same rule. Usage as r2scripts/reviewer_mutants.py:
r3_reanchored.py <clone> <scratch-dir> <probe.py>. KILLED = self-test rc != 0."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "r2scripts"))
import reviewer_mutants as runner  # noqa: E402

runner.MUTANTS = (
    ("M07r history resolution ceiling raised to 0.5",
     "or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):",
     "or not 0 <= observation_resolution_s < 0.5):"),
    ("M11r tu resolution limit uses the 0.5 s bound only",
     "    resolution_limit_s = RELEASE_TU_RESOLUTION_LIMIT_S\n",
     "    resolution_limit_s = 0.5\n"),
    ("M13r mr resolution limit is the full second",
     "    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S / 2\n    detail = {",
     "    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S\n    detail = {"),
    ("M28r history empty-interval coarse-resolution guard removed",
     "            or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):",
     "            or not 0 <= observation_resolution_s):"),
    ("M29 tu limit restored to the round-2 one-sided value (0.25)",
     "RELEASE_TU_RESOLUTION_LIMIT_S = 0.25 / 2", "RELEASE_TU_RESOLUTION_LIMIT_S = min(0.25, 0.5)"),
    ("M30 upper bound restored to the round-2 one-sided compare",
     'return ("PASS" if latest_clear_s <= deadline_s else "FAIL", detail)',
     'return ("PASS" if clear_s <= deadline_s else "FAIL", detail)'),
)

if __name__ == "__main__":
    raise SystemExit(runner.main())
