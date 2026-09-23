[R244] POSITIVE - exact head bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34

Round R244-2, external cleared-context review of issue #423 / PR #519.
Exact head `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34`, tree
`ab96af335f1428770a1a96c0345a9f55278ad25b`, source base (live dev when the lane
merged it) `483a133ed08867ea0d300d2b4a027b5b48a4282f`. I applied all five lenses
independently to the whole PR (`483a133e..bb4be4d3`, 10 files) and not just the
correction commits.

No BLOCKER, MAJOR or MINOR finding is open. Three SUGGESTIONs are recorded; they
do not affect coverage. All four R244-1 findings (A MAJOR, B/C/D MINOR) are
resolved at their root, and the earlier F1/F2/F3 resolutions still hold. Three
pre-existing, out-of-scope behaviors are recorded as observations for new Issues
(O-1 to O-3). None of them was introduced or worsened by this PR.

## Reconstruction

Order followed: AGENTS.md, CONTRIBUTING.md (2.1 step 7), docs/README.md,
REQUIREMENTS.md REQ-VER-04, the #423 body, the frozen
[decision 5777210218](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218)
and the design report it cites (for the T mode rule), the manager and author
comments on #423. Then the full diff `483a133e..bb4be4d3` and its history
(`fed4f63f`, `b911c116`, `4671e582`, dev merge `e1e0f979`, `1a43ba80`,
`e4354566`, `bb4be4d3`), then my own executable probes. I read the public
author packet (`review-evidence/423-r1/correction-a186/`: HANDOFF, PR-BODY,
REVIEW-READY) only after my probes had run.

Prior finding texts (R244-1 report 5789494311, R251-1 5780883992, R251-2
5782234201) were read only after my independent pass over the diff and all
five lenses. I read no current-round report from another reviewer and no
private author, lane or management material.

The dev merge `e1e0f979` reproduces: `git merge-tree --write-tree 4671e582
483a133e` = `12dcd757`, equal to its tree. Its dev-side paths
(`docs/ENDSTATION_BUILDER.md`, `sw/builder/*`) are disjoint from the PR.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S-1 - SUGGESTION - Tests, Docs

- **Location:** PR #519 body, "Validation" paragraph, as published at this
  head: "Removing ... the byte source copies ... fails the self-test, including
  on a host without `localedef`."
- **Evidence:** I restored text-mode copies in
  `scripts/merge_containment_selftest_mutations.py:48-50,62-63` (mutant
  `text-source-copies`). Results:
  - Default self-test, UTF-8 parent: 678/678, exit 0.
  - The same with `locale`/`localedef` removed from PATH: 507 ok, 3 NOT RUN,
    exit 0.
  - Only an ASCII parent catches it: crash after 147 assertions, exit 1.
  - Receipts: `receipts/mutants/text-copies-*.txt`.
- **Impact:** the R244-B fix itself is correct: every parent passes (see below).
  The PR's "How to reproduce" lists the ASCII-parent command, so the sentence
  can be read as true. But the ordinary `--selftest` run that the suite and
  hosted CI execute (UTF-8 parents) does not guard against this regression. A
  reader may assume it does.
- **Optional outcome:** reword the sentence to "fails the ASCII-parent
  self-test command". Or have the ASCII locale child exercise one
  mutation-harness copy, so the default run guards it.
- **Verification:** rerun `scripts/probe_mutants.py` with
  `ONLY=text-source-copies` under a UTF-8 parent.

### S-2 - SUGGESTION - Tests, Docs

- **Location:** `scripts/run_all_suites.sh:249-261` (unchanged by this PR) and
  `CONTRIBUTING.md:249-251`.
- **Evidence:** the self-test prints `NOT RUN locale-...` when locale data is
  missing and still exits 0. `run_all_suites.sh` prints the captured self-test
  output only on exit 3 or failure, so the notice is dropped on success.
- **Impact:** a full-suite or hosted pass cannot show whether the strict
  UTF-8, Latin-1 and Big5 fresh-process controls ran. Coverage of the
  transport itself does not depend on them: the in-process Big5 control still
  kills every transport restoration without locale tools (below). So this is
  observability only.
