#!/usr/bin/env python3
"""Reviewer-owned #671 mutation probes (R602-3).

Usage: probe_plants.py TREE OUTDIR JOBS LABEL[,LABEL...] [CFG_STEM[,CFG_STEM...]]

TREE is a disposable copy of the repository at the exact head under review.
Each plant below is applied to the firmware TEXT only (the tree's file is
never written), compiled into the head's host harness, and graded by the
head's checks 13 and 14 in full (no early stop), so every finding is
counted. 'base' grades the merge-base firmware (git show of e8454e27, read
from BASE_FW env or OUTDIR/base_fw.c) with the restart model narrowed to
the base writer's statics. 'head' is the unmodified firmware.
Writes OUTDIR/<label>.<shape>.txt with the findings and prints one summary
line per plant and shape.
"""
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[3])
LABELS = sys.argv[4].split(",")
STEMS = sys.argv[5].split(",") if len(sys.argv) > 5 else ["endstation_arty_4x4"]
sys.path.insert(0, str(TREE / "sw/firmware/nvm_hosttest"))

import tempfile                                   # noqa: E402
from dataclasses import replace                   # noqa: E402

import test_nvm_firmware as T                     # noqa: E402
import writer_restart as W                        # noqa: E402

PLANTS = {
    # the hold removed on the cold load path alone (the re-attach keeps it)
    "p_cold_goes_live": [(
        "\t\t\tnvm_publish(verdict);\n\t\t\tnvm_go_live();\n",
        "\t\t\tnvm_publish(verdict);\n\t\t\tnvm_ready = 1;\n")],
    # a held writer keeps answering the liveness deadline (nvm_backed stays)
    "p_held_heartbeats": [(
        "\tnvm_retired = 1;\n\tnvm_held = 1;\n",
        "\tnvm_held = 1;\n")],
    # a third read may agree with the first only, not with the second
    "p_agree_first_only": [(
        "(n >= 2u && nvm_reads_agree(second, rd))",
        "(n >= 2u && nvm_reads_agree(second, first))")],
    # a judgement that never stands is not marked UNREAD (VD_LEN still)
    "p_judge_unread_unmarked": [(
        "\tnvm_unread |= (slot == NVM_SLOT_A) ? 1u : 2u;\n\trd.vd = VD_LEN;\n",
        "\trd.vd = VD_LEN;\n")],
    # a judgement that never stands keeps its last refused verdict
    "p_judge_keeps_verdict": [(
        "\tnvm_unread |= (slot == NVM_SLOT_A) ? 1u : 2u;\n\trd.vd = VD_LEN;\n",
        "\tnvm_unread |= (slot == NVM_SLOT_A) ? 1u : 2u;\n")],
    # the re-stage is tried once, not NVM_READ_TRIES times
    "p_restage_once": [(
        "\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
        "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
        "\tfor (n = 0; n < 1u; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
        "\t\tif (rd.vd == VD_OK && rd.seq == seq)")],
    # the re-stage has no bound
    "p_restage_unbounded": [(
        "\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
        "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
        "\tfor (n = 0; n != 0xffffffffu; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
        "\t\tif (rd.vd == VD_OK && rd.seq == seq)")],
    # no re-stage at all: the window is filled from whatever the stage last held
    "p_no_restage": [(
        "\twhile (chosen != NVM_SLOT_NONE &&\n\t       !nvm_restage(",
        "\twhile (chosen != NVM_SLOT_NONE && 0 &&\n\t       !nvm_restage(")],
    # a blank verdict stands on one read, as an OK one does
    "p_blank_one_read": [(
        "\t\tif (rd.vd == VD_OK || (n >= 1u",
        "\t\tif (rd.vd == VD_OK || rd.vd == VD_BLANK || (n >= 1u")],
    # the hold only when both slots are unread
    "p_hold_both_only": [(
        "\tif (!nvm_unread) {\n\t\tnvm_ready = 1;",
        "\tif (nvm_unread != 3u) {\n\t\tnvm_ready = 1;")],
    # the console commit is no longer refused by name when held
    "p_console_unnamed": [(
        "\t\tif (nvm_held)\n\t\t\tprintf(\"NVM: refused; slot %s gave no standing verdict at boot, "
        "the writer is HELD until reset.\\n\",\n\t\t\t       nvm_unread_name());\n\t\telse if (!nvm_ready)",
        "\t\tif (!nvm_ready)")],
    # the sequence re-read from flash after the judgement (base behaviour)
    "p_seq_from_flash": [(
        "\tseq_a = rd_a.seq;\n\tseq_b = rd_b.seq;\n",
        "\tseq_a = (rd_a.vd == VD_OK) ? nvm_seq_of(nvm_slot(NVM_SLOT_A)) : 0;\n"
        "\tseq_b = (rd_b.vd == VD_OK) ? nvm_seq_of(nvm_slot(NVM_SLOT_B)) : 0;\n")],
    # the re-attach does not publish when held (spec: it publishes, then holds)
    "p_reattach_held_no_publish": [(
        "\t\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);\n\t\tnvm_publish(verdict);\n",
        "\t\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);\n\t\tif (!nvm_unread) nvm_publish(verdict);\n")],
    "head": [],
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    head_text = T.FIRMWARE.read_text()
    cfgs = {p.stem: p for p in (TREE / "configs").glob("endstation_*.yaml")}
    rc = 0
    statics = dict(W.WRITER_STATICS)
    with tempfile.TemporaryDirectory(prefix="r602probe.", dir=str(OUT)) as tmp:
        for stem in STEMS:
            for label in LABELS:
                if label == "base":
                    text = (OUT / "base_fw.c").read_text()
                    W.WRITER_STATICS = {k: v for k, v in W.WRITER_STATICS.items()
                                        if k not in ("nvm_unread", "nvm_held", "nvm_read_faults")}
                else:
                    W.WRITER_STATICS = dict(statics)
                    text = head_text
                    for old, new in PLANTS[label]:
                        n = text.count(old)
                        if n != 1:
                            print(f"{label}: plant anchor occurs {n} times; NOT APPLIED")
                            rc = 2
                            break
                        text = text.replace(old, new)
                    else:
                        pass
                    if rc == 2:
                        continue
                work = Path(tmp) / f"{label}.{stem}"
                work.mkdir()
                bench = replace(T.make_bench(cfgs[stem], work, text), jobs=JOBS)
                got = T.grade(bench, T.READ_FAULT_GRADES)
                (OUT / f"{label}.{stem}.txt").write_text("".join(x + "\n" for x in got))
                kinds = {}
                for item in got:
                    for key in ("was lost on the clean reboot", "did not survive", "over the bound",
                                "want exactly", "one faulty read held", "did not hold the writer",
                                "re-attached live", "persisted something", "printed no boot line",
                                "not the container it judged", "another valid container",
                                "yet the boot offered", "does not name it unread",
                                "on reads that returned different bytes", "generation was taken",
                                "did not refuse the console", "named the slot on the console",
                                "neither committed nor refused", "printed that it re-attached",
                                "reloaded the window", "did not name the unread slot"):
                        if key in item:
                            kinds[key] = kinds.get(key, 0) + 1
                print(f"{label:<28} {stem:<28} findings={len(got)} {kinds}", flush=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
