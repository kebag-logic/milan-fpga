[R392] POSITIVE - exact head 0e5ae9c82bbdb5abc3feba84f07d0e6481254906

# R392-3: internal independent delta review of PR #616 (issue #451)

- **Head under review.** `0e5ae9c82bbdb5abc3feba84f07d0e6481254906`, tree `38f7ca763a9713bea02d78ff865e0c02ea240445`. It matches the published PR head and the remote branch (`receipts/remote_refs.txt`).
- **Delta.** `335e55c4..0e5ae9c8` holds two commits, each with a one-line message and no body or trailers:
  - The merge `f4bb2bd7` "Merge dev into 451-tdm8-first-light". Its parents are `335e55c4` and dev `7390b436`, and its merge base is the source base `6d5ebd73`.
  - The rewording commit `0e5ae9c8`.
- **Net against live dev** (`7390b436`, still the remote `dev` tip at 2026-09-28T17:04Z): 4 files, +441/-2. They are the page `docs/findings/451_TDM8_FIRST_LIGHT.md` (+438, blob `cb7dd0aa`, unchanged from `335e55c4`), one index row, and one line in each of `docs/reference/MILAN_COMPLIANCE_MATRIX.md` and `docs/litex/CLOCK_DOMAINS.md`.
- **Round.** R392-3, internal reviewer, cleared context, applying all five lenses. I reconstructed the task in this order:
  1. AGENTS.md and CONTRIBUTING.md.
  2. docs/README.md.
  3. The #451 body, the PocketBeagle 2 amendment (5729936674), the first-light assignment (5859278962), the merge-dev assignment (5874480178), the gitlink correction (5874543161) and the executor's TAKEN and REVIEW READY comments (5874519241, 5874638182).
  4. The diff and history.
  5. Hosted evidence at the exact head.

  I read the prior public review findings only after my own pass over the diff was complete. My round-2 packet was not used.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. The two suggestions below do not affect lens coverage.

