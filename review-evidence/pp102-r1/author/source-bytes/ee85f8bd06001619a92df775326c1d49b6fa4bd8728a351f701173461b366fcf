#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
Re-measure the figures this suite's README quotes, and diff them against it.

WHY THIS EXISTS. The README carries a device-error coverage table, a set of
mutation counts, probe counts and a device-model result table. Four review
rounds found them stale, and each time the figures that had been corrected were
the ones somebody thought to check while the rest drifted. Splitting one check
into two moves every row that reaches it; replacing an array-negative check with
a bus check moves every row whose mutant wedges earlier. There is no edit to
this suite that reliably leaves the numbers alone, so hand-maintaining them is
the wrong shape.

WHAT IT COVERS. Every figure in the README, and the covered set is DERIVED
rather than asserted: each `N of M` and `N PASS, M FAIL` in the file is a claim
by default, satisfied only by a measurement here or by an explicit entry in
WAIVERS whose reason is printed on every clean run. Twelve arm rows plus the arm
COUNT read from the RTL; eighteen mutations and probes; seven device-model result
rows; and all thirty cells of the pre-fix matrix.

Three earlier versions each closed a narrower class than they claimed, and the
progression is the useful part. The first checked only denominators and
result-row sums, so seven of eight falsifications walked past it. The second
added a table of named mutations and still missed M3 -- the very numerator that
had gone stale -- because nothing required the table to cover the file's own
claims. The third coupled the table to the file but matched ONE PHRASE, "fails
N of M", so three figures already present were invisible: "the same mutations
FAIL 68 of 90", "that check FAILS while the header check PASSES, 2 of 90", and
a prose restatement of a model row. A wider vocabulary would have been the same
mistake with a longer list. Inverting the default is what ended it.

The third version also declared the thirty matrix cells unmeasurable "because
the forms no longer exist in the tree". That was a cost choice dressed as an
impossibility -- the README's own text says "re-deriving it is re-running it" --
and re-injecting all six forms costs five builds. They are measured now.

Inverting the default paid for itself immediately: on its first run it found
that the coincident-completion figure could not be re-derived, because its
recipe had never been committed. Unverifiable, not fabricated -- a different
defect with a different fix, so the recipe is now `_COINCIDENT` and the number
is measured rather than asserted.

`--check` is accepted for symmetry with the other gates but changes nothing:
this exits non-zero on any disagreement either way. `--write` is deliberately
NOT provided, because a figure nobody looked at is how the table went stale in
the first place.

It is slow: one Verilator build per arm, mutation, probe and device model, five
for the matrix, plus the baseline. The exact count is DERIVED and printed at the
start of a run rather than written here. That is not fussiness: this number was
wrong in three consecutive rounds, and it is the one figure the inverted default
structurally cannot reach, because it matches no FIGURE_RE shape and does not
live in the README at all. A hand-maintained integer inside the tool that exists
to end hand-maintained integers is the joke writing itself.

