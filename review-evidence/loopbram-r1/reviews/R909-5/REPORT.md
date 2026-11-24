[R909] POSITIVE - exact head 1516b2ffe321337858389ec8e42897f8a80644bb

# R909-5: internal independent narrow re-review of PR #987 (issue #979)

- **Head.** `1516b2ffe321337858389ec8e42897f8a80644bb`, tree `2f5f891e7599abeebfc5fda13e0324fe353f5eff`. This is the PR's live `headRefOid` (`receipts/pr_head.json`). It is one docs commit on the previously reviewed head `c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99`.
- **Source base.** `3cda030c17`. The live dev tip the manager will build the merge candidate on is `e275d7950ef3385753e6a15d2e191ba855b171ed`. Nothing in this round builds that candidate.
- **Scope.** This round re-reviews only R909-4-N1 (MINOR, Docs) and R909-4-R1 (RESIDUE, Docs) against the one-commit delta. Code the delta does not touch keeps its R909-4 lens verdicts, because the delta changes nothing those verdicts depend on.
- **Verdict reason.** R909-4-N1 is resolved and R909-4-R1 carries its exact fix. The delta has no open BLOCKER, MAJOR or MINOR. I found one new RESIDUE (preamble wording) and two SUGGESTIONs.

## Delta (`git diff --stat c413d33a..1516b2ff`)

```
 docs/testing/CI_WORKFLOWS.md | 2 ++
 docs/testing/TESTING.md      | 2 +-
 2 files changed, 3 insertions(+), 1 deletion(-)
```

Nothing else changed. My own diff is byte-identical to the packet's `author-r6b/receipts/diff.txt`: `cmp` was silent, and the blob is `d5763fd1...`.

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R909-4-N1 MINOR, Docs. The CI policy's budget table contradicted the 300 s arms | **RESOLVED** | See (1) |
| R909-4-R1 RESIDUE, Docs. `TESTING.md:442` said "selftest's new-suite steps" | **RESOLVED**, exact fix applied | See (2) |
| R909-4-S1, S2, S3 SUGGESTIONs | Unchanged and optional. The delta does not touch them | The delta has no receipt, builder or manifest bytes |
| R909-3-N1 and all earlier findings (R909-1-F1..F7, R909-2-N1..N3, R910-1-F1, R910-2-F1/F2, earlier RESIDUE/SUGGESTION) | Prior resolutions stand | None of their artifacts has a byte in this delta |

### (1) R909-4-N1: suite-budget table (RESOLVED)

I checked each part of the required outcome:

- **The 300 s rows exist.** `docs/testing/CI_WORKFLOWS.md:584` reads `input_loopback`, `input_loopback_dp` | 300 s each. The two loopback arms are at `scripts/run_all_suites.sh:259-260`.
- **The rows state their basis.** That basis is:
  - provisional at their own arm;
  - under the new-suite steps in the selector's docstring, which exist at `scripts/suite_shards.py:15-20`;
  - from cold local runs;
  - hosted windows owed, which will replace the figures.
- **The recommended `reboot_ctrl` row was added.** `CI_WORKFLOWS.md:585` reads `reboot_ctrl` | 300 s | provisional. That matches `run_all_suites.sh:265`, and `reboot_ctrl` is in `PROVISIONAL_SUITES` (`scripts/suite_shards.py:151`).
- **The 'every other default suite' row is true.** My probe `scripts/table_vs_arms.py` parses the `suite_timeout` case at `run_all_suites.sh:256-266` and the table at `CI_WORKFLOWS.md:580-590`. At this head (`receipts/table_vs_arms_head.log`, rc 0, RESULT PASS):
  - all 8 named arms appear in the table with equal seconds;
  - all 9 table rows equal the arm the driver gives them (`mmcm_servo` gets the `*` arm, 1800 s);
  - the 'every other default suite' row is 1800 s, which equals the `*` arm;
  - 59 of the 68 discovered `tb/verilator/*/Makefile` suites have no row, and every one of them gets 1800 s;
  - the rows marked provisional are exactly `PROVISIONAL_SUITES`.
- **The probe can fail.** Run against the `c413d33a` export, it reports `FAIL (5)` (`receipts/table_vs_arms_prev_c413d33a.log`): three missing arms, the unlisted suites that are not at 1800 s, and a mismatch in the provisional set.

### (2) R909-4-R1: TESTING.md:442 (RESOLVED)

- `docs/testing/TESTING.md:442` now reads exactly as R1's fix: "Both are provisional under the new-suite steps in the selector's docstring: each figure in `scripts/suite_shards.py` is 300 s." A string comparison returned YES.
- The old phrase "selftest's new-suite steps" now appears 0 times under `docs/` and `scripts/` (`receipts/testing_442_check.log`).

## Docs gates at this head (my own runs in this clone)

