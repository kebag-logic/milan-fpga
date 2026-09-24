#!/usr/bin/env python3
"""Record every (command frame, model response) pair the AECP contract
feature delivers, tagged with its scenario and feature line.

Usage: record_frames.py <repo-root> <out.jsonl>
Runs behave in-process on tests/features/aecp_response_contract.feature with
AecpEngineModel.deliver and Scenario.run wrapped; the checkout is only read.
"""
import json
import os
import sys

root, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
tests = os.path.join(root, "tests")
os.chdir(tests)
sys.path.insert(0, os.path.join(tests, "steps"))
sys.dont_write_bytecode = True

import aecp_engine_model as M  # noqa: E402  (the steps import this instance)
import behave.model as BM  # noqa: E402

records = []
current = {"name": None, "line": None}

_run = BM.Scenario.run


def _scenario_run(self, runner):
    current["name"], current["line"] = self.name, self.line
    return _run(self, runner)


BM.Scenario.run = _scenario_run

_deliver = M.AecpEngineModel.deliver


def _record(self, frame):
    rsp = _deliver(self, frame)
    records.append(dict(scenario=current["name"], line=current["line"],
                        frame=bytes(frame).hex(),
                        model=None if rsp is None else bytes(rsp).hex()))
    return rsp


M.AecpEngineModel.deliver = _record
from behave.__main__ import main  # noqa: E402

rc = main(["--no-capture", "-f", "plain",
           "features/aecp_response_contract.feature"])
with open(out, "w", encoding="utf-8") as fh:
    for r in records:
        fh.write(json.dumps(r) + "\n")
print("behave exit", rc, "frames", len(records))
sys.exit(rc)
