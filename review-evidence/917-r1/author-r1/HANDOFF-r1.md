# HANDOFF round 1, [A784], lane 917 (#917, part of #665)

Status: DONE at 3926c271; REVIEW READY posted on #917 (text in comments/REVIEW-READY.md)

- Branch: 917-aecp-hold, base origin/dev-soft-core cec88385ad
- TAKEN: #917 issuecomment-6894290176 (text in comments/TAKEN.md)
- REVIEW READY: #917 issuecomment-6899259827 (text in comments/REVIEW-READY.md); head 3926c271, not pushed
  (the manager pushes and opens the PR; PR-BODY.md is ready)
- Ruling implemented: #665 issuecomment-6894152131 item 2 (default)

## Instruction conflicts noted (resolved as stated)

- Handoff file named three ways (HANDOFF.md, HANDOFF-r1.md, HANDOFF-r4.md):
  this file is the one kept current; the other two point here.
- PR body: "Relates to #665 / Closes #917" vs a later "Relates to #894 /
  #872, no closing keywords, PR #914". The later lines name another lane's
  PR (#914 is the composed head of the flip train); PR-BODY.md follows the
  first, lane-specific, instruction (Relates to #665, Closes #917) and the
  template, first line [A784], no host paths, account names, tool names or
  footer.
- Memory: "unit capped at 12 GB" vs "unit cap 24 GB, keep it under 12 GB":
  kept under 10 GB per unit either way.

## 1. Analysis before any change: how hard is a deferred commit

Read at the base cec88385ad: sw/mailbox/mailbox.yaml (channels, rate, RATE_DROP),
gen_mailbox.py / mailbox_emit.py / mailbox_model.py / mailbox_skeleton.py,
KL_mbx_rx.sv, KL_mbx.sv's u_rx, MAILBOX_CONTRACT.md, MAILBOX_SPLIT.md,
tb/verilator/mbx (suite.hpp, bench.hpp, tb_mbx_top.sv, mutants.py, cosim),
sw/firmware/ctrl/host/mbx_model.c, tb/verilator/ctrl_service_budget.

Verdict: moderate, and contained in KL_mbx_rx plus the fabric's host model.

- The words are already in place. KL_mbx_rx writes a frame's words past
  head_r while it arrives, the two header words at HDR0/HDR1, and only then
  advances head_r (KL_mbx_rx.sv:486, :499-516, :722-725). A deferred commit
  is therefore "write everything, do not advance the head, advance it later":
  no buffer, no RAM, no new state machine state.
- The one real hazard is the next frame of the same channel: its speculative
  words are based at head_r (:486) and its free space is ring minus
  (head_r - tail) (:445-446), so it would overwrite the held record and
  ignore its space. Both must be based on a second, per-channel write head
  (head_r plus the held record). That write head is invariant across the
  held record's commit, so a frame arriving while it commits needs no fix-up.
- The refill race: a refill can land between the verdict (FIN) and HDR1, or
  in HDR1 itself. A frame decided "to hold" then commits at once, or a held
  frame would sit beside a token and be overtaken. Invariant to keep: a
  channel holds a frame only while its bucket is empty.
- Order: while a frame is held the bucket is empty, so every later frame of
  that channel finds no token and is dropped (the ruling's only drop); the
  held one commits first. A one-in-flight controller therefore never loses.
- Load: every commit, held or not, still takes one token, so the committed
  rate (burst, then one a refill) and the load gate's charge are unchanged.
- Cycle identity: a frame that finds a token can take exactly the base's
  states and cycles (FIN, VRD, HDR0, HDR1), so V0/V1 and every harness that
  never empties a bucket see the base's waveform.
- Observers that read internals by name: tb_mbx_top (act_w, fin_ready_w) and
  the CPU budget harness (observe.vlt: commit_w, ch_r). Keep both names with
  their base meaning for a frame that finds a token.
- Contract: no register, field, ring or version change is needed. RATE_DROP's
  text ("frames the channel's rate limiter refused") stays true; the
  generated KL_mbx_pkg.sv, KL_mbx.sv and mbx_contract.h can stay
  byte-identical, so no firmware input changes. The firmware reads
  arrival_ms only in srp_mbx.c:614 (a retry age); a held record keeps its
  arrival time, which is the contract's meaning (NOW_MS at the last byte).
- Collateral: the shared suite (suite.hpp) grades the RTL and the host model
  with the same checks (T0, T1, Q10 assume a drop at an empty bucket), and the
  co-simulation compares the two, so the host model must follow the RTL.
  Mutant arms anchored on changed RTL lines must be re-anchored.
- Generic: all five channels carry a rate and the buckets are per channel, so
  the mechanism is generic at no extra cost; no per-channel switch (which
  would need a contract field) is introduced.
- No formal proof exists for the mailbox (no .sby, no SVA in
  hdl/milan/mailbox); the invariant is checked every clock by the
  cycle-by-cycle bench instead.

## 2. Changes (file:line, reason)

RTL, `hdl/milan/mailbox/KL_mbx_rx.sv` (the only RTL file changed):

- :38-57 banner: the held frame, why (#917, ruling item 2, 9.2.2.4), the write head, the invariant.
- :230-232 `wr_head_r[c]` (write head: head_r plus a held record) and `held_r[c]`.
- :457-473 space: used from the write head, plus `cused_w` so a tail ahead of RX_HEAD inside a held
  record still leaves no free word (mailbox.yaml RX_TAIL: "ahead of it, leaves no free word").
- :512, :529, :535 speculative words and both header words at the write head (never over a held record).
- :566-611 verdict: RATE_DROP only with no token AND a frame held; stored otherwise. In HDR1,
  `tok_now_w` (token now, or a refill this clock) commits (`commit_w`), else `hold_w` holds.
  `commit_w` keeps its name and base meaning for a frame with a token (the budget harness's
  observe.vlt reads `commit_w`/`ch_r`; tb_mbx_top reads `act_w`/`fin_ready_w`).
- :731-791 buckets: `refills` block split out (no UNOPTFLAT through tok_now_w); `rel_w[c]` =
  refill and held: commits the held record (head_r <= wr_head_r, RX_PASS+1) and takes the refill's
  token; wr_head_r moves at HDR1 for a committed or held record; held_r set by hold_w, cleared by rel_w.

Contract and docs:

- `sw/mailbox/mailbox_emit.py` (the generated reference page's filter sentence) and its output
  `docs/reference/MAILBOX_CONTRACT.md`. `gen_mailbox.py --write`: KL_mbx_pkg.sv, KL_mbx.sv and
  mbx_contract.h byte-identical; only the reference page moved.
- `sw/mailbox/mailbox.yaml` filter comment only (YAML comment, not emitted); figures, RATE_DROP's
  doc string, version unchanged.
- `docs/design/MAILBOX_SPLIT.md`: filter section, new "The held frame" subsection, verification table
  counts (measured at this head), planted-defect row.

Host model of the fabric (compiled into no firmware image; see section 6):

- `sw/firmware/ctrl/host/mbx_model.h:119` `rx_held_words`; `mbx_model.c:265-271` the refill commits a
  held record; `:520-538` `rx_store` holds when no token; `:555-570` space past a held record, tail
  guard, RATE_DROP only behind a held record. Word count past RX_HEAD (not a second head) because
  test_acmp_mbx.cpp posts records by writing RX_HEAD directly.

Tests: see section 3. Firmware host tests: `sw/firmware/ctrl/test/test_acmp_mbx.cpp` K7, F4, F5 fill
loops count committed records from RX_PASS and wait out a held frame (they counted
`mbx_model_rx() == true` only, so a held-then-committed record went uncounted); expectations unchanged.

## 3. New checks, planted mutants, failing words

Shared suite (`tb/verilator/mbx/suite.hpp`, RTL through both adapters and the host model):

- T0/T1 (:780-850) rewritten for the ruling; Q10 burst+2; V0 (RTL) thirteen frames incl. held and
  refused-behind-held.
- New group `HeldNotDropped` (:1546-1640), checks B0-B4 (letter B: H0-H2 were already taken):
  B0 fifty AECP READ_DESCRIPTORs one in flight at line rate, all delivered, in order, burst at once,
  rest within one refill; B1 three on one token: first now, third dropped and counted (RATE_DROP 1,
  ERR), second at next refill; B2 1 kHz controller, 100 commands, none lost (the hardware finding);
  B3 reset forgets the held frame; B4 tail inside the held record -> RX_DROP.
- RTL-only `run_hold_timing` (:141): B5 refill landing in HDR0, HDR1 and the clock after (bench helper
  `send_frame_tick_after_verdict`); B6 over every clock: never held while a token is in the bucket
  (probe `probe_rx_hold_o` in tb_mbx_top, BENCH_P only).

Planted mutants (`tb/verilator/mbx/mutants.py`, new #917 block; `rx-drop-instead-of-hold` in QUICK, so
the default `make` runs it):

| Arm | Defect | Failing words (needle) |
|---|---|---|
| rx-drop-instead-of-hold | empty bucket drops (base behaviour) | "B0 fifty AECP commands, each sent at line rate as the one before it is delivered, are all delivered" |
| rx-hold-behind-a-held-frame | frame behind a held one dropped uncounted | "B1 the third, behind the held second, is dropped and counted in RATE_DROP" |
| rx-held-record-never-committed | refill leaves RX_HEAD | "T0 and RX_HEAD then covers the held record" (3926c271; at 84d8a214 the arm was caught only by other checks, 237 of 238 by name) |
| rx-next-frame-over-the-held-record | next frame's words at RX_HEAD | "B1 the records are the first and the second, byte for byte, in order" |
| rx-tail-inside-the-held-record-frees-space | free space from RX_HEAD only | "B4 a tail ahead of RX_HEAD, inside the held record, leaves no free word" |
| rx-refill-in-the-header-clock-missed (+axil) | refill in HDR1 not seen | "B5 a refill in the clock of its second commits the frame then" |
| model-drop-instead-of-hold (ctrl_mutants.py) | model drops at empty bucket | "B0 fifty AECP commands" on Suite/MbxModelGroup.PassesOnTheModel/HeldNotDropped |

Re-anchored (defect unchanged): rx-bucket-never-drains (needle now "T0 only the frame behind the held
one counts in RATE_DROP"), rx-refusal-takes-a-token, rx-tail-unguarded, rx-verdict-acts-unregistered,
model-rate-unlimited (needle "T0 only the frame behind the held one counts").

New T0 check at 3926c271: "T0 and RX_HEAD then covers the held record" (RX_HEAD after the refill's commit).
Counts at 3926c271: Wishbone 607, AXI4-Lite 652, co-sim 32, two interfaces 614/659, host model 532.

## 4. CPU budget harness

- It models this fabric path: `split_soc.py` Verilates the exported split SoC, so the real `KL_mbx_rx`
  runs under the firmware, and `observe.vlt` reads `KL_mbx_rx.commit_w` and `ch_r` for its `RXC`
  line; `grade.owner()` ties each commit to the last frame ended within COMMIT_LATENCY_MAX (64) cycles.
- It is not a CI gate (no Makefile, so `run_all_suites.sh` does not run it; no workflow names it).
- Legs whose scenarios empty a bucket (tokens to 0): every composed row offers each channel
  `admission()['at_once']` = min(burst, room) records at once (`scenario.composed_load`), which empties
  every bucket whose ring holds its burst. Computed from `scenario.admission` at the head: adp 8 of
  burst 8 (room 11), aecp 16 of 16 (room 30) and srp 32 of 32 (room 60) empty their buckets; acmp 12
  of 16 (room 12) and maap 7 of 8 (room 7) are bounded by the ring and keep 4 and 1 tokens. Rows:
  `backlog`, `backlog-adp`, `backlog-adp-refill` (ADP then one record a refill period up to the ring's
  room), `backlog-owed`, the save windows `backlog-adp@<phase>-<k>` and the aged windows
  `backlog-adp@<phase>-aged<age>-<n>`; `save-held` and `save-starved` hold every channel at its refill
  rate in bursts of at_once every at_once refill periods (`save_window.arrivals`), emptying each bucket
  at every burst (AECP's first burst one refill period late because the SET_NAME took a token,
  `save_window.held_start`). The paced groups (`aecp`, `aecp-fanout`, `scenario.paced`) send one frame
  a refill period and never empty it.
- Emptying is not holding: a hold needs a frame to arrive at an empty bucket. At the base such a frame
  was refused, and `grade.check_load` fails a composed window with any refused record, so a passing
  base run holds none in its graded windows.
- Measured (receipts/budget/): `run.py --point 1x1` on clean clones of cec88385 and 84d8a214, 94 groups
  each, rc 0, 0 refusals, the same 7 recorded budget misses (pre-existing): 283 of 284 output files
  byte-identical (every group's simulation log, script and graded json, and table.md); results.json differs
  only in `build`, the digest of the inputs, which include KL_mbx_rx.sv. So no scenario held a frame and
  every row is unchanged. None of the files 84d8a214..3926c271 changes is a recorded harness input
  (`inputs-vs-later-commits.txt`). The 8x8 point was not run (about five hours a point on this host).
- A held frame's later commit is not a `commit_w` (that stays the frame's own HDR1 commit), so if a
  future scenario did hold one, the grader would see it as refused, a loud failure, not a mismeasure.

## 5. Gates (all on a clean clone of the final head)

Final head: 3926c271 (cec88385ad + 84d8a214 + bb001e10 + 3926c271). Earlier heads' runs are kept as
supplementary evidence, named by head.

| Gate | Head | Command | Result | Receipt |
|---|---|---|---|---|
| full Verilator sweep, 4 shard units, clean clones | 84d8a214 | `run_all_suites.sh --shard k/4` (native-shards.py) | 65/65 suites, rc 0 every shard | receipts/sweep-84d8a214/ |
| sweep shard 1/4 (holds `mbx`), clean clone | 3926c271 | `run_all_suites.sh --shard 1/4` | 17/17 suites, rc 0; mbx 607/652/32/614/659/532 checks, 13/13 quick mutants | receipts/sweep-3926c271/ |
| full mailbox mutant campaign, clean clone | 3926c271 | `python3 mutants.py --jobs 6` | 238/238 caught, 4 positive controls, rc 0 | receipts/mbx/mutants-full-3926c271.log |
| rtl-fast (every job, fresh clone per job) | 3926c271 | `run_wf.py` + `verify_wf.py` | 0 bad (all four workflows: 139 steps rc 0, 226 not run with a reason) | receipts/workflows/ |
| elaborate (every job) | 3926c271 | same | 0 bad (with docs) | receipts/workflows/ |
| docs (every job) | 3926c271 | same | 71 steps rc 0, 70 not run with a reason, 0 bad (docs + elaborate) | receipts/workflows/ |
| rtl.yml yosys-shards 0-3, yosys-portability, yosys-tool, full-ci-gate | 3926c271 | same | 21 steps rc 0, 0 bad (verilator-shards: native sweep above) | receipts/workflows/ |
| firmware control / AECP / SRP mutants | 3926c271 | rtl-fast jobs | control 699/699 caught; aecp, srp rc 0 | receipts/workflows/ |
| lint ratchet, generator check, docs_check, em dash, py idiom (lane tree) | 3926c271 | local | PASS / 0 findings / 0 / 0 / PASS | receipts/local/ |
| split boot 1x1 and 8x8 | 84d8a214 (RTL and firmware equal at 3926c271) | `ctrl_split_boot/run.py` | PASS / PASS | receipts/route/ |
| firmware images base vs head | 84d8a214 and 3926c271 | `images.sh`, split exports | identical: 46 fixture images at both; split 1x1/1if and 8x8/1if | receipts/images/ |
| CPU budget harness 1x1, base vs head | cec88385 vs 84d8a214 (no harness input changed after) | `run.py --point 1x1 --jobs 6` | 94 groups each, rc 0; 283/284 outputs identical, results.json only in its input digest | receipts/budget/ |

Runner notes: `run_wf.py`/`verify_wf.py`/`not_run.json` adapted from a recent lane (paths, branch,
`total` left out of a matrix job's tag); every not-run reason re-read for this lane and two rewritten (the
RV32 SDK step: the runner's `$HOME/br-milan-rv32` links the pinned SDK; the hosted verilator-shards
partition: the native sweep above). The elaborate jobs ran with the LiteX venv as the job venv, the
others with the pinned gates venv. At 84d8a214 the first runs failed for these two environment gaps,
and docs-gates-0 gate_39 failed for real (ctrl_mutants.py 1002 lines > 1000): fixed in bb001e10.

CPU booking note: when `cpu_ranges.py pick` had no free range, units ran on this session's own pool
(96-127); the fourth 84d8a214 sweep shard ran on 96-103 of that pool beside three picked ranges, measured
idle when booked; two budget units and two batches were re-bound (taskset, own processes) to ranges
pick returned later.

## 6. Firmware images byte-identical

- Inputs: `git diff --stat cec88385ad 84d8a214 -- sw/firmware` touches only `ctrl/host/mbx_model.{c,h}`
  (the fabric's host model, compiled by host tests only) and `ctrl/test/{ctrl_mutants.py,test_acmp_mbx.cpp}`.
  `gen_mailbox.py --write` leaves `mbx_contract.h`, `KL_mbx_pkg.sv`, `KL_mbx.sv` byte-identical.
- Fixture images, every config x {1,2} interfaces x {flat,split} + `ctrl_image.py` + the ledgered 8x8/2if
  split: 46 ELF/BIN files, sha256 identical base vs head (receipts/images/). The 8x8/2if split without its
  ledger override refuses (rc 2) at both, identically.
- Shipping split platform image (1x1/1if) and 8x8/1if: compared against the base route's manifests
  (`bb04b696...` 145,496 B and `506a1ae4...` 158,176 B) in section 7.
- All-fabric images: `--ctrl-mailbox` off adds no mailbox source, so no input of theirs changed.

## 7. AX7101 split image, timing and area

S9's recipe at 3926c271, one Vivado at a time through vivado-slot.sh, no sweep running (receipts/route/,
SUMMARY.md there). Export identical to 84d8a214's; firmware `bb04b696...`, the base's.

| Directive | worst WNS / WHS over the four corners | floor (both >= +0.030) |
|---|---|---|
| ExtraPostPlacementOpt (integrated) | +0.202 / +0.016 | not met (hold) |
| ExtraTimingOpt | +0.063 / +0.036 | met |
| AltSpreadLogic_high | +0.203 / +0.036 | **met, best** |

0 failing endpoints and 0 routing errors in all three. Base (tree-identical 084cf7a8, #810's route):
+0.148/+0.028, +0.189/+0.008, +0.074/+0.008, so no base directive met the hold floor. ETO's worst two
setup paths are the receive verdict (`u_rx/ch_r` -> `vd_acc_r`/`vd_rate_r`, +0.063/+0.099, 21 levels),
which now reads the held flag.

Area, base -> head (placed): LUT +74 / +176 / +181 (EPPO / ETO / ASL), FF +76 / +76 / +75, LUTRAM
+1 / 0 / 0, BRAM 78.5 tiles (60 RAMB36 / 37 RAMB18) and DSP 9 unchanged; `KL_mbx_rx` +124 to +133 LUT
and +77 FF.

## 8. Open risks / questions

- Final head bb001e10 = 84d8a214 + one commit: `ctrl_mutants.py` compacted (996 -> 1002 lines at
  84d8a214 tripped the Python idiom gate's 1000-line module rule, docs-gates-0 gate_39 "long module 11 >
  ratchet 10"; now 998) and one MAILBOX_SPLIT.md sentence (a frame held when its channel closes is still
  committed). Every workflow job and the sweep shard holding `mbx` re-run on bb001e10; the full 4-shard
  sweep ran on 84d8a214, whose difference to bb001e10 no Verilator suite reads (`git diff --stat
  84d8a214 bb001e10`: those two files; no tb/verilator Makefile or driver reads either).
- Observation for a new Issue (not fixed here, pre-existing): `tb/verilator/ctrl_service_budget/{build,
  grade,scenario}.py` cite MAILBOX_SPLIT.md by line (`:516-523`, `:523`, `:666-678`, `:773-778`); at
  the base those lines already hold unrelated text (e.g. `:523` is the MAAP owner paragraph), and this
  change's new subsection moves them further. Citations by heading would not rot.
- Host model and host tests live under sw/firmware/ctrl/ (host/, test/); classified as not firmware
  image sources (stated in TAKEN); image identity proven by hash (section 6).
- `scripts/suite_shards.py` registers `mbx` at 73 s; this change adds one quick mutant build and ~60
  checks per build, so the estimate may need `--measure` after a hosted run.
- Left on disk: scratch (about 6 GB, under the 20 GB cap: the route checkpoints and reports the receipts
  hash, the budget build directories, the clean clones); the native shard clones the sweep tool made
  (`<lanes>/917-a784-shard0..3`, `917-a784-final-shard1`, about 12 GB of build products); no unit of
  this lane is running.
