[R582] NEGATIVE - exact head 651ccb5aea1bc4d99f356503c188947d39e0c9e4

# R582-2: internal independent re-review, issue #665 / PR #736 (F3b, milan-fpga half)

**Head and scope**

- Head under review: `651ccb5aea1bc4d99f356503c188947d39e0c9e4`, tree `efe717466398cf59ad71dc436feb74c6d1fe9c9d`. This is also PR #736's published head at review time (`headRefOid`, read 2026-10-13T21:03Z).
- Lane range: `d40e4e9827be2516f8f34b9d65f0a483fff2194c..651ccb5a`, four commits. The base is PR #705's reviewed head.
- Round-2 delta: `db29bdd0..651ccb5a`, three commits (`d8cae51e`, `2748ed52`, `651ccb5a`). All four commit messages are one line with no trailers.
- Source base and live dev: `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`.

**Scope sources**

- AGENTS.md and CONTRIBUTING.md; the issue #665 body.
- Assignment [6151273346](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151273346), as corrected by [6151422598](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151422598).
- Ruling [6092086337](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6092086337), items 4 and 5.
- The round-2 assignment [6153927545](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6153927545).
- The author's REVIEW READY (6152902757), the author's STOP (6154659374), and the PR body.

**Authorities**

- `protocol-processor/docs/architecture/05_acmp_engine.md:405` (F05.12).
- `protocol-processor/hdl/acmp/KL_acmp_talker.sv:397`.
- Stack `src/acmp.c:1250-1266` (`acmp_declaring`) and `:113-128` (the answered-probe stamp in `p_send`).
- `sw/mailbox/mailbox.yaml:323`.

