[R301] POSITIVE - exact head 4538d7c03dc4f56d7ed4c971603e15bda82050a8

Round R301-4. I am the external reviewer, with a cleared context. This is the Docs-round delta review of PR #563 / issue #545.

- Head: `4538d7c03dc4f56d7ed4c971603e15bda82050a8`, tree `79587dc14eb458d5b98ca1c79aafbc155608f218`. It is the PR's published head (`receipts/hosted_pr_state.txt`).
- Parent: `b376f6113b388929fe82e883d400e5361319b966`, which R301-3 covered in full.
- Delta judged: `b376f611..4538d7c0`. It is one commit with a one-line message and no trailers.
- Scope: assignment 5833028966, items 1 and 2. They are R301-3 F1 and R301-3 S1 (= R300-3 S2), limited to docs and the evidence-reader text.

**Summary.** Both assigned items are fixed.

- The suite README's present-tense statement of what `make gmstep-mutants` runs now matches the executable inventory.
- The `slew_mutants.py` disposition now names eight classes for eight defects.
- Two files changed. Their modes are unchanged, and so are all four gitlinks. The evidence reader's syntax tree is identical apart from the one disposition string.
- Every requested gate passes: docs, TOC, anchor and evidence.
- I found no finding at MINOR or above. One SUGGESTION is recorded: two dated historical records still say "eleven".

## Findings

### S1 SUGGESTION - Docs - `tb/verilator/milan_dp/README.md:621`, `:865` - two dated records still say `make gmstep-mutants` runs "all eleven"

- **Evidence:**
  - `:621` reads "Measured on 2026-09-24 ... `make gmstep-mutants` (the leg and all eleven controls) 405 s".
  - `:865` is the `obj_gmstep` row of the check-count table, where the 48 / 0 is dated 2026-09-24. Its note says "`make gmstep-mutants` all eleven (two on the option-off leg)".
  - The three #545 controls came in at `fc8a719f` on 2026-09-25, so both statements were true on their record date.
  - `scripts/derive_counts.py` flags them mechanically (`receipts/derive_counts_head.log`).
  - R301-3 explicitly ruled these same lines (then `:615` and `:859`) to be dated historical records, outside F1, and allowed them to stay. Having re-read them at this head, I agree. The page's controlling present-tense statement at `:593-594` is now correct and names the defining list.
- **Impact:** a reader skimming `:621` or `:865` without their dates could take eleven to be the current inventory, and 405 s to be the current campaign time. Nothing executable is affected.
- **Optional outcome:** qualify each record with "(before the three #545 controls)", or re-measure the timing at fourteen.
- **Verification:** re-run `scripts/derive_counts.py`, or read the two lines.

No BLOCKER, MAJOR or MINOR finding.

## Delta verification

