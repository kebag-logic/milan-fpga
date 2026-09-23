# A185 handoff: #504 / PR #521 correction round for R228-1

Author: A185 (sole correction-round author). Public assignment:
issue #504 comment 5789172582. TAKEN: issue #504 comment 5789252310.
REVIEW READY: issue #504 comment 5789563728.
Nothing was pushed; the PR, its metadata and the issue board were not edited.

## Identity

| Item | Value |
|---|---|
| Corrected head | `5081a25a451b4ac1c00f286ec59ab041c22fdde9` |
| Corrected tree | `68a0628be2b55c1180a0e5751d2355cb8f987268` |
| Reviewed head (R227-1, R228-1) | `3d90958f3a82ca2a9617112c107a22f332117e17`, tree `b595c57b41d253660fcc84794352f174b90008a6` |
| Source base of the PR | `52711029f374650dc93830d5ea28e81cb5c8f410` |
| Live dev merged in | `483a133ed08867ea0d300d2b4a027b5b48a4282f`, ancestor of the head |
| Dev merge commit | `f6a55e4c85b6bdcdaeab6caa6b6e575c51cf97df`, tree `160a71776e7caf2dd51a48de3293bca26bb5f061`, equal to `git merge-tree --write-tree 3d90958f 483a133e` (clean, no conflict) |
| Branch | `504-hosted-rv32-compiler`, 3 local commits ahead of `origin/504-hosted-rv32-compiler` (merge + 2) |

Commits after the reviewed head (one-line subjects, no trailers):

1. `f6a55e4c` Merge dev 483a133e into 504-hosted-rv32-compiler
2. `48226b2f` builder: classify every RV32 store class in the resolved store census
3. `5081a25a` ci: fail the SDK installer self-test on download and receipt faults

Final integrity (`receipts/18-final-integrity.txt`): INTEGRITY PASS. 854
committed files match bytes and modes; the index equals HEAD with no
assume-unchanged or skip-worktree flag; the worktree status is empty. The
three required submodules sit at their gitlinks with clean worktrees. The
gitlinks are identical at the head, the reviewed head and dev: verilog-axis
`48ff7a7e2ef782cf778d47910cf85835c64b1bce`, protocol-processor
`424c688fa2205b934a7689a58f2aa766420f2326`, gptp-processor
`c1b617435824929a790739ea8585c3fe1a328cc0`, and `external`
`efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`, which is not initialised.

Change boundary (`receipts/19-change-boundary.txt`). The two correction
commits touch only `sw/builder/test_builder.py`,
`scripts/ci_rv32_sdk_selftest.py`, `docs/integration/BAREMETAL_FIRMWARE.md`
and `docs/testing/CI_WORKFLOWS.md`. Both workflows, the installer
`scripts/ci_rv32_sdk.py` (SHA256 `ffcc5433...cb4`, so the cache key is
unchanged), `scripts/ci_events.py`, `scripts/check_baremetal_only.py` and
`sw/builder/test_firmware_compiler.py` are blob-identical to the reviewed
head. No path under `hdl/`, `tb/`, `syn/`, `sw/firmware/`, `sw/litex/` or
`configs/` changes, and no budget or ratchet file changes.

## Per-finding resolution

### R228-F1 MAJOR: FP stores bypassed the resolver

The root cause was a mnemonic allow-list (`RV32_STORES = ("sw", "sh", "sb")`)
with a silent default that only cleared an unknown instruction's first operand.
The route is the one set by the manager's correction assignment and recorded in
TAKEN. The resolver and census were fixed; the census ISA and SDK selection were
not changed.

- Stores are classified by instruction class. `RV32_STORE_BYTES` covers `sb`,
  `sh`, `sw`, `fsh`, `fsw`, `fsd` and `fsq`, with their widths.
  `RV32_ATOMIC_STORE_RE` covers every `amo*.w` and `sc.w` with its ordering
  suffixes. The memory operand is the last operand of every class.
- A store is reported at every 32-bit word it writes (`rv32_footprint_words`),
  so an `fsd`, or a misaligned `sw`, whose first byte lies just below the
  window is refused on the window word it reaches. A bounded-range store
  covers its footprint (`hi + width - 1`).
- Class fail-closed default: any other instruction with a register memory
  operand that is not a recognised load (`lb`/`lh`/`lw` family, `flh`..`flq`,
  `lr.w`) is reported as `unclassified` and refused by rule 1b.
- Every store makes the modelled frame or static words it overlaps unknown.
  An AMO or SC clears its `rd`. Integer exact-word semantics are unchanged.
