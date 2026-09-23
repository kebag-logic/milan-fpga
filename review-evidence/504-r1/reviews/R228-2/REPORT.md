[R228] NEGATIVE - exact head 5081a25a451b4ac1c00f286ec59ab041c22fdde9

External independent review, round R228-2, issue #504 / PR #521 (correction round for R228-1).
Head `5081a25a451b4ac1c00f286ec59ab041c22fdde9`, tree `68a0628be2b55c1180a0e5751d2355cb8f987268`, source base `483a133ed08867ea0d300d2b4a027b5b48a4282f`.
Paths use `$REVIEW_OUT` for this round's output directory and `$CLONE` for the isolated review clone.

## Verdict summary

The three R228-1 findings are resolved at their root:

- **R228-F1 (MAJOR)**: RESOLVED. FP, AMO and SC stores are classified and judged at every word they write. Unknown memory-writing mnemonics fail closed.
  - Six compiled FP and atomic plants of my own are refused on the resolver at this head.
  - Two of them pass the complete gate at the source base, so the controls are sensitive to the defect.
- **R228-F2 (MAJOR)**: RESOLVED. Four download-path weakenings of my own are each killed by the new control.
- **R228-F3 (MINOR)**: RESOLVED. Every binding R228-1 named is now failure-sensitive.

Two new MINOR findings keep the verdict NEGATIVE:

- **R228-F4 (MINOR, Tests)**: two load-bearing parts of the F1 correction have no failing control.
  - Narrowing the symbol-overlap width from `width` to 4 leaves gate 1b green.
  - With that regression in place, the complete gate then accepts an entity enable written before the AEM verdict. The head refuses the same firmware.
- **R228-F5 (MINOR, Docs)**: the corrected firmware page claims coverage that my compiled plants contradict at this head.
  - The contradicting plants: a 64-bit atomic or `memset` call through the paged base, and an FP or integer overwrite through a pointer to a local.
  - The gaps themselves predate this PR (observation O1). What this PR adds is the claim.

Lens result: Conformance, RTL and Robustness are CLEAN. Tests and Docs are UNCLEAN.

## Reconstruction

I read these in order: AGENTS.md, CONTRIBUTING.md, docs/README.md and REQUIREMENTS.md (REQ-VER-03/04). Then the issue #504 body and comments:

- 5771447690: readiness;
- 5771915061: the selection and installation decision;
- 5778746031: assignment and scope limits;
- 5789172582: the correction assignment;
- 5789252310: the author's published F1 route, recorded before any edit;
- 5789563728: the author's handoff.

After that I read the full diff `483a133e..5081a25a` and its four commits, and the author's public correction packet `review-evidence/504-r1/correction-a185` at `f88d663b`. Last, I inspected the exact-head hosted evidence.

My scope reading:

- The installer, both workflows, `ci_events.py`, `check_baremetal_only.py` and `test_firmware_compiler.py` are blob-identical to `3d90958f`.
- The correction changes only these four files:
  - the store classifier and its controls in `sw/builder/test_builder.py`;
  - `scripts/ci_rv32_sdk_selftest.py`;
  - `docs/integration/BAREMETAL_FIRMWARE.md`;
  - `docs/testing/CI_WORKFLOWS.md`.
- The following are all unchanged: the selection, the text refusals, `RESOLVER_STORE_RESIDUAL`, product and RTL sources, and the gitlinks.
- The F1 route (classify by instruction class, keep the census ISA) was published in the author's TAKEN comment before the edit, under the manager's correction assignment. That meets R228-1's request for a public decision.

I read R228-1 only after my own pass over the diff. I have not read any other reviewer's report for this head.

## Prior public findings on this PR

R228-1 (comment 5789107763) is the only prior round with findings. R227-1 was POSITIVE with none.

