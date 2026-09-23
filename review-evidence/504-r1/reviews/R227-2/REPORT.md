[R227] NEGATIVE - exact head 5081a25a451b4ac1c00f286ec59ab041c22fdde9

Round R227-2. This is the internal cleared-context review of issue #504 / PR #521.

- Head `5081a25a451b4ac1c00f286ec59ab041c22fdde9`, tree `68a0628be2b55c1180a0e5751d2355cb8f987268`.
- Source base `483a133ed08867ea0d300d2b4a027b5b48a4282f` (live dev merged in). The original PR base is `52711029f374650dc93830d5ea28e81cb5c8f410`.
- Paths: `$CLONE` is the isolated review clone and `$REVIEW_OUT` is this round's output directory. The published receipts are path-neutralized; see Real limits.

## Verdict summary

All three R228-1 findings are resolved at their root at this head:

- F1: FP and atomic stores are now classified, and unknown memory-writing mnemonics fail closed.
- F2: the download-path digest check has failing controls.
- F3: the receipt bindings are failure-sensitive.

Two new MINOR findings remain open. Both come from the correction round's own resolver changes.

- **R227-2-F1 (MINOR; Robustness, Tests, Docs).** The doc sentence the correction adds, "an FP, byte or AMO overwrite of a parked address leaves nothing stale for a later store to be placed by", is false for a byte or half-word overwrite at a frame slot's own offset.
  - A firmware that writes ADP_CTRL bit 0 before the AEM decision through a union byte overwrite passes the entire compiled gate 1b on the adopted SDK.
  - The same plant without the overwrite is refused on the resolver store pin.
- **R227-2-F2 (MINOR; Tests, Docs).** Three resolver behaviour changes in the correction have no control that fails when they are reverted: the ranged-store footprint width, the slot-mirror stop on every store class, and the "cannot say" value of non-swap AMO/SC. Each revert passes the PR's whole compiled gate, yet the doc says literal controls exist "for all of this".

Conformance and RTL are covered clean at this head. Robustness, Tests and Docs are UNCLEAN.

## Reconstruction

Sources, read in the order the contract requires:

1. AGENTS.md and CONTRIBUTING.md.
2. `docs/README.md` and REQUIREMENTS.md (REQ-VER-03/04).
3. The #504 issue body, frozen acceptance items 1-5, and these public decisions:
   - readiness research 5771447690;
   - selection 5771915061;
   - assignment 5778746031;
   - the correction assignment 5789172582;
   - TAKEN 5789252310;
   - REVIEW READY 5789563728.
4. The PR #521 body.
5. `docs/testing/CI_WORKFLOWS.md` and `docs/integration/BAREMETAL_FIRMWARE.md`.
6. The complete `483a133e..5081a25a` diff (10 files) and the history.
7. The author packet `correction-a185/` and the exact-head hosted job logs.

The history is merge `f6a55e4c` followed by two one-line commits. The merge tree `160a7177...` equals `git merge-tree --write-tree 3d90958f 483a133e`, so the merge is clean.

The prior review reports R227-1 and R228-1 were read only after the independent pass, findings and ledger below were settled. No private author material, lane scratchpad or management workspace was read.

## Findings

### R227-2-F1 MINOR - Robustness, Tests, Docs - frame-slot sub-word overwrite breaks the overwrite contract the correction states

**Artifacts**

- `sw/builder/test_builder.py:1501-1508`. The `_rv32_forget_overlap` docstring says "a byte store into a word slot ... leaves no whole word this lattice may still read back".
- `sw/builder/test_builder.py:1579-1581`. The frame-slot branch calls that function, then immediately writes `state.mem[(base, offset)] = value`. That value comes from `_rv32_store_value` (`:1511-1517`), which returns the FULL source register for `sb`/`sh`.
- The static-symbol branch written in the same commit (`:1571-1575`) records `None` for every store except `sw`/`amoswap`. The two branches disagree.
- `sw/builder/test_builder.py:5232-5270`. The stale probes cover an `fsd` over a frame slot, an `fsw` and an `sb` over a static, and an AMO rewriting its base. None covers a frame-slot byte or half-word overwrite, yet the gate note prints "overwrites (FP, byte and AMO) left no stale word for a later store to be placed by".
- `docs/integration/BAREMETAL_FIRMWARE.md:470-473`: "A store also makes every modelled word it overlaps unknown, so an FP, byte or AMO overwrite of a parked address leaves nothing stale for a later store to be placed by."

