[R795] POSITIVE - exact head c687810b74b53b69c1fbdff7bfd0ec9da94eaa78

# R795-1: internal independent review of kebag-logic/tsn-c-stack PR #29 (issue #27)

- Head: `c687810b74b53b69c1fbdff7bfd0ec9da94eaa78`, tree `20c8786758807efef217f6db8dc97158a5fa8a95`. The isolated clone matched both before and after the probes (`receipts/clone-integrity.txt`).
- Base: `70936b77dc41981e192438388cd0aced69954f18`. One commit, eight files, +76/-7.
- Review start: PR #29 issuecomment-6719698220.
- Author evidence: kebag-logic/milan-fpga@d40afd2b2a9b03d685e1e97fb25680461db18a7c `review-evidence/tsn27-r1`. All 50 manifest entries match their published sha256 (`receipts/author-evidence-check.txt`).
- Verdict: **POSITIVE**. No BLOCKER, MAJOR, MINOR or RESIDUE is open. Three SUGGESTIONs are recorded. They do not affect the verdict.

## Reconstruction (in order)

1. **Contributor rules.** There is no AGENTS.md. `CONTRIBUTING.md` requires:
   - a one-line commit subject with no body or trailers;
   - neutral role labels;
   - a failing assertion and a runnable planted defect for each regression;
   - no lowering of the coverage ratchet.

   I also read `docs/VERIFICATION.md`, `docs/PORTING.md` (wire preconditions, lines 386-391), `docs/REQUIREMENTS.md` (ACMP-02), `docs/TESTS.md` and `docs/TRACEABILITY.md`.
2. **Issue #27.** I read the body and the two lane comments (TAKEN, REVIEW READY). No maintainer or manager comment changes the scope. The frozen acceptance has four items:
   - `validate.py` passes in the pinned CI environment;
   - the ratchet is regenerated there;
   - both plants are killed;
   - no `__lshrdi3` is left in the parent's split image (`nm`).

   The change list also asks for:
   - two 32-bit halves, bit-exact for widths 1 to 8;
   - test W1 with halves that differ in every crossing byte, every width, the byte-form oracle and an untouched byte past the field;
   - two plants, each killed by W1;
   - header-plant support in `scripts/mutation.py`.
3. **Delta.** `git diff 70936b77..c687810b` and the history. The commit has a one-line subject, no body and no trailers. The tree has no submodule gitlinks.
4. **Evidence.** The author's published receipts and scripts, and exact-head hosted CI:
   - run 42465283076 (push) and run 42465293588 (pull_request);
   - both `quality` and `bare-metal` jobs executed and succeeded on both runs;
   - the checkout step shows `HEAD is now at c687810`;
   - for the pull_request run I downloaded the `quality-evidence` and `rv32-evidence` artifacts and inspected them (`receipts/hosted/`).
5. **Prior public findings.** There were none before my pass. The PR has two review-start notices (R795-1, R796-1), no reviews and no inline comments. No earlier finding needs to be resolved or kept at this head.

## Acceptance items, checked independently

### (1) Bit-exact at every width; W1's design

- **Code.** `include/wire.h:38-47` writes the last byte first. Each step feeds the next byte of `high` into `low` with 32-bit shifts only. No 64-bit variable shift remains.
- **Equivalence harness.** `scripts/equiv.c` and `scripts/equiv.sh` compare the head function with the old byte form. Coverage:
  - widths 0 to 8, at four offsets, with guard bytes on both sides;
  - 12 special values, the 128 single-bit and inverted single-bit values, and pseudo-random values (2,000,000 hosted, 20,000 on RV32).

  Results, all rc 0 (`receipts/equiv/summary.txt`):
  - hosted gcc 16.2 and clang, at -O0, -O2, -Os and -O3, with UBSan set to halt on error;
  - RV32I and RV32IM run under `qemu-system-riscv32`, at -O0, -O2, -O3 and -Os.
