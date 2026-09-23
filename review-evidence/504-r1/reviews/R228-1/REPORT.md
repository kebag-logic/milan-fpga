[R228] NEGATIVE - exact head 3d90958f3a82ca2a9617112c107a22f332117e17

External independent review, round R228-1, issue #504 / PR #521.
Head `3d90958f3a82ca2a9617112c107a22f332117e17`, tree `b595c57b41d253660fcc84794352f174b90008a6`, source base `52711029f374650dc93830d5ea28e81cb5c8f410`.
Paths use `$REVIEW_OUT` for this round's output directory and `$CLONE` for the isolated review clone.

## Verdict summary

Most of the installer works as specified. Every probe I ran behaved correctly:

- archive authentication, fresh install and cache hit;
- interrupted install;
- foreign, stale and tampered caches;
- unsupported host and symlinked destination;
- hosted selector adoption.

Two MAJOR findings and one MINOR finding remain open:

- **F1 (MAJOR)**: the adopted compiler's default ISA (`rv32imafd`, ILP32D) emits `fsw` and `fsd`. The resolver neither classifies nor refuses those stores.
  - Float and double versions of an existing resolver-only hostile control pass the complete boot-contract gate on the hosted compiler configuration.
  - The integer version of the same control is refused.
- **F2 (MAJOR)**: the digest check on the download path, which is the path the hosted jobs take, has no test that can fail.
  - Deleting that check leaves all 16 installer tests green.
  - With it deleted, a well-formed archive that is not the pinned one is installed, its `relocate-sdk.sh` runs, and it gets a verified receipt.
- **F3 (MINOR)**: four claimed receipt bindings have no test that can fail: installer digest, host, symlinks, and compiler realpath containment.

Only the RTL lens is covered clean in this round.

## Findings

### R228-F1 MAJOR - Conformance, Robustness, Tests, Docs - the hosted compiler's FP stores bypass the resolver

**Artifacts**

- `sw/builder/test_builder.py:738`: `RV32_STORES = ("sw", "sh", "sb")`.
- `sw/builder/test_builder.py:1437-1482`: the store family. At `:1523-1526`, an unhandled mnemonic only clears its first operand.
- `sw/builder/test_builder.py:3675` and `:3833-3838`: the bare driver `()` is adopted first.
- `sw/builder/test_builder.py:3785-3797`: the arch check accepts any `rv32*` string.
- `sw/builder/test_builder.py:3975-3979`: the new `--require-rv32` adoption.
- `sw/builder/test_builder.py:13054`: the hosted verdict string ("EVERY OTHER STORE IS CLASSIFIED").
- `docs/testing/CI_WORKFLOWS.md:1050`.
- `docs/integration/BAREMETAL_FIRMWARE.md:431`, `:1173` and `:1262-1265`.

**Authority**

- Readiness comment 5771447690 on #504:
  - ILP32D "does not establish ABI/library or resolver compatibility";
  - "the real pristine/hostile gates ... must settle the choice".
- Selection decision 5771915061.
- The issue objective: "Do not treat any compiler that accepts `-march=rv32...` as sufficient".
- Acceptance items 2 and 5 (negative controls for unresolved stores).
- AGENTS.md section 6:
  - Tests: "do not merely reproduce implementation assumptions";
  - Robustness: "configuration-dependent behavior".

**Evidence**

- Hosted adoption. Both hosted jobs adopt `/home/runner/br-milan-rv32/host/bin/riscv32-linux-gcc` with `driver=()`:
  - docs-check: `hosted/docs-check-106851428580.log` lines 793 and 796;
  - elaborate: `hosted/elaborate-106851429374.log` line 720.
- Census ISA. Every census compile in my mapped runs declares `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0` (`receipts/gate1b/*-argv.jsonl`).
- Unit probe (`scripts/probe_fp_store.py`, `receipts/14-fp-store-resolver.json`). It uses the census flags `-std=gnu99 -O0 -fno-inline -S` and the same GCC 14.3.0.
  - SDK default ISA:
    - `*(volatile float *)(0x90000750u) = 1.0f` emits `fsw`, and the resolver reports no store;
    - `double` emits `fsd`, again with no store reported.
  - `-march=rv32ima_zicsr -mabi=ilp32` (the ISA and ABI class of the previously supported compiler):
    - the same source emits `sw`;
    - the resolver reports `0x90000750`, `0x90000614` and `0x90000618`.
