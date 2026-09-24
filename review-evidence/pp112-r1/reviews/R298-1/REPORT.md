[R298] NEGATIVE - exact head 73a5478784bd861f8c8d33c0d1619594390b9529

# R298-1 internal independent review: issue #112 / PR #114

Scope: Mister-M-alt/protocol-processor-control-plane-avb-milan PR #114 (closes #112), exact head
`73a5478784bd861f8c8d33c0d1619594390b9529`, tree `98a8591b6c716027e03f6ef12c1433036471ff0d`,
source base `939c143333d11e2378a514f1c7b6abd4c3259bfd`. The review ran in a cleared context in an
isolated detached clone. It covered the following, in order: the repository conventions (the
repository has no AGENTS.md or CONTRIBUTING.md, so the conventions come from README.md,
docs/README.md, docs/guides/hdl-engineer.md, hdl.yml and scripts/run_suites.sh); the issue's
frozen acceptance; the manager's assignment and decision comments (issue #112 comments 5816023315
and 5816726610, and parent kebag-logic/milan-fpga comment 5816014072); the interface authorities
(10 §6.3, F02.10, the integrator guide and the top-level port comments); the full diff and
history; and the public evidence at
kebag-logic/milan-fpga@5891d560424620234a23a7c4f0d01ead09a6abfe `review-evidence/pp112-r1`.

## Verdict

**NEGATIVE.** The fix does what it sets out to do for the declaring source. A source's own
refused re-declaration never pulses a grant, at the processor top or in the engine, in every
direction, at every phase and shape tested. The stale-evaluation mutants are killed.

The fix also introduces a new cross-source licence pulse (F1). When any lower-index source is
accepted with a new declaration, including an identical re-declaration, that source becomes
"pending". The admission rules treat a pending source as absent from the running sum. The
first round after acceptance can therefore grant a higher-index source that the current
declarations refuse. At the default shape that source is published admitted for 8 or 16
clocks, its talker declaration swaps from Failed to Advertise, and with a Ready registration
ACTIVE is high for 7 or 15 clocks. So ACTIVE AND `srp_sr_admitted_o`, the confirmed-admission
gate that the #551 decision prescribes, opens for a refused stream. The pre-fix base shows
zero such cycles under the same stimulus. The manager's own receipt also reports that the
parent consumer idiom gates fail at this head (F2, acceptance 5).

## Findings

### F1: MAJOR. A pending re-declaration releases its capacity and licenses a refused higher-index source

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Location:**
  - `hdl/srp/KL_srp_admission.sv:177-179`: `fit_w`/`refuse_w` treat a source without a
    valid slope as contributing nothing.
  - `hdl/srp/KL_srp_admission.sv:206-226`: the restart keeps unrelated grants, and the next
    completed round publishes `wgrant_now_w`, which was computed without the pending source.
  - `hdl/srp/KL_srp_top.sv:755-758`: every accepted declaration strobes, identical ones included.
  - `docs/architecture/10_srp_engine.md:289-300`: "Pending evaluation contributes neither a
    grant nor a ceiling refusal … A refused TSpec never produces a grant pulse."
- **Authority:** 10 §6.3 and the admission banner say admission is greedy in index order
  against the 75 % ceiling, and that a refused source never displaces a lower-indexed grant.
  F02.10 defines `sr_admitted[src]` as admitted against the Σ-slope ceiling. Issue #112
  acceptance 1 is the intent that the verdict belongs to the current declarations. The parent
  #551 decision (comment 5816014072) wants "cannot open" claims to become true, with ACTIVE
  AND the real grant as the confirmed licence.