| ID | Severity | Disposition at 5081a25a | Evidence (mine) |
|---|---|---|---|
| R228-F1 | MAJOR | **RESOLVED** | See "Verification of R228-F1" below |
| R228-F2 | MAJOR | **RESOLVED** | `receipts/installer-mutations.json`: F2-no-digest-in-extract, F2-prefix-digest-compare, F2-digest-after-root-check and F2-digest-moved-after-extraction are each killed by `test_download_path_refuses_unpinned_bytes` |
| R228-F3 | MINOR | **RESOLVED** | same receipt: F3-drop-destination, F3-drop-installer-digest, F3-installer-digest-of-wrong-file, F3-drop-host, F3-drop-release, inventory-ignores-links and identify-no-escape-check are all killed |
| R228-S1 | SUGGESTION | RESOLVED | extract-no-root-check, inventory-accepts-special and verify-accepts-extra-sections are all killed |
| R228-S2 | SUGGESTION | RETAINED | Installer blob-identical to `3d90958f`; relocation still proven only via `sdk-location` and the sysroot |
| R228-S3 | SUGGESTION | RETAINED | Installer blob-identical; still no download retry or total deadline |
| R228-1 out-of-scope atomic observation | - | RESOLVED in this PR | Compiled `amoswap.w` (`.aq`, `.aqrl`), `amoor.w` (plain, `.aqrl`), `amoand.w.aqrl` and `sc.w` (plain, `.rl`), plus literal `amomax.w.aq`, `amominu.w.rl`, `sc.w.aqrl` and a bare-`(a4)` `sc.w`, are all reported at the window word (`receipts/probe-resolver-head.json`) |

**Verification of R228-F1**

- Unit level (`scripts/probe_resolver.py`, `receipts/probe-resolver-head.json`). The resolver is fed 25 C units compiled by the selected SDK at the census flags, plus 19 hand-written store shapes and 3 load shapes. That is 47 cases:
  - 43 stores are caught: at the window word, or as a refused `unclassified`, `unreadable` or `unplaced` store.
  - The 3 load shapes report no store.
  - The one miss is a 64-bit atomic compiled to `call __atomic_exchange_8`. That is a separate root (see F5 and O1).
- End to end: I planted each firmware edit myself at the end of `configure_fabric()`, through a typedef'd paged base, and ran the head's gate 1b with the SDK mapped (`receipts/e2e/`).
  - Refused on `RESOLVER_STORE_PIN`: float overlay (E1), `_Complex float` member (E3b), float `+=` (E4), 8-bit `__atomic_fetch_or` (lr/sc loop, E5) and `__sync_lock_test_and_set` (E6).
  - Refused on `RESOLVER_UNPLACED_PIN`: an FP overwrite of a parked frame word (E7b).
  - E3 and E7, spelled with `*(T)x =`, are refused by the text pointer-store rule first.
- Defect sensitivity (`receipts/e2e-base/`). With the same SDK, E1 and E7b **pass the complete gate at the source base** (GATE 1b PASS, 212 compiles).
- Fix-removal (`receipts/resolver-mutations/`):
  - frame-overlap width fixed at 4 (RM12): killed;
  - `fsw` dropped from the class table, graded in compiler-absent mode (RM13): killed, so the literal controls run on every machine.
- Hosted, at the exact head (`receipts/hosted-exact-head.txt`): both jobs report that the compiled store-class mutants "reached the resolver as fsw, fsd, amoswap.w, amoor.w, sc.w, each refused on the resolved store address".
- The hostile tally includes the new entries: 213/213 locally, 208 plus 5.

## Findings

### R228-F4 MINOR - Tests - two load-bearing parts of the F1 correction have no failing control

**Artifacts**

- `sw/builder/test_builder.py:1566-1567`: a store through a bounded range is reported over `[lo + offset, hi + offset + width - 1]`.
- `sw/builder/test_builder.py:1573`: a store through a symbol invalidates every modelled word its `width`-byte footprint overlaps.
- The existing controls:
  - `:5180-5199`: literal class probes, through a resolved integer base only;
  - `:5241-5259`: stale probes: an fsd over a frame slot, an fsw or sb over a static's FIRST word, and an AMO onto its base.
- The claims these parts implement: `docs/integration/BAREMETAL_FIRMWARE.md:465-473`.
  - "A store is judged at EVERY 32-bit word it writes".
  - "A store also makes every modelled word it overlaps unknown".
  - "Literal-assembly controls for all of this run on every machine".

**Authority**

- AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect" and "Positive, negative, and boundary behavior is covered".
- R228-1 held claimed receipt bindings without a failing control to MINOR (F3). This is the same standard.

**Evidence**

`scripts/mutate_resolver.py` runs the head's gate 1b with the SDK mapped and scoped Verilator 5.050:

