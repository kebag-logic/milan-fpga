[R299] NEGATIVE - exact head 73a5478784bd861f8c8d33c0d1619594390b9529

# R299-1 external independent review: processor issue #112 / PR #114

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `73a5478784bd861f8c8d33c0d1619594390b9529`, tree `98a8591b6c716027e03f6ef12c1433036471ff0d`
- Source base `939c143333d11e2378a514f1c7b6abd4c3259bfd`. The live parent dev at the merge turn (`57456af96b3127b9d309a995bbbd35a6113ce52d`) is the manager's responsibility and was not exercised here.
- Reviewer role: external independent reviewer, working in a cleared context in its own detached clone. It made no GitHub writes, no source edits and no commits.
- Simulator: the pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), verified before use.

## Verdict

**NEGATIVE.** The fix does what the issue asks for the re-declared source itself:
- A 224 → 20000-byte re-declaration never pulses a grant, even with a second source concurrently requesting. At base it pulses 16 times out of 16.
- Shrink and identical re-declarations grant after 8, 16 or 24 clocks at eight sources.
- Every stale-evaluation mutant I built is killed.

However, the fix treats a still-requesting source whose new slope is pending as absent from the Σ walk. That hands the pending source's capacity to higher-index sources for one or two rounds. A source that the greedy walk refuses both before and after another source's identical or shrinking re-declaration now gets:
- `srp_sr_admitted_o`,
- `srp_active_o` AND `srp_sr_admitted_o` (the confirmed gate the parent #551 decision prescribes),
- an internal Talker Failed → Advertise → Failed swap,
- when the pulse straddles a T-MRP-JOIN transmit opportunity, a Talker Advertise on the wire.

Base shows none of this. This is the licence-pulse hazard #112 exists to remove, moved to a different source, and it contradicts the new documentation's "A refused TSpec never produces a grant pulse". One MAJOR finding (F1) is open, so all five lenses are UNCLEAN.

A MINOR finding (F2) is also retained from the manager's public receipt: the new test code fails the parent consumer idiom gates, so issue acceptance 5 is not met at this head.

## Reconstruction (order followed)

1. The repository has no `AGENTS.md` and no `CONTRIBUTING.md`. I read `README.md` (build/check commands, submodule contract) and `docs/README.md` (single-source rules, editing workflow).
2. Issue #112: the body with its five frozen acceptance items, the assignment comment and the REVIEW READY comment. Decision context: kebag-logic/milan-fpga#551 comment 5816014072. Option (a) applies: the processor owns the fix, with no new port; the grant stays low until the new TSpec has been evaluated. The parent then relies on ACTIVE AND the real grant, and #553's "cannot open" claims are meant to become true.
3. Interface authorities: `docs/architecture/10_srp_engine.md` §6.3 (new `sec-10-admission-freshness`), `02_interfaces.md` F02.10 (`sr_admitted`, `granted_slope_bps`), `docs/guides/integrator.md` port table, and the port comments in `hdl/top/protocol_processor_top.sv` and `hdl/srp/KL_srp_top.sv`.
4. `git diff 939c1433..73a54787`: 16 files, +636/−25, in one commit. RTL: `KL_srp_admission.sv`, `KL_srp_top.sv` and top port comments. Tests: new `tb/srp_admission`, extended `tb/srp_top` H scenario. Docs: 10 §6.3, integrator guide, module matrix. Synthesis: `syn/ooc/srp_ooc.tcl`.
5. Public executable evidence: kebag-logic/milan-fpga@5891d560 `review-evidence/pp112-r1`. I checked eight receipts against the published MANIFEST.json hashes (`receipts/evidence-check.txt`), and all match. There are no manager evidence comments on the issue or PR beyond the review-start comments.

## Findings

### F1: a pending re-declaration releases its capacity, so a refused source gets a real grant pulse (MAJOR)

- **Severity:** MAJOR
- **Lenses:** Conformance, RTL, Robustness, Tests, Docs
- **Location:**
  - `hdl/srp/KL_srp_admission.sv:177-179`: fit/refuse require `slope_valid_r`, so a pending but requesting source contributes neither grant nor Σ.
  - `hdl/srp/KL_srp_admission.sv:215-216`: the next completed round publishes `wgrant_now_w` for every source.
  - `hdl/srp/KL_srp_top.sv:447`, consumed at `hdl/srp/KL_srp_talker_fsm.sv:439-441,541,803`: `adm_fix_w` swap and `active_o`.
  - Docs: `docs/architecture/10_srp_engine.md:282-283,289-290,299,328-330`; `hdl/srp/KL_srp_admission.sv:31-32,52`; `docs/guides/integrator.md:285`.
- **Authority:**
  - Issue #112, acceptance 1 and 4, which say ACTIVE, `sum_slope` and `granted_slope` "behave as documented".
  - The #551 decision: a refused TSpec must get no licence pulse, and the parent consumer gates ACTIVE AND the real grant.
  - 10 §6.3's own statement "A refused TSpec never produces a grant pulse".
  - The greedy rule in the admission banner: a refused source is admitted "the moment capacity frees". Here no capacity is freed; the lower-index source is still declared and requesting.
- **Evidence (all reproducible with the scripts in `probes/`):**
  - Unit level (`receipts/unit-probe-{head,base}-N{2,8}.log`): source 0 is admitted at about 700 Mb/s and source N−1, at about 131 Mb/s, is refused (Σ 830.7 Mb/s > 750 Mb/s). Source 0 is re-declared identically, or shrunk to about 643 Mb/s, where source N−1 is still refused. At every slope-sampling phase:
    - head: source N−1 grants in 8 of 8 phases for identical and 8 of 8 for shrink at N=8 (2 of 2 each at N=2), for up to 16 clocks;
    - base: 0 in every phase.
  - The same probe's P1 half (the parent reviewers' stale-grant idea at processor level, with two sources concurrently requesting 224 → 20000 bytes): head 0 of 16, base 16 of 16. The fix itself works.
  - End to end through the real service port and real Listener Ready PDUs (`receipts/top-probe-{head,base}.log`, 100 Mb/s port): source 0 is at about 70 Mb/s and admitted; source 7 is at about 15.5 Mb/s, has Listener Ready, and is Talker Failed. After an identical or shrinking re-declaration of source 0, at all 8 phases:
    - head: `srp_sr_admitted_o[7]` high for 8 or 16 clocks; `srp_active_o[7]` AND `srp_sr_admitted_o[7]` high for 7 or 15 clocks; `tk_decl_state[7]` = Advertise for 8 or 16 clocks. That is 16 of 16 runs, with 48 FAIL checks out of 80;
    - base, same bench: 0 of 16 runs, 80 of 80 PASS.
  - Wire (`receipts/top-wire-probe-{head,base}.log`): the identical re-declaration is placed k = 1..40 clocks before a T-MRP-JOIN tick.
    - head: a Talker Advertise vector with source 7's stream ID is transmitted for k = 1-5, 7 and 8 (7 of 40);
    - base: 0 of 40.
    - Source 7 is refused before and after, and it settles back to Failed.
