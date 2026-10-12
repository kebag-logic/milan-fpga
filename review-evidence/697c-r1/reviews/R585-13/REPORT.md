[R585] NEGATIVE - exact head a8fe548a083239efc799a79c540b2be63e9d13e7

# R585-13: external independent review of PR #705 (issue #697), round 14 delta

- Exact head `a8fe548a083239efc799a79c540b2be63e9d13e7`, tree `ee9efde299139ba3ac1d2a834b56497a54a1b231`. Delta reviewed: `8aaa2da7..a8fe548a` (four commits, six files under `sw/firmware/ctrl`). Source base `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8`.
- All five lenses were applied. Conformance and RTL are clean.
- One MINOR finding is open, under Robustness, Tests and Docs. A partial-clone promisor transport named in the stack's own configuration is still started by the proof's Git while the pin is decided. Round 14's published claim says no repository's own configuration does this.
- New items: one RESIDUE (a stale PR-body link) and three SUGGESTIONS.
- Everything the round-14 assignment asked this round to confirm holds at this head:
  - Every object the proof reads is hashed against its id and fails closed.
  - R585-12's F1 is refused by name before any build, and F0 and F2 keep their verdicts.
  - `-c core.fsmonitor=false` is present and has a standing control that can fail.
  - The S2 alternates control holds.
  - The PR-body residue is applied.
  - The 79 earlier pin controls and the environment controls hold, and no image input changed.
- The verdict is NEGATIVE only because of F1.

## Order of reconstruction

1. `AGENTS.md` and `CONTRIBUTING.md` (lenses, severities, completion ledger) and `docs/README.md`.
2. Issue #697: the frozen acceptance 1 to 5, the [round-12 scope ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461), the [round-13](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6116488747) and [round-14](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117713386) assignments, and the [round-14 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6118316100).
3. The diffs `8aaa2da7..a8fe548a` (line by line) and `c20c85bd..a8fe548a` (stat and history), then the code the delta calls into: `ctrl_build.py` (the helper, its audit hook and environment judge, `stack_gitlink`, `on_disk` and `stack_pin`), `ctrl_pin.py` (`pin_controls`, `Clone`, THE THREAT MODEL), `ctrl_pin_env.py` and the new `ctrl_pin_store.py`.
4. The PR body at the head and the published author evidence `review-evidence/697c-r1/author-r14/round14` at `ef056833`. I read these logs: `bjob-head.log`, `forge-probe-head.txt`, `model-routes-head.txt`, `super-fsmonitor.txt`, `store-mutants-head.log`, `tree-equiv-head.txt`, `image-table.md` and both `images-*-elf.sha256`.
5. Only after my own pass and probes did I read the prior findings: [R584-11](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6117711037) and [R585-12](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6117666847).

## Findings

### R585-13-F1 - MINOR - Robustness, Tests, Docs - a program named in the stack's own configuration (a partial-clone promisor transport) is still started by the proof's Git while the pin is decided; the round's published claim says no repository's own configuration does so

- **Artifact:**
  - `sw/firmware/ctrl/test/ctrl_build.py:385`: the helper adds only `-c core.fsmonitor=false`.
  - `ctrl_build.py:187` (`GIT_ENVIRONMENT`): nothing disables lazy fetching.
  - `ctrl_build.py:435-446` (`stored`, `git cat-file <type> <id>`, which fetches a missing object from a promisor remote).
  - PR body `## Status`, third line: "every Git command of the proof runs with `core.fsmonitor=false`, so no repository's own configuration starts a program while the pin is decided".
  - Commit `b62c1981`'s subject says the same.