**Authority**

- AGENTS.md section 6:
  - Robustness: malformed input, boundary input and minimum/maximum values;
  - Tests: "Tests do not merely reproduce implementation assumptions";
  - Docs: "Changed contracts are reflected in authoritative docs".
- AGENTS.md section 8: "Never hide a material assumption ... in code".
- The author's REVIEW READY and handoff disclose that the "pre-existing sub-word frame-slot value imprecision remains". The authoritative page states the opposite.

**Evidence**

- `receipts/subword-asm-probe.txt`. The census flags with the adopted GCC 14.3.0 emit this sequence:
  - `sw a5,-20(s0)` stores the address 0x90000600;
  - `sb zero,-20(s0)` overwrites the slot;
  - `lw a5,-20(s0)` reloads it;
  - `sw a5,0(a4)` stores through it.
  The head resolver reports that last store at `0x0`. The real target is 0x90000600, ADP_CTRL, because the byte write keeps the low byte 0x00.
- `receipts/plant-byte-overwrite.{diff,log,verdict}`, run with `scripts/firmware_plant.sh`:
  - The plant is `union { uint32_t w; uint8_t b; }`. It sets `w = (page << 16) | MILAN_ADP_CTRL`, sets `b = 0`, then writes `((blk)w)->ctrl = 1u`.
  - It sits at the end of `configure_fabric()`, before the AEM decision.
  - The whole compiled gate 1b passes: `GATE 1b PASS; 0 NOT RUN`, 213/213 mutations, 17/17 firmware edits, 67 stores classified.
  - `plant-half-overwrite` (a `uint16_t` member) also passes.
  - `plant-no-overwrite` is the same union without the overwrite. It is refused: "STORES into the Milan CSR window ... at 0x90000600". The plant therefore reaches the resolver, and only the sub-word overwrite hides it.
- `receipts/resolver-controls-{head,3d90,base}.txt`, run with `scripts/resolver_controls.py`. `X-subword-slot-store` fails identically at this head, at `3d90958f` and at `483a133e`. The value behaviour predates the lane; the claim that it is closed is new.
- A second counterexample to the same doc sentence exists at resolver level. A full-word store through a stack-class pointer to the same frame slot leaves the slot's old value (`X-stack-alias-overwrites-slot`). Its whole-gate spelling, `*p = ...`, is refused only by the retained text pointer-store rule (`receipts/plant-pointer-alias.log`), which #408/#409 may retire.

**Impact**

- The authoritative firmware contract now says byte overwrites leave nothing stale. On the hosted configuration, a firmware that advertises the entity before AEM verification through a union byte or half-word overwrite passes every instrument and every text rule.
- This is not a regression against dev: dev's hosted runs ran no resolver, and the value model predates the lane.
- The claim is false, though, and it is exactly the claim #408/#409 would retire text rules against.

**Required outcome.** One of the following, with the route recorded publicly:

1. The frame-slot model is made to satisfy the stated contract:
   - a narrow or non-integer store leaves the overlapped slot unknown, as the symbol branch already does;
   - a store through a stack-class base forgets the frame slots it may alias;
   - controls fail when either is reverted.
2. The doc sentence, the `_rv32_forget_overlap` docstring and the gate note are narrowed to what is actually modelled. The sub-word and alias imprecision is named as an open limitation and tracked in a public Issue that #408/#409 depend on.

**Verification**

- Route 1: `firmware_plant.sh byte-overwrite half-overwrite` must report REFUSED on a resolver reason, and `resolver_controls.py` X-subword-slot-store and X-stack-alias must pass.
- Route 2: the three texts no longer claim the case, and the Issue link is present.

### R227-2-F2 MINOR - Tests, Docs - three correction-round resolver changes have no failing control

**Artifacts**

- `sw/builder/test_builder.py:1566-1567`: a ranged store covers `hi + offset + width - 1`.
- `sw/builder/test_builder.py:1312-1315`: the slot-mirror walk stops at every store class and at every memory-writing non-load.
- `sw/builder/test_builder.py:1516`: only integer stores and `amoswap` carry a value. Every other AMO, and SC, writes "cannot say".
- The controls at `:5179-5270` and the compiled store-class entries at `:11085-11250`.
- `docs/integration/BAREMETAL_FIRMWARE.md:465-473`: "Literal-assembly controls for all of this run on every machine".

