[R559] NEGATIVE - exact head 030eb98a12685a2ca41cf8d785bb0eb69dc32a98

Round R559-1, external cleared-context review of PR #706 (issue #696), tree `7f6bb537f2979cee38d199cf709bce782cdd6db5`.
Source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`; merged dev `8b61b70902f3ebf118e56967277e2686731081bd`; live dev named by the manager `aef7ac66605c4404900ce04cbaaeff88e41bb880` (not built here).

## Verdict in one paragraph

The RTL is sound. Each closed deviation conforms to the IEEE 1722-2016 Annex B text: M1, M2, M4, M5 and M7 fully, and M3, M6 and M8 within their recorded, ruled limits.
The merge of dev is clean and content-preserving. The resource re-record was written by `record --write` with every policy value unchanged. The two re-baseline docs pages match the record figure for figure.
I reproduced every advertised suite number:
- 171 unit and 3 datapath checks;
- 215/215 lines;
- 49/49 planted defects plus 2 controls;
- 12/12 differential cases and 17/17 differential defects.

The verdict is NEGATIVE on three MINOR findings in the `Tests` and `Docs` lenses:
- **F1:** both M5 checks hold the link down for only 8 cycles, so a restart on link *loss* instead of link *return* passes the whole MAAP target.
- **F2:** the Mark II plan still calls the superseded figures "the current record".
- **F3:** a changed zero-seed test fixture is still described by its old MAC.

`Conformance`, `RTL` and `Robustness` are covered clean at this head.

## Reconstruction (public state only)

Read in order:
1. `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
2. Issue #696: the body and its acceptance 1-4; assignment 6076750392; the author STOP comments; rulings 6076940309, 6079087547, 6079463350, 6080332335 and 6089712293; REVIEW READY 6092935897.
3. `REQUIREMENTS.md` and FR-MAAP-01.
4. The IEEE 1722-2016 Annex B text, B.1 to B.4 with Tables B.7 to B.10, read from a licensed copy that is not republished here.
5. `docs/design/MAAP_FABRIC.md`, `KL_maap.md`, `AREA_BUDGET.md`, the #234 findings page and the Mark II plan.
6. The diff `6aa25dec..030eb98a` and its history.
7. The published evidence tree `97f433d6…/review-evidence/696-r1`.

The PR carries no prior review findings: zero reviews, zero inline comments, and only the two review-start notices. Two earlier findings tracked by the issue are resolved at this head:
- **R548-2-F1 (M4 seed timing):** resolved. Sampling now happens at first enable (`KL_maap.sv:350-355`). The datapath check, the author's reset-sampling defect and my plant `r_seed_from_mac_high_bits` all grade it.
- **R548-1-S2 (M8 truncation):** resolved as ruled. Truncated PDUs are discarded with no effect. The missing count is recorded as a B.2 deviation in `MAAP_FABRIC.md:160-162`, per ruling 6076940309.

## What I executed (receipts in this packet)

All runs used the pinned Verilator 5.050, with identity verified (`--version` = `5.050 rev v5.050`). Builds and outputs went to a scratch directory, never the clone.

