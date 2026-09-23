[R253] POSITIVE - exact head e0c43b03f31d6c1220dd05a110e4bb30029233a0

Round R253-1, external independent review of protocol-processor issue #102 / PR #103.
Head `e0c43b03f31d6c1220dd05a110e4bb30029233a0`, tree `0547903adc17449dfb4f0c2610a23e6adb4ff6a2`,
base `f70ba36ecb634467e4b1c3f0dbf1239d1e12af57` (equal to donor `main` at review time).

## Verdict and ledger (written before any prior review report was read)

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. One SUGGESTION (S1), outside the frozen #102 scope, does not affect the verdict.

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #102 acceptance 1-4 and scope decision; parent `scripts/check_cpp_idiom.py:cflags_missing` (blob `1d9ccd7f`, identical at parent `483a133e` and live dev `574c29fa`); parent CONTRIBUTING §§2-3, CODE_QUALITY Rule 11 "Seven ratchets"; `tb/pp_top/Makefile:54-63`; receipts `probe_cflags.log`, `parent_inputs.txt` | R253-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 |
| RTL | CLEAN | `git diff --name-status` (one Makefile, no `hdl/` path); RTL `+define+PP_TOP_SRP_DOM_DEF_VID=16'h$(SRP_VID_FIXTURE)` at `tb/pp_top/Makefile:58` unchanged; `pp_top_wrap.sv:332-334` binding unchanged; `lint_hdl.sh` 37 LINT OK; hosted portability (Yosys/sv2v) executed and passed | R253-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 |
| Robustness | CLEAN | effective compiler invocation for the fixture build at base and head (generated `VM_USER_CFLAGS`, full g++ flag list, `-Q --help=warnings` table: byte-identical, 183 enabled); quoting/tokenisation of the edited group; `SRP_VID_FIXTURE` override path; parent PP testbench-Makefile population (30 at base and head); other parent gates that read Makefiles | R253-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 |
| Tests | CLEAN | full `tb/pp_top` `make run` at head with Verilator 5.050 (exit 0, 1411 PASS / 0 FAIL: default 1391, fixture 20); fixture guards 4 cases + locale unittest; real-checker controls (9 expectations per parent revision); DV mismatch mutation (13 of 20 fixture checks fail incl. DV5 LINK_DOWN and DV6 LINK_UP); hosted push and PR `suites` jobs (pp_top 1411/0, 14943 total, 0 failing) | R253-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 |
| Docs | CLEAN | `tb/pp_top/Makefile:1-15` header comments, `tb/pp_top/README.md` section DV (build table around line 505-511), `docs/README.md`, `docs/guides/hdl-engineer.md`, `docs/architecture/09_verification.md`; tracked-text search for the changed recipe; links/matrix/modmatrix/UPC-map gates on the head tree; PR description | R253-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 |

Per-lens results, in the parent AGENTS §6 clean-lens format:

```text
[R253] PASS Conformance — tb/pp_top/Makefile:21,59; receipts/probe_cflags.log — both -CFLAGS groups carry -Wall -Wextra; SRP_VID_FIXTURE 5A3C unchanged; real parent cflags_missing: base [-Wall,-Wextra], head [], each single-flag removal reported; PP build-without-warnings 1 -> 0 against budget 0; one-line scope as frozen in #102
[R253] PASS RTL — receipts/diff_hygiene.txt; tb/pp_top/Makefile:58; tb/pp_top/pp_top_wrap.sv:332-334 — no hdl/ or wrapper byte changed; RTL define and binding unchanged; lint_hdl 37 OK; hosted portability executed and passed
[R253] PASS Robustness — receipts/probe_effective_flags.log; receipts/effective_flags/ — g++ enabled-warning table identical at base and head under the full generated flag set; group tokenises correctly; no -Werror; no other parent gate parses these groups
[R253] PASS Tests — receipts/pp_top_head_run.log; receipts/mutation_vid_mismatch_full.log; receipts/hosted_runs.txt — full pp_top 1411/0 with guards and locale test; the edited group still drives DV (13/20 FAIL on mismatch, DV5/DV6 included); hosted suites 14943/0
[R253] PASS Docs — tb/pp_top/Makefile:1-15; tb/pp_top/README.md:505-511; receipts/docs_gates_head.log — no tracked doc quotes the changed recipe; build/override/expectation descriptions remain true; links, matrix, modmatrix, UPC map pass
```

