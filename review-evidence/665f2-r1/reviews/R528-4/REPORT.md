[R528] POSITIVE - exact head 5968967e19411428b71dde5c4712d4a8fa528cfb

# R528-4: internal cleared-context review of PR #687 (issue #665, lane F2), final merge round

- Head `5968967e19411428b71dde5c4712d4a8fa528cfb`, tree `df2c47e21f7c068b245236ab477b5c6313036538`.
- Delta reviewed: `8b78a8fd..5968967e`. That is the `--no-ff` merge `d4bc335c`, with ordered parents
  `8b78a8fd` and authorized dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` (FC plus #677). Two later
  commits, `24be55fc` and `5968967e`, change only README files.
- Governing assignment: #665 comment 6033552374. Acceptance addition: 6030870481. Lane rules: 6026720272.
- Sources, in order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #665 body and the manager comments
  above. Then the diff and history. Then the author's round-4 packet (evidence branch `d56236ac`:
  HANDOFF.md and PR-BODY.md, sha256 `9e0c0eca...` and `8dbe4b6a...`, matching REVIEW READY 6034588675).
  Then my own executable evidence. I read the round-3 public findings (R528-3, R529-3) only after my
  independent pass over the diff. I read no other round-4 report.

## Verdict summary

No BLOCKER, MAJOR or MINOR is open. All five lenses are covered clean at this head.

- **Merge.** The merge keeps both sides.
  - The merged controller catalog is exactly the union of the two parents' catalogs: 193 + 100 -> 196,
    with no record changed.
  - All #677 arms, checks, planted defects and the `assert.h` allowance are present and live.
  - All F2 MAAP arms, partitions and planted defects are present and live.
- **Round-3 finding.** R528-3-F1 / R529-3-F1 is resolved. The MAAP README uses `MILAN_RV32_CC`, and
  the selector probe shows the named compiler wins.
- **R528-3-S1** is addressed, and its limit is stated honestly. My probe shows that a debug RV32 link
  fails on exactly one symbol, `__assert_fail`.
- **Linked image.** My independent link of the composed `ctrl_app` reproduces the author's report
  within 0.6 %. It is a real link: MAAP code is linked in, nothing is unresolved, and the
  formatter is gc'd. The `ctrl_app` object sizes match exactly.
- **Gates.** The firmware gates pass at this head: 196/196 controller defects, 109/109 NVM defects,
  coverage 17/17, differential 12 + 16/16, mailbox suite and docs gates.
- **Probes.** Ten merge-sensitive planted defects or regradings behave as predicted.
- **Open items.** Two wording-only RESIDUE items and two optional SUGGESTIONs, below.

## Findings

### R528-4-R1 RESIDUE - Docs

- **Artifact:** PR #687 body, section "Round 4", first paragraph. The live body differs from the
  archived PR-BODY.md only by one trailing newline. The sentence is "No check meaning changed or
  required a relaxed verdict."
- **Evidence:**
  - At dev `d51b373a`, `ctrl_build.py` `RV32_FLAGS` had no `-DNDEBUG`, and its comment read "ADP's
    re-entry guard asserts in this (NDEBUG-free) build".
  - At this head, `sw/firmware/ctrl/test/ctrl_build.py:42` adds `-DNDEBUG`. So the `rv32` arm now
    compiles dev's ADP objects in the release profile: its undefined set has no `__assert_fail`
    (`receipts/head/ctrl_arms.log`).
  - This changes one check's build profile. The body's next sentences disclose the change and the
    separate debug-profile check, so no evidence is missing.
  - Probes D and E show the arm passes in both profiles. `receipts/rv32_debug.json` reproduces the
    debug profile.
- **Impact:** Wording only. It changes no test, measurement, verdict or code.
- **Exact fix:** Replace the sentence with: "One check's build profile changed: the regular `rv32` arm
  now compiles dev's ADP objects with `-DNDEBUG` (F2's release profile), where dev's arm kept
  assertions; no failure obligation was relaxed, and the assertion-enabled profile was checked
  separately at this head."
- **Verification:** Read the corrected paragraph against `ctrl_build.py:42`. This item goes to the
  manager's residue checklist.

### R528-4-R2 RESIDUE - Docs

- **Artifact:** `sw/firmware/gtest/README.md:273`, inherited from #677: "Debug/test builds assert;
  release builds ignore and count violations."
- **Evidence:**
  - After the merge, the regular host test arms compile with `-DNDEBUG`
    (`ctrl_build.py:40`, F2's host flags), so they take the release path.
  - Only `reentry_debug` and `maap_debug` compile with `-UNDEBUG` (`ctrl_arms.py:47,70`).
  - The authoritative contract, `adp/adp.h:139` "Debug/test builds (NDEBUG absent) assert", is
    correct.
  - Probe J shows the host-flag choice is graded: dropping `-DNDEBUG` from the host flags fails
    `MaapCore.ReentrantPortsAreCountedAndIgnored`. So no test claim rests on this sentence.
- **Impact:** Wording only. A reader may assume the regular host arms run with assertions.
- **Exact fix:** "Builds without `NDEBUG` (the `reentry_debug` and `maap_debug` arms) assert; builds
  with `NDEBUG`, including the regular host arms and the `rv32` object arm, ignore and count
  violations."
- **Verification:** Read the sentence against `ctrl_build.py:40` and `ctrl_arms.py:47,70`. Residue
  checklist.

### R528-4-S1 SUGGESTION - Tests, Docs

- **Artifact:** `sw/firmware/ctrl/test/ctrl_build.py:45-47` (`RV32_LIBC` includes `__assert_fail`),
  `sw/firmware/ctrl/test/ctrl_arms.py:223` (`arm_rv32`) and `sw/firmware/ctrl/maap/README.md:145`.
- **Evidence:**
  - Probe D removes `__assert_fail` from the allowance, and every controller arm still passes. No
    gated controller build is assertion-enabled, so the allowance is not exercised by any gate.
  - Probe F drops `-DNDEBUG` and the allowance together; the `rv32` arm then fails on
    `__assert_fail`. So the allowance matters only for the debug profile.
  - `maap/README.md:145` ("A debug RV32 compile also passes") is true at this head (my
    `rv32_debug.json`), but it is one-off evidence.
- **Suggested outcome (optional):** have `arm_rv32` also compile the portable set with `-UNDEBUG` and
  apply the same ABI and symbol checks. Then the allowance and the README sentence are protected
  against regression.

### R528-4-S2 SUGGESTION - Tests

- **Artifact:** `sw/firmware/ctrl/test/test_ctrl_firmware.py:128-135` (the baseline arm list) and
  `ctrl_mutants.py:518-523` (the campaign's arm map).
- **Evidence:**
  - Probe A drops `reentry_debug` and `reentry_release` from the baseline list, the merge-sensitive
    hunk. The baseline gate still passes.
  - The coverage gate still runs both arms, and probe B shows it catches their removal there.
  - This harness shape is inherited, not introduced by this delta.
- **Suggested outcome (optional):** self-check that the baseline list covers every key of the
  campaign's arm map, so a future merge cannot silently drop an arm from the baseline run.

## Clean-lens results at this head

[R528] PASS Conformance - assignment 6033552374 items 1-5; `sw/firmware/ctrl/maap/README.md:156`; `receipts/image/link_5968967e.json`; `receipts/rv32_debug.json`; `git diff d51b373a 5968967e -- hdl syn configs` (empty) - Item 1: the merge keeps both sides (catalog union, arms, assert.h allowance), and the one re-graded profile is disclosed (R1 is wording only). Item 2: the selector is `MILAN_RV32_CC`, and `grep -rn CTRL_RV32_CC sw docs scripts` returns rc 1. Item 3: the debug `maap.c` compile passes with the pinned SDK, and the limit is exact (only `__assert_fail` is unresolved in a debug link). Item 4: the linked image is real and reproduced for the shipping shape and the largest shape, at one and two interfaces, with static pools and the delta from dev. Item 5: the gates were re-run. No RTL, configuration or shipping-default change against dev. The Annex B scope (`maap.c`, `maap_mbx.c`, `maap_csr.c`, `ctrl_app.c`) is byte-identical to the R528-3 head `8b78a8fd`, so that round's Annex B conformance carries forward.

[R528] PASS RTL - `git diff 8b78a8fd 5968967e -- hdl tb sw/mailbox` (empty); head equals dev for `hdl`, `syn`, `configs` and all four gitlinks; `receipts/head/mbx_make.log`; `receipts/head/ctrl_arms.log` rv32 lines - F2 still makes no RTL, register or interface change. With the pinned 5.050 simulator (identity verified), the mailbox suite passes: Wishbone 316, AXI4-Lite 361, co-sim 13, two-interface 316/361/316, and 5/5 RTL controls. The RV32 arm (pinned SDK, sha256 matches `ci_rv32_sdk.py`) passes 12 objects: text 20028, data 0, bss 178, largest static frame 112 B, release profile.

[R528] PASS Robustness - `sw/firmware/ctrl_nvm/nvm_klj2.c:298-299`; `sw/firmware/ctrl/adp/adp.c:27-35`; `sw/firmware/ctrl/maap/maap.c:13-24`; probes G, H, J - #677's erased-prefix guard is live (probe G: removing it aborts `NvmCodec.codec_erased_loaded_prefix` under the sanitizer). The ADP re-entry assertion is live (probe H: neutering it fails three named `reentry_debug` tests). MAAP release re-entry counting is graded under the merged host flags (probe J). The 122 debug and 122 release re-entry cases pass in the composed tree.

[R528] PASS Tests - `receipts/catalog_union.json`; `receipts/head/ctrl_mutants_s{0..3}.log`; `receipts/head/nvm_selftest.log`; `receipts/head/fw_coverage_check.log`; `receipts/head/maap_differential.log`; `receipts/probes/*.json` - The merged catalog equals the exact union of both parents (193 + 100 = 196; 3 dev-only reentry defects; 96 MAAP; no changed record). Campaign: 196/196 caught in four disjoint shards of 49. NVM: 435 tests across 5 shapes, 109/109 caught. Coverage: 17/17 files at 100 % after the unchanged exclusions; the self-test passes 28/28. Differential: 12/12 baseline and 16/16 controls. The RV32 self-test passes 17/17 and the tally self-test 18/18. All ten reviewer probes behave as predicted.

[R528] PASS Docs - `sw/firmware/ctrl/README.md:25,58-62`; `sw/firmware/ctrl/maap/README.md:141-156`; `sw/firmware/gtest/README.md:346-350`; the PR body "Round 4"; `receipts/docs/*.log` - The README resolution carries both arm populations and drops the stale arm count. The MAAP and gtest wording on release versus debug is accurate. The linked-image text and figures match my independent link within 0.6 %. 18 docs gates pass at rc 0 (docs_check, doc paths and style, em-dash against dev, TOC check and anchors, idiom, port, bare-metal, hygiene, TODO, ratchets, feature status, solution and submodule docs). R1 and R2 are wording-only RESIDUE and leave the lens clean.

## Assignment items, in detail

### 1. Merge resolution

- Merge mechanics: `d4bc335c`'s ordered parents are `8b78a8fd` and `d51b373a`. Both
  `021b9c1f`/`db9aa8c9` (FC) and the #677 commits `6c94e9f5`, `34475e77` and `708e5634` are ancestors.
- Method: I re-ran the three-way merge myself for every file both sides touched, with base `09f1841b`
  (the merge of the two merge bases `910f338d` and `db9aa8c9`). I then compared the committed result
  hunk by hunk.
  - `ctrl_arms.py`: the conflict is resolved to both sides, the MAAP arms plus dev's `reentry*` arms.
  - `ctrl_mutants.py`: the conflict is resolved to the union arm map plus dev's `jobs` argument.
  - `test_ctrl_firmware.py`: the baseline list, coverage list and argument parser each carry both
    sides, including `--mutation-shard` and `--jobs`.
  - `README.md`: the contents line is re-worded without a count, and the `reentry` and `rv32` rows are
    taken from dev.
  - `ctrl_build.py` merged cleanly. One comment was rewritten so that it no longer claims an
    NDEBUG-free build.
  - `coverage.ratchet` merged cleanly: dev's higher ADP and NVM rows plus F2's three MAAP rows.
- Every file only one side touched is byte-identical to that side.
- Commits: three, each with a one-line subject and no body or trailers.

### 2. R528-3-F1 / R529-3-F1

Resolved. `receipts/selector_probe.log` shows:

- The README line (`:156`) uses `MILAN_RV32_CC`.
- With a competing pinned-SDK default on `PATH`, the literal prefix selects `riscv64-elf-gcc`.
- The retired `CTRL_RV32_CC` would select the SDK default instead (control).
- With no competing default, the prefix also selects `riscv64-elf-gcc`.
- The grep over `sw`, `docs` and `scripts` returns rc 1 (no matches).

### 3. R528-3-S1

Addressed. With the pinned SDK (riscv32-linux-gcc 14.3.0) and the gate's flags minus `-DNDEBUG`
(`receipts/rv32_debug.json`):

- `maap.c` compiles to RV32I/ILP32 with no ABI findings. Its undefined symbols are exactly
  `__assert_fail`, `__lshrdi3`, `__umodsi3`, `memcpy` and `memset`.
- All twelve controller/MMIO objects compile: text 20130, data 0, bss 171. Nothing falls outside the
  allowance.
- The author reports 20126 text bytes for the twelve objects, 4 B less. This does not change any
  conclusion.
- Limit, checked: a debug link of the composed app (`receipts/image/link_debug_5968967e.txt`) fails
  in all ten shapes on exactly one undefined reference, `__assert_fail`. The header declares the
  handler and supplies none, as the MAAP README now states.

### 4. Linked RV32 image (acceptance addition 6030870481)

Method (`scripts/link_image.py`):

- Export each tree. Generate each config's entity header with the tree's own `adp_entity.py`.
- Compile the tree's own `PORTABLE` set plus `plat/mbx_plat_mmio.c` with its `RV32_FLAGS`.
  - Release profile throughout: `-DNDEBUG` is added to dev, whose arm omits it.
  - Also `-ffunction-sections -fdata-sections`, with the gate's freestanding include set.
- Add a reviewer-written entry that calls `ctrl_app_start_maap(..., maap_csr_allocation, &csr, 0)`
  and then `ctrl_loop_run`. Dev's entry calls `ctrl_app_start`.
- Link with a reviewer linker script: `-nostdlib`, `--gc-sections`, `--no-undefined`, a 4 KiB NOLOAD
  stack, rv32i/ilp32 newlib `libc.a` and `libgcc.a` (bare-metal GCC 15.2.0, newlib 4.6).

Results:

| Image (bytes) | text | rodata | data | bss | sum before stack | `app` object | MAAP symbols linked | undefined |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dev, 1 interface, every shipped config | 8376 | 180 | 0 | 2189 | 10745 | 2076 | 0 | 0 |
| head, 1 interface, every shipped config | 14336 | 192 | 0 | 3325 | 17853 | 3184 | 11 | 0 |
| delta, 1 interface | +5960 | +12 | 0 | +1136 | +7108 | +1108 | | |
| dev, 2 interfaces (`--variant-interfaces 2`) | 8768 | 180 | 0 | 2277 | 11225 | 2168 | 0 | 0 |
| head, 2 interfaces | 15056 | 192 | 0 | 4477 | 19725 | 4336 | 11 | 0 |
| delta, 2 interfaces | +6288 | +12 | 0 | +2200 | +8500 | +2168 | | |

- **Real link.** The MAAP adapter, core and CSR functions are present in the final ELF, nothing is
  undefined, and `vsnprintf` is removed by gc.
- **Agreement with the author.** The `app` and `csr` (32 B) object sizes match the author's report
  exactly. Section sums agree within 0.6 %: author 10688 / 17780 / 11172 / 19652 against mine
  10745 / 17853 / 11225 / 19725. The remaining differences come from our different entry/arena
  scaffolding (mine uses a 64-byte arena and its own CSR accessors).
- **Shape independence.**
  - All five shipped configs give identical sections at each interface count, as the author reports.
  - The composed state's only array dimensions are `MBX_N_IF`, `MBX_N_CH` and fixed constants
    (`maap.h:27,62`, `maap_mbx.h:35`, `adp_mbx.h:142`, `ctrl_loop.h:124-129`, `ctrl_pool.h:60`).
    Entity shape changes immediates only.
  - So the author's 15x16 capacity fixture, which is not public, cannot change the size. The
    two-interface variant is the largest measured shape.
- **Budget.** With the 4 KiB stack, the largest head image is about 23.8 KB, well below the ~128 KB
  planning budget.
- **Not established.** This is sizing scaffolding only: not a boot image, a stack proof or a routed
  fit.

### 5. Firmware gate re-run at this head (`receipts/head/`, `receipts/docs/`)

| Gate | Result |
|---|---|
| `test_ctrl_firmware.py --require-rv32` (pinned SDK) | PASS. model 22, port 31, adp 26, unit 23+2, walk 41, entity 5x9, rv32 PASS, maap 37+12, maap_debug 1, maap_if2 13, reentry_debug 122, reentry_release 122 |
| `--self-test --mutation-shard i 4`, i = 0..3 | 49/49 in each shard; 196 unique defects, 196 caught |
| `test_ctrl_nvm.py --require-rv32 --self-test` | 5 shapes, 435 tests, 109/109 planted defects |
| `fw_coverage.py --selftest` / `--check` | 28/28 / PASS, 17 files at 100 % after exclusions |
| `fw_rv32_selftest.py --require-rv32` | 17 checks PASS |
| `tally_selftest.py` | 18/18 |
| `maap_differential.py --self-test` | 12 tests PASS; 16/16 controls |
| `make -C tb/verilator/mbx` (pinned 5.050) | WB 316, AXI-Lite 361, co-sim 13, if2 316/361/316, controls 5/5 |
| Docs gates (18 commands) | all rc 0 |

### Reviewer probes (`receipts/probes/`, `scripts/probe.py`; disposable clones, head bytes restored)

| Probe | Plant | Expectation | Result |
|---|---|---|---|
| A | drop the reentry arms from the baseline list | baseline still passes (gate blind) | rc 0, as predicted (S2) |
| B | drop the reentry arms from the coverage list | coverage fails | adp.c 189/203 lines, 83/93 branches, below the ratchet |
| C | drop `maap_if2` from the coverage list | coverage fails | maap_mbx.c 53/60 branches |
| D | drop `__assert_fail` from `RV32_LIBC` | passes (allowance unexercised) | rc 0, as predicted (S1) |
| E | dev's RV32 profile (drop `-DNDEBUG`) | passes | rc 0 |
| F | E plus D | rv32 fails | `[FAIL] symbols outside the C library and libgcc: __assert_fail` |
| G | remove #677's loaded-prefix guard (`nvm_klj2.c:298-299`) | NVM fails | `NvmCodec.codec_erased_loaded_prefix` aborts |
| H | `assert(!port_active)` -> `assert(1)` | reentry_debug fails | three named AdpReentry/AdpPortEntry failures |
| J | dev's host flags (drop `-DNDEBUG`) | maap fails | `MaapCore.ReentrantPortsAreCountedAndIgnored` aborts |
| K | drop the maap.c ratchet row | coverage fails | "measured, but the ratchet does not record it" |

## Prior public findings at this head

| Finding | Status at `5968967e` |
|---|---|
| R528-3-F1 MINOR (Docs) / R529-3-F1 MINOR (Docs, Tests): retired selector in the MAAP recipe | RESOLVED. `maap/README.md:156`; selector probe; grep rc 1 |
| R528-3-S1 SUGGESTION (Docs): debug target build and `assert.h` | ADDRESSED. `maap/README.md:144-146`; debug compile and debug-link limit reproduced |
| R529-3-R1 RESIDUE (Docs): "The branch has not been pushed" | RESOLVED. The sentence is absent from the live body |
| R528-1-F1..F6, R529-1-F1/F2, R528-1-S1, R528-2-S1, R528-2-R1 (all resolved by round 3) | RESOLVED, retained. The MAAP sources, tests, mutants and differential are byte-identical to `8b78a8fd` (`git diff 8b78a8fd 5968967e` touches only `maap/README.md` in F2's scope). Every named control is caught again in the 196/196 campaign and the 16/16 differential. R528-2-R1's "ten arms" wording was replaced by count-free wording that remains accurate with twelve arms. |

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment items 1-5 and acceptance addition 6030870481; merge resolution; linked image; no-default-change check against dev; Annex B scope unchanged since round 3 | R528-4 (delta, acceptance); R528-3 for the unchanged Annex B scope | `5968967e19411428b71dde5c4712d4a8fa528cfb` (R528-3: `8b78a8fd36864246336c71c061ac4f21d629952f`; MAAP sources unchanged since) |
| RTL | CLEAN | hdl/tb/mailbox delta (empty); head equals dev for hdl/syn/configs/gitlinks; mailbox suite with the pinned simulator; RV32 ABI/frame checks with the pinned SDK | R528-4; R528-3 for F2's unchanged interface scope | `5968967e19411428b71dde5c4712d4a8fa528cfb` |
| Robustness | CLEAN | #677 erased-prefix guard and ADP re-entry guard live in the composed tree; MAAP release re-entry graded; probes G, H, J | R528-4 | `5968967e19411428b71dde5c4712d4a8fa528cfb` |
| Tests | CLEAN (S1, S2 optional) | Catalog union; 196/196; NVM 109/109 and 435 tests; coverage 17/17; differential; self-tests; probes A-K | R528-4 | `5968967e19411428b71dde5c4712d4a8fa528cfb` |
| Docs | CLEAN (R1, R2 residue) | ctrl, MAAP and gtest READMEs; PR body Round 4; HANDOFF Round 4; 18 docs gates | R528-4 | `5968967e19411428b71dde5c4712d4a8fa528cfb` |

## Real limits

- **Source review only.** This is source review of the exact head, not of the current-dev
  candidate merge. Physical calibration was NOT RUN. Field skips and host-model timing are not
  hardware or target proof.
- **Linked-image toolchain.** The linked image uses the bare-metal GCC 15.2.0 / newlib toolchain,
  because the pinned SDK is a hosted glibc toolchain. The object-level checks use the pinned SDK.
  The image is sizing scaffolding with a reviewer entry and linker script: not board startup, not a
  shipping image, not a call-chain stack bound, not routed resource evidence.
- **Not reproduced.** The author's measurement helper and 15x16 capacity fixture are not in the
  public archive, so I did not reproduce them. My script is the public reproduction, and the size is
  shape-independent by construction (see item 4).
- **Not run.**
  - The `lwsrp` arm (no lwSRP checkout; F2 does not touch it).
  - The full builder, parent, PP, gPTP and Yosys banks (not allowed).
  - Docker/act.
  - The CI tool installs.
- **Hosted evidence, inspected only (read-only).** `receipts/hosted_check_runs.tsv` is a point-in-time
  snapshot:
  - `firmware-unit`, `rtl-fast`, `docs-check`, `elaborate` and `yosys-elaboration` succeeded.
  - Verilator shards 1, 2 and 4 were in progress.
  - "Physical gPTP" was skipped.
  - I did not determine which hosted aggregates took a no-op path.
- **Resources.** Peak memory of this review's service was 8.0 GiB, under the 12 GiB cap. The clone's
  shared object store reports one unrelated commit-graph entry under `fsck`. The head tree, blobs,
  index and gitlinks verify (`receipts/restore_integrity.log`).

## Pending manager duties

- Carry R528-4-R1 and R528-4-R2 to the residue checklist.
- Publish the author's linked-size helper and capacity fixture, which the PR body says "the packet
  includes". The archived `author-r4/` holds only HANDOFF.md and PR-BODY.md. Otherwise, adjust that
  PR-body sentence, or point to this report's `scripts/link_image.py`.
- Obtain the external round-4 verdict, which together with this one makes the two positive reviews.
- Own hosted and act acceptance at the exact head, including the Verilator shards in progress.
- Build and validate the final current-dev candidate. Source base `021b9c1f`; live dev `d51b373a`;
  re-check if dev moves.
- After explicit maintainer merge authorization, do post-merge containment and close #665 lane F2
  per section 7.

## Receipts

All listed in `MANIFEST.sha256`. Paths are relative to this packet.

- **Scripts:**
  - `scripts/gate.sh`
  - `scripts/catalog_union.py`
  - `scripts/link_image.py`
  - `scripts/rv32_debug.py`
  - `scripts/probe.py`
  - `scripts/selector_probe.sh`
- **Gate receipts:**
  - `receipts/head/*.log|rc`
  - `receipts/docs/*.log|rc`
- **Probe receipts:** `receipts/probes/*.json|log`
- **Image receipts:** `receipts/image/*.json|txt`
- **Other receipts:**
  - `receipts/catalog_union.json`
  - `receipts/rv32_debug.json`
  - `receipts/selector_probe.log`
  - `receipts/hosted_check_runs.tsv`
  - `receipts/restore_integrity.log`

R528-4 FINISHED
