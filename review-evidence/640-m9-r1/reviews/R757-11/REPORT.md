[R757] POSITIVE - exact head c576fe540838c353a1cfc9455a6b89eff2b77ffc

# R757-11: round 10 delta review of PR #828 (issue #640)

Head `c576fe540838c353a1cfc9455a6b89eff2b77ffc`, tree `5936f42145c658cd9d939b6d33c9610235897c21`. Delta `d63b378d..c576fe54`: one commit, four Markdown pages, 14 insertions and 9 deletions, no figure changed. Source base and live dev are both `1f29f189`.

Abbreviations: AB = `docs/design/AREA_BUDGET.md`, MS = `docs/design/MAILBOX_SPLIT.md`, MG = `docs/guides/gptp/MANAGER.md`, Q = `docs/traceability/ieee8021q.md`, SPLIT = `docs/ARCHITECTURE_HW_SW_SPLIT.md`, FR = `docs/reference/FR_NFR.md`.

## Result

- **No BLOCKER, MAJOR or MINOR is open.** All five lenses are clean at this head.
- **R757-10-F1 is resolved at its cause.** MS:42-44 now bounds the gPTP plane at F6, in the text that finding suggested.
- **R758-10-R1 to R4 are resolved.** R1, R2 and R3 use the exact text. R4 uses a shorter sentence, and the style gate does require the shortening.
- **Two new RESIDUE items and one new SUGGESTION** are below, with the items retained from earlier rounds.
- **This is not a merge clearance on its own.** The exact-head long gates were still running at my last check. See "Pending manager duties".

Order of work: my provisional verdict and ledger are in `receipts/own-pass-before-prior-reports.md`, written before I opened any prior report. The two later-numbered residue items and the suggestion were already in it.

## Named for the owner, not a finding

D8's 1 percent margin against the 20,000-LUT ceiling is still undecided. R757-10 and R758-10 both named it, and the delta does not touch it.

## The requested checks

| Check | Result | Evidence |
|---|---|---|
| MS bounds the gPTP plane at F6 (R757-10-F1) | Holds. The sentence agrees with its authorities: firmware owns "the protocol and servo", and timestamps stay in the fabric list | MS:42-44; `REQUIREMENTS.md:36`, `:43`; SPLIT:51, 115-117, 226-227, 237-238 |
| Q takes R758-10-R1 | Holds. The rendered section has two top-level items, and the MRP text sits in the Reservation item. The Mark II sentences are a paragraph after the list | Q:37-45; `receipts/ieee8021q_render_probe.txt` |
| AB takes R758-10-R2 | Holds. All three lines say "at 32x32", matching FR:473 | AB:130, 140, 180 |
| AB takes R758-10-R3 | Holds. Exactly three sentences follow the marker, and the current plan and schedule sentences come after them | AB:182-186 |
| MG takes R758-10-R4 | Holds. The scope and a resolving split-contract link are on their own paragraph | MG:8-9 |
| MG's sentence was shortened for the style gate | Holds. R758-10-R4's text has 12 words against a limit of 10, and the gate refuses it | `receipts/gates/mut_style_r4_prior_text.log`, rc 1 |
| Nothing else changed | Holds. Four paths, all `100644` at both heads, one parent, no gitlink differs from the base | `receipts/delta_d63b378d_c576fe54.diff`, `receipts/gitlinks_after.txt` |
| No figure moved | Holds. The only figure added is the 32x32 shape. 13,972, 10,521, 57 % and 31.5 % recompute | AB:130-140, 180-186; delta diff |
| Comment rule | Holds. The delta has no source comment | Delta path list |

As ruled, I ran no further tree-wide search for stale placement text.

## Findings

### R757-11-R1 RESIDUE - Docs - `author-r10/HANDOFF.md:3` - the handoff miscounts the delta and names no head

- **Evidence:** it says "13 lines added", and the diff has 14 insertions and 9 deletions. It says "One commit over `d63b378d`", and the text never contains `c576fe54`.
- **Impact:** a cold reader cannot tie the handoff to an exact head from the handoff alone. No gate or figure depends on this.
- **Exact fix:** "One commit, `c576fe540838c353a1cfc9455a6b89eff2b77ffc`, over `d63b378d`, by the manager, 4 pages, 14 lines added and 9 removed. No figure changes."
- **Verification:** compare with `git diff --stat d63b378d..c576fe54`.

### R757-11-R2 RESIDUE - Docs - PR body lines 24, 91, 298 and its contents list - the body stops at round 9

