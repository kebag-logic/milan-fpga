[R251] POSITIVE - exact head bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34

Round R251-4: cleared-context internal review of issue #423 / PR #519.

| Item | Value |
|---|---|
| Exact head | `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34` |
| Tree | `ab96af335f1428770a1a96c0345a9f55278ad25b` |
| Source base | `483a133ed08867ea0d300d2b4a027b5b48a4282f` (live dev, an ancestor of the head through merge `e1e0f979`) |
| Frozen contract | [Decision 5777210218](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218); issue AC1-AC4 |
| Focus | Correction round for R244-1 (A MAJOR, B/C/D MINOR); F1/F2/F3 re-checked |

I applied all five lenses independently at this head. No BLOCKER, MAJOR or MINOR is open. Every lens is clean.

- Three SUGGESTIONs are recorded; they do not affect coverage.
- Two pre-existing, out-of-scope observations need their own Issues.
- The base and this head behave identically on both of them.

## Independence and reconstruction

- **Reading order:**
  1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
  2. The issue body, the manager and author comments, and the frozen decision.
  3. REQ-VER-04 as cited, then CONTRIBUTING 2.1 step 7.
  4. `git diff 483a133e..bb4be4d3` and its history (four commits after the reviewed head, including the dev merge).
  5. The public A186 packet: HANDOFF, gate summary and gate command list.
- **Independent pass first.** My verdict and ledger were written before any prior review finding on the PR was read:
  - file `receipts/verdict-before-prior-findings.md`;
  - sha256 `42314d89065e1ef22b6865a942c4b1a894ff8a525ae513067a0ba165774650ba`;
  - written 2026-09-23T07:11:26Z.
- **Reconciliation afterwards.** I then read the findings and dispositions of R243-1, R251-1, R251-2, R251-3 and R244-1. The published F1 reproducer script was fetched only after that verdict file existed. Reconciliation changed no severity and no lens state.
- **S3's provenance.** S3 was added after the draft. It comes from my own mutant S18, which I measured before the draft; I confirmed its effect on a real history afterwards.
- **Not read:** private author material, lane scratchpads and other reviewers' evidence folders.

## Prior findings at this head

| Finding (original severity; lenses) | Disposition | Evidence at this head |
|---|---|---|
| R244-A (MAJOR; Conformance, RTL, Robustness, Tests, Docs) | **RESOLVED** | See the R244-A note below the table. |
| R244-B (MINOR; Tests, Robustness, Conformance) | **RESOLVED** | See the R244-B note below the table. |
| R244-C (MINOR; Tests) | **RESOLVED** | See the R244-C note below the table. |
| R244-D (MINOR; Robustness, Tests) | **RESOLVED** | See the R244-D note below the table. |
| R244-1 O-1 (observation) | **RETAINED** as out-of-scope observation O1 | Reproduced at base and head. No Issue exists yet. |
| F1 (R251-1, BLOCKER; Conformance, Robustness) | **RESOLVED, still holds** | Published F1 reproducer at this head (`receipts/f1-published-probe/`): linear `STRANDED`/1 and merge `UNKNOWN`/1 naming `'\xc3\xa9.txt'`, in UTF-8 and Latin-1. The locale probe's `latin1` rows pass. Enumerated-bytes, postimage, entry and patch-byte controls run in every child. |
| F2 (R251-1, MAJOR; Tests, Conformance) | **RESOLVED, still holds** | The default owner runs five fresh children plus the in-process Big5 control, with byte-defined names, aliases, positives and negatives. All transport restorations are killed (see Tests). |
| F3 (R251-2, MINOR; Tests, Robustness, Conformance) | **RESOLVED, still holds** | Latin-1 parent 678/678. The byte-defined `raw-\xff` fixture and exact path assertion are retained (`merge_containment_selftest_retention.py:35`, `:84-87`, `:131-135`). The label is now derived from bytes alone. |
| R243-1, R251-3 | No findings raised | n/a |

