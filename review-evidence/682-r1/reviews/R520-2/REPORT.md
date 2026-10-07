[R520] NEGATIVE - exact head cb359db3424c895010e89b4f9688347857008c85

# R520-2: internal cleared-context review of issue #682 / PR #692, round 3

- Repository: kebag-logic/milan-fpga, PR #692 (`682-pp-pin-2ad2f845` into `dev`).
- Exact head `cb359db3424c895010e89b4f9688347857008c85`, tree `408e0e80d98dc7eeaed7ecda322c5abd7caded51`.
- Round-2 head `5428b044176f95248e6916dc00dd89c0df154078`; source base and live `dev` both `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` when checked.
- Delta reviewed: `5428b044..cb359db3`, one commit, `CHANGELOG.md` (+30) and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (+18 -11).

## Verdict

NEGATIVE, on one open MINOR finding under `Docs`.

R520-1-F2 and R520-1-S1 are resolved. R520-1-F1's required outcome is met: the section exists, it has a generated contents entry, and it covers every required topic. However, one claim it carries is not true for this pin. It credits processor C11 (PR #156) with documenting synchronous reset. That wording was already in the previous pin `ead80360`, added through processor PR #157. The same misattribution is in `docs/reference/SUBMODULES.md:163`, which the CHANGELOG section mirrors (R520-2-F1). Every other claim in the section is true at the head. All required gates return 0. No source, record, generated file or gitlink changed.

## Reconstruction (public state only)

1. `AGENTS.md`, `CONTRIBUTING.md` (by reference) and `docs/README.md` routing.
2. Issue #682 body: acceptance 1-5, plus the manager comments for round 1, the round-2 ruling (6028334443) and the round-3 assignment (6043632388).
3. Executor comments TAKEN, STOP, REVIEW READY 6042116222 and REVIEW READY 6044322927.
4. Processor PRs #156, #159, #160, #161, #162 and #164 (public bodies), and the processor history `ead80360..2ad2f845`.
5. `git diff e21c1ca0..cb359db3` (18 files) and `git diff 5428b044..cb359db3` (2 files).
6. Public evidence tree `8d4e0732` `review-evidence/682-r1`: 133 paths, all author round-1/round-2 evidence. The exact-head hosted check-run snapshot.

Prior review findings (R520-1, R521-1) were read only after this review's own pass over the delta was complete.

## Findings

### R520-2-F1 - MINOR - Docs - `CHANGELOG.md:54`; `docs/reference/SUBMODULES.md:163`

- **Claim:** `CHANGELOG.md:53-54` reads "C11 documents the landed byte interfaces and TX backpressure. It also documents synchronous reset and complete FCS-good RX frames." `SUBMODULES.md:163` credits PR #156 with "Documents the landed byte interfaces, TX backpressure, synchronous reset and complete FCS-good RX frames".
- **Authority/evidence** (`receipts/reset_attribution.txt`):
  - The synchronous-reset wording is byte-identical at `ead80360` and `2ad2f845`, in both `docs/guides/integrator.md` and `docs/architecture/02_interfaces.md` (2 lines each; same digest at both pins).
  - That wording was introduced by processor commit `371505d` ("State in 02 §2 rule 5 the synchronous active-low reset the RTL implements"). That commit came in through PR #157 and is an ancestor of `ead80360`. The `ead80360` CHANGELOG section already lists #157.
  - The PR #156 merge changes no line containing "synchronous".
  - The PR #156 body (#71 item) says: "Acceptance 2's synchronous reset wording came from merged PR #157; this lane supplies acceptance 1 and 3."
  - The round-3 assignment and this review's focus require every claim in the section to be true at the head.
- **Why re-opened:** the `SUBMODULES.md` row was at the round-2 head and passed `Docs` there. The new evidence is the byte comparison across pins together with PR #156's own statement. The CHANGELOG line is new in this round.
- **Impact:**
  - The product's record of changes says this image changes the processor's documented reset contract, and it does not.
  - A release note built from this section would send an integrator to re-check reset wiring for a change that does not exist.
  - It also misstates what processor PR #156 delivered.
  - No measurement, code, test or generated artifact is affected.
  - This could arguably be residue. It is classified MINOR because a false "what changed" statement in a change record is a factual error, not only phrasing, and the tie-break rule sends doubtful cases to MINOR.
- **Required outcome:** neither file attributes synchronous-reset documentation to C11 or this pin. Exact minimal fix:
  - `CHANGELOG.md:54`: `- It also documents complete FCS-good RX frames.`
  - `SUBMODULES.md:163`, third cell: `Documents the landed byte interfaces, TX backpressure and complete FCS-good RX frames`
  - Alternatively, either line may say the reset wording arrived with PR #157 at `ead80360`.
