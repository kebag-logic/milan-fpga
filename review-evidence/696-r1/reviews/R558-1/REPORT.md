[R558] NEGATIVE - exact head 030eb98a12685a2ca41cf8d785bb0eb69dc32a98

Round R558-1. Internal cleared-context review of issue #696 / PR #706.
Head `030eb98a12685a2ca41cf8d785bb0eb69dc32a98`, tree `7f6bb537f2979cee38d199cf709bce782cdd6db5`.
Source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. Merged dev `8b61b70902f3ebf118e56967277e2686731081bd`.

All five lenses were applied. Conformance, RTL, Robustness and Tests are clean at this head.
Docs is unclean because of one MINOR finding (R558-1-F1). The MAAP design page still states the pre-merge MAAP area as if it were the measurement for this head. The fix is one line.
That one open MINOR is the only reason for the NEGATIVE verdict. There are no BLOCKER or MAJOR findings and no RESIDUE.

## 1. How the task was reconstructed

I read the following, in this order:

- AGENTS.md and CONTRIBUTING.md (sections 2.1 and 3).
- docs/README.md.
- The issue #696 body (acceptance 1-4) and assignment 6076750392.
- Rulings 6076940309, 6079087547, 6079463350, 6080332335 and 6089712293.
- The author STOP and REVIEW READY comments on the issue, and the PR #706 body.
- REQUIREMENTS.md, the MAAP rows only.
- docs/design/MAAP_FABRIC.md, hdl/ieee1722/maap/doc/KL_maap/KL_maap.md and hdl/milan/KL_pp_maap_shim.sv (its conflict-trigger contract).
- `git diff 6aa25dec..030eb98a` and the lane history.
- The public evidence tree `97f433d6:review-evidence/696-r1`.

Prior public review findings: at review time, PR #706 had no reviews. Its only comments were the two review-start notices, and the issue has no reviewer comments. No earlier finding exists to resolve or retain.

## 2. Findings

### R558-1-F1 - MINOR - Docs - `docs/design/MAAP_FABRIC.md:141-143`: the MAAP area figure is the pre-merge lane head, not this head

- **What the page says:** "Its 1x1 recipe measures `g_maap.maap_engine` at 441 LUT / 340 FF. Against `6aa25dec` (439 LUT / 280 FF), growth is +2 LUT / +60 FF." The sentence is in the present tense, with no commit. The M6 bullet two items later does qualify its figure ("At the M6 step").
- **What was measured:**
  - 441 / 340 is the lane head `39571196` before the merge (`author/final-receipts/area/m3/util_hier_base.rpt`).
  - At merge result `0df48637`, whose MAAP and datapath bytes this head carries, the same instrument measures **445 LUT / 340 FF**, which is **+6 / +60** against `6aa25dec` (`author/merge-receipts/maap-ooc-merged/util_hier_base.rpt:66`).
  - Dev `8b61b709` alone measures 443 / 280 (`maap-ooc-dev/util_hier_base.rpt:67`), so the lane's own share is +2 / +60.
  - The PR body and the REVIEW READY comment both state 445 / 340 for the merge result. The authoritative design page does not.
- **Authority:** AGENTS.md section 7, "authoritative documentation is current"; ruling 6089712293 item 4, which asks for the MAAP resources at the merged head against the ceiling.
- **Impact:** a reader of the design page reads 441 / +2 as the area of the image being merged, against a ceiling whose FF allowance is fully used. The ceiling verdict does not change (+6 / +60 still fits +60 / +60). But a measurement figure of record is stale, so this is not wording-only RESIDUE.
- **Required outcome:** the page states the figure for the code being merged. Either:
  - give the merge-result figure (445 / 340, +6 / +60 against `6aa25dec`, lane share +2 / +60 against dev `8b61b709`); or
  - explicitly attribute 441 / 340 to the pre-merge lane head `39571196` and add the merge-result figure.
