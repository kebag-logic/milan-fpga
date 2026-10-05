[A536]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally (simulation only). `milan_dp_gptp` (pinned Verilator 5.050) gives physical
139 / 0 and accounting 6 / 0, 20 / 0, 14 / 0, rc 0, at the fix commit `c24722ac`. The head
`d0e29f6d` adds README prose only. At that exact head, the hosted job's own driver and tally
give `PASS milan_dp_gptp`, 179 checks, 0 failures, driver rc 0 and tally rc 0. `656-dp-gptp-order` -> `dev`, two
commits on dev `c0280fc0`. The hosted nightly half of acceptance item 3 is still open (see
below), so this PR says "Relates to".

## Linked Issue / roles

Relates to #656
<!-- Switch to "Closes #656" once a hosted Physical gPTP run at this PR's head reports 139 / 0 (acceptance item 3, second half). -->

Executor: `[A536]`
Internal cleared-context reviewer: `[R484]`
External reviewer: `[R485]`

## Description

**Finding.** The three `milan_dp_gptp` sample-order failures (139 / 3) are a bench timing
defect, not a datapath defect.

**First bad merge and commit.** The range `1269cdaf..241f9184` was bisected on its four
first-parent merges. A run takes about 55 minutes, over the 40-minute limit, so the bisect
covers merges only.

| Point | Verdict (physical leg, pinned 5.050) |
|---|---|
| `1269cdaf` (good end) | 139 / 0, accounting 40 / 0 |
| `bbf704ec` Merge PR #634 | 139 / 3 |
| `54643724` Merge PR #644 (docs only, bisect midpoint) | 139 / 3 |
| `241f9184` Merge PR #638 | 139 / 3 (hosted nightly 37184411090) |
| dev `c0280fc0` | 139 / 3 |

The first bad merge is `bbf704ec`. Inside it, the first bad commit is `d676ecfd4`, named by
mechanism: it is the only commit in that PR to change the grid aligner's select, to
`wire mga_sel_w = int_clk_selected_r | follow_sel_r;` (`hdl/milan/milan_datapath.sv:5905`,
A2-a, owner decision #629 D4). The aligner is then engaged at INTERNAL, which this leg keeps.
A run of the commit and of its parent confirms it, on the same pins: parent `0b074298` gives
139 / 0 and 40 / 0, and `d676ecfd` gives 139 / 3.

**Mechanism.**

- The leg models plan A: the audio clock is 782/1591 of the 50 MHz axis clock, so the TDM
  FSYNC is 47,999.49 Hz, 10.64 ppm under 48 kHz.
- Under A2-a the aligner holds the media NCO (`media_tick_p`) on that FSYNC, and the
  loopback queue in `KL_chan_map_capture` drains on `media_tick_p`.
- The bench's peer talker was paced on the axis clock, at exactly 48 kHz. The queue (8 events
  per pair, one 6-event PDU plus 2 spare) therefore fills 0.51 events/s faster than it drains.
- Once the spare is used, the queue drops the oldest event and counts it on `lb_skip`
  (`SLIP_LB`): a one-sample gap every 1.958 s.
- Before `d676ecfd4` the INTERNAL grid free-ran on the axis clock, the talker's own rate.
  The same 10.64 ppm slip then sat at the TDM junction, which this leg does not grade.

A print-only trace at dev shows the aligner engaged from boot, trim settling at -170
(1/16 ppm per LSB, so -10.6 ppm), and the TDM junction clean. Every ordering error is a
one-sample gap on the edge where `lb_skip` steps by 4 (once per loopback pair):

```text
TRACE ORDER t=4.513547 last=216645 index=216647 step=2 lb_dup=0 lb_skip=4 tdm_dup=0 tdm_skip=0 mga_eng=1 trim=-170
TRACE ORDER t=6.471693 last=310635 index=310637 step=2 lb_skip=8
TRACE ORDER t=8.429839 last=404625 index=404627 step=2 lb_skip=12
TRACE ORDER t=10.387985 last=498615 index=498617 step=2 lb_skip=16
TRACE ORDER t=15.283986 last=216603 index=216605 step=2 lb_skip=4   (after the reset at about 10.75 s)
```

