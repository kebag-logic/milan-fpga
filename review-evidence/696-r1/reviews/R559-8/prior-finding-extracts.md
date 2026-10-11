Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093137183
[R558] NEGATIVE - exact head 030eb98a12685a2ca41cf8d785bb0eb69dc32a98

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



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093167069
[R559] NEGATIVE - exact head 030eb98a12685a2ca41cf8d785bb0eb69dc32a98

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



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093606049
[R558] POSITIVE - exact head f909d6c460344527f102f24b8e7a77f09959e755

## 2. Round-1 findings: resolution at this head

| Finding | Required outcome | State at `f909d6c4` | Evidence |
|---|---|---|---|
| R559-1-F1 (Tests) | An M5 check holds the port down longer than a walk; the drop causes no restart or PROBE; the fresh walk starts after the rise; the falling-edge plant fails that named check in the default campaign | **Resolved** | See note 1 below the table. |
| R558-1-F1 (Docs) | `MAAP_FABRIC.md` states the merge-result figure and attributes 441/340 | **Resolved** | See note 2 below the table. |
| R559-1-F2 (Docs) | Plan "current record" figures and the gate row follow the re-record | **Resolved** | See note 3 below the table. The remaining baseline wording is R558-2-R1. |
| R559-1-F3 (Docs, Tests) | Both texts name `02:00:00:00:00:00` with clock 0 | **Resolved** | See note 4 below the table. |
| R559-1 residue R1-R3 | Wording | Applied | `MAAP_FABRIC.md:143`, `:36` and `:137-138`; `docs/findings/README.md:25` |
| R558-1-S1 (suggestion) | Optional | Applied | `MARK_II_AREA_PLAN.md:56` |
| R559-1-S1..S4 (suggestions) | Optional | Not applied; the reasons are in REVIEW READY | No lens effect |

Notes on the four resolved findings:

1. **R559-1-F1.** The new check is at `sim_main.cpp:68-71,763-803,974` and the campaign row at `mutants.py:70-72`.
   - R559-1's patch, applied verbatim, gives 172 checks and 1 failure: only `M5 B.3.5.9 link loss is no event; return reprobes`. The harness exits 1.
   - The same plant against the `030eb98a` harness gives 171 checks and 0 failures. So the new check is what closes the gap.
   - The default campaign row `m5_restart_on_link_loss` exits 1 at that check.
2. **R558-1-F1.** `MAAP_FABRIC.md:143-148` now gives:
   - 441/340 at `39571196`;
   - 445/340 at merge result `0df48637`, which is +6/+60 against `6aa25dec`;
   - dev `8b61b709` at 443/280, so the lane share is +2/+60.

   I checked the arithmetic. The figures equal the round-1 receipts that R558-1 quoted.
3. **R559-1-F2.** `MARK_II_AREA_PLAN.md:110-141` has 22 rows and 66 figures, with 0 differences against the `pp_resource_baseline.json` scopes at this head. At `030eb98a` the route column differed in 18 rows. For the gate row at `:56`:
   - 0.114 - 0.030 = 0.084, which is less than 0.25, so the floor binds first;
   - the floor (0.03) and the tolerance (0.25) were read from the record.
4. **R559-1-F3.** The fixture is named correctly at `MAAP_FABRIC.md:227-229` and `sim_main.cpp:9,58-59,645-646`.
   - With `realtime_ns_i=0` (`sim_main.cpp:228`) the low 32 bits sum to 0, so the fallback is exercised.
   - Both `zero_seed_freezes_*` defects are still caught.


## 3. Findings

### R558-2-R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:66-67`, `:317`, `:970` - baseline sentences still point at the live record file as if it held the #645/#647 record

- **Evidence:**
  - `:66-67` says "Source: `pp_resource_baseline.json`, all three `record` objects. Each `measured` note identifies `a5ca6e51...`". The link resolves to the file at this head. There, every `measured` note now identifies `0df48637`, and the route figures are #696's.
  - `:317` says "The current ledger starts from the committed 50,267 record".
  - `:970` names "current three-endpoint record".
- **Why this is residue and not a finding:**
  - Every figure in those sections is correct for the baseline they describe.
  - `:110-111` says explicitly that only the route figures changed, and that the levers and ledger keep the baseline's figures.
  - Correcting the sentences changes no figure, verdict, test or clause claim.
- **Exact fix:**
  - `:66`: "Source: the three `record` objects of [`pp_resource_baseline.json`](https://github.com/kebag-logic/milan-fpga/blob/d5f938dde2fb346602530435e4556ad54c6bcaec/review-evidence/696-r1/reviews/R558-2/../../syn/ooc/pp_resource_baseline.json) as stored at dev `5603c353`; #696's record has since replaced them (see [Current processor inventory](#current-processor-inventory))."
  - `:317`: "The [current ledger](#ledger) starts from the 50,267 route figure of the #645/#647 record."
  - `:970`: "Adopted processor pin and the #645/#647 three-endpoint record".
- **Verification:** reread the three lines, then run `docs_check.py`, `gen_toc.py --check` and `check_em_dash.py`.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093655306
[R559] POSITIVE - exact head f909d6c460344527f102f24b8e7a77f09959e755

## Findings of this round

### R559-2-R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:66-67` - baseline source line points at the live record file

- **Evidence:** the dated section "Baseline recorded on dev `5603c353`" says "Source: `pp_resource_baseline.json`, all three `record` objects. Each `measured` note identifies `a5ca6e51…`".
  - Its figures and input SHA-256 values equal the record as committed at `5603c353`, which is byte-equal to the pre-#696 record (`receipts/markii_baseline_section_vs_records.log`).
  - The linked file at this head now holds #696's record, measured at `0df48637`.
  - The section heading dates the baseline, and `:110-113` now say the current record differs, so no figure, measurement or gate claim is affected. This is wording only.
- **Exact fix:** replace "Source: [`pp_resource_baseline.json`](https://github.com/kebag-logic/milan-fpga/blob/dc9f94d21fe4329ced8db3f12987551597faf22f/review-evidence/696-r1/reviews/R559-2/../../syn/ooc/pp_resource_baseline.json), all three `record` objects." with "Source: [`pp_resource_baseline.json`](https://github.com/kebag-logic/milan-fpga/blob/dc9f94d21fe4329ced8db3f12987551597faf22f/review-evidence/696-r1/reviews/R559-2/../../syn/ooc/pp_resource_baseline.json) as committed on dev `5603c353`, all three `record` objects; #696 has since re-recorded the file (see [Current processor inventory](#current-processor-inventory))."

No BLOCKER, MAJOR or MINOR finding.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6095037677
[R558] NEGATIVE - exact head b9b389611304850ea435b2056887568afe5e6bf4

## 3. Findings

### R558-3-F1 - BLOCKER - Conformance, Robustness, Tests - `tb/verilator/maap/integration.mk:8`, `:15` - the nested captures still collect directory lines on the hosted make; shard 1/5 fails at this head

- **Authority:**
  - Issue #696 acceptance 2 asks for a datapath-level check showing that the MAC changes the intervals, with planted defects. Its rows are `m4_datapath_clean`, `m4_reset_time_sampling`, `m5_datapath_ignores_link` and `m3_datapath_ignores_clock`.
  - AGENTS.md section 7 requires exact-head `verilator-suites` evidence on an RTL/tooling PR head.
  - This commit's stated purpose is to answer hosted run 38021886237.
- **Evidence:**
  - Hosted job 114140492769 at `b9b38961` concluded failure: `maap` has 4 in-suite failures. All four integration rows stop at `integration.mk:13 ... non-files: make[2]:` (`receipts/hosted-b9b38961-shard1-maap-excerpt.log`).
  - GNU Make 4.3 reproduces it only under inherited `w` together with a `-j8` recursive parent. There, the `$(shell)` child cannot use the jobserver and warns. Its stdout still carries `make[1]: Entering directory '<start dir>'` and `make[1]: Leaving directory '<-C dir>'`, although `--no-print-directory` is on its command line (`receipts/make43-probe.log`).
  - The same file passes under GNU Make 4.4.1 in every context, which is why the local campaigns pass.
  - Clearing the inherited flags for the capture removes the pollution under 4.3 and the integration builds and passes (`receipts/make43-build.log`). That is the pattern `pp_shadow/Makefile:107`, `milan_dp_mclk/Makefile:62,70` and `milan_dp_render/Makefile:86,91` already use; `milan_dp_mclk/Makefile:44-54` records why.
- **Impact:**
  - The mandatory hosted `verilator-suites` gate is red at this head.
  - The acceptance-2 datapath check and the M5/M3 datapath plants cannot be graded on the hosted runner. Locally they pass only because the local make differs.
  - The failure is loud, not a false pass: the guard names it.