| Check | Result | Receipt |
|---|---|---|
| Tree delta `b376f611` → `4538d7c0` | Only `scripts/measure_test_evidence.py` and `tb/verilator/milan_dp/README.md` changed, both still 100644. The four gitlinks are identical (external `efeb541a`, gptp-processor `5dce647a`, protocol-processor `990f9652`, verilog-axis `48ff7a7e`). No `hdl/`, test harness, Makefile or campaign file was touched | `receipts/tree_delta.txt`, `receipts/delta.diff` |
| Evidence-reader change is text only | The AST of `measure_test_evidence.py` at both commits is identical once the `slew_mutants.py` disposition string is masked. The dictionary's keys drive the check (`:818-819`); the value is only printed (`:880`) | `receipts/ast_equivalence.txt` |
| gmstep counts, derived from `gmstep_mutants.py` `CONTROLS` (`:125-199`) | 14 controls: 3 acceptance (the default sweep), 2 option-off, 3 `--slew` ("the policy level ..."), 12 on the gmstep leg. The README table has 11 rows, and they equal the 11 non-`--slew` names exactly. Of those, 3 are marked "the sweep" and 2 "option-off leg". README `:591` "three", `:593` "all fourteen" and `:596` "the eleven tabulated above, plus three #545 controls" all agree. The `:594` link resolves to the defining `CONTROLS` list. TESTING.md:268 gives "twelve gmstep controls and two option-off controls" = 14 | `receipts/derive_counts_head.log` |
| Selection semantics, imported | Default = 3, `--all` = 14, `--slew` = 3. Legs: gmstep 12, option-off 2. The Makefile's `gmstep-mutants` target runs `--all` (Makefile:360-361) | `receipts/gmstep_selection_import.log` |
| Provenance of the three additions | All three were introduced by lane commit `fc8a719f`, which is not an ancestor of dev `864b36f5` (`git merge-base --is-ancestor` false). That supports the README's "three #545 controls" and "cover the policy level and applied-rate tail" (tied-low level, omitted tail, extra addend stage) | recorded in this report |
| Servo disposition vs `slew_mutants.py` | 8 defects (5 `MUTANTS` + 3 `STREAK_MUTANTS`), mapped to 8 named classes in order. `discard_removed` → discard removal, `level_tied_low` → tied-low level, `partial_tail_trusted` → partial-tail trust, `discard_not_counted` → omitted tally, `step_dedupe_removed` → boundary step double counting, `slew_streak_reset_removed` → retained guard streak, `slew_discard_extends_streak` → streak increment on slew discard, `slew_discard_counts_as_guard_trip` → slew discard counted as a guard trip. TESTING.md:269 says "eight defects" | `receipts/derive_counts_head.log` |
| Discrimination of the count script | At the parent `b376f611` it reports the F1 sentence (`:592`), the six-for-eight disposition, and the two dated records. At the head only the two dated records remain (S1) | `receipts/derive_counts_b376f611.log` |
| `measure_test_evidence.py --check` / `--selftest` | rc 0 / rc 0. Ratchet PASS: 0 unexplained DUT readers, 101/101. The existing note that the ratchet "can be lowered to 75" is informational and not caused by this text-only delta | `receipts/measure_test_evidence.py_--check.log`, `receipts/measure_test_evidence.py_--selftest.log` |
| `docs_check.py` with Git / `--selftest` / no Git (archive of HEAD) | 0 findings (scrub 23/23, routing 4/4) / PASS / 0 findings (only inventory parity skipped, as expected without Git) | `receipts/docs_check.py.log`, `receipts/docs_check.py_--selftest.log`, `receipts/docs_check_nogit.log` |
| `gen_toc.py --verify-anchors` / check (pinned renderer, private venv) | 174 cross-page anchors reproduced / TOC OK | `receipts/gen_toc_verify_anchors.log`, `receipts/gen_toc_check.log`, `receipts/renderer_env.txt` |
| `check_em_dash.py --base 864b36f5`, `check_doc_style`, `check_doc_paths`, `check_py_idiom`, `git diff --check` (vs parent and vs dev base) | all rc 0 | `receipts/check_em_dash_base.log`, `receipts/check_doc_style.log`, `receipts/check_doc_paths.log`, `receipts/check_py_idiom.log`, `receipts/diff_check.log`, `receipts/gates_rc.txt` |
| Hosted, exact head (read-only snapshot) | 15 success, 1 skipped (`Physical gPTP (nightly and manual)`: a skipped context, not hardware proof), 4 still in progress at snapshot time (`docs-check`, Verilator shards 1, 2 and 4) | `receipts/hosted_checkruns_4538d7c0.tsv` |
| Clone restored | HEAD, tree and index tree exact; worktree equals HEAD; `status --ignored` empty (my `scripts/__pycache__` byproduct removed); submodules at their gitlinks and clean; tracked mode/blob/path digests equal between index and HEAD | `receipts/final_state.log` |

No Verilator build or mutation campaign was run this round. The delta changes no executable input to either campaign. R301-3 ran both campaigns at `b376f611`: `gmstep-mutants` 16/16 and `slew-mutants` 10/10.

The commands are in `scripts/commands.sh`, and the count derivation is `scripts/derive_counts.py`. It reads source only and runs none of the repository's code.

## Prior public findings on PR #563, resolved or retained at this head

I read these only after my own pass over the delta.

