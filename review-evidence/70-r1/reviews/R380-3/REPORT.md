[R380] NEGATIVE - exact head 816c3b742940b9ac8d160ff03e05553a47e5e66d

# R380-3: internal independent re-review of PR #610 (issue #70, lane 0: adopt the D3 contract)

- Head `816c3b742940b9ac8d160ff03e05553a47e5e66d`, tree `d6f5b20fc823db88139e70653bb5e3c2e9a416bf`. The parent is `e796c68a460fe6946e28cb9da0349a382c868352`, the round-2 head.
- Delta under review: `e796c68a..816c3b74`, one commit by [A407], "docs: complete D3 contract sweep and alarm carrier ruling". It has a one-line subject with no body or trailers.
- Whole PR: `c07232228c12b72805dd20e6852bf93f25794da0..816c3b74`, four commits, five documentation files.
- Processor gitlink `16be6768f710e79450aace277abacd6c2c3336e5`. All four gitlinks are unchanged (`receipts/20`, `receipts/90`).
- Verdict: **NEGATIVE**. One MINOR finding is open (F1). It leaves Conformance, Tests and Docs unclean. RTL and Robustness are covered clean at this head.
- My round-2 finding R380-2 F1, the R381-2 findings F1 and F2, and the taken suggestion R380-2 S1 are all resolved at this head.
- F1 is new. D3 says its contract sweep matches statements wrapped across "intervening comment prefixes". That is true only for a bare `//` on one alternative. The `//!`, `#` and `*` prefixes break every multi-word alternative, and the processor's source banners use exactly those prefixes.

## Reconstruction (public state only)

I read these sources in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.
3. The issue #70 body and its comments, including:
   - the lane-0 assignment, 5862193501;
   - the rulings DR1a to DR6, 5862405632 (`receipts/50`);
   - the DR2c-carrier ruling, 5863247772 (`receipts/51`);
   - the round-3 assignment, 5863263971 (`receipts/52`);
   - [A407] TAKEN, 5864908223, and REVIEW READY, 5865095789.

   The rulings are fixed and are not reopened here.
4. The review-start comment on PR #610, 5865110623.
5. The FASTCONNECT, D3, snapshot-ownership and BAREMETAL_FIRMWARE pages at the head.
6. The processor tree at `16be6768` (docs, hdl, tb).
7. The delta diff and the whole-PR history.
8. Public evidence:
   - the tree `6cf46c2a:review-evidence/70-r1` (`receipts/61`);
   - the exact-head hosted check runs (`receipts/60`, `receipts/62`).

My round-2 packet was read-only input. I read R381-2's report (PR comment 5863242490) only after my own pass over the diff and the processor tree.

My round-2 packet contains no script named `finding_evidence.sh`. The round-2 script for my F1 is `scripts/f1_mark_semantics.sh`. I re-ran it unchanged (`receipts/10`). It hard-codes the round-2 sweep pattern, so every "sweep-miss" line it prints is expected, and that output is historical only. The current-head check is `scripts/finding_evidence.py` (`receipts/11`). It extracts the sweep from D3 at the head and runs it exactly as written.

## Round-3 focus items

