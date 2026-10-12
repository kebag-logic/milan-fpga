[R585] NEGATIVE - exact head 8aaa2da74e3d5ee569fed420debc2b69c6749d44

External independent review R585-12 of issue #697 / PR #705, round 13 delta (`adb93604..8aaa2da7`: `c03e9c9c4`, merge `30744883f` of dev `c20c85bd`, `5425fb644`, `6382dc88a`, `8aaa2da74`). Tree `cb90055f0843f221ceb6fecc20777cb24cea7f5a`.

All five lenses were applied. Conformance, RTL and Docs are clean. One MINOR finding is open: R585-12-F1, under Robustness and Tests. It is not new code in this round. It is R584-8-S1 (a SUGGESTION under the earlier model), re-graded because the round-12 ruling now puts Git's object store inside the pin proof's threat model, and the route stays open at this head with no recorded decision.

Every round-13 item the assignment names was confirmed at this head:
- The tsn-c-stack gitlink is `405dc68310a18f669049ffc10cc23eef7300dcff`. It is the tag `milan-fpga-697-pin-405dc683`, the head of tsn-c-stack PR #22 and branch `acmp-publish-port`, and it is not `main` (`1ba27354`).
- Its seven core files match dev `c20c85bd`'s copies token for token and line for line, checked with this round's own lexer. They compile to 6 of 6 byte-equal RV32 objects.
- The merge keeps the ACMP core's removal and dev's adapter with its `publish` wiring. It keeps both sides' CI jobs.
- F-INT's 11 core plants target the stack's `acmp.c`, and each fails by name. A no-op twin of each escapes.
- 35 of 35 RV32 images are byte-identical to dev's, linked at this exact head.
- The 79 pin controls and the 17 inherited-environment controls hold.
- The records are regenerated through their generators.
- Hosted CI at this tree: `rtl-fast`, `firmware-unit`, `firmware-boundary`, `firmware-verilator` and `publication-census` succeeded.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`.
2. Issue #697:
   - the body and its frozen acceptance 1-5;
   - the owner decisions 6074086970, 6074093506 and 6074191062;
   - the lane assignment 6091228902 and the pin ruling 6092176555;
   - the round-12 ruling 6114400461, the round-12 STOP 6115091316, the round-13 assignment 6116488747 and REVIEW READY 6117226531.
3. The PR body at this head (Status, Round 12, Round 13, How to validate, Known limitations, DoD).
4. `git diff c20c85bd..8aaa2da7`, the round-13 commits one by one, and the merge resolution file by file.
5. Public evidence at `2f4a5c59`: `review-evidence/697c-r1/author-r13/` (HANDOFF round 13, `review-ready-round13.md`, `pin-proof.txt`, the round-12 probe). Round 13 publishes no image manifest or gate logs, so this round re-executed those itself.
6. Hosted check runs and job logs at this head.
7. Only after this round's own verdict and ledger were written (`REPORT.md` draft): the prior review findings on PR #705 (R584-10, R585-9 and the tables they carry).

## Findings

### R585-12-F1 - MINOR - Robustness, Tests - the pin proof accepts an edited `src/adp.c` under a forged `src/` tree object, a route inside the ruled threat model, open with no decision

- **Artifact:**
  - `sw/firmware/ctrl/test/ctrl_build.py:439` (`ls-tree -r -t` of the pin, whose subtrees Git reads without checking their hash) and `:425-460` (`stack_pin`);
  - `sw/firmware/ctrl/test/ctrl_pin.py:45-62` (THE THREAT MODEL, "Two routes within the model are open, for a decision", `:59`);
  - `sw/firmware/ctrl/README.md:184-190`;
  - PR body, Round 12 "Open, for the manager" (b), Round 13 "Open, for the manager" (a), Known limitations "Round 12: within that model two routes are open".
- **Authority/evidence:**
  - The [round-12 ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461), item 2: "The pin proof's threat model is the state it reads: the checkout's files and modes, Git's object store, refs, configuration and attributes, and the environment the proof inherits." Only adversarial code inside the proof's own modules is ruled out of scope.
  - This round's probe, `scripts/forge_probe.py`, on a scratch clone of the pinned stack (Git 2.56.0), result in `receipts/forge-probe.txt`:
    - F0 control: an edit of `src/adp.c` alone is refused (`differs from the pinned 405dc683: src/adp.c`).
    - F1: the pinned `src/` tree's loose object is overwritten with a tree holding the edit's blob, plus the same edit on disk. Result: `ACCEPTED 405dc683…`. `git fsck --full` exits 11 with `hash-path mismatch`.
    - F2: a forged pinned commit object is refused (`hash mismatch 405dc683…`), so the open route is the subtree read.
  - The texts state this route as open "for a decision". The round-13 assignment (item 5) keeps the texts and makes no decision on it. No later ruling exists on the issue or the PR.
  - Prior history: R584-8-S1 was retained as a SUGGESTION because object-store corruption lay "outside the ruled replacement/graft/filter class". The round-12 ruling widened the model to the whole object store, which removes that reason.
- **Impact:**
  - The proof's claim that every gate builds the pinned stack or none fails for one state the ruling places in scope. A checkout with a forged subtree object passes every gate that calls `stack_pin`, while building edited stack code.
  - Exposure is limited. Objects fetched from the remote are hash-checked on transfer, so a hosted runner's fresh checkout cannot hold such an object. It takes deliberate local tampering of `.git/modules/third_party/tsn-c-stack/objects`.
  - This is not wording: the verdict changes, and no control covers it.
- **Required outcome:** one of these, recorded publicly:
  - (a) The proof checks every tree object it reads against its id, failing closed, with a standing pin control that plants a forged subtree and ends in a named refusal. One way is to hash each tree's raw bytes as listed, as R584-8-S1 suggested.
  - (b) A maintainer ruling that narrows the model, for example to exclude forged or corrupt objects. The README, the docstring and the PR body then state the narrowed model.
  - This review does not prescribe the design.
- **Verification:**
  - For (a): `forge_probe.py` F1 refused by name at the corrected head; the new control `[ok]`; the other 79 pin controls `[ok]`.
  - For (b): the ruling's link, and the three texts consistent with it.

### SUGGESTIONS (optional, no effect on the verdict)

- **R585-12-S1 - SUGGESTION - Robustness** - `ctrl_build.py:389` (`stack_gitlink`, `ls-files --stage`): a `core.fsmonitor` program set in the superproject's own `.git/config` runs 4 times while the proof decides. The verdict stays correct: `receipts/fsmonitor-super-probe.txt`. The same setting in the stack clone's own config is not run (`forge_probe.py` F3, 0 runs). The texts already state it as the second open route. `-c core.fsmonitor=false` on the helper's command line would close it, as the author noted.
- **R585-12-S2 - SUGGESTION - Tests** - `ctrl_pin_env.py:131-135` (`unstored`) keeps `.git/objects/info`. When the stack's object store has its own `objects/info/alternates`, for example a submodule initialised with `--reference`, the local clone the controls make inherits it. The control "GIT_ALTERNATE_OBJECT_DIRECTORIES, the clone's objects, which its own store no longer holds" then reports `[ESCAPED]` with a correct verdict. Receipts: `receipts/pin-controls-with-alternates.log` (1 of 79 misbehaved) and `receipts/pin-controls-head.log` (0 of 79 without the file). This fails closed and the documented setup has no alternates file. The setup could empty or neutralise `info/alternates`, or refuse the setup by name.

### RESIDUE (PR body wording only; exact fixes for the manager's checklist)

- **R585-12-RS1** - PR body Status, line 1: "(round 13, four commits and a merge of dev `c20c85bd` on `adb93604`, not pushed)". The PR head is `8aaa2da7`, so it is pushed. Fix: delete ", not pushed".
- **R585-12-RS2** - PR body Definition of Done: "(all met locally; pin confirmed in #697 comment 6092176555)". That comment confirms `1a9f651c`, and the pin is now `405dc683`. Fix: "(all met locally; pin `405dc683` set by #697 comment 6116488747 under the rule of comment 6092176555)".
- **R585-12-RS3** - PR body "Authoritative references", fourth bullet: the [Control firmware], [firmware harness], [submodule map], [CI workflow policy] and [mailbox bench] links all pin `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1`, whose pages predate the `405dc683` pin; for example that `SUBMODULES.md` has no `405dc683` row. Fix: replace `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1` with `8aaa2da74e3d5ee569fed420debc2b69c6749d44` in those five links of that bullet.
- **R585-12-RS4** - PR body Known limitations: "The hosted `firmware-unit` step needs CMake and Clang for the stack's own gate; both ship on the hosted Ubuntu image; the boundary step passed in `firmware-unit` at `386b8e69`." Since round 8 the stack's own gate runs in `firmware-boundary`. Fix: "The hosted `firmware-boundary` job needs CMake and Clang for the stack's own gate; both ship on the hosted Ubuntu image."

## What was confirmed at this head

| Item | Result | Receipt |
|---|---|---|
| Pin is `405dc683`, tagged, reachable, not `main` | Gitlink `405dc68310a1…` at HEAD. Remote refs: `refs/tags/milan-fpga-697-pin-405dc683`, `refs/pull/22/head` and `refs/heads/acmp-publish-port` all name it; `main` is `1ba27354`. The pin is not an ancestor of `main`, which differs in `src/adp.c` only (6+/2-), as `SUBMODULES.md` says. tsn-c-stack's own `quality` and `bare-metal` runs succeeded at `405dc683`. | source; GitHub refs and check runs |
| Cores token- and line-identical to dev `c20c85bd` | `scripts/token_compare.py`, a lexer of this round's own that drops comments and whitespace: adp.c 1736, adp.h 497, acmp.c 7849, acmp.h 1175, maap.c 2064, maap.h 394, wire.h 202 tokens, each `tokens-equal=True lines-equal=True`. Dev's seven files are the same bytes at F-INT's `09c7231e`. `acmp_fake.hpp` is token-equal; its lines are not, which the lane does not claim. | `receipts/token-compare.txt` |
| Stack ACMP tests cover dev's | Dev's 69 `test_acmp.cpp` tests are all among the stack's 79. 2 bodies differ only in three assertion messages (A29), and the two killers that name them use the stack's words. | `receipts/test-acmp-bodies.txt` |
| Byte-equal RV32 objects | `scripts/objects.sh`, the image flags with `-DNDEBUG` and `-UNDEBUG`, pinned SDK (gcc 14.3.0, archive sha256 `d42680e9…`): adp, acmp and maap each EQUAL in both modes, 6 of 6. | `receipts/rv32-objects.txt` |
| Images byte-identical to dev, every shape | `scripts/images.sh` in fresh clones at dev `c20c85bd` and at `8aaa2da7`, with the same pinned SDK and the same freshly built runtime archives (`-fno-stack-protector` for AECP): 35 of 35 ELF hashes equal. The manifests are byte-equal, sha256 `968f4f53…`. The head's `ctrl_image.py` prints `tsn-c-stack at 405dc683…`. The five `ctrl_image` hashes equal the author's table, for example arty_4x4 `8c27ee19b7a4f0a6…`. The SRP hashes differ from the author's because the runtime archives differ, but they are equal between dev and head. | `receipts/images-{dev,head}.sha256` |
| Merge keeps the deletion and dev's adapter | `sw/firmware/ctrl/{acmp/acmp.{c,h},test/acmp_fake.hpp,test/test_acmp.cpp,wire/}` are absent. Outside `test/`, every `.c` and `.h` under `sw/firmware/ctrl` and `sw/firmware/ctrl_nvm` equals dev's. The exceptions are the seven removed core files and a two-line comment in `mbx_wire.h`, so `acmp_mbx.{c,h}` is dev's. `acmp_mbx.c:98` is `m->ports.publish = port_publish;`. | `git diff c20c85bd HEAD` |
| Merge resolution, file by file | For the 22 files both sides changed, the head-vs-dev diff carries exactly the lane's changes, plus: `publication-census` kept in `rtl-fast` `needs` and checks and in `CI_WORKFLOWS.md`; `.PHONY` holding `census` and `stack-pin`; the pinned-link SHA moved; the 11 plant paths. No dev line is lost. | `receipts/merge-both-sides.txt` |
| CI jobs, both sides | The `rtl-fast` aggregate needs and checks `publication-census`, `firmware-unit`, `firmware-boundary` and `firmware-verilator`. `ci_events.py --check` (1974 items) and `--selftest` (2766 arms) pass. | `receipts/docs-subset.txt` |
| F-INT's 11 core plants | `scripts/pub_acmp_plants.py` runs the tree's own `campaign()` over the 15 `pub-acmp-*` plants. The 11 core plants name `tsn-c-stack/src/acmp.c`, each fixture occurs once, and each is `[ok]` at the head. Each no-op twin is `[ESCAPED]`, so the catches come from the plants. Failing-check counts at head are at least dev's for every plant (51 against 39, 26/22, 3/1, 4/3, 9/7, 5/4; the rest equal). Hosted `firmware-unit` prints the same 15 lines with the same counts. Fixtures, killers and words are dev's; only the path argument changed. | `receipts/pub-acmp-{head,dev}.log`, `receipts/hosted-firmware-unit.log` |
| 79 pin controls and 17 environment controls | `scripts/pin_controls.py` runs the tree's `pin_controls()`: 79 controls, 0 misbehaved, census 0 findings, CPython 3.14.7. The 16 inherited-environment arms plus the `fork_exec` key-twice judge are each `[ok]`, and so are the R585-9, R584-9 and replacement, graft and filter controls. The hosted boundary jobs show the same 79 on CPython 3.12.3. | `receipts/pin-controls-head.log`, `receipts/hosted-firmware-{boundary,verilator}.log` |
| `8aaa2da7`'s `OUTSIDE` entry | `publication_census.py` runs `run.sh --emit`, sv2v, Yosys and the builder's generator, and compiles no C. With the entry removed it is the one unplaced program, so the gate would refuse it by name. No `OUTSIDE` entry is stale. | `receipts/outside-probe.txt` |
| Records through generators | `submodule_boundaries.gen.py --check` and `--selftest`, `check_submodule_docs.py` (6 exact gitlinks) and its self-test, `check_diagram_pngs.py`, `DOC_MAP.gen.py --check`, `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `docs_check.py` (0 findings), `check_em_dash.py --base c20c85bd` (0 findings over 401 added lines, pinned renderer), and the py, cpp and hygiene ratchets all pass. All 20 pinned tsn-c-stack links name `405dc683`, and every target exists at the pin; no `1a9f651c` remains. | `receipts/docs-subset.txt`, `receipts/docs/` |
| Firmware gates | `test_ctrl_firmware.py --require-rv32 --jobs 4`: `tsn-c-stack at 405dc683…`, 60 arms `[ok]`, PASS (301 s). `fw_coverage.py --check --jobs 4`: PASS, 30 files, the cores read at the stack's paths (250 s). `make -C tb/verilator/mbx` with Verilator 5.050: six tallies, 0 failures, `mbx mutants: 6 of 6 caught`. `maap_differential.py --self-test`: `16/16 caught`, rc 0. | `receipts/gates/` |
| Hosted at this tree | The merge ref `eb9d51f`'s tree is `cb90055f`, equal to the head's. Succeeded: `rtl-fast`, `firmware-unit` (`mutants: 506 of 506 caught`, coverage 30 files, store 435 tests, 41 min 28 s of 45), `firmware-boundary` (2822 of 3049, 0 findings, 105/79/4 controls, 0 misbehaved), `firmware-verilator` (829 of 926, 6/79/4), `publication-census`, `docs-check`, `docs-check-no-git`, `elaborate`, `wire-accountability`, the 4 Yosys shards and Verilator shard 3. Still in progress at 04:15 UTC: Verilator shards 0, 1, 2 and 4. `verilator-suites` and `yosys-portability` are not yet emitted. | `receipts/hosted-checks.txt` |