- RM8 drops `+ width - 1` from the range branch. Gate 1b stays green: 213/213, 0 NOT RUN, 227 compiles (`receipts/resolver-mutations/RM8-range-store-without-width.log`).
- RM11 fixes the symbol-overlap width at 4. Gate 1b stays green: 213/213 (`RM11-sym-overlap-fixed-4.log`).
- The resolver is called only from gate 1b (`test_baremetal_profile_contract`), so no other builder gate can see either change.

Both parts matter on compiled C. The plants are in `receipts/e2e-mutated/`, each with its diff:

- **E11b.** A static union parks `0x80001000` in its second word. A `double` computed at run time (`r228_half * 2.0`, so no constant holds a window word) is written over the union. An integer member store then goes through the second word.
  - At run time that word is `0x90000600`, which is `MILAN_CSR_BASE + MILAN_ADP_CTRL`. The store sets the entity enable before the AEM verdict.
  - Head: refused on `RESOLVER_UNPLACED_PIN`.
  - Under RM11: **the complete gate 1b passes** (GATE 1b PASS, 0 NOT RUN, 227 compiles).
- **E10b.** A byte-indexed loop stores a `double` through a typedef'd member overlay from a static base `0x8FFFFFF0`. The last store straddles the window's first word.
  - Head: refused on `RESOLVER_STORE_PIN` at `[0x8ffffff0..0x90000002]`.
  - Under RM8: the boot-contract stage accepted the same firmware. The run then stopped at `test_builder.py:9934`, on an unrelated `-Werror` compile of a splice mutant derived from my plant.
  - The word reached is `MILAN_ID`, which is read-only today.
- The first spellings, E10 and E11, carried a window word as an immediate or as a data constant. The immediate census refuses those even under RM8 and RM11, which is why the `b` variants avoid such constants.

**Impact**

- The head behaves correctly, and my own E10b and E11b refusals show it.
- A one-token regression of the symbol-overlap width would reopen an F1-class bypass: an ADP_CTRL enable before the AEM verdict that passes the complete compiler-backed gate. Nothing in the builder would notice.
- The range-width regression reopens a rule-1 escape at the window's lower boundary.
- Why this is not MAJOR: the exposure is to a future regression only. The class tables, the integer-base footprint, the frame overlap and the unclassified default are all controlled.

**Required outcome**

Add controls that fail when either term regresses:

- a multi-word store over a static whose parked word is not the first word;
- a bounded-range store whose footprint reaches the window when its first byte does not.

Literal assembly suffices, as it does for the existing probes.

**Verification**

- RM8 and RM11 (`scripts/mutate_resolver.py`) turn gate 1b red.
- E10b and E11b stay refused at the corrected head (`scripts/run_planted_on.sh`).

### R228-F5 MINOR - Docs - the corrected firmware page claims coverage that compiled plants contradict

**Artifacts**

- `docs/integration/BAREMETAL_FIRMWARE.md:1213`: the instrument table that #408/#409 read before retiring a text rule. Its "What it sees that the text rule cannot" cell says the store census sees "a float, double or atomic store through a paged base".
- `docs/integration/BAREMETAL_FIRMWARE.md:470-472`: "A store also makes every modelled word it overlaps unknown, so an FP, byte or AMO overwrite of a parked address leaves nothing stale for a later store to be placed by."
- `docs/integration/BAREMETAL_FIRMWARE.md:481-490`: "The boundary of that classification" names raw encodings, numeric local labels and the census ISA, and nothing else.

**Authority**

- AGENTS.md section 6, Docs: "Changed contracts are reflected in authoritative docs".
- docs/README.md: executable tests outrank summaries.

**Evidence**

All plants run at this head through the complete gate 1b with the SDK mapped. Each one writes ADP_CTRL on the boot path before the AEM verdict, through the same typedef'd paged base as the F1 controls. The logs and diffs are in `receipts/e2e/`.

| Plant | What it does | Why the resolver misses it | Result at head |
|---|---|---|---|
| E8 | `__atomic_exchange_n` on a `volatile uint64_t` | GCC 14.3.0 at `rv32imafd` emits `call __atomic_exchange_8`, which is a call, not a store in this unit | GATE 1b PASS, 0 NOT RUN, 227 compiles |
| E9b | `__builtin_memset(<paged ADP_CTRL>, 1, 64)` | compiles to `call memset` | GATE 1b PASS |
| E12 | integer store through a pointer to a local (`r228_q = (r228_wp)&r228_v`) overwrites a parked `0x80001000` | the store is classed `stack`; the frame slot is not invalidated, and the next store is placed at `0x80001000` | GATE 1b PASS |
| E12f | the same with an `fsw` of a float doubled at run time. This is exactly "an FP overwrite of a parked address" | same as E12 | GATE 1b PASS |

