[R556] POSITIVE - exact head abe2476c4771bedc84531cf8d05fd12ef947c0cf

Internal independent review R556-8 of kebag-logic/milan-fpga#697 / kebag-logic/tsn-c-stack PR #16, round 9.
Exact head `abe2476c4771bedc84531cf8d05fd12ef947c0cf`, tree `06ec5d3e9a4a677a2506e96b9fe77a933137b03c`.
Delta reviewed: `68070cb5..abe2476c` (three one-line commits, linear on `68070cb5`, one per assigned item), within the full PR range `ae982af8..abe2476c`.

## 1. Verdict

POSITIVE. The three Round 9 items are implemented as assigned. Each fix has a control that fails when the fix is reverted.

- R556-7-F1 (`gtest-spi.h` assertions): RESOLVED.
- R556-7-F2 and R557-7-F1 (pinned install in a non-default prefix): RESOLVED.
- R556-7-S1 (prefix rule): ADOPTED.
- R556-7-RS1 (rule-table full stop): RESOLVED.

No MINOR, MAJOR or BLOCKER is open. There is one new SUGGESTION (S1). Earlier suggestions and one residue carry over (section 4).

## 2. Scope and authorities

- Contributor rules: `CONTRIBUTING.md`, `docs/CODING_STANDARD.md`, `docs/VERIFICATION.md`. The repository has no `AGENTS.md`.
- Issue body and owner decisions: comments 6074086970, 6074093506 and 6074191062 (MIT licence, separate repository, name).
- Lane assignment: comment 6074245112. Threat model: comment 6079166369.
- Round 9 assignment: comment 6079940414. REVIEW READY: comment 6080196029.
- PR body, Round 9 section.
- Threat model applied: a deliberately obfuscated construction outside the six listed rules is a SUGGESTION unless it is in the shipped tree.

## 3. Findings at this head

### R556-8-S1 - SUGGESTION - Robustness, Tests

