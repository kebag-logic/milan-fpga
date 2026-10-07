[A531]

# Round 2d handoff (#645, #647): settle-held walks never count as loopback dups; STOP at the timing gate

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
