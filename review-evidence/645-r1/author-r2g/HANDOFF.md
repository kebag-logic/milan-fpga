[A531]

# Round 2g default-suite wall clock (#645, #647)

Current head: `1e79ebdc06528edff74c0a7f530f20f99e3326a2`.
Status: STOP pending manager publication and exact-head hosted evidence.
Both cold defaults meet the assigned scaled limit. All 44 verification
commands exited 0; the builder's historical gate 11 remains uncovered.
All jobs have finished. See Round 2g for commands, traces, receipts,
source binding, campaign ownership and the remaining handoff.

## Historical Round 2f overview

Head: `4640d995913cb93653a47e73856e8bd7dfe7c428`.
Status at that handoff: REVIEW READY. All three resource comparisons passed, policy is
unchanged, and assigned final verification commands passed. The historical
builder calibration arm without its placed report remains explicitly
uncovered. See Round 2f for measurements, commands, receipts and limits.

## Historical Round 2e overview

Head: `85db353400c6bf3965d279a9f5b5d47e08a0d1ed`.
Status at that handoff: REVIEW READY. The Round 2e section below retains its
scope and results. Earlier round sections retain their historical evidence.

## Historical Round 2d handoff

Head: `2525eae9567865a8bc741901914bdf5a1caf2c26` (branch `645-ring-slip`, target `dev`):
two one-line commits on the round-2c head `886e16201654ba0fd0c60c41c228ea4c75b2f6d3`,
then `--no-ff` merges of live `dev` `d51b373a` and `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`
(firmware, the `mbx` Makefile and one design note; no HDL), each clean. Origin:
`https://github.com/kebag-logic/milan-fpga.git`. Executor `[A531]`; reviewers
`[R474]` (internal) and `[R475]` (external). Nothing pushed.

