# [A685d] #665 lane S2c, round 2 continuation: the owner's NFR-SCOUT-01 amendment (HANDOFF)

Status: **REVIEW READY**, 2026-10-27.

- Branch `665-s2c-icache`, local, not pushed. Start head `de91db59d10d4e9e3de607f068ace7680f293fd7` ([A685c] REVIEW READY, issuecomment-6434846736). Head **`e0bb857a9f4b8e9d29736970a1135afde03260c5`**, one commit on top.
  - Commit: one-line subject, no body, no trailers (`receipts/scope/commits_and_scope.txt`).
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified). Lane base `origin/dev-soft-core` `e76a755a` is an ancestor of the head (verified). `origin/dev-soft-core` is `9220f9b3`; the PR targets `dev-soft-core`.
  - S2's remote branch `665-s2-cpu-budget` is still `f58d049b` (`git ls-remote`, in the scope receipt): no re-base.
- No git command ran inside a submodule. No submodule pointer changed.
- Task: the owner's amendment, issuecomment-6434741232, with its correction issuecomment-6434744436 (the corrected wording governs).
- TAKEN: issuecomment-6435024913 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6435396245 (`REVIEW-READY-COMMENT.md`). PR body for the manager: `PR-BODY.md`.
- Nothing pushed. No PR, issue or comment edit. No bench, hardware, flashing, Vivado or sweep: a docs-only change.

## Contents

1. Result
2. Changes, file:line and reason
3. Checks, planted mutants and failing words
4. Gate table
5. Findings, decisions and open questions

## 1. Result

The four edits the owner listed are applied in one commit, `e0bb857a`, and nothing else changed (`receipts/scope/commits_and_scope.txt`: 4 files, +8 -6; `docs/history/` untouched; no submodule pointer).

## 2. Changes, file:line and reason

Line numbers at `e0bb857a`.