## Findings

No MINOR, MAJOR or BLOCKER finding.

```text
[R253] SUGGESTION Tests, Robustness — scripts/ ; Makefile:13 (check) ; .github/workflows/hdl.yml — no donor-side gate for the per-group warning-flag rule
Requirement/evidence: parent check_cpp_idiom.py:484-503 enforces "every -CFLAGS group carries -Wall and -Wextra" only on the parent's pinned PP population. A tracked-text search of the donor's scripts/ and .github/ for Wextra/CFLAGS finds no equivalent. This defect came in with donor PR #96 and was found only at parent integration (#400/#403).
Impact: a later donor PR could add another warning-free -CFLAGS group, and it would be caught only at the next parent pin adoption. This PR does not cause that and it does not block this PR; the frozen #102 scope excludes build-system changes.
Required change: optional. If wanted, a separate donor issue could run the parent's cflags_missing rule (or an equivalent) over tb/*/Makefile in `make check`.
Verification: the donor gate fails on a disposable copy that drops either flag from any group, and passes at the corrected tree.
```

## What I checked, by lens

### Conformance

- Acceptance 1. At head, `tb/pp_top/Makefile` has exactly two `-CFLAGS` groups: common `"-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"` (line 21) and fixture `"-DPP_TOP_SRP_DOM_DEF_VID=0x$(SRP_VID_FIXTURE) -Wall -Wextra"` (line 59). Both carry both flags. `SRP_VID_FIXTURE = 5A3C` (line 15) is unchanged. The executed fixture compile line shows `-DPP_TOP_SRP_DOM_DEF_VID=0x5A3C -Wall -Wextra`, and the binary reports `SRP_DOM_DEF_VID_P 0x5a3c`.
- Acceptance 2. I imported the unmodified parent checker (blob verified against the parent repository at `483a133e` and at live dev `574c29fa`; the bytes are identical) and ran it on git objects:
  - base returns `['-Wall', '-Wextra']`; head returns `[]`;
  - head without `-Wall` in the fixture group returns `['-Wall']`; without `-Wextra`, `['-Wextra']`; without both, both;
  - removing either flag from the common group is also reported, so the repeated flags cannot hide a regression in the other group;
  - across the parent-visible PP testbench Makefiles (30), the build-without-warnings count is 1 at base and 0 at head. This matches the parent budget `build without warnings = 0` (`receipts/probe_cflags.log`).