- The text rules run in both modes, so they accept these plants too.
- All four also pass at the source base with the same SDK (`receipts/e2e-base/`), so the gaps are not introduced here (O1).
- The claims at `:470-472`, `:481-490` and `:1213` are new in this PR.

**Impact**

- The retirement table now says the resolver sees atomic stores through a paged base.
- The new paragraph says an FP overwrite of a parked address leaves nothing stale.
- The boundary paragraph reads as complete.
- A reader deciding #408/#409, or reviewing the next change to the resolver, is told that classes are covered which enable the entity before the AEM verdict with every instrument and text rule green.

**Required outcome**

The page states only what is proved:

- AMO and SC instruction classes (RV32A), not "atomic stores";
- stores performed inside a called function are not observed, even when this unit forms the pointer. This covers C-library and libatomic calls, including 64-bit atomics and `memset` or `memcpy` calls;
- overlap invalidation covers frame slots and statics addressed through the same base, not stores through a pointer to a local.

Closing the gaps instead is outside #504 and belongs to O1's Issue.

**Verification**

- Reread `:465-490` and `:1213` against the E8, E9b, E12 and E12f receipts. No statement may claim coverage that one of them contradicts.
- `docs_check.py`, `check_em_dash.py`, `check_doc_style.py` and `gen_toc.py --verify-anchors` stay green.

## Suggestions (optional; they do not affect coverage)

- **R228-S2 (Robustness), retained**:
  - installer relocation is proven only through `share/buildroot/sdk-location` and the sysroot;
  - `relocate-sdk.sh` silently skips text files when `file` is absent.
- **R228-S3 (Robustness), retained**: the download has a 120 s timeout per read, but no retry and no total deadline.
- **R228-S4 (Tests), new**: two defensive branches of the correction have no control. Each mutation leaves gate 1b at 213/213:
  - RM1: the slot-mirror bail-out, `test_builder.py:1312-1315`, is returned to the integer store list;
  - RM5: the fail-closed default, `:778`, recognises only a displaced `N(reg)` operand.

  GCC prints every memory operand in the displaced `N(reg)` form, and the census compiles C. Both are therefore reachable only through asm templates, which the inline-asm set pins. A literal `cbo.zero (a4)` probe would pin RM5, and an FP store between a slot load and its branch would pin RM1.

## Out-of-scope observation O1 (for a new Issue; not attributed to this PR)

- E8, E9b, E12 and E12f each enable the entity before the AEM verdict. Each passes the complete compiler-backed gate 1b:
  - at this head;
  - at the source base `483a133e` with the same SDK;
  - under the text rules, which also grade a compiler-absent runner.
- Two classes of gap, both independent of the compiler choice:
  1. **A window pointer handed to a callee that stores through it.** Examples: libatomic 64-bit atomics, `memset`, `memcpy`.
     - The resolver records the call's arguments but never judges them.
     - E8 may not link in the product, which has no libatomic.
     - `memset` is normally supplied by the bare-metal C library. I did not verify that with a product build.
  2. **A store through a stack-derived pointer does not invalidate the frame-slot model**, so a parked address reads back stale. This holds for integer and FP stores alike.
- These gaps should be tracked and closed before #408/#409 retire any text rule onto the resolver. Possible directions, not prescribed:
  - refuse a call whose argument resolves into the window;
  - on a store through a stack pointer, invalidate every frame slot, or refuse such stores.

## Lens results at 5081a25a

- [R228] PASS Conformance - issue #504 acceptance 1-5 against `receipts/gate1b/`, `receipts/hosted-exact-head.txt` and `receipts/01-sdk-fresh-install.log` - checked against acceptance items 1-5:
  - SDK installed from the verified official archive (102597892 bytes, the pinned SHA256), GCC 14.3.0, target `riscv32-buildroot-linux-gnu`;
  - compiled gate 1b: 213/213 hostile, 17/17 and 4/4 positives, 46/46 RTL variants, 0 NOT RUN, 227 compiles;
  - absent gate 1b: 182/182, exactly one NOT RUN, 0 compiles;
  - both exact-head hosted jobs, checked out at merge `eb3c17ac`: a verified cache hit, adoption of `/home/runner/br-milan-rv32/host/bin/riscv32-linux-gcc`, 166/166 non-RTL compiled and 135/135 absent with explicit NOT RUN;
  - `RESOLVER_STORE_RESIDUAL` unchanged; no text refusal retired; selection unchanged.
