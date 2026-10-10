[R584] NEGATIVE - exact head d1b22e804158cbcb33fa12116d60e982f9a4c55b

# R584-3: internal independent review of PR #705 (issue #697), round 3

**Head.** `d1b22e804158cbcb33fa12116d60e982f9a4c55b`, tree `bc319e0b59aa24fb561d51a13da5da7b43a9d676`. In the review clone, the index equals the head tree and `git write-tree` gives that tree (`receipts/clone_restore_check.txt`).

**Delta reviewed.** `386b8e69e..d1b22e804`: three commits (`76c0e27c3`, `36699f6c9`, `d1b22e804`) and nine files.
- `.github/workflows/rtl-fast.yml`
- `docs/testing/CI_WORKFLOWS.md`
- `sw/firmware/ctrl/README.md`
- `sw/firmware/ctrl/test/ctrl_boundary.py`, `ctrl_configs.py` (new), `ctrl_image.py` and `ctrl_pin.py` (new)
- `tb/verilator/mbx/Makefile` and `tb/verilator/mbx/README.md`

The raw diff is `receipts/delta_386b8e69_d1b22e80.diff`. The delta touches none of these:
- a firmware source or header, or a stack file or gitlink;
- a coverage row, the ratchet, a mutation table or a build flag;
- an `hdl/` file.

**Authorities**, read in this order:
- AGENTS.md and CONTRIBUTING.md;
- issue #697 acceptance 1 to 5;
- the lane assignment 6091228902, the pin ruling 6092176555, and rounds 2 (6092628778) and 2b (6093389868);
- the round-3 assignment 6094873968: item 1 (R584-2-F1 = R585-2-F1), item 2 (R584-2-F2 = R585-2-F2) and item 3 (R585-2-S1);
- the author's REVIEW READY (round 3) 6095730057, and the published evidence `review-evidence/697c-r1` at `ec6854f6` (round 1 only).

**Verdict.** One MINOR finding is open, R584-3-F1, so the verdict is NEGATIVE. Every other round-3 item is met at this head, as the table in section 2 shows.

## 1. Findings

### R584-3-F1 - MINOR - Conformance, Tests, Robustness - a C++ source that a builder names is not found, so a firmware header it alone reaches is judged only as C

`[R584] MINOR Conformance/Tests/Robustness - sw/firmware/ctrl/test/ctrl_configs.py:404 - cxx_sources misses test_maap_differential.cpp, which maap_differential.py:36 names and compiles as C++`

**Where**
- `sw/firmware/ctrl/test/ctrl_configs.py:404`: `cxx_sources` resolves a builder's C++ name only against `path.parent, HERE, STACK, ROOT, PP`.
- `sw/firmware/ctrl/test/maap_differential.py:36` names the source as `str(ctrl / "test/test_maap_differential.cpp")`, relative to the firmware tree. It compiles it as C++ through Verilator `--exe` with `-std=c++20`.

**Authority**
- Round-3 item 1: derive each unit's language from the builders, with nothing hand-listed. Firmware headers compiled by C++ arms are judged as C++.
- The gate states the same contract at `ctrl_configs.py:32` ("every C++ source a builder names"), `ctrl_boundary.py:46` and `sw/firmware/ctrl/README.md:93`.

**Evidence**
- `receipts/derive_scan.log` (section UNRESOLVED C++ NAMES) and `receipts/cxx_unresolved.log`:
  - `maap_differential.py 'test/test_maap_differential.cpp'` resolves against none of the gate's bases.
  - The 55 C++ sources the gate finds omit it. It is the only C++ test source under `sw/firmware/ctrl/test/` that is missing.
- `receipts/boundary_probes_g2.log`. The plant is a new firmware header, `maap/maap_r584.h`, holding `#ifdef __cplusplus` and `#include "../../../../third_party/tsn-c-stack/tests/acmp_fake.hpp"`.
  - Included from `test_maap_mbx.cpp`, a source the gate finds: **CAUGHT**, `firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers`.
  - Included from `test_maap_differential.cpp`: **ESCAPED**. The gate exits 0 with 0 findings.
  - The two plants are identical; only the C++ source that includes the header differs.