- **W1** (`tests/test_acmp.cpp:2561-2580`):
  - five values, each fatally asserted to have halves that differ in every crossing byte;
  - widths 1 to 8, with the old byte form as oracle;
  - the field sits at offset 1 of a 0x5A-filled 10-byte buffer, and the whole buffer is compared. So the byte before and the byte past the field are both checked. No value contains 0x5A, so a guard byte can never look like a written one.
- **Head run.** W1 passes at the head (`receipts/hosted-head/`). The 8/8 hosted binaries pass.
- **Old implementation.** W1 also passes against the base `wire.h` (`receipts/escape/old-wire-with-w1/`). It checks behaviour, not this implementation.

### (2) Plants: odd widths only, killed by W1 alone, they replace the draft's plants, placed before the entity plants

- **Widths in use.** Every `wire_put_be` call in `src/`, `examples/` and `tests/` uses width 2, 4, 6 or 8 (repository grep).
- **Repository driver.** `mutation.py --select wire-put-be` at the head: `{"CAUGHT": 2, "ESCAPED": 0, "ERROR": 0}`. Both kills are on W1's needle (`receipts/mutation-select/`).
- **Hosted CI at the head.** 390/390 CAUGHT, both wire plants killed by W1 at `test_acmp.cpp:2577` (`results.json` in the quality artifact).
- **Escape probes.** Full hosted build and ctest per variant (`scripts/escape.sh`, `receipts/escape/`):
  - each plant with W1: only `acmp_tests` fails, and only on `Wire.W1PutBeWritesTheLowBytesMostSignificantFirst`;
  - each plant with W1 removed: 8/8 binaries pass, so the plant **escapes**. W1 is the only test that catches either plant;
  - the draft-style crossing defects (`high << 16`, `high` never shifted) with W1 removed: adp, acmp (aborted), maap and entity tests fail. So the replaced draft plants were already caught by other tests, as the author states (`receipts/escape/ctest-failure-summaries.txt`);
  - control: the head with W1 removed passes 8/8.
- **Placement.**
  - The plants are at registry indices 385-386, before the three generated-entity plants at 387-389.
  - The `entity_selftest.py` check `golden_planted_drift` passes as committed.
  - With the wire plants moved last it fails, so the placement is required (`receipts/order/`).
  - `docs/VERIFICATION.md:24`: 386 core plants plus four generated configuration plants, 390 in total. This matches both campaigns.

### (3) `scripts/mutation.py`: header plants and the new error path

- **Shared mapping.** `arm_module()` (`:36-37`) is now shared with `prepare()` (`:141`).
- **Header fallback.** At `:222-224`, if `src/<stem>.c` is missing, the driver builds `src/<arm module>.c`. The header plant also rebuilds the arm's test object (`:229-234`), as before.
- **Probes** (`scripts/mutation_errors.sh`, `receipts/mutation-errors/`):
  - head, wire plant with no `arm`: ERROR `unknown mutation arm: wire`, rc 1;
  - head, `acmp.h` header plant with arm `bogus`: ERROR `unknown mutation arm: bogus`, rc 1, `results.json` written;
  - base driver, both wire plants: ERROR `mutant build failed`. The fallback is what makes them runnable;
  - base driver, `acmp.h` plant with arm `bogus`: `KeyError: 'bogus'` escapes at `SOURCES[arm]` and no `results.json` is written. This confirms the PR's "instead of stopping the campaign".
- **Controls.** `mutation_selftest.py` (mutation-controls) passes at the head (`receipts/gates-small/`).

### (4) Coverage ratchet

- **Value.** `tests/coverage.ratchet:4` reads `include/wire.h lines 14/14 branches 2/2`. The ratchet is exact (`scripts/coverage.py:305-320`).
- **Pinned CI image (ubuntu-24.04, GoogleTest 1.14.0).** The hosted CI coverage log at the exact head measures exactly 14/14 and 2/2, and the coverage gate rc is 0.
- **Host compiler.** The author regenerated the ratchet with host gcc 16 and pinned GoogleTest, not inside the CI image. My host gcc 16 run gives the same figure (`receipts/coverage-host/`). The committed ratchet is therefore what the pinned environment produces.

