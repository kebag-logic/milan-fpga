# [A700c] milan-fpga #787 round 2 (extended) handoff: no PHY hold before the egress path has drained

Status: REVIEW READY at head `667b9bbc`. The fix, its tests, mutants and docs, the re-pin to processor PR #209's merge commit and the records are committed, and every gate below is rc 0, with xvlog not run (a Vivado tool; no Vivado this round). Neither STOP condition is met. Not pushed; no PR opened; PR-BODY.md is ready for one.

## Assignment

- Issue #787. Round 2, extended: [A10] issuecomment-6518083444 (the silicon defect, done first) and
  issuecomment-6517663056 (the re-pin round). Round 1: issuecomment-6493879824.
- Executor [A700c]. TAKEN: issuecomment-6518452658. REVIEW READY: issuecomment-6523288182 (`review-ready.md`); these two
  are the lane's only posts this round. A700b was stopped; its commit `0d4be94c` is kept and its
  working tree was reviewed (below).
- Processor pin: **`a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`**, the merge commit of processor PR #209 (#203). The PR was
  OPEN at the start, with `0d4be94c` pinning its reviewed head `013ee63f`. It merged at 09:02 UTC during this round, so
  `667b9bbc` re-pins to the merge commit, as the re-pin assignment requires. Its tree `b0f66acb` is `013ee63f`'s, and the
  processor diff between the two is empty. The ROM ledger rows, the boundary diagram and its PNG manifest were
  regenerated through `ooc.sh --record-rom-digests` and `submodule_boundaries.gen.py`; the pin table and the adoption
  prose were updated and pass `check_submodule_docs.py`.

## Base and head

- Repository milan-fpga, branch `787-reboot-reset`; `git remote get-url origin` is
  `https://github.com/kebag-logic/milan-fpga.git`. Base dev `1e80128f` (`git merge-base` checked; the live remote
  `dev` is still `1e80128f`, `git ls-remote`). Commits added on top of `0d4be94c`: no rebase, no force, no push.
- **Head: `667b9bbc02b99a08d71efab750f95e8702cbbe57`.**