1. **Section 15.2 completeness and the sweep.** Met, apart from F1.
   - 15.2 now has 37 rows over 29 files. Every path exists at `16be6768`, and all 39 links pin that commit (`receipts/40`).
   - `receipts/11` checked 31 required lines, the union of both round-2 lists:
     - `gen_ucode.py` 1364, 1439, 1582-1584, 1675, 1791, 1925, 2002, 2091;
     - 06 at 341-344 (6.2.1), 365 (6.4) and 421-425 (6.5);
     - `00_MILAN_COMPLIANCE_REVIEW.md` 206-208 (GAP-08);
     - 03 at 236, rule (d);
     - 02 at 492-493;
     - `protocol_processor_top.sv` 2448-2451;
     - `tb/acmp_nvm/README.md:15`.

     Every line is cited by a 15.2 row's line list. The named sweep matches each one or shows it as `-C 2` context (`RESULT PASS`, rc 0). The IDENTIFY rationale (1582-1584) is matched at 1582, and 1583-1584 appear as context.
   - The mark rows state the required semantics:
     - `gen_ucode.py` (D3 `:2356`) says the marks "stop being persistence triggers";
     - 06 (`:2326`), 00 (`:2354`) and 02 (`:2325`) say the marks stay "as completion notifications, never persistence triggers".
   - The exemption is narrowed (D3 `:2381-2385`): "That exemption never covers comments describing marks as persistence triggers", and "Every omitted match needs a stated, location-specific scope reason".
   - Multi-line matching works for the arbiter banner, `KL_pp_nvm_mgr_arb.sv:15-16`, because that wrap's prefix is a bare `//` (`receipts/43`). The same property fails for the other comment prefixes (F1).
   - My own search of the pinned tree for missed statements covered:
     - my round-2 nine-probe sweep, re-run at this head (`receipts/41`);
     - six further probes: mark semantics, platform/integrator writer, response delay, future manager, IDENTIFY exclusion and dynamic dirty (`receipts/44`).

     No missed D3-falsified statement remains. The remaining hits are of four kinds:
     - notification triggers (Table 5.22) or ACMP binding-record marks, which D3 leaves unchanged;
     - diagnostic `dirty_o` test checks;
     - the raw port fact `KL_pp_nvm_port.sv:25`, "commits stay asynchronous ... because the port never blocks anything but its own lane", which is still true under D3;
     - one duplicate of a listed claim, `tb/acmp_nvm/acmp_nvm_wrap.sv:12-14`. The named sweep matches it, so lane 1's obligation at D3 `:2377`/`:2385` reaches it. It has no row, so it is S1 below, not a finding.
2. **DR2c-carrier ruling.** Met on all four pages. Each has a working FASTCONNECT 9.2 cross-reference, and 163 fragment links resolve (`receipts/31`).
   - **FASTCONNECT 9.2** `:1129-1143`:
     - only `nvm_alarm` is reset-sticky, and no bit is added;
     - firmware exhaustion is "a `VD_*` verdict loss without ACK" (ruling item 6);
     - a later success clears `nvm_stale` under 9.2's condition and never clears `nvm_alarm`.
   - **D3** `:763-779` (policy) and `:2583-2590` (lane 2 acceptance).
   - **Snapshot** `:1097-1104`, and item 7 at `:1818-1823`.
   - **BAREMETAL_FIRMWARE** `:1916-1924`.
   - The lane-2 negative control (D3 `:2620-2625`) targets `nvm_alarm`:
     - "Clear `nvm_alarm` on heartbeat or later success" is the killed mutant;
     - "Drive producer exhaustion before checking those `nvm_alarm` controls" is the precondition;
     - "For firmware loss alone, require later verified recovery to clear `nvm_stale`. That required recovery is not a negative control."

     This agrees with the unchanged FASTCONNECT Recovery line (`:1553-1555`) and with 9.2's next-state rule (`:1177-1181`). Those two no longer demand opposite outcomes.
   - I found no residual "firmware alarm" or "forgive" wording on the four pages. The remaining alarm lines are the producer alarm or historical discrepancy text.
3. **R380-2 S1.** Taken. D3 5.1 (`:544`, `:546-552`) names:
   - `RETRY_BACKOFF_CYC_P` in processor `clk_i` cycles, counted from the error;
   - its product value, `ceil(processor_clock_hz * 500 / 1000)`: 50,000,000 cycles at 100 MHz and 25,000,000 at 50 MHz. I checked that arithmetic;
   - that it uses neither debounce ticks nor firmware time.

   The processor top declares `CLK_HZ_P` (`protocol_processor_top.sv:91`) and derives other cycle counts from it (`:93`, `:129`). The 01_overview (`:2330`) and 08_timing (`:2328`) rows carry the conversion forward. See S2 for a note on integer width.
4. **Scope and frozen items.** Met.
   - The delta touches exactly the four documents (`receipts/20`).
   - FASTCONNECT section 16 has the same 5 checked and 21 unchecked states, in the same order, at the base, at `e796c68a` and at this head. The FASTCONNECT hunk is only at `:1126` (9.2).
   - The whole D3 section 15.1 is byte-identical to round 2, with 10 rows RULED.
   - `scripts/compare_rulings.py` shows every "Selected option" cell equal to ruling 5862405632 (`receipts/21`, rc 0).
   - The nine lane-0 gates all return rc 0 at this head (`receipts/30`). They ran with the hash-locked Markdown renderer wheels and PyYAML 6.0.3 in a disposable environment.

## Findings

