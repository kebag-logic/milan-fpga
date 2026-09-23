[R228] POSITIVE - exact head 50c0d00ac3e7b7aa319ba4eab995d7e12b89149e

External independent review, round R228-5: composition acceptance for issue #504 / PR #521.

- **Candidate.** `50c0d00ac3e7b7aa319ba4eab995d7e12b89149e`, tree `4819081971902d71acba2948e659e9658b3fb977`.
- **Candidate parents.** First: `18271bebbd1a4abf2e32e7783477573114e2a5fa`, the #523 merge-train candidate. Second: the PR source head `4876423d4cf8e89b820c56f8339f230abefb4827`.
- **Candidate base parents.** Live `dev` `ede8d48ecd7c7f589a14b957951f040d92c99c70` and the #523 head `015edd9ab2248289ff000f6ef14890be1812ba7b`.
- **PR merge base** against the candidate base: `574c29fa111c74e5e5ed63e4670aff1f492e28e2`, which is unique.

The review clone was only read. Every probe and gate run that could write ran in disposable copies under `scratch/`. The clone is byte- and mode-exact before and after, over 872 tracked blobs. Its index equals HEAD with no flags, its status is clean including ignored files, and the three required gitlinks are checked out (`receipts/integrity-initial.json`, `receipts/integrity-final.json`).

## Verdict summary

- **No open BLOCKER, MAJOR or MINOR finding at this head.** All five lenses are CLEAN.
- **The composition is exact in both directions.** `git merge-tree --write-tree 18271beb 4876423d` reproduces tree `48190819` with exit 0. Two patch-id comparisons are EQUAL (`receipts/composition-scope.txt`):
  - the candidate adds exactly the predecessor's patch (`574c29fa..18271beb`) to the PR head;
  - it adds exactly the PR's patch (`574c29fa..4876423d`) to the predecessor.
- **Two files are changed by both sides**, not the one named in the dispatch hint:
  - `docs/testing/CI_WORKFLOWS.md`;
  - `scripts/check_baremetal_only.py`.

  Both auto-merge in disjoint regions, and each is re-gated here.
- **The hint's `sw/builder/test_builder.py` was checked.**
  - No predecessor commit in `574c29fa..18271beb` touches it.
  - Its candidate blob `408e8790` is the PR head's.
  - The earlier dev delta on that file, `099e1911` from `52711029..574c29fa`, was merged into the lane before this round. Its postimage is present verbatim at the candidate (reverse-apply check exit 0).
  - The one semantic read that crosses sides is its gate 20a row over the predecessor-changed `syn/yosys/run.sh`. That row passes on the candidate and fails when the include dir is dropped.
- **Both lanes' controls run in the composed tree, and the counts add exactly** (`receipts/compare-sides.log`):

  | Measure | Merge base | Predecessor | PR head | Candidate |
  |---|---|---|---|---|
  | Bare-metal scope files | 831 | 843 (+12) | 834 (+3) | 846 |
  | Bare-metal self-test arms | 342 | 354 (+12) | 365 (+23) | 377 |
  | `ci_events` contract items | 1589 | 1589 | 1631 (+42) | 1631 |
  | `ci_events` self-test arms | 2135 | 2135 | 2183 | 2183 |

  Removing any one side's file-pinned mask from the merged tables makes `--check` refuse that side's file: 4/4 KILLED.
- **Gate 1b on the candidate**, scoped Verilator 5.050, SDK installed from the pinned archive by the candidate's own installer:
  - mapped: 217/217 hostile controls, 17/17 and 4/4 positives, 46/46 RTL variants, 0 NOT RUN, 235 firmware compiles;
  - absent: 182/182, 17/17 and 4/4, 46/46, exactly 1 explicit NOT RUN, 0 compiles.

  These are the same counts as the source head.
- **One optional suggestion, R228-S9 (Docs).** It is pre-existing at the reviewed source head and not introduced by the composition.

## Reconstruction

I read these in the contract's order:

1. `AGENTS.md`, `CONTRIBUTING.md` sections 2-3 and 6, and `docs/README.md`.
2. Issue #504: its body, frozen acceptance 1-5, scope and dependencies.
3. The #504 thread: decisions 5771447690, 5771915061 and 5778746031, the correction assignments 5789172582, 5790944031 and 5793839488, and the author statements.
4. The authorities named there: `docs/testing/CI_WORKFLOWS.md`, `docs/integration/BAREMETAL_FIRMWARE.md`, the workflows, `scripts/ci_events.py` and `scripts/check_baremetal_only.py`.
5. `git diff 18271beb..50c0d00a` (10 files, +1673/-67), the predecessor side `574c29fa..18271beb` (29 files), and the history of both sides.
6. The manager's public source evidence under `review-evidence/504-r1/` at `ecf88577`, for its command bank only. I did not open its `reviews/` directory.
7. Exact-head hosted check runs, read-only.