- **Required outcome:** under the hosted runner's GNU Make 4.3, the derived source list and flag list carry only the datapath suite's own output. This must hold when the capture runs inside the recursive `-j` parent that `mutants.py` creates, with `w` inherited.
  - One way to get there is the sibling suites' `MAKEFLAGS=` prefix on both captures.
  - If inherited flags are cleared, decide how the job bound that `mutants.py` passes as `VERILATOR_JOBS=` reaches `print-dp-vflags`. Today it travels in `MAKEFLAGS`.
  - Keep the guard.
- **Verification:**
  - Hosted Verilator shard 1/5 and `verilator-suites` green at the corrected exact head, with `== maap mutants: checks: 52 failures: 0 ==` in the `suite-logs-1` maap log.
  - Locally, `scripts/make43_probe.sh` and `scripts/make43_build.sh` from this packet, with a GNU Make 4.3 binary: the head variant is clean in all four contexts, and the head `integration-build` gives rc 0.
  - A cold reviewer re-applies Conformance, Robustness and Tests at that head.

### R558-3-S1 - SUGGESTION - Robustness, Tests - `tb/verilator/maap/integration.mk:11-13` - the guard tests existence, not "file", and accepts an empty list

- **Evidence:** `$(wildcard)` matches directories. An injected `../milan_dp` passes, and so does an empty list (`receipts/derive-probe.log` §4).
  - The commit subject says "refuse non-file entries".
  - Both cases still fail at elaboration (`receipts/dir-empty-probe.log`, Verilator exit 1), and `mutants.py:165-168` counts a compile failure as escaped. So neither can produce a false pass.
- **Optional outcome:** refuse a directory entry and an empty list with the guard's own message.
- **Verification:** the §4 probes stop at the guard.

### R558-3-S2 - SUGGESTION - Tests - `tb/verilator/maap/mutants.py` - no in-suite arm builds the integration in the hosted shape

- **Evidence:** `capture_coherence/mutants.py` has an inherited-`MAKEFLAGS=w` arm. The maap campaign has none.
  - F1 also shows that `MAKEFLAGS=w` alone, on GNU Make 4.4.1, does not reproduce the hosted defect.
- **Optional outcome:** a regression row that builds the integration from a `-j` recursive parent with `w` inherited.
  - It is useful mainly on a GNU Make 4.3 host. The hosted shard already exercises that shape on every rtl-full run.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6095122585
[R559] NEGATIVE - exact head b9b389611304850ea435b2056887568afe5e6bf4

## Findings

### R559-3-F1 - BLOCKER - Tests, Robustness, Conformance - `tb/verilator/maap/integration.mk:8`, `:15` (with `:12-14`) - the derived source list is still polluted on the hosted toolchain; the datapath mutant arm never builds

- **Authority/evidence:**
  - AGENTS.md section 7 requires exact-head `verilator-suites` evidence; at this head it is a failure.
  - Issue #696 acceptance 1 requires planted defects caught by suite checks.
  - Acceptance 2 requires a datapath-level check showing that different MACs draw different intervals. In the suite, that check runs only as the campaign's `m4_datapath_clean` case.
  - Hosted shard 1/5 at `b9b38961` reports `maap mutants: checks: 52 failures: 4`, with all four datapath cases refused at `integration.mk:13` naming `make[2]:`. The exact-head make 4.3 reproduction and the minimal case show the cause. Under GNU make 4.3, a nested make inheriting a print-directory flag plus an unusable jobserver writes `Entering/Leaving directory` to stdout around its jobserver warning, and `--no-print-directory` does not suppress it.
  - The commit's validation used make 4.4.1, which never takes that path. So `MAKEFLAGS=w make -C tb/verilator/maap` passing locally (`receipts/w2.log`) does not show that the hosted condition is fixed.
- **Impact:** the campaign is the only place the real-datapath harness runs, so the required hosted gate cannot show M3, M4 or M5 being killed at datapath level, or the acceptance-2 datapath check passing. `verilator-suites` is red at the exact head, and every later PR head that keeps this derivation will fail the same way. The guard makes the failure explicit, which is an improvement over `f909d6c4`, but it does not let the campaign run.
- **Required outcome:** the datapath arm builds and passes under the hosted invocation chain on GNU make 4.3: `run_all_suites.sh` → `make -C tb/verilator/maap` → `mutants.py` `make -j8 -s -C … integration-build` → `$(MAKE) -f integration.mk`. The derived source and flag lists must not depend on flags inherited from the caller. For reference only, not as a prescribed design: clearing inherited flags on the nested call, as `pp_shadow`, `milan_dp_mclk` and `milan_dp_render` already do, passed this chain in a disposable probe (`receipts/chain43_makeflags_probe.log`).
- **Verification:**
  1. Hosted Verilator shard 1/5 reports `PASS maap`, and `verilator-suites` succeeds at the new exact head.
  2. Locally at that head, a GNU make 4.3 run of `make -C tb/verilator/maap` with stdout to a file gives 172/0 and 52/0, with all four datapath cases `[ok]`.
  3. `scripts/minimal_jobserver_leak.sh`-style evidence, or the act replica, shows the inherited-jobserver case is covered. A regression check that runs under make 4.3 with `w` plus an inherited jobserver would keep this from returning.

### R559-3-S1 - SUGGESTION - Robustness - `tb/verilator/maap/integration.mk:12-14` - the guard admits directories and an empty list

The commit subject says it refuses "non-file entries", but `$(wildcard)` also returns directories. A directory word (`../milan_dp`) passes the guard (115 words), and so does an empty derived list (0 words); see `receipts/guard_probes.txt`. Both still fail closed later: Verilator rejects a directory (`receipts/directory_entry_fails_closed.txt`), and an empty list cannot elaborate `milan_datapath`. So this changes no outcome, only the diagnostic. Optional: also refuse directories and an empty list, so the refusal names the problem at derivation time.

### Observation for the manager, not a finding against this PR

`tb/verilator/capture_coherence/Makefile:101,105` uses the same `--no-print-directory`-only capture. Its hosted runs pass today. If its parse-time captures ever run under an inherited print-directory flag plus a `-j` jobserver on make 4.3, it is exposed to the same mechanism. AGENTS section 4 routes this to a separate public Issue if the manager judges it worth tracking.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6095865153
[R558] POSITIVE - exact head 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f

## Findings

### R558-4-R1 - RESIDUE - Docs - PR #706 body, "Status" and "How to get into the same state" - the stated head is two commits stale
- **Evidence:** the body says "review ready at `f909d6c4…`" and `git rev-parse HEAD   # f909d6c460344527f102f24b8e7a77f09959e755`. Its review-round table ends at round 2. The branch tip is `30073ee9`, which adds `b9b38961` and `30073ee9` (both `integration.mk` only). A cold reviewer who follows the recipe gets a mismatching hash.
- **Impact:** the fix is wording only. No figure, count, command, measurement or verdict in the body changes, because 172 / 3 / 52 rows hold at this head.
- **Exact fix:**
  - Replace both `f909d6c460344527f102f24b8e7a77f09959e755` occurrences with `30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f`.
  - Add a round-3 row: "R558-3-F1 / R559-3-F1 (Conformance, Robustness, Tests): the two datapath derivations clear inherited make flags and pass the job bound explicitly; an empty list is refused | `b9b38961`, `30073ee9`".
- **Verification:** read the PR body.

### R558-4-S1 - SUGGESTION - Robustness, Tests - `tb/verilator/maap/integration.mk:19-21` - a directory entry still passes the non-file guard
`$(wildcard)` matches directories (`receipts/directory_entry_probe.log`). An empty list is now refused. A directory in the list would still fail loudly at Verilator elaboration, not silently. This is optional and carries over the directory half of R558-3-S1.

### R558-4-S2 - SUGGESTION - Docs - `tb/verilator/maap/integration.mk:8-10` - the comment could name the trigger exactly
The comment says the leak happens "under an inherited w flag inside a recursive -j parent". On GNU Make 4.3 the leak needs both an inherited `w` and a jobserver advertised to the capture but unavailable there. The hosted log shows the `jobserver unavailable` warning. With a working jobserver (w+j8 locally) the old form does not leak (`receipts/leak_control.log`, `make43_probe.log`). Naming the jobserver condition is optional. The fix is right for either reading.