## Prior findings at this head

| Prior finding | Status at `8aaa2da7` | Evidence |
|---|---|---|
| R584-10-F1 (hosted 3.12.3 Python-level rebinding filed under the native-code limit) | RESOLVED by the round-12 ruling item 2: code inside the proof's modules is out of scope, at most a SUGGESTION. The texts state the ruled model (`ctrl_pin.py:45`, `README.md:184`, PR body Known limitations Round 12). | source |
| R585-9-F1 (dynamic code through attributes and inside the helper) | RESOLVED (round 11 hook). The `inspect.builtins`, `pkgutil.importlib`, inside-the-helper and `sys.audit`-rebound controls are each `[ok]`. | `receipts/pin-controls-head.log` |
| R584-8-S1 (object-store corruption) | SUPERSEDED by R585-12-F1 (MINOR) under the round-12 model | `receipts/forge-probe.txt` |
| R584-9-S1 (`census()` indexes `defs[0]`) | RETAINED SUGGESTION (`ctrl_pin.py:573`) | source |
| R585-2-S2 (explicit `--stack` uses default `STACK_TESTS`) | RETAINED SUGGESTION (`aecp_arms.py:83`) | source |
| R584-8-S2, R584-8-S3, R584-3-S1 remainder, R585-5-S1 / R584-5-S3 | RETAINED SUGGESTION or documented limit; nothing in this delta touches them | source |
| R584-4-S2, R585-4-S1, R584-5-S2 (`firmware-unit` headroom) | RETAINED under #716. Hosted `firmware-unit` took 41 min 28 s of 45 at this head. | `receipts/hosted-checks.txt` |
| Historical figure-refresh suggestions (R584-4-S1 and peers) | RETAINED optional | - |
| R584-8-RES-1 | RETAINED RESIDUE for #495: `sw/firmware/ctrl/README.md:240` still reads `runs it, with GoogleTest and GoogleMock 1.14.0:` | source |
| R585-8-RS1, R584-7-RES1 / R585-7-RS1, R585-9 residue wording | RETAINED for the manager's #495 checklist | - |
| Earlier resolved findings (replacement, graft, filter, mode, symlink, figures, bench prerequisites, capture and boundary) | Still RESOLVED: their controls are `[ok]` at this head, locally and hosted | `receipts/pin-controls-head.log`, hosted boundary logs |