| Commit | Subject |
|---|---|
| `15796754` | Hold the PHY in reset on an AECP REBOOT only after every frame given to the MAC has reached its PHY: KL_reboot_ctrl stops the MAC port and counts frames out on MilanMAC's new phy.sink frame-end toggle within a bound derived from the MAC's FIFO depths, graded at a MAC model's wire side in pp_shadow RB and by 33 reboot_ctrl mutants (#787) |
| `3aa23245` | Say in the REBOOT reset design and the suite documents how the egress wait keeps ENTITY_DEPARTING on the wire, what bounds it, and the 13,505 ms restated from the request to the IPROG word on the AX7101 (#787) |
| `ce30f6b4` | Leave the MAC port ungated through the REBOOT's egress wait, as the gPTP plane's direct path to the MAC requires: end the wait only after a millisecond quiet on every clock, count frames on the RMON tap's own beat terms, and grade that the PHY hold follows the request (#787) |
| `e12147d4` | Say in the REBOOT reset design and the suite documents why the egress wait leaves the MAC port open and how its quiet millisecond holds, with the 30 unit controls and six datapath arms that grade it (#787) |
| `52e3fb64` | Read the datapath source list in pp_shadow's REBOOT mutant driver as its Makefile does, with MAKEFLAGS cleared and no directory lines, so an outer make -C no longer splices those lines into the sources it plants (#787) |
| `faa25c3f` | Keep the CHANGELOG's REBOOT entry and the #787 adoption record in SUBMODULES to the concise-documentation gate's ten-word sentences, the re-pin's four included (#787) |
| `667b9bbc` | Re-pin the processor at processor PR #209's merge commit a9e84b66, whose tree is the reviewed head 013ee63f's, and re-record its ROM ledger rows, boundary diagram and pin table through their generators (#787) |

`15796754` gated the MAC port (a "stop") during the egress wait. The builder bank's gate 1b at `3aa23245` refused it:
the baremetal profile contract pins `assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;` and a reference census of
the MAC handshake ports, so that no runtime gate can sit between the MAC-boundary arbiter and the MAC and silence the
gPTP plane (#187). Relaxing that contract is outside #787, so `ce30f6b4` removes the stop rather than the check.
Nothing the defect needs depended on it (below). The gates were stopped at `3aa23245` and rerun at `e12147d4`.

Three findings of this round's own gates followed, each fixed in its own commit:

- `52e3fb64`: the campaigns bank found that `make -C tb/verilator/pp_shadow reboot-mutant` built nothing. Under an
  outer `make -C`, the driver's `make -s -C ../milan_dp print-srcs` inherited the print-directory flag, and its
  "Entering directory" lines were spliced into the source list (receipt `receipts/campaigns-e12147d4/`). Round 1's
  driver had the same line. The listing now runs as the Makefile's does.
- `faa25c3f`: the docs workflow's concise-documentation gate refused ten sentences over ten words in CHANGELOG.md and
  SUBMODULES.md, four of them from the re-pin commit `0d4be94c` (receipt `receipts/docs-e12147d4-first-run/`).
- `667b9bbc`: processor PR #209 merged during the round, so the pin moved to its merge commit (above).

**Why the long banks at `e12147d4` stand for `667b9bbc`.** `git diff --stat e12147d4 667b9bbc` touches only:

- the mutant driver;
- CHANGELOG.md, SUBMODULES.md and AREA_BUDGET.md;
- the boundary diagram, its PNG manifest and the ROM ledger rows;
- the `protocol-processor` gitlink, to a commit with the identical tree `b0f66acb`.

No RTL, suite source or synthesis input changes in content. The sweep, rtl-fast and Yosys therefore stand. The
static and pin-record bank, the docs workflow and the campaigns bank were rerun at `667b9bbc`.

## The defect, confirmed by test

[A10]'s cause is confirmed. `KL_reboot_ctrl` at `0d4be94c` leaves `S_DRAIN` at once on a clean saved state and raises
`hold_r` (`phy_hold_o`) in the same clock: the PHY hold rose two clocks after `reboot_req_o`. The processor at
`013ee63` raises `reboot_req_o` one clock after its arbiter goes idle following the last DEPARTING byte at its own
1 B/clk transmit face (`protocol_processor_top.sv` `rbt_sequence`, RB_DEP -> RB_REQ). At that moment the frame is still
in the parent's egress path: the `KL_pp_shadow` packer's last beat, then the SoC's `mac_tx_cdc` (17 beats), `tx_sf`
(store and forward, 513 beats, 8 frame slots), LiteEth's own 32-beat transmit crossing and pipeline, and the PHY stage.
The datapath stages between the processor and the MAC port (`ctl_tx_mux`, the IFG gasket, `gptp_ctl_mux`,
`adp_tx_mux`) are combinational pass-throughs, so every frame in flight is in the SoC's MAC.

Receipt `receipts/confirm-0d4be94c/`: the new `[RB]` wire-side checks, built against the unfixed RTL at `0d4be94c`,
fail 10 of 69. (That harness is `15796754`'s, without its two references to RTL the unfixed head lacks.) The
advertising REBOOT's ENTITY_DEPARTING never leaves the MAC model: 5 frames are lost in the MAC at the PHY reset. The
hold rises 2 clocks after the request, and without advertising the notification, the last frame, is lost. That is
the pattern silicon showed: SUCCESS and the notification out, then nothing. The committed `[RB]` at `0d4be94c` passed
38 of 38 because it graded the datapath's port only.

## Signal used, and the STOP checks

- **The egress-idle observation is built at the MAC boundary from two existing seams, all in parent code.** The
  datapath counts frames it hands the MAC on its own `m_axis_mac_tx` handshake, on the RMON tap's terms
  (`tx_mac_beat_w`, `tx_mac_good_w`). The MAC counts them out: `MilanMAC` flips a new reset-less toggle `ethtxend_tgl`
  on `self.phy.sink.valid & ready & last`, the last octet of each frame at LiteEth's `phy.sink`. That is the stream the
  PHY's transmit register stage consumes, one register stage before the GMII/MII pads, and the seam
  `KL_gptp_gmii_launch` already observes. It reaches the datapath as `i_ethtxend_tgl` and is synchronised in
  `KL_reboot_ctrl` with three flops and an edge detect, like the link guard's three toggles (CONTRIBUTING: toggle +
  sync is a blessed CDC pattern). LiteEth and LiteX are used as pinned; no submodule changes. **The STOP (egress-idle
  signal absent at the MAC boundary, or needing a change inside a submodule) is not met.**
- **The re-pin round's STOP** (the re-pin changing the parent wiring beyond what the new semantics need): not met.
  `0d4be94c` and `667b9bbc` are gitlink plus generated records; `667b9bbc` moves to a commit with the same tree. The
  wiring this round adds is the defect's fix: one input, two parameters and one instance's connections, all
  requested by [A10]'s later comment. The MAC handshake assignments are unchanged.

## A700b's uncommitted edits: kept and discarded

Saved before discarding: `receipts/a700b/uncommitted.diff` (20,961 bytes, sha256
`a38b8d8b4a48b7654cea100a0e4e660d9c258f7ed7ec93d7968ad09b1ab15aa2`).

- **Discarded: the RTL** (`hdl/milan/KL_reboot_ctrl.sv`). It added `T_EGRESS_MS_P = 10`, a fixed minimum wait
  from the request to the hold. It observes nothing at the MAC, so it does not meet requirement 1. Its value is a
  figure worked out by hand in a comment, a mirrored number, which [A10] forbids.
- **Discarded: its mutants and harness scenarios built on that timer** (`egress-wait-*`, `grade_egress`, U12).
- **Kept, re-derived: the bound-grading idea.** Its `grade_bound` helper grades the request to the IPROG word against
  the stated bound. It survives in the new harness as `grade_bound`, with the restated bounds (U2, U11, U14 durable,
  U17 worst case). Also kept: U7 waits for the hold rather than assuming its clock.
- **Kept as a finding:** A700b's F1 (the hold cuts frames in the SoC's MAC) is the defect [A10] reported.

## Changes (file:line at head, clause)

| # | File:line | Change | Clause / item |
|---|---|---|---|
| 1 | `hdl/milan/KL_reboot_ctrl.sv:158` (`S_EGRESS`), `:288` (the phase), `:297` (the quiet ms cleared on any busy clock), `:246` (`egress_account`), `:240` (`idle_w`) | a fourth phase between DRAIN and HOLD. It ends on a tick once no frame is half taken at the port and none is in the MAC, and the path has stayed so on every clock since the previous tick (a whole quiet millisecond, for the PHY's own transmit path), or at its bound | [A10] 1; Milan v1.2 5.6.3.3, 5.6.3.5.8, 5.6.3.5.11, Table 5.51; IEEE 1722.1-2021 6.2.4.1.3, 6.2.5.2.2 |
| 2 | `hdl/milan/KL_reboot_ctrl.sv:120` (`MAC_TX_OCTETS_P`, `MAC_MIN_MBPS_P`), `:174` (`T_EGRESS_MS_C`), `:177` (`FLY_MAX_C`), `:192` (refusal below one maximum frame) | the bound derived from the MAC's statement: ceil(octets x 8 / (Mbps x 1,000)) ms plus the quiet ms; the count saturates at the most frames that statement allows | [A10] 1 (named, derived, not mirrored); IEEE 802.3-2022 3.2.1, 3.2.2, Table 4-2 |
| 3 | `hdl/milan/KL_reboot_ctrl.sv` banner | THE BOUND restated: `T_DRAIN + T_EGRESS + T_HOLD + 3 ms + 8 clocks`; 13,505 ms on the AX7101, 13,514 ms on the Arty, 13,531 ms at the default; why the port is not gated | [A10] 1 (restate the 13,502 ms) |
| 4 | `hdl/milan/milan_datapath.sv:373` (`REBOOT_MAC_TX_OCTETS_P`, `REBOOT_MAC_MIN_MBPS_P`), `:598` (`i_ethtxend_tgl`), `:9073` (`tx_mac_beat_w`, the RMON tap split, no new port reference), `:9747` (the instance; `mac_flush_i` = the guard's `reinit & eth_rst` at `:9763`) | the MAC's statement as parameters, the frame-end toggle as a port, the account on the existing tap | the boundary; [A10] 1 |
| 5 | `sw/litex/milan_soc.py:1414` (named depths `_MAC_TX_SF_*`, `_MAC_CORE_TX_*`, framing octets, `_MAC_DATA_WIDTH`, `_BOARD_PHY_MODEL`, `_PHY_MODEL_MIN_MBPS`), `:1439` (`_mac_tx_egress_octets`), `:1760` (`ethtxend_tgl`), `:1795`/`:1813` (the constructions read the names), `:2162` (dp_ports: the toggle and the two parameters), `:883` (the no-MAC stub ties it 0), `:3187` | the toggle and the derived statement: 11,656 octets; 1,000 Mb/s for GMII, 10 for MII | [A10] 1 (derived from the FIFOs as built) |
| 6 | `sw/builder/endstation_builder.py:4952`, `:4966` (`reboot_mac_statement`), `:5056` | the builder states the same two parameters by evaluating the SoC's own definitions (AST whitelist, empty builtins), for gate 23m and the publication census | gate 23m |
| 7 | `sw/builder/test_builder.py:18150`, `:18204` (gate 1f), `:18237` (its nine cuts), `:18294` (gate 1d: `phy.sink` read by the launch observer and the toggle only) | new builder gate and its controls; gate 1d widened by exactly the toggle's three reads | builder bank |
| 8 | `scripts/check_py_idiom.py:187` | the builder's guarded evaluation recorded in `DYNAMIC_EXEC_INVENTORY` with its guard | Rule 12 |
| 9 | `scripts/check_solution_docs.py:181`; the generated row in `docs/integration/INTEGRATION_GUIDE.md` and `docs/guides/SYSTEM_INTEGRATOR.md` | the End-station reset port group gains `i_ethtxend_tgl` (tie 0: the wait runs to its bound) | integration contract |
| 10 | `tb/verilator/gptp_txts/generated/manifest.json` | the MilanMAC region hash, regenerated by `sw/litex/gen_mac_tx_model.py`; the converted Verilog is byte-identical | generator rule |
| 11 | `tb/verilator/pp_shadow/sim_main.cpp:348` (`MacModel`), `:378` (`mac_step`), `:4246`, `:4309`, `:4393`, `:4483`, `:4521`; `reboot_mutant.py` | the wire-side check, three REBOOTs, six arms | [A10] 2, 3; re-pin round 2 (early request; the reset follows only a raised request) |
| 12 | `tb/verilator/reboot_ctrl/sim_main.cpp` (U0 to U18; `:458`, `:573`, `:585`), `Makefile` (two legs), `mutants.py` (30) | the unit grading of the egress account and every bound | [A10] 3 |
| 13 | `docs/design/REBOOT_RESET.md` (sections 1, 3 with "The egress wait", the contract, 6, 7), `docs/litex/CLOCK_DOMAINS.md` (the crossing), `docs/fpga/FPGA_DESIGN.md`, `docs/reference/SUBMODULES.md`, `docs/testing/TESTING.md`, `CHANGELOG.md`, the three tb READMEs | the documents | docs |
| 14 | `protocol-processor` gitlink `013ee63f` -> `a9e84b66` (identical tree); `syn/yosys/rom_digests.tsv` (two rows, digests equal to `013ee63f`'s); `docs/diagrams/submodule_boundaries.{svg,drawio,png}`, `PNG_MANIFEST.json`; `docs/reference/SUBMODULES.md:25` and the adoption record; `CHANGELOG.md`; `docs/design/AREA_BUDGET.md` | the re-pin to the merge commit, its records through `ooc.sh --record-rom-digests` and `submodule_boundaries.gen.py` | re-pin round 1 |

**Why the port is not gated, and what that leaves.** Every frame the REBOOT owes the network was handed to the MAC
before the request: the response, the notifications and ENTITY_DEPARTING. The account therefore holds each from the
moment the request rose and waits for it. The DEPARTING's last beat may still be in the packer then; the frame is
half taken, so `in_frame` covers it. Frames other sources start later (a stream PDU, a MAAP probe, a gPTP message)
are counted and waited for while the path still empties. One that enters the port on the clock the wait ends is lost
with the PHY reset and the reload, as at a cut. Traffic that never leaves a quiet millisecond ends the wait at its
bound, after the derived drain time of the whole MAC.

## New checks, planted mutants and failing words

### `tb/verilator/pp_shadow` section `[RB]`, at the MAC model's wire-side output

The model stands for `MilanMAC`'s transmit side behind the datapath's port. A frame may leave 8 clocks after its last
beat entered (store and forward), and frames leave in order with preamble, padding, FCS and gap, at 4 clocks per octet
in `[RB]`. The model flips `i_ethtxend_tgl` on each last octet and keeps it across resets. 3 clocks after
`o_reboot_phy_hold` rises the PHY is in reset: a frame on the wire is cut and every queued frame is lost; a frame
offered later is counted apart. `--reboot-only`: 68 checks.

| Scenario | Graded |
|---|---|
| advertising, a second controller registered, KL_maap probing | at the port: the request after the response and after DEPARTING. The hold after the request. On the wire: the SUCCESS response, the notification to the other controller and ENTITY_DEPARTING whole and in that order before the PHY hold; no frame cut, none left in the MAC; the hold more than 1 ms and at most 2 ticks + 8 clocks after the last frame, inside the 28 ms egress bound. Then the IPROG words, their retry, the hold held |
| not advertising | no DEPARTING at the port or on the wire; response and notification whole and in order before the hold; the hold after the last frame the port started |
| dead transmit clock | nothing on the wire; the hold still rises, 2,827 clocks after the request, inside (2,800, 2,904] |

`make -C tb/verilator/pp_shadow reboot-mutant`: six arms, each in a private copy, 6 of 6 caught at `52e3fb64` and at the head:

| Arm | Plant | Named failing check | Failing checks |
|---|---|---|---:|
| `request-ignored` | `.reboot_req_i (pp_reboot_req_w & 1'b0)` | `RB advertising: the PHY hold rises` | 21 |
| `early-request` (re-pin round 2: the reset follows only a raised request) | `.reboot_req_i (pp_reboot_req_w \| (pp_shadow.u_pp.rbt_st_r != 3'd0))`: the request at the processor's acceptance | `RB advertising: the PHY hold follows the processor's REBOOT request` | 5 |
| `hold-on-the-request-alone` ([A10] 3a, today's behaviour) | DRAIN -> HOLD with `hold_r` | `RB advertising: ENTITY_DEPARTING leaves after the notification, before the PHY hold` | 8 |
| `egress-ignores-the-mac-fifo` ([A10] 3b) | `idle_w` without the MAC count | the same | 8 |
| `egress-without-a-bound` ([A10] 3c) | the egress deadline never fires | `RB dead transmit clock: the PHY hold still rises` | 3 |
| `txend-unwired` | `.mac_txend_tgl_i (i_ethtxend_tgl & 1'b0)` | `RB advertising: ...and at most two ticks and eight clocks after it` | 2 |

### `tb/verilator/reboot_ctrl`

There are two legs. The module default (32,768 octets at 10 Mb/s, egress bound 28 ms) runs every scenario, 221 checks.
A 1 Gb/s statement (11,656 octets at 1,000 Mb/s, 2 ms) runs U14 and U17, 46 checks. Each leg's bound is an
independent literal in the Makefile. Measured: U17's worst case is 108,255 clocks against the stated 108,256; U14 at
the default 228 clocks in (224, 232]; U18 15 clocks in (8, 21]. `mutants.py`: golden PASS, 30 of 30 killed (counts from
the run at the head's sources; the campaigns bank repeats it):

| Mutant | Named failing check | Failing checks |
|---|---|---:|
| `request-ignored` | U1 no writer, nothing in the MAC: from the request the PHY hold rises more than one tick later | 165 |
| `drain-ignores-dirty` | U3 dirty work with a live writer: no PHY hold and no IPROG for 4,000 ms | 6 |
| `drain-ignores-pend` | U4 pending work with a live writer: no PHY hold for 1,500 ms | 3 |
| `drain-ignores-a-lost-writer` | U6 the writer is lost: from that clock ...and at most two ticks and the crossing later | 28 |
| `no-drain-deadline` | U5 ...and at most one tick more | 37 |
| `drain-deadline-a-tick-early` | U5 a writer that never commits: the PHY hold more than 10,000 ms and two ticks after the request | 1 |
| `hold-skipped` | U1 the hold is longer than 3,500 ms | 7 |
| `hold-a-tick-short` | U1 the hold is longer than 3,500 ms | 7 |
| `hold-a-tick-long` | U1 the hold is at most one tick longer than 3,500 ms | 10 |
| `bits-not-reversed` | U1 eight consecutive clocks carry dummy, sync, NOOP, WBSTAR, 0, CMD, IPROG, NOOP, bits reversed per byte | 12 |
| `wbstar-write-dropped` | the same | 12 |
| `desync-for-iprog` | the same | 11 |
| `words-repeat-without-a-hold` | U1 CSIB is high again after the eighth word | 12 |
| `phy-hold-released-for-iprog` | U1 the PHY hold stays up through the IPROG words | 100 |
| `request-not-latched` | U7 a one-clock request: the PHY hold still rises | 12 |
| `hold-survives-reset` | U9 a reset during the hold: back to idle, and no IPROG afterwards | 42 |
| `hold-on-the-request-alone` ([A10] 3a) | U12 frames in the MAC at the request: no PHY hold 20 ms later with three frames still in the MAC | 25 |
| `egress-ignores-the-mac-fifo` ([A10] 3b) | the same | 15 |
| `egress-without-a-bound` ([A10] 3c) | U14 a MAC that never finishes: the PHY hold still rises | 39 |
| `egress-bound-a-tick-short` | U14 ...after more than the derived egress bound | 2 |
| `egress-bound-a-tick-long` | U14 ...and at most one tick more | 4 |
| `egress-bound-rounded-down` | U14 ...after more than the derived egress bound | 2 |
| `egress-without-the-quiet-tick` | U12 the last frame reaches the PHY: from its end the PHY hold rises more than one tick later | 13 |
| `egress-ignores-the-frame-at-the-port` | U13 a frame still being taken 3 ms into the wait: no PHY hold | 3 |
| `frames-taken-not-counted` | U12 frames in the MAC at the request: no PHY hold 20 ms later with three frames still in the MAC | 15 |
| `end-read-as-a-level` | U12 two frames still in the MAC: no PHY hold | 9 |
| `end-wins-over-a-take` | U12 coincide: the second frame is still in the MAC: no PHY hold | 2 |
| `count-wraps-below-zero` | U16 it reaches the PHY: from its end ...and at most two ticks and the crossing later | 8 |
| `flush-ignored` | U15 a flush in the wait: from the flush ...and at most two ticks and the crossing later | 1 |
| `egress-quiet-sampled-only-at-ticks` | U18 ...no PHY hold at the next tick | 2 |

### Builder gate 1f (`sw/builder/test_builder.py`)

Gate 1f holds `tx_sf` to `_MAC_TX_SF_PAYLOAD_DEPTH`/`_PARAM_DEPTH` and the core's crossing to
`_MAC_CORE_TX_CDC_DEPTH`. It holds the two parameters to `_mac_tx_egress_octets(nb, crossed)` and
`_PHY_MODEL_MIN_MBPS[phy_model]`, and `i_i_ethtxend_tgl` to the toggle. The toggle must be one reset-less `Signal`
flipped in `eth_tx` on `phy.sink`'s valid, ready and last, the no-MAC stub must tie it to zero, and the AX7101
statement must be 11,656 octets at 1,000 Mb/s. `test_reboot_egress_statement_gate_bites` plants nine cuts, each
rejected by the finding that names it:

- the payload depth and the frame slots as literals;
- the core crossing left at its default;
- the octets mirrored as 11656, and the rate as 1000;
- the toggle unwired, reset, or on the receive stream;
- the stub's tie removed.

Gate 23m (the SoC's Instance binds exactly `eb.datapath_params()`) covers the two new parameters on all five
configs. Gate 1b (the baremetal profile contract: the MAC handshake direct and its reference census) passes
unchanged at the head.

## Resources

No Vivado this round (both assignments): no route, no resource gate, no timing. The route is redone after #814 merges,
against the record #814 re-records. The change's cost is measured with Yosys:

| `KL_reboot_ctrl` | Gate cells (portability gate) | `synth_xilinx` LUTs | FFs | CARRY4 | MUXF7 / MUXF8 |
|---|---:|---:|---:|---:|---:|
| `0d4be94c` (before) | 140 | 41 | 22 | 5 | 0 / 0 |
| head, the AX7101 statement (11,656 octets, 1,000 Mb/s) | - | 82 | 36 | 7 | 8 / 2 |
| head, the default statement (32,768 octets, 10 Mb/s) | 245 | 85 | 37 | 8 | 1 / 0 |

So the shipping build gains about 41 LUTs and 14 FFs: the 8-bit account, the 3-flop synchroniser, the quiet bit, one
more state and the derived deadline compare. In the SoC, one reset-less flop in `eth_tx` and its LUT. Round 1's route
left 57 of 15,850 slices free, and the route after #814 measures what this adds
(`receipts/yosys-synth-xilinx-KL_reboot_ctrl/`).

## Gates

Every rc is the command's own exit status, run in a clean clone at the stated head (`scripts/make_clone.sh`: the
lane's tree, its submodules from the lane's checkouts, origin/dev the live remote dev tip `1e80128f`).

| Gate | Head | rc | Result | Receipt |
|---|---|---:|---|---|
| Full sweep, `native-shards.py 787-a700c <spec> <out> 4 16-19 20-23 24-27 28-31` (`cpu_ranges.py` free range 16-31, one 4-CPU block per shard; MemAvailable 52 GB at the start) | `e12147d4` | 0 x 4 | shards of 15, 17, 17 and 16 suites, every suite PASS, none timed out (`capture_coherence` included) | `receipts/sweep-e12147d4/shard-*` |
| `scripts/suite_tally.py` over the four log dirs `--expect-suite-root tb/verilator` | `e12147d4` | 0 | **65 suites, each once; 2,192,196 checks, 0 in-suite failures**. `reboot_ctrl` 298 (221 + 46 + 31 mutant controls), `pp_shadow` 2,514 (base 719, vid73 719, crf 759, pending 317) | `receipts/sweep-e12147d4/tally.log`, `shard-0/logs/pp_shadow-RB-excerpt.log` |
| rtl-fast replica (`rtl_fast_steps.py`, every job of the aggregate's `needs:`), behave included | `e12147d4` | 0 | `rtl-fast: success; failed jobs: none`; 12 of 12 jobs; behave 14 features, 508 scenarios, 2,330 steps passed; 6,359 s; base the live dev `1e80128f` | `receipts/rtlfast-e12147d4/` |
| `syn/yosys/run.sh` (full serial; Yosys 0.66, sv2v v0.0.12) | `e12147d4` | 0 | tops 61, pass 61, fail 0 (`KL_reboot_ctrl` 245 cells); tied inputs 30, justified 2, unjustified 0; TAP-PURITY PASS; 1,546 s | `receipts/yosys-e12147d4/` |
| Static and pin-record bank (`static_bank.sh`: 32 gates one at a time; xvlog not run) | `667b9bbc` | 0 x 32 | check-baseline PASS; ROM ledger re-recorded byte-identical (`git diff --exit-code`); both diagram checks; submodule docs (exact gitlinks); gPTP docs with and without the submodule; port contracts; naming; test evidence; integrator params; RTL lint and its self-test; the four idiom gates and two self-tests; RTL source lists and self-test; `pp_srcs.py`; **the builder bank: ALL GATES PASS EXCEPT 2 NOT RUN** (gate 1b's `MAKEFLAGS += -e` arm has nothing to observe on this make; gate 11 needs an Arty build tree not on disk), gates 1b, 1d, 1f and 23m among the passes; hygiene; fail-fast; TODO ownership; module matrix; SoC sources; NVM capture; feature status; docs_check. xvlog not run: a Vivado tool, and no Vivado this round | `receipts/static-667b9bbc/` |
| The same bank at the two earlier heads | `e12147d4`, `faa25c3f` | 0 x 32 each | the same 32 gates pass; builder bank ALL GATES PASS EXCEPT 2 NOT RUN (gate 1b's `MAKEFLAGS += -e` arm has nothing to observe on this make; gate 11 needs an Arty build tree not on disk) | `receipts/static-e12147d4/`, `receipts/static-faa25c3f/` |
| Docs workflow (`docs_steps.py`, GNU Make 4.3, CPython 3.12.3), builder leg 1 with the LiteX interpreter, the five markdown gates on CPython 3.12.3, the no-git step | `667b9bbc` | 0 | 44 steps, 0 failed: 42 run, all rc 0, and 2 skipped by rule (the act runner contract gate, and the no-git job's own step, run separately: docs_check 0, feature_status 0); gate 9 (concise documentation) and gate 12 (verified submodule documentation) pass; leg 1 with LiteX 0 failed; markdown gates 5 of 5 | `receipts/docs-667b9bbc/` |
| The same docs bank at `faa25c3f` | `faa25c3f` | 0 | 44 steps, 0 failed (42 run, 2 skipped by rule); leg 1 0 failed; markdown 5 of 5; no-git docs_check 0, feature_status 0 | `receipts/docs-faa25c3f/` |
| The same docs bank at `e12147d4` (the first run) | `e12147d4` | 1 | one finding, gate 9 (concise documentation): ten sentences over ten words in CHANGELOG.md and SUBMODULES.md, fixed in `faa25c3f` | `receipts/docs-e12147d4-first-run/` |
| Campaigns bank (`campaigns_run.sh`) | `667b9bbc` | 0 x 15 | `reboot_ctrl` 221 + 46 checks, 30 of 30 killed; `[RB]` 68 checks; `reboot-mutant` 6 of 6 (21, 5, 8, 8, 3, 2 failing checks); planner 123 tests OK; behave 189 scenarios; UART smoke 13 negative and 4 reboot arms; LiteX sims 7 of 7 (`test_retained_cdc_storage` builds `MilanMAC`); `gen_mac_tx_model.py --check` OK at both levels; py idiom and its self-test, hygiene, test evidence, TODO ownership, docs_check | `receipts/campaigns-667b9bbc/` |
| The same bank at `52e3fb64` | `52e3fb64` | 0 x 15 | `reboot_ctrl` 221 + 46, 30 of 30 killed; `[RB]` 68; `reboot-mutant` 6 of 6; planner 123 tests OK; behave 189 scenarios, 708 steps; UART smoke 13 negative and 4 reboot arms; LiteX sims 7 of 7; `gen_mac_tx_model.py --check` OK at both levels; py idiom and its self-test, hygiene, test evidence, TODO ownership, docs_check | `receipts/campaigns-52e3fb64/` |
| The same bank at `e12147d4` | `e12147d4` | 2 (reboot-mutant) | `reboot-mutant` built nothing under `make -C` (the listing defect fixed in `52e3fb64`); everything else rc 0 | `receipts/campaigns-e12147d4/` |
| Builder subset on the reworked tree: `test_builder.py --gates test_baremetal_profile_contract,test_gptp_launch_observer_seam,test_reboot_egress_statement,test_reboot_egress_statement_gate_bites,test_datapath_params_match_the_instance,test_datapath_params_gate_bites` | the tree of `ce30f6b4` before commit | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 1b's `MAKEFLAGS += -e` arm) | run in the lane; the full builder bank at each head is in the static bank above |
| Confirmation of the cause: `[RB]`'s wire-side checks on the unfixed RTL | `0d4be94c` | 1 (expected) | 69 checks, 10 failures: DEPARTING lost in the MAC; the committed `[RB]` there passed 38 of 38 | `receipts/confirm-0d4be94c/` |


## Receipts

Everything cited is under `receipts/`. `INDEX.md` at the top of the output directory lists every file present, with
bytes and SHA-256, generated by `scripts/gen_index.py` from the files themselves. Host paths are replaced by
placeholders (`scripts/collect.py`): `<scratch>`, `<lane>`, `<lanes>`, `<tools>`, `<home>` and `<tmp>`. A file over
200 KB is not copied; its size and full SHA-256 are in a `RAW-RECORDS.txt` beside the copies. The large ones are five
sweep logs, among them `pp_shadow.log`, whose `[RB]` lines are excerpted beside it.

| Directory | Holds |
|---|---|
| `confirm-0d4be94c/` | the wire-side `[RB]` on the unfixed RTL (the cause confirmed), the harness diff applied, the committed `[RB]` there |
| `a700b/` | A700b's uncommitted edits as they were |
| `sweep-e12147d4/` | each shard's spec, verdict and suite logs; the tally; the `[RB]` excerpt |
| `rtlfast-e12147d4/` | the replica's step table, summary and every step log |
| `yosys-e12147d4/`, `yosys-synth-xilinx-KL_reboot_ctrl/` | the full Yosys gate's log, rc, versions and per-top results; the `synth_xilinx` statistics before and after |
| `static-667b9bbc/`, `static-faa25c3f/`, `static-e12147d4/` | the 32 static and pin-record gate logs and their tables |
| `docs-667b9bbc/`, `docs-faa25c3f/`, `docs-e12147d4-first-run/` | the docs workflow banks |
| `campaigns-667b9bbc/`, `campaigns-52e3fb64/`, `campaigns-e12147d4/` | the mutant drivers and self-tests; the `make -C` listing defect's evidence |

`scripts/` holds the drivers this lane ran: round 1's `make_clone.sh`, `static_bank.sh` (xvlog left out this round),
`yosys_run.sh`, `rtlfast_run.sh` with `rtl_fast_steps.py`, `docs_run.sh` with `docs_steps.py` and
`docs_steps_md312.py`, `env.sh`, `fw_env.sh`, `make_sweep_spec.py`, `collect.py` and `gen_index.py`, with the paths
changed; and this round's `campaigns_run.sh` and `collect_bank.sh`.

## Not done (by the assignment's rules)

No push, no PR, no merge or rebase, and no edits to any issue or PR comment. On #787 the only posts are TAKEN and
REVIEW READY (or STOP). No hardware or bench access and no flashing. No sub-agents. No Vivado tool: the route and the
xvlog ratchet wait for the post-#814 round.