- **Evidence:** the status line and validation record name `d63b378d`, the contents list ends at Round 9, and the commit table has no `c576fe54`. `author-r10/PR-BODY.md` matches the live body apart from a trailing newline. Each statement is true of the head it names.
- **Impact:** a reader of the body alone would not learn of the round 10 commit or which findings it closed. The handoff holds that information.
- **Exact fix:** add a Round 10 contents entry and section carrying the handoff's table, add a `c576fe54` commit-table row, and point the status line and validation record at the head they were actually recorded on.
- **Verification:** read the body against the head at publication.

### R757-11-S1 SUGGESTION - Docs - `docs/design/MAILBOX_SPLIT.md:43` - "F6" has a second meaning on this page

MS:719 and MS:772 use F6 for a test case in `test_acmp_mbx.cpp`. The page's title and MS:14 give enough context to read MS:43 as the #665 lane, so this is optional. Clearer text: "It keeps the gPTP plane until #665 lane F6, then firmware owns the protocol and servo."

## Prior findings

Read after my independent pass. I opened the R757-10 and R758-10 reports only. Older items are taken from their prior-findings tables and spot-checked where a line is cited.

| Finding | State at this head | Evidence |
|---|---|---|
| R757-10-F1 MINOR | **Resolved** | MS:42-44 |
| R757-10-R1 RESIDUE | **Resolved**, same cause as R758-10-R1 | Q:37-45 |
| R757-10-R2 RESIDUE | **Resolved in part, the rest retained.** The shape is added. AB:129 still says "accepted headroom target", and AB:180 does not say "fitting Block RAM" | AB:129, 180. Exact fix: AB:129 "is the accepted target"; AB:180 "That is fewer than 20,000 LUTs at 32x32, fitting Block RAM, with timing met." |
| R757-10-R3 RESIDUE | **Retained** | MS:13 still says "defines the Mark II default"; `docs/findings/README.md:26` is unchanged. Exact fixes are in R757-10 |
| R757-10-S1 SUGGESTION | **Retained**, optional | `docs/guides/SYSTEM_INTEGRATOR.md:95`, `docs/BUILD_FLASH_BOOT.gen.py:44` |
| R758-10-R1, R2, R3 RESIDUE | **Resolved**, exact text | Q:37-45; AB:130, 140, 180; AB:182 |
| R758-10-R4 RESIDUE | **Resolved**, shortened from the given text; the gate requires it | MG:8-9 |
| R758-10-S1 SUGGESTION | **Retained**, optional | PR body line 24 still says "documentation only" |
| R757-8-R1 (96 kHz row), R757-8-R2 RESIDUE | **Retained** | FR:306 still reads "that derivation"; the delta does not touch FR |
| R757-7 RR13 RESIDUE | **Retained**, the manager's | The #640 body still reads "Every talker stream meets the 65 µs target" |
| R757-9 S1, S2; R757-8 S1-S5; R758-8 S1, S2; earlier optional items | **Retained**, optional, not re-judged | The delta does not touch them. FR:473 and `docs/design/MARK_II_AREA_PLAN.md:38`, `:71` still give 52,008 |

## Lens results

