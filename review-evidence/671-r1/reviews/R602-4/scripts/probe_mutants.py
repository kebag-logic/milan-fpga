#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe for PR #715 / issue #671 (round R602-4).

Plants reviewer-chosen writer defects (not the lane's own controls) into a
COPY of the firmware text held in memory, compiles the repository's host
harness for one or more shapes in a disposable work directory, and runs the
repository's checks 13 and 14 IN FULL (no early stop), recording every
finding. The repository tree is only read.

Usage:
  probe_mutants.py REPO WORK OUT.json --configs a,b --jobs N [--labels x,y]
                   [--base-firmware FILE]

With --base-firmware, the given file (the pre-#671 writer) is graded as the
"base" label, with the restart model reduced to the statics it declares.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import replace
from pathlib import Path

# (label, [(old, new), ...], what the defect is)
PROBES = {
    "q_judge_no_second_agree": (
        [("(n >= 2u && nvm_reads_agree(second, rd))", "(n >= 2u && 0 && nvm_reads_agree(second, rd))")],
        "a third read that agrees only with the second does not stand"),
    "q_go_live_not_retired": (
        [("\tnvm_retired = 1;\n\tnvm_held = 1;\n", "\tnvm_held = 1;\n")],
        "a held writer is not retired (keeps answering the liveness deadline?)"),
    "q_restage_while_to_if": (
        [("\twhile (chosen != NVM_SLOT_NONE &&\n\t       !nvm_restage(",
          "\tif (chosen != NVM_SLOT_NONE &&\n\t       !nvm_restage(")],
        "the fallback slot is offered without its own re-stage"),
    "q_judge_no_unread_mark": (
        [("\tnvm_unread |= (slot == NVM_SLOT_A) ? 1u : 2u;\n\trd.vd = VD_LEN;",
          "\trd.vd = VD_LEN;")],
        "a judgement with no standing verdict does not mark the slot UNREAD"),
    "q_ok_needs_agreement": (
        [("\t\tif (rd.vd == VD_OK || (n >= 1u && nvm_reads_agree(first, rd)) ||",
          "\t\tif ((n >= 1u && nvm_reads_agree(first, rd)) ||")],
        "an OK verdict also needs a second agreeing read"),
    "q_hold_on_unstaged_only": (
        [("\tif (!nvm_unread) {\n\t\tnvm_ready = 1;", "\tif (!nvm_unstaged) {\n\t\tnvm_ready = 1;")],
        "only a failed re-stage holds the writer, not a failed judgement"),
    "q_hold_on_a_only": (
        [("\tif (!nvm_unread) {\n\t\tnvm_ready = 1;", "\tif (!(nvm_unread & 1u)) {\n\t\tnvm_ready = 1;")],
        "only slot A unread holds the writer"),
    "q_restage_two_tries": (
        [("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
          "\tfor (n = 0; n < 2u; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)")],
        "a re-stage takes two reads, under the stated three"),
    "q_judge_two_tries": (
        [("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK ||",
          "\tfor (n = 0; n < 2u; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK ||")],
        "a judgement takes two reads, under the stated three"),
    "q_unstaged_wrong_slot": (
        [("\t\tnvm_unstaged |= (chosen == NVM_SLOT_A) ? 1u : 2u;",
          "\t\tnvm_unstaged |= (chosen == NVM_SLOT_A) ? 2u : 1u;")],
        "the re-stage cause is recorded against the wrong slot"),
    "q_restage_no_fault_count": (
        [("\t\tif (rd.vd == VD_OK && rd.seq == seq)\n\t\t\treturn 1;\n\t\tnvm_read_faults++;\n",
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)\n\t\t\treturn 1;\n")],
        "a failed re-stage read is not counted in read faults="),
    "q_judge_no_fault_count": (
        [("\t\t\t/* other bytes than every earlier read */\n\t\t\tnvm_read_faults++;\n",
          "\t\t\t/* other bytes than every earlier read */\n")],
        "a differing judgement read is not counted in read faults="),
    "q_digest_ignores_bytes": (
        [("\treturn a.vd == b.vd && a.digest == b.digest && a.bytes == b.bytes;",
          "\treturn a.vd == b.vd && a.digest == b.digest;")],
        "agreement ignores the byte count (expected equivalent)"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--configs", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--labels", default="")
    ap.add_argument("--base-firmware", type=Path)
    a = ap.parse_args()
    sys.path.insert(0, str(a.repo / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t   # the repository's own host gate
    import writer_restart as wr

    text = (a.repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
    labels = [x for x in a.labels.split(",") if x] or list(PROBES)
    results = {}
    a.work.mkdir(parents=True, exist_ok=True)
    for stem in a.configs.split(","):
        cfg = a.repo / "configs" / f"{stem}.yaml"
        base = replace(t.make_bench(cfg, a.work / stem / "head", text), jobs=a.jobs)
        todo = [(lab, PROBES[lab][0], PROBES[lab][1]) for lab in labels]
        if a.base_firmware:
            todo.append(("base", None, "the pre-#671 writer, graded by this head's checks 13 and 14"))
        for label, pairs, what in todo:
            t0 = time.time()
            saved = dict(wr.WRITER_STATICS)
            if pairs is None:
                planted = a.base_firmware.read_text()
                found = set(re.findall(r"^static (?:int|uint32_t|uint64_t|unsigned int) (nvm_\w+)(?: = [^;(]+)?;$",
                                       planted, re.M))
                for k in list(wr.WRITER_STATICS):
                    if k not in found:
                        del wr.WRITER_STATICS[k]
            else:
                planted = text
                ok = True
                for old, new in pairs:
                    if planted.count(old) != 1:
                        ok = False
                        break
                    planted = planted.replace(old, new)
                if not ok:
                    results[f"{label}@{stem}"] = {"what": what, "error": "plant text does not match exactly once"}
                    continue
            try:
                pb = t.replant(base, a.work / stem / label, planted)
                got = t.grade_refused_generation(pb) + t.grade_read_faults(pb)
            except SystemExit as e:
                results[f"{label}@{stem}"] = {"what": what, "error": str(e)[:2000]}
                print(f"{label:<28} {stem:<28} ERROR {str(e)[:300]}", flush=True)
                continue
            finally:
                wr.WRITER_STATICS.clear()
                wr.WRITER_STATICS.update(saved)
            kinds = {}
            for item in got:
                for key in ("want exactly", "over the bound", "was lost on the clean reboot",
                            "held the writer; the bound must resolve it", "did not hold the writer",
                            "re-attached live", "persisted something", "names another cause",
                            "yet the boot offered", "does not name it unread", "another valid container",
                            "is not the container it judged", "generation was taken", "other saved record",
                            "on reads that returned different bytes", "did not refuse the console",
                            "named the slot on the console", "neither committed nor refused",
                            "printed no boot line", "read storm"):
                    if key in item:
                        kinds[key] = kinds.get(key, 0) + 1
            results[f"{label}@{stem}"] = {"what": what, "findings": len(got), "by_kind": kinds,
                                          "first": got[:3], "seconds": round(time.time() - t0, 1)}
            print(f"{label:<28} {stem:<28} findings={len(got):<6} {round(time.time() - t0, 1)} s", flush=True)
            a.out.write_text(json.dumps(results, indent=1) + "\n")
    a.out.write_text(json.dumps(results, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
