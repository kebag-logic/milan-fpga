[R584] NEGATIVE - exact head a8fe548a083239efc799a79c540b2be63e9d13e7

Internal independent review R584-12 of issue #697 / PR #705. This is the delta review of round 14 ([A583]): four commits on `8aaa2da7` (`d89898db`, `b62c1981`, `4a35f2f4`, `a8fe548a`). Head tree `ee9efde299139ba3ac1d2a834b56497a54a1b231`.

All five lenses were applied. Conformance and RTL are clean. One MINOR finding is open, R584-12-F1, under Robustness, Tests and Docs. The verdict is NEGATIVE only because of F1.

Every item the round-14 assignment asks this review to confirm holds at this head:
- Every object the pin proof reads is hashed against its id, and a forged or corrupt one fails closed. That covers the pinned commit and every tree under it. No blob is read.
- R585-12's `forge_probe.py` F1 is refused by the forged tree's place, and F0 and F2 keep their REFUSED verdicts.
- The helper passes `-c core.fsmonitor=false`, and a standing control fails without it.
- The PR-body residue is applied.
- All 84 pin controls hold, the 79 earlier ones and the environment controls among them.
- The delta changes no image input.

F1 is a second route in the same class as the `core.fsmonitor` route this round closed. The class is a program that a repository's own configuration names, started by Git while the pin is decided. When an object the proof reads is missing from the stack's store, and the stack's own configuration declares a promisor remote, Git fetches the object lazily. That fetch runs the program the configuration names (`remote.<name>.uploadpack`, or `core.sshCommand`), inside `stack_pin`. The route existed at `8aaa2da7` and is unchanged by this round. The PR body now states that this class is closed.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`.
2. Issue #697:
   - the body and its frozen acceptance 1 to 5;
   - the owner decisions 6074086970, 6074093506, 6074191062, 6074811248 and 6074877336;
   - the lane assignment 6091228902 and the pin ruling 6092176555;
   - the round-12 ruling 6114400461, the round-12 STOP 6115091316, the round-13 assignment 6116488747;
   - the round-14 assignment 6117713386 and the REVIEW READY 6118316100.
3. `git diff 8aaa2da7..a8fe548a`, commit by commit, then the touched functions in full: `ctrl_build.py:179-494`, `ctrl_pin_store.py`, `ctrl_pin_env.py:1-160`, and `ctrl_pin.py:1-160,905-995`.
4. Executable evidence of this round (below).
5. Only after this round's own pass over the diff and its own probes: the prior findings R584-11 (6117711037) and R585-12 (6117666847), their published probes, the PR body and the author's round-14 logs at `ef056833:review-evidence/697c-r1/author-r14/round14/logs/`.

## What the assignment asks, confirmed at this head