- **Verification:**
  - Re-read both lines against `receipts/reset_attribution.txt`.
  - `gen_toc.py --check`, `docs_check.py`, `check_doc_style.py` and the em-dash gate (base `e21c1ca0`) return 0.
  - `git diff cb359db3..<new>` touches only these two lines.

### R520-2-S1 - SUGGESTION - Docs - `CHANGELOG.md:69-70`, `SUBMODULES.md:181-183`

Issue #682 acceptance 5 lists three post-merge bench duties: the #608 withdrawal cycles, the #658 default map, and the soak of all streams and counters. Both pages name the first two only. Consider adding the soak the next time either page is touched. This changes no claim, so it does not affect coverage.

## Prior public findings on this PR

| Finding | State at `cb359db3` | Evidence |
|---|---|---|
| R520-1-F1 (MINOR, Docs) | RESOLVED as to its required outcome: the section is at `CHANGELOG.md:44-71` with contents entry `:11`, in the same form as the `ead80360` section. It records PRs #156, #159-#162 and #164, parent-observable changes and limits, the harness adaptation, baseline F, unchanged ROMs and capture, and unchanged VERSION. One carried claim is not true and is filed as R520-2-F1 | `receipts/changelog_claims.md`; `gates/gen_toc_check.log` |
| R520-1-F2 (MINOR, Docs) | RESOLVED: `PP_SHADOW_BASELINE_RECIPE.md:105-113` states that F was recorded with the flag, that every measurement against F passes it, which endpoints that covers, and the re-record rule. All five preparation commands carry the flag (`:124`, `:125-126`, `:189-190`, `:191-192`, `:265-266`), and `:461` repeats it. The two remaining Python snippets (`:147-179`, `:376-397`) only reopen saved checkpoints and run no synthesis, so the flag does not apply. Consistent with `pp_resource_baseline.json`: every endpoint's `record.identity.flow[0]` is `set_param synth.maxThreads 1` | flow-identity probe below |
| R520-1-S1 (SUGGESTION) | RESOLVED: the PR body quotes `(cd tb/verilator/milan_dp_render && make tdm8render-mutants)` | PR #692 body, validation block |
| R521-1 | Published no findings | PR #692 comment 6042536807 |

## Focus checks

### Delta scope and integrity (`receipts/integrity.json`, verdict PASS)

- `git diff --name-status 5428b044..cb359db3`: only `M CHANGELOG.md` and `M docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
- Gitlinks are identical to round 2: `protocol-processor` `2ad2f845`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e`, all checked out and clean. `external` stays uninitialized, as before.
- After all probes, all 1,164 tracked blobs match HEAD in bytes and modes. The index equals HEAD's tree with all entries at stage 0, and `git status --ignored` is empty. Bytecode caches created by the gate runs were removed.

### CHANGELOG claims (`receipts/changelog_claims.md`)

Each line of the section was checked against the processor history, PR bodies, parent records and `SUBMODULES.md`:

- **Processor PRs:** the first-parent merges `ead80360..2ad2f845` are exactly PRs 159, 156, 161, 160, 162 and 164.
- **Processor top:** `hdl/top` is byte-identical across the two pins.
- **Interfaces:** the only changed HDL declaration line is a trailing comment on `wr_data_i` in `KL_pp_trace_ring.sv`, so no port, parameter or register changed.
- **ROMs:** the two `2ad2f845` rows in `rom_digests.tsv` equal the `ead80360` rows.
- **Analysis budget:** the xvlog submodule section reads "0 finding(s)".
- **Harness bound:** `sim_nxn.cpp:973` stops extending at `cyc + 2048`.
- **Capture, firmware and VERSION:** none of these paths changed relative to `dev`.
- **Behaviour lines:** the lines for #134, #158 and #42 match the bodies of processor PRs #160, #161 and #164.
- **Wording:** the #148 line matches the round-2 accepted `SUBMODULES.md` wording.
- **Exception:** only `:54` (synchronous reset) fails; see R520-2-F1.

### Recipe against baseline F

- `syn/ooc/pp_resource_baseline.json`: all three endpoints (`route-1x1`, `ooc-1x1`, `ooc-8x8`) record `set_param synth.maxThreads 1` before `create_project`, with `general.maxThreads 32` unchanged.
- `syn/ooc/pp_baseline.py:581-583` prepends exactly that line under `--single-thread-synthesis`.
- **Flow-identity probe** (`scripts/flow_identity_probe.py`, `receipts/flow_identity_probe.log`). It uses the gate's own self-test fixtures, with a baseline recorded with the cap first, for both the route and OOC kinds:
  - candidate keeps the flag: exit 0;
  - candidate drops it: exit 2, "NOT COMPARABLE: tool or recipe change in flow";
  - candidate moves the cap after synthesis: exit 2.