**Impact**
- A firmware header that only the MAAP differential's C++ source reaches is judged as C only. A C++-only include there of the stack's `src/`, `tests/` or `examples/` passes the boundary gate, and the real C++ build compiles it.
- Today no firmware header is affected:
  - The source includes only `maap.h`, `fw_gtest.hpp`, `verilator_harness.hpp` and the Verilated model's header.
  - All 24 firmware headers are reached by sources the gate finds (`receipts/cxx_units.log`).
- So no current include escapes. But the derivation that round 3 requires is incomplete, and a planted control of the round-3 class escapes.

**Required outcome**
- Every C++ source a builder names is found, including a name relative to the firmware tree or any other base the builder joins it to. An unresolved C++ name of the checkout is either resolved or refused by name, never skipped silently.
- A planted control of this shape is refused by name: a C++-only include in a header that only the differential's source reaches.
- With that fixed, the statements at `README.md:93`, `ctrl_configs.py:32` and `ctrl_boundary.py:46` hold as written. No wording change is required.

**Verification**
- `scripts/boundary_probes.py <copy> cplusplus-new-header-maap-differential` reports CAUGHT.
- `scripts/derive_scan.py` lists `test_maap_differential.cpp` among the C++ sources and shows no unresolved firmware-tree name.
- `ctrl_boundary.py --require-rv32 --selftest` passes with the new control, 0 misbehaved.

### R584-3-S1 - SUGGESTION - Robustness, Tests - three forms the derivation and the static pin check do not read

**Where**
- `sw/firmware/ctrl/test/ctrl_configs.py:155-191`: the flag forms.
- `ctrl_configs.py:70`: `FORCED`, the force-included header's name, written as a constant.
- `sw/firmware/ctrl/test/ctrl_pin.py:129`: a pin target is any recipe line holding `--stack-pin`.

**Evidence**
- `receipts/boundary_probes_g5.log`, probe `fw-multiword-string-flag`: a builder flag written inside a multi-word literal (`"-O2 -DR584_MULTI".split()`) is not derived. The gate passes an include of a stack source under `#ifdef R584_MULTI`.
- The force-included SRP header is a named constant. It is not read from the builders' `-include` pairs (`srp_arms.py:38` is the only firmware one today).
- `receipts/boundary_probes_g1.log`, probe `makefile-pin-errors-ignored`: the static Makefile check accepts a pin recipe whose errors are ignored (`-python3 ... --stack-pin`). The `--selftest` bench arms catch it: 5 of 20 controls are ESCAPED (`receipts/pin_controls_pin_errors_ignored.log`), so CI's `--selftest` step would fail.

**Why it is not a finding**
- No current flag is missed. The raw scan in `receipts/derive_scan.log` finds every `-D`/`-U` name of every builder among the derived modes or values. Its only extras are a CMake line in `scripts/ci_events.py` and docstring prose.
- The one multi-word flag today, `-CFLAGS "-DPP_TOP_IF2"` in `aecp_wire.py:116`, is also written as a literal, so it is derived.
- The documented forms are "one argument or two", and both hold.

**Optional**
- Derive or refuse a `-D`/`-U` token inside a multi-word literal.
- Read force-included headers from the builders' `-include` pairs.
- Have the static check refuse a pin recipe that ignores its exit status.

## 2. Round-3 items, re-run independently at this head

