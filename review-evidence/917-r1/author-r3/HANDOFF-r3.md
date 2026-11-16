# HANDOFF round 3, [A784], lane 917 (#917, PR #918, part of #665)

Status: DONE at 394612c5; REVIEW READY posted once on #917 (issuecomment-6904532515); not pushed

- Branch: 917-aecp-hold, base origin/dev-soft-core cec88385ad. Round 2 head 8f73ade5 (pushed; REVIEW READY #917
  issuecomment-6902798240). Round 3 head **394612c5**, two commits on 8f73ade5 (93163957, 394612c5), not pushed:
  the manager pushes them to PR #918 and replaces the body with PR-BODY.md (whole PR, Round 3 section, roles
  R845-3 / R846-3).
- Reviews answered: R845-2 NEGATIVE (PR #918 issuecomment-6903179473, `review-evidence/917-r1/reviews/R845-2/REPORT.md`,
  archive 5cfa3de4) and R846-2 NEGATIVE (issuecomment-6903058735, `.../R846-2/REPORT.md`, archive 0d55a8db), one
  MINOR each.
- Resume after a host restart: nothing of round 3 had started when the session was cut (no round3 output, no
  round-3 comment, no unit of this lane running, the lane clean at the pushed 8f73ade5). Every gate below ran
  afterwards, on clean clones of 394612c5.
- Comment: REVIEW-READY text in comments/REVIEW-READY.md, posted once on #917 (issuecomment-6904532515).

## 1. Findings and their closure (lines at 394612c5)

| Finding | Closure (file:line) | Verification |
|---|---|---|
| R845-2 F1 MINOR (Conformance, Docs, Tests): FR_NFR's held allowance and margins an unchecked copy | Generated (the preferred remedy). `docs/reference/FR_NFR.md:432-439`: the table between `response-margins` markers, a new Channel column; each row states deadline, channel, timeout, bound, T_egress; the header the 10 ms proposal. `sw/mailbox/mailbox_margins.py` (new): `_row` `:54-68` writes token T_ingress, both token margins, held T_ingress (refill_ms + 1), both held margins; `findings` `:90-105` names a row whose written cells differ and a non-positive margin. `gen_mailbox.py:180` (`--check`), `:183-199` (`--write`), `:489-520` (self-test arms). FR_NFR `:425-430` describes the mechanism (the old `:425` sentence is gone). `scripts/ci_scope.py:65-66,75,295`: FR_NFR.md is a gate-read page (its self-test failed until it was: "gate-read page docs/reference/FR_NFR.md (named at sw/mailbox/mailbox_margins.py:26) is relevant"). `docs/testing/CI_WORKFLOWS.md:208-211`, `docs/design/MAILBOX_SPLIT.md:305-307`. | P1 rerun, `receipts/generator/P1-refill-probe.txt`: before `--write`, `--check` fails on the 3 AECP rows; after it they read 11 ms and 208/218/208 (218/228/218 at the proposal), ACMP unchanged, `--check`/`--crosscheck`/`docs_check` clean; a hand edit named. `--selftest`: positive control, 4 margin arms named, the regenerated rows moved; 0 arms failed |
| R846-2 F1 MINOR (Tests, Robustness): commit-order validation incomplete | `tb/verilator/ctrl_service_budget/held.py:42-47` `overtaken` (RXC on a channel holding a record refused), `:50-54` `follows_hold` (a release at or before its hold refused), `:57-61` `commit` (every RXC, `grade.py:196`), `:64-77` `release`. Controls `selftest_held.py:72-94` (the 2 invalid histories, a valid other-channel commit between, another channel's commit in the release's clock). Mutants `selftest_mutants.py:449-452` remove each guard. README `:387-389`, `:398`. | The review's `probe_attribution.py` at 394612c5 (`receipts/budget/probe_attribution.log`): both histories refused by name, valid cases measured. Self-test (clean clone): 0 failures, 216 caught; each guard's removal caught by its named check. Recorded held logs, the control and the 94-group population regrade byte-identically |
| R845-2 R1 / R846-2 R1 (residue): bench labels in `suite.hpp:1648-1650` | The exact fix; check names unchanged | No added comment line in `cec88385..394612c5` carries a bench label (grep) |
| R845-2 R2 (residue): the PR body's population reason | PR body Known limitations: the review's exact text | |
| R845-2 S1 (suggestion): aecp-held at 8x8/2if | Taken: run at `8x8` at 394612c5: 5.310 ms, ingress 4.986 of 6, within 20; 0 refusals, 0 misses, no STATED line. Points run: 1x1, 8x8/1if (round 2), 8x8 | `receipts/budget/held-8x8/` |
| R845-2 S2 (suggestion): author-r2 INDEX stale for 4 files | Not mine to fix in place: round 2's INDEX matches all 430 files as handed over (checked again now); the 4 workflow logs (`docs__docs-gates-1__gate_25_0.log`, `docs__docs-gates-2__gate_25_1.log`, `elaborate__elaborate-gates-{0,1}__gate_15_{0,1}.log`) are 8-12 bytes shorter only in the published copies, so a publication pass changed them after the INDEX. Round 3's INDEX is generated last; if publication rewrites anything, the INDEX should be regenerated after it. | |
| R845-2 S3 (suggestion): the held row already contains its ingress | Taken: `FR_NFR.md:444`, harness README `:396` | |