- Permanent controls, part of gate 1b:
  - Literal-assembly store-class controls run on every machine, compiler or
    none. There are 13 class probes, 4 loads that must not be stores, 2
    unclassified mnemonics (`c.sw`, `amocas.w`) and 4 stale-value probes.
  - Five compiled resolver-only mutants use the paged base: `float` (`fsw`),
    `double` (`fsd`), atomic exchange (`amoswap.w`), fetch-or (`amoor.w`) and
    compare-exchange (`sc.w`). Each is refused on `RESOLVER_STORE_PIN` through
    the whole gate.
  - A compiled measurement requires each to actually emit its class when the
    census arch declares the extension. The atomic three are registered only
    when the census ISA carries `a`; otherwise a registered `NOT RUN`.
- Docs: `docs/integration/BAREMETAL_FIRMWARE.md` states the class table, the
  footprint rule, the fail-closed default and the boundary. `CI_WORKFLOWS.md`
  now states the census ISA (`rv32imafd`/ILP32D) and that it matters to the
  instruments. The boundary: raw `.insn` and data words are not instructions to
  the reader and stay with the inline-asm pin, and numeric local labels are not
  bound.

Evidence at the head, using scoped Verilator 5.050, the freshly verified SDK
prefix and the lane checkout read-only:

| Check | Result |
|---|---|
| Gate 1b mapped (`receipts/gate1b/pristine-sdk.*`) | exit 0 in 341 s. 213/213 mutations (208 before, plus 5 new); 17/17 and 4/4 positives; 46/46 RTL variants elaborated; 7/7 instrument-only shapes; 0 NOT RUN; 227 actual firmware compiles. Census arch `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0`; compiled classes `fsw, fsd, amoswap.w, amoor.w, sc.w`; residual unchanged (`parse_u64() through call(__errno_location) x1`); 66 pristine stores |
| Gate 1b absent (`receipts/gate1b/pristine-absent.*`) | exit 0 in 283 s. 182/182; 17/17, 4/4, 46/46; exactly 1 NOT RUN (the census); 0 firmware compiles; all three cross candidates hidden. The skipped-entry count is now 31 (26 before, plus the 5 new resolver-only entries) |
| Compiler audit (`receipts/16`) | 234 records; 231 map only argv[0]; every argument tail preserved; the single non-zero return is the gate's deliberate 64-bit probe |
| R228-1 plants, applied in memory (`receipts/17`) | float, double and uint32 each refused on the resolver pin; gate 1b PASS each |
| F1 mutants (`receipts/17`, logs in `receipts/store-class-logs/`) | 8/8 KILLED on the expected sentence, including pre-fix classification with the literal control removed (the compiled measurement fails) and with the measurement also removed (the table entry fails as "passed the boot-contract gate") |
| R228-1 `probe_fp_store.py` (`receipts/13`) | on the SDK default ISA, `fsw`/`fsd`/`amoswap.w` are reported at `0x90000750`, `0x90000614`+`0x90000618` and `0x90000750`: the same words the ILP32 soft-float compile reports |
| Resolver equivalence (`receipts/14`, `15`) | pre-fix `f6a55e4c` vs head over all 116 census assemblies of a full mapped run: 106 identical (pristine and every prior mutant); the 10 that differ are exactly the five new store-class mutants compiled twice |

### R228-F2 MAJOR: download-path digest check had no failing control

`scripts/ci_rv32_sdk_selftest.py` now drives `install()` with no `--archive`,
the hosted path, through a mocked `urlopen`.

- `test_download_path` (positive) proves the branch is taken and the pinned
  bytes install. `urlopen` is called once with the pinned URL.
- `test_download_path_refuses_unpinned_bytes` serves four payloads. Each must
  be refused with `archive digest mismatch`, with no `tarfile.open`, no
  subprocess (no tar, no `relocate-sdk.sh`), no prefix and no relocation
  marker:
  - a well-formed archive with the pinned root and a marker-writing
    relocation;
  - a truncated archive;
  - an empty payload;
  - the pinned fixture under a pin one hex digit away, which kills any prefix
    comparison.

Evidence:

- R228-1's `mutate_installer.py` (`receipts/10`) now KILLS "extract: drop
  digest check (download path)".
- `mutate_download_auth.py` (`receipts/12`) KILLS 6/6 weakenings: delete,
  first-8-digit compare, warn-only, self-compare, check after tar, and skip for
  the download file name.
- R228-1's `probe_download_auth.py` (`receipts/11`) gives the same result as at
  the reviewed head: the head refuses, and the deleted check would install.

### R228-F3 MINOR: receipt bindings not failure-sensitive

