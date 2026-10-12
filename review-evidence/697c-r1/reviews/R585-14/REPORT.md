[R585] NEGATIVE - exact head 44eef11f8ee0d0f980eb68355c930efe2cce8cd8

# R585-14: external independent review of PR #705 (issue #697), rounds 14 and 15

Head `44eef11f8ee0d0f980eb68355c930efe2cce8cd8`, tree `df7a60de69acd7de3ac29042b014e0a4dd6ae342`. This is a delta review of `8aaa2da7..44eef11f`: four round-14 commits (`d89898db`, `b62c1981`, `4a35f2f4`, `a8fe548a`) and the round-15 commit `44eef11f`. All five lenses were applied.

Rounds 14 and 15 do what their assignments ask:
- Every object the proof reads is hashed against its id and fails closed.
- R585-12's F1 is refused by the forged tree's place, and F0 and F2 keep their verdicts.
- The helper passes `-c core.fsmonitor=false`, with a standing control.
- The stack's configuration allowlist runs before any object read and refuses every refused key family by name.
- `GIT_NO_LAZY_FETCH=1` is set, and the versions that honour it are correctly recorded.
- R584-12's lazy probes end in the refusal with `RAN=0`.
- All 98 pin controls hold on CPython 3.14.7 and 3.12.3, and on Git 2.56.0 and upstream 2.43.0.

The verdict is NEGATIVE because of one MINOR finding, R585-14-F1. It is the same class round 15 closed, reached through the superproject rather than the stack:
- On a Git that does not honour `GIT_NO_LAZY_FETCH`, the superproject's own configuration still makes Git start a promisor transport program while the gitlink is read.
- The README says the superproject's configuration is held.

There is one RESIDUE, a stale PR-body link.

## Order of reconstruction

1. `AGENTS.md` and `CONTRIBUTING.md` (review bar, lenses, severities), then `docs/README.md`.
2. Issue #697: the body and its frozen acceptance 1 to 5. Then the manager's rulings and assignments: round 12 (6114400461, threat model), round 13 (6116488747), round 14 (6117713386) and round 15 (6118625227).
3. The REVIEW READY comments for rounds 14 (6118316100) and 15 (6119366539), and the PR body at the head.
4. `git diff 8aaa2da7..44eef11f` (six files, all under `sw/firmware/ctrl`), read in full, and the history `c20c85bd..44eef11f`.
5. Independent probes, mutants and the pin controls (below).
6. Only after that: the prior findings of R584-12 (6118601165) and R585-13 (6118621917), and their published scripts, run unchanged.

## What the assignments ask, confirmed at this head