I read no private author material, lane scratchpad or management workspace.

**Independence.** Everything before the prior-findings section was measured before I read any review report on PR #521:

- the gate bank and all probes;
- both gate 1b runs;
- the hosted reads;
- my own pass over the installer, the gate helper and the builder diff outline.

The #504 thread itself names earlier findings in its assignment comments. I read it as the reconstruction order requires.

## Composition scope and semantic interactions

Receipt: `receipts/composition-scope.txt`.

| Interaction | Sides | Gate on the candidate | Result |
|---|---|---|---|
| Mask tables and self-test groups in `check_baremetal_only.py` | #523 adds `HOST_RUNTIME_MASKS` for `owned_process.py` and `process_test_support.py`, plus an arm group. The PR adds `TERM_MASKS` for the installer and its fixture, plus host-tooling arms | `--check`, `--selftest`, and mask-removal probes (`receipts/probe-masks.log`) | 0 findings over 846 files; 377 arms; 4/4 KILLED |
| Policy prose in `CI_WORKFLOWS.md` | #520 extends the Yosys result-cache key sentence and adds the ROM-bundle paragraph (`:225-226`, `:245-257`). The PR adds its paragraphs in the Elaboration section (`:1085-1156`) | `ci_events.py --check` reads this page as its policy. `docs_check`, TOC, anchors, doc style, doc paths and em-dash also run | all exit 0; em-dash finds 0 over 188 added lines against the parent and 0 over 297 against live `dev` |
| Workflow pins | The PR's `ci_events.py` pins `docs-check` at 47 steps and `elaborate` at 20. #522 changed only a comment in `rtl.yml`, and neither predecessor touched `docs.yml` or `elaborate.yml` | `ci_events.py --check` and `--selftest` | 1631 items, 2183 arms |
| Builder read of a predecessor file | `test_builder.py` gate 20a (PR head blob) reads `syn/yosys/run.sh` INCDIRS (#522) | Gate 20a alone, in a candidate copy (`receipts/probe-gate20a-*.log`) | PASS, 4 consumers; REFUSED when `$R/hdl/common/csr` is dropped |
| Shared ratchet budgets | Both lanes add Python and shell | Python and shell idiom, fail-fast, test-evidence, naming, TODO and hygiene gates at four revisions (`receipts/compare-ratchets.log`) | Identical counts at all four revisions; no budget consumed by either side |
| Sweep and shape gates next to the changed `docs-check` | #523 changed `run_all_suites.sh` | Sweep shape, deploy shape, wire-accountability and shard self-tests (`receipts/extra/`) | all exit 0 |
| RTL, firmware and pins | none | `git diff 574c29fa..50c0d00a -- hdl sw/firmware sw/litex configs`; gitlinks | 0 paths; gitlinks identical |

## Findings

None open at this head.

### R228-S9 SUGGESTION - Docs - the testing guide narrates the elaboration job without the SDK steps

- **Where.** `docs/testing/TESTING.md:899-906` says `elaborate.yml` installs LiteX, runs the patch series, "and then runs `sw/builder/test_builder.py --require-elaboration`".
- **Evidence.** At this head the job also restores and verifies the pinned RV32 SDK. It then calls `--require-elaboration --require-rv32` (`.github/workflows/elaborate.yml:242-260`). The authoritative CI page states this (`docs/testing/CI_WORKFLOWS.md:1085-1086`, `:1121-1122`).
- **Provenance.** These lines are byte-identical at `574c29fa`, `4876423d`, `18271beb` and this head. Neither side of the composition wrote them, so this is not a composition defect.
- **Impact.** The statement is incomplete, not false. A reader following the guide learns nothing about the RV32 requirement. It does not change a gate.
- **Suggested outcome.** Optional: name the SDK step and `--require-rv32` there, or link the CI page's paragraph.
- **Verification.** Read the sentence against the job's step list.

## Per-lens results at this head

```text
[R228] PASS Conformance - receipts/gate1b-sdk.log, gate1b-absent.log, gate1b-audit-summary.jsonl, sdk-install-*.log, gates/G05-G06, hosted-rv32-steps-4876423d.txt - acceptance 2, 3 and 5 re-measured on the composed tree: 217/217 hostile controls including the whole-firmware, conditional/splice and resolved-store classes, 17/17 and 4/4, 46/46, 0 NOT RUN, 242 audited invocations with 0 argument tails changed and 120 rv32imafd census assemblies; absent 182/182 with 1 explicit NOT RUN and 0 compiles; residual unchanged (parse_u64 through __errno_location x1). For acceptance 4, the workflow integrity checks pass on the candidate; hosted and trusted-replica acceptance are manager-owned (limits). The composition touches this lens only through the CI policy page and the scope gate, both re-gated clean.
[R228] PASS RTL - receipts/composition-scope.txt (0 paths in hdl, sw/firmware, sw/litex or configs across 574c29fa..50c0d00a and 4876423d..50c0d00a; gitlinks identical); receipts/gate1b-*.log (46/46 real option-on RTL variants elaborated with scoped Verilator 5.050, wrapper sha256 905795b9...e92f, in both modes); receipts/probe-gate20a-*.log (the builder and Yosys include-dir contract holds across sides). The composition does not touch RTL scope; RTL content is covered by the source rounds R228-4 and R227-4 at 4876423d.
[R228] PASS Robustness - scripts/check_baremetal_only.py at the candidate; receipts/probe-masks.log; receipts/gates/G04; receipts/sdk-*.log - both lanes' mask boundaries are enforced together: #523's wrong-context, second-path, same-line, wrong-file and product-file arms and the PR's wrong-file, second-term and boundary arms all run (377); removing any one mask is refused on its own file. The candidate installer's fresh install (13.07 s), verified cache hit (0.81 s) and verify-only all exit 0 from the pinned archive (102,597,892 bytes, sha256 d42680e9...b78f). The compiler-absent mode fails closed under --require-rv32 (G35).
[R228] PASS Tests - receipts/compare-sides.log; receipts/gates/results.json (38/38 exit 0); receipts/gate1b-*.log; receipts/probe-*.log - both lanes' self-tests execute in the composed tree with additive counts; the gates reading the overlap files are failure-sensitive to each side's content (4/4 mask probes, gate 20a include-dir probe); the installer self-test (25 tests), the gate helper self-test, shape self-tests and gate 1b in both modes pass on the candidate.
[R228] PASS Docs - docs/testing/CI_WORKFLOWS.md:225-226 and :245-257 (#520) and :1085-1156 (#504), in separate sections of the merged page; receipts/gates/G08-G24 - docs_check 0 findings over 164 md files, TOC 106 pages, 147 cross-page anchors reproduced, doc style, 832 cited paths, feature status 0, em-dash 0 against 18271beb and 0 against ede8d48e; the only Docs note is the optional R228-S9, which predates the composition.
```

## Reviewer-owned lens ledger

| lens | status | composition touches its scope | examined artifacts | covering round | exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes: the CI policy page and the scope gate | Acceptance 1-5 against the candidate's gate 1b in both modes, the audit summary, the SDK logs, `ci_events` check and self-test, and the source-head hosted RV32 steps | R228-5 | `50c0d00ac3e7b7aa319ba4eab995d7e12b89149e` |
| RTL | CLEAN | No: 0 RTL, firmware or LiteX paths; gitlinks identical | The scope receipt, 46/46 RTL variants with 5.050 in both modes, the gate 20a interface probe | Source rounds R228-4 and R227-4 for RTL content; R228-5 re-check | `4876423d4cf8e89b820c56f8339f230abefb4827`, an ancestor with nothing in RTL scope changed since; re-check at `50c0d00ac3e7b7aa319ba4eab995d7e12b89149e` |
| Robustness | CLEAN | Yes: the merged mask boundaries | Merged mask tables, 377 arms, 4 mask-removal probes, installer fresh, cache-hit and verify-only runs | R228-5 | `50c0d00ac3e7b7aa319ba4eab995d7e12b89149e` |
| Tests | CLEAN | Yes: both lanes' self-tests in the merged gate | Additive counts at 4 revisions, the 38-command bank, probes, both gate 1b modes | R228-5 | `50c0d00ac3e7b7aa319ba4eab995d7e12b89149e` |
| Docs | CLEAN | Yes: the merged `CI_WORKFLOWS.md` | Section placement, docs, TOC, anchor, style, path, feature-status and em-dash gates (parent and live dev); R228-S9 is optional | R228-5 | `50c0d00ac3e7b7aa319ba4eab995d7e12b89149e` |

## Prior public review findings on this PR, at this head

I read these only after the verdict, the findings, the per-lens lines and the ledger above were written.

The candidate carries every PR artifact byte-identical to `4876423d`:

- the installer and its self-test;
- both workflows and `ci_events.py`;
- the gate helper and `test_builder.py`;
- `BAREMETAL_FIRMWARE.md`.

The two merged files differ from the PR head only by the predecessor's patch.

| Finding | Status at `50c0d00a` | Evidence |
|---|---|---|
| R228-1 F1 MAJOR (hosted FP stores bypass the resolver) | RESOLVED, still resolved | Resolver byte-identical. The candidate's mapped gate 1b refuses 217/217. Its log reports the compiled store-class mutants reaching the resolver as `fsw`, `fsd`, `amoswap.w`, `amoor.w` and `sc.w`, each refused on the resolved address (`receipts/gate1b-sdk.log`) |
| R228-1 F2 MAJOR (download-path digest check has no failing control) | RESOLVED, still resolved | Installer and self-test byte-identical; 25 tests pass on the candidate (`receipts/gates/G34`) |
| R228-1 F3 MINOR (receipt bindings not failure-sensitive) | RESOLVED, still resolved | Same artifacts and self-test |
| R228-1 S1 | TAKEN | Its controls are in the passing self-test |
| R228-S2, R228-S3 (Robustness: relocation proof, download retry and deadline) | RETAINED, optional | Installer unchanged; the installer reports its own digest `ffcc5433...` |
| R227-1 | POSITIVE at `3d90958f`; no open finding recorded | n/a |
| R227-2 F1 MINOR, F2 MINOR; R227-2 S1 | RESOLVED or TAKEN, still so | Resolver and controls byte-identical. The candidate gate prints "15 rewrites of a parked word ... while 5 stores ... left exactly theirs" |
| R228-2 F4 MINOR, F5 MINOR; R228-2 S4 | RESOLVED or TAKEN, still so | Controls and firmware page byte-identical |
| R227-3 MINOR Tests and R228-3 F6 MINOR Tests (overlap low boundary) | RESOLVED at `4876423d`, still resolved | `test_builder.py` byte-identical; the stale and kept probes run in the candidate's gate 1b, both modes |
| R227-3 S1 (M16, M17), R228-S8, R227-4 S1 (companion high boundary) | RETAINED, optional | Code unchanged |
| R227-3 S2, R228-S5, R228-S6, R228-S7, R227-4 S2 (symbol-addend aliasing) | RETAINED, optional | Code and page unchanged |
| R227-2 OBS-1, R227-3 O1, R228-2 O1 (called-function, call-crossing, numeric-stack and sub-word frame-load shapes) | Out of scope, pre-existing, documented on the page | Unchanged; see pending duties |
| R227-4 and R228-4 | POSITIVE at `4876423d` | Source reviews; this round adds composition only |

## Executions on the candidate

All of these ran in the foreground. Gates that write ran in a disposable shared clone of the candidate, with the three submodules initialised from the review clone's own module repositories.

| Run | Result | Receipt |
|---|---|---|
| 38-command composition bank: merge-tree, diff check, bare-metal, `ci_events`, `ci_scope`, docs, TOC and anchors, em-dash (parent and live dev), style, paths, archive, hygiene, TODO, feature status, submodule docs, the idiom and ratchet gates, `pp_srcs`, installer and helper self-tests, compile | 38/38 exit 0, Python 3.14.7 | `receipts/gates/` |
| Four-revision comparison: bare-metal and `ci_events` | additive, all exit 0 | `receipts/compare-sides.log` |
| Four-revision ratchet comparison | identical counts, all exit 0 | `receipts/compare-ratchets.log` |
| Mask-removal probes | 4/4 KILLED | `receipts/probe-masks.log` |
| Gate 20a alone, pristine and without the csr include dir | PASS; REFUSED | `receipts/probe-gate20a-*.log` |
| SDK: fresh install, cache hit, verify-only | exit 0; GCC 14.3.0, `riscv32-buildroot-linux-gnu` | `receipts/sdk-*.log`, `receipts/sdk-archive-sha256.txt` |
| Gate 1b, SDK mapped (5 m 43 s) | PASS: 217/217, 17/17, 4/4, 46/46, 0 NOT RUN, 235 compiles | `receipts/gate1b-sdk.log`, `receipts/gate1b-sdk-argv.jsonl` |
| Gate 1b, absent (4 m 36 s) | PASS: 182/182, 17/17, 4/4, 46/46, 1 NOT RUN, 0 compiles | `receipts/gate1b-absent.log`, `receipts/gate1b-absent-argv.jsonl` |
| Audit summary | mapped: 242 invocations, 0 tails changed, 120 rv32imafd assemblies. Absent: 3 cross tools hidden, 0 compiles | `receipts/gate1b-audit-summary.jsonl` |
| Sweep, deploy, wire and shard self-tests | 4/4 exit 0 | `receipts/extra/` |
| Hosted, read-only | Candidate: no runs, since the commit is not on the remote. PR head `4876423d`: 21 success, 1 skipped (physical gPTP, nightly and manual only, not executed). The RV32 cache, install, absent-control and builder steps executed with success in both `docs-check` and `elaborate` | `receipts/hosted-*.txt` |
| Clone integrity, before and after | PASS, 872 blobs | `receipts/integrity-*.json` |

**Tool identity.** Scoped Verilator 5.050 (wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`) was first on `PATH` for both gate 1b runs. The pinned archive is 102,597,892 bytes with the installer's pinned SHA256.

**Path hygiene.** Receipts had local paths replaced by `$PACKET`, `$HOME` and `$SDK_ARCHIVE_DIR`. The digests of the original bytes are in `receipts/pre-neutralization-digests.sha256`. JSON validity and the audit summary were re-verified after replacement.

## Real limits

- I did not run the full parent, PP, gPTP, Yosys or builder banks, the trusted local replica, or any hosted job. Gate 1b and gate 20a are focused builder gates, not the builder bank.
- **The candidate has no exact-head hosted evidence.** The hosted runs I read are for the source head `4876423d`. A tree-equal final candidate still needs its own hosted and replica acceptance.
- **This candidate is `dev` `ede8d48e` plus #523 plus #504.** If `dev` or the queue moves before the merge turn, this verdict covers only this tree.
- The SDK-mapped run is local compatibility evidence through an argv[0] mapping, not hosted selector adoption.
- The public source evidence I found for the manager banks is the `source-r2` command list. I relied on it only to choose which gates read the overlap files. I claim nothing about banks I did not see.
- Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Publish this report and its manifest-listed receipts.
- Hosted and trusted-replica acceptance at the final candidate.
- Obtain the internal composition verdict, if one is scheduled.
- At the merge turn, with maintainer authorization:
  - build the final current-`dev` candidate and confirm its tree equals `48190819`, or re-gate it;
  - post-merge containment, the issue close, and the Done readback.
- A public Issue before #408/#409 retire any text rule onto the census. It should cover the shapes the firmware page lists as not observed:
  - a callee's store through a handed pointer;
  - a callee's write into its caller's frame;
  - a numeric store that reaches the stack;
  - a sub-word frame-slot load.
- Optionally, R228-S9.

## Reproduction

`$PACKET` is this packet, `$CLONE` a clean candidate clone, `$PINNED_TOOLS` the directory holding the scoped Verilator 5.050 wrapper, and `$ARCHIVE` the pinned SDK archive.

```sh
CLONE="$CLONE" python3 -B scripts/integrity.py initial
CLONE="$CLONE" OUT="$PACKET/receipts/gates" JOBS=4 python3 -B scripts/run_gates.py
bash scripts/composition_scope.sh "$CLONE"
git clone -q --shared --no-checkout "$CLONE" "$PACKET/scratch/cand" && git -C "$PACKET/scratch/cand" checkout -q 50c0d00ac3e7b7aa319ba4eab995d7e12b89149e
# initialise third_party/verilog-axis protocol-processor gptp-processor in the copy from local module repositories
bash scripts/compare_sides.sh "$PACKET/scratch/cand"
bash scripts/compare_ratchets.sh "$PACKET/scratch/cand"
(cd "$PACKET/scratch/cand" && python3 -B "$PACKET/scripts/probe_masks.py")
(cd "$PACKET/scratch/cand" && python3 -B "$PACKET/scripts/probe_gate20a.py" pristine)
(cd "$PACKET/scratch/cand" && python3 -B "$PACKET/scripts/probe_gate20a.py" drop-incdir; git checkout -- syn/yosys/run.sh)
(cd "$PACKET/scratch/cand" && python3 -B scripts/ci_rv32_sdk.py --destination "$PACKET/scratch/sdk/host" --archive "$ARCHIVE")
(cd "$PACKET/scratch/cand" && PATH="$PINNED_TOOLS:$PATH" python3 -B -u sw/builder/test_firmware_compiler.py --sdk-destination "$PACKET/scratch/sdk/host" --audit "$PACKET/receipts/gate1b-sdk-argv.jsonl")
(cd "$PACKET/scratch/cand" && PATH="$PINNED_TOOLS:$PATH" python3 -B -u sw/builder/test_firmware_compiler.py --absent --audit "$PACKET/receipts/gate1b-absent-argv.jsonl")
python3 -B scripts/audit_summary.py receipts/gate1b-sdk-argv.jsonl receipts/gate1b-absent-argv.jsonl
CLONE="$CLONE" python3 -B scripts/integrity.py final
```

R228-5 FINISHED