- **Impact:**
  - A stream whose steady-state verdict is refused is licensed through the exact confirmed gate the parent is told to use. So the #553 "cannot open" claims stay false after #112 merges; the path is just different.
  - `srp_over_limit_o` clears and `srp_sum_slope_bps_o` drops to the refused source's slope for that round, while the re-declared source is still in its optimistic window.
  - The wire can carry a spurious Talker Advertise → Failed flap for the refused stream.
  - This is a regression against base for identical and shrinking re-declarations.
- **Required outcome:**
  - While a requesting source's current-declaration slope is pending, no published round may grant another source that the greedy walk over the current declarations would refuse. Only a withdrawal, or an evaluated shrink, may release capacity. One option is to freeze other sources' grants, or hold round publication, until every requesting source has a valid slope; the design choice belongs to the author.
  - Add a test with at least two concurrently requesting sources, the lower one admitted and the higher one refused before and after an identical and a shrinking re-declaration of the lower one. It must run at all phases, at unit level and through `tb/srp_top`, and assert on every clock: no grant, no ACTIVE∧grant and no declared Advertise for the refused source.
  - Add a mutant that restores "pending = absent" and show that it fails that test.
  - Make the per-cycle oracle in `tb/srp_admission/sim_main.cpp:40-41` judge the grant against the Σ context, not the source's slope alone.
  - Correct 10 §6.3, the integrator row and the admission banner so they state the cross-source rule.