### F1: MINOR. Lenses: Conformance, Tests, Docs. The contract sweep claims to match across comment prefixes, but only a bare `//` is crossed, and only by one alternative.

- **Where:**
  - `docs/design/SAVED_STATE_MATERIALIZATION.md:2373`: "Multiline matching includes wrapped prose and intervening comment prefixes."
  - The pattern at `:2369`.
- **Authority:**
  - Round-3 assignment item 1: "The named sweep finds every such statement, and it matches across line breaks".
  - D3 `:2364-2365`: the sweep is "required at the adopted processor head", and lane 1 "reconciles every affected statement, including newly moved ones".
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
- **Evidence** (`scripts/wrap_tolerance.py`, `receipts/12`):
  - Every multi-word alternative joins its words with `[[:space:]]+`: `dirty mark`, `Nothing in the processor`, `groups 6 and 7`, `platform's saved-state`, `never delay` and `asynchronous to protocol`. The one exception is `integrating[[:space:]/]*platform`.
  - So a wrap whose continuation line starts with `//!` (the SV doc-comment prefix of the top banner at `:2448-2451`), `#` (`gen_ucode.py`) or ` * ` is not matched. The `integrating` alternative misses `//!` too, because `!` is not in its class.
  - Seven synthetic wrapped fixtures, each modelled on a statement class the sweep targets (for example the top banner, rule (d), and the groups 6/7 wording). The five comment-wrapped ones are all missed by the D3 sweep:

    | Fixture | Prefix | D3 sweep | Joints also crossing `//`, `//!`, `#`, `*` |
    |---|---|---|---|
    | `never` / `// delay` | `//` | miss | match |
    | `platform's` / `//! saved-state writer` | `//!` | miss | match |
    | `groups 6` / `# and 7` | `#` | miss | match |
    | `integrating` / `//! platform` | `//!` | miss | match |
    | `dirty` / `// mark` | `//` | miss | match |
    | bare-prose wraps (2) | none | match | match |

  - At the pin itself, the comment-tolerant variant adds 0 matched lines. So no statement at `16be6768` is missed today, and focus item 1 stands.
- **Impact:**
  - The sweep's stated purpose is to run at lane 1's head after lane 1 rewrites and moves these statements.
  - A statement such as "Manager 1 is the platform's saved-state writer", re-wrapped in the top's `//!` banner, or "never delay" split across a `#` comment, would be silently absent from the inventory.
  - The authoritative contract tells lane 1 and its reviewers that the sweep covers exactly that case. That is false assurance about the one gate that stands in for statement-by-statement reconciliation. It also leaves the round-3 "matches across line breaks" item met only for prose.
- **Required outcome.** One of these must be true:
  - The multi-word joints cross the comment prefixes this tree uses (`//`, `//!`, `#`, `*`), for example `(?:[[:space:]]|/|!|#|\*)+`.
  - Or `:2373` is narrowed to what the pattern actually does, and it says how comment-wrapped statements are found instead.

  Either way, the claim and the pattern must agree. DR rulings and 15.2 rows are unaffected.
- **Verification:**
  - Re-run `scripts/wrap_tolerance.py` from the repository root. Every fixture must show a non-zero count for the D3 sweep, or `:2373` must no longer claim comment-prefix coverage.
  - Re-run `scripts/finding_evidence.py`, which must still end with `RESULT PASS`.
- **Why RTL is not attributed.** The finding is about a documented text search and its claimed detection power. No RTL behaviour, width, FSM or interface contract at this head is wrong because of it, and at the pin nothing is missed (`receipts/12` part B). If the maintainer or the other reviewer reads it as an RTL-contract finding, the finding is recorded under that lens as well, and RTL is not banked clean by this round (AGENTS.md section 3).

### Suggestions (non-blocking; they do not affect coverage)

- **S1 (Conformance, Docs).** `tb/acmp_nvm/acmp_nvm_wrap.sv:12-14` makes the same claim as `tb/acmp_nvm/README.md:15`: "manager 1 is a harness face, as the platform's saved-state writer will be". The named sweep matches it (`receipts/44`, P2), but no 15.2 row names it. Extending the `tb/acmp_nvm/README.md` row (D3 `:2348`) to include the wrapper banner would treat the twin statements alike.
- **S2 (RTL, Robustness, Docs).** D3 `:546-552` could name the clock parameter as `CLK_HZ_P` and give an overflow-free integer form such as `(CLK_HZ_P + 1) / 2`. `CLK_HZ_P` is `int unsigned` (top `:91`). Evaluated literally in 32 bits, `CLK_HZ_P * 500` overflows above 8,589,934 Hz, including at the 100 MHz default. The top's existing conversions divide instead (`:93`, `:129`).
- **S3 (Docs).** Not taken from round 2, and still true: snapshot `:188` says "Seven items this contract does not settle", and that count does not match section 20. No coverage effect.