| Item | Result | Receipt |
|---|---|---|
| R584-2's shape probe: an `#if IMAGE_SINKS > 1u` stack-example include in `image_main.c` | CAUGHT: `firmware [-DIMAGE_SINKS=2u -DIMAGE_SOURCES=1u]: test/rv32_image/image_main.c includes tsn-c-stack/examples/adp_port.h` | `boundary_probes_g1.log` |
| Exact-value shape probes: `IMAGE_SOURCES == 1u` (arty_current only) and `IMAGE_SINKS == 9u && IMAGE_SOURCES == 9u` (8x8 only) | both CAUGHT, each naming its own shape's flags | `boundary_probes_g1.log` |
| Shape values from `ctrl_image.shape_build` at every shipped config | 5/5, 2/1, 2/2 and 9/9 over the 5 configs. These equal the image builder's own per-shape stream counts (5/5 twice, 2/1, 2/2, 9/9) | `gate_selftest.log` line 2, `img_head.log` |
| Builders, modes and values read from the builders | 32 builders; 18 modes; 7 computed values refused if tested; the mbx Makefile is the one Makefile builder. The raw `-D`/`-U` scan finds nothing missed | `derive_scan.log` |
| `#ifdef __cplusplus` include in a firmware header reached by C++: `adp/adp_mbx.h`, and `aecp/aecp.h` through `#if defined(__cplusplus)` | both CAUGHT as `firmware c++` | `boundary_probes_g2.log` |
| A C++-only include reached only through `test_maap_differential.cpp` | ESCAPED: R584-3-F1 | `boundary_probes_g2.log` |
| Two-argument forms, each derived | `-D NAME` in a Python list: CAUGHT `[-DR584_TWO_ARG]`<br>`-D NAME` in call arguments: CAUGHT `[-DR584_CALL]`<br>`-D NAME=2` tuple in the image builder: CAUGHT `[-DR584_TWO_ARG=2]`<br>`-D NAME=3` as two Makefile words: CAUGHT `[-DR584_MK=3]`<br>`-U NAME` as Makefile words and in a tuple: in the derived modes (`R584_MK2 (-UR584_MK2)`, `R584_UNDEF (-UR584_UNDEF -DR584_UNDEF)`) | `boundary_probes_g3.log`, `boundary_probes_g5.log` |
| The same plants written on the stack side of the checkout | refused first by the pin check (exit 2, `differs from the pinned 1a9f651c`), as designed. Stack-side plants are judged through the self-test's planted copies. `boundary_probes_g3.log` labels `two-arg-U-tuple` ESCAPED only because my needle listed the two flags in the other order; its modes line shows both derived | `boundary_probes_g3.log`, `boundary_probes_g4.log` |
| Every mbx Makefile target whose recipe compiles with the stack depends on `stack-pin` | `tb/verilator/mbx/Makefile:82` (the library), `:91` (`run-cosim`) and `:115` (`run-if2`), each order-only on the phony `stack-pin` (`:79`). `mutants` and `mutants-quick` build RTL only (`mutants.py:43`). Planted controls, all CAUGHT by name: `run-cosim` unpinned, a new unpinned `$(FW_INC)` target, and a recipe naming the checkout's stack | `boundary_probes_g4.log` |
| Pin probes against a poisoned, hidden, off-revision or extended stack | 16 of 16 as expected. `all`, `run-cosim`, `run-if2`, `obj_fw/libctrlfw.a`, `stack-pin`, `-j16 all`, `-k -j16 all` and `-j16 run-if2 run-cosim` each exit 2 on `REFUSED: tsn-c-stack ...` and never compile the poison. So do an assume-unchanged edit, another revision and an extra header. The clean stack passes `stack-pin` and builds the library | `pin_probes.log` |
| The gate's self-test at the head | PASS, rc 0: `51 firmware units (24 also as C++) ... 18 build modes, 5 shapes and 2 mailbox contracts (942 preprocessings) ... 0 finding(s), 45 boundary and 20 pin controls, 0 misbehaved`. The stack's own gate and its controls pass | `gate_selftest.log`, `gate_selftest.rc` |
| `d1b22e804`: the gate without `gptp-processor` | exit 2: `REFUSED: the end-station builder refused endstation_arty_4x4.yaml ... the gptp-processor submodule is not checked out`. `rtl-fast.yml:255` initialises it in `firmware-unit` | `no_gptp.log` |
| Images byte-identical to dev | `ctrl_image.py` at all 5 shipped shapes, built at the head and at dev `aef7ac666` (a separate copy checked out there): 5 of 5 ELF sha256 identical | `img_head.sha256`, `img_dev.sha256`, `img_*.log` |
| The `ctrl_image.py` refactor (`shape_build` extracted from `measure`) | `ctrl_image_selftest.py`: 33 checks PASS. Nothing else imports `ctrl_image` except the gate | `ctrl_image_selftest.log` |
| Mailbox bench at the head, with the pinned Verilator 5.050 (identity `Verilator 5.050 2026-07-01 rev v5.050`) | 382 / 427 / 32 / 384 / 429 / 369 checks, 0 failures, mutants 5 of 5. The pin line prints once, before the library build | `mbx_bench_head.log`, `mbx_bench_head.rc` |
| Coverage denominator and kill counts | unchanged by construction, not re-run here. The delta holds no coverage, ratchet, mutation table, firmware or stack file, and no campaign imports a changed module | `delta_386b8e69_d1b22e80.diff` |
| `ci_events.py --check` | OK (1757 contract items) | `ci_events_check.log` |
| Docs gates | rc 0: `docs_check.py`, `check_doc_style.py`, `DOC_MAP.gen.py --check`, `check_submodule_docs.py`, `submodule_boundaries.gen.py --check` and `check_solution_docs.py`.<br>`check_em_dash.py` could not run: its pinned renderer is not installed here, and no shared install was allowed. A raw scan of the 1142 added lines finds 0 em or en dashes | `docs_checks.log`, delta diff |

