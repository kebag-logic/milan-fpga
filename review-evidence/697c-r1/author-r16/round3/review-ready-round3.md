[A583] REVIEW READY (round 3)
Commit: d1b22e804158cbcb33fa12116d60e982f9a4c55b (tree bc319e0b59aa24fb561d51a13da5da7b43a9d676), three new commits on 386b8e69: 76c0e27c3, 36699f6c9, d1b22e804. No rebase or amend, not pushed (PR #705 still shows 386b8e69).

Changed (no firmware source, header, test, mutation table, coverage row or build flag):
- R584-2-F1 = R585-2-F1, each unit judged as its builders compile it, read from them by the new `sw/firmware/ctrl/test/ctrl_configs.py`. The gate lists no flag: its `FIRMWARE_DEFINES` (the fixed `IMAGE_SINKS`/`IMAGE_SOURCES` 1u among them) and `SRP_ENTITY` are gone, and every macro is explored in each state a builder leaves it in, undefined included.
  - Language: every unit as C. A firmware unit that a C++ source a builder names (a test, a bench) reaches is judged as C++ too, with the arms' test flags and include path (the stack's `tests/` on it): 24 of 51. Every `#include` is followed as text, every branch alike; one a macro computes is a finding.
  - Shape values: the image's stream counts come from the image builder's own `ctrl_image.shape_build` (extracted from `measure`, the same flags and headers) at every shipped config: 5/5, 2/1, 2/2 and 9/9, or undefined as every other builder leaves them. A judged unit whose includes depend on any other value a builder computes (7 of them) is refused.
  - Shapes: every shipped config's generated headers, written by the builders' own generators (every `*_entity.py`, and the store's headers through `shape_build`); the SRP shape header force-included, as the SRP builds compile every unit, or not.
  - Mailbox contract: the tracked one, or the variant `gen_mailbox.py` writes for every other interface count it admits (it refuses 3).
  - The compiler's `-dU` macros are kept where the conditionals and `#include` lines of the files read name them, or their definitions do. A configuration that stops on an `#error` is one no builder compiles; what it reads is still judged.
- R584-2-F2 = R585-2-F2: `tb/verilator/mbx/Makefile` gives `run-if2` and `run-cosim` the `stack-pin` prerequisite the firmware library has. The new `ctrl_pin.py` reads every Makefile builder's targets from make's own database and dry run: a target whose recipe names the stack without the pin check as a prerequisite is a finding. The self-test runs every target whose dry run reaches the stack (`all`, `run-cosim`, `run-if2`, `obj_fw/libctrlfw.a`, `stack-pin`) for real in a scratch copy, against a clone with a poisoned `wire.h` and a simulator that builds nothing: each refuses on the pin check and never compiles the poisoned header.
- R585-2-S1: `-D NAME` / `-U NAME`, two literals of a list, tuple or call, or two words of a Makefile line, are derived like `-DNAME`.
- d1b22e804: the gate now loads every shape through the end-station builder, which needs `gptp-processor`; without it the gate exits 2 naming the submodule instead of crashing. `firmware-unit` initialises it.
- Docs: `sw/firmware/ctrl/README.md:85-126`, `tb/verilator/mbx/README.md:12-20`, `docs/testing/CI_WORKFLOWS.md:58-66,197-201`, the `rtl-fast.yml` step comment, and the three modules' docstrings.

Validation at the head (CI-parity container with CPython 3.12.3, gcc 13.3 and GoogleTest 1.14.0 for the firmware gates; host for the pinned RV32 SDK, Verilator 5.050, the boundary and the docs; each in a clean clone):
- `ctrl_boundary.py --require-rv32 --selftest`: PASS, `51 firmware units (24 also as C++) ... 18 build modes, 5 shapes and 2 mailbox contracts (942 preprocessings), and every Makefile builder's pin prerequisites; 0 finding(s), 45 boundary and 20 pin controls, 0 misbehaved`. New controls, each refused by name:
  - R584-2's probe: `firmware [-DIMAGE_SINKS=2u -DIMAGE_SOURCES=1u]: test/rv32_image/image_main.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers`
  - R585-2's n1: `firmware c++: acmp/acmp_mbx.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers`
  - `firmware [shape=endstation_ax7101_8x8]: test/ctrl_aecp_image.c includes tsn-c-stack/src/acmp.c`, `firmware [-include srp_entity_gen.h]: maap/maap_mbx.c ...`, `firmware [interfaces=2]: adp/adp_mbx.c ...`, an include under `#ifndef LWSRP_MILAN`, and a unit testing `AECP_TEST_INTERFACES`
  - two-argument modes: `host [-DCTRL_SPLIT_MODE]: ...` (Python builder) and `host [-DCTRL_SPLIT_MAKE]: ...` (Makefile)
  - pin: the five derived bench targets, each `exit 2: REFUSED: tsn-c-stack differs from the pinned 1a9f651c: include/wire.h`; `make stack-pin` passes the clean clone; a planted Makefile with `run-if2` unpinned is refused by name.
- The reviews' own probe scripts, rerun unchanged against a clean clone of the head:
  - R584-2 `boundary_probes.py`: 8 CAUGHT, and both former gap probes (`IMAGE_SINKS > 1u`, two-token mode) refused by findings naming them.
  - R584-2 `shape_probe.sh`: the gate exits 1 with the finding above.
  - R584-2 `pin_probes.sh`: 44 of 44 refused, and S6 (`make run-if2` on a poisoned `wire.h`) exits 2 on the pin check.
  - R585-2 `boundary_probes.py all`: 11 of 11 CAUGHT, n1 to n4 included.
  - R585-2 `pin_probes.sh`: 27 of 27 refused, `WIRE-mbx_run_if2` included.
- RV32 images: 35 of 35 ELF files byte-identical to dev aef7ac66 (the manifest equals round 2b's, sha256 de8ae063…); `ctrl_image.py --base aef7ac66` +0 everywhere.
- `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`: PASS, 59 arms; control 471/471, AECP 74/74, SRP 169 and 68, lwSRP pin 2/2; the 843 verdict lines are identical to round 2b's line for line and to dev's by name.
- Coverage: `--selftest` 29 of 29, `--check` PASS (30 files), every row identical to round 2b's (dev's raw counts); the ratchet is unchanged.
- `make -C tb/verilator/mbx`: 382/427/32/384/429/369 checks, 5/5 mutants. `make run-if2` alone and `make run-cosim` alone each print the pin line before compiling. MAAP differential: the pin, then 16/16.
- Harness self-tests: 17, 18/18 and 33 checks. All 54 docs-job commands exit 0, with every submodule and with only the hosted docs job's three. `ci_events.py --check` OK (1757 items), `--selftest` PASS (2387 arms). em-dash: 0 findings over 40 added lines.

Acceptance criteria: met at the head. Images are byte-identical to dev aef7ac66 at every shape; coverage and kills are unchanged; round 3 items 1 to 3 are met as above.
Open risks/questions:
- The boundary self-test does more work: 630 s here on a shared host (2 min 51 s hosted at 386b8e69, in a 45-minute `firmware-unit` that took 26 min). Not yet measured on a hosted runner.
- The dimensions are explored independently, a superset of what builders compile together, so a finding may name a combination no single builder compiles.
- R585-2-S2 (optional) is not addressed.
- Hosted CI and act have not run at any round-3 commit.

Details are in the Round 3 sections of the lane packet's HANDOFF.md and PR-BODY.md.