- **Verification:** at the fixed head, `probes/run_unit_probe.sh` (N=2 and 8), `probes/run_top_probe.sh` (default probe) and `run_top_probe.sh … top_wire_probe.inc probe_wire join` must all report 0 FAIL, and P1 must stay at 0 pulses. The author's suites and a new mutant campaign must pass or kill as stated.

### F2: the new test code fails the parent consumer idiom gates, so acceptance 5 is not met (MINOR)

- **Severity:** MINOR
- **Lenses:** Tests, Conformance (issue acceptance 5)
- **Location:**
  - `tb/srp_top/sim_main.cpp:325,1118-1120`: multi-declarator declarations, all new at this head; base has none.
  - `tb/srp_top/sim_main.cpp:1060-1167`: `check_redeclaration_never_publishes_a_stale_slope`, 108 lines.
  - `tb/srp_admission/mutants.py:11`: `def main():` has no annotation and no docstring.
- **Authority and evidence:**
  - Issue #112 acceptance 5: "The parent consumer gates stay green with this head as the processor gitlink".
  - The manager's public receipt on issue #112 (comment 5816726610, posted during this review). At `73a54787` the parent `check_cpp_idiom` (Rule 11) fails on three multi-declarator declarations and one long function in `tb/srp_top/sim_main.cpp`, and `check_py_idiom` (Rule 12) fails on one unannotated, undocumented public function in `tb/srp_admission/mutants.py`.
  - I confirmed the cited constructs in the source. I did not run the parent gate scripts, which live in the parent repository.
- **Impact:** the processor pin cannot move in the parent at this head. The published author evidence ran only the parent source-list and pp_shadow checks, not the idiom gates.
- **Required outcome:** the manager's round-1b assignment (A266): test code only, with the same checks, counts and results.
- **Verification:** the parent idiom gates pass with the new head as gitlink (manager receipt), and the processor suites keep their check counts.

### S1: two port comments still describe the old semantics (SUGGESTION)

- **Severity:** SUGGESTION
- **Lens:** Docs
- **Location:** `hdl/top/protocol_processor_top.sv:523` and `hdl/srp/KL_srp_top.sv:213-215`.
- **Evidence:** the top port comment for `srp_granted_slope_bps_o` still ends "same optimistic lag", but the neighbouring `srp_sr_admitted_o` comment no longer describes an optimistic lag. The `KL_srp_top` port comments for `sum_slope_bps_o` and `over_limit_o` do not say "round-latched" or "pending is not refusal", which the top-level comments and the integrator guide now say.
- **Impact:** only reader confusion; the architecture page and the integrator guide are correct.
- **Required outcome:** align the wording. This does not block the verdict.

### S2: the area reduction is unexplained (SUGGESTION)

- **Severity:** SUGGESTION
- **Lenses:** RTL, Docs
- **Artifact:** published `author/area-comparison.json`. The admission block goes from 782 to 503 LUTs even though logic was added (engine 7566 → 7334).
- **Evidence:** I did not re-run synthesis, so this was not reproduced here.
- **Impact:** a large unexplained drop could hide a synthesis-only trim. The simulation results above are not affected.
- **Required outcome:** a one-line explanation in the handoff or `syn/ooc/README.md`. This does not block the verdict.

