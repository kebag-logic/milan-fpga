#!/usr/bin/env python3
"""Probe: the store's per-step byte accounting after the layout 3 header change.

nvm_rec_frame's crc16 now runs over NVM_REC_HDR - 2 = 8 header bytes plus the payload, but
nvm_latch counts `6u + r.plen` and NVM_STEP_BOUND is `2 * NVM_PAYLOAD_MAX + 6`. Two planted
variants are graded against the suite's service_bound test exactly as the self-test grades
a defect ("caught" = the named test FAILS):
  A  accounting corrected only (8 header bytes counted): the suite's own invariant
     step_max <= step_bound must then fail, i.e. the corrected count exceeds the declared bound;
  B  accounting and bound both corrected: service_bound's expected value (2*max_plen + 6)
     must then fail, i.e. the test pins the stale constant.
usage: probe_step_bytes.py <clone> <jobs>
"""
import sys
import tempfile
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2])
sys.path.insert(0, str(clone / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as t  # noqa: E402
M = t.nvm_mutants

ACC_OLD = "\tnvm.step_bytes += 6u + r.plen;"
ACC_NEW = "\tnvm.step_bytes += (NVM_REC_HDR - 2u) + r.plen;"
BND_OLD = "#define NVM_STEP_BOUND NVM_MAX(NVM_STEP_BYTES, 2u * NVM_PAYLOAD_MAX + 6u)"
BND_NEW = "#define NVM_STEP_BOUND NVM_MAX(NVM_STEP_BYTES, 2u * NVM_PAYLOAD_MAX + (NVM_REC_HDR - 2u))"
probes = (
    M.Mutant("probeA_accounting_only", (("nvm_store.c", ACC_OLD, ACC_NEW),), ("service_bound",)),
    M.Mutant("probeB_accounting_and_bound", (("nvm_store.c", ACC_OLD, ACC_NEW), ("nvm_store.h", BND_OLD, BND_NEW)),
             ("service_bound",)),
)
t.fw_gtest.EXECUTION.run = True
with tempfile.TemporaryDirectory(prefix="probe-step.") as tmp:
    work = Path(tmp)
    stem = t.SELF_TEST_SHAPE
    shape = t.prepare(t.ROOT / "configs" / f"{stem}.yaml", work / "shapes" / stem)
    shared = t.fw_gtest.Build(jobs=1)
    listing = t.build(shape, work / "listing", t.fw_gtest.Build(jobs=jobs, cache=shared.cache))
    held = t.suite_tests(listing, shape)
    for p in probes:
        v = t.plant_and_grade(p, shape, held, work / "probes", shared)
        print(f"PROBE {p.name}: {'service_bound FAILED (caught)' if not v else v}", flush=True)