- **Evidence (reviewer probes, exact head, pinned Verilator 5.050):**
  - Unit level, head's own `srp_admission_wrap`. Source 0 and source N-1 both declare a
    7770-byte TSpec at 1 Gb/s (the engine probe below uses 700 bytes at 100 Mb/s): each fits
    alone, the pair does not. At settle, source 0 is
    granted and N-1 is refused. Source 0 then re-declares:
    - identically: N-1 is published admitted for 8 or 16 cycles at N=8 (all 8 phases), and
      4 cycles at N=2;
    - with a grow that still dominates: same result;
    - twice, 5 cycles apart: the pulse survives the second invalidation (10 cycles at N=2).
    - The legitimate shrink control (source 0 frees capacity) produces no violation.
    - The live Σ of per-source granted slopes never exceeded the ceiling.
    - Receipts: `receipts/probe_cross_source/head-N2.log` and `head-N8.log`, 240 of 32832
      checks failing at N=8.
  - Engine level, real `KL_srp_top`, service port and Listener PDUs. Source 0 is admitted and
    Ready; source 1 or 7 is refused and declared Talker Failed. Source 0 then re-declares
    identically. In each of 32 runs (2 victim sources × 8 phases × Listener Ready or
    AskingFailed), the refused source is published admitted for 8 or 16 cycles, and
    `tk_decl_state` swaps to Advertise for 8 or 16 cycles. With a Ready registration, ACTIVE
    is high for 7 or 15 cycles. Receipt: `receipts/probe_srp_top/head.log`, 80 of 192 checks
    failing.
  - The same bench against the base RTL gives 0 admitted, 0 Advertise and 0 ACTIVE cycles on
    the refused source, 192/192 passing (`receipts/probe_srp_top/base-hdl.log`). This is a
    regression introduced by the invalidation.
  - Within 1000 ms after the pulse, no Talker Advertise frame for the refused stream was
    observed on the wire. The exposure is on the published levels (`srp_sr_admitted_o`,
    `srp_active_o`, `tk_decl_state`), not a confirmed MRPDU.
- **Impact:** A refused stream gets a licence window (ACTIVE AND real grant) every time any
  lower-index source is accepted with a declaration. The engine's own talker path re-declares
  on each DA-gate open, and the external svc face can re-declare at any time. That is the
  #551 hazard class, moved from the declaring source to its higher-index neighbours. It
  contradicts the new 10 §6.3 claim. Neither the unit suite nor the engine suite can see it:
  the per-cycle oracle checks only each source's own slope against the ceiling, and every
  re-declaration case runs a single source.
- **Required outcome:**
  - No `sr_admitted[s]` may rise from a round in which any requested source's current slope
    was still pending. Grants may only be retired until every requested source has been
    evaluated in a completed round. An equivalent rule is acceptable if it guarantees that
    every newly published grant is the greedy result over all current declarations.
  - Preserve the legitimate capacity-reuse case: a shrink or withdrawal still admits the
    refused source once the round is evaluated.
  - Add a test with at least two competing sources: identical and changed re-declaration of
    a lower-index source while a higher-index source stands refused. It must be checked every
    cycle against a current-declaration greedy oracle, at unit and engine level, with a
    mutant restoring "pending = absent" that fails it.
  - Correct 10 §6.3, the integrator guide and the port comments if the latency or window
    statements change.
- **Verification:** Re-run `scripts/probe_cross_source/run.sh` (N=2 and N=8) and
  `scripts/probe_srp_top/run.sh`. Expect 0 refused-grant, 0 refused-Advertise and 0
  refused-ACTIVE cycles, with the shrink control still admitting. Then re-run the unit shapes
  1/2/3/5/8, `srp_top`, `pp_top`, and the author's and this review's mutants.

### F2: MINOR. Parent consumer idiom gates fail at this head (manager receipt)

- **Lens:** Tests.
- **Location:**
  - `tb/srp_top/sim_main.cpp:1118-1120`: three multi-declarator declarations
    (`:325` is another new one; the receipt counts three).
  - `tb/srp_top/sim_main.cpp:1060`: `check_redeclaration_never_publishes_a_stale_slope`,
    about 108 lines.
  - `tb/srp_admission/mutants.py:11`: `def main():` has no annotation or docstring.
- **Authority:** Issue #112 acceptance 5 ("The parent consumer gates stay green with this head
  as the processor gitlink"). Manager comment 5816726610 on issue #112 reports that at
  `73a54787` the parent's `check_cpp_idiom` (Rule 11: 3 multi-declarator declarations and 1
  long function in `tb/srp_top/sim_main.cpp`) and `check_py_idiom` (Rule 12: one unannotated,
  undocumented public function in `tb/srp_admission/mutants.py`) fail. The PR body states
  that both prescribed parent consumer checks pass.
- **Impact:** Acceptance 5 is not met at this head, and the PR body's gate claim is
  inaccurate.
- **Required outcome:** Fix the test code with no behaviour change: same checks, counts and
  results. The manager's A266 round already carries this.
- **Verification:** Manager receipt of the parent consumer gates at the new head. This review
  did not run parent gates, as instructed.

### Suggestions (do not affect the verdict)

- **S1 (Tests):**
  - `scripts/run_suites.sh` runs `make` in `tb/srp_admission`, which is N=8 only.
  - The 1/2/3/5-source shapes that 10 §6.3 and the suite README quote, including the N=1
    case, are not gated in CI.
  - Consider making `make` run `shapes`, or adding a CI step.
