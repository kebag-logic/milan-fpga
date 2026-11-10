[A759] Round 2: pin the multi-word owed-release mask with named assertions at the word boundary and on slot reuse, and refuse sink counts that probe_of cannot name

Closes #31

## Round 2

This round answers the round 2 ruling, items 1 to 3, on the two round 1 reviews (R811-1 F1 = R812-1 F1). Head `97414fe6518cda2bf7c4ea136fdd8bd25c860d83`, three commits on round 1's `c6013804`. The only core lines changed are S1 (`src/acmp.c:37`) and S2 (`src/acmp.c:312`). No public function, callback, configuration, view, counter or field changes, and the RV32 object code equals round 1's.

### What

- **Word boundary, 33 sinks.** `AcmpWide.SinksThirtyOneAndThirtyTwoWaitOnlyForTheirOwnResponses` (`tests/test_acmp_wide.cpp:140`) binds sink 31, the last bit of word 0, and sink 32, the first of word 1, with no transmit room (ACMP-09, Milan v1.2 5.5.3.5).
  - Each sink waits behind one owed response, its own, and no other sink is held.
  - Sink 31's response leaving releases sink 31 alone.
  - Sink 31's UNBIND_RX response is then owed behind sink 32's frames. Sink 32's response leaving releases sink 32 alone while sink 31 still waits, and sink 31's unbind response then releases it.
- **Slot reuse.** A probe owed in the slot that held another sink's response must hold no sink. Each test asserts that sink 3's probe lies in that slot. It then checks that only sinks 1 to 3 wait, that the old sink's next change (`acmp_set_started`) is reported at once, and that no sink is held after the drain.
  - At 33 sinks, for each mask word: `AcmpWide.ProbeInTheSlotOfSinkThirtyOnesResponseHoldsNoSink` (word 0, `:170`) and `AcmpWide.ProbeInTheSlotOfSinkThirtyTwosResponseHoldsNoSink` (word 1, `:185`).
  - At the default 16 sinks, where the stale-bit defect is live: `AcmpCore.A19AProbeInTheSlotOfAnEarlierResponseHoldsNoSink` (`tests/test_acmp.cpp:1159`), with the entity built with all 16 sinks.