## Focus items judged

| Item | Result | Evidence |
|---|---|---|
| Refused grow (224 → 20000 B), ≥2 sources: no grant pulse | holds for the re-declared source at every phase, alone or with a second source requesting | author suites; `unit-probe-*` P1: head 0/16, base 16/16 |
| Admitted shrink: grant with measured latency | 8/16/24 clocks at N=8 unit and service port (80–240 ns at 100 MHz, 160–480 ns at 50 MHz); N=1: 4; N=2: 4/6; N=3: 6/9; N=5: 5/10/15. These exactly match the 10 §6.3 table | `head-srp_admission-shapes.log`, `head-srp_top.log` LATENCY lines |
| Stale-evaluation mutants | author M1 plus reviewer M2 (stage-1 invalidation), M3 (stage-2), M4 (stage-3 override), M5 (no round restart), M6 (no immediate retire): all KILLED by adm N=2, adm N=8 and srp_top. M7 (top strobe removed) is killed by srp_top and survives the unit bench, as expected because that bench has no top. Controls pass | `receipts/mutants-summary.txt`, `receipts/mutants/` |
| Identical re-declarations | own grant drops and returns after 8/16/24 clocks as documented; **cross-source licence (F1)** | suites; `top-probe-head.log` |
| Aggregate/granted slope during invalidation | per-source slope is zero while pending, as documented; sum/over hold the previous snapshot and discard the partial round, as documented; **the next round's snapshot omits the pending requester and can admit a refused source (F1)** | unit suite checks; probes |
| Optimistic ACTIVE window unchanged | 3 completed rounds, restarted by a new declaration, checked every clock by the srp_top H scenario; the talker sees `opt_r | grant` | `KL_srp_top.sv:447,781-791,864-868`; `head-srp_top.log` |
| No top-level port change | port declarations identical base → head, comments only | diff of `protocol_processor_top.sv` and `KL_srp_top.sv` port lists; published `interface-check.log` |
| Docs 10_srp_engine / port comments | latency and window text accurate; "A refused TSpec never produces a grant pulse" contradicted (F1); stale comment wording (S1) | reading and probes |

## Issue acceptance mapping

| # | Status at this head |
|---|---|
| 1 | Met for the re-declared source. The verdict for another source can still be published from a Σ that omits a standing requester whose new slope is pending (F1) |
| 2 | Both directions, several source indices and all phases are covered, but always with a single declared source except the unit's final fresh-declare competition. No concurrent competing-source case (F1, Tests) |
| 3 | Met, and strengthened by the six reviewer mutants |
| 4 | Ports unchanged. ACTIVE/window as documented. Documented grant/aggregate behaviour contradicted by F1 |
| 5 | Processor suites green per published evidence; I re-ran the SRP suites. **Not met at this head:** per manager receipt 5816726610, the parent idiom gates fail on the new test code (F2). The parent consumer gates at parent dev remain manager receipts |

## Commands executed (all in the foreground, at most 4 parallel jobs)

