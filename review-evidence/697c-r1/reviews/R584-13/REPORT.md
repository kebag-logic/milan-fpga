[R584] POSITIVE - exact head 44eef11f8ee0d0f980eb68355c930efe2cce8cd8

Internal independent review R584-13 of issue #697 / PR #705. This is a delta review of rounds 14 and 15: five commits on `8aaa2da7` (`d89898db`, `b62c1981`, `4a35f2f4`, `a8fe548a`, `44eef11f`). Exact head `44eef11f8ee0d0f980eb68355c930efe2cce8cd8`, tree `df7a60de69acd7de3ac29042b014e0a4dd6ae342`. Source base `c20c85bd`.

All five lenses were applied, and all five are CLEAN at this head. No BLOCKER, MAJOR or MINOR is open. Two new RESIDUE items are PR-body wording only and go to the manager's checklist: R584-13-RES-1 (one stale link) and R584-13-RES-2 (an incomplete version list). One new SUGGESTION is optional.

The two MINOR findings this round answers are both RESOLVED at this head:
- R584-11-F1 = R585-12-F1: a forged `src/` tree object in the stack's store was accepted.
- R584-12-F1 = R585-13-F1: a promisor transport named in the stack's own configuration ran while the pin was decided.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md` (lane, review bar, one-line commits, em-dash rule) and `docs/README.md` (authority order).
2. Issue #697:
   - the body and its frozen acceptance 1-5;
   - owner decisions 6074086970, 6074093506, 6074191062, 6074811248 and 6074877336;
   - the lane assignment 6091228902 and the pin ruling 6092176555;
   - the round-12 scope ruling 6114400461, and the round-13, 14 and 15 assignments (6116488747, 6117713386, 6118625227);
   - the author's REVIEW READY comments 6118316100 (round 14) and 6119366539 (round 15).
3. The issue and the round-15 assignment cite no new requirement or interface clause. The authority for the delta is the round-12 threat model plus the round-14 and round-15 items.
4. `git diff c20c85bd..44eef11f`, with the delta `8aaa2da7..44eef11f` read line by line: `ctrl_build.py`, `ctrl_pin.py`, `ctrl_pin_env.py`, `ctrl_configs.py`, the new `ctrl_pin_store.py`, and `sw/firmware/ctrl/README.md`.
5. Public executable evidence: the author's round-14 and round-15 receipts under `review-evidence/697c-r1/author-r15/` at `f7619127` (the boundary and Verilator job logs, and the PR body), and the live PR body.
6. Prior review findings on PR #705 (R584-11, R585-12, R584-12, R585-13). These were read only after this round's own pass over the diff and its probes were complete.

## What the assignments ask, confirmed at this head