| Ask | Result | Evidence |
|---|---|---|
| R14-1: every object the proof reads (commit, trees) is checked against its id, failing closed | `ctrl_build.stored` (`ctrl_build.py:450-461`) reads `git cat-file <kind> <oid>` as bytes, hashes `<kind> <len>\0<raw>` with the repository's format and refuses a mismatch by place. `pinned_tree` (`:464-483`) parses the commit and every tree itself. No blob is read (`blob_id`, `:416-420`). | Own probes Q1 (depth-2 tree), Q2 (root tree), Q3 (forged tree served only through `objects/info/alternates`) and Q4 (corrupt loose tree): each refused, rc 2 (`receipts/r585_14_probes.git2.56.txt`, `...git2.43.0-upstream.txt`) |
| R585-12 `forge_probe.py` F1 refused by name before any build; F0 and F2 keep their verdicts | F0 REFUSED `src/adp.c`; F1 REFUSED `... the pinned src/ tree (tree 5c8c189a) hashes to 9b48fa40, not to its id`; F2 REFUSED `... the pinned commit (commit 405dc683) hashes to 55f2ca0d ...`. F3 is now refused by `core.fsmonitor (local)` | `receipts/prior/forge_probe.R585-12.head.txt` (script blob `8365fc8a`, unchanged) |
| The hash check can fail, and Git does not do it | Mutants: compare removed (MB): the forged-tree and forged-commit controls escape, `accepted 405dc683…`. Trees below the root unchecked (MG): the forged `src/` control escapes. Commit unchecked (MH): two controls escape | `receipts/mutants.git2.56.txt`, `receipts/mutants.git2.43.0-upstream.rest.txt` |
| R14-2: helper passes `-c core.fsmonitor=false`, with a standing control | `ctrl_build.py:400`. The superproject control fails without it: MD gives `Git ran a program a repository's own configuration names` | `receipts/mutants.*` |
| R14-3: alternates control independent of an inherited `objects/info/alternates` | `ctrl_pin_env.py:151` unlinks it | Read only. Not re-executed with `--reference` |
| R15-1: local configuration allowlist, through the helper, before any object read, refusing by name | `configured` (`ctrl_build.py:486-509`) runs `git config --list --show-scope -z` through the helper. It is called at `:525`, after `rev-parse --show-toplevel` (which reads no object) and before `rev-parse HEAD` and every `cat-file`. Each key outside `STACK_CONFIG` (`:199-202`) is refused by name and scope. Refused this way: `extensions.partialClone`, `remote.*.promisor`, `remote.*.uploadpack`, `core.sshCommand`, `core.fsmonitor`, `core.hooksPath`, `credential.helper`, the 7 other helpers, `include.path`, `includeIf.*.path`, a work tree's configuration and an unknown key | Own probes Q5 to Q8, Q11, Q12 and Q15. Q5 has mixed-case keys; Q6 has keys with no value; Q7 has dotted subsections, a subsection on a flat key and a flat key in a subsection family; Q8 is an `includeIf`. Pin controls 78 and 80 to 91 |
| The allowlist is load-bearing, and its order matters | MA (allowlist not checked): 14 escape on Git 2.56. On upstream 2.43.0 the run hangs: Git fetches lazily from itself without end, and the transport ran. MC (allowlist after the object reads): 4 escape on 2.56, and it hangs the same way on 2.43.0. MF (any local key accepted): 14 escape | `receipts/mutants.git2.56.txt`, `receipts/mutants.git2.43.0-upstream.MA.txt`, `...rest.txt` |
| R15-2: `GIT_NO_LAZY_FETCH=1`, and the honoured versions recorded | Set at `ctrl_build.py:190`, and required key for key by the hook's judge. Upstream source: `v2.45.0` defines it (`environment.h`, `environment.c`); `v2.39.4`, `v2.42.2`, `v2.43.4` and `v2.44.1` read it in `promisor-remote.c`; `v2.43.0` and `v2.44.0` do not. Measured: Git 2.56.0 honours it (transport 1 start without it, 0 with it). Upstream 2.43.0 ignores it (1 start with it set). The PR's statement is accurate | `receipts/git_no_lazy_fetch_upstream.txt`; own Q13/Q14; `receipts/prior/lazy_fetch_env.R585-13.git2.56.0.txt` (2 → 0) and `...git2.43.0.txt` (2 → 2) |
| R15-3: R584-12 `store_probe.py` lazy cases end in the refusal with `RAN=0` | `lazy_uploadpack_fail`, `lazy_uploadpack_serve`, `lazy_ssh` and `lazy_toctou` are each REFUSED by the allowlist, naming their keys, with `RAN=0`. Toctou's plant does not land. The other 16 probes keep the expected verdicts. Verdicts are identical on CPython 3.14.7/Git 2.56.0 and on CPython 3.12.3/upstream Git 2.43.0 | `receipts/prior/store_probe.head.py314.git2.56.txt`, `...py312.git2.43.0-upstream.txt` (script blob `040fa985`, unchanged) |
| R585-13 `forge_probes.sh` P13 and P14 | At the head both exit 2 with 0 recorder runs. At `a8fe548a`, P13 ran the recorder 2 times, and P14 ran it 2 times then accepted, and a later edit landed. P0 to P12 keep their verdicts, and P11 is now refused by `core.fsmonitor (local)` | `receipts/prior/forge_probes.R585-13.head-vs-a8fe548a.txt` (script blob `8f18ddc2`) |
| One control per refused family, plus an accepted clean clone | `ctrl_pin_store.py:258-310`: 13 configuration controls and the allowlisted-families clone (`accepted 405dc683…`), plus the line-ending control. All `[ok]` | `receipts/pin_controls.head.git2.56.txt` lines 73-91 |
| The 79 pin controls, the environment and object-id controls hold; README figure | 98 of 98 `[ok]`, 0 misbehaved, on CPython 3.14.7/Git 2.56.0, CPython 3.12.3/Git 2.56.0 and CPython 3.14.7/upstream Git 2.43.0. Census 0 findings. Figures 0 findings, 4 of 4 figure controls `[ok]` (98 stated = 98 counted) | `receipts/pin_controls.head.*.txt`, `receipts/census_figures.head*.txt` |
| Images unchanged | `git diff --name-only 8aaa2da7..44eef11f` lists only `sw/firmware/ctrl/README.md` and five test-harness modules. No firmware source, header, linker input, builder flag, Makefile, workflow or gitlink changed. The tsn-c-stack gitlink is `405dc683` at both ends. Images were not rebuilt (see limits); the author's receipt is 35 of 35 identical to `c20c85bd` | diff; `receipts/checkout_integrity.txt` |
| PR-body residue (R585-12-RS1 to RS4, R584-11-RES-1, R584-12-RES-1/R585-13-RES-1) | Applied. Status has no "not pushed". The DoD reads "pin `405dc683` set by #697 comment 6116488747 under the rule of comment 6092176555". The hosted `firmware-boundary` CMake/Clang line is present. The five reference links name `a8fe548a`; one of them is stale again, see RES-1 | PR body at the head |

