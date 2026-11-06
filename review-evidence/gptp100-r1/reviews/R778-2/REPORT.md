[R778] POSITIVE - exact head 84fd22781c95f7b7e65d7d18c99a5ed49a68e11c

# R778-2 independent review: Mister-M-alt/FPGA-gPTP PR #101 (issue #100), round 2

- Exact head `84fd22781c95f7b7e65d7d18c99a5ed49a68e11c`, tree `46aadfe70a0df98aaeaf4c52efacd4793d1fd27c`. Both were verified in the review clone, and the index tree equals the head tree (`receipts/integrity.log`).
- Round 2 delta: `3e3f041..84fd227`. That is the merge `1615187` of main `5184fb3` (PR #99), followed by the wording commits `1400c83`, `1d61f9e` and `84fd227`.
- Source base `3e3a4e7695ce66eed609089f280c2fba45b24d36`; live dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`. The manager builds the current-dev merge candidate at the merge turn, and no manager source bank is claimed or inferred here.
- Scope follows the round 2 assignment on issue #100: (1) the merge, (2) the suites, both mutation arms and the parent consumer gates with #99 and #100 together, and (3) the three wording items. Round 1 RTL is not re-reviewed. Code the delta does not touch keeps its round 1 lens verdict from R778-1 at `3e3f041`.

## Verdict

POSITIVE. There is no open BLOCKER, MAJOR or MINOR finding.

- The merge keeps both sides. Every anchor resolves exactly through the source-evidence checker.
- The only change to `hdl/` or `tb/` beyond PR #99 is a help string, and it prints the same text and leaves the ROM unchanged.
- The suites and the #100 mutation controls pass at the head, run by this reviewer.
- The three wording items are correct against their clauses.

There are two RESIDUE wording items (R1 and R2) and no new SUGGESTION.

## Reconstruction (order followed)

1. The repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md`, `docs/README.md` (truth order, the `make docs` gate), `docs/MANAGER.md` and the `Makefile`.
2. Issue #100: the frozen acceptance and the maintainer decisions of 2026-11-05. The round 2 assignment (issuecomment-6670464742) sets the merge, the three wording items, "no other change" and the gates.
3. PR #101 body at the head, including the "Round 2" section.
4. My own pass over `git diff 3e3a4e7..84fd227`, `3e3f041..84fd227`, `1615187..84fd227` and `5184fb3..84fd227`, plus the history graph.
5. Public evidence at `kebag-logic/milan-fpga@0b04253`, `review-evidence/gptp100-r1/`: `MANIFEST.json` and everything under `author-r2/`. I did not open `reviews/` before writing this verdict, and did not open round 1's `author/` material.
6. After that pass, the prior public reviews R777-1 (issuecomment-6669054367) and R778-1 (issuecomment-6670441467), read for their findings only.

## Focus item (1): the merge keeps both sides

| Check | Evidence | Result |
|---|---|---|
| Merge shape | `1615187` has parents `3e3f041` and `5184fb3`. Subject "Merge main 5184fb3 into 100-followup-tlv-values", no body, no trailers (`receipts/static/03-merge-msg.log`) | As assigned |
| Union of both sides | `git merge-tree --write-tree 3e3f041 5184fb3` gives tree `9ba112a`. It differs from `1615187` only in `docs/SOURCE_EVIDENCE.md`, the one conflicted file (`receipts/static/02-merge-tree.log`). Every auto-merged file is exactly the merge machinery's result | Both sides kept |
| Conflict resolution | The hunk keeps main's `KL_gptp_rx_parser.sv#L439` and the branch's engine anchors `#L559`, `#L586`, `#L407` and `#L413`. "Ignored receive flag bits" auto-merged to main's `#L521`. This matches the round 1 handoff and the assignment | Correct |
| Anchors re-pointed | `check_source_evidence.py`: "20 exact, 0 findings"; selftest 7 arms PASS (`receipts/static/07-source-evidence.log`, `06-make-docs.log`). I read every anchored line at the head (`08-anchor-lines.log`). `#L439` is `if (fin_r) begin` (the deferred event) and `#L521` is the flags capture | Exact |
| No behaviour change beyond #99 | The engine RTL (`hdl/top`, `hdl/ucpu`, `hdl/common`), `hdl/ucode`, the engine `mutants.py`, `p100_mutants.py` and the engine `Makefile` are identical at `3e3f041` and `1615187`. At the head, `hdl/wire`, `tb/verilator/parser` and `scripts/check_docs*.py` are identical to main (`05-...log`). After the merge, only `gen_gptp_ucode.py` (help string) and two guides change (`04-delta-stat.log`). Main's `tb/verilator/engine/sim_main.cpp` hunk is comments only | Holds |
| Help string and ROM | `--help` output is byte-identical at `1615187` and at the head (`11-help-diff.log`). The regenerated engine ROM matches the committed image (`12-rom-regen.log`). No hex file changes after the merge | No behaviour change |
| Whitespace | `git diff --check 5184fb3 84fd227` rc 0 (`13-diff-check.log`) | Clean |
| Mergeability | GitHub reports the PR `MERGEABLE` / `CLEAN` at the head | Read-only observation |

## Focus item (2): #99 and #100 together

| Gate | Reviewer run at head (pinned Verilator 5.050, `receipts/dynamic/`) | Author receipt (hash-verified) |
|---|---|---|
| Parser suite and arm in full (`make -C tb/verilator/parser`) | 482 checks, 0 FAIL. Arm: 35 checks (control and 34 mutants, 19 of them the #98 TLV walk), 0 FAIL; rc 0 | `final/repo-gates-84fd227/03.log`: same counts |
| Engine suite (`make -C tb/verilator/engine run`) | 2,098 × 3 shipping passes and 61 in the fourth pass (`--p1 255 --clock-accuracy 0xFE`), 0 FAIL; rc 0 | `04.log`: same counts |
| Engine arm | Not run in full. I ran a subset: the arm's own control and all 24 #100 controls, through `mutants.run_mutant()` (`scripts/engine_arm_subset.py`, 8 workers). 25/25 PASS, each mutant failing every check it names, the clock-accuracy controls included; rc 0 | `final/engine-arm-84fd227/jobs.md`: "160 checks: 160 PASS, 0 FAIL" (control and 159 mutants). The driver (`tools/arm_jobs.py`) only calls the arm's own `stage`, `build`, `generate_image`, `run_harness`, `verdict` and `run_mutant`, so it has the same verdict semantics as `mutants.main()` |
| Parent `gptp_shadow` | Not run (outside this review's allowance) | `final/parent-A-84fd227/01.log`: 325 checks, 0 FAIL, RESULT PASS |
| Parent `milan_dp gptp` / `gptp-lat` | Not run | `02.log` and `03.log`: 210 checks each, 0 FAIL |
| Parent gitlink identity | n/a | `11.log` (xvlog gate): "gptp-processor@84fd2278 - the superproject gitlink". The scratch parent commit `2278661` is local and unpublished |
| Other parent gates | n/a | `milan_dp_gptp` (physical suite, 151 checks; controls 6/20/14/14), `gm_steps` 196, plane/txts/tables, idiom, xvlog and lint gates: rc 0. Builder: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 needs a place report). `tsn_fuzz ptp`: its field campaign was skipped, which is not a pass |
| OOC (author) | n/a | `ooc-84fd227/engine_util.rpt`: 5,395 LUTs (4,905 + 490), 3,620 FFs, 6 DSPs. `engine_timing.rpt`: WNS +2.043 ns, 0 of 12,372 failing. Main's figures are 4,920 / 3,461 / 4 DSPs / +2.249 ns. These match the PR table |

The author packet's integrity:

- All 65 `author-r2/` files match their `published_sha256` in `MANIFEST.json`, and no file is unlisted (`receipts/author-packet-verify.log`).
- Logs are host-path-redacted copies, so their `original_sha256` values cannot be reproduced here.
- The evidence commit `0b04253` is not cryptographically signed: GitHub reports "unsigned". Integrity therefore rests on the manifest inside that same commit.

## Focus item (3): the three wording items

| Item | At head | Check | Result |
|---|---|---|---|
| R777-1 R1 / R778-1 P3 | `docs/HDL_DEVELOPER.md:328`: "Region 6 serves gmTimeBaseIndicator, lastGmPhaseChange as ScaledNs." and `:330`: "It also serves scaledLastGmFreqChange, scaled by 2^41." | The review's exact 13-word sentence fails the 10-word docs gate (author receipt `residue/r777-r1-exact-text-docs-check.log`, rc 1), so shortening it is justified. The scale 2^41 is 11.4.4.3.9's, and the line moved from `:320` to `:328` because of #99's eight lines. The split keeps the fix's content, but its first sentence still lets "as ScaledNs" read over gmTimeBaseIndicator. That ambiguity is the defect R1 was raised for | Resolved, with wording residue R1 |
| R778-1 S3 | `docs/INTEGRATION.md:857-865` | 11.4.4.3.8 is correctly numbered (consistent with the repository's .2 to .9 citations): a ScaledNs, the current grandmaster's time minus the previous one's, at the time the current grandmaster became grandmaster. "This plane sends the offset last measured as a slave" has the sign of `INTEGRATION.md:364` ("local time minus grandmaster time"), which is current minus previous at this plane's handover. "Not extrapolated to the handover" is the disclosure R778-1 S3 asked for. The RTL is unchanged | Resolved |
| R778-1 S4 / R777-1 S4 | `hdl/ucode/gen_gptp_ucode.py:2612` reads `CLOCK_ACCURACY_UNKNOWN_C` (`:553`, 0xFE) in the `--clock-accuracy` help | `grep` now finds a reader, the help output is byte-identical (`11-help-diff.log`), and the ROM is unchanged. No new source comment exists, so the comment rule has no new instance in this delta | Resolved |
| PR body's account of R1 | "So the same words, in the same order, are split into two sentences at "and"." | Inexact: "and" was replaced by "It also serves", and a comma was added | RESIDUE R2 |

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R1 | RESIDUE | Docs | `docs/HDL_DEVELOPER.md:328` | 802.1AS-2011 11.4.4.3.7 and 11.4.4.3.8. gmTimeBaseIndicator is a UInteger16 and only lastGmPhaseChange is a ScaledNs. In "serves gmTimeBaseIndicator, lastGmPhaseChange as ScaledNs" the comma can be read as a list under "as ScaledNs". R1 was raised against the earlier "all three fields as ScaledNs". Wording only: no figure, code, test or clause claim changes | A reader may still take gmTimeBaseIndicator for a ScaledNs | Exact fix: replace line 328 with "Region 6 serves gmTimeBaseIndicator and the ScaledNs lastGmPhaseChange." Keep line 330 as it is. That text passes the docs gate (`receipts/static/15-residue-fix-docs-gate.log`: "docs check: PASS", in a disposable copy, since restored) | `make docs` PASS; text present |
| R2 | RESIDUE | Docs (PR body) | PR #101 body, "Round 2", the paragraph after the "Wording only" table | Compare the head text with R777-1 R1's exact text in the author's own receipt | None. The account of the change is slightly inexact | Exact fix: replace "So the same words, in the same order, are split into two sentences at "and"." with "So it is split into two sentences at "and", which becomes "It also serves"." | PR body text present |

## Prior public findings at this head

| Prior item | Disposition at `84fd227` |
|---|---|
| R777-1 R1 = R778-1 P3 (RESIDUE, region 6 wording) | Resolved by `1400c83`. Shortened to pass the 10-word gate, which is justified. The remaining ambiguity is carried as R1 above |
| R777-1 S4 = R778-1 S4 (unused `CLOCK_ACCURACY_UNKNOWN_C`) | Resolved by `84fd227` |
| R778-1 S3 (lastGmPhaseChange per 11.4.4.3.8) | Resolved by `1d61f9e` (the documentation option) |
| R777-1 S1 = R778-1 S1 (TLV frequency grade tolerates truncation) | Retained, SUGGESTION. `sim_main.cpp` and the engine are unchanged by the delta, so the cause is unchanged. On the residue checklist |
| R778-1 S2 (no Sync between an Announce's last octet and its handler) | Retained, SUGGESTION, unchanged. Residue checklist |
| R777-1 S2 = R778-1 S6 (`CLK_HZ_P` bound for the TLV multiply) | Retained, SUGGESTION. `KL_gptp_engine.sv` is unchanged. Residue checklist |
| R777-1 S3 = R778-1 P1 (BTCA literal 3000 vs `ANN_RTO_MS_C`) | Retained, SUGGESTION, unchanged. Residue checklist |
| R777-1 S5 = R778-1 P2 (parent cannot select 0xFE; manager to confirm 0x22 covers every board) | Retained, SUGGESTION and a pending manager duty. Belongs to the parent re-pin PR |
| R777-1 R2 = R778-1 P4 (parent builder wording) | Retained, RESIDUE. Parent re-pin PR |
| R778-1 S5 (parent `OUR_CQ` peer constants) | Retained, SUGGESTION. Parent side |

## Lens results

- **Conformance: CLEAN.**
  - 11.4.4.3.8 is restated correctly, and its sign agrees with the documented offset sign.
  - The 2^41 scale is 11.4.4.3.9's.
  - The 8.6.2.3 b) 0xFE alternative is unchanged in behaviour, and its help now names the constant.
  - No behaviour change means no clause reading moved. The round 1 conformance verdict for the issue items carries.
- **RTL: CLEAN.**
  - After the merge, no `.sv` file changes.
  - The merge's `hdl/wire/KL_gptp_rx_parser.sv` is byte-identical to main's (PR #99), and the engine RTL is byte-identical to `3e3f041`.
  - The generator change is a help f-string, with identical output and an unchanged ROM.
  - The round 1 RTL verdict carries.
- **Robustness: CLEAN.**
  - The one new interaction is #99's parser under #100's engine. It is exercised by the engine suite (all four passes), the #100 controls and the author's full arm, all green.
  - The parent shadow, datapath and physical suites ran with the head as gitlink (author receipts).
- **Tests: CLEAN.**
  - Reviewer runs at the head: parser 482 checks plus its arm (35); engine 2,098 × 3 + 61; 25 of 25 arm jobs (the control and every #100 control).
  - The author's full engine arm (160/160) and the parent gates are hash-verified receipts.
  - No test file changes after the merge.
- **Docs: CLEAN.**
  - `make docs` PASS at the head (docs check, selftest, source evidence 20 exact, diagrams).
  - The three wording items are correct.
  - Two RESIDUE items, R1 and R2, remain. Neither leaves the lens unclean.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `docs/INTEGRATION.md:364, 852-871`; `docs/HDL_DEVELOPER.md:310-330`; `gen_gptp_ucode.py:552-553, 2609-2613`; 11.4.4.3.7 to 11.4.4.3.9 and 8.6.2.3 citations across `hdl/` and `tb/`; issue #100 acceptance | R778-2 (delta); R778-1 for the unchanged #100 behaviour | 84fd22781c95f7b7e65d7d18c99a5ed49a68e11c |
| RTL | CLEAN | merge replay `9ba112a` vs `1615187`; `git diff 1615187..84fd227 -- hdl`; byte identity of `hdl/top`, `hdl/ucpu`, `hdl/common` and `hdl/ucode` vs `3e3f041`, and of `hdl/wire` vs `5184fb3`; ROM regeneration; `--help` identity | R778-2; R778-1 carried for round 1 RTL | 84fd22781c95f7b7e65d7d18c99a5ed49a68e11c |
| Robustness | CLEAN | engine suite (four passes) with #99's parser; the 24 #100 controls; author full arm `jobs.md`; parent-A 01-03, 08, 11 and parent-B 01 logs | R778-2 | 84fd22781c95f7b7e65d7d18c99a5ed49a68e11c |
| Tests | CLEAN | `receipts/dynamic/{parser,engine-run,engine-arm-p100}.log`, `engine-arm-p100.jsonl`; author `repo-gates-84fd227/03-04`, `engine-arm-84fd227/jobs.md`, `arm_jobs.py`; engine `mutants.py:910-995` | R778-2 | 84fd22781c95f7b7e65d7d18c99a5ed49a68e11c |
| Docs | CLEAN (RESIDUE R1, R2) | `docs/SOURCE_EVIDENCE.md`, `docs/HDL_DEVELOPER.md`, `docs/INTEGRATION.md`, `docs/TEST_DEVELOPER.md`, `docs/MANAGER.md`, `docs/README.md` diffs; `make docs`; PR body "Round 2" | R778-2 | 84fd22781c95f7b7e65d7d18c99a5ed49a68e11c |

## Real limits

- I did not run the engine mutation arm in full, only the control and the 24 #100 controls. The other 135 mutants rest on the author's hash-verified `jobs.md`, which this delta's unchanged engine and mutants make sufficient.
- I did not run the parent consumer gates (`gptp_shadow`, `milan_dp gptp` / `gptp-lat`, or others). That is outside this review's allowance, so they rest on the author's receipts.
- The gitlink identity rests on the xvlog log line and the handoff. The scratch parent commit `2278661` and the companion change are not public.
- I did not re-run `ucpu`, `gaskets`, `tsngen`, `bench/arty`, `make lint`, `make ooc` or `make contract`, so these rest on the author receipts (rc 0). OOC figures were checked against the published Vivado reports, whose source commit is identified only by the receipt layout.
- The evidence commit is not signed. Hash agreement is with the manifest in that same commit, and the logs are redacted copies.
- No hosted check run or status context exists at the exact head (0 check runs, 0 statuses), so there is no hosted job to distinguish.
- Physical calibration is NOT RUN. The `tsn_fuzz` field campaign was skipped, and builder gate 11 is NOT RUN. Neither is a hardware or field proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR. Source base `3e3a4e7`, live dev `cc204c6`.
- Hosted/act acceptance at the merge candidate.
- Carry R1 and R2, and the retained suggestions (R777-1 S1 to S3, R778-1 S1, S2, S6, P1), to the residue checklist.
- In the parent re-pin PR: the companion change (`clock_accuracy 0x22`, builder pins); R777-1 R2 / R778-1 P4 wording; R778-1 S5. Confirm that the 0x22 decision covers every parent configuration (R777-1 S5 / R778-1 P2).
- Open physical calibration risks stay open.

## Receipts

Listed in `MANIFEST.sha256`:

- `scripts/static_probes.sh`, `scripts/launch_dynamic.sh`, `scripts/engine_arm_subset.py`, `scripts/verify_author_packet.py`
- `receipts/static/*.log`, `receipts/dynamic/*`, `receipts/author-packet-verify.log`, `receipts/integrity.log`
- In `receipts/dynamic/parser.log` and `engine-run.log`, the host home and toolchain paths are replaced by `<home>` and `<pinned-verilator-root>` placeholders. The manifest hashes the redacted copies.

After the probes, the review clone has HEAD, the index tree, every tracked blob and every mode equal to the exact head. The status is clean, and the repository has no submodule gitlinks (`receipts/integrity.log`). The probe clones were left with no tracked changes.

R778-2 FINISHED