- **S2 (Robustness, Docs):**
  - Declarations or withdrawals spaced less than one round apart, from any sources, keep
    restarting the admission round. While that continues, no grant can rise, optimistic
    windows keep extending, and `sum`/`over_limit` stay at their old snapshot.
  - The bound is stated as holding "without another declaration/withdrawal", so this is
    documented.
  - Consider stating the service-rate assumption in the integrator guide next to the svc face.
- **S3 (Docs):** `hdl/top/protocol_processor_top.sv:523` still says
  `srp_granted_slope_bps_o` has the "same optimistic lag". The neighbouring
  `srp_sr_admitted_o` comment no longer uses that framing. Suggest "zero until the real
  grant; follows `srp_sr_admitted_o`".
- **S4 (RTL):**
  - Mutant A5 (dropping `!invalid_w[aidx_r]` from `fit_w`) survives every suite.
  - Under the port contract it is equivalent. The invalidation cycle takes the restart
    branch, which ignores `fit_w`. `slope_valid_r` is already cleared by the time a
    withdrawn request is next visited.
  - The term is defensive. Consider saying so in a comment.

## What was verified clean

Each item gives the claim, the evidence and the result.

- **Own-source stale slope, grow past ceiling (acceptance 1/2).**
  - Evidence: reviewer processor-top probe through the real svc face. The previous TSpec is
    224 B (admitted); the source then re-declares at 20000 B, either directly or after a
    withdrawal. Sources 0/1/7, 8 phase offsets.
  - Result: head gives 0 admitted cycles after gate acceptance in all 48 runs. Base
    reproduces the bug: 8 cycles after withdraw-then-declare, and 9–23 cycles after a direct
    re-declaration (`receipts/probe_pp_top/{head,base}-hdl.log`).
- **Admitted shrink latency (acceptance 2).**
  - Evidence: unit shapes N=1/2/3/5/8 and engine M=8 (`receipts/focused/latency-summary.txt`).
  - Result: N=1 gives 4 clocks; N=2 gives 4/6; N=3 gives 6/9; N=5 gives 5/10/15; N=8 gives
    8/16/24. The engine gives 8/16/24 from gate acceptance. At the F01.5 default of 100 MHz
    that is 80–240 ns, and 160–480 ns at 50 MHz, matching 10 §6.3.
  - Every first grant lands on a round-completion cycle.
- **Identical re-declaration, own source.**
  - Evidence: unit and engine suites.
  - Result: the grant retires at acceptance and returns after 8/16/24 clocks. This is
    intended by acceptance 1. It is also the trigger for F1's cross-source effect.
- **Stale-evaluation mutants (acceptance 3).**
  - Evidence: the author's campaign, re-run (`receipts/author_mutants`).
  - Result: controls pass. The mutant fails 184/5252 at N=2 and 4032/723046 at N=8, matching
    the suite README.
- **Reviewer mutants.**
  - Evidence: `receipts/mutants_r298/summary.txt`.
  - Result: A1 (no stage invalidation), A2 (no final override), A3 (no grant retire),
    A4 (no round restart), A6 (stage-1 only) and T1 (top strobe removed) are all killed by
    the head suites. A5 is equivalent (S4).
- **Aggregate and granted slope during invalidation.**
  - Evidence: unit suite checks, the reviewer probe's per-cycle live-sum check, and RTL reading.
  - Result: `granted_slope` is 0 while pending. `sum`/`over` hold the previous snapshot. The
    live Σ never exceeded the ceiling in any probe. Grants only rise at round publication,
    so `sum_r` is always ≥ the live Σ.
- **Optimistic ACTIVE window.**
  - Evidence: RTL (`opt_cnt_r <= 2'd2`, unchanged) and the srp_top H window/ACTIVE-equation
    checks.
  - Result: still three completed rounds. It is now counted from a restarted round, and
    other sources' invalidations can extend it; 10 §6.3 documents both. The banner's former
    "one full round" text was inaccurate and is corrected.
  - At N=1 the grant latch and the window drop fall on the same edge by derivation. No
    engine suite covers N=1.
- **No port change (acceptance 4).**
  - Evidence: RTL diff and the author's interface-check receipt.
  - Result: only port comments change in `protocol_processor_top.sv`. `KL_srp_admission`
    gains an internal `invalidate_i`.
- **Suites (acceptance 5, source side).**
  - Evidence: `receipts/focused/summary.txt`.
  - Result: `srp_admission` N=1/2/3/5/8 (683 / 5252 / 20053 / 123286 / 723046),
    `srp_top` 735, `srp_stream_fsms` 1068 and `pp_top` 1454 all pass at head. This matches
    the published suites log, whose hash was verified.