| Item | Result | Receipt |
|---|---|---|
| 1. Every object the proof reads is checked against its id, failing closed | `ctrl_build.stored` (`ctrl_build.py:435-446`) reads `git cat-file <kind> <oid>` as bytes, hashes `<kind> <len>\0<raw>` with the repository's object format, and raises `Refusal` on a mismatch or a failed read. `pinned_tree` (`:449-468`) walks the pinned commit and every tree through `stored`. For the pin it gives the same 89 entries as `ls-tree -r -t` (`receipts/tree_equivalence_head.txt`). Each file is hashed from its own bytes (`blob_id`), so no blob is read. This round's own probes, on clones with every object loose, under CPython 3.14.7 and 3.12.13 (see the list after this table): 0 of 13 forged, swapped, corrupt or missing states accepted. | `receipts/store_probe_head_py314.txt`, `receipts/store_probe_head_py312.txt` |
| The hash check can fail, and Git does not do it | With the comparison removed (mutant `no-hash`), the store controls for the forged `src/` tree and the forged commit both escape, `accepted 405dc683…` (3 of 5 held). All 7 of this round's forged-object probes are then ACCEPTED. With a wrong type header (`wrong-header`), every genuine object is refused. At `8aaa2da7` the forged `src/` tree is ACCEPTED. | `receipts/store_arms_mutant_no-hash.txt`, `receipts/store_probe_mutant_no_hash.txt`, `receipts/store_arms_mutant_wrong-header.txt`, `receipts/store_probe_base_8aaa2da7.txt` |
| R585-12 `forge_probe.py`, unchanged | F0 REFUSED `src/adp.c`. F1 REFUSED: `the pinned src/ tree (tree 5c8c189a) hashes to 9b48fa40, not to its id`. F2 REFUSED: `the pinned commit (commit 405dc683) hashes to 55f2ca0d`. F3 ACCEPTED, program ran 0 times. `stack_pin` runs before any build in every gate, and this round's 84 pin controls show it. | `receipts/forge_probe_head.txt` |
| R584-11 `model_routes.sh`, unchanged | Clean: exit 0. Edit: exit 2 naming `src/adp.c`. Route 1: exit 2, naming the forged `src/` tree, not `src/adp.c` (see prior findings). Route 2: exit 0, 0 recorder lines. | `receipts/model_routes_head.txt` |
| 2. `-c core.fsmonitor=false`, with a standing control | The helper is `["git", "-c", "core.fsmonitor=false", "-C", …]` (`ctrl_build.py:385`). Its environment is still exactly `GIT_ENVIRONMENT`, and the hook's judge is unchanged. This round's superproject probe gives 0 starts at the head and 2 at `8aaa2da7`. With the setting removed (mutant `no-fsmonitor-off`), the in-tree superproject control escapes (4 of 5 held). | `receipts/store_probe_head_py314.txt`, `receipts/store_probe_base_8aaa2da7.txt`, `receipts/store_arms_mutant_no-fsmonitor-off.txt` |
| 3. R585-12-S2 (optional, taken) | `unstored` (`ctrl_pin_env.py:145-151`) also unlinks `objects/info/alternates`. Checked by reading the code. It was not re-executed with a `--reference` initialisation. | source |
| 4. PR-body residue | R585-12-RS1 / R584-11-RES-1: the Status line no longer says "not pushed". RS2: the DoD line reads "pin `405dc683` set by #697 comment 6116488747 under the rule of comment 6092176555". RS3: the five links of the fourth reference bullet name `8aaa2da7…`. RS4: "The hosted `firmware-boundary` job needs CMake and Clang…". | PR body (as updated 2026-10-12T05:37:26Z) |
| The 79 pin controls and the environment controls hold | `ctrl_pin.pin_controls` was run alone, with the boundary gate's own Makefile list. CPython 3.14.7: 84 controls, 0 misbehaved. CPython 3.12.3: 83 `[ok]`; the one `ESCAPED`, the AECP wire comparison, is this host's child interpreter lacking PyYAML (`ModuleNotFoundError: No module named 'yaml'`), not the code. The head's 5 store controls, run alone, hold 5 of 5 on 3.14.7 and on 3.12.13. The README figure `84 pin controls` (`README.md:209`) equals the count. | `receipts/pin_controls_head_py314.txt`, `receipts/pin_controls_head_py312.txt`, `receipts/store_arms_head_py314.txt`, `receipts/store_arms_head_py312.txt` |
| Images unchanged | The delta touches six files: five pin-proof and control scripts under `sw/firmware/ctrl/test/` and the README. No firmware source, header, build flag, builder, Makefile, workflow or gitlink changed. In `ctrl_build.py` only the Git helper, `stored`, `pinned_tree` and `stack_pin` changed, not `C_FLAGS` or the compile functions. The head's `ctrl_image.py` built all 5 shapes with rc 0 and printed `tsn-c-stack at 405dc683…`. The author's published manifests for dev `c20c85bd` and the head are byte-equal, 35 of 35, and the head manifest's sha256 is `8b1292db…`, as the REVIEW READY states. | `receipts/ctrl_image_head.log`, `receipts/ctrl_image_head_elf.sha256`; `ef056833:…/round14/logs/images-{dev-c20c85bd,head}-elf.sha256` |
| Self-review commit `a8fe548a` | `forge` writes `<oid>.forged`, then `replace()`s the loose file, so no inode shared through a hard link is written. `loose()` refuses a clone that keeps a pack or an alternates file. | source |
| Docs gates | `docs_check.py`: 0 findings. `check_em_dash.py --base c20c85bd` (pinned renderer venv): 0 findings over 409 added lines. `check_py_idiom.py`: every ratchet held; `--selftest` 54 of 54. | `receipts/docs_gates_head.txt` |

The 13 states in the head probes:
- forged `src/` tree, root tree and pinned commit;
- forged deepest tree (`examples/rv32/include`);
- forged blob, which is refused by name: `src/adp.c`;
- annotated tag in place of the pinned commit (peeled by `cat-file commit`);
- commit in place of the `src/` tree (peeled by `cat-file tree`);
- forged object served from an `objects/info/alternates` store;
- truncated zlib, trailing bytes and a missing object;
- `core.worktree`, which fails closed;
- the stack's own `core.fsmonitor`.

