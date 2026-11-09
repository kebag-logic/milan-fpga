#!/usr/bin/env python3
"""Probe the prior public review's test-gap claims at this head: plant each defect into a copy of
the tree at the shipping 1x1 shape, build every binary of that shape, run every binary's WHOLE
suite, and report how many tests fail (0 = the defect survives the suite).
usage: probe_prior_findings.py <clone> <jobs>
"""
import re
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2])
sys.path.insert(0, str(clone / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as t  # noqa: E402
M = t.nvm_mutants
S, H = "nvm_store.c", "nvm_shape.h"
PROBES = (
    # positive control: a known defect the suite must catch
    ("control_klj2_not_recognised", (("nvm_klj2.c", "\tif (nvm_rd32le(hdr) == NVM_KLJ2_MAGIC)\n\t\treturn NVM_VD_VER;\n", ""),)),
    ("erase_first_block_every_time", ((S, "f->erase(f->ctx, nvm_slot_addr(nvm.target) + nvm.block * NVM_ERASE_BLOCK)",
                                       "f->erase(f->ctx, nvm_slot_addr(nvm.target))"),)),
    ("legacy_any_nonblank_header", ((S, "\t\t    nvm_rd32le(nvm_chunk) == NVM_KLJ2_MAGIC)",
                                     "\t\t    !nvm_all_erased(nvm_chunk, NVM_KLJ_HDR))"),)),
    ("ver_overrides_own_refusal", ((S, "if (nvm.st.last_verdict == NVM_VD_BLANK && nvm.st.legacy)",
                                    "if (nvm.st.legacy)"),)),
    ("legacy_b_wrong_place", ((H, "#define NVM_LEGACY_B       (MILAN_FLASH_JOURNAL_OFFSET + MILAN_FLASH_JOURNAL_SIZE / 2u)",
                               "#define NVM_LEGACY_B       (MILAN_FLASH_JOURNAL_OFFSET + MILAN_FLASH_JOURNAL_SIZE)"),)),
)
t.fw_gtest.EXECUTION.run = True


def grade(name, edits, shape, work, shared):
    tree = work / name / "tree"
    M.plant(M.Mutant(name, edits, ()), tree)
    try:
        exes = t.build(shape, work / name, shared, tree)
    except t.Refusal as exc:
        return f"PROBE {name}: does not build: {exc}"
    fails = []
    for b in t.binaries(shape):
        _ok, log = t.run_suite(exes[b.name], t.fixture_of(shape, b), ())
        fails += [ln.strip()[:160] for ln in log.splitlines() if "[FAIL]" in ln]
    head = f"PROBE {name}: {len(fails)} failing test line(s) -> {'SURVIVES the suite' if not fails else 'CAUGHT'}"
    return "\n".join([head] + [f"    {f}" for f in fails[:4]])


with tempfile.TemporaryDirectory(prefix="probe-prior.") as tmp:
    work = Path(tmp)
    stem = t.SELF_TEST_SHAPE
    shape = t.prepare(t.ROOT / "configs" / f"{stem}.yaml", work / "shapes" / stem)
    shared = t.fw_gtest.Build(jobs=1)
    t.build(shape, work / "listing", t.fw_gtest.Build(jobs=jobs, cache=shared.cache))
    with ThreadPoolExecutor(max_workers=len(PROBES)) as pool:
        for line in pool.map(lambda p: grade(p[0], p[1], shape, work, shared), PROBES):
            print(line, flush=True)
