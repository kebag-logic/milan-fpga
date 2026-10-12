[R584] NEGATIVE - exact head 8aaa2da74e3d5ee569fed420debc2b69c6749d44

Internal independent review R584-11 of issue #697 / PR #705. This is the delta review for round 13 ([A583]), the way on from the round-12 STOP. The delta runs `aca5e8af..8aaa2da7`: round 12's three commits (`6b03a887`, `a3992e54`, `adb93604`), the round-13 pin move `c03e9c9c`, the merge of dev `c20c85bd` (`30744883`), and `5425fb64`, `6382dc88` and `8aaa2da7`. Tree `cb90055f0843f221ceb6fecc20777cb24cea7f5a`.

All five lenses were applied. Conformance, RTL and Docs are clean. One MINOR finding is open: R584-11-F1, under Robustness and Tests. One RESIDUE is new: R584-11-RES-1. Every item the round-13 assignment asks this review to confirm holds at this head. The verdict is NEGATIVE only because of F1.

F1 is a route inside the pin proof's own threat model, as the round-12 ruling states that model. The author found it in round 12 and published it as "open, for a decision". No decision and no fix exist at this head. With the pinned `src/` tree object forged in the stack's object store, the shared pin check accepts a stack whose `src/adp.c` is edited. R584-8 filed this route as an optional SUGGESTION (R584-8-S1), because it then fell outside the class that round's ruling covered. The round-12 ruling ([6114400461](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461), item 2) has since put "Git's object store" inside the model. So the route is now in scope, and it is reproduced here at the head.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`.
2. Issue #697:
   - the body and its frozen acceptance 1 to 5;
   - the round-12 assignment and scope ruling ([6114400461](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461));
   - the round-12 STOP ([6115091316](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6115091316));
   - the round-13 assignment ([6116488747](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6116488747));
   - the round-13 REVIEW READY ([6117226531](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117226531));
   - the public review start ([6117239984](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6117239984)).
3. tsn-c-stack at the pin: tag `milan-fpga-697-pin-405dc683`, PR #22 and `main`.
4. The diff `c20c85bd..8aaa2da7` and the history `aca5e8af..8aaa2da7`, commit by commit. For the merge commit, each side and Git's automatic merge were compared with the committed result.
5. The PR body at this head, and the published evidence tree `2f4a5c59:review-evidence/697c-r1/author-r13`.
6. Executable evidence, run by this round (below), and the hosted check runs at this head.
7. Only after this round's own verdict and ledger were written (`receipts/independent-verdict-before-prior-findings.txt`): the prior public findings R584-10 and R584-8-S1.

## What the assignment asks, confirmed at this head