| Gate | Result | Receipt |
|---|---|---|
| `scripts/docs_check.py` | rc 0, 0 findings across 226 md and 1933 scrubbed files | `receipts/docs_check.log` |
| `scripts/check_em_dash.py --base c413d33a` (pinned renderer, installed from `tools/markdown/requirements.txt` with hashes into a scratch-only venv) | rc 0, 0 findings over 3 added lines | `receipts/em_dash_venv_c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99.log` |
| `scripts/check_em_dash.py --base 3cda030c17` | rc 0, 0 findings over 642 added lines | `receipts/em_dash_venv_3cda030c17.log` |
| `check_doc_style.py` and its `--selftest` | rc 0, OK (25 documents) | `receipts/doc_style.log`, `receipts/doc_style_self.log` |
| `check_doc_paths.py` | rc 0, 1762 cited paths resolve | `receipts/doc_paths.log` |
| `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `check_gptp_docs.py`, `check_submodule_docs.py` | each rc 0 | `receipts/{doc_map,solution_docs,gptp_docs,submodule_docs}.log` |
| `check_feature_status.py`, `check_hygiene.py --check` | rc 0 | `receipts/{feature_status,hygiene}.log` |
| `suite_shards.py --selftest` (checks the provisional figures against the driver) | rc 0, selftest PASS | `receipts/suite_shards_self.log` |

The plain-interpreter em-dash runs exited 2 because the renderer was absent (`receipts/em_dash_c413.log`, `receipts/em_dash_base.log`). That was an environment gap, and the venv reruns above replace those results. A manual scan for U+2014 and U+2013 in the added lines was also clean (`receipts/em_dash_manual.log`).

## Signed packet and receipts

- The packet is `review-evidence/loopbram-r1/author-r6b` at `8b6ab716f3fb7f2cb118b6c796ecd2ad1f66b7ca`. That commit is **unsigned** (GitHub verification `unsigned`), so its integrity rests on content hashes.
- All 3 files match their tree blob ids and their `MANIFEST.json` `published_sha256` and `original_sha256` values (`receipts/author-r6b-tree.tsv`):
  - `REVIEW-READY.md` `1669fd0c...`
  - `receipts/diff.txt` `20a6acc6...`
  - `receipts/docs-gates.txt` `929737b8...`
- Its `docs-gates.txt` lines are identical to my own `docs_check` and `doc_style` tails. Its claims (two rows plus a `reboot_ctrl` row, the R1 wording, no code/test/image change, no U+2014) all reproduce.

## Hosted CI at the exact head (snapshot 2026-11-24T19:26:13Z)

`receipts/hosted_check_runs_exact_head_final.tsv` and `receipts/hosted_run_list_exact_head.json` show four pull_request runs at `1516b2ff`:

| Run | Workflow | State |
|---|---|---|
| 45469087930 | docs | **executed:** only `docs-check-no-git` (success, 21 s); `docs-gates-0` in progress; `docs-gates-1`, `docs-gates-2` and `wire-accountability` queued |
| 45469088206 | rtl-fast | pending |
| 45469087943 | rtl-full | pending |
| 45469088250 | elaborate | pending: `elaborate-gates-2` in progress, the rest queued |

No hosted context has concluded except `docs-check-no-git`. I claim no hosted `rtl-fast`, `verilator-suites` or `yosys-portability` evidence at this head. Hosted acceptance belongs to the manager.

## Findings

### R909-5-R1 - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:576-578`

- **Text.** "The measured hosted worst case plus a stated margin sets each named entry:"
- **Problem.** Three named entries are now explicitly provisional: `CI_WORKFLOWS.md:584-585` sets them from the driver's arm, not from a hosted window. R909-4-N1 already noted this sentence in its evidence, but its required outcome did not include it.
- **Wording only.** The rows state their own basis correctly. No figure, check or claim changes.
- **Exact fix.** "The measured hosted worst case plus a stated margin sets each named entry, except a provisional one, which keeps its own arm until its hosted window is measured:"
- **Verification.** Read `CI_WORKFLOWS.md:576-578`. Docs gates stay green.

### R909-5-S1 - SUGGESTION - Docs - `docs/testing/CI_WORKFLOWS.md:584`

- "provisional at their own arm ..., from cold local runs" could be read as saying that the 300 s figure was derived from the cold runs.
- `TESTING.md:445-447` is clearer: the arm is the figure, and the cold runs show the arm keeps at least three times the slowest run.
- **Optional wording.** "...; cold local runs took at most 34.2 s and 98.0 s, so each keeps at least three times its slowest run; their hosted windows are owed and replace these figures".

### R909-5-S2 - SUGGESTION - Docs - `scripts/suite_shards.py:150`

- The comment cites "step 3 of the module docstring's new-suite steps", but the docstring at `:15-20` is an unnumbered paragraph.
- This wording predates the PR: it is identical at base `3cda030c17`. It is not in this delta and is not RESIDUE here. Leave it for a later tidy.