**R244-A.** Git-derived filenames and patch text now travel as bytes:

- `merge_containment_git.py:19-30`;
- `check_merge_containment.py:147-190`, `:446-469` and `:507-515`;
- `merge_containment_replay.py:55-71` and `:109-129`.

Other decoded output that does not round-trip is refused (`merge_containment_git.py:33-48`).

- **CLI probe.** My probe over 8 real locales passes 84/84 at this head (`receipts/locale-probe-bb4be4d3.jsonl`). It covers four non-injective codecs: Big5, Big5-HKSCS, JOHAB and Windows-31J. On those four codecs, the reviewed head `4671e582` gives 8 false `contained`/0 results: `linear-missing` and `merge-reverted` on each.
- **Mutants.** A1-A10 and A2b-A4b are all killed. All transport mutants are also killed on a host without `locale` or `localedef`.
- **Documentation.** The docstrings restore the rc/stdout contract. The CONTRIBUTING claims at `:242-251` hold as measured.

**R244-B.** Source copies in the mutation harness are now bytes.

- **Parents.** An ASCII parent passes 678/678. UTF-8 and Latin-1 parents also pass 678/678.
- **Restoration.** Restoring decoded copies (mutant B1) crashes an ASCII parent with the original `UnicodeDecodeError` on byte 0xc2 (`receipts/mutants-ascii.jsonl`).
- **Suggestion.** No default-run control guards this fix; see S1.

**R244-C.** Each named guard mutant is killed by a named verdict-and-exit control:

| Mutant | Killing control |
|---|---|
| C1, `--no-renames` dropped | `retention-hostile-rename-undone` |
| C2, `--ignore-submodules=none` dropped | `retention-hostile-gitlink-reset` |
| C3, single merge base weakened | `retention-merge-base-two-real-bases`, an injection of real object IDs |
| C4, ancestor type rule removed | `retention-symlink-ancestor-clean-merge` |
| C5, replay distinctness removed | `retention-distinct-linear` and `retention-distinct-merge` |

**R244-D.** My four-target report through a real stdout is complete in all 8 locales (`receipts/stdout-probe-bb4be4d3.jsonl`):

- the report order is `contained`, `STRANDED`, `UNKNOWN`, `contained`;
- both summaries are present, exit is 1, stderr is empty, and the output is ASCII only;
- every name is quoted.

The reviewed head `4671e582` truncates under every strict stdout. Even in UTF-8 mode, raw newline-bearing names split its report lines. Mutants A7, A8 and A9 are killed by the in-suite stdout and label controls.

## Findings at this head

None at BLOCKER, MAJOR or MINOR.

Suggestions are optional and do not affect coverage.

```text
[R251] SUGGESTION Tests - scripts/merge_containment_selftest_mutations.py:45-50; PR #519 body "Validation" - S1: the ASCII-parent source-copy fix has no default-run control
Requirement/evidence: restoring locale-decoded copies (mutant B1) passes the
  default self-test under a UTF-8 parent (rc 0, receipts/mutants-default.jsonl).
  It is killed only when the parent itself is ASCII with locale coercion and
  UTF-8 mode disabled. The fresh ASCII child runs the locale controls, not the
  mutation harness. The PR body's list of removals that "fail the self-test"
  includes "the byte source copies", which holds only under the ASCII-parent
  command it shows.
Impact: a later text-mode copy passes CI and fails only for an ASCII parent.
  The failure is a crash that fails closed, never a containment error.
Suggested outcome: run one mutation replica inside the existing ASCII child, or
  state in the PR text that this control needs the ASCII-parent invocation.
Verification: mutant B1 fails the default self-test under a UTF-8 parent.
```