**Authority**

- AGENTS.md section 5: "add or update self-checking tests for changed behavior".
- AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
- The REVIEW READY cites "8/8 fix-removal mutants are KILLED". Those eight exercise none of these three changes.

**Evidence**

- `receipts/gate-R5-*`, `gate-R6-*` and `gate-R10-*`, run with `scripts/resolver_gate_mutants.sh`. Each mutant reverts one change in a disposable clone. The PR's own compiled gate 1b then passes (exit 0, 213/213).
- In the same harness:
  - the R0 setup control (no edit) passes;
  - R1 (FP classes dropped) and R3 (the class default dropped) are killed by the PR's literal controls. The harness therefore detects reverts elsewhere.
- The reviewer's literal controls detect all three (`receipts/resolver-controls-mutant-R5/R6/R10-*.txt`):
  - F1-range-footprint, 4 probes;
  - F1-mirror-stopped, 3 probes;
  - F1-amo-slot-forgotten, 3 probes.
  The mutants are therefore not equivalent.

**Impact.** Any of these could be silently reverted by a later edit while the gate stays green and the doc says controls exist:

- judging a ranged store by its tail bytes, so that a bounded loop store whose last bytes enter the window is accepted again;
- refusing to invent a branch-refined range for a slot that an FP store or an AMO overwrote;
- modelling a non-swap AMO or an SC as writing `rs2`.

**Required outcome.** Each of the three behaviours has a shipped control that fails when it is reverted (literal-assembly controls suffice), or the doc stops claiming controls for it.

**Verification.** `resolver_gate_mutants.sh R0-pristine R5-range-footprint-width R6-mirror-integer-stores-only R10-amo-value-rs2` at the fixed head. R0 must survive, and each of the other three must be KILLED by its new control's reason.

### R227-2-S1 SUGGESTION - Docs - name both unbound LR/SC edges

`docs/integration/BAREMETAL_FIRMWARE.md:484-487` says GCC's retry loop leaves "the loop's back edge" unmodelled. The forward exit `bne ...,1f`, which skips the SC, is unbound too: GCC 14 emits `1:` on its own line, and `rv32_blocks` binds only named labels.

Soundness is unaffected. The SC-path state is a lower bound of the skip-path state, so dropping that edge equals the meet. Naming both edges would make the boundary statement exact. This suggestion does not affect coverage.

## Prior public review findings on this PR

| Prior finding | Disposition at this head | Evidence |
|---|---|---|
| R228-F1 MAJOR (Conformance, Robustness, Tests, Docs): FP stores bypass the resolver | **RESOLVED at the root**, detailed below the table | `receipts/resolver-controls-*.txt`, `gate-R1-*`, `gate-R3-*`, `gate1b-compiled.log`, `hosted-exact-head-summary.txt` |
| R228-F2 MAJOR (Tests, Conformance): the download digest check had no failing control | **RESOLVED**. My mutants I01-I06 (delete, 8-hex prefix, warn-only, trust the downloaded digest, check after the root listing, check after tar) are each killed by `test_download_path_refuses_unpinned_bytes`. I07 (dropped timeout) is killed by the positive `test_download_path` | `receipts/installer-mutants.txt` |
| R228-F3 MINOR (Tests): receipt bindings | **RESOLVED**. Each of these is killed: I09-I12 (provenance installer digest, host, destination), I13 (symlinks dropped from the inventory) and I16 (realpath containment) | `receipts/installer-mutants.txt` |
| R228-S1 SUGGESTION | Taken. I15 (special file), I22 (extra receipt section) and I27 (archive root) are killed | same |
| R228-S2, R228-S3 SUGGESTION | Not taken, because they would change installer behaviour. They remain optional and do not affect coverage | author TAKEN 5789252310 |
| R228 out-of-scope note: atomic stores unreported | Closed in this PR. AMO and SC are classified and judged | `resolver-controls-head.txt` (all `F1-amo*`/`F1-sc*` probes pass) |
| R227-1 (POSITIVE at `3d90958f`, no findings) | Nothing to retain. Its coverage belongs to `3d90958f` and is superseded: later commits changed artifacts in the Conformance, Robustness, Tests and Docs scopes | - |