- The expected provenance field set is pinned in the test
  (`PROVENANCE_FIELDS`). `test_wrong_provenance` asserts it and iterates it.
- `test_provenance_values` recomputes the installer SHA256 and host
  independently.
- `test_changed_installer` refuses a cache made by other installer bytes.
- `test_retargeted_symlink` retargets the selector to an identical in-prefix
  twin and must be refused on inventory before execution.
- `test_escaping_compiler` plants a compiler whose realpath leaves the prefix
  and must be refused without execution.
- Optional R228-S1, tests only: `test_archive_root`, `test_special_file` and
  `test_extra_receipt_section`.

Evidence: R228-1's `mutate_installer.py` KILLS 23/23 (15/23 at the reviewed
head), including all four F3 mutants and the three S1 guards. Installer
self-test: 25 tests (16 plus 9), exit 0.

## Acceptance kept intact

These are unchanged: the selection (Bootlin stable 2025.08-1 riscv32-ilp32d
glibc), authentication before extraction or execution, and the installer bytes
and behaviour. The latter covers fresh install (13.1 s), cache hit (0.83 s),
verify-only, relocation, interrupt, tamper and the unsupported host.

The rest of the acceptance is also unchanged. Every text refusal and the
declared residual are unchanged. The absent tally is 182, and the positives
are 17 and 4. There are 46 RTL variants and 7 instrument-only shapes. PP and
gPTP pins and ratchets are unchanged. #408/#409 still own text-rule retirement.

## Focused static gates at the head (`receipts/static-final/`, all exit 0)

- The installer self-test ran 25 tests.
- `test_firmware_compiler.py --selftest` passed.
- `check_baremetal_only.py`: `--check` found 0 findings and `--selftest` passed
  365 arms.
- `ci_events.py`: `--check` passed 1555 items and `--selftest` passed 1198
  arms.
- `docs_check.py` found 0 findings.
- `check_em_dash.py` found 0 findings with `--base 52711029` (136 added lines)
  and with `--base 483a133e` (135). Its self-test passed 57 arms.
- `check_doc_paths.py` passed.
- `gen_toc.py --check` and `--verify-anchors` passed.
- `check_doc_style.py` passed.
- `check_py_idiom.py`, `check_hygiene.py --check`,
  `measure_fail_fast.py --check`, `measure_test_evidence.py --check`,
  `measure_naming.py --check`, `check_todo_ownership.py` and `py_compile` all
  passed.

The "can be lowered" notes from `measure_fail_fast` and
`measure_test_evidence` concern HDL-module and suite counts that this diff does
not touch.

## Not done here (manager-owned or out of scope)

- Out of scope by instruction: pushing, and editing the PR or the board. So
  are the full parent, PP and gPTP Verilator, Yosys, builder and behave banks,
  Docker or act, and hosted runs. A hosted cache-hit run has not been
  observed. The hosted counts will differ from the local counts for the reasons
  R227-1 and R228-1 recorded (no Verilator at the gate call, and make without
  `-e`).
- R228-S2 (relocation without `file`) and R228-S3 (download retries and a total
  deadline, job `timeout-minutes`) change installer or workflow behaviour. They
  were not taken.
- Out-of-scope observations for the manager (new Issues if wanted):
  1. `rv32_blocks()` drops a branch target that is not a block label. GCC's
     numeric local labels (`1:`, `1f`, `1b`), which appear only in LR/SC
     loops here, therefore leave those loops without their edges. Conditional
     branches keep the fall-through, so the SC store is still reached and
     judged. An unconditional jump to such a label would make the following
     block unreachable, and its stores unobserved. Only inline asm could emit
     that here, and the inline-asm set pins it.
  2. `sb`/`sh` into a frame slot still record the full source register as the
     slot value, and `lb`/`lh` read it back unmasked. This value imprecision
     predates the lane and was left unchanged. Overlap invalidation now covers
     the partial-overwrite case.
- Raw receipts contain local absolute paths and must be neutralized before
  any public copy.
- The disposable trees under `scratch/` were deleted: the SDK prefixes,
  captures, probe directories and fixture copies.

## Files

- `TAKEN.md` is the posted TAKEN text.
- `PR-BODY.md` is the proposed PR body for the manager.
- `REVIEW-READY.md` is the posted REVIEW READY text.
- `COMMANDS.md` lists the exact commands.
- `scripts/` holds the author scripts, and `scripts/r228-1/` holds unmodified
  copies of R228-1's scripts.
- `receipts/` holds the numbered receipts, with `gate1b/`, `static-final/`,
  `static/` and `store-class-logs/`. The `static/` receipts are the pre-commit
  working-tree runs; `static-final/` holds the head runs.