**Status: STOP.** Ruling items 1 and 2 are done. Every functional gate, both
campaigns, the planted controls and the own-area limit pass at this head.
The BUILDING.md section 5 timing gate does not. All three placement
directives stop at the shipping IOB-pack check (#475) on `eth0_rx_dv`
before routing, so there is no bitstream and no timing table. The cause is a
synthesis remap of a LiteEth input register outside this lane, set off by
this round's one-term RTL change. The options and the recommendation are
under "STOP: the timing gate" below. Posted as
[A531] STOP: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6041331463.

## Authority

- [Original assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5981976917).
- [Round 2 ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009543884),
  amended by the [two-PDU span ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009767440)
  and the [quiet-band and recovery ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6010634115).
- [Timing bar: best of the three-directive sweep](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6009790232),
  as `docs/integration/BUILDING.md` section 5 defines it.
- [Round 2d ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6032466525),
  on [R474-2](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6032462363)
  (NEGATIVE, one MINOR) and [R475-2](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6031787384) (POSITIVE).
- `REQUIREMENTS.md`, `docs/design/MEDIA_CLOCK_FOLLOWING.md`,
  `docs/design/TIME_SYNC.md`, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`.

The takeover comment is 6010644995; it was not repeated in rounds 2c or 2d.
Nothing here is a review verdict or a lens ledger: R474-2's finding awaits
independent re-review at this head.

## Round 2d

### Commits

| Commit | Content |
|---|---|
| `2d9f995b` | `pop_dup_w` excludes `pop_hold_w` (`KL_chan_map_capture.sv:894-897`); standing `[LRC]` case for a held walk before a pair's first commit, with its no-pulse reachability twin; follow_ring controls HELD-DUP and STARVED-HELD-DUP; the `[LRC]` and controls rows of `MEDIA_CLOCK_FOLLOWING.md`'s test plan |
| `3eee12dc` | R474-2-R1 in `TIME_SYNC.md` (split to pass the style gate, see below) and R474-2-R2 in `REGISTER_MAP.md` 0x8D4 (verbatim) |
| `701b8332` | `--no-ff` merge of dev `d51b373a` (#684): 30 files under `sw/firmware/ctrl`, `ctrl_nvm` and `gtest` only; its tree equals the automatic merge of its parents |
| `2525eae9` | `--no-ff` merge of dev `e21c1ca0` (MAAP firmware): 24 files under `sw/firmware/ctrl` and `gtest`, `tb/verilator/mbx/Makefile` and `docs/design/MAILBOX_SPLIT.md`; its tree equals the automatic merge of its parents |

One-line subjects, no body, no trailers; no rebase, no amend. Dev moved twice
during the round: from `09f1841b` to `d51b373a` mid-run, then to `e21c1ca0`
before the handoff. Neither merge changes HDL, shipping build scripts,
dependencies or any harness but `mbx`'s. The only readers of what they change
are the `mbx` suite, dev's firmware-unit job, and the CI scope scripts and docs
that the source gates read (`round2d/merge-701b8332/`, `round2d/merge-2525eae9/`).
Those were rerun at each merge head. Every other gate ran on exports of
`3eee12dc`, whose inputs neither merge touches.

### Item 1: R474-2-F1, a held walk on a still-empty pair counted a dup

**Change.** `pop_dup_w = pop_visit_w && q_primed_r && q_fed_r && (pop_cnt_w == 0) && !pop_hold_w`.
A walk the settle action holds re-emits the pair's last event because the
action holds it, whether or not the pair's first commit of the PDU has
landed. It is the declared repeat, so it counts in neither half. Nothing else
moves: `pop_act_w` already excluded `pop_hold_w`, so the pops, holds, drops,
lockstep and wire output are unchanged. The hold lasts at most five walks
(`act_hold_r`); once it ends, a still-empty fed pair counts one dup per walk
as before, with no grace.

**Standing case** (`tb/verilator/chmap_capture/sim_main.cpp`,
`lrc_hold_before_first_commit`). One stimulus run twice: drain the stream to
zero left; (pulse); drive only the PDU's first beat, pair 0's event, which is
the decision beat; run a walk; then the rest of the PDU.

- Without the pulse (run before the block's counter snapshot): the walk counts
  exactly one dup, pair 1's. This proves the walk lands between the decision
  beat and pair 1's first commit.
- With the pulse: the frame is e6 five times then e7 on both pairs in
  lockstep, the dup and skip deltas are 0, and the next PDU follows in order
  with no sixth hold. The block's `LRC: no recentre moved the dup counter`
  covers it too.

`chmap_capture`: 785 checks, 0 failures (777 at `886e1620`, plus 8 new).

**Planted controls** (`tb/verilator/follow_ring/mutants.py`, built through
chmap_capture's recipe from a planted copy; a mutant counts as caught only
when every named check fails):

| Control | Plant | Named checks that fail |
|---|---|---|
| HELD-DUP | every held pop counts as a dup: `((pop_cnt_w == '0) \|\| pop_hold_w)` | new case (got 0xa), `LRC: no recentre moved the dup counter` (0x20), `SPAN: no action counted as a duplicate` (0xa per phase) |
| STARVED-HELD-DUP | the round-2c term, `(pop_cnt_w == '0)` without `!pop_hold_w` | new case (got 0x1), `LRC: no recentre moved the dup counter` (0x1) |

STARVED-HELD-DUP is the head's defect: it survives every pre-existing check
and is caught only by the new case. Receipts: `round2d/mutants/`.

**R474-2 probe P1**, applied unchanged to the round-2c suite
(`git show 886e1620:tb/verilator/chmap_capture/*`):

| RTL | Pulsed (hold declared) | Control (no pulse) |
|---|---|---|
| `886e1620` (`cmc` sha256 `abf102da`) | dup +1 | dup +2 |
| `3eee12dc` (`cmc` sha256 `2b07955b`) | dup **0** | dup +2 |

The probe's control still moves the block's counter by 2, a genuine dup, so
that copy keeps one failing check by construction. Receipts: `round2d/probe-p1/`.

**Campaigns.** The follow_ring model was built from the head's sources
(6.25 MHz, `FRAME_DIV` 64) and run through round 2c's driver with the same
arguments and seeds:

- the quiet and arrival campaign: 128/128 rc 0. The reader prints `quiet
  distributions: 128 phases, 512 windows, peak 1 axis cycles; band 2: PASS`;
- the INTERNAL pull-in sweep (16 feed phases x 52 and 56 us): 32/32.

All 160 logs are byte-identical to round 2c's run of the same case, and so is
the reader's JSON (`round2d/campaigns/campaign-compare.json`). The quiet
distribution (320,462,699 samples within +/-1 axis cycle), the arrival grid
(margins and slips before and after each settle) and the pull-in table are
therefore unchanged, as the ruling expected. follow_ring counts a slipped
frame at every second dup of its stream's two pairs. So the identical logs
show that every reported quantity is unchanged; they do not count how often
the F1 state occurred in these runs.

**Area** (vendor OOC, own-logic rule, shipping 1x1 TDM8 generics, base
`origin/dev` `09f1841b`, whose capture and settle sources are byte-identical
to round 2c's base):

| Row | Round 2c | Round 2d |
|---|---|---|
| settle base / head | 41 / 74 LUT, 51 / 93 FF | 41 / 74 LUT, 51 / 93 FF (rerun, same) |
| capture base | 1076 LUT, 1336 FF | 1076 LUT, 1336 FF (rerun, same) |
| capture head | 1162 LUT, 1376 FF | **1156 LUT, 1372 FF** |
| own delta (limit 120 / 120) | +119 LUT / +82 FF | **+113 LUT / +78 FF: PASS** |

Only `cmc_head.sv` changed; the other five inputs hash as in round 2c. The
4 FF and 6 LUT drop is synthesis variance, not a saving: the run no longer
replicates `skid_wp_r` bits 0 and 1 (`_rep__0`, `_rep__1`), and the LUT
mapping shifts between sizes. The change itself adds one term. Read the
round-2c +119 / +82 as the conservative figure. Receipts: `round2d/area-ooc/`.

### Item 2: wording fixes

- **R474-2-R2**, verbatim: `REGISTER_MAP.md:1870` now reads "held pops or
  dropped events count in neither half".
- **R474-2-R1**: the reviewer's exact sentence fails a mandatory gate.
  `scripts/check_doc_style.py` holds `TIME_SYNC.md` to 10-word sentences,
  20-word paragraphs and two sentences per paragraph. With the exact text it
  exits 1: "sentence has 17 words" and "paragraph has 25 words"
  (`round2d/gates/style-exact-wording.log`). The phrase "each pull-in that
  starts outside a previous action's recovery window" is 10 words alone. The
  same content is split. The reviewer's replacement for line 492 is verbatim
  (it is line 495 at the head):

  ```text
  A settle recentre follows each change.
  Each pull-in starting outside a previous action's recovery gets one.

  It waits until the servo and aligner rest.
  A pull-in starting inside that recovery is the declared residual.

  Outside that declared residual, nothing moves the stage after it.
  ```

  This deviates from "exact wording" to keep the gate at rc 0. It is
  published for the reviewer to accept or reword.

Not touched (outside this ruling): R475-2's residues R1 (PR-body status line;
`PR-BODY.md` now states this head's actual publication state) and R2 (the
`g_settle_recentre` locator at `MEDIA_CLOCK_FOLLOWING.md:1086`), both on the
manager's residue checklist, and R474-2's suggestions S1 to S3.

### STOP: the timing gate

**What fails.** The round-2c recipe was rerun at this head's gateware: synthesis
with one thread, then a fresh 32-thread implementation per placement
directive, with the shipping hooks. Synthesis passes (rc 0). Every directive
then raises CRITICAL WARNING [Place 30-722] for `eth0_rx_dv` in "IO
Placement", and the pre-routing IOB-pack check (`sw/litex/iob_pack_check.tcl`,
#475) ends the run:

| Directive | Result | `eth0_rx_dv` row |
|---|---|---|
| ExtraPostPlacementOpt | rc 1 at the IOB-pack check; no route, no bitstream | `FAIL ... no register reads the pad, only:` six LUTs |
| AltSpreadLogic_high | rc 1, same | same |
| ExtraTimingOpt | rc 1, same | same |

At round 2c (`f6bd415f` gateware) the same row read `IOB-PACK PASS eth0_rx_dv:
IN, milansoc_phy_source_valid_reg (FDRE @ ILOGIC_X0Y119); also read by 4
fabric cell(s)`, and all three directives produced bitstreams.

**Why.** The two synthesis checkpoints were read with vendor queries
(`round2d/iob/probe*.tcl`, `probe*-round2c.log`, `probe*-round2d.log`):

| Checkpoint | `milansoc_phy_source_valid_reg` D | R |
|---|---|---|
| round 2c (`f6bd415f`) | `eth0_rx_dv_IBUF` (the pad) | `eth_rx_rst` |
| round 2d (`3eee12dc`) | LUT2 `milansoc_phy_source_valid_i_1`, INIT `4'h2` = `eth0_rx_dv & ~eth_rx_rst` | constant 0 |

In round 2d, synthesis moved the register's synchronous reset `eth_rx_rst`
(fanout 10) off the flop's R pin into a LUT in front of D. That is a
control-set remap. A flop behind a LUT cannot sit in the ILOGIC, so the
`IOB TRUE` constraint on `eth0_rx_dv` cannot be met.

**Attribution.**

- The 120 synthesized source files and every include directory are
  identical between the two rounds except `KL_chan_map_capture.sv`. That
  file differs by this round's one term. The elaborated top differs only in
  comment lines: two date stamps and the order of one hierarchy-comment line.
- Round 2c's inputs, re-synthesized today in a fresh directory with round 2c's
  own script, reproduce round 2c's netlist: D from the pad, `eth_rx_rst` on R.
  So the host and the tool have not drifted.
- Round 2d's inputs, re-synthesized in a fresh directory, reproduce the LUT2
  remap exactly (INIT `4'h2`, R tied to 0), so the result is deterministic
  (`round2d/iob/resynth-results.json`).

So the remap is a global synthesis heuristic reacting to the change, not a
logic dependency: the capture crossbar and the LiteEth RX register share no
logic. The fragility is latent in the shipping build. The `eth0_rx_dv` IOB
constraint holds only while synthesis keeps that low-fanout reset on the
flop's R pin, and any change to the image's control-set census can move it.
Receipts: `round2d/iob/`, `round2d/tf/` (driver, logs, IOB-pack reports).

**Options.**

| Option | Area | Protocol-visible effect | Test plan |
|---|---|---|---|
| T1: make the GMII RX IOB capture registers independent of control-set remapping, in a separate Issue for the MAC/#475 owner (for example, no synchronous reset on the IOB input capture flops, or the reset held on the flop's pin by attribute) | about 0 (removes a LUT2) | none intended; the owner must show the reset-time behaviour downstream is unchanged | three-directive sweep at this lane's head with the fix; IOB-pack PASS on every constrained port; a synthesis probe at the round-2c and round-2d contents showing D from the pad in both; BUILDING.md's live red-side check |
| T2: turn off control-set remapping in the shipping synthesis recipe | whole image, unmeasured: more control sets | none intended | three-directive sweep plus area against the scoreboard; a recipe change in `sw/litex` and BUILDING.md |
| T3: declare R474-2-F1 instead of fixing it (the reviewer's alternative): restore round 2c's term, and state the case in `MEDIA_CLOCK_FOLLOWING.md`, REGISTER_MAP 0x8D4, the milan_dp README and the physical checker's counter rule | round 2c's measured +119 LUT / +82 FF; gateware back to round 2c's (timing PASS, +0.368 ns) | `SLIP_LB` may count one dup per still-empty pair during a declared hold at zero left | the new `[LRC]` case inverted to require the declared count; physical checker allowance with a control; needs a ruling |
| T4: reshape this lane's RTL until synthesis returns to the old census | 0 | none | not recommended: unprincipled, and any later change re-exposes the latent defect |

**Recommendation: T1, as its own Issue.** The defect is in the shipping
build, not in this lane. Keep this lane at `2525eae9` with F1 fixed and
every functional gate green. Once T1 is in `dev`, merge it with `--no-ff`
and rerun the three-directive sweep here. If the lane must not wait, T3
needs a ruling.

### Evidence at the head

Each gate ran on a fresh source export, identical blob for blob to its tree
(`round2d/gates/export-identity-*.json`), or in the clean lane checkout.
Every command ran unpiped and kept its own log and rc. The `3eee12dc` rows
carry to `2525eae9` by the two merges' identity proofs.

| Evidence | Tree | Result |
|---|---|---|
| Source and docs gates (28 commands, including the module matrix check, the style gate and the evidence selftest) | `2525eae9` (also `701b8332`, `3eee12dc`) | 28/28 rc 0 |
| `chmap_capture` (in shard 0/2) | `3eee12dc` | 785 checks, 0 failures; the yosys netlist leg 20/0 |
| Default sweep shard 0/2 (60 suites) | `3eee12dc` | 60/60 suites, 2,173,356 checks, 0 failures, rc 0 (the four declared `tsn_fuzz` skips). follow_ring: b8 48/0, pull-in 18/0, settle controller PASS at all four rates, small pulls 10/10, controls 12/12 |
| Default sweep shard 1/2 (`milan_dp`) | `3eee12dc` | 12,064 checks, 0 failures, rc 0 |
| Default sweep total | `3eee12dc` | 61 suites, 2,185,420 checks, 0 failures |
| Physical (`--physical-gptp`) | `3eee12dc` | 197 checks, 0 failures, rc 0. Both declared recentre steps reach the wire, consecutive within two output PDUs, with both loopback slip counters unchanged; recentre controls 14/0 |
| Render pull-in (`tdm8render-pullin`) | `3eee12dc` | 18/18 phases, 31 checks each, 0 failures. One settle recentre 1246.8 ms after the hold; no loopback slip during or after |
| LAW boundary (`tdm8render-law-boundary`) | `3eee12dc` | 81/81 PASS over 564 windows; largest walk 3 cycles (stated 5) |
| Builder (`--require-rv32 --require-elaboration`) | `3eee12dc` | rc 0. One arm NOT RUN for a recorded reason, as in earlier rounds: gate 11 needs an Arty build tree that is absent from this host |
| Source-list and wire-truth selftests | `3eee12dc` | rc 0, rc 0 |
| Portability (`syn/yosys/run.sh`) | `3eee12dc` | 58 modules PASS (`KL_chan_map_capture` included), tap purity PASS, rc 0 |
| `mbx` suite (reads the merged firmware) | `2525eae9` (also `701b8332`) | Wishbone 316, AXI4-Lite 361, host model 316 and cosim 13 checks, 0 failures; mutants 5/5 |
| Dev's firmware-unit job (7 commands) | `2525eae9` (also `701b8332`) | 7/7 rc 0; `test_ctrl_firmware` 122 tests, saved-state store 435 tests over 5 shapes, coverage PASS |
| Quiet/arrival and pull-in campaigns | model from `3eee12dc` sources | 128/128, reader PASS; 32/32; all 160 logs byte-identical to round 2c |
| R474-2 probe P1 | `3eee12dc` RTL | pulsed dup delta 0 (+1 at `886e1620`) |
| Planted controls | `3eee12dc` | 12/12 caught, including HELD-DUP and STARVED-HELD-DUP |
| Own area (vendor OOC) | `3eee12dc` capture | +113 LUT / +78 FF: PASS (round 2c: +119 / +82) |
| Vendor parser (`xvlog_gate.py --check`, shared lock) | `701b8332`; `hdl/` and the pins unchanged at the head | PASS, rc 0: 0 findings in `hdl/`, 2 in the pinned processor equal to the ratchet |
| Timing, three directives (BUILDING.md section 5) | `3eee12dc` gateware | **FAIL**: synthesis rc 0; every directive stops at the IOB-pack check on `eth0_rx_dv` (Place 30-722); no bitstream, no WNS/WHS (see STOP above) |

**Interruption (not a result).** At 11:40 the lane's own memory guard
stopped shard 1/2 and the LAW boundary with SIGKILL, at 8.90 GB service
memory. The `mbx` and firmware-unit jobs for the dev merge had been started
beside three gate lanes and the campaign. Both legs were rerun alone from the
start and passed. Nothing from the stopped attempt is credited
(`round2d/functional/interrupted-guard/`).

### Reproduction (round 2d)

```sh
REPO=$LANES/645-ring-slip
S=$VALIDATION_STORAGE/645-a531/reproduce-2d
SIM=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
cd "$REPO/tb/verilator/chmap_capture"
make build VERILATOR="$SIM" VERILATOR_JOBS=2 MDIR="$S/cmap" && "$S/cmap/Vchmap_wrap"
cd ../follow_ring
python3 -B mutants.py --mdir "$S/mut" --jobs 2 --select HELD-DUP STARVED-HELD-DUP SINGLE-DROP
make build VERILATOR="$SIM" VERILATOR_JOBS=2 MDIR="$S/model"
python3 -B "$PACKET/round2c/campaign.py" --repo "$REPO" \
  --exe "$S/model/Vfollow_ring" --out "$S/campaign" --jobs 4
python3 -B quiet_distributions.py "$S/campaign" --band 2 --out "$S/quiet.json"
python3 -B sweep.py pullin --exe "$S/model/Vfollow_ring" --out "$S/pullin" --jobs 4 --hold-us 52 56
```

Expected: `KL_chan_map_capture: 785 checks, 0 failures`; `follow_ring
mutants: 3/3 caught`; campaign 128/128 and the reader PASS; pull-in 32/32.

The timing STOP is reproduced by the round-2c timing recipe at this head's
gateware (`round2d/tf/run_timing.py` and `run_alt.py`; vendor work alone under
the shared lock). Its synthesis checkpoint is then read with
`round2d/iob/probe2.tcl`:

```sh
vivado -mode batch -nojournal -nolog -notrace -source probe2.tcl \
  -tclargs <outdir>/gateware/alinx_ax7101_synth.dcp
```

Expected at this head: `D net: milansoc_phy_source_valid_i_1_n_0 driver:
milansoc_phy_source_valid_i_1 LUT2`, `R net: <const0>`, `lut INIT: 4'h2`.
At round 2c's gateware: `D net: eth0_rx_dv_IBUF`, `R net: eth_rx_rst`.

# Round 2c record (context for the head above)

Everything below is the round-2c handoff as published at `886e1620`. Where
round 2d reran a gate, the round-2d evidence table above supersedes it.

## Commits this round (on top of `583f93a3`)

| Commit | Content |
|---|---|
| `639814a1` | Two-axis-cycle quiet-band arm, recovery qualification (one state bit, the existing dwell counter), recovery watch, fine-pull and paired-pull cases, three planted controls, controller regression at four clock rates, quiet-distribution reader |
| `4bddd95e` | Measured recovery windows and the declared residual in `MEDIA_CLOCK_FOLLOWING.md` |
| `31538f4b` | Quiet-band settling text; render harness comment on its focused coverage |
| `132d79e7` | `--no-ff` merge of dev `30e3c018` (#658, #670): reader-disposition table moved into `scripts/measure_test_evidence_readers.py`, `milan_dp/Makefile` resolved keeping both target sets |
| `5afae068` | `--no-ff` merge of dev `bd884631` (#676): adds only `docs/findings/667_TALKER_START_BENCH.md` |
| `b00df050` | States the measured 128-phase quiet distribution behind the arm |
| `33c951fc` | Corrects the 56 us pull-in slip count (4 phases, not 3) and widens the declared-transient measurement scope to both offset signs and the 0 to 60 us envelope |
| `9e529b20` | `--no-ff` merge of dev `6714181d` (#674, #675): docs, firmware unit tests, CI scope scripts and the `mbx` harness header; no file conflicts and no file of this lane touched |
| `f6bd415f` | `--no-ff` merge of dev `6a05347d` (#680): AAF packetizer startup admission (`KL_aaf_packetizer.sv`, +8 lines), its `aaf` startup suite and text; `TIME_SYNC.md` and the reader table auto-merged with this lane's edits |
| `4951c471` | `--no-ff` merge of dev `79b086d4`: per-suite default time limits in `run_all_suites.sh`, test-evidence scripts and documentation; `TESTING.md` and the milan_dp README auto-merged |
| `0a196192` | `--no-ff` merge of dev `910f338d`: firmware RV32 test tooling, `ci_events.py` and documentation; no HDL, testbench, harness or build input |
| `886e1620` | `--no-ff` merge of dev `09f1841b` (#665 FC): mailbox RTL and its `mbx` suite, mailbox generator, control-plane firmware and documentation; the mailbox is not in the AX7101 shipping file list |

`b00df050` and `33c951fc` change documentation only
(`round2c/resume/final-doc-identity-k.json`). The `9e529b20` merge changes no
HDL, synthesis, constraint or configuration file
(`round2c/resume/dev-merge-identity-m.json`). The `f6bd415f` merge changes the
AAF packetizer, so every gate that elaborates it was rerun at `f6bd415f`
(`round2c/resume/dev-merge-identity-f.json`). This lane's own sources
(`milan_datapath.sv`, `KL_chan_map_capture.sv`) and the follow_ring and
chmap_capture harnesses are byte-identical from `132d79e7` to the head. The
source exports used for the functional gates match `f6bd415f` blob for blob,
submodules included (`round2c/resume/export-identity-f6bd415f.json`). The
`4951c471` merge changes no HDL, harness, constraint or build input
(`round2c/resume/dev-merge-identity-g.json`). Its runner change only moves
default per-suite time limits, and every sweep here ran under an explicit
`SUITE_TIMEOUT` override, so the `f6bd415f` functional and timing evidence
covers the head. The source and docs gates and the changed evidence selftest
were rerun at `4951c471`. The `0a196192` merge changes only firmware test
tooling, `ci_events.py` and documentation (`round2c/resume/dev-merge-identity-h.json`);
the source and docs gates and dev's firmware-unit job were rerun at it. The
`886e1620` merge changes the mailbox RTL, which the shipping AX7101 image does
not elaborate, its `mbx` suite and the control-plane firmware
(`round2c/resume/dev-merge-identity-j.json`). The `mbx` suite, portability,
the vendor parser, the firmware-unit job and the source and docs gates were
rerun at `886e1620` (`round2c/gates-j/`, `round2c/vendor-j/`).

## Response to the negative reviews

This maps findings to changes and evidence. Classifications stay the reviewers'.

| Finding | Change | Evidence at this head |
|---|---|---|
| R474-1 F1: full-side asymmetry | From the full side the action drops exactly the excess above the target in every pair, in lockstep, counters unchanged; reversed offset sign added to the campaigns | `[LRC]` ten-left case and its SINGLE-DROP control; fast-sign campaigns (ring at the full edge at the switch) 64/64 |
| R475-1 F1: output-PDU span | Ruled rule: the action's repeats or drops are consecutive events within at most two consecutive output PDUs of each output, exact count, nothing outside, no grace | Six-phase capture span check, two-talker fanout, enable offsets 0 to 5, three span controls (non-consecutive, third PDU, extra repeat); physical wire check |
| R474-1 F2: sub-arm INTERNAL pull | Arm on any excursion past the two-cycle quiet band; arm disabled after an action until 2,048 quiet ticks; declared residual for a second pull inside that recovery | Full quiet distributions; fine pulls at 1/64-sample quanta; paired inside/outside pulls; NO-RECOVERY, HIGH-ARM and QUIET-ARM controls |
| R474-1 F3 / R475-1 F3: traceability | The generator credits only compiled sources; `follow_ring`'s text-copied datapath glue is marked, not credited | `gen_module_matrix.py --check` in the 28 source gates |
| R474-1 F4 / R475-1 F2: disengaged timing | `MEDIA_CLOCK_FOLLOWING.md` states the same 2,048-tick run, engaged or disengaged | Controller regression, disengaged leg, four rates |

## Classification (unchanged) and repair

#645 is the servo's pull-in phase walk accumulated in the diagnostic
listener loopback ring, outside the #386 at-switch render recentre: about
1.43 samples of walk, 0.03 sample left after LOCKED. #647 is a render-law
shift left when the INTERNAL aligner moves the grid under a running stream,
which armed no recentre. The stage-1 reproduction, traces and
classification evidence are in `HANDOFF_STAGE1.md` and `traces/`; they are
historical, not acceptance for this head.

Repair (option C as ruled): one settle recentre per transient, after the
servo reads LOCKED for 8 windows under following, or after the aligner
rests in its settle and quiet bands for 2,048 ticks at INTERNAL. A 2^20-tick
ceiling still applies. It reaches the render stage and every loopback pair.
The loopback queue is 16 deep with the derived target 11. Fewer than five
events left holds the missing pops; more than five drops exactly the excess,
in every pair together. The slip counters do not move; the render stage
counts it as a recentre.

Round 2's arm: the absolute aligner error strictly above two axis cycles
(320 ns at 6.25 MHz, 80 ns at 25 MHz, 40 ns on the shipping 50 MHz shapes,
20 ns at 100 MHz), outside recovery. After every action the arm stays off
until the engaged aligner spends 2,048 consecutive ticks inside the band;
source changes and re-engagement still arm at once.

## Quiet distributions (ruling 6010634115, item 1)

| Campaign | Cases | Windows | Samples | Quiet error | Band check |
|---|---:|---:|---:|---|---|
| Candidate (this implementation) | 128/128 rc 0 | 512 | 320,462,699 | -1..+1 axis cycle | band 2 = 2 x 1: PASS |
| Baseline (preserved four-band arm) | 128/128 rc 0 | 512 | 320,462,699 | -1..+1, identical histograms | PASS |

Phases are 16 set phases x {slow -11.02 ppm, fast +0.82 ppm against INTERNAL
-5.1 ppm} x {no lateness, 0 to 5 us uniform, 2 us plus a 1e-4 tail to 24 us,
0 to 60 us uniform}. Quiet windows are selected by stimulus time. Each run's
`[STEADY]` checks (no settle pulse, no excursion arm and no pending settle in a
quiet window) are counted in its tally; all 128 candidate runs report zero
failures. Every candidate run has exactly one settle recentre and one render
recentre per transient (384 windows), with zero loopback slips after it. The
histograms are identical sample for sample because the arm does not feed the
aligner. Of the baseline cases, 56 rest on
`round2c/resume/baseline-recovered-receipts.json`: the original driver's rc
line, plus log and binary SHA-256 values re-verified against the graded logs.

Arrival margins after the settle recentre, candidate, minimum per envelope (ticks; bar 1):

| Envelope | Empty side, slow / fast | Full side, slow / fast | Pre-settle slips max, slow / fast (bound 3) |
|---|---|---|---|
| none | 4.984 / 5.030 | 5.084 / 5.023 | 2 / 2 |
| 0 to 5 us | 4.846 / 4.854 | 4.908 / 4.908 | 2 / 2 |
| 2 us + 24 us tail | 3.848 / 3.802 | 5.100 / 5.030 | 3 / 2 |
| 0 to 60 us | 2.173 / 2.665 | 2.235 / 2.327 | 2 / 2 |

Stream-to-stream switches slipped nothing in any envelope. Late-arrival runs
report rather than grade the render law where #643's ambiguity window makes
it ungradable; the fine-pull and INTERNAL campaigns grade the law.
Receipts: `round2c/campaigns/summary.json` and per-group margins and inventories.

## Recovery and the declared residual (items 2 to 4)

All seven nonzero fine holds (25 MHz, 1/64-sample quanta) give exactly one
action. The one-quantum hold peaks at +9 axis cycles and arms. Every
completed recovery holds exactly 2,048 quiet ticks. The worst isolated
recovery window observed is 0.551148640 s (56 us hold at 6.25 MHz); the
longest fine-hold window is 0.538336080 s. Further disturbances can extend
the window without bound; the design document says so.

A second hold starting 0.10 s after an action, inside the measured
0.409918800 s recovery, gets no second action and keeps its render shift, as
declared and graded. The same hold at 1.50 s gets one new action and the law
back. The stimulus is checked against the actual recovery state.

Controls, each failing its named check (follow_ring `mutants.py`, 10/10):
NO-RECOVERY (two actions for one hold), HIGH-ARM (misses the +9 pull),
QUIET-ARM (arms in quiet), plus NO-SETTLE, SINGLE-DROP, EARLY, RENDER-ONLY,
OVERSHOOT, W1 and NO-ARM.

INTERNAL pull-in campaign (`make sweep-pullin`, 16 feed phases x 52 and
56 us holds) at `b00df050`, executable-identical to this head: 32/32 rc 0.
Every phase gets one settle recentre, 0.854 s and 0.190 s after the hold, and
no loopback slip after it. At 56 us, feed phases 0 to 3 slip once before the
settle (the declared transient). Four windows fall in #643's ambiguity window
and are reported. Table: `round2c/final-pullin/pullin.md`.

## Evidence status

| Evidence | Tree | Result |
|---|---|---|
| Source and docs gates (28 commands, including the module matrix check and the evidence selftest) | `886e1620` (also `0a196192`, `4951c471`, `f6bd415f`, `9e529b20`, `33c951fc`) | 28/28 rc 0; `measure_test_evidence_selftest.py` rc 0 at `4951c471` |
| `mbx` suite (the only suite reading the mailbox or the changed firmware sources), with the runner's verdict | `886e1620` | Wishbone 316, AXI4-Lite 361 and host model 316 checks, 0 failures; mutants 5/5 caught; verdict rc 0 |
| Default sweep shard 0/2 (60 suites, including aaf with dev's new startup sweep, follow_ring with its fine pulls, controller and ten controls, chmap_capture with the span checks, render, mclk, mbx and pp_shadow) | `f6bd415f` | 60/60 suites, 2,171,991 checks, 0 failures, rc 0 (four declared tsn_fuzz skips: generator absent) |
| Default sweep shard 1/2 (`milan_dp`, all legs) | `f6bd415f` | 12,064 checks, 0 failures, rc 0 |
| Default sweep total | `f6bd415f` | 61 suites, 2,184,055 checks, 0 failures |
| Physical (`--physical-gptp`) | `f6bd415f` | 197 checks, 0 failures, rc 0; 16.993 s simulated; two recentres on the wire, step -5 exact, inside the two-PDU span; recentre controls 14/0 |
| Render pull-in (`tdm8render-pullin`, 18 phases) | `f6bd415f` | 18/18 runs, 31 checks each, 0 failures; one settle recentre 1246.8 ms after the hold, no loopback slip; rc 0 |
| LAW boundary (`tdm8render-law-boundary`) | `f6bd415f` | 81/81 PASS over 564 windows, largest walk 3 cycles (stated 5); rc 0 |
| Builder (`--require-rv32 --require-elaboration`) | `f6bd415f` | rc 0, all gates pass; one arm NOT RUN for a recorded reason (gate 11 needs an Arty build tree absent from this host), as in earlier rounds |
| Source-list and wire-truth selftests | `f6bd415f` | rc 0, rc 0 |
| Portability (`syn/yosys/run.sh`) | `886e1620` (also `f6bd415f`) | 58 modules PASS including `KL_mbx`, tap purity PASS, rc 0 |
| Vendor parser (`xvlog_gate.py --check`, lane tree, shared lock) | `886e1620` (also `f6bd415f`) | PASS, rc 0: 0 findings in `hdl/`, 2 in the pinned processor equal to the ratchet |
| Dev's firmware-unit job (tally and RV32 selftests, control-plane and saved-state suites with the RV32 builds, coverage selftest and ratchet) | `886e1620` (also `0a196192`) | 7/7 rc 0: 18/18 and 28/28 planted cases, RV32 selftest 17 checks, control-plane PASS, 434 saved-state tests over 5 shapes, coverage PASS |
| Quiet distributions and arrival campaigns | models whose inputs are byte-identical at the head | 256/256 runs, readers rc 0 |
| INTERNAL pull-in campaign | `b00df050`, inputs byte-identical at the head | 32/32, rc 0 |
| Timing, three directives (best qualified image graded) | `f6bd415f` gateware; no gateware input changed through the head | ExtraPostPlacementOpt +0.368 ns WNS, minimum WHS +0.034 ns: PASS (at `132d79e7`: AltSpreadLogic_high +0.261 / +0.036) |
| Own area (OOC, own-logic rule) | `132d79e7`; own sources byte-identical at the head | OOC +119 LUT / +82 FF; routed bound +92 LUT / +80 FF at `132d79e7` (limit 120 / 120) |

Timing at the head's gateware (`f6bd415f` content, re-elaborated and
rebuilt), all corners at 0 and 85 C (setup WNS / hold WHS, ns). The shipping
1x1 TDM8 recipe was used: synthesis with one synthesis thread to a saved checkpoint,
then a fresh 32-thread implementation per placement directive, the
timing-grade hook, bitstream, rejected-constraint check and flash manifest.

| Directive | Slow | Fast | Critical warnings | |
|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.368 / +0.062 | +1.633 / +0.034 | 0 | selected |
| AltSpreadLogic_high | +0.039 / +0.102 | +1.434 / +0.019 | 1 (`Route 35-39`) | meets the margin |
| ExtraTimingOpt | +0.017 / +0.102 | +1.536 / +0.036 | 1 (`Route 35-39`) | below +0.030, recorded, not selected |

TNS, THS and failing endpoints are zero everywhere; speed file `-2 PRODUCTION
1.23`. All three runs produced bitstreams and manifests, with no rejected
constraint (`12-4739`, `20-1307`, `12-5201` absent). `Route 35-39` is the
intermediate route-slack warning that post-route optimisation clears. The
re-elaborated project equals the earlier one apart from dates, a comment's
order and the flash manifest (`round2c/timing-f6bd415f/elaboration/elaboration-compare.json`).
Receipts: `round2c/timing-f6bd415f/timing-current/` (per-directive corner
tables, CDC, exceptions, clock interaction, DRC, critical-warning census,
artifact hashes) and `sweep-grade.json` (rc 0). For reference, the dev
`28f9666f` manager table read +0.032, +0.345 and +0.164 ns, and this lane at
`132d79e7` read +0.129, +0.261 and +0.013 ns (`round2c/timing-current/`).
Placement in a sweep is noise-dominated; the gate grades the best image.

Area: OOC own logic +119 LUT / +82 FF (limit 120 / 120) at `132d79e7`, whose
own sources are byte-identical at the head; routed own-logic bound +92 LUT /
+80 FF in that image. Receipts: `round2c/area-ooc/`, `round2c/area-route/`.

## Reproduction

Use scratch outside the tree. Pins: processor `ead80360`, time processor
`5dce647a`, AXIS `48ff7a7e`; verify each dependency's repository root before
running Git inside it. `PACKET` is this handoff's directory.

```sh
REPO=$LANES/645-ring-slip
SCRATCH=$VALIDATION_STORAGE/645-a531/reproduce
SIM=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
cd "$REPO/tb/verilator/follow_ring"
make VERILATOR="$SIM" VERILATOR_JOBS=2 SWEEP_JOBS=4 MDIR="$SCRATCH/fr"
make sweep-pullin VERILATOR="$SIM" VERILATOR_JOBS=2 SWEEP_JOBS=4 MDIR="$SCRATCH/pullin"
make build VERILATOR="$SIM" VERILATOR_JOBS=2 MDIR="$SCRATCH/model"
python3 -B "$PACKET/round2c/campaign.py" --repo "$REPO" \
  --exe "$SCRATCH/model/Vfollow_ring" --out "$SCRATCH/campaign" --jobs 4
python3 -B quiet_distributions.py "$SCRATCH/campaign" --band 2 \
  --out "$SCRATCH/quiet.json"
cd "$REPO"
bash scripts/run_all_suites.sh "$SCRATCH/sweep"
bash scripts/run_all_suites.sh "$SCRATCH/physical" --physical-gptp
```

Expected: every command rc 0; campaign 128/128; `quiet distributions: 128
phases, 512 windows, peak 1 axis cycles; band 2: PASS`; the default `make`
ends `small pulls: 10/10 passed` and `follow_ring mutants: 10/10 caught`;
pull-in `32/32 runs passed`. `round2c/campaign.py` is scratch tooling, not
committed.

## Options and recommendation

| Option | Area | Protocol-visible effect | Test plan |
|---|---|---|---|
| A: servo phase feedback | historical OOC prototype +169 LUT / +129 FF | changes loop dynamics; does not restore an INTERNAL render phase | offset, arrival and phase sweeps; zero-gain control; integration |
| B: render-only correction | historical OOC prototype +9 LUT / +1 FF | fixes the render shift, leaves the loopback slip | both directions, fine boundaries, exact law, missing-arm control |
| C (implemented): both rings, quiet-band arm, qualified recovery | OOC +119 LUT / +82 FF; routed bound +92 / +80 | one exact consecutive action inside two output PDUs per output; counters and AAF presentation law unchanged; diagnostic loopback target 11 (+62.5 us over 8) | quiet and arrival distributions, fine and paired pulls, span and fanout controls, integration, area and timing |
| D: keep the behaviour or widen the residual | none | leaves a shift or slip outside the ruled residual | needs a new public decision |

Recommendation: C as implemented. The one declared residual is a second
INTERNAL pull starting inside the previous action's recovery window.

## Operational notes (not results)

- Dev moved four times during this resume. Each move was merged with
  `--no-ff`, and every gate whose inputs changed was rerun at the new head.
- The first vendor synthesis at `f6bd415f` content was stopped by this lane's
  own memory guard (rc -15, service peak 8.816 GB) after the reclaim threshold
  had been lowered mid-run. It was rerun with the earlier recipe's 8.75 GB
  threshold and an 8.95 GB guard (under the 9 GB ceiling); the synthesis then
  peaked at about 8.75 GB. Two driver mistakes (a path assertion and the wrong
  interpreter for the constraint checker) stopped the driver between vendor
  steps without affecting any vendor run. Receipts in
  `round2c/timing-f6bd415f/run/`; nothing from the stopped attempt is credited.

- A previous session ended on a service capacity error mid-run; its
  interrupted shard 0/2 and campaign cases were rerun, never credited.
- On resuming, overlapping launches briefly ran up to three writers per case
  log for under two minutes. All were stopped and every affected case was
  rerun by one driver (`round2c/resume/duplicate-start-a531k.json`).
- One gate relaunch ignored SIGHUP in its children, so the sweep's own
  hard-HUP cancellation control timed out in preflight (rc 2). It was
  relaunched without that; nothing from it is credited
  (`round2c/resume/gate-launch-nohup-abort.json`).
- Earlier resource interruptions, vendor scheduling, the memory guards
  and their receipts are described in `HANDOFF_ROUND2C_INTERIM.md`.

Large logs, checkpoints and executables remain in
`$VALIDATION_STORAGE/645-a531/round2c/`; this packet keeps text receipts under
200 KB, with size and SHA-256 for the rest. Hardware, flashing, push and PR
edits were not performed.


## Round 2e

Assignment: [#645 comment 6050481968](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6050481968).
Starting head `2525eae9567865a8bc741901914bdf5a1caf2c26` was confirmed against
PR #672. Origin is `https://github.com/kebag-logic/milan-fpga.git`.

**Status: REVIEW READY**, head
`85db353400c6bf3965d279a9f5b5d47e08a0d1ed`.

Public handoff: [A531 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6056511818).

### Merge and wording corrections

| Commit | Change |
|---|---|
| `9a0d68e2016c0385171107277721aa187ce19674` | Merge dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240` with `--no-ff`; clean automatic merge, no conflict resolutions |
| `85db353400c6bf3965d279a9f5b5d47e08a0d1ed` | R474-3-R1: mutation-driver usage and four capture controls; R474-3-R2: TESTING.md links the complete twelve-control list |

Processor pin: `2ad2f845dd583f8310075fa2380cb60a04fd091a`.
Time processor: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.
AXIS: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
Each dependency's repository root was verified before its Git commands.
No RTL was authored in this round.

Scratch and complete raw logs are under `$VALIDATION_STORAGE/645-a531/round2e`.
Each launched job has a command record under `jobs/` and a log, return code
and receipt under `logs/`. The source exports stay there, outside this packet.
`functional.log`, `functional-continuation.log`, `parallel-sweeps.log`,
`litex.log` and `firmware-shards.log` record scheduling. The continuation
supervisor waited for existing jobs and started independent render campaigns
from separate source exports; it did not restart completed gates.
`vendor_bank.py` ran serially; `vendor.log` records each job and its return
code.

### Changed inputs and validation scope

| Merged input | Required evidence |
|---|---|
| Processor gitlink; mailbox RTL, generated contract and firmware | Full parent sweep, including datapath pool, loopback and render; physical-gPTP leg; firmware tests, RV32 build and coverage; source and protocol gates |
| Datapath NxN harness; simulation infrastructure and generated transmit chain | Full parent sweep; explicit render default, pull-in, LAW boundary and `tdm8render-mutants`; comparison with dev for #657 |
| Shared media-plane inputs and processor | follow_ring default and all twelve controls, 128 arrival cases and quiet reader, 32 INTERNAL pull-ins |
| GMII capture patch and build inputs | Builder including gate 23h; cycle fixture; shipping elaboration and full three-directive timing sweep with the complete IOB check |
| Resource baseline and measurement helper | `check` against the recorded route-1x1, ooc-1x1 and ooc-8x8 baselines; own logic compared with merged dev |
| Documentation and review wording | All 28 source/documentation gates |

### Functional results at the merged head

Shared infrastructure was treated as affecting the entire validation set.
`round2e/validation-scope.json` maps all 93 changed paths to their checks;
`round2e/merge-audit.json` records the automatic merge tree and zero conflict
resolutions. Credited commands returned 0 except the explicitly compared
#657 campaign below. Command vectors, working directories and return codes
are retained in `round2e/commands.json`, `round2e/jobs/` and
`round2e/source-gates/commands.json`.

| Gate | Result |
|---|---|
| Default sweep | 61/61 suites; 2,185,760 checks; zero failures, including datapath pool, loopback and render |
| Source/documentation gates | 28/28, rc 0 |
| follow_ring | Default suite, small pulls 10/10, all 12 mutation controls caught; settle controller at 6.25, 25, 50 and 100 MHz |
| Capture ring | 785 behavioral checks and 20 netlist checks, zero failures |
| Arrival campaign | 128/128; every log byte-identical to Round 2d; 384 post-settle windows with one settle pulse and render action, zero post-settle slip; minimum empty/full margins 2.17344 / 2.23488 ticks |
| Quiet reader | 128 phases, 512 windows; peak 1 axis cycle against band 2; statistics byte-identical to Round 2d |
| Standalone INTERNAL pull-in | 32/32, logs byte-identical to Round 2d; 28 on-law cases and four not gradable in the documented ambiguity band (two before, two after); one recentre and zero post-settle slip in every case |
| Full render pull-in | 18/18 phases, 558 checks, zero failures; all phases gradable; zero slip during the pull or after settling |
| Render LAW boundary | 81/81 checks over 564 windows; largest measured walk 3 cycles against the stated bound of 5 |
| Physical gPTP | 197 checks, zero failures: main 143, setup-abort 6, no-TX 20, no-Pdelay 14, recentre controls 14 |
| Firmware | Unit, NVM, RV32, tally, image and image controls rc 0; coverage gate passes all 20 files |
| Firmware mutations | 469/469 caught exactly once in four disjoint contiguous slices: 118 / 118 / 118 / 115; each command rc 0 |
| Specification suite | 14 features, 404 scenarios, 1,968 steps passed |
| Builder | rc 0, including gate 23h and all 5 missing-patch controls |
| Build-environment simulations | 5/5 simulations and 10/10 controls |
| GMII capture fixture | 1,036 cycle comparisons, nine direct pad registers, all 6 structure controls caught |
| Portability | 58/58 tops; tied-input check passes with two justified and zero unjustified ties; tap-purity check has zero violations |
| Vendor front-end | rc 0, zero findings across 81 owned RTL and 52 pinned processor files |

Four standalone 56-us pull-in cases, phases 0 to 3, each show one slip during
the pre-settle transient. This is unchanged from Round 2d; the claim is zero
slip **after** the settle. The full render campaign settles about 124,683,570
axis cycles (1,246.8 ms) after the hold. Detailed classifications and per-case
hashes are in `campaign-summary.json` and `render-summary.json` under
`round2e/`.

The physical trace independently observes both declared actions:

```text
RECENTRE WIRE decision=1 output_pdu=9822 declared_step=-5 observed_step=-5 events dup=0 skip=0
RECENTRE WIRE decision=2 output_pdu=95985 declared_step=-5 observed_step=-5 events dup=0 skip=0
```

See `round2e/physical/milan_dp_gptp.log` lines 518 and 689 and the retained
negative-control transcripts in `round2e/physical-controls/`.

### #657 comparison

| Revision | Result | Exit |
|---|---|---|
| Dev `99e4eb6c` | 28/32 passed; four known failures | 2 |
| Candidate `85db3534` | 30/34 passed; the same four failures | 2 |

All 32 shared outcomes match exactly, including the four failing lines:
the clean epoch leg, the acknowledgement-level and serial-reset arrival-skew
clean controls, and the surviving uncounted-repeat mutation. The candidate's
two additional checks pass: clean pull-in and the missing-settle mutation.
There is no observed merged-suite regression. This is the assignment's
accepted comparison, not a claim that the full mutation gate is clean.
Evidence: `round2e/mutation-comparison.json` and both campaign logs.

### Uncredited work and execution attempts

The optional external TSN field campaigns were skipped because their generator
is absent. Builder gate 11, the historical Arty calibration arm, was NOT RUN
because its report is absent. Neither is credited. Hardware, flashing and
bench campaigns remain outside this assignment.

Initial sweep preflights inherited ignored SIGHUP from their detached launcher
and failed their hard-HUP cancellation control before any suite ran. After
restoring the default signal disposition, both complete shards passed. The
initial specification-suite invocations used a missing executable and then an
incorrect working directory; the corrected complete invocation passed. The
first 8x8 elaboration used an incorrect configuration name and was corrected
before the successful elaboration. These attempts remain in the receipts.

The serial firmware mutation run was interrupted to partition it. Initial
interleaved `--mutation-shard INDEX 4` attempts trimmed the table before the
global named-test coverage check and reported uncovered tests; they were
interrupted and receive no validation credit. The documented
`--slice K/4 --jobs 4` invocations preserve that check and passed all 469
controls exactly once. The driver and coverage code are byte-identical to
dev `99e4eb6c`. See `round2e/firmware-sharding-comparison.json` and
`round2e/firmware-summary.json`.

### Three-directive shipping timing sweep

The sweep passes under the [#691 best-image ruling](https://github.com/kebag-logic/milan-fpga/issues/691#issuecomment-6045752839).
**Kept: AltSpreadLogic_high**, worst setup **+0.066 ns**, worst hold
**+0.024 ns**. Shipping synthesis and each implementation returned 0.
Every image passed constraint validation and manifest generation.

Values below are setup WNS / hold WHS in ns. The 0 C and 85 C reports give
the same values within each listed corner. TNS, THS and failing endpoints
are zero in all twelve reports; speed file is `-2 PRODUCTION 1.23`.

| Directive | Slow, 0 C and 85 C | Fast, 0 C and 85 C | Full IOB check | Margin grade |
|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.057 / +0.102 | +1.642 / +0.024 | 21 PASS, 1 INERT, 0 FAIL | Pass |
| AltSpreadLogic_high | +0.066 / +0.055 | +1.660 / +0.024 | 21 PASS, 1 INERT, 0 FAIL | Pass; kept |
| ExtraTimingOpt | +0.011 / +0.102 | +1.633 / +0.036 | 21 PASS, 1 INERT, 0 FAIL | Below +0.030 setup; not selected |

All nine GMII RX registers occupy ILOGIC sites in every row, including RX
valid at `ILOGIC_X0Y119`. The one INERT endpoint is `eth0_rx_er`: it
has no net and nothing drives or reads the pin, as the complete shipping
IOB checker verifies. There are zero critical warnings in synthesis and
each implementation. No rejected constraint was reported. The third row's
low positive setup result is recorded; it does not supply the kept image.

Evidence: `round2e/timing-summary.json`, per-directive corner reports and
critical-warning records, IOB reports, constraint return codes and manifests.
The kept bitstream is 3,825,992 bytes, SHA-256
`7b0c5eead7a68221c47e1f16077ec8ddbc3ca3631a033ff3e5e9235881c09977`.
Its manifest is 616 bytes, SHA-256
`76f092615a88014219ca74f234396a5680f040816e8202e66c93c22f2451859a`.
`round2e/kept-artifact.json` binds both to the candidate head.

### Resource checks and own-area limit

All three repository resource checks pass, rc 0, against the recorded
baseline. Each recipe identity matches. No baseline was changed.

| Endpoint | Baseline LUT / FF | Candidate LUT / FF | Delta LUT / FF | Candidate RAMB36 / RAMB18 | DSP | Result |
|---|---|---|---|---|---|---|
| route-1x1 | 49,957 / 54,274 | 49,913 / 54,309 | -44 / +35 | 74 / 27 | 14 | PASS |
| ooc-1x1 | 23,179 / 19,779 | 23,179 / 19,779 | +0 / +0 | 16 / 3 | 8 | PASS |
| ooc-8x8 | 30,135 / 27,380 | 30,135 / 27,380 | +0 / +0 | 21 / 5 | 8 | PASS |

The route is complete with no unrouted net or routing error. Its slice count
is 15,754 versus 15,734 (+20), with 87.5 BRAM tiles unchanged. The recorded
route recipe's WNS is +0.057 ns versus +0.124 (-0.067); WHS is +0.024 ns
versus +0.031 (-0.007). All are within the recorded policy. RAM and DSP
comparisons are retained in each endpoint report. OOC timing is characterization;
the shipping sign-off result is the kept image reported above.

The separate own-area comparison uses the exact dev and candidate capture
and settle logic, shipping 1x1 generics, and a 20 ns axis clock:

| Component | Dev LUT / FF | Candidate LUT / FF | Delta LUT / FF |
|---|---|---|---|
| Settle and existing source recentre | 41 / 51 | 74 / 93 | +33 / +42 |
| Capture ring | 1,076 / 1,336 | 1,156 / 1,372 | +80 / +36 |

**Own delta: +113 LUT / +78 FF; limit 120 / 120: PASS.**
The four separate synthesis commands and the area grade returned 0.
Evidence: `round2e/resource-summary.json`, the three resource-check logs,
`round2e/area-ooc/comparison.json`, and `round2e/area-source-audit.json`.
The GMII good/bad placement fixture also returned 0.

### Disposition and recommendation

**REVIEW READY at `85db353400c6bf3965d279a9f5b5d47e08a0d1ed`.** The assignment's merge, both wording
corrections and affected verification are complete, with the expressly
accepted #657 comparison. No STOP condition was triggered. This is an author
handoff; independent review and the protected publication/merge gates remain
required.

Recommendation remains option C, the implemented correction of both rings.
Its fresh own-area result is +113 LUT / +78 FF, and the
kept shipping image clears the timing and IOB bar. The classification,
protocol-visible effects, alternatives and test plans retained in
`HANDOFF.md` remain applicable. Alternative prototype area figures are historical, not
new measurements. The declared residual remains a second INTERNAL pull
starting during the previous action's recovery window. The diagnostic
loopback target remains 11 events; the AAF presentation law is unchanged.

The final tree and all three dependencies are clean at the recorded pins.
Both new first-parent commits have one-line subjects and no body or trailers.
Every job has ended. Peak service memory was
13.357 GB, below 17 GB. Vendor jobs
ran serially under the shared lock; the 8x8 OOC job waited behind another
service's run. No heavy functional build overlapped a vendor job in this
service. See `round2e/final-audit.json`, the command receipts and
`round2e/vendor.log`.

### Reproduction and evidence

Use the candidate and dependency revisions listed above. Before each Git
query within a dependency, verify that its top-level directory is that
dependency. Use external scratch and separate frozen source exports for
independent builds; the receipts in `round2e/functional/exports-*.json`
bind those exports to the exact revisions. The dev comparison uses
`99e4eb6c`, with its own recorded dependency pins.

The following are the principal executed commands. `$WORK` denotes scratch,
`$REPO` the appropriate source export, `$PACKET` this evidence packet and
`$SIM` the pinned simulator executable. The command records supply exact
working directories and all other gates. Absolute roots in retained receipts
and helpers are normalized to these placeholders; replace them with the chosen
roots when replaying a helper. Long jobs use separate detached
sessions, logs and rc files, followed by foreground waits; independent
functional jobs run concurrently, while vendor jobs run serially under the
shared lock with no heavy build beside them.

```sh
# From the two candidate sweep exports, one command per export:
bash scripts/run_all_suites.sh "$WORK/sweep-rerun/0" --shard 0/2
bash scripts/run_all_suites.sh "$WORK/sweep-rerun/1" --shard 1/2
# From the candidate physical-clock export:
bash scripts/run_all_suites.sh "$WORK/physical" --physical-gptp

# From the candidate follow_ring directory:
make -j16 build MDIR="$WORK/follow-model"
python3 -B "$PACKET/round2e/campaign.py" --repo "$REPO" \
  --exe "$WORK/follow-model/Vfollow_ring" --out "$WORK/arrival" --jobs 16
python3 -B sweep.py pullin --exe "$WORK/follow-model/Vfollow_ring" \
  --out "$WORK/follow-pullin" --jobs 16 --hold-us 52 56
python3 -B quiet_distributions.py "$WORK/arrival" --band 2 \
  --out "$WORK/quiet.json"

# From separate candidate milan_dp_render exports:
make -j16 tdm8render-pullin PULLIN_JOBS=16
make -j16 tdm8render-law-boundary LAW_BOUNDARY_JOBS=16
# Once on the candidate and once on dev, with separate logs:
make -j16 tdm8render-mutants

# From candidate roots; repeat the mutation command for slices 1/4 through 4/4:
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py \
  --require-rv32 --self-test --slice 1/4 --jobs 4
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
bash syn/yosys/run.sh
```

Set `VERILATOR` to the pinned 5.050 executable. The functional runner records
`MAKEFLAGS=-j16`; the compile wrapper bounds simultaneous compiler work to
stay within the service memory limit. No gate output is piped into another
command. The expected mutation exception is exactly the #657 comparison
above; other credited gates require rc 0.

Shipping elaboration uses `build.sh ax7101 --dry-run` and
`build.sh ax8x8 --dry-run`, the shared environment with patch 0007, and the
recorded argument vectors under `round2e/timing/elaboration/`. The baseline
helper creates the recorded recipe with `--single-thread-synthesis` (plus
`--synthesis-only` for the integrated 8x8 input). Shipping synthesis runs
once to a checkpoint. Each implementation reopens that checkpoint and runs
the unchanged baseline tail with its assigned placement directive, including
the complete IOB hook, routing, four corner reports and bitstream. Constraint
validation and manifest generation follow each successful image.

The route resource endpoint uses ExtraPostPlacementOpt, the recorded recipe,
regardless of which image the timing sweep keeps. Both OOC preparations use
`--integrated-clock --single-thread-synthesis` and the corresponding
integrated synthesis log. The required comparisons are:

```sh
python3 -B syn/ooc/pp_resource_gate.py check "$WORK/timing/ax7101/gateware" --endpoint route-1x1
python3 -B syn/ooc/pp_resource_gate.py check "$WORK/timing/ooc-1x1" --endpoint ooc-1x1
python3 -B syn/ooc/pp_resource_gate.py check "$WORK/timing/ooc-8x8" --endpoint ooc-8x8
```

`round2e/area-ooc/prepare.py` reproduces the separate own-area extraction
from the repository at the candidate head and dev `99e4eb6c`.
`round2e/area-source-audit.json` proves that the captured source inputs match
those commits. The OOC recipe runs `settle_base`, `settle_head`, `cmc_base`
and `cmc_head` separately, with shipping 1x1 generics and a 20 ns axis clock.
Its grade sums the two head-minus-base LUT and register differences against
the 120/120 limit.

Each vendor invocation holds the shared `milan-vivado.lock` and has its own
log, rc and memory receipt. `vendor.log` records the serial schedule.
The packet retains text files below 200 KB; large reports and logs have
bounded excerpts plus original sizes and SHA-256 in `inventory-*.json`.
Checkpoints, bitstreams, generated HDL and source exports are represented by
hashes and sizes rather than copied into the packet. These excerpts are
labelled and are not presented as complete logs.


## Round 2f: merge-result resource re-baseline

[Assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6061613334), following the [composition review](https://github.com/kebag-logic/milan-fpga/pull/672#issuecomment-6061607463).

Status: REVIEW READY.
Public handoff: [A531 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6066156323).
Final head: `4640d995913cb93653a47e73856e8bd7dfe7c428`.
Records commit: `Re-baseline merged listener settle resource records`.
Measurement head: `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`.
It merges requested dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246` into
round-2e head `85db353400c6bf3965d279a9f5b5d47e08a0d1ed` with `--no-ff`.
The merge had no conflicts. Its tree, `47e1e22d511016d3772c33419afc84ca88930f55`,
is exactly the composition review's candidate tree.
Required dependencies were initialized; each root was verified before its
repository commands. Pins: processor `2ad2f845`, time-sync processor
`5dce647a`, streaming library `48ff7a7e`, reservation library `9197193e`.
`resource-receipts/merge-admission.json` records full identities.

### Measurements and policy

The preceding records describe #686's inputs at `e519e31f`.
All three comparisons against those records exited 0 before any record
was replaced. Every `record --write` also exited 0.

| Endpoint | LUT (delta) | FF (delta) | Slices (delta) | RAMB36 / RAMB18 | DSP | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|
| route-1x1 | 50,267 (-124) | 54,413 (+150) | 15,779 (-9) | 74 / 27 | 14 | +0.299 / +0.031 |
| ooc-1x1 | 23,179 (0) | 19,779 (0) | - | 16 / 3 | 8 | -3.562 / +0.159 |
| ooc-8x8 | 30,135 (0) | 27,380 (0) | - | 21 / 5 | 8 | -2.278 / +0.159 |

Every RAMB36, RAMB18 and DSP delta is zero. Route CARRY4 changes by +30;
standalone CARRY4 is unchanged. The route leaves 71 slices free.
WNS improved by 0.058 ns and exceeds the +0.030 ns floor by 0.269 ns.
WHS improved by 0.002 ns and exceeds its zero floor by 0.031 ns.
There are no unrouted nets or routing errors; the full IOB check passes.
Slow corners at 0 and 85 C have WNS/WHS +0.299/+0.063 ns; fast corners
have +1.434/+0.031 ns. The critical setup path has 14 levels and 9.294 ns
data delay, including 7.331 ns of routing.
Standalone timing has no I/O constraints and does not establish an 8x8 route.

All measurement identities match the preceding baseline. Both integrated
runs and both standalone runs use one synthesis worker; the route keeps
the recipe's `ExtraPostPlacementOpt` placement and 32 general workers.
The 8x8 integrated run supplies bound parameters, and the standalone
clock is the shipping 20 ns. The four processes ran serially under the
shared lock, with no heavy functional build overlapping them.
Peak sampled service memory during measurement: 13,151,162,368 bytes, below 17 GB.

Policy is unchanged. Its canonical SHA-256 before and after is
`f0e6babaeeff50eb098f3ea2e55ca8cd76ee746f83134f44c6c958f85a581158`.
Every stored record equals the measured record. The budget still records
the unmet 60% LUT target: this route is 12,227 LUTs over it. At the new
WNS record, the unchanged 0.25 ns fall rule requires a comparable candidate
to retain at least +0.049 ns; the absolute floor remains +0.030 ns.

### Reproduction and receipts

The standing recipe is `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
`resource-receipts/measure-commands.json` contains every executed argument
vector, working directory, rc, elapsed time and sampled memory peak.
`ax7101-argv.json` and `ax8x8-argv.json` retain the shipping elaboration
arguments from the builder dry runs; only the external output destination
and omission of `--build` separate elaboration from the recipe steps.
Use those arguments at the measurement head with the same patched build
environment. The recipe helper was given `--single-thread-synthesis`;
standalone exports additionally received `--integrated-clock` and their
completed integrated log. Executed Tcl is retained for all four runs.

`baseline-before.json` preserves the preceding records;
`commands/check-*.log` and `.rc` preserve the three comparisons;
`record-commands.json` and `commands/record-*.log` preserve the writes.
`policy-audit.json`, `measurement-summary.json` and `input-audit.json`
record policy equality, deltas, and source/header/memory-image rehashes.
Each measurement has six memory images; no source or image changed during
measurement, and no completed log reports a missing memory image.
The input SHA-256 values are:

| Endpoint | Input SHA-256 |
|---|---|
| route-1x1 | `95a6cc95786fa743da28e2aa603d3a6af08200c86bf4bb7c452aeba7ec072c4c` |
| ooc-1x1 | `2dd522bd12b3480a8817cf2bb3dd969ac7be6f3d80be70d13fe32ce5576011a5` |
| ooc-8x8 | `5604984543f875b19f344900a8b183adf81281c02ba42517ff894502f7a07f0c` |

`resource-receipts/inventory.json` records the original SHA-256 and byte
size of every retained or inventoried artifact. Executed Tcl, input
manifests, utilization, route status, timing, IOB results and gate output
are retained in full when within 200 KB. Larger artifacts remain outside
this packet, with size/hash receipts and clearly labelled text excerpts.

### Verification

The full builder command exited 0. Gate 23h reproduced the five-patch
series byte for byte across four installed files, and all five missing-patch
controls were rejected. No elaboration arm was skipped for a toolchain
reason. Historical gate 11 calibration did not run because its mf48 placed
report is absent; this verdict does not cover that unrelated calibration.
Portability passed all 58 tops and its structural checks. Firmware,
MAAP, capture ring, the standing follow-ring suite, default render and the
corrected datapath suite all exited 0. The render pull-in campaign passed
18/18 phases, 558 checks, zero failures and no ungradable windows.
The main physical-rate integration scenario also passed: 143 checks over
16.992556520 simulated seconds, 6,517,392 payload comparisons, 814,672
sample-order comparisons and 135,935 packet-sequence comparisons. Both
observed recentres completed on the wire. All 54 failure-control checks
passed: setup abort 6, no-TX accounting 20, no-Pdelay accounting 14, and
recentre controls 14. The complete suite exited 0. Traffic in this physical-rate test uses the diagnostic AAF bypass;
licensed streaming is not its claim.
All 39 source, documentation, policy and negative-control checks completed
with rc 0. The extra hierarchy ranking command also completed with rc 0.
The resource self-test passed 260 arms and 500 generated cases; its mutation
campaign rejected 174 of 174 defects. Recipe self-tests and mutants passed.

Two invocation failures are retained: the ranking formatter was first given
an unsupported `--selftest` option (rc 2), then invoked with its actual
report/root arguments (rc 0); the datapath pool rejected `SIM_JOBS=8`
(rc 2), then passed with rc 0 using the documented ceiling of 2. Neither
failure changed RTL, tests, expectations or policy. Final command receipts
are under `round2f-verification/`.

Final execution commands are recorded per job in `round2f-verification/jobs/`
and `checks/`. The suite builds used external build directories whose
tracked bench inputs were checked byte for byte against the lane. The
following commands describe the repeated scope; `$BENCH` is that staged
bench directory and `$PHYSICAL` is its separate physical-rate build directory:

```sh
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$WORK/firmware"
make -C "$BENCH/follow_ring" -j16 SWEEP_JOBS=8
make -C "$BENCH/maap" -j16
make -C "$BENCH/chmap_capture" -j16 run netcheck
make -C "$BENCH/milan_dp" -j16 SIM_JOBS=2
make -C "$BENCH/milan_dp_render" -j16
make -C "$BENCH/milan_dp_render" -j16 tdm8render-pullin PULLIN_JOBS=16
make -C "$PHYSICAL/milan_dp_gptp" -j16
bash syn/yosys/run.sh --results "$WORK/portability"
python3 -B syn/ooc/pp_resource_gate.py check-baseline
python3 -B syn/ooc/pp_resource_gate.py --selftest
```

`source-gate-spec.json` gives the exact source/documentation and recipe
control invocations. Two compile slots, each with four compiler workers,
bounded memory without changing model parameters. Independent groups ran
concurrently; each long job had its own detached process, log and rc file,
with bounded foreground waits.

### Final admission

The 50 effective verification commands all exited 0. Their retained initial
supervisor exited 1 because it includes the two rejected invocations;
`final-verification.json` explicitly maps each to its successful corrected
receipt. No test, assertion or policy was changed to obtain a pass.
Five post-commit checks also exited 0: punctuation against dev, resource
policy, the full PR diff, documentation and documentation paths after
removing the three temporary build links. The final audit binds the tested
file hashes to the committed bytes and confirms that exactly the baseline
JSON and two area documents changed after the measured merge.

Peak sampled verification memory: 11,493,605,376 bytes.
Peak sampled memory across measurement and verification: 13,151,162,368
bytes, below 17 GB. All jobs have ended. The worktree and all four
submodules are clean. Both first-parent commits have one-line subjects,
without bodies or trailers. The recorded measurement head remains distinct
from the final records/documentation head.

### Classification, scope and recommendation

This round updates measurement records and authoritative area documentation;
it adds no protocol-visible behavior. The prior diagnosis, option analysis,
settle action, residual recovery limitation and protocol test plan remain
in the earlier sections. The prior +113 LUT/+78 FF own-area result is
historical evidence accepted by the composition review. Whole-image mapping
changes in this round are not an isolated cost estimate of the settle logic.

Recommend independent review of the new records and documentation.
All assigned final verification commands passed. The assigned three-endpoint resource comparison
passes without changing policy. This round does not repeat the earlier
three-directive timing sweep or the full arrival-envelope campaign.
Broader merge-bank, hosted-context, independent review and physical bench
obligations remain with the integration handoff. Desk and physical-rate
simulation results do not discharge hardware acceptance. Earlier rounds
and their fix options remain above.


## Round 2g: default-suite wall clock

Complete raw build/log root: `$VALIDATION_STORAGE/645-a531/round2g`.
Public STOP: issue #645 comment 6074038320.
Candidate head: `1e79ebdc06528edff74c0a7f530f20f99e3326a2`.
Parent: `4640d995913cb93653a47e73856e8bd7dfe7c428`.
Assignment: issue #645 comment 6073617515.
Review addressed: PR #672 comment 6073609394, R474-4-F1 and R474-4-R1.
Status: STOP pending manager publication and exact-head hosted evidence.

### Change and classification

The review's failure was default-suite wall clock: both suites hit the
1,800-second hosted guard. The retained hosted receipt compares the dev-class
runner with the faster earlier candidate run. This round changes scheduling
inside existing targets, with no RTL, interface, protocol, source-list,
suite-list or timeout change. R474-4's Tests and Docs finding still needs
independent re-review; these are author verification results.

- `follow_ring` defaults to its four existing legs: `b8`, `pullin`,
  `small-pullin` and `settle-control`. Its twelve rebuilt defects remain
  executable through `make mutants`.
- The render default keeps both shapes, all eighteen LAW phases, and the
  five leg-side positive/negative controls. `--with-pullin` preserves the
  former standing pull-in at its original position after serial/CRF/LAW.
  The existing `tdm8render-pullin` target runs that history plus eighteen
  fresh-boot phases. No grading function, wait bound or stimulus duration
  changed. `scope-audit.json` binds the unchanged phase implementations.
- TESTING.md declares both explicit campaigns and the manager merge bank
  as owner. Its second test-plan link now lands on `#simulation`, which
  contains the controls column; the settle-recentre link remains. The
  existing-source-recentre locator now names `g_src_recentre`.
- The old 152.6 ms fresh-boot comment was stale. The measured standalone
  case takes 1,246.8 ms of simulated time after the hold; its corrected
  comment keeps the existing two-second guard.

### Cold default wall clock

| Default command | Measured seconds | At 1.58x | Limit | Result |
|---|---:|---:|---:|---|
| `make -j16` in `follow_ring` | 354.107 | 559.489 | 1440 | rc 0 |
| `make -j16` in `milan_dp_render` | 733.249 | 1158.533 | 1440 | rc 0 |

Both satisfy the assigned ceiling, 80% of the unchanged 1,800-second guard.
The committed page and Makefile headers round these figures to one decimal.
Both object trees started empty. The suites ran concurrently with the builder;
the later controls overlapped the render default's tail. Outer make used
`-j16`; a two-slot compile wrapper limited each elaboration to four compiler
workers. Elapsed time includes compilation, simulation, controls and queueing,
measured monotonically with a one-second completion poll. No gate output was
piped. Each background job had its own log and exit-code receipt and was
waited to completion.

A standalone, fully graded one-case render smoke (`--pullin`) passed all 33
checks in 591.216 s. Adding it to the measured default gives 1,324.465 s,
or 2,092.655 s at 1.58x, beyond the assigned limit. It remains explicit.
No shorter settling wait or weaker grading is substituted. The four-leg
`follow_ring` default still retains its INTERNAL pull-in and fine-pull cases.

### Reproduction and receipts

Set `LANE` to this candidate, `WORK` to an empty external build directory,
`SIM` to the pinned 5.050 executable, `RV32_SDK` to the existing compiler
installation, and `LITEX_PYTHON` to the interpreter with the required patches.
The retained helper recipes describe the isolated bench input copy, compiler
limit, environment, and detached job launcher. This build directory contains
no Git checkout. `bench-inputs.json` records every staged bench file by hash;
source directories reference the verified candidate. Neither generated files
nor build outputs belong in the repository or this evidence packet.

The commands, run from the corresponding staged suite directory, were:

```sh
make -j16
make -j16 mutants SWEEP_JOBS=4
make -j16 tdm8render-pullin PULLIN_JOBS=6
./obj_tdm8r/Vmilan_dp_tdm8r --pullin
python3 -B "$WORK/check_pullin_control.py"
```

The first command was run once per cold default. The second belongs to
`follow_ring`; the remaining commands belong to `milan_dp_render`. The
render campaign started with six children; ten GNU xargs parallelism
increments were requested after the ring controls completed. The request
and observed child count are retained in `campaign-parallelism.json`.
Using `PULLIN_JOBS=16` reproduces the same nineteen independent cases.

The focused negative uses the existing `tdm8_render_mutants.py` plant,
build, run and verdict functions for its named no-settle mutation, on a
scratch copy only. Its raw negative exit is 1 as expected; the control
runner exits 0 only when the named law check fails. The positive binary
must pass beside it. This does not claim a repeat of the unrelated full
render mutation campaign or erase the earlier #657 exception.

Source and documentation gates run from the candidate:

```sh
python3 -B scripts/measure_test_evidence.py --check
python3 -B scripts/measure_test_evidence.py --selftest
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
```

`jobs/gate-*.command.json` retains all 32 source/documentation command
vectors, including the pinned Markdown interpreter. Their matching `.rc`
and `.result.json` files record success. The final comment-only edit was
followed by repeated C++ idiom, wording and diff checks, also rc 0. The
scheduling checker and 105-check self-test both pass. Suite/target discovery
is unchanged, so `run_all_suites.sh`, the evidence pins and CI_WORKFLOWS.md
remain byte-identical to the parent.

| Evidence | Result |
|---|---|
| Cold follow_ring | b8 48/0; pullin 18/0; fine pulls 10/10; controller at four rates; rc 0 |
| Cold render default | shipping 258/0; second shape 71/0; leg-side controls 5/5; rc 0 |
| Explicit ring defects | 12/12 caught by their named checks; rc 0 |
| Explicit render campaign | rc 0; 19/19 legs, 830 checks, zero failures; includes the preserved history |
| Standalone pull-in | 33/0, 591.216 s; rc 0 |
| Missing-recentre control | named first-event law check fails; raw rc 1; control runner rc 0 |
| Source/documentation | 32 commands plus three final repeats, all rc 0 |
| Evidence contract | check rc 0; self-test 105/105, rc 0 |
| Builder | rc 0; no elaboration arm skipped for a toolchain reason; historical gate 11 uncovered |

The builder's gate 11 requires a placed utilization report that is absent.
Its calibration claim remains uncovered, as recorded in Round 2f. This
round does not claim a new hardware, placement or area measurement.

The standalone trace recentres after 124,683,570 axis cycles (1,246.8 ms),
then grades fill 14 and first-event delay 8.733..8.734 media ticks, with zero
loopback slips after the recentre. The preserved history recentres after
132,771,070 cycles (1,327.7 ms) and passes all 272 checks with zero later
loopback slips. The negative trace, phase logs and command receipts are in
this round's packet. `receipts.json` records raw and retained hashes/sizes;
home and build roots in retained text are replaced by variables. Files over
200 KB are represented by hashes, sizes and bounded excerpts.

`measured-source-binding.json` records both measured and committed hashes.
Only full-line comments changed after the cold runs: measured times and
the stale settling-time note. The non-comment text is identical.

### Area, protocol effect and recommendation

The selected split has zero RTL delta: no LUT, register, memory, timing,
wire-field or stream-behavior change is introduced by this round. The
Round 2f resource records and their stated limits remain applicable.
Earlier diagnosis, fix options, area comparisons and physical acceptance
obligations remain in the preceding rounds.

Retain the split and the declared manager-owned campaigns. Publish this
candidate, run the required replication and obtain a passing hosted
`verilator-suites` result on this exact head, then seek independent re-review
and post REVIEW READY. Hosted success is not established by these timings.
No merge or further RTL work is authorized by this handoff.