## Findings

### R585-14-F1 - MINOR - Robustness, Tests, Docs - the superproject's own configuration still makes Git start a program while the gitlink is read, on a Git that does not honour `GIT_NO_LAZY_FETCH`; the texts say that configuration is held

- **Artifact:**
  - `sw/firmware/ctrl/test/ctrl_build.py:407-413` (`stack_gitlink`: `git ls-files --stage -- third_party/tsn-c-stack` in the superproject, whose configuration is not judged).
  - The claims: `ctrl_build.py:191-192` ("so that no repository's own configuration (the superproject's, whose index stack_gitlink reads) names a program Git starts to read an index"), `sw/firmware/ctrl/README.md:180` ("`core.fsmonitor=false`, which holds the superproject's own configuration when the gitlink is read from its index") and `README.md:181-182`, `ctrl_pin_store.py:44-48`, and the PR body's Known limitations ("Round 15: the superproject's own configuration is not under the allowlist; the proof reads only its index there, with `core.fsmonitor=false` and `GIT_NO_LAZY_FETCH=1`").
- **Authority:**
  - The round-12 ruling (6114400461) puts Git's configuration in the proof's threat model.
  - The round-15 assignment (6118625227) names the class: "repository configuration that makes Git start a program". The class's first instance, `core.fsmonitor`, was the superproject's (R585-12-S1).
  - The assignment says "the allowlist is the guarantee" where the variable is not honoured. That guarantee covers only the stack's repository.
- **Evidence:**
  - Script: `probes/r585_14_superproject_sparse_gitlink_serve.sh`. Its state is a superproject that is a partial clone (`extensions.partialClone`, `remote.origin.promisor`) with a sparse index. The gitlink lies under the sparse directory `third_party/`, whose tree object is absent. `remote.origin.uploadpack` names a program that records its start, then serves.
  - On upstream Git 2.43.0, `ctrl_build.stack_gitlink` returns `405dc683…` and the program ran once while the gitlink was read (`receipts/r585_14_superproject_sparse_gitlink_serve.git2.43.0-upstream.txt`).
  - With a program that records and exits 1, the read is refused ("not one stage-0 gitlink"), but the program still ran (`receipts/r585_14_superproject_sparse_gitlink.git2.43.0-upstream.txt`, `RAN=1`).
  - On Git 2.56.0 the same states start nothing and are refused (`RAN=0`).
  - Without a sparse directory around the gitlink, nothing starts on either Git (`receipts/r585_14_superproject*.txt`).
  - The hosted runner's Git 2.55 and Ubuntu's patched 2.43.0 honour the variable. So the route needs a Git older than 2.45.0 without the CVE-2024-32465 backport, such as upstream 2.43.0 or 2.44.0.
- **Impact:**
  - On such a Git, a program named in the superproject's configuration runs while the pin is decided, and the decision continues to an accept. That is the same shape as R584-12-F1/R585-13-F1, whose P14 showed such a program can edit the stack after a correct verdict.
  - The README and the code comment state the opposite, so a reader takes the superproject as held.
  - Tests: the superproject has one control, for `core.fsmonitor` only. No control holds the lazy-fetch route there.