## Prior public review findings: resolved or retained at this head

| Finding | State | Evidence |
|---|---|---|
| R380-2 F1 (mark-as-trigger statements outside 15.2 and the sweep) | RESOLVED | All 15 of my round-2 lines, plus `gen_ucode.py:1584`, are row-cited and swept (`receipts/11`). The unchanged round-2 script's "sweep-miss" lines (`receipts/10`) are expected: it hard-codes the round-2 pattern. The new comment-prefix gap is a different defect, filed as F1 |
| R380-2 S1 (BACKOFF time base) | APPLIED | Focus item 3 |
| R380-2 S2 (firmware exhaustion carrier) | APPLIED through the DR2c-carrier ruling | Focus item 2 |
| R380-2 S3 (snapshot count) | NOT TAKEN (suggestion) | Retained as S3 |
| R381-2 F1 (gen_ucode, 06 6.2.1/6.4/6.5, GAP-08, 03 (d), 02:492, top :2448-2451, tb/acmp_nvm/README:15; sweep; exemption) | RESOLVED | Every location is row-cited and swept (`receipts/11`). The mark rows say the marks stay and stop being triggers. The exemption is narrowed (`:2381-2385`). The arbiter wrap `:15-16` is now matched (`receipts/43`) |
| R381-2 F2 (firmware alarm carrier and conflict with 9.2) | RESOLVED | Focus item 2. The lane-2 control and the Recovery line are consistent |
| R380-1 F1-F3, R381-1 F1-F2, R381-1 S1/S2 | STILL RESOLVED | `receipts/42`. The one "0" count there, for the 02 boot paragraph, comes from the row's reworded location cell. The row still cites lines 532-572 (`receipts/43`) |

## Lens results (clean lens lines carry their evidence)

```text
[R380] PASS RTL — D3 :544-552 (RETRY_BACKOFF_CYC_P in clk_i cycles, ceil(hz*500/1000): 50,000,000 @100 MHz, 25,000,000 @50 MHz) vs processor 16be6768 protocol_processor_top.sv:91/:93/:129 (CLK_HZ_P and its divided conversions); D3 :627-639/:653-655/:691-698 DR2c FSM (attempts counted at grant, retry while < 1+RETRY_MAX_P, giveup at 3, BACKOFF holds no bus/port) unchanged and consistent with 5.1; 15.2 rows vs pinned gen_ucode.py:1364-2091 and :1582-1584, top :2448-2451, KL_pp_nvm_mgr_arb.sv:13-18, 06 :341-344/:365/:421-425, 03 :236, 02 :492-493 (receipts/11, 40, 43)
[R380] PASS Robustness — DR2c-carrier error/recovery paths: FASTCONNECT :1129-1143 vs 9.2 next-state :1177-1181 and Recovery :1553-1555 (firmware-only loss heals via backed' AND NOT dirty'; producer exhaustion holds the nvm_alarm level, so backed stays 0 until reset); D3 :763-779 and :2583-2590, snapshot :1097-1104/:1818-1823, BAREMETAL :1916-1924 state identical semantics; capture refusal before START is still not a media attempt; BACKOFF value across clock rates (D3 :546-552)
[R380] MINOR Conformance — see F1
[R380] MINOR Tests — see F1
[R380] MINOR Docs — see F1
```

These artifacts were also checked under the unclean lenses and found nothing further:

- **Conformance:**
  - round-3 items 1 to 4;
  - the register against the ruling (`receipts/21`);
  - checkbox states and the file list (`receipts/20`);
  - required locations (`receipts/11`);
  - the reviewer probes (`receipts/41`, `receipts/44`).
- **Tests:**
  - lane-2 negative controls D3 `:2615-2625` against the FASTCONNECT Recovery and healed-outage lines `:1553-1559`;
  - lane-1 controls `:2558`;
  - the nine gates, rc 0 (`receipts/30`);
  - anchors, 163/0 (`receipts/31`).