- **Authority/evidence:**
  - The [round-12 ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461), item 2: "The pin proof's threat model is the state it reads: the checkout's files and modes, Git's object store, refs, configuration and attributes, and the environment the proof inherits."
  - The [round-14 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117713386) closed a route of the same model "closed, not narrowed". Its item 2 stated the aim: the repository's configuration "starts no program while the proof decides".
  - The probe (`scripts/forge_probes.sh`, receipt `receipts/forge_probes.log`, Git 2.56.0) sets up the stack clone's own `.git/config` with:
    - `extensions.partialClone=probe`, `remote.probe.promisor=true`, `remote.probe.url=ssh://probe.invalid/x`;
    - `core.sshCommand=<recorder>`;
    - one pin object (the `src/` tree) absent from the store.
  - Results:
    - **P13:** the head's CLI (`ctrl_build.py --stack-pin`) exits 2, but the recorder ran 2 times while the pin was decided. At `8aaa2da7`: the same.
    - **P14:** the recorder serves the missing object (`git upload-pack` of an intact store) and leaves a process behind. The head's proof exits 0 (`tsn-c-stack at 405dc683…`). Two seconds later `src/adp.c` is edited, and a second run of the proof refuses it. A build that starts after the first verdict reads edited stack code.
  - `scripts/lazy_fetch_env.sh` (`receipts/lazy_fetch_env.log`) passes Git exactly the proof's environment and arguments: the transport program runs 2 times. With `GIT_NO_LAZY_FETCH=1` added it runs 0 times on Git 2.56.0. That variable's support on the runner's Git (Ubuntu 24.04) was not checked.
  - The in-tree texts limit their claim to index reads (`README.md:175`, `ctrl_pin.py:62-63`, `ctrl_pin_store.py:21-22`), and `README.md:191` says what Git itself starts is outside the hook. No text lists this route as open, though, and the PR body states the whole class closed.
- **Impact:**
  - The class this round closed for `core.fsmonitor` stays open by another setting of the same repository configuration. The class is a program that in-model state makes Git start while the proof decides.
  - At decision time the verdict is correct: the fetched object is genuine, and the proof hashes it.
  - But the started program can act after the verdict (P14). That defeats "every gate builds the pinned stack or none" in the same way the superproject's `core.fsmonitor` could, and that route was required closed this round.
  - Exposure is local: it takes write access to `.git/modules/third_party/tsn-c-stack/config` and its store. A hosted fresh checkout is not a partial clone.
  - Why MINOR and not a SUGGESTION, unlike R585-12-S1:
    - R585-12-S1 judged the `fsmonitor` start harmless because the verdict stayed correct. P14 shows that a configuration-started program changes what is built after a correct verdict.
    - Round 14 publishes the whole class as closed.
