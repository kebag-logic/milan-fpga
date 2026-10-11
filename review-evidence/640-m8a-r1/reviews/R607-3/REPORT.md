[R607] POSITIVE - exact head ce10328c3d89d81509e47836fa4a48b22ecdbc20

External source review, round R607-3, issue #640 / PR #721. Tree `783d10c5ae40dad516d52e1fbf77b0e25680e4a3`. All five lenses were applied. No BLOCKER, MAJOR or MINOR remains in the reviewed delta. One new prose-only RESIDUE is recorded below. This verdict does not approve a merge or establish completion of issue #640.

Process limitation: after the independent diff pass, retrieval of the prior public finding comments also displayed historical report summaries and ledgers before this verdict was written. That exceeded the requested findings-only reading boundary. No concurrent round-3 report, private author material, lane scratchpad or management checkout was consulted. The manager must determine whether this review may count toward the procedural independence bar; the executed evidence remains independently reproducible.

**Scope and reconstruction**

Read AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, REQUIREMENTS.md section 1 and section 8, NFR-SCOUT/NFR-RES-01, the split architecture and memory interfaces, then the requested `e8454e2751d05b02ee8e5a571857589ab358ab86..ce10328c3d89d81509e47836fa4a48b22ecdbc20` diff and history. The independent delta pass preceded the prior finding comments; `independent-pass.txt` records its artifact-level conclusions, not private reasoning.

The [initial assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100371426), [M8a-1 ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101485877), [round-2 scope](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105011666) and [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6107088105) govern acceptance. The firmware allocation is up to 56 RAMB36 equivalents. M8a-1 covers memory layout, instantiation, fit, ledger, named controls and preservation of the all-fabric default. Boot, service, removal of the retained wrapper/DDR3 and integrated route remain M8a-2 after F-INT PR 2. The issue-wide 38,040-LUT target is not claimed by this PR.

The round-3 range contains exactly five descendant commits and eight changed files. `receipts/delta-integrity.log` proves identical Git objects for `hdl/`, `tb/`, `syn/`, `sw/litex/milan_soc.py`, `sw/firmware/`, and all five gitlinks since `76605880a20005cbc2acad1b23ba2ccebde64ca8`. The inherited dev merge is distinguished from this delta. Unchanged all-fabric construction and unchanged mapping inputs preserve the earlier comparison basis; no new default-export or synthesis campaign is claimed here.

**Prior findings: resolved or retained at this head**

The [round-2 internal findings](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6107064124) and [round-2 external finding](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6107065061) were checked against construction and fresh execution.