| Run | Result | Receipt |
|---|---|---|
| MAAP unit harness (`make run`) | 171 checks, 0 failures, rc 0 | `receipts/campaign/unit.*` |
| Real-datapath integration (`integration-build` + run) | 3 checks, 0 failures; M4 stations draw 5249/5290/5360 vs 5259/5550/5270 cycles | `receipts/campaign/integration.*` |
| Coverage gate | `KL_maap.sv` 215/215 lines (100 %), gate PASS | `receipts/campaign/coverage.*` |
| Parallel replay of `mutants.py` (its own `MUTANTS` table and `run_case()` acceptance, the four datapath rows of its `main()`) | 51 rows: 2 clean controls pass; 49/49 defects exit 1 at their named check; #686 item guard holds | `receipts/campaign/campaign-summary.txt`, `campaign-rows.json` |
| Firmware differential `--self-test` | clean 12/12 tests; 17/17 differential defects caught; overall rc 0; 1,024 MAC/phase pairs give 5173..5810 cycles | `receipts/campaign/differential.log.gz`, `.rc` |
| Reviewer plants (11, not in the author's table) | 9 caught at the named check; **the link-loss edge defect escapes both unit and datapath (F1)** | `receipts/plants/SUMMARY.txt`, `*.patch`, `*.log`, `*.rc` |
| Independent generator-order check (hand-built from the RTL expression, not the harness) | `{r[30:0], r31^r21^r1^r0}` has order exactly 2^32-1; seeding with the low 32 bits of MAC + clock equals the low 32 bits of the full sum | `scripts/lfsr_period.py`, `receipts/lfsr_period.*` |
| Merge checks | parents `39571196`, `8b61b709`; empty remerge diff; the lane diff over dev equals the lane diff over `6aa25dec` (same 12 files, identical 1,473 body lines, only index and hunk-offset lines differ, in `milan_datapath.sv`); gitlinks identical across base, lane, dev, merge and head | `scripts/merge_equivalence.py`, `receipts/merge_equivalence.*` |
| Re-record checks | only measured fields changed (58 leaves; 0 policy, identity or schema leaves); the published `record --write` after-file is byte-identical to the head's baseline, and the before-file to the merge's; `check-baseline` PASS, 3 endpoints | `scripts/policy_diff.py`, `receipts/rerecord.log`, `receipts/check-baseline.*` |
| Docs figures vs record | 24/24 figure checks match (budget table, binding-limit arithmetic, wrapper ceiling, findings tables, input SHA-256s, deltas) | `scripts/docs_vs_record.py`, `receipts/docs_vs_record.log` |
| MAAP ceiling | merge-result instrument 445 LUT / 340 FF = +6 / +60 vs `6aa25dec` (439/280); dev alone 443/280; the measured `KL_maap.sv` and `milan_datapath.sv` hash equal to this head's files | `receipts/maap_ceiling.log` |
| Static | `docs_check` 0 findings; em-dash 0 findings over `8b61b709..HEAD` and `6aa25dec..HEAD`, self-test 339 arms; TOC OK; lint 90 <= 90; `pp_srcs --check` and `measure_test_evidence --check` pass | `receipts/static/*` |
| Clone restore | HEAD and tree exact; index tree = HEAD tree; worktree = index; no index flags; every tracked blob rehashes equal with its mode; gitlinks at pins; submodule worktrees clean | `receipts/restore.log` |

## Findings

### F1 - MINOR - Tests - `tb/verilator/maap/sim_main.cpp:743`, `tb/verilator/maap/sim_integration.cpp:46-47` - M5 checks cannot tell link return from link loss

- **Authority:** B.3.5.9 says PortOperational! fires when the port *enters* an operational state. Table B.7 defines no event for leaving it.
  AGENTS.md section 6 (`Tests`) requires that each new test can fail for the defect it claims to detect. The check names claim "link return restarts PROBE" and "link return revokes and reprobes".
- **Evidence:** both checks drop the port for only 8 cycles. That is shorter than one 8-beat PROBE frame, so a restart at the falling edge is indistinguishable from one at the rising edge.
  Plant `r_restart_on_link_loss` (`KL_maap.sv:157` to `!port_operational_i && port_operational_r`) passes the unit harness at 171 checks, 0 failures. It also passes the datapath harness at 3 checks, 0 failures, with output identical to the clean run (`delay 504`).
  The author's M5 defects only cover "ignore the event" and "level-sensitive", so the whole default MAAP target is blind to this.
- **Impact:** the RTL at this head is correct. A regression to edge-on-loss would ship green. That engine would probe into a dead link and announce on return without having probed the live network, which is exactly the M5 deviation #696 closes.
- **Required outcome:** at least one M5 check holds the port non-operational long enough for a loss-edge restart to be observable. Example: an outage longer than a full PROBE walk, with no restart or PROBE attributable to the drop, and the fresh walk starting after the rise.
  A planted falling-edge defect must fail that named check in the default campaign, in the unit harness, the datapath harness or both.
- **Verification:** rerun `make -C tb/verilator/maap` (unit plus campaign) and re-apply `receipts/plants/r_restart_on_link_loss.patch`. Its named M5 check must fail.

### F2 - MINOR - Docs - `docs/design/MARK_II_AREA_PLAN.md:108-137` - "Current record" figures superseded by this PR's re-record

- **Authority:** AGENTS.md section 6 (`Docs`) says changed contracts must be reflected in authoritative docs. This PR changes the gate's record (`e6f00121`) and updates the budget and findings pages to it (`030eb98a`).
- **Evidence:** the plan says "These are the current record's source-scope references". At dev `8b61b709` that was true. At this head the route column no longer matches `syn/ooc/pp_resource_baseline.json`:

  | Scope | Plan | Head record |
  |---|---:|---:|
  | `wrapper` | 23,345 | 22,873 |
  | `u_pp` | 22,794 | 22,318 |
  | `u_pp/u_aecp/u_dyn` | 1,440 | 1,054 |
  | `u_pp/u_notify` | 2,259 | 2,199 |

  `MARK_II_AREA_PLAN.md:56` ("With the current record, WNS >= +0.049 ns also preserves the 0.25 ns fall limit") is still literally sufficient, but it is no longer the binding limit that `AREA_BUDGET.md:383` now states.
- **Impact:** a Mark II lane pricing split savings from the plan's "current record" uses superseded scope figures. The `u_dyn` row alone is off by 386 LUT. Two authoritative area documents now disagree about the current record.
- **Required outcome:** every "current record" statement in the plan is true at the merge head. Either name the record those figures describe (#645/#647, `a5ca6e51`) or refresh them to the #696 record. The choice belongs to the manager.
- **Verification:** each route-column figure the plan attributes to the current record equals the head's `pp_resource_baseline.json` `route-1x1` scopes, or the text names the `a5ca6e51` record.

### F3 - MINOR - Docs, Tests - `docs/design/MAAP_FABRIC.md:222-223`, `tb/verilator/maap/sim_main.cpp:640-641` - Zero-seed fixture described by its superseded MAC

- **Authority:** AGENTS.md section 6 (`Docs`: changed contracts reflected; `Tests`: reports must describe what is tested).
- **Evidence:** this PR changed `kZeroSeedMac` to `0x020000000000` (`sim_main.cpp:59`), because under the new additive 32-bit seed `02:00:00:00:00:00` with clock 0 is the zero sum.
  `MAAP_FABRIC.md:222-223` and the harness banner at `sim_main.cpp:640-641` still name `02:00:00:00:AC:E1`. Under this RTL that MAC seeds `0x0000ACE1`, not the fixed point.
- **Impact:** a reader or reproducer is told that the fixed-point fallback is exercised by a MAC that no longer exercises it. The test log prints the wrong stimulus. The check itself is correct.
- **Required outcome:** both texts name the fixture actually used (`02:00:00:00:00:00` with clock 0).
- **Verification:** grep both files; the zero-seed defects `zero_seed_freezes_*` must still be caught.

### Residue (wording only; carried to the manager's residue checklist)

- **R1** - `docs/design/MAAP_FABRIC.md:141-143`: the 441 LUT / 340 FF figure is the M3 step at lane head `39571196`, before the dev merge. The ceiling conclusion is unchanged at the merge result (445/340, +6/+60).
  Exact fix: replace "Its 1x1 recipe measures" with "At the M3 step (lane head `39571196`, before the dev merge), the 1x1 recipe measures".
- **R2** - `docs/design/MAAP_FABRIC.md:135-136` (and the Contents entry at `:36`): "Remaining deviations outside #686's items. These are recorded here and not changed by #686; each needs its own decision." The list now holds #696 items whose decisions are recorded.
  Exact fix: "**Remaining deviations.** These are recorded here; #696 rulings settled M6 capacity and M8 counting, and any further change needs its own decision."
- **R3** - `docs/findings/README.md:25`: "The gate's current record is #686's re-baseline of 2026-10-08". This was already stale at dev `8b61b709`, and this PR supersedes it again.
  Exact fix: "The gate's current record is #696's re-baseline of 2026-10-10".

### Suggestions (optional)

- **S1:** mutant `m3_trap_outside_basis` traps state `0x12345678`, which is one of the harness's hard-coded linearity samples (`sim_main.cpp:862`). It demonstrates detection only at a sampled state. A trap state outside the explicit list would make the claim stronger.
- **S2:** the PR's "How to validate" runs `"$WORK/integration/maap_integration"` from the repository root. The processor ROM images are then not found (8 `$readmem` warnings). The MAAP checks are unaffected, and the campaign runs it from its build directory. Suggest `(cd "$WORK/integration" && ./maap_integration)`.
- **S3:** the first-enable seed path (PHC through the 32-bit adder and `rand_offset` into `offset_r`) has 18 logic levels and 15.727 ns of data delay. It keeps +4.037 ns at the 50 MHz shipping clock. The RTL default `MILAN_CLK_FREQ_HZ` is 100 MHz. If any non-shipping 100 MHz build is still supported, register the seed or document the 50 MHz assumption.
- **S4:** `mutants.py:192` guards only the #686 items 1-4. A matching guard for M1-M8 would stop a later edit silently dropping a #696 item's last mutant.

## Lens results with evidence

- **PASS `Conformance`** - `KL_maap.sv:146-149, 157, 193-195, 229, 285-297, 301-308, 352-355, 393-394, 401-413, 433-440`; `milan_datapath.sv:7171-7172`. Checked against IEEE 1722-2016 Annex B:
  - **M1:** compare_MAC is octet-reversed, TRUE means no action, per Table B.7 note d and B.3.6.4. The rProbe!/PROBE and rDefend!/DEFEND cells restart only when not lower; the equal-MAC case yields.
  - **M2:** the DEFEND requested_* fields echo the PROBE, with all 16 count bits (B.2.5, B.2.6, B.3.6.6). The conflict_* fields carry the overlap (B.2.7, B.2.8).
  - **M3:** maximal 32-bit generator. The seed is the low 32 bits of MAC + PHC at first enable (B.3.6.1, "least-significant octets of the sum"). Pool-fold bias is documented.
  - **M4:** the seed is taken at first enable, after firmware programs the MAC (`milan_baremetal.c:1591-1601` order).
  - **M5:** a rising `eff_link_w` restarts with a fresh draw (Table B.7 PortOperational! in PROBE/DEFEND = INITIAL/Restart!). The shim fans out on falling validity (`KL_pp_maap_shim.sv:238-241`).
  - **M6:** one shared buffer, with its capacity limit documented as not full conformance.
  - **M7:** a supplied range must fit the 0xFE00 dynamic pool (Table B.9).
  - **M8:** discarded with no effect; the counter deviation is recorded per ruling 6076940309.

  Rulings 6079087547 and 6089712293 are applied: the ceiling is on `g_maap.maap_engine`, at 445/340 at the merge result; dev was merged without a rebase; no floor exception. The scope rulings hold: RTL changes only in `KL_maap.sv` and its six-line datapath integration; no register-map, filter or mailbox change; firmware changes only the two authorized test files and the authorized README.
  Acceptance 1-3 are met on evidence. Acceptance 4 is the post-merge bench lane.
- **PASS `RTL`** - `KL_maap.sv:141-160, 184-196, 215-229, 238-279, 293-308, 310-476`:
  - Every new register (`rng_seeded_r`, `port_operational_r`, `tx_own_cnt_r`, `tx_defend_off_r`, `tx_cnt_r`, `defend_pending_r`, `rx_bytes_valid_r`) is in the synchronous reset.
  - Widths are correct: 17-bit range ends, a 16-bit echo, an 8-bit own-count snapshot, and `lfsr_next_w[15:0]` into `rand_offset`.
  - `defend_w` and `save_probe_w` are mutually exclusive by construction. The DEFEND fields are latched at request time and never alter an in-flight PROBE/ANNOUNCE frame.
  - Priority order is disable, restart/PortOperational, DEFEND, then timer.
  - `realtime_ns_i` follows the existing synchronous PHC contract (`milan_datapath.sv:2934-2935`, as at its other consumers). The routed image times the new path at +4.037 ns setup in and +6.719 ns out (published route queries).
  - Lint is 90 <= 90. The datapath elaborates in my integration builds. Hosted Yosys shards 0-3 succeeded at this head.
- **PASS `Robustness`** - `sim_main.cpp` sections `truncated_pdus_have_no_effect`, `pending_response_cancelled`, `defend_to_the_prober` [4c] and `probe_mid_frame_is_defended`, plus `receipts/campaign/unit.log`. Checked against the lens list:
  - Truncated PDUs at every length 1..41 and every missing byte 0..41 for all three types, against an idle-tap cycle-matched control.
  - Reset, disable, link return and conflicting ANNOUNCE during a pending DEFEND; stalls at 0, 2, 4 and 7 accepted beats; supplied-seed boundaries for counts 1, 8 and 255.
  - A steady link level makes no repeated restart; the empty own range never conflicts.
  - By reading: a link loss leaves the state machine untouched until return, as Table B.7 requires. The test gap on that is F1.
- **UNCLEAN `Tests`** - F1 and F3 are open. Everything else is reproduced, as listed in the table above.
- **UNCLEAN `Docs`** - F2 and F3 are open; R1-R3 are residue only. Checked clean:
  - `AREA_BUDGET.md` and `234_PP_SHADOW_AREA_BASELINE.md` match the record exactly (`receipts/docs_vs_record.log`).
  - `KL_maap.md` and the firmware README describe the head's behaviour.
  - No page still describes a closed deviation as open.
  - Static docs gates are green.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_maap.sv` (whole), `milan_datapath.sv:7168-7190`, Annex B B.1-B.4 and Tables B.7-B.10, issue #696 acceptance and five rulings, `MAAP_FABRIC.md`, `maap_ceiling.log` | R559-1 | `030eb98a12685a2ca41cf8d785bb0eb69dc32a98` |
| RTL | CLEAN | `KL_maap.sv` diff `6aa25dec..HEAD`, datapath integration lines, `KL_pp_maap_shim.sv:225-270`, route-query reports, lint receipt, `lfsr_period` receipt | R559-1 | `030eb98a12685a2ca41cf8d785bb0eb69dc32a98` |
| Robustness | CLEAN | `sim_main.cpp` M5/M6/M7/M8 sections, unit log, campaign rows, RTL reset/priority paths | R559-1 | `030eb98a12685a2ca41cf8d785bb0eb69dc32a98` |
| Tests | UNCLEAN (F1, F3) | `sim_main.cpp`, `sim_integration.cpp`, `mutants.py`, `Makefile`, `integration.mk`, differential sources, campaign/plant/coverage/differential receipts | R559-1 | `030eb98a12685a2ca41cf8d785bb0eb69dc32a98` |
| Docs | UNCLEAN (F2, F3) | `MAAP_FABRIC.md`, `KL_maap.md`, `sw/firmware/ctrl/maap/README.md`, `AREA_BUDGET.md`, `234_PP_SHADOW_AREA_BASELINE.md`, `MARK_II_AREA_PLAN.md`, `docs/findings/README.md`, `FR_NFR.md:167`, static docs receipts | R559-1 | `030eb98a12685a2ca41cf8d785bb0eb69dc32a98` |

## Real limits

- No Vivado run here. The endpoint, route-query and MAAP OOC figures are the author's published receipts. I checked them by input-hash equality to this head, by byte equality of the recorded JSON, and by `check-baseline`; I did not re-measure them.
  The per-corner timing table in the #234 page cites corner reports that the evidence lists as scratch-only (`SCRATCH-ARTIFACTS.json`), so it is not verifiable from public receipts.
- I did not run the parent suite bank, the Yosys bank, the parser gate (no Vivado here), behaviour, the firmware RV32 bank, or field campaigns. For those I rely on the author's merge-result receipts:
  - 61/61 suites and 2,185,905 checks;
  - focus bank 11/11 steps rc 0. The bank driver's own rc of 1 comes from its dirty-tree guard: the field campaign rewrites two generated timestamp lines, which the REVIEW READY comment discloses.
- No manager source bank ran at this head, and none is claimed or inferred. Physical calibration was NOT RUN. Field-campaign skips are not hardware proof. No bench or hardware work was done.
- The hosted snapshot (UTC 2026-10-10T03:06:59Z) is mid-run: 12 check runs completed with success, 1 skipped (`Physical gPTP`, a conditional skip), 7 in progress. No aggregate contexts had been emitted yet. This is not acceptance evidence (`receipts/hosted-snapshot-summary.txt`).
- The datapath plants were applied by editing `milan_datapath.sv` in the clone, one at a time, and restored. The restore is verified in `receipts/restore.log`.

## Pending manager duties

- F1-F3 fixed on the branch, then a re-review that applies `Tests` and `Docs` at the new head. Any commit touching `KL_maap.sv` or the harness also un-covers `Conformance`, `RTL` and `Robustness` for that scope.
- R1-R3 carried to the residue checklist.
- The current-dev candidate merge on live dev `aef7ac66` (builder and native banks), with its receipts linked on the PR. The source base is `6aa25dec`.
- Hosted contexts and the local replica accepted on the exact final head.
- Acceptance 4 (bench interop with the reference peer) in the post-merge bench lane. Post-merge containment.

R559-1 FINISHED