- **Verification:** reread `MAAP_FABRIC.md:138-144` against the two `util_hier_base.rpt` rows above. Rerun `docs_check.py`, `gen_toc.py --check` and `check_em_dash.py`.

### R558-1-S1 - SUGGESTION - Docs - `docs/design/MARK_II_AREA_PLAN.md:56`: gate row written for the superseded record

- **What it says:** "With the current record, WNS >= +0.049 ns also preserves the 0.25 ns fall limit."
- The sentence is still literally true. But at the new +0.114 ns record, the binding limit is the absolute +0.030 ns floor. This lane already updated the identical sentence in `AREA_BUDGET.md:383`.
- **Optional change:** align the row, or point it at `AREA_BUDGET.md#the-resource-gate`. It does not affect any lens.

## 3. Results per lens

### Conformance - CLEAN

[R558] PASS Conformance - `hdl/ieee1722/maap/KL_maap.sv` at 030eb98a, `hdl/milan/milan_datapath.sv:7171-7172`, `docs/design/MAAP_FABRIC.md` - each item checked against the issue clause, the ruling and the harness:

| Item | Clause (issue/rulings) | Implementation at head | Result |
|---|---|---|---|
| M4 seed timing | B.3.4 NOTE, B.3.6.1 | `KL_maap.sv:352-355`: the seed is taken at the first `enable_i` after reset. Shipping firmware writes the MAC before MAAP_CTRL (`milan_baremetal.c:1591-1592` then `:1601`). | Conformed. Datapath check reproduced: intervals [5249,5290,5360] and [5259,5550,5270]. |
| M2 DEFEND echo | B.3.6.6 | `:405-412` latches the PROBE's start and all 16 count bits. `:248-253` selects them for a DEFEND only. The high octets are the pool base because conflicts need `rx_pool_r`. | Conformed |
| M7 supplied seed | B.4, Table B.9 | `:300-308`: the block must satisfy offset < 0xFE00 and end <= 0xFE00. Otherwise a bounded random draw is used. | Conformed |
| M8 truncated PDU | B.2 (counting withdrawn by 6076940309) | `:191-195`, `:371` and `:393-394` require every keep strobe through byte 41. The count is recorded as a deviation in `MAAP_FABRIC.md:160-162`. | Conformed as ruled |
| M1 compare_MAC | Table B.7 note d, B.3.6.4 | `:285-290` covers the rProbe!/PROBE and rDefend!/DEFEND cells. rDefend!/PROBE and rAnnounce!/PROBE still restart unconditionally. | Conformed |
| M5 PortOperational! | B.3.5.9, Table B.7 | `:156-157` detects the rising edge. `:433` restarts without counting a conflict. It is wired from the existing `eff_link_w` with no register-map change. | Conformed |
| M6 busy-wire PROBE | Table B.7, B.3.6.6 | `:293-297` and `:399-413`: one shared buffer defends after the wire frees. Its capacity of one response is recorded as a deviation (`MAAP_FABRIC.md:145-158`), as ruling 6079087547 item 3 allows. | Conformed within the documented limit |
| M3 generator | B.3.6.1 | `:144-149`: 32-bit LFSR with taps 32,22,2,1, seeded from MAC[31:0] plus PHC[31:0]. My own GF(2) order computation confirms period 2^32-1 (`receipts/lfsr-order.log`). The pool fold bias is recorded as a deviation, as ruling 6079087547 item 4 allows. | Conformed for period and seed |

Acceptance:

- Acceptance 1 is met; the M6 capacity, the M3 pool bias and the M8 count are documented by clause.
- Acceptance 2 is met.
- Acceptance 3 is met (section 5).
- Acceptance 4 is assigned to the post-merge bench lane.

There is no register-map, filter, mailbox, firmware-source or pin change. The lane's firmware edits are limited to the two authorized test files and the authorized README.

### RTL - CLEAN