- [R228] PASS RTL - `git diff --name-only 483a133e..5081a25a` plus the gitlinks - checked for any product change:
  - no path under `hdl/`, `tb/`, `syn/`, `sw/firmware/`, `sw/litex/`, `configs/` or `constraints/` changes;
  - verilog-axis, protocol-processor, gptp-processor and external are pinned identically at base and head;
  - 46/46 RTL mutation variants elaborated with scoped Verilator 5.050 in both of my pristine runs (`receipts/gate1b/pristine-*.log`).
- [R228] PASS Robustness - `receipts/installer-mutations.json`, `receipts/probe-resolver-head.json`, `receipts/e2e/` and `receipts/hosted-exact-head.txt` - checked the installer and the resolver against their failure cases:
  - 32 installer mutations: 30 killed. The 2 survivors (a truncated `archive_sha256` field and a constant `installer_revision`) are redundant, because `installer_sha256` binds the constants that hold them;
  - resolver edge cases: straddles of the first window word, `fsq` and `fsh`, bare `(reg)` operands, RV64-only, Zabha, Zacas, Zicbom, compressed and vector memory ops, and an unreadable operand;
  - loads are not reported as stores;
  - FP and atomic plants are refused;
  - hosted cache hits verify provenance and bytes before any cached tool runs.
- Tests: UNCLEAN under R228-F4. Otherwise applied to:
  - the 25 installer tests;
  - the literal and compiled store-class controls (RM12 and RM13 killed);
  - `test_firmware_compiler.py --selftest`;
  - `ci_events.py --check` (1555 items) and `--selftest` (1198 arms);
  - `check_baremetal_only.py --check` (0 findings) and `--selftest` (365 arms).
- Docs: UNCLEAN under R228-F5. Otherwise applied to both changed pages. All of these are green:
  - `docs_check.py` (0 findings);
  - `check_doc_paths.py` (824 paths);
  - `check_em_dash.py --base 483a133e` (0 findings, 57 arms);
  - `check_doc_style.py`;
  - `gen_toc.py --verify-anchors`;
  - the `#editing-contract-for-this-firmware` and `#elaboration` anchors exist.

## Reviewer-owned lens ledger

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #504 body, comments 5771447690, 5771915061, 5778746031, 5789172582, 5789252310; acceptance 1-5 against `receipts/gate1b/*`, `receipts/01-sdk-fresh-install.log`, `receipts/hosted-exact-head.txt`; blob identity of installer, workflows, `ci_events.py`, `check_baremetal_only.py`, helper vs `3d90958f`; residual table unchanged | R228-2 | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |
| RTL | CLEAN | Changed-path list `483a133e..5081a25a` (no RTL, firmware, SoC, config or constraint path); four gitlinks identical; 46/46 RTL variants elaborated with scoped Verilator 5.050 (`receipts/gate1b/`); `receipts/final-integrity.txt` | R228-2 | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |
| Robustness | CLEAN | `scripts/ci_rv32_sdk.py` under 32 mutations (`receipts/installer-mutations.json`); resolver under 47 shapes (`receipts/probe-resolver-head.json`); planted E1, E3b, E4, E5, E6, E7b (`receipts/e2e/`); hosted cache-hit verification (`receipts/hosted-exact-head.txt`); O1 recorded as pre-existing, not attributed | R228-2 | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |
| Tests | UNCLEAN (R228-F4) | `scripts/ci_rv32_sdk_selftest.py`; `sw/builder/test_builder.py:5170-5270`, `:11088-11138`, `:11218-11248`, `:12991-13003`, `:13034-13049`; RM1, RM5, RM8, RM11, RM12, RM13 (`receipts/resolver-mutations/`); E10b and E11b at head and under RM8 and RM11 (`receipts/e2e-mutated/`); `receipts/focused/` | R228-2 | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |
| Docs | UNCLEAN (R228-F5) | `docs/integration/BAREMETAL_FIRMWARE.md` diff hunks (`:294`, `:452-490`, `:1199-1311`), `docs/testing/CI_WORKFLOWS.md:1042-1112`; E8, E9b, E12, E12f at head and base; `receipts/focused/r07-doc-gates.log` | R228-2 | 5081a25a451b4ac1c00f286ec59ab041c22fdde9 |