| Prior ID and lenses | Disposition | Exact-head evidence |
|---|---|---|
| R606-2-F1, BLOCKER; Conformance, Tests, Docs | RESOLVED | `scripts/ci_scope.py:66` registers the page and its classification case; `CI_WORKFLOWS.md:76` names the seventh gate-read page. Isolated `ci_scope.py --selftest` passes and the page alone prints `true`. Hosted classifier steps and `rtl-fast` succeed. |
| R606-2-F2, MAJOR; Tests, Docs | RESOLVED | `test_ctrl_memory.py:639` overrides only firmware make-input generation while retaining SoC headers and real export. Fresh Python 3.12.3 with the pinned, patched stack and PyYAML has no firmware data package. Aggregate 7/7; focused suite 123 checks, 44 mutants. The stage-call mutant fails its stage-size control; the shipping-library mutant fails the no-shipping-firmware check. No SoC kill comes from ImportError. Removing the include hook in a disposable copy makes the baseline fail and all six SoC mutants NOT GRADED. `receipts/grading-control.log` and child log. |
| R607-2-F1, MINOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED | `ctrl_memory.py:246,264` checks continuous file-backed load coverage, including the reset word, before `add_ctrl_memory` can construct ROM. The new rule is registered and documented. The unmodified `probe_load_soc.py` now observes rc 1, named reset refusal, zero Verilog and no init output. Its old defect assertion consequently exits 1; this is the expected disappearance of its reproduction, not a passing script exit. `receipts/load-soc-original.log`; independent acceptance check in `receipts/load-soc-verdict.log`. |
| R606-2-F3, MINOR; Docs | RESOLVED | `MARK_II_AREA_PLAN.md:842,870` and `AREA_BUDGET.md:269,279` use the ruled 56-tile basis and `124 + 6 = 130`, 8.5 over the ceiling. Arithmetic reproduced from current rows in `receipts/evidence-arithmetic.log`. |
| R606-1-R1, RESIDUE; Docs | RESOLVED | Both requested sentences now explicitly include M2's unused +2 allowance, verbatim at `AREA_BUDGET.md:263` and `MARK_II_AREA_PLAN.md:832`. |
| R606-1-F1; Robustness, Tests | RESOLVED, preserved | Writable data in ROM is refused by `writable in rom`; genuine link-script plant and removal mutant run in the passing suite. |
| R606-1-F2 and R607-1-F1; Tests | RESOLVED, preserved | Exact budget boundaries, missing reset section, NOBITS, LMA overlap, decode width, hole width/start and immediate post-error access have effective arms. All corresponding standing mutants fail by named checks. The independent bus scoreboard passes 864 cases through word 65535. The old twelve-mutation driver was not separately rerun in this round. |
| R606-1-F3 and R607-1-S1; Tests, Robustness | RESOLVED, preserved | Real `main()` controls, flag pairings, initialized banks and absent BIOS are tested; the stage-call removal is caught in the pins-only environment. |
| R606-1-F4 and R607-1-F2; Docs | RESOLVED, preserved | Both limit-case ledgers give 116, leaving 5.5; allocation and lane row name 56; measured 53 remains explicitly out of context. |
| R606-1-F5 and R607-1-R2; Docs | RESOLVED, preserved | The 231 LUT-cell figure belongs to the ROM region including decoder/multiplexer; the corresponding report has 220 Slice LUTs. |
| R607-1-F3 and R606-1-R2; Docs | RESOLVED, preserved | PR body identifies the exact head, five round-3 commits, previous dev merge and seven-member aggregate. The separate present-tense dev-tip sentence is new residue below. |
| R607-1-R1; Docs | RESOLVED, preserved | Contract states three mapped tiles versus 1.5 planned tiles / 6 KiB growth. |
| R607-1-S2 and R606-1-S3; Robustness, Tests | RESOLVED for reported truncation cases | All six independent header cuts and the standing truncation arms refuse by `elf truncated`. No claim of complete malformed-ELF validation. |

The optional suggestions remain optional and were not silently treated as fixed. No change in their severity or scope is claimed:

| Retained ID / severity / lenses | Artifact and authority | Impact, optional outcome and verification |
|---|---|---|
| R606-2-S1 / SUGGESTION / Robustness | `ctrl_memory.py:264`; reset copy/clear ranges in `ctrl_split_start.S:12`; original public suggestion | Orphan initialized or NOBITS SRAM sections outside startup ranges are not checked. Optionally check ranges against linker symbols; verify with orphan-section links. Published images do not exercise that class. |
| R606-2-S2 / SUGGESTION / Robustness | `ctrl_memory.py:204`; original public suggestion | Invalid table indices or zero symbol-entry size may fail unnamed. Optionally give them named refusals; verify malformed table controls. They still fail closed. |
| R606-2-S3 = R606-1-S1 / SUGGESTION / RTL, Robustness | `ctrl_split_start.S:10`; original public suggestion | No trap vector is installed here. Optionally define/install one and verify trap behavior in the deferred boot vehicle. This round makes no trap-service claim. |
| R606-2-S4 = R606-1-S2 / SUGGESTION / RTL, Robustness | `milan_soc.py:2725`, `ctrl_memory.py:312`; original public suggestion | No independent assertion bounds surplus initialization words by planned banks. Optionally add that assertion and an oversized-load control. New load-coverage validation addresses missing bytes, not surplus segments. |
| R606-2-S5 = R607-1-S3 / SUGGESTION, pre-existing / Tests, Docs | `sw/firmware/ctrl/test/ctrl_image_runtime.py`; round-2 manager assignment | Runtime stack-protector handling remains separately assigned work. Verify its own linked-runtime reproducer in that lane. No runtime rebuild or separate-issue closure is claimed here. |

**Reviewer execution and public evidence**

All commands were run under foreground parents that waited for children. Independent checks overlapped; no campaign exceeded the 16-job limit. The aggregate's build used `MAKEFLAGS=-j16`. Disposable clones, SDK, interpreter, CPU-generation files, probes and outputs stayed in `scratch/`. No full parent, processor, gPTP, Yosys or builder bank ran. No synthesis run, hardware access, workflow replica, source fix, commit, push, GitHub write, author contact or delegation occurred.