- **Required outcome:** one of these, recorded publicly:
  - (a) No program named by a repository's own configuration starts while the pin is decided, the transport or helper of a promisor remote included. For example, lazy fetching is disabled on the runner's Git, or a stack whose repository names a promisor remote is refused before any object is read. A standing pin control holds it: a promisor remote whose transport is a recorder, beside a missing pin object. It must end in a named refusal (or the clone's own verdict) with 0 program starts, and must escape when the protection is removed.
  - (b) A maintainer ruling that narrows the model, for example "programs Git starts through a repository's fetch or transport configuration are out of scope". The README, `ctrl_pin.py`'s THE THREAT MODEL and the PR body then state the narrowed model.
  - Under either, the PR body Status line must claim no more than holds. This review does not prescribe the design.
- **Verification:**
  - For (a): `forge_probes.sh` P13 and P14 report 0 recorder runs, and P14 does not end in "exit 0 … later edit: edited". The new control is `[ok]` and the other 84 are `[ok]`. Check on the runner's Git version.
  - For (b): the ruling's link, and the three texts consistent with it.

### RESIDUE (PR body wording only; exact fix for the manager's checklist)

- **R585-13-RES-1 - Docs** - PR body `## Authoritative references`, fourth bullet: the `[Control firmware]` link pins `8aaa2da74e3d5ee569fed420debc2b69c6749d44`. This round changed that page, and the pinned copy still reads "79 pin controls" and "Two routes within the model are open". The other four links in that bullet name pages unchanged since `8aaa2da7`. Exact fix: in the `[Control firmware]` link only, replace `8aaa2da74e3d5ee569fed420debc2b69c6749d44` with `a8fe548a083239efc799a79c540b2be63e9d13e7`.

### SUGGESTIONS (optional, no effect on the verdict)

- **R585-13-S1 - Tests** - `ctrl_pin_store.py:154-165`. No standing control forges the pinned **root** tree.
  - Mutant M4 (`receipts/mutants.log`) reads only the root tree unhashed, and all 84 controls stay `[ok]`.
  - The head refuses a forged root tree (`forge_probes.sh` P3) and a forged depth-2 tree (P5), so the code is right. The check simply has no control of its own.
  - A sixth store control forging the root tree, or a deeper tree, would hold it.
- **R585-13-S2 - Tests** - `ctrl_pin_store.py:107-110,163-164`. The stack's own `core.fsmonitor` control cannot fail if the `-c` setting is removed: the proof reads no index of the stack.
  - P11 shows 0 starts at both `8aaa2da7` and the head, and mutant M2 trips only the superproject control. The author's evidence says the same.
  - It is a fair guard against a future index read, and the docstring could say so.
- **R585-13-S3 - Robustness** - `ctrl_build.py:441`. When the pinned commit cannot be read, the refusal reads "cannot read the pinned tree of <stack>: the pinned commit (commit 405dc683): …" (seen in `receipts/pin_controls_head.log`, the `GIT_ALTERNATE_OBJECT_DIRECTORIES` control). "cannot read the pin of …" or "cannot read an object of …" would fit both kinds. This is a code string, so it is a SUGGESTION, not residue.

## What was confirmed at this head

| Item | Result | Receipt |
|---|---|---|
| Every object read is checked against its id, failing closed | `pinned_tree` reads the commit and every tree raw through `stored`. It hashes `<type> <len>\0<raw>` with the repository's object format and refuses a mismatch by place. No blob is read; files are hashed from disk (`blob_id`). Forged objects are refused by place: `src/` subtree (P2), root tree (P3), commit (P4), depth-2 tree `.github/workflows/` (P5), and a commit stored under the `src/` tree's id that peels to a forged tree (P7). So is a forged tree served from an alternate store (P8). A corrupt object (P9) and a missing one (P10) fail closed. A forged blob is refused by the file's name (P6). At `8aaa2da7` P2, P5 and P8 are accepted. | `receipts/forge_probes.log` |
| R585-12 F1 refused by name before any build; F0 and F2 keep their verdicts | F1 (P2, and the control "the pinned src/ tree's object overwritten…") is refused: "…holds a forged or corrupt object: the pinned src/ tree (tree 5c8c189a)…". F0 (P1) is refused naming `src/adp.c`. F2 (P4) is refused, now by name. The author's run of the unchanged `forge_probe.py` (`forge-probe-head.txt`) agrees. | `receipts/forge_probes.log`, `receipts/pin_controls_head.log` |
| The controls can fail | M1 (no hash compared): the forged-tree and forged-commit controls escape. M3 (trees unhashed): the forged-tree control escapes. M5 (commit unhashed): the forged-commit control escapes. M6 (no subtree walked): 30 controls escape. M4: see S1. File bytes were restored after every mutant. | `receipts/mutants.log` |
| `-c core.fsmonitor=false` with a standing control | The superproject `core.fsmonitor` gives 2 recorder starts at `8aaa2da7` and 0 at the head (P12). Mutant M2 (setting removed): the superproject control escapes. | `receipts/forge_probes.log`, `receipts/mutants.log` |
| R585-12-S2 taken | With the stack submodule initialised by `--reference` (its `objects/info/alternates` names another store), 84 of 84 are `[ok]`, the alternates control included. | `receipts/pin_controls_head_reference.log` |
| The 79 pin controls and the environment controls hold | At the head: 84 of 84 `[ok]`, census 0 findings, README figures equal, 4 of 4 figure controls. This holds on CPython 3.14.7 and on 3.12.3 (3.12 ran with a pure-Python PyYAML on its import path). At `8aaa2da7`: 79 of 79. Every one of the 79 labels is `[ok]` at the head, and the only new labels are the five store controls. | `receipts/pin_controls_head.log`, `receipts/pin_controls_head_py312.log`, `receipts/pin_controls_8aaa2da7.log`, `receipts/pin_control_labels_diff.txt` |
| Images unchanged | The delta touches only `README.md`, `ctrl_build.py` (helper I/O and pin functions; no build function), `ctrl_configs.py` (`GATE`, the gate's own modules, now with `ctrl_pin_store.py`), `ctrl_pin.py`, `ctrl_pin_env.py` and the new `ctrl_pin_store.py`. No C, H, assembly, linker, Makefile, CMake or workflow file. The author's manifests at dev `c20c85bd` and at the head are byte-identical (35 of 35 ELF hashes). I did not rebuild the images. | `git diff --name-only 8aaa2da7..a8fe548a`; published `images-*-elf.sha256` |
| PR-body residue | R585-12-RS1 / R584-11-RES-1 ("not pushed" gone from Status), RS2 (Definition of Done names `405dc683` and comment 6116488747), RS3 (links moved to `8aaa2da7`; see RES-1) and RS4 (`firmware-boundary` needs CMake and Clang) are applied. | PR body at review time |
| Docs checks of the delta | `docs_check.py`: 0 findings. `check_py_idiom.py`: every ratchet held. 0 added lines in the delta carry an em dash, counted by hand: `check_em_dash.py` could not run because its pinned renderer's dependencies are missing here. `README.md:209` "84 pin controls" equals the self-test's count. | `receipts/docs_checks.log` |

## Prior public findings at this head

| Prior finding | Status | Evidence |
|---|---|---|
| R585-12-F1 = R584-11-F1 (MINOR: forged `src/` tree accepted) | RESOLVED: refused by place, with a standing control that can fail | P2, P5, P8; M1, M3 |
| R585-12-S1 (superproject `core.fsmonitor`) | RESOLVED: 0 starts, with a standing control that can fail. The wider class is R585-13-F1. | P12; M2 |
| R585-12-S2 (alternates control with `--reference`) | RESOLVED | `pin_controls_head_reference.log` |
| R585-12-RS1 to RS4, R584-11-RES-1 | APPLIED in the PR body. RS3's target is now one round stale for one link: R585-13-RES-1. | PR body |
| R584-11-S1 (pin-only commit `c03e9c9c` not buildable) | RETAINED SUGGESTION, optional, not taken (needs history rewrite) | history |
| R584-9-S1 (`census()` indexes `defs[0]`) | RETAINED SUGGESTION, now `ctrl_pin.py:579` | source |
| R585-2-S2 (explicit `--stack` uses default `STACK_TESTS`) | RETAINED SUGGESTION, `aecp_arms.py:83` | source |
| R584-8-RES-1 | RETAINED RESIDUE for #495: `sw/firmware/ctrl/README.md:248` still reads "runs it, with GoogleTest and GoogleMock 1.14.0:" | source |
| R585-8-RS1, R584-7-RES1 / R585-7-RS1, R585-9 residue wording, other carried optional suggestions and `firmware-unit` headroom (#716) | RETAINED as carried. Nothing in this delta touches them; not re-verified one by one. | - |

## Per-lens results

[R585] PASS Conformance - `git diff --name-only 8aaa2da7..a8fe548a` (six files, none firmware, build, workflow or pin), `receipts/forge_probes.log` P1/P2/P4/P12, `receipts/pin_controls_head.log`, `receipts/pin_control_labels_diff.txt`, the PR body - Checked against #697 acceptance 1 to 5 (unchanged by a delta that touches no core, adapter, image input or gitlink; the pin is `405dc683`) and round-14 items 1 to 4. Item 1 is met (every object read is hashed, F1 is refused by name before any build, F0 and F2 refused). Item 2 is met as asked (`-c core.fsmonitor=false`, with a superproject control). Item 3 is taken. Item 4 is applied. The round-12 ruling is respected: no finding here relies on code inside the proof's modules.

[R585] PASS RTL - `sw/firmware/ctrl/test/ctrl_build.py:196-205,376-390,428-490`, `ctrl_pin.py:156-198,245,977-991`, callers `ctrl_pin.py:789` and `ctrl_pin_env.py:56`, the `8aaa2da7..a8fe548a` stat (0 HDL, SV, testbench or synthesis files) - No clock, reset, CDC, FSM or width change.
- The helper's interface change is consistent in every caller, exercised by 84 controls on CPython 3.12.3 and 3.14.7. The change: bytes I/O, with stdout and stderr decoded as UTF-8 with `surrogateescape` as before, `stdin` encoded the same way, and a new `raw` field.
- The audit hook's judge (program and environment) is unchanged. The census vocabulary widening (`bytes`, `append`, `decode`, `hex`, `partition`, `pop`, `raw`) adds no reach to a launch facility. Census: 0 findings.
- `pinned_tree` parses `<mode> <name>\0<id>` with the id width taken from the pin's length. It maps modes as `ls-tree` prints them (`40000` to `040000`), giving 89 entries equal to `ls-tree -r -t` (author's `tree-equiv-head.txt`). It recurses only into hash-verified trees, so it cannot loop.

[R585] FAIL Robustness - R585-13-F1 (`ctrl_build.py:385`, `:187`, `:435-446`; `receipts/forge_probes.log` P13/P14; `receipts/lazy_fetch_env.log`). The other robustness paths applied were clean:
- forged objects in subtree, root tree, commit, depth-2 tree, type confusion and alternate store (P2-P5, P7, P8);
- corrupt and missing objects, which fail closed (P9, P10);
- the superproject and stack `core.fsmonitor` (P11, P12);
- a `--reference` stack.

[R585] FAIL Tests - R585-13-F1: no control holds the promisor-transport route, and the class claim is untested. Otherwise:
- the five new controls are `[ok]`, and four of them fail under the matching mutant (M1, M2, M3, M5);
- the 79 earlier controls are unchanged and `[ok]`;
- the figure check holds at 84.
S1 and S2 are optional.

[R585] FAIL Docs - R585-13-F1: the PR body Status line claims more than holds. RES-1 is residue. The in-tree texts (`README.md:172-175,209,230-235`, `ctrl_pin.py:45-64,125-130`, `ctrl_pin_store.py:3-28`) agree with the code at their stated scope. `docs_check.py` finds 0.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #697 acceptance 1-5; round-12 ruling; round-14 items 1-4; delta file list; P1/P2/P4/P12; 84-control log; label diff; PR body | R585-13 | a8fe548a083239efc799a79c540b2be63e9d13e7 |
| RTL | CLEAN | `ctrl_build.py:196-205,376-390,428-490`; helper callers `ctrl_pin.py:789`, `ctrl_pin_env.py:56`; census; delta has 0 HDL/SV/syn files | R585-13 | a8fe548a083239efc799a79c540b2be63e9d13e7 |
| Robustness | UNCLEAN (F1) | `ctrl_build.py:187,385,435-490`; P0-P14; `lazy_fetch_env.log`; `--reference` run | R585-13 | a8fe548a083239efc799a79c540b2be63e9d13e7 |
| Tests | UNCLEAN (F1) | `ctrl_pin_store.py`; `ctrl_pin.py:977-991`; 84 controls on 3.14.7 and 3.12.3; 79 at `8aaa2da7`; mutants M1-M6 | R585-13 | a8fe548a083239efc799a79c540b2be63e9d13e7 |
| Docs | UNCLEAN (F1; RES-1 residue) | `README.md:165-239`; `ctrl_pin.py:45-64`; `ctrl_pin_store.py:3-28`; PR body Status, Round 14, Authoritative references, Known limitations, Definition of Done; `docs_checks.log` | R585-13 | a8fe548a083239efc799a79c540b2be63e9d13e7 |

## Real limits of this round

- I did not run these, and the round relies on the author's published receipts for them:
  - the boundary self-test (`ctrl_boundary.py --selftest`, either half);
  - the `firmware-unit` steps, the mutation campaigns, coverage, the Verilator suites, the image builds and `ctrl_image.py --base`;
  - the hook-rule campaign (H1-H24), the entry-point campaign, and the docs job's 54 commands.
- `check_em_dash.py` could not run because its pinned renderer's dependencies are missing here, so the em-dash count was done by hand. Scoped Verilator was not needed and not used.
- I ran the pin controls alone with `scripts/run_pin_controls.py`. It calls `ctrl_pin.pin_controls` and the README figure check exactly as `ctrl_boundary.py --selftest` does, but without the gate's builds.
- Probes ran on Git 2.56.0. The promisor route (F1) was not run on the runner's Git (Ubuntu 24.04). Lazy fetching of a missing object from a promisor remote is long-standing partial-clone behaviour, but I did not run it there.
- Forgeries were planted as loose objects and in an alternate store, not inside a pack. The check reads `cat-file` output, which is the same whichever way the object is stored.
- The proof hashes SHA-1 with the plain algorithm, not Git's collision-detecting one. Passing a forged object still needs a second preimage of a pinned id, as the PR body's Known limitations states.
- Hosted evidence: no check run, status or workflow run exists for `a8fe548a` (`receipts/hosted_checks_a8fe548a.txt` is empty; `receipts/hosted_runs_a8fe548a.txt`: 0 runs). The PR reports `mergeable: CONFLICTING` (`receipts/pr_state.json`).
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Rule on or route F1 (fix (a) or model ruling (b)), and carry RES-1 to the residue checklist.
- Current-dev merge candidate. Live dev `c6bd08c6` contains `c20c85bd`. A merge-tree of the head with it conflicts only in `docs/diagrams/PNG_MANIFEST.json`, `submodule_boundaries.drawio` and `submodule_boundaries.png` (`receipts/merge_tree_live_dev.txt`); these are generated, and their generator remakes them. The manager builds and validates the candidate (builder and native banks, images against dev) at the merge turn.
- Hosted `rtl-fast` and exact-head `verilator-suites` / `yosys-portability`, and the act replica, on the published candidate head. None ran at this head.
- Merge requires two independent positive reviews and the full completion bar. This round's ledger has Robustness, Tests and Docs unclean.

Scratch clones under `scratch/` were disposable. Afterwards the review clone was verified byte-identical to the head (`receipts/clone_integrity.txt`):
- index tree equal to the head tree;
- 1291 tracked blobs hashed from disk, 0 differing;
- 0 status entries;
- all six gitlinks as recorded.

R585-13 FINISHED
