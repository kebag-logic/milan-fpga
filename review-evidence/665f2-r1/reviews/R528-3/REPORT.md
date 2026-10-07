[R528] NEGATIVE - exact head 8b78a8fd36864246336c71c061ac4f21d629952f

# R528-3: internal cleared-context delta review of PR #687 (issue #665, lane F2), merge round

- Head `8b78a8fd36864246336c71c061ac4f21d629952f`, tree `ee59c5cb2b3adc55d3907eac24f9a5e27466b6c8`
  (`refs/pull/687/head` and `refs/heads/665-f2-maap` both read this SHA).
- Delta under review: `938497af1dffd8a87edebf3ab93663914bf85e5e..8b78a8fd`. It is the `--no-ff` merge
  `5901ab08` of dev `910f338dbd050f4efd2d96991ddcf928a583d55f` (#673, #679), then `a71b8c80` (link-bounce
  test, control and README) and `8b78a8fd` (debug-only `assert.h`).
- Scope sources: AGENTS.md, CONTRIBUTING.md, the #665 body, the F2 assignment 6026720272, the round-3
  assignment 6029938743, the executor's REVIEW READY 6030259747, and the PR body at this head. Also the
  author packet `review-evidence/665f2-r1/author-r3/` at `0b965bbd` (HANDOFF.md sha256 `be58cdf1...a980`,
  which matches the posted digest).
- Prior findings (R528-2 6029935831, R529-2 6029833929) were read only after my own pass.

## Verdict

One MINOR remains open under Docs: after the merge, the MAAP README's gate command still sets
`CTRL_RV32_CC`, which the merged harness no longer reads.

Everything else in the delta checks out:

- The merge resolution keeps both sides. All three conflicted files resolve to dev's #679 code plus
  F2's additions.
- R528-2-S1 is pinned by the new link-bounce test, and its named control is caught.
- The arm count is corrected.
- 8b78a8fd leaves the release object byte-identical and keeps the debug assertion's meaning.

Conformance, RTL, Robustness and Tests are clean at this head. Docs is unclean while R528-3-F1 is
open, so the verdict is NEGATIVE.

## Findings

### R528-3-F1 MINOR - Docs

- Where: `sw/firmware/ctrl/maap/README.md:155`, from `1a5d70fa`:

  ```sh
  CTRL_RV32_CC=riscv64-elf-gcc python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
  ```

- Evidence:
  - At `938497af`, `ctrl_arms.py:190` read `CTRL_RV32_CC`.
  - The merge took #679's side. `ctrl_arms.py:187-189` now calls `fw_rv32.compiler()`, which reads
    only `MILAN_RV32_CC` (`sw/firmware/gtest/fw_rv32.py:31`).
  - The `compiler` probe (`receipts/r528_3_probes.log`) shows the effect.
    `CTRL_RV32_CC=riscv64-elf-gcc` still selects the SDK's `riscv32-linux-gcc`.
    `MILAN_RV32_CC=riscv64-elf-gcc` selects `riscv64-elf-gcc`.
  - In this same delta, `a71b8c80` removed the matching `CTRL_RV32_CC` paragraph from
    `sw/firmware/ctrl/README.md`. The PR body and HANDOFF Round 3 both name `MILAN_RV32_CC`. Only
    the lane's own MAAP README was left behind.
- Impact:
  - The MAAP page's documented gate silently ignores its compiler selection. It runs with whichever
    candidate is found first, not the compiler it names, and gives no error.
  - A reader reproducing the evidence gets objects from a different compiler than the page states.
  - This is a changed interface name inside an executable instruction, not prose wording. So it is
    MINOR, not RESIDUE.
- Required outcome:
  - The command names the variable the harness reads (`MILAN_RV32_CC=...`). Or it drops the prefix,
    so the pinned SDK is used as the PR body describes.
  - No other current page names `CTRL_RV32_CC`. The historical Round 1/2 HANDOFF sections may keep
    it as history.
- Verification:
  - `grep -rn CTRL_RV32_CC sw docs scripts` finds nothing.
  - `scripts/r528_3_probes.py CLONE SCRATCH compiler` shows that the documented variable selects the
    named compiler.
  - The docs gates stay at rc 0.

### R528-3-S1 SUGGESTION - Docs