| Item | Result | Receipt |
|---|---|---|
| The pin is `405dc683`, not `main`, and reachable | The gitlink is `405dc68310a18f669049ffc10cc23eef7300dcff`. The remote lightweight tag `milan-fpga-697-pin-405dc683` names it, and so do PR #22's head (closed, unmerged), `acmp-publish-port` and `integrate-21`. It is not an ancestor of `main` `1ba27354`. Between the pin and `main`, `src/` and `include/` differ only in `src/adp.c` (6 insertions, 2 deletions), as `SUBMODULES.md:240-243` states. | `receipts/pin_reachability.txt` |
| The cores are token- and line-identical to dev `c20c85bd`'s | This round's own lexer drops comments and whitespace. All seven files have identical tokens, each token on the same line: ADP 1736 and 497, ACMP 7849 and 1175, MAAP 2064 and 394, `wire.h` 202. The bytes differ only in comments and SPDX lines. The seven files are unchanged between `09c7231e` and `c20c85bd`. | `receipts/core_tokens.txt` |
| They compile to byte-equal RV32 objects | The pinned SDK's GCC 14.3.0 (archive sha256 `d42680e9…`, equal to `scripts/ci_rv32_sdk.py`) compiles flat copies with the image flags. All 6 of 6 objects are byte-equal (`-DNDEBUG` and `-UNDEBUG`), and their sha256 prefixes equal the author's published ones. | `receipts/core_objects.txt` |
| The merge keeps the ACMP core's removal and dev's adapter wiring | `acmp/acmp.c`, `acmp.h`, `test/acmp_fake.hpp` and `test/test_acmp.cpp` are deleted. `acmp_mbx.{c,h}` are byte-identical to dev, including `m->ports.publish = port_publish;` (`acmp_mbx.c:98`). Only the 13 conflicted paths differ from Git's automatic merge. Every path only one side changed equals that side (0 exceptions). Dev's `ctrl_mutants.py` change is carried exactly. | `receipts/merge_audit.txt` |
| The merge keeps both sides' CI jobs | The `rtl-fast` aggregate (`rtl-fast.yml:487`) needs and checks `publication-census`, `firmware-unit`, `firmware-boundary` and `firmware-verilator`. Dev's `firmware-unit` steps are unchanged except for fetching `third_party/tsn-c-stack`. `ci_events.py` holds both sides' result names and job constants. `CI_WORKFLOWS.md` names all four jobs as skipped for documentation changes. The mbx `.PHONY` names `census` and `stack-pin`. | `receipts/merge_audit.txt`, `receipts/docs_gates.txt` |
| Dev's ACMP tests are kept | All 69 of dev's `test_acmp.cpp` tests are among the stack's 79. In four of them only the failure-message text differs, or code outside the test body moved; no assertion changed. `acmp_fake.hpp` has identical tokens (2803 by this round's lexer), but some tokens sit on other lines. | `receipts/acmp_tests_subset.txt`, `receipts/core_tokens.txt` |
| F-INT's 11 `pub-acmp-*` plants are retargeted and each fails by name | Each of the 11 core plants equals dev's in every field except `path`, which is now `tsn-c-stack/src/acmp.c`. Each fixture occurs exactly once in the stack's `acmp.c`, and all 506 plant names equal dev's. The ACMP arm passes unplanted (rc 0, 0 `[FAIL]`). Planted through the campaign's own `plant()` and `caught()`, 15 of 15 `pub-acmp-*` plants (11 core, 4 adapter) are caught by their named killers on their words. As a control, re-pointed at dev's `acmp/acmp.c`, all 11 refuse (`FileNotFoundError`). Hosted `firmware-unit` at this head shows all 15 `[ok]`, `mutants: 506 of 506 caught` and 0 `ESCAPED`. The restricted run's exit status is 1 only because a 15-plant table leaves 37 tests named by no plant; the full table names them. | `receipts/pub_plants.txt`, `receipts/pub_campaign_head.txt`, `receipts/pub_campaign_oldpath.txt`, `receipts/hosted_firmware_unit_extract.txt` |
| No campaign's kill tuple became unfindable | Across all 630 kills of the control campaign, 476 have their test name and words in a test source at both dev and the head. No kill findable at dev is unfindable at the head under the same text. The two whose words differ were re-worded onto the stack's messages in earlier rounds. The ACMP, review-ACMP and MAAP tables are unchanged since `adb93604`. | `receipts/kill_words_differential.txt`, `receipts/tables_compare.txt` |
| The firmware images are byte-identical to dev's at every shape | Each tree's own builders ran: `ctrl_image.py` at the 5 shipped shapes, and `ctrl_srp_image.py` at 5 shapes × 2 interface counts × {SRP, no SRP, AECP}. 35 of 35 ELF sha256 are identical between dev `c20c85bd` and the head. The head's builds print `tsn-c-stack at 405dc683…`. | `receipts/images/*` |
| The 79 pin controls and the environment controls hold | `ctrl_pin.pin_controls` was run alone, as `ctrl_boundary.py --selftest` runs it. It gives 79 of 79 `[ok]`, 0 misbehaved, on CPython 3.14.7 and on 3.12.3. That includes 16 inherited-environment controls and the hook plants. Independent probes inherit `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_CONFIG_COUNT` (`core.worktree`), `GIT_CEILING_DIRECTORIES` and `HOME`/`XDG_CONFIG_HOME`; each still refuses the edited clone by name and accepts the clean one. A repository-local `core.worktree` fails closed. `ctrl_build.py`, `ctrl_pin.py` and `ctrl_pin_env.py` are unchanged since `adb93604`. | `receipts/pin_controls_py314.txt`, `receipts/pin_controls_py312.txt`, `receipts/inherited_probe_head.txt` |
| Records regenerated through their generators | `submodule_boundaries.gen.py --check`: OK (6 exact gitlinks, decoded PNG). `check_submodule_docs.py`: OK. `ci_events.py --check`: OK, 1974 items; `--selftest`: PASS, 2766 arms. `docs_check.py`: 0 findings. `check_em_dash.py --base c20c85bd` with the pinned renderer: 0 findings over 401 added lines. `check_py_idiom.py`: every ratchet held. `1a9f651c` appears nowhere in the tree. | `receipts/docs_gates.txt` |
| `8aaa2da7` (`publication_census.py` in `OUTSIDE`) | The program names the firmware tree only in its docstring (`:7`, `:90`). It and `census_elab.py` start only `sv2v` and `yosys` (`census_elab.py:239-240,426-480`) and compile no C, so the stated reason is accurate. | source |
| Round 12, items 2 and 3 | `GIT_ENVIRONMENT` (`ctrl_build.py:187`) is the helper's whole environment, and `environment_judge` checks it before any lookup. Its checks: plain `dict` or `fork_exec` entries with each key once; plain `str` keys and values; both settings; exact key-for-key equality except `CTRL_CAPTURE_FROM`. The README (`:184-189`), the docstring (`ctrl_pin.py:45-62`) and the PR body (Round 12) state the ruling's model in place of "native code is the remaining limit". | source, `receipts/pin_controls_py3*.txt` |
| Hosted at this head | At 2026-10-12T04:18:39Z: `rtl-fast` success. `firmware-unit` success (41 min 28 s), `firmware-boundary` success (13 min 52 s), `firmware-verilator` success (12 min 17 s), `publication-census` success. `docs-check`, `docs-check-no-git`, `elaborate`, `verilator-lint`, `bdd-conformance`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0 and 3, and `full-ci-gate`: success. Verilator shards 1, 2 and 4 were still in progress. "Physical gPTP" was skipped (a nightly/manual context, not executed). | `receipts/hosted_checks.tsv`, `receipts/hosted_checks_time.txt` |