## Per-lens results

[R585] PASS Conformance - `third_party/tsn-c-stack` gitlink `405dc683`, `receipts/token-compare.txt`, `receipts/rv32-objects.txt`, `receipts/images-{dev,head}.sha256`, `receipts/merge-both-sides.txt`, issue #697 acceptance 1-5 and the round-13 assignment items 1-5 - The pin follows the 6092176555 rule (token-identical cores, byte-identical images). The ACMP core comes only from the submodule, and the lwSRP pin is dev's. Coverage is 100 % with dev's rows. Every plant dev's campaigns catch is caught. No firmware behaviour change: 35 of 35 images are equal.

[R585] PASS RTL - `git diff --stat c20c85bd HEAD -- '*.sv' '*.v' '*.svh' hdl rtl syn` (empty), `tb/verilator/mbx/Makefile` (`.PHONY` with `census` and `stack-pin`), `receipts/gates/mbx-bench.log` - The lane changes no HDL, clock, reset, CDC or mailbox ABI. The mailbox bench, including the firmware-on-RTL co-simulation, passes on Verilator 5.050, and its six RTL mutants are caught.

[R585] UNCLEAN Robustness - `ctrl_build.py:425-460`, `receipts/forge-probe.txt`, `receipts/fsmonitor-super-probe.txt`, `receipts/pin-controls-head.log` - F1 is open. The environment, replacement, graft, filter, mode and symlink states, and the stack clone's own fsmonitor, are each handled. The superproject fsmonitor is S1.