The gaps are 1.958146 s apart. That gives 2 in the peer-loss window, 2 in the recovery window
and 1 after the reset (cumulative only), so 5 in all. The gPTP transitions play no part: the
windows are where the beat lands. The checker grades correctly, and the DUT counts every
slip. A listener at INTERNAL slips honestly against a talker on another clock; that is
documented behaviour (the LOOP QUEUE banner in `KL_chan_map_capture.sv`).

Two statements already in the tree agree. `REGISTER_MAP.md`'s `SLIP_LB`/`SLIP_TDM` reading
table reads `SLIP_LB` climbing with `SLIP_TDM` static as "the upstream talker's clock is
not this media clock": this trace exactly. And the same suite's `obj_aclk` ring phases
(`sim_aclk.cpp:816-852`, #390) already pace their upstream talker "on the PHYSICAL grid
... the cadence a peer disciplined to the same CRF produces". At this leg's 50 MHz that
is 6,250 + 52/782 cycles per PDU, which is what this PR gives the physical leg.

**Fix.**

| File | Change |
|---|---|
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp` | The peer talker sends one six-sample PDU per `6 * 512` rising edges of the modeled audio clock, instead of one per `kHz * 6 / 48000` axis cycles. That models a peer following the DUT's INTERNAL media clock, the case in which no duplicate or gap is the correct expectation. Check code, windows, timers and check counts are unchanged. |
| `tb/verilator/milan_dp/README.md` | A model-table row and one paragraph stating the talker model and the counted 10.64 ppm slip an axis-paced talker meets at INTERNAL under A2-a. |

No RTL, port, register or parameter change.

**Planted controls and causal check** (scratch copies; the planted RTL line is the existing
`tdm8render` mutant "#629's A2-a removed", `wire mga_sel_w = follow_sel_r;`):

| RTL \ peer talker paced on | axis clock (old harness) | audio clock (this PR) |
|---|---|---|
| A2-a present (dev) | FAIL 139 / 3 | **PASS 139 / 0, 40 / 0** |
| A2-a removed (planted) | PASS 139 / 0, 40 / 0 | **FAIL 139 / 5** (4 windows fail; 8 ordering errors cumulative) |

The corrected check fails on both plants: a DUT whose INTERNAL grid leaves the audio clock
(bottom right), and a talker off the DUT's media clock (top left). It passes only when the
two clocks agree.

**#645 / #647.** #645 involves the same queue and counter, but in a followed, locked case, where a slip is
undeclared. This mechanism (a steady slip against an unfollowed talker) does not explain it.
It does show that the queue keeps 2 events of margin and never recentres, so a 2-sample
phase offset at lock would give #645's one-slip signature. That is a hypothesis for that
lane, untested here. #647 is the render path and does not overlap. This PR changes no RTL,
so it does not touch lane A531's files.

## Authoritative references

- #656 acceptance 1-3; lane comment `issuecomment-5985174558`; R470-1 on PR #655 (comment
  5982983632, item 5); hosted nightly 37184411090 (Physical gPTP, `241f9184`, 139 / 3).
- #629 D4 = A2-a (owner decision, issuecomment-5937643550) and its known-risk note
  (issuecomment-5937848189); `docs/design/MEDIA_CLOCK_FOLLOWING.md` (D4 row, A2 table).
- `hdl/milan/milan_datapath.sv:5905`, `:5924`, `:5932` (A2-a select); `:750-790` (the media
  NCO and `media_tick_p`).
- `hdl/ieee1722/aaf/KL_chan_map_capture.sv:173-224` (LOOP QUEUE: depth 8, drop-oldest and
  repeat, counted on `lb_skip_cnt_o` / `lb_dup_cnt_o`).
- `tb/verilator/milan_dp/README.md`, section "AX7101 1x1 eight-channel gPTP physical-rate
  run" (plan A model, 782/1591).

## How to get into the same state

```sh
git fetch origin
git checkout 656-dp-gptp-order
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git submodule status   # no '-', '+' or 'U' prefix
export PATH=<pinned-verilator-5.050-dir>:$PATH
verilator --version    # Verilator 5.050 2026-07-01 rev v5.050
```

## How to validate

```sh
make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4
# or the hosted job's own two commands:
env -u SUITE_TIMEOUT VERILATOR_JOBS=4 scripts/run_all_suites.sh /tmp/physical-logs --physical-gptp
python3 scripts/suite_tally.py /tmp/physical-logs --quiet --expect-suite-root tb/verilator --physical-gptp
```

Expected result / pass criteria: rc 0;
`== ax1x1gptp physical: checks: 139   failures: 0 ==`, every `AUDIO result` line
`bad_order=0`; then setup abort 6 / 0, no-TX 20 / 0, no-Pdelay 14 / 0. The simulation took
about 55 minutes here (3,228 s at the head).

Planted control C1 (expect rc 2 and physical 139 / 5). Run it in a scratch worktree, never
in the lane:

```sh
sed -i 's/^  wire        mga_sel_w = int_clk_selected_r | follow_sel_r;$/  wire        mga_sel_w = follow_sel_r;/' hdl/milan/milan_datapath.sv
make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4
```

Control C2 is the parent commit `c0280fc0` itself: the same command gives rc 2 and 139 / 3.

Other gates run at the head, all rc 0:

- `python3 sw/builder/test_builder.py`: the builder bank, which reads this harness in
  `test_sim_clock`. Result "ALL GATES PASS EXCEPT 1 NOT RUN"; gate 11 needs a Vivado build
  tree.
- `sw/builder/test_clock_contract.py`
- `scripts/check_cpp_idiom.py`, `measure_naming.py --check`, `measure_test_evidence.py
  --check`, `check_hygiene.py --check`, each with `--selftest`.
- `scripts/docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`,
  `check_feature_status.py`.
- With the pinned markdown lock: `check_em_dash.py --base c0280fc0` (0 findings over 10
  added lines) and `gen_toc.py --check` / `--verify-anchors`.

## Known limitations / out of scope

- **The hosted nightly half of acceptance item 3 is open.** It needs this branch pushed and
  the Physical gPTP job dispatched at its head, or the first nightly after merge.
- **Not run:** `act_ci.py` (nothing pushed). `milan_dp`'s default sweep: it never builds
  `sim_ax1x1gptp.cpp` (`tb/verilator/milan_dp/Makefile:496` is its only recipe), and the
  README edit is prose. Lint, `xvlog`, Yosys, synthesis and area: no RTL change.
- **INTERNAL against an asynchronous talker is not graded by this leg.** It still slips
  about 0.48 events/s per fed pair per 10 ppm on the loopback path (0.51/s at plan A's
  10.64 ppm), counted on `SLIP_LB`. That is A2-a's documented consequence. For this leg's
  old axis-paced talker the slip sat at the TDM junction before A2-a; a talker on any other
  clock slipped on the loopback path at INTERNAL before A2-a too. A zero-glitch run
  through the loopback lane (#396) needs the DUT to follow the talker, or the talker to follow
  the DUT.
- **The exact 160-PDU pin.** `verify_abort.py` pins the no-TX control's 20 ms window at
  exactly 160 RX PDUs. At the new pacing a PDU is 6,250.0665 axis cycles (6,250 + 52/782), so a window holds 159
  for about 0.17 % of start phases (the last 10.6 cycles of a period). The model is deterministic, and all eight 20 ms windows
  counted here gave 160.
- **Stale counts, left alone.** `tb/verilator/milan_dp/README.md:297` (at this head) and
  `tb/verilator/milan_dp_gptp/README.md:7,9` still say 137 physical / 177 total; the leg has
  counted 139 / 179 since before this lane.
- **Simulation only.** No hardware, bench or flashing.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (items 1 and 2 met; item 3 met locally, hosted nightly pending)
- [x] New or changed behavior has self-checking tests (the existing order checks under the corrected model, with planted controls C1 and C2)
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
