[R227] NEGATIVE - exact head 97aa1ec943ac740a27b942210a248f6512ae3ff6

Round R227-3: cleared-context internal review of issue #504 / PR #521. Tree
`4a12a545bdb478083d711a8f319d3c6d70c1b1d9`, source base and live dev
`574c29fa111c74e5e5ed63e4670aff1f492e28e2`.

## Verdict in one paragraph

All four findings from the second round are resolved at their root: R227-2-F1,
R227-2-F2, R228-2-F4 and R228-2-F5. The first-round R228-1 F1-F3 resolutions
still hold, and I re-verified each with my own fault probes (below). One new
MINOR finding is open. The low boundary of the new overlap-invalidation function
has no failing control. A one-token regression there passes every literal
control and the complete compiled gate 1b. It also reopens the R227-2-F1 class
of bypass: a union byte store into the top byte of a parked word, which then
advertises the entity before the AEM verdict. Conformance, RTL, Robustness and
Docs are covered clean at this head. Tests is UNCLEAN.

## Reconstruction

I read these in the contract's order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md, and REQUIREMENTS.md REQ-VER-03/04.
3. The #504 body and frozen acceptance items 1-5, with the public decisions
   5771447690, 5771915061, 5778746031, 5789172582 and 5790944031.
4. docs/testing/CI_WORKFLOWS.md and docs/integration/BAREMETAL_FIRMWARE.md.
5. The complete `574c29fa..97aa1ec9` diff (10 files) and its history.
6. Exact-head hosted job logs, read-only.

The history holds six one-line, trailer-free commits and two dev merges. Merge
`4914eea5` has tree `fdf07c85`, which equals `git merge-tree --write-tree
5081a25a 574c29fa`, so the merge is clean (`receipts/history.txt`).

I wrote my findings in `receipts/independent-draft-findings.txt` before reading
any prior review report, and before reading the A191 REVIEW READY
(5791630048). No private author material, lane scratchpad or management
workspace was read.

The draft recorded the sub-word frame-slot load as a MINOR. After the
independent pass I re-read the page text and compared it with the earlier
disposition of the same behaviour, R227-2 OBS-1. The page now names the
behaviour as not observed and claims nothing about it. The behaviour is also
identical at the base. So it is reported below as a pre-existing out-of-scope
observation, O1, with a documentation suggestion, and not as a finding against
this PR. The draft is published unchanged.

## Findings

[R227] MINOR Tests - `sw/builder/test_builder.py:1501-1508` (`_rv32_forget_overlap`, condition `key[-1] + 3 >= start`) - the overlap low boundary that closes the top-byte union overwrite has no failing control

Requirement/evidence:
- AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims
  to detect", and "Positive, negative, and boundary behavior is covered".
- The same standard held R228-F4 at MINOR: "A one-token regression ... would
  reopen an F1-class bypass ... Nothing in the builder would notice".
- The function is new in this correction lane. Its low boundary decides whether
  a store touching only the LAST byte of a modelled word invalidates that word.
- Mutant M15 changes `>=` to `>`. It passes every literal resolver control:
  `receipts/mutants/M15-overlap-low-boundary.{json,log}` reaches the planted
  stop marker.
- It also passes the complete compiled gate 1b on the adopted SDK: C4 exits 0
  with `GATE 1b PASS; 0 NOT RUN` (`receipts/mutants/C4-compiled-M15.{json,log}`).
- Compiled plants, where a union byte store rewrites byte 3 of a parked
  `0x12000600` so that the word becomes ADP_CTRL `0x90000600` (the resolver asked
  alone, and the whole gate asked):
  - at this head, the frame-slot and static plants are both REFUSED as
    unplaced stores (`receipts/mutants/P-plants.plants.json`);
  - under M15 both are ACCEPTED by the resolver and by the complete gate
    (`receipts/mutants/P-plants-M15.plants.json`).
- The literal-assembly equivalents behave the same way:
  - `receipts/literal-probes-head.json`: `top-byte-store-*` is unplaced;
  - `receipts/literal-probes-m15.json`: placed at `0x12000600`, outside the
    window, so rule 1 accepts it.
- The existing stale probes cover byte offsets 0 and 1 only
  (`test_builder.py:5272-5312`). The compiled rewrite mutants use offset 0 only
  (`:11293-11325`).