```text
[R251] SUGGESTION Tests, Docs - scripts/run_all_suites.sh:249-261; CONTRIBUTING.md:249-251 - S2: NOT RUN locale notices are invisible in the suite sweep
Requirement/evidence: the sweep captures the containment self-test output and
  prints it only on a nonzero status. The hosted rtl-full log at this head
  (run 35825057127) shows no locale line. Without locale data the self-test
  passes 507/507 with three NOT RUN notices
  (receipts/mutants-nolocale.jsonl, control).
Impact: CI evidence cannot show whether the Latin-1, Big5 and strict UTF-8
  children ran. Protection is kept: the in-process Big5 control and the
  UTF-8/ASCII children kill every transport mutant without locale data.
Suggested outcome: print NOT RUN lines from the sweep on success.
Verification: a sweep on a host without localedef shows the three notices.
```

```text
[R251] SUGGESTION Tests, Conformance - scripts/check_merge_containment.py:560-571 - S3: arm order has no killing control
Requirement/evidence: the decision says to preserve the existing arms "and
  their order". It also says the new arm runs only after every existing arm
  declines. The code satisfies both. Moving the fallback ahead of the
  touched-path arm (mutant S18) passes the default self-test. On a real
  redundant-merge history with full replay and no net tree change, the head
  says contained/0 and the mutant says UNKNOWN/1
  (scripts/arm_order_probe.sh, receipts/arm-order-probe.txt).
Impact: only the fail-closed direction. A reorder turns existing proofs into
  UNKNOWN.
Suggested outcome: add that history as a default-self-test control.
Verification: mutant S18 fails the default self-test.
```

## Out-of-scope observations (pre-existing; base `483a133e` behaves identically)

These are not findings against this head. Each needs its own Issue, per AGENTS section 4.

**O1: subdirectory invocation** (R244-1 O-1, retained). Evidence: `receipts/edge-probe-{bb4be4d3,483a133e}.jsonl`.

- **Cause.** `check_merge_containment.py:183-184` and `:468-469` pass root-relative names as cwd-relative literal pathspecs.
- **Measured from `sub/`.** Both fixtures read `contained`/0 from the touched-path arm, before the new fallback runs:
  - a linear branch whose `sub/file` edit never landed;
  - a replay whose `sub/file` edit the tip reverted.
- **Measured from the root.** The same fixtures give `STRANDED`/1 and `UNKNOWN`/1.
- **Related survivor.** `--full-tree` at `merge_containment_replay.py:57-58` (surviving mutant S02) cannot be observed until O1 is fixed. The follow-up should control both.
- **Tracking.** An issue search on 2026-09-23 found no Issue for this.

**O2: command-line ref operands under a non-injective codec** (new). Evidence: `receipts/edge-probe-*.jsonl`.

- **Measured.** Under a real `zh_TW.BIG5` locale, operand bytes `a1 fe` resolve as `refs/heads/a2 41`. A stranded branch named with bytes `a1 fe`, beside a contained branch named with bytes `a2 41`, reads `contained`/0. The printed label is `refs/heads/\xa2A`.
- **Controls.** UTF-8 mode gives `STRANDED`/1. The base gives the same false result under Big5.
- **Preconditions.** A non-injective locale, and two branch names that alias under it.
- **Related code.** `check_merge_containment.py:396` treats a non-round-tripping symbolic name as "not a remote". That line is in the same domain.
- **Scope.** This PR's wording and transport cover Git-derived filenames, patches and other Git output. They do not cover command-line operands or GitHub JSON labels, which the author's handoff lists as unmeasured.
- **Required outcome for the follow-up.** An operand that does not round-trip is refused, or is carried as its original bytes.

## Clean-lens evidence

Each clean lens below was applied at this head.