- **Optional outcome:** echo `NOT RUN` lines even on success, or count them in
  the self-test summary.

### S-3 - SUGGESTION - Docs

- **Location:** `CONTRIBUTING.md:260`: "The decision records both
  original/replay pairs and their hashes."
- **Evidence:** decision comment 5777210218 contains neither the commit pairs
  nor the SHA-256 values. They are in the #423 body, and the cited design
  report calls them "the issue's SHA-256 values". The command at
  `CONTRIBUTING.md:256` is correct: at the pinned gPTP processor objects it
  reproduces `fa20a251...` twice and `d3d164b3...` twice
  (`receipts/pr62.txt`).
- **Optional outcome:** say that Issue #423's body records them.

## Prior findings at this head

| Finding | Disposition at bb4be4d3 | Evidence (this round) |
|---|---|---|
| R244-A MAJOR (Conformance, RTL, Robustness, Tests, Docs): filename bytes changed under a non-round-trip codec, false `contained`/0 | **RESOLVED** | See the R244-A detail below the table. |
| R244-B MINOR (Tests, Robustness, Conformance): self-test crashed under an ASCII parent | **RESOLVED** | 678/678, exit 0, nothing NOT RUN, under 7 parents: UTF-8 locale, UTF-8 mode, ASCII, Latin-1, Big5, JOHAB, cp932 (`receipts/parent-selftest/`). The previous head still crashes after 147 under ASCII (`receipts/parent-selftest-prev/ascii.log`). Regression guarding is noted in S-1. |
| R244-C MINOR (Tests): T guards without killing controls | **RESOLVED** | Each guard mutant fails the default self-test on its intended control: single merge base (`retention-merge-base-two-real-bases`), `--ignore-submodules=none` (`hostile-gitlink-reset`), `--no-renames` (`hostile-rename-undone`), ancestor type rule (`symlink-ancestor-clean-merge`), replay distinctness (`distinct-linear`/`distinct-merge`). Receipt: `receipts/mutants/sweep-full-path.txt`. |
| R244-D MINOR (Robustness, Tests): STRANDED note crashed a strict stdout | **RESOLVED** | See the R244-D detail below the table. |
| F1 (R251-1) BLOCKER (Conformance, Robustness): literal paths changed by decoding | **RESOLVED, holds** | Its full required matrix passes in fresh UTF-8 and Latin-1 processes, and now also under non-injective codecs. Rows: linear missing / retained, merge reverted (original path named) / retained via raw retention, postimage helper, entry lookup, exact bytes. Sources: `receipts/probe-codec/head.json` and the self-test's locale children. |
| F2 (R251-1) MAJOR (Tests, Conformance): no locale regression coverage | **RESOLVED, holds** | The default owner runs verified-encoding children (UTF-8 mode, ASCII, strict UTF-8, Latin-1, Big5) plus the in-process Big5 control. They use byte-defined names including `c3 a9`, alias `e9`, raw `ff`, euro and `a1 fe`, with entry, postimage, patch and CLI rows. Unavailable locales print NOT RUN. |
| F3 (R251-2) MINOR (Tests, Robustness, Conformance): Latin-1 parent diagnostic assertion | **RESOLVED, holds** | Latin-1 parent 678/678. The raw-name fixture and exact path assertion are retained (`merge_containment_selftest_retention.py:84-87`). The expected label is now derived from the exact bytes, so it is locale-independent. |
| O-1 (R244-1 observation, pre-existing): subdirectory invocation | **RETAINED as out-of-scope** | See O-1 below. |

**R244-A detail.**

- **My probe:** `scripts/probe_codec.py` runs 57 checks per environment in a
  fresh verified process through a real stdout. Environments: UTF-8 locale,
  UTF-8 mode, ASCII, Latin-1, Big5, Big5-HKSCS, JOHAB and cp932. The last
  three non-injective codecs are beyond the author's Big5 witness.
- **At the exact head:** 0 mismatches in all 8 environments
  (`receipts/probe-codec/summary-head.txt`).