### Observation (no finding)
- **Job bound defaults:** `integration.mk:5` (`VERILATOR_JOBS ?= 2`) is now live. A direct `make integration-build` with no bound builds the datapath with `-j 2`, where it used to get the datapath suite's `-j 0`. `mutants.py:166` always passes `VERILATOR_JOBS` (default `0`), so the campaign and hosted behaviour are unchanged. The bound only affects compile parallelism.
- **Other cleared overrides:** clearing MAKEFLAGS also drops the other command-line overrides. Callers pass `MAAP_RTL`, `MDIR` / `DP_MDIR` and `VERILATOR`, and none of these feeds the two print targets (`milan_dp/Makefile:83-101,648-664`). The byte-identical equality probe confirms this.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6095881954
[R559] POSITIVE - exact head 30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE at this head.

### R559-4-S1 - SUGGESTION - Robustness, Tests - `tb/verilator/maap/integration.mk:19-21` - the non-file guard still admits a directory entry (retains the directory half of R558-3-S1 / R559-3-S1)

- **Evidence:** `$(wildcard)` matches directories. In a disposable tree, a `print-srcs` that names `adir`, `real.sv adir` or `../milan_dp` passes the guard under make 4.3 and under 4.4.1. Parsing ends normally and the run stops only at the recipe's first line (`receipts/dir-entry-probe.log`). The empty and blank cases now stop at `integration.mk:17: *** datapath source list is empty.` (`receipts/flags-guard-probe.log`).
- **Impact:** none on verdicts. A directory in the list fails at elaboration, and `mutants.py:165-168` counts a compile failure as escaped, so this cannot produce a false pass. The cost is a less direct diagnostic.
- **Optional outcome:** refuse directory entries at the guard, with its own message.
- **Verification:** the three directory cases in `scripts/dir_entry_probe.sh` stop at the guard.

### R559-4-S2 - SUGGESTION - Tests - `tb/verilator/maap/mutants.py` - no in-suite arm reproduces the hosted make 4.3 shape (retains R558-3-S2)

- **Evidence:** the hosted defect needs a make 4.3 that sees an inherited print-directory flag and an unusable jobserver (`receipts/jobserver-ab.log`). On a 4.4.1 host, the inherited-`MAKEFLAGS=w` suite run cannot show it.
- **Impact:** a local 4.4.1 run cannot catch a regression of this fix. The hosted shard exercises the real shape on every rtl-full run, and it is now green.
- **Optional outcome:** a regression row that builds `integration-build` under an inherited `w` plus an unusable `--jobserver-auth`, which is meaningful on a make 4.3 host.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097253076
[R558] NEGATIVE - exact head 87d51e76972de36be477844a39182da8a122a5eb

## Findings

### R558-5-F1 - MINOR - Docs - `docs/design/AREA_BUDGET.md:368`, `docs/design/MARK_II_AREA_PLAN.md:653-654` - after the merge, M0s's step-1 status still names the #645 50,267-LUT route as the accepted comparison record