- **Required outcome:** one of these.
  - (a) No key of the superproject's configuration can make Git start a program or fetch while the gitlink is read, on every Git the proof accepts, with a standing control that fails without it. Possible ways (not prescribed):
    - refuse the superproject's promisor and partial-clone keys by name (this does not touch `actions/checkout`'s `http.<url>.extraheader`);
    - read the gitlink without Git;
    - refuse a Git that does not honour `GIT_NO_LAZY_FETCH`.
  - (b) A recorded maintainer ruling places this route outside the model. Then `README.md:180-182`, `ctrl_build.py:191-192`, `ctrl_pin_store.py:44-48` and the PR body state the route and its Git-version condition, instead of saying the superproject's configuration is held.
- **Verification:**
  - For (a): `r585_14_superproject_sparse_gitlink_serve.sh` and `r585_14_superproject_sparse_gitlink.sh` on upstream Git 2.43.0 give `RAN=0`. The new control is `[ok]` at the head and `ESCAPED` under its mutant. The 98 pin controls still hold.
  - For (b): the texts are re-read against the ruling.

### RESIDUE (PR-body wording only; exact fix for the manager's checklist)

- **R585-14-RES-1 - Docs** - PR body, `## Authoritative references`, fourth bullet: the `[Control firmware]` link pins `a8fe548a083239efc799a79c540b2be63e9d13e7`. Round 15 changed that page: at `a8fe548a` it reads "84 pin controls follow the boundary controls" (line 209) and has no allowlist text, while the head says 98. The other four links (`gtest/README.md`, `SUBMODULES.md`, `CI_WORKFLOWS.md`, `mbx/README.md`) are unchanged since `a8fe548a`. Exact fix: in the `[Control firmware]` link only, replace `a8fe548a083239efc799a79c540b2be63e9d13e7` with the head the PR merges at (`44eef11f8ee0d0f980eb68355c930efe2cce8cd8` at this head). The fix is link wording only.

### SUGGESTIONS (optional; no effect on the verdict)

- **R585-14-S1 - Tests** - `ctrl_pin.py:992`. For the configuration controls the README says "Each is refused naming exactly the keys it planted" (`README.md:248`), but the check is `needle in detail`. Because the refusal sorts its keys, an extra refused key sorted after the planted ones would still pass. Every refusal at the head names exactly its keys (`receipts/pin_controls.head.git2.56.txt:78-91`), and the allowlisted-clone control would catch an over-refusal of Git's own keys. Comparing the configuration controls' detail for equality would make the claim the check.
- **R585-14-S2 - Tests** - No standing control fails when `GIT_NO_LAZY_FETCH` is dropped from `GIT_ENVIRONMENT` (ME: 0 escapes on 2.56.0 and on upstream 2.43.0). None fails when the command-scope branch of `configured` accepts any key (MI: 0 escapes). Both are defence in depth behind the stack allowlist and the environment allowlist, and the author states the first (M2). A control could hold each layer alone.
- **R585-14-S3 - Robustness** - When the stack's configuration cannot be parsed, the first Git call (`rev-parse --show-toplevel`) fails. The refusal then reads "... is not its own checkout: initialise the tsn-c-stack submodule" (own Q9), which misnames the cause. It fails closed.

## Prior public findings at this head