[R558] PASS RTL - `KL_maap.sv:141-476`, `milan_datapath.sv:2934-2956,3000,7168-7172`, `KL_pp_maap_shim.sv:103-124`, merge-result reports. What was checked:

- **Clock domains.** `ptp_now_w` comes from `ts_counter` on `gtx_clk`. The documented contract is gtx_clk == axis_clk, and the routed report times PHC `acc_reg[31]` to `offset_r_reg[12]` as a synchronous 20 ns path with +4.037 ns of slack. `eff_link_w` is an existing axis-domain level. No new crossing is introduced.
- **Widths.** I checked the 17-bit seed end, the 16-bit echo with an 8-bit own count, and the overlap count (at most 255).
- **Fixed point.** The all-zero LFSR state is avoided.
- **Priority order.** Disable, then restart or link return, then DEFEND, then the timer. A response being saved can never alter a frame in flight, because the PROBE and ANNOUNCE own-range snapshots `tx_off_r`/`tx_own_cnt_r` are separate from the DEFEND fields.
- **Shim contract.** A re-probe on link return leaves ANNOUNCE, so the shim's `blk_valid_i` falling-edge trigger covers it.
- **Lint ratchet.** It passes 90 <= 90 (`receipts/lint-check.log`). The single MAAP item, `:381`, is pre-existing and unchanged.

### Robustness - CLEAN

[R558] PASS Robustness - `KL_maap.sv:371-413,431-440`; harness sections `pending_response_cancelled`, `truncated_pdus_have_no_effect`, `supplied_seed_bounds`, `port_return_reprobes` at head. The following cases were checked and are graded:

- Truncation at every length from 1 to 41 bytes, and every single missing keep byte from 0 to 41 in a full-length frame, in both states. Each is compared cycle-for-cycle with an idle RX tap.
- Supplied seeds at the boundary, one past it, at 0xFE00, at 0xFF00 and at 0xFFFF, for counts 1, 8 and 255.
- Disable, link return, a conflicting-ANNOUNCE restart and reset, each while a DEFEND is pending. In every case the pending DEFEND is discarded.
- Backpressure at 0, 2, 4 and 7 accepted beats while a DEFEND or an ANNOUNCE is on the wire.
- A steady operational level, which must not restart.
- Equal MAC addresses, which make this station yield.

The single-response capacity is a documented deviation, not an unhandled path.

### Tests - CLEAN

[R558] PASS Tests - `tb/verilator/maap/{sim_main.cpp,sim_integration.cpp,mutants.py,Makefile,integration.mk}`, `sw/firmware/ctrl/test/{test_maap_differential.cpp,maap_differential.py}` at head. Every run used the pinned Verilator 5.050, identity checked.

| Gate | Reproduced at head | Receipt |
|---|---|---|
| Unit harness | 171 checks, 0 failures, rc 0 | `receipts/focus/unit.log` |
| Real-datapath harness | 3 checks, 0 failures (M4, M5, M3), rc 0 | `receipts/focus/integration.log` |
| Planted-defect campaign | 51 rows: 49 defects exit 1 at their named check, 2 clean controls, 0 escapes, rc 0 | `receipts/focus/campaign.log` |
| Line coverage | 215/215 (100 %, gate 95 %), rc 0 | `receipts/focus/coverage.log` |
| Firmware differential `--self-test` | 12/12 cases, 17/17 defects, highest-draw sweep 5173..5810 cycles, rc 0 | `receipts/differential-summary.log` |
| Reviewer plants | 14/14 caught: 7 author plants re-applied independently (M1, M2, M4 datapath, M5, M6, M7, M8) and 7 new plants | `receipts/plants.log` |

The 7 new plants were:

- M2 echoing only the low byte of the count;
- M8 requiring only one byte in beat 5;
- M5 counting a link return as a conflict;
- M6 keeping a pending DEFEND across a restart;
- M3 reseeding on every enabled cycle;
- M1 with the PROBE cell inverted;
- M5 with the datapath link edge disabled.