### (5) The parent split image

The author's receipts are internally consistent:
- 1x1 with one interface: `00005200 T __lshrdi3` before, absent after.
- 8x8 with two interfaces: `0000547c T __lshrdi3` before, absent after.
- The full `nm` symbol diff is `__lshrdi3` removed and one more out-of-line `wire_put_be` copy (3 to 4). Nothing else changes.
- After the change, no compiler-runtime helper symbol remains.
- Text: 107278 to 106854 B (-424; `.text` 95064 to 94640) and 122106 to 121686 B (-420). These match the PR table.
- Without the parent's hot-list edit, the parent gate refuses the image. This is receipted, and the edit belongs to the parent's pin move.

Independent corroboration, with a different RV32 compiler (gcc 16.2) and the parent's flags (-Os, -ffunction-sections), on the three core objects (`receipts/objects/summary.txt`):
- base: 3 `R_RISCV_CALL __lshrdi3` relocations;
- head: 0 at rv32im and rv32i;
- -Os text: rv32im 17128 to 16888 B, rv32i 17232 to 16992 B;
- the stack's -O0 and -O3: 0 relocations both before and after.

### Both targets

- **Linux hosted.** Reviewer Debug build and ctest pass 8/8. Hosted `quality` passed all 28 gates at the head, including the clang-tidy 18 static analysis and the sanitizer build. Focused reviewer gates rc 0: comments, needles, traceability, test-inventory, privacy, licence and mutation-controls.
- **Bare-metal RV32.** Reviewer `baremetal.py` rc 0 on both base and head (`receipts/baremetal/`). Hosted `bare-metal` passed at the head.
  - Smoke text: Debug 47508 to 47428 B, Release 36857 to 37653 B. These match the author.
  - The head Release ELF is bit-identical to the author's (sha256 `cadc526c…`). The base Release ELF is bit-identical to the author's main receipt.
  - Core imports are unchanged between base and head.

## Recorded trade-off

The author records +796 B of text in this repository's Release (-O3) RV32 smoke image against the parent's size-optimized build.
- **Confirmed at -O3.** The core objects grow by +676 B at -O3 (25908 to 26584), matching the author's variant table.
- **Confirmed at -Os.** The same change saves 240 B at -Os and removes every `__lshrdi3` call.
- **Why I accept it.**
  - The issue targets the parent's -Os split image on a 32-bit core with a service-time bound.
  - This repository has no size budget gate for its smoke image.
  - The -O3 growth costs nothing at run time on the target.
  - The author measured an alternative (select a half per byte) and recorded it: size-neutral at -O3 but 92 B larger at the parent's -Os.

I accept the halves form as the issue prescribes it.

## Lens assessments

- **Conformance: CLEAN.**
  - Behaviour on the wire is unchanged: bit-exact on every width, on both compilers and on RV32. So IEEE 1722.1-2021 big-endian field order (the `wire.h` header reference) and every ACMP, ADP and MAAP PDU byte are unchanged.
  - W1 is traced to ACMP-02 (PDU build) in the generated `TESTS.md:162` and `TRACEABILITY.md:16`. The traceability and test-inventory gates pass.
  - The `PORTING.md:391` precondition (one to eight bytes) is unchanged and still accurate. So is `PORTING.md:388` ("one byte at a time").
- **RTL: CLEAN.**
  - The delta has no HDL. This lens examined the target code the parent's soft-core control hart runs:
    - RV32 helper calls in the core objects, before and after;
    - the parent image symbol lists;
    - the bare-metal imports in both configurations;
    - RV32 execution of the equivalence harness under QEMU at four optimization levels.
  - The parent hot-list coupling is identified and assigned to the parent pin move.
  - Timing on the soft core was not measured (see limits).
