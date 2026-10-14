#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant omissions against fresh driver inventories and actual union code."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile

from ci_case_receipts import canonical, partition
from ci_suite_pieces import PIECE_SECONDS, expand_suites, inventory, piece_identity, union
from suite_shards import ROOT, SUITE_SECONDS, WORKER_OVERHEAD_SECONDS, balance, sweep_suites


def write_leg(root: Path, suite: str, leg: int, names: list[str]) -> Path:
    """A fixture carries actual output files, so the production digest reader runs."""
    piece = f"{suite}__{leg}"
    total = len(PIECE_SECONDS[suite])
    path = root / "cases" / (piece + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.with_suffix(".logs").mkdir()
    output = "1 checks: 1 PASS, 0 FAIL\n"
    results = []
    for name in partition(names, f"{leg}/{total}"):
        results.append({"case": name, "outcome": "pass", "returncode": 0,
                        "output_sha256": hashlib.sha256(output.encode()).hexdigest()})
        path.with_suffix(".logs").joinpath(hashlib.sha256(name.encode()).hexdigest() + ".log").write_text(output)
    value = {"schema": 1, "suite": suite, "head": "a" * 40, "tree": "b" * 40,
             "inventory": names, "shard": f"{leg}/{total}", "results": results}
    path.write_bytes(canonical(value))
    (root / (piece + ".log")).write_text(output * len(results))
    return path


def suite_controls(suite: str, root: Path) -> None:
    """All omissions must fail against this tree's own driver-derived cases."""
    names = inventory(suite)
    roots = [root / f"worker-{leg}" for leg in range(len(PIECE_SECONDS[suite]))]
    paths = [write_leg(directory, suite, leg, names) for leg, directory in enumerate(roots)]
    union(suite, roots, root / "positive", "a" * 40, "b" * 40)
    originals = [path.read_bytes() for path in paths]
    dropped = names[-1]
    for path in paths:
        value = json.loads(path.read_text())
        value["inventory"].remove(dropped)
        value["results"] = [row for row in value["results"] if row["case"] != dropped]
        path.write_bytes(canonical(value))
    def refused(label: str, sources: list[Path]) -> None:
        """Every negative arm reaches the same public verifier as hosted jobs."""
        try:
            union(suite, sources, root / "negative", "a" * 40, "b" * 40)
        except (ValueError, OSError, KeyError):
            print(suite + ": refused " + label)
        else:
            raise AssertionError("accepted " + label)
    refused("case dropped from all legs and every claimed inventory", roots)
    for path, data in zip(paths, originals):
        path.write_bytes(data)
    refused("missing leg", roots[:-1])
    refused("duplicate leg", roots + roots[:1])
    value = json.loads(paths[0].read_text())
    for field in ("head", "tree"):
        changed = copy.deepcopy(value)
        changed[field] = "c" * 40
        paths[0].write_bytes(canonical(changed))
        refused("changed " + field, roots)
    paths[0].write_bytes(originals[0])
    log = roots[0] / (f"{suite}__0.log")
    log.write_text("1 checks: 0 PASS, 1 FAIL\n")
    refused("masked failing log", roots)
    log.unlink()
    refused("missing executed log", roots)


def main() -> int:
    """Cover complete ownership, source inventories and each fail-closed union."""
    physical = sweep_suites(ROOT / "tb/verilator")
    pieces = expand_suites(physical)
    assert set(SUITE_SECONDS) == set(pieces)
    assert "milan_dp_gptp" not in pieces
    owners, load = balance(pieces, len(WORKER_OVERHEAD_SECONDS))
    assert owners["tsn_fuzz"] == 1 and owners["chmap_capture"] == 3
    assert max(load[:-1]) <= 1620 and load[-1] <= 2160
    assert [name for name in pieces if owners[name] == len(load) - 1] == ["milan_dp_mclk__0"]
    for bad in ("milan_dp", "milan_dp__04", "milan_dp__4", "other__0", "milan_dp__-1"):
        try:
            piece_identity(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("accepted " + bad)
    with tempfile.TemporaryDirectory(prefix="suite-piece-controls-") as directory:
        for suite in PIECE_SECONDS:
            suite_controls(suite, Path(directory) / suite)
    print(f"suite pieces: {len(physical)} parents, {len(pieces)} scheduled units, all controls PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