| Finding | Status at `44eef11f` | Evidence |
|---|---|---|
| R584-12-F1 = R585-13-F1 (MINOR: a promisor transport in the stack's configuration starts a program while the pin is decided) | RESOLVED for the stack's repository. The allowlist refuses by name before any object read, with 13 standing controls that fail without it (MA/MF 14, MC 4). The same class through the superproject is R585-14-F1 | `store_probe` lazy_* `RAN=0` on both Gits; `forge_probes` P13/P14; mutants |
| R584-12-S1 = R585-13-S2 (stack `core.fsmonitor` control could not fail) | RESOLVED: refused by key, escapes under MA | `receipts/mutants.git2.56.txt` |
| R584-12-RES-1 = R585-13-RES-1 | APPLIED (links name `a8fe548a`); one link is stale again (R585-14-RES-1) | PR body |
| R585-13-S1 (no standing control forges the root tree) | RETAINED SUGGESTION. The head refuses a forged root tree (own Q2; `store_probe` forged_root; `forge_probes` P3) | receipts |
| R585-13-S3 (commit-read refusal says "cannot read the pinned tree") | RETAINED SUGGESTION, `ctrl_build.py:456` | source |
| R584-11-F1 = R585-12-F1 (forged `src/` tree accepted) | RESOLVED (refused by place; MB and MG escape) | `forge_probe` F1; mutants |
| R585-12-S1 (superproject `core.fsmonitor`) | RESOLVED: control, MD escapes. The wider superproject class is R585-14-F1 | mutants |
| R585-12-S2 (alternates control with `--reference`) | RESOLVED by code reading (`ctrl_pin_env.py:151`); not re-executed | source |
| R585-12-RS1 to RS4, R584-11-RES-1 | APPLIED | PR body |
| R584-11-S1, R584-9-S1 (`ctrl_pin.py:583` `defs[0]`), R585-2-S2 | RETAINED SUGGESTIONS, optional | source |
| R584-8-RES-1 (`README.md:262` "runs it, with GoogleTest and GoogleMock 1.14.0:") and the other carried residue for #495 | RETAINED; not re-verified one by one | source |
| R584-10-F1 | Still RESOLVED by the round-12 ruling; the threat-model texts are kept (`ctrl_pin.py:45-69`) | source |

## Per-lens results

[R585] PASS Conformance - `ctrl_build.py:182-202,400,450-537`, `ctrl_pin_store.py:258-310`, the PR body (Status, Round 14, Round 15, How to validate, Known limitations), `receipts/prior/*`, `receipts/git_no_lazy_fetch_upstream.txt` - Issue #697's acceptance 1 to 5 is untouched by this delta: the pin is still `405dc683`, and no image input changed. Each item of the round-14 and round-15 assignments is met as specified, as tabled above. The recorded `GIT_NO_LAZY_FETCH` versions agree with upstream source and measurement. R585-14-F1 lies outside item 1's stated scope (the stack's configuration). It is recorded under the lenses where the same class was recorded before.

[R585] PASS RTL - `git diff --name-only 8aaa2da7..44eef11f` (six files: `sw/firmware/ctrl/README.md` and five Python harness modules; no HDL, SV, testbench, synthesis, Makefile, workflow or gitlink), `ctrl_build.py:407-537` (signatures of `stack_gitlink`, `stack_pin` and `main` unchanged; callers in `ctrl_pin.py:926` and `ctrl_pin_store.py:232,252`) - No clock, reset, CDC or hardware interface is touched. The module contracts of the pin proof (`stack_pin(stack, pin) -> head` or `Refusal`; CLI exit 0/2) are unchanged. The tree parse sizes object ids by the pin's length and pads modes as `on_disk` does, and `pinned_tree` gives the same entries as before (98 controls and the clean-clone accept).

[R585] UNCLEAN Robustness - R585-14-F1 (`ctrl_build.py:407-413`; `receipts/r585_14_superproject_sparse_gitlink*.txt`). Otherwise clean, with these 17 own states and 20 + 15 prior probe states each failing closed or accepting as they should (`receipts/r585_14_probes.*`, `receipts/prior/*`):
- forged root, depth-2 and alternates-served trees;
- corrupt and missing objects;
- mixed-case, valueless and dotted-subsection keys;
- `includeIf`;
- a broken configuration;
- a hostile `core.worktree`;
- `extensions.objectFormat`;
- a relocated gitdir with genuine objects (accepted).

[R585] UNCLEAN Tests - R585-14-F1: no control holds the superproject's lazy-fetch route. Otherwise:
- 98 of 98 pin controls hold on three interpreter/Git combinations.
- Each new mechanism has a control that fails under its mutant: MA, MB, MC, MD, MF, MG and MH escape. ME and MI do not (S2).
- Census and figure checks pass, and the figure controls are 4 of 4.

[R585] UNCLEAN Docs - R585-14-F1: `README.md:180-182`, `ctrl_build.py:191-192`, `ctrl_pin_store.py:44-48` and the PR body's Known limitations say the superproject's configuration is held. RES-1 is residue only. Otherwise the in-tree texts (`README.md:170-182,213-249`, `ctrl_pin.py:24-69,107-134`, `ctrl_pin_store.py:1-49`) agree with the code and receipts. The docs gates are clean: `check_em_dash --base c20c85bd` 0 findings over 423 added lines, `docs_check` 0, `check_doc_style` OK, `check_doc_paths` OK and `gen_toc --check` OK (`receipts/docs_*.log`).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #697 acceptance; round-12 to round-15 rulings; `ctrl_build.py:182-537`; PR body; prior probes; upstream Git source | R585-14 | 44eef11f8ee0d0f980eb68355c930efe2cce8cd8 |
| RTL | CLEAN | delta file list; `ctrl_build.py:407-537` contracts and callers | R585-14 | 44eef11f8ee0d0f980eb68355c930efe2cce8cd8 |
| Robustness | UNCLEAN (F1) | `ctrl_build.py:182-537`; 17 own probe states and 4 superproject states on Git 2.56.0 and upstream 2.43.0; R584-12 `store_probe` (20), R585-12 `forge_probe` (4), R585-13 `forge_probes` (15 × 2 heads), `lazy_fetch_env` | R585-14 | 44eef11f8ee0d0f980eb68355c930efe2cce8cd8 |
| Tests | UNCLEAN (F1) | `ctrl_pin_store.py`, `ctrl_pin_env.py`, `ctrl_pin.py:912-998`; 98 pin controls × 3 configurations; 9 mutants × 2 Gits; census; figures | R585-14 | 44eef11f8ee0d0f980eb68355c930efe2cce8cd8 |
| Docs | UNCLEAN (F1) | `sw/firmware/ctrl/README.md`; `ctrl_pin.py` THE THREAT MODEL; `ctrl_build.py` comments; `ctrl_pin_store.py` docstring; PR body; docs gates | R585-14 | 44eef11f8ee0d0f980eb68355c930efe2cce8cd8 |

## Real limits

- **Images:** no RV32 SDK matching CI was available, so images were not rebuilt. Their identity rests on the delta's file scope (no image input changed) and the author's 35 of 35 receipt.
- **Git versions:**
  - Measured on Git 2.56.0 and on upstream Git 2.43.0, which is unpatched and built here.
  - Ubuntu's patched `1:2.43.0-1ubuntu7.3` and the hosted runner's 2.55 were not executed.
- **Python:** CPython 3.12.3 ran from a disposable environment holding `pyyaml`.
- **What ran:** the pin controls ran alone through `probes/r585_14_pin_controls.py`, which calls `ctrl_pin.pin_controls` exactly as `ctrl_boundary.py --selftest` does, plus the census and figure checks.
- **What did not run:**
  - the full `ctrl_boundary.py --selftest` build matrix, `firmware-unit`, the mutation campaigns and the coverage gate;
  - `check_py_idiom.py` and `check_hygiene.py`, which refused because the scratch copy lacks the other submodules (`receipts/docs_scripts_check_py_idiom.py.log`, `receipts/docs_scripts_check_hygiene.py_--check.log`).
- **Mutants on upstream 2.43.0:** MA and MC hang there: Git fetches lazily from itself without end. They are recorded as TIMEOUT at 240 s, with their escapes before the hang. The process chains were killed, and the mutated copy was restored and compared.
- **Hosted CI:** none ran. GitHub Actions had 0 runs at this exact head at 2026-10-12T07:40Z (`receipts/hosted_runs_at_head.txt`).
- **Physical calibration:** not run. Field skips are not hardware proof.
- **Checkout integrity:** the review clone is untouched: HEAD `44eef11f`, tree `df7a60de`, index and worktree equal to HEAD, and the six gitlinks as recorded (`receipts/checkout_integrity.txt`). All probes ran in disposable copies under `scratch/`.

## Pending manager duties

- R585-14-F1: a round implementing outcome (a), or a ruling under (b). Then a re-review of the resulting head.
- R585-14-RES-1 goes to the residue checklist. The carried residue goes to #495.
- Hosted exact-head `rtl-fast`, `firmware-boundary`, `firmware-verilator`, `verilator-suites` and `yosys-portability`, and the act replica, once the head is final.
- The current-dev merge candidate: dev is `c6bd08c6`, and the author reports a conflict only in the generated submodule diagram. Validate it with the builder and native banks.

## Receipts and scripts

Every published file is listed in `MANIFEST.sha256`, with paths relative to this packet.
- `probes/` holds this round's scripts. Each takes its trees and work directory as arguments.
- `receipts/prior/` holds the outputs of R584-12's `store_probe.py`, R585-12's `forge_probe.py` and R585-13's `forge_probes.sh` and `lazy_fetch_env.sh`. The scripts were run unchanged, fetched by blob id from `f7619127:review-evidence/697c-r1/reviews/`.

R585-14 FINISHED
