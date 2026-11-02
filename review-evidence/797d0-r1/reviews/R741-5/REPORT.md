[R741] POSITIVE - exact head e8ec8d209a3d9055cc034a23d94925a0bf7b9a63

Internal independent review, round R741-5, PR #815 / issue #797 lane D0. Tree `274a5320231c562168a58416a3a3c316ced60493`. Delta judged: `8d8c2e36..e8ec8d20`. It has two commits: merge `b48b2fd5` of dev `e61a4afa`, and regeneration commit `e8ec8d20`, which changes `docs/DOCUMENTATION_AUDIT.md` only.

## Verdict basis

All five lenses are clean at this head, and no BLOCKER, MAJOR or MINOR is open. This round records one new wording residue, retains one earlier residue and adds two suggestions. Earlier optional suggestions are retained.

This verdict covers the source at this head. It does not clear the hosted bar. At the snapshot `2026-11-02T16:07Z`, 1 of 23 exact-head check runs had completed (`changes`, success), 3 were in progress and 19 were queued (`receipts/hosted_check_runs.txt`). The manager owns hosted and act acceptance, and the current-dev merge candidate.

| Focus check | Result | Evidence |
|---|---|---|
| (1) The merge keeps both sides; `docs/README.md` | PASS | `git merge-tree --write-tree 8d8c2e36 e61a4afa` gives rc 0 and tree `f10e50b9`, which equals `b48b2fd5^{tree}`. `docs/README.md` is the only file changed on both sides since base `1f29f189`. The merged file holds dev's "Mark II stream engines" row and the lane's "Media-clock following, implemented" change. Relative to dev, the only difference is the lane's hunk. (`receipts/merge_and_delta.txt`) |
| (2) Regenerated only by the generator; `--write` then `--check` rc 0; byte-identical when regenerated here | PASS | See "Regeneration identity" |
| (3) Page-count change and moved rows follow the generator's rules, with nothing added or dropped by hand | PASS | See "What moved, and why" |
| (4) One merge base; gates pass | PASS | `git merge-base --all e61a4afa HEAD` gives only `e61a4afa`. The other gate results are in "Gates run here" |

### Regeneration identity

- `scripts/docs_inventory.json` and `scripts/docs_inventory.py` have the same blobs at `8d8c2e36` and at the head (`242c0553`, `fe9cbbc5`). The merge did not touch either file or the audit page. `git diff b48b2fd5 8d8c2e36` is empty for all three.
- `e8ec8d20` changes only `docs/DOCUMENTATION_AUDIT.md`.
- In this clone:
  - `--check` gave rc 0 (540 lines, fresh).
  - `--write` gave rc 0, with `git status --porcelain` empty afterwards.
  - `--check` gave rc 0 again.
  - The rewritten page hashes to blob `245e63cf`, the committed blob. It is byte-identical. (`receipts/check_before.log`, `write.log`, `status_after_write.txt`, `check_after.log`, `regen_identity.txt`)
- `--selftest` gave rc 0 with 50 controls (`receipts/selftest.log`).
- `--findings-dir` gives 76 rows: 9 archive, 1 design, 11 overview and guides, 54 reference, 1 testing and CI. Its output is byte-identical to the five generated pages in the published `author-r5/findings`. The author's hand-written `findings/README.md` is the only file that differs (`receipts/findings_dir.log`, `findings_dir_vs_published.diff`).
- The command-table digest at `ci/image/command-table.json:13701` still equals `sha256(scripts/docs_inventory.py)`.

### What moved, and why

I compared the Findings rows (ID, page and line) and the status of every page between `8d8c2e36` and the head with `rows.py` (`receipts/rows_delta.txt`).

