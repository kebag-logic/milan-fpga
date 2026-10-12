[R584] NEGATIVE - exact head 516a69be9afba02670e37874294bd1f45ccb9316

# R584-14: internal independent review of issue #697 / PR #705, rounds 14 to 16

Exact head `516a69be9afba02670e37874294bd1f45ccb9316`, tree `544d7611d7baa462d9f7bc4b752fa6dc8b7fcedf`. Source base `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8`.

This is a delta review of the six commits on `8aaa2da7`:
- round 14: `d89898db`, `b62c1981`, `4a35f2f4`, `a8fe548a`;
- round 15: `44eef11f`;
- round 16: `516a69be`, the published head.

All five lenses were applied independently. Rounds 14 and 15 do what their assignments ask, and round 16 refuses R585-14's probed shape. The verdict is NEGATIVE on one MINOR finding.

**R584-14-F1 (MINOR).** The superproject's refused keys match a remote's keys only when they carry a non-empty subsection (`remote.<name>.promisor`). Git also reads a subsection-less `remote.promisor` or `remote.partialCloneFilter`, and an empty-subsection `remote "".promisor`, as a promisor remote. On upstream Git 2.43.0, which does not honour `GIT_NO_LAZY_FETCH`, such a superproject passes the check. Git then fetches the tree its sparse index lacks, and starts a configured `ext::` program while the gitlink is read. The README and the PR body say this cannot happen on any Git.

There is also one RESIDUE, a version list in the README.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
2. Issue #697:
   - the body and its frozen acceptance 1-5;
   - the owner decisions 6074086970, 6074093506, 6074191062, 6074245112, 6074811248 and 6074877336;
   - the lane assignment 6091228902;
   - the round-12 scope ruling 6114400461;
   - the round 13, 14, 15 and 16 assignments (6116488747, 6117713386, 6118625227, 6119960001);
   - the author's REVIEW READY comments 6118316100, 6119366539 and 6120798872.
3. No new requirement or interface clause is cited. The authority for the delta is the round-12 threat model plus the round 14-16 items.
4. `git diff c20c85bd..516a69be`. The delta `8aaa2da7..516a69be` was read line by line: `ctrl_build.py`, `ctrl_pin.py`, `ctrl_pin_env.py`, `ctrl_configs.py`, the new `ctrl_pin_store.py`, and `sw/firmware/ctrl/README.md`. The history was checked too.
5. Public executable evidence:
   - the author's receipts under `review-evidence/697c-r1/author-r16/` at `55acac86` (image hashes, boundary and Verilator logs, unit-job outer log, the 28-key probe);
   - the live PR body, which is byte-identical to `author-r16/PR-BODY.md`;
   - the exact-head hosted state.
6. Only after this round's own pass, probes, verdict and ledger draft: the prior findings of R584-11, R585-12, R584-12, R585-13, R584-13 and R585-14.

## What the assignments ask, confirmed at this head