**Comment-rule scan of the delta.** The delta's three added lines are prose in documentation pages. They contain no source comment and no lane label, review round, reviewer ID or comment ID. There is no new RESIDUE under the comment rule.

## Lens results (this round)

```text
[R909] PASS Conformance - docs/testing/CI_WORKFLOWS.md:580-590 vs scripts/run_all_suites.sh:256-266 and scripts/suite_shards.py:151 - every stated budget equals the driver's arm; provisional set equal; the delta has no protocol, RTL or acceptance-criterion bytes, so #979's frozen criteria keep their R909-4 result
[R909] PASS RTL - git diff --stat c413d33a..1516b2ff (2 Markdown files only) - no HDL, CDC, FSM or interface artifact in the delta; R909-4's RTL verdict depends on nothing changed
[R909] PASS Robustness - git diff c413d33a..1516b2ff - no executable or configuration path changed; the only runtime-affecting figures (suite_timeout arms) are unchanged and now documented, cross-checked by scripts/table_vs_arms.py
[R909] PASS Tests - receipts/suite_shards_self.log, receipts/table_vs_arms_head.log, receipts/table_vs_arms_prev_c413d33a.log - no test changed; the provisional selftest stays green; my probe passes at head and fails at the prior head (it can fail)
[R909] PASS Docs - docs/testing/CI_WORKFLOWS.md:576-590, docs/testing/TESTING.md:440-447, author-r6b packet - N1 and R1 resolved; docs gates green (receipts/); R909-5-R1 is RESIDUE only, and S1 and S2 are optional
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CI_WORKFLOWS.md:580-590`, `run_all_suites.sh:256-266`, `suite_shards.py:15-20,148-151`. Delta stat. The R909-4 result stands for code the delta does not touch | R909-5 (delta), R909-4 (rest) | 1516b2ffe321337858389ec8e42897f8a80644bb; untouched scope is unchanged since c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |
| RTL | CLEAN | Delta stat: no HDL bytes. R909-4 RTL verdict | R909-5 (delta), R909-4 (rest) | 1516b2ffe321337858389ec8e42897f8a80644bb; RTL scope is unchanged since c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |
| Robustness | CLEAN | Delta: no executable or config change. Arm cross-check probe | R909-5 (delta), R909-4 (rest) | 1516b2ffe321337858389ec8e42897f8a80644bb; untouched scope is unchanged since c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |
| Tests | CLEAN | `suite_shards.py --selftest`. `table_vs_arms.py` at head and at the prior head | R909-5 (delta), R909-4 (rest) | 1516b2ffe321337858389ec8e42897f8a80644bb; test scope is unchanged since c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |
| Docs | CLEAN (R909-5-R1 RESIDUE carried; S1, S2 optional) | `CI_WORKFLOWS.md:576-590`, `TESTING.md:440-447,646`. Docs gates (receipts/). The author-r6b packet and its manifest | R909-5 | 1516b2ffe321337858389ec8e42897f8a80644bb |

## Limits

- This is a narrow delta review. The lenses outside the delta rest on R909-4 (`c413d33a`), and the delta has no byte in their scope.
- I ran no manager source bank and claim none. I ran no full parent, PP, gPTP, Yosys or builder bank, and no Verilator build: the delta has no source the scoped Verilator would compile.
- Hosted CI was still running at the snapshot. Only `docs-check-no-git` had concluded (success).
- The packet commit `8b6ab716` is unsigned. I verified it by content hash and by independent reproduction.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The em-dash gate ran with the pinned renderer in a disposable scratch venv, not in the hosted image.
- I verified the clone afterwards (`receipts/tree_integrity.log`):
  - HEAD, tree and index tree all equal `2f5f891e...`, and the status is clean;
  - all six submodule gitlinks are unchanged (`efeb541a`, `1616fc8f`, `801ef228`, `08ee86e8`, `715589c1`, `48ff7a7e`).

## Pending manager duties

- Hosted acceptance at `1516b2ff`: `docs-gates-0..2`, `wire-accountability`, `rtl-fast`, `rtl-full` (`verilator-suites`, `yosys-portability`) and `elaborate`. All were in flight at the snapshot.
- Current-dev merge candidate on `e275d795` with the builder and native banks, with the receipts linked on the PR.
- The hosted windows owed for `input_loopback`, `input_loopback_dp` (and `reboot_ctrl`) replace their provisional 300 s figures in `scripts/suite_shards.py` and `CI_WORKFLOWS.md:584-585` after the first hosted run that carries them.
- Carry R909-5-R1 to the residue checklist (R909-4-R1 is now applied).
- The external review and the full completion bar. Merge only with explicit maintainer authorization.

R909-5 FINISHED
