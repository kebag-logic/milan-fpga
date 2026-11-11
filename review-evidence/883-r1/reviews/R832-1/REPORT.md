[R832] NEGATIVE - exact head e18c822536ebeaf1cb0f42abea74513501aa26c7

# R832-1: external review of PR #893 (issue #883), the seventh parent pin adoption

- Head under review: `e18c822536ebeaf1cb0f42abea74513501aa26c7`, tree `be1aea4667ad7572f109c68fb492a7c15c45ab56`, branch `883-adopt-processor-801ef228`.
- Source base `46c971fa`; live dev `fa6c094b`. `46c971fa..fa6c094b` touches only `docs/testing/CI_WORKFLOWS.md` and `scripts/act_ci.py`. No file is in common with this PR (`receipts/24_live_dev_overlap.txt`).
- Gitlinks at the head: `protocol-processor` `801ef2283ec793e35a2590fc6593c90313a64041`, `gptp-processor` `1616fc8f062fbf58c35ad31674b5b233207bbdb8`.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. All five were applied at this head.
- Verdict: **NEGATIVE**. One MINOR finding is open (F1, under `Tests` and `Robustness`). Three RESIDUE wording items go to the manager's residue checklist.

## Context reconstructed

I read these in order: AGENTS.md and CONTRIBUTING.md; the issue #883 body, which holds the frozen acceptance items 1 to 5; the `[A768]` TAKEN, STOP and REVIEW READY comments; and the maintainer ruling on the STOP (issuecomment-6805166676, option (b)). Option (b) keeps `gptp-processor` at `1616fc8f` and changes item 1 to "the processor gitlink moves to `801ef228`". I also read the PR body, the #495 rows the PR cites (6758088112, 6731336971, 6758048783 and 6777009988), and the requirement entries they point at. Those entries are NFR-RES-01 (`docs/reference/FR_NFR.md:473`) and the processor's REQ-ADP-011 row (`protocol-processor/docs/00_MILAN_COMPLIANCE_REVIEW.md:424`). Then I read `git diff 46c971fa..e18c8225` commit by commit, and the published author evidence at archive `e99c3d13` (`review-evidence/883-r1`).