- So the recipe's statements at `:110-113` are true at this head.

### Gates at the exact head (`receipts/gates/gate_rc.tsv`, all rc 0)

The Markdown renderer was the repository-locked set; the interpreter's lock file is byte-identical to `tools/markdown/requirements.txt`.

| Gate | Result |
|---|---|
| `gen_toc.py --selftest` | PASS, 1501/1501 arms |
| `gen_toc.py --verify-anchors` | 393 links reproduced |
| `gen_toc.py --check` | OK, 139 pages |
| `docs_check.py` | 0 findings, 199 md + 1140 text files |
| `check_doc_style.py` | OK, 22 documents |
| `check_doc_style.py --selftest` | OK |
| `check_em_dash.py --base e21c1ca0` | 0 findings over 313 added lines, arms 339/339 |
| `pp_baseline.py --selftest` | PASS, default and worker-capped scripts |
| `pp_resource_gate.py --selftest` | 260 arms + 500 fuzz cases PASS |
| `pp_resource_gate.py check-baseline` | PASS, 3 endpoints |
| `git diff --check e21c1ca0 HEAD` | clean |

### Fault probes (`receipts/probes/`, `receipts/em_probes/`)

| Probe | Gate | Result |
|---|---|---|
| P1 drop the new contents entry | `gen_toc --check` | KILLED (rc 1) |
| P2 rename the new heading | `gen_toc --check` | KILLED (rc 1) |
| P4 11-plus-word bullet in the new section | `check_doc_style` | KILLED (rc 1) |
| P6 helper emits `maxThreads 2` | `pp_baseline --selftest` | KILLED |
| P7 helper ignores the flag | `pp_baseline --selftest` | KILLED |
| E1 committed U+2014 in the new CHANGELOG section | em-dash gate | KILLED (rc 1, `CHANGELOG.md:48`) |
| E2 committed U+2014 in the new recipe paragraph | em-dash gate | KILLED (rc 1, `:105`) |
| P8 drop the flag from one recipe command | `docs_check` | SURVIVED: no gate reads recipe command text |

- **P3/P5:** these first em-dash attempts edited only the worktree. The gate judges committed lines `base..HEAD`, so they were invalid by construction. E1/E2 repeat them as commits in a disposable clone; the review clone was never committed to.
- **P8:** the resource gate's flow-identity refusal (probe above) is the fail-closed backstop, so this survivor is not a finding.

## Per-lens results