It runs in CI and should be run after any change to this suite; it is
deliberately not part of `run`. `make -C tb/nvm_port figures`.
"""

import argparse
import atexit
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parent
README = SRC / "README.md"          # read only, never written

# Every mutation below edits a WORKING COPY, not the checkout. The `finally`
# restores in place correctly, but for the ~4 minutes a sweep runs the tracked
# sources on disk are wrong, and anything else reading them gets a false answer:
# during one run a concurrent read reported 11 arms and "M4: anchor occurs 0
# times", both false, both artefacts of reading mid-sweep. Copying removes the
# class rather than narrowing the window.
_WORK = Path(tempfile.mkdtemp(prefix="nvm_figures."))
atexit.register(shutil.rmtree, _WORK, True)
HERE = _WORK / "tb" / "nvm_port"
shutil.copytree(SRC, HERE, ignore=shutil.ignore_patterns("obj_dir", "__pycache__"))
_rtl_src = SRC.parent.parent / "hdl" / "packet_engine"
shutil.copytree(_rtl_src, _WORK / "hdl" / "packet_engine")
# `sim_main.cpp` includes the shared model owner as `../common/verilator_harness.hpp`
# (Core Guidelines R.11, and the copy `check_cpp_idiom.py` refuses to let drift).
# That header lives one directory up from the suite, so the working copy needs it
# too or every one of the 35 builds below fails to compile and the gate reports a
# build failure where it means to report a figure.
shutil.copytree(SRC.parent / "common", _WORK / "tb" / "common")
RTL = _WORK / "hdl" / "packet_engine" / "KL_pp_nvm_port.sv"
SIM = HERE / "sim_main.cpp"

#: (line in the RTL, state name) for every `if (dev_err_i)` arm. Cross-checked
#: against the RTL below: a THIRTEENTH arm added anywhere used to leave this
#: gate printing "all figures agree" while the README's "twelve arms" silently
#: became false.
ARMS = [(211, "S_WEREQ"), (220, "S_WEWAIT"), (230, "S_WWREQ"), (240, "S_WHPUMP"),
        (253, "S_WDPUMP"), (263, "S_WWAIT"), (274, "S_RHREQ"), (284, "S_RHCOLL"),
        (302, "S_RHWAIT"), (329, "S_RPREQ"), (339, "S_RPPUMP"), (349, "S_RPWAIT")]

#: The coincident-completion model. Unlike every other model here it varies the
#: HANDSHAKE, not what the array retains: the device raises `dev_done_i` on the
#: same clock edge that moves a command's final byte. `KL_pp_nvm_port.sv:175-179`
#: says the sticky `done_seen_r` latch exists for exactly this device, so it is
#: a documented contract freedom, not a broken peer -- and the port handles it,
#: with the suite green on pristine RTL. Its whole interest used to be that
#: deleting the latch was INVISIBLE without it; T21 and T22 now catch that on
#: the pristine model too, and this model still catches far more of it.
#:
#: It used to be four edits that spliced the behaviour into the harness from
#: here, and the mechanism they spliced in is now the harness's own armed
#: backend behaviour -- `Harness::present_coincident_completion`, which T22
#: arms for one commit and one restore. So this model is what it always meant:
#: the same freedom, taken by the backend for the WHOLE run rather than at one
#: armed moment. One anchor, on the declaration alone, so the comment beside it
#: can be reworded without the gate going dark; the reason the pulse has to be
#: written onto the pin between the two `eval()` calls is recorded in the
#: harness beside the code that does it, where a reader of that code will find
#: it.
_COINCIDENT = [
    (SIM, "  bool done_on_last_byte = false;", "  bool done_on_last_byte = true;"),
]

#: The state half of the ownership window: `dev_cmd_owned_w` narrowed to the
#: grant handshake alone, which is the simplification a maintainer reaches for.
#: The four states that can move a final byte are what carries a completion
#: that rides one, so this is the mutation T22 exists to reject.
_GRANT_ONLY_OWNERSHIP = [
    (RTL, """  assign dev_cmd_owned_w = (dev_req_o && dev_gnt_i)
                      || (state_r == S_WEWAIT) || (state_r == S_WHPUMP)
                      || (state_r == S_WDPUMP) || (state_r == S_WWAIT)
                      || (state_r == S_RHCOLL) || (state_r == S_RHWAIT)
                      || (state_r == S_RPPUMP) || (state_r == S_RPWAIT);""",
          "  assign dev_cmd_owned_w = (dev_req_o && dev_gnt_i);")]


#: Every `fails N of M` claim in the README, and how to reproduce it.
#:
#: `claim` is a regex that must match the README EXACTLY ONCE and must capture
#: the claimed count. Keying on the claim text rather than on a bare name is
#: what makes the coverage check below possible: a claim nobody listed here is
#: detectable precisely because every listed claim points at its own sentence.
#:
#: `edits` is a list of (file, old, new). Every `old` must occur exactly once --
#: see `apply_edits`. Two of these anchors were one-line strings that appear
#: twice in the file, and a count-1 replace silently patched whichever came
#: first; they carry a line of context now so the ambiguity is impossible
#: rather than merely unlikely.
#:
#: An anchor also carries the harness's INDENTATION, and that is how this gate
#: last went dark. When the suite's phases moved out of `main` into member
#: functions the whole body shifted left by two spaces; four anchors here and
#: three in `MATRIX_FORMS` kept the old form, and `apply_edits` raised on the
#: first of them.
#:
#: What that run actually did is worth stating exactly, because the first
#: account of it in this file was wrong and a maintenance note that misstates
#: the failure sends the next reader looking in the wrong place. It did not
#: fail to start. Run at the baseline it printed its build count, a green
#: 90-check baseline, all twelve arm rows and the six RTL mutation rows, then
#: raised on `probe-armearly` -- the first row whose anchor is in
#: `sim_main.cpp` rather than the RTL -- and stopped there, with `make`
#: exiting non-zero. The refusal is the design working: a stale table must not
#: measure. The failure mode to know is the other one. Rows printed before the
#: refusal look like a clean sweep, the mutations, models and matrix after it
#: never ran at all, and neither absence is announced -- so partial output is
#: not a result, and only the EXIT STATUS says whether the gate finished.
MUTATIONS = [
    # ---- mutations of the RTL ------------------------------------------------
    ("M1", r"rewritten to `S_WWREQ`.*?\*\*Fails (\d+) of", [
        (RTL, "                state_r <= S_WEREQ;",
              "                state_r <= S_WWREQ;")]),
    ("M1-sibling", r"so the ERASE is REQUESTED but never awaited, \*\*fails\s+only (\d+) of", [
        (RTL, "          end else if (dev_gnt_i) begin\n"
              "            state_r <= S_WEWAIT;\n          end",
              "          end else if (dev_gnt_i) begin\n"
              "            state_r <= S_WWREQ;\n          end")]),
    ("M2", r"\*\*M2\*\*.*?\*\*fails (\d+) of", [
        (RTL, "(hdr_r[0] == MAGIC_HI_C) && (hdr_r[1] == MAGIC_LO_C)", "1'b1")]),
    ("M3", r"\*\*M3\*\*.*?\*\*fails (\d+) of", [
        (RTL, "            if (bcnt_r == (plen_r - 16'd1)) state_r <= S_WWAIT;",
              "            if (bcnt_r == plen_r) state_r <= S_WWAIT;"),
        (RTL, "            if (bcnt_r == (plen_r - 16'd1)) state_r <= S_RPWAIT;",
              "            if (bcnt_r == plen_r) state_r <= S_RPWAIT;")]),
    ("M4", r"\*\*M4\*\*.*?\*\*fails (\d+) of", [
        (RTL, "        S_WDPUMP: begin\n          if (dev_err_i) begin",
              "        S_WDPUMP: begin\n          if (1'b0) begin")]),
    ("M5", r"\*\*M5\*\*.*?\*\*fails (\d+) of", [
        (RTL, "        S_WWAIT: begin\n          if (dev_err_i) begin",
              "        S_WWAIT: begin\n          if (1'b0) begin")]),
    # The defect issue #14 named, re-injected: the sticky latch set outside the
    # case, so a `done` is remembered in EVERY state -- including the ones with
    # no granted command outstanding, where it belongs to nobody. This is the
    # tree as it stood before the fix, and it is the mutation the standing
    # unsolicited-completion phases exist to reject.
    ("M6", r"\*\*M6\*\*.*?\*\*fails (\d+) of", [
        (RTL, "      if (dev_done_i && dev_cmd_owned_w) done_seen_r <= 1'b1;",
              "      if (dev_done_i) done_seen_r <= 1'b1;")]),
    # The fix the ticket proposed first and then withdrew: the global set, plus
    # a one-line clear in `S_WHDR`. Measured rather than argued, because "that
    # would not have been enough" is exactly the kind of claim this file has
    # had to retract before -- and because the cheap fix is what a later reader
    # will reach for.
    ("M6-sibling", r"the withdrawn one-line clear in `S_WHDR`.*?\*\*fails (\d+) of", [
        (RTL, "      if (dev_done_i && dev_cmd_owned_w) done_seen_r <= 1'b1;",
              "      if (dev_done_i) done_seen_r <= 1'b1;"),
        (RTL, "        S_WHDR: begin\n          if (nvm_wvalid_i) begin",
              "        S_WHDR: begin\n          done_seen_r <= 1'b0;\n"
              "          if (nvm_wvalid_i) begin")]),
    # ---- mutations of the TEST (the README calls these probes) ---------------
    ("probe-armearly", r"fails before its first byte moves, fails (\d+) of", [
        (SIM, "  std::vector<uint8_t> torn = frame(1, pattern(16, 0x22));\n"
              "  h.arm_err(1, 5);",
              "  std::vector<uint8_t> torn = frame(1, pattern(16, 0x22));\n"
              "  h.arm_err(1, -1);")]),
    ("probe-nodevice", r"the port the T16 prose names as the threat \S+ fails (\d+) of", [
        (SIM, "  h.arm_err(1, 5);\n  rc = h.commit(1, torn);\n  h.disarm_err();",
              "  rc = 1;")]),
    ("probe-t18", r"replacing a T18 arm with a bare `r = 1`, port never touched: now\s+fails (\d+)", [
        (SIM, "  int r = h.restore(5);", "  int r = 1;")]),
    # The retraction at "On checks that cannot fail alone": T15's tear moved
    # into the completion window, so the survival check fails while the
    # header-agreement check beside it passes. Its numerator was invisible to
    # the first inverted-default pass because it reads "FAILS ... PASSES, 2 of
    # 90" -- no "fails N of M" anywhere in the sentence.
    # The `done_seen_r` escape. It WAS green on pristine both ways, and only
    # the coincident model exposed it. This was an UNVERIFIABLE figure -- the
    # recipe lived in a scratch run that was never committed, so it could not
    # be re-derived. That is a different defect from a fabricated one and it
    # gets a different fix: commit the recipe, not retract the number. T21
    # since gave the latch coverage on the pristine model as well, so the row
    # now measures how much MORE the coincident model catches.
    ("done_seen_r/coincident",
     r"under a coincident-completion model the same\s+mutations fail (\d+) of",
     _COINCIDENT + [(RTL, "      if (dev_done_i && dev_cmd_owned_w) done_seen_r <= 1'b1;\n",
                     "")]),
    ("done_seen_r/pristine",
     r"deleting the set\s+line now reddens (\d+) of", [
        (RTL, "      if (dev_done_i && dev_cmd_owned_w) done_seen_r <= 1'b1;\n", "")]),
    # The state half of the ownership window, which no standing check reached
    # until T22: every backend the suite ran completed some cycles after the
    # last byte, and a completion that lands with the port already in a wait
    # state is read live, so the sticky flag was never consulted and the eight
    # state terms could all be deleted with the suite green. These four rows
    # are that measurement, kept as figures so it cannot quietly come back.
    ("own-states-dropped",
     r"ownership narrowed to the grant handshake alone \*\*fails (\d+) of",
     _GRANT_ONLY_OWNERSHIP),
    # The `|| ` is part of both anchors below: three of the eight states are
    # also named by an output assign, two of them with a second paren, so the
    # bare `(state_r == X)` is ambiguous for `S_WHPUMP` and `S_RHCOLL` and
    # `apply_edits` refuses it -- correctly, since a count-1 replace would have
    # mutated the datapath instead of the ownership window.
    ("own-minus-rhcoll",
     r"dropping the single `S_RHCOLL` term \*\*fails (\d+) of", [
        (RTL, "|| (state_r == S_RHCOLL)", "|| 1'b0")]),
    # ...and the other half of the same honesty: a term that CANNOT be pinned,
    # measured as such rather than asserted. A wait state consumes `dev_done_i`
    # on the cycle it arrives, so setting the flag there changes nothing any
    # observer can reach. If that ever stops being true this row goes red and
    # the README paragraph naming these four terms undiscriminated is wrong.
    ("own-minus-wwait",
     r"dropping the single `S_WWAIT` term \*\*fails (\d+) of", [
        (RTL, "|| (state_r == S_WWAIT)", "|| 1'b0")]),
    # The exclusion at the other end: ownership widened by one state that owns
    # nothing. T20a is the check that must reject it.
    ("own-plus-rhreq",
     r"admitting an ungranted `S_RHREQ` into the window \*\*fails (\d+) of", [
        (RTL, "  assign dev_cmd_owned_w = (dev_req_o && dev_gnt_i)",
              "  assign dev_cmd_owned_w = (dev_req_o && dev_gnt_i)\n"
              "                      || (state_r == S_RHREQ)")]),
    ("retraction", r"that check FAILS while the header check PASSES, (\d+) of", [
        (SIM, "  h.arm_err(1, 12);                 // op 0 = ERASE, op 1 = WRITE: cut at 12 B",
              "  h.arm_err(1, static_cast<int>(replacement.size()));")]),
]

#: The device-model result table. Each varies what the ARRAY retains and must
#: not redden a check about the PORT; the README's claim for each is a
#: `N PASS, F FAIL` row. Measuring these closes a shape the size/sum checks are
#: structurally blind to: "90 PASS, 0 FAIL" -> "45 PASS, 45 FAIL" preserves the
#: sum, so nothing below caught it until these ran.
_HALFPAGE = (SIM,
             "        d_stall = wstall;\n"
             "        if (fail_cur && d_bytes == err_after_bytes) { err_ctr = 2; d_st = 2; }",
             "        d_stall = wstall;\n"
             "        if (fail_cur && d_bytes == err_after_bytes) {\n"
             "          for (int k = 0; k < 4 && d_bytes - 1 - k >= 0; ++k)\n"
             "            store[d_cur.region % N_REGIONS]\n"
             "                 [(d_cur.offset + d_bytes - 1 - k) % REG_BYTES] = 0xFF;\n"
             "          err_ctr = 2; d_st = 2;\n        }")
_PAGEBUF = [
    (SIM, "  std::vector<uint8_t> sent;",
          "  std::vector<uint8_t> sent;\n  std::vector<uint8_t> pagebuf;"),
    (SIM, "        sent.push_back(dut->dev_wdata_o);\n"
          "        store[d_cur.region % N_REGIONS][(d_cur.offset + d_bytes) % REG_BYTES] =\n"
          "            dut->dev_wdata_o;\n        ++d_bytes;",
          "        sent.push_back(dut->dev_wdata_o);\n"
          "        pagebuf.push_back(dut->dev_wdata_o);\n        ++d_bytes;"),
    (SIM, "        else if (d_bytes == d_cur.len) { finish_data_phase(); }\n"
          "      } else if (d_stall > 0) --d_stall;\n    }\n\n    // read byte delivery",
          "        else if (d_bytes == d_cur.len) {\n"
          "          for (size_t k = 0; k < pagebuf.size(); ++k)\n"
          "            store[d_cur.region % N_REGIONS][(d_cur.offset + k) % REG_BYTES] =\n"
          "                pagebuf[k];\n"
          "          pagebuf.clear();\n          finish_data_phase();\n        }\n"
          "      } else if (d_stall > 0) --d_stall;\n    }\n\n    // read byte delivery"),
    (SIM, "        d_stall = wstall;\n"
          "        if (fail_cur && d_bytes == err_after_bytes) { err_ctr = 2; d_st = 2; }",
          "        d_stall = wstall;\n"
          "        if (fail_cur && d_bytes == err_after_bytes) {\n"
          "          pagebuf.clear(); err_ctr = 2; d_st = 2;\n        }"),
]
_LAZY = [(SIM, "        int r = d_cur.region % N_REGIONS;\n"
               "        memset(store[r], 0xFF, REG_BYTES);\n"
               "        ++erase_count[r];",
               "        int r = d_cur.region % N_REGIONS;\n"
               "        ++erase_count[r];")]

#: A model measurement may be quoted in more than one place. `claims` is a
#: LIST, and every listed site must agree with the one measurement: the prose
#: sentence at "Model probe" restates the half-page row, and a falsification of
#: the prose alone survived a gate that anchored on the table row only.

MODELS = [
    ("pristine", [r"\| pristine \| \*\*(\d+) PASS, (\d+) FAIL\*\*"], []),
    ("half-page", [r"\| half-page \| \*\*(\d+) PASS, (\d+) FAIL\*\*",
                   r"The half-page model is (\d+) PASS, (\d+) FAIL"], [_HALFPAGE]),
    ("page-buffered NOR", [r"\| page-buffered NOR \| \*\*(\d+) PASS, (\d+) FAIL\*\*"], _PAGEBUF),
    ("lazy erase", [r"\| lazy erase \| (\d+) PASS, (\d+) FAIL"], _LAZY),
    ("lazy erase + page-buffered",
     [r"\| lazy erase \+ page-buffered \| (\d+) PASS, (\d+) FAIL"], _PAGEBUF + _LAZY),
    ("coincident completion",
     [r"\| coincident completion \| \*\*(\d+) PASS, (\d+) FAIL\*\*"], _COINCIDENT),
]

#: Models whose columns the pre-fix matrix carries, in the table's own order.
#: NOT simply "every model": the matrix is about what the array RETAINS, and
#: the coincident model varies the handshake instead. Deriving the columns from
#: MODELS produced a six-wide measurement against a five-wide table on the run
#: that added `pristine` -- the gate caught it, which is the point.
MATRIX_MODELS = ["pristine", "half-page", "page-buffered NOR", "lazy erase",
                 "lazy erase + page-buffered"]

#: The six-by-five pre-fix matrix. Each row is a check FORM that was removed
#: from the suite because it read the array where it should not; the table
#: records which device model exposed each. Two earlier versions of this script
#: declared these thirty cells unmeasurable "because the forms no longer exist
#: in the tree". That was a cost choice dressed as an impossibility, and the
#: README's own text contradicted it: "re-deriving it is re-running it." The
#: forms are recoverable from `ba403c6~1`, `62d96d6~1` and `dc354be~1`, and
#: re-injecting all six beside the current checks costs FIVE builds -- one
#: fewer than MODELS already spends.
#:
#: (README row label, anchor, code injected before it). Order matters: the two
#: T17 forms must be injected BEFORE the good commit, because both pre-fix
#: spellings restored the TORN region and anchoring after `h.commit(3, rec)`
#: measures the wrong array.
MATRIX_FORMS = [
    ("T16 byte comparison",
     "  CHECK(h.sent.size() == 5 && std::equal(h.sent.begin(), h.sent.end(),",
     '    CHECK(std::equal(torn.begin(), torn.begin() + 5, h.store[1])\n'
     '              && h.store[1][5] == 0xFF,\n'
     '          "MX T16 byte comparison");\n'),
    ("T17 restore vs the record",
     "  h.ops.clear();\n  rc = h.commit(3, rec);\n"
     "  CHECK(rc == 0 && h.store_match(3, rec),",
     # Byte-faithful to the removed code, and pinned as such below. The
     # earlier version renamed `rc` to `pr`, MERGED the two original checks
     # into one conjunction, and captured the array BEFORE the restore across
     # two restores instead of after it across one. All thirty cells agreed
     # either way, which is exactly why it needed a pin rather than a re-run:
     # a reconstruction and a re-reconstruction share their errors.
     '    h.ops.clear();\n'
     '    rc = h.restore(3);\n'
     '    std::vector<uint8_t> in_array(h.store[3], h.store[3] + late.size());\n'
     '    CHECK(rc == 0 && h.rbytes == late,\n'
     '          "MX T17 restore vs the record");\n'
     '    CHECK(rc == 0 && h.rbytes.size() == late.size(),\n'
     '          "MX T17 restore vs the record length");\n'
     '    CHECK(h.rbytes == in_array,\n'
     '          "MX T17 restore vs the array");\n'),
    ("T15 branch pin", "  bool hdr_intact =",
     '    CHECK(crc_rejects && h.rbytes.size() == whole.size(),\n'
     '          "MX T15 branch pin");\n'
     '    CHECK(!h.store_match(7, whole) && !h.store_match(7, replacement),\n'
     '          "MX T15 cut was real");\n'
     '    CHECK(refused || crc_rejects,\n'
     '          "MX T15 #70 property, unconditioned");\n'),
]
#: Rows carried by an injection above rather than owning an anchor of their own.
MATRIX_ROWS = ["T16 byte comparison", "T17 restore vs the record",
               "T17 restore vs the array", "T15 branch pin",
               "T15 cut was real", "T15 #70 property, unconditioned"]


#: The one assumption the thirty matrix cells rest on that had no check behind
#: it: that each injected form IS the form that was removed. Re-running proves
#: nothing here -- two independent reconstructions share whatever transcription
#: error both made, and both agreed on all thirty cells while one of them had
#: merged two checks and moved an array capture. Git is the third party.
#:
#: (matrix row, revision, predicate that must appear VERBATIM in that file).
#:
#: The row is not decoration. The first version of this pin had five predicates
#: and all five were T17 -- the row where a defect had already been found and
#: fixed. The four rows where nothing had been found were the four with no pin,
#: and swapping T16's predicate for a DIFFERENT one was caught by nothing: not
#: by the pin, and not by the cell comparison either, since all thirty cells
#: stayed identical. An instrument that covers exactly where a defect was
#: already found is the same failure this gate has now made in five different
#: costumes, so `git_verbatim` requires every row to carry at least one pin.
GIT_FORMS = [
    ("T17 restore vs the record", "dc354be~1", "CHECK(rc == 0 && h.rbytes == late,"),
    ("T17 restore vs the record", "dc354be~1", "rc = h.restore(3);"),
    ("T17 restore vs the array", "62d96d6~1",
     "std::vector<uint8_t> in_array(h.store[3], h.store[3] + late.size());"),
    ("T17 restore vs the array", "62d96d6~1", "CHECK(rc == 0 && h.rbytes.size() == late.size(),"),
    ("T17 restore vs the array", "62d96d6~1", "CHECK(h.rbytes == in_array,"),
    ("T16 byte comparison", "dc354be~1", "CHECK(std::equal(torn.begin(), torn.begin() + 5, h.store[1])"),
    ("T16 byte comparison", "dc354be~1", "&& h.store[1][5] == 0xFF,"),
    ("T15 branch pin", "dc354be~1", "CHECK(crc_rejects && h.rbytes.size() == whole.size(),"),
    ("T15 cut was real", "dc354be~1",
     "CHECK(!h.store_match(7, whole) && !h.store_match(7, replacement),"),
    ("T15 #70 property, unconditioned", "dc354be~1", "CHECK(refused || crc_rejects,"),
]


def git_verbatim() -> list[str]:
    """Problems where an injected predicate is not what git records."""
    bad = []
    # Every row must carry a pin. Without this the pin covers whichever row
    # somebody last found a bug in, which is precisely the coverage shape that
    # let the T16 predicate be swapped for a different one unnoticed.
    for row in MATRIX_ROWS:
        if not any(r == row for r, _rev, _p in GIT_FORMS):
            bad.append(f"git-form pin: matrix row '{row}' has NO pinned "
                       "predicate, so nothing checks that its injected form is "
                       "the form that was removed")
    for row, rev, pred in GIT_FORMS:
        blob = subprocess.run(["git", "show", f"{rev}:tb/nvm_port/sim_main.cpp"],
                              cwd=SRC, capture_output=True, text=True)
        if blob.returncode:
            bad.append(f"git-form pin: cannot read {rev} -- the revision the "
                       "matrix injection was reconstructed from is gone")
        elif pred not in blob.stdout:
            bad.append(f"git-form pin [{row}]: {pred!r:.60} is NOT in {rev}. "
                       "The injected form is not the removed form, so the "
                       "matrix row measures something the suite never had.")
        elif not any(pred in code for _r, _a, code in MATRIX_FORMS):
            bad.append(f"git-form pin [{row}]: {pred!r:.60} is in {rev} but no "
                       "longer in any injection -- the pin has gone slack")
    return bad


def _check_condition_lines(code):
    """Every line of an injected CHECK that carries CONDITION, not message.

    By paren balance, after stripping the message LITERAL. The first version
    used `'"MX ' in line` as a terminator, which meant a condition sharing a
    line with its message was never collected at all -- a one-line
    `CHECK(cond, "MX row");` yielded nothing, not a partial result. Folding
    T16's second condition onto its message line, altering it, and dropping the
    now-unmatched pin passed all three rules with all thirty cells identical.
    The rule this function implements was simply false whenever a condition
    shared a line with a message.
    """
    lines, out = code.splitlines(), []
    i = 0
    while i < len(lines):
        if "CHECK(" not in lines[i] or lines[i].strip().startswith("//"):
            i += 1
            continue
        depth, body = 0, []
        while i < len(lines):
            raw = lines[i]
            # drop the message literal but keep its comma, so a condition
            # folded onto the same line is still seen
            stripped = re.sub(r'"(?:[^"\\]|\\.)*"', "", raw)
            body.append(stripped)
            depth += stripped.count("(") - stripped.count(")")
            i += 1
            if depth <= 0:
                break
        for b in body:
            b = b.strip().rstrip(";").rstrip(",").strip()
            if b and b not in ("CHECK(", ")"):
                out.append(b)
    return out


def pin_completeness() -> list[str]:
    """Every condition line of every injected CHECK must be pinned to git.

    NOT "at least one pin per row", which was the rule this replaces and was
    the weak default wearing new clothes. T16's form spans two lines and so
    carried two pins; deleting the second left the row compliant, `git_verbatim`
    clean, and re-opened the exact escape the pin had been added to close --
    swapping `h.store[1][5] == 0xFF` for a DIFFERENT predicate, invisible to the
    cell comparison because all thirty cells stay identical.

    A minimum COUNT would have been the same mistake again: the three forms
    carry one, three and three checks, so any threshold is arbitrary. The rule
    is read off the artifact instead -- what must be pinned is determined by
    what is injected, so it cannot drift out of proportion with it.
    """
    pinned = [pred for _row, _rev, pred in GIT_FORMS]
    bad = []
    for row, _anchor, code in MATRIX_FORMS:
        for line in _check_condition_lines(code):
            if not any(line in pred or pred.strip() in line for pred in pinned):
                bad.append(f"pin completeness [{row}]: the condition line "
                           f"{line!r:.60} is injected but not pinned to any "
                           "revision, so it can be swapped for a different "
                           "predicate and nothing will notice")
    return bad


def line_multiplicity() -> list[str]:
    """No injected line may appear more times than in its source revision.

    This closes the structural hole the two other mechanisms share. The cell
    comparison catches structure that moves a result; the git pin catches
    predicate text; a structural change that does NEITHER -- prepending a
    second restore, say -- leaves predicates verbatim and cells byte-identical
    and passes both. Counting occurrences catches it, because the duplicate is
    the structure.

    Deliberately NOT the shape first proposed for this, which was diffing the
    injected span against the git hunk: T17's form merges removals from two
    revisions and T15's from three, so that rule false-positives on the landed
    forms unless given a splice budget of three or more -- an arbitrary number,
    which is how the waiver cap got its 4.
    """
    revs = sorted({rev for _r, rev, _p in GIT_FORMS})
    blobs = {}
    for rev in revs:
        r = subprocess.run(["git", "show", f"{rev}:tb/nvm_port/sim_main.cpp"],
                           cwd=SRC, capture_output=True, text=True)
        if not r.returncode:
            blobs[rev] = r.stdout
    bad = []
    for row, _anchor, code in MATRIX_FORMS:
        # The `"MX ..."` labels are renamed on purpose, so `measure_matrix`
        # can find each form by name in the run's FAIL lines. They are the one
        # thing here that legitimately does not exist in git.
        # Was `len(strip()) > 12`, a threshold introduced while removing
        # thresholds. Inert today, but its boundary sat on a load-bearing line:
        # `refused = 1;` is exactly twelve characters and valid in T15's scope.
        # Brace-only lines are what actually needed excluding.
        for line in {l.strip() for l in code.splitlines()
                     if l.strip() not in ("", "{", "}") and '"MX ' not in l}:
            got = sum(1 for l in code.splitlines() if l.strip() == line)
            allowed = max((sum(1 for l in b.splitlines() if l.strip() == line)
                           for b in blobs.values()), default=0)
            if got > allowed:
                bad.append(f"line multiplicity [{row}]: {line!r:.55} appears "
                           f"{got}x in the injection but at most {allowed}x in "
                           "any source revision -- the injected form has extra "
                           "structure the removed form did not have")
    return bad


def readme_matrix() -> tuple[dict[str, list[str]], list[str]]:
    """{row: [pass/FAIL per model]} exactly as the README's matrix claims."""
    out, cols = {}, None
    for line in README.read_text().splitlines():
        if line.startswith("| pre-fix form |"):
            cols = [c.strip() for c in line.strip("|").split("|")][1:]
        elif cols and line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells[0] in MATRIX_ROWS:
                out[cells[0]] = ["FAIL" if "FAIL" in c else "pass" for c in cells[1:]]
            elif out:
                break
    return out, (cols or [])