R228-F1 resolution in detail:

- Stores are classified by class in `test_builder.py:759-789` and `:1521-1588`, with the fail-closed default at `:1632-1640`.
- The reviewer controls pass 92/92 at this head. They pass only 6/92 at `3d90958f` and at `483a133e`.
- The PR's own gate kills R1 (FP classes dropped) and R3 (default dropped).
- In my compiled run (213/213), the float, double, exchange, fetch-or and compare-exchange paged-base mutants are refused on the store pin.
- Both exact-head hosted jobs log "compiled store-class mutants reached the resolver as fsw, fsd, amoswap.w, amoor.w, sc.w, each refused on the resolved store address".
- The census ISA is stated in `CI_WORKFLOWS.md:1049-1053` and `BAREMETAL_FIRMWARE.md:452-457` and `:1306`.
- R228-1 asked for a published route decision. The correction assignment (5789172582) directed the fix, and TAKEN (5789252310) published the classification route before the first edit. That route changes no selection, residual, text refusal, product option, RTL or firmware; it only adds refusals. R227-2-F1 and R227-2-F2 are new, adjacent defects of the correction, not R228-F1 retained.

## Per-lens results

[R227] PASS Conformance - `scripts/ci_rv32_sdk.py:24-30`, `.github/workflows/docs.yml:172-190`, `.github/workflows/elaborate.yml:242-260`, `sw/builder/test_builder.py:4094-4104`, `receipts/gate1b-{compiled,absent}.log`, `receipts/audit-*.txt`, `receipts/hosted-exact-head-summary.txt` - checked against #504 items 1-5 and decisions 5771915061, 5778746031 and 5789172582. The findings are:

- The Bootlin stable 2025.08-1 riscv32-ilp32d glibc archive, URL and full digest are pinned. The digest check precedes `tarfile`, `tar` and `relocate-sdk.sh`.
- Both builder calls require `--require-rv32`, and adoption of the absolute selector is asserted.
- Item 2 (compiled, locally): 213/213 hostile, 17/17 firmware and 4/4 Makefile positives, 46/46 RTL variants, 0 NOT RUN, 227 compiles. Every argument tail is preserved, and all 116 census assemblies are `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0`.
- Item 3 (absent): 182/182, 17/17, 4/4, 46/46, exactly one NOT RUN, zero compiles, all cross candidates hidden.
- Item 5: the residual is unchanged (`__errno_location` x1).
- Hosted jobs, observed and not adjudicated:
  - at `3d90958f`, both jobs freshly downloaded and verified the archive with identical installer bytes and cache key;
  - at this head, both jobs got verified cache hits and adopted `/home/runner/br-milan-rv32/host/bin/riscv32-linux-gcc`.
- No text refusal was retired.

[R227] PASS RTL - `git diff --stat 483a133e..5081a25a` (10 files), `receipts/final-integrity.txt`, `receipts/gate1b-{compiled,absent}.log`, `docs/integration/BAREMETAL_FIRMWARE.md:41,488-490`, `sw/litex/milan_sim.py:5`. The findings are:

- No path under `hdl/`, `tb/`, `syn/`, `sw/firmware/`, `sw/litex/` or `configs/` changes.
- The verilog-axis `48ff7a7e`, protocol-processor `424c688f` and gptp-processor `c1b61743` gitlinks are unchanged, and their 539 files match the committed bytes and modes.
- The 46 RTL mutation variants elaborate as the real top with scoped Verilator 5.050 in both compiler modes.
- The census ISA, `rv32imafd`/ILP32D, is correctly documented as distinct from the shipping RV32I hart.

Robustness - UNCLEAN (R227-2-F1). The following were applied and found sound:

- Installer: 31 installer mutants, 30 killed. The survivor, I31, drops a redundant post-install re-verify and is equivalent.
- Real SDK: fresh install in 13.3 s, cache hit in 0.76 s, and verify-only all pass.
- Resolver:
  - every class, width, misaligned and boundary probe (92/92);
  - the unclassified default for `c.fsw`, `c.fsd`, `c.sw`, `sd`, `cbo.zero`, `vse32.v`, `vsse32.v`, `amocas.w`, `amoswap.b`, `amoadd.h`, `ssamoswap.w` and `prefetch.w`;
  - unreadable operands, rd clearing, FP, static-symbol and AMO overlap invalidation, and a store that ends exactly below the window is not a hit;
  - the GCC 14 LR/SC template shape.

