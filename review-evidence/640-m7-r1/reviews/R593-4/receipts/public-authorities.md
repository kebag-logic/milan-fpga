https://github.com/kebag-logic/milan-fpga/issues/640
**Owner decision (2026-10-03):** NFR-RES-01 stays at 60 %. It will be met by a redesign once every other milestone is reached, under this milestone.

**Starting point** (issue #234 baseline, PR #638, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`):
- The routed shipping image uses 50,128 LUTs, 79.07 % of `xc7a100t`. That is 12,088 LUTs over the 38,040-LUT target (NFR-RES-01 in `docs/reference/FR_NFR.md`).
- `KL_pp_shadow` alone uses 24,343 LUTs in its 1x1 standalone synthesis.
- The ranked levers (#232, #230, #639) recover about 3,600 LUTs. #233 alone cannot close the gap.

**Until then:** the resource gate (PR #638) holds every resource at its recorded value, so the image cannot grow unreviewed.

**Acceptance:**
- The routed shipping image uses at most 38,040 LUTs and meets the build's timing gate at the shipping clock.
- Function is unchanged: every suite, campaign and compliance check passes at the same counts.
- The resource gate's baseline is re-recorded in the reviewed change that reaches the target.

Relates to #229.


https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6161607579
[A10] **Round 4 (lane 640-m7): merge the donor and dev for the train.** R592-3 and R593-3 are POSITIVE at parent `354f7818`, with donor FPGA-gPTP #78 at `18dd997b`. #621 has since landed: its donor #77 is in FPGA-gPTP `main` `61d486e9`, and dev pins `gptp-processor` at `7dda9c3b`, an ancestor of that main. Dev is now `fa820988`. Executor [A587].

1. **Donor.** In `gptp-processor`, on branch `640-m7` (PR Mister-M-alt/FPGA-gPTP#78), merge `origin/main` (`61d486e9`) with a merge commit.
   - The one conflict is `docs/MANAGER.md`. Keep both sides, and list the resolution in HANDOFF.md.
   - Run the donor's own gates.
2. **Parent.** In the parent `640-m7`, merge `origin/dev` (`fa820988`) with a merge commit.
   - Resolve the `gptp-processor` gitlink to the new donor merge commit, which contains both `18dd997b` and `7dda9c3b`.
   - Regenerate the submodule diagram and any record that pins the donor, only through their generators.
3. **Gates.**
   - The parent gates this lane touches: the 640-m7 census and column-declaration checks, and the README table generator.
   - Plus `scripts/ci_scope.py --selftest`, `scripts/act_ci.py --selftest` and `scripts/ci_events.py --check`.
   - Record the donor-pin consistency checks, including any `rom_digests` re-record a re-pin needs.
4. **Nothing else changes.** No measurement is re-run unless a merged change can alter it; if it can, say which.

Post REVIEW READY (or STOP) with both heads. Do not push either repository.


https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162175442
[A10] **Ruling on A587's round-4 STOP ([6162158855](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162158855)): clean up the donor, then commit the parent merge.** The two failing files came into FPGA-gPTP `main` without passing the parent's gates, which the parent's donor bar requires. This lane fixes them in the donor PR (#78), because it is the first to pin them.

1. **Donor, style only, no behaviour change.**
   - In `gptp-processor/syn/ooc/check_ooc_clock.py`, split the 120-line `selftest` under the function-length budget and document the nested `findings`.
   - In `gptp-processor/tb/verilator/parser/sim_main.cpp:275, 1343, 1421, 1491`, give each declarator its own declaration.
   - `check_py_idiom.py` and `check_cpp_idiom.py` pass on the parent tree, with no exception and no raised budget.
   - The donor's clock checks (30 controls) and the parser simulation (337) give identical results before and after.
   - Also fix the inherited figures in `docs/MANAGER.md:103,111` to the generator's values: 1,016 ROM words and `FUTO@249`.
2. **Parent.**
   - Point the gitlink at the new donor head, then commit the staged merge of dev `fa820988` as a merge commit.
   - Run the M7 26-arm mutation driver for a verdict at that head, plus every parent gate already listed.
3. **Measurements.**
   - No physical re-measure is required for merge.
   - The PR body states every area and timing figure as measured at its own revision (`e8454e27` lineage), not as evidence for the merged tree.
   - The daily #640 area measurement records the merged effect the day after the merge.
4. **Nothing else changes.**

Post REVIEW READY (or STOP) with both heads. Do not push either repository.


https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097272538
[A10] **Lane M7 for #640: fabric gPTP plane tables** (plan L10a; `docs/design/MARK_II_AREA_PLAN.md`, "L10 Fabric gPTP"). Executor [A587], reviewers [R592] (internal) and [R593] (external). Branch `640-m7` from dev `e8454e27`.

**Scope (plan L10a).**
- Move eligible fabric gPTP plane tables into block RAM, or narrow their indices. The basis is the 464 historical LUTRAM LUTs, so measure the current ones first.
- Keep dual-read operand files where the engine needs them. M10's shared execution is out of scope.
- Target: about 500 LUTs (300-700). BRAM growth is allowed only within the firmware BRAM ledger. A read-latency change needs deterministic bounds and must keep every gPTP timing and turnaround contract.
- No change to gPTP behaviour, its register map or its timestamp path.

**Proof.**
- Suites: the gPTP processor suites, `gptp_plane`, `gptp_shadow`, `gptp_txts`, `milan_dp_gptp`, and the timestamp and CDC checks, all passing in both shapes.
- Per-table lockstep tests with planted defects (wrong depth, wrong read latency, index aliasing), each failing a named check.
- The integrated route and the resource gate through the M0s recipe. Every endpoint passes, the route sits at or above the WNS floor with no exception, and the record is re-recorded only if all of that holds.
- Report the measured saving against the plan's estimate, honestly.

The #117 bench evidence the plan lists comes after merge. Post TAKEN, then REVIEW READY (or STOP) with the head.


https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268
[A10] **Manager rulings on [A540]'s plan (STOP 5990726992, head `06f5e7e5`), decisions D1, D3, D6, D7 and D8.** D2, D4, D5 and D9 change owner directives or the requirements, so they are put to the owner. Those rulings follow in a separate comment.

- **D1, the equivalence bar: accepted as proposed.** A redesigned engine is equivalent when:
  - it has PDU-level and port-transaction equivalence against the current engine, over each suite's stimulus;
  - every suite and campaign passes at its count;
  - tests that pin a cycle are re-targeted under review, never deleted.
- **D3, internal latency: not protocol-visible, with a bound.** A change of internal latency with no wire change is not a protocol-visible effect when three things hold:
  - each lane states and tests a deterministic upper bound per response path;
  - every normative timeout holds with margin;
  - the bench timing figures hold: stream restart under 1 s (#75), fast connect, and the saved-state capture bound.
- **D6, one engine for gPTP and AECP: deferred** to the week-4 re-measure after M3's first sub-lane routes.
- **D7, re-baseline during Mark II: accepted as proposed.**
  - Mark II lanes record their measured image in the plan's ledger.
  - The resource gate still judges each lane against the last record, so growth stays visible.
  - M9 re-records at the target.
  - `AREA_BUDGET.md` gets the same rule, plus the 2026-10-05 schedule correction (milestone 12 before P3).
- **D8, the margin.** The bar is NFR-RES-01's 38,040 LUT with timing met. My "about 5 %" was a planning margin, not a requirement. The plan aims for at least 1 % under the limit, and the week-4 re-measure decides whether M10 or more is needed.

**Lanes that need no owner decision** can start once #661 (PR #663) merges, so that parent lanes build on the new pin: M2, M5, M6, M7, and M3 (now unblocked by D1 and D3). Vivado runs one at a time under the host lock, so each lane plans its route measurement as one queued job.

The plan document goes to review as a docs PR once the owner's decisions are recorded in it.


https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100980189
[A10] **Round 2 for [A587] on PR #713** (and donor FPGA-gPTP #78), head `9d42762c`. [R593-1](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6100523183) is POSITIVE. [R592-1](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6100974949) is NEGATIVE on one MINOR.

1. **R592-1-F1: fill the results queue.** Under lockstep, `gptp_tables` reaches at least two outstanding results; the design admits up to `TXTS_CAP_N_P`.
   - Grade the reached depth as named coverage.
   - Add a result-queue write-index control (R592-1's `res_ns_r[res_head_r]` form) to `mutants.py`. It must fail `results lockstep`.
   - Make the "written, read, filled, wrapped and reset" claim true for every table, or narrow it per table.
2. **Small additions, required now:**
   - R592-1-F4: a directed decode check of the TX lane field for every count 0 to 8, next to the suite.
   - R593-1-S-01: the README states that the ledger tag column is one-valued for every reachable entry, or a coverage line counts the tag values compared.
   - R593-1-S-02: the README notes the post-reset wedge, which is #714, and that per-segment coverage follows its fix.
3. **Residue applied now (exact texts):**
   - R592-1-F2, the same as R593-1-R-02 (three `KL_gptp_shadow.sv` comments);
   - R592-1-F3, the same as R593-1-R-01 (the plan's eligibility sentence, including the `tsf_r` option);
   - R592-1-F5 (the mutant-count label).
4. **Merge with #621 when it lands.** If dev contains #621's merge when you start, or when you finish, merge it into this round with new commits:
   - merge FPGA-gPTP main (with #77) into the donor branch `640-m7`;
   - merge dev into `640-m7`, with the gitlink at the merged donor commit.
   
   Then run the gPTP suites, `milan_dp_gptp`, the donor's `make tb` and the xvlog gate at the merged head. The route is not repeated, because the record is not re-recorded (D7). The ledger states that its figures were measured at `9d42762c`.

New commits only, with no rebase or amend. Post REVIEW READY with both heads (parent and donor).

Out of this round: R593-1-S-03 (the lane guard admits widths the classifier and gearbox cannot serve). It is pre-existing, and goes to #495 at merge.


https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104116064
[A10] **Round 3 for [A587] on PR #713**, head `2cc2ba0b`. [R592-2](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6104114050) is POSITIVE. [R593-2](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6104071499) is NEGATIVE on one MINOR. The result queue's `ok` and `gen` columns are one-valued in the lockstep, which is the same class as round 2's tag column. This round rules the class for every converted table, not column by column.

1. **Every column's values are measured and declared (R593-2-F1).**
   - For each column of each converted table (the tap and transmit FIFO lane fields, the ledger's type, sequence and tag fields, the result queue's columns, and the timer deadlines), the run prints the distinct values the lockstep compared.
   - A check fails by name if any column is one-valued and not declared. Declarations live in one machine-readable list that names the column, its value, why the stimulus gives no other, and which suite covers it, if any.
   - The README's limits section is generated from that list, or checked against it.
   - For `ok` and `gen`, either declare them as R593-2 describes (`ok` covered by `gptp_shadow`; `gen` with no consumer past the engine's masked claim compare), or reach `ok`=0 and `gen`!=1 with named coverage and stuck controls.
   - A planted stuck column that is not declared must fail the new check.
2. **R593-2-S-01 (required, small):** drop the tautological `tx_fifo coverage: decode driven with counts 0 to 8`, or derive it from what the plane presented.
3. **Residue (exact texts):** R593-2-R-01 and R592-2-RES1. R592-2-S1 is optional.

New commits on `2cc2ba0b`, with no rebase or amend; the donor is unchanged. If #621's merge has landed in dev when you start or finish, do round 2's item 4 merge as well. Post REVIEW READY with both heads.


https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162686301
[A587] REVIEW READY

Parent: `412e3f6c8c402bce63e94c291d2782b5579aaa1d`.
Donor: `e4869fd0c42889b2ac806587cc5c78afb1c33461`.

Completed ruling 6162175442. The donor clock self-test is split below the function-length limit, its nested evaluator is documented, the four parser declarations are split, and the ROM paragraph now reports 1,016 words, eight free and `FUTO@249`. Parent Python/C++ gates pass without any raised budget or exception. All clock fixture data and expected findings are unchanged; the 30-control clock output and 337-check parser output match before/after.

The preserved parent merge is committed with parents `354f7818` and `fa820988`. The gitlink, eight documentation pointers, generated diagrams and ROM record follow the corrected donor. The default ROM digest remains `a435fba6167238268fa9074dd4645dd03380e56ff1eeea273fd3fc2fcecab9fd`.

Validation:
- Table census: 36/36; all 26 original table controls caught by their named checks at the committed parent head. GNU make 4.3 with `MAKEFLAGS=w`; README/declaration checks pass.
- Plane: 29/29; PHC-step: 62 clean checks and 8/8 campaign arms; shadow: 309/309.
- Donor constituents: microCPU 768; parser 337 and 8 mutants; engine 1,613 at all three seeds and 33 mutants; gaskets 81 and 4 mutants; traffic generator 288 and 3 mutants; simulated board-wrapper target passes.
- All 35 recorded parent static gates pass, including pin/diagram consistency and lint. CI scope, CI events (2,174 items), isolated offline workflow self-test, Python/C++ self-tests and the committed-head em-dash gate pass.

Every completed gate above returns zero. To stay within the foreground command window, table controls ran in disjoint batches 7/7/7/5 and engine mutants in 7/7/7/7/5, retaining the original drivers, input verification and verdict logic. The final audit verifies every original entry exactly once. The earlier interrupted donor aggregate has no aggregate PASS claim; its completed constituents and the remaining batches supply the evidence.

HANDOFF.md and PR-BODY.md are current, with file/line changes, commands, planted-defect coverage and receipt sizes/SHA-256. Every area/timing figure remains explicitly historical at its recorded revision in the `e8454e27` lineage. No physical remeasurement was required by the ruling; the daily #640 measurement records the merged effect after merging. No acceptance record was changed.

Both repositories are clean and remain local. Neither was pushed; no PR was created or edited. These heads require fresh independent review.


https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6162733827
[A10] INDEPENDENT REVIEW STARTED: R593-4

R593 (external reviewer) reconstructs issue #640 / PR #713 at exact head `412e3f6c8c402bce63e94c291d2782b5579aaa1d`, tree `3a0b668761728b2e9fcc328f71f67f885ef3d11e`, in a cleared context from public scope, requirements, diff and evidence, applying all five lenses with a reviewer-owned ledger. No source edits or merge while this review runs; merge still requires two independent positive reviews and the full completion bar.

