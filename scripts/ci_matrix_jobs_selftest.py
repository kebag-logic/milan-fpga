#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove complete matrix expansion and execute the generated fail-closed carrier."""

import copy
import json
import os
import subprocess

from ci_matrix_jobs import expand


def fixture() -> dict:
    """Two axes exercise substitutions in names, commands, environment and conditions."""
    return {"jobs": {
        "prepare": {"runs-on": "ubuntu-latest", "steps": [{"run": "true"}]},
        "work": {"name": "case ${{ matrix.shard }}/${{ matrix.total }}",
                 "needs": ["prepare"], "runs-on": "ubuntu-latest", "if": "${{ true }}",
                 "strategy": {"fail-fast": True, "matrix": {"shard": [0, 1], "total": [2, 3]}},
                 "steps": [{"name": "Execute", "if": "${{ matrix.shard == 1 }}",
                            "env": {"TOTAL": "${{ matrix.total }}"},
                            "run": "echo ${{ matrix.shard }} $TOTAL\n"}]},
        "finish": {"needs": ["work"], "runs-on": "ubuntu-latest", "steps": [{"run": "true"}]},
    }}


def main() -> int:
    """A missing, failed, cancelled or skipped dependency must fail the actual carrier shell."""
    source = fixture()
    original = copy.deepcopy(source)
    generated = expand(source)
    assert source == original
    jobs = generated["jobs"]
    assert set(jobs) == {"prepare", "work", "finish", "work-0", "work-1", "work-2", "work-3"}
    for index, (shard, total) in enumerate(((0, 2), (0, 3), (1, 2), (1, 3))):
        job = jobs["work-" + str(index)]
        assert "strategy" not in job
        assert job["name"] == f"case {shard}/{total}"
        assert job["steps"] == [{"name": "Execute", "if": "${{ " + str(shard) + " == 1 }}",
                                  "env": {"TOTAL": str(total)}, "run": f"echo {shard} $TOTAL\n"}]
        assert job["needs"] == ["prepare"]
    assert jobs["finish"] == original["jobs"]["finish"]
    carrier = jobs["work"]
    actual = {job: {"result": "success"} for job in carrier["needs"]}
    step = carrier["steps"][0]
    def run(values: dict) -> int:
        """Execute the real generated verifier without a hosted service."""
        env = dict(os.environ, CI_MATRIX_NEEDS=json.dumps(values),
                   CI_MATRIX_EXPECTED=step["env"]["CI_MATRIX_EXPECTED"])
        return subprocess.run(["bash", "-e", "-c", step["run"]], env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode
    assert run(actual) == 0
    for job in actual:
        for status in ("failure", "cancelled", "skipped", None):
            changed = copy.deepcopy(actual)
            changed[job]["result"] = status
            assert run(changed) != 0, (job, status)
        changed = copy.deepcopy(actual)
        del changed[job]
        assert run(changed) != 0
    changed = {**actual, "unexpected": {"result": "success"}}
    assert run(changed) != 0
    for matrix in ({}, {"shard": []}, {"shard": [0, 0]}, {"shard": [0.5]},
                   {"include": [{}]}, {"shard": list(range(257))},
                   {"shard": ["${{ secrets.TOKEN }}"]}):
        broken = fixture()
        broken["jobs"]["work"]["strategy"]["matrix"] = matrix
        try:
            expand(broken)
        except ValueError:
            pass
        else:
            raise AssertionError("ambiguous matrix accepted")
    broken = fixture()
    broken["jobs"]["work"]["strategy"]["fail-fast"] = False
    try:
        expand(broken)
    except ValueError:
        pass
    else:
        raise AssertionError("non-fail-fast matrix accepted")
    print("matrix expansion: exact Cartesian union, command preservation and 26 carrier refusals PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
