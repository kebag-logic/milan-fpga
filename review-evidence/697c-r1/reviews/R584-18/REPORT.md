[R584] NEGATIVE - exact head 6758fe0216955c96f37b52d7129509586c9c0a8c

Composition review R584-18 of issue #697 / PR #705 on the merge-train candidate `6758fe02` (tree
`241c6276b43f3d8f921ad9aaa276b1b85698d035`): dev `49da9fd9` (#727, PR #728), then #726 (PR #729, candidate
`cdb49e7e`), then B16 (PR #725, candidate `ada26e56`), then PR #705's source head `97e71316`. All five lenses
were applied to what the composition adds to the reviewed source. One BLOCKER and one MINOR are open, so the
verdict is NEGATIVE. Both come from one interaction the manager's brief did not list: #726 adds a program that
builds this PR's firmware through this PR's builders, and the composed tree neither classifies it in the
boundary registry nor pins the stack it compiles. The required `firmware-boundary` job exits 2 on this tree.

## What was reconstructed, and from what

- AGENTS.md, CONTRIBUTING.md sections 3 and 6, docs/README.md.
- Issue #697: acceptance 1-5, owner decisions (MIT, own repository `tsn-c-stack`, Linux and bare-metal),
  the lane-697c assignment, the round-2 ruling (every gate that builds the stack refuses an off-pin or
  modified stack, one shared check, each with a planted control), the round-12 threat-model ruling, the
  round-18 and round-19 merge assignments and the round-19 ruling (classify each program that names the
  firmware's tree on evidence of what it runs; a firmware compiler gets a capture).
- `sw/firmware/ctrl/README.md` (the TSN stack submodule section), `docs/testing/CI_WORKFLOWS.md`,
  `sw/firmware/ctrl/test/ctrl_configs.py` (the boundary registry), `.github/workflows/rtl-fast.yml`.
- `git diff ada26e56..6758fe02`, the per-merge parents, and the three deltas in
  `receipts/composition_deltas.txt`: the PR's 74 paths (`d5858bbe..97e71316`), the predecessors' 37
  (`d5858bbe..ada26e56`), and the 37 the composition adds to the reviewed source (`97e71316..6758fe02`).
- Public evidence: the author's round-19 tree under `review-evidence/697c-r1/author-r19` at `a1f940cd`
  (listed, used as the source-head record only), the manager's round comments on #697, the live PR body.
- Prior public findings were read only after this round's verdict and ledger were drafted.

## The composition, file by file

`scripts/compose_check.sh` takes every path that differs between the merge base `d5858bbe` and the candidate
(109) and checks it three ways (`receipts/compose_check.txt`):

- a path only the PR changed equals the PR source head's blob; a path only the predecessors changed equals
  `ada26e56`'s blob: 0 mismatches;
- two paths both sides changed:
  - `docs/testing/CI_WORKFLOWS.md` (#727's measured-time split, and the PR's boundary jobs);
  - `sw/firmware/ctrl/aecp/README.md` (#726's counter paragraph at lines 55-64, and the PR's wire-comparison
    stack paragraphs at lines 141-164). The brief named only the first; the second also overlaps.
- Each overlap is exactly `git merge-file` of the two sides over the base, with no conflict
  (`receipts/overlap_remerge.txt`). Both sides' text stands in both files.
- The submodule gitlinks are the PR's: `tsn-c-stack` `405dc683`, lwSRP `08ee86e8`; no predecessor moves a
  gitlink.

The semantic interaction is not in an overlapping file. #726 adds `tb/verilator/milan_dp/stream_counter_f5.py`
(the F5 gap check). It imports this PR's modified `ctrl_build` and `aecp_arms` (`stream_counter_f5.py:15-17`),
builds the AECP core and mailbox adapter with `aecp_arms.core_arm` (`:63`, `:70`), and therefore compiles
against the stack's `include/` (`ctrl_build.py:110-113`, `aecp_arms.py:62`). It is a program (`:86`) that names
the firmware's tree. The Makefile targets `counters-f5` and `counters-mutants`
(`tb/verilator/milan_dp/Makefile:673-684`) run it. No other predecessor path names the firmware's tree or an
image input (`receipts/composition_deltas.txt`; the S-to-H delta is RTL, testbenches, BDD, docs,
`scripts/suite_shards.py`, `scripts/measure_test_evidence_readers.py` and the AECP README).

## Gates and probes run on the candidate

Environment: the review clone at `6758fe02` with `tsn-c-stack` and lwSRP initialised at their gitlinks;
scratch copies of the candidate, of `ada26e56` (dev side) and of `97e71316` (source head); the pinned RV32 SDK
installed and verified by `scripts/ci_rv32_sdk.py` (archive sha256 `d42680e9...`); CPython 3.12.3 venv with
PyYAML, `sw/litex/litex_pins.txt` and the markdown lock; GoogleTest/GMock 1.14.0 headers and libraries; host
GCC 16.2.1, Git 2.56.0. Every result below is in `receipts/`.

| Run | Result | Receipt |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (the `firmware-boundary` step, `rtl-fast.yml:515`) | **rc 2** after all five builders exit 0: `REFUSED: tb/verilator/milan_dp/stream_counter_f5.py names the firmware's tree and is a program, and is neither a known builder ...` | `boundary_fw_candidate.log` |
| Counterfactual P4: the same step in a scratch copy with only that program added to `SUITES` (`probe_p4_patch.diff`) | rc 0, `ctrl_boundary: PASS`: 2824 sources of 3052 invocations, 0 findings, 110 boundary, 106 pin and 4 figure controls, 0 misbehaved (the source head's own figures) | `probe_p4_boundary_fw_classified.log` |
| P2: the gate's own `ctrl_configs.held()` over a stand-in capture, at `97e71316` and at `6758fe02` | program refusals: 0 at the source head, 1 at the candidate (`stream_counter_f5.py`) | `probe_p2_held_text.txt` |
| P1: stack `include/wire.h` edited by one comment line | `ctrl_build.py --stack-pin` rc 2 (`differs from the pinned 405dc683: include/wire.h`); `stream_counter_f5.py --shape 1` rc 0, `F5 1x1 clean` | `probe_p1_f5_unpinned.txt`, `probe_f5_pin_script.txt` |
| P1b: `#error` planted in the stack's `include/wire.h` | `stream_counter_f5.py` stops in `aecp.c` on that header: it compiles the stack | `probe_p1b_f5_reads_stack.txt` |
| P3: `make -n` of `counters-f5` and `counters-mutants` | recipes run `stream_counter_f5.py` with no pin prerequisite; `milan_dp/Makefile` names `stack-pin` 0 times (the mbx bench: `Makefile:99-102`) | `probe_p3_milan_dp_dryrun.txt` |
| #726's F5 gap check on the composed tree, `--shape 1` and `--shape 8` | rc 0 each (the PR's `ctrl_build.Tree` and `core_arm` serve it unchanged) | `f5_shape1_candidate.log`, `f5_shape8_candidate.log` |
| F5 planted variants `late`, `rate`, `fixed-grid` | each `run.log: rc=1` (detected), `escape.log: rc=0` (omission escapes), as #726 claims | `f5_mutants_candidate.log` |
| Standalone control images, all five shipped shapes, candidate and `ada26e56` with the same SDK | 5 of 5 ELFs byte-identical; both manifests sha256 `546b0d42a0b19399...` | `images_standalone_*.MANIFEST`, `images_logs/` |
| 36 documentation and CI-contract commands (`scripts/docs_gates.sh`) | 36 of 36 rc 0 | `docs_gates_candidate.txt` |

The 36 commands include `docs_check.py` (0 findings, 206 pages); `check_em_dash.py --base ada26e56` (0 over 449
added lines) and `--base d5858bbe` (0 over 3180) and `--selftest`; `gen_toc.py --selftest`,
`--verify-anchors` (488 links) and `--check`; `check_doc_paths.py`, `check_doc_style.py`, `DOC_MAP.gen.py
--check`, `submodule_boundaries.gen.py --check`, `check_submodule_docs.py` and `--selftest`;
`ci_events.py --check` (2169 items), `--selftest` (3064 arms) and `--firmware-census` (`preserved: true`);
`ci_scope.py --selftest`; `suite_shards.py --selftest` (PASS); `measure_test_evidence.py --check` (62 default
suites) and `--selftest`; the hygiene, idiom, fail-fast, naming, TODO, port-contract, archive and source-list
gates; `ctrl_build.py --stack-pin` (accepted `405dc683`).

## Judgement of the brief's items

- **CI_WORKFLOWS.md states both sides.** The merged page carries #727's measured-time split, the per-suite
  duration table in `suite_shards.py`, the 60 % prediction gate read from `rtl.yml` and the add-a-suite steps
  (`:285-305`), and the PR's `firmware-boundary` and `firmware-verilator` bullets (`:67-117`), the four
  firmware jobs' `tsn-c-stack` fetch (`:59`), the aggregate's two extra needs (`:132`), the docs-only skip
  list (`:161`) and the Verilator workers' fetch (`:320-325`). `ci_events.py --check` reads the page against
  the workflows and passes. Two of the PR's sentences became false in combination with #726, not with #727:
  `:93` and `:322-325` (finding F2).
- **`suite_shards.py --selftest` passes on the composed tree.** The PR adds and renames no default Verilator
  suite (no `tb/verilator/*` directory added or removed in its delta; `measure_test_evidence.py` counts 62
  default suites); its only `rtl.yml` change adds `third_party/tsn-c-stack` to the workers' fetch and moves no
  `timeout-minutes`.
- **The 65 linked images.** The five standalone images are byte-identical between the candidate and the dev
  side `ada26e56`. The 60 runtime variants were not linked here (see limits); no path in `97e71316..6758fe02`
  is an image input (the builders read `sw/firmware`, `sw/builder`, `sw/mailbox`, `configs`, the stack, lwSRP
  and the processor submodules, none of which a predecessor changes but the AECP README), and no path in
  `d5858bbe..ada26e56` is one either, so the source head's published 65-of-65 equality with `d5858bbe` carries
  to the composed pair.
- **#726 and B16.** B16 changes two findings pages; nothing reads them. #726 is the source of F1 and F2.

## Findings

### R584-18-F1 - BLOCKER - Conformance, Tests - the required boundary gate refuses the composed tree

- **Artifact:** `tb/verilator/milan_dp/stream_counter_f5.py:15-17,63,70,86` (from #726) against
  `sw/firmware/ctrl/test/ctrl_configs.py:110-189` (the registry: `BUILDERS`, `PART_OF`, `OUTSIDE`, `SUITES`)
  and `:283-290` (`held()`); `.github/workflows/rtl-fast.yml:484-515` (`firmware-boundary`, required by the
  aggregate at `:590`).
- **Authority/evidence:** the #697 round-19 ruling: a program that names the firmware's tree is classified on
  evidence of what it runs, and a firmware compiler gets a capture; `CI_WORKFLOWS.md:80` and
  `sw/firmware/ctrl/README.md:152-155` state that such a program "must be a known builder or listed with why".
  AGENTS.md section 7 requires the required jobs to pass on the merge candidate. On this tree the step exits 2
  naming the program (`receipts/boundary_fw_candidate.log`). With only that one registry entry added, the same
  step passes with the source head's exact figures (`probe_p4_boundary_fw_classified.log`), and the gate's own
  `held()` finds no such program at `97e71316` (`probe_p2_held_text.txt`). So this is the only boundary defect
  the composition adds, and neither source tree has it alone.
- **Impact:** merging this candidate turns `firmware-boundary`, and so the `rtl-fast` aggregate, red on `dev`
  and on every later firmware or RTL change until fixed. Classified only to pass, the program's own compiles
  of the AECP core and mailbox adapter against the stack would still be judged by no capture.
- **Required outcome:** the merged tree classifies `stream_counter_f5.py` on evidence of what it compiles
  (it compiles firmware sources against the stack's public headers), so that its compiles are judged or its
  listing states truthfully why they need not be, with a control showing the entry is load-bearing; the
  manager rules which lane carries the change and in which train order.
- **Verification:** `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without
  verilator` on the new candidate ends `ctrl_boundary: PASS`; `scripts/held_text_probe.py <tree>` reports 0
  program refusals; the new control fails when the entry is removed.

### R584-18-F2 - MINOR - Conformance, Robustness, Tests, Docs - a stack consumer runs without the pin check

- **Artifact:** `tb/verilator/milan_dp/stream_counter_f5.py:63,70` and `tb/verilator/milan_dp/Makefile:673-684`;
  the claims `sw/firmware/ctrl/README.md:177` ("Every gate that builds the stack first runs the same pin
  check"), `:233` ("no target run alone reaches it unpinned"), `docs/testing/CI_WORKFLOWS.md:93` ("Every
  Makefile target that builds against the stack has the pin check as a prerequisite") and `:322-325` ("Every
  bench target that compiles against the stack has the shared pin check as a prerequisite").
- **Authority/evidence:** the #697 round-2 ruling item 2 (every gate that builds the stack refuses an off-pin
  or modified stack, through one shared check with a planted control; "the statements then hold as written").
  With the stack's `include/wire.h` edited, the shared check refuses and `stream_counter_f5.py` builds and
  passes (P1); a planted `#error` in the same header stops it in `aecp.c`, so it does compile the stack (P1b);
  its two Makefile targets carry no pin prerequisite (P3). The PR's entry-point census and pin controls do not
  include it, because it did not exist at the source head.
- **Impact:** the #726 gap-check evidence can be produced against a stack that is not the pinned one without
  any refusal, and four PR statements about every stack consumer are false on the merged tree. It is not in a
  hosted job today (`milan_dp`'s `run` target calls `counters`, not `counters-f5`), so it is not a CI escape.
- **Required outcome:** in the merged tree the F5 gap check and both `milan_dp` targets that run it refuse an
  off-pin or modified stack before building, through the shared check, with a planted control; or the four
  statements are narrowed to what holds. One change can carry this with F1.
- **Verification:** `scripts/probe_f5_pin.sh` in a disposable copy: P1 ends in a pin refusal before any build,
  P3 shows the prerequisite; the README and CI_WORKFLOWS statements re-read true.

## Prior public findings at this head

The composition changes none of the PR's own files (`compose_check.txt`: every PR-only path equals
`97e71316`'s blob), so every prior source-head finding keeps the status the source reviews gave it.

| Finding | Status at `6758fe02` | Evidence |
|---|---|---|
| R584-17-RES-1, R585-18-RES-1 (PR body calls the published head "unpushed") | RETAINED RESIDUE; the live body still says "unpushed" (its Status paragraph and the last Round 19 paragraph) | `gh pr view 705` at 05:41Z, head `97e71316` |
| R584-17-RES-2 (carried fix cites `README.md:181`) | RETAINED RESIDUE; the body still cites `:181`; the sentence is at `sw/firmware/ctrl/README.md:193` in the candidate | grep of the candidate |
| R585-16-RES-1 (allowlist "names a program") | RETAINED RESIDUE; text unchanged at `README.md:193`, `ctrl_build.py:199`, `:551-552` | candidate blobs equal `97e71316`'s |
| R584-17-S1 (`PART_OF` entry for `ctrl_memory_probe.py` not load-bearing), R584-17-S2 ("the firmware's" in the `milan_soc.py` reason) | RETAINED SUGGESTION; `ctrl_configs.py:140`, `:149-152` unchanged | candidate blob |
| R584-16-S1 / R585-17-S1, R584-15-S1, R585-16-S1 and the earlier carried suggestions and #495 residue | RETAINED as the source reviews list them; no artifact they name is touched by the composition | `composition_deltas.txt` |
| R584-1 ... R584-16 and R585-1 ... R585-17 blocking findings | RESOLVED at the source head per R584-17 and R585-18; unchanged by the composition | same |

## Lens results

[R584] UNCLEAN Conformance - `stream_counter_f5.py:15-17,63,70,86`; `ctrl_configs.py:110-189,283-290`; #697 round-2 and round-19 rulings; `receipts/boundary_fw_candidate.log`, `probe_p1_f5_unpinned.txt` - F1 and F2. Otherwise checked: the composition keeps both CI_WORKFLOWS.md sides and both aecp README sides as merged (`overlap_remerge.txt`), the pin `405dc683` and lwSRP `08ee86e8` are unchanged, and five standalone images equal the dev side.

[R584] PASS RTL - `receipts/compose_check.txt`, `composition_deltas.txt` (`d5858bbe..97e71316` holds no `.sv`/`.v`/`.vh`; every `hdl/` path in the candidate is `ada26e56`'s blob); `rtl-fast.yml:484-620` job graph via `ci_events.py --check` and `--firmware-census` - the composition adds #726's RTL beside a PR that changes none, and the job budgets are untouched (P4's step took 800 s locally, 44 % of `firmware-boundary`'s 30 minutes). The PR's own RTL-lens scope stays covered by the source reviews R584-17 (comment 6138624793) and R585-18 (comment 6138415991) at `97e71316`.

[R584] UNCLEAN Robustness - `probe_p1_f5_unpinned.txt`, `probe_p1b_f5_reads_stack.txt`, `probe_p3_milan_dp_dryrun.txt` - F2: a modified stack is compiled and graded without refusal through #726's entry point. Otherwise checked: without the edit the shared pin check accepts the clean clone (`docs_gates_candidate.txt`, last command).

[R584] UNCLEAN Tests - `boundary_fw_candidate.log`, `probe_p4_boundary_fw_classified.log`, `probe_p2_held_text.txt`, `f5_*_candidate.log` - F1 (the required gate fails on the candidate) and F2 (no control covers the new stack consumer). Otherwise checked: #726's F5 gap check and its three planted variants keep their verdicts on the composed builders; `suite_shards.py --selftest`, `ci_events.py --selftest`, `ci_scope.py --selftest` and `measure_test_evidence.py --selftest` pass.

[R584] UNCLEAN Docs - `docs/testing/CI_WORKFLOWS.md:59,67-117,132,161,285-305,320-325`; `sw/firmware/ctrl/aecp/README.md:55-64,141-164`; `sw/firmware/ctrl/README.md:152-155,177,231-233`; `docs_gates_candidate.txt` - F2: four statements about every stack consumer are false in composition. Otherwise both overlap files state both sides correctly, and the docs, em-dash (base `ada26e56` and `d5858bbe`), TOC, anchor, path, submodule-docs and CI-contract gates pass.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #697 rulings; `ctrl_configs.py` registry; `stream_counter_f5.py`; overlap re-merge; pins; standalone images | R584-18 | `6758fe0216955c96f37b52d7129509586c9c0a8c` |
| RTL | CLEAN | three-way composition check (no PR-side HDL; every `hdl/` path is the predecessor's blob); job graph and census; PR-side RTL scope by R584-17 and R585-18 at `97e71316` | R584-18 | `6758fe0216955c96f37b52d7129509586c9c0a8c` |
| Robustness | UNCLEAN (F2) | pin-edit and poison probes; Makefile dry runs | R584-18 | `6758fe0216955c96f37b52d7129509586c9c0a8c` |
| Tests | UNCLEAN (F1, F2) | `firmware-boundary` step and its counterfactual; `held()` differential; F5 gap check and variants; selector and CI self-tests | R584-18 | `6758fe0216955c96f37b52d7129509586c9c0a8c` |
| Docs | UNCLEAN (F2) | `CI_WORKFLOWS.md`, both READMEs, 36 documentation and contract commands | R584-18 | `6758fe0216955c96f37b52d7129509586c9c0a8c` |

## Real limits

- The 60 runtime image variants (`ctrl_srp_image.py`, flat and split) were not linked. Their runtime archives
  need external picolibc and compiler-rt sources; the release fetched here does not build with
  `ctrl_image_runtime.py`. Their equality rests on the input argument above and the source head's published
  65-of-65 receipt, not on a link at this head.
- The Verilator side of the boundary (`--only verilator`), the firmware execution and mutation campaigns,
  coverage and the store suite were not run at the candidate. No predecessor path is read by them
  (`composition_deltas.txt`); they remain covered by the source reviews at `97e71316`.
- Of the docs workflow, 36 commands ran; the HDL reference, WaveDrom, diagram PNG, bare-metal sv2v, builder,
  NVM and wire-accountability steps did not. The runner's own `act_ci.py --selftest` was not run (host use is
  not allowed).
- Host, not the runner's Ubuntu 24.04 replica: GCC 16.2.1, Git 2.56.0, CPython 3.12.3, GoogleTest 1.14.0.
- A first `firmware-boundary` attempt aborted at 263 s on a broken interpreter link this round introduced in
  its own scratch venv; the link was repaired and the run repeated from the start. The aborted log is not a
  receipt.
- Hosted runs at this candidate were not inspected; no hosted or act acceptance is claimed. Physical
  calibration NOT RUN; no hardware was touched.
- Host paths in receipts are rewritten to `$PACKET`, `$CLONE`, `$TOOLS` or `<host path>`.

## Pending manager duties

- Rule which lane carries F1 and F2 (PR #705, or #726's PR #729 ahead of it in the train), and rebuild the
  candidate; the boundary step then needs a passing run at the new candidate head.
- Note that the overlap set is two files, not one: `sw/firmware/ctrl/aecp/README.md` merges cleanly.
- Hosted `rtl-fast` (including both boundary jobs), `rtl` and `docs` acceptance, and the act replica, at the
  final candidate.
- Carry R584-17-RES-1, R584-17-RES-2, R585-18-RES-1 and R585-16-RES-1 to the residue checklist.

## Clone integrity

After the probes the review clone holds exactly the candidate: HEAD `6758fe02`, tree `241c6276`, index equal
to the tree entry for entry (1314), every tracked file's bytes hashed from disk equal to its blob, no
untracked or ignored file, `tsn-c-stack` at `405dc683` and lwSRP at `08ee86e8`, both clean
(`receipts/clone_integrity.txt`). Every probe that edited a file ran in a scratch copy.

R584-18 FINISHED