- Where: `sw/firmware/ctrl/maap/README.md:144-145` and `sw/firmware/gtest/rv32_include/`.
- Evidence: the `h1-no-ndebug` probe drops `-DNDEBUG` from the RV32 flags. `maap.c` then fails to
  build for RV32I, because the isolated freestanding header set declares no `assert.h`. The README
  already limits RV32 validation to `-DNDEBUG` objects, so nothing it claims is false.
- Suggested outcome (optional): add one sentence saying that a debug target build must take
  `assert.h` (and `__assert_fail` or an equivalent) from the product runtime, because `rv32_include`
  does not supply it.

## Prior findings at this head

| Finding | Status | Evidence at 8b78a8fd |
|---|---|---|
| R528-2-S1 SUGGESTION (Tests): `r2-saved-range-never-consumed` escaped | RESOLVED | `test_maap.cpp:330-351` adds `MaapCore.LinkBounceDrawsAfterSuppliedRange`. It runs Begin! with `kBase` while down, then: up (one PROBE for `kBase`); down (INITIAL, timer stopped, no frame); up (PROBE state, timer running, base != `kBase`, in pool, a second PROBE for the drawn base). `maap_mutants.py:28-31` adds the exact control. That control is caught by its named assertion in the campaign (shard 0) and in my replay `p9`. My own variant `p8` (a bounce re-probes the previous base) is caught by the same assertion. |
| R528-2-R1 RESIDUE (Docs): "The seven arms" | RESOLVED | `sw/firmware/ctrl/README.md:25` now reads "The ten arms (and the optional `lwsrp` arm)". The arm list at `test_ctrl_firmware.py:124-127` has exactly ten arms: model, port, adp, unit, walk, entity, rv32, maap, maap_debug and maap_if2. |
| R529-2 | no findings | R529-2 recorded no open finding, so there is nothing to carry. |

## Merge-resolution analysis (assignment item 1)

Conflicts and resolution:

- `git merge-tree --write-tree 938497af 910f338d` conflicts in exactly the three named files.
- The recorded merge `5901ab08` differs from the automatic merge tree `a6311bbe` only in those three
  files' conflict hunks. No other file carries a hidden change.
- Each hunk resolves to dev's #679 side, with F2's `-DNDEBUG` kept in `RV32_FLAGS`:
  - `ctrl_arms.py`: the compiler comes from `fw_rv32.compiler()`.
  - `ctrl_build.py`: `RV32_CANDIDATES` is gone and the `-fstack-usage` flags are in.
  - `test_ctrl_firmware.py`: the docstring takes dev's wording.

Both sides are kept:

- `git diff 910f338d 8b78a8fd` over the three files shows only F2 additions:
  - the `arm_maap`, `arm_maap_debug` and `arm_maap_if2` arms;
  - the MAAP sources in `PORTABLE` and the `maap` include directory;
  - host `-DNDEBUG`, `Build(jobs=4)` and `--mutation-shard`.
- #679's parts are all present at head:
  - isolated headers (`fw_rv32.includes`);
  - ELF class, ABI and ISA findings;
  - the static-frame report;
  - `--extern-only --defined-only` resolution;
  - the exact helper allowlist.

Planted-defect catalog (`scripts/catalog_compare.py`, `receipts/catalog_compare.txt`):

- 192 controls at `938497af` and 193 at head.
- None was removed or changed. The one addition is `r2-saved-range-never-consumed`.
- Named obligations go from 197 to 198.

Re-grading:

- One check's meaning did change: the `rv32` arm now applies #679's stricter criteria. These are exact
  helpers instead of any `__` prefix, extern-only resolution, and the ABI and frame checks.
- This is dev's reviewed change, adopted unchanged. It is stricter, and the MAAP objects pass it at
  head.
- F2's only `rv32` control, `pool-falls-back-to-heap`, keeps its needle. The new code still prints that
  needle (`symbols outside the C library and libgcc`). No control's expected grade changed.

RTL:

- `git diff 938497af 8b78a8fd -- hdl` is byte-identical to `git diff 6714181d 910f338d -- hdl`, which
  is dev's own `KL_aaf_packetizer.sv` change.
- Since the FC round-2 head `db9aa8c9`, that file is the only hdl change. F2 adds no RTL.

## 8b78a8fd keeps the assertion's meaning

Object comparison (`receipts/maap_assert_object_equivalence.txt`): host gcc 16.2.1, `maap.c` at
`a71b8c80` against the head.

- Release (`-DNDEBUG`): the disassembly is byte-identical (sha256 `1d51ecb5...`). `maap.c` uses no other
  identifier from `assert.h` (no `static_assert`).