## Findings

### R584-12-F1 - MINOR - Robustness, Tests, Docs - Git's lazy fetch, configured by the stack's own repository, starts a program that configuration names while the pin is decided; no control holds it, and the PR body states the class is closed

- **Artifact:**
  - `sw/firmware/ctrl/test/ctrl_build.py:187-188`: `GIT_ENVIRONMENT`, which disables replacement objects, grafts and system or global configuration, but not lazy fetching from a promisor remote.
  - `sw/firmware/ctrl/test/ctrl_build.py:385` (the helper) and `:439` (`stored`'s `cat-file`, the first read of an object the store lacks).
  - `sw/firmware/ctrl/test/ctrl_pin_store.py:154` (`store_arms`): no control holds this route.
  - The PR body:
    - Status, second bullet: "every Git command of the proof runs with `core.fsmonitor=false`, so no repository's own configuration starts a program while the pin is decided";
    - Contents, the Round 14 line: "how no repository's own configuration starts a program while the pin is decided".
- **Authority/evidence:**
  - The [round-12 ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461), item 2, puts "Git's object store, refs, configuration and attributes" inside the pin proof's threat model.
  - The proof's own controls require that no program a configuration names may run:
    - `ctrl_pin_env.py:25`: "no program the configuration names may run";
    - `ctrl_pin_store.py` docstring: "the recorder never runs".
  - The [round-14 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117713386), item 2, asks that configuration start no program while the proof decides.
  - `scripts/store_probe.py`, at the head, on Git 2.56.0, under CPython 3.14.7 and 3.12.13. Setup:
    - a loose-object clone of the pinned stack has its `src/` tree object removed;
    - its own `.git/config` sets `extensions.partialClone=origin` and `remote.origin.promisor=true`;
    - the program is named through `remote.origin.uploadpack` (a local path URL) or `core.sshCommand` (an `ssh://` URL).
  - Results:
    - `lazy_uploadpack_fail`: REFUSED (`Could not read from remote repository`), `RAN=1`;
    - `lazy_ssh`: REFUSED, `RAN=2`. The recorder logged `example.invalid git-upload-pack '…/full'`;
    - `lazy_uploadpack_serve`, where the program then runs the real `git upload-pack`: ACCEPTED `405dc683…`, `RAN=1`;
    - `lazy_toctou`, the same, with the program also leaving a process that appends to `src/adp.c` three seconds later: ACCEPTED, `RAN=1`. Afterwards `src/adp.c` holds the plant, and a second check refuses it (`differs from the pinned 405dc683: src/adp.c`).
  - Through the command-line entry point the Makefile builders use (`ctrl_build.py --stack-pin`), the `lazy_ssh` state exits 2, and the recorder ran twice more (`receipts/lazy_fetch_cli.txt`).
  - The route predates this round. At `8aaa2da7` the same probes give `RAN=1`, `RAN=2` and an ACCEPT (`receipts/store_probe_base_8aaa2da7.txt`).
  - A fix is feasible. In a disposable mutant whose `GIT_ENVIRONMENT` also sets `GIT_NO_LAZY_FETCH=1`, every lazy probe gives `RAN=0` and is refused, the clean clone is accepted, and the audit hook accepts the environment (`receipts/store_probe_remedy_no_lazy_fetch.txt`). That is on Git 2.56.0 only; whether the runner's Git 2.43 honours that variable was not tested.
- **Impact:**
  - The state is in scope: a stack store missing one pinned object, plus a repository configuration declaring a promisor remote. In that state the pin decision runs an arbitrary program the configuration names, with the gate's privileges.
  - The verdict at that instant stays correct, because a fetched object is hashed like any other. But the program can change the checkout after it has been hashed. `lazy_toctou` shows the proof accept, and an edited `src/adp.c` then sits in the tree the gate builds. This is the same consequence for which the round-14 assignment required `core.fsmonitor=false`.
  - The PR body states the whole class closed. A maintainer reading Status would take the property as held.
  - The README (`README.md:175`) and the docstrings (`ctrl_pin.py:62`, `ctrl_pin_store.py`) claim only the index-read case, and are accurate.
- **Required outcome:** one of these, recorded publicly. This review does not prescribe the design.
  - (a) No program a repository's own configuration names runs while the pin is decided, lazy fetch included, failing closed. A standing pin control plants a missing pinned object and a promisor configuration naming a recorder. It must end in a refusal with the recorder never run, and must fail when the protection is removed.
  - (b) A maintainer ruling that narrows the protected property, for example to `core.fsmonitor` only. The PR body's Status and Contents lines then state the narrower property in place of "no repository's own configuration starts a program while the pin is decided".
- **Verification:**
  - For (a): `scripts/store_probe.py` `lazy_uploadpack_fail`, `lazy_uploadpack_serve`, `lazy_ssh` and `lazy_toctou` give `RAN=0` at the corrected head, on the runner's Git 2.43 and on 2.56. The new control is `[ok]`, and `ESCAPED` under its mutant. `pin_controls` stays 0 misbehaved, with the README figure equal to the count.
  - For (b): the ruling's link, and the PR body's lines consistent with it.

### R584-12-S1 - SUGGESTION - Tests - the stack's own `core.fsmonitor` control cannot fail for the loss of the setting at this head

`ctrl_pin_store.py:107` (`monitored_stack`). The proof reads no index of the stack, so Git starts no fsmonitor there with or without `core.fsmonitor=false`. Under mutant `no-fsmonitor-off` this control stays `[ok]` (`receipts/store_arms_mutant_no-fsmonitor-off.txt`). At `8aaa2da7`, with no setting, the same state gives 0 starts (`receipts/store_probe_base_8aaa2da7.txt`). The control guards a future read of the stack's index, which is legitimate. The REVIEW READY claims only that the superproject control escapes under the mutant. This is optional: say in the docstring that the control guards a future read of the stack's index, or give it a state in which the proof reads that index.

### R584-12-RES-1 - RESIDUE - Docs - the PR body's reference links name `8aaa2da7`, whose firmware README predates round 14

- **Artifact:** PR body, "Authoritative references", fourth bullet: the [Control firmware], [firmware harness], [submodule map], [CI workflow policy] and [mailbox bench] links name `8aaa2da74e3d5ee569fed420debc2b69c6749d44`.
- **Evidence:** at `8aaa2da7`, `sw/firmware/ctrl/README.md` says "79 pin controls" and "Two routes within the model are open, for a decision". The head's page says 84, and those routes are closed.
- **Exact fix:** replace `8aaa2da74e3d5ee569fed420debc2b69c6749d44` with `a8fe548a083239efc799a79c540b2be63e9d13e7` in those five links. This is link wording only; no measurement, figure, verdict, test, code or claim depends on it.

## Prior public findings at this head

| Prior finding | Status | Evidence |
|---|---|---|
| R584-11-F1 = R585-12-F1 (MINOR: a forged `src/` tree accepted an edited `src/adp.c`) | RESOLVED by option (a). Every object read is hashed against its id, failing closed; standing controls exist and fail under the `no-hash` mutant. R584-11's verification asked for a refusal naming `src/adp.c`. The refusal names the forged object by place (`the pinned src/ tree`) instead, before any build. That is the most the proof can honestly name, since the only listing of that tree the store holds is the forged one. The round-14 assignment asks for refusal "by name", and the place and id satisfy it. | `receipts/forge_probe_head.txt`, `receipts/model_routes_head.txt`, `receipts/store_arms_mutant_no-hash.txt` |
| R585-12-S1 (superproject `core.fsmonitor`) | RESOLVED: 0 starts at the head (2 at `8aaa2da7`), with a standing control that fails without the setting | `receipts/store_probe_head_py314.txt`, `receipts/store_arms_mutant_no-fsmonitor-off.txt` |
| R585-12-S2 (alternates inherited from `--reference`) | RESOLVED (taken), by code reading (`ctrl_pin_env.py:151`); not re-executed with `--reference` | source |
| R585-12-RS1 to RS4, R584-11-RES-1 | RESOLVED: applied in the PR body, as listed above | PR body |
| R584-11-S1 (`c03e9c9c` not a buildable state) | RETAINED SUGGESTION, not taken (it needs a history rewrite) | REVIEW READY |
| R584-9-S1 (`census()` indexes `defs[0]`) | RETAINED SUGGESTION, now `ctrl_pin.py:579` | source |
| R584-8-RES-1 | RETAINED RESIDUE for #495: `README.md:248` still reads "runs it, with GoogleTest and GoogleMock 1.14.0:" | source |
| R585-8-RS1; R584-7-RES1 / R585-7-RS1; R585-9 residue wording; R585-2-S2 and the other retained suggestions R585-12 lists | RETAINED as carried; nothing in this delta touches them; not re-verified one by one | - |
| R584-10-F1 | Still RESOLVED by the round-12 ruling; the threat-model texts are kept (`ctrl_pin.py:45-63`, `README.md`) | source |

## Per-lens results

[R584] PASS Conformance - `ctrl_build.py:385,435-494`, `ctrl_pin_env.py:145-151`, the PR body (Status, DoD, references, Known limitations), `receipts/forge_probe_head.txt`, `receipts/pin_controls_head_py314.txt`, `git diff --stat 8aaa2da7..a8fe548a` - Checked against round-14 items 1 to 4 and #697 acceptance 1 to 5. Item 1: every read object is hashed against its id, and F1 is refused with F0 and F2 unchanged. Item 2: the setting and its control are present, and the superproject starts no program. Item 3: taken. Item 4: residue applied. The delta changes no image input, gitlink, plant or coverage row, and the author's manifests are 35 of 35 equal. F1 lies outside item 2's literal scope, which names the superproject's configuration and is met. F1 is recorded under the lenses below.

[R584] PASS RTL - `ctrl_build.py:197-206,377-389,431-494`; `git diff --stat 8aaa2da7..a8fe548a` (no HDL, SV, syn, Makefile or workflow file); `receipts/tree_equivalence_head.txt`, `receipts/store_probe_head_py314.txt` - No clock, reset, CDC or HDL change. Checked as module and interface contracts:
- `GitRun` gains `raw` with a default, and every caller keeps its fields;
- the helper's stdin and stdout decoding is equivalent to the old text mode;
- `stack_pin` still returns the head or raises `Refusal`;
- the tree parser's id width (`len(pin)//2`), indexing and mode normalisation (`f"{mode:0>6}"`) give exactly the 89 entries of `ls-tree -r -t`;
- every error path (failed read, wrong type, peeled type, hash mismatch, a commit that names no tree) raises `Refusal`.

[R584] UNCLEAN Robustness - `ctrl_build.py:187-188,385,439`, `receipts/store_probe_head_py314.txt`, `receipts/store_probe_head_py312.txt`, `receipts/lazy_fetch_cli.txt` - 13 forged, swapped, corrupt and missing states fail closed. F1: a missing object plus the stack's own promisor configuration starts a configured program inside the decision.

[R584] UNCLEAN Tests - `ctrl_pin_store.py:113-169`, `ctrl_pin.py:977-994`, `receipts/store_arms_*.txt`, `receipts/pin_controls_head_py314.txt`, `receipts/pin_controls_head_py312.txt` - 84 of 84 pin controls hold on 3.14.7. The new store controls fail under their mutants: `no-hash` gives 2 escapes, and `no-fsmonitor-off` gives 1. F1: no control holds the lazy-fetch route. S1 is optional.

[R584] UNCLEAN Docs - `sw/firmware/ctrl/README.md:172-175,209,230-235`, `ctrl_pin.py:56-63`, `ctrl_pin_store.py:1-28`, the PR body, `receipts/docs_gates_head.txt` - The README and the docstrings are accurate and narrow, the figure equals the count, and the docs, em-dash and idiom gates pass. F1: the PR body's Status and Contents state "no repository's own configuration starts a program while the pin is decided", which the head does not hold. RES-1 is residue.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round-14 items 1-4 and #697 acceptance 1-5 against `ctrl_build.py:385,435-494`, `ctrl_pin_env.py:145-151`, the PR body, `forge_probe_head.txt`, `model_routes_head.txt`, `pin_controls_head_py314.txt`, the author's image manifests, the delta file list | R584-12 | a8fe548a083239efc799a79c540b2be63e9d13e7 |
| RTL | CLEAN | `ctrl_build.py:197-206,377-389,431-494` (helper and parser contracts, widths, error paths); `tree_equivalence_head.txt`; the delta has no HDL, Makefile or workflow change | R584-12 | a8fe548a083239efc799a79c540b2be63e9d13e7 |
| Robustness | UNCLEAN (F1) | `ctrl_build.py:179-494`; 20 head probes on two interpreters; the CLI entry point; probes at `8aaa2da7`; the remedy mutant | R584-12 | a8fe548a083239efc799a79c540b2be63e9d13e7 |
| Tests | UNCLEAN (F1) | `ctrl_pin_store.py`, `ctrl_pin_env.py` diff, `ctrl_pin.py:905-995`; 84 pin controls on 3.14.7 and 3.12.3; store controls under 3 mutants | R584-12 | a8fe548a083239efc799a79c540b2be63e9d13e7 |
| Docs | UNCLEAN (F1) | `sw/firmware/ctrl/README.md`, `ctrl_pin.py` THE THREAT MODEL, the `ctrl_pin_store.py` docstring, the PR body (Status, Contents, Round 14, references, Known limitations), the docs gates | R584-12 | a8fe548a083239efc799a79c540b2be63e9d13e7 |

## Real limits

- No manager source bank, builder bank or native bank ran at this head, and none is claimed or inferred.
- This round did not run:
  - the full boundary self-tests (`--without verilator`, `--only verilator`);
  - the `firmware-unit` steps, the 506-plant campaign or the coverage ratchet;
  - the 24-mutant hook-rule campaign;
  - the 119-case entry-point campaign.
  For those, the source-head evidence is the author's published receipts: `ef056833:…/author-r14/round14/logs/` (`bjob-head.log`: `ctrl_boundary: PASS`, rc 0, 750 s; `hook-mutants-*`; `entrypoints14.log`).
- No hosted run exists at `a8fe548a`. At 2026-10-12T05:48:18Z the head had 0 check runs and 0 workflow runs. PR #705 is CONFLICTING (`DIRTY`) against dev `c6bd08c6` (`receipts/hosted_checks_head.txt`).
- The images were not rebuilt dev against head.
  - The head's five `ctrl_image` shapes were built with this host's GCC 14.3.0. That is a Buildroot build, not the pinned SDK archive, so its hashes are not comparable with the author's table.
  - A dev-side rebuild needed shared clones of the submodules, which this session did not permit.
  - "Images unchanged" therefore rests on three things: the delta touches no compile input; the author's 35-of-35 manifests; and R584-11's and R585-12's independent 35-of-35 at `8aaa2da7`, whose image inputs this delta does not change.
- Interpreters:
  - the 3.12.3 used is a standalone build without PyYAML, given a pure-Python PyYAML copy on `sys.path`. Child interpreters do not get it, which is why the one AECP control shows `ESCAPED` there;
  - the store probes and the store controls ran on CPython 3.12.13 and 3.14.7;
  - Git is 2.56.0. The runner's Git 2.43 was not available, so F1's route was not executed on it. Lazy fetch from promisor remotes predates 2.43.
- R585-12-S2's fix was checked by reading the code only.
- act was not run (not allowed). Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- F1: a round implementing option (a), or a ruling under option (b). Then a re-review of the resulting head.
- RES-1 goes to the residue checklist. The carried residue (R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1, R585-9's wording) goes to #495.
- PR #705 conflicts with live dev `c6bd08c6` (the generated submodule diagram, per the REVIEW READY). Hosted exact-head evidence cannot exist until that is resolved. Hosted and act acceptance stays with the manager.
- The final current-dev candidate at the merge turn: builder and native banks, source base `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8`, live dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, with the receipts linked on the PR.
- `firmware-unit` headroom stays with #716.

## Checkout integrity

`receipts/integrity_final.txt` records the final state:
- HEAD is `a8fe548a…`, and the HEAD tree and the index tree are both `ee9efde2…`.
- There are 0 status lines, ignored files included. `__pycache__` directories this round's first runs created were removed.
- Every regular tracked file hashes to its blob, with its mode. 0 entries are assume-unchanged or skip-worktree.
- The gitlinks are unchanged. `third_party/tsn-c-stack` (`405dc683`) and `third_party/lwSRP` (`08ee86e8`) were initialised at their gitlinks and are clean.
- Every probe, mutant and build ran under the packet's `scratch/`.

## Receipts and scripts

Every published file is listed in `MANIFEST.sha256`, with paths relative to this packet.
- `scripts/store_probe.py`, `scripts/store_arms_run.py`, `scripts/pin_controls_run.py` and `scripts/make_mutant.py` are this round's. Each takes its trees and work directory as arguments.
- `scripts/prior/forge_probe.py` and `scripts/prior/model_routes.sh` are R585-12's and R584-11's published scripts, copied unchanged from `ef056833`.
- In `receipts/ctrl_image_head.log`, the local home-directory prefix of the compiler path is shown as `~/`. No other byte was changed.
- The failed dev-side image attempt is not published.

R584-12 FINISHED
