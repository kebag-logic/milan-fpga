[R721] POSITIVE - exact head b0473e697e0f93e3bb38a4da1ba2ad48012d2253

# R721-3: independent internal review of FPGA-gPTP PR #93 (issues #87, #88)

- **Head:** `b0473e697e0f93e3bb38a4da1ba2ad48012d2253`, tree `0b2113f42183b37bbe253d1181c06d7b8ea41e5a`. The review clone was verified byte-exact at the end: HEAD, tree and index tree match, the worktree is clean, and there are no gitlinks (`receipts/clone_integrity.txt`).
- **Source base:** `55680bff`. Main, merged in: `3426089a` (PR #92: #89, #90, #91).
- **Previously reviewed head:** `c1bc9e21`. R721-1 was NEGATIVE with 3 MINOR and 1 SUGGESTION; R722-1 was POSITIVE with 1 RESIDUE and 4 SUGGESTION. No R721-2 report was published, because the round was superseded by the merge round.
- **Delta judged in this round** (`c1bc9e21..b0473e69`):
  - `7c71dcb`: the strict named-check prefix `#87 `;
  - `5ed415a`: `PAIRS = ((`;
  - `98edabb`: the merge of main `3426089a`, with conflicts in `tb/verilator/engine/mutants.py`, `tb/verilator/engine/sim_main.cpp` and `docs/SOURCE_EVIDENCE.md`;
  - `b0473e6`: the two #88 issue shapes move to phase 43.
- **Code outside the delta:** the parser and engine RTL is byte-unchanged since `c1bc9e21`. Its lens verdicts from R721-1 carry forward unless the merge changes something they depend on, and that dependency was checked (below).

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head.

- **Merge:** keeps both sides. Every line each side changed from `55680bff` is carried by the merge. The only differences are the intended union of the strict-prefix tuple and one SOURCE_EVIDENCE anchor row that was re-anchored to the merged engine line numbers.
- **ROM images:** byte-identical to main's, and they regenerate identically from the head generator. The generator's change from main is comments only. Its sole reader of bank word 12 (`gen_gptp_ucode.py:1099`, which shifts right by 8 and then does a 32-bit compare) is unchanged, so the new presence bit 63 stays outside what the microcode reads.
- **Phase 43:** the relocation keeps the #88 issue acceptance. Both issue shapes come from a better grandmaster (priority1 247 against 248). Both are elected, defer for a whole Announce interval while the parent's usable Sync flows, and publish the received head.
  - Restoring either removed refusal is caught. In this round's own run, each restored refusal printed FAIL on `no longer master` (got AMGM) and on `no Announce for one interval` (got 1), which reproduces the issue's symptom.
- **Prior findings:** R721-1 F1, F2 and F3 are resolved at their cause, and S1 is applied. R722-1's RESIDUE is retained unchanged; it lies outside the delta.
- **New items:** one RESIDUE (a stale phase-index comment left by the relocation) and one SUGGESTION.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R721-3-F1 | RESIDUE | Tests, Docs | `tb/verilator/engine/sim_main.cpp:85-89` (the phase index entry for 8o) and `:2608` (the 8o banner) | `b0473e6` moved the only engine case of "a path not headed by its grandmaster" (`#88 head not the grandmaster`) out of 8o into phase 43 (`:5958-5971`). 8o now holds only `#88 two entries, stepsRemoved 5` and `#88 three entries, stepsRemoved 0`, and both are headed by their grandmaster (`:2615-2627`). The 8o function comment was updated (`:2611`, "Every path below has a count other than stepsRemoved+1"). The index line at `:86-87` ("or whose path is not headed by it") and the banner "neither the path count nor its head disqualifies" were not. | Comment wording only. No check, figure, verdict or code depends on it, and the head case is still covered, in phase 43. | At `:85-89`, read: `// 8o      #88: a better grandmaster whose path count is not stepsRemoved+1` / `//         (a NOTE to 802.1AS-2011 10.5.3.3.4) is elected, and its path is` / `//         published as received from entry 0 with thisClock appended, and` / `//         every degraded grandmaster yields. A path not headed by its` / `//         grandmaster, with the issue's two shapes, is phase 43`. At `:2608`, read `// ---- 8o: #88, the path count does not disqualify ---…` (keep the rule width). | Read `:85-89` and `:2608` against `:2615-2627` and `:5958-5971`. |
| R721-3-S1 | SUGGESTION | Tests | `tb/verilator/engine/sim_main.cpp:5959` (phase 43, after the degraded GMS Announce) | The first issue shape's `no longer master` and `no Announce for one interval` checks hold the deferral only if this plane is master right before the 247 Announce. No clean-run check states that precondition. It is proven today only indirectly: under both restored-refusal mutants, `no longer master` reads AMGM set (`receipts/engine_subset_runs/run_the_path_count_refusal_restored.log:34`, `run_the_path_head_refusal_restored.log:27`). The second shape's precondition is the first shape's `the degraded grandmaster yields` check. | The suite and arm are correct today. A later change to the phases before 43 could leave the plane slave there, and the first shape's deferral checks would then pass vacuously in the clean run. | Optional: after `:5959`, add `expect("#88 issue shapes: the degraded GMS hands mastership back", dut->pub_gm_id_o == OUR_CID && (dut->pub_flags_o & FL_AMGM), 1);`. | The engine suite stays green, and both restored-refusal mutants are still caught. |

## Prior public findings at this head

| Prior finding | State at `b0473e69` | Evidence |
|---|---|---|
| R721-1 F1 MINOR (the #87 mutants were not held to every named check) | **Resolved** | `tb/verilator/engine/mutants.py:888-892`: the strict prefixes are `#82 #84 #85 #87 #88 #89 #90 #91` and `p1 255`. In this round's own subset run, under that strict rule, `the empty sequence published without a TLV` and `a TLV-less Announce publishes {thisClock}` are both `[PASS] mutant caught` (`receipts/engine_subset.log`). The published head arm reports 113/113, with 2/2 #87 mutants failing 19/19 named checks (`author-r3/receipts/engine-merge/merge-checks.txt`, hash-verified). |
| R721-1 F2 MINOR (the parent `REGISTER_MAP_CLASSES.md` row for 0x7DC–0x7E4) | **Resolved** (companion) | The stacked companion (sha256 `3a3db518…`, verified) rewrites that row to the 2011 rules: entries from entry 0; a TLV copied as received with thisClock appended; an empty TLV gives `{thisClock}`; no TLV keeps the previous pathTrace; Table 5.22 compares `(count ? entry 0 : 0, count, active tails)`. The patch adds no line containing `count zero` or `count ? GM`. |
| R721-1 F3 MINOR (no check of the entry-0-only change) | **Resolved** (companion) | The companion adds the `entry-0-only change …` checks in gptp_shadow (patch lines 637-645) and milan_dp `gptp` (1073-1092). Control C3 fails 2 of them on the stacked companion (`author-r3/…/C3_….log`). Control C2 fails gptp_shadow 2 and milan_dp 1 (`author-r2/…/C2_….log`). The changed lines in `KL_gptp_shadow.sv` and in the gptp_shadow `sim_main.cpp` are identical between the round-2 and round-3 companions, so C2 still applies to that bench. All files are hash-verified against the evidence manifest. |
| R721-1 S1 SUGGESTION (`PAIRS =((`) | **Applied** | `tb/verilator/parser/mutants.py:134`. |
| R722-1 F1 RESIDUE ("one to eight" leaves out the gated zero case) | **Retained**, unchanged (outside the delta) | `docs/INTEGRATION.md:472` and `hdl/top/KL_gptp_engine.sv:121` against `:1062-1064`. The manager carries it to the residue checklist with R722-1's exact fix. |
| R722-1 S1-S4 SUGGESTION | Unchanged; outside the delta | No action is required by this round. |

## Lens evidence (delta-scoped)

### Conformance: CLEAN

- **Scope from the issue acceptance:**
  - #88: a short path trace, and a path not headed by its grandmaster, each from a better grandmaster. The end station defers, and a restored refusal is caught.
  - #87 (ruling): with no TLV, the previous pathTrace stays.
  - Ruling (A): `pub_path_o` carries eight entries from entry 0, and entry 0 is the received head.
- **RTL against 802.1AS-2011 10.3.10.2.1 a)-d):** the RTL is unchanged since `c1bc9e21`, where R721-1 and R722-1 both judged it conformant. A spot re-read at head confirms:
  - `KL_gptp_rx_parser.sv:318-322`: the PathTrace framing keeps only 8N and the singular-TLV rule;
  - `:566-579`: presence is marked for an empty TLV and for a non-empty one;
  - `KL_gptp_engine.sv:986-1003`: address 7 copies from entry 0 and appends thisClock only when a TLV is present; otherwise the path is kept.