[R585] UNCLEAN Tests - `ctrl_pin.py:902` (`pin_controls`), `ctrl_pin_env.py`, `ctrl_mutants.py:585-645`, `receipts/pub-acmp-head.log`, `receipts/pin-controls-with-alternates.log` - The 11 retargeted plants each fail by name, and their no-op twins escape. 79 of 79 controls pass. No control covers the forged-subtree state (F1). S2 is optional.

[R585] PASS Docs - `docs/reference/SUBMODULES.md` (pin row, tag sentence, five-submodule init, test row), `sw/firmware/ctrl/README.md`, `sw/firmware/gtest/README.md`, `sw/firmware/ctrl/maap/README.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/testing/CI_WORKFLOWS.md`, `receipts/docs-subset.txt` - Every pinned link resolves at `405dc683`, and dev's F-INT README text is kept. The tag and `main` statements are true. The open routes are stated accurately. The docs, em-dash, TOC, path, diagram and submodule gates pass. PR-body wording items are RESIDUE RS1-RS4.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gitlink and remote refs; seven core files against dev by tokens and lines; 6 RV32 object pairs; 35 images dev against head; merge resolution of 22 files; acceptance 1-5 and round-13 items 1-5 | R585-12 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |
| RTL | CLEAN | lane diff against dev (no HDL); `tb/verilator/mbx/Makefile`; mbx bench and co-simulation on Verilator 5.050; hosted `firmware-verilator` | R585-12 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |
| Robustness | UNCLEAN (F1) | `stack_pin`/`stack_gitlink`/`git` (`ctrl_build.py:376-460`); forged-subtree, forged-commit and both fsmonitor probes; 79 pin controls; alternates-file control | R585-12 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |
| Tests | UNCLEAN (F1) | `ctrl_mutants.py` retarget; 15 `pub-acmp` plants with no-op twins, head against dev; `pin_controls`, `ctrl_pin_env.py`; `OUTSIDE` cross-check; firmware arms, coverage, MAAP differential, hosted campaign lines | R585-12 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |
| Docs | CLEAN | SUBMODULES.md, the firmware, gtest and MAAP READMEs, MAILBOX_SPLIT.md, CI_WORKFLOWS.md; 20 pinned links; docs-job gates; PR body (RESIDUE RS1-RS4) | R585-12 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |

## Real limits

- No manager source bank, builder bank or native bank was run or inferred. The source-head execution evidence beyond this round's own runs is the author's published gate receipts and the hosted jobs.
- This round did not complete the full boundary self-tests locally. `ctrl_boundary.py --selftest --without verilator` exceeded the 10-minute foreground limit; its firmware builder alone took 335 s, and the partial log is `receipts/gates/boundary.log` (rc 124, timeout). `--only verilator` was not run locally. Both are covered by the hosted `firmware-boundary` and `firmware-verilator` successes at this tree, which this round read but does not own.
- The full ctrl, AECP and SRP mutation campaigns were not re-run locally, only the 15 `pub-acmp` plants. The 506-of-506 figure is the hosted `firmware-unit` log's.
- The local host is not CI-parity: CPython 3.14.7, gcc 16.2.1, GoogleTest 1.18, Git 2.56.0. The hosted jobs carry CPython 3.12.3 and the runner toolchain.
- The RV32 runtime archives were built by this round from the local LiteX picolibc and compiler-rt sources, so SRP image hashes are comparable dev against head only, not with the author's table.
- The stack's own CMake suite was not run here. Its CI (`quality`, `bare-metal`) succeeded at `405dc683`.
- act was not run (not allowed). Physical calibration was NOT RUN; field skips are not hardware proof.