- Whole-gate probe (`scripts/plant_fp_mutant.py` with `scripts/run_focused_gates.sh`).
  - It ran on scratch copies only, never on the review clone. The planted diffs are `receipts/gate1b/probe-*-planted.diff`.
  - The starting point is the existing resolver-only control "entity enabled by a struct-overlay store through a paged base" (`test_builder.py:10839-10846`, table at `:12610-12612`). That table states that no text rule answers these shapes.
  - I planted it first in the mutation table, changing only the member type:
    - `uint32_t` / `1u`: refused on `RESOLVER_STORE_PIN`. The rest of the gate stays green (`receipts/gate1b/probe-uint32.log`).
    - `float` / `1.0000001f`, bit pattern `0x3F800001`, which sets ADP_CTRL bit 0: `AssertionError: ... FLOAT struct-overlay store through a paged base mutation passed the boot-contract gate` (`receipts/gate1b/probe-float.log`).
    - `double` / `1.0000000000000002`, low word `0x00000001`: `... DOUBLE ... mutation passed the boot-contract gate` (`receipts/gate1b/probe-double.log`).
  - "Passed the boot-contract gate" is `assert_rejected` at `test_builder.py:9438`. It means `assert_boot_contract` accepted the firmware: every text rule, the immediate census and the resolver.

**Impact**