- **Merge interaction with #89 ageing:** an elected grandmaster with no Sync is aged (802.1AS-2011 10.3.11, Figure 10-13 per Cor1). The test answer, feeding the parent's usable Sync during the deferral interval, is the protocol-correct premise for "defer a whole interval". It does not weaken the #88 rule.

### RTL: CLEAN

- **RTL files:** there is no RTL change in `c1bc9e21..b0473e69` (`git diff --stat c1bc9e21 HEAD -- hdl/wire hdl/top` is empty).
- **Generator:** its change from main is comment-only (22+/17−, all `#` comments or docstring).
- **ROM images:** byte-identical to main's in all four images, and they regenerate identically (`gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000` is `cmp`-equal to `tb/verilator/engine/gptp_ucode.hex`).
- **Lint:** `make lint` rc 0 with the pinned simulator 5.050 (`receipts/contract_docs_lint_head.log`).

### Robustness: CLEAN

- The merge adds no RTL path. The only bank-word-12 reader in the merged microcode is unchanged, and it reads below bit 40.
- The R721-1 robustness probes covered presence against zero-gap capture, stale-entry gating, EOF and mid-chain empty TLVs, and warm reset. They still apply to identical RTL.
- The merged #89/#90/#91 rules run against this RTL in the whole engine suite: 1977 ×3 + 60, all PASS, in this round's own run.