## Focused executions at this head

- **Installer, fresh**: `ci_rv32_sdk.py --archive <verified official archive> --destination $REVIEW_OUT/scratch/sdk/host`. Exit 0 in 13.2 s (`receipts/01-sdk-fresh-install.log`).
  - Realpath `bin/toolchain-wrapper`; sysroot inside the prefix.
  - Installer SHA256 `ffcc5433d97209b00cac5155c61bc464a43a60fec49bce0330d81279e1df7cb4`.
- **Gate 1b, SDK mapped** (`test_firmware_compiler.py --sdk-destination`, scoped Verilator 5.050 first on PATH): exit 0 in 5 min 39 s.
  - 213/213 hostile, 17/17 firmware and 4/4 Makefile positives, 46/46 RTL variants, 0 NOT RUN, 227 compiles.
  - The census ISA is `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0`.
  - The audit mapped only `argv[0]`, and every argument tail was preserved (`receipts/gate1b/compiler-audit-summary.txt`).
- **Gate 1b, absent**: exit 0.
  - 182/182 hostile, the same positives, 46/46 RTL variants, exactly one NOT RUN, 0 compiles.
  - All three cross candidates were hidden.
- **Other focused checks** (`receipts/focused/`), all exit 0:
  - `ci_rv32_sdk_selftest.py`: 25 tests;
  - `test_firmware_compiler.py --selftest`;
  - `ci_events.py --check` and `--selftest`;
  - `check_baremetal_only.py --check` and `--selftest`;
  - the docs gates listed above.
- **Tool identity** (`receipts/00-tool-identity.txt`):
  - archive: 102597892 bytes, SHA256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`;
  - scoped Verilator: 5.050, wrapper SHA256 `905795b9...`, binary SHA256 `fb2cc573...`.

## Evidence index

`MANIFEST.sha256` lists every published file under `$REVIEW_OUT`.

**Scripts**

The scripts take their paths as arguments.

- `scripts/probe_resolver.py`
- `scripts/plant_firmware.py`, with the `run_planted.sh`, `run_planted_base.sh` and `run_planted_on.sh` drivers. The base copy is `483a133e` with the head's installer and helper copied in untracked.
- `scripts/mutate_installer.py`
- `scripts/mutate_resolver.py`. RM13 was applied by hand; its diff is recorded.
- `scripts/verify_integrity.py`
- `scripts/sanitize.py`

**Receipts**

Local paths in the receipts are neutralized to placeholders.

## Real limits

- By instruction, I did not run:
  - the full builder;
  - the parent, protocol-processor, gPTP or Yosys banks;
  - act or Docker;
  - the host `act_ci` or its self-test;
  - hardware.

  Physical calibration was NOT RUN, and the field skips are not hardware proof.
- My compiled runs point only the selector's `argv[0]` at a local prefix, installed from the official archive with `--archive`. That is local compatibility evidence.
  - Hosted adoption and the hosted cache hit come from the exact-head hosted logs of the merge ref.
  - At this head, the hosted install was a cache hit. The fresh hosted download path is byte-identical to `3d90958f`, where the manager published it.
- The base comparisons use the base's own `test_builder.py`, with the head's installer and helper copied in untracked.
- Under RM8, E10b was accepted at the boot-contract stage. That run did not reach a whole-gate verdict (see F4).
- I did not execute the workstation compiler.
- I did not verify:
  - the manager's full source banks for this head, which are still running;
  - the trusted act replica;
  - the complete required-context set.
- The disposable trees under `$REVIEW_OUT/scratch/` are not published: the SDK, probe copies and the base copy. They contain SDK binaries and can be deleted.

## Pending manager duties

- Decide on R228-F4 and R228-F5. Once fixed, re-establish the internal and external reviews at the new head.
- Open an Issue for O1 before #408/#409 rely on the resolver.
- Keep the other duties current at the final head:
  - exact-head hosted required contexts: at this head, all executed jobs succeeded and only the non-required physical gPTP context skipped;
  - the trusted act replica;
  - the manager's full static, builder and native banks.
- Current-dev candidate validation at the merge turn: source base `483a133e`, live dev `776bc77d`. Then containment, and closing #504 as Done.

R228-2 FINISHED