## Findings

### R584-11-F1 - MINOR - Robustness, Tests - the shared pin check accepts an edited core source when the pinned `src/` tree object is forged in the stack's object store, a route inside the proof's stated threat model, with no decision and no fix

- **Artifact:**
  - `sw/firmware/ctrl/test/ctrl_build.py:425-439` (`stack_pin`: `rev-parse HEAD`, then `ls-tree -r -t -z --full-tree <pin>`, whose trees Git reads without checking their hash);
  - `sw/firmware/ctrl/README.md:184` and `:189`;
  - `sw/firmware/ctrl/test/ctrl_pin.py:45-62` (THE THREAT MODEL);
  - `ctrl_pin.pin_controls` (`ctrl_pin.py:902-985`): no control holds this route.
- **Authority/evidence:**
  - The [round-12 ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461), item 2: "The pin proof's threat model is the state it reads: the checkout's files and modes, Git's object store, refs, configuration and attributes, and the environment the proof inherits." The README restates this at `:184`.
  - `receipts/model_routes_head.txt` (`scripts/model_routes.sh`), at the head, on disposable clones of the pinned stack with every object loose:
    - control, the pin unmodified: exit 0;
    - control, `src/adp.c` edited on disk: `REFUSED … differs from the pinned 405dc683: src/adp.c`, exit 2;
    - route 1: the same edit, with the pinned `src/` tree's loose object overwritten by a tree holding the edited blob. The result is exit 0, `tsn-c-stack at 405dc68310a18f669049ffc10cc23eef7300dcff`, while `git fsck` reports `hash mismatch 5c8c189a…`.
  - The README and the docstring disclose the route as "open, for a decision" (`README.md:189`). The REVIEW READY lists it as open risk 2, "awaiting a ruling". No public ruling exists: the issue and PR comments up to this review's start contain none.
  - Disclosure does not resolve it. `AGENTS.md` section 7 says a finding moved elsewhere is still open while the defect is in the tree. Section 4 says a task with an unresolved decision is not ready.
  - R584-8-S1 was optional only because the route then lay outside the ruled class. The round-12 ruling widened the class to the object store.