- **At the previous head `4671e582`:** the same probe reproduces false
  `contained`/0 under Big5, Big5-HKSCS, JOHAB and cp932. Affected checks:
  linear missing, merge reverted, repeated-block postimage, and patch-ID
  collisions (`summary-prev.txt`). This shows the probe is sensitive.
- **Restorations, one site at a time:** argv, T lookup, patch transport,
  path arm, postimage paths and the lossy-output guard. Each fails the default
  self-test. Each still fails with `locale`/`localedef` absent from PATH,
  where the in-process Big5 control kills it
  (`receipts/mutants/sweep-no-localedef.txt`).
- **Docstrings:** both transport docstrings restore the "(rc, stdout)...
  Never raises" contract (`merge_containment_git.py:18-47`).

**R244-D detail.**

- **Probe:** three targets through a real stdout in all 8 environments. Each
  gives `contained`, `STRANDED`, `contained`, empty stderr, ASCII-only output,
  every filename label present, exit 1 (`report-*` rows in
  `receipts/probe-codec/head.json`).
- **Restoration:** reverting to decoded labels fails the self-test, with or
  without locale tools.
- **Previous head:** crashes after the first target under strict UTF-8, Big5,
  Big5-HKSCS and JOHAB.

## Lens results at this head

- [R244] PASS Conformance - `scripts/merge_containment_replay.py:32-153`;
  `scripts/check_merge_containment.py:518-580`; `CONTRIBUTING.md:208-260`;
  decision 5777210218; `receipts/pr62.txt`; `receipts/selftest-names-*.txt`.
  What was checked:
  - **G1:** one source-only merge, 3 fields, P2's parents equal `[P1]`, and
    tree(M) = tree(P2).
  - **H:** the unchanged distinct whitespace-exact helper. Arm order is
    ancestry, touched path, linear patch-ID, new fallback, STRANDED.
  - **T:** exactly one merge base; a raw `--no-renames
    --ignore-submodules=none -z` changed-path set; identity including
    absence; regular-blob and mode rule exactly as in the design report
    ("tip mode = branch mode, or branch mode = B mode"); `merge-file -p` over
    (tip, B, source); rc 0 with byte-equal output; rc outside 0-127 is a
    measurement error.
  - **Verdicts:** G1/H decline keeps the existing verdict. Unproved T gives
    UNKNOWN/1 with paths named. Exit codes are unchanged.
  - **Actual gPTP processor PR62:** UNKNOWN/1 at `f0f1c055` and `c1b61743`,
    naming `'tb/tsngen/mutants.py'` and `'tb/verilator/gaskets/mutants.py'`.
    PR61 stays contained/0. The base gives STRANDED/1. All four decision
    patch hashes reproduce.
  - **Existing arms:** all 145 base assertion names are present among the 678
    at head.
- [R244] PASS RTL - `git diff --name-status 483a133e..bb4be4d3` (CONTRIBUTING
  plus 9 Python files); gitlinks identical at base and head; transport and
  replay interfaces; exit contract; suite consumption; runtime.
  - **Scope:** no HDL, testbench, synthesis, constraint, firmware, workflow,
    `.gitmodules` or gitlink change. The four gitlinks are identical at base
    and head (`c1b61743`, `424c688f`, `48ff7a7e`, `efeb541a`).
  - **Transport contract:** `merge_containment_git.py:18-52`; `git_text` rc 256
    cannot collide with a process status.
  - **Replay interface:** `merge_containment_replay.py:132-153`.
  - **Exit contract:** `check_merge_containment.py:83-87,880-911`, unchanged
    0/1/2/3. `run_all_suites.sh:249-261` consumption is unchanged.
  - **Runtime:** the self-test is bounded at about 29 s here. Isolated-mode
    (`-I`) invocation works through the mutation replicas.