- **Lint and doc gates.**
  - Evidence: `receipts/doc_gates`.
  - Result: tree-flag lint of `KL_srp_admission` (N=1/2/3/8), `KL_srp_top` and
    `protocol_processor_top` has 0 warnings. `check-links`, `check-matrix` and
    `gen_matrix --check` are OK.
- **Hosted checks.**
  - Evidence: `receipts/public_evidence/hosted-check-runs.tsv`.
  - Result: `suites`, `docs-gates` and `portability` completed with success at the exact
    head, in two workflow runs (push and pull_request). The commit-status API shows no
    legacy statuses. The manager owns hosted acceptance.

## Prior public review findings

This is round 1. No review findings were posted on PR #114 before this pass; only the two
review-start notices existed. A concurrent independent report from the other reviewer
appeared on the PR during this review. It was deliberately not read, to keep the two reviews
independent, so nothing in this report depends on it.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #112 acceptance 1–5; parent #551 decision 5816014072; 10 §6.3, F02.10, admission/top banners; processor-top and engine probes at head and base | R298-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |
| RTL | UNCLEAN (F1) | `KL_srp_admission.sv` full, `KL_srp_top.sv` service plane/optimistic window/strobe, talker FSM swap/ACTIVE, `protocol_processor_top.sv` SRP adapter and ports; tree-flag lint; 7 reviewer mutants | R298-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |
| Robustness | UNCLEAN (F1) | cross-source re-declaration, repeated/rapid invalidation, withdraw, identical re-declaration, N=1/2 aliasing, livelock under dense declarations (S2), live Σ bound | R298-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |
| Tests | UNCLEAN (F1, F2) | `tb/srp_admission` (sim_main, wrap, Makefile, mutants.py, README), `tb/srp_top` H section and wrap, focused runs, both mutant campaigns, manager receipt 5816726610, CI runner coverage (S1) | R298-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |
| Docs | UNCLEAN (F1) | 10 §6.3 freshness/latency/window/accounting text, integrator guide table, top port comments (S3), `srp_top` banner, suite READMEs, MODULE_MATRIX, syn/ooc README | R298-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |

## Real limits

- Physical calibration was not run, and there was no hardware. Field skips are not hardware
  proof.
- Suite and probe execution was focused only: `srp_admission` (5 shapes), `srp_top`,
  `srp_stream_fsms` and `pp_top`. The full 33-suite bank, portability/Yosys, parent, builder
  and gPTP banks were not run by this review. Those rely on the published receipts, whose
  hashes were verified against the evidence manifest, and on the manager.
- The parent consumer gates were not run here. F2 rests on the manager receipt.
- The area figures (7566 → 7334 LUTs, 10485 → 10464 registers) were not reproduced; no
  vendor synthesis was run.
- The wire-level consequence of F1 (MRPDU churn) was not observed within 1000 ms. The finding
  rests on the published levels.
- `scripts/run_focused.sh` was amended after its run only to take an explicit work directory,
  which changes no behaviour. Receipt logs have local paths redacted to `<packet>`,
  `<pinned-verilator-root>`, `<home>` and `<review-clone>`.
- After the probes, the review clone was verified byte-identical to the exact head: HEAD,
  tree and index tree match; there are no untracked or ignored files; 243 tracked entries
  match in blob bytes and modes. The repository has no submodule gitlinks
  (`receipts/clone/verify.txt`).

## Pending manager duties

- Carry F1 (and F2 via A266) to the author. Assign the re-review at the new head.
- Build the merge-turn current-dev candidate. The source base is `939c143`; live dev is
  `57456af96b3127b9d309a995bbbd35a6113ce52d`. Run the full static, builder and native banks
  there.
- Run the parent consumer gates at parent dev with the candidate processor gitlink
  (acceptance 5).
- Own hosted and act acceptance, and physical calibration when scheduled.
- Reconcile this report with the independent R299-1 report only after publication.

## Reproduction

Set `VL_PINNED` to the pinned 5.050 binary. Then:

- `scripts/run_focused.sh <clone> scripts/vl8.sh receipts/focused <work>`
- `scripts/probe_cross_source/run.sh <head-tree> scripts/vl8.sh <work> {2|8}`
- `scripts/probe_srp_top/run.sh <head-tree> scripts/vl8.sh <work> [<base-tree>]`
- `scripts/probe_pp_top/run.sh <head-tree> {<head-tree>|<base-tree>} scripts/vl8.sh <work>`
- `scripts/mutants_r298.py <head-tree> scripts/vl8.sh <work> <out>`
- `scripts/verify_clone.sh <clone> <head> <tree>`

Trees are `git archive` extractions of the exact head and base.

R298-1 FINISHED
