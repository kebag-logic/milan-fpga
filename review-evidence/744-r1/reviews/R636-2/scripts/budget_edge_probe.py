#!/usr/bin/env python3
"""Edge probes of the emitted census budget step, through the generator self-test's own harness.

Usage: python3 budget_edge_probe.py <checkout>
Plants extra cgroup shapes the self-test does not list and prints what the emitted shell exports.
"""
import os
import pathlib
import sys
import tempfile

checkout = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(checkout / "scripts"))
import ci_gate_workflows_selftest as t  # noqa: E402

gib = 1024 * 1024
container = {"": str(8 * 2**30)}
deep = {"": "max", "a": "max", "a/b": str(8 * 2**30), "a/b/c": "max"}
with tempfile.TemporaryDirectory(prefix="r636-2-budget-") as temporary:
    root = pathlib.Path(temporary)
    print("mode 000 denies a read here:", t.mode_zero_denies(root))
    for described, cpus, kib, cgroup, limits, denied, want in (
        ("leaf cgroup itself mode 000", 16, 61 * gib, "/", container, {"": "directory"}, None),
        ("unsearchable cgroup two levels above the leaf", 16, 61 * gib, "/a/b/c", deep, {"a": "directory"}, None),
        ("mode-000 limit two levels above the leaf", 16, 61 * gib, "/a/b/c", deep, {"a/b": "limit"}, None),
        ("readable 8 GiB two levels above the leaf", 16, 61 * gib, "/a/b/c", deep, {}, "4"),
        ("4 GiB host below an 8 GiB limit", 16, 4 * gib, "/", container, {}, "2"),
    ):
        got = t.census_budget(pathlib.Path(tempfile.mkdtemp(dir=root)), cpus, kib, cgroup, limits, denied)
        print(f"{'ok' if got == want else 'UNEXPECTED'}: {described}: got {got!r}, want {want!r}")
    # a dangling memory.max symlink is not -e, so the walk treats it as absent
    case = pathlib.Path(tempfile.mkdtemp(dir=root))
    got = None
    (case / "sys").mkdir()
    os.symlink(case / "nowhere", case / "sys" / "memory.max")
    got = t.census_budget(case, 16, 61 * gib, "/", {}, {})
    print(f"observed: a dangling memory.max symlink at the leaf: got {got!r} (treated as absent)")