- **Rows go from 87 to 76.** Eleven D0-001 copy rows were dropped, on `REQUIREMENTS.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `MAAP_FABRIC.md`, `DATAPLANE_WALKTHROUGH.md`, `FPGA_DESIGN.md`, `LITEX_SOC.md`, `overview/ARCHITECTURE.md`, `FULL_FPGA_SOLUTION.md`, `SYSTEM_DOMAIN_MAP.md`, `FR_NFR.md` and `traceability/ieee8021q.md`. No row was added.
- **Three rows now read "re-verify: quote not found":** D0-001, D0-033 and D0-056. The generator renders a missing quote this way (`scripts/docs_inventory.py:604`) and still counts it as open in the status rule (`:453-462`). The three pages carrying these rows also hold other findings, so all three stay stale.
- **Eight rows moved line:** `README.md` D0-002, 003, 004, 005, 046 and 047 by +6, and `FR_NFR.md` D0-019 and 020 by +5. Each matches the lines dev inserted above them.
- **Status changes:** nine pages go from stale to current, and `docs/design/MARK_II_STREAM_ENGINES.md` (new on dev) enters as current.
  - Totals: current goes 166 + 9 + 1 = 176, stale goes 25 - 9 = 16, obsolete stays 21, for 213 pages in all. These match the summary table.
  - `FPGA_DESIGN.md` and `FR_NFR.md` lost a copy row but stay stale on D0-057 and on D0-019/020/056.
- **The cause was checked against the source, not just the generator.** Dev `e61a4afa` (#828) rewrote the "Mark II default" sentences on each of these pages (`git diff 1f29f189 e61a4afa`). Each one now says all-fabric is the shipping default until F2 to F5 acceptance. That matches `sw/litex/milan_soc.py:4116`, where `--ctrl-mailbox` is `store_true`, and `:2873`, "default is off". So the contradiction D0-001 recorded is gone from those pages, not merely respelled.
- **Independent paraphrase probe.** I searched every non-archive page for the claim's surviving forms, with a pattern covering "default is/to bare-metal", "defaults ... to firmware/the core", "Mark II default" and "default ... packet mailbox" (`receipts/paraphrase_probe.txt`). It returned two lines. `MAILBOX_SPLIT.md:13` names the Mark II default, and its next line says all-fabric stays the shipping default. `MARK_II_AREA_PLAN.md:1580` is a decision table row about the design target. Neither repeats the contradiction.
- **Falsification probes** ran on exported copies of the head with no Git metadata (`probe_revival.sh`, `receipts/probe_revival.txt`):
  - The clean copy gives `--check` rc 0.
  - Re-appending D0-001's quote to `README.md` gives `--check` rc 1. `--write` then restores the row at the planted line 490.
  - Appending D0-033's quote to `DATAPLANE_WALKTHROUGH.md`, with underscore emphasis and no closing stop, gives `--check` rc 1. `--write` then gives that page a D0-033 row and makes it stale.
  - So the vanished rows would come back if the statement did, and nothing was dropped by hand.
- **The author's published accounting agrees exactly** with the counts and moves in `rows_delta.txt`: 87 to 76 rows, 22 to 11 copies, eight line moves, three re-verify rows and nine pages to current.

### Gates run here

| Command | Result | Receipt |
|---|---|---|
| `python3 -I scripts/docs_inventory.py --check` / `--selftest` | rc 0 / rc 0 (50 controls) | `check_before.log`, `selftest.log` |
| `python3 -I scripts/pp_srcs.py --check --selftest` (rtl-fast source-list step) | rc 0 | `pp_srcs.log` |
| `python3 -I syn/ooc/dp_srcs.py --selftest`; `--top milan_datapath`; `--top KL_pp_shadow` | rc 0 (35 self-test arms) | `dp_srcs.log` |
| `python3 scripts/ci_events.py --check` | rc 0 (2207 contract items) | `ci_events_check.log` |
| `python3 scripts/ci_gate_workflows.py --check` | rc 0 | `ci_gate_workflows_check.log` |
| `git diff --check e61a4afa HEAD` | rc 0 | `diff_check.log` |
| `python3 scripts/ci_tool_inventory.py --check` | rc 2, REFUSED: `CI_IMAGE_SHFMT` unset. This is an environment prerequisite, not a result; see limits | `ci_tool_inventory_check.log` |

`scripts/docs_inventory.json` is read only by `scripts/docs_inventory.py`. `pp_srcs.py` and `dp_srcs.py` do not read it. They were run because the brief names them as the rtl-fast source-list steps, and because the merge brought dev's RTL and SoC changes.

### Author packet

- Evidence commit `82a31a67` carries `review-evidence/797d0-r1/author-r5`, with 281 files. All 281 match `published_sha256` in `MANIFEST.json`, with no unlisted file (`receipts/author_r5_manifest_verify.txt`, `verify_manifest.py`).
- **The packet is not signed.** GitHub reports the evidence commit as `unsigned`. Its integrity rests on the manifest digests and the commit.
- Spot-checks of the packet:
  - `receipts/regen/check-merged-before-write` shows rc 1 on the merged tree before regeneration (166 to 176 at line 30), and `write` and `check-after-write` show rc 0.
  - `probes/stale-page-mutants` shows three arms, each giving rc 1, then rc 0 after `--write`.
  - `gates/docs-yml-verify.rc` and `rtl-fast-verify.rc` are both 0.
  - These agree with my own runs.

### Dev content the merge brought

- The delta's code changes come from dev `e61a4afa`, which was reviewed in its own PRs (#828, #829/#831). I read them only for what this audit depends on. `milan_datapath.sv` gains 6 parameter lines at `:85` and 2 binding lines near `:8882`. `milan_soc.py` gains MII launch-shape tables at `:1440` and observer wiring near `:2079-2187`. None of these touches the substance of a remaining finding (classifier/CBS, MAC_STATUS, counters, saved state and similar).
- The page states that findings cite lines at dev `1f29f189`, and the citations stay correct at that pin. See S2.
- Gitlinks are unchanged from dev (`git diff --stat e61a4afa HEAD` lists no gitlink).
- **Comment rule.** The lane added no source comment in this round; its only own change is the generated page. That page's lane column ("Verified by D0", "area lane") is a findings and inventory artifact, which may name lanes. There is no new RESIDUE under the rule.

## Findings

No BLOCKER, MAJOR or MINOR.

### R1 - RESIDUE - Docs - PR #815 body, line 16 ("Status") and line 114 ("Known limitations") - the hosted statements are stale again

- **Authority/evidence:** the PR head is `e8ec8d20`, non-draft, and its check runs exist (`receipts/hosted_check_runs.txt`). The body still says "GREEN locally; hosted not yet run" (line 16) and "this head has no hosted run until it is pushed" (line 114). This is the same cause as R741-4 R1 and R742-4 R1: the text describes push state, which goes stale on the next push.
- **Impact:** a cold reader is told the head is unpushed and has no hosted runs. Nothing else is affected: no measurement, code or verdict changes.
- **Required outcome, exact fix (manager, PR body). Use wording that does not depend on the push state:**
  - Line 16: replace "GREEN locally; hosted not yet run." with "GREEN locally. Hosted results at `e8ec8d20` are read from its check runs; the manager owns their acceptance."
  - Line 114: replace the bullet with "Hosted result: read from the exact-head check runs of `e8ec8d20`; local results above are not hosted evidence."
- **Verification:** read the body against `gh pr view 815 --json headRefOid` and the head's check runs.

### R2 - RESIDUE (retained from R741-4 R2) - Docs - `scripts/docs_inventory.py:32` - "the punctuation ending it" is wider than the code

- **Authority/evidence:** `needle_of()` at `scripts/docs_inventory.py:374` strips only `.,;:`. The generator is unchanged in this round, so the docstring is unchanged. The PR-body half of R741-4 R2 no longer appears: the body has no "punctuation" text.
- **Impact:** wording only. No recorded statement ends in `!` or `?`.
- **Required outcome, exact fix:** change "the punctuation ending it" to "the full stop, comma, semicolon or colon ending it". The edit moves the digest at `ci/image/command-table.json:13701`, so it can wait for the next edit of the file, as the author proposed.
- **Verification:** read `:32` against `:374`, and check that the command-table digest still matches.

### S1 - SUGGESTION - Conformance, Docs - `scripts/docs_inventory.json` D0-001, D0-033, D0-056 - three entries now fixed upstream remain as "re-verify" rows

- **Evidence:**
  - Dev's rewrite removed each quote and every copy (see "What moved").
  - D0-001's correction asks the default build to keep all five functions in fabric. The README now says exactly that (`README.md:63`).
  - D0-001's correction also defers `REQUIREMENTS.md` to "a maintainer decision on what 'Mark II default' names". `REQUIREMENTS.md:28` now says the all-fabric build is the shipping default, and the PR body (line 61) points at NFR-SCOUT-02 as the owner decision.
  - The data file's own instruction (`docs/DOCUMENTATION_AUDIT.md` Findings preamble) is to remove an entry once no copy row remains.
- **Impact:** none on correctness. The rows are visibly marked re-verify, and each page stays stale on its other findings, so nothing is hidden. Until the entries are retired, the summary counts three open findings that the source no longer carries.
- **Suggested outcome:** when the owner confirms the decision, a lane re-verifies the three statements and removes the entries, through the generator, in one commit.
- **Verification:** `--check` rc 0, 73 rows, and pages `README.md`, `AXIS_CORES_ON_BAREMETAL_SOC.md` and `FR_NFR.md` stay stale on their remaining findings.

### S2 - SUGGESTION - Docs - `docs/DOCUMENTATION_AUDIT.md:26` and the Findings "Contradicted by" cells - citations pinned at `1f29f189` now trail the merged tree

- **Evidence:**
  - The page states "Findings cite source lines at dev `1f29f189`".
  - After the merge, `hdl/milan/milan_datapath.sv` lines after `:85` sit 6 lower. That affects, for example, D0-002 `734-750`, D0-029/030 `684-694` and D0-049 `6709-6710`.
  - `sw/litex/milan_soc.py` lines after `:1440` sit 10 to 19 lower. For example, D0-001's `2854-2856`/`4097` are now `2873`/`4116`.
  - The pin makes every citation reproducible. A reader at dev after the merge needs to check out `1f29f189`.
- **Suggested outcome:** re-pin the citations to the base current when the area lanes next change the data file. Alternatively, have the generator print the pin beside each "Contradicted by" cell.
- **Verification:** sample cited lines at the new pin.

### Prior public findings at this head

I read these after my own pass over the delta and my probes, and before writing this verdict. I read the published R741-4 and R742-4 reports. No round-5 report from another reviewer had been published when I listed the comments.

| Prior item | Disposition | Evidence |
|---|---|---|
| R741-4 R1 / R742-4 R1 RESIDUE, PR body hosted status | **Applied, then overtaken again** | The `8d8c2e36` wording was replaced. The new wording is stale since the push. Carried as R1 with wording that does not depend on push state |
| R741-4 R2 RESIDUE, "punctuation ending it" | **Docstring part retained; PR-body part resolved** | R2 above |
| R741-4 S1 / R742-4 S3 SUGGESTION, broad `also` fragments (D0-059, D0-002) | **RETAINED, optional** | Data file unchanged |
| R741-4 S2 / R742-4 S2 SUGGESTION, a quote that normalises to nothing is accepted | **RETAINED, optional** | Generator unchanged |
| R741-4 S3 / R742-4 S1 SUGGESTION, surviving self-test mutants | **RETAINED, optional** | Generator unchanged |
| R741-4 S4 / R742-4 S4 SUGGESTION, 999 lines against the 1,000-line limit | **RETAINED, optional** | Generator unchanged |
| R742-4 S5 SUGGESTION, watcher expiry cancels healthy runs | **RETAINED, optional, outside this PR** | Not touched |
| Round 1 to round 3 BLOCKER, MAJOR and MINOR findings (source-list gate literal path, search misses and earlier) | **Stay RESOLVED** | The delta leaves the generator, the data file and the source-list gate unchanged, and `pp_srcs.py --check --selftest` gives rc 0 at this head |
| Round 1 to round 3 optional suggestions | **RETAINED, optional** | Not touched by the delta |

The unresolved decisions are not findings: what "Mark II default" names (S1 records that dev may have settled it), and the owner additions of 2026-10-30. Both are published in the PR body.

## Lens results

```text
[R741] PASS Conformance - receipts/rows_delta.txt; git diff 1f29f189 e61a4afa on README.md, REQUIREMENTS.md:28, FR_NFR.md:75-78, AXIS_CORES_ON_BAREMETAL_SOC.md:21, ARCHITECTURE_HW_SW_SPLIT.md:6 against sw/litex/milan_soc.py:2873,4116; receipts/paraphrase_probe.txt - every row that left or reads re-verify follows a real upstream fix, no remaining finding's evidence changed in substance; S1 optional
[R741] PASS RTL - git diff e61a4afa e8ec8d20 has no hdl, tb, syn, sw or gitlink path; merge-tree recompute equals b48b2fd5's tree; pp_srcs.py and dp_srcs.py rc 0; milan_datapath.sv:85-90,8882-8883 and milan_soc.py:1440-1450 read for the cited findings - the lane changes no RTL, and the dev RTL the merge brought leaves every finding's substance intact
[R741] PASS Robustness - receipts/probe_revival.txt (clean export without Git metadata, quote re-planted, underscore-emphasis copy without a closing stop) and scripts/docs_inventory.py:453-462,604 - vanished rows come back with the statement, and re-verify rows still hold their page stale
[R741] PASS Tests - receipts/selftest.log (50 controls); check_before.log / write.log / check_after.log with the committed blob reproduced byte for byte; findings-dir output equal to the published packet; author's 281-file packet verified - prior suggestions S1-S4 retained, optional
[R741] PASS Docs - docs/DOCUMENTATION_AUDIT.md at e8ec8d20 (213 pages, 176/16/21, 76 rows), docs/README.md merge, PR #815 body lines 16, 34-61 and 100-114 - counts and moves are stated correctly; R1 and R2 are wording residue only, S2 optional
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 optional) | Findings rows and page statuses at `8d8c2e36` and the head (`rows_delta.txt`); dev's rewrite of the "Mark II default" sentences against `milan_soc.py:2873,4116`; `paraphrase_probe.txt` | R741-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |
| RTL | CLEAN | `merge_and_delta.txt` (merge-tree recompute, both-sides file list, gitlinks); `pp_srcs.log`, `dp_srcs.log`; dev's `milan_datapath.sv` and `milan_soc.py` hunks read against the findings | R741-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |
| Robustness | CLEAN (prior S retained) | `probe_revival.txt`; `scripts/docs_inventory.py:453-462,604`; no-Git export `--check` | R741-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |
| Tests | CLEAN (prior S retained) | `selftest.log`; `check_before.log`, `write.log`, `check_after.log`, `regen_identity.txt`; `findings_dir_vs_published.diff`; `author_r5_manifest_verify.txt` | R741-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |
| Docs | CLEAN (R1, R2 residue; S2 optional) | `docs/DOCUMENTATION_AUDIT.md`; `docs/README.md` merge (`merge_and_delta.txt`); PR #815 body | R741-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |

## Real limits

- **Hosted evidence is incomplete.** At the snapshot, 19 of 23 exact-head check runs were queued and 3 were in progress. None of `rtl-fast`, `docs`, `verilator-suites` or `yosys-portability` had a result. Round 4 noted the earlier head lost its `rtl-full` result to a watcher cancellation, and that may recur.
- **Not run here:**
  - `scripts/ci_tool_inventory.py --check` refused for want of the pinned shfmt (`CI_IMAGE_SHFMT`).
  - The full docs and rtl-fast step sets were not rerun; I relied on the author's verified receipts (verify rc 0).
  - No Docker or act run, no parent, processor, gPTP, Yosys or builder bank, and no Verilator build. No Verilator build was needed, because the delta changes no RTL owned by this lane.
- **Not re-verified:** no recorded statement was re-verified against current source beyond the D0-001 family and the dev hunks read above. That matches the author's declared limit.
- **No manager source bank** ran at this head, and none is claimed. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **The packet is unsigned.** Its integrity rests on the `MANIFEST.json` digests and evidence commit `82a31a67`.

## Pending manager duties

- Read and accept the exact-head hosted contexts once they finish, including `verilator-suites` and `yosys-portability`.
- Build and validate the current-dev merge candidate (source base `e61a4afa`, live dev `e61a4afa` at review time) with the builder and native banks, and link the receipts.
- Apply R1 to the PR body. Carry R2 to the residue checklist.
- Route S1 to the owner's "Mark II default" decision.
- Obtain the second independent positive review at this head.

## Clone state after review

`HEAD` is `e8ec8d20` with tree `274a5320`. `git status --porcelain --ignored` is empty: I removed the `scripts/__pycache__` my runs created. The index modes and blobs equal the HEAD tree, and the six gitlinks equal dev's (`receipts/restore_verify.txt`).

R741-5 FINISHED