- **Authority/evidence:**
  - At the candidate, `pp_resource_baseline.json` records `route-1x1` LUT = 50230 (#696, merge result `0df48637`).
  - `AREA_BUDGET.md:129` says "The table is the gate's record", and its table at `:122` gives 50,230.
  - `MARK_II_AREA_PLAN.md:110` names #696's re-baseline as "the gate's current record".
  - On the same pages, the M0s text reads:
    - `AREA_BUDGET.md:368`: "The accepted 50,267-LUT route remains the comparison record."
    - `MARK_II_AREA_PLAN.md:653-654`: "The last accepted gate record remains unchanged. Its 50,267 LUTs and 74/27 RAM primitives remain comparison anchors."
  - `AREA_BUDGET.md:354` and the recipe page require D7 and the selected routes to compare against "the last accepted gate record" and "the accepted `route-1x1` record". At the candidate, the gate compares against 50,230.
  - Both sentences come from dev `e8454e27`, where they were true. They are absent at source `30073ee9` (`receipts/f1_evidence.txt`). The merge alone makes them false.
  - The manager's composition criterion asks that every figure and record identity on both pages match the recorded file at the candidate.
- **Why MINOR and not RESIDUE:** both sentences make a claim about a figure and a record's identity: which record is the gate's comparison anchor, and its LUT count. They are not baseline-scoped sentences. That differs from R558-2-R1 / R559-2-R1, where every figure was correct for a baseline the page explicitly retains (`MARK_II_AREA_PLAN.md:110-113`). Here the sentences name the *gate* record. A later M0s or D7 lane following them would report its delta against 50,267 while the gate judges against 50,230, a 37-LUT and 105-FF difference.
- **Impact:** the merged pages contradict themselves about the current acceptance record, and the text that steers the next measurement lane points at a superseded record. No gate detects this; all 32 documentation and resource gates pass.
- **Required outcome:** at the merged head, each sentence either names #696's record as the comparison record (50,230 LUTs, 74/27, 87.5 tiles unchanged) or is explicitly dated to the `7c1b52be` base. Neither may claim the gate record is unchanged or is 50,267. One fix that keeps every other M0s claim:
  - `AREA_BUDGET.md:368`: "At base `7c1b52be` the comparison record was #645's 50,267-LUT route; [#696](https://github.com/kebag-logic/milan-fpga/issues/696)'s 50,230-LUT route has since replaced it."
  - `MARK_II_AREA_PLAN.md:653-654`: "At that base the last accepted gate record was #645/#647's 50,267 LUTs and 74/27 RAM primitives. [#696](https://github.com/kebag-logic/milan-fpga/issues/696) has since re-recorded it at 50,230 LUTs with 74/27 unchanged; that record is the comparison anchor, and the ledger keeps the baseline figures."
- **Verification:**
  - `git grep -n "50,267" -- docs/design/AREA_BUDGET.md docs/design/MARK_II_AREA_PLAN.md` shows no sentence that calls 50,267 the current, last accepted or comparison gate record.
  - `python3 -I check_figures.py <tree>` exits 0 (this packet).
  - `docs_check.py`, `gen_toc.py --check`/`--verify-anchors` and `check_em_dash.py --base <parent>` exit 0, plus `pp_resource_gate.py check-baseline`.

### R558-5-R1 - RESIDUE - Docs - `docs/design/AREA_BUDGET.md:359,376`, `docs/design/MARK_II_AREA_PLAN.md:666` - lane-scoped "records are unchanged" lines now sit beside #696's re-record

These three M0s sentences ("Acceptance records and policy values remain unchanged." / "Acceptance records, schema and policy are unchanged." / "The acceptance schema, thresholds and records are unchanged.") are true of the M0s change, and their paragraphs make that the subject. On the composed pages, a reader could take them as page-wide. This is wording only: no figure or record identity is stated. Exact fix: prefix each with "M0s changes no", e.g. "M0s changes no acceptance record, schema or policy value." Verification: reread the lines, then run `check_em_dash.py --base <parent>` and `docs_check.py`.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097443587
[R559] POSITIVE - exact head 6de3904ec2d6b2f04325c94c7686519ecd92a202

## Findings of this round

### R559-5-S1 - SUGGESTION - Tests, Docs - `docs/design/AREA_BUDGET.md:122-127,368`, `docs/design/MARK_II_AREA_PLAN.md:110-141,653-654` - no repository gate ties the area pages' record sentences to the recorded file

- **Evidence:** I built a disposable probe tree and made two plants:
  - restore dev's "The accepted 50,267-LUT route remains the comparison record." at `AREA_BUDGET.md:368`;
  - put 50,267 back at `MARK_II_AREA_PLAN.md:654`.

  `docs_check.py` still reports 0 findings (`receipts/probe_docs_check_on_mutated_text.txt`). The reviewer-side figure check fails each plant (`receipts/probe_revert_368.txt`, `receipts/probe_revert_654.txt`).
- **Impact:** none at this head; all figures match. A future merge that composes stale record text, as R558-5-F1 found, is caught only by review.
- **Optional outcome:** a docs-gate arm that compares the record-table and comparison-record figures with `syn/ooc/pp_resource_baseline.json`.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097490649
[R558] NEGATIVE - exact head 6de3904ec2d6b2f04325c94c7686519ecd92a202

## 2. Findings

### R558-6-F1 - MINOR - Conformance, RTL, Robustness, Tests - `hdl/ieee1722/maap/KL_maap.sv:306-308` (with `:146-149`, `:172`, `:352-355`); `tb/verilator/maap/sim_integration.cpp:129-141`; `tb/verilator/maap/sim_main.cpp:903-953` - the first Begin! address draw uses the raw low 16 seed bits and is graded by no check

- **Authority:**
  - Issue #696 M4 (B.3.4 NOTE, B.3.6.1) records the defect as: "every shipping station seeds `0xACE1` and the station MAC never enters the draws".
  - M3 (B.3.6.1) asks for a generator "seeded from the MAC and the real-time clock". B.3.6.1 is generate_address, the address-range draw.
  - Acceptance 1: "Each item is either conformed, with a suite check and a planted defect, or justified by clause in MAAP_FABRIC.md."
  - `KL_maap.md:5` states: "Randomness uses a 32-bit LFSR with period 2^32 - 1 (offset choice + interval draws). First enable samples the low 32 bits of the programmed MAC plus the local real-time clock."
  - Table B.7 note b judges a conflict by range overlap.
- **Evidence at this head:**
  - At first enable, `new_off_w = rand_offset(enable_seed_w[15:0], count_i)`, which folds the sum `mac[31:0] + clock` and uses only its low 16 bits (`:307-308`). The first probe re-arm then reads `lfsr_r[5:0]` of that same seed (`:172`, `:353`). No generator step separates the seed from either first draw.
  - Probe `scripts/first_draw_probe.cpp` (`receipts/first_draw_probe.log`) runs the head RTL with equal reset/enable timing and an equal clock:

    | MAC pair | First offsets | First probe intervals (cycles) | 8-address blocks |
    |---|---|---|---|
    | `02:00:00:00:00:01` / `02:00:00:00:00:02` | 0x0001 / 0x0002 | 5190 / 5200 | overlap |
    | `02:00:00:00:00:01` / `02:00:00:01:00:01` | 0x0001 / 0x0001 | 5190 / 5190 | identical |
    | `02:00:00:0a:12:34` / `02:00:00:5b:12:34` | 0x123b / 0x123b | 5770 / 5770 | identical |
    | `02:00:11:00:12:34` / `02:00:22:00:12:34` | 0x1234 / 0x1234 | 5700 / 5700 | identical |

  - The committed datapath fixture shows the same thing on the real CSR path. With the stations' first-PROBE `requested_start` printed and nothing else changed (`scripts/sim_integration_offsets.patch`, `scripts/p7_offset_check.sh`, `receipts/p7chk_head.log`), MACs `…:01` and `…:02` claim 0x1447 and 0x1448: overlapping blocks. The check at `sim_integration.cpp:140` passes because it compares interval vectors only.
  - The firmware C core, the differential's reference, steps its xorshift32 before its first draw (`sw/firmware/ctrl/maap/maap.c:31-54,108`). Adjacent seeds therefore do not give adjacent first offsets there.
  - Planted defect p7 (`scripts/p7_first_offset_ignores_seed.patch`) restores the pre-#696 first-draw expression `rand_offset(lfsr_next_w[15:0], count_i)`. Every station then claims the same first block (0x7c4f in the datapath fixture; 0xc73c in the probe). It **escapes** the unit harness (172 checks, 0 failures) and the real-datapath harness (3 checks, 0 failures) (`receipts/probes.log`, `receipts/p7chk_p7.log`). The M3 seed check (`sim_main.cpp:939`) grades `lfsr_r` after enable, not the address drawn at that enable.
- **Impact:**
  - In M4's own scenario (identical boot timing), the two cases in the table above both collide on their first claim, which is the failure M4 set out to remove. Stations whose MACs agree in their last two octets claim the identical block. Adjacent MACs, the normal case within one vendor batch, claim overlapping blocks. compare_MAC resolves the collision with an extra walk, but M4 and B.3.6.1 seed from the MAC precisely so that this first draw differs.
  - Any regression of the first-draw seeding, including a literal revert of the pre-#696 expression, is invisible to the suite. Acceptance 1 is met for intervals and generator state, not for the address draw.
- **Required outcome:**
  1. A suite check, unit or datapath, grades the first Begin! range across equally timed stations. At minimum, different MACs (and, separately, different clocks) must give different first offsets. A planted defect equivalent to p7 must fail that named check in the default campaign.
  2. Either the first offset (and preferably the first interval) depends on the full 32-bit seed, so that MAC pairs which differ only in bits 16..31, or are adjacent, do not claim identical or overlapping first blocks under equal timing; or `MAAP_FABRIC.md` justifies, by clause and with a manager decision, that the first draw is the seed's low 16 bits and records the collision cases above. Option 1 needs combinational mixing or a stepped generator value, so LUTs only: the FF allowance is fully used, and the LUT side has 54 left against `6aa25dec`.
- **Verification:**
  - Rerun `scripts/reviewer_probes.py` (p7 rows must become CAUGHT), `scripts/first_draw_probe.cpp` (no identical or overlapping pair, if option 1 is taken) and the default MAAP target (unit, datapath and campaign, all rc 0).
  - If the RTL changes: OOC MAAP area against the ceiling, and the endpoint records per the recipe or a manager decision.

### R558-6-R1 - RESIDUE - Docs - PR #706 body, "Status", "How to get into the same state" and the review-round table - stale head (carries R558-4-R1 forward)

- **Evidence:** the body still says "review ready at `f909d6c4…`" and `git rev-parse HEAD   # f909d6c460344527f102f24b8e7a77f09959e755`. The branch is now `6de3904e`, which adds `b9b38961`, `30073ee9`, the merge of live dev `e8454e27` (`941ba746`) and `6de3904e`. Its round table ends at round 2.
- **Why residue:** no figure, count, command or verdict in the body changes at this head. Unit 172, datapath 3 and campaign 52 rows all reproduce here.
- **Exact fix:**
  - Replace both `f909d6c460344527f102f24b8e7a77f09959e755` with `6de3904ec2d6b2f04325c94c7686519ecd92a202`.
  - Add rows for round 3 ("R558-3-F1 / R559-3-F1: the datapath derivations clear inherited make flags and pass the job bound explicitly; an empty list is refused | `b9b38961`, `30073ee9`") and for the composition ("merge of dev `e8454e27` (`941ba746`); R558-5-F1: the M0s step-1 status names #696's record as the comparison anchor | `6de3904e`").
- **Verification:** read the PR body.

### Suggestions (optional; no lens effect)

- **R558-6-S1 - Tests - `KL_maap.sv:241-252,449`.** Probe p6 replaces the own-count snapshot `{8'd0, tx_own_cnt_r}` with live `count_i`, and it escapes (172/0). The documentation says reconfiguration during a frame is not protected (`MAAP_FABRIC.md:71-72`), so no claim is broken. A one-line check would keep the snapshot from regressing silently.
- **R558-6-S2 - Docs - `MAAP_FABRIC.md:104-111`.** The fabric engine keeps walking, with `addr_valid_o` held, through a link outage (ruled contract). The C core withdraws on link loss (`maap.c:226-243`, `withdraw()` publishes invalid). The protocol-processor engine treats link loss as Release! (`11_maap_engine.md:103,135-147`). One sentence naming this difference would warn a later placement switch (M0s F2) that the observable `addr_valid` behaviour during an outage changes.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6102796423
[R558] NEGATIVE - exact head d1b18b3fa0b476a9b534c88466b163e15f469004

## 3. Findings

### R558-7-F1 - MINOR - Tests - `tb/verilator/maap/sim_main.cpp:383-384`, `:389-391`, `:403-404`, `:419-421`, `:508-510`; `tb/verilator/maap/mutants.py:107-110` - the M2 requested_start check cannot fail for an echo of the overlap start

- **Authority:**
  - Issue #696 M2 (B.3.6.6): "DEFEND echoes the PROBE's requested start address and count".
  - Acceptance 1 requires a suite check and a planted defect for each conformed item.
  - `AGENTS.md` section 6, Tests lens: "Each new test can fail for the defect it claims to detect."
  - `docs/design/MAAP_FABRIC.md:65` states "Its requested_* fields echo the triggering PROBE (B.3.6.6)".
- **Evidence:**
  - The RTL stores `tx_defend_off_r <= rx_start_r` (`hdl/ieee1722/maap/KL_maap.sv:439`). The overlap start is `conf_start_w = max(rx_start_r, offset_r)` (`:250`).
  - requested_start is graded in four places:
    - `sim_main.cpp:383` (PROBE at `off0+4`);
    - `:404` (`off0+7`);
    - `:419-421` and `:508-510` (`off0+1`, `off+2`).
  - Every one of those PROBEs starts at or above this station's offset, so the PROBE's requested_start equals the overlap start.
  - The only fixture whose PROBE starts below the station's offset is `[4b]` at `:389-391`, at `off0-4`. Its DEFEND's requested_start is never read.
  - The campaign's M2 start plant, `m2_own_requested_start` (`mutants.py:107`), writes `offset_r`, which differs from `off0+4`. It does not cover the overlap-start variant.
  - Probe `q1_m2_echo_overlap_start` writes `conf_start_w` into `tx_defend_off_r`. It **escapes**: rc 0, 177 checks, 0 failures (`receipts/reviewer_probes.log`, `receipts/probes/q1_m2_echo_overlap_start.log`).
  - Adding one check to a scratch copy of the harness at `[4b]` (requested_start == pool | `off0-4`) gives:
    - clean RTL: 178 checks, 0 failures;
    - q1: 1 failure, at that check (`scripts/echo_gap_demo.sh`, `receipts/echo_gap_demo.log`, `receipts/echo_demo/`).
- **Impact:**
  - A plausible regression puts the conflict range's start into the requested_start field of every DEFEND whose prober's range begins below this station's block, which is a B.3.6.6 wire defect. The suite reports it green.
  - The value sits next to `tx_conf_start_r <= conf_start_w` (`KL_maap.sv:441`) and is one identifier away from it.
  - M2's acceptance 1 evidence holds for the own-offset defect class only.
- **Required outcome:**
  - A named M2 check reads the DEFEND's requested_start for a PROBE whose requested_start is below this station's offset.
  - A planted defect echoing the overlap start (`conf_start_w`) joins the default campaign and must fail that named check.
  - No RTL change is needed.
- **Verification:**
  - The default MAAP target is rc 0, with the new campaign row `[ok]` at its named check.
  - `scripts/reviewer_probes.py <clone> <work> q1_m2_echo_overlap_start` reports CAUGHT.

### R558-7-R1 - RESIDUE - Docs - `docs/design/MAAP_FABRIC.md:257` - the interval-check sentence names more pairs than the check grades

- **Evidence:**
  - The sentence says the "adjacent and bit 16..31 pairs" must give different first probe intervals.
  - The preceding sentences define the bits 16..31 set as all pairs differing only in bits 16..31. The check grades 139 of those pairs for disjoint blocks.
  - The interval check (`sim_main.cpp:1043-1061`, `:1076`) grades 52 pairs:
    - 33 adjacent pairs;
    - R558-6's three high pairs;
    - the 16 single-bit pairs in bits 16..31.
  - The property itself holds for every carry run (`receipts/fold_claims.log`, C5), so no design claim is wrong.
- **Why RESIDUE:**
  - The fix is prose only. It changes no test, code, figure, verdict or clause claim, and the PR body already states "52 first-interval pairs".
- **Exact fix:**
  - Replace "Clocks one power of two apart must give different first offsets, and the adjacent and bit 16..31 pairs different first probe intervals." with "Clocks one power of two apart must give different first offsets. The adjacent pairs, R558-6's pairs and the 16 single-bit pairs in bits 16..31 must give different first probe intervals."
- **Verification:** reread the line, then run `docs_check.py` and `check_em_dash.py`.

### Suggestions (optional; no lens effect)

- **R558-7-S1 - Tests - `KL_maap.sv:202`; `sim_main.cpp:1076`.** This extends the author's disclosed open risk.
  - Probe `q3_probe_fold_unstepped` folds `lfsr_r` instead of `lfsr_next_w` and escapes the suite (177/0).
  - Algebraically, the unstepped probe fold gives equal first probe draws for 3 of the 528 carry runs (`receipts/unstepped_fold.log`). The step therefore carries part of the guarantee at `MAAP_FABRIC.md:115`.
  - Either extending the interval check to all 528 carry runs or one golden first-interval value would grade it.
  - No clause requires distinct first intervals, so this stays optional.
- **R558-7-S2 - Tests - `KL_maap.sv:337-339`; `MAAP_FABRIC.md:110`.**
  - Probe `q4_every_begin_refolds` makes every Begin!, not only the first, re-fold MAC plus clock. It escapes (177/0).
  - The documented "later Begin! events draw the running generator" is therefore ungraded.
  - A check that two consecutive Release!/Begin! cycles at a frozen clock claim different offsets would grade it.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6102829355
[R559] NEGATIVE - exact head d1b18b3fa0b476a9b534c88466b163e15f469004

## 2. Findings

### R559-6-F1 - MINOR - Tests, Conformance - `tb/verilator/maap/sim_main.cpp:1073` (with `:1044-1046`, `mutants.py:71`); issue #696 assignment 6097504752 item 2 - the "bits 16..31" check is named for a property the head does not have, and the round-6 criterion it answers is unmet and needs a recorded narrowing

**Authority:**
- Assignment 6097504752 item 2: MACs "differing only in bits 16..31 must give non-identical, non-overlapping first blocks".
- AGENTS.md section 4: wrong or contradictory acceptance needs a public change request, not a private interpretation.
- AGENTS.md section 6 (Tests): each test can fail for the defect it claims to detect.

**Evidence at this head.** I ran my own first-claim harness (`scripts/first_offsets.cpp`) on the unmodified head RTL. Stations were reset and enabled on the same cycles at clock 0, count 8:

| MAC pair (differ only in bits 16..31) | First offsets | 8-address blocks | Receipt |
|---|---|---|---|
| `02:00:00:00:12:34` / `02:00:90:00:12:34` | 0xa074 / 0xa075 | overlap | `receipts/xval.log` |
| `02:00:01:80:12:34` / `02:00:ed:6f:12:34` | 0x0074 / 0x0074 | **identical** | `receipts/identical_pair.log` |

- A model of the RTL first draw reproduces the head harness on 202 stations (`receipts/xval.log`). On that model:
  - 513 first offsets are shared by more than one high half (`receipts/identical_pair.log`).
  - 14 of 65,535 high halves overlap one fixed MAC (`receipts/high_half_overlap.log`).
- This cannot be fixed:
  - 65,536 high halves map onto at most 65,017 offsets, so no count-8 draw makes all such pairs non-identical, let alone non-overlapping.
  - The author's open risk and the PR body say so: "no 16-bit draw can separate every pair".
- The check at `:1073`, "M4 B.3.6.1 MACs differing in bits 16..31 claim disjoint first blocks", still asserts that property. It passes because it samples 136 power-of-two-apart pairs (i ≥ 16) and three fixed pairs (`:1044-1046`).
  - The PR body and the REVIEW READY cite it as "139 pairs differing only in bits 16..31".
  - No published decision narrows the round-6 criterion to the power-of-two pairs that the RTL actually guarantees. The REVIEW READY lists the limit as an open risk, not as a requested change.

**Impact:**
- The suite's named evidence states a separation guarantee that the head violates for concrete MAC pairs, including M4's own failure mode: an identical first block under identical timing.
- A cold reader of the check list would conclude that the round-6 criterion is met as written.

**Required outcome:**
- Each first-draw check is named for what it establishes. For example, "MACs 2^i apart (i ≥ 16) claim disjoint first blocks", with the fixed pairs named as fixed pairs. Mutant anchors follow the rename.
- The manager publicly records the narrowed round-6 criterion: disjoint for seeds a power of two apart, and different words for any bits-16..31 difference. The other option is a different achievable criterion.

**Verification:**
- `grep` of the check names in `sim_main.cpp` and `mutants.py`.
- Campaign rc 0 with the renamed anchors.
- A link to the manager's narrowing comment.

### R559-6-F2 - MINOR - Tests, Docs - `docs/design/MAAP_FABRIC.md:112-116`, `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5`, `hdl/ieee1722/maap/KL_maap.sv:156-162`; checks `sim_main.cpp:1072-1074` - the documented universal first-draw guarantees have no check that can fail when they are lost

**Authority:**
- AGENTS.md section 6 Tests: "Each new test can fail for the defect it claims to detect".
- AGENTS.md section 6 Docs: "The PR and Issue contain enough evidence for another cold reviewer".

**Evidence:**
- The docs claim, for every seed:
  - two seeds a power of two apart, with any carry, claim disjoint first blocks of up to 8, "through the pool fold and the clip";
  - seed bits 16..31 map one-to-one onto the offset word.
- At the head both claims are true. My exhaustive check (`scripts/fold_proof.py`, `receipts/fold_proof.log`, rc 0) reads the constants from the RTL and confirms them:
  - all 528 carry runs × all 65,536 words × counts 1..8 are disjoint;
  - all 528 runs give different probe draws;
  - bits 16..31 are a bijection;
  - the 22 rows have rank 22.
- No artifact in the repository or the public evidence establishes these claims. The suite draws one random seed per carry run (`sim_main.cpp:1050-1063`, described at `MAAP_FABRIC.md:254-255`).
- Two planted fold-constant regressions show that the checks cannot fail when the claims are lost:
  - **q3** drops one bit of offset row 0 (`32'h0000_0081` to `32'h0000_0080`). The bijection breaks: 32,768 distinct words, with kernel `0x9000`. MACs `02:00:00:00:12:34` and `02:00:90:00:12:34` then claim the identical block 0xa074. The unit harness reports **177 checks, 0 failures** (`receipts/probes.log`, `receipts/q3_pair.log`, `receipts/xval.log`).
  - **q9** drops one bit of offset row 6 (`32'h8008_0040` to `32'h8000_0040`). Run 18..18 overlaps. MACs `02:00:17:a1:47:bb` and `02:00:17:a5:47:bb`, 2^18 apart, claim 0xfdf8 / 0xfdf3, overlapping blocks at the clip, where the head gives 0xfdf8 / 0xfdb3. The unit harness reports **177 checks, 0 failures** (`receipts/q9_pair.log`), although the check "M4 B.3.6.1 MACs 2^i apart claim disjoint first blocks" is named for exactly this.
  - A model search (`receipts/row_flip_search.log`) finds that 109 of the 512 single-bit row flips break a documented universal claim while every sampled suite pair still passes.

**Impact:**
- The central round-6 guarantee is protected only by sampling.
- A later edit of the fold constants, or of the pool mapping, can silently reintroduce first-claim collisions between equally timed stations.
- A cold reviewer cannot confirm the universal statements from public state without writing a proof.

**Required outcome:** one of the following.
- An executable check in the default MAAP target establishes the universal claims for the RTL's actual constants and fails for q3 and for q9. It may be exhaustive over carry runs and words through the pool fold and clip, plus the bits-16..31 bijection, at RTL or model level, provided the model is tied to the RTL.
- Or the universal statements at the three cited places are narrowed to what the suite establishes.

**Verification:**
- Apply q3 (anchor in `scripts/probes.py`) and q9 (the `32'h8008_0040` replacement above). Each must fail a named check.
- The default MAAP target stays rc 0.

### R559-6-R1 - RESIDUE - Docs - `docs/design/MAAP_FABRIC.md:116`; PR #706 body, "What the folds guarantee", third bullet - "always draw different words" omits that the pool fold can still give equal blocks

- **Evidence:** the head pair `02:00:01:80:12:34` / `02:00:ed:6f:12:34` draws different words but claims the identical block 0x0074 (`receipts/identical_pair.log`). The sentence is true but invites the stronger reading.
- **Exact fix:** append to both sentences: "; the pool fold can still map two such words onto one block, so their first blocks can coincide or overlap like any pair that is not a power of two apart."
- This is wording only. It changes no figure, check or claim.

### Suggestions (optional; no lens effect)

- **R559-6-S1 - Tests - `KL_maap.sv:202`.** Probe q1 replaces `probe_fold(lfsr_next_w)` with `probe_fold(lfsr_r)`, so the first probe interval comes from the unstepped seed. It escapes (177/0). The author disclosed this. A golden first-interval value for one seed would pin the generator step that the round-6 assignment asks for.
- **R559-6-S2 - Robustness, Tests - `KL_maap.sv:193-198, 337-339`.** Probe q8 replaces `count_i` in the Begin! draw with `8'd8` and escapes (177/0). No check drives a random draw into the pool-clip region with a count other than 8, and the M7 test (`sim_main.cpp:825-842`) reaches the clip only by chance. This gap predates #696, so it is a candidate for its own Issue.
- **R559-6-S3 - Tests.** Probe q5 makes every Begin! use the first-draw fold and escapes (177/0). The documented "later Begin! events draw the running generator's next low 16 bits" (`MAAP_FABRIC.md:110`) is not graded. Behaviour stays acceptable because the clock moves between enables.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6103750948
[R558] POSITIVE - exact head 32582421bbf095a7b5a7d4b953c4d737b86fe54b

## 3. Findings of this round

No BLOCKER, MAJOR, MINOR or RESIDUE.

### R558-8-S1 - SUGGESTION - Docs - `docs/testing/TESTING.md:606` - the suite-index row for `tb/verilator/maap` does not mention #696's real-datapath arm

- **Evidence:**
  - Since #696, the default `make` of this suite also builds `milan_datapath` through `integration.mk`.
  - It runs `sim_integration.cpp` as the clean datapath control and as five datapath plants (`mutants.py:191-208`, `DATAPATH_MUTANTS`).
  - The row still describes only the #686 shape: "every check grades an IEEE 1722-2016 Annex B clause, and `mutants.py` plants at least one defect per #686 item".
  - Some #696 checks, such as "M3 Release/Begin retains the generator sequence" and "M4 first-draw maps learned from the RTL are linear in the seed", grade a property rather than naming a clause.
- **Impact:** none on any verdict. A reader planning shard wall time would not learn from the index that this suite elaborates the full datapath.
- **Optional change:** add one sentence to the row, for example: "Since #696 its default target also builds the real `milan_datapath` CSR-to-MAAP path (`sim_integration.cpp`) and plants its M3, M4 and M5 datapath defects there."

### Reviewer probe observations (no new finding)

- **u1 (own requested_count follows live `count_i`).** This probe escapes. It is the same gap as retained **R558-6-S1**.
  - No contract is broken: `MAAP_FABRIC.md:71-72` leaves reconfiguration during a frame unprotected.
  - The 8-bit `tx_own_cnt_r` snapshot (`KL_maap.sv:272,282,480`) is part of the +60 FF that fully uses the MAAP FF allowance.
  - Either a check or dropping the snapshot remains optional.
- **Caught probes:**
  - Beat-4 acceptance (`u2`) and a one-byte conflict_count requirement (`u3`): both M8 checks.
  - Link return ignored while probing (`u4`): M5.
  - Count echo losing its high byte (`u5`): M2 and M6.
  - Reseeding at every Begin! (`u6`): M3 continuity and the probe-draw range.
  - A pending DEFEND surviving link return (`u7`): M6.
  - A link return counted as a conflict (`u8`): M5.
  - The generator not loaded with the seed (`u9`): M3/M4, eight checks.
  - The datapath tying `port_operational_i` high (`d1`): M5 datapath.
  - The datapath feeding PHC bits 63:32 (`d2`) or zero (`d3`): both M3 datapath checks.


## 5. Lens results (same format as findings)

- `[R558] PASS Conformance - KL_maap.sv:146-154,163-178,202,222-225,281-282,315-339,383-386,402,424-425,432-443,464-471; milan_datapath.sv:7171-7172; issue #696 acceptance 1-3 and comment 6102832618`
  - Each item was checked against its cited clause, as the issue states it:
    - M4: seed at first enable from the programmed MAC plus PHC; the datapath check and its reset-time plant are in the default campaign.
    - M2: requested_start and all 16 count bits are echoed (B.3.6.6).
    - M7: a supplied range must lie inside 0..0xFE00, with the boundary kept (Table B.9).
    - M8: truncation or a missing keep strobe through byte 41 is discarded with no effect (B.2); counting is withdrawn by ruling and recorded at `MAAP_FABRIC.md:186-188`.
    - M1: compare_MAC in the rProbe!/PROBE and rDefend!/DEFEND cells (Table B.7 note d).
    - M5: a rising `eff_link_w` revokes and re-probes, and a falling one is no event (B.3.5.9).
    - M6: one shared response buffer; its capacity limit is justified at `MAAP_FABRIC.md:171-185`.
    - M3: a 32-bit generator `x^32+x^22+x^2+x+1` with period 2^32-1, checked from the RTL map. The pool-fold bias is justified at `:158-170`.
  - The recorded separation criterion holds for every seed (independent model).
  - Acceptance 3: MAAP 490/340, +51/+60, within the ceiling; three records re-written with `check-baseline` PASS.
  - Acceptance 4 is not this lane's.
- `[R558] PASS RTL - KL_maap.sv:137-203,248-253,268-276,341-507; milan_datapath.sv:2934-2935,3000-3001,7168-7178; receipts/lint.log`
  - The new inputs are synchronous to `axis_clk`: the PHC is on `gtx_clk == axis_clk`, and `eff_link_w` is already consumed synchronously at `:3589-3615`.
  - Every new flop has a synchronous reset value (`:349-373`).
  - The 17-bit range ends cannot overflow, and the `seed_end_w` and `req_end_w` widths are correct.
  - In priority order (disable, Restart!/PortOperational!, DEFEND, timer), `save_probe_w` and `defend_w` are mutually exclusive, and the pending buffer is cleared on every allocation loss.
  - The first draw's added logic is in the recorded route with +3.906 ns incoming slack (`234_PP_SHADOW_AREA_BASELINE.md:34-108`).
  - Lint stays at 90 <= 90. There is no register-map, filter or mailbox change; the datapath diff since `e8454e27` is two port connections and one comment.
- `[R558] PASS Robustness - sim_main.cpp:781-941; receipts/reviewer_probes.log (u2-u5,u7,u8); receipts/fold_model.log (zero-sum pairs)`
  - Exercised and passing:
    - truncated lengths 1..41 and every single missing byte 0..41 for each message type, cycle-matched against idle RX;
    - reset, disable, link return and conflicting ANNOUNCE while a DEFEND is pending;
    - link outage longer than a walk;
    - supplied-seed boundaries for counts 1, 8 and 255;
    - backpressure across a pending DEFEND.
  - Six of my robustness plants are rejected.
  - The one-response capacity limit is documented, not hidden. A count of 0 makes the `< POOL_SIZE_C` term reachable only for an empty range, which never conflicts.
- `[R558] PASS Tests - receipts/unit.log (186/0), integ.log (5/0), coverage.log (225/225), mutants.log (65 rows, 63 named rejections, 2 controls), differential.log.gz (12/12, 17/17), p7_copy.log (186/9); sim_main.cpp:1083-1276; mutants.py:43-224`
  - Each new check failed for its claimed defect in the campaign.
  - Section [13] derives its constants from the RTL (`POOL_SIZE_C`, `PROBE_MIN_MS_C`, learned maps), so a constant change is graded as it stands.
  - Real integration wiring is graded by three of my datapath probes.
  - The one escape (`u1`) is an ungraded implementation detail that no contract states. It is retained as R558-6-S1.
- `[R558] PASS Docs - docs/design/MAAP_FABRIC.md:50-76,96-129,142-188,211-273; hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5,22-29; KL_maap.sv:12-56; sw/firmware/ctrl/maap/README.md:189-192; docs/design/AREA_BUDGET.md:10,104-129,143-152,371,410,460-470; docs/design/MARK_II_AREA_PLAN.md:56,107-147,650-654; docs/findings/234_PP_SHADOW_AREA_BASELINE.md:1-180; PR #706 body`
  - Every statement about the first draw, the folds, the zero-sum exclusion, the MAC low-32-bit scope and PortOperational! matches the RTL and my model.
  - I recomputed every figure against `pp_resource_baseline.json` (50,013 = 50,230 - 217; 15,753 = 15,823 - 70; WNS 0.233 = 0.114 + 0.119; 11,973 over; wrapper 11,020 / 52 %; MAAP +51/+60).
  - Documentation gates pass. The PR body's p7 command reproduces its stated 9 failures.
  - Wording: SUGGESTION R558-8-S1 only. The open RESIDUE items are prior and retained.



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6103915710
[R559] POSITIVE - exact head 32582421bbf095a7b5a7d4b953c4d737b86fe54b

## 2. Findings of this round

### R559-7-S1 - SUGGESTION - Tests, Robustness - `hdl/ieee1722/maap/KL_maap.sv:464-466`, `:332`, `:203`; `docs/design/MAAP_FABRIC.md:124`, `:52-55`, `:99` - three documented details are correct at this head but no check grades them

- **Evidence (probe set run with `scripts/campaign.py`, `receipts/campaign.log`):** each of these probes builds and passes all 186 unit checks (rc 0).
  - `p_m5_link_keeps_offset` keeps `offset_r` on a PortOperational! restart. `MAAP_FABRIC.md:124` says the event "draws a fresh range", and the C core's `restart()` (`sw/firmware/ctrl/maap/maap.c:117-123,237`) also draws afresh. `port_return_reprobes` and `port_loss_is_no_event` walk on `dut->offset_o` and never compare it with the pre-outage range.
  - `p_m7_count0_offset_bound` drops `seed_offset_i < POOL_SIZE_C`. This differs only at count 0, where a supplied `0xFE00` is refused today. `supplied_seed_bounds` uses counts 1, 8 and 255 only.
  - `p_m3_announce_from_fold` draws the announce interval from the probe fold instead of `lfsr_r[9:0]`, which `MAAP_FABRIC.md:99` documents. The draw stays in bounds and random, so no clause is affected.
- **Impact:** a later edit could change these documented behaviours silently. None is an acceptance item, and none is a defect at this head.
- **Optional outcome:** the next harness change can add:
  - an M5 assertion that the post-return range is a fresh draw: with the generator state known, compare it with `rand_offset(lfsr_r[15:0])` at the event;
  - a count-0 supplied-seed boundary row.
- **Verification:** both probes fail a named check.

### R559-7-R1 - RESIDUE - Docs - PR #706 body, "Known limitations / out of scope", last bullet - the sentence is stale now that the head is pushed

- **Evidence:** the body says "Hosted checks and the local workflow replica need the pushed head." The head is now pushed, and hosted contexts are running at it (`receipts/hosted_checks_snapshot.tsv`).
- **Why RESIDUE:** this is PR-body wording only. It changes no figure, check, verdict or clause claim.
- **Exact fix:** replace the sentence with "Hosted checks run at the pushed head `32582421`; hosted and local-replica acceptance belongs to the manager."

### Probe observations that reproduce retained suggestions (no new finding)

- `p_m2_own_count_live` (own requested_count read from live `count_i`) escapes, 186/0. This is retained **R558-6-S1**. `MAAP_FABRIC.md:71-72` disclaims reconfiguration during a frame.
- `p_m4_rebegin_reuses_first_fold` (every Begin! re-folds) escapes, 186/0. This is retained **R558-7-S2 = R559-6-S3**, disclosed in the PR body.
- `p_q8_first_draw_count_fixed_8` (the Begin! draw clipped for 8 whatever `count_i` is) escapes, 186/0 (`receipts/probe_q8_first_draw_count.txt`).
  - This is retained **R559-6-S2**, older than #696 and disclosed in the PR body. Section [13] claims counts 1..8, so it cannot see a fixed-8 clip.
  - The gap only matters for blocks larger than 8. A separate Issue remains the right home.


## 5. Lens results (same format as findings)

```text
[R559] PASS Conformance - issue #696 acceptance 1-4 and rulings 6076940309, 6079087547, 6089712293, 6102832618; hdl/ieee1722/maap/KL_maap.sv:141-203,248-259,311-339,380-386,430-497; hdl/milan/milan_datapath.sv:7168-7172; receipts/first_draw_proof.txt, maap_integration.log, check_baseline.txt - M1 compare_MAC in rProbe!/PROBE and rDefend!/DEFEND (:315-320; equal MAC yields); M2 DEFEND echoes rx_start_r and all 16 count bits while conflict_* carry the overlap (:436-443, B.3.6.6); M3 x^32+x^22+x^2+x+1 with the period proven by the harness's order test, seeded from MAC[31:0] + PHC at first enable; M4 sampling at first enable, not reset, with datapath intervals and first blocks differing for different MACs (acceptance 2) and the 6102832618 criterion proven for every seed; M5 rising eff_link_w restarts while a fall is no event (B.3.5.9; ruling 6093171536); M6 shared buffer with its capacity deviation recorded; M7 Table B.9 bounds; M8 discard without effect, counting withdrawn and recorded (MAAP_FABRIC.md:186-188); acceptance 3 MAAP 490/340 (+51/+60, author's measurement) and three records rewritten with policy unchanged, check-baseline PASS; acceptance 4 assigned to the bench lane; no register-map, filter or mailbox change in e8454e27..HEAD
```
```text
[R559] PASS RTL - KL_maap.sv (full file at the head); milan_datapath.sv:2124,2165,2934-2956,3000-3001,7168-7172; sw/litex/milan_soc.py:811-813 - widths (seed_end_w 17 bits, probe_iv_w <= 581, announce <= 31511 in 16 bits, conf_cnt 16, tx_own_cnt 8); the first-draw select only while rng_seeded_r = 0; zero-seed fallback; port_operational_r reset to 0 so the post-reset edge is ignored in IDLE; defend_pending cleared on every exit from ANNOUNCE, which makes the ANNOUNCE term of defend_w redundant but harmless; save/defend mutually exclusive; every new register reset; no new clock crossing (axis_clk and gtx_clk are both milan_cd); FSM default arm and MAAP_P=0 tie-off unchanged; lint 90 <= 90
```
```text
[R559] PASS Robustness - tb/verilator/maap/sim_main.cpp:781-806 (disable, link flap, conflicting ANNOUNCE and reset during a pending response), :836-872 (outage longer than a walk), :874-893 (supplied seeds 0, limit, limit+1, 0xFE00, 0xFF00, 0xFFFF at counts 1/8/255), :895-941 (lengths 1..41 and each missing byte 0..41 for all three types in both states), :442-471 and :536-566 (backpressure at 0/2/4/7 beats); receipts/campaign.log probes p_m8_* (3 caught), p_m6_cancel_* (3 killed), p_dp_link_tied_high (killed) - truncation, boundaries, reset during activity, repeated link events and backpressure are graded and pass at this head; ungraded details are recorded as S1 and the retained suggestions
```
```text
[R559] PASS Tests - sim_main.cpp sections [1]-[13], sim_integration.cpp, mutants.py, maap_differential.py, test_maap_differential.cpp; receipts/maap_unit.log, maap_integration.log, maap_coverage.txt, campaign.log, differential_summary.txt, first_draw_proof*.txt - unit 186/0, datapath 5/0, coverage 225/225, 63/63 suite defects killed at their named checks with 2/2 controls; each round-7 plant fails exactly its intended check; section [13] verified as non-vacuous against an independent proof; differential 12/12 and 17/17; 22 reviewer probes, with every escape a correct-but-ungraded detail (S1, R558-6-S1, R558-7-S2/R559-6-S3, R559-6-S2)
```
```text
[R559] PASS Docs - docs/design/MAAP_FABRIC.md:42-188,197-273; hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5,22-29; hdl/ieee1722/maap/KL_maap.sv banner :12-55 and comments :141-203; sw/firmware/ctrl/maap/README.md:189-192; docs/design/AREA_BUDGET.md:10,104-160,368-371,407-411,460-470; docs/design/MARK_II_AREA_PLAN.md:56,107-147,650-655; docs/findings/234_PP_SHADOW_AREA_BASELINE.md:1-107; docs/findings/README.md:25; PR #706 body - every first-draw, fold, seed, link, M6/M8 deviation and area statement checked against the RTL, the executed results, the record file (66/66; arithmetic recomputed) and the 6102832618 criterion; documentation gates rc 0; RESIDUE R559-7-R1 and the retained residues are wording only
```



Source: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6113540239
[R558] NEGATIVE - exact head eb86b843557c6d9300847e3b6e12851604580b69

## 3. Findings of this round

### R558-9-F1 - MINOR - Docs - `docs/design/MARK_II_AREA_PLAN.md:695-696`, `:947` - after the merge, M2's base route is said to equal the `route-1x1` record, which is now #696's

- **Authority/evidence:**
  - At the candidate, `syn/ooc/pp_resource_baseline.json` records `route-1x1` as follows:
    - LUT 50013, FF 54306, SLICE 15753, WNS 0.233, WHS 0.017;
    - its `measured` note names #696's lane head `bee1b0d7`.
  - The same page says so at `MARK_II_AREA_PLAN.md:110`: "the gate's current record, #696's first-draw re-baseline". `:656` says "now at 50,013 LUTs ... that record is the comparison anchor".
  - Dev's M2 section (`2b22bf29`, PR #710) tabulates "Base route at dev `e8454e27` | 50,267 | 54,413 | 15,779 | 74 / 27 | +0.299 / +0.031" (`:690`). It then states at `:695`: "The base route equals the `route-1x1` record in every gated figure."
  - `:696` ("Against that record, the M2 route passes") and M6's `:947` ("Against the record, the M6 route passes") use the same referent.
  - `scripts/record_vs_lane_routes.py` (`receipts/record_vs_lane_routes.txt`) reads the record and the plan at each revision:
    - At dev `cfadd767` the base row equals the record: YES.
    - At the PR head `32582421` the M2/M6 sections do not exist.
    - At the candidate the base row does **not** equal the record: LUT, FF, SLICE, WNS and WHS all differ.
  - So neither source carries the defect. The merge alone makes `:695` false.
- **Why MINOR and not RESIDUE:** the sentence states the identity and figures of the *gate* record ("equals the `route-1x1` record in every gated figure"). It is not a baseline-scoped sentence.
  - This is the same class as R558-5-F1 on this PR (comment 6097253076). There, the merge made M0s's "the accepted 50,267-LUT route remains the comparison record" false, and that finding was MINOR and was fixed at `:656`.
  - It differs from R558-2-R1 / R559-2-R1, where each figure was correct for a baseline the page explicitly retains.
- **Impact:**
  - The merged page names two different records as the `route-1x1` record (`:110`/`:656` against `:695`).
  - D7 lanes take their comparison anchor from these intermediate-measurement sections (`AREA_BUDGET.md:365,452`). The next lane modelled on M2/M6 would anchor on 50,267, which is no longer the gate's record.
  - No gate detects it: all 39 documentation, static and record gates pass on the candidate.
  - The M2 and M6 pass verdicts themselves survive. Against #696's record, M2 moves +126 LUT, +48 FF and +18 slices, and its WNS rises. M6 moves +38 slices, and its WNS falls 0.092 ns to +0.141. Both are within every tolerance and floor (`receipts/record_vs_lane_routes.txt`). So no measurement or verdict is wrong, only the record each section names.
- **Required outcome:** at the merged head, `:695-696` and `:947` name the record each lane was compared against: #645/#647's `route-1x1` record, the gate record at dev `e8454e27`. Either they say that #696's record has since replaced it, or they name both. None of them may imply that the current `route-1x1` record is the 50,267 figure. One fix that keeps every figure:
  - `:695`: "The base route equals #645/#647's `route-1x1` record, the gate record at dev `e8454e27`, in every gated figure; [#696](https://github.com/kebag-logic/milan-fpga/issues/696)'s 50,013-LUT re-record has since replaced it."
  - `:696`: "Against that record, the M2 route passes with no failing endpoint; it also passes against #696's record."
  - `:947`: "Against #645/#647's record, the M6 route passes with no failing endpoint; it also passes against #696's record."
- **Verification:**
  - `python3 -I scripts/record_vs_lane_routes.py <repo> <merged-head>` reports the base row against the record. The sentences must then name the record that row matches.
  - `docs_check.py`, `gen_toc.py --check` / `--verify-anchors`, `check_em_dash.py --base <first parent>` and `pp_resource_gate.py check-baseline` exit 0.

### R558-9-R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:706`, `:968` - lane-scoped "gate record stays unchanged" lines now sit beside #696's re-record

- Both M2 and M6 end with "The gate record stays unchanged under D7." Each is true of its lane, and the paragraph makes the lane its subject. On the composed page, though, the gate record did change, through #696.
- This is wording only: it states no figure or record identity, and it changes no verdict. It is the same class as retained R558-5-R1.
- **Exact fix:** `:706` "M2 does not re-record the gate under D7." and `:968` "M6 does not re-record the gate under D7."

No BLOCKER or MAJOR.


## 6. Lens results (same format as findings)

```text
[R558] PASS Conformance - hdl/milan/milan_datapath.sv:7181-7186 (composed KL_maap instance) and tb/verilator/maap at eb86b843 - checked against #696 acceptance 1-3 and rulings 6079463350/6102832618: KL_maap.sv patch byte-identical to source; candidate unit 186/0, real datapath 5/0, campaign 65/65, differential 12/12 + 17/17; the M5 link-return and M3 clock-seed behaviour hold through the composed datapath (probes: dropping either connection fails its named check)
[R558] PASS RTL - hdl/milan/milan_datapath.sv:267,2124,2165,3000,3450-3533,6337-6344,7181-7186 - PR hunks (+267, +7171) and M6 hunks (+3450..3533, +6337..6344) are disjoint; port_operational_i and realtime_ns_i are connected once each to nets declared once (eff_link_w :2165, ptp_now_w :2124) under `default_nettype none; fresh merge-tree equals the candidate tree; lint 90 <= 90; every composed milan_dp shape elaborates and passes (incl. MAAP_P=0 prune leg)
[R558] PASS Robustness - receipts/probes/*.run.log, receipts/milan_dp_run.log - the PINMISSING waiver means a dropped connection compiles; three wiring faults (link tied high, link dropped, clock dropped) are each caught by the composed suite; pruned-engine leg 33/0; link-return and MAAP-off talker holds pass on the composed datapath; GET_COUNTERS checks that read M6's counter table pass beside the live MAAP engine
[R558] PASS Tests - tb/verilator/maap/{integration.mk,mutants.py,sim_integration.cpp} and tb/verilator/milan_dp at eb86b843 - integration build derives the composed source list (milan_dp unchanged by dev); 65-row campaign with both clean controls; milan_dp run rc 0 (12,065 checks, matches the manager's candidate shard); no test changed by composition (patch-ids identical); R558-8-S1 retained as optional
[R558] UNCLEAN Docs - docs/design/MARK_II_AREA_PLAN.md:695-696,947 - open MINOR R558-9-F1; also examined and otherwise clean: AREA_BUDGET.md:10,104-152,197-212,277,365-387,410-470 (record table arithmetic 50,013/63,400 = 78.88 %, 11,973 over, 97 slices free, wrapper 22,993 - 11,973 = 11,020); MARK_II_AREA_PLAN.md:56,107-147,650-668,677-706,924-968; docs/findings/README.md (21 rows, each once, dev's row set); 39 documentation/static/record gates rc 0; RESIDUE R558-9-R1
```