- **Artifact:** `scripts/assertion_templates.py:43-45`. This line predates the round and was not changed in it.
- **Problem:** the template generator reads `pkg-config --cflags --libs gmock gtest_main` with `str.split()`. It passes the raw `-I` flags, under `-Werror`.
- **Contrast:** since `8af4988`, every other consumer (`refused_macros`, the selftest controls, `mutation.py` and `dependency_selftest.py`) uses `package_flags()`. That function uses `shlex` and maps `-I` to `-isystem`.
- **Evidence:** the same real 1.14.0 install was copied to a prefix whose path contains a space. `assertion_templates.py --check` then fails: the include path is split into `-I…/space\` and `prefix/gtest/include`. With the same install, `mutation.py --select` passes. Receipt: `receipts/run/space-prefix-probe.log`; script: `scripts/space_prefix_probe.sh`.
  - In the documented separate-prefix setup without a space, the generator passes. Receipts: `receipts/validate/assertion-templates.log`, all 24 gates rc 0.
  - The hosted system install also passes.
- **Impact:** the failure is fail-closed. An unusual prefix path makes the assertion-templates gate fail; nothing is wrongly accepted. In a non-default prefix, the generator also still treats the pinned headers as ordinary headers. Today's forms compile cleanly that way.
- **Optional outcome:** build the generator's flags with `package_flags('--cflags')` and `package_flags('--libs')`, plus `-lgtest_main`, as the selftest controls already do.
- **Verification:** re-run `scripts/space_prefix_probe.sh`. `--check` should return 0.

No other new finding. Wording in the docs and PR body was checked against behaviour (section 5, Docs) and no residue was found.

## 4. Prior findings: disposition at this head

I read the round-7 public findings only after my own pass and draft verdict.

| Prior ID | Severity | Disposition | Exact-head evidence |
|---|---|---|---|
| R556-7-F1 `gtest-spi.h` assertions pass the gate (regression) | MINOR | RESOLVED | `assertion_forms.py:45-65` preprocesses every `gtest/*.h` and `gmock/*.h` of the pinned install: 21 public headers. g++ and clang++ both regenerate the shipped 85 names (probe A1, A6). The four failure-capturing names are listed (A2). The unchanged round-7 probe `probe_assertions.py` now refuses all four spi rows, which round 7 accepted. The unchanged `probe_spi_tree.sh` honest-contributor tree is now refused by `needles` and `test-inventory`. Reverting the generator to two headers fails `--check` (B1). Dropping the four names from the JSON fails `--check` (B3). |
| R556-7-S1 trailing-underscore internals | SUGGESTION | ADOPTED | `assertion_forms.py:22-23` refuses any `EXPECT_`/`ASSERT_`/`GTEST_` identifier outside the 14 forms. Every one of 205 such or `FAIL*`/`ADD_FAILURE*`/`SUCCEED` macro names defined by all 38 installed headers (public and internal) is refused (A3). The 14 allowed forms stay accepted (A4). The `GTEST_NONFATAL_FAILURE_` control compiles, fails at runtime and is refused. Removing the prefix rule fails `--check --selftest` (B2). The shipped `tests/` contain no refused name (D1). |
| R556-7-F2 = R557-7-F1 non-default-prefix install | MINOR | RESOLVED | `assertion_forms.py:28-42` maps `-I` (joined or separate) to `-isystem` and keeps every other flag. `dependency_selftest.py:23-25` removes ambient include and library variables. `:41-46` puts the real pinned headers in a scratch include directory supplied through package flags. `:66-73` requires a project `-Wsign-compare` error. Details below the table. |
| R556-7-RS1 rule-table sentence | RESIDUE | RESOLVED | `docs/VERIFICATION.md:71` ends with a full stop. The two threat-model sentences are at `:82-83`, after the table. |
| R556-6-S2 / R556-7 directory scope (headers or linker `INCLUDE` outside the four directories) | SUGGESTION | RETAINED | Unchanged `probe_comment_gate.py` row `ld-include-other` is still accepted, as declared. Not in the shipped tree. |
| R556-2-S1 long blank runs in public headers | SUGGESTION | RETAINED (deferred by the manager) | Maximum blank runs are 81 (`acmp.h`), 43 (`adp.h`), 10 (`wire.h`) and 3 (`maap.h`) lines. |
| R556-1-R3 closed PR #1 body | RESIDUE | RETAINED (manager duty) | PR #1 still says "Hosted execution awaits publication of this branch." The exact fix stands as carried. |
| R556-1-S4 clause-check confirmation | carried | RETAINED | No normative-text re-audit in this delta. |
| All other earlier IDs (R556-1..6, R557-1..6) | various | Still RESOLVED | The unchanged public replay (18 scripts) gives the same status as at `68070cb5` for every row. See section 6. |

Details for R556-7-F2 / R557-7-F1:

- R557-7's `probe_package_prefix.py`, re-run unchanged against a real 1.14.0 build (`f8d7d77c`) in a scratch prefix with no ambient paths: configure, build, test, mutation, dependency-control and system-header-control all return 0. At `68070cb5` the mutation and dependency steps failed.
- The unchanged round-7 `probe_dependency.sh` with the upstream `-I` metadata now returns 0. Its version, compile-flag and link-flag reversals still fail.
- Reverting only the rewrite makes the dependency gate fail at `gtest/gtest.h:1379` `-Werror=sign-compare`, inside the scratch-copied headers (B4a). The scratch-prefix mutation build fails the same way (B4b). So the control works even where the pinned package is a system install, as on the hosted runner.
- A project signed comparison added to a test still fails the real mutation build with g++ and clang++ (C1). The unmodified head builds and catches with both compilers from the scratch prefix (C0).

## 5. Lenses

- **Conformance - CLEAN.**
  - Item 1 matches the assignment: every public header of the pinned install, the prefix rule including trailing underscores, `--check` regeneration, and controls `EXPECT_NONFATAL_FAILURE` and `GTEST_NONFATAL_FAILURE_` (plus the other three spi forms). A1-A7, B1-B3.
  - Item 2 matches: `-isystem` as CMake imported targets do, project warnings and checked flags kept, `-Wsign-compare` not disabled, a real-1.14.0 scratch-prefix control with no ambient paths. B4, C0/C1, the R557-7 probe.
  - Item 3 matches: VERIFICATION `:71`, `:82-83`.
  - One commit per item, one-line subjects, holder identity on all three commits.
  - Production, test and CI files are unchanged in the delta (`git diff --stat 68070cb5..abe2476 -- src include examples tests cmake CMakeLists.txt .github` is empty).
  - RV32 Debug and Release ELF images and the core objects are byte-identical between `68070cb5` and `abe2476` when built from the same source path (`receipts/rv32-same-path-compare.txt`). Built from different paths, the Debug ELF differs only through embedded paths.
  - Issue acceptance items (boundary, licence, traceability, privacy) still pass as gates.
- **RTL - CLEAN (not applicable).** The repository has 74 tracked files and no HDL, constraint or tool-script files (`git ls-files` count of `.v/.sv/.vhd/.xdc/.tcl` is 0). The delta is Python and Markdown only. No simulator run applies, so the pinned simulator was not used. The freestanding RV32 target is covered under Tests.
- **Robustness - CLEAN (S1 is a suggestion).**
  - `package_flags` handles `-I` both joined and split. It refuses a dangling `-I`, and handles quoted and escaped paths through `shlex`; the dependency control uses a path with a space.
  - Ambient variables are removed in the control.
  - `refused_macros` refuses an empty header set. The generated list is identical under both compilers.
  - The prefix rule refuses object-like and function-like names alike, and does not match identifiers that merely contain a prefix (A7).
  - Out-of-rule constructions (direct `::testing::internal` calls, the `GMOCK_INTERNAL_*` static checks listed in `A-other-names.json`) are outside the threat model and not in the shipped tree.
  - S1 is the only new robustness observation.
- **Tests - CLEAN.**
  - Local isolated run of all 24 gates: rc 0 (`receipts/validate/gates.json`).
  - GCC coverage and Clang address/undefined-behaviour suites: 7 binaries each. Adjusted coverage is 100%, matching the ratchet totals of 1164 lines and 583 branches.
  - Fresh campaign: 311/311 CAUGHT. Independent per-arm XML regrade: 311 plants, 329 killers, 0 unconfirmed (`receipts/regrade-xml.log`).
  - RV32 Debug and Release: rc 0, no unresolved symbols, minimal-port smoke passes, link with `-Wl,--no-undefined -Wl,--fatal-warnings` (`receipts/rv32/*/link.txt`).
  - 19 of my probes pass (`receipts/r556-8-probes/results.json`).
  - Earlier probes re-run unchanged (section 6).
  - Hosted CI at the exact head: both jobs green on both events, with the same 311/329 regrade on both artifacts.
- **Docs - CLEAN.**
  - `CODING_STANDARD.md:32-34` and `VERIFICATION.md:85-107` describe the observed behaviour:
    - every public header,
    - `gtest-spi.h`,
    - the prefix rule,
    - the controls executing with 0 or 1 failures, as the gate logs show,
    - `-I` to `-isystem`,
    - the signedness control,
    - the separate-install instructions. I used these instructions as written for the isolated run.
  - PR body Round 9 claims checked: 21 headers, 85 names from both compilers, six isolated-prefix steps passing, removal controls failing, 311/329, coverage totals, RV32 results.
  - The rule table now ends its introduction with a full stop.

## 6. Executed evidence (this review)

All receipts are listed in `MANIFEST.sha256`. Host paths are redacted as `$PACKET`, `$HEAD_CLONE` and `$HOME`.

| Evidence | Result | Receipt |
|---|---|---|
| Isolated environment: GoogleTest 1.14.0 built from `f8d7d77c` into a scratch prefix; Ubuntu clang 18.1.3 lexer; download hashes equal to R557-7's | prepared | `receipts/sdk-downloads.json`, `receipts/environment.json`, `scripts/make_env.py`, `scripts/isolated.sh` |
| `validate.py --jobs 8 --graphs` at head, no `CPATH`/`C_INCLUDE_PATH`/`CPLUS_INCLUDE_PATH`/`LIBRARY_PATH` | 24/24 gates rc 0; 311/311; graphs rendered | `receipts/validate/`, `receipts/run/validate.*` |
| Independent per-arm XML regrade, local and both hosted artifacts | 329/329 killers confirmed, three times | `receipts/regrade-xml.log`, `receipts/hosted-regrade.log` |
| `baremetal.py` at head; same-path comparison with `68070cb5` | Debug and Release rc 0; ELF and core objects byte-identical | `receipts/rv32/`, `receipts/rv32-same-path-compare.txt` |
| R557-7 `probe_package_prefix.py`, unchanged | 6/6 steps rc 0 | `receipts/r557-7-package-prefix/` |
| R556-7 probes, unchanged (`probe_assertions`, `probe_comment_gate`, `probe_spi_tree`, `probe_dependency`) | all rows as intended; round-7 F1/F2 rows now closed | `receipts/r556-7-replay/` |
| R557-7 `replay_public.py` with verified published blobs (32): R556-3..6, R557-4..6 and the early scripts | 18 rows; statuses identical to `68070cb5`. The three nonzero rows (`R557-4-full`, `R557-6-full`, `early-comments`) are historical bypass scripts whose own "bypass works" assertions fail because the gate refuses them. All 11 R556-6 full-tree rows are CAUGHT. | `receipts/public-replay/` |
| My probes A1-A7, B1-B5, C0-C1, D1 | 19 PASS (B5 informational) | `scripts/r556_8_probes.py`, `receipts/r556-8-probes/` |
| Space-in-prefix probe | S1 reproduced | `scripts/space_prefix_probe.sh`, `receipts/run/space-prefix-probe.log` |
| Hosted CI (`gh pr checks`; runs 37925745383 pull_request and 37925739153 push) | quality and bare-metal success on both, `headSha` = exact head; 24 gates rc 0, 311 CAUGHT, RV32 rc 0 in the artifacts | `receipts/hosted-checks.txt`, `receipts/hosted-runs.json`, `receipts/hosted/` |
| Clone integrity after all probes | `HEAD` = `abe2476c`; worktree equals HEAD; index blob ids and modes equal `ls-tree HEAD`; `git fsck` clean; no ignored or untracked files; no submodule gitlinks exist in this repository | this report |

## 7. Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round 9 assignment items 1-3 against `assertion_forms.py`, `assertion_templates.py`, `assertion-defaults.json`, `dependency_selftest.py`, `VERIFICATION.md`, `CODING_STANDARD.md`; commit shape; unchanged production, test and CI files; RV32 byte identity | R556-8 | abe2476c4771bedc84531cf8d05fd12ef947c0cf |
| RTL | CLEAN (not applicable) | Tracked file list (no HDL); delta file types | R556-8 | abe2476c4771bedc84531cf8d05fd12ef947c0cf |
| Robustness | CLEAN | Flag rewriting, ambient-path removal, header enumeration, prefix rule, compiler agreement, space-in-prefix behaviour (S1) | R556-8 | abe2476c4771bedc84531cf8d05fd12ef947c0cf |
| Tests | CLEAN | 24 isolated gates, 311-plant campaign with 329-killer regrade, RV32 two configurations, 19 own probes, 4 + 18 + 1 unchanged earlier probe scripts, hosted runs and artifacts | R556-8 | abe2476c4771bedc84531cf8d05fd12ef947c0cf |
| Docs | CLEAN | `CODING_STANDARD.md`, `VERIFICATION.md` (rule table, threat model, pin, generator and dependency claims), `CONTRIBUTING.md`, PR body Round 9, closed PR #1 body (R556-1-R3) | R556-8 | abe2476c4771bedc84531cf8d05fd12ef947c0cf |

## 8. Real limits

- Local compilers (GCC 16.2, Clang 23.1, RV32 GCC from the host distribution) are newer than the hosted Ubuntu 24.04 toolchain. Hosted runs cover only the unmodified head with the system 1.14.0 package.
- The non-default-prefix controls ran locally only.
- The scratch install is built from the upstream 1.14.0 source, not the Ubuntu package.
- The dependency control in the tree copies headers only. Its libraries come from whichever install `pkg-config` selects. A full prefix install was exercised by the R557-7 probe and my isolated gate run, not by an in-tree gate.
- The assertion vocabulary is closed for the macros the pinned install defines. Direct calls to GoogleTest internals are outside the listed rules (threat model).
- No manager source bank runs at this head. I do not claim or infer one. Source-head execution evidence is the author's published receipts plus this review's own runs.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware applies to this repository.
- Another reviewer session ran concurrently on the same host. It shared nothing with this packet.

## 9. Pending manager duties

- Hosted/act acceptance at this head. Both hosted jobs are green; the manager owns the acceptance.
- At the merge turn, validate the current-dev merge candidate (builder and native banks) and link its receipts. Source base `ae982af85ec97286bd35b39403926d8f0eaec81d`; live dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.
- Carry R556-1-R3 (closed PR #1 body) on the residue checklist.
- Track the retained suggestions R556-2-S1 and R556-6-S2, and the new R556-8-S1, at the manager's discretion.
- Obtain the second independent review. Two positive reviews are required before merge.

R556-8 FINISHED