```text
[R251] PASS Conformance - scripts/merge_containment_replay.py:32-153; scripts/check_merge_containment.py:518-580; CONTRIBUTING.md:208-260 - G1/H/T and arm order read clause by clause against decision 5777210218
  G1: exactly one source-only merge, two parents, P2's sole parent is P1,
    tree(M) equals tree(P2).
  H: the existing distinct whitespace-exact helper, unchanged.
  T: one merge base; raw entries on the net-changed paths with renames
    unfolded; identity including absence; the regular-blob and mode rule; a
    conflict-free raw merge-file whose output is byte-identical to the tip;
    every failure UNKNOWN/1.
  Actual gPTP processor PR62: UNKNOWN/1 at f0f1c055 and c1b61743, naming
    'tb/tsngen/mutants.py' and 'tb/verilator/gaskets/mutants.py'.
    PR61: contained/0. The documented raw-diff command reproduces all four
    decision patch hashes (receipts/actual-pr62.txt).
  The 31-case matrix and ten guard mutations run in the default self-test.
  All 145 base arms are present with identical names, descriptions and order
    (receipts/selftest-base-483a133e.log vs receipts/selftest-default.log).
  The R244-A..D required outcomes are met.
```

```text
[R251] PASS RTL - diff 483a133e..bb4be4d3; check_merge_containment.py:83-87, :98-144, :193-230, :422-580; merge_containment_replay.py:25-29; run_all_suites.sh:237-261 - architecture and interface contracts
  No file under hdl/, tb/, syn/, sw/ or .github/ changes.
  Gitlinks are unchanged from the base: gptp-processor c1b61743,
    protocol-processor 424c688f, third_party/verilog-axis 48ff7a7e.
  Exit contract 0/1/2 plus self-test status 3 is unchanged, as is the sweep's
    handling of it.
  RC_LOSSY_OUTPUT (256) fails closed wherever a git_text result feeds a
    containment measurement: each nonzero status becomes UNKNOWN or a refusal.
    The replay module's _measure sites raise. The ref-name lookup at :396
    belongs to O2.
  lint_rtl.py --check: PASS, 90 <= 90, with the identity-checked Verilator
    5.050 wrapper (receipts/gates/lint-rtl-check.out, receipts/env.txt).
```

```text
[R251] PASS Robustness - merge_containment_git.py:19-52; merge_containment_replay.py:55-129; receipts/locale-probe-*.jsonl, stdout-probe-*.jsonl, parents/, mergefile-algo-probe.json - codecs, stdouts, parents, hostile configuration and failure paths
  Locales: 8 real locales, including 4 non-injective codecs, pass 84/84.
  Stdout: the four-target strict-stdout report is complete in all 8.
  Parents: nine parent locales pass the default self-test 678/678.
  Hostile configuration: merge-file ignores a configured diff.algorithm, so
    configuration cannot change T's alignment. core.ignorecase does not affect
    tree pathspecs.
  Failure paths: missing blob, command errors, malformed ls-tree, signals, a
    temporary-storage error and invalid configuration are all UNKNOWN/1.
  O1 and O2 are out-of-scope pre-existing behavior, as recorded above.
```

```text
[R251] PASS Tests - scripts/merge_containment_selftest_{locale,retention,replay,mutations,content}.py; receipts/mutants-{default,ascii,nolocale}.jsonl - 38 single-guard mutants plus a control, each run through the full default self-test
  Kills: 26 are killed under a UTF-8 parent by named cases. B1 is killed under
    an ASCII parent. Every transport mutant is also killed without locale data.
  Harness: no kill came from a collision with the self-test's own mutation
    harness.
  Equivalent survivors under real Git from the repository root:
    S01 (returned-name check; literal exact-byte lookup).
    S03 (conflict-style override; conflicts already fail).
    S05 (--no-ext-diff/--no-textconv on --name-only).
    S06-S08 (OID and record validation of Git's own output).
    S09-S10 (NUL-terminated or empty set; Git always terminates, and an empty
      set still errors).
    S15 (blob kind; implied by the regular modes).
  Survivor that cannot be observed yet: S02 (--full-tree), until O1 is fixed.
  Survivor that only fails closed: S18, see S3.
```