### Tests: CLEAN (one RESIDUE, one SUGGESTION)

- **Merge preservation:** `scripts/merge_sides.py` was run on every file each side changed (`receipts/merge_branch_side.txt`, `merge_branch_side_all.txt`, `merge_main_side.txt`).
  - Every added or removed line of each side is on the merge.
  - The exceptions are the strict-prefix tuple and its comment (the intended union) and the SOURCE_EVIDENCE slew-level row (re-anchored, and `check_source_evidence.py` reports 20 exact, 0 findings).
- **Arm union:** 112 entries. The three entries missing from the union each match a deletion made by one side (`merge-checks.txt`):
  - main's two retired 2020-rule mutants, deleted by this branch;
  - this branch's copy of `the receipt timeout publishes nothing`, deleted by main.
- **`b0473e6`:** the two shapes now run from `defer_a_whole_interval_to_the_issue_shapes()` (`:5958`). It is called after phase 40 and before the whole-run grades (`:425`), and it feeds nine 125 ms usable Sync intervals from the elected parent port (`:2664-2665`).
  - No check is added, removed or renamed. The names match what `mutants.py` refers to: `:603`, `:628-637`, `:680`, `:773`.
  - The author's receipt `engine-merge/sync-fed-in-place-at-8o-pass1.log` shows why the shapes were not left at 8o with Sync fed there: `late FU never steers` fails (got 0x14, expected 2).