| ID | Severity | Status at `4538d7c0` | Evidence |
|---|---|---|---|
| R301-3 F1 (README says "all eleven") | MINOR | Resolved | README `:593-596` states fourteen and derives it (eleven tabulated plus three #545), linking `CONTROLS`. Dated records at `:621` and `:865` stay, as R301-3 allowed. See S1 |
| R301-3 S1 = R300-3 S2 (six classes for eight defects) | SUGGESTION | Resolved | `measure_test_evidence.py:597-601` names eight classes, mapped one-to-one above |
| R300-3 S1 (U15 blind to a level-gated streak reset on sub-window slews) | SUGGESTION | Retained, open | `sim_main.cpp` and the servo RTL are unchanged by this delta |
| R301-2 S-A (tail oracle one-sided) | SUGGESTION | Retained, open | `sim_gmstep.cpp` is unchanged. Routed to #495 by the manager |
| R300-1 F1-F3, R301-1 F1-F3, R301-1 S1, R300-1 S1, R300-2 F4-F5, R301-2 S-B/S-C | as published | Resolved (per R301-3 at `b376f611`) | The delta touches none of their artifacts |

## Lens results

```text
[R301] PASS Conformance - assignment 5833028966 items 1-2 vs receipts/delta.diff and receipts/derive_counts_head.log - both items met exactly; "docs and evidence-reader text only" honoured (receipts/tree_delta.txt, receipts/ast_equivalence.txt); issue #545 acceptance unaffected, since no behaviour, gitlink or ROM input changed from b376f611, where R301-3 covered it
[R301] PASS RTL - receipts/tree_delta.txt at 4538d7c0 - no hdl/, constraint, gitlink or build-recipe path changed; the RTL is byte-identical to b376f611, which R301-3 covered (KL_mmcm_drp_servo.sv, milan_datapath.sv slew hunks)
[R301] PASS Robustness - receipts/tree_delta.txt and receipts/ast_equivalence.txt at 4538d7c0 - no harness, stimulus or error-path code changed; the only code-file edit is a printed string; R301-3's servo robustness cases (U15, S1-S5 at b376f611) run on identical inputs
[R301] PASS Tests - scripts/measure_test_evidence.py:597-601 and tb/verilator/milan_dp/gmstep_mutants.py:125-199 at 4538d7c0 - the disposition's key set is unchanged; --check and --selftest rc 0 (101/101); campaign inventories and selection (3/14/3) confirmed by import; no test weakened; the campaigns' inputs are unchanged since R301-3's 16/16 and 10/10
[R301] PASS Docs - tb/verilator/milan_dp/README.md:589-600, docs/testing/TESTING.md:268-269, scripts/measure_test_evidence.py:597-601 at 4538d7c0 - the counts match the source inventories (receipts/derive_counts_head.log); docs_check with Git, with no Git and --selftest, gen_toc check and --verify-anchors, em-dash, style, paths and diff-check are all rc 0; only SUGGESTION S1 remains
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5833028966; `receipts/delta.diff`, `tree_delta.txt`, `ast_equivalence.txt`, `derive_counts_head.log` | R301-4 | `4538d7c03dc4f56d7ed4c971603e15bda82050a8` |
| RTL | CLEAN | `receipts/tree_delta.txt` (no RTL, gitlink or recipe delta from `b376f611`, which R301-3 covered) | R301-4 | `4538d7c03dc4f56d7ed4c971603e15bda82050a8` |
| Robustness | CLEAN | `receipts/tree_delta.txt`, `ast_equivalence.txt` (no harness or stimulus delta) | R301-4 | `4538d7c03dc4f56d7ed4c971603e15bda82050a8` |
| Tests | CLEAN | `scripts/measure_test_evidence.py:597-601` (`--check` / `--selftest`), `gmstep_mutants.py` `CONTROLS` and selection, `slew_mutants.py` tables | R301-4 | `4538d7c03dc4f56d7ed4c971603e15bda82050a8` |
| Docs | CLEAN (S1 SUGGESTION only) | `tb/verilator/milan_dp/README.md:589-600,621,865`, `docs/testing/TESTING.md:268-269`; docs, TOC, anchor, em-dash, style and path gates | R301-4 | `4538d7c03dc4f56d7ed4c971603e15bda82050a8` |

## Limits

- This is a delta review of `b376f611..4538d7c0`. The full content at `b376f611` rests on R301-3, which applied every lens there. R300-3 is POSITIVE at the ancestor `92ad1687`.
- I did not run any Verilator build, mutation campaign, Yosys run, builder run or full bank this round, and I did not run the act replay. The delta changes no input to any of them.
- The hosted snapshot was taken while 4 contexts were still in progress. The skipped physical gPTP context is not hardware proof.
- Physical calibration was NOT RUN. Neither field skips nor simulation are hardware evidence.
- The count script's sentence matcher is heuristic. It covers the phrasings present in this README, and was checked against the parent, where it finds the known F1 sentence.

## Pending manager duties

- Accept the exact-head hosted contexts once the 4 in-progress ones complete, and the act replay, distinguishing executed jobs from skipped contexts.
- Build and validate the final current-dev candidate at the merge turn: source base `864b36f5e9450ef64f75ca3f0d68c44330e447d7`, live dev `fd9e0ebf2bbaa38330e99d1c489f01a820f1c363`.
- Confirm the full CONTRIBUTING review bar (two independent positives, one external) and obtain explicit maintainer authorization before any merge. Then run post-merge containment and close issue #545.
- Optional: route S1.

R301-4 FINISHED
