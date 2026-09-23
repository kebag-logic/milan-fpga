[R228] NEGATIVE - exact head 97aa1ec943ac740a27b942210a248f6512ae3ff6

External independent review, round R228-3, issue #504 / PR #521 (second correction round).
Head `97aa1ec943ac740a27b942210a248f6512ae3ff6`, tree `4a12a545bdb478083d711a8f319d3c6d70c1b1d9`.
Source base and live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2`. Reviewed from public state and a detached clone only.

## Verdict summary

- One open finding: **R228-F6 MINOR (Tests)**. The overlap test that forgets a modelled word has a boundary for a byte store into the word's last byte. No control covers that boundary. Reverting it (`>=` to `>`) leaves both the literal controls and the complete compiler-backed gate 1b green, at 217/217. Under that one-token revert, a compiled union write of 0x90 into byte 3 turns a parked 0x80000600 into ADP_CTRL, and the whole boot contract accepts it. At this head the same write is correctly refused. This is the R227-2-F2 / R228-F4 standard, so it is MINOR, and the verdict is NEGATIVE.
- All four findings under re-review are resolved at their root: R227-2-F1, R227-2-F2, R228-F4 and R228-F5. So are the first round's R228-F1, F2 and F3, re-verified at this head with my own controls. 31 of my 35 fix-removal mutants are KILLED. The 4 survivors are F6, its unreachable twin (S8) and the census-ISA filter (S5).
- Clean lenses at this head: Conformance, RTL, Robustness and Docs. The only unclean lens is Tests.
- The head behaves correctly on everything I measured:
  - 50/50 in-contract literal resolver probes are sound (16/50 at the base).
  - Every compiled plant the page says is refused is refused.
  - The shapes the page lists as not observed behave as it says.

## Reconstruction

- **Authority.** AGENTS.md sections 2-8, CONTRIBUTING.md sections 2-3, docs/README.md, and REQUIREMENTS.md REQ-VER-03/04.
- **Issue #504.** The issue body (acceptance items 1-5, scope, and "No text refusal is retired") and the manager decisions 5771447690, 5771915061 and 5778746031. Also the correction assignments 5789172582 and 5790944031, and the author's public scope statements (A185 TAKEN 5789252310, A191 TAKEN 5791069118).
- **Scope change on record.** The resolver's store-class classification adds refusals only. It was published as a material decision before implementation, in A185 TAKEN, and was accepted through two review rounds. It changes no text refusal, residual, product, firmware, RTL or pin.
- **Diff and history.** `git diff 574c29fa..97aa1ec9` covers 10 files, +1660/-67. I checked the history directly:
  - Merge `4914eea5` has tree `fdf07c85…`. This equals `git merge-tree --write-tree 5081a25a 574c29fa` (exit 0).
  - Since `5081a25a`, the non-merge changes touch only `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md` and `docs/testing/CI_WORKFLOWS.md`.
  - `scripts/ci_rv32_sdk.py` and both workflows are byte-identical to `3d90958f`, so the cache key is unchanged since the round that exercised fresh hosted acquisition.
- **Evidence read.** The published author packet `correction-a191/` at `3c9b4990`, the manager's evidence comments, and read-only exact-head check runs and job logs.
- **Prior findings.** I read the R228-1, R227-2 and R228-2 reports only after my own pass over the diff and my own probes.

## Findings

### R228-F6 MINOR - Tests - the overlap boundary for a byte store at a modelled word's last byte has no failing control

**Artifacts**

- `sw/builder/test_builder.py:1501-1509`: `_rv32_forget_overlap()`. The term that decides a store at a word's LAST byte is `key[-1] + 3 >= start`, at `:1508`.
- It is called from the static branch at `:1577` and from the frame branch at `:1588`.
- The existing controls:
  - the stale probes at `:5272-5308`: a byte store at a slot's own offset, at a static's own offset, and at a static's byte 1;
  - the kept probes at `:5313-5320`;
  - the compiled slot-rewrite mutants at `:11293-11325`: byte 0 and half-word 0 through a union.
- None of them writes byte +3 of a modelled word, so none reaches that boundary.

**Authority**

- AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect" and "Positive, negative, and boundary behavior is covered".
- The R227-2-F1 required outcome: "controls fail when either is reverted".
- The same standard as R227-2-F2 and R228-F4, both MINOR.

**Evidence**

- **Mutant `overlap-last-byte`** (`scripts/r228_mutate.py`) changes `>=` to `>`. It SURVIVES:
  - the literal controls (`receipts/mutations/overlap-last-byte.json`);
  - the complete gate 1b with the SDK mapped and scoped Verilator 5.050: exit 0, 217/217, 0 NOT RUN (`receipts/mutations/overlap-last-byte-gate1b.json` and `.log`).
- **Compiled plants** (`scripts/r228_gate_probes.py` via `r228_gate_run.py`). Each is spliced at the end of `configure_fabric()` before the AEM verdict and judged by the gate's own `assert_boot_contract()`. Each parks `0x80000600`, outside the window, then writes `0x90` into byte 3 through a union and stores through the word. At run time the word is `0x90000600`, which is ADP_CTRL.

  | Plant | Head | Head with the mutant | Base `574c29fa` |
  |---|---|---|---|
  | frame union | REFUSED on `RESOLVER_UNPLACED_PIN` | ACCEPTED | ACCEPTED |
  | static union | REFUSED on `RESOLVER_UNPLACED_PIN` | ACCEPTED | ACCEPTED |

  Receipts: `receipts/gate-probes/head.json`, `head-overlap-last-byte.json` and `base-574c29fa.json`.
- **Literal probes.** "frame: sb at the slot's LAST byte (+3)" and "static: sb at byte 3" are sound at the head (`receipts/resolver-probes-head.json`).

**Impact**

- The head is correct. The byte-3 shape is the R227-2-F1 bypass in its most natural spelling: rewriting the page byte of a parked little-endian address.
- A one-token regression reopens that bypass, and nothing in the builder notices. The page (`BAREMETAL_FIRMWARE.md:494`) presents the literal controls as covering these rewrites.
- It is not MAJOR, because the exposure is to a future regression only.

**Required outcome**

- Add a control that fails under the `>=` to `>` revert, for example:
  - a byte store at byte +3 of a modelled frame slot, then at byte +3 of a static word;
  - each followed by a reload and a store, which must come back unplaced.
- Literal assembly suffices.

**Verification**

- `r228_mutate.py … overlap-last-byte` and `… overlap-last-byte-gate1b` report KILLED.
- The two byte-3 plants stay REFUSED at the corrected head.

## Suggestions (optional; they do not affect coverage)

- **R228-S5 (Tests): the census-ISA filter.** Nothing fails if the census-ISA parse at `test_builder.py:11327-11328` regresses.
  - Mutant `census-isa-parse` SURVIVES with `--require-rv32` semantics on the selected SDK: GATE 1b PASS, 1 NOT RUN, 226 compiles (`receipts/mutations/census-isa-parse.log`).
  - Its NOT RUN line contradicts itself: "declares rv32…_a2p1… with no A extension".
  - The three compiled atomic mutants then drop out while hosted jobs stay green. The literal AMO/SC class probes still run, so no bypass reopens.
  - A fix: assert that `a` is in `census_isa` under `--require-rv32`, or make mapped mode refuse any NOT RUN.
- **R228-S6 (Docs): overlap is per frame register.** `BAREMETAL_FIRMWARE.md:482-484` says a frame-register store makes "every other word of that frame" it overlaps unknown. That holds for words keyed through the same register only: an `sp`-keyed store over an `s0`-keyed slot is not invalidated (literal probe in `receipts/resolver-probes-head.json`).
  - The compiled census does not reach this. The pristine census has 176 `sp`-relative stores and none overlaps an `s0` slot (`receipts/gate-probes/pristine-frame-alias-scan.json`).
  - Saying "keyed through the same frame register" would make the sentence exact.
- **R228-S7 (Docs): state consequences in the not-observed list.** In "What the census does NOT observe":
  - The sub-word-load bullet (`:538`) could state its consequence as the call bullet does. My compiled byte-LOAD plant writes ADP_CTRL and passes the complete boot contract at the head and at the base (`receipts/gate-probes/head-2.json`). The shape is pre-existing and already routed to #408/#409 by the page.
  - The memset example could say "a memset or memcpy that GCC emits as a call". A 4-byte `__builtin_memset` onto ADP_CTRL is inlined as four `sb` stores and refused at `0x90000600..603`.
- **R228-S8 (Tests): the companion boundary.** `key[-1] <= start + width - 1` has the same gap (`overlap-first-byte` SURVIVES). Only a misaligned `sh`, `sw` or `fsd` reaches it, and GCC 14.3.0 at the census flags stores packed members byte-wise (checked). It is therefore not load-bearing for compiled C, and a control is optional.
- **R228-S2 and R228-S3 (Robustness), retained unchanged.** These are relocation proof and the download retry/deadline. The author declined them because they change installer behaviour.

## Prior public review findings on this PR, at this head

| Finding | Status at `97aa1ec9` | My evidence |
|---|---|---|
| R228-F1 MAJOR: FP stores bypass the resolver | RESOLVED | Mutants `fp-classes`, `atomic-classes`, `footprint-first-byte`, `stores-first-word` and `unclassified-default` are KILLED. Gate 1b with the SDK mapped reports that the compiled `fsw`, `fsd`, `amoswap.w`, `amoor.w` and `sc.w` mutants were each refused on the resolved address, and the hosted docs-check and elaborate logs at this head say the same. The pages state the census ISA `rv32imafd`/ILP32D and the RV32I product hart; the hart is confirmed in `docs/litex/LITEX_SOC.md:64` |
| R228-F2 MAJOR: download-path digest has no failing control | RESOLVED | `download-digest` and `digest-prefix` are KILLED by `test_download_path_refuses_unpinned_bytes` |
| R228-F3 MINOR: receipt bindings not failure-sensitive | RESOLVED | `provenance-drop-host`, `provenance-drop-destination`, `installer-digest-constant`, `inventory-no-links`, `no-escape-check`, `no-tools-check` and `hit-skips-verify` are all KILLED |
| R228-S1 | TAKEN | `test_archive_root`, `test_special_file` and `test_extra_receipt_section` exist and pass (25 tests) |
| R228-1 out-of-scope atomics | CLOSED here | AMO/SC classified. In the literal probes `amoxor`, `amomaxu.w.aqrl` and `sc.w.aqrl` are sound |
| R227-2-F1 MINOR: frame-slot sub-word overwrite | RESOLVED (route 1) | `value-subword`, `value-all-classes`, `stack-forget-frame` and `frame-overlap` are KILLED. The compiled byte-0 union plant is REFUSED at the head and ACCEPTED at the base. The byte-+3 boundary is **F6** above |
| R227-2-F2 MINOR: three resolver changes uncontrolled | RESOLVED | `range-footprint`, `mirror-integer-only` and `value-amo-sc` are KILLED |
| R227-2-S1 | TAKEN | `BAREMETAL_FIRMWARE.md:513-516` names both unbound LR/SC edges. A compiled sub-word `__atomic_fetch_or` (typedef spelling, LR/SC loop with numeric labels) is REFUSED at `0x90000600` at the head and ACCEPTED at the base |
| R227-2 OBS-1: sub-word frame load | DOCUMENTED, not closed (pre-existing) | `:538`. See S7 and the pending duties |
| R228-F4 MINOR: two F1 terms uncontrolled | RESOLVED | `range-footprint` (RM8) and `sym-overlap-width-4` (RM11) are KILLED, and `frame-overlap-width-4` (RM12) is also KILLED |
| R228-F5 MINOR: page over-claims coverage | RESOLVED | The page names RV32A AMO/SC instruction classes, not atomic stores. It adds "What a store leaves behind" and "What the census does NOT observe". Compiled checks at the head agree: the 64-bit `__atomic_exchange_n` is ACCEPTED, as is a callee writing its caller's local through a member store; the page lists both as not observed. The E12/E12f-class pointer rewrites are refused, as permanent compiled mutants |
| R228-S4 | TAKEN | `mirror-integer-only`, `mirror-no-memop` and `memop-displacement` are KILLED |
| R228-S2, S3 | Not taken; retained as suggestions | The installer is unchanged since `3d90958f` |
| R228-2 O1 | Class 2 in-function half closed; the rest documented | Neither is attributed to this PR. See pending duties |

## Per-lens results

```text
[R228] PASS Conformance - issue #504 acceptance 1-5; test_builder.py:4112-4122; RESOLVER_STORE_RESIDUAL (unchanged); hosted jobs 107106136535/107106136284 - acceptance checked against my runs and exact-head hosted logs: pinned SDK adopted at the absolute selector with driver=(); census ISA stated; compiled 217/217 local (hosted 170/170 non-RTL, no Verilator/MAKEFLAGS arm there); absent 182/182, explicit NOT RUN, 0 compiles (hosted 135/135, 3 NOT RUN); --require-rv32 absent refusal exit 1 with the named message; residual still only __errno_location; no text refusal retired; no firmware/RTL/pin change; store-class scope change publicly recorded before implementation.
[R228] PASS RTL - git diff 574c29fa..97aa1ec9 -- hdl tb syn sw/firmware sw/litex configs and the four gitlinks - empty diff, gitlinks identical at base and head; 46/46 RTL mutation variants elaborated as the real option-on top with scoped Verilator 5.050 in both the mapped and absent gate 1b runs (receipts/gate1b-sdk.log, gate1b-absent.log).
[R228] PASS Robustness - scripts/ci_rv32_sdk.py (unchanged since 3d90958f); test_builder.py:1489-1648 - real SDK fresh install and cache hit; in-place tamper of a sysroot header refused with inventory mismatch and zero tool executions, restored and re-verified; relocated copy refused on provenance; 50/50 literal resolver probes sound, covering every class, 16-byte and misaligned straddles at the window edge, 32-bit wrap, negative displacement, unreadable AMO operand, AMO rd, mirror stops on every memory writer, and loads not reported as stores.
[R228] PASS Docs - BAREMETAL_FIRMWARE.md:291-294,452-541,1248-1363; CI_WORKFLOWS.md:1070-1141 - each claim checked against code and my probes (census ISA, RV32I hart, class table, footprints, leaves-behind rules, LR/SC edges, not-observed list with compiled 64-bit atomic and callee plants ACCEPTED as stated, installer/cache contract, hosted log identification); docs_check, check_em_dash --base 574c29fa (188 added lines, 0 findings), doc_style, doc_paths, gen_toc --check/--verify-anchors, feature_status all exit 0. S6/S7 are optional precision.
```

Tests is UNCLEAN at this head because of R228-F6. What I examined under Tests:

- `ci_rv32_sdk_selftest.py`: 25 tests.
- `test_firmware_compiler.py --selftest`.
- The literal controls at `test_builder.py:5185-5450`.
- The compiled store-class and slot-rewrite mutants.
- 35 fix-removal mutants: 31 KILLED and 4 SURVIVED, 1 of them F6.
- `ci_events.py --check` (1631 items) and `--selftest` (2183 arms).
- `check_baremetal_only.py --check` (0 findings) and `--selftest` (365 arms).

## Reviewer-owned lens ledger

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #504 body and decisions 5771447690, 5771915061, 5778746031, 5789172582, 5790944031. Author scope statements 5789252310 and 5791069118. Acceptance 1-5 against `receipts/gate1b-sdk.log`, `gate1b-absent.log`, `gate1b-absent-require.log`, `hosted-exact-head-extract.txt`. `RESOLVER_STORE_RESIDUAL` unchanged. Merge-tree equality and change boundary | R228-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| RTL | CLEAN | No diff under `hdl/`, `tb/`, `syn/`, `sw/firmware/`, `sw/litex/` or `configs/`. Four gitlinks identical. 46/46 RTL variants elaborated with scoped 5.050 (`receipts/gate1b-*.log`). Clone integrity (`receipts/final-integrity-clone.txt`) | R228-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| Robustness | CLEAN | Installer on the real SDK: fresh, hit, verify-only, tamper, relocated copy (`receipts/sdk-*.log`). `receipts/resolver-probes-head.json` (50/50). Compiled plants (`receipts/gate-probes/*.json`). Pristine frame-alias scan | R228-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| Tests | UNCLEAN (R228-F6) | `receipts/mutation-summary.json` and `receipts/mutations/*` (35 mutants plus 2 null controls). Installer and audit self-tests. `ci_events` and `check_baremetal_only` check and selftest (`receipts/static/`) | R228-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| Docs | CLEAN | `BAREMETAL_FIRMWARE.md` and `CI_WORKFLOWS.md` diff claims against code and probes. Docs gates in `receipts/static/` (docs_check, em-dash, style, paths, TOC, anchors, feature status) | R228-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |

## Executions at this head

All of these ran in disposable copies under `scratch/`; the review clone was never written.

**Toolchain**

- Official archive: 102,597,892 bytes, SHA256 `d42680e9…b78f`, verified (`receipts/tool-identity.txt`).
- Scoped Verilator 5.050: wrapper SHA256 `905795b9…e92f`. It was first on PATH for every gate 1b and whole-gate run.

**SDK installer** (`receipts/sdk-*.log`)

- Fresh install through the head's installer took 13.1 s. Its target is `riscv32-buildroot-linux-gnu`, GCC 14.3.0, with 5007 inventory entries and 93 links.
- A cache hit took 0.75 s. Verify-only exits 0. The tamper and relocated-copy controls are as in the ledger.

**Gate 1b, SDK mapped** (`test_firmware_compiler.py --sdk-destination`)

- Exit 0: 217/217, 17/17 and 4/4, 46/46.
- 0 NOT RUN and 235 compiles.
- 242 audited invocations, with 0 argument tails changed.

**Gate 1b, absent** (`--absent`)

- Exit 0: 182/182, 17/17 and 4/4, 46/46.
- 1 NOT RUN and 0 compiles.
- With `--require-rv32` it exits 1 with "--require-rv32: the hosted firmware instruments must run".

**Resolver probes and mutants**

- `r228_resolver_probes.py`: 50/50 sound at the head and 16/50 at the base. The 5 documented-limit probes are unsound at both, as the page states.
- `r228_mutate.py`: 37 runs, 35 mutants plus 2 null controls. Every mutated file was restored and its SHA-256 re-verified.
- `r228_gate_run.py`: compiled whole-gate plants at the head, at the head with the F6 mutant, and at the base; plus the pristine frame-alias scan.

**Static gates** (`r228_static_gates.sh`)

- 20/20 exit 0, with the worktree clean afterwards.

**Exact-head hosted** (read-only; `receipts/hosted-exact-head-extract.txt`)

- All seven required contexts are `success`. "Physical gPTP" is `skipped`, as a nightly or manual job.
- Both builder jobs restored the SDK from cache ("SDK cache hit: verified"). Neither shows a fresh download at this head.

**Final integrity**

- 860 tracked blobs are byte- and mode-exact, and the index equals the HEAD tree.
- No assume-unchanged or skip-worktree flags. Status is clean, including ignored files.
- `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are at their gitlinks (`receipts/final-integrity-clone.txt`).

## Real limits

- I did not run the full parent, PP, gPTP, Yosys or builder banks, `act`, or any hosted job.
- Hosted evidence was read, not produced. At this head both hosted builder jobs used the verified-cache path. I did not observe a fresh hosted download at this head: the installer and workflows are byte-identical to `3d90958f`, where the manager recorded one.
- The mapped-prefix runs are local compatibility evidence, not hosted selector adoption.
- Compiled plants were judged by the gate's own `assert_boot_contract()` through an exec hook in disposable copies.
  - "ACCEPTED" means the whole boot contract passed the firmware. It does not assert that the product links, which matters for libatomic in the 64-bit plant.
  - Plants using `*p =` or raw `(T *)` casts were refused by the retained text rules, so they measure those rules and not the census.
- My mutation set is reviewer-chosen and not exhaustive.
- The pristine `sp`/`s0` alias scan covers the pristine firmware only.
- I did not independently repeat the author's old-versus-new resolver equivalence over all 120 census assemblies. The pristine gate at the unchanged residual, and 17/17 legitimate edits accepted, are my substitute.
- Scoped Verilator identity is established by version string and wrapper hash.
- Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Publish the full source static/builder and native banks for this head. I claim nothing about them.
- Trusted `act` and exact-head hosted acceptance, including whether a fresh hosted acquisition is required at the final head.
- The internal R227-3 verdict. I have not read it.
- After F6 is corrected, a re-review of the corrected head.
- The final current-dev candidate at the merge turn, then post-merge containment and the Done readback.
- A public Issue before #408/#409 retire any text rule onto the census, for the four shapes the page lists as not observed:
  - a callee's store through a handed window pointer (memset, memcpy, libatomic);
  - a callee's write into its caller's frame;
  - a numeric store that reaches the stack;
  - a sub-word frame-slot load.

  My compiled byte-load, 64-bit atomic and callee-member plants each pass the complete boot contract at the head and at the base.

R228-3 FINISHED