- Scope decision. The diff is one line in one file (`1 1 tb/pp_top/Makefile`, mode 100644 kept, `git diff --check` clean). It adds no checker exemption, ratchet change, RTL change, fixture renumbering, scenario removal or build rewrite. The edit copies the existing donor idiom at `tb/dyn_state/Makefile:25` (`-CFLAGS "-DSHAPE_1x1=1 -Wall -Wextra"`).
- Parent pin. Parent dev `574c29fa` still pins protocol-processor at `424c688f`, and this PR moves no parent pin. The only authorized PP integration pin (8452f564, for parent #400/#403) is not touched or implied.

### RTL

- No `hdl/` or `pp_top_wrap.sv` change. The RTL-side `+define+` and the child binding are the same bytes. Donor `lint_hdl.sh` on the head tree gives 37 LINT OK, exit 0. Hosted portability (Yosys + sv2v elaboration) executed in both source runs and passed.

### Robustness

- The effective compiler behaviour does not change. I verilated the fixture recipe exactly as each tree's Makefile spells it (base and head), then asked g++ for its enabled-warning table under the complete generated flag set: Verilator's `-Wno-*` list, `-O2`, both user groups, `-Os`.
  - The only flag-list difference is the second `-Wall -Wextra`.
  - The enabled-warning tables are byte-identical: full `-Q --help=warnings` tables sha256 `e4a7af66...` (unpublished scratch); the published 183-name enabled lists `receipts/effective_flags/enabled_warnings_{base,head}.txt` are both sha256 `c49c338e...`.
  - This matches the issue's own statement that the defect is a per-group policy incompatibility, not proof that warnings were disabled.
- The repeat is idempotent under any left-to-right option model too: at base the first `-Wall -Wextra` already followed Verilator's suppression list.
- Tokenisation is correct: `VM_USER_CFLAGS` gets separate `-DPP_TOP_SRP_DOM_DEF_VID=0x5A3C`, `-Wall`, `-Wextra` tokens. The parent `CFLAGS_RE` reads the group as one group. There is no trailing whitespace or CRLF (checked with `cat -A`), so the parent hygiene byte checks are unaffected.
- No other parent gate I inspected parses PP `-CFLAGS`: `check_hygiene.py` (byte checks only), `check_rtl_source_lists.py` (milan_dp source lists), `suite_tally.py`, `suite_shards.py`, `run_all_suites.sh`, `pp_srcs.py`. The pp_top tally format is unchanged.
- Nothing uses `-Werror`, so repeating the flags cannot turn an existing warning into a failure.

### Tests

- Full `tb/pp_top` `make run` at head: scoped Verilator 5.050, build/verilate jobs capped at 8 ("on 8 threads" in the Verilator report), g++ 16.2.1.
  - Unittest OK; fixture guards 4 cases PASS (default and 5A3C compile; 0002 refused with both diagnostics; 1002 refused with the class-D diagnostic).
  - `[build default, SRP_DOM_DEF_VID_P 0x0002] 1391 checks, 0 failures`; `[build fixture, SRP_DOM_DEF_VID_P 0x5a3c] 20 checks, 0 failures`; `1411 checks: 1411 PASS, 0 FAIL`; exit 0.
  - No C++ compiler warning lines. The Verilator PINMISSING/PINCONNECTEMPTY warnings were there before and come from the unchanged VFLAGS.
- DV sensitivity after the edit. In a disposable copy, only the C++ `-D` in the edited group was changed to 0x5A3D (RTL stays 16'h5A3C). The fixture build then reports 13 of 20 failures, including DV5 "LINK_DOWN restores" and DV6 "LINK_UP re-declares", and `make` exits 2. So the edited group still drives the C++ expectation, and the #97/#98 default-versus-fixture and LINK_DOWN/LINK_UP assertions still fire.
- The real parent checker is the acceptance test for the policy, and all 9 expectations pass at each of the two parent revisions.
- Hosted, exact head: push run 35772526304 and PR run 35772531911 both concluded success, with jobs `suites`, `docs-gates` and `portability` executed. The only skipped step is "Build Verilator v5.050" (cache hit), which is not a check. Both `suites` logs show Verilator 5.050, `PASS pp_top (1411 checks: 1411 PASS, 0 FAIL)` and `suites: 14943 checks total, 0 failing`.
- Manager native source bar (public evidence `ff273ff3`): nine commands, all exit 0. pp_top is 1411/0 there too, and the suite total of 14943 matches hosted.

### Docs

- No tracked document quotes the changed recipe. The Makefile header (two builds, one canonical tally) and the README DV build table stay accurate, because the override, the builds and the expectations did not change.
- Donor docs gates on the head tree: links 807 OK; matrix 115 REQ rows OK; modmatrix 86 rows, 0 untested; UPC map PASS. The manager's `make -j1 check` and hosted `docs-gates` also passed.
- The PR description matches the change and the checker behaviour. Its status paragraph and DoD boxes were written before the hosted runs and reviews finished (see pending manager duties).

## Commands and results (this round)

| # | What | Result | Receipt |
|---|---|---|---|
| 1 | Scoped Verilator identity | 5.050 rev v5.050; wrapper, binary and `verilated.mk` sha256 recorded | `receipts/tool_identity.txt` |
| 2 | Parent inputs, blob-verified | checker/scope/budget/CONTRIBUTING/CODE_QUALITY identical at `483a133e` and `574c29fa` | `receipts/parent_inputs.txt` |
| 3 | `python3 -B scripts/probe_cflags.py` at both parent revisions | 9 of 9 expectations PASS, exit 0 at each | `receipts/probe_cflags.log` |
| 4 | `taskset -c 0-7 make run VERILATOR=scripts/verilator-j8` on the head tree | exit 0, 1411 PASS / 0 FAIL | `receipts/pp_top_head_run.log` |
| 5 | `scripts/probe_effective_flags.sh` base and head | IDENTICAL warning set, exit 0 | `receipts/probe_effective_flags.log`, `receipts/effective_flags/*` |
| 6 | DV mismatch mutation (disposable copy) | fixture 13 of 20 FAIL, make exit 2 (expected) | `receipts/mutation_vid_mismatch.patch`, `receipts/mutation_vid_mismatch.log`, `receipts/mutation_vid_mismatch_full.log` |
| 7 | `bash scripts/lint_hdl.sh` on the head tree | 37 LINT OK, exit 0 | `receipts/lint_hdl_head.log` |
| 8 | links / matrix / gen_matrix --check / check_upc_map on the head tree | all exit 0 | `receipts/docs_gates_head.log` |
| 9 | Hosted runs, jobs, steps and suite tallies | both success; only the Verilator-cache build step skipped | `receipts/hosted_runs.txt` |
| 10 | Diff hygiene (`--check`, bytes, mode, name-status) | clean | `receipts/diff_hygiene.txt`, `receipts/pr-diff.patch` |
| 11 | Clone integrity (mid-round and final) | PASS | `receipts/integrity_mid.txt`, `receipts/integrity_final.txt` |

## Prior public review findings on this PR

I read these only after the verdict and ledger above were written. The one prior public review round on PR #103 is internal reviewer R252-1, POSITIVE at this same head: issue comment 5782917537, with the manager's summary in 5782918013. It records five per-lens PASS lines and no BLOCKER, MAJOR, MINOR or SUGGESTION. So there is no prior finding to resolve or keep at this head.

Its factual claims agree with my independent results:

- same real-checker outputs;
- same 1391 + 20 = 1411 pp_top tally and guard outcomes;
- same hosted runs and skipped cache step.

It also says the PR-event run checked out synthetic merge `e66e6eb9`. I confirmed that merge has tree `0547903a`, identical to the head tree, with parents base and head (`receipts/hosted_runs.txt`). The PR-event hosted run therefore tested the reviewed bytes.

The R252 limits (the author's parent self-test attempt exited 2 for an uninitialized parent clone; historical PR13/6 continuity UNKNOWN; PR13/9 negative-review baseline) do not change this verdict. I do not claim a full parent checker or self-test pass.

## Real limits of this round

- No full parent gate ran. That includes no parent `check_cpp_idiom.py` `main()`/`--selftest` (they need an initialized parent with pinned submodules), no parent builder, native or act bank, and no Docker/act. The parent policy result rests on the real `cflags_missing` function applied to the parent-visible PP Makefile population (30 files, filtered the way the checker's `testbench_makefiles` filters).
- I did not rerun donor `run_suites.sh` (the full donor bank), Yosys or the nvm_port figures. For those I rely on the manager's public native evidence (`ff273ff3`, nine commands exit 0) and on the two exact-head hosted runs I inspected. The pp_top suite, HDL lint and docs/matrix/UPC gates were run independently.
- Effective-warning equivalence was measured with host g++ 16.2.1 only. The hosted ubuntu g++ and any clang consumer were not measured. The equivalence argument there is that the first `-Wall -Wextra` already followed Verilator's `-Wno-*` list at base, so repeating it is idempotent.
- Probes ran on `git archive` copies of base and head under the unpublished scratch directory, with Verilator build/verilate jobs capped at 8 (`--build-jobs 8 --verilate-jobs 8`, `taskset -c 0-7`). The review clone was never built in, and it verifies byte-exact before and after (224 blobs/modes/index entries, 0 gitlinks: this repository has no submodules, so no gitlinks were required).
- No physical calibration or hardware ran. Field skips are not hardware proof. This donor change has no hardware-facing content.
- Receipts have host path prefixes replaced by `$PACKET`, `$REVIEW_CLONE`, `$VALIDATION_STORAGE` and `$WORKSPACE_HOME` using `scripts/sanitize.sh`. No other byte was changed.

## Pending manager duties

- Validate the final current-main merge candidate at the merge turn. Donor `main` is still `f70ba36e` (identical to the PR base), and parent live dev is `574c29fa`.
- Own hosted/act acceptance.
- Obtain the second required independent positive under the completion bar. With R252-1, this round would make two, including the external system.
- Merge only with maintainer authorization, then run post-merge containment and close #102 to Done.
- Refresh the PR #103 status paragraph and DoD checkboxes. They still say hosted gates and reviews are pending.
- Keep parent #400/#403 unchanged. This PR authorizes no parent pin adoption; the only authorized PP integration pin remains 8452f564 for #400/#403. Any future parent pin selection must separately pass the complete parent gate and integration bar.
- Decide whether to track the optional S1 in a separate donor issue. It is not required for this PR.

## Packet

`REPORT.md` plus every file listed in `MANIFEST.sha256` (paths relative to the packet root). `scratch/` is disposable and unpublished.

R253-1 FINISHED
