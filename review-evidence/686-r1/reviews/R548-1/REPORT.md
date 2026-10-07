[R548] NEGATIVE - exact head c7b69cd0fb2bdf980546ab413b3b82198267cbd8

# R548-1 internal cleared-context review: issue #686 / PR #695

- Head: `c7b69cd0fb2bdf980546ab413b3b82198267cbd8`, tree `f391905e7afd3485edc9d21ab317dd0802959c45`.
- Source base: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.
- Scope: the assignment in issue comment 6043036997 and the TAKEN decisions in comment 6043296747.
- Authority: IEEE 1722-2016 Annex B. I read it from the standard's text and cite it by clause only. I read B.2.1 to B.2.8, B.3.1 to B.3.6.7 (Tables B.3 to B.8) and B.4 (Tables B.9 and B.10).

The verdict is NEGATIVE.

My independent pass found two MINOR findings. At that point I judged the RTL conformant on all four #686 items.
- **F1.** The harness does not test the in-flight-frame guard on the DEFEND path. Removing the guard passes all 120 checks and all 22 mutants. It also puts a malformed ANNOUNCE on the wire.
- **F2.** The new deviation list in `MAAP_FABRIC.md` misreads Table B.7 when it explains the "PROBE not defended while a frame is on the wire" deviation.

I wrote the verdict and ledger before reading any other review (`receipts/independence.log`). Afterwards I read the parallel external round R549-1 on the same head and reproduced three of its claims with my own probe (`receipts/crosscheck.log`). I adopt them as F3 to F5 below. One of them is an RTL defect in item 2's timer randomization (F3), so the RTL lens is UNCLEAN as well. Every entry changed after that reading is marked † in the [Ledger](#ledger).

## Contents