- Scratch exports of the exact head and base trees (`git archive`); the review clone was never modified.
- `make shapes` in `tb/srp_admission` at head: 683 / 5252 / 20053 / 123286 / 723046 checks at N = 1/2/3/5/8, 0 FAIL, rc 0.
- `make run` in `tb/srp_top` at head: 735 checks, 0 FAIL, rc 0.
- Scoped Verilator lint with the flags of `scripts/lint_hdl.sh` for `KL_srp_admission`, `KL_srp_top` and `protocol_processor_top`: rc 0, no warnings.
- `make links matrix modmatrix` on the scratch head: 843 links OK; 115 REQ rows and 17 GAP findings OK; 92 module rows, 0 untested.
- Reviewer probes and mutation campaign: see `probes/` and `receipts/`.
- Clone integrity (`receipts/clone-integrity.txt`): HEAD and tree exact, index and worktree clean, every tracked blob hash and mode matches HEAD, 0 gitlinks (the repository has no submodules).
- Hosted checks at the exact head (`receipts/hosted-check-runs.txt`): `docs-gates` and `portability` completed with success in both runs; `suites` was still `in_progress` in both runs at capture. It is not counted as evidence.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | issue #112 acceptance 1–5; manager receipt 5816726610; #551 decision 5816014072; 10 §6.3; F02.10; greedy/ceiling rule; unit and top probes | R299-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |
| RTL | UNCLEAN (F1) | `KL_srp_admission.sv` (all of it: validity pipeline, override loop, restart branch, publish); `KL_srp_top.sv` invalidation strobe, sole `adm_*` write site, window aging; talker FSM consumption of `sr_admitted_i`; scoped lint; N=1..8 shapes | R299-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |
| Robustness | UNCLEAN (F1) | all sampling phases; both directions; identical; one-cycle withdraw; rapid changes; saturation; concurrent two-source cases; join-tick-straddling wire probe; round starvation under back-to-back ops (bounded and documented, no finding) | R299-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |
| Tests | UNCLEAN (F1, F2) | `tb/srp_admission` (sim_main, wrap, Makefile, mutants.py, README); `tb/srp_top` H scenario and wrap probes; 7 mutants × 3 benches plus controls | R299-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |
| Docs | UNCLEAN (F1; S1/S2 non-blocking) | 10 §6.3 freshness section; integrator guide rows; top and SRP port comments; admission banner; tb READMEs; MODULE_MATRIX; `syn/ooc` README/tcl; link/matrix gates | R299-1 | 73a5478784bd861f8c8d33c0d1619594390b9529 |

## Prior public review findings at this head

When this review started, and when I rechecked after writing the verdict and ledger, PR #114 had no posted review, no review comments and no reviewer finding. The only comments were the two review-start notices (R298-1, R299-1). No reviewer finding exists to resolve or retain.

During the review the manager posted one public receipt on issue #112 (comment 5816726610, assignment A266): the parent consumer idiom gates fail at `73a54787`. It is **retained** at this head as F2. The fix is assigned to round 1b and was not published before this review ended.

## Real limits

- I did not run the full 33-suite bank, `lint_hdl.sh` over all 40 tops, Yosys or the native/builder banks, parent consumer gates, or Vivado (not allowed or not available). I relied on the published evidence, which I verified by hash, and re-ran only the two SRP suites, scoped lint and the link/matrix gates.
- The wire probe uses the bench's time compression (1 ms = 40 clocks, T-MRP-JOIN = 8000 clocks). The fraction of re-declaration instants that reach the wire is timing-dependent; that the flap exists does not depend on the compression.
- The probes use the 1 Gb/s (unit) and 100 Mb/s (top) port rates with class-A slopes; I did not sweep other port rates.
- Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.
- The hosted `suites` job was in progress at capture; hosted and act acceptance is the manager's.

## Pending manager duties

- Hosted `suites` job completion at the exact head, and hosted/act acceptance.
- Parent consumer gates at parent dev with the eventual processor head as gitlink (acceptance 5); the final current-dev candidate build at the merge turn.
- Parent idiom gate receipts after the A266 round-1b test-code fix (F2).
- Re-review after F1 and F2 are addressed. Merge still requires two independent positive reviews.

## Packet contents

`REPORT.md`, `probes/` (portable scripts: `run_unit_probe.sh`, `cross_source_probe.cpp`, `base_admission_wrap.sv`, `run_top_probe.sh`, `top_cross_source_probe.inc`, `top_wire_probe.inc`, `mutants_r299.py`) and `receipts/` (raw logs, with absolute local paths redacted to `<packet>`, `<clone>`, `<pinned-tool-bin>`, `<pinned-tool-root>`, `<home>`, `<tmp>`). Every publishable file is listed in `MANIFEST.sha256`. `scratch/` is disposable and not published.

R299-1 FINISHED