| Item | Result | Evidence |
|---|---|---|
| R14-1: every object the proof reads is checked against its id, failing closed | `ctrl_build.stored` (`ctrl_build.py:450-461`) reads `cat-file <type> <id>` raw and hashes `<type> <len>\0<bytes>`. `pinned_tree` (`:464-483`) walks the commit and every tree that way. No blob is read: files are hashed from disk. A loose forged `src/` tree or commit is refused by place. So are two forms the controls do not plant: a forgery served from a pack through a swapped `.idx` entry (Q1, Q9), and one served from an alternates store (Q2). A missing object is refused (Q4). | `receipts/pin_arms_head.log`, `receipts/probes_head.log` |
| R14-1: R585-12's F1 (forged subtree) refused by name before any build; F0 and F2 keep their verdicts | The standing control and Q1/Q2 give `holds a forged or corrupt object: the pinned src/ tree (tree 5c8c189a) hashes to 832cc534`. An edit is refused as `src/adp.c` (F0 equivalent). A forged commit is refused (F2 equivalent, Q9). All six entry points refuse before building. | `receipts/entry_points_head.log` |
| R14-2: the helper passes `-c core.fsmonitor=false`, with a standing control | `ctrl_build.py:400`. Under mutant MC (setting removed), the superproject control escapes because the recorder runs. | `receipts/mutant_MC-no-helper-config.log` |
| R14-3 (optional): alternates control independent of an inherited `objects/info/alternates` | Taken (`ctrl_pin_env.py:151`). With an alternates file in the stack's own store: 42 arms, 0 misbehaved. | `receipts/pin_arms_head_with_stack_alternates.log` |
| R14-4: PR-body residue applied | R585-12-RS1 to RS4 and R584-11-RES-1 are present in the live PR body. The RS3/R584-12-RES-1 link target is one round stale again: see R584-13-RES-1. | live PR body (`updatedAt 2026-10-12T07:02:42Z`) |
| R15-1: configuration allowlist, checked before the first object read, refusing by name | `configured` (`ctrl_build.py:486-509`) is called at `:525`, after `rev-parse --show-toplevel` and before `rev-parse HEAD` and every object read. `STACK_CONFIG` (`:199-202`) matches the assignment's list. Mixed case (`[Core] FSMonitor`), a subsection (`core.x.fsmonitor`), `includeIf`, a valueless `core.fsmonitor`, and `url.*.insteadOf` are each refused by name with `RAN=0`. A newline inside an allowlisted value is parsed correctly. | `receipts/probes_head.log` Q3a-Q3f |
| R15-2: `GIT_NO_LAZY_FETCH=1`, and versions recorded | `ctrl_build.py:189-190`. Upstream source check: the variable is read from v2.45.0, and also by the CVE-2024-32465 backports v2.39.4, v2.42.2, v2.43.4 and v2.44.1. It is not read by v2.43.0 or v2.44.0. That matches `README.md:181`. Removing the variable alone (mutant MD) lets 0 controls escape, so the allowlist alone holds. Removing both the variable and the allowlist (mutant MAD) makes Git start the recorder in both transport controls. | `receipts/git_no_lazy_fetch_upstream.txt`, `receipts/mutant_MD-no-lazy-env.log`, `receipts/mutant_MAD-no-config-no-lazy.log` |
| R15-3: one control per refused family, a clean allowlisted clone accepted, the earlier controls holding | 19 store/configuration arms plus the 17 inherited-environment arms and 6 basic arms: 42 of 42 `[ok]`. The 35 census/hook arms are 35 of 35 `[ok]`, and the proof census reports 0 findings. The author's round-15 boundary log reports 98 pin controls, 0 `ESCAPED`, and `ctrl_boundary: PASS`. | `receipts/pin_arms_head.log`, `receipts/census_arms_head.log`, author `round15/logs/bjob-head.log` |
| R15-4: README, docstring and PR body state the allowlist; the "class closed" sentence fixed | `README.md:175-182`, `ctrl_pin.py:59-68` and `ctrl_build.py` docstrings say this. The PR body's round-14 Status line now says the stack's configuration is held to an allowlist in round 15. | source, live PR body |
| Scope ruling (round 12) | Applied. No finding here depends on adversarial code inside the proof's own modules. | - |
| Images unchanged | No image input changed in the delta: six files, all pin-proof code, its controls or the README. No changed line of `ctrl_build.py` touches `RV32_FLAGS`, `INCLUDE_DIRS`, `PORTABLE`, the stack include paths or the build functions. The gitlink is unchanged. Images were not rebuilt in this round; the author reports 35 of 35 ELF hashes equal to dev `c20c85bd`'s. | `receipts/delta_scope.txt` |

## Findings

### R584-13-RES-1 - RESIDUE - Docs - the PR body's Control firmware link names `a8fe548a`, whose README predates the allowlist

- **Artifact:** PR body, `## Authoritative references`, fourth bullet, the `[Control firmware]` link: `https://github.com/kebag-logic/milan-fpga/blob/a8fe548a083239efc799a79c540b2be63e9d13e7/sw/firmware/ctrl/README.md`.
- **Evidence:** at `a8fe548a`, that page says "84 pin controls follow the boundary controls" (`README.md:209`) and has no allowlist text. At the head the page says 98 and states the allowlist (`README.md:175-182`, `:216`). Of the five pages in that bullet, only this one changed between `a8fe548a` and the head (`git diff --stat a8fe548a 44eef11f`).
- **Impact:** wording only. A reader following the link sees the round-14 page. No measurement, figure, verdict, test, code or claim of the PR depends on it.
- **Exact fix:** replace `a8fe548a083239efc799a79c540b2be63e9d13e7` with `44eef11f8ee0d0f980eb68355c930efe2cce8cd8` in the `[Control firmware]` link. For uniformity, the other four links may change the same way.
- **Verification:** the link opens a page that reads "98 pin controls".

### R584-13-RES-2 - RESIDUE - Docs - the PR body names only two of the CVE-2024-32465 releases that read `GIT_NO_LAZY_FETCH`

