#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 6): at which list index do the generator's note and entry-key cases put their key?

Calls the self-test's own mutate_json() and mutate_report() on its own fixtures (fixtures()), seeds 0 to N-1, and
for every "note" case whose note became a list, and every "entry key" case, records the list index that holds the
written key. Also counts how many of those cases the oracle marks broken. Read-only: nothing of the gate runs.

Usage: probe_r6_generator.py <checkout> <scratch-dir> [N]
"""

from collections import Counter
import json
from pathlib import Path
import random
import sys

REPO, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
N = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
sys.path.insert(0, str(REPO / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402
import pp_resource_gate_selftest as selftest  # noqa: E402


def lenient(data: bytes) -> object:
    """Read a case's JSON, keeping the last of a repeated key and any lone surrogate."""
    return json.loads(data.decode("utf-8", "surrogatepass"))


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    work = SCRATCH / "fixtures"
    if not work.exists():
        work.mkdir()
    targets, base, _ = selftest.fixtures(work) if not (work / "route").exists() else (None, None, None)
    if base is None:
        raise SystemExit("scratch fixtures already exist; pass an empty scratch directory")
    manifest = (targets[0][0] / "baseline_images.json").read_text()
    entries = len(json.loads(manifest))
    print(f"fixture manifest entries: {entries}; fixture runs note items: {len(base['description']['runs'])}")
    notes = [(name,) for name in gate.NOTES["file"]] + [
        ("endpoints", end, name) for end in base["endpoints"] for name in gate.NOTES["endpoint"]]
    note_shapes, note_index, note_broken, entry_index, entry_broken = Counter(), Counter(), Counter(), Counter(), Counter()
    for seed in range(N):
        rng = random.Random(seed)
        operator, data, broken = selftest.mutate_json(rng, base)
        if operator == "note":
            try:
                tree = lenient(data)
            except ValueError:
                note_shapes["unparsed"] += 1
                continue
            for note in notes:
                value = selftest.at(tree, note[:-1]).get(note[-1])
                original = selftest.at(base, note[:-1]).get(note[-1])
                if value == original:
                    continue
                if isinstance(value, list) and len(value) == 4:
                    others = [i for i, item in enumerate(value) if not (isinstance(item, dict) and list(item) == ["run"])]
                    note_shapes["list"] += 1
                    note_index[others[0] if len(others) == 1 else "?"] += 1
                    note_broken[broken] += 1
                elif isinstance(value, dict) and list(value) == ["scopes"]:
                    note_shapes["scopes"] += 1
                else:
                    note_shapes["object"] += 1
        rng = random.Random(seed)
        operator, files, broken = selftest.mutate_report(rng, "baseline_images.json", manifest, "route")
        if operator == "entry key":
            after = lenient(files["baseline_images.json"])
            changed = [i for i, (old, new) in enumerate(zip(json.loads(manifest), after)) if old != new]
            entry_index[changed[0] if len(changed) == 1 else f"?{changed}"] += 1
            entry_broken[broken] += 1
    print(f"seeds: {N}")
    print(f"note cases by shape: {dict(sorted(note_shapes.items()))}")
    print(f"note list cases by index of the written key: {dict(sorted(note_index.items(), key=str))}")
    print(f"note list cases marked broken: {dict(note_broken)}")
    print(f"entry key cases by entry index: {dict(sorted(entry_index.items(), key=str))}")
    print(f"entry key cases marked broken: {dict(entry_broken)}")
    reached = set(note_index) >= {0, 1, 2, 3} and set(entry_index) >= set(range(entries))
    print(f"probe_r6_generator: every list index reached: {'yes' if reached else 'NO'}")
    raise SystemExit(0 if reached else 1)


if __name__ == "__main__":
    main()