## The four focus checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | The only conflict, `docs/findings/README.md`, keeps every row from both sides, in the index's own order, with no duplicate | **MET.** `git merge-tree --write-tree 335e55c4 7390b436` reports exactly one conflicted path, the index. The recorded merge differs from the automatic merge only in that file: the three conflict-marker lines are removed. The merged row set equals the union of both sides (10 rows), with no duplicate and no marker. The #451 row is first, and dev's rows follow in dev's order. The index's own ordering is newest first: each lane prepends its row above the previous top row (`7f997b60` put #397 above #117, `5c7577e5` put #75 above #397, and `3b5603e3` put #395 above #397). #451 is the newest, so it goes first. The #395 lane's own merge, `895be307`, put the incoming #75 row above its #395 row. That precedent orders an older-lane row against an incoming one and does not conflict with putting the newest lane first. Every index table line has 3 cells. | `verify_delta.sh`, `receipts/verify_delta.txt` section (1) |
| 2 | The protocol-processor gitlink equals dev's `c951a9ff`, and the lane changes no pin | **MET.** At HEAD, `protocol-processor` = `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`. The full recursive gitlink set equals dev's: `external` `efeb541a`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`. Pre-merge, the lane (`6d5ebd73..335e55c4`) touched only `docs/`. The gitlink moved from `870ff88a` only because dev moved it. The page's "Image pin" table (`:67-72`) still records `870ff88a`. That is correct: it describes the tested image, not the tree. | `receipts/verify_delta.txt` section (2), `receipts/clone_integrity.txt` |
| 3 | The rewording commit changes exactly the two statements the page falsifies and states only what the page proves | **MET.** `f4bb2bd7..0e5ae9c8` changes one line in each of two files (numstat 2/2). Details follow the table. | `receipts/verify_delta.txt` section (3), `stale_statement_search.sh`, `receipts/stale_statement_search.txt` |
| 4 | Nothing else changed, and the Markdown gates pass | **MET.** Against dev, the only differences are the 4 files above. All gates below return 0 at the head with the pinned Markdown environment, and the tree stayed clean. | `receipts/gate_*.txt`, `receipts/verify_delta.txt` section (4) |

### Check 3: the two reworded statements

- **`MILAN_COMPLIANCE_MATRIX.md:207`.**
  - Old text: "the TDM render lane is not clocked on any shipping build".
  - New text: "the TDM render lane is clocked on the shipping AX7101 1x1 TDM8 shape (#447), and [TDM8 first light] (#451) decoded its eight slots in order". "its silicon figure rides #117" is kept.
  - "Clocked on the shipping shape" is true independently of the page:
    - `configs/endstation_ax7101_1x1_tdm8.yaml:160` backs `render: 8` since #447;
    - `configs/generated/sweep_opts_ax7101.sh:15` emits `--audio-interface-master --audio-interface-render`;
    - `hdl/milan/milan_datapath.sv:185-189` elaborates `KL_tdm_render_master` for a nonzero `AUDIO_IF_RENDER_SLOTS_P` on a master bus;
    - several documents name 1x1 TDM8 as the shipping shape, for example `docs/integration/BUILDING.md:153` and `docs/findings/COMMERCIAL_TIMING_395.md:5`.
  - "Decoded its eight slots in order" is page `:204-217` and `:405`.
  - The row makes no latency figure claim and no #386 acceptance 4 claim.
- **`CLOCK_DOMAINS.md:140`.**
  - Old text: "exposes capture, not physical TDM rendering".
  - New text: "exposes capture and physical TDM rendering. [TDM8 first light] carried both on hardware (#451)".
  - "The example configuration" is `configs/endstation_ax7101_1x1_tdm8.yaml`, per `CLOCK_DOMAINS.md:9`.
  - "Carried both" is what the page shows at `:5-13` and `:405-407`: identifiable audio in all eight slots, both directions.
  - The line states no timing or latency figure.

### Check 3: my own search for other falsified statements

My search covered the merged tree outside `docs/history`, the page itself and the submodules. It had eight pattern families, S1 to S8 in the receipt. No other statement is contradicted by the page. Each remaining hit, and why the page does not contradict it:

- **Arty pmodb comments.** `configs/endstation_arty_4x4.yaml:36`, `configs/endstation_arty_8ch.yaml:71` and `sw/litex/platforms/board_audio_routing.py:100-101` say "No TDM8 device is on the bench yet" for the Arty pmodb header. First light used the AX7101 J11 header, so these are not contradicted.
- **Simulation-scoped statements.** `tb/verilator/milan_dp/README.md:165` ("serial input silent") and `:230` ("Physical rendering ... untested") describe that simulation. `docs/design/TIME_SYNC.md:365` is a modelled commit-to-pin figure.
- **Silicon latency figures that still ride #117.** `docs/design/TIME_SYNC.md:451`, `docs/AAF_LATENCY_TAPS.md:111-118` and matrix row 4.3.2 (`:210`). The page records no latency figure, and its `:403-404` keeps #386 acceptance 4 and #117 NOT RUN.
- **Capture semantics.** `docs/CHANNEL_MAP_64.md:312-333` states that physical inputs are "latest-sample sources" and makes no frame-coherence claim, so it is consistent with the page's `:283-295` mechanism and #617. `:394-406` assigns the physical completion record to #117, which the page does not close (`:413`).
- **Slip-counter semantics.** `docs/reference/REGISTER_MAP.md:1829-1850` and `:1941` give `SLIP_TDM` dups at 0.51/s. `docs/design/TIME_SYNC.md:165-167` gives -10.64 ppm and one slip per 1.9582 s. Both agree with the page's measured 0.5108/s and -10.64 ppm (`:345-351`).
- **Conditional pruned-arm text.** `docs/integration/BUILDING.md:389-391` and `docs/CHANNEL_MAP_64.md:112-113` describe the pruned arm conditionally, so they are not contradicted.
- **The slave front-end member.** `hdl/ieee1722/aaf/doc/audio_frontend_family.md:52` lists `KL_tdm_capture` with status "RTL". That is the slave member, which the master-bus first light did not exercise.
- **Other statements.** `sw/litex/deploy.sh:80-83` already says "TDM8 bus master in BOTH directions". `docs/litex/LITEX_SOC.md:72` is not a proof-status statement.

## Findings

No BLOCKER, MAJOR or MINOR finding.

**S1 - SUGGESTION - lenses: Tests, Docs - artifact: `receipts/fault_probes.txt` (repository Markdown gates against `docs/findings/README.md` and `MILAN_COMPLIANCE_MATRIX.md`).**
- **Evidence.** I ran disposable probes on a clone of this head (`fault_probes.sh`).
  - Gates that caught their fault:
    - a duplicated index row, conflict markers and a lost dev row each fail the reviewer row check;
    - conflict markers also fail `git diff --check` (rc 2);
    - an over-long sentence on `CLOCK_DOMAINS.md:140` fails `check_doc_style.py`;
    - an em dash in the reworded matrix row fails `check_em_dash.py`;
    - a broken link target on `:140` fails `docs_check.py`.
  - Blind spots:
    - `docs_check.py` passes a duplicated index row, conflict markers and an extra table cell in the matrix row;
    - `gen_toc.py --check` passes conflict markers;
    - `check_doc_paths.py` passes a broken Markdown link target.
- **Impact.** None at this head: the row set, duplicates and cell counts were checked directly (`verify_delta.sh`), and `git diff --check` is a required gate that returns 0. In general, though, whether a merge resolution of a Markdown table is correct depends on a reviewer script or a manual count, not on a repository gate. This is pre-existing tooling and outside #451's scope.
- **Suggested outcome.** If the maintainers want it, open a separate Issue for a table-shape and duplicate-row check in the docs gate. This PR needs no change.
- **Verification.** Re-run `fault_probes.sh`: the F2 and F7 rows would turn from GATE-BLIND to AS-EXPECTED.

**S2 - SUGGESTION - lens: Docs - `docs/litex/CLOCK_DOMAINS.md:140`.**
- **Evidence.** The sentence is true as written: the page shows capture carried identifiable audio in all eight slots. The one capture-side defect the page records, #617, is itself a clock-domain effect. The TDM frame drifts 10.64 ppm against the media tick across per-pair holds (page `:283-295`). This page is where a reader of clock domains would look for it.
- **Impact.** A cold reader could take "carried both on hardware" to mean frame-coherent capture.
- **Suggested outcome.** Optionally cite #617 beside the capture half of that line. This does not block.
- **Verification.** The docs gates and `check_doc_style.py` (10-word sentence limit) at the new head.

## Prior public findings on this PR, at this head

The page blob is unchanged since `335e55c4` (`cb7dd0aa`), so the round-2 resolutions still apply. I re-checked them at this head (`receipts/prior_findings_at_head.txt`):

| Prior item | Severity | Status at `0e5ae9c8` |
|---|---|---|
| R392-1 F1 = R393-1 S1 (idle-high claim) | MINOR | RESOLVED: no match for the removed claims; the stop-boundary text is at `:242-256` |
| R392-1 F2 = R393-1 F1 (#617 not linked) | MINOR | RESOLVED: `issues/617` at `:16`, `:295`, `:409` and in the index row |
| R393-1 F2 (page not indexed) | MINOR | RESOLVED: one index row, `README.md:11`, kept through the merge |
| R393-1 F3 (owner check unsourced; conductor count) | MINOR | RESOLVED: owner report cited at `:111` and `:401`; seven conductors at `:113` |
| R392-1 F3 to F6, R393-1 S2 to S6 | SUGGESTION | Taken at `335e55c4` (round-2 verification); unchanged |
| R392-1 F7 (lateness split) | SUGGESTION | Retained as optional, unchanged (`:311-316`) |
| R392-2 S1 (archive PR-BODY hash note), S2 (USB Audio item in index State) | SUGGESTION | Retained as optional; the index row text is unchanged by the merge |
| R393-2 S7 (State-column "continuity" wording), S8 (`[A403]` on `:3`) | SUGGESTION | Retained as optional; unchanged |

No retained item is above SUGGESTION.

## Gates and probes at this head

These gates ran with the pinned Markdown environment, unpiped, byte-code writing off. Each returned 0:

- `scripts/docs_check.py`: 0 findings, 175 md files.
- `scripts/check_doc_style.py` (22 documents, including `CLOCK_DOMAINS.md`), plus `--selftest`.
- `scripts/check_doc_paths.py`.
- `scripts/gen_toc.py --check`.
- `scripts/check_em_dash.py --base 7390b436`: 0 findings over 441 added lines in 4 pages. Also `--selftest`: 339 arms.
- `scripts/check_baremetal_only.py --check`.
- `scripts/ci_scope.py --selftest`.
- `git diff --check 7390b436 HEAD`.
- `git diff --check 6d5ebd73 HEAD`.

`scripts/ci_scope.py` classifies the diff against dev as docs-only (`false`), and the diff against the source base as RTL-relevant (`true`), because the latter includes dev's own delta (`receipts/ci_scope_classify.txt`). That matches the hosted scope below.

I used no Verilator build. The delta against dev has no RTL, config, script or test file, so no simulation could fail for a defect in this delta. The scoped simulator was not needed.

## Hosted evidence at the exact head

The snapshot is in `receipts/hosted_checks_snapshot.txt`. Every run's `headSha` is `0e5ae9c8`.

- **Executed, SUCCESS:** `rtl-fast`, `elaborate`, `changes`, `bdd-conformance`, `full-ci-gate`, `wire-accountability`, `docs-check-no-git`.
- **SKIPPED contexts:** `verilator-suites`, `yosys-portability`, the shard matrices, `verilator-lint`, `yosys-elaboration`, physical gPTP. These are skips, not passes. They agree with the docs-only classification against the PR base.
- **`docs-check`:** still in progress at the last snapshot (17:05Z). Its outcome is a manager item.

The manager's static, builder and native banks at this head were not located in the linked archive `851f835c` (`review-evidence/451-r1`), which predates this head. I did not rely on them. My coverage rests on the reviewer-run gates and scripts above.

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Merge-dev assignment 5874480178 and correction 5874543161 against `verify_delta.sh` sections (1) to (4). Reworded `MILAN_COMPLIANCE_MATRIX.md:207` and `CLOCK_DOMAINS.md:9,140` against page `:5-13`, `:204-217`, `:403-407`, `:413`. Shipping render lane in `configs/endstation_ax7101_1x1_tdm8.yaml:160`, `configs/generated/sweep_opts_ax7101.sh:15`, `hdl/milan/milan_datapath.sv:185-189`. | R392-3 | `0e5ae9c82bbdb5abc3feba84f07d0e6481254906` |
| RTL | CLEAN | `git diff --name-only 7390b436 HEAD`: no file under `hdl/`, `sw/`, `syn/`, `tb/`, `configs/`, `scripts/`. `git ls-tree -r` gitlinks at HEAD equal dev (`protocol-processor` `c951a9ff`). Lane `6d5ebd73..335e55c4` is docs-only. `milan_datapath.sv:185-189,946-952` checked for the matrix claim. | R392-3 | `0e5ae9c82bbdb5abc3feba84f07d0e6481254906` |
| Robustness | CLEAN | Merge-resolution failure cases: probes F1 (markers), F2 (duplicate row) and F3 (lost dev row) are all caught by the row check at HEAD, and the head itself passes. Page blob identical across the merge. `git merge-tree` agrees with the recorded merge except for the resolved file. Numeric consistency of `SLIP_TDM` and -10.64 ppm between page `:345-351`, `REGISTER_MAP.md:1829-1850,1941` and `TIME_SYNC.md:165-167`. | R392-3 | `0e5ae9c82bbdb5abc3feba84f07d0e6481254906` |
| Tests | CLEAN (S1 open as SUGGESTION only) | `receipts/gate_*.txt` (11 gates, rc 0). `receipts/fault_probes.txt`: each probe's result shown as caught or blind, with the head restored to a clean state. `receipts/ci_scope_classify.txt`. Hosted `rtl-fast` SUCCESS at the exact head. | R392-3 | `0e5ae9c82bbdb5abc3feba84f07d0e6481254906` |
| Docs | CLEAN (S2 open as SUGGESTION only) | `docs/findings/README.md:9-20` (10 rows, 3 cells each). `CLOCK_DOMAINS.md:140`, `MILAN_COMPLIANCE_MATRIX.md:207` (3 cells). The stale-statement search S1 to S8 and the classification of each hit above. PR body "Merge with dev" section. Executor REVIEW READY 5874638182. Prior findings table. | R392-3 | `0e5ae9c82bbdb5abc3feba84f07d0e6481254906` |

Coverage note under AGENTS.md section 7. The merge and the rewording changed Docs artifacts (the index, the matrix and `CLOCK_DOMAINS.md`) after `335e55c4`. R393-2's Docs coverage at `335e55c4` therefore does not by itself cover those lines at this head; this round does. Whether the two-positive bar needs an external round at this head is the manager's decision under CONTRIBUTING.md.

## Real limits

- **No hardware.** No physical calibration, scope, continuity or USB Audio item was run or checked. The page records those as NOT RUN, and field skips are not hardware proof.
- **Raw captures not re-read this round.** The page blob is byte-identical to `335e55c4`, where round 2 re-derived its numbers.
- **Not run by me.** No Docker, act, candidate merge build, full parent, processor, gPTP or Yosys bank, or Verilator suite.
- **Hosted `docs-check`** was still in progress at the last snapshot.
- **The search is pattern-based.** It covers eight pattern families and all tracked text outside `docs/history` and the submodules. A statement phrased outside those families could be missed. I read the matched contexts rather than only the lines.

## Pending manager duties

- Build and validate the final current-dev candidate at the merge turn. Live `dev` was `7390b436`, equal to the merged dev parent, at 17:04Z. Re-check that it has not moved.
- Run the act replica.
- Confirm hosted acceptance, including the in-progress `docs-check`.
- Obtain maintainer merge authorization.
- Perform post-merge containment.
- Decide whether an external round is needed at this head.
- Optional: file S1 as a separate Issue.

## Clone state after probes

All probes ran in a disposable shared clone under `scratch/`. The review clone is at `0e5ae9c8`, tree `38f7ca76`, with no status lines. Its index equals the HEAD tree by mode, blob and path (sha256 `a67b0f2e...`), and its gitlinks equal dev's (`receipts/clone_integrity.txt`).

R392-3 FINISHED