Tests - UNCLEAN (R227-2-F1, R227-2-F2). The following were applied and found sound:

- The 25-test installer self-test.
- `test_firmware_compiler.py --selftest`.
- The PR's literal and compiled store-class controls kill R1 and R3.
- `ci_events.py --check`/`--selftest` and `check_baremetal_only.py --check`/`--selftest` exit 0.

Docs - UNCLEAN (R227-2-F1, R227-2-F2). These gates exit 0:

- `docs_check.py`;
- `check_em_dash.py` against both `483a133e` and `52711029`;
- `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --check`/`--verify-anchors` and `check_hygiene.py --check`.

The documentation otherwise matches the implementation: the selection, the cache trust boundary, the absent path and the retirement boundary with #408/#409.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #504 body, acceptance 1-5 and decisions 5771915061, 5778746031, 5789172582, 5789252310. Installer pin constants and order. Both workflow diffs. `--require-rv32` adoption (`test_builder.py:4094-4104`). Local compiled and absent gate 1b and both audits. Exact-head hosted docs-check and elaborate logs (read-only) | R227-2 | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |
| RTL | CLEAN | Base-to-head diff boundary. Byte-level integrity of 854 parent and 539 submodule files and all 3 gitlinks. 46/46 RTL variants elaborated with scoped Verilator 5.050 in both modes. Census-ISA and shipping-ISA statements | R227-2 | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |
| Robustness | UNCLEAN (R227-2-F1 open) | `ci_rv32_sdk.py` (31 mutants). Real SDK fresh/hit/verify. Resolver (`test_builder.py:733-1733`) under 92 literal probes plus 3 pre-existing-behaviour probes. 6 whole-gate firmware plants | none at this head (R227-2 applied) | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |
| Tests | UNCLEAN (R227-2-F1, R227-2-F2 open) | `ci_rv32_sdk_selftest.py` against 31 mutants. `test_firmware_compiler.py --selftest`. PR store-class controls against 5 whole-gate resolver mutants plus the R0 control. `ci_events` and `check_baremetal_only` check/selftest | none at this head (R227-2 applied) | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |
| Docs | UNCLEAN (R227-2-F1, R227-2-F2 open) | Full diff of `BAREMETAL_FIRMWARE.md` and `CI_WORKFLOWS.md` against the implementation. `test_builder.py` comments and notes. Docs, em-dash, style, paths, TOC and hygiene gates. PR body | none at this head (R227-2 applied) | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |

No finding was deferred, downgraded or moved to another Issue. A later commit that touches an artifact in a lens's scope un-covers that lens (AGENTS.md section 7).

## Independent executions at this head

| Execution | Result | Receipt |
|---|---|---|
| Archive identity | 102,597,892 bytes. SHA256 `d42680e9...78f` matches the installer constant and decision 5771915061 | `tool-identity.txt` |
| Fresh install, cache hit, verify-only (verified archive, fresh `$REVIEW_OUT/scratch` prefix) | exit 0, 13.3 s / 0.76 s. GCC 14.3.0, target `riscv32-buildroot-linux-gnu`, realpath `bin/toolchain-wrapper`, relocated sysroot. Installer SHA256 `ffcc5433...cb4` | `sdk-*.log` |
| `ci_rv32_sdk_selftest.py` | 25 tests OK | `ci_rv32_sdk_selftest.log` |
| `test_firmware_compiler.py --selftest` | PASS | `test_firmware_compiler-selftest.log` |
| Gate 1b, mapped SDK, scoped Verilator 5.050 | exit 0 in 5m34s: 213/213, 17/17, 4/4, 46/46, 0 NOT RUN, 227 compiles | `gate1b-compiled.log`, `audit-compiled.txt` |
| Gate 1b, absent | exit 0 in 4m38s: 182/182, 17/17, 4/4, 46/46, 1 NOT RUN, 0 compiles | `gate1b-absent.log`, `audit-absent.txt` |
| Reviewer resolver controls | head F1 92/92; `3d90958f` 6/92; `483a133e` 6/92. X 0/3 at all three | `resolver-controls-*.txt` |
| Installer mutants | 30/31 killed (I31 equivalent); pristine exit 0 | `installer-mutants.txt` |
| Whole-gate resolver mutants | R1 and R3 KILLED. R5, R6 and R10 SURVIVED. R0 setup control passes | `probe-verdicts-summary.txt`, `gate-R*` |
| Whole-gate firmware plants | byte-overwrite and half-overwrite PASSED the gate. no-overwrite and memcpy-alias refused by the resolver. pointer-alias refused by the text pointer-store rule. call-escape refused by the compiled immediate census | `probe-verdicts-summary.txt`, `plant-*` |
| Focused static gates (17 commands) | all exit 0 | `static/SUMMARY.txt` |
| Final integrity | PASS. HEAD and tree as reviewed, index equals HEAD with no hidden flags, 854 + 539 files byte/mode-exact, status empty (ignored included), 3 gitlinks at their pins | `final-integrity.txt` |