## Pending manager duties

- F1: obtain the fix (a) or the ruling (b), then a re-review of the resulting head.
- Exact-head hosted acceptance: Verilator shards 0, 1, 2 and 4, and the `verilator-suites` and `yosys-portability` aggregates, were still pending at 04:15 UTC.
- The current-dev merge candidate (builder and native banks) at the merge turn: source base `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8`, live dev `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8`.
- The act audited-install bootstrap for the new submodule manifest entry.
- RESIDUE RS1-RS4, and the carried R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1 and R585-9 wording, to #495.
- `firmware-unit` headroom (41.5 of 45 minutes hosted) stays with #716.

## Checkout integrity

- HEAD is `8aaa2da74e3d5ee569fed420debc2b69c6749d44`, and both the HEAD tree and the index tree are `cb90055f0843f221ceb6fecc20777cb24cea7f5a`. There are 0 status lines, the worktree equals HEAD, and 0 entries are assume-unchanged or skip-worktree.
- `third_party/tsn-c-stack` (`405dc683`) and `third_party/lwSRP` (`08ee86e8`) were initialised at their gitlinks and are clean. Every other submodule is unchanged at its gitlink. Receipt: `receipts/integrity-final.txt`.
- All builds, plants and probes ran in disposable clones under `scratch/`. No file of this clone was edited.

R585-12 FINISHED