- **Artifact:** PR body, `## Round 15`, table row "2. `GIT_NO_LAZY_FETCH=1`": "Upstream defines it from `v2.45.0`; `v2.43.4` and `v2.44.1`, the CVE-2024-32465 releases, read it too; `v2.43.0` and `v2.44.0` do not."
- **Evidence:** `promisor-remote.c` reads `GIT_NO_LAZY_FETCH` at v2.39.4 and v2.42.2 as well (`receipts/git_no_lazy_fetch_upstream.txt`). "the CVE-2024-32465 releases" reads as if only those two exist. The README's general wording, "a Git patched for CVE-2024-32465" (`README.md:181`), is accurate.
- **Impact:** wording only. The allowlist is the guarantee on every Git, and no figure, test or code depends on the list.
- **Exact fix:** replace "`v2.43.4` and `v2.44.1`, the CVE-2024-32465 releases, read it too" with "the CVE-2024-32465 maintenance releases read it too (checked: `v2.39.4`, `v2.42.2`, `v2.43.4`, `v2.44.1`)".
- **Verification:** the sentence lists the checked releases.

### R584-13-S1 - SUGGESTION - Robustness, Docs - the allowlist assumes a case-sensitive, symlink-capable file system

- **Artifact:** `ctrl_build.py:196-202` (`STACK_CONFIG`) and `README.md:175` ("the keys Git writes itself for a clone and a submodule").
- **Observation:** when `git init` or `git clone` runs on a case-insensitive file system, Git also writes `core.ignorecase`. On macOS it writes `core.precomposeunicode`, and where symbolic links are unavailable it writes `core.symlinks`. This is from Git's init behaviour and was not executed here. None of these keys names a program. On such a host, every checkout is refused by those keys' names. That fails closed, and the PR body's open item (b) covers the general case. The repository's gates target Linux, where Git writes only allowlisted keys (`receipts/tools_and_init_config.txt`).
- **Optional:** either say on the README line that the list is what Git writes on the Linux hosts the gates run on, or add the three value-only file-system keys to the allowlist with a control. This does not affect the verdict.

## Prior public findings at this head