| Check | Result and receipt |
|---|---|
| Fresh environment | Python 3.12.3, repository pins and patch series, PyYAML; no firmware data package. SDK archive verified and extracted freshly. Scoped compiler identifies as Verilator 5.050; wrapper/frontend/binary hashes retained. `environment.log`, `pinned-setup.log`, `sdk.log`, `verilator-identity.log`. |
| Required delta gates | Classifier self-test and page classification, CI events check/self-test (1,749 items, 2,374 arms), docs wording, paths, style, contents, anchors, em-dash against requested base, Python idiom, hygiene, TODO, fail-fast, test-evidence, resource-baseline check and diff whitespace all rc 0. Separate logs and rc files under `receipts/`. |
| LiteX aggregate and harness | 7 passed, 0 failed/skipped/timed out; harness self-test rc 0. `aggregate.log`, seven `aggregate-test_*.log`, `runner-selftest.log`. Memory member: 123 successful checks, 44 mutants, 17 registered rules. |
| Independent previous probes | Original R607-2 load/ELF/bus probes rerun unchanged. Empty reset and no-load variants refused by `entry bytes`; short reset refused by `load coverage`; header truncations named. Bus probe: 864 cases across three bank sets, ROM/SRAM, byte enables, holes and boundaries. |
| Added load validation | 20,000 deterministic segment-union cases agree with a byte-set oracle. Eight genuinely linked `p_filesz` cuts refuse by the expected rule. Valid linked ROM agrees with independent binary export and round-2 ROM bytes/plan. `load-validation.log`. |
| Mutation grading fault control | Baseline environment failure produces no credited SoC mutation kill; six NOT GRADED lines and rc 1 are required. Disposable fault copy removed. `grading-control.log`, `grading-control-child.log`. |
| Checkout integrity | Raw blob bytes, file kinds, executable modes, index entries and required submodule populations verified before and after. All five gitlinks checked; both original and disposable clone retain the exact head/tree. `integrity-before.log`, `integrity-final.log`, `integrity-disposable.log`, `delta-integrity.log`. |