## 3. Prior public findings at this head

| Finding | Status at d1b22e80 | Evidence |
|---|---|---|
| R584-2-F1 (shape values hand-listed; per-shape headers from one config) | **Resolved.** The shape values and headers are derived from `ctrl_image.shape_build` and every `*_entity.py` at each config, `FIRMWARE_DEFINES`/`SRP_ENTITY` are gone, and the probe and its exact-value variants are CAUGHT | section 2 rows 1-3 |
| R585-2-F1 (firmware headers judged only as C; image only at 1/1) | **Resolved for every source the gate finds**, and for the shapes. The n1/n2 class is CAUGHT (`adp_mbx.h`, `aecp.h`) and n3 (the image's shape value) is CAUGHT. A residual gap in finding the C++ sources is the new R584-3-F1 | section 2 |
| R584-2-F2 = R585-2-F2 (`run-if2` unpinned) | **Resolved.** `run-if2` and `run-cosim` take `| stack-pin`, the static check derives targets from make's own database and dry run, and every reaching target refuses a poisoned stack on the pin | `pin_probes.log`, `gate_selftest.log` lines 63-69 |
| R584-2-S1 = R585-2-S1 (two-argument modes), required in round 3 | **Resolved.** List, tuple, call and Makefile forms are derived (section 2) | `boundary_probes_g3.log`, `_g5.log` |
| R585-2-S2 (an explicit `--stack` pins that clone while the AECP tests take the submodule's `tests/`) | **Retained as SUGGESTION** (optional, not addressed). `aecp_arms.py:83` still uses `STACK_TESTS` (`ctrl_build.py:56`) while `:144` pins `args.stack` | code read |
| R584-2-R1, R585-2-RS1 to RS3 (PR body) | **Applied.** The body has no relative `../` links and none of the three quoted phrases; it cites its round-3 state and hosted runs at `386b8e69` | PR body at review time |
| Round 1: R584-1-F1, -S1, -S2; R585-1-F1, -F2, -S1, -R1 to R4 | **Resolved in round 2, and still holding.** The MAAP differential and AECP pin controls, the hidden-edit, extra-file, script and CMake pin controls, the stack-tests plants and the mode plants all pass in this head's self-test, and my pin probes repeat the hidden-edit and extra-file cases | `gate_selftest.log`, `pin_probes.log` |

## 4. Lens results

```text
[R584] PASS RTL - tb/verilator/mbx/Makefile:79,82,91,115 and receipts/mbx_bench_head.log at d1b22e80 - the order-only stack-pin prerequisites add no rebuild edge and change no RTL list, VFLAGS or relink rule; the bench passes 382/427/32/384/429/369 with 5/5 mutants; 386b8e69..d1b22e80 has no hdl/ file
[R584] PASS Docs - sw/firmware/ctrl/README.md:80-126, tb/verilator/mbx/README.md:12-20, docs/testing/CI_WORKFLOWS.md:58-66,195-201, .github/workflows/rtl-fast.yml:287-295, and the ctrl_pin.py, ctrl_configs.py and ctrl_boundary.py docstrings at d1b22e80, against the code and the self-test output - the counts (42 refused plants and 3 passing, 20 pin controls, the five derived bench targets) and the gptp-processor refusal match; docs gates rc 0; 0 em/en dashes in the added lines
[R584] MINOR Conformance - R584-3-F1 (above)
[R584] MINOR Tests - R584-3-F1 (above)
[R584] MINOR Robustness - R584-3-F1 (above)
```

R584-3-F1 is a code defect in the gate. The docs describe the contract that round 3 requires, and fixing the code makes them true as written, so Docs is not attributed.

## 5. Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R584-3-F1) | #697 acceptance 1-5; round 2, 2b and 3 items; `ctrl_configs.py`, `ctrl_boundary.py`, `ctrl_pin.py`, `ctrl_image.py:339-360` and the mbx `Makefile`; images against dev `aef7ac666` | R584-3 | d1b22e804158cbcb33fa12116d60e982f9a4c55b |
| RTL | CLEAN | `tb/verilator/mbx/Makefile`, `mbx_bench_head.log`; the delta has no `hdl/` change | R584-3 | d1b22e804158cbcb33fa12116d60e982f9a4c55b |
| Robustness | UNCLEAN (R584-3-F1) | the derivation's forms (`derive_scan.log`); the language derivation (`cxx_units.log`, `cxx_unresolved.log`); poisoned, hidden, off-revision and extra-file pin probes; `-j` and `-k` make; a missing `gptp-processor` | R584-3 | d1b22e804158cbcb33fa12116d60e982f9a4c55b |
| Tests | UNCLEAN (R584-3-F1) | the 45 `ctrl_boundary.py` PLANTS and 20 `ctrl_pin.py` controls (self-test run), 20 independent boundary probes, 16 pin probes, `ctrl_image_selftest.py` | R584-3 | d1b22e804158cbcb33fa12116d60e982f9a4c55b |
| Docs | CLEAN | as in the PASS line above | R584-3 | d1b22e804158cbcb33fa12116d60e982f9a4c55b |

## 6. Real limits

- **Images.** Only the `ctrl_image.py` fixture was rebuilt (5 shapes, head against dev `aef7ac666`). The SRP and AECP fixtures (`ctrl_srp_image.py`, 30 ELFs) need the runtime archives that `ctrl_image_runtime.py` builds, which are not present here.
  - Neither that builder nor anything it imports (`ctrl_build`, `srp_arms`, `ctrl_arms`, `fw_gtest`, `fw_rv32`) changes in the delta.
  - Their identity rests on round 2b's 35/35 and the author's round-3 receipt.
- **Coverage and kills.** The coverage gate, the firmware gate and the mutation campaigns were not re-run here. They are unchanged by construction (no input in the delta), and the author's round-3 receipt reports them identical.
- **Em dashes.** `check_em_dash.py` could not run without its pinned renderer. A raw scan substitutes.
- **Probe environment.**
  - Host with gcc 16.2.1 and the RV32 compiler at the SDK path the gate finds (`fw_rv32.compiler()`), not the CI-parity container.
  - Every probe ran in a disposable copy under `scratch/`.
  - The review clone was then verified: 1261 tracked blobs re-hashed with their modes (0 mismatches), no index flags, every gitlink at its pin, and status empty including ignored files. Ignored `__pycache__` directories that this session's tool runs created were removed.
- **Hosted CI.** At review time, hosted checks at this head were partly complete: lint, Yosys shards, yosys-elaboration, Verilator shard 3, docs-check-no-git and full-ci-gate succeeded. `firmware-unit`, docs-check, elaborate and Verilator shards 0, 1, 2 and 4 were still in progress, and Physical gPTP was skipped (nightly and manual only) (`receipts/hosted_checks.tsv`). No act run and no host act self-test were made.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.

## 7. Pending manager duties

- Carry R584-3-F1 to the next round.
- Hosted and act acceptance at the exact head: the hosted runs above were still in progress.
- At the merge turn, the current-dev candidate (source base `8b61b709`, live dev `e8454e27`): builder and native banks, the 35 linked images against dev, coverage denominator and kill counts.
- Two independent POSITIVE reviews, and the completion ledger re-covered at the final head.

R584-3 FINISHED