- **This round's runs at the exact head** (scratch copies made by `git archive`, pinned simulator 5.050):
  - engine suite rc 0: 1977/1977 ×3 and 60/60 (`receipts/engine_suite_head.log`);
  - parser suite and arm rc 0: 378/378 and 16/16 (`receipts/parser_suite_head.log`);
  - the targeted engine-arm subset (every mutant naming an issue-shape check or a #87 check), graded by the arm's own `run_mutant`/`named_verdict`: control pass, 10/10 caught (`receipts/engine_subset.log`, with per-mutant harness output in `receipts/engine_subset_runs/`).
- **Full engine arm:** this round's own full-arm run did not complete; that job ended without an exit code and was not re-run. The full arm is taken from the author's published head gate: `head-repo/04.log` reports 113 checks, 113 PASS, 0 `[FAIL]` and 0 `missed its named`, and `head-repo/results.json` binds that run to head `b0473e69`. All of it is hash-verified.

### Docs: CLEAN (one RESIDUE)

- `make docs` rc 0: diagrams pass; docs check 11 current / 17 historical pages; source evidence 20 exact, 0 findings; all selftests pass.
- The auto-merged #92 text in `INTEGRATION.md`, `HDL_DEVELOPER.md`, `TEST_DEVELOPER.md` and `MANAGER.md` is consistent with the #87/#88 text. "After reset or mastership, that is thisClock alone" (`INTEGRATION.md:510`) also holds for #89's ageing-driven mastership.
- **Comment rule:** the delta's added lines contain no bench lane label, lane name, review round, reviewer ID or issue-comment ID. A scan of `c1bc9e21..5ed415a`, `5ed415a..b0473e6` and `3426089a..b0473e6` found only false positives on the word "plane".
- **PR body:** its figures were checked against the published receipts: 1977 ×3 + 60; arm 113/113; 79 strict mutants and 332 named checks (24+6+9+2+9+15+4+3+7 and 80+13+99+19+51+38+15+7+10); parser 378 and 16/16; companion sha256 `3a3db518…`; stacking order. All agree.

## Gates and runs (all waited on in the foreground, each with its own log and exit code)

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/engine run` (4 passes) | rc 0; 1977/1977 ×3, 60/60 | `receipts/engine_suite_head.log`, `.rc` |
| `make -C tb/verilator/parser` (suite and arm) | rc 0; 378/378, arm 16/16 | `receipts/parser_suite_head.log`, `.rc` |
| `make contract`, `make docs`, `make lint` | rc 0 each | `receipts/contract_docs_lint_head.log` |
| Engine-arm subset (10 mutants, 8 jobs) | control pass; 10/10 caught | `receipts/engine_subset.log`, `.rc`, `receipts/engine_subset_runs/` |
| Full engine arm | **not completed here**; the author's head receipt was used (113/113) | see Tests |
| Merge side preservation | both sides carried | `receipts/merge_*.txt`, `scripts/merge_sides.py` |
| Evidence hashes (author-r3 receipts, the companion patches, and the round-2 C2 control) | 102 verified, 0 mismatched | `receipts/evidence_verify.txt`, `scripts/verify_evidence.py` |
| Hosted checks at the exact head | none: 0 check runs, combined status `pending`, and the repository has no workflow directory | GitHub API, read-only |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 802.1AS-2011+Cor1/Cor2 10.3.10.2.1 a)-d), 10.3.11 (Cor1 Figure 10-13) and 10.5.3.3.4 NOTE, read against parser `:318-322`, `:566-579` and engine `:986-1003`, which are unchanged since R721-1; the phase-43 premise; companion `REGISTER_MAP_CLASSES.md` row | R721-3 (RTL carried from R721-1) | b0473e697e0f93e3bb38a4da1ba2ad48012d2253 |
| RTL | CLEAN | empty RTL delta; generator diff from main (comments only); identity of the 4 ROM images and their regeneration; the single w12 reader; lint rc 0 | R721-3 (RTL carried from R721-1) | b0473e697e0f93e3bb38a4da1ba2ad48012d2253 |
| Robustness | CLEAN | the merge adds no RTL path; the merged #89-#91 rules run through the full engine suite against this RTL; R721-1 probes R1-R6 still apply to identical RTL | R721-3 (probes carried from R721-1) | b0473e697e0f93e3bb38a4da1ba2ad48012d2253 |
| Tests | CLEAN (R721-3-F1 RESIDUE, R721-3-S1) | merge preservation for all files on both sides; the arm union of 112; `b0473e6` phase 43; strict-prefix gate `mutants.py:888-892`; engine suite, parser suite and arm run here; engine-arm subset 10/10; published head arm 113/113; companion C2/C3 controls and the entry-0-only checks | R721-3 | b0473e697e0f93e3bb38a4da1ba2ad48012d2253 |
| Docs | CLEAN (R721-3-F1 RESIDUE; R722-1 F1 RESIDUE retained) | `INTEGRATION.md`, `HDL_DEVELOPER.md`, `TEST_DEVELOPER.md`, `MANAGER.md`, `SOURCE_EVIDENCE.md` at the merge head; `make docs` rc 0; comment-rule scan of the delta; PR body figures; companion `REGISTER_MAP_CLASSES.md` | R721-3 | b0473e697e0f93e3bb38a4da1ba2ad48012d2253 |

## Real limits

- **Full engine arm:** this round's own run of the full arm did not complete (the job ended without an exit code), and it was not re-run because of its cost (about 2 h serially). The 113/113 result comes from the author's published, hash-verified head receipt. This round independently re-ran only the 10 mutants that the relocation and the #87 fix touch.
- **Not re-run here:** gaskets, tsngen, ucpu, `bench/arty` and the OOC selftest. They are unaffected by the delta, and the author's head receipts are rc 0.
- **Not run here:** the milan-fpga consumer list and tsn_fuzz `ptp` with both companions stacked. These rest on the author's published receipts (`head-parent/`, `head-fuzz/`) and on hash verification. The companion patch was inspected, not applied.
- **No manager bank:** no manager source bank ran at this head, and none is claimed or inferred. The source execution evidence is the author's published gate receipts, plus this round's runs listed above.
- **No hardware evidence:** physical calibration was NOT RUN. Simulation results and field skips are not hardware proof.
- **Hosted checks:** none exist at this head.

## Pending manager duties

- At the merge turn, build and validate the current-dev merge candidate (source base `55680bff`, live dev `5fcec84b`), including the builder and native banks, and link its receipts on the PR.
- At pin adoption, carry the stacked companion order: #92's `b53944d5…` first, then this lane's `3a3db518…`.
- Hosted and act acceptance is owned by the manager; no hosted runs exist at this head.
- Add R721-3-F1 (exact fix above) and the retained R722-1 F1 to the residue checklist.
- Physical calibration and parent acceptance against the reference peer remain open under their own issues.

R721-3 FINISHED