| Item | Result | Evidence |
|---|---|---|
| R14-1: every object the proof reads is checked against its id, failing closed | `ctrl_build.stored` (`ctrl_build.py:466-477`) reads `cat-file <type> <id>` as bytes, hashes `<type> <len>\0<bytes>` with the repository's format, and refuses a mismatch by its place. `pinned_tree` (`:480-499`) parses the commit and every tree itself. No blob is read: files are hashed from disk (`blob_id`, `:432-436`). A missing object, or a `40000` entry that `cat-file tree` would dereference, fails closed through the same compare. | `receipts/pin_controls_git2.*.log` (the three forge controls `[ok]`) |
| R14-1: R585-12's F1 (forged subtree) refused by name before any build; F0 and F2 keep their verdicts | The forged `src/` tree is refused at three real entry points: `ctrl_build.py --stack-pin`, `maap_differential.py --stack` and `aecp_arms.py --stack`. Each exits 2 with `holds a forged or corrupt object: the pinned src/ tree (tree 5c8c189a) hashes to 832cc534`, and 0 objects are built. The forged commit (F2 shape) and the forged blob are refused by their controls. A plain edit is refused as `src/adp.c` (F0 shape). | `receipts/forged_entrypoints.txt`; pin controls |
| R14-1: the hash check is load-bearing | Mutant M1 (compare removed): the forged-tree and forged-commit controls escape with `accepted 405dc683…`, on Git 2.56.0 and on upstream 2.43.0. Mutant M7 (no recursion): 30 controls escape, the clean clone among them. | `receipts/mutants/M1-*.log`, `M7-*.log` |
| R14-2: the helper passes `-c core.fsmonitor=false`, with a standing control | Done at `ctrl_build.py:413`. Since round 16 both repositories' checks refuse `core.fsmonitor` by name first, so the setting is defence in depth. Mutant M4 (setting removed) lets 0 controls escape on either Git. Mutant M3 (superproject check removed) makes the superproject `core.fsmonitor` control escape. | `receipts/mutants/M3-*.log`, `M4-*.log` |
| R14-3 (optional): the alternates control is independent of an inherited `objects/info/alternates` | Taken: `ctrl_pin_env.py:151` unlinks the file. Verified by reading the code; not re-run with `--reference`. | source |
| R14-4 / R16-4: PR-body residue applied | Applied. The five reference links name `516a69be…` (`[Control firmware]` at PR body line 414). The round-15 row lists `v2.39.4`, `v2.42.2`, `v2.43.4` and `v2.44.1`. "not pushed" is absent. The DoD names the `405dc683` pin rule. | live PR body |
| R15-1: stack configuration allowlist, through the helper, before any object read, refusing by name | `configured` (`ctrl_build.py:521-532`) is called at `:561`, after `rev-parse --show-toplevel` and before `rev-parse HEAD` and every `cat-file`. `STACK_CONFIG` (`:201-204`) is the assignment's list. The spellings that pass the superproject check (F1) are refused here by name with `RAN=0`: `remote.promisor`, `remote..promisor`, `url.<ext>.insteadof` and `protocol.ext.allow`. | `receipts/stack_spelling_probe.txt`; pin controls |
| R15-1: the allowlist is load-bearing, and its order matters | Mutant M2 (not called): 14 controls escape on 2.56.0. On upstream 2.43.0 the recorder runs in both transport controls. Mutant M8 (called after the object reads): 4 escape on 2.56.0; on upstream 2.43.0 the run hangs past 500 s. | `receipts/mutants/M2-*.log`, `M8-*.log` |
| R15-2: `GIT_NO_LAZY_FETCH=1` set, with the versions that honour it | Set at `ctrl_build.py:191`. Upstream check: `v2.45.0` defines it. `v2.39.4`, `v2.43.4` and `v2.44.1` read it in `promisor-remote.c`. `v2.39.3`, `v2.43.3` and `v2.44.0` do not, and nor does the source of the built `v2.43.0`. Mutant M5 (removed) lets 0 controls escape. | gh API reads of `git/git` tags; `receipts/mutants/M5-*.log` |
| R15-3 / R16-2: controls, and the earlier controls holding | 102 of 102 pin controls `[ok]`, 0 misbehaved, with census 0, figures 0 and 4 of 4 figure controls `[ok]`. This holds on Git 2.56.0 and on upstream 2.43.0 (built from `git-2.43.0.tar.xz`; its sha256 matches kernel.org's `sha256sums.asc`), both under CPython 3.14.7. The README count (23 store controls, 102 in all) equals the code. | `receipts/pin_controls_git2.56.0.log`, `receipts/pin_controls_git2.43.0.log`, `receipts/git-2.43.0.tar.xz.sha256` |
| R16-1: superproject keys refused before the index is read | `superproject_configured` (`ctrl_build.py:535-545`) is called at `:425`, before `ls-files --stage`. R585-14's shape, built by the head's own control (named remote `origin`, partial clone, sparse index without the tree, a serving upload-pack), is REFUSED by name with `RAN=0` on 2.43.0. With the check removed (S1) on 2.43.0, the program runs and the gitlink is read. Mutant M3: 4 escape. Mutant M6 (local scope only): the include/work-tree control escapes. **Other spellings of the same keys pass: R584-14-F1.** | `receipts/superproject_spelling_git2.43.0.txt` S0, S1, S5; `receipts/mutants/M3-*.log`, `M6-*.log` |
| R16-3: the texts state what is held | They state it, but the superproject claim is not true on every Git: see F1. | `README.md:179-186`; `ctrl_build.py:535-541`; `ctrl_pin.py:66-68`; `ctrl_pin_store.py:45-51`; PR body lines 33 and 510 |
| Scope ruling (round 12) | Applied. F1 needs no code inside the proof's own modules: it is the superproject's configuration, which the ruling places in the model. | - |
| Images unchanged | No image input changed in the delta (see the RTL line below). Images were not rebuilt here. The author's `images-head-516a69be-elf.sha256` (35 entries) equals `images-dev-c20c85bd-elf.sha256` entry for entry. | `author-r16/round16/logs/`, `author-r16/round14/logs/` |

## Findings

### R584-14-F1 - MINOR - Conformance, Robustness, Tests, Docs - the superproject's refused keys miss the subsection-less and empty-subsection spellings Git reads as a promisor remote, so on a Git without `GIT_NO_LAZY_FETCH` a program still starts and a fetch still happens while the gitlink is read

- **Artifact:**
  - `sw/firmware/ctrl/test/ctrl_build.py:213-214` (`SUPERPROJECT_REFUSED`: `remote.*.promisor`, `remote.*.partialclonefilter`, `remote.*.uploadpack`).
  - `ctrl_build.py:515-517`: `configuration` names a key `section.*.variable` only when it has a non-empty subsection. `remote.promisor` keeps its own name, and `remote..promisor` keeps `remote..promisor`.
  - `ctrl_build.py:542-543`: `superproject_configured` refuses only names in that list.
  - The claims: `ctrl_build.py:539-541` ("so the superproject declares no promisor remote … whatever a Git version makes of GIT_NO_LAZY_FETCH"); `sw/firmware/ctrl/README.md:182` ("without a promisor remote Git fetches nothing, so a tree its sparse index lacks is not fetched through a program while the gitlink is read"); `ctrl_pin.py:66-68`; `ctrl_pin_store.py:45-51`; the PR body's Status (line 33, "so no Git, whatever it makes of `GIT_NO_LAZY_FETCH`, fetches a tree a sparse index lacks through a program while the gitlink is read") and Known limitations (line 510, "on any Git").
- **Authority:**
  - Round-16 assignment 6119960001: items 1 and 2 ("whatever the Git version").
  - R585-14-F1's required outcome (a): "No key of the superproject's configuration can make Git start a program or fetch while the gitlink is read, on every Git the proof accepts".
  - The round-12 ruling 6114400461 places Git's configuration in the threat model.
  - Git 2.43.0's own parsing (`promisor-remote.c`, `promisor_remote_config`) uses `parse_config_key`, then `xmemdupz(name, namelen)`. So `remote.promisor=true` (no subsection) and `remote "".promisor=true` (empty subsection) each create a promisor remote named `""`, and so does a subsection-less `remote.partialCloneFilter`. The lazy fetch then runs `git fetch ''`. An `url.<base>.insteadOf` with an empty value rewrites `''` to `<base>`.
- **Evidence:** `superproject_spelling_probe.py` builds the head's own sparse-superproject scene (`ctrl_pin_store.sparse_superproject`), writes the keys into the superproject's config, and calls the head's `ctrl_build.stack_gitlink`. On upstream Git 2.43.0, with the check in place:
  - S6: `remote.promisor=true`, `url."ext::<program>".insteadOf=` and `protocol.ext.allow=always`. The check passes; the program ran (`RAN=1`).
  - S7: the same with `remote.partialCloneFilter=tree:0` in place of `remote.promisor`: `RAN=1`.
  - S9: `remote "".promisor=true` with the same rewrite: `RAN=1`.
  - S8: `remote.promisor=true`, `url.<origin>.insteadOf=`. Git lazily fetched the missing tree from the origin, and the gitlink was read as `405dc683…`: `ACCEPTED`.
  - The trace (`receipts/superproject_spelling_trace_git2.43.0.txt`) runs under the helper's environment and `-c core.fsmonitor=false`. It shows `ls-files --stage` running `git fetch ''`, then `git remote-ext`, then the configured program.
  - Controls: S0 (the head's own control shape) and S5 (a named remote) are refused by name with `RAN=0`.
  - On Git 2.56.0, every case gives `RAN=0`, because it honours `GIT_NO_LAZY_FETCH`.
  - The stack's allowlist refuses all of these spellings by name (`receipts/stack_spelling_probe.txt`).
  - The author's 28-key probe (`author-r16/round16/probes/super_other_keys.py`) planted no promisor key, so it could not reach this route.
- **Impact:**
  - Conformance: round 16's outcome is not met on a Git that does not honour the variable (upstream releases before 2.45.0, apart from the CVE-2024-32465 maintenance releases). There, the superproject's own configuration still makes Git start a program, or fetch, while the pin's gitlink is read. This is the class R585-14-F1 raised, through another spelling.
  - Robustness: the check depends on the spelling of a key, not on what Git does with it.
  - Tests: every superproject control uses a named remote, so no control can fail for this gap.
  - Docs: the README, the code comment, the threat model and the PR body state a guarantee that does not hold.
  - The hosted runner's Git 2.55 and Ubuntu 24.04's patched 2.43.0 honour the variable, so CI itself is not exposed.
- **Required outcome:** one of these.
  - (a) Every key Git reads as declaring a promisor remote or its transport is refused by name in the superproject, whatever its subsection: none, empty or named. The remaining texts then state exactly what is held. One way, not prescribed: judge `remote` keys by section and variable whatever their subsection. Add a standing control for the subsection-less spelling and one for the empty-subsection spelling. Each must be `[ok]` at the fixed head and `ESCAPED` without the fix. Because each asserts the refusal by key name, it fails without the fix on any Git.
  - (b) A recorded maintainer ruling places these spellings outside the model. Then the texts listed above state the route and its Git-version condition, instead of "on any Git" or "whatever a Git version makes of it".
- **Verification:**
  - For (a): `superproject_spelling_probe.py`, unchanged, on upstream Git 2.43.0. S2, S3 and S6-S9 must each end REFUSED naming the keys with `RAN=0`, and S0 and S5 must keep their verdicts. The new controls must escape under their mutant, and every earlier pin control must still hold.
  - For (b): re-read the texts against the ruling.

### R584-14-RES-1 - RESIDUE - Docs - the README's list of Gits that do not honour `GIT_NO_LAZY_FETCH` reads as complete

- **Artifact:** `sw/firmware/ctrl/README.md:186`: "Where a Git does not honour it (upstream 2.43.0 or 2.44.0), the stack's allowlist and the superproject's refused keys are the guarantee."
- **Evidence:** besides those two, upstream `v2.39.3` and `v2.43.3` also do not read the variable. Every release before 2.45.0 that is not a CVE-2024-32465 maintenance release (`v2.39.4`, `v2.42.2`, `v2.43.4`, `v2.44.1` checked) has the same behaviour.
- **Impact:** wording only. No measurement, figure, verdict, test or code depends on the parenthesis.
- **Exact fix:** replace "(upstream 2.43.0 or 2.44.0)" with "(an upstream release before 2.45.0 other than the CVE-2024-32465 maintenance releases, such as 2.43.0 or 2.44.0)".
- **Verification:** re-read the line.

## Prior public findings at this head

| Finding | Status at `516a69be` | Evidence |
|---|---|---|
| R585-14-F1 (MINOR: superproject promisor makes Git start a program while the gitlink is read, on Git < 2.45 without the backport) | RESOLVED for the probed spelling: the named-remote shape is refused by name with `RAN=0` on upstream 2.43.0, and four standing controls fail without the check (M3). Its required outcome (a), "no key of the superproject's configuration", is not met for the other spellings: carried forward as R584-14-F1. R585-14's own scripts were not re-run; their shape was rebuilt by the head's control and by S0/S1. | `receipts/superproject_spelling_git2.43.0.txt`; `receipts/mutants/M3-*.log` |
| R585-14-RES-1 = R584-13-RES-1 (stale `[Control firmware]` link) | APPLIED: the links name `516a69be…` | PR body line 414 |
| R584-13-RES-2 (incomplete CVE release list in the PR body) | APPLIED | PR body line 377 |
| R584-11-F1 = R585-12-F1 (MINOR: forged `src/` tree accepted) | RESOLVED: refused by place at three entry points before any build; the controls escape under M1 | `receipts/forged_entrypoints.txt`; `receipts/mutants/M1-*.log` |
| R584-12-F1 = R585-13-F1 (MINOR: promisor transport in the stack's configuration ran) | RESOLVED for the stack: the allowlist refuses before any object read, including the F1 spellings. Controls escape under M2 and M8. | `receipts/stack_spelling_probe.txt`; `receipts/mutants/M2-*.log`, `M8-*.log` |
| R584-12-S1 = R585-13-S2 (stack `core.fsmonitor` control could not fail) | RESOLVED: refused by key, escapes under M2 | `receipts/mutants/M2-*.g256.log` |
| R585-12-S1 (superproject `core.fsmonitor`) | RESOLVED: refused by key; escapes under M3 | `receipts/mutants/M3-*.log` |
| R585-12-S2 (alternates with `--reference`) | RESOLVED by code reading (`ctrl_pin_env.py:151`); not re-run with `--reference` | source |
| R585-12-RS1 to RS4, R584-11-RES-1, R584-12-RES-1 = R585-13-RES-1 | APPLIED | live PR body |
| R585-14-S1 (`needle in detail`, not equality) | RETAINED SUGGESTION, `ctrl_pin.py:994` | source |
| R585-14-S2 (no control fails for `GIT_NO_LAZY_FETCH` or `core.fsmonitor=false` alone) | RETAINED SUGGESTION. Confirmed: M4 and M5 each let 0 controls escape on both Gits. | `receipts/mutants/M4-*.log`, `M5-*.log` |
| R585-14-S3 (unparsable stack configuration misnamed as "not its own checkout") | RETAINED SUGGESTION, `ctrl_build.py:558-560` | source |
| R584-13-S1 (allowlist assumes a case-sensitive, symlink-capable file system) | RETAINED SUGGESTION, `STACK_CONFIG` unchanged | source |
| R585-13-S1 (no control forges the root tree), R585-13-S3 ("cannot read the pinned tree" for a commit read, `ctrl_build.py:472`) | RETAINED SUGGESTIONS | source |
| R584-11-S1 (`c03e9c9c` not buildable), R584-9-S1 (`defs[0]`, now `ctrl_pin.py:585`), R585-2-S2 (`aecp_arms.py:83`) | RETAINED SUGGESTIONS | source, history |
| R584-8-RES-1 (`README.md:270` "runs it, with GoogleTest and GoogleMock 1.14.0:") and the other carried residue for #495 | RETAINED; not re-verified one by one | source |
| R584-10-F1 | Still RESOLVED by the round-12 ruling; the threat-model texts are kept (`ctrl_pin.py:45-70`) | source |
| `firmware-unit` headroom (#716) | RETAINED as carried | - |

## Lenses

- **Conformance**
  - Applied to the round 14, 15 and 16 items and the round-12 ruling, against `ctrl_build.py:183-214` and `:420-573`, `ctrl_pin_store.py` and the PR body. #697 acceptance 1-5 are untouched by the delta: no moved path, no pin and no licence changed.
  - UNCLEAN: R584-14-F1 (round 16's "whatever the Git version" is not met).
- **RTL** (architecture and interface contracts; this delta has no RTL)
  - `git diff --name-only 8aaa2da7..516a69be` lists six files under `sw/firmware/ctrl/`: no `hdl/`, `tb/`, Makefile, workflow or firmware source.
  - The changed hunks of `ctrl_build.py` all lie from line 183 on. `C_FLAGS`, `RV32_FLAGS`, `PORTABLE` and `INCLUDE_DIRS` (`:60-77`) are unchanged.
  - The gitlinks are `405dc683` (tsn-c-stack) and `08ee86e8` (lwSRP), equal to the base.
  - The helper's contract stays compatible: `GitRun.raw` has a default. Output is decoded with `surrogateescape` and no newline translation. The only callers are the pin modules, whose 102 controls hold.
  - `ctrl_configs.GATE` gains `ctrl_pin_store.py`, a gate module that is not a builder.
  - CLEAN.
- **Robustness**
  - Applied: forged, missing and dereferenced objects (fail closed); configuration parse failure (Refusal); mixed key spellings on both repositories; ordering of the checks (M8); two Git versions.
  - UNCLEAN: R584-14-F1 (spelling-dependent superproject check).
- **Tests**
  - Applied: 102 controls on two Gits, and 8 mutants on two Gits. Every new check has a control that fails without it (M1, M2, M3, M6, M7, M8). M4 and M5 are defence in depth (R585-14-S2, retained).
  - UNCLEAN: R584-14-F1 (no control for the subsection-less or empty-subsection spelling).
- **Docs**
  - Applied: README `:167-186` and `:220-257`, the docstrings and the threat model, the PR body, and the docs gates. All gates pass, including the em-dash gate (0 findings over 431 added lines) under the pinned Markdown renderer.
  - UNCLEAN: R584-14-F1 (texts claim "any Git"). R584-14-RES-1 is residue only.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R584-14-F1) | Issue #697 acceptance 1-5 and assignments 6114400461, 6117713386, 6118625227, 6119960001; `ctrl_build.py:183-214`, `:420-573`; `ctrl_pin_store.py`; live PR body | R584-14 | `516a69be9afba02670e37874294bd1f45ccb9316` |
| RTL | CLEAN | `git diff --name-only 8aaa2da7..516a69be` (6 files, no HDL, tb, Makefile or flags); `ctrl_build.py:60-77` unchanged; `ctrl_build.py:225-235`, `:407-417` helper contract; gitlinks `405dc683` and `08ee86e8`; `ctrl_configs.py:74-76` | R584-14 | `516a69be9afba02670e37874294bd1f45ccb9316` |
| Robustness | UNCLEAN (R584-14-F1) | `ctrl_build.py:466-545`; `receipts/superproject_spelling_*`, `stack_spelling_probe.txt`, `forged_entrypoints.txt`, `mutants/M8-*` | R584-14 | `516a69be9afba02670e37874294bd1f45ccb9316` |
| Tests | UNCLEAN (R584-14-F1) | `ctrl_pin_store.py:1-420`; `ctrl_pin.py:914-1000`; `receipts/pin_controls_git2.56.0.log`, `pin_controls_git2.43.0.log`; `receipts/mutants/` (M0-M8, two Gits) | R584-14 | `516a69be9afba02670e37874294bd1f45ccb9316` |
| Docs | UNCLEAN (R584-14-F1; RES-1 residue only) | `sw/firmware/ctrl/README.md:167-257`; `ctrl_pin.py:1-140`; `ctrl_pin_env.py:1-35`; live PR body; `receipts/docs_gates_head.txt` | R584-14 | `516a69be9afba02670e37874294bd1f45ccb9316` |

## Real limits

- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts.
- Images were not rebuilt here, because this host has no RV32 compiler. The claim that they are unchanged rests on the delta touching no image input, plus the author's 35-of-35 hash table.
- These were not run here: the full `ctrl_boundary.py --selftest` (with its boundary builds), `firmware-unit`, coverage, the mutation campaigns, the hook-rule campaign and the 54 docs-job commands. Only the docs gates listed in `receipts/docs_gates_head.txt` were run. The pin controls were run alone, through `run_pin_controls.py`.
- Python was CPython 3.14.7 only. CPython 3.12.3 and Ubuntu's patched Git 2.43.0 were not exercised. Upstream Git 2.43.0 was built from the verified tarball.
- Mutant M2 on upstream 2.43.0 ended after 5 escapes were printed, and M8 on 2.43.0 hung past 500 s. Their Git 2.56.0 runs give the counts.
- R585-14's own probe scripts and R585-12's `--reference` setup were not re-run.
- Hosted CI: no check run or workflow run exists at `516a69be`. The latest hosted runs are at `8aaa2da7`. Hosted and act acceptance belong to the manager.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- After the probes, the clone was verified: 1291 tracked blobs match their index entries by bytes and mode, the index equals HEAD, the status is clean, all six gitlinks match, and the pin check passes (`receipts/checkout_integrity.txt`). The only change to the clone is the initialised tsn-c-stack submodule at its gitlink.

## Pending manager duties

- Assign the R584-14-F1 outcome, (a) or (b), and re-review the corrected head.
- Carry R584-14-RES-1 and the retained #495 residue to the residue checklist.
- Validate the current-dev merge candidate: source base `c20c85bd`, live dev `c6bd08c6`. The author reports a conflict only in the generated submodule diagram. The builder and native banks run at the merge turn.
- Own the hosted and act acceptance at the exact merge head. There is no hosted run at `516a69be`.
- The external review R585-15 is running at the same head.

R584-14 FINISHED