Each new plant built, exited 1 and failed the expected named check.

### Docs - UNCLEAN (R558-1-F1 open)

These parts of the documentation were examined and are clean:

- `KL_maap.md` (port table and behaviour text) and `sw/firmware/ctrl/maap/README.md:189-192` match the RTL and the sweep.
- The `KL_maap.sv` banner matches the code.
- The `AREA_BUDGET.md` and #234 findings changes in `030eb98a` match the recorded baseline exactly (section 5).
- `docs_check.py`, `gen_toc.py --check` and `check_em_dash.py --base 8b61b709` all pass (rc 0).

The open finding is `MAAP_FABRIC.md:141-143` (R558-1-F1).

## 4. Merge commit `0df48637`

`receipts/merge-check.log`, produced by `scripts/merge_check.sh`, shows:

- The automatic merge of `39571196` and `8b61b709` has no conflict and produces tree `c7fa1f77`. That is the recorded merge tree.
- The lane diff over dev and the lane diff over `6aa25dec` are byte-identical once hunk positions are normalised (sha256 `e2aa55f8...`, 12 files). Only the `milan_datapath.sv` hunk offset moves, from line 7065 to line 7168.
- The commits after the merge touch only `pp_resource_baseline.json`, `AREA_BUDGET.md` and the #234 findings.
- The gitlinks equal dev's.
- Every commit message is a single line with no trailers (`receipts/commit-format.log`).

## 5. Resource re-record and the docs commit

- **`e6f00121` changes only figures, scopes, input digests and measured notes.** Against dev `8b61b709`, those classes account for 58 changed values. No tolerance, floor, ceiling or identity changed (`scripts/policy_diff.py`, `receipts/policy-diff-dev-vs-head.log`).
- **`check-baseline` passes** (`receipts/check-baseline-head.log`).
- **The committed file matches the record step.** It is byte-identical to the published `record/resource-baseline-after.json`. The `before` file equals dev's. All `record --write`, the re-checks after the write, and `check-baseline` exited 0.
- **`route-1x1`:**
  - WNS is +0.114 ns, at or above the +0.030 ns floor. No exception or waiver key exists.
  - The fall is 0.185 ns, within the 0.25 ns limit.
  - WHS is +0.036 ns.
  - All 101,344 of 101,344 nets are routed.
  - The figures (LUT 50,230, FF 54,308, slice 15,823, RAMB36 74, RAMB18 27, DSP 14, CARRY4 3,397) match the published `baseline_utilization.rpt` and `worst_path.rpt`.
  - Datapath 41,367 LUT and KL_maap 425 / 339 match `baseline_hierarchy.rpt:114,163`.
- **`ooc-1x1` and `ooc-8x8`** keep every figure.
- **MAAP against the ceiling at the merge result:** 445 LUT / 340 FF, +6 / +60, within +60 / +60, with the FF allowance fully used.
- **`030eb98a` matches the record.** I checked every figure in the AREA_BUDGET record table against the record:
  - 79.23 / 42.83 / 99.83 %, 27 free slices, 12,190 over;
  - wrapper 22,873, needs at most 10,683, 53 %;
  - 41,367 / 65.2 %;
  - the binding-limit sentence (0.114 - 0.030 = 0.084);
  - the seventh re-baseline deltas.

  The #234 tables (endpoints, deltas, input SHA-256 values, the worst path 9.574 = 2.279 + 7.295 ns, and the MAAP slack figures +4.037 / +6.719 / +0.135) also match.