The standards text is not in the tree. I checked the clause readings against the clause text the harness and pages quote, against the processor's requirement rows and against the project's earlier decisions (#85: available_index goes to 0 after ENTITY_DEPARTING). I did not re-derive them from the standards documents.

## Executed at this head (my own runs, on scratch copies of this clone)

Every run used the pinned Verilator 5.050 wrapper (`$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, `Verilator 5.050 2026-07-01 rev v5.050`, sha256 `905795b9...`). Mutant builds inherit it through MAKEFLAGS, which I confirmed from the running process lines.

| What | Result | Receipt |
|---|---|---|
| Processor `044cb25f` is an ancestor of `801ef228`; the donor's remote `main` is `801ef228` | fast-forward, 20 commits (PRs #218 and #219) | `receipts/01_gitlinks.txt` |
| gPTP revert: every file touched by `4bf3eb72` and `a89802c8` compared with dev | the gPTP gitlink, `GPTP_PLANE.md`, `TIME_SYNC.md`, the four gPTP guides, `ieee8021as.md` and the `timesync_chain` diagram all equal dev's. Only the processor-pin pages and the ledger differ | `receipts/04_revert_check.txt` |
| gPTP `1616fc8f..a64be73d` | only `docs/TEST_DEVELOPER.md`, `tb/mutation_jobs_test.py`, `tb/verilator/engine/Makefile` and `mutants.py`. No `hdl/` or `syn/` byte | `receipts/01_gitlinks.txt` |
| ROM images generated at both processor pins | `ucode.hex` `264fbb03...` at `801ef228` and `49a993be...` at `044cb25f`; `ltn_rom.hex` `23cc67ee...` at both. Each equals its ledger row | `receipts/05_rom_images.txt`, `02_rom_ledger.txt` |
| `bash syn/yosys/ooc.sh --record-rom-digests`, then `git diff --exit-code syn/yosys/rom_digests.tsv` | rc 0 and rc 0: the ledger is unchanged | `receipts/17_rom_digests_record.txt` |
| `make crflic`, new pins | `checks: 458   failures: 0`. Domain `0 0 1`; VID 2 and both Talker Advertises `0 0 3`. MVRP LeaveAlls at 99401, 113601 and 126601 ms after the Lv at 95208 ms; MSRP at 96203, 107003 and 120403 ms | `receipts/13_crflic_new_old.txt`, `raw_new_crflic.log.gz` |
| `make crflic`, processor `044cb25f`, same harness | `checks: 458   failures: 7`, each a new check by name: three `[MVRPLA]` MVRP checks; Domain message 2; VID 2 messages 2 and 3; and `no MVRP JoinIn` `got=185`. MSRP and Talker Advertise rows pass | same, `raw_old_crflic.log.gz` |
| `make notify`, new pins | `checks: 535   failures: 0`. The wire carries 31, 32 and 33, then DEPARTING with 34, then 0 and 1. The descriptor reads 31, 32, 33, 0, 0 and 1 | `receipts/15_notify_new_old.txt`, `raw_new_notify.log.gz` |
| `make notify`, processor `044cb25f` | `checks: 535   failures: 4`: `[AIDX]` A1, A2, A3 and R2 read 0 against 0x1f, 0x20, 0x21 and 0x1 | same, `raw_old_notify.log.gz` |
| `make crflic-mutants` | `16 checks: 16 PASS, 0 FAIL`. All six processor-copy arms are caught by their named checks, the two-layer #851 control among them | `receipts/25_crflic_mutants.txt` |
| `python3 gsi_mutants.py 15`, `16`, `17`, `18` (the four `[AIDX]` arms, each beside its clean control) | 2/2 each, caught with 4, 4, 5 and 1 failures across 535 checks | `receipts/26_gsi_aidx_arms.txt` |
| `make gsi-mutants` (full campaign) | `19 checks: 19 PASS, 0 FAIL`: the clean leg plus all 18 arms, the four `[AIDX]` arms with 4, 4, 5 and 1 failures | `receipts/27_gsi_mutants.txt` |
| `make gptp`, `make gptp-lat` (milan_dp consumer legs) | `212 checks: 212 PASS, 0 FAIL` each; clockAccuracy 0x22 and 0xFE on the wire | `receipts/20_gptp_consumer_legs.txt` |
| `check_cpp_idiom.py --selftest`; the gate itself; `check_py_idiom.py` | 78/78; the tree at 0 for every rule; `long module: 10 <= 10`, `unannotated public function: 0 <= 0`, `undocumented public function: 0 <= 0` | `receipts/06_idiom_gates.txt` |
| The base `MULTI_DECL_RE` planted back into the head's gate | the new arm fails by its name; 77/78 | `receipts/08_cpp_old_pattern_mutant.txt` |
| Multi-declarator regex probe, base pattern against head pattern | see F1 | `receipts/07_cpp_multidecl_probe.txt` |
| `check_submodule_docs.py`, `check_gptp_docs.py --with-submodule`, `check_diagram_pngs.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 46c971fa`, `docs_check.py`, `check_doc_paths.py`, `docs_inventory.py --check`, `pp_resource_gate.py check-baseline`, `git diff --check 46c971fa HEAD` | all rc 0. The two renderer-bound gates ran in a private venv holding `tools/markdown/requirements.txt` | `receipts/16_pin_doc_gates.txt`, `11_check_baseline.txt` |
| `measure_test_evidence.py --check` (the docs.yml step that reads `gptp-processor/tb`) | rc 0, ratchet PASS | `receipts/19_measure_test_evidence.txt` |
| The processor top's parent-facing interface across the pin move | no port or parameter line changes. Parent `hdl/` is unchanged by the PR | `receipts/22_processor_interface.txt` |
| Commit form | 16 commits, each one line, with no trailers and one parent | `receipts/23_commit_form.txt` |
| Comment rule on the added source lines (`*.cpp`, `*.py`, `*.sv`, the Makefile) | no lane label, lane name, review round, reviewer ID or comment ID. The one hit, "each round's drain", is the encoder's drain round | `receipts/14_comment_rule_scan.txt` |

## Inspected, not executed (author's published receipts, `e99c3d13`)

- **Route set.** I read the receipts at `vivado/` and summarised them in `receipts/09_route_summary.txt` and `10_route_slacks.txt`.
  - Every directive has worst setup and hold paths MET at every corner: ExtraPostPlacementOpt +0.334 / +0.017 ns, ExtraTimingOpt +0.218 / +0.036 ns, AltSpreadLogic_high +0.162 / +0.039 ns.
  - Every `*_negative.rpt` reads "No timing paths found", and every route status shows 0 nets with routing errors.
  - Placed slices are 15,849, 15,850 and 15,850 of 15,850. LUT and FF counts equal the PR tables.
  - The receipts do not show the "one synthesis checkpoint" directly. I take it from the recipe's route set and the record's notes.
- **Synthesis inputs.** `7a19f62b..46c971fa` moves no `hdl/`, `configs/`, gitlink, `sw/firmware` or `syn/vivado` file. `a89802c8..e18c8225` changes only docs, tests, the baseline JSON and the gPTP gitlink, whose move touches no `hdl/` or `syn/` (`receipts/12_synth_input_moves.txt`).
- **Sweep and gates.** These receipts are the source-head execution evidence: the sweep `sweep-6c6706e5` (65/65, 2,192,633 checks), the gates at `f58347df` and `e18c8225`, and the 11 consumer suites at `e18c8225` (40,591 checks). I did not re-run the full banks.
- **Hosted runs.** At the time I checked, all four `pull_request` workflows at the exact head (docs, rtl-full, rtl-fast, elaborate) were `queued`, with no conclusion (`receipts/21_hosted_runs_head.tsv`). No hosted job has executed at this head, and I infer nothing from them.

## Findings

### F1 - MINOR - `Tests`, `Robustness` - `scripts/check_cpp_idiom.py:269-271` - the brace-initialiser fix stops the multi-declarator rule flagging a second declarator beside a nested initialiser

- **Authority and evidence.** #495 row 6758088112 asks the rule to exclude commas inside `{...}` initialisers. The fix's `_DECL_TEXT` (`(?:[^;(){}\n]|\{[^{}\n]*\})*`) accepts a single-level `{...}` and no brace inside one. A line whose initialiser nests braces therefore no longer matches at all, even when it carries a second declarator.
- **What the probe shows** (`receipts/07_cpp_multidecl_probe.txt`):
  - The base pattern (`46c971fa`) flags `uint32_t m[2][2] = {{0, 0}, {0, 0}}, n = 1;` and `int n = 1, m[2][2] = {{0, 0}, {0, 0}};`. The head pattern flags neither.
  - The single-level cases the row names are fixed correctly.
  - The new selftest arms (`:706-710`) cover only single-level braces, so nothing pins the nested case.
  - The comment at `:269`, "a whole `{...}` initialiser is one", claims more than the pattern does.
- **Impact.** The gate's ratchet is `0 <= 0`. A real multi-declarator declaration with a nested aggregate initialiser now enters the tree unflagged, where the base caught it. AGENTS.md section 8 forbids weakening a gate, and this delta weakens one beyond the residue it was fixing.
- **Required outcome.** A nested brace initialiser beside a second declarator is still a finding, and a nested initialiser alone is not. For example, the pattern can accept balanced braces to at least two levels. The selftest gains arms for both nested cases, and the `:269` comment states what the pattern really accepts.
- **Verification.** Run `python3 -I probe_cpp_multidecl.py <checkout>` (`scripts/` in this packet). Every row's head verdict must equal `real>1`. `check_cpp_idiom.py --selftest` must pass with the new arms. The base pattern planted back must still fail the brace-initialiser arm, and a single-level-only pattern must fail the nested arm.

### RESIDUE (wording only; none changes a measurement, test, verdict or code)

- **R1 - `Docs` - `docs/testing/TESTING.md:357`.** This PR rewrites the `crflic-mutants` row but keeps "the three gate mutants". `crflic_mutants.py` has six gate arms, and the Makefile (`:665`) and README (`:617`) say six.
  - Exact fix: "the three gate mutants" -> "the six gate mutants".
  - This is #495 row 6731336971, item 2, already classified there as wording only.
- **R2 - `Docs` - `syn/ooc/pp_resource_baseline.json:451`** (route-1x1 `measured` note). The note writes "+29 slices (80)" beside "(tolerance +500)" and "(+600)".
  - Exact fix: "+29 slices (80)" -> "+29 slices (+80)".
  - This is the same item as #495 row 6731336971, item 4.
- **R3 - `Docs` - PR #893 body, "#495 rows" table.** The table says row 6731336971 is "Taken with this PR's own comment edit". Only item 3 of the four (the Makefile line) is taken. Items 1, 2 and 4 stay open, and item 2 sits in a line this PR edits.
  - Exact fix: "6731336971 item 3 (the milan_dp Makefile line): taken; items 1, 2 and 4 remain on #495".

### Checked and not a finding

- **The ROM ledger keeps an `a64be73d` `gptp_ucode.hex` row** after the revert. The PR body discloses it. Its digest equals the `1616fc8f` row, and that pin changes no ROM generator or `hdl/` byte. The generator retains other pins' rows by design (`ooc.sh` record mode), and dev's ledger already carries two pins that were never dev gitlinks, `0922e434` and `6b5a4282` (`receipts/03_ledger_precedent.txt`). It is true and consistent with the ledger's practice.
- **The new `-Wunused-function` for `phase_nothing_declared` in the `TSPEC_ONLY_TB` build** follows the file's existing pattern: ten other phases are already unused in that build. The C++ idiom gate's warnings-flag rule stays at 0.
- **The [AIDX] D case expects 0 after ENTITY_DEPARTING** while the DEPARTING frame itself carries 34. This matches REQ-ADP-011 ("0 on DEPARTING") and the project's #85 decision. The harness does not grade the DEPARTING frame's own index, and the issue does not ask it to.
- **The 2026-11-10 area note** (maintainer, #665 issuecomment-6759197512: "the under-20k LUT target is for the 1x1 shape") concerns the Mark II image. I found no other public 2026-11-10 area acceptance. The current all-fabric shipping image stays under NFR-RES-01's "MUST fit `xc7a100t`; the resource gate holds it at its recorded figures". This record meets that: it fits with 1 slice free, and the gate passes within every tolerance, so no maintainer acceptance is needed.
- **NFR-RES-01's text still says the shipping image "measures 52,008 LUTs"** (`docs/reference/FR_NFR.md:473`). That figure was already stale on dev (53,534) and is outside this delta. The gated record and `AREA_BUDGET.md` carry the current 53,461. I note it for the residue owner and do not count it here.

## Lens results

- **`Conformance` PASS** - `sim_crf_licence.cpp:917-1061`, `sim_nxn.cpp:2091-2113,3019-3121`, `receipts/13`, `15`, `01`, `04`, `09`, `10`. Checked against the frozen items 1 to 5 as amended by the ruling:
  - Item 1: the processor fast-forward on `main`.
  - Item 2: the #495 rows and their planted arms.
  - Item 3: the three issues graded at AX7101 1x1, each new check failing at `044cb25f` by its own words. The clause readings hold: Table 10-3 VN and AN `sN`, then the Join by note 8; 10.7.6.3 JoinIn only with the Registrar IN; 10.7.9 and Table 10-5 LeaveAll with nothing declared, within Milan Table 4.3's 9.5 to 15.5 s; 1722.1-2021 Table 7-2 and 6.2.2.15 per REQ-ADP-011.
  - Item 4: every corner meets the +0.030 / 0 ns floors on all three directives, and the LUT, FF and slice deltas go against `46c971fa` under NFR-RES-01's fit-and-gate accounting.
  - Item 5: the author's gate receipts, plus my re-runs of the gates the revert touches.
- **`RTL` PASS** - `receipts/22_processor_interface.txt`, `09`, `10`, `12`, and the processor `hdl/` diff `044cb25f..801ef228` (9 files).
  - Parent `hdl/` and `KL_pp_shadow` are unchanged, and the processor top keeps every port and parameter. Its 22 added lines are internal: the per-interface index select, with an out-of-range interface falling back to interface 0.
  - No new clock domain or crossing appears in the parent.
  - The routes complete with 0 routing errors and no negative path at any corner.
  - The one-slice margin is a stated risk, not a defect: NFR-RES-01 requires the image to fit, and it does.
- **`Robustness` UNCLEAN (F1)** - `scripts/check_cpp_idiom.py:269-271`, `receipts/07`. The test harnesses passed my checks:
  - Each wait is bounded: 20 s withdrawal, 10 s per advertisement, 1 s DEPARTING.
  - A missing frame fails a named check rather than hanging.
  - `[AIDX]` refuses a read during which an ADPDU left.
  - `[MVRPLA]` judges both too-early (< 9.5 s) and overdue (> 15.5 s) LeaveAlls.
  - The campaign pattern-count guard refuses a stale arm.
- **`Tests` UNCLEAN (F1)** - `receipts/25`, `26`, `13`, `15`, `08`, `07`, `20`.
  - Each new check fails at the old pin, and each planted arm is caught by its named check.
  - The #851 control is two-layer and caught.
  - The C++ gate's new arm fails against the base pattern.
  - The consumer legs and gate re-runs are green.
  - F1 is open: the gate's own selftest does not pin the nested case, and the change regresses it.
- **`Docs` PASS** (RESIDUE R1 to R3 carried) - `CHANGELOG.md:60-87`, `docs/reference/SUBMODULES.md:859-947`, `docs/design/AREA_BUDGET.md:13,135-139,156-169`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` (the 2026-11-11 section), `MILAN_COMPLIANCE_MATRIX.md:94,98,119`, `traceability/ieee8021q.md:136,138`, `TESTING.md:357-358`, `tb/verilator/milan_dp/README.md`, `receipts/16`.
  - Each figure matches the route reports and the leg outputs I ran.
  - The pin pages and diagrams match the gitlinks, and the docs gates are all rc 0.
  - No obsolete requirement is restored.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the issue #883 items and ruling; the `[MRPAPP]`, `[MVRPLA]` and `[AIDX]` code and outputs at both pins; gitlinks; ROM ledger; route reports | R832-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |
| RTL | CLEAN | the processor `hdl/` diff, the top's interface, parent `hdl/` (unchanged), route timing, utilization and route status | R832-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |
| Robustness | UNCLEAN (F1) | `check_cpp_idiom.py` pattern probe; harness wait bounds and refusals | R832-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |
| Tests | UNCLEAN (F1) | the campaigns, old-pin controls, the idiom-gate selftest and planted base pattern, consumer legs | R832-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |
| Docs | CLEAN (R1 to R3 to the residue checklist) | the changelog, the pin, area, finding-234, matrix, traceability and testing pages, the suite README, diagrams, docs gates | R832-1 | `e18c822536ebeaf1cb0f42abea74513501aa26c7` |

## Prior public review findings

When this round started there were no PR reviews, no review comments and no finding on the PR or the issue. The only PR comments were the two review-start notices (6806806298, 6806812291).

The internal round `[R831]` published its review at 21:50 (issuecomment-6807870051), while this round was running. I read it only after the verdict, findings and ledger above were written, as instructed. I record each of its findings here at this head:

| `[R831]` item | Disposition at `e18c8225` |
|---|---|
| F1, MINOR, Tests and Robustness, nested brace initialiser | **Retained.** I found it independently as this round's F1, with the same evidence and the same required outcome. |
| R1, RESIDUE, PR body row 6731336971 | **Retained** as this round's R3. |
| R2, RESIDUE, `TESTING.md:357` "three gate mutants" | **Retained** as this round's R1. |
| S1, SUGGESTION, the [AIDX] D check is labelled "is the wire's" but expects the constant 0 | **Retained as SUGGESTION.** It matches my note under "Checked and not a finding": the DEPARTING frame carries 34 and the descriptor is graded against 0 per 6.2.2.15 and REQ-ADP-011. Only the label is affected. |
| S2, SUGGESTION, no planted arm for [MVRPLA]'s 9.5 to 15.5 s bounds | **Retained as SUGGESTION, not reproduced here.** I checked the bound logic by reading (`sim_crf_licence.cpp`, `grade_leave_all_gaps`) and saw it pass with margin. I did not plant the timer-length probes `[R831]` reports. |
| S3, SUGGESTION, NFR-RES-01's stale 52,008-LUT figure | **Retained as SUGGESTION.** It matches my note under "Checked and not a finding". It is outside the delta. |

There is one difference of detail. `[R831]` calls row 6731336971's JSON item moot because the route note was rewritten. The rewritten note at `syn/ooc/pp_resource_baseline.json:451` repeats the same "(80)" form, so I keep it as residue R2. It is wording either way and moves no lens.

## Real limits

- Not run by me:
  - the full sweep, the rtl-fast, rtl and elaborate banks, docs.yml as a whole, `test_builder.py --require-rv32`, behave, and `unb-mutants`. For these the author's published receipts are the source-head evidence.
  - Vivado. The route figures are read from the author's reports, not reproduced.
  - `dynmap-mutants`, whose fresh-clone fault is pre-existing and goes to its own issue.
- The two older-pin builds checked out `044cb25f` only in a scratch copy's submodule, never in this clone. Every build and probe ran in a disposable copy under `scratch/`. The review clone was never edited: after the runs it has an empty status (ignored files included), the index tree equals the head tree `be1aea46`, the `ls-files -s` and `ls-tree -r` listings have the same sha256, there are no assume-unchanged or skip-worktree entries, the gitlinks are `801ef228` and `1616fc8f`, and both submodules are clean (`receipts/29_restore_verification.txt`).
- Publishable receipts have this host's home and scratch paths replaced by placeholders (`<home>`, `<packet>`, `<clone>`, `<tmp-campaign>`). The scripts are `scripts/probe_cpp_multidecl.py` (F1) and `scripts/route_summary.py`. Both are read-only; run them with `python3 -I`.
- I read the clause interpretations from the quoted clause text and the processor's requirement rows, not from the standards documents.
- No hosted job had executed at the exact head when I checked. I make no hosted claim.
- Physical calibration was not run, and nothing here is hardware proof.

## Pending manager duties

- Build and validate the current-dev candidate on `fa6c094b` (builder and native banks), and link its receipts.
- Accept or reject the hosted and act results at the exact head.
- Route F1 back to the lane for a fix and re-review. F1 un-covers only `Tests` and `Robustness`, and a fix confined to `scripts/check_cpp_idiom.py` leaves the `Conformance`, `RTL` and `Docs` coverage above standing at any head that changes nothing else in their scope.
- Carry R1 to R3 to the residue checklist (R1 and R2 are already #495 row 6731336971's items 2 and 4).
- File the two pre-existing faults the author names: `dynmap-mutants` on a fresh clone, and the resource gate's `inputs_sha256` reading the exporter's `/* */` hierarchy comment.

R832-1 FINISHED