- **Impact:**
  - A stack edited in its core sources passes every gate that relies on the pin check. That includes the firmware gate, the coverage gate, both image builders, the MAAP differential, the AECP tools and the mailbox bench: they build and report the edited code as the pinned `405dc683`.
  - The precondition is write access to the submodule's object store. That is exactly the state the ruling put inside the model.
  - The README's "So Git reads the real objects only" (`:171`) is true of which store is read, not of what it holds. The pin controls cover replacement refs and grafts, but not an object whose content does not hash to its id.
- **Required outcome:** one of these, recorded publicly.
  - (a) The check fails closed when an object it reads does not hash to its id: the pinned commit, and every tree from the root down to each listed entry. One direction is R584-8-S1's: recompute the ids in Python from the bytes Git returns, or from the disk entries. A standing control must plant the forged-tree case (and a forged commit) and end in a refusal naming the edited source.
  - (b) A maintainer ruling that takes a forged object store out of the model, or accepts it as a stated limit. The README, the docstring and the PR body must then say so, in place of "open, for a decision".
  - This review does not prescribe the design.
- **Verification:**
  - for (a), `scripts/model_routes.sh` route 1 ends in exit 2 naming `src/adp.c`, with the clean control still exit 0. The new controls are `[ok]` on CPython 3.12.3 and 3.14.7. The other 79 pin controls are unchanged, and the README's control figures equal the code's;
  - for (b), the ruling's link, and the three texts consistent with it.
- **Not part of F1:** the second route the author published, a repository-local `core.fsmonitor`, did not reproduce here. With Git 2.56.0, the pin check on a clone whose own `.git/config` names a recorder never started it, and the verdicts stayed correct: clean clone exit 0, edited clone exit 2 by name. The recorder ran only on a later plain `git status` by the probe. The author's probe also reports an unchanged verdict. That route is carried as the author's open question, not as a finding of this round.

### R584-11-RES-1 - RESIDUE - Docs - the PR body's Status line calls the published head "not pushed"

- **Artifact:** PR body, `## Status`, first line: "GREEN locally at `8aaa2da7…` (round 13, four commits and a merge of dev `c20c85bd` on `adb93604`, not pushed):".
- **Evidence:** `8aaa2da7` is PR #705's published head (`receipts/pr_state.json`), and hosted checks ran on it.
- **Exact fix:** delete ", not pushed" from that line. This is wording only. No measurement, figure, verdict, test, code or generated artifact depends on it.

### R584-11-S1 - SUGGESTION - Robustness - the pin-only commit `c03e9c9c` is not a buildable firmware state

At `c03e9c9c` the stack's ACMP core calls the `publish` port unguarded, and only the merge's adapter sets it. The author discloses this (open item c). No rule in `CONTRIBUTING.md` requires every commit to build. If the PR is landed by a method that keeps individual commits on `dev`, a bisect can stop there. This is optional.

## Prior public findings at this head

