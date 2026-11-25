[R913] POSITIVE - exact head 67838b379f9e9ecb6cf6fbd0f162a5bb852ca570

# R913-5: internal delta review of kebag-logic/milan-fpga PR #992 (issue #991), the held-egress ledger restated

- Head: `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570`, tree `8c4d79be339a4c9b702335aef8b98d7278878505`. This is the live PR head (`headRefOid`, read 2026-11-25T00:0xZ).
- Scope: a narrow re-review of the delta since R913-4 at `507bce7f`.
  - Round 4 was evidence only, with no commit: the harness ran on the merge head's images, and the PR body was rewritten.
  - Round 5 is one commit, `507bce7f..67838b37`. It touches three paths: `tb/verilator/ctrl_service_budget/egress_ledger.py`, its `README.md`, and `docs/design/SPLIT_CONTROL_MEMORY.md`.
- Authority for the restatement: the manager's ruling https://github.com/kebag-logic/milan-fpga/pull/992#issuecomment-7146658362 (2026-11-24, item 1).

## Verdict summary

- **POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. All five lenses were applied and are clean.
- **R913-4 F1 is resolved** by option (a), with one carve-out.
  - Arm A ran at both points on images whose sha256 equals the merge head's mapped images (`79c5326c…` at 1x1/1if, `eed56acc…` at 8x8/1if). The `answering-every-port` and `answering-later` arms also ran, all rc 0.
  - The carve-out: one 8x8/1if pass exceeds THE SHARE. It is `srp-bound`'s 210,174 cycles, which the harness itself grades OWED to #977. #969's amended ruling of 2026-11-23, item 2, provides for that grading.
- **R913-4 F2 is resolved.** The PR body now describes the sync merge, the gates run at `507bce7f` and `67838b37`, the image deltas and the merge-head route. The carried pre-merge measurements are labelled as such.
- **The ruling's figures are reproduced exactly.**
  - `TRAIN` and `PINNED` equal round 4's 10 ns receipts, every row to the last digit.
  - Each figure is hold + largest + 5 %, rounded up to 0.01 ms. A separate Decimal computation gives 64.31, 64.51, 64.71, 64.91, 65.11 and 63.29, all set by `507bce7f`, and 63.23, set by `2509db68`. These are the ruling's figures and the tool's `LEDGER`.
- **The self-test passes:** rc 0, 72 controls, 18 of 18 mutants caught. Six extra mutation probes were all refused, and the unplanted control passed.
- **Two suggestions and one retained residue.** None of them affects the verdict.

## How the task was reconstructed (public state only)

- AGENTS.md and CONTRIBUTING.md (the lens and ledger rules).
- Issue #991 and its AC2 (harness, ledger leg).
- The ruling on #992.
- Issue #1005 (the train's growth as recorded debt, AC1 to AC3).
- #969's amended ruling https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252 (item 2).
- FR_NFR 3.4.1 as cited by the tool's README.
- `git show 67838b37` and `git diff --name-only 507bce7f 67838b37`.
- The published packets `review-evidence/lwsrppin-r1/author-r4` and `author-r5` at `0a95297c`.
- The live PR body. It equals `author-r5/PR-BODY.md` except for the leading role line.
- The prior public findings, read only after the independent pass over the diff: R913-4, and through it R913-1 to R913-3.

## Evidence produced by this round