## Out-of-scope observation (pre-existing; not attributed to this PR)

- OBS-1: a sub-word load from a frame slot reads the slot's whole modelled word (`test_builder.py:1483-1484`, used for `lb`/`lh`/`lbu`/`lhu`).
  - `X-subword-slot-load` fails identically at this head, at `3d90958f` and at `483a133e`.
  - No new text claims it is handled, so it is not a finding here.
  - It belongs in the public Issue suggested under R227-2-F1 route 2, before #408/#409 retire text rules onto the resolver.

## Real limits

**Not run, by instruction.** These were not run:

- the full parent, PP, gPTP, Yosys and builder banks;
- Docker/act, and host `act_ci` or its self-test;
- hardware.

Physical calibration remains NOT RUN, and field skips are not hardware proof. The manager's banks for this head are neither claimed nor inferred.

**Local mapping.**

- The mapped-SDK run substitutes only the selector's `argv[0]`. It is local compatibility evidence, not hosted adoption.
- Hosted adoption, fresh acquisition (observed at `3d90958f` only) and the exact-head cache hits are recorded from read-only job logs. The manager owns hosted and act acceptance.

**Probe clones.**

- Mutants and plants ran in disposable `git clone --shared` copies under `$REVIEW_OUT/scratch`, with the three submodules initialised from the review clone's local module repositories.
- The review clone ran only the two pristine gates and the static gates. Those wrote only ignored `__pycache__` directories, which were removed before the final integrity check.
- R1 and R3 ran in a first batch whose clones lacked submodule git metadata. Both failed at the PR's literal store-class control, which runs before any submodule-dependent stage.
- The first batch's R5, R6 and R10 results were infrastructure failures and were discarded. Only the rerun is reported.

**Scope of the pre-existing claim.** The pre-existing status of the R227-2-F1 value behaviour is shown at resolver level, at base and at `3d90958f`. The whole-gate plant ran at this head only.

**Receipts.**

- Published receipts substitute `$CLONE`, `$REVIEW_OUT`, `$HOME`, `$ARCHIVE_DIR` and `$PINNED_TOOL_BIN` for local paths. Unmodified copies stay in the unpublished `scratch/raw-receipts/`.
- `scratch/` is never published. The SDK prefix and probe trees were deleted after measurement.

**Other reviewers' scripts.** The R228-1 scripts were not executed. Independent equivalents were used.

## Pending manager duties

- Record the route for R227-2-F1 (model fix, or narrowed claims plus an Issue) and correct R227-2-F2. Then re-review the corrected head (internal and external) and re-bank every lens that the change touches.
- At the corrected head: the full source static, builder and native banks; the trusted act replica; and acceptance of the exact-head hosted required contexts. All seven were observed as success at the capture in `hosted-exact-head-summary.txt`, but that is not adjudicated here.
- Validate the current-dev candidate at the merge turn (source base `483a133e`, live dev `776bc77d`), then the authorized merge, containment, post-merge hosted results and Closed/Done.
- Optionally, file the Issue for OBS-1 and the frame-slot alias behaviour before #408/#409 proceed.
- Publish only REPORT.md and the MANIFEST-listed files.

R227-2 FINISHED