## 2. Gates at 394612c5 (clean clones; INDEX.md lists every file)

| Gate | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/mbx` | 622 / 667 / 32 / 629 / 674 / 547, 0 failures; 13/13 quick; mover 520,041, 24/24 | `mbx/make-and-mutants-394612c5.log` |
| `test_ctrl_firmware.py --require-rv32` (gates venv, pinned RV32 SDK) | PASS | `firmware/` |
| `make -C tb/verilator/mbx mutants` | 242/242 caught after 4 positive controls (the three round-2 arms caught by B7, B8, B9 by name) | same |
| Local: lint, gen_mailbox --check/--crosscheck/--selftest, ci_scope --selftest, docs_check, doc paths, em-dash, py/cpp/sv/sh idioms | all rc 0 (lint 89 <= 89; py long function 9 <= 9, long module 10 <= 10; cpp long function 0 <= 0) | `local/local-gates-394612c5.txt` |
| Workflows step by step: docs.yml (6 jobs), rtl-fast `changes`, rtl `full-ci-gate`, elaborate gate jobs | 77 steps rc 0, 49 not run with a stated reason (hosted orchestration, installs this host already has), 0 bad | `workflows/` |
| Budget self-test | 0 failures, 216 caught (214 at 8f73ade5 + 2 guards) | `budget/selftest/` |
| aecp-held at 8x8 (2 interfaces) | 5.310 ms, ingress 4.986 / 6, 0 refusals, 0 misses, rc 0 | `budget/held-8x8/` |
| Regrade by the round-3 grader: held 1x1, held 8x8-1if, the aecp control, population cec88385 and 84d8a214 | all byte-identical (1, 1, 1, 94, 94 groups); 0 refusals; 7 pre-existing misses | `budget/regrade/` |
| RTL / firmware / contract | `hdl` tree 363860ab728d at 8f73ade5 and 394612c5; `sw/firmware` 85c0f27c01e9 since 3926c271; package, skeleton, header, MAILBOX_CONTRACT.md, mailbox.yaml unchanged since 8f73ade5 | `rtl/trees.txt` |
| Firmware images against cec88385 | 46 fixture images identical; split 1x1/1if bb04b696 145,496 B, 8x8/1if 506a1ae4 158,176 B, ROM banks and xdc identical | `images/` |

## 3. Open risks / questions

- **gen_mailbox.py --check runs in no hosted job** (CI_WORKFLOWS.md says "No `docs-check` step runs it"); that was
  already so for MAILBOX_CONTRACT.md. FR_NFR's table is now generated and the local gate fails on divergence, but a
  hosted job running `gen_mailbox.py --check --crosscheck --selftest` would make it enforced on every PR. That is a
  CI template change (ci_gate_workflows.py regenerates the workflows); worth its own Issue. The manager may prefer
  to rule it into this PR.
- **8x8/1if STATED lines** (round 2, unchanged): three link-up build passes over `ctrl_loop.h`'s one-interface stated
  costs; the same in the no-hold `aecp` group; for #914's 8x8/1if measurement. At 8x8 (2 interfaces) the held run
  reports none.
- **Hardware acceptance owed**: three descriptor walks on the test machine; `Closes #917` would close the Issue at
  merge before them.
- **Directive choice** (round 1): AltSpreadLogic_high or ExtraTimingOpt meet the #870 hold floor; the RTL logic is
  unchanged since.
- **Pre-existing**: the budget harness cites MAILBOX_SPLIT.md by line number, stale at the base; worth an Issue.
- **Doc path gate count**: it reports 2 allowlisted paths on a fresh clone (`sw/litex/boards.local.sh` and
  `sw/builder/out/`, both gitignored build artifacts) and 1 where an image build has created `sw/builder/out/`;
  environmental, not this change.

## 4. Process notes

- Every command in the foreground with waits under 10 minutes; heavy work in transient units (MemoryMax 10G) on
  CPU ranges from cpu_ranges.py, one heavy job per clone (r3s self-test and local gates, r3m mailbox, r3h budget
  build, r3i/r3i1/r3i8 images, r3p1 the disposable P1 copy; the workflow runner makes its own).
- The firmware gate's first attempt ran the system Python under the scratch HOME (no PyYAML) and refused at its
  first generator call; a second was started without the venv by mistake and stopped by PID (its processes
  listed first); the third, with the gates venv, passed (`firmware/README.md`).
- One shell call was refused by the permission mode (an `rm -rf` of clone paths that did not exist yet); the clones
  were made without it.
- No push, no PR edit, no comment but the one REVIEW READY.