- **Five new plants**, the five defects R811-1 found surviving, each with named needles in `tests/mutations.json`:

  | Plant | Change | Killer |
  |---|---|---|
  | `acmp-wide-release-word-off-by-one` | `transmit` writes word `release / 32u` | the word-boundary test |
  | `acmp-wide-owed-count-word-off-by-one` | the change-owed loop reads word `(k + 1u) / 32u` | the word-boundary test; the word-0 slot test (sink 31's count wraps to 255) |
  | `acmp-wide-release-loop-word-off-by-one` | the release loop reads word `(k + 1u) / 32u` | the word-boundary test; the word-0 slot test |
  | `acmp-owed-release-not-cleared` | the clear of the stored mask is deleted | the 16-sink slot test and both 33-sink slot tests |
  | `acmp-wide-release-clears-one-word` | the clear covers word 0 only | the word-1 slot test |

  - With its killers filtered out, each plant passes every other test of `acmp_tests` and `acmp_wide`. With only its killers, each fails with every registered needle in the output. `acmp-wide-release-word-ignored` follows S2's text with the same defect.
  - `docs/VERIFICATION.md` counts 448 core plants, and `docs/TESTS.md` and `docs/TRACEABILITY.md` are regenerated: 181 declarations, 452 plants. ACMP-09 names the four new tests.
- **S1.** `src/acmp.c:37` refuses a build of more than 255 sinks: `probe_of` stores one plus the sink index in a `uint8_t`, so 255 sinks is the exact bound. The [owed bound](docs/PORTING.md#acmp-owed-bound) says so.
- **S2.** `src/acmp.c:312` shifts `UINT32_C(1)` into the mask word.
- **The refusal's compile control.** The `conditionals` gate's selftest (`scripts/check_conditionals.py:141`) compiles the ACMP core with gcc and with clang.
  - The committed storage compiles at 33 and 255 sinks and is refused at 256, by "the owed probe_of names one plus the index of every sink".
  - With `ACMP_RELEASE_WORDS` planted to one word, it compiles at 32 and is refused at 33, by "the owed release mask holds a bit for every sink".
  - Each refusal must name its own assertion. With either assertion removed, the gate fails.
- **R812-1 S1** (increment the released sink directly in `transmit`) was measured and not taken. At `-Os` it would not grow (10,921 to 10,861 B; −60 B at `-O2`, −1,232 B at `-O3`). It was not taken for two reasons:
  - It deletes the change-owed loop, the target of a plant this round registers.
  - The hold and the release would no longer read the same stored bits. With the clear deleted, the variant never holds the stale sink, but when the probe leaves it wraps that sink's count from 0 to 255, and every later change of the sink would be held. The head's paired loops instead hold the stale sink only while that probe is owed, and the new tests catch that at once.
- **Residue.** The size tables name their compiler and flags. The 33-sink command in `docs/VERIFICATION.md` names both build directories.

### How to validate

```sh
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
```

The new tests and plants alone:

```sh
ctest --test-dir build-validation/gcc -R 'acmp_tests|acmp_wide' --output-on-failure
python3 scripts/mutation.py --work build-mutations --jobs 16 --select acmp-wide
python3 scripts/mutation.py --work build-mutations --jobs 16 --select acmp-owed-release-not-cleared
python3 scripts/check_conditionals.py --selftest --work build-conditionals --jobs 16
```

### Results at the head

On a clean clone of `97414fe6518cda2bf7c4ea136fdd8bd25c860d83`, the two `run:` steps of `.github/workflows/quality.yml` that test, run concurrently with `--jobs 16`:

| Step | rc | Result |
|---|---:|---|
| `python3 scripts/validate.py --work build-validation --jobs 16 --graphs` | 0 | 28 of 28 gates rc 0. Mutation: 452 caught, 0 escaped, 0 error. Coverage 100 % of lines and branches after the exclusions: `src/acmp.c` 815/815 lines, 426/426 branches. All 9 CTest binaries pass in the GCC and the sanitizer builds |
| `python3 scripts/baremetal.py --work build-rv32 --jobs 16` | 0 | Debug and Release rc 0 with the QEMU smoke run; the core imports are those of round 1 and `main` |

The clone's status and diff were empty before and after. The install steps were not run: GoogleTest and GMock 1.14.0, Clang 18.1.3 for the lexing gates, clang-tidy 18.1.3 and Mermaid CLI 11.16.0 were pinned, and the host's GCC 16.2.1, Clang 23.1.4, cppcheck, CMake, RISC-V GCC 16.2.0 and QEMU supplied the rest.

Both reviewers' scripts were run unchanged at the head:

- R811-1's `survivors_full_ctest.sh`: each of the five former survivors now fails the full 9-binary CTest, and the unplanted control passes.
- R812-1's disposable 33-sink test: it passes unplanted, and its three plants fail.
- R811-1's `plants.py` stops at its own check that each plant applies once, at `review-transmit-unbounded-shift`. That plant's text, `= 1u << ((release - 1u) % 32u);`, is the shift S2 rewrites.
  - The plant outcomes it had produced are kept.
  - A copy whose only change is that plant's anchor, now `UINT32_C(1) <<` with the same defect, runs to the end. Every one of its eight review plants fails `acmp_wide`, and the unplanted row passes.

### Size

Text of `src/acmp.c` for RV32I (riscv64-elf-gcc 16.2.0, `-march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -std=c11 -DNDEBUG -DCTRL_REENTRY_ASSERT`) at the default 16 sinks:

| Flags | `main` | Round 1 | This head |
|---|---:|---:|---:|
| `-Os` | 10,825 B | 10,921 B | 10,921 B |
| `-O2` | 16,029 B | 16,141 B | 16,141 B |
| `-O3` | 19,365 B | 20,365 B | 20,365 B |

The disassembly equals round 1's at each level. The `scripts/baremetal.py` Release image is byte-identical to round 1's: 51,480 B, with text 41,645 B, data 0 and bss 65,552 B. The Debug image's loaded sections are equal too, text 51,964 B, data 0 and bss 65,552 B.

## Round 1 ([A752d]): Size the ACMP owed-release mask from ACMP_MAX_SINKS

### What

`struct acmp_owed` kept its owed-release mask in one `uint32_t` (`include/acmp.h:401` at `main` `ea4af6f`), but `ACMP_MAX_SINKS` may be set above 32.
At 33 sinks, `respond`'s `1u << k` (`src/acmp.c:844`, `:899`) and the change-owed and release loops' `(release >> k) & 1u` (`:311`, `:1263`) shift by 32, which C11 leaves undefined (6.5.7p3).
On RV32 and x86 the shift uses the count's low five bits, so sink 32 and sink 0 share one bit, and each sink's change notice waits behind the other's owed response, against ACMP-09 and Milan v1.2 5.5.

- `acmp_owed.release` is now `uint32_t release[ACMP_RELEASE_WORDS]`, with `ACMP_RELEASE_WORDS` defined as `(ACMP_MAX_SINKS + 31u) / 32u` (`include/acmp.h:165`, `:402`). Bit s % 32 of word s / 32 is sink s.
  At up to 32 sinks the mask is one word, as before, so the owed set stays eight frames of 80 bytes, 640 bytes, on both targets. Each further 32 sinks add 4 bytes to every frame.
- `respond` and `transmit` now take one plus the index of the sink whose change the frame releases, or zero for none, as `probe_of` already names a probe's sink (`src/acmp.c:296`, `:323`). `transmit` sets that sink's bit in the stored mask (`:309-312`). `bind_response` and `unbind` pass `k + 1u` where they passed `1u << k` (`:850`, `:905`).
- The change-owed loop in `transmit` and the release loop in `acmp_poll` read word `k / 32u`, bit `k % 32u` (`:317`, `:1269`). No shift reaches the word width.
- `src/acmp.c:35` refuses at build time a mask that cannot hold one bit for each of `ACMP_MAX_SINKS` sinks: a `_Static_assert` on the field's size.
  The array grows with `ACMP_MAX_SINKS`, so the type as committed holds every count. The refusal fires when the field is narrower than the count: the old one-word mask, planted back at 33 sinks, fails with "the owed release mask holds a bit for every sink", and compiles at 32.
- No public function, callback, configuration, view or counter changes. `acmp_owed` is core-owned storage, listed in [ACMP machine storage](docs/PORTING.md#acmp-machine-storage). Its `release` row and the [owed bound](docs/PORTING.md#acmp-owed-bound)'s size paragraph are updated, and the paragraph keeps its pinned phrase.

### Tests and plants

- A new binary, `acmp_wide` (`tests/test_acmp_wide.cpp`; CMake target `tsn_wide`), builds the ACMP core and its test with `ACMP_MAX_SINKS=33u`, under `-fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined`. The mutation driver's new `acmp_wide` arm uses the same definition and flags (`scripts/mutation.py:26`).
  Each test configures 33 sinks on two interfaces and binds with no transmit room:
  - `AcmpWide.OwedResponsesHoldOnlyTheirOwnSinksChanges` binds sink 32, then sink 0. Each sink must wait behind one owed response, its own. The first poll's response then releases sink 32's change alone, the probe after it releases none, and sink 0's response releases sink 0's.
  - `AcmpWide.SinkZerosOwedResponseLeavesSinkThirtyTwoFree` binds sink 0. That must hold sink 0 and not sink 32, and its acceptance must leave sink 32's count at zero.
  - The binary's fixture asserts that it was built at 33 sinks. The conditional gate compiles every test file at the default 16, so the check is a runtime one.
- Against `main`'s `src/acmp.c` the new test stops at the first shift: `src/acmp.c:844:31: runtime error: shift exponent 32 is too large for 32-bit type 'unsigned int'`. Built to recover, both tests fail on the alias, sink 0 held by sink 32's response and sink 32 by sink 0's.
- Three new plants, each putting a sink's bit in word 0, each caught by its named assertion in the 33-sink arm: `acmp-wide-release-word-ignored`, `acmp-wide-owed-count-word-ignored` and `acmp-wide-release-loop-word-ignored`. Each passes all 126 tests of the 16-sink `acmp_tests`, so only the new binary detects it.
  They sit before the wire and entity plants, because `entity_selftest.py` reads the last three entries as the entity plants.
- Seven existing plants follow the lines they plant into, with the same defect: `acmp-unbind-echoes-the-talker`, `acmp-unbind-srp-after-response`, `acmp-unbind-change-before-response` and `owed-bind-answer-lost-after-decline` (the call's `k + 1u`); `acmp-change-not-held-for-its-response` and `acmp-first-owed-releases-every-change` (the two loops); and `owed-entry-widened` (the field, `uint64_t release[ACMP_RELEASE_WORDS]`, still caught by the 80-byte entry).
- `docs/TESTS.md` and `docs/TRACEABILITY.md` were regenerated by `test_inventory.py --write` and `traceability.py --write`; ACMP-09 names the two tests. `docs/VERIFICATION.md` counts 443 core plants and lists the 33-sink binary.

### Validation

On a clean clone of the head `c6013804d0fec6bc763a64b496f1a52d4a5d9f6a`, the two `run:` steps of `.github/workflows/quality.yml` that test:

| Step | rc | Result |
|---|---:|---|
| `python3 scripts/validate.py --work build-validation --jobs 8 --graphs` | 0 | 28 of 28 gates rc 0. Mutation: 447 caught, 0 escaped, 0 error. Coverage 100 % of lines and branches after the exclusions: `src/acmp.c` 815/815 lines, 426/426 branches. All 9 CTest binaries pass in the GCC and the sanitizer builds |
| `python3 scripts/baremetal.py --work build-rv32 --jobs 8` | 0 | Debug and Release rc 0; the core imports are those of `main` |

The clone's status and diff were empty before and after.
The two install steps (`apt-get`, `npm`) were not run. A pinned toolchain stood in for them: GoogleTest and GMock 1.14.0, Clang 18.1.3 for the comment and assertion lexing, clang-tidy 18.1.3 and Mermaid CLI 11.16.0. The host's GCC, Clang, cppcheck, CMake, RISC-V GCC and QEMU supplied the rest. The two artifact-upload steps have no `run:`.

R807-1's probe (`acmp_mask_probe.sh <tree> <out> 33`, its 33-sink BIND_RX tests under `-fsanitize=shift`) exits 0 at the head, 2 of 2 passed with no shift report. It exits 1 at `main` (`src/acmp.c:844:31`).

### Size

Text of `src/acmp.c` for RV32I (riscv64-elf-gcc 16.2.0, `-march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc -std=c11 -DNDEBUG -DCTRL_REENTRY_ASSERT`) at the default 16 sinks:

| Flags | `main` | This head |
|---|---:|---:|
| `-Os` (the milan-fpga firmware's) | 10,825 B | 10,921 B (+96) |
| `-O2` | 16,029 B | 16,141 B (+112) |
| `-O3` (`baremetal.py`'s Release) | 19,365 B | 20,365 B (+1,000) |

At `-O3` the loops no longer fold away where `respond(..., 0u)` is inlined, because they read the stored mask, and they are unrolled.

### Not in this PR

- milan-fpga adopts this change through its own pin move to `main`.
- `probe_of` holds one plus a sink index in a `uint8_t`, so it could not name a sink past 254. Round 2 refuses such a build (S1).