| Finding | Status at `44eef11f` | Evidence |
|---|---|---|
| R584-11-F1 = R585-12-F1 (MINOR: a forged `src/` tree accepted an edited `src/adp.c`) | RESOLVED. Every object read is hashed against its id. The standing controls fail under mutants MB (no hash check), ME (commit not hashed) and MG (only commit and root hashed). | `receipts/mutant_MB*.log`, `mutant_ME*.log`, `mutant_MG*.log`, `probes_mutant_MB.log` |
| R584-12-F1 = R585-13-F1 (MINOR: a promisor transport named in the stack's configuration ran while the pin was decided; the PR body called the class closed) | RESOLVED by option (a). The allowlist refuses before any object read, and `GIT_NO_LAZY_FETCH=1` is set. Through all six entry points a partial clone with a recorder upload-pack is refused by name with `RAN=0`. Removing the allowlist (MA) lets 14 controls escape, and removing it together with the variable (MAD) makes Git run the recorder. The PR body no longer claims more than holds. The "toctou" variant has no route left: no program starts, so nothing remains to act after the verdict. Measured here on Git 2.56.0 only; the allowlist's check (`git config --list`) does not depend on lazy-fetch support. | `receipts/entry_points_head.log`, `receipts/mutant_MA*.log`, `receipts/mutant_MAD*.log` |
| R584-12-S1 / R585-13-S2 (the stack's `core.fsmonitor` control could not fail) | RESOLVED. The control is now refused by its key and escapes under MA. | `receipts/mutant_MA-no-config-check.log` |
| R584-12-RES-1 / R585-13-RES-1 (reference links at `8aaa2da7`) | APPLIED (the links name `a8fe548a`). That target is stale again: R584-13-RES-1. | live PR body |
| R585-12-S1 (superproject `core.fsmonitor`) | RESOLVED (round 14). The control fails under MC. | `receipts/mutant_MC-no-helper-config.log` |
| R585-12-S2 (alternates control and `--reference`) | RESOLVED. Re-executed with an alternates file in the stack's store. | `receipts/pin_arms_head_with_stack_alternates.log` |
| R585-12-RS1 to RS4, R584-11-RES-1 | APPLIED in the live PR body: "not pushed" is gone, the DoD names the `405dc683` pin rule, and the limitation names `firmware-boundary`. | live PR body |
| R585-13-S1 (no control forges the root tree) | RETAINED SUGGESTION, not taken. The code refuses a forged root (it is hashed like any tree), but no control plants one. | source `ctrl_pin_store.py:258-266` |
| R585-13-S3 ("cannot read the pinned tree of" worded for a commit read) | RETAINED SUGGESTION, `ctrl_build.py:456` | `receipts/pin_arms_head.log` (the `GIT_ALTERNATE_OBJECT_DIRECTORIES` arm) |
| R584-11-S1 (`c03e9c9c` is not a buildable state) | RETAINED SUGGESTION, not taken (it needs a history rewrite) | history |
| R584-9-S1 (`census()` indexes `defs[0]`) | RETAINED SUGGESTION, now `ctrl_pin.py:583` | source |
| R585-2-S2 (an explicit `--stack` uses the default `STACK_TESTS`) | RETAINED SUGGESTION, `aecp_arms.py:83` | source |
| R584-8-RES-1 | RETAINED RESIDUE for #495. `sw/firmware/ctrl/README.md:262` still reads "runs it, with GoogleTest and GoogleMock 1.14.0:" | source |
| R585-8-RS1; R584-7-RES1 / R585-7-RS1; R585-9 residue wording; `firmware-unit` headroom (#716); other carried optional suggestions | RETAINED as carried. Nothing in this delta touches them. They were not re-verified one by one. | - |

## Per-lens results

[R584] PASS Conformance - `ctrl_build.py:189-202,394-404,450-536`; `ctrl_pin_store.py:258-310`; issue comments 6117713386 and 6118625227; `receipts/delta_scope.txt` - Each round-14 item (1-4) and round-15 item (1-4) was checked against the code and its executed controls. The allowlist is exactly the assignment's list. The check runs before the first object read. The helper's command line carries only `core.fsmonitor=false`. #697 acceptance 1-5 are not touched by the delta: no image input, gitlink, mutation table or coverage row changed.

[R584] PASS RTL - `git diff --name-only c20c85bd..44eef11f -- '*.sv' '*.v' '*.svh' hdl/` (0 files) and the delta's six files - No HDL or testbench RTL is in the PR diff, so the lens's clock, reset, CDC and FSM scope does not apply. Its width and indexing angle was applied to the delta's tree parser instead: `pinned_tree` takes the id width from `len(pin) // 2` and pads the mode with `f"{mode:0>6}"`. Both are exercised by the clean accept, by Q6 (shallow) and Q7 (linked worktree) accepts, and by the forged-object refusals.

[R584] PASS Robustness - `receipts/probes_head.log` (16 probes, 0 unexpected), `receipts/entry_points_head.log` (12 of 12), `receipts/pin_arms_head_with_stack_alternates.log` - Probed beyond the standing controls:
- a forged tree and a forged commit served from a pack, and from an alternates store;
- a missing object without promisor configuration;
- `core.worktree` pointing at a pristine checkout;
- configuration-syntax variants: case, subsection, `includeIf`, valueless key, `insteadOf`, and a newline in a value;
- shallow and linked-worktree checkouts;
- the six entry points under an edit and under a lazy upload-pack transport.

Each fails closed by name, or is accepted where pinned, with no program started.

[R584] PASS Tests - `receipts/mutant_*.log` (8 mutants), `receipts/probes_mutant_MB.log`, `receipts/probes_mutant_MA.log`, `receipts/census_arms_head.log` - Every non-equivalent mutant is caught by at least one standing control:
- MA (no allowlist) 14;
- MB (no hash check) 2;
- MC (no helper setting) 1;
- ME (commit unhashed) 1;
- MF (promisor keys allowlisted) 5;
- MG (subtrees unhashed) 1;
- MAD 14, with Git running the recorder.

MD (variable removed) is equivalent by design. The independent probes Q1, Q2 and Q9 turn to ACCEPT under MB, so they are live. The 35 census/hook arms are `[ok]`, and the proof census reports 0 findings. The README's figures match the arm lists: 17 inherited, 19 store, 98 in the author's boundary log.

[R584] PASS Docs - `sw/firmware/ctrl/README.md:167-249`, `ctrl_pin.py:20-68,100-135`, the `ctrl_pin_store.py` and `ctrl_build.py` docstrings, and the live PR body - The README's statements were checked against code and execution: the allowlist list, the check's order, the 2.45.0/CVE wording, the control counts 98/17/19/13, and the description of each control. `check_em_dash.py --base c20c85bd` finds 0 findings over 423 added lines, and `docs_check.py` finds 0. `check_py_idiom.py` holds every ratchet (`receipts/em_dash.log`, `docs_check.log`, `py_idiom.log`). The two open PR-body items are RESIDUE (RES-1, RES-2) and do not leave the lens unclean.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta code (`ctrl_build.py`, `ctrl_pin_store.py`, `ctrl_pin_env.py`, `ctrl_pin.py`, `ctrl_configs.py`) against the round-14/15 assignments and the round-12 ruling; `receipts/delta_scope.txt` | R584-13 | `44eef11f8ee0d0f980eb68355c930efe2cce8cd8` |
| RTL | CLEAN | PR diff file list (no HDL); `pinned_tree` parsing | R584-13 | `44eef11f8ee0d0f980eb68355c930efe2cce8cd8` |
| Robustness | CLEAN | `probes.py` Q0-Q9, `entry_points.py`, alternates re-run | R584-13 | `44eef11f8ee0d0f980eb68355c930efe2cce8cd8` |
| Tests | CLEAN | 42 store/env/basic arms, 35 census/hook arms, 8 mutants, probe liveness under mutants | R584-13 | `44eef11f8ee0d0f980eb68355c930efe2cce8cd8` |
| Docs | CLEAN (two RESIDUE for the manager) | firmware README, module docstrings, live PR body, em-dash/docs/idiom gates | R584-13 | `44eef11f8ee0d0f980eb68355c930efe2cce8cd8` |

## Real limits

- No hosted run exists at this exact head: 0 check runs and 0 workflow runs at `2026-10-12T07:05:00Z` (`receipts/hosted_at_head.txt`). Nothing hosted was inspected for this head.
- Not run in this round:
  - the full `ctrl_boundary.py --selftest` (boundary and Verilator jobs), `firmware-unit`, the mutation campaigns, coverage, and the image builds;
  - the 7 Makefile bench arms and the 34 hook plants on CPython 3.12.

  For these, the source-head execution evidence is the author's published receipts: round-15 `bjob-head.log` and `vjob-head.log`, which report 98 pin controls with 0 misbehaved. Those logs do not print their own commit id; they are tied to `44eef11f` only by the author's REVIEW READY.
- Executed here on Git 2.56.0 and CPython 3.14.7 only. The runner's Git 2.55.0 and the replica's Git 2.43.0 / CPython 3.12.3 were not run. The allowlist's refusal comes from `git config --list --show-scope`, which needs no lazy-fetch support.
- Images were not rebuilt. Identity rests on the delta touching no image input (`receipts/delta_scope.txt`) and on the author's 35-of-35 receipt.
- The pinned Verilator was not used (no RTL or bench run).
- A concurrent writer that changes the stack's configuration or files after the check is outside what any pre-build check can hold. This is not a finding.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Apply R584-13-RES-1 and R584-13-RES-2 to the PR body (residue checklist). Carry R584-8-RES-1 and the other retained residue to #495.
- Push-time hosted evidence at `44eef11f`: `rtl-fast` (including `firmware-unit`, `firmware-boundary`, `firmware-verilator`, `publication-census`), `verilator-suites` and `yosys-portability`. This round saw none. Act/hosted acceptance is the manager's.
- Validate the current-dev merge candidate against live dev `c6bd08c6` (builder and native banks): the generated submodule diagram conflict the author reports, and image identity at the candidate. Link the receipts on the PR.
- Carried: `firmware-unit` headroom (#716), and the `MAKEFLAGS=w` source-list self-test as at dev.

## Checkout integrity

After all probes, the review clone was checked (`receipts/checkout_integrity.txt`):
- HEAD is `44eef11f…` with tree `df7a60de…`;
- 1291 tracked blobs, hashed from disk with their modes, match HEAD's tree (0 differ);
- the index equals HEAD's tree, and `status --porcelain` is empty;
- the gitlinks are unchanged: `third_party/tsn-c-stack` `405dc683…`, `third_party/lwSRP` `08ee86e8…`, `protocol-processor` `2ad2f845…`, `gptp-processor` `5dce647a…`, `third_party/verilog-axis` `48ff7a7e…`, `external` `efeb541a…`.

All probes, mutants and gates ran on disposable copies under `scratch/`, which is not published.

## Receipts and scripts

Listed in `MANIFEST.sha256`:
- `scripts/pin_arms.py`, `census_arms.py`, `probes.py`, `entry_points.py`, `mutate.py`, `integrity.py`;
- the logs under `receipts/`.

R584-13 FINISHED