- [R244] PASS Robustness - `receipts/probe-codec/`, `receipts/probe-config-head.txt`,
  `receipts/merge-alignment-*.json`, `receipts/revert-distance-gap*.json`,
  `receipts/parent-selftest/`.
  - **Encodings:** 8 encodings, including 4 non-injective codecs, give correct
    verdicts. Output that does not round-trip is refused: the no-operand lossy
    HEAD gives rc 2, where the base false-passes.
  - **Hostile configuration and environment:** a baseline plus 20 hostile
    settings x 5 histories (105 runs), 0 unsafe results. Deviations fail closed as UNKNOWN (`color.*=always`,
    `GIT_ICASE_PATHSPECS`, `GIT_GLOB_PATHSPECS`).
  - **Merge alignment:** lost unique insertions 11,199/11,199 refused
    (`merge-alignment-v1-by-mode.json` plus `merge-alignment-smoke-by-mode.txt`).
    Partial reverts 19,981/19,981 refused. Exact in-place reverts with edits
    at least 2 lines away: 0/15,025 accepted. The only acceptances need an
    edit adjacent to the hunk that realigns it (O-3).
  - **Faults:** missing blobs, fault injections and temporary-storage errors
    are UNKNOWN (self-test).
- [R244] PASS Tests - `receipts/selftest-default.log` (678/678, 0 FAIL, 0 NOT RUN);
  `receipts/mutants/sweep-full-path.txt`, `sweep-no-localedef.txt`.
  - **Sweep:** 23 mutants plus 1 control; the control passes 678/678.
    - 22 mutants ran in one sweep: 16 killed by the default self-test,
      including all 5 R244-C guards, the 5 transport-site restorations, the
      lossy-output guard and decoded labels.
    - The 23rd, `text-source-copies`, ran separately. It survives a UTF-8
      parent and is killed only under an ASCII parent (S-1).
  - **The six sweep survivors** are each equivalent in verdict terms. Five are
    listed here; the sixth, `RC_LOSSY_OUTPUT = 0`, follows the list.
    - `_tree_entry` name check: a literal pathspec with exact-byte argv
      returns only that name.
    - `--full-tree`: matters only from a subdirectory, where the earlier arm
      already false-passes (O-1).
    - Conflict-style override: a conflict is rc > 0 in every style.
    - T `--no-ext-diff`/`--no-textconv`: no effect on `--name-only`.
    - G1 parent-read check: without it the result is STRANDED instead of
      UNKNOWN, both exit 1.
  - **`RC_LOSSY_OUTPUT = 0`:** every `git_text` caller treats (0, "") as
    failure or refusal, so it is equivalent too.
  - **Public mutations:** the ten public mutations and the 31-case matrix run
    in the default owner.
- [R244] PASS Docs - `CONTRIBUTING.md:204-260`;
  `check_merge_containment.py:44-61`; module docstrings of
  `merge_containment_git.py`, `merge_containment_replay.py` and
  `merge_containment_selftest_locale.py`; PR #519 body; `receipts/gates/`
  (16 commands exit 0).
  - **Claims checked:** every step-7 claim matches code and measurements:
    G1/H/T wording, byte transport, lossy refusal, ASCII labels, in-process
    Big5, the five children, NOT RUN semantics, the hash command.
  - **Gates:** em-dash gate 0 findings over 54 added lines. All added lines
    are ASCII. Idiom, hygiene, TOC, doc-style/paths, naming, fail-fast,
    test-evidence, TODO, feature-status and `git diff --check` exit 0.
  - **Open:** only S-1..S-3.

