# A175 correction handoff

The bounded F1/F2/F3 text correction is committed locally and ready for independent re-review.

| Identity | Value |
|---|---|
| Repository / issue / PR | kebag-logic/milan-fpga / #372 / draft #518 |
| Executor | A175, cleared-context Codex |
| Branch | `372-bound-axis-assertions` |
| Worktree | `$CANDIDATE` |
| Starting head | `60c5225fe5f93209bf313c51b7a722f25f9aaa7d` |
| Starting tree | `64182178131d03f157fe1a4ec767edee618bc6ff` |
| Corrected head | `059c3a60b8290873ed9fd14673f9981e8af754ce` |
| Corrected tree / index tree | `600468436fb9435a6b15c41db0156e5304848cb6` |
| Sole parent | `60c5225fe5f93209bf313c51b7a722f25f9aaa7d` |
| Commit subject | `docs: correct pinned assertion semantics and witness grading` |
| Final source status | Clean; local and unpublished by A175 |
| Review ownership | R240 internal Codex; R239 external Opus, availability pending |

Authority: [public assignment](https://github.com/kebag-logic/milan-fpga/issues/372#issuecomment-5780262565), [settled contract](https://github.com/kebag-logic/milan-fpga/issues/372#issuecomment-5776353888), REQUIREMENTS REQ-VER-01/02/04, AGENTS, CONTRIBUTING, docs/README, R239-1, R240-1, [round completion](https://github.com/kebag-logic/milan-fpga/pull/518#issuecomment-5779875726) and replica cleanup. The assignment supersedes older role labels in prior comments. [A175 TAKEN](https://github.com/kebag-logic/milan-fpga/issues/372#issuecomment-5780285051) preceded every source edit.

## Corrected findings

All three retain R239's **MINOR Docs** classification. These are executor corrections offered for re-review, not reviewer closure.

| Finding | Correction | Files |
|---|---|---|
| F1 | An attempt completing on a reset edge is skipped; a start on a reset edge can produce a vacuous pass at the next running edge, flag 0. First-edge history starts at 0 in the measured pinned 5.050 two-state setup, even for a signal declared initially 1. The witness must sample reset together with the antecedent inside `$past`; current reset or antecedent-only history miscounts the reset-started attempt. | `docs/testing/ASSERTIONS.md` |
| F2 | All summaries agree with actual grading: 15 equality, 2 floor, 4 presence checks. The guide names the two floor properties and explains that immediate-law counts only need both values above zero. | Guide, `docs/testing/TESTING.md`, `tb/verilator/README.md`, header only in `tb/verilator/ptp_ts/mux_sva_main.cpp` |
| F3 | Removed unsupported construct-compatibility and automatic formal-flow claims. Retained only that simulation ran and no formal tool read these properties. No untested future conversion is presented as measured behavior. | Guide |

No conflict with the assigned correction was found. No requirement, acceptance criterion, checker, bind, stimulus, scoreboard, property, campaign, witness, count, Makefile, workflow, budget, RTL, firmware or processor pin changed. No optional #495 suggestion was adopted.

## Measurement attribution

No simulation, campaign, new behavior test or formal tool ran in this correction. The user expressly allowed precise attribution to unchanged public measurements.

The guide now links [immutable R239-1 evidence](https://github.com/kebag-logic/milan-fpga/tree/7795e487048867fde07a224ec1a5885acfb4375b/review-evidence/372-r1/review/R239-1), at evidence commit `7795e487048867fde07a224ec1a5885acfb4375b`, measured on source `60c5225f...` with pinned Verilator 5.050. `public-measurement-audit.json` records hashes and verifies all 18 downloaded evidence files against that commit's Git blobs.

- F1 reset: `raw/probe-reset-R1.log:104-123`, authored by R239. Edge 9 has reset low and stalled s0/m valid; its disabled protocol pass actions do not run. Edge 10 has reset released; s0 and m TVALID pass actions run with flag 0. `scripts/probes/probe_reset.cpp` is the unchanged probe source. R2/R3 logs are also retained.
- F1 initial history: `scripts/probes/pastprobe.sv` declares constant `one = 1'b1`. `raw/pastprobe-run.log` reports both past-equals-one and stable checks failing at time 5, then no further such failures. The original `raw/pastprobe-summary.txt` records build 0 and run 0; these diagnostics are probe observations, not a failed suite or an A175 execution.
- F2 grading: `raw/focused-witness-and-tallies.txt` contains 15 equal, 2 at-least and 4 both-above-zero rows at each width. R239's w8/w64 tallies are 170/171 with zero failures. Examples: w8 owner-held 787 versus 379 (floor); w8 grants-mutually-exclusive 1514 versus 677 (presence); w64 valid-forwarded 1689 versus 754 (presence). The unchanged `witness_expectations()` and `grade_witnesses()` match those relations.
- F3: no formal measurement is available or claimed.
- The replaced upstream `raw/verilator-v5.050-Changes.txt` is a reference receipt, not the changelog. It names the fixed v5.050 URL and original digest `71f0d60715572b45f69b65e791412305f086c487306f3d88357de6c7df1c7bce` for 288248 original bytes. That digest is not the receipt-file digest.

A175 ran only the supplied selector's `--version`, exit 0: `Verilator 5.050 2026-07-01 rev v5.050`. Selector SHA256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f` matches R239's public tool receipt. Host 5.052 was not invoked. No installed tool was changed.

The cited [Arm IHI0051A section 2.2](https://documentation-service.arm.com/static/642583d7314e245d086bc8c9), [pinned language support](https://github.com/verilator/verilator/blob/v5.050/docs/guide/languages.rst) and [pinned options](https://github.com/verilator/verilator/blob/v5.050/docs/guide/exe_verilator.rst) were read as public authority; no normative interpretation changed.

## Local validation

`validation-ledger.json` selects the completed receipts. Every command runs in the assigned worktree through `rtk`; raw combined output and exact argv/cwd/environment/head/tree/exit hashes are under `commands/`. Precommit receipts keep their actual starting head/tree. Their changed-file hashes equal the later committed content, and scope checks prove other source files unchanged. They are not relabelled as later executions.

The following checked commands exited 0:

```sh
rtk proxy python3 scripts/docs_check.py
rtk proxy python3 scripts/check_doc_style.py
rtk proxy python3 scripts/check_doc_paths.py
rtk proxy python3 scripts/gen_toc.py --check
rtk proxy python3 scripts/gen_toc.py --verify-anchors
rtk proxy python3 scripts/check_cpp_idiom.py
rtk proxy python3 scripts/check_sv_idiom.py
rtk proxy python3 scripts/check_py_idiom.py
rtk proxy python3 scripts/check_sh_idiom.py
rtk proxy python3 scripts/check_hygiene.py --check
rtk proxy python3 scripts/check_em_dash.py --base 60c5225fe5f93209bf313c51b7a722f25f9aaa7d
rtk proxy git diff --check 60c5225fe5f93209bf313c51b7a722f25f9aaa7d HEAD
```

Em-dash: zero findings over 29 added lines in three Markdown pages, controls 57/57. Docs: zero findings, scrub controls 23/23, routing 4/4. TOC: 106 lists; anchors: 144 reproduced cross-page links. The other checks remain within unchanged budgets.

Collector exception: initial parallel collectors called `git write-tree` and collided on `index.lock`. The TOC-anchor wrapper failed before starting its gate; the hygiene wrapper failed while recording post-command identity. Both wrappers exited 1; their identity subcommands exited 128. Hygiene's original raw log is retained, but its missing exit receipt is not reconstructed or used. The collector now reads the index without that write operation; separate `toc-anchors-corrected` and `hygiene-corrected` executions exit 0. See `collector-exceptions.json` and preserved `record-initial.py`. No source change resulted.

## Preservation and reproducible evidence

`source-scope-and-token-comparison.json` and `commands/scope-final.log` prove:

- Exactly the four authorized source paths differ from the starting head.
- All 39,374 bytes from the harness's first `#include` to EOF are byte-identical. That token remains on line 36. Both prefixes consist only of comments/blanks, with no line splicing and the same newline count; all executable tokens and their line numbers are preserved.
- Executable-suffix SHA256 before and after: `88da057b116caa9ca6fb3602e38ca94f205dc8e3234a7a0e9b820e7b8bce6339`.
- The other 853 ordinary parent files, all modes and all four gitlinks are unchanged.
- No hidden index flags; required submodule revisions/status unchanged.

`final-integrity.json` additionally records all 857 committed parent blobs/kinds/modes, matching index tree, clean status, and exact diff hash. `source.diff` contains the reviewable correction. `initial-integrity.json` records the corresponding starting checks. `record.py`, `verify_scope.py` and `verify_measurements.py` are factual evidence helpers outside the source checkout, not added repository tests.

## Remaining ownership and limits

R240 internal Codex and R239 external Opus own corrected-source review, including Docs and the Tests/Robustness coverage required by the harness artifact change. Opus availability is pending and cannot be waived by the author. No prior positive is carried over by A175, no lens is banked, and F1/F2/F3 await reviewer disposition.

Manager owns full validation, public source/evidence publication, trusted act, protected hosted contexts, any later candidate integration, merge authorization and completion. This correction did not run a parent/PP/gPTP/Yosys/builder bank, Docker/act, candidate runner/selftest, hardware or privilege operation, installation, another checkout, push, PR metadata change, merge or delegation.

Issue acceptance criteria remain unchanged. Existing AC1/AC2 simulation evidence retains its original source identity. AC3's guide has the assigned corrections and bounded validation above; independent re-review and manager gates remain pending. The source commit is local and ready for manager handoff, not approved for merge.


Published [A175 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/372#issuecomment-5780455022). Only the issue comment was published; the source remains local. The exact connector request/result is in `publication.json`.