| Check | Result | Receipt |
|---|---|---|
| `egress_ledger.py --selftest` at the head | rc 0. 72 PASS lines (36 in process, 36 as a process). `RESULT: PASS: 18 mutants, 0 failure(s)`. Each of the 3 new mutants is caught by "section 13's measurement is the one the ledger derives from" | `receipts/selftest-67838b37.log` |
| Independent derivation | `PINNED` equals round 4's merge receipt `author-r4/receipts/harness/egress-ledger-8x8-1if.log` and `TRAIN` equals round 4's train receipt `train-2509db68/egress-ledger-base-8x8-1if.log`, both to 10 ns. The Decimal rule, the ruling and the tool agree on all 7 rows. The set-by image matches the ruling: PINNED for six rows, TRAIN for `service.aecp.last`. `RESULT PASS` | `scripts/derive_check.py`, `receipts/derive_check.txt` |
| The leg on the published round-4 logs, using the head's tool | merge image `run-8x8-1if.log` (full 101-group run): rc 0, PASS, every row within by 0.15950 to 0.38150 ms at the log's held-up value. Train image `train-2509db68/run-8x8-1if.log`: rc 0, PASS. The same images fail against the old ledger (round 4's `egress-ledger-*.log`, rc 1), so the restatement is what makes the leg pass | `receipts/ledger-from-r4-log-merge.log`, `receipts/ledger-from-r4-log-train.log` |
| Mutation probes, each on a fresh `git archive` copy | All 6 refused (rc 1): a PINNED cell off by 10 ns in section 13, a ledger cell 63.24, the TRAIN and PINNED columns swapped on one row, a TRAIN constant one cycle low, `MEASURED` dropping `TRAIN` from its max, and a table row deleted. The unplanted control passes (rc 0) | `scripts/probe_mutations.sh`, `receipts/probe_mutations.txt` |
| Python idiom gate at the head | rc 0 | `receipts/py-idiom-67838b37.log` |
| Build-input analysis | No changed path is read by any image build. Every non-Markdown file that names `SPLIT_CONTROL_MEMORY.md` does so in a comment or a link string. `scripts/ci_scope.py` lists it only as a CI-scope trigger. No harness `build.json` names a changed path (`author-r5/receipts/identity/identity.txt`). The author's 28-file sha lists at `507bce7f` and `67838b37` are byte-identical (`cmp`) | this report |
| Delta scans | 0 em-dashes in added lines. Added source comments (`egress_ledger.py:78-80`, `:87-90`, `:270-272`, `:277`) contain no bench lane label, lane name, review round, reviewer ID or issue-comment ID. The `issuecomment` links are in the Markdown pages only, as section 13 and the README already use them | this report |
| Restore | HEAD, tree, worktree and index equal the exact head. The porcelain listing is empty, including ignored files, after removing this round's own `__pycache__`. Gitlinks are unchanged, `third_party/lwSRP` `d1bb4f4e` among them | `receipts/restore-check.txt` |
| Hosted contexts, snapshot 2026-11-25T00:07Z | 17 pending, 0 completed. The manager owns acceptance | `receipts/hosted-checks-summary.txt`, `receipts/hosted-checks-snapshot.tsv` |

### Figure-by-figure check against the ruling

| Row (8x8/1if) | TRAIN `2509db68` | PINNED `507bce7f` | Largest | Figure (rule = tool = ruling) | Set by |
|---|---:|---:|---:|---:|---|
| `backlog.owed.if0` | 64.01426 | 64.09994 | 64.09994 | 64.31 | PINNED |
| `backlog.owed_behind0.if0` | 64.20677 | 64.29245 | 64.29245 | 64.51 | PINNED |
| `backlog.owed_behind1.if0` | 64.39672 | 64.48319 | 64.48319 | 64.71 | PINNED |
| `backlog.owed_behind2.if0` | 64.58746 | 64.67393 | 64.67393 | 64.91 | PINNED |
| `backlog.owed_behind3.if0` | 64.77829 | 64.86397 | 64.86397 | 65.11 | PINNED |
| `backlog-owed.service.acmp.last.if0` | 63.03567 | 63.12992 | 63.12992 | 63.29 | PINNED |
| `backlog-owed.service.aecp.last.if0` | 63.07053 | 62.84763 | 63.07053 | 63.23 | TRAIN |

The three earlier measurements (MERGED, COMPOSED, LISTENED) are below these on every row, so the earlier columns set no figure.

### Section 13's stated shares, recomputed from the round-4 receipts

- **Train against `402834ac`:** +0.75169 (`owed_behind3`) to +1.50327 (`aecp.last`). The doc says "0.75 to 1.50" (correct).
- **Train over the old figures:** 5 of 7 rows, by 0.03672 to 0.91053 ms. The doc says "0.037 to 0.911" (correct). `402834ac` was within every old figure (correct).
- **Merge against the train:** +0.08568 on `owed`, `owed_behind0` and `owed_behind3`, +0.08647 on `owed_behind1` and `owed_behind2`, +0.09425 on `acmp.last`, and -0.22290 on `aecp.last` (all as stated).
- **The PR body:** "took `owed_behind2` and `owed_behind3` over the old figures, by 0.064 and 0.004 ms" (correct: 0.06393 and 0.00397).
- **Image difference:** the train's image differs from the merge's only in `mrp_mad.o` (`author-r4/.../train-2509db68/identity-base.txt`: `DIFFERS 31-mrp_mad.o`). Each measured image is its point's ledger image (`harness = ledger: SAME` for both).

## Findings

### S1 - SUGGESTION - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:3044` (the first restatement bullet's last sentence); issue #1005 AC3

- **Evidence:**
  - Section 13 still says "a later restatement needs a ruling, only for growth reproduced at a ruled upstream head (item 3)".
  - #1005 AC3 (opened 2026-11-24T22:48:01Z, two seconds after the ruling) says: "From now on, restating these rows needs this per-PR cost/phase attribution; a ruled upstream head alone is no longer enough."
- **This PR's ordering is consistent.** The ruling on #992 decides this restatement by name. #1005 AC3 is prospective. The new bullet (`:3047-3050`) says the train's attribution is #1005's. This answers the author's open question in `author-r5/REVIEW-READY.md`: no conflict.
- **Impact:** a reader of section 13 alone sees the older condition for the next restatement. Delivering AC3 is #1005's job, not this PR's.
- **Optional outcome:** when #1005 lands, or now, add one clause to the new bullet: "a later restatement of these rows also needs the per-PR cost or phase attribution (#1005, AC3)".

### S2 - SUGGESTION - Tests - `tb/verilator/ctrl_service_budget/egress_ledger.py:453-461` (the three new mutants)

- **Evidence:**
  - Each new mutant, like the earlier composed and Listener ones (`:449-452`), patches `MEASURED` only. `LEDGER` is derived from `MEASURED` at import (`:104`), so the planted "figure at an earlier image's measurement" never changes a figure.
  - The mutant is caught by the measurement-equality control, not by a figure difference (`receipts/selftest-67838b37.log:86-88`).
  - This round's source-level probe `tool-max-drops-train` re-derives `LEDGER` and is refused by the figure control too (`receipts/probe_mutations.txt`). The defect class is therefore caught both ways.
- **Impact:** none on the verdict. The mutant names overstate what each plant does.
- **Optional outcome:** re-derive `LEDGER` inside these mutants, for example `patch.dict(m.LEDGER['8x8-1if'], {r: m.figure(v) ...})` alongside the `MEASURED` patch, so that each one also proves the figure control. Or name them "a measurement at ...".

### R1 - RESIDUE - Docs - `sw/firmware/ctrl/test/test_ctrl_firmware.py:81-82` (R913-4 R1, retained)

- The delta does not touch this file. The words are unchanged: "a Listener withdrawn 5 to 200 ms after the board's own LeaveAll sent as Lv within 240 ms".
- **Exact fix:** "... after the board's own LeaveAll is sent as Lv within 240 ms ...", re-wrapped to the entry's column.

### Notes (no action on the PR)

- **N1.** The packet's text is stale about the push. `author-r5/REVIEW-READY.md:2` and `author-r5/receipts/INDEX.md:3` say "local, not pushed", but `67838b37` is now the published PR head. This is the same publication-time staleness as R913-4 N1.
- **N2.** The train-image base run exits rc 1 (`author-r4/.../train-2509db68/times.txt`).
  - Cause: it graded `backlog-owed` and `srp-bound` without `srp-kept`. The harness then reports `srp-bound`'s pass over THE SHARE as a `SHARE` line rather than OWED, and states that the pair is graded together.
  - `backlog-owed` itself graded with 0 refusals (`2 groups graded, 0 refusals`), and the `TRAIN` measurement is that group's grade. The rc does not taint it.
  - The base run is a measurement run, not a gate, which matches the ruling's use of it.
- **N3.** "the flip train" in the new source comment (`egress_ledger.py:78`) names PR #988's integration train, which the commit history and PR titles use. It is not a bench lane label or a lane name, so it is not residue under the comment rule.

## Prior public findings at this head

| Finding | Status at `67838b37` | Evidence |
|---|---|---|
| R913-4 F1 (MINOR; Conformance, RTL, Tests): harness not run on the merge images | **RESOLVED** by option (a) | `author-r4/receipts/harness/identity.txt` and `grade-*.txt`. Arm A `harness = ledger: SAME` at both points. Every arm and every point rc 0 at head `507bce7f` (`times.txt`). 0 over THE SHARE in 1x1/1if (arm A, `every`, `later`) and in 8x8/1if `every` and `later`. 8x8/1if arm A: 1 of 325,929, the `srp-bound` pass of 210,174, graded `OWED ... owed to #977` by the harness (`run-8x8-1if.log:499`). That is the grading #969's amended ruling (item 2) prescribes, and it predates F1. F1's "0 passes may exceed THE SHARE" is read with that standing carve-out. `kept_grade` PASS. The variant images differ from arm A only in the size fixture `ctrl_aecp_image.o` (`variant-objects.txt`). Images at `67838b37` equal `507bce7f`'s, so the results carry to this head |
| R913-4 F2 (MINOR, Docs): stale PR body | **RESOLVED** | The live body has a sync-merge section (parents, base, 18 and 145 paths, the two conflicting paths and three resolved hunks), evidence rows naming `507bce7f` and `67838b37`, the image deltas against `2509db68` (+60 B `.text`, ROM +56/+64, SRAM and tiles unchanged) and `30796098`, and the merge-head route table (LUT 45,958 against 45,982, WNS +0.038, WHS +0.036). "stand from `402834ac`" and "the route stands for this head" are gone. The remaining pre-merge figures are explicitly labelled as measured on the pin before the merge (the red leg at body `:94-96`, `make srptx` at `:185-188`). The THE SHARE section names #969's amended ruling with its link and item 2 (`:98-107`), and 216,785 - 210,174 = 6,611 as stated |
| R913-4 R1 (RESIDUE) | RETAINED as R1 above | file unchanged |
| R913-4 S1, S2 (SUGGESTION, Tests) | open, optional | files unchanged |
| R913-2-S1, R913-2-S2, R913-3 N-S1 (SUGGESTION) | open, optional | files unchanged |
| R913-4 N2, N3 | no action | publication tooling and this reviewer's own check |
| The round-4 stop (egress ledger leg FAIL at `507bce7f`) | **RESOLVED** by the ruling and round 5 | The leg passes at the head on the merge image's results (author) and logs (this round), and on the train image |

## Lens results

```text
[R913] PASS Conformance - egress_ledger.py:81-92,104; SPLIT_CONTROL_MEMORY.md:3047-3060; the ruling (item 1); receipts/derive_check.txt - TRAIN and PINNED are the round-4 10 ns receipts. MEASURED is the max of five. Each figure is hold + largest + 5 %, rounded up to 0.01 ms, and equals the ruling's seven figures with the ruled set-by image. Section 13 has both columns, each head's share stated apart, the ruling and #1005 linked. No owner bound or row budget moved (FR_NFR 3.4.1 rows stay recorded misses). #991 AC2's harness part: R913-4 F1 resolved (author-r4 grade-*.txt)
[R913] PASS RTL - git diff --name-only 507bce7f 67838b37 (3 paths, no hdl/, firmware, config or build input); author-r5/receipts/identity/sha-507bce7f.txt == sha-67838b37.txt (cmp, 28 files); author-r4 identity.txt arm A harness = ledger SAME - the delta changes no RTL or image, so R913-4's RTL lens, unclean only through F1, is now clean on the round-4 harness results for these exact images
[R913] PASS Robustness - egress_ledger.py:273-297 (DOC_ROW, doc_rows, doc_ledger, doc_measurements); receipts/probe_mutations.txt; receipts/selftest-67838b37.log - the parser fails closed on a missing row, swapped columns or a wrong cell. The fail-closed controls (new miss, unmeasured row, refused run, log without summary, BUDGET short of the summary) all still pass in both process modes. The leg on round-4 logs passes at the log's held-up value
[R913] PASS Tests - egress_ledger.py:367-369,453-461; receipts/selftest-67838b37.log (72 controls, 18/18 mutants); receipts/probe_mutations.txt (6/6 refused, control rc 0) - each new mutant can fail and is caught. The five-column control replaces the three-column one. Independent probes at source level and doc level are refused. Optional S2 on mutant plant depth
[R913] PASS Docs - SPLIT_CONTROL_MEMORY.md:3047-3060; ctrl_service_budget/README.md:203,207; live PR body (compared to author-r5/PR-BODY.md); author-r5/receipts/docs/run.log (46 steps rc 0) and receipts/py-idiom-67838b37.log - the shares recompute exactly from the round-4 receipts. The README names five measurements with their rulings and the true mutant count (18, counted in the self-test). The PR body resolves F2 and names #969's amended ruling for THE SHARE. 0 em-dashes in added lines. No comment-rule residue in the delta. Optional S1; R1 residue retained
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `egress_ledger.py` constants and `figure`; section 13 bullet and table; the ruling; #1005; #969 amended ruling; `derive_check.txt`; author-r4 grades | R913-5 | `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570` |
| RTL | CLEAN | the delta's path list; the author's 28-file sha lists at `507bce7f` and `67838b37`; build-input analysis; author-r4 harness identity and grades | R913-5 | `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570` |
| Robustness | CLEAN | `egress_ledger.py` parser and fail-closed controls; probes; the leg on round-4 logs | R913-5 | `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570` |
| Tests | CLEAN | self-test (72 controls, 18 mutants); 6 independent probes | R913-5 | `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570` |
| Docs | CLEAN | `SPLIT_CONTROL_MEMORY.md` section 13; tool README; live PR body; author docs-gate receipts; Python idiom gate | R913-5 | `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570` |

- **Code outside the delta keeps its prior lens verdicts** (R913-3 POSITIVE at `30796098`, R913-4 at `507bce7f` apart from F1/F2), because the delta changes nothing those verdicts depend on: no image or input changed.
- **Open findings:** none of severity MINOR or above. Optional: S1 and S2. R1 is RESIDUE for the manager's checklist.

## Real limits

- This round re-ran no harness, image build or route.
  - The harness, `kept_grade`, the route and the 28-file identity rebuild are the author's published receipts.
  - They were checked here by reading them, by `cmp` of the sha lists, by build-input analysis, and by re-grading round 4's published run logs with the head's tool.
- The round-4 results directories (the 10 ns `backlog-owed.json`) are not published.
  - `TRAIN` and `PINNED` were matched to the published 10 ns `egress-ledger` receipts that the author derived from those directories.
  - The headline figures were also matched to the published 1 us logs.
  - The json sha256 values in `author-r5/receipts/ledger/measurements.txt` could not be re-hashed here.
- At the snapshot, all 17 hosted contexts at the exact head were pending and none had completed. No hosted result is claimed.
- No manager source bank runs at this head, and none is claimed or inferred. The current-dev merge candidate is not built here: source base `aa30d77f`, live dev `e275d795`, dev-soft-core now `2f2a8152`.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- Act, the host CI runner and its self-test were not run, by instruction.

## Pending manager duties

- Hosted-context acceptance at `67838b37`. All were pending at 00:07Z.
- The current-dev merge-candidate validation (builder and native banks) at the merge turn. This includes the ruling's item 3: the candidate gate runs `backlog-owed` plus `egress_ledger.py --point 8x8-1if` and `--selftest`, with REUSED only on proven image identity.
- Carry R1 to the residue checklist.
- Track #1005 (attribution before the dev-soft-core -> dev PR, 2026-11-27) and #977, which owes the `srp-bound` pass over THE SHARE before the post-flip in-house qualification closes.
- External review per CONTRIBUTING's two-positive bar. This internal round is one delta reviewer, which is the ruling's last condition.

R913-5 FINISHED