- **Robustness: CLEAN.**
  - The loop uses only `uint32_t` shifts, by 8 and 24, so it has no undefined shift. UBSan is clean on both compilers.
  - `bytes == 0` writes nothing, as before.
  - Widths above 8, outside the contract, now write leading zeros instead of the old undefined shift.
  - In the driver, an unknown arm becomes a per-plant ERROR instead of an uncaught `KeyError`.
  - The fallback fails safe for misregistered targets (S2).
- **Tests: CLEAN.**
  - W1 meets every clause the issue sets for it.
  - Both plants are killed by W1 alone and escape without it.
  - The draft's replaced plants are shown to be caught by other tests.
  - The ratchet is exact in the CI image.
  - The new driver error path is shown by reviewer probes but has no standing control (S1).
- **Docs: CLEAN.**
  - `VERIFICATION.md:24`: the plant count of 386 core plants (390 in total) is true.
  - `VERIFICATION.md:195`: the header-plant sentence matches the intent. Its scope is narrower than the code's (S2).
  - The generated docs were regenerated, and their gates pass.
  - Comment rule: the new source comments are `// REQ: ACMP-02` (`test_acmp.cpp:2561`) and one behaviour sentence (`mutation.py:221`). No bench lane label, lane name, review round, reviewer ID or issue-comment ID appears in the delta's source or docs. `W1` is the test-case ID in the existing `<letter><n>` test naming scheme, not a lane label.
  - The PR body's figures match the receipts, except the unreceipted call-site count (S3).

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R795-1-S1 | SUGGESTION | Tests, Robustness | `scripts/mutation.py:219-220`; `scripts/mutation_selftest.py:107-151` | CONTRIBUTING (regressions get a failing assertion); `mutation_selftest.py` already has an unknown-test ERROR control. The new unknown-arm ERROR path works (`receipts/mutation-errors/head-noarm`, `head-bogus`), but no standing gate exercises it. | If the check were removed, no gate would fail. A bad arm on a header plant would again crash the campaign. That still fails, but without a per-plant record. | Optional: add an "unknown arm" control to `campaign()` in `mutation_selftest.py`, giving a one-plant registry an arm outside `SOURCES` and expecting rc 1 with status ERROR. | mutation-controls rc 0 with the new control; rc 1 if the check is deleted. |
| R795-1-S2 | SUGGESTION | Robustness, Docs | `scripts/mutation.py:222-224`; `docs/VERIFICATION.md:195` | The fallback runs for any target whose `src/<stem>.c` is missing, not only headers as the comment and the docs say. Example: a plant in `examples/adp_port.c` with arm `port`. Such a plant would build unplanted `src/adp.c` and baseline `port_extra.o`. | It fails safe: the mutant is absent, so the result is ESCAPED and the gate fails. But a misregistered non-header plant would be reported as ESCAPED instead of the old ERROR `mutant build failed`. No such plant exists today. | Optional: apply the fallback only when `target.suffix == '.h'`, matching the comment and the docs. | Probe: a one-plant registry on a non-header non-`src` target reports ERROR. |
| R795-1-S3 | SUGGESTION | Docs, RTL | PR body and handoff: "defined, 7 call sites" in the 1x1 image | Only `nm` (definitions) is published. My -Os core-object relocation count (3) corroborates the stack's share, not the parent's 4 inlined sites. | None on acceptance, which is `nm` absence and is receipted. The figure is context, not a gate. | Optional: publish the `objdump -dr` call-site count for the before image beside the `nm` receipts. | The call-site receipt exists and matches 7. |