Impact:
- At this head the behaviour is correct.
- A single-token regression would silently reopen a pre-AEM entity enable, and
  the complete compiler-backed gate would stay green: `u.b[3] = x` on a parked
  word is ordinary compiled C.
- This is the same exposure R228-F4 was raised for, at the other end of the
  same function.

Required change: a shipped control that fails when a store covering only the
last byte of a modelled frame-slot or static word leaves that word readable.
A literal-assembly control is enough, as it is for the existing probes.

Verification:
- M15 (`scripts/probe_mutants.py ... M15-overlap-low-boundary`) must be KILLED on
  the new control's sentence.
- The `top-byte-store-*` plants stay REFUSED at the corrected head.
- M0 still reaches the stop marker.

## Suggestions (optional; no effect on coverage)

- **R227-3-S1 (Tests).** Two more boundaries survive every control:
  - M16: a slot that starts exactly at a store's last byte;
  - M17: the footprint's last word computed one byte short. For example, a
    `sw` at `csr_base-3` loses the window word.

  Both are reachable only by misaligned spellings that GCC does not emit here,
  and the inline-asm set pins asm templates. The page says a misaligned
  straddling `sw` is refused, and the probe uses offset -2 only. Probes at odd
  offsets (-1 and -3) would pin both boundaries.

  Separately, M4 shows that the slot-mirror's first term
  (`rv32_store_bytes(mnem) is not None`) is redundant for every readable store
  operand, because the memory-operand term already covers them. It only matters
  for an unreadable store operand, which rule 1b refuses anyway. The mirror
  behaviour itself is controlled: M45 and M5 are KILLED.