```text
[R520] PASS Conformance - issue #682 acceptance 1-4 evidence binding at cb359db3 (integrity.json: delta = 2 Markdown files, gitlinks/records/ROM ledger/baseline JSON unchanged from the R520-1/R521-1-covered 5428b044) + round-3 assignment 6043632388 items 1-3 + 802.1Q Table 10-4 / Milan Table 5.22 statements at CHANGELOG.md:49,55-56 against processor PRs #159/#160 - no conformance or acceptance claim changed or misstated
[R520] PASS RTL - CHANGELOG.md:62-65 RTL claims vs processor hdl delta ead80360..2ad2f845 (receipts/pp_pin_delta_audit.txt: hdl/top identical, blob 098c5381; only a comment changed on a declaration line) and parent hdl/ (no change e21c1ca0..cb359db3) - no RTL, interface or parameter artifact in the round-3 delta
[R520] PASS Robustness - PP_SHADOW_BASELINE_RECIPE.md:105-113 fail-closed claim vs syn/ooc/pp_resource_gate.py identity/FLOW (flow_identity_probe.log: dropped or moved cap -> exit 2, control -> 0, route and OOC); sim_nxn.cpp:973 bound vs CHANGELOG.md:51-52 - no new failure mode
[R520] PASS Tests - gates/gate_rc.tsv (13 rc 0 incl. pp_baseline and pp_resource_gate self-tests, check-baseline) + probes P1/P2/P4/P6/P7/E1/E2 killed; P8 survivor covered by the gate's flow refusal - the gates that guard this delta can fail for the defects they claim
[R520] MINOR Docs - CHANGELOG.md:54; docs/reference/SUBMODULES.md:163 - R520-2-F1 synchronous-reset documentation credited to C11/this pin
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #682 acceptance and round-3 assignment; `integrity.json` delta/gitlink binding; `CHANGELOG.md:49,55-56` protocol statements vs processor PRs #159/#160 | R520-2 | `cb359db3424c895010e89b4f9688347857008c85` |
| RTL | CLEAN | `pp_pin_delta_audit.txt` (processor hdl delta, top identity, declaration lines); parent `hdl/` unchanged; `CHANGELOG.md:62-65` | R520-2 | `cb359db3424c895010e89b4f9688347857008c85` |
| Robustness | CLEAN | `PP_SHADOW_BASELINE_RECIPE.md:105-113` vs `pp_resource_gate.py` flow identity (flow-identity probe); `sim_nxn.cpp:973` | R520-2 | `cb359db3424c895010e89b4f9688347857008c85` |
| Tests | CLEAN | 13 gate/self-test receipts; 7 killed fault probes; P8 survivor analysis | R520-2 | `cb359db3424c895010e89b4f9688347857008c85` |
| Docs | UNCLEAN (R520-2-F1) | `CHANGELOG.md:11,44-71`; `SUBMODULES.md:158-185`; `PP_SHADOW_BASELINE_RECIPE.md` (whole file); `AREA_BUDGET.md:102`; `234_PP_SHADOW_AREA_BASELINE.md:27-35`; `pp_resource_baseline.json` identity; PR #692 body round-3 section; processor PR bodies | R520-2 | `cb359db3424c895010e89b4f9688347857008c85` |

The four clean lenses were applied to this head's delta. None of their in-scope artifacts changed between `5428b044` and `cb359db3` except the two Markdown files examined here.

## Real limits

- Vivado was not run. Baseline F's figures, the routes, timing and `Synth 8-6901` counts were not regenerated. This round audits only the recipe's statements against the recorded identity and the gate's refusal logic.
- Not run, by assignment: the full parent, processor, gPTP and Yosys banks, the builder and its documentation workflow step bodies, render or other Verilator campaigns, and any act or hosted job. Verilator was not needed for this delta.
- The manager's source static/builder and native bank results for `cb359db3` were not found in the public evidence tree `8d4e0732` (133 paths, author round-1/2 evidence only) or in issue/PR comments when this report was written. This review relies on its own gate runs and does not restate those results.
- The executor's round-3 gate receipts (`round3-gate-*`) are in a non-public packet and were not read.
- The CHANGELOG claim check reads processor documentation and PR bodies. It does not re-derive processor behaviour beyond the RTL lines cited.
- Hosted exact-head snapshot at 2026-10-07T18:39:57Z (`receipts/hosted_check_runs.tsv`):
  - completed success: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, and Yosys shards 1 and 3;
  - in progress: `docs-check`, `elaborate`, `firmware-unit`, `yosys-elaboration`, Verilator shards 0-4, and Yosys shards 0 and 2;
  - skipped, not executed: "Physical gPTP (nightly and manual)".
  - The manager owns hosted and local-replica acceptance.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry R520-2-F1 to the executor (two-line documentation fix), then a re-review of the corrected head. R520-2-S1 is optional.
- Publish the round-3 bank evidence for `cb359db3` (or its successor) where reviewers can read it.
- Collect R521-2's independent verdict.
- Exact-head hosted `verilator-suites` and `yosys-portability` conclusions, and local-replica acceptance.
- Final current-dev candidate validation at the merge turn.
- Explicit merge authorization and post-merge containment.
- Acceptance 5 on hardware: the #608 withdrawal cycles, the #658 default map, and the stream and counter soak.
- #657 stays open with its own acceptance.

## Receipts and reproduction

The scripts take paths as arguments. `$MARKDOWN_PYTHON` is an interpreter with the repository-locked Markdown renderer (`tools/markdown/requirements.txt`). `$REPO` is a clean checkout of the exact head with its three required submodules.

- `scripts/run_gates.sh $REPO $MARKDOWN_PYTHON <out> e21c1ca024d37ea188ad15b5c8f9c2dae18628df`: documentation gates and the helper self-test. Run the two `pp_resource_gate.py` commands in `gate_rc.tsv` from `$REPO` with `python3`.
- `scripts/probes.sh $REPO $MARKDOWN_PYTHON <out> <base>`: worktree fault probes. Each probe restores HEAD bytes for its file.
- `scripts/em_dash_probe.sh $REPO $MARKDOWN_PYTHON <disposable-clone-dir> <out> <base> <head>`: committed em-dash probes in a disposable clone.
- `scripts/flow_identity_probe.py $REPO <scratch>`: the gate's refusal when the worker cap is dropped or moved.
- `scripts/integrity.py $REPO cb359db3424c895010e89b4f9688347857008c85 5428b044176f95248e6916dc00dd89c0df154078`: byte, mode, index and gitlink audit.
- `receipts/pp_pin_delta_audit.txt`, `receipts/reset_attribution.txt` and `receipts/changelog_claims.md`: claim evidence, built from `git` in the processor checkout and public PR bodies.

Host paths in receipts are replaced by `$REPO`, `$PACKET` and `$MARKDOWN_PYTHON`. No other content was removed. `MANIFEST.sha256` lists every publishable file.

R520-2 FINISHED
