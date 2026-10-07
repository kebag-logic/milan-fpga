#!/usr/bin/env python3
"""R529-2 focused controls. Usage: focused_controls.py CHECKOUT SCRATCH RECEIPTS"""
import sys
from pathlib import Path
root, scratch, receipts = map(lambda x: Path(x).resolve(), sys.argv[1:])
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build as b
import ctrl_arms as a
import ctrl_mutants as m
import fw_gtest
from dataclasses import replace
receipts.mkdir(parents=True, exist_ok=True)
build = fw_gtest.Build(jobs=4)
failed = 0
for arm in ("maap", "maap_if2", "maap_debug", "model", "port", "unit"):
    result = getattr(a, "arm_" + arm)(b.Tree(b.CTRL, scratch / "positive", scratch / "reuse", build))
    (receipts / ("positive-" + arm + ".log")).write_text(result.log)
    (receipts / ("positive-" + arm + ".rc")).write_text(str(result.rc) + "\n")
    print("positive", arm, "rc", result.rc, flush=True)
    failed += result.rc != 0
# Standalone substitutions at production decision points; no altered assertion is a kill.
M = m.Mutant
controls = [
 M("missing-maap-interrupt", "app/ctrl_app.c", "mbx_place(channels, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH)", "mbx_place(channels & ~(1u << MBX_CH_MAAP), MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH)", "maap", "MaapHost.AppWaitWakesForMaapWithinBudget", "accepted MAAP wakes idle loop"),
 M("lost-preferred-range", "maap/maap.c", "reserve(m, m->preferred);", "reserve(m, 0);", "maap", "MaapCore.BeginBeforePortOperationalRetainsRange", "Begin supplied range survives port down"),
 M("restart-reuses-base", "maap/maap.c", "reserve(m, 0);", "reserve(m, m->base);", "maap", "MaapCore.RestartDrawsNewRange", "fixed seed Restart draws a new range"),
 M("priority-only-last", "maap/maap.c", "reverse_mac(m->mac) >= reverse_mac(peer)", "(reverse_mac(m->mac) >> 40) >= (reverse_mac(peer) >> 40)", "maap", "MaapCore.PriorityAfterTiedOctets", "every reversed octet decides"),
 M("priority-drops-first", "maap/maap.c", "i < 6u;", "i < 5u;", "maap", "MaapCore.PriorityAfterTiedOctets", "every reversed octet decides"),
 M("csr-listener-direction", "maap/maap_csr.c", "STRM_SEL, 0x100u | k", "STRM_SEL, k", "maap", "MaapCsr.EveryStreamAddressAndLossGate", "stream destination base plus index"),
 M("csr-early-enables", "maap/maap_csr.c", "if (c->aaf_outputs != 0u) {", "write_word(c, interface, AAF_CTRL, c->aaf_control); write_word(c, interface, CRFT_CTRL, c->crf_control);\n\tif (c->aaf_outputs != 0u) {", "maap", "MaapCsr.AdmissionAfterEveryDestinationWrite", "enables follow every destination word"),
 M("interface-one-no-poll", "maap/maap_mbx.c", "owed = maap_poll(&m->ifs[k].core) || owed;", "owed = (k == 0u && maap_poll(&m->ifs[k].core)) || owed;", "maap_if2", "MaapHost.InterfaceOneStallDrainsWithinBudget", "interface 1 poll drains deferred output"),
]
controls.insert(1, replace(controls[0], name="missing-maap-interrupt-if2", arm="maap_if2"))
controls += [x for x in m.MUTANTS if x.name.startswith("maap-generic-") or x.name in ("maap-late-service", "maap-ignored-input-late", "model-msg-type-off-by-one", "model-tuple-msg-type-ignored", "maap-numeric-mac-priority")]
for defect in controls:
    copy = m.plant(defect, scratch / "mutants")
    result = getattr(a, "arm_" + defect.arm)(b.Tree(copy, copy.parent / "build", scratch / "reuse", build))
    (receipts / (defect.name + ".log")).write_text(result.log)
    (receipts / (defect.name + ".rc")).write_text(str(result.rc) + "\n")
    killed = m.caught(defect.test, defect.needle, result)
    print("KILLED" if killed else "ESCAPED", defect.name, defect.test, "rc", result.rc, flush=True)
    failed += not killed
print("CONTROLS", len(controls), "FAILURES", failed, flush=True)
sys.exit(bool(failed))