- **Docs:**
  - the four delta pages;
  - the carrier wording and 9.2 cross-references;
  - 5.1;
  - the 15.2 rows and exemption text;
  - no residual firmware-alarm or forgiveness wording.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | round-3 assignment items 1-4 (5863263971); DR2c-carrier ruling 5863247772 vs FASTCONNECT 9.2, D3 6.3/18.2, snapshot, BAREMETAL; ruling 5862405632 vs D3 15.1 (receipts/21); D3 15.2 and its sweep vs processor 16be6768 (receipts/11, 12, 40, 41, 44) | R380-3 | 816c3b742940b9ac8d160ff03e05553a47e5e66d |
| RTL | CLEAN | D3 5.1 `RETRY_BACKOFF_CYC_P` vs top `CLK_HZ_P` `:91/:93/:129`; D3 6.1/6.3 DR2c FSM; 15.2 rows vs pinned `gen_ucode.py`, top `:2448-2451`, arbiter `:13-18`, shadow `:117-122/:865-895` (receipts/11, 40, 43) | R380-3 | 816c3b742940b9ac8d160ff03e05553a47e5e66d |
| Robustness | CLEAN | DR2c-carrier exhaustion and recovery paths on all four pages vs FASTCONNECT 9.2 next-state and Recovery line; producer vs firmware exhaustion composition; BACKOFF value range | R380-3 | 816c3b742940b9ac8d160ff03e05553a47e5e66d |
| Tests | UNCLEAN (F1) | sweep detection power (receipts/12); D3 18.1/18.2 negative controls vs FASTCONNECT §16 Recovery/healed-outage; checkbox states (receipts/20); gates (receipts/30); anchors (receipts/31) | R380-3 | 816c3b742940b9ac8d160ff03e05553a47e5e66d |
| Docs | UNCLEAN (F1) | the four delta pages; D3 `:2364-2386` sweep text; 15.2 row wording; carrier wording and 9.2 links; residual alarm/forgiveness search | R380-3 | 816c3b742940b9ac8d160ff03e05553a47e5e66d |

## Real limits

- **Manager bank receipts.** I found none for this head in public state:
  - the evidence tree `6cf46c2a:review-evidence/70-r1` holds the round-1 author logs only (`receipts/61`);
  - no manager evidence comment had been posted on #70 or PR #610 when I polled at 07:11 UTC.

  This review does not rely on those banks and did not run them.
- **Hosted checks at 07:11 UTC** (`receipts/60`, `receipts/62`):
  - completed successfully: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `wire-accountability`, `verilator-lint`, and Yosys shards 0-3;
  - still in progress: the `rtl-fast`, `docs`, `elaborate` and `rtl-full` workflows, including `docs-check`, `elaborate`, `yosys-elaboration` and Verilator shards 0-4;
  - skipped, so not executed evidence: `Physical gPTP`.

  None of these is relied on here. The manager owns hosted and act acceptance.
- **Live `dev` has moved.** It was `54ce877371ee6e8878cf67294e86c2a8481b62f6` per the assignment, not the source base `c0723222`. This review says nothing about the final current-dev candidate.
- **No simulation or mutation.** None was run, because the delta is documentation only. The scoped Verilator was not used, so its identity was not checked. The only probes were text fixtures under the packet's scratch directory.
- **Milan and IEEE clause text** was not re-read. The delta changes no clause interpretation.
- **No hardware.** Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.
- **Clone state.** The clone was left at exact head bytes:
  - HEAD, tree and index file digest `f37bb968...` are the same before and after;
  - the index entries equal HEAD's tree;
  - porcelain is empty;
  - all four gitlinks are unchanged, and the processor checkout is clean at `16be6768` (`receipts/00`, `receipts/90`).

## Pending manager duties

- Publish this report and obtain R381-3.
- Route F1 to the executor. After the fix:
  - Conformance, Tests and Docs must be covered again at a head that includes it;
  - RTL and Robustness are banked at `816c3b74` unless their scope is touched.
- Let the in-progress hosted workflows finish at the exact head, and own hosted and act acceptance.
- Publish the static, builder and native bank receipts for this head.
- At the merge turn, build and validate the current-dev candidate against live `dev` (`54ce8773`).
- Later, not this lane: DR3a ratification after lane 1 measures.

R380-3 FINISHED