| Prior finding | Status | Evidence |
|---|---|---|
| R584-10-F1 (MINOR: on CPython 3.12.3 a pure-Python `sys.audit` rebinding keeps a start from the hook, filed under "native code" without a ruling) | RESOLVED by the [round-12 ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461), item 2: adversarial code inside the proof's own modules is out of scope, at most a SUGGESTION. The required texts now state the model: `README.md:184-188`, `ctrl_pin.py:45-62`, PR body Round 12 and its reference list. The Round 11 rows remain as history, marked superseded. | source, PR body |
| R584-8-S1 (SUGGESTION: a corrupted object store can stand in for the pinned tree) | SUPERSEDED by R584-11-F1. The round-12 ruling made the object store part of the model, and the route reproduces at this head. | `receipts/model_routes_head.txt` |
| R584-9-S1 (SUGGESTION: `census()` indexes `defs[0]` when the helper is bound only by assignment) | RETAINED SUGGESTION, still at `ctrl_pin.py:573` | source |
| R584-8-RES-1 | RETAINED RESIDUE for #495: `README.md:240` still reads "runs it, with GoogleTest and GoogleMock 1.14.0:" | source |
| R585-8-RS1; R584-7-RES1 / R585-7-RS1; R585-9's residue wording | RETAINED for the manager's #495 checklist. Not re-verified individually in this round. | — |
| R585-10 | Void (ended on a provider error, per the round-12 assignment); no findings to carry. | issue comment 6114400461 |

## Per-lens results

[R584] PASS Conformance - `receipts/pin_reachability.txt`, `core_tokens.txt`, `core_objects.txt`, `merge_audit.txt`, `pub_plants.txt`, `pub_campaign_head.txt`, `images/verdict.txt`, `acmp_tests_subset.txt` - Checked against acceptance 1 to 5 and the round-13 assignment items 1 to 5. The pin is the tagged `405dc683`, not `main`. The cores are token- and line-identical with byte-equal objects. The merge keeps the deletions, dev's adapter and both sides' CI jobs. The 11 plants are retargeted and caught by name. 35 of 35 images are identical to dev's. The 79 pin controls and the round-12 texts and allowlist are kept. The round-12 items 2 and 3 are met as ruled.

[R584] PASS RTL - `receipts/merge_audit.txt` (0 HDL, SV or syn files in `c20c85bd..8aaa2da7`), `tb/verilator/mbx/Makefile:71-111`, `acmp.h` token identity (`receipts/core_tokens.txt`), `receipts/images/verdict.txt` - No clock, reset, CDC, FSM or width change. The mailbox bench's merged targets keep `stack-pin` as an order-only prerequisite of every stack build, and `census` builds no stack. The firmware/core port contract (`struct acmp_ports`, including `publish`) is dev's token for token. The images are byte-identical. Hosted `firmware-verilator` ran the bench, the differential and the wire comparison at this head and passed.

[R584] UNCLEAN Robustness - `ctrl_build.py:425-439`, `receipts/model_routes_head.txt`, `receipts/inherited_probe_head.txt`, `receipts/pin_controls_py3*.txt` - The inherited-environment, repository-config (`core.worktree`) and hook plants are refused on both interpreters. F1 is open: a forged tree object is accepted.

[R584] UNCLEAN Tests - `ctrl_pin.py:902-985`, `receipts/pub_campaign_head.txt`, `pub_campaign_oldpath.txt`, `kill_words_differential.txt`, `tables_compare.txt`, `hosted_firmware_unit_extract.txt`, `pin_controls_py3*.txt` - The retargeted plants can fail and do; the old-path control refuses; no kill became unfindable; 79 of 79 pin controls pass. F1: no control holds the forged-object route, which lies inside the stated model.