- Debug: the only differences are the `__LINE__` operand (15 -> 18, from the two added guard lines) and
  the file string. The reentry assertion is still compiled and still fires.

Plants, each in a copy of the tree (`receipts/r528_3_probes*.log`):

- `p1` (include left unguarded): refused by `rv32` with `maap.c does not build for RV32I`. This is the
  integration defect 8b78a8fd fixes.
- `p2` (8b78a8fd reverted): refused the same way. The host arms pass.
- `p3` (assertion moved to release only): `MaapDebug.SynchronousExpiryAsserts` fails, and the release
  arms fail to compile. My first run expected the release arms to pass, which was a probe-design
  error; the rerun corrects it.
- `p4` (assertion removed): `maap_debug` fails by name.

The repository controls `maap-debug-no-assert` and `maap-reentry-not-counted` are also caught in the
campaign.

## Lens evidence (all five applied at this head)

```text
[R528] PASS Conformance - sw/firmware/ctrl/maap/maap.c:106-110,182-247; test_maap.cpp:330-351 - A link bounce after a consumed Begin! range draws a fresh range per Table B.7 (Restart!/PortOperational!). Note a permits reuse but does not require it, so the pinned draw is a local contract (maap.h:49,77-80; README:29-31) and conforms. 8b78a8fd changes no wire, state or timer behaviour: the release object is identical. Annex B behaviour is otherwise unchanged since R528-2 (maap.c release code identical).
[R528] PASS RTL - git diff 938497af..8b78a8fd -- hdl == git diff 6714181d..910f338d -- hdl (dev's KL_aaf_packetizer.sv only); db9aa8c9..8b78a8fd -- hdl is that one file - F2 makes no RTL, register or interface change. The firmware/host interface passes #679's stricter object checks with the SDK and with riscv64-elf-gcc: RV32I/ILP32, 12 objects, text 19280, data 0, bss 170, largest static frame 112 B. With the pinned 5.050 simulator, the mailbox suite passes on both adapters, at two interfaces and in co-sim, and 5/5 RTL controls are caught.
[R528] PASS Robustness - maap.c:13-24 (enter), test_maap.cpp:330-351 - Release reentry is still counted and refused (maap-reentry-not-counted caught). Down/up/down/up stops the timer and sends nothing while down, then restarts cleanly. A merge-era stray runtime dependency in any MAAP object is refused by name: p5 memmove (maap.c), p6 malloc (maap_mbx.c) and p7 puts (maap_csr.c) each fail rv32.
[R528] PASS Tests - receipts/ctrl_selftest_shard*of3.log and others - The ctrl campaign catches 193/193 in three shards. Positive arms: maap 37+12, maap_if2 13, maap_debug 1, rv32 PASS. fw_rv32_selftest 17/17. Differential 12/12 with 16/16 controls. Coverage: 17 files at 100 % (maap.c 209/209 lines, 140/140 branches), selftest 28/28. Saved-state: 434 tests across 5 shapes. The catalog is unchanged plus one control. My plants p1-p9 and h1 behave as expected; the new test fails for the defect it names and for my independent variant p8.
[R528] UNCLEAN Docs - sw/firmware/ctrl/maap/README.md:155 - R528-3-F1 (MINOR) is open. Otherwise: ctrl/README.md:25 and :121-127 match the harness. The gtest/README.md RV32 section is dev's. The PR body's round-3 figures match my measurements: 193 controls, 16 differential controls, 37/12/13/1/12 = 75 cases, 112 B frame, 19280/0/170 sizes, H-MAAP path unchanged. Docs gates rc 0 (receipts/docs_gates.log).
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `maap.c` bounce and Begin paths; `test_maap.cpp:330-351`; Table B.7 and note a; release object equivalence. The unchanged F2 Annex B scope was covered by R528-2 at `938497af`. | R528-3 (delta); R528-2 (unchanged F2 scope) | `8b78a8fd36864246336c71c061ac4f21d629952f` (R528-2: `938497af1dffd8a87edebf3ab93663914bf85e5e`; release code identical since) |
| RTL | CLEAN | hdl delta identity against dev; RV32 object and ABI checks with two compilers; mailbox suite. F2's RTL scope is untouched since R528-2. | R528-3; R528-2 (F2 RTL scope) | `8b78a8fd36864246336c71c061ac4f21d629952f` (R528-2: `938497af...`) |
| Robustness | CLEAN | `enter()` reentry in release and debug; the bounce sequence; stray-dependency plants p5-p7 | R528-3 | `8b78a8fd36864246336c71c061ac4f21d629952f` |
| Tests | CLEAN | full ctrl campaign (193); RV32 self-test; differential; coverage; saved-state; catalog diff; plants p1-p9 and h1 | R528-3 | `8b78a8fd36864246336c71c061ac4f21d629952f` |
| Docs | UNCLEAN | `maap/README.md:155` (R528-3-F1); `ctrl/README.md`; `gtest/README.md`; PR body; HANDOFF Round 3; docs gates | R528-3 | `8b78a8fd36864246336c71c061ac4f21d629952f` |

## Commands and receipts

Every command ran in the foreground, or detached with its own log and rc file, with at most 16 jobs.

| Command | rc | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard I 3`, for I = 0, 1, 2 | 0, 0, 0 | 65 + 64 + 64 = 193 caught; the union is 193 distinct controls (`ctrl_selftest_shard*of3.log`) |
| `fw_rv32_selftest.py --require-rv32` | 0 | 17 checks PASS |
| `scripts/r528_3_probes.py` (13 probes) | 1 | 11 as expected. `p3` and `p6` were probe-design errors: `p3` had a mis-stated expected outcome, and `p6` did not build because of `-Wunused-result`. |
| `scripts/r528_3_probes.py ... p3 p6` (corrected) | 0 | 2 of 2 as expected |
| `fw_coverage.py --check --jobs 4` and `--selftest` | 0, 0 | 17 files at 100 %; 28 of 28 |
| `make -C tb/verilator/mbx -j1 VBUILD_JOBS=6 VERILATOR=<pinned 5.050>` | 0 | Wishbone 316, AXI 361, co-sim 13; two-interface 316, 361 and 316; mutants 5 of 5 |
| `maap_differential.py --self-test` (pinned 5.050) | 0 | 12 of 12 at baseline; 16 of 16 controls (`differential.log.gz`) |
| `test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 434 tests across 5 shapes |
| Docs gates in the hash-locked renderer environment: `docs_check.py`; `gen_toc.py --selftest`, `--verify-anchors` and `--check`; `check_em_dash.py --base 938497af`, `--base 910f338d` and `--selftest` | all 0 | `docs_gates.log` |
| Hosted check runs at the exact head, read at 2026-10-07T03:42Z | n/a | `hosted_checks_8b78a8fd.tsv`. 14 succeeded, including `firmware-unit`, `rtl-fast` and all Yosys shards. 6 were still running: Verilator shards 0, 1, 2 and 4, `docs-check` and `elaborate`. 1 was skipped (`Physical gPTP`); a skipped context is not executed evidence. |

Restoration (`receipts/integrity_before.txt` and `integrity_after.txt`):

- HEAD, the tree, the `ls-files -s` digest and the `ls-tree -r` digest are identical before and after.
- 1161 tracked non-gitlink files: 0 blob mismatches and 0 mode mismatches.
- Worktree and index match HEAD, with no untracked or ignored leftovers.
- All four gitlinks are unchanged. `external` is not initialized, as it was at the start.

For public hygiene, home-directory prefixes in two receipts were rewritten to `~`. No other receipt
was edited.

## Real limits

- This is a source review. No hardware was used, and physical calibration was NOT RUN. Field and
  physical skips are not hardware proof.
- I did not run the full builder bank; the parent, PP, gPTP or Yosys banks; `act`; or any hosted job.
  For those I rely on the manager's published source and native bank results.
- `tally_selftest.py --mutants` and the AAF startup gate were not re-run. This lane changed none of
  their inputs, and the AAF gate is dev's own content.
- My mutation campaign used three shards where the author's used four. Either way, the union is the
  complete 193-control catalog.
- Host-model H-MAAP times are model figures, not target timing.

## Pending manager duties

- Carry R528-3-F1 back to the executor. The fix is one token at `maap/README.md:155`, and Docs then
  needs a re-review at the new head. The other lenses stay banked only if nothing else in their scope
  changes.
- R528-3-S1 is optional.
- At read time, hosted Verilator shards 0, 1, 2 and 4, `docs-check` and `elaborate` were still running.
- The manager still owns:
  - hosted and `act` acceptance;
  - the later trivial dev merge after FC #685 lands;
  - candidate-merge validation;
  - post-merge containment.

R528-3 FINISHED