- This lane makes one compiler configuration authoritative. On that configuration, a firmware can enable the entity before AEM (Milan's entity model) verification by writing through a float- or double-typed overlay at a paged base, and every instrument and every text rule accepts it.
- The previously supported ILP32 soft-float compiler class would emit `sw` for the same source, which the resolver resolves and refuses.
- The published verdict and the firmware page say every emitted store is classified. The PR text calls the ILP32D default inconsequential. Neither statement holds for the census.
- This is not weaker than dev's hosted runs, because those ran no resolver at all.
- It does make the hosted instrument claims false for a whole class of stores. The #408/#409 lanes would retire text rules against exactly these hosted instruments.

**Required outcome**

- The hosted instruments must not silently drop any store class the adopted compiler can emit. Two routes would satisfy this:
  - drive the census at an ISA and ABI that emit no FP stores, with that selection evidenced on the real SDK;
  - or classify FP stores in the store census, plus any other store mnemonic the adopted ISA provides, with hostile controls compiled by the adopted compiler.
- Either route changes gate or selection behavior outside the assignment in comment 5778746031. The choice therefore needs a published scope decision first (AGENTS.md section 2).
- The authoritative docs must state the census ISA honestly. `CI_WORKFLOWS.md:1050` must not present the ILP32D default as irrelevant to the instruments.

**Verification**

- Rerun the float, double and uint32 probes (`plant_fp_mutant.py` with `run_focused_gates.sh`) at the fixed head. All three must be refused on a resolver or census reason.
- `probe_fp_store.py` must show either FP stores reported, or no FP stores emitted, at the census driver.
- The hostile tally must include the new controls.

### R228-F2 MAJOR - Tests, Conformance - the download-path digest check has no failing control

**Artifacts**

- `scripts/ci_rv32_sdk.py:125-127`: the digest check in `extract()`. It is the only authentication on the download path (`:158-166`).
- `scripts/ci_rv32_sdk.py:152-153`: the separate pre-check for `--archive`.
- `scripts/ci_rv32_sdk_selftest.py:91-95`: `test_bad_archive`, whose docstring says "A wrong download never reaches tar or creates an installation".

**Authority**

- Decision comment 5771915061: "Add failure-sensitive workflow/installer controls".
- AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".

**Evidence**

- `scripts/mutate_installer.py` (`receipts/12-installer-mutants.jsonl`): the mutant "extract: drop digest check (download path)" survived, with all 16 tests passing.
- The reason: `test_bad_archive` passes an explicit `--archive`, so the `install()` pre-check refuses it before `extract()` is reached. No test drives the download branch with wrong bytes.
- `scripts/probe_download_auth.py` (`receipts/13-download-auth.jsonl`) serves a well-formed archive that is not the pinned one, through a mocked download:
  - the exact head refuses it with `SDK archive digest mismatch` and creates no prefix;
  - with only that check deleted, the installer reports "INSTALLED AND VERIFIED", runs the unpinned `relocate-sdk.sh`, and writes a receipt.

**Impact**

- On hosted runners, this check is all that stands between an unauthenticated download and extraction followed by script execution.
- It can be removed or weakened while the self-test in the same CI step stays green.
- The test named for this case cannot fail for it.

**Required outcome**

- Add a control that calls `install()` without `--archive`, which is the hosted path.
- It supplies wrong but well-formed archive bytes and requires refusal before any tar extraction or relocation.
- It must fail when the `extract()` check is removed.

**Verification**

- `mutate_installer.py` reports that mutant as KILLED.
- `probe_download_auth.py` gives the same result as now for the exact-head installer.

### R228-F3 MINOR - Tests - claimed receipt bindings are not failure-sensitive

**Artifacts**

- `scripts/ci_rv32_sdk.py:50-55` (provenance), `:66-67` (symlink records) and `:79-81` (compiler realpath containment).
- `scripts/ci_rv32_sdk_selftest.py:129-138`: `test_wrong_provenance` iterates the implementation's own receipt keys. A field dropped from `provenance()` therefore also drops its own subtest.
- `docs/testing/CI_WORKFLOWS.md:1055-1060`, which says the caches "bind ... installer source bytes" and the receipt "binds ... symlinks".

**Evidence**

Four mutants survived in `receipts/12-installer-mutants.jsonl`, each with all 16 tests passing:

- "provenance: drop installer digest";
- "provenance: drop host";
- "inventory: drop symlinks";
- "identify: drop compiler realpath containment".

**Impact**

- The receipt properties the docs claim can regress without any test noticing.
- Symlink retargeting is the realistic form of cache drift here, because the compiler selector is itself a symlink.

**Required outcome**

Add three controls. Each must fail when its guard is removed:

- one that pins the expected provenance field set independently of the implementation's output;
- one that retargets an installed symlink;
- one that plants a compiler whose realpath escapes the prefix.

**Verification**

- The four mutants above are reported as KILLED.

### Suggestions (optional; they do not affect coverage)

- **R228-S1 (Tests)**: three more guards survived deletion with no test noticing (`receipts/12`):
  - the archive root check at `ci_rv32_sdk.py:131-133`, which the pinned digest makes unreachable today;
  - the special-file refusal at `:71-72`;
  - the exact receipt key set at `:109-110`.
- **R228-S2 (Robustness)**: relocation is proven only through `share/buildroot/sdk-location` and the sysroot the wrapper computes (`ci_rv32_sdk.py:95-99`).
  - With the `file` utility absent, `relocate-sdk.sh` skipped every text file. The installer still printed "SDK fresh installation: verified", while 377 text files still named the build prefix (`receipts/08-relocation-without-file.txt`).
  - This is not reachable on the hosted image or the full act image. The hosted logs contain no `command not found`, and `-E`/`-S` do not read the unrelocated files.
  - Scanning text files for the old prefix, or requiring `file` up front, would make the claim exact.
- **R228-S3 (Robustness)**: the download has a 120 s timeout per read, but no retry and no total deadline (`ci_rv32_sdk.py:162-165`). Neither job sets `timeout-minutes`.
  - A trickling mirror can hold two required contexts until the platform limit.
  - A transient network error fails them outright.
  - Bounded retries plus a total deadline would keep the behavior fail-closed.

### Out-of-scope observation (for a new Issue, not attributed to this PR)

- Atomic stores (`amoswap.w`, and `sc.w` by the same rule) are also outside `RV32_STORES`.
- They go unreported on both ISAs, ILP32D and ILP32 soft-float (`receipts/14`, function `amo_swap`). The gap is independent of the compiler and predates this lane.
- It should be tracked before #408/#409 retire anything onto the resolver.

## Reviewer-owned lens ledger

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #504 body and comments 5771447690, 5771915061, 5778746031. Acceptance items 1-5 checked against hosted runs 35758843423 and 35758843483 (official download, digest line, adoption line, 161+46 compiled vs 135+46 absent, 17/17 and 4/4 positives). Also `ci_rv32_sdk.py`, `test_builder.py:3975-3985` and both workflow diffs | R228-1 | 3d90958f3a82ca2a9617112c107a22f332117e17 |
| RTL | CLEAN | No path under `hdl/`, `tb/`, `syn/`, `sw/firmware/`, `sw/litex/` or `configs/` changes. All four gitlinks are identical at base and head (`receipts/17`). In both pristine gate 1b runs (mapped SDK and absent), 46 RTL mutation variants elaborated as the real top with scoped Verilator 5.050, and the RTL integration facts passed (`receipts/gate1b/pristine-*.log`, `receipts/15`). Final integrity of the clone and submodules passes (`receipts/18`) | R228-1 | 3d90958f3a82ca2a9617112c107a22f332117e17 |
| Robustness | UNCLEAN (F1) | Fresh install and cache hit (`receipts/03`, `04`, `05`). Interrupts at 2, 7, 10 and 12 s (`receipts/09`). Foreign, stale, tampered, special-file and symlink cache probes (`receipts/10`). Unsupported host under an i686 persona (`receipts/11`). Relocation remnants (`receipts/07`, `08`). Mode round trip: only 0644 and 0755 are installed, and no link is absolute or escapes the prefix (`receipts/06`) | R228-1 | 3d90958f3a82ca2a9617112c107a22f332117e17 |
| Tests | UNCLEAN (F1, F2, F3) | `ci_rv32_sdk_selftest.py`: 16 tests, 23 mutants, 15 killed and 8 survived (`receipts/12`). `test_firmware_compiler.py --selftest`. `ci_events.py --check` (1555 items) and `--selftest` (1198 arms). `check_baremetal_only.py --check` (0 findings) and `--selftest` (365 arms) (`receipts/static/`). Whole-gate float, double and uint32 probes (`receipts/gate1b/`) | R228-1 | 3d90958f3a82ca2a9617112c107a22f332117e17 |
| Docs | UNCLEAN (F1) | `docs/testing/CI_WORKFLOWS.md:1042-1101`. The `docs/integration/BAREMETAL_FIRMWARE.md` diff hunks, plus `:431`, `:1173` and `:1262-1265`. `check_em_dash.py --base 52711029`: 0 findings, 57 arms. The `#elaboration` anchor exists (`CI_WORKFLOWS.md:975`) | R228-1 | 3d90958f3a82ca2a9617112c107a22f332117e17 |

## Focused executions at this head (review clone, unmodified)

- **Mapped SDK gate 1b**: `test_firmware_compiler.py --sdk-destination <fresh prefix>`, run with scoped Verilator 5.050 (`receipts/gate1b/pristine-sdk.*`).
  - Exit 0 in 325 s.
  - 208/208 mutations rejected, 17/17 firmware and 4/4 Makefile positives, 46 RTL variants elaborated, 7/7 instrument-only shapes, 0 NOT RUN.
  - 212 actual firmware compilations.
  - 216 of 219 audit records mapped only `argv[0]`, and every argument tail was preserved.
- **Absent gate 1b**: `--absent` (`receipts/gate1b/pristine-absent.*`).
  - Exit 0 in 273 s.
  - 182/182 mutations rejected, the same positives and 46 RTL variants.
  - Exactly one NOT RUN, the compiled census.
  - 0 firmware compilations. All three cross candidates were hidden.
- **Installer**:
  - Fresh install: exit 0 in 13.27 s. Cache hit: exit 0 in 0.77 s. `--verify-only`: exit 0.
  - Identity: `riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`, target `riscv32-buildroot-linux-gnu`, realpath `bin/toolchain-wrapper`, sysroot inside the prefix.
  - Installer SHA256: `ffcc5433d97209b00cac5155c61bc464a43a60fec49bce0330d81279e1df7cb4`.
- **Archive**: 102597892 bytes, SHA256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`. The installer constant, decision comment 5771915061 and the upstream published `.sha256` all agree (`receipts/01`, `02`).

## Evidence index

- Everything is under `$REVIEW_OUT`.
- `MANIFEST.sha256` lists all 64 receipt, hosted-log and script files with their hashes.
- The scripts take their paths as arguments.
- The raw receipts contain local absolute paths, which must be neutralized before any public copy.

**Receipts**

- `receipts/03-fresh-install-receipt.json`: the installer's own provenance and inventory receipt for the fresh prefix.
- `receipts/06-inventory-summary.txt`:
  - 5007 entries: 4914 files and 93 links;
  - 0 absolute links and 0 links that escape the prefix;
  - 6 dangling `/proc`-style links inside the sysroot.
- `receipts/09` and `receipts/interrupt-logs/` (`scripts/probe_interrupt.sh`). Each interrupt left the prefix either absent or refused on rerun. The installer never repaired a tree, and no tool ran.
- `receipts/10-tamper-probes.jsonl` (`scripts/probe_tamper.py`):
  - refused before any tool ran: a flipped byte, a setuid bit, an extra file, a FIFO, a retargeted selector, a removed receipt, a foreign receipt, and a stale installer digest;
  - accepted: a consistently forged receipt. This is the trust boundary the docs state (`CI_WORKFLOWS.md:1063-1064`);
  - accepted: an extra empty directory, because directories carry no record.
- `receipts/11-unsupported-host.txt`: refused with `unsupported SDK host: Linux/i686`, and no prefix created.
- `receipts/18-final-clone-integrity.txt` (`scripts/verify_clone_integrity.py`):
  - the parent checkout: HEAD and tree as reviewed, 854 committed files, and index equal to HEAD with no hidden flags;
  - all 539 files in the three required submodules match their committed blob bytes and modes;
  - the pins: verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`, gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`;
  - every status output is empty.

**Hosted logs**

- `hosted/`: docs-check job 106851428580 (SHA256 `f5b2af03...`) and elaborate job 106851429374 (SHA256 `ec38664a...`).
- Both jobs checked out GitHub merge `c0b2b7cc067ece28e3124f94ccd9ee45c91b85e3`, which is this head merged into `483a133e`. They did not check out the source head alone.

## Prior public review findings on this PR

I read these only after the verdict and ledger above were written.

- **R227-1** (comment 5781198822) is POSITIVE at this head, with no findings. So there is no prior finding to retain or resolve.
- Its per-lens PASS lines do not reach the three open findings here:
  - Its seven killed installer mutants do not include deleting the download-path digest check (F2), or any of the F3 bindings.
  - Its compiled store probes and the hostile table use integer-typed stores (F1).
  - Its RTL note says ILP32D does not change the shipping CPU. That is true, but F1 concerns the census ISA, not the product CPU.
- Under AGENTS.md section 7, a lens is clean at a head only if no finding remains open under it. Conformance, Robustness, Tests and Docs therefore stay uncovered at this head until F1-F3 are fixed and re-reviewed at the new head. RTL is clean in both rounds.

## Real limits

- By instruction, I did not run any of these: the full builder; the parent, protocol-processor, gPTP or Yosys banks; act or Docker; or hardware.
  - Physical calibration was NOT RUN, and the field skips are not hardware proof.
- I measured the whole-gate FP escape with the adopted SDK only.
  - The claim that the previously supported compiler would refuse it is an inference. It rests on the unit-level `sw` emission plus the resolver refusing the integer control.
  - The workstation compiler was not executed.
- No hosted cache-hit run exists at this head.
  - Both jobs missed the cache, and elaborate saved the key (docs-check log line 4401, elaborate log line 1084).
  - The cache hit is proven locally only (`receipts/04`, `10`).
- My mapped compiled run points only the selector's `argv[0]` at a fresh prefix. It is local compatibility evidence. Hosted adoption comes from the hosted logs of the merge ref.
- I did not independently verify the manager's act replica (5781839077) or the complete required-context set (5781249025).
- Housekeeping, which touched no tracked content:
  - I fetched object `c0b2b7cc` into the review clone's object store. HEAD, the index and the worktree are unchanged and verified in `receipts/18`.
  - About 3.6 GB of disposable trees remain under `$REVIEW_OUT`: `sdk-fresh/`, `probe-interrupt-*/`, `probe-nofile/` and `scratch-{float,double,uint32}/`. They contain SDK binaries. My removal attempt was declined in this session. They must not be published and can be deleted.

## Pending manager duties

- Before any fix, publish a scope decision for F1: choose between changing the census ISA selection and extending the store class.
- After fixes, re-establish at the new head:
  - hosted required contexts, including a hosted cache-hit run;
  - the trusted act replica;
  - the internal review and this external review.
- Current-dev candidate validation at the merge turn (base 52711029, live dev 483a133e), then containment, then closing #504 as Closed/Done.
- Neutralize local paths in any published copy of these receipts, and delete the disposable trees listed above.

R228-1 FINISHED