The [published source evidence](https://github.com/kebag-logic/milan-fpga/tree/b68338bfdaf0535576335d7fae6a877c2bbe6d7d/review-evidence/640-m8a-r1) was fetched selectively: no handoff or report files. Each selected blob was verified against its Git object ID (`public-evidence/provenance.tsv`). The [author's round-3 receipt](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6107961867) and the examined PR body bind the source gates to this head. Source evidence is the author's execution plus the reviewer checks above. **No manager source bank ran at this exact head; none is inferred.**

`check_evidence.py` reconciles eight utilization reports with the primitive TSV, recomputes all four plans and checks the identical published pre/post ROM digests:

| Shape / interfaces | ROM / SRAM bytes | Planned tiles | Mapped RAMB36 / RAMB18 | Mapped tiles |
|---|---:|---:|---:|---:|
| 1x1 / 1 | 95,032 / 45,520 | 35.0 | 33 / 2 | 34.0 |
| 1x1 / 2 | 96,320 / 56,880 | 38.0 | 37 / 1 | 37.5 |
| 8x8 / 1 | 108,680 / 86,080 | 48.5 | 46 / 2 | 47.0 |
| 8x8 / 2 | 110,056 / 112,208 | 54.5 | 52 / 2 | 53.0 |

The ledger is `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`; full split conditionally subtracts 11 to give 113. The 56-tile allocation gives 116; partial placement retains six AECP tiles and gives 130 before release. The 121.5 ceiling excludes the separate 13.5 reserve. These are reconciled published measurements and planning arithmetic, not a fresh integrated fit measurement.

Hosted evidence is in `hosted-snapshot.json`. [rtl-fast run 38131308856](https://github.com/kebag-logic/milan-fpga/actions/runs/38131308856) and its `rtl-fast` aggregate job succeeded on the exact head. `elaborate`, `docs-check`, `wire-accountability` and `docs-check-no-git` also succeeded. At the recorded observation, `rtl-full` remained in progress: four synthesis shards and one simulation shard had succeeded; four simulation shards were still running. The physical job was skipped. Executed jobs, pending jobs and skipped contexts are distinct; no exhaustive aggregate success is inferred.

**R607-3-R1 - RESIDUE - Docs**

Artifact: `pr-body-as-examined.md:21`, Status, second bullet. Authority/evidence: the sentence "The live `dev` tip is still `ac2c5e77`" is stale; this assignment specifies live dev `6bfeeb132fa0b1ad8a5b957446c66a498e633af7`. Impact: present-tense wording only. It changes no source, measurement, figure, verdict, test, generated artifact, conformance claim or privacy rule. The historical merge and its evidence remain correctly attributed.

Exact fix: replace that sentence with "That merge used dev `ac2c5e77`; the current-dev merge candidate is validated separately at merge time."

Required outcome and verification: apply that sentence to the PR body while preserving all historical evidence heads and gate results. Carry it to the manager's residue checklist. This residue does not leave a lens unclean.

**Reviewer-owned ledger**

CLEAN records the applied source lens at this exact head, subject to the disclosed reading-process limitation. No previous round's coverage is substituted for this delta assessment.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue rulings; REQUIREMENTS.md:28,306; `ctrl_memory.py:66,246,264`; named load refusal and budget boundaries; `ci_scope.py:66`; fit/ledger receipts; scoped M8a-1 acceptance | R607-3 | ce10328c3d89d81509e47836fa4a48b22ecdbc20 |
| RTL | CLEAN | `milan_soc.py:2710,2740` decode/error/init path; `ctrl_split.ld:13`, `ctrl_split_start.S:10`; raw unchanged hardware objects; real exported ROM control; 864-case bus scoreboard | R607-3 | ce10328c3d89d81509e47836fa4a48b22ecdbc20 |
| Robustness | CLEAN | `ctrl_memory.py:204,246,264`; empty/short load and truncated-header probes; eight linked cuts; 20,000 coverage cases; full-window/error-recovery and ROM/byte-lane tests | R607-3 | ce10328c3d89d81509e47836fa4a48b22ecdbc20 |
| Tests | CLEAN | `test_ctrl_memory.py:473,559,639,729,928,969`; 123 checks / 44 mutants in fresh pins-only environment; failing-environment grading control; 7/7 aggregate; classifier/event gates and exact-head hosted fast evidence | R607-3 | ce10328c3d89d81509e47836fa4a48b22ecdbc20 |
| Docs | CLEAN | `SPLIT_CONTROL_MEMORY.md:64,136`; `CI_WORKFLOWS.md:76,1190`; `TESTING.md:696`; both ledger rows and partial-placement sentences; public source receipts and current PR body; residue above is wording only | R607-3 | ce10328c3d89d81509e47836fa4a48b22ecdbc20 |

**Limits and pending manager duties**

- Decide whether the disclosed historical-report exposure permits counting this review toward the independent-review requirement. No concurrent reviewer verdict was read.
- Accept exact-head hosted and local-replica evidence, including the outstanding exhaustive aggregates. The reviewer ran neither the host orchestrator nor its self-test.
- Validate the final current-dev merge candidate with the builder and native banks at the merge turn and link the receipts on the PR. Source base `e8454e2751d05b02ee8e5a571857589ab358ab86` and assigned live dev `6bfeeb132fa0b1ad8a5b957446c66a498e633af7` are different from this reviewed source head. No candidate result is implied here.
- Resolve all concurrent review rounds, carry the residue and retained optional work, obtain merge authorization, then prove post-merge containment before declaring the lane complete. Issue #640 retains its broader milestone acceptance.
- Four full firmware size fixtures and synthesis were not rerun. Their published bytes/measurements were reconciled; newly linked execution used the small probe. All-fabric preservation is checked by unchanged construction and earlier public comparisons, not a fresh default build.
- Physical calibration **NOT RUN**. Field skips and the skipped physical hosted job are not hardware proof. Split boot, service, 8x8 capture and integrated routing/timing remain M8a-2 obligations; conditional wrapper reclamation is not yet measured integrated capacity.

**Packet and reproduction**

`setup_env.py <repo>` creates the pinned interpreter when launched with Python 3.12.3. `run_checks.py` takes repository, Python, Markdown-Python and SDK-archive parameters. `run_campaigns.py` takes disposable exact-head clone, interpreter, SDK and scoped compiler parameters and waits for all children. `probe_load_validation.py`, `probe_grading.py`, `check_evidence.py`, `verify_checkout.py` and the unchanged published probe scripts reproduce the focused checks. Set `TMPDIR` to packet `scratch/`, `MILAN_RV32_CC` to its verified SDK compiler and `PYTHONDONTWRITEBYTECODE=1` for probe runs. The grading control requires a disposable clone beneath `scratch/`.

`receipts/` preserves command output with local path substitutions only; the original output and disposable trees remain in unpublished `scratch/`. `MANIFEST.sha256` is the publication allowlist, with relative paths. Previous report-comment captures and all unlisted files are excluded. No skeleton remains.

R607-3 FINISHED