## Reviewer-owned lens ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Decision 5777210218 and the cited mode rule vs `merge_containment_replay.py:32-153`; arm order `check_merge_containment.py:518-580`; `CONTRIBUTING.md:204-260`; actual PR62/PR61 at both targets; hash reproduction; 145 original assertion names | R244-2 | bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34 |
| RTL | CLEAN | Diff name-status (no HDL/tb/syn/workflow/gitlink change); gitlinks base = head; transport contract `merge_containment_git.py:18-52`; replay interface `:132-153`; exit contract `check_merge_containment.py:83-87,880-911`; `run_all_suites.sh:249-261`; self-test runtime | R244-2 | bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34 |
| Robustness | CLEAN | 8-encoding CLI probe; argv/HEAD ref probe; 105-run hostile config/env probe; 104,704 raw merge-file trials; fault controls `merge_containment_selftest_retention.py:240-304`; parent-locale runs | R244-2 | bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34 |
| Tests | CLEAN (S-1, S-2 suggestions only) | Default self-test 678/678; 23-mutant sweep plus no-locale-tools rerun; 7 parent locales; `merge_containment_selftest_{locale,retention,replay,mutations}.py` | R244-2 | bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34 |
| Docs | CLEAN (S-1, S-2, S-3 suggestions only) | `CONTRIBUTING.md:204-260`; checker and module docstrings; PR #519 body at this head; 16 docs/style gate receipts | R244-2 | bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34 |

## Out-of-scope observations (pre-existing; recommend new Issues)

- **O-1 (retained from R244-1): subdirectory invocation.** Running the checker
  from a repository subdirectory makes the existing arms' literal pathspecs
  cwd-relative. It then reports `contained`/0 for a stranded root-level edit.
  The behavior is identical at base `483a133e` and at head
  (`receipts/probe-subdir.txt`). T's `--full-tree` is not the cause. No Issue
  for it was found by search.
- **O-2: argv branch names under non-injective codecs.** Under Big5 and cp932,
  Python's startup decoding of argv (libc) and `os.fsencode` (Python codec)
  disagree. So `--no-fetch --base main <a1fe-branch>` measures the `a2 41`
  branch and prints `contained`/0 for a stranded branch. The same happens at
  the base. Under Big5-HKSCS and JOHAB the run is refused, or crashes printing
  the label (exit 1).
  - This PR improves the no-operand case: the base false-passes under all four
    codecs, and the head refuses with rc 2 (`receipts/probe-refs/`).
  - Branch names are not filenames, and the author lists command-line ref
    labels as unmeasured. So this is outside #423.
- **O-3: bounded alignment characterization.** T accepted 12 of 16,180 cases
  where the tip restores a deleted unique line between its original
  neighbours. Every case has an edit adjacent to the hunk that lets
  `merge-file` align the deletion as shared.
  - Example: `end / D / end / end` -> source `end / end / end` -> tip
    `end / end / D / end` (`receipts/merge-alignment-hdl-examples.txt`).
  - The tip is byte-identical to "source plus D re-added one line later". The
    frozen contract discloses this as "cannot prove arbitrary later semantic
    rewrites" and "without a general alignment proof", so it is not a finding.
  - With edits at least 2 lines from the hunk, no revert was accepted.

## Hosted evidence inspected (metadata only; not executed by this reviewer)

- **Check runs at the exact head:** 22 (`receipts/hosted-check-runs.tsv`).
  - **21 completed `success`.** This includes all seven required contexts:
    `rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`,
    `elaborate`, `verilator-suites`, `yosys-portability`. Verilator shards 0-4
    and Yosys shards 0-3 completed. Yosys shards took 26-31 s each.
  - **1 `skipped`:** "Physical gPTP (nightly and manual)", which is outside the
    required aggregates.
- **Not read:** logs. Whether the hosted sweep executed the three
  locale-dependent children is not visible (S-2). Hosted and act acceptance
  belong to the manager.

## Real limits of this round

- **Not run:** full parent/PP/gPTP/Yosys/builder banks, Docker/act, the host
  replica or its self-test, hardware, or Verilator. Nothing in this PR needed
  Verilator, so the scoped Verilator 5.050 binary was not used and its
  identity was not checked.
- **Pending manager banks:** the manager's source static/builder and native
  banks for this head were still running. I neither claim nor infer their
  results.
- **No hardware proof:** physical calibration is NOT RUN, and field skips are
  not hardware proof.