**Review order.** I made my own pass over the diff, the tests and the executable evidence first. Only then did I read the prior public findings, R582-1 ([6153917004](https://github.com/kebag-logic/milan-fpga/pull/736#issuecomment-6153917004)) and R583-1 ([6153315844](https://github.com/kebag-logic/milan-fpga/pull/736#issuecomment-6153315844)). No private author material and no other reviewer's working notes were read.

## Verdict summary

The round-2 firmware is correct:

- Each DA_GATE source bit is now the stack core's own per-source `acmp_declaring` answer, ANDed with interface, MAAP validity and allocation index. This resolves R583-1-F1.
- R583-1's `probe_owner.cpp`, run unchanged, now passes.
- Every service figure on the design page recomputes from the compiled headers. This resolves R583-1-F2.
- The pin-control scratch lifecycle fix is present, and its six controls pass in both local boundary runs.

The verdict is NEGATIVE for one new BLOCKER:

- The round-2 commit `651ccb5a` added a firmware gate (`ctrl_service_bounds.py`) that reads `docs/design/MAILBOX_SPLIT.md`.
- It did not register that page as gate-read in `scripts/ci_scope.py`.
- The hosted `changes` job's classifier self-test therefore fails at this head. `rtl-fast` fails, and every firmware context, including `firmware-boundary` and `firmware-verilator`, is **skipped**, not executed.
- The round-2 acceptance item "rtl-fast, including firmware-boundary and firmware-verilator, is green at the new head" is therefore unmet.
- For the same reason R582-1-F1 stays open: its hosted proof is still missing.

## Findings

### R582-2-F1 - BLOCKER - Conformance, Tests

**Artifact:** `scripts/ci_scope.py:68` (`GATE_READ_DOCS`) against `sw/firmware/ctrl/test/ctrl_service_bounds.py:13` (`PAGE = ROOT / "docs/design/MAILBOX_SPLIT.md"`).

**Hosted evidence:** run [38464016325](https://github.com/kebag-logic/milan-fpga/actions/runs/38464016325) (`rtl-fast`, `pull_request`, attempt 1, head `651ccb5a`).

**Authority:**

- Round-2 assignment item 2 requires hosted `rtl-fast`, including `firmware-boundary` and `firmware-verilator`, green at the new head.
- AGENTS.md section 7 requires a successful `rtl-fast` at the current PR head. For an RTL/tooling-relevant PR it also requires exact-head `verilator-suites` and `yosys-portability`.
- Assignment item 5 requires that every touched gate passes.

**Evidence**

- `changes` job 115526169267, step "Classify the change conservatively", runs `python3 scripts/ci_scope.py --selftest` and prints:
  - `FAIL gate-read page docs/design/MAILBOX_SPLIT.md (named at sw/firmware/ctrl/test/ctrl_service_bounds.py:13) is relevant`
  - `selftest: 1 FAILURE(S)`, exit 1.

  Receipt: `hosted/rtl-fast-changes-job-115526169267-excerpt.log`.
- The `rtl-fast` aggregate job 115526473179 reports:
  - `CHANGES_RESULT: failure`;
  - `FIRMWARE_UNIT`, `FIRMWARE_CONTROL_MUTANTS`, `FIRMWARE_AECP_MUTANTS`, `FIRMWARE_SRP_MUTANTS`, `FIRMWARE_BOUNDARY`, `FIRMWARE_VERILATOR`, `PUBLICATION_CENSUS`, `VERILATOR_LINT` and `YOSYS_ELABORATION`: all `skipped`;
  - exit 1.

  Receipt: `hosted/rtl-fast-aggregate-job-115526473179-excerpt.log`.
- The same self-test failure stops `elaborate` (job 115526170541) and `rtl-full`'s `full-ci-gate` (job 115526170122). Receipts: `hosted/job-*-failures.log`.
- Because their shards never ran, `verilator-suites` and `yosys-portability` then fail on "found 0 shard directories".
- Full exact-head check-run table: `hosted/check-runs-651ccb5a.json`.
- **Local reproduction at this head:** `python3 -I scripts/ci_scope.py --selftest` returns rc 1 with the identical FAIL line (`ci_scope_selftest.log`, `ci_scope_selftest.rc`).
- **Cause:** the reader was added in this lane's round 2, and the page is not in the derived gate-read table. That table exists so a page a gate reads is never classified docs-only (#444, the `ci_scope.py:343` docstring).

**Impact**

- No hosted firmware gate executed at the PR head.
- The lane's boundary and pin proofs have no exact-head CI evidence, and neither does the round-2 harness fix for R582-1-F1.
- The classifier is also wrong in substance. A later docs-only edit to `MAILBOX_SPLIT.md` would skip the very firmware gate that now reads that page.

**Required outcome**

- `scripts/ci_scope.py --selftest` passes at the PR head, with `docs/design/MAILBOX_SPLIT.md` classified as gate-read (or equivalent, by the script's own derivation rule).
- The exact-head hosted `rtl-fast` succeeds with `firmware-boundary` and `firmware-verilator` **executed** and green.
- `elaborate`, `rtl-full`, `verilator-suites` and `yosys-portability` are no longer stopped by this self-test.

**Verification**

- Local: `python3 scripts/ci_scope.py --selftest` rc 0.
- Hosted: the exact-head check-run table shows the firmware jobs with conclusion `success`, not `skipped`.

### R582-2-S1 - SUGGESTION - Tests, Robustness

This retains and extends R582-1-S1. Reviewer plants in `sw/firmware/ctrl/maap/maap_mbx.c` (`scripts/r582_probes.py`, `runs/probes.log`) were applied to copies and judged across the `acmp`, `acmpif2`, `maap` and `maap_if2` arms. Five escaped:

| Plant | What it removes or moves | Why the escape is bounded |
|---|---|---|
| `r582-rx-refresh-removed` | The refresh at `:127` (receive) | The stack's `pump()` can report an allocation from RX, but the same pass's poll refreshes and rewrites the gate within one pass |
| `r582-link-refresh-removed` | The refresh at `:157` (link) | As above |
| `r582-poll-writes-before-maap-poll` | Computes the gate before `maap_poll` at `:169` | An allocation reported by a deferred ANNOUNCE in that poll is wrongly closed for one pass. The direction is conservative |
| `r582-range-cache-not-updated` | The cache write at `:96` | Only redundant writes result |
| `r582-allocation-filter-removed` | The `s < count` term at `:56` | The term narrows the gate beyond the core's own answer. No test drives demand on a source past the MAAP count; `srp_feedback.hpp:8` configures such a source, but gives it no demand |

None of these breaks a stated claim. Optional improvements:

- a deferred-ANNOUNCE (TX stall) allocation test under demand;
- a source past `count` with demand;
- or a statement that the RX and link refreshes are freshness-only.

Five plants were killed: interface filter, event refresh, poll refresh, demand reset, and (invalidly) MAAP validity. The last one failed to compile, so it is not counted as a kill. The author's `pub-maap-gate-open-while-invalid` plant covers that term and was caught in my control campaign.

### R582-2-R1 - RESIDUE - Docs (PR body only)

**Artifact:** the PR #736 body, section "Status" and two "Known limitations" bullets.

**Evidence:** the body still says:

- "Round 2 resumes `db29bdd0…`, still the published head of PR #736. The assignment prohibits pushing; this candidate is local."
- "Hosted `rtl-fast` at the local head cannot be proven under the no-push instruction."
- "This body is prepared for later publication; no PR or existing public comment was edited."

`651ccb5a` is now the published head. This is pure wording: it changes no figure, test, code or verdict.

**Exact fix:**

- In "Status", replace "Round 2 resumes `db29bdd07529fbc697b7956827092f64b1241714`, still the published head of PR #736. The assignment prohibits pushing; this candidate is local." with "Round 2 resumes `db29bdd07529fbc697b7956827092f64b1241714`; `651ccb5aea1bc4d99f356503c188947d39e0c9e4` is the published head of PR #736."
- Delete the two quoted limitation bullets.

## Prior public findings at this head

| Finding | Status at `651ccb5a` | Evidence |
|---|---|---|
| R583-1-F1 (MAJOR): DA_GATE substituted MAAP validity for per-source DA | **Resolved** | See below |
| R583-1-F2 (MINOR): four-module table and 10 ms conclusion stale | **Resolved** | See below |
| R583-1-R1 (RESIDUE): `SUBMODULES.md:256` sentence | **Resolved** | `:256` now reads "The current pin includes #19's `src/adp.c` discovery refusals." |
| R582-1-F1 (MAJOR): hosted `firmware-boundary` and `firmware-verilator` crash in `Clone.fresh` | **Retained (open)** | See below |
| R582-1-F2 (MINOR): `SUBMODULES.md:256` | **Resolved** | As R583-1-R1 |
| R582-1-R1 (RESIDUE): old-pin permalinks in `gtest/README.md` | **Resolved** | `git grep 405dc683` outside the submodule finds nothing |
| R582-1-S1 to S4 (SUGGESTION) | S1 and S2 retained, S3 partly addressed, S4 open | See below |
| Ruling 6092086337 item 4 (DA_GATE publishes the predicate) | **Resolved** | See below |
| Ruling 6092086337 item 5 (two-interface DA_GATE test) | **Retained** | `test_maap_mbx.cpp:200,216`; plant `rv-maap-gate-on-interface-0` caught |

**R583-1-F1, resolved.**

- `maap_mbx.c:36-48` caches `acmp_declaring(m->acmp, s)`, which is `dest_mac_valid && (answered || listener_registered)` (stack `acmp.c:1265`), before entering MAAP.
- `:50-62` ANDs it with interface, MAAP `valid` and `s < count`.
- No core is called from a MAAP callback. The owner callback asserts `!in_call` (`test_maap_mbx.cpp:59-63`), and plant `f3b-query-inside-allocation` was caught.
- New tests:
  - `AcmpMailbox.F3bListenerRequiresSourceDestination` and `F3bProbeRequiresSourceDestination` (`test_acmp_mbx.cpp:490-539`), each at IF1 and IF2: valid MAAP with invalid and then valid source DA, comparing the core predicate with the published bit on every interface;
  - `MaapHost.DaGateWaitsForSourceOwnerAfterAllocation` (`:303`).
- Plant `f3b-source-validity` was caught by all five named kills (`runs/control2.log`).
- R583-1's `probe_owner.cpp`, run unchanged (SHA-256 `075a7987…`, equal to R583-1's MANIFEST and to the author's copy), prints `core predicate=0 DA_GATE=0` for both the Listener and the answered-probe arm and passes its positive control: test rc 0 (`r583-probe/owner-probe.log`).
- Its driver returns rc 1 by design. It returns 0 only when the defect reproduces (`r583-probe/run_probes.py:45`).

**R583-1-F2, resolved.**

- My compiled headers give THREE 1,783 / 1,879 and PASS 3,523 / 4,429 (`runs/bounds_probe.txt`; R583-1's driver agrees, `r583-probe/bounds-if*.log`).
- Every row of `MAILBOX_SPLIT.md:702-760` rechecks with `(pass + 1) * cost` and `floor(10 ms / bound)`: 10,569 / 13,287; 38,753 / 48,719; 77,506 / 97,438; 31,707 / 39,861; and the three-module rows 5,349, 19,613, 39,226 and 16,047.
- The conclusion "event envelopes are 10.569 / 13.287 ms … neither fits" is correct.
- The new arm `service_bounds` passes, with 47 checks and 0 failures (`runs/normal2.log:63`).
- The model's measured worst passes, 231 / 233, still match the page (`runs/normal2.log:131,188`).

**R582-1-F1, retained (open).** The fix is present and passes locally:

- `ctrl_build.py:194-196` defines `NO_MAINTENANCE` and adds it to `HELPER_CONFIG` on every helper Git call.
- `ctrl_pin_env.py:62` (`create`) persists `gc.auto=0` and `maintenance.auto=false` in every scratch init and clone.
- `ctrl_pin.py:735-757`: `vanished` swallows only `FileNotFoundError`.
- Six lifecycle controls (`ctrl_pin_lifecycle.py`) are all `[ok]` in both `runs/boundary_verilator.log` and `runs/boundary_host3.log`. They cover: persisted settings, command overrides, loose fetch then fresh clone, a vanishing file tolerated, and EACCES and EIO propagated.

Its required outcome, exact-head hosted `firmware-boundary` and `firmware-verilator` green, is still unmet: both were skipped at this head (R582-2-F1).

**R582-1 suggestions.**

- S1 (refresh plants): still escapes; retained as R582-2-S1.
- S2 (funded clock-read worst case never driven): `CallbackWorkAndEveryOutputCount` (`test_maap_mbx.cpp:526-538`) still registers Listeners only, so it is retained.
- S3 (latency figures): partly addressed. `maap/README.md` now says the gate opens "on the next MAAP poll".
- S4 (#23 in the PR body): the body still names only #19, #20 and #25. It remains optional.

**Ruling item 4, resolved.**

- `mailbox.yaml:323` and its generated copies state the `acmp_declaring_o` equivalence.
- `MAILBOX_SPLIT.md:1060` drops the egress-consequence choice ("Three choices are the firmware's").

## Assigned verification points

1. **Pin, confirmed.** Receipt: `runs/pin-audit.txt`.
   - The gitlink is `70936b77`, with 45 changed paths from `405dc683`; the merge-base is `1a9f651c`.
   - The range commits are #19 `51870377`, #20 `98dc9e30`, #23 `1ba27354` (the reviewed integration of the old pin's own content) and #25 (five commits plus merge `70936b77`).
   - Each squash tree equals its reviewed head's tree (#19 `66b3a757`, #20 `0c5ef532`, #23 `3c9ca52f`, #25 `f13c9c16`). Each has POSITIVE exact-head verdict lines: R576/R577, R578/R579, R622/R623 plus the #23 merge-bar record, and R630/R631.
   - The core `src`/`include` delta is only `src/adp.c`, byte-equal to #19's own delta, plus `src/acmp.c` and `include/acmp.h` (#25).
   - #23's conflict resolution touches no core path.
   - Nothing is unmerged or unreviewed.
2. **Parent-harness tests for each parent-visible effect, confirmed.**
   - ADP: `AdpAdapter.PinRejects*` and `PinAcceptsCompleteDiscoveryThroughMailbox`; all four `pin-adp-*` plants caught.
   - Predicate: the `MaapHost.DaGate*` and `AcmpMailbox.F3b*` tests.
3. **DA_GATE predicate, confirmed.**
   - The predicate is valid DA (owner `dest_mac_valid`, together with MAAP validity and allocation) AND (answered probe younger than 15000 ms OR registered Listener).
   - The interface filter is applied; gate-before-allocation-report ordering is kept (`maap_mbx.c:96-98`).
   - Idle expiry: `ctrl_app.c:78-81` enables the tick, and every poll refreshes.
   - The contract text states the equivalence, and the design page drops the egress choice.
4. **Controls per arm, confirmed.**
   - Arms: fresh probe, Listener, neither, aged probe (14999 / 15000 / 15001 ms), and invalid source DA for both demand arms at IF1 and IF2.
   - The two-interface DA_GATE tests are kept.
   - Control campaign: **520 of 520 caught** (`runs/control2.log`). This is the one new round-2 plant on top of round 1's 519.
5. **Images, confirmed for ADP-ACMP-MAAP.**
   - I rebuilt `ctrl_image.py --base d40e4e98` for all five shapes. All 10 ELF SHA-256 values equal the author's round-2 table (`runs/image_elf_hashes.txt`).
   - Load growth is +988 B on every shape (`runs/images.log`). `ctrl_image_selftest.py` passes 33 checks.
   - The SRP and SRP-AECP rows (maximum +1,304 B, under the +2,048 B Release ceiling of tsn-c-stack#24 comment 6126295947) need runtime archives I did not build; they are author receipts.
   - All-fabric BIOS 52988 B and AEM 7512 B were not rebuilt. They are corroborated by construction: the round-2 source changes are `maap_mbx.c`, `maap_mbx.h` and `mbx.h`, which `milan_soc.py` reaches only through `--ctrl-mailbox`, off by default (`:2613`).
   - No firmware behaviour change beyond the predicate and the listed pin effects was found.
6. **Gates.**
   - Local results: listed in the evidence section.
   - Hosted results at exact head: `rtl-fast` **failure**, with every firmware context **skipped** (F1); `elaborate` failure; `rtl-full` failure; `bdd-conformance`, `wire-accountability` and `docs-check-no-git` success; `docs` still in progress at 21:03Z.
   - "Physical gPTP" was skipped, and a skipped context is not execution evidence.

## Independent execution evidence (all at this head)

Firmware suites and campaigns:

| Run | Command (abridged) | Result |
|---|---|---|
| `runs/normal2.*` | `test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4` | rc 0. Shard inventory 938 invocations, `[61, 521, 77, 279]`; service bounds 47/0 |
| `runs/control2.*` | `--shard 1/4` | rc 0, **520 of 520 caught** |
| `runs/aecp2.*` | `--shard 2/4` | rc 0, 76 `[ok]`, 0 escaped |
| `runs/srp2.*` | `--shard 3/4` | rc 0, 280 `[ok]` (278 plants and 2 lwSRP pin controls), 0 escaped |
| `runs/coverage2.*` | `fw_coverage.py --check --jobs 4` | rc 0, 30 files at 100% after exclusions; `maap_mbx.c` 127/127 lines, 82/82 branches |

Boundary runs:

| Run | Command (abridged) | Result |
|---|---|---|
| `runs/boundary_host3.*` | `ctrl_boundary.py --require-rv32 --selftest --without verilator` | rc 0, PASS. 2,854 compiled sources from 3,084 invocations; 126 pin controls, including 6 lifecycle controls. A local LiteX tree was on `PYTHONPATH`, read-only, with bytecode writing disabled |
| `runs/boundary_verilator.*` | `--only verilator`, with the pinned Verilator 5.050 (`runs/verilator_identity.txt`) | rc 0, PASS. 829 compiled sources from 926 invocations; 126 pin controls |

Images and controls:

| Run | Command (abridged) | Result |
|---|---|---|
| `runs/images.*` | `ctrl_image.py --base d40e4e98`, five shapes | rc 0, ELF hashes match the author's |
| `runs/image_selftest.*` | `ctrl_image_selftest.py --require-rv32` | rc 0, 33 checks PASS |
| `r583-probe/*` | R583-1's `run_probes.py` and `probe_owner.cpp`, unchanged | Test rc 0; driver rc 1 by design |
| `runs/probes.*` | `scripts/r582_probes.py`: reviewer plants on copies | 5 killed, 5 escaped (S1) |
| `ci_scope_selftest.*` | `scripts/ci_scope.py --selftest` | **rc 1** (F1) |

Documentation and tooling gates (`runs/gate_*`), all rc 0:

- `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`;
- `check_em_dash.py --base d40e4e98` and `gen_toc.py --check`, both with the pinned Markdown renderer;
- `check_submodule_docs.py`, `check_hygiene.py --check`, `measure_test_evidence.py --check`;
- `gen_mailbox.py --check --crosscheck --selftest`, `submodule_boundaries.gen.py --check`;
- `check_py_idiom.py`, `check_rtl_source_lists.py`.

The run scripts are `scripts/launch.sh` and `scripts/wait.sh`. Each run has `.cmd`, `.time`, `.log` and `.rc` files.

**Final integrity** (`runs/integrity-final.txt`):

- The index listing and every tracked file's bytes have the same SHA-256 as the pre-review baseline.
- `git status --porcelain --ignored` shows 0 lines, and every submodule is clean.
- All six gitlinks are unchanged; tsn-c-stack is `70936b77`.
- The ignored build products my runs created (`__pycache__` and `tb/verilator/mbx/obj_*`) were removed with `git clean -fdX` after inspection.

## Reviewer-owned lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R582-2-F1; R582-1-F1 retained) | Assignment, correction, round-2 assignment; ruling 6092086337 items 4 and 5; processor `05_acmp_engine.md:405`, `KL_acmp_talker.sv:397`; stack `acmp.c:113-128,1237-1266`; `maap_mbx.c:36-98,163-180`; `acmp_mbx.c:102`; `mailbox.yaml:323`; `runs/pin-audit.txt`; R583-1 owner probe; hosted run 38464016325 | R582-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |
| RTL | CLEAN | No HDL change in round 2. `KL_mbx_pkg.sv` lane change is a generated comment (`gen_mailbox.py --check --crosscheck --selftest` rc 0). Firmware widths and indexing: `maap_mbx.c:40-58` (`UINT32_C(1) << s`, `s < n_sources <= 16`), `published_gate[MBX_N_IF]`. Access bounds: `maap_mbx.h:19-23`, `acmp_mbx.h:136`, compiled 801/866, 1,783/1,879, 3,523/4,429 (`runs/bounds_probe.txt`) | R582-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |
| Robustness | CLEAN | Invalid source DA with both demand arms (`test_acmp_mbx.cpp:490-539`, owner probe); expiry at 15000 ms and idle tick (`ctrl_app.c:78-81`, `test_acmp_mbx.cpp:447`); MAAP loss closes before report (`test_maap_mbx.cpp:294`); no-owner path (`maap_mbx.c:39,53`); reentry count 0; scratch-removal error paths (`ctrl_pin.py:735-757`, lifecycle EACCES/EIO/ENOENT controls); escaped plants analysed for bounded effect (S1) | R582-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |
| Tests | UNCLEAN (R582-2-F1; R582-1-F1 retained) | `test_acmp_mbx.cpp:447-539`; `test_maap_mbx.cpp:173-312,526`; `ctrl_mutants.py:503-555,745-760`; `ctrl_service_bounds.py`; `ctrl_pin_lifecycle.py`; shards 0 to 3 (520/76/278 plus 2, 0 escaped); coverage; both boundary runs; reviewer probes; `scripts/ci_scope.py --selftest` rc 1; hosted check runs | R582-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |
| Docs | CLEAN (RESIDUE R582-2-R1 carried) | `MAILBOX_SPLIT.md:648-760,823,1060-1090` (recomputed); `SUBMODULES.md:24,214-262` (`:256` corrected); `sw/firmware/ctrl/README.md:62-90,196-260,381-445`; `maap/README.md:109-165`; `gtest/README.md:243-320`; `mbx.h:95`; `mailbox.yaml:323` and generated copies; doc gates rc 0; PR body | R582-2 | 651ccb5aea1bc4d99f356503c188947d39e0c9e4 |

## Real limits

- **Not rebuilt:** the all-fabric BIOS and AEM binaries, and the SRP and SRP-AECP image rows (no runtime archives here). The standalone stack `validate.py` and `baremetal.py` were not run; they are stack-owned, and #25's reviews and the author's receipts cover them. The publication census was not run (pinned sv2v not checked here); its only change is a description string.
- **Python version:** local Python runs used host CPython 3.14.7. The pinned CPython 3.12.3 here lacks PyYAML, and the first attempts with it were discarded. Hosted runs use 3.12.3. The `rmtree(onerror=...)` path behaves the same in both.
- **Stack submodule object store:** my provenance checks ran `git fetch` (redundant: the commit was already present) and `git merge-tree --write-tree`. These added objects and a `FETCH_HEAD` to the stack submodule's object store. No ref, index, worktree or gitlink changed (`runs/integrity-final.txt`).
- **DA validity timeline (not examined):** firmware DA validity follows the MAAP adapter and the integrator's source owner. Whether the firmware has an equivalent of the processor's post-conflict `BACKOFF` (F05.12) belongs to the MAAP and owner lanes, and I did not examine it.
- **Specification text:** the Milan v1.2 and IEEE texts were not read directly. The processor page and RTL, plus the stack's comments, served as the predicate authority.
- **No manager source bank:** no manager source bank ran at this head, and none is claimed or inferred.
- **Hardware:** physical calibration was NOT RUN. Skipped field and physical contexts are not hardware proof.

## Pending manager duties

- Disposition and repair of R582-2-F1, then exact-head hosted acceptance: `rtl-fast` with `firmware-boundary` and `firmware-verilator` executed and green, plus `elaborate`, `rtl-full`, `verilator-suites` and `yosys-portability`. That hosted run also closes R582-1-F1.
- Carrying R582-2-R1 to the residue checklist.
- An independent re-review at the corrected head.
- The current-dev candidate merge build (builder and native banks) with public receipts, candidate-merge validation, the merge of dev after #705 lands, explicit merge authorization, and post-merge containment.

R582-2 FINISHED