```text
[R251] PASS Docs - CONTRIBUTING.md:208-260; check_merge_containment.py:44-61; merge_containment_git.py:1-52; merge_containment_replay.py:1-8; PR #519 body; #423 REVIEW READY 5789912186 - every claim checked against measurement
  Claims confirmed: Big5 re-encodes a1 fe as a2 41. Five fresh processes run,
    with a real stdout each. NOT RUN supplies no evidence. The documented
    patch-hash command reproduces the hashes.
  No consumer parses the reformatted "paths differing:" note.
  Gates, all rc 0 (receipts/gates/summary.txt): docs_check; check_em_dash
    --base 483a133e (0 findings over 54 added lines) and --selftest;
    check_doc_style; check_doc_paths; gen_toc --check and --verify-anchors;
    check_feature_status; check_py_idiom and --selftest; check_hygiene --check
    and --selftest; check_todo_ownership; git diff --check.
  The PR-body wording is S1, a suggestion only.
```

## Reviewer-owned lens ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Decision 5777210218 vs `merge_containment_replay.py:32-153`, `check_merge_containment.py:518-580`; `CONTRIBUTING.md:208-260`; actual PR62/PR61 at both targets; patch hashes; 145-arm preservation; R244-A..D outcomes | R251-4 | `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34` |
| RTL | CLEAN | Diff scope (no HDL/tb/syn/sw/workflow change); unchanged gitlinks; exit and lossy-status contracts at all `git_text`/`_measure` sites; `run_all_suites.sh:237-261`; `lint_rtl.py --check` 90 <= 90 | R251-4 | `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34` |
| Robustness | CLEAN | Byte transport and T lookups; 8-locale CLI probe (84/84); 4-target strict-stdout probe (8/8); nine parent locales (678/678); hostile merge-file/pathspec configuration; fault paths | R251-4 | `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34` |
| Tests | CLEAN | Default self-test 678/678; 38 mutants plus control in three profiles; survivors characterized; base arms preserved | R251-4 | `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34` |
| Docs | CLEAN | `CONTRIBUTING.md:208-260`, module/transport docstrings, PR body, REVIEW READY; 14 documentation/style gates rc 0 | R251-4 | `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34` |

## Hosted evidence inspected

This section is inspection only; hosted and act acceptance belong to the manager (`receipts/hosted-check-runs-bb4be4d3.tsv`).

- **Required contexts.** All seven succeeded on the exact head: `rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites` and `yosys-portability`.
- **Executed jobs.** Verilator shards 0-4 ran for 5-33 minutes each. Yosys shards 0-3 ran about 30 s each. Both aggregates succeeded after them.
- **Skipped.** Only "Physical gPTP (nightly and manual)" was skipped.

## Real limits

- **Not run by me:** the full parent, PP, gPTP, Yosys and builder banks; Docker/act; host `act_ci` and its self-test; hardware.
- **Manager banks:** the manager's full source static/builder and native banks for this head are still running. They are not claimed or inferred here.
- **Calibration:** physical calibration is NOT RUN, and field skips are not hardware proof.
- **Candidate:** source validation is not the final current-dev candidate (source base `483a133e`, live dev `574c29fa`). That candidate is not examined here.
- **Gate environment:** the focused gates ran in a disposable clone of the exact head. Its three required submodules were initialized from the review clone's pinned checkouts.
  - `receipts/gates/summary.txt` also records the first `py-idiom`, `hygiene` and `todo-ownership` attempts. They correctly refused (rc 2) before submodule initialization, and then passed (rc 0).
- **Codec coverage:** non-injective codecs went through the CLI only for Big5, Big5-HKSCS, JOHAB and Windows-31J, using disposable `localedef` output. A two-byte scan of 15 CJK codecs found no other lossy pair except cp950, which was not run through a locale.
- **Mutation coverage:** it is the 38 listed single-guard mutants. The equivalence of the survivors is argued, not proved.
- **Alignment:** this round did not extend the bounded alignment evidence. T's merge logic is unchanged since `4671e582`, and only its transport changed.
- **Hosted evidence:** check-run metadata and one job log only.
- **O1 and O2:** measured only at the base and at this head.
- **Tools:** Linux x86_64, Git 2.55.0, Python 3.14.7. At most 8 parallel jobs.