def measure_matrix() -> dict[str, list[str]]:
    """{row: [pass/FAIL per model]} measured: inject all six, run every model."""
    inject = [(SIM, anchor, code + anchor) for _, anchor, code in MATRIX_FORMS]
    got = {r: [] for r in MATRIX_ROWS}
    by_name = {n: e for n, _c, e in MODELS}
    for mname in MATRIX_MODELS:
        failed = apply_edits(inject + list(by_name[mname]), want_fail_names=True)
        for r in MATRIX_ROWS:
            got[r].append("FAIL" if any(f"MX {r}" in f for f in failed) else "pass")
    return got


TALLY_RE = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")

#: EVERY figure in the README. Not "every figure phrased the way I expected" --
#: that was the previous version and it was a recogniser, matching one
#: vocabulary ("fails N of M") and blind to everything else. Three figures
#: already in the file sat outside it: "the same mutations FAIL 68 of 90"
#: (fail, not fails), "that check FAILS while the header check PASSES, 2 of 90"
#: (numerator not adjacent to any verb), and a prose restatement of a model row.
#: Seven plausible phrasings of a future claim were silent too -- `reddens 22 of
#: 90`, `FAILS 22 of 90`, `fails twenty-two of 90`, `| M6 | 22 |`, `22 of 90
#: checks go red`. A wider vocabulary would have been the same mistake with a
#: longer list, so the default is inverted: this matches the SHAPE of a figure,
#: and anything it finds is a claim that must be measured or waived out loud.
#: A spelled-out numerator is still a numerator, and so is one with an extra
#: word in the middle. The previous version argued that enumerating English
#: number words CLOSED this, and that argument was wrong in an instructive way:
#: the closed class is number words, but the OPEN class is ways of writing a
#: ratio, and closing one axis leaves the other untouched. Ten of thirteen
#: phrasings still evaded, and the two cheapest used digits only --
#: `fails 22 of the 122 checks` and `fails 22 out of 122`. A reviewer's own
#: earlier attack was literally `68 out of 83`, caught only because the
#: DENOMINATOR happened to be wrong.
#:
#: The two optional words below close all four digit-only cases and match
#: exactly the twenty-eight figures in the current file -- no false positives.
#: What they do NOT do is close the class, and this comment is deliberately not
#: claiming they do. `| Mx | 22 |`, `reddens 22 checks`, `a fifth of the
#: suite`, `68/90ths` and `24%` all still evade. A real closure would mean
#: treating every bare integer as a claim; measured, 292 numbers in this file
#: fall outside every claim and waiver span, so the waiver list would be larger
#: than the thing it protects. The honest position is that this is a strong
#: default that catches every phrasing anyone has actually written here, not a
#: proof that none can be written.
_ONES = ("one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "twenty thirty forty fifty sixty seventy eighty ninety".split()
_WORDS = "|".join(sorted(
    _ONES + _TENS + [f"{a}-{b}" for a in _TENS for b in _ONES[:9]] + ["zero"],
    key=len, reverse=True))
_RATIO = r"(?:out )?of (?:the )?\d+"
FIGURE_RE = re.compile(
    rf"\d+ {_RATIO}|\d+ PASS, \d+ FAIL|\b\d+/\d+\b|\b(?:{_WORDS}) {_RATIO}")

#: (regex, reason). A figure this file does not measure must be listed here with
#: why, and the reason is PRINTED on every clean run. The exclusion list is now
#: derived from the file rather than asserted in a docstring: a claim that is
#: neither measured nor waived is a hard error, so it cannot be added silently
#: and it cannot be quietly dropped from the covered set either.
#: A waiver that absorbs too much is the escape hatch swallowing the gate:
#: `\d+ of \d+` would absorb ten of the nineteen figures here, and `\d+` would
#: absorb all nineteen. A waiver that absorbs NOTHING is the other failure --
#: the same "row that stops being generated" class already closed for
#: measurements, still open one door over. Both are checked, and the absorbed
#: count is printed beside the reason on every clean run.
WAIVER_CAP = 4
#: ...and a cap on the TOTAL, because per-waiver is not a bound on the whole.
#: Six individually legal waivers silence all twenty-one figures and the gate
#: exits 0. The threat here is drift rather than malice, so this is a ratchet
#: with a comment attached: raising it is a deliberate act that shows up in a
#: diff, which is all it needs to be.
WAIVER_TOTAL_CAP = 6

WAIVERS = [
    # The README's own paragraph about what this gate does NOT close quotes two
    # evading phrasings as examples. The gate reads them as figures, which is
    # correct and is the mechanism working: they are waived by a pattern narrow
    # enough to reach only that sentence, so a real `22 out of 90` anywhere else
    # is still a hard error.
    (r"`fails 22 of the 122 checks` and `fails\s+22 out of 122`",
     "two illustrative phrasings quoted inside the paragraph explaining what "
     "the inverted default does not close; not claims about this suite"),
    (r"\b122/122\b",
     "suite tally shorthand; both halves are the suite size, which the size "
     "check already pins against the measured total"),
]


def run_suite(want_fail_names: bool = False) -> tuple[int, int, int] | list[str]:
    """Build and run; return (total, passed, failed), or the failing names."""
    subprocess.run(["make", "-s", "clean"], cwd=HERE, check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p = subprocess.run(["make", "-s"], cwd=HERE, capture_output=True, text=True)
    m, names = None, []
    for line in (p.stdout + p.stderr).splitlines():
        hit = TALLY_RE.search(line)
        if hit:
            m = hit
        elif line.startswith("FAIL: "):
            names.append(line[6:])
    if not m:
        raise RuntimeError("no tally line; build failed:\n" + p.stdout[-2000:])
    if want_fail_names:
        return names
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def apply_edits(edits: list[tuple[Path, str, str]],
                want_fail_names: bool = False) -> tuple[int, int, int] | list[str]:
    """Apply every edit, run, restore byte-identically. Returns the tally.

    An `old` that occurs zero times means this table is stale, which is the
    class the gate exists to catch. An `old` that occurs MORE than once is
    refused for the same reason at one remove: a count-1 replace would still
    measure something, just not necessarily the thing the README names, and a
    measurement of the wrong site is worse than a missing one because it looks
    like coverage.
    """
    saved = {p: p.read_text() for p, _, _ in edits}
    try:
        for path, old, new in edits:
            text = path.read_text()
            n = text.count(old)
            if n != 1:
                raise RuntimeError(
                    f"{path.name}: anchor occurs {n} times, need exactly 1 -- "
                    "this table is stale or the anchor is ambiguous, which is "
                    f"the class this gate exists to catch\n    {old!r:.120}")
            path.write_text(text.replace(old, new, 1))
        return run_suite(want_fail_names)
    finally:
        for path, text in saved.items():
            path.write_text(text)


def with_arm_disabled(lineno: int) -> int:
    """Force one `if (dev_err_i)` arm false, run, restore. Returns fail count.

    Line-indexed, NOT text-anchored, and deliberately does not go through
    `apply_edits`: all twelve arms are the same twelve characters, so the
    uniqueness rule that protects every other edit here would reject all of
    them. The line number IS the identity, and the guard below is the
    corresponding staleness check.
    """
    original = RTL.read_text()
    lines = original.splitlines(keepends=True)
    idx = lineno - 1
    if idx >= len(lines) or "if (dev_err_i) begin" not in lines[idx]:
        raise RuntimeError(
            f"{RTL.name}:{lineno} is not an `if (dev_err_i)` arm any more -- "
            "the ARMS table in this script is stale, which is exactly the "
            "class it exists to catch")
    try:
        lines[idx] = lines[idx].replace("if (dev_err_i) begin", "if (1'b0) begin")
        RTL.write_text("".join(lines))
        return run_suite()[2]
    finally:
        RTL.write_text(original)


def rtl_arm_count() -> int:
    """How many `if (dev_err_i)` arms the RTL actually has, counted not assumed."""
    return RTL.read_text().count("if (dev_err_i) begin")


def flat_readme() -> str:
    """The README as one whitespace-normalised line, so a figure split across
    a line break is still one match for the claim patterns."""
    return " ".join(README.read_text().split())


def readme_arm_rows() -> dict[str, int]:
    """{state: count} as the README's coverage table currently claims."""
    rows = {}
    for line in README.read_text().splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*`(S_\w+)`\s*\|\s*\**(\d+)", line)
        if m:
            rows[m.group(2)] = int(m.group(3))
    return rows


def claim_coverage(flat: str) -> list[str]:
    """Problems with the claim<->measurement correspondence, as strings.

    Both directions, because one direction is not a coupling. Measurement ->
    README catches a claim reworded or deleted; README -> measurement catches a
    claim ADDED, which is the direction M3 escaped through.

    The README -> measurement half now works by SHAPE, not by phrase. Every
    `N of M` and `N PASS, M FAIL` in the file is a claim by default; it is
    satisfied only by falling inside a measurement's own claim span or by an
    explicit waiver. That inversion is what makes the covered set derivable
    instead of asserted, and it found a figure nobody could reproduce on its
    first run.
    """
    bad, spans = [], []
    for name, claims, _ in _all_claims():
        for claim in claims:
            hits = list(re.finditer(claim, flat))
            if len(hits) != 1:
                bad.append(f"{name}: its README claim matches {len(hits)} times, "
                           "need exactly 1 -- the claim was reworded, moved or "
                           "deleted, so nothing checks this measurement any more")
            spans.extend((h.start(), h.end()) for h in hits)
    waived_total = set()
    for pat, _reason in WAIVERS:
        hits = list(re.finditer(pat, flat))
        absorbed = 0
        for m in FIGURE_RE.finditer(flat):
            if any(h.start() < m.end() and m.start() < h.end() for h in hits):
                absorbed += 1
                waived_total.add(m.span())
        if absorbed == 0:
            bad.append(f"waiver /{pat}/ absorbs no figure at all -- it is dead, "
                       "and a dead waiver is indistinguishable from a live one "
                       "until the figure it was written for comes back")
        elif absorbed > WAIVER_CAP:
            bad.append(f"waiver /{pat}/ absorbs {absorbed} figures, cap is "
                       f"{WAIVER_CAP}. A broad waiver silences real claims: "
                       "write one waiver per figure, with its own reason.")
        spans.extend((h.start(), h.end()) for h in hits)
    if len(waived_total) > WAIVER_TOTAL_CAP:
        bad.append(f"waivers absorb {len(waived_total)} figures in total, cap is "
                   f"{WAIVER_TOTAL_CAP}. Each may be individually legal and the "
                   "aggregate still empties the gate: six legal waivers silence "
                   "every figure in this file.")
    for m in FIGURE_RE.finditer(flat):
        # OVERLAP, not containment: a claim regex captures the numerator and
        # ends at "... of", while the figure shape runs on through the
        # denominator. Containment rejected all eleven real claims.
        if not any(s < m.end() and m.start() < e for s, e in spans):
            ctx = flat[max(0, m.start() - 60):m.end() + 20]
            bad.append(f"UNCLAIMED FIGURE {flat[m.start():m.end()]!r} -- every "
                       "figure in the README must be measured by an entry here "
                       "or waived in WAIVERS with a reason. Do not delete the "
                       f"claim to silence this.\n      ...{ctx}...")
    return bad


def _all_claims():
    """(name, [claim regexes], edits) over mutations and models alike."""
    return ([(n, [c], e) for n, c, e in MUTATIONS]
            + [(n, cs, e) for n, cs, e in MODELS])


def readme_figures(total: int, flat: str) -> list[str]:
    """Suite-size claims that disagree with `total`, as human-readable strings.

    A SIZE claim ("90 checks", "1 of 90", "the 90-check suite") is stale if it
    is not `total`. A RESULT row ("89 PASS, 1 FAIL") is stale if pass + fail is
    not `total` -- 89 is a good number in a five-model table and must not be
    flagged, while "82 PASS, 1 FAIL" must be.

    Note what this canNOT see, and why MODELS exists: "45 PASS, 45 FAIL"
    preserves the sum. Sums are a weak test and are the second line of defence
    here, not the first.
    """
    bad = []
    for pat in (r"of (\d+)\b", r"(\d+) checks\b", r"(\d+)-check\b"):
        for n in {int(x) for x in re.findall(pat, flat)}:
            if n > 40 and n != total:
                bad.append(f"suite size quoted as {n}, measured {total}")
    for pas, fail in re.findall(r"(\d+) PASS, (\d+) FAIL", flat):
        if int(pas) + int(fail) != total:
            bad.append(f"result row '{pas} PASS, {fail} FAIL' sums to "
                       f"{int(pas) + int(fail)}, suite is {total}")
    return sorted(set(bad))


def _arm_coverage_disagreements(claimed):
    """Print the per-arm measured-vs-README table; return the rows that disagree."""
    bad = []
    print("\narm coverage (measured vs README):")
    for lineno, state in ARMS:
        got = with_arm_disabled(lineno)
        says = claimed.get(state)
        print(f"  [{'ok ' if says == got else 'STALE'}] {lineno:>4} {state:<10} "
              f"measured={got:<4} readme={says}")
        if says != got:
            bad.append(f"{state}: README says {says}, measured {got}")
    return bad


def _mutation_disagreements(flat):
    """Print the mutation and probe table; return the rows that disagree."""
    bad = []
    print("\nmutations and probes (measured vs README):")
    for name, claim, edits in MUTATIONS:
        got = apply_edits(edits)[2]
        hit = re.search(claim, flat)
        says = int(hit.group(1)) if hit else None
        print(f"  [{'ok ' if says == got else 'STALE'}] {name:<16} "
              f"measured={got:<4} readme={says}")
        if says is not None and says != got:
            bad.append(f"{name}: README says {says}, measured {got}")
    return bad


def _model_disagreements(flat):
    """Print the device-model table; return the rows that disagree, including a
    claim site that has vanished from the README."""
    bad = []
    print("\ndevice models (measured vs README):")
    for name, claims, edits in MODELS:
        _, mp, mf = apply_edits(edits)
        got = (mp, mf)
        for claim in claims:
            hit = re.search(claim, flat)
            says = (int(hit.group(1)), int(hit.group(2))) if hit else None
            print(f"  [{'ok ' if says == got else 'STALE'}] {name:<26} "
                  f"measured={mp} PASS, {mf} FAIL  readme={says}")
            if says is None:
                bad.append(f"model '{name}': a claim site vanished from the README")
            elif says != got:
                bad.append(f"model '{name}': README says {says[0]} PASS/{says[1]} "
                           f"FAIL, measured {mp} PASS/{mf} FAIL")
    return bad


def _matrix_disagreements():
    """Print the pre-fix matrix; return the rows that disagree, and the row count
    itself when the README carries fewer than the known rows."""
    bad = []
    print("\npre-fix matrix (measured vs README), 5 builds:")
    says_m, cols = readme_matrix()
    got_m = measure_matrix()
    if len(says_m) != len(MATRIX_ROWS):
        bad.append(f"README matrix has {len(says_m)} of {len(MATRIX_ROWS)} known rows")
    for row in MATRIX_ROWS:
        says, got = says_m.get(row), got_m[row]
        print(f"  [{'ok ' if says == got else 'STALE'}] {row:<34} "
              f"measured={' '.join(got)}")
        if says != got:
            bad.append(f"matrix row '{row}': README says {says}, measured {got}")
    return bad


def _print_waivers():
    """Print each waiver with the reason and how many figures it absorbs, so the
    exclusion set is derived from the file rather than asserted in a comment."""
    if WAIVERS:
        print("\nNOT measured (waived, with the reason, so the exclusion set is\n"
              "derived from the file rather than asserted in a comment):")
        flat_r = flat_readme()
        for pat, reason in WAIVERS:
            hits = list(re.finditer(pat, flat_r))
            n = sum(1 for m in FIGURE_RE.finditer(flat_r)
                    if any(h.start() < m.end() and m.start() < h.end() for h in hits))
            print(f"  - /{pat}/ absorbs {n} (cap {WAIVER_CAP}): {reason}")

def main() -> int:
    """Re-measure every figure and report the ones the README no longer says;
    non-zero on any disagreement, with or without `--check`."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="accepted for symmetry with the other gates; this "
                         "exits non-zero on a disagreement with or without it")
    ap.parse_args()

    n_builds = 1 + len(ARMS) + len(MUTATIONS) + len(MODELS) + len(MATRIX_MODELS)
    print(f"{n_builds} Verilator builds: 1 baseline + {len(ARMS)} arms + "
          f"{len(MUTATIONS)} mutations + {len(MODELS)} models + "
          f"{len(MATRIX_MODELS)} matrix")
    total, passed, failed = run_suite()
    print(f"baseline: {total} checks, {passed} PASS, {failed} FAIL")
    if failed:
        print("baseline is not green; fix that before trusting any figure below")
        return 1

    flat = flat_readme()
    bad = readme_figures(total, flat)
    bad.extend(claim_coverage(flat))
    bad.extend(git_verbatim())
    bad.extend(pin_completeness())
    bad.extend(line_multiplicity())

    rtl_arms = rtl_arm_count()
    if rtl_arms != len(ARMS):
        bad.append(f"the RTL has {rtl_arms} `if (dev_err_i)` arms; this gate's "
                   f"ARMS table lists {len(ARMS)}. A new arm is invisible to "
                   f"every row below until it is added here.")

    claimed = readme_arm_rows()
    if len(claimed) != len(ARMS):
        bad.append(f"README table has {len(claimed)} rows; the RTL has {len(ARMS)} arms")

    bad.extend(_arm_coverage_disagreements(claimed))
    bad.extend(_mutation_disagreements(flat))
    bad.extend(_model_disagreements(flat))
    bad.extend(_matrix_disagreements())

    if bad:
        print("\nfigures disagree with the tree:")
        for b in bad:
            print("  -", b)
        print("\nRe-measure and update README.md. Do NOT edit only the rows you\n"
              "changed: four review rounds found staleness in the rows nobody\n"
              "thought to check.")
        # Always non-zero. The first version returned 0 without --check, so a
        # caller that forgot the flag got a clean exit over a stale file.
        return 1

    print("\nall measured figures agree with the tree")
    _print_waivers()
    return 0


if __name__ == "__main__":
    sys.exit(main())