```text
[R757] PASS Conformance - MS:42-44; AB:130,140,180; REQUIREMENTS.md:36,43; SPLIT:51,115-117,226-227,237-238; FR:473 - each changed claim read against its requirement or contract clause; retained residue R757-10-R2 recorded
[R757] PASS RTL - receipts/delta_d63b378d_c576fe54.diff; receipts/gitlinks_after.txt - no HDL, register, generator or constraint path in the delta, gitlinks equal the base; earlier verdicts depend on nothing it changed
[R757] PASS Robustness - receipts/delta_d63b378d_c576fe54.diff; receipts/gates/resource_baseline.log; receipts/gates/builder_tier1_helper.log - no runtime path changed; both readers of the edited AREA_BUDGET.md page accept it
[R757] PASS Tests - receipts/gate_summary.txt; receipts/gates/mut_style_*.log; run_gates.sh; run_probes.sh - no test in the delta; 14 gates and page readers re-run with rc 0; the style gate fails on both controls
[R757] PASS Docs - MS:42-44; MG:8-9; Q:37-45; AB:129-140,179-186; receipts/ieee8021q_render_probe.txt - four pages read in context, links and anchors pass their gates; residue and suggestions recorded with exact fixes
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN; residue retained | MS:42-44; AB:130, 140, 180; `REQUIREMENTS.md:36`, `:43`; SPLIT F6 clauses; FR:473 | R757-11 | c576fe540838c353a1cfc9455a6b89eff2b77ffc |
| RTL | CLEAN | Delta path list; six gitlinks against base | R757-11 for the delta; earlier verdicts carried, as nothing they depend on changed | c576fe540838c353a1cfc9455a6b89eff2b77ffc |
| Robustness | CLEAN | Delta path list; `pp_resource_gate.py check-baseline`; tier-1 table reader | R757-11 for the delta; earlier verdicts carried, as nothing they depend on changed | c576fe540838c353a1cfc9455a6b89eff2b77ffc |
| Tests | CLEAN | 14 gate rc files; two negative controls | R757-11 | c576fe540838c353a1cfc9455a6b89eff2b77ffc |
| Docs | CLEAN; residue R757-11-R1, R2 and retained items | Four delta pages; rendered Q section; PR body; handoff | R757-11 | c576fe540838c353a1cfc9455a6b89eff2b77ffc |

## Packet and gate evidence

- **Packet hashes match.** `author-r10/HANDOFF.md` and `PR-BODY.md` at evidence commit `a7e4faac` match their `MANIFEST.json` entries (sha256 `2b9f006f...` and `20019395...`).
- **Handoff gates reproduced.** Every gate it lists exits 0 here, as do `check_solution_docs.py` and `gen_toc.py --verify-anchors` and the traceability matrix check. See `receipts/gate_summary.txt`.
- **`check_doc_style.py` can fail.** It refused both planted MG sentences. The two `mut_style_*` entries in that summary are these controls, so rc 1 is the expected result.
- **Page readers.** `ctrl_service_bounds.py` reads MS and exits 0. `pp_resource_gate.py` and the builder's `_assert_area_budget_table_agrees` read AB and accept it. `check_gptp_docs.py` reads MG and passes. `scripts/ci_scope.py:71-72` classifies AB and MS as gate-read, so the long gates apply to this head.
- **Hosted state, exact head, 2026-11-01T22:17:57Z (`receipts/hosted_checks_snapshot.tsv`):** 9 succeeded, 1 skipped (Physical gPTP, nightly and manual), 20 in progress, 19 queued, none failed. `docs-gates-0`, `-1` and `-2` were still in progress. This is an observation only; acceptance is the manager's.

## Real limits

- **The packet is hash-pinned, not signed.** GitHub reports both `a7e4faac` and `c576fe54` as unsigned, and the packet has no detached signature. The manifest sits in that same commit, so I checked integrity against the manifest and could not check a signature.
- **The round 10 packet has no raw gate logs.** The handoff states rc 0 in prose. My re-runs stand in for those receipts, for the gates listed only.
- **One of my probes was mis-selected and is not evidence.** A filter meant for the tier-1 table reader instead ran 98 builder tests: 17 passed and 81 failed, in this clone whose six submodule directories are empty. I sampled the failure causes and did not root-cause each one. The sampled causes include missing files and modules and failed dry runs. I did not establish that all 81 are environmental, and I ran no comparison at another head. The builder legs were out of scope for me, and that log is not published because it contains local paths. I then called the reader directly, with rc 0. The delta changes only the four pages above, so the builder legs in the hosted run are the evidence to read.
- **Not run:** builder banks, parent, processor, gPTP or synthesis banks, the docs workflow's self-tests, `act`, and any tree-wide stale-text search (closed by ruling).
- **Restore is complete for tracked content, with one leftover.** Tree and index digests agree, the worktree is clean, and all six gitlinks equal the base. Four ignored `__pycache__` directories from my first gate runs remain in this disposable clone, because this session refused the command that included their removal. They are not tracked content.
- **The renderer dependency** was installed with its pinned hashes under `scratch/` only.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. The hosted "Physical gPTP" skip is one of these.
- **No manager source bank exists at this head,** and I infer none.

## Pending manager duties

- Accept the hosted and local-replica results at the exact head. At my last snapshot the docs gate legs and the long gates had not finished.
- Build and validate the current-dev merge candidate and link its receipts at the merge turn.
- Carry R757-11-R1, R2 and the retained RESIDUE items, including RR13, to the residue checklist.
- Update the PR body for round 10, as R757-11-R2 describes.
- Obtain the owner's answer on D8's margin.
- Publish this report and the listed receipts. Merge still needs two independent positive reviews at the merge head and explicit maintainer authorization.

R757-11 FINISHED