## Pending manager duties

- Publish this packet.
- Report the full source static/builder and native bank results at this head.
- Run the trusted local replica at this head and accept the hosted contexts.
- Obtain the external R244 re-review of this head, for the second independent positive.
- Validate the final current-dev candidate (base `483a133e`, live dev `574c29fa`).
- Then carry out the authorized merge, post-merge containment, and Closed/Done.
- File Issues for O1 and O2. S1-S3 are optional.

## Reproduction

Paths are relative to this packet, and `<clone>` is a checkout at the exact head.

1. Build the locales: `sh scripts/mklocales.sh scratch/locales`.
2. Extract the sources for `bb4be4d3`, `4671e582` and `483a133e`:
   `git -C <clone> archive <sha> scripts | tar -x -C scratch/src-<sha8>`
3. Run the parent-locale sweep:
   `scripts/run_parents.sh <clone> scratch/locales receipts/parents`
4. Run the filename and report probes against each extracted source:
   - `python3 scripts/locale_probe.py scratch/src-<sha8>/scripts scratch/lp-<sha8> scratch/locales`
   - `python3 scripts/stdout_probe.py scratch/src-<sha8>/scripts scratch/sp-<sha8> scratch/locales`
5. Run the mutation campaign:
   - First create `scratch/cwd-repo`: `git init`, then commit one file.
   - Then run `python3 scripts/mutate.py scratch/src-bb4be4d3/scripts scratch receipts/mutants-<profile>.jsonl <default|ascii|nolocale> [mutant...]`.
6. Check the actual PR62/PR61 history:
   `sh scripts/actual_pr62.sh scratch/src-<sha8>/scripts <clone of gptp-processor>`
7. Run the edge and arm-order probes:
   - `python3 scripts/edge_probe.py scratch/src-<sha8>/scripts scratch/ep-<sha8> scratch/locales`
   - `sh scripts/arm_order_probe.sh <checker> scratch/armorder`
8. Run the merge-file algorithm probe: `python3 scripts/mergefile_algo_probe.py scratch/mfalgo`
9. Run the published F1 probe:
   `HEAD_SHA=bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34 bash scripts/f1_published_probe_headvar.sh <clone> scratch/f1w receipts/f1-published-probe`
   - It is the published `locale_transport_probe.sh` (sha256 `69808512...`, verified against the public packet's SHA256SUMS).
   - The only edit makes `HEAD_SHA` overridable.
   - Its printed label "head-df53dfa1" is fixed text.
10. Run the gates using the commands in `receipts/gates/summary.txt`, from a clone at the exact head with the three required submodules initialized.
11. Check integrity:
    `python3 scripts/integrity.py <clone> bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34 ab96af335f1428770a1a96c0345a9f55278ad25b`

## Final integrity

`receipts/final-integrity.json` reports ALL_OK (exit 0).

- **HEAD and tree:** HEAD is `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34`, and its tree is `ab96af335f1428770a1a96c0345a9f55278ad25b`.
- **Blobs:** all 857 tracked root blobs match their committed bytes and modes, checked by direct hashing.
- **Index and status:** the index equals HEAD at stage 0, with no assume-unchanged or skip-worktree flag. Porcelain status is empty.
- **Required submodules:** each is a real checkout at its gitlink, with clean status and every tracked file hash-verified.

| Submodule | Revision | Files verified |
|---|---|---|
| `third_party/verilog-axis` | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` | 214 |
| `protocol-processor` | `424c688fa2205b934a7689a58f2aa766420f2326` | 222 |
| `gptp-processor` | `c1b617435824929a790739ea8585c3fe1a328cc0` | 103 |

- **Scope of edits:** no file in the review clone was edited.
- **Where work ran:** all copies, fixtures, locales and mutants were built under `scratch/`, which is never published.

R251-4 FINISHED