- [Findings](#findings): five MINOR findings, three of them adopted after the parallel cross-check, and four SUGGESTION items. No RESIDUE remains.
- [Item-by-item conformance](#item-by-item-conformance): each #686 item checked cell by cell against its clause.
- [Executed evidence](#executed-evidence): what I ran at this head and the results.
- [Lens results](#lens-results): one line per lens, with its artifacts.
- [Ledger](#ledger): the reviewer-owned completion ledger.
- [Prior and parallel public findings](#prior-and-parallel-public-findings): their state at this head.
- [Limits and pending manager duties](#limits-and-pending-manager-duties)
- [Receipts](#receipts)

## Findings

### F1 - MINOR - Tests, Robustness

**Where:**
- `hdl/ieee1722/maap/KL_maap.sv:262-264`: the `!tx_busy_r` term of `defend_w`.
- `tb/verilator/maap/sim_main.cpp:335-346`: section [4c], which injects only a non-conflicting PDU during the stall.
- `tb/verilator/maap/mutants.py`: no row for this guard.

**The documented contract.**
- `docs/design/MAAP_FABRIC.md:102` gives the rProbe!/ANNOUNCE cell as "sDefend, unless a frame is already on the wire".
- `docs/design/MAAP_FABRIC.md:62-63` and `KL_maap.sv:213-215` say that a Restart! or the next RX PDU cannot rewrite a frame on the wire.
- `MAAP_FABRIC.md:172-174` says the harness checks "every conflict cell above".

**Why this is a finding.**
- The only thing that keeps the sDefend path from rewriting `tx_msg_r`, `tx_dst_r`, `tx_off_r` and the conflict registers mid-frame is the `!tx_busy_r` term. Nothing grades it.
- I planted the defect: I removed `&& !tx_busy_r` (`receipts/r548_probes.log`, `defend_while_busy`). The harness still reports `KL_maap: 120 checks, 0 failures`.
- A directed probe (`scripts/r548_inflight.cpp`) held an ANNOUNCE under backpressure after two beats and then injected a conflicting PROBE.
  - At this head, the ANNOUNCE leaves intact and no DEFEND is sent (`receipts/inflight_head.log`, rc 0).
  - With the guard removed, the frame that leaves is typed ANNOUNCE but has `91:E0:F0:00:CE:09 / 0x0008` in conflict_start_address and conflict_count, bytes 34 to 41 (`receipts/inflight_mut.log`, rc 1).
  - B.3.6.7 sets both fields to zero in an ANNOUNCE (B.2.7, B.2.8).

**Impact.** A regression that corrupts frames on the wire under backpressure would pass the suite and its campaign. The PR's claim that the frame on the wire is protected is verified for Restart! but not for the RX/DEFEND path.

**Required outcome.**
- Add a named check: a conflicting PROBE parsed while a frame is on the wire must leave that frame byte-identical and must not produce a DEFEND. The stall starts mid-frame under backpressure.
- Add a `mutants.py` row that removes the guard and must fail that check.
- The RTL needs no change.

**Verification.** Re-run `make -C tb/verilator/maap`. The new row must be caught. My probe `defend_while_busy` must be killed when re-run with `scripts/r548_probes.py <repo> <workdir>`.

### F2 - MINOR - Docs, Conformance

**Where:** `docs/design/MAAP_FABRIC.md:125-126`. It says: "A PROBE parsed while any frame is on the wire is not defended. The prober repeats its PROBE within 600 ms."

**Why this is a finding.**
- Under Table B.7, probetimer! sends a PROBE and then runs dec_maap_probe_count (B.3.6.3).
- When the count reaches zero, probeCount! runs sAnnounce and moves to DEFEND. It does not send another PROBE.
- So a prober's fourth PROBE (the ReserveAddress! PROBE plus MAAP_PROBE_RETRANSMITS, Table B.8) is never repeated.
- If that PROBE goes undefended, the prober's ANNOUNCE follows at once. This station then resolves the overlap through the rAnnounce!/DEFEND cell with compare_MAC (B.3.6.4, note d). When this station is not the lower, it gives up the range it already held.
- The sentence is new in this PR. It explains a deviation left for a follow-up decision, and it states the consequence as always recoverable by a repeat.

**Impact.** The deviation recorded for the follow-up decision understates its consequence: an established holder can lose its block. The follow-up issue would be decided on an incorrect reading of the standard.

**Required outcome.** State the consequence as Table B.7 gives it:
- PROBEs one to three are repeated within the probe interval.
- A missed fourth PROBE is not repeated. The overlap is then settled by the prober's ANNOUNCE and compare_MAC, which can move this station.

**Verification.** Read the revised text against Table B.7 rows probetimer! and probeCount!, and against B.3.6.3.

### Findings adopted after the parallel cross-check †

I reproduced each of these myself at this head (`scripts/r548_crosscheck.cpp`, `receipts/crosscheck.log`) before adopting it.

#### F3 † - MINOR (the parallel round rates it MAJOR) - Conformance, RTL, Robustness, Tests, Docs

This is the same defect as parallel finding R549-1-F1.

**Where:**
- `hdl/ieee1722/maap/KL_maap.sv:278-279`: the reset seed.
- `:139-140`: the feedback.
- `:161-162`: the timer draws.
- `tb/verilator/maap/sim_main.cpp:47`: the harness tests one station MAC only.
- `docs/design/MAAP_FABRIC.md:85`.

**Why this is a finding.**
- The reset seed is `0xACE1 ^ mac[15:0] ^ mac[31:16]`. It is zero for every station MAC whose two low 16-bit halves XOR to `0xACE1`, which is 1 in 65,536 MACs. For example, `02:00:00:00:AC:E1`.
- A Fibonacci LFSR that starts at zero stays at zero.
- My probe ran 26 announcements on that MAC and saw exactly one ANNOUNCE interval, 304,880 cycles, which is 30,488 ms. An ordinary MAC gave 25 distinct intervals.
- The probe draw is also fixed at 518 ms. Only the tick phase varies it.
- Both values stay inside the B.3.4 open intervals. B.3.4.1 and B.3.4.2 require a *random* T, and the NOTE to B.3.4.1 gives the reason: to avoid synchronized bursts.
- The seed mechanism predates the PR. The timer draws are item 2, which this PR declares conformed.
- `MAAP_FABRIC.md:85` says successive intervals differ, and that is false for this MAC class.

**Impact.** For an affected MAC, timer randomization is absent. The address draw is also frozen, but that part falls under the deferred B.3.6.1 deviation.

**Severity.** I rate this MINOR, because the intervals stay in bounds and the affected class is narrow. The parallel round's stricter MAJOR classification is noted, and the manager settles it.

**Required outcome.**
- The timer draws must stay random for every station MAC: no reachable zero LFSR state.
- Add a check with a zero-seed MAC and a mutant planted against it.
- The strict bounds stay as they are.

**Verification.** Re-run `scripts/r548_crosscheck.cpp`. Both MACs must give more than one distinct ANNOUNCE interval. Then re-run the maap suite and its campaign.

My R1 (the wording at `:85`) is folded into this finding. It is not wording only once the LFSR can freeze.

#### F4 † - MINOR (was my R2, RESIDUE) - Docs

This is the same defect as parallel finding R549-1-F2.

**Where:** `docs/design/MAAP_FABRIC.md:62`, the comment at `KL_maap.sv:213-215`, and the PR body's "Every per-frame field, including the requested offset, is latched at the send".

**Why this is a finding.**
- The type, destination, requested offset and conflict range are latched (`KL_maap.sv:217-220`, `:371-375`, `:380-387`).
- requested_count (byte 33, `count_i`) and the source MAC (`station_mac_i`) are read live (`KL_maap.sv:229`, `:238`).
- I first classified this as wording. The parallel round showed a count change altering a held DEFEND beat, so the sentence states an interface guarantee the RTL does not give.
- Under the owner rule, uncertainty means MINOR.

**Required outcome.** Use this text, or text equivalent to it: "Every per-frame field a protocol event can change (message type, destination, requested offset, conflict range) is latched at the send request; requested_count and the source MAC follow `count_i` and `station_mac_i` and are not protected against reconfiguration during a frame."

**Verification.** Read the corrected text against the builder's inputs at `KL_maap.sv:223-246`.

#### F5 † - MINOR - Docs, Conformance

This is the same defect as parallel finding R549-1-F3.

**Where:** `docs/design/MAAP_FABRIC.md:50-51`, which says "The claimed block always fits inside it" for the 0xFE00 dynamic pool of Table B.9.

**Why this is a finding.**
- At `KL_maap.sv:268`, the provisioning seed is used without a range check.
- My probe used `seed_offset_i` = 0xFEFF with count 8. It reached ANNOUNCE with `addr_valid_o` = 1 and offset 0xFEFF, so the block ends at 0x0FF07. That is beyond the dynamic pool, and it overlaps the Table B.10 MAAP multicast address `91:E0:F0:00:FF:00`.

**Required outcome.** Bound the claim to random draws and state that a supplied seed must be a valid in-pool block. Alternatively, validate the seed, but that needs a public decision.

**Verification.** Read the text against both arms of `new_off_w`.

### S1 - SUGGESTION - Tests - this station's own empty range

`KL_maap.sv:197` adds `(count_i != 8'd0)` so that this station's empty block never conflicts, and `MAAP_FABRIC.md` says "a range of count 0 never conflicts". The harness grades only received ranges of count 0. My probe `own_empty_range_conflicts` removes the term and survives (`receipts/r548_probes.log`). `count_i` = 0 is a degenerate configuration, so this does not block. Either add a `count_i` = 0 check or scope the sentence to received ranges.

### S2 - SUGGESTION - Tests, Robustness - truncated PDUs (pre-existing, outside #686)

Dropping the `rbeat_r >= 3'd5` gate at `KL_maap.sv:340` survives (`truncated_pdu_accepted`). The base harness did not test this either. It is a candidate for the follow-up issue.

### S3 - SUGGESTION - Tests - campaign item labels

`mutants.py` files `restart_rewrites_the_frame_on_the_wire` under item 3 and `overlap_count_to_our_end` (B.2.8) under item 1. Both grade supporting changes, not the item's own clause. The guard that refuses to run unless items 1 to 4 each have a mutant still holds without them, so nothing is masked today. A separate "supporting" label would keep the guard honest.

### S4 - SUGGESTION - Docs - stale code comments the PR body already lists

`hdl/milan/milan_datapath.sv:267` still quotes `KL_maap` at "621 LUT / 268 FF measured". Yosys now gives 474 / 278, and gave 637 / 268 at base. `:280` still describes a "3-probe / 500 ms" walk. Refresh both at the next touch.

## Item-by-item conformance

| # | Clause / cell | RTL at this head | Result |
|---|---|---|---|
| 1 | B.2.1 control_data_length 16 in all MAAP frames | `CDL_C` = 16, `:114`, byte 17 at `:234`; byte 16 = maap_version 1 << 3, cdl[10:8] = 0 | conforms. Golden frames and the cdl checks pass, and mutant `cdl_28` is caught |
| 1 | B.2.1 PROBE/ANNOUNCE DA = Table B.10 address | `:227-228` | conforms (`every_frame_to_the_prober` is caught) |
| 1 | B.2.1 DEFEND DA = source MAC of the triggering PROBE | `rx_src_r` from bytes 6 to 11 (`:320-324`), latched into `tx_dst_r` when the DEFEND is requested (`:372`) | conforms. The DA holds under backpressure and against a later PDU (`defend_destination_not_latched` is caught; probe `src_mac_lanes_swapped` is killed) |
| 1 | B.2.1 SA = sender, B.2.4 stream_id 0, sv/version 0 | `:229`, `:232`, bytes 18 to 25 zero | conforms (golden frames) |
| 2 | B.3.4.2 500 < T < 600 ms (Table B.8 base 500, variation 100) | draw 518 + `lfsr[5:0]`; a load of N expires in (N-1, N] ms plus one cycle | conforms. 456 measured intervals fall in 517.2 to 581.0 ms (`receipts/maap_run.log`) |
| 2 | B.3.4.1 30 < T < 32 s (Table B.8 base 30 s, variation 2 s) | draw 30488 + `lfsr[9:0]` | conforms. 24 intervals fall in 30.531 to 31.501 s; the differential parent interval is in bounds. † Both timer rows fail randomness for the zero-seed MAC class (F3) |
| 3 | Note b: only conflicting PDUs are events | half-open overlap with 17-bit ends; a received count of 0 never conflicts; pool prefix required (`:195-199`) | conforms. The adjacent-above, adjacent-below and empty edges are caught for both PROBE and ANNOUNCE; probe `conflict_ignores_pool` is killed |
| 3 | ANNOUNCE range = requested_* (B.2.5, B.2.6; its conflict_* is zero by B.2.7, B.2.8, B.3.6.7) | beat selected by message type (`:188-190`, `:330-337`) | conforms (`announce_judged_on_conflict_fields` is caught). Judging a DEFEND on conflict_* (the defender's addresses) is unchanged from base and is reasonable; probe `defend_judged_on_requested` is killed |
| 3 | rAnnounce!/PROBE: Stop probe_timer, Restart!, no compare_MAC | `restart_w` term `state_r == PROBE_S` (`:260-261`) | conforms. I read the cell columns from the layout of Table B.7 |
| 3 | rAnnounce!/DEFEND: compare_MAC (note d), else Restart! | `!mac_lower_w`; compare_MAC octet-reversed, TRUE when the station is lower (`:207-210`) | conforms with B.3.6.4. The inverted-direction probe and the unreversed mutant are both caught |
| 4 | ReserveAddress!: init count 3, start probe_timer, sProbe | Begin! and Restart! load `PROBE_SENDS_C` = 4 sends with the timer at 0 (`:355-356`, `:365-366`) | conforms. The first PROBE goes out within 4 cycles at Begin! (151 walks), at Restart! and at the seeded Begin! |
| 4 | probetimer!: sProbe and decrement; probeCount! at zero: sAnnounce, start announce_timer | `:386-396`: after the fourth send, ANNOUNCE with the timer at 0 | conforms. Four PROBEs, then the ANNOUNCE back to back. Probes `five_probes` and `restart_keeps_probe_count` are caught |

**The TAKEN decisions (6043296747).** One predicate serves PROBE, DEFEND and ANNOUNCE (`conflict_w`, `:197`), and the rAnnounce! row is implemented as decided. Both match the RTL and the documentation.

**The deviations left for follow-up.** I checked each against the RTL:
- compare_MAC is absent in the rProbe!/PROBE and rDefend!/DEFEND cells (`restart_w` `:258-259`).
- The DEFEND carries this station's range in requested_* (`:237-238`, `:373`).
- The address comes from a 16-bit LFSR seeded from the MAC (`:137-140`, `:278`).
- There is no PortOperational! input.
- The PROBE is not defended while a frame is on the wire (`:264`). F2 covers how the doc describes it.
- RX parsing is untagged only.

Each deviation sits outside the four items in the assignment. The differential's shared stimulus uses the prober's range equal to this station's, so the requested_* echo deviation does not show there, as `sw/firmware/ctrl/maap/README.md` says.

**The crflic stimulus change (`7b2896568`).**
- Every former assertion is still there. "KL_maap reached ANNOUNCE" moved to phase [A] at t0 + 3.9 s, "the first PROBE_TX is answered TALKER_DEST_MAC_FAIL (3)" is unchanged, and the new check "KL_maap is probing, no block claimed yet" was added.
- The listener now probes while the claim is in flight, as in Run B. The refusal therefore no longer depends on the phase of the processor's 100 ms retry.
- This is a stimulus fix, not a weakened assertion.
- The leg passes 417 checks, and its campaign catches 6 of 6 mutants with the control passing.

**The F2 differential.** The six former #686 deltas are now equalities:
- raw frames equal the core's for PROBE, ANNOUNCE and DEFEND;
- five frames, the first PROBE at once and the ANNOUNCE at once;
- parent intervals in 500..600 ms and 30..32 s.

The controls for the parent bound (581 to 499) and the count (5 to 4) are caught. The result is 12/12, with 16/16 controls caught.

## Executed evidence

All runs used this head. Each scratch copy came from the clone at this head; the base copy differs only in `KL_maap.sv` at `e21c1ca0`. Verilator was the pinned 5.050 build, checked with `--version`. Every Verilator build ran with `-j 4` or less, through `scripts/verilator_j4.sh`, and at most two ran at once.

| Run | Result | Receipt |
|---|---|---|
| `tb/verilator/maap` harness | `KL_maap: 120 checks, 0 failures`, rc 0 | `receipts/maap_run.log` |
| `tb/verilator/maap/mutants.py` | `checks: 23 failures: 0`: the control passes and 22 mutants each fail their named check | `receipts/maap_mutants.log` |
| `make -C tb/verilator/maap coverage` | `KL_maap.sv` line 100.0 % (167/167), gate PASS | `receipts/maap_coverage.log` |
| Reviewer fault probes (14) | 11 killed. Survivors: `defend_while_busy` (F1), `own_empty_range_conflicts` (S1), `truncated_pdu_accepted` (S2, pre-existing) | `receipts/r548_probes.log`, `scripts/r548_probes.py` |
| Directed in-flight probe | head: intact ANNOUNCE and no DEFEND (rc 0); guard removed: corrupted ANNOUNCE (rc 1) | `receipts/inflight_head.log`, `receipts/inflight_mut.log`, `scripts/r548_inflight.cpp` |
| `maap_differential.py --self-test` | 12/12 checks; 16/16 controls caught; rc 0 | `receipts/maap_differential_selftest.summary`, `receipts/maap_differential_selftest.log.gz` |
| `make -C tb/verilator/milan_dp crflic` | leg `checks: 417 failures: 0`, PASS | `receipts/crflic_leg.log` |
| `crflic_mutants.py` | 7 checks: 7 PASS (control, plus 6 mutants caught) | `receipts/crflic_mutants.log` |
| Yosys `syn/yosys/ooc.sh KL_maap` | head 474 LUT / 278 FF / 59 CARRY4; base 637 / 268 / 74; delta -163 / +10, within +40 / +40 | `receipts/yosys_ooc_head.log`, `receipts/yosys_ooc_base.log` |
| Verilator `--lint-only -Wall` on `KL_maap` | head has 2 warnings, both also at base (WIDTHTRUNC `rx_msg_r`, unused `rx_tkeep_i`); base has 3; nothing new | `receipts/verilator_lint_kl_maap.log` |
| `pp_resource_gate.py check-baseline` | `baseline PASS: 3 endpoints` | `receipts/check_baseline.log` |
| Baseline JSON leaf diff, base to head | 57 changed leaves, all under figures, scopes, inputs_sha256 or measured; none outside, so no tolerance, floor, ceiling, identity or policy moved | `receipts/baseline_diff.log`, `scripts/r548_baseline_diff.py` |
| docs_check, check_em_dash (base `e21c1ca0`), gen_toc `--check`, gen_module_matrix `--check`, measure_test_evidence `--check`, lint_rtl `--check` | all rc 0 (lint 90 <= 90) | `receipts/gate_*.log`, `receipts/gates.rc` |
| Clone integrity after the probes | HEAD and tree exact; index equals the HEAD tree (modes, blobs, paths); `KL_maap.sv` blob exact; gitlinks `5dce647a` / `ead80360` / `48ff7a7e`; status empty, including ignored files | `receipts/clone_integrity.log` |
| Tool identity | Verilator 5.050 rev v5.050, Yosys 0.66, sv2v v0.0.13 | `receipts/tool_identity.log` |
| † Cross-check, run after reading the parallel round | zero-seed MAC `02:00:00:00:AC:E1`: 1 distinct ANNOUNCE interval (304,880 cycles) against 25 for an ordinary MAC; seed 0xFEFF with count 8: ANNOUNCE, `addr_valid_o` 1, block end 0x0FF07, past the 0xFE00 pool | `receipts/crosscheck.log`, `scripts/r548_crosscheck.cpp` |

**Resource records.** The re-recorded route-1x1 figures match the published REVIEW READY and PR-body figures exactly:

| Figure | Recorded value |
|---|---|
| LUT | 50,088 |
| FF | 54,188 |
| SLICE | 15,843 |
| RAMB36 | 74 |
| RAMB18 | 27 |
| DSP | 14 |
| WNS / WHS | +0.317 / +0.036 ns |
| CARRY4 | 3,372 |

- ooc-1x1 (23,178 LUT) and ooc-8x8 (29,853 LUT) kept every figure. Only their `inputs_sha256` and `measured` changed.
- The arithmetic in `AREA_BUDGET.md` is consistent with the record: 79.00 %, 12,048 over, 99.96 %, 7 free, wrapper 22,984 and at most 10,936, and a +0.067 ns fall limit.
- The dev in-context figure, 479 / 267, matches `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:223`. `KL_maap.sv` was last changed on 2026-08-25, before that measurement.

## Lens results

The first block is as written in my independent pass. The † block was added after the parallel cross-check.

```text
[R548] PASS RTL - hdl/ieee1722/maap/KL_maap.sv@c7b69cd0 (full read :110-408; diff vs e21c1ca0) - FSM priority (disable > Restart! > sDefend > timer send), probe_left 3-bit 4..1, 17-bit range ends, conf_cnt truncation, octet_rev compare, TX latching under backpressure, RX beat selection; Verilator -Wall lint has no new warning; Yosys OOC 474/278 against 637/268; no clock or CDC change; ports, CSR fields and state_o unchanged
[R548] MINOR Conformance - docs/design/MAAP_FABRIC.md:125-126 - F2 (Table B.7 probetimer!/probeCount! misread in a deviation's consequence); RTL items 1-4 conform cell by cell (table above)
[R548] MINOR Robustness - hdl/ieee1722/maap/KL_maap.sv:262-264 + tb/verilator/maap/sim_main.cpp:335-346 - F1 (in-flight frame integrity under backpressure on the RX/DEFEND path is unverified; the RTL is correct at this head)
[R548] MINOR Tests - tb/verilator/maap/sim_main.cpp:335-346, tb/verilator/maap/mutants.py - F1 (the guard mutant survives 120 checks and 22 mutants)
[R548] MINOR Docs - docs/design/MAAP_FABRIC.md:125-126 - F2; R1 and R2 are RESIDUE
```

```text
† [R548] MINOR RTL - hdl/ieee1722/maap/KL_maap.sv:139-140,278-279 - F3 (zero LFSR seed for 1 in 65,536 station MACs freezes the B.3.4 timer draws); the RTL PASS above is withdrawn
† [R548] MINOR Conformance - KL_maap.sv:161-162; docs/design/MAAP_FABRIC.md:50-51 - F3 (B.3.4 random T absent for the zero-seed MAC class), F5 (Table B.9 containment claim false on the seed path)
† [R548] MINOR Robustness - KL_maap.sv:278-279 - F3 (configuration-dependent: the station MAC decides whether the timers randomize)
† [R548] MINOR Tests - tb/verilator/maap/sim_main.cpp:47 - F3 (one station MAC only; no zero-seed check)
† [R548] MINOR Docs - docs/design/MAAP_FABRIC.md:50-51,62,85 - F3, F4 (was R2), F5; R1 is folded into F3
```

The Tests lens otherwise holds:
- Each of the 22 named mutants fails its own named check.
- 11 of my 14 independent probes are killed.
- The harness expectations come from the clauses: the open intervals, Figure B.1, the Table B.7 cells and compare_MAC operands that are sensitive to the octet reversal.
- The crflic change and the differential re-pointing do not weaken any assertion.

The Docs lens otherwise holds:
- `FR_NFR.md:167`, `TESTING.md:519`, `KL_maap.md`, `sw/firmware/ctrl/maap/README.md`, the two suite READMEs, `AREA_BUDGET.md`, the #234 findings header and the findings index all match the RTL and the record.
- The docs gates pass.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2; † F3, F5) | IEEE 1722-2016 B.2.1-B.2.8, B.3.1-B.3.6.7, Tables B.7/B.8/B.9/B.10 against `KL_maap.sv:110-408`; `MAAP_FABRIC.md:42-135`; issue acceptance, 6043036997, 6043296747; † `receipts/crosscheck.log` | R548-1 | `c7b69cd0fb2bdf980546ab413b3b82198267cbd8` |
| RTL | † UNCLEAN (F3); CLEAN in the independent pass | `KL_maap.sv` full and diff vs `e21c1ca0`; Verilator lint head/base; Yosys OOC head/base; 14 fault probes; directed in-flight probe; † zero-seed cross-check | R548-1 | `c7b69cd0fb2bdf980546ab413b3b82198267cbd8` |
| Robustness | UNCLEAN (F1; † F3) | backpressure and in-flight paths (`KL_maap.sv:213-264`, `sim_main.cpp:335-346`, `receipts/inflight_*`), disable/re-enable, version handling, non-pool/disjoint/empty/adjacent ranges, restart during TX; † station-MAC dependence of the seed | R548-1 | `c7b69cd0fb2bdf980546ab413b3b82198267cbd8` |
| Tests | UNCLEAN (F1; † F3) | `sim_main.cpp` (120 checks), `mutants.py` (23/23), coverage 100 %, differential 12/12 and 16/16, crflic leg 417 and campaign 7/7, `measure_test_evidence --check` | R548-1 | `c7b69cd0fb2bdf980546ab413b3b82198267cbd8` |
| Docs | UNCLEAN (F2; † F3, F4, F5) | `MAAP_FABRIC.md`, `FR_NFR.md:167`, `TESTING.md:519`, `KL_maap.md`, ctrl MAAP README, milan_dp/pp_shadow READMEs, `AREA_BUDGET.md`, #234 findings, findings index, PR body, docs gates | R548-1 | `c7b69cd0fb2bdf980546ab413b3b82198267cbd8` |

† Changed after reading the parallel round R549-1 (comment 6047415775). My independent ledger, written first, had RTL CLEAN, Conformance UNCLEAN (F2), Robustness and Tests UNCLEAN (F1), and Docs UNCLEAN (F2, with R1 and R2 as residue). The verdict was NEGATIVE before and after.

## Prior and parallel public findings

**Prior findings.** When my independent pass started there were none. PR #695 carried only the two review-start notices (6047108671 and 6047116152), there were no PR review objects or inline comments, and issue #686 had no review findings. No prior finding needs resolving or retaining at this head.

**Parallel review.** While this round ran, the parallel external round R549-1 posted a verdict on the same head (comment 6047415775). I wrote this verdict, the findings and the ledger before reading it (`receipts/independence.log`). It is a parallel round, not a prior one. Its disposition is recorded in the section below, which is the only part written after reading it.

**Disposition of the parallel round's findings at this head.** All four stay open.

| Parallel finding | Disposition | My evidence |
|---|---|---|
| R549-1-F1, zero-seed LFSR freezes the timer draws (MAJOR) | Retained, open. I reproduced it and adopted it as F3. I rate it MINOR, because the intervals stay inside both open intervals and 1 in 65,536 MACs are affected. The stricter class stands until the manager settles it. My independent pass missed this. | `receipts/crosscheck.log` (A-zero-seed: 1 distinct interval) |
| R549-1-F2, all-fields snapshot overclaim (MINOR) | Retained, open. It is the same defect as my R2, which I first filed as RESIDUE. I accept MINOR and adopt it as F4. | `KL_maap.sv:229`, `:238` read live |
| R549-1-F3, unconditional pool-containment claim (MINOR) | Retained, open. I reproduced it and adopted it as F5. I also attribute it to Conformance, because the sentence is a Table B.9 claim. | `receipts/crosscheck.log` (B: block end 0x0FF07) |
| R549-1-F4, resource records lack public raw receipts (MAJOR) | Retained, open, as an evidence-publication gap. My own limits section says the same: only figures and hashes are public, and I could check the records for consistency and policy (`receipts/baseline_diff.log`, `receipts/check_baseline.log`) but not against raw reports. It is not a defect in the source tree, so I do not attribute it to a source lens. The manager owns publishing the receipts, and the second-to-merge re-record with #682 replaces these records anyway. | `receipts/baseline_diff.log` |

The parallel round has no counterpart for my F1 or F2. Both stay open.

## Limits and pending manager duties

**Limits.**
- The Vivado figures are not reproduced here. I did not run Vivado. The raw route and standalone reports are not published, only their sha256 values in the author's handoff. I checked the records for internal consistency, against the published figures and with `check-baseline`. I did not check them against the reports themselves. The `inputs_sha256` values were not recomputed, because that needs the builder export. The in-context figure of 435 / 279 is the author's.
- Physical calibration and bench interop were NOT RUN. Simulation and field skips are not hardware proof.
- My runs were source validation at this head. They are not the final current-dev candidate.
- The full parent, processor, gPTP, Yosys and builder banks, and the other datapath suites (milan_dp full, pp_shadow, capture_coherence, milan_dp_mclk, milan_dp_render), were not re-run. The manager's bank evidence covers them.
- The ctrl RV32 suite (`--require-rv32`) was not re-run. I ran only the host-built differential.
- Hosted checks at this head when I looked:
  - completed with success: rtl-fast, the Yosys shards 0 to 3, yosys-elaboration, verilator-lint, firmware-unit, full-ci-gate and docs-check-no-git;
  - still in progress: the Verilator shards 0 to 4, elaborate and docs-check;
  - skipped: "Physical gPTP".

  The manager owns hosted acceptance.
- In the published copies of `crflic_leg.log`, `maap_coverage.log` and `maap_differential_selftest.log.gz`, a home-directory prefix in compiler include paths is replaced by `<home>`. No other content was changed.

**Pending manager duties.**
1. Acceptance 4: the bench interop with the reference peer, after merge. The wire now differs: cdl 16, a unicast DEFEND and a 30 to 32 s ANNOUNCE.
2. File the follow-up issue or issues for the six remaining deviations. No public issue exists for them; the only issues with MAAP in the title are #686, #665, #664 and #403.
3. Candidate merge validation at live dev `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`.
4. Re-record order with #682 (pin `2ad2f845`, baseline F): whichever merges second re-records the three endpoints on the merge result.
5. Hosted Verilator shard acceptance at the final head.
6. Nothing goes to the residue checklist: R1 is folded into F3, and R2 became F4.
7. Settle the severity of F3 (MINOR here, MAJOR in the parallel round), and publish the raw resource receipts (R549-1-F4).
8. Re-review the commits that fix F1 to F5. The fixes touch `tb/verilator/maap` and `docs/design/MAAP_FABRIC.md`, and `KL_maap.sv` for F3. That un-covers all five lenses.

## Receipts

The receipts are under `receipts/` and the scripts under `scripts/`. `MANIFEST.sha256` lists every published file. Paths are relative to this packet.

R548-1 FINISHED