[R584] PASS Docs - `sw/firmware/ctrl/README.md:150-215,240`, `docs/reference/SUBMODULES.md:20-30,228-252,286-296`, `docs/testing/CI_WORKFLOWS.md:95-120`, `ctrl_pin.py:45-62`, the PR body, `receipts/docs_gates.txt` - The pinned links, pin rows, diagram, tag statement and threat model are accurate at this head. The two in-model routes are disclosed honestly. RES-1 is residue. The docs, em-dash, idiom, submodule-docs, diagram and `ci_events` gates pass.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Acceptance 1-5 and round-13 items 1-5 against `pin_reachability.txt`, `core_tokens.txt`, `core_objects.txt`, `merge_audit.txt`, `pub_plants.txt`, `pub_campaign_head.txt`, `images/*`, `acmp_tests_subset.txt`; round-12 items 2-3 against `ctrl_build.py:180-381`, `ctrl_pin.py:11-62`, `README.md:150-215` | R584-11 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |
| RTL | CLEAN | `merge_audit.txt` (no HDL/SV/syn in the delta); `tb/verilator/mbx/Makefile:52-140`; `acmp.h`/`acmp_mbx.c` port contract; `images/*`; hosted `firmware-verilator` | R584-11 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |
| Robustness | UNCLEAN (F1) | `ctrl_build.py:180-439` (environment, judge, helper, `stack_pin`); `model_routes_head.txt`; `inherited_probe_head.txt`; `pin_controls_py314.txt`, `pin_controls_py312.txt` | R584-11 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |
| Tests | UNCLEAN (F1) | `ctrl_mutants.py:532-645` and `ctrl_mutant.py:13-17`; `pub_campaign_head.txt`, `pub_campaign_oldpath.txt`; `kill_words_differential.txt`; `tables_compare.txt`; `ctrl_pin.py:902-985` and its 79 controls on two interpreters; hosted `firmware-unit` extract | R584-11 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |
| Docs | CLEAN | `sw/firmware/ctrl/README.md`, `sw/firmware/ctrl/maap/README.md`, `sw/firmware/gtest/README.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/reference/SUBMODULES.md`, `docs/testing/CI_WORKFLOWS.md`, `tb/verilator/mbx/README.md`, the diagram and PNG manifest, the PR body; `docs_gates.txt` | R584-11 | 8aaa2da74e3d5ee569fed420debc2b69c6749d44 |

## Real limits

- No manager source bank, builder bank or native bank ran at this head, and none is claimed or inferred. This round ran:
  - focused probes: the token comparison, the core objects, the merge audit and the kill-word differential;
  - the 15 `pub-acmp-*` plants through the campaign's own functions;
  - both trees' image builders at every shape;
  - `pin_controls` on two interpreters;
  - the in-model route probes and the docs gates.
- This round did not run:
  - the complete firmware gate, the coverage ratchet, the full 506-plant campaign, or the AECP and SRP campaigns;
  - the full boundary self-test (`--without verilator` / `--only verilator`);
  - the 24-mutant hook-rule campaign, or the stack's own CMake/ctest suite.
  For those, the source-head evidence is the author's figures in the REVIEW READY, plus hosted `firmware-unit`, `firmware-boundary` and `firmware-verilator` passing at this head.
- The author's round-13 gate logs are not in the published evidence tree. `author-r13/round13/` holds only `review-ready-round13.md`, and `pin-proof.txt` holds the token and object figures. So the REVIEW READY's dev-versus-head plant-by-plant comparison, its coverage rows and its image manifest `8b1292db…` were not inspectable as logs. The claims this review relies on were reproduced independently instead.
- The SRP-composition images (30 of 35) were linked against a differential stand-in runtime. Both trees used the same archives, built from the repository's own `rv32_image/image_rt.c` and `image_arith.c` (`scripts/runtime.sh`), not the picolibc/compiler-rt runtime the author used. The comparison is valid as dev against the head; the absolute ELF hashes differ from the author's. The 5 `ctrl_image.py` images use no external runtime.
- CPython 3.12.3 here is a standalone build in a scratch venv with PyYAML 6.0.3, not the hosted Ubuntu interpreter. Host Git is 2.56.0.
- Hosted Verilator shards 1, 2 and 4 of the full gate were still running at the snapshot time. The manager owns hosted and act acceptance.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- F1: a ruling under option (b), or a round that implements option (a).
- RES-1 and the carried residue items (R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1, R585-9's wording) go to the #495 checklist.
- Publish the author's round-13 gate logs (boundary, verilator and unit jobs at `8aaa2da7`, and the dev-side run) beside the REVIEW READY, if they are to serve as source-head evidence.
- The final current-dev candidate: the builder and native banks at the merge turn (source base and live dev `c20c85bd`), and their receipts on the PR.
- Hosted completion of the remaining Verilator shards. `firmware-unit` headroom (41 min 28 s of 45 at this head) stays with #716.

## Receipts

Every receipt and script is listed in `MANIFEST.sha256`, with paths relative to this packet. The scripts are portable: each takes its trees and work directory as arguments.

R584-11 FINISHED