## 6. Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_maap.sv`, `milan_datapath.sv:7171-7172`, `MAAP_FABRIC.md`, issue acceptance, the 5 rulings, `milan_baremetal.c:1591-1601` | R558-1 | 030eb98a12685a2ca41cf8d785bb0eb69dc32a98 |
| RTL | CLEAN | `KL_maap.sv:141-476`, `milan_datapath.sv` PHC/link/MAAP wiring, `KL_pp_maap_shim.sv:103-124`, routed MAAP slack reports, lint ratchet | R558-1 | 030eb98a12685a2ca41cf8d785bb0eb69dc32a98 |
| Robustness | CLEAN | truncation, seed-boundary, cancellation, backpressure and link-level paths in RTL and harness | R558-1 | 030eb98a12685a2ca41cf8d785bb0eb69dc32a98 |
| Tests | CLEAN | unit, datapath, campaign, coverage, differential, 14 reviewer plants | R558-1 | 030eb98a12685a2ca41cf8d785bb0eb69dc32a98 |
| Docs | UNCLEAN (R558-1-F1) | `MAAP_FABRIC.md`, `KL_maap.md`, firmware MAAP README, `AREA_BUDGET.md`, #234 findings, `MARK_II_AREA_PLAN.md`, PR body | R558-1 | 030eb98a12685a2ca41cf8d785bb0eb69dc32a98 |

## 7. Limits

- The IEEE 1722-2016 text was not available inside this review. Clause conformance is judged against the clauses the issue and rulings cite, the repository's clause-by-clause contract, and the harness checks.
- **Not rerun here (author receipts only):**
  - the full parent suite sweep (61/61);
  - Yosys portability (58/58);
  - the xvlog parser gate;
  - behave (404 scenarios);
  - the RV32 firmware bank;
  - the 94-command docs bank;
  - `tsn_fuzz`;
  - the processor banks.

  I ran the lint ratchet and three documentation checks.
- **Vivado measurements were not reproduced.** The published measurement directories leave out large inputs (the route timing report and cell tables), so the gate's `check` cannot re-read them (`receipts/recheck-published-dirs.log`). The recorded figures were cross-checked against the published reports instead. The four-corner timing table appears only in the author's HANDOFF; no raw corner receipt is published.
- **Hosted checks at this exact head were still running at my last snapshot** (`receipts/hosted-check-runs.tsv`, 03:03Z): 12 success, 7 in progress, and 1 skipped (Physical gPTP, nightly/manual). No hosted verdict is claimed.
- Physical calibration was not run. The field-campaign skips are not hardware proof. Bench interop (acceptance 4) is not evidenced here.
- No manager source bank ran at this head, and none is claimed. The current-dev candidate was not built: this head is based on `8b61b709`, while live dev is `aef7ac66605c4404900ce04cbaaeff88e41bb880`.

## 8. Pending manager duties

- Carry R558-1-F1 to the author, then have a reviewer re-check the corrected head under the Docs lens.
- Build and validate the current-dev merge candidate against live dev `aef7ac66` (builder and native banks), and publish the receipts.
- Accept the hosted and replica checks on the final PR head. Note that the Verilator shards, `firmware-unit`, `elaborate` and `docs-check` were still running at my snapshot.
- Hand acceptance 4 to the post-merge bench lane.
- Optionally carry R558-1-S1.

## 9. Receipts and reproduction

All receipt paths below are relative to this packet and listed in `MANIFEST.sha256`.

- **Scripts:**
  - `scripts/launch_focus.sh <tree> <out>`: runs the five focused gates concurrently. It expects `scratch/bin/verilator` and `verilator_coverage` shims that select the pinned 5.050.
  - `scripts/plants.py <tree> <work> --jobs N`
  - `scripts/merge_check.sh <repo>`
  - `scripts/policy_diff.py <repo> <old> <new>`
  - `scripts/lfsr_order.py`
- **Receipts:** under `receipts/`.
- After the probes, the review clone was verified byte-exact at the head:
  - worktree equals index equals HEAD;
  - index modes, blobs and paths equal the HEAD tree;
  - gitlinks unchanged;
  - no untracked files.

  Before that check I removed one ignored `__pycache__` that my `check-baseline` run had created (`receipts/clone-integrity.log`).

R558-1 FINISHED