- **Final candidate not built:** the final current-dev candidate (source base
  `483a133e`, live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2`) was not
  built. That is the manager's merge-turn duty.
- **Locales:** disposable glibc 2.44 `localedef` outputs for Latin-1, Big5,
  Big5-HKSCS, JOHAB and cp932. JOHAB was compiled with `-c` (exit 1 with
  warnings), and Python's `johab` codec was verified in use. Strict UTF-8 used
  the installed `en_US.utf8`.
- **Tooling:** only Linux, Python 3.14.7 and Git 2.55.0 were exercised.
- **Bounded probes:** the mutation sweep is the listed 24 probes (23 mutants
  plus the control), not exhaustive. Alignment probes use small repetitive
  alphabets and are bounded evidence, not a proof.
- **Not read:** another reviewer's current-round report.

## Pending manager duties

- **Publish** this report and the listed receipts.
- **File new Issues** for O-1 (still unfiled since R244-1) and O-2.
  Optionally route S-1..S-3 to the lane.
- **Before merge,** all of these remain required:
  - the manager's complete source banks at this head;
  - the trusted replica and exact-head hosted acceptance;
  - the second independent (internal) positive with its own five-lens ledger
    at this head;
  - final current-dev candidate validation (live dev `574c29fa`);
  - explicit maintainer merge authorization, post-merge containment, and
    Closed/Done.

## Reproduction (paths relative to this packet; `<clone>` = exact-head checkout)

- **Sources:** `git -C <clone> archive <rev> scripts | tar -x -C scratch/src/<head|prev|base>`
  for `bb4be4d3`, `4671e582` and `483a133e`.
- **Locales:** `localedef --no-archive -c -i <src> -f <charmap> scratch/locales/<src>.<charmap>`
  for `en_US`/ISO-8859-1, `zh_TW`/BIG5, `zh_HK`/BIG5-HKSCS, `ko_KR`/JOHAB and
  `ja_JP`/WINDOWS-31J.
- **Codec probe:** `PROBE_SCRATCH=scratch/probe-work python3 -B scripts/probe_codec.py --driver head scratch/src/head/scripts scratch/locales receipts/probe-codec/head.json`
  (repeat with `prev`).
- **Parent locales:** `scripts/parent_selftest.sh <label> <clone>/scripts/check_merge_containment.py scratch/locales <outdir>`.
- **Mutations:** `python3 -B scripts/probe_mutants.py scratch/src/head/scripts scratch/mut <out.json> 8 [PATH]`.
  Optional environment: `ONLY=...` selects mutants; `PARENT=ascii` uses an
  ASCII parent.
- **Ref names:** `python3 -B scripts/probe_refs.py scratch/src/<v>/scripts scratch/locales <scratch>`.
- **Hostile configuration:** `python3 -B scripts/probe_config.py scratch/src/head/scripts <scratch> <out.json>`,
  run with `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`.
- **Alignment:**
  - `python3 -B scripts/probe_merge_alignment.py 40000 200000 8 scratch/align <out> v2`
  - `... 40000 100000 8 scratch/align <out> v1`
  - `python3 -B scripts/probe_revert_distance.py 8000 <seed> <gap> scratch/align <out>`
- **Subdirectory:** `scripts/probe_subdir.sh <checker> <workdir>`.
- **Codec survey:** `python3 -B scripts/find_lossy_codecs.py`.
- **Integrity:** `scripts/integrity.sh <clone> <out>`.

## Final integrity

`receipts/integrity-before.txt` and `receipts/integrity-after.txt` are
byte-identical:

- HEAD `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34`, tree `ab96af33...`.
- Index SHA-256 `ef0d3c61...`.
- Empty porcelain status, including ignored files.
- All 861 tracked entries were re-hashed from the worktree: 857 blobs match
  their committed object IDs and executable bits, 0 mismatches. The index
  equals HEAD.
- Gitlinks: `gptp-processor` `c1b61743`, `protocol-processor` `424c688f` and
  `third_party/verilog-axis` `48ff7a7e` are checked out at their pins with
  clean status. The optional `external` submodule is uninitialised, as at
  start.

A bytecode cache created by my first self-test run was removed. All fixtures,
source copies, locales and the PR62 clone (a local clone of the gPTP
submodule's objects, read-only use) live under `scratch/`, which is not
published.

R244-2 FINISHED