| File:line | What | Reason |
|---|---|---|
| `docs/reference/FR_NFR.md:321` | NFR-SCOUT-01's first sentence is now "The release architecture MUST use one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless." The row's other sentences, priority and verification are unchanged. | The owner's correction (issuecomment-6434744436), whose wording governs over issuecomment-6434741232's first text |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md:62` | "One cacheless RV32I control hart remains the release target." becomes "The release architecture uses one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless." | The amendment: "wherever it repeats 'cacheless': the same wording". `:62` is the page's only occurrence. The hart's description is verbatim; the verb is "uses", because the page carries no uppercase requirement keyword (0 occurrences of `MUST`) and states architecture, not requirements |
| `docs/design/MARK_II_AREA_PLAN.md:383` | "the control hart (NFR-SCOUT-01: one cacheless RV32I)" becomes "the control hart (NFR-SCOUT-01: one RV32I hart, 4 KiB instruction cache, no data cache)" | The amendment's text for this line, as listed ("The other edits are as listed") |
| `docs/design/SPLIT_CONTROL_MEMORY.md:243-247` | The three-line open-conflict paragraph becomes five lines: the owner amended NFR-SCOUT-01 on 2026-10-27 (links to the decision and its correction), following the 2026-10-26 decision; the old text; the new text; the architecture repeats it; a geometry change or a data cache needs the owner again | The amendment: "becomes a record of the amendment and this decision, no longer an open conflict"; the last sentence restates the decision's own condition |
| (PR body) `PR-BODY.md` | First line `[A685d]`; Status states the amendment; Linked Issue, Description (new amendment table), the pieces table, Authoritative references, How to validate (`test_ctrl_memory.py` added), Known limitations (the conflict bullet replaced) and the DoD line | "Update the PR body to state the amendment instead of an open conflict" |

Not edited, by the assignment: `docs/history/`. Not edited, outside the listed edits (section 5): `docs/reference/FR_NFR.md:6`; the area plan's D5 lines `:610`, `:1302`, `:1357`.

## 3. Checks, planted mutants and failing words

No new check: the change is four Markdown pages. No check or mutant changed.

## 4. Gate table

Every gate ran at the head `e0bb857a9f4b8e9d29736970a1135afde03260c5` (`receipts/gates/HEAD.txt`).

- The runner is `scripts/gates_s2c.py`, round 1's and [A685c]'s runner. This round's copy adds two things: `GATE_SKIP` (gates skipped by name, which the summary names), and the gate `ctrl_memory`, `python3 sw/litex/test_ctrl_memory.py` in the product LiteX environment. That test reads `docs/design/SPLIT_CONTROL_MEMORY.md` (`scripts/ci_scope.py:73` lists the page among the documents a gate reads).
- It ran the gates one at a time, each to its own log, unpiped. It refused a dirty tree before starting and checked `git status --porcelain --untracked-files=all --ignore-submodules=none` after every gate. Logs are in `receipts/gates/`, each with its rc and the tree's state on its last lines; `summary.md` is the runner's table with seconds, and `serial.out` its console.
- Two logs exceed 200 KB and are kept out of the packet by digest: `bdd_conformance.log` and `ci_events_selftest.log` (`<log>.digest.txt`).
- Environments as in round 2: the pinned Markdown renderer's environment (`tools/markdown/requirements.txt`, sha256 prefix `40cdefe08ebd`), `tools/hdl_reference/requirements.txt`, and the product LiteX environment with the pinned RV32 SDK for `soc_options` and `ctrl_memory`.
- Skipped by name: `builder_require_rv32` (about 23 minutes). It passed at `de91db59` ([A685c]'s gate table: `ALL GATES PASS EXCEPT 1 NOT RUN`). This commit changes four Markdown pages, none of which the builder bank reads: `git grep` finds no reference to them from `sw/builder/test_builder.py`, and the four pages are not inputs to an export.

**0 of 97 gates nonzero or left the tree dirty** (`summary.md`).

| Gate | Command | Result |
|---|---|---|
| `baremetal_check`, `baremetal_selftest` | `python3 scripts/check_baremetal_only.py --check`, `--selftest` | rc 0: `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))`; `baremetal-only selftest: PASS (867 arm(s))` |
| The docs workflow's check-mode commands: 87 gates, `wire_accountability_selftest` to `ci_events_selftest` in `summary.md` | as listed in `scripts/gates_s2c.py` | rc 0 each. `check_em_dash: 0 finding(s) over 1009 added line(s) in 5 changed Markdown page(s) ... [e76a755a..HEAD]`; `docs_check: 0 finding(s) across 211 md files + 1433 scrubbed text files`; `TOC gate: OK`; `anchor check: 552 existing cross-page fragment links reproduced`; `doc path gate: OK (1062 cited paths all resolve, 1 allowlisted; 10 line anchor(s) within their file)`; `documentation style: OK (23 current documents)`; `HYGIENE RATCHET: PASS` |
| `git_diff_check` | `git diff --check e76a755a HEAD` | rc 0 |
| `bdd_conformance` (rtl-fast) | `cd tests && behave` | rc 0: 14 features, 406 scenarios, 1977 steps passed |
| `ctrl_memory` (new in the runner) | `python3 sw/litex/test_ctrl_memory.py` | rc 0: `test_ctrl_memory: 0 failure(s)`, `RESULT: PASS` |
| `harness_selftest` | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0: 93 `PASS`, 70 `MUTANT caught`, `self-test: 0 failures` |
| `soc_options` | `python3 sw/builder/test_soc_options.py` | rc 0: `Split placement CPU: the 4 KiB direct-mapped instruction cache on the split CPU only, 6 killed controls`; `RESULT: PASS` |
| `firmware_compiler_absent` | `python3 sw/builder/test_firmware_compiler.py --absent --audit <scratch>/rv32-absent.jsonl` | rc 0 |
| `hdl_reference_selftest`, `hdl_reference` | `python3 scripts/gen_hdl_reference.py --selftest`, `--output <scratch>` | rc 0 |

Receipts: `receipts/INDEX.md`, generated by `scripts/make_index.py` from the files present (100 files, 8 with host paths replaced by role placeholders, their raw sha256 given; none over 200 KB). `receipts/scope/commits_and_scope.txt` holds the remote, the ancestry check, `git ls-remote`, the commit, its empty body, the full diff, and every remaining "cacheless" in the four pages.

## 5. Findings, decisions and open questions

1. **`docs/reference/FR_NFR.md:6` still says "The release uses one cacheless RV32I control hart".** It is the page's introduction, a paraphrase of NFR-SCOUT-01. The amendment lists only line 321 on that page ("The rest of the row is unchanged"), and the brief says to apply the amendment exactly, so it is not edited. Published in the PR body's Known limitations and the DoD line, and in REVIEW READY, for the owner or a reviewer to decide.
2. **`MARK_II_AREA_PLAN.md:383` carries the owner's text on a row measured on the all-fabric hart.** The row is in the plan's "Historical source inventory at `e6172750`" (`:321`), a routed image before the split, whose hart is cacheless and stays so under the amended text. The edit is the owner's listed text; the observation is published beside item 1.
3. **The area plan's D5 lines** (`:610`, `:1302`, `:1357`) say "cacheless" about the 2026-08 D5 decision and the cores as priced. They are records, not repetitions of NFR-SCOUT-01, and the amendment does not list them.
4. **The architecture's verb.** "uses", not "MUST use" (section 2).