- **R227-3-S2 (Docs).** Two precision points in
  `docs/integration/BAREMETAL_FIRMWARE.md`:
  - The bullet at `:538-539` ("A byte or half-word load from a frame slot reads
    the slot's whole modelled word") does not state its consequence. The
    called-function bullet above it states its own. That consequence is
    measured below under O1: a compiled pre-AEM ADP_CTRL enable that passes the
    complete gate.
  - The memset example at `:522-530` holds only where GCC emits a call. A
    small constant-size `__builtin_memset` is expanded inline even at -O0, and
    is then observed and refused: plant `doc-memset` is REFUSED. The 64-bit
    exchange plant is ACCEPTED, exactly as the page says.

## Out-of-scope observation O1 (pre-existing; not attributed to this PR)

This is R227-2 OBS-1, re-measured, with its consequence now shown on compiled C.

- **The mechanism.**
  - `test_builder.py:1483-1484` reads a frame slot's whole modelled word for
    every load width: `lb`, `lbu`, `lh`, `lhu` and `lw`.
  - Statics are read only by `lw` (`:1469-1482`). The code comment there calls a
    partial read "a WRONG value rather than a missing one".
- **At this head.**
  - A union half-word read of a parked `0x12340600`, OR-ed into the window
    page, stores to ADP_CTRL `0x90000600`. The lattice places that store at
    `0x92340600`, outside the window.
  - The resolver alone and the complete compiled gate 1b both ACCEPT it. So
    does the byte-read variant (`receipts/mutants/P-plants.plants.json`).
  - The whole-word control read of the same union is REFUSED.
- **At the base.**
  - `receipts/literal-probes-base-574c29fa.json` shows the identical placement
    on the source base `574c29fa`.
  - The diff does not touch `_rv32_step_load`.
- **Disclosure.**
  - The page names the behaviour under "What the census does NOT observe"
    (`:538-539`) and says a retired text rule would not cover it either
    (`:541`).
  - No text claims the case is handled.
- **Information for the follow-up Issue, not a prescribed design.**
  - The disposable probe `FIX1` restricted frame-slot reads to `lw`, as
    statics already are.
  - Both read plants and both top-byte plants then became REFUSED.
  - The pristine census passed up to the plant point
    (`receipts/mutants/FIX1-plants-frame-lw-only.plants.json`).
  - The later gate stages were not run under FIX1.
- **Other documented gaps.** The callee-writes-caller-frame plant and the
  64-bit atomic plant also pass the complete gate. The page documents both.
- **Status.**
  - I found no public Issue that tracks these documented gaps.
  - The author's REVIEW READY recommends one before #408/#409 retire any text
    rule onto the census.

## Per-lens results at 97aa1ec9

[R227] PASS Conformance - `scripts/ci_rv32_sdk.py:24-30`, `.github/workflows/docs.yml:172-190`, `.github/workflows/elaborate.yml:242-260`, `sw/builder/test_builder.py:4112-4122,4158-4165`, `receipts/head-gate1b-{sdk,absent}.log`, `receipts/compiler-audit-summary.txt`, `receipts/hosted-exact-head-summary.txt`, `receipts/hosted-check-runs.tsv` - checked against acceptance items 1-5 and decision 5771915061:
- **Selection and installer.** The pinned Bootlin 2025.08-1 archive:
  102,597,892 bytes with the pinned SHA256 (`receipts/tool-identity.txt`).
  - Fresh install took 13.2 s and the verified cache hit 0.76 s. The SDK
    reports GCC 14.3.0, target `riscv32-buildroot-linux-gnu` and a relocated
    sysroot (`receipts/sdk-install.log`).
  - Both workflows install it at the selector location, with the cache keyed by
    digest, OS, architecture, revision and installer bytes. Elaborate keeps its
    scope guard.
- **Compiled gate 1b, the item 2 counts.**
  - 217/217 hostile refusals, 17/17 firmware and 4/4 Makefile positives, 46/46
    RTL variants, 0 NOT RUN.
  - 235 firmware compiles, and all 120 census assemblies are
    `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0`. Every argv tail is
    preserved, and only argv[0] of the selector is mapped.
  - The five store-class mutants emitted `fsw`, `fsd`, `amoswap.w`, `amoor.w`
    and `sc.w`, and each was refused on its resolved address.
- **Absent gate 1b, item 3.** 182/182, 17/17, 4/4, 46/46, exactly one compiler
  NOT RUN, and 0 firmware compiles.
- **Residual, item 5.** Unchanged: only `("parse_u64", "call",
  "__errno_location")`.
- **Scope.**
  - No text refusal is retired.
  - No RTL, firmware, gitlink or product setting changed.
- **Exact-head hosted, items 1 and 4, read-only.**
  - `docs-check` and `elaborate` executed and succeeded. Both restored the SDK
    from the digest-bound cache, verified it, and adopted
    `/home/runner/br-milan-rv32/host/bin/riscv32-linux-gcc` (GCC 14.3.0).
  - They graded 170/170 non-RTL compiled refusals, and docs-check graded
    135/135 absent refusals. These match 217 and 182 without the 46 RTL entries
    and the MAKEFLAGS entry, which the hosted make does not honour.
  - `verilator-suites`, `yosys-portability` and `rtl-fast` succeeded.
    `Physical gPTP` is a skipped context.

[R227] PASS RTL - `git diff --name-only 574c29fa..97aa1ec9` (10 files; no `hdl/`, `tb/`, `syn/`, `sw/firmware/`, `sw/litex/` or `configs/` path), `git ls-tree` gitlinks identical at base and head, `receipts/head-gate1b-sdk.log` (46/46 RTL mutation variants elaborated as the real option-on top with scoped Verilator 5.050), `receipts/final-integrity*.txt` - no RTL, CDC, reset, interface or processor-pin change exists to review:
- the census ISA (`rv32imafd`) differs from the shipping RV32I hart only inside
  the census compile, as both pages state;
- the exact-head hosted Verilator and Yosys aggregates succeeded.

[R227] PASS Robustness - `scripts/ci_rv32_sdk.py:103-170`, `scripts/ci_rv32_sdk_selftest.py`, `sw/builder/test_builder.py:1489-1649`, `receipts/installer-workflow-probes.json`, `receipts/probe-summary.txt`, `receipts/literal-probes-head.json` - the changed artifacts were checked against hostile and corrupt input:
- **Installer.**
  - A wrong, truncated, empty or near-pin download is refused before tar reads
    it or any script runs.
  - Cache receipts that are corrupt, stale, symlinked or carry an extra section
    are refused before any cached tool executes. So are special files, a
    retargeted selector, an escaping realpath, an unrelocated SDK, a moved cache
    and an unsupported host.
  - A failed relocation leaves no success receipt, and an existing unreceipted
    tree is never replaced.
- **Resolver, correct at this head.**
  - Every store class is classified: integer, FP, AMO and SC.
  - A store is judged at every word it writes, and a ranged store over its
    footprint.
  - Unknown memory-writing mnemonics fail closed.
  - Sub-word, FP, non-swap AMO and SC stores leave the slot unknown, including
    the top byte.
  - Stores through a stack address forget the frame, and an AMO's rd is
    cleared.
- **Scope of this lens.** The sub-word LOAD path is pre-existing and unchanged
  (O1).

[R227] PASS Docs - `docs/integration/BAREMETAL_FIRMWARE.md:452-541,1265`, `docs/testing/CI_WORKFLOWS.md:1070-1140`, the printed gate lines (`test_builder.py:13579-13590,13979-13990`), `receipts/static/SUMMARY.txt`, `receipts/mutants/P-plants.plants.json` - every contract statement was compared with the code and with my plants and mutants. These all match:
- the class table;
- footprint judgement;
- the UNCLASSIFIED default;
- what a store leaves behind, including the stack-address rule;
- the LR/SC boundary, with both unbound edges named;
- the census ISA against the shipping hart;
- the three "does NOT observe" bullets. The 64-bit atomic and
  callee-frame plants pass, as stated;
- the cache and trust-boundary text;
- `--require-rv32`;
- the absent control;
- the reproduction commands, which I ran.

No text claims a case my plants contradict. The docs, em-dash (0 findings over
188 added lines), style, path, TOC and anchor gates pass. S2 is optional.

## Prior public review findings on this PR

| Prior finding | Disposition at 97aa1ec9 | My evidence |
|---|---|---|
| R228-1 F1 MAJOR, FP stores bypass the resolver | RESOLVED, retained | M14, M11, M12 and M13 KILLED by the literal class controls. C3 (pre-F1 classes, literal controls neutralised) KILLED by the compiled store-class check. The five compiled classes are emitted and refused, locally and on the exact-head hosted jobs |
| R228-1 F2 MAJOR, download digest check had no failing control | RESOLVED, retained | I1 (check removed) and I2 (prefix compare) KILLED by `test_download_path_refuses_unpinned_bytes` |
| R228-1 F3 MINOR, receipt bindings | RESOLVED, retained | These are KILLED: I3 (destination dropped), I4 (installer digest constant), I5 (symlinks dropped), I6 (realpath escape) and I14 (modes dropped) |
| R228-1 S1 | RESOLVED | I10 (root check) KILLED. Special-file and extra-section tests present |
| R228-1/R228-2 S2, S3 | RETAINED, optional | The installer is unchanged: relocation is proven through `sdk-location` and the sysroot, and the download has no retry or total deadline |
| R227-1 (POSITIVE at 3d90958f) | Superseded | Later commits changed artifacts in four lens scopes |
| R227-2-F1 MINOR, frame-slot sub-word overwrite | RESOLVED at the root (route 1) | These are KILLED: M1 (sub-word stores keep the value), M2 (no frame forget on a stack store) and M3 (no frame overlap). With those literal controls neutralised, C1 and C2 are KILLED by the compiled union and pointer mutants. The top-byte plants are REFUSED at head. The remaining boundary gap is the new finding above |
| R227-2-F2 MINOR, three changes without a failing control | RESOLVED | These are KILLED: M6 (range footprint), M45 and M5 (slot mirror), M7 and M7b (non-swap AMO or SC write rs2), M8 (AMO rd kept) and M21 (the amoswap positive arm) |
| R227-2-S1 | TAKEN | `BAREMETAL_FIRMWARE.md:508-516` names both the back edge and the forward exit |
| R227-2 OBS-1, sub-word frame load | RETAINED as out-of-scope O1 | Now named on the page. Still in the tree, and no Issue exists |
| R228-2-F4 MINOR, two load-bearing parts without a control | RESOLVED | M6 (the RM8 equivalent) and M10b (static overlap width fixed at 4, the RM11 equivalent) are KILLED, and M9 and M18 are KILLED |
| R228-2-F5 MINOR, the page claimed contradicted coverage | RESOLVED | The page states RV32A AMO and SC instruction classes, and says a called function's stores are not observed. The stack-pointer rewrite is now closed in code (M2 and C2), not only narrowed in the text. The 64-bit atomic plant still passes, as stated |
| R228-2-S4 | TAKEN | M45 (the RM1 class) and M13 (the RM5 equivalent) are KILLED |
| R228-2 O1 | Partly closed | The in-function stack-pointer half is closed in this PR. The called-function and call-crossing halves remain documented, and no Issue exists |

## Execution evidence (all at exact head 97aa1ec9)

| Execution | Result | Receipt |
|---|---|---|
| Archive and tool identity | 102,597,892 bytes with the pinned SHA256. Scoped Verilator 5.050 | `receipts/tool-identity.txt` |
| Fresh install, then cache hit, under a disposable scratch prefix | exit 0 and exit 0; 13.2 s and 0.76 s | `receipts/sdk-install.log` |
| Gate 1b with the SDK mapped | exit 0 in 335 s: 217/217, 17/17, 4/4, 46/46, 0 NOT RUN, 235 compiles | `receipts/head-gate1b-sdk.{log,exit}`, `receipts/compiler-audit-summary.txt` |
| Gate 1b absent | exit 0 in 270 s: 182/182, 17/17, 4/4, 46/46, 1 NOT RUN, 0 compiles | `receipts/head-gate1b-absent.{log,exit}` |
| Focused static and policy gates (25 commands) | all exit 0. Installer self-test 25 tests; ci_events 1631 items and 2183 arms; bare-metal 0 findings and 365 arms; em-dash 0 findings and 57 arms | `receipts/static/` |
| Resolver fault probes (literal) | 22 fault mutants: 18 KILLED on their own control's sentence. M4 (redundant term) and M15, M16 and M17 (boundaries) survive. The no-edit control M0 reaches the stop marker | `receipts/probe-summary.txt`, `receipts/mutants/` |
| Compiled-mutant sensitivity | C1, C2 and C3 KILLED. C4 (M15) survives the complete gate, exit 0 | same |
| Compiled plants (resolver alone and whole gate) | head, M15 and FIX1 tables | `receipts/probe-summary.txt`, `receipts/mutants/*.plants.json` |
| Literal resolver probes | head, M15 and base `574c29fa` | `receipts/literal-probes-*.json` |
| Installer faults and workflow edits | installer 16/16 KILLED (unmutated control passes). Workflow 8/8 REFUSED by `ci_events.py --check` | `receipts/installer-workflow-probes.json` |
| Exact-head hosted | read-only job logs and check runs | `receipts/hosted-exact-head-summary.txt`, `receipts/hosted-check-runs.tsv` |
| Final integrity | PASS. HEAD and tree as reviewed. The index equals HEAD with no hidden flags. 860 parent blobs byte- and mode-exact. Status clean, including ignored files. The three initialised submodules (222 + 103 + 214 blobs) are at their gitlinks and clean. `external` is uninitialised at its pin | `receipts/final-integrity.txt`, `receipts/final-integrity-submodules.txt` |

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #504 acceptance 1-5 and the decisions listed above; installer constants; both workflow diffs; `--require-rv32` adoption; residual table; compiled and absent gate 1b; compiler audit; exact-head hosted logs | R227-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| RTL | CLEAN | changed-path list; gitlinks at base and head; 46/46 RTL variants elaborated; final integrity of parent and submodules; exact-head hosted Verilator and Yosys contexts | R227-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| Robustness | CLEAN | installer under 16 faults plus the real SDK fresh and hit runs; resolver under 22 literal fault mutants, 4 compiled-mutant runs and 8 compiled plants in 3 variants; literal probes at head, M15 and base | R227-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| Tests | UNCLEAN (R227-3 MINOR, overlap low boundary) | PR literal controls `test_builder.py:5188-5440`; compiled mutants `:11239-11440` and `:13179-13248`; installer self-test; firmware-compiler self-test; ci_events arms; M15 survives the complete gate (C4) | none at this head | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| Docs | CLEAN | `BAREMETAL_FIRMWARE.md:452-541,1265`; `CI_WORKFLOWS.md:1070-1140`; printed gate claims; the documentation gates; plants against each "does NOT observe" bullet | R227-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |

## Real limits

- **Not run, by instruction.**
  - The full parent, PP, gPTP, Yosys and builder banks. Only gate 1b ran, through
    `sw/builder/test_firmware_compiler.py`, and not the whole
    `test_builder.py`.
  - Docker/act, and host `act_ci` or its self-test.
  - Hardware. Physical calibration is NOT RUN, and field skips are not hardware
    proof.
  - The manager's static/builder and native banks for this head are neither
    claimed nor inferred.
- **Local mapping.**
  - The mapped-SDK runs substitute only the selector's argv[0]. That is
    local compatibility evidence, not hosted adoption.
  - Hosted adoption is recorded from read-only exact-head logs. At this head
    both hosted jobs were verified cache hits. A fresh hosted acquisition was not
    observed at this head; the installer-bytes component of the cache key is
    unchanged.
- **Probe trees.**
  - Mutants, plants and static gates ran on disposable copies of the exact-head
    clone, including its initialised submodules, under unpublished scratch.
  - The review clone ran only the two pristine gate 1b modes. They wrote ignored
    `__pycache__` directories, which I removed. They also rewrote six
    tracked generated `.svh` files with identical bytes, which integrity verified.
- **Classification method.** Probe verdicts are read from the gate's own
  assertion sentences and from a planted stop marker. A literal-mode "SURVIVED"
  exits 1 by design, through the stop marker. Anchors are applied by
  exact-string edits, each asserted to apply exactly once.
- **FIX1** is information for the follow-up Issue only. It ran as far as the
  plant point and is not evidence that the candidate passes the full gate.
- **Plant construction.** The plants reuse the gate's own mutant helpers
  (`stored_before_aem`, the typedef'd paged base) and are asked through its
  `assert_resolved_boot_flow` and `assert_boot_contract`.
- **Receipt paths.** Published receipts substitute `$REVIEW_OUT`, `$CLONE`,
  `$HOME`, `$ARCHIVE_DIR` and `$PINNED_TOOL_BIN` for local paths. The raw
  copies stay in unpublished scratch. The SDK prefix and probe trees were
  deleted after measurement.

## Pending manager duties

- Publish this report and route the MINOR to the author. R227 re-reviews the
  corrected head; R228-3 is in flight separately.
- Record, or file, the public follow-up Issue for the documented resolver gaps,
  before #408/#409 retire any text rule onto the census:
  - stores inside a called function handed a window pointer;
  - a callee's write into its caller's frame;
  - numeric stores that alias a model;
  - sub-word frame-slot loads (O1).
- The full source static/builder and native banks for this head, trusted act,
  and exact-head hosted acceptance, including fresh-acquisition evidence for
  the installer revision in use.
- The final current-dev candidate at the merge turn (source base and live dev
  `574c29fa`), then post-merge containment.

## Reproduction

The commands below run from an exact-head clone, with `PATH` prefixed by the
scoped Verilator directory and the archive verified as above.

```sh
python3 scripts/ci_rv32_sdk.py --destination "$REVIEW_OUT/scratch/sdk/host" --archive "$ARCHIVE_DIR/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz"
python3 scripts/ci_rv32_sdk.py --destination "$REVIEW_OUT/scratch/sdk/host"
python3 -u sw/builder/test_firmware_compiler.py --sdk-destination "$REVIEW_OUT/scratch/sdk/host" --audit "$REVIEW_OUT/scratch/head-sdk-argv.jsonl"
python3 -u sw/builder/test_firmware_compiler.py --absent --audit "$REVIEW_OUT/scratch/head-absent-argv.jsonl"
bash "$REVIEW_OUT/scripts/run_focused_static.sh" <exact-head-copy> "$REVIEW_OUT/receipts/static" 574c29fa111c74e5e5ed63e4670aff1f492e28e2
python3 "$REVIEW_OUT/scripts/probe_mutants.py" <exact-head-copy> <work> "$REVIEW_OUT/receipts/mutants" "$REVIEW_OUT/scratch/sdk/host" M0-none M15-overlap-low-boundary C4-compiled-M15 P-plants P-plants-M15   # and the other IDs in the script
python3 "$REVIEW_OUT/scripts/literal_probes.py" <tree> [--m15]
python3 -B "$REVIEW_OUT/scripts/probe_installer.py" <exact-head-copy> <work> "$REVIEW_OUT/receipts/installer-workflow-probes.json"
python3 -B "$REVIEW_OUT/scripts/verify_integrity.py" "$CLONE" 97aa1ec943ac740a27b942210a248f6512ae3ff6 4a12a545bdb478083d711a8f319d3c6d70c1b1d9
```

R227-3 FINISHED