No finding is BLOCKER, MAJOR, MINOR or RESIDUE.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `include/wire.h`; `docs/PORTING.md:386-391`; `docs/REQUIREMENTS.md` ACMP-02; `docs/TESTS.md:162`; `docs/TRACEABILITY.md:16`; equivalence harness (hosted and RV32); traceability and test-inventory gates | R795-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| RTL | CLEAN | RV32 core objects before and after (`receipts/objects`); bare-metal ELFs and imports (`receipts/baremetal`); RV32 QEMU equivalence (`receipts/equiv`); author parent-image `nm`, size and hot-list receipts (hash-verified) | R795-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Robustness | CLEAN | `wire_put_be` shift widths, zero and over-contract widths, UBSan runs; `mutation.py` error paths at head and base (`receipts/mutation-errors`) | R795-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Tests | CLEAN | W1 source; hosted ctest; `--select wire-put-be` campaign; eight escape variants; plant-order control; hosted CI mutation results (390 CAUGHT); coverage ratchet (CI log and host run) | R795-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |
| Docs | CLEAN | `docs/VERIFICATION.md:24,195`; generated TESTS and TRACEABILITY rows; `CONTRIBUTING.md` commit rules; comment-rule scan of the delta; PR body figures against receipts | R795-1 | c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 |

## Real limits

- **Parent image not rebuilt.** I did not build the parent split image: full parent banks were not allowed. Acceptance item (5) rests on the author's hash-verified `nm` and size receipts, which are internally consistent. My own RV32 -Os core-object relocation counts corroborate it in part, using a different compiler from the parent's buildroot toolchain.
- **No full validation run of my own.** I did not run the full `validate.py`. Static analysis (clang-tidy 18), the sanitizer build, graphs and the full 390-plant campaign at this head come from exact-head hosted CI (executed, success). My own runs were focused: build and test, the two-plant campaign, escapes, controls, metadata gates, coverage with host gcc 16, and bare-metal.
- **Two environment-only reruns.** My first focused-gate and campaign attempt failed only because the pinned clang-18 was not on PATH. Both were rerun with the pinned Clang 18.1.3 and passed. The receipts hold the reruns (`receipts/tool-identity.txt`).
- **No timing measured.** I did not measure the service-time effect at 100 MHz on the parent's control hart.
- **No hardware.** Physical calibration was NOT RUN. No field skip is hardware proof.
- **No manager source bank** ran at this exact head. None is claimed or inferred.

## Pending manager duties

- **Merge-turn candidate.** Validate the current-dev merge candidate (builder and native banks; source base 70936b77, live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c) and link its receipts. The manager owns hosted and act acceptance.
- **Merge order with PR #28 (issue #26).** #28 also edits `tests/mutations.json`, `tests/test_acmp.cpp` (+214/-6), `tests/coverage.ratchet`, `docs/TESTS.md`, `docs/TRACEABILITY.md` and the `docs/VERIFICATION.md` plant count. Whichever PR merges second must merge main and then:
  - regenerate the TESTS and TRACEABILITY rows (W1's `#L2562` anchor will move);
  - regenerate the ratchet;
  - set the core-plant count to the combined total;
  - keep the three generated-entity plants last;
  - re-run the mutation and entity-controls gates.
- **Parent follow-up (milan-fpga).** Move `third_party/tsn-c-stack` to the merged commit. In the same commit, drop the `__lshrdi3` entry from `sw/firmware/ctrl/plat/ctrl_split.ld` and `plat/ctrl_split_hot.txt`: the parent refuses the image otherwise, as receipted. That pin move needs its own validation.
- **Suggestions.** Carry S1-S3 as optional follow-ups. None is required before merge.

## Packet

- `scripts/`: portable probe scripts. Set `REPO`, `PKT` and `TOOLS`. `wave.sh` runs independent jobs concurrently.
- `receipts/`: raw outputs. Host paths are redacted to `$REPO`, `$PKT`, `$TOOLS`, `$HOME` and `$SLOTS`.
- `MANIFEST.sha256`: every published receipt and script.

R795-1 FINISHED
