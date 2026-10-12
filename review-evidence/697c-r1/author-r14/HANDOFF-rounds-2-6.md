# HANDOFF, rounds 2 to 6 — lane 697c, [A583]

Moved verbatim out of `HANDOFF.md` in round 8, which keeps round 1, round 7 and round 8, so that file stays under 200 KB. Anchors below are this file's.

## Round 2

Assignment: #697 comment 6092628778. It answers R584-1 (PR #705 comment 6092573026) and R585-1 (comment 6092623741), both NEGATIVE on MINOR gaps in the boundary and pin gates. The pin ruling 6092176555 confirms `1a9f651c`.
Base of the round: `60e7b57c962dce06ae8862b0992c98f20d1afe76`. Three new commits; no rebase, amend or push.

| Commit | Subject | Items |
|---|---|---|
| `e11733db4` | Prove the stack pin by blob hashes and run it before the MAAP differential and the mailbox bench build the stack | 2, 3 |
| `a205dab92` | Judge the TSN stack boundary in every configuration the builders compile, the stack's tests included | 1, 4, and the controls of 2 and 3 |
| `38240ac4c` | Cite the stack's porting guide for the no-callback rule in the five adp.c coverage rows | 5 (R5) |

No firmware source, test, mutation table or build flag changed; images and coverage are unchanged (below).

### Item 1 — R585-1-F1: the boundary in every configuration the firmware builds

- The modes are read from the builders, not restated: `sw/firmware/ctrl/test/ctrl_boundary.py:115` `BUILDERS` (`ctrl_build.py`, `ctrl_arms.py`, `srp_arms.py`, `ctrl_image.py`, `ctrl_srp_image.py`, `maap_differential.py`, the bench's Makefile), `:155` `mode_flags` (every `-D`/`-U` string literal of a Python builder, every such word of the Makefile; a flag computed at run time, an f-string such as a shape's stream count, is a value, not a mode) and `:168` `modes`. At this head they are, as the gate prints them: `NDEBUG` (`-DNDEBUG`, `-UNDEBUG`), `CTRL_REENTRY_ASSERT`, `ADP_TEST_RELEASE`, `ADP_TEST_COVERAGE`, `CTRL_APP_TEST_SRP`, `CTRL_IMAGE_SRP`, `CTRL_MBX_BASE` (two values), `CTRL_MBX_WFI`, `LWSRP_MILAN`, `mrp_transmit`, `shlan_calloc`. The assignment's `-DNDEBUG`, `-UNDEBUG` and `-DCTRL_REENTRY_ASSERT` come from `ctrl_arms.py`.
- Combinations, by construction: `:191` `preprocess` runs `-E -dU -MD`, so one preprocessing yields both the unit's dependencies and every macro it tested or expanded. `:222` `explore` preprocesses the unit's default build, then every combination of the modes of the macros it tests, with every other mode's macro defined, until no new one appears. A configuration that agrees with an explored one on every macro that one tested follows the same path; with the untested modes defined, a test of any of them (`#ifdef`, `defined`, `#if M`) would have been reported. So no combination of the builders' modes is left out, and none is enumerated blindly: 268 preprocessings at this head (`round2/configs.txt`, per unit).
- Both directions, host and RV32: the stack's side (`:309`) under `C_FLAGS` and `RV32_FLAGS`, the firmware's side (`:390`) now with the RV32 compiler as well; the C library allow-list is computed per configuration (`:284`). A finding names the smallest configuration that reaches it (`:275`), e.g. `host [-DCTRL_REENTRY_ASSERT]: ...`.
- The firmware's side refuses a non-public dependency in the stack judged and in the checkout's submodule (`:395`): R585-1's fourth probe resolves into the checkout's submodule (through the lwSRP include directory) while it judges a copy of the stack. A stand-in for an unfound header is written only for a plain name; a `..` or absolute path that resolves nowhere is an error, never stood in for (`:191`).
- `FIRMWARE_DEFINES` (`:107`) no longer forces `CTRL_IMAGE_SRP`: the SRP image's switch is a mode, so both `ctrl_image.c` compositions are judged.
- R585-1's own probe script (`scripts/boundary_probes.py` of its packet, run unchanged at this head, `round2/r585-boundary-probes-head.txt`): 4 of 4 CAUGHT by `ctrl_boundary` itself:

| Probe | `ctrl_boundary` |
|---|---|
| control: `src/acmp.c` includes `mbx_hal.h` unconditionally | `host: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| `mbx_hal.h` inside the stack's `CTRL_REENTRY_ASSERT` region | `host [-DCTRL_REENTRY_ASSERT]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| `ctrl_debug.h` under `#ifndef NDEBUG` | `host [-UNDEBUG]: the stack's src/maap.c includes sw/firmware/ctrl/port/ctrl_debug.h` |
| the adapter reaching `tests/acmp_fake.hpp` under `CTRL_REENTRY_ASSERT` | `firmware [-DCTRL_REENTRY_ASSERT]: acmp/acmp_mbx.c includes third_party/tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers` |

### Item 2 — R585-1-F2 = R584-1-F1: every gate that builds the stack refuses an off-pin or modified stack

- One shared check: `sw/firmware/ctrl/test/ctrl_build.py:211` `stack_pin`, with a command line at `:265` (`python3 -B sw/firmware/ctrl/test/ctrl_build.py --stack-pin [DIR]`: exit 0 with the pin, or 2 with the refusal).
- The mailbox bench: `tb/verilator/mbx/Makefile:76` phony `stack-pin`, an order-only prerequisite of `obj_fw/libctrlfw.a` (`:79`), so it runs before every firmware build and even when the library is current (`make obj_fw/libctrlfw.a` on a built bench printed the pin and rebuilt nothing).
- The MAAP differential: `sw/firmware/ctrl/test/maap_differential.py:95,100`: `--stack` (default the submodule), pin check first, so both modes refuse before building; the self-test plants into a copy of the checked stack (`:49`).
- Every gate that builds the stack now runs it: the firmware gate (with its coverage), `ctrl_boundary.py`, the MAAP differential in both modes, the bench, and both image fixtures with the submodule as their stack (`ctrl_srp_image.py --stack-source DIR` measures an explicitly given stack as given, unchanged). The statements now hold as written: `sw/firmware/ctrl/README.md:92-101`, `ctrl_boundary.py:44-47`, `ctrl_build.py:211-215`, `tb/verilator/mbx/README.md:16-18`, `sw/firmware/ctrl/maap/README.md:171-172`, `docs/testing/CI_WORKFLOWS.md:58-63,195-197`.
- Controls (`ctrl_boundary.py:598` `pin_controls`): the bench passes the pinned clone; the bench (`obj_fw/libctrlfw.a`, with `CC=false` so an escape builds nothing), the differential and the differential's self-test (with `VERILATOR=false`) each refuse an edited clone by name, exit 2.

### Item 3 — R584-1-S1: the pin check proves content

- `ctrl_build.py:188` `STACK_PROVEN`: `src`, `include`, `tests`, `examples`, `scripts`, `cmake`, `CMakeLists.txt` (`examples` too, because the boundary searches it and copies it into its controls).
- `:191` `blob_id` hashes the file's bytes as git hashes a blob (a symbolic link's target), `:198` `worktree_files` lists what is on disk, and `:211` compares both with `git ls-tree -r` of the gitlink's commit: a changed, missing, added or type-changed file is refused by name. The index is never consulted, so `assume-unchanged` and `skip-worktree` hide nothing.
- Controls: an edit hidden by `assume-unchanged` (submodule `git status` empty) refused; a script, a CMake file and an added `include/stdint.h` refused.

### Item 4 — R584-1-S2: the boundary covers the stack's tests

- `ctrl_boundary.py:331` `tests_side`: every `tests/*.cpp` and `tests/*.hpp`, preprocessed as C++ with the include path the arms compile them with (`ctrl_build.includes`, the stack's `tests/`, its `examples/` last), in every configuration. A dependency inside milan-fpga outside the submodule is refused by name; the host's libraries (C++, GoogleTest) are allowed. The gate refuses (exit 2) without GoogleTest's headers. The C++ view also covers the stack headers' `__cplusplus` regions.

### Item 5 — residue

- R5: `sw/firmware/gtest/README.md:245-247` and the five rows `:312-316`, worded as R585-1 asks. `fw_coverage.py --check` matches rows by file, function and statement; it passes with the same 22 files.
- R1 to R4: the PR body (round 2 section of `PR-BODY.md`).
- Not taken (optional): the lwSRP pin (`ctrl_arms.lwsrp_pin`) still reads `git status`; R584-1-S1 marks that part optional and it is not #697's submodule.

### Planted controls of the round-2 gate (`round2/boundary-selftest-final.log`)

25 refused by name and 3 passing boundary controls, then 12 pin controls; 0 misbehaved. New in round 2:

| Control | Refused by |
|---|---|
| `src/acmp.c`: `mbx_hal.h` in the `CTRL_REENTRY_ASSERT` region | `host [-DCTRL_REENTRY_ASSERT]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| `src/maap.c`: `ctrl_debug.h` under `#ifndef NDEBUG` | `host [-UNDEBUG]: the stack's src/maap.c includes sw/firmware/ctrl/port/ctrl_debug.h` |
| `src/maap.c`: `mbx_contract.h` under `#ifndef NDEBUG` and `#ifdef CTRL_REENTRY_ASSERT` (a combination no single arm builds) | `host [-DCTRL_REENTRY_ASSERT -UNDEBUG]: the stack's src/maap.c includes sw/firmware/ctrl/mbx/mbx_contract.h` |
| `acmp/acmp_mbx.c` reaches the stack copy's `tests/acmp_fake.hpp` under `CTRL_REENTRY_ASSERT` | `firmware [-DCTRL_REENTRY_ASSERT]: acmp/acmp_mbx.c includes tsn-c-stack/tests/acmp_fake.hpp, ...` |
| the same by its checkout path (R585-1's spelling) | `firmware [-DCTRL_REENTRY_ASSERT]: acmp/acmp_mbx.c includes third_party/tsn-c-stack/tests/acmp_fake.hpp, ...` |
| `maap/maap_mbx.c` tests a mode by value (`#if CTRL_REENTRY_ASSERT`) | `firmware [-DCTRL_REENTRY_ASSERT]: maap/maap_mbx.c includes tsn-c-stack/src/maap.c, ...` |
| `test/ctrl_image.c`: the SRP composition reaches a stack source | `firmware [-DCTRL_IMAGE_SRP]: test/ctrl_image.c includes tsn-c-stack/src/acmp.c, ...` |
| `tests/test_maap_debug.cpp` includes `mbx_hal.h` | `tests: the stack's tests/test_maap_debug.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| `tests/test_adp.cpp` includes the harness's `fw_gtest.hpp` | `tests: the stack's tests/test_adp.cpp includes sw/firmware/gtest/fw_gtest.hpp` |
| `tests/test_adp_reentry.cpp`: `ctrl_pool.h` under `ADP_TEST_RELEASE` | `tests [-DADP_TEST_RELEASE]: the stack's tests/test_adp_reentry.cpp includes sw/firmware/ctrl/port/ctrl_pool.h` |
| `include/acmp.h`: `mbx_hal.h` for C++ only | `tests: the stack's tests/test_acmp.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| a mode planted into a copy of `ctrl_arms.py`'s text (`-DCTRL_PLANTED_MODE`) guards a plant in `src/adp.c` | `host [-DCTRL_PLANTED_MODE]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| pass: a stack test reaches the stack's example header | passes |

Pin controls: the pinned clone accepted; refused: an edited source, test, script and CMake file, an `assume-unchanged` edit, an added header, another revision; the bench accepts the pinned clone and refuses an edited one; the differential and its self-test refuse an edited one.

### Real-path probes (`round2/realpath-probes.txt`, script `round2/realpath.sh`)

A disposable clone of the lane at `38240ac4`, its own submodules initialised from local checkouts; edits in the clone's submodule only, a plant committed locally there with its gitlink staged in the clone's index so the pin check passes and the real path runs.

| Probe | Gate | Result |
|---|---|---|
| `src/maap.c` edited | `make -C tb/verilator/mbx run-cosim` | exit 2, `REFUSED: tsn-c-stack differs from the pinned 1a9f651c: src/maap.c` |
| same | `maap_differential.py`, `maap_differential.py --self-test` | exit 2, same refusal |
| same | `test_ctrl_firmware.py --require-rv32` (control) | exit 2, same refusal |
| `src/adp.c` edited, `assume-unchanged`, `git status` empty | `ctrl_build.py --stack-pin`; the bench | exit 2, `... differs from the pinned 1a9f651c: src/adp.c` |
| `scripts/check_boundary.py` edited | `ctrl_boundary.py --require-rv32` | exit 2, `... differs ...: scripts/check_boundary.py` |
| `tests/test_maap_debug.cpp` includes `mbx_hal.h` (R584-1-S2) | `ctrl_boundary.py --require-rv32` | exit 1, `tests: the stack's tests/test_maap_debug.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| `mbx_hal.h` in the `CTRL_REENTRY_ASSERT` region | same | exit 1, `host [-DCTRL_REENTRY_ASSERT]: ...` and `rv32 [-DCTRL_REENTRY_ASSERT]: ...` |
| `ctrl_debug.h` under `#ifndef NDEBUG` | same | exit 1, `host [-UNDEBUG]: ...`, `rv32 [-UNDEBUG]: ...`, and the stack's own gate |
| the adapter reaching `tests/acmp_fake.hpp` under `CTRL_REENTRY_ASSERT` | same | exit 1, `firmware [-DCTRL_REENTRY_ASSERT]: ...` and `firmware rv32 [-DCTRL_REENTRY_ASSERT]: ...` |

### Images (round-2 head)

All 25 ELF files rebuilt at the gate tree of this head (same pinned SDK, same runtime archives as round 1): the manifest `round2/images-head.sha256` (sha256 `611b05e5a0ca7e87c9685d89145abd55ec81f45989c59bd91e4bcfbf80d6928f`) equals both dev's and round 1's line for line, so every row of the table [above](#rv32-image-hashes-before-and-after) holds at `38240ac4` too: 25 of 25 byte-identical.

### Gates at the round-2 head

The long gates ran on the working tree recorded as tree `bb107517` before the commits. Its only difference from the head's tree is docstrings and two wrapped lines in `ctrl_boundary.py`, which none of those gates imports; the boundary gate and the docs gates ran again after that edit, at the head.

| Gate | Where | Result | Planted controls |
|---|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest` | host | PASS, 0 findings, 268 preprocessings, 155 s | 28 boundary, 12 pin, 0 misbehaved |
| the round-1 gate at `e11733db` (new pin check, old gate) | disposable clone | PASS | 15 boundary, 4 pin |
| `ctrl_boundary.py --require-rv32` without the RV32 compiler | host | exit 2, refused | — |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | container | PASS, 51 arms; `mutants: 471 of 471 caught`; SRP 169 and 68, 0 escaped; lwSRP pin 2 of 2; its 761 verdict lines equal round 1's by name (log 269,191 bytes, sha256 `b461844f…5c77`) | its campaigns |
| `fw_coverage.py --selftest`, `--check --jobs 4` | container | 29 of 29; PASS, 22 files, raw counts equal to the table above (`round2/coverage-head.log`) | 29 |
| `maap_differential.py --self-test` | host, Verilator 5.050 | prints the pin first; 16 of 16, the same plants as round 1 (log 13,802,189 bytes, sha256 `58813dbd…981f`) | 16 |
| `make -C tb/verilator/mbx` | host, Verilator 5.050 | the pin check before the firmware build; 382, 427, 32, 384, 429, 369 checks, 0 failures; `mbx mutants: 5 of 5 caught` (log 80,358 bytes, sha256 `41ec4716…8e30`) | 5 |
| images, 25 | host, pinned SDK | 25 of 25 identical | — |
| `ci_events.py --check`, `--selftest` | container | OK, 1757 items; PASS, 2387 arms (log sha256 `7090311b…6d46`) | its own |
| `tally_selftest.py`, `fw_rv32_selftest.py --require-rv32`, `ctrl_image_selftest.py --require-rv32` | container | 18 of 18; 17 checks; 33 checks | their own |
| docs job, 54 repository commands (links, paths, style, em-dash, contents, TOC and anchors, submodule docs and diagram, PNGs, idioms incl. Python, hygiene, naming, fail-fast, test evidence, RTL source lists, CI contract and scope) | host with the pinned Markdown renderer | all rc 0; em-dash: 0 findings over 183 added lines in 11 pages, `8b61b709..HEAD` | their own |
| the same 54 | container, CPython 3.12.3 | 45 rc 0; the other 9 need `rsvg-convert` or the pinned Markdown renderer, which the container lacks (they pass on the host) | — |

Not run: `act_ci.py --selftest` (`act_ci.py` unchanged since round 1, where it passed), `test_ctrl_nvm.py` (builds no stack), hosted CI and act (no push).

### Open risks and questions (round 2)

1. The boundary self-test now takes about 155 s on this host (268 preprocessings for the checkout, then the same for each of 28 controls); `firmware-unit` has a 45-minute budget.
2. The bench pin control runs `make` in `firmware-unit`; the hosted Ubuntu image ships it.
3. The gate relies on GCC's `-dU` (host gcc and the RV32 gcc, as in CI).
4. Hosted CI and act still have not run at any head of this lane; the act bootstrap note of round 1 stands.

## Round 2b

Assignment: #697 comment 6093389868. PR #705 conflicted with dev after F5 (#700) merged as `aef7ac66`, so this round merges dev into `697-consume` as a merge commit (no rebase), keeps F5's sources, tests, coverage rows and mutation entries, extends the boundary gate, the blob-hash pin check and the configuration derivation to what F5 added, and reruns the full bar at the merge head.
Base of the round: `38240ac4c251b2813384a9524e7c1cb43de520e8`. Merge head: `386b8e69e6f2fd0233e7a432e75c9d877c583a7b` (tree `adbf9c46415f9eed0d90da652020ab9ec78bb54f`), parents `38240ac4` and dev `aef7ac66605c4404900ce04cbaaeff88e41bb880`. Not pushed.
Status: REVIEW READY, posted on #697 as comment 6094033396.

### Commit

| Commit | Subject | Parents |
|---|---|---|
| `386b8e69e` | Merge dev aef7ac66 (F5 AECP) and judge its builders, units and tools at the TSN stack boundary and pin | `38240ac4c`, `aef7ac666` |

One commit, because the merge alone does not pass. F5's arms and wire comparison name `sw/firmware/ctrl/wire`, which #697 removed, so they cannot build; and the round-2 boundary gate at the bare merge state fails with `firmware rv32: app/ctrl_app_aecp.c does not preprocess: aecp_mbx.h: No such file or directory`. The assignment places the gate coverage under the resolution, so the merge commit carries it and every gate passes at the merge commit itself.

### Resolution (file:line at the merge head)

Conflicts (2):

- `sw/firmware/ctrl/README.md:46-47`: the lane's `acmp/` row (the adapter, the core is the stack's) and F5's `aecp/` row.
- `sw/firmware/ctrl/test/ctrl_srp_image.py`: `:37` `source_tree` kept (stack pin, legacy trees); `:47` F5's `aecp_inputs`, `verify_abi` and `arguments` kept; `:105` the cores through `source(...)`, from the stack; `:106` F5's `ctrl_aecp_image.c` for `--with-aecp`.

Auto-merged, no edit: `sw/firmware/ctrl/test/test_ctrl_firmware.py` (F5's AECP arms and campaign run after the gate's own pin check), `sw/firmware/gtest/coverage.ratchet` (F5's eight rows beside the stack's four; `fw_coverage.py --write` at the merge head rewrites it byte for byte), `docs/README.md`, `docs/design/MAILBOX_SPLIT.md`.

F5's builders onto the stack (they named the removed `wire/`):

- `sw/firmware/ctrl/test/aecp_arms.py:43` the application arm's cores through `source(...)`; `:62` and `:101` the stack's `include/` where `wire/` was; `:83` the test compile adds the stack's `tests/`, because `test_aecp.cpp` includes `acmp_fake.hpp`, now the stack's (token-identical to dev's copy: 2509 of 2509 tokens); `:122` the debug arm keeps the tree's stack.
- `sw/firmware/ctrl/test/aecp_wire.py:123` the stack's `include/`.

The pin check covers F5's tools. Inside the firmware gate the AECP arms and campaign already run after its pin check, and `ctrl_srp_image.py --with-aecp` runs it through `source_tree`. Run alone:

- `aecp_arms.py:141-147`, `aecp_mutants.py:510-518` and `aecp_wire.py:151-161` take `--stack` (the submodule by default) and run `stack_pin` before anything else, `REFUSED` and exit 2 otherwise; `aecp_mutants.py:469,476` the campaign builds the stack it is given; `aecp_wire.py:123` compiles with it.

The boundary covers F5 (`sw/firmware/ctrl/test/ctrl_boundary.py`):

- Units, by construction: `:108` `TEST_EQUIPMENT` and `:313` `firmware_dirs` (every directory of `sw/firmware/ctrl` but `host/` and `test/`, so `aecp/`), `:414` `firmware_units` (those, and every C source under `test/`, so `ctrl_aecp_image.c`): 51 units, 34 before.
- Include path: `:319` `search`, ctrl_build's include path then every firmware directory (`aecp/` as the AECP arms add it), on all three sides, so a stack source or test reaching `aecp.h` resolves and is named.
- Generated headers: `:421` `generated` runs every entity generator (`*/*_entity.py`: ADP, AECP, SRP) on the shipping entity; `:433` they are on the firmware's path (SRP's force-included as before), so the AECP image's `aecp_entity_gen.h` is read, not stood in for.
- Modes, nothing hand-listed: `:121` `BUILDER_NAMES`, `:175` `candidates` (every `*.py`, `*Makefile`, `*.mk` of the checkout, tracked or new, not ignored), `:184` `builders` (each that names `sw/firmware/ctrl` or `ctrl_build`, this gate excepted), `:125` `RESERVED` (C11 7.1.3 names are the implementation's, not modes), `:191` `modes`. At the head 32 files match and 10 carry flags; the universe is 18 macros: `ADP_TEST_COVERAGE`, `ADP_TEST_RELEASE`, `AECP_TEST_APP`, `AECP_TEST_MAILBOX`, `AECP_TEST_NVM`, `CTRL_APP_TEST_SRP`, `CTRL_IMAGE_SRP`, `CTRL_MBX_BASE` (two values), `CTRL_MBX_WFI`, `CTRL_REENTRY_ASSERT`, `LWSRP_MILAN`, `NDEBUG` (`-UNDEBUG`, `-DNDEBUG`), `NVM_DOCTORED_MAPIN`, `NVM_DOCTORED_NONAME`, `PP_TOP_IF2`, `PP_TOP_TIM_DEFAULTS`, `mrp_transmit`, `shlan_calloc`. F5's three `AECP_TEST_*` flags (`aecp_arms.py:21,32,42`) come from F5's file; `ctrl_image_runtime.py`'s `_LIBC` and `_YUGA_*` (Picolibc and compiler-rt) are reserved and dropped.
- 376 preprocessings (268 at round 2). F5's units explore `CTRL_REENTRY_ASSERT` (the AECP core tests it); `test/ctrl_aecp_image.c` nine configurations of `CTRL_IMAGE_SRP` and the modes its SRP composition tests (`round2b/configs.txt`).
- Controls: `:522` `Plant.builder` and `:526` `NEW_BUILDER` (a mode planted into a builder file the checkout does not hold); eight new boundary controls `:607-631`, three new pin controls `:736-765` (below).

Docs: `sw/firmware/ctrl/README.md:73,75` (the stack must not include the AECP core; AECP is the firmware's), `:85-97` (units, include path, derived builders, reserved names, 33 plants), `:104-109` (the AECP tools run the pin check; fifteen pin controls); `docs/testing/CI_WORKFLOWS.md:63`; `sw/firmware/ctrl/aecp/README.md:128-130` (the wire comparison builds with the stack's wire layer after its pin check).

### Boundary and pin controls (`round2b/boundary-selftest-head.log`)

`ctrl_boundary.py --require-rv32 --selftest` at the merge head: PASS, 0 findings, 376 preprocessings, 36 boundary controls (33 refused by name, 3 passing) and 15 pin controls, 0 misbehaved, then the stack's own 12; 4 min 20 s. New in round 2b:

| Control | Refused by |
|---|---|
| `src/acmp.c`: `mbx_hal.h` under `#ifdef AECP_TEST_APP` (F5's flag, read from `aecp_arms.py`) | `host [-DAECP_TEST_APP]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| `src/maap.c`: `ctrl_loop.h` under a mode written only in a new builder file nobody lists | `host [-DCTRL_PLANTED_BUILDER]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h` |
| `src/adp.c` includes the AECP core's `aecp.h` | `host: the stack's src/adp.c includes sw/firmware/ctrl/aecp/aecp.h` |
| `tests/test_adp.cpp` includes `aecp_mbx.h` | `tests: the stack's tests/test_adp.cpp includes sw/firmware/ctrl/aecp/aecp_mbx.h` |
| `aecp/aecp.c` reaches `src/acmp.c` by a relative path | `firmware: aecp/aecp.c includes tsn-c-stack/src/acmp.c, not one of the stack's public headers` |
| `app/ctrl_app_aecp.c` reaches the stack example's `adp_port.h` | `firmware: app/ctrl_app_aecp.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers` |
| `test/ctrl_aecp_image.c`: the SRP composition reaches `src/maap.c` | `firmware [-DCTRL_IMAGE_SRP]: test/ctrl_aecp_image.c includes tsn-c-stack/src/maap.c, not one of the stack's public headers` |
| a copy named `aecp/acmp.h` | `firmware: ctrl/aecp/acmp.h has the name of the stack's acmp.h` |
| pin: `aecp_arms.py --app` on an edited clone | `exit 2: REFUSED: tsn-c-stack differs from the pinned 1a9f651c: src/acmp.c` |
| pin: `aecp_mutants.py --shard 0 1000` on an edited clone | `exit 2: REFUSED: tsn-c-stack differs from the pinned 1a9f651c: src/acmp.c` |
| pin: `aecp_wire.py` (`VERILATOR=false`) with the clone's `include/wire.h` edited | `exit 2: REFUSED: tsn-c-stack differs from the pinned 1a9f651c: include/wire.h` |

The 28 boundary and 12 pin controls of round 2 are unchanged and all `[ok]`.

### Real-path probes (`round2b/realpath2b.txt`, script `round2b/realpath2b.sh`)

A disposable clone of the lane at the merge head with its own submodules; edits only in the clone's submodule or tree.

| Probe | Gate | Result |
|---|---|---|
| `src/acmp.c` edited | `aecp_arms.py --app`, `aecp_mutants.py`, `aecp_wire.py`, `ctrl_srp_image.py --with-aecp`, `test_ctrl_firmware.py --require-rv32` | each exit 2, `REFUSED: tsn-c-stack differs from the pinned 1a9f651c: src/acmp.c` |
| `src/adp.c` includes `aecp.h` (committed in the clone's submodule, gitlink staged) | `ctrl_boundary.py --require-rv32` | exit 1, `host: the stack's src/adp.c includes sw/firmware/ctrl/aecp/aecp.h` (and `rv32:`) |
| `src/acmp.c`: `mbx_hal.h` under `#ifdef AECP_TEST_APP` | same | exit 1, `host [-DAECP_TEST_APP]: ...` and `rv32 [-DAECP_TEST_APP]: ...` |
| `aecp/aecp_mbx.c` includes `../../../../third_party/tsn-c-stack/src/acmp.c` | same | exit 1, `firmware: aecp/aecp_mbx.c includes tsn-c-stack/src/acmp.c, not one of the stack's public headers` (and `firmware rv32:`) |

### RV32 images, dev `aef7ac66` and the merge head

Both fixtures at every shipped shape: `ctrl_image.py` at five shapes; `ctrl_srp_image.py` at five shapes, one and two interfaces, without SRP, with SRP and with AECP (F5's `--with-aecp`, which needs SRP). 35 of 35 ELF files are byte-identical; the manifests (`round2b/images-dev.sha256`, `round2b/images-head.sha256`) hash alike (`de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`). The 25 images without AECP also equal round 1's and round 2's line for line. `ctrl_image.py --base aef7ac66` (dev holds its own cores: the legacy path) reports `+0` in every section at both default shapes.

Runtime archives: the 25 earlier images use round 1's (`libc.a` `6c93b7f6…7d51`, `libcompiler_rt.a` `dff1861b…653c`). The AECP composition links compiler-rt's `__umoddi3`, which `ctrl_image_runtime.py` compiles with the pinned SDK's default `-fstack-protector-strong`, so with those archives the AECP image fails to link at dev and at the head alike (`undefined reference to __stack_chk_guard`). The ten AECP images use the freestanding archives F5 measured with (the same sources with `-fno-stack-protector`; `libc.a` sha256 `66ab39046f0c95f63fed511f044340906b35dde234ae12d278067fe0e01f2413`, `libcompiler_rt.a` sha256 `caeddc0417e8ecec3edf525e23cfd26f9fc08561bb92c550480c159ad2e626a7`), the same archives for dev and the head.

| Image (fixture/shape) | Runtime | sha256 dev aef7ac66 | sha256 head | |
|---|---|---|---|---|
| ctrl_image.py endstation_arty_4x4 | round 1 | `5232e40ecbc0d0ed97c31d645b51b3b7c6a2b0c4c407be2f6c1663175bf8d071` | `5232e40ecbc0d0ed97c31d645b51b3b7c6a2b0c4c407be2f6c1663175bf8d071` | identical |
| ctrl_image.py endstation_arty_8ch | round 1 | `6073714e3fe7dfb49b7c384b71777cb39d16fd1a642ebfbc300132e33d0bbaae` | `6073714e3fe7dfb49b7c384b71777cb39d16fd1a642ebfbc300132e33d0bbaae` | identical |
| ctrl_image.py endstation_arty_current | round 1 | `604f16d207c01178b30519ea5e9f93a1fb40ff51106b80e1df95b60831291260` | `604f16d207c01178b30519ea5e9f93a1fb40ff51106b80e1df95b60831291260` | identical |
| ctrl_image.py endstation_ax7101_1x1_tdm8 | round 1 | `c47a379013c3d2f518f11a09c46f42baf6c327038c97d5393c60ce4a7a863a6f` | `c47a379013c3d2f518f11a09c46f42baf6c327038c97d5393c60ce4a7a863a6f` | identical |
| ctrl_image.py endstation_ax7101_8x8 | round 1 | `da74a7ead4a80cdabe3a8659ac6dc2bd90f950f06ec892301f9743b9c70ec5f6` | `da74a7ead4a80cdabe3a8659ac6dc2bd90f950f06ec892301f9743b9c70ec5f6` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if1-aecp | freestanding | `7119c330a5a09e3fa10acdaea6fd489a8b637a3bddb370a2c9106ddaef31c402` | `7119c330a5a09e3fa10acdaea6fd489a8b637a3bddb370a2c9106ddaef31c402` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if1-nosrp | round 1 | `2daabe0c1b4367b6979d4d1938e38b13553051a10d2a891b64c9468a5b3bf182` | `2daabe0c1b4367b6979d4d1938e38b13553051a10d2a891b64c9468a5b3bf182` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if1-srp | round 1 | `2f735a17dd84b43d802b7bbfd48d3c4f08a4b26e222dae5b864ce944674b1a4d` | `2f735a17dd84b43d802b7bbfd48d3c4f08a4b26e222dae5b864ce944674b1a4d` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if2-aecp | freestanding | `e7e54606634495b04680b9bbef7ebae86c45ceb1b6cb940fbdd7068da20a0cbd` | `e7e54606634495b04680b9bbef7ebae86c45ceb1b6cb940fbdd7068da20a0cbd` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if2-nosrp | round 1 | `67cb0e1cc7f46a2c6d347983cd4305b3f97359555a7777738f02ae1da7699319` | `67cb0e1cc7f46a2c6d347983cd4305b3f97359555a7777738f02ae1da7699319` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if2-srp | round 1 | `621c0703c34f27a981841df62c6ed24b1bf42500b4c7c86948dab225655e0814` | `621c0703c34f27a981841df62c6ed24b1bf42500b4c7c86948dab225655e0814` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if1-aecp | freestanding | `c5c5800431ed4895baebe750f315c8de235de93cfc1ee80ce75bc5aa2245c3fd` | `c5c5800431ed4895baebe750f315c8de235de93cfc1ee80ce75bc5aa2245c3fd` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if1-nosrp | round 1 | `18b67362d222ee4cff516e6e552c322bac94b7e851fd8a147881ab2ba9e651d3` | `18b67362d222ee4cff516e6e552c322bac94b7e851fd8a147881ab2ba9e651d3` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if1-srp | round 1 | `935f86f68f4fcaaaddf20dc56e9088ef4a992210a522caca5a5aa581273ee05d` | `935f86f68f4fcaaaddf20dc56e9088ef4a992210a522caca5a5aa581273ee05d` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if2-aecp | freestanding | `cd8c0b4d8f1921485a2e4a19251d0b8dab089212138169837791dc8aab39e8a4` | `cd8c0b4d8f1921485a2e4a19251d0b8dab089212138169837791dc8aab39e8a4` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if2-nosrp | round 1 | `a5f36deb6c139f3783afd4c301e1a5f17d9d87345cbf4069cfd834ce2818e38a` | `a5f36deb6c139f3783afd4c301e1a5f17d9d87345cbf4069cfd834ce2818e38a` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if2-srp | round 1 | `991374a26c691848c44f1d800fed328f2cdd1ae713989b0e98226792317c64fb` | `991374a26c691848c44f1d800fed328f2cdd1ae713989b0e98226792317c64fb` | identical |
| ctrl_srp_image.py endstation_arty_current-if1-aecp | freestanding | `cbef444372c5b1ab51ea492bc44af83efa5811f9dbc4e9965002197aa254f1ec` | `cbef444372c5b1ab51ea492bc44af83efa5811f9dbc4e9965002197aa254f1ec` | identical |
| ctrl_srp_image.py endstation_arty_current-if1-nosrp | round 1 | `39f5ed170bd43de4e0d8fc4132bad14a90f9a041a91582f36a73c41cd1d132de` | `39f5ed170bd43de4e0d8fc4132bad14a90f9a041a91582f36a73c41cd1d132de` | identical |
| ctrl_srp_image.py endstation_arty_current-if1-srp | round 1 | `d0a54aa47af63e0f7e43da32ddd5f17d32a38532360037a3e3d86d7952570e78` | `d0a54aa47af63e0f7e43da32ddd5f17d32a38532360037a3e3d86d7952570e78` | identical |
| ctrl_srp_image.py endstation_arty_current-if2-aecp | freestanding | `b4281f6edf66a6845c0589679a8c055d309a2e5c600318cf80c706a37c5ed13f` | `b4281f6edf66a6845c0589679a8c055d309a2e5c600318cf80c706a37c5ed13f` | identical |
| ctrl_srp_image.py endstation_arty_current-if2-nosrp | round 1 | `1cb077c3c02ebe6b948cb20b28a0985730608e50d3edb5c384e71bb0010f1908` | `1cb077c3c02ebe6b948cb20b28a0985730608e50d3edb5c384e71bb0010f1908` | identical |
| ctrl_srp_image.py endstation_arty_current-if2-srp | round 1 | `8a8b61f8f88ad0d636b565d7b5262df9a64d7867bfbb30f6184de7a4987ee938` | `8a8b61f8f88ad0d636b565d7b5262df9a64d7867bfbb30f6184de7a4987ee938` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if1-aecp | freestanding | `ec1a28946369a724ff6aca045d23aaac8e0d9a882dc691923659203abc6343e2` | `ec1a28946369a724ff6aca045d23aaac8e0d9a882dc691923659203abc6343e2` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if1-nosrp | round 1 | `3ed7fdc5d3fa36afc8fb63f45795b56d7caa0844f7b91d583fc853a29130995f` | `3ed7fdc5d3fa36afc8fb63f45795b56d7caa0844f7b91d583fc853a29130995f` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if1-srp | round 1 | `ed04049b21806328b75701d6737c6b0c4ff4f88ae85438d7730a3285f0ac973e` | `ed04049b21806328b75701d6737c6b0c4ff4f88ae85438d7730a3285f0ac973e` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if2-aecp | freestanding | `4786d47a3fab4e0e05572edeead86b972da6a1dc154d80fe679088877215879b` | `4786d47a3fab4e0e05572edeead86b972da6a1dc154d80fe679088877215879b` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if2-nosrp | round 1 | `26039329ad2ed34cd83acfa8c39d0e2c0447bc6d2ccd97c22fa80ae9274578c5` | `26039329ad2ed34cd83acfa8c39d0e2c0447bc6d2ccd97c22fa80ae9274578c5` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if2-srp | round 1 | `c1142f8d5a18564dbaa791247820939d39ecdf5704eb32216e1ee89833e197ea` | `c1142f8d5a18564dbaa791247820939d39ecdf5704eb32216e1ee89833e197ea` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if1-aecp | freestanding | `e5e62290c8a77783fe03381d88e5333b33e6be5b732fa87ff521e98d7dd3789a` | `e5e62290c8a77783fe03381d88e5333b33e6be5b732fa87ff521e98d7dd3789a` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if1-nosrp | round 1 | `b5f79fd932cb17d6090158827f626710fa6a27a6d45eddb4281f67c7577f6989` | `b5f79fd932cb17d6090158827f626710fa6a27a6d45eddb4281f67c7577f6989` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if1-srp | round 1 | `4688e4c84ecc487a805126acefbdd5d4a9d7f8adf35cee0fd9775cad27521c21` | `4688e4c84ecc487a805126acefbdd5d4a9d7f8adf35cee0fd9775cad27521c21` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if2-aecp | freestanding | `ac0658cad589c9735c7397f2055cecfa8983366fc532fdeda74c79f507c5af6d` | `ac0658cad589c9735c7397f2055cecfa8983366fc532fdeda74c79f507c5af6d` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if2-nosrp | round 1 | `1503a953ad94e7863f516f11122b92e6151df59988f6deeccfbe054f77b5685a` | `1503a953ad94e7863f516f11122b92e6151df59988f6deeccfbe054f77b5685a` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if2-srp | round 1 | `5cd36014ec1857c35c133138cddc55d519f70ada9b477910e461e791b47a13b6` | `5cd36014ec1857c35c133138cddc55d519f70ada9b477910e461e791b47a13b6` | identical |

### Coverage, dev `aef7ac66` and the merge head

Same denominator: 30 files at both, every raw row identical; the four core files only change path. Both runs in the CI-parity container. `fw_coverage.py --selftest` 29 of 29 at the head; `--check` PASS (30 files) at both. `fw_coverage.py --write` at the head leaves the committed ratchet unchanged. Dev's ratchet still records `srp_mbx.c` at 515/515 while dev measures 514/514; the lane's ratchet records the measurement (round 1).

| File (dev -> head) | Raw lines dev / head | Raw branches dev / head | Ratchet dev | Ratchet head |
|---|---|---|---|---|
| `sw/firmware/ctrl/acmp/acmp.c -> third_party/tsn-c-stack/src/acmp.c` | 742/742 / 742/742 | 348/348 / 348/348 | 742/742 348/348 | 742/742 348/348 |
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 73/73 / 73/73 | 26/26 / 26/26 | 73/73 26/26 | 73/73 26/26 |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 / 38/38 | 10/10 / 10/10 | 38/38 10/10 | 38/38 10/10 |
| `sw/firmware/ctrl/adp/adp.c -> third_party/tsn-c-stack/src/adp.c` | 204/206 / 204/206 | 95/102 / 95/102 | 204/204 95/95 | 204/204 95/95 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 / 83/83 | 38/40 / 38/40 | 83/83 38/38 | 83/83 38/38 |
| `sw/firmware/ctrl/aecp/aecp.c` | 357/357 / 357/357 | 308/308 / 308/308 | 357/357 308/308 | 357/357 308/308 |
| `sw/firmware/ctrl/aecp/aecp_commands.c` | 424/424 / 424/424 | 362/362 / 362/362 | 424/424 362/362 | 424/424 362/362 |
| `sw/firmware/ctrl/aecp/aecp_image.c` | 77/77 / 77/77 | 80/80 / 80/80 | 77/77 80/80 | 77/77 80/80 |
| `sw/firmware/ctrl/aecp/aecp_maps.c` | 222/222 / 222/222 | 290/290 / 290/290 | 222/222 290/290 | 222/222 290/290 |
| `sw/firmware/ctrl/aecp/aecp_mbx.c` | 101/101 / 101/101 | 40/40 / 40/40 | 101/101 40/40 | 101/101 40/40 |
| `sw/firmware/ctrl/aecp/aecp_nvm.c` | 102/102 / 102/102 | 86/86 / 86/86 | 102/102 86/86 | 102/102 86/86 |
| `sw/firmware/ctrl/aecp/aecp_state.c` | 63/63 / 63/63 | 69/69 / 69/69 | 63/63 69/69 | 63/63 69/69 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 / 42/43 | 40/44 / 40/44 | 42/42 40/40 | 42/42 40/40 |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | 107/107 / 107/107 | 64/64 / 64/64 | 107/107 64/64 | 107/107 64/64 |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 / 82/82 | 62/62 / 62/62 | 82/82 62/62 | 82/82 62/62 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 / 101/101 | 62/62 / 62/62 | 101/101 62/62 | 101/101 62/62 |
| `sw/firmware/ctrl/maap/maap.c -> third_party/tsn-c-stack/src/maap.c` | 209/209 / 209/209 | 140/140 / 140/140 | 209/209 140/140 | 209/209 140/140 |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 / 39/39 | 18/18 / 18/18 | 39/39 18/18 | 39/39 18/18 |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 / 98/98 | 60/60 / 60/60 | 98/98 60/60 | 98/98 60/60 |
| `sw/firmware/ctrl/mbx/mbx.c` | 189/189 / 189/189 | 74/74 / 74/74 | 189/189 74/74 | 189/189 74/74 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 / 15/15 | 12/12 / 12/12 | 15/15 12/12 | 15/15 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 / 10/10 | 0/0 / 0/0 | 10/10 0/0 | 10/10 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 / 19/19 | 6/6 / 6/6 | 19/19 6/6 | 19/19 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 / 99/99 | 60/60 / 60/60 | 99/99 60/60 | 99/99 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 / 22/22 | 6/6 / 6/6 | 22/22 6/6 | 22/22 6/6 |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 514/514 / 514/514 | 478/478 / 478/478 | 515/515 478/478 | 514/514 478/478 |
| `sw/firmware/ctrl/wire/wire.h -> third_party/tsn-c-stack/include/wire.h` | 10/10 / 10/10 | 2/2 / 2/2 | 10/10 2/2 | 10/10 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 / 198/199 | 106/110 / 106/110 | 198/198 106/106 | 198/198 106/106 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 / 434/434 | 259/266 / 259/266 | 434/434 259/259 | 434/434 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 / 100/100 | 63/64 / 63/64 | 100/100 63/63 | 100/100 63/63 |

### Mutation campaigns, dev `aef7ac66` and the merge head

| Campaign | dev `aef7ac66` | head |
|---|---|---|
| control (`ctrl_mutants.py` with ACMP, ACMP review and MAAP tables) | 471 of 471 | 471 of 471 |
| AECP (`aecp_mutants.py`, F5) | 74 of 74 | 74 of 74 |
| SRP, two interfaces | 169 caught, 0 escaped | 169 caught, 0 escaped |
| SRP, one-interface subset | 68 caught, 0 escaped | 68 caught, 0 escaped |
| lwSRP pin arms | 2 of 2 | 2 of 2 |
| tests named by no defect | 0 | 0 |
| MAAP differential | 16 of 16 | 16 of 16 (pin first) |
| mailbox bench quick mutants | 5 of 5 | 5 of 5 (pin before the firmware build) |
| AECP wire oracle controls | 11 (one interface); 11 and 11 (two) | the same |
| saved-state store (`test_ctrl_nvm.py --require-rv32 --self-test --jobs 4`) | 109 of 109, 5 shapes, 435 tests | 109 of 109, 5 shapes, 435 tests |
| tally listener (`tally_selftest.py --mutants`) | 18 of 18 | 18 of 18 |
| boundary gate (this lane) | — | 36 boundary, 15 pin, the stack's own 12 |

The firmware gate's 843 verdict lines are identical by name between dev and the head (59 arms: dev's 51 and F5's eight). Logs: dev 311,497 bytes, sha256 `8114885417617a805794f574c2d9f8ca11726c0e426ac78869abce52a290d085`; head 310,994 bytes, sha256 `985c0b7e90b491d3bdeaa9aaf7f9a787d8082695d41c8702b4e543e10b5de6bc`. F5 changed none of the inputs of the control and SRP tables, the MAAP differential or the mailbox bench (`git diff 8b61b709 aef7ac66` on them is empty).

### Gates at the merge head

| Gate | Where | Result |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | container | PASS, prints `tsn-c-stack at 1a9f651c…` first; 59 arms; campaigns above; 28 min 36 s (dev 27 min 16 s) |
| `fw_coverage.py --selftest`; `--check --jobs 4`; `--write` | container | 29 of 29; PASS (30 files); ratchet unchanged |
| `ctrl_boundary.py --require-rv32 --selftest` | host | PASS, controls above |
| `ctrl_boundary.py --require-rv32` on the bare merge state (round-2 gate) | host | exit 1 (the reason for one commit, above) |
| images, 35 | host, pinned SDK | 35 of 35 identical to dev |
| `ctrl_image.py --base aef7ac66` | host | `+0` everywhere |
| `aecp_wire.py --interfaces 1` (reference the pinned `protocol-processor`) | host, Verilator 5.050 | PASS, 142 observations, 11 controls; `verdict.json` and the observation log byte-identical to dev's |
| `aecp_wire.py --interfaces 2` (reference `c9f74b68`, exported read-only with `git archive`) | host, Verilator 5.050 | PASS, 294 observations, 11 and 11 controls; identical to dev's |
| `maap_differential.py --self-test` | host, Verilator 5.050 | the pin, then 16/16 |
| `make -C tb/verilator/mbx` | host, Verilator 5.050 | the pin before the firmware build; 382, 427, 32, 384, 429, 369 checks, 0 failures; 5 of 5 (dev the same) |
| `tally_selftest.py`, `fw_rv32_selftest.py --require-rv32`, `ctrl_image_selftest.py --require-rv32` | container | 18 of 18; 17 checks; 33 checks |
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 4`, then `tally_selftest.py --mutants` | container | OK, 5 shapes, 435 tests, 109 of 109 planted defects; 18 of 18 listener defects; the same verdicts by name as dev |
| `ci_events.py --check`, `--selftest` | container | OK, 1757 items; PASS, 2387 arms |
| docs job, 54 repository commands | host, pinned Markdown renderer | all rc 0; `check_em_dash --base aef7ac66`: 0 findings over 192 added lines in 12 pages |
| the same 54 as the hosted docs job runs them | fresh clone: no submodule, then only `verilog-axis`, `protocol-processor`, `gptp-processor` | all rc 0 (the docs-only gates also with no submodule at all) |
| `check_py_idiom.py` | host | 0 over-long lines (two wrapped before the commit) |

Not run: `act_ci.py --selftest` (unchanged since round 1, where it passed), hosted CI and act (no push).

### Open risks and questions (round 2b)

1. The runtime builder `ctrl_image_runtime.py` (dev) compiles compiler-rt with the pinned SDK's default stack protector, so the archives it builds cannot link `ctrl_srp_image.py --with-aecp` at dev or here. The AECP images above use the `-fno-stack-protector` archives F5 measured with. This is dev's, unchanged by this lane, and worth its own Issue.
2. The boundary self-test now takes about 4 min 20 s here (round 2: 155 s); `firmware-unit` has a 45-minute budget, and the firmware gate itself takes about 28 min on this host.
3. The builder rule is "names `sw/firmware/ctrl` or `ctrl_build`": a file that compiles the firmware without naming either would be missed. Every builder at the head names one; 22 matching files carry no flag.
4. Hosted CI and act still have not run at any head of this lane.

## Round 3

Assignment: #697 comment 6094873968, answering [R584-2](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6094643793) and [R585-2](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6094869698), both NEGATIVE on the same two MINOR gaps (F1, F2), plus R585-2-S1, required now. Earlier rulings: pin 6092176555, round 2 6092628778, round 2b 6093389868.
Base of the round: `386b8e69e6f2fd0233e7a432e75c9d877c583a7b`. New commits only (no rebase, no amend); not pushed, so PR #705 still shows the round-1 head.
Head: `d1b22e804158cbcb33fa12116d60e982f9a4c55b` (tree `bc319e0b59aa24fb561d51a13da5da7b43a9d676`).
Status: REVIEW READY, posted on #697 as comment [6095730057](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6095730057).

### Commits

| Commit | Subject |
|---|---|
| `76c0e27c3` | Make the pin check a prerequisite of every mailbox bench target that compiles against the TSN stack |
| `36699f6c9` | Judge each unit at the TSN stack boundary as its builders compile it, and run every bench target that reaches the stack against a poisoned one |
| `d1b22e804` | Refuse the TSN stack boundary gate by name when the end-station builder cannot load a shape |

One-line subjects, no body, no trailers, configured identity. No firmware source, header, test, mutation table, coverage row or build flag changes: `git diff --name-only 386b8e69 d1b22e804` is the bench Makefile and README, the gate (`ctrl_boundary.py`, new `ctrl_configs.py` and `ctrl_pin.py`), `ctrl_image.py` (one function extracted, the same flags and headers), `sw/firmware/ctrl/README.md`, `docs/testing/CI_WORKFLOWS.md` and a comment in `.github/workflows/rtl-fast.yml`. The third commit exists because R584-2's probe clone lacked `gptp-processor`: the gate now takes every shape through the end-station builder, which needs it, and crashed (exit 1) where it should refuse; it now exits 2 naming the submodule (`round3/refusal-without-gptp-processor.log`). `firmware-unit` initialises it.

### Item 1 — R584-2-F1 = R585-2-F1: each unit judged as its builders compile it

Nothing is hand-listed: the gate's `FIRMWARE_DEFINES` (`-DNDEBUG`, `-DCTRL_MBX_BASE=0x80000000u`, `-DIMAGE_SINKS=1u`, `-DIMAGE_SOURCES=1u`, `-DLWSRP_MILAN=1`) and `SRP_ENTITY` are gone. The firmware side's default build is the compiler's own flags only (the host's `-std=c11`; RV32's `RV32_FLAGS`), and every macro is explored in each state a builder leaves it in, undefined included. What a builder varies is a dimension (`ctrl_configs.py:102` `Dim`), each derived from the builders:

| Dimension | Derived from | Alternatives at the head | File:line |
|---|---|---|---|
| Language | Every firmware unit is C (every builder compiles the sources as C). A firmware unit that a C++ source a builder names reaches is C++ too: `cxx_sources` reads every `.cpp`/`.cc`/`.cxx` literal or Makefile word of every builder and resolves it beside the builder, in `test/`, in the stack, the processor or the checkout; `cxx_units` follows every `#include` line of them as text, every branch alike, against every directory a builder searches; an `#include` whose operand a macro computes is a finding (text cannot follow it). C++ units are preprocessed with the arms' test flags (`fw_gtest.CXX_FLAGS`) and include path (the stack's `tests/` on it). | C, and C++ for 24 of the 51 units (every header a test or bench reaches) | `ctrl_configs.py:392`; `ctrl_boundary.py:435,467,509-511` |
| Build modes | Every `-D`/`-U` flag a builder writes, one argument (`"-DNAME"`) or two (`"-D", "NAME"` adjacent in a list, tuple or call; two words of a Makefile line) | 18 macros, unchanged | `ctrl_configs.py:155,183,218` |
| Values | A flag a builder computes (an f-string, or a bare `-D`/`-U` before one) is a value. `IMAGE_SINKS`/`IMAGE_SOURCES` are taken from the image builder's own `ctrl_image.shape_build` (`ctrl_image.py:339`, which `measure` now calls, `:359`) at every shipped config; undefined is every other builder's state. Every other computed macro (7: `AECP_TEST_INTERFACES`, `AECP_WIRE_INTERFACES`, `FW_GTEST_LABEL`, `NVM_TALLY_SHAPE`, `PP_ENTITY_CAPS`, `SRP_EXPECT_SINKS`, `SRP_EXPECT_SOURCES`) is a finding wherever it decides what a judged unit reads. A flag whose macro is computed too refuses the gate. | undefined; 5/5, 2/1, 2/2, 9/9 (the shapes' pairs, deduplicated) | `ctrl_configs.py:148,341,349` |
| Shapes | Every shipped config (`configs/*.yaml`, each a shape `ctrl_image.py --shape` and `ctrl_srp_image.py --config` take): `ctrl_image.shape_build` writes the store's headers, and every entity generator (`*/*_entity.py`) its own, as the arms and both image fixtures run them; searched first for a quoted include (`-iquote`), as the image builder orders them. The arms' default entity (`srp_arms.DEFAULT_ENTITY`) is the default build. | 5 shapes | `ctrl_configs.py:256,262-268,306` |
| SRP shape header | Force-included (`-include srp_entity_gen.h`), as the SRP builds compile every unit, the stack's cores included, or left out, as the others do; on the stack's side the forced header is not a dependency of the stack. | left out; force-included | `ctrl_configs.py:320`; `ctrl_boundary.py:358` |
| Mailbox contract | The tracked contract, and the variant `gen_mailbox.py --variant-interfaces N` writes for every N it admits, counting up from one until it refuses (it refuses 3: the register space), force-included ahead of the tracked one, whose include guard then keeps it out (the variant differs only in `MBX_N_IF`). | tracked (1 interface); 2 interfaces | `ctrl_configs.py:256,330` |

Exploration (`ctrl_boundary.py:247` `explore`): the compiler's `-dU` reports the macros a preprocessing tests or expands; `deciding` (`:194`) keeps those that the conditionals and `#include` lines of the files it read name, or that their definitions name in turn (a macro only code expands cannot change what is read). A dimension is explored once one of its macros decides a read (`Dim.shown`), every combination of the explored dimensions' alternatives, every other at its seed (defined), until no new one appears. `-fdirectives-only` was tried for this and rejected: with it, GCC 16's `-dU` drops tests made after a file's last `#include` and some made in the main file (scratch probes, not in the tree). A configuration that stops on an `#error` is one no builder compiles: it is not a finding, and what it read is still judged from the dependency list GCC writes in full (`preprocess`, `:217`); a unit that stops in every configuration is a finding (`common`, `:297`).

### Item 2 — R584-2-F2 = R585-2-F2: no build target reaches the stack unpinned

- `tb/verilator/mbx/Makefile:91` `run-cosim: obj_fw/libctrlfw.a | stack-pin` and `:115` `run-if2: if2-gen | stack-pin` (with `:82` `obj_fw/libctrlfw.a: ... | stack-pin`): every target whose recipe compiles with `$(FW_INC)` has `stack-pin` as a prerequisite. Comment `:43-49`.
- Static rule, every run (`ctrl_pin.py:122` `stack_targets`, `:146` `makefile_findings`): for every Makefile builder, make's own database (`make -p`, `:88`) gives the targets and their prerequisites, and its dry run (`make -n -B --trace`, `:107`) each target's own recipe lines, with `STACK_DIR` a link to the submodule. A target whose own recipe names the stack must have a target that runs `ctrl_build.py --stack-pin` among its prerequisites; a recipe naming the checkout's `third_party/tsn-c-stack` instead of `STACK_DIR` is refused too.
- Self-test (`ctrl_pin.py:179` `bench_arms`): every target whose dry run reaches the stack is run for real in a scratch copy of the bench directory (`mirror`, `:156`: the directory's files copied, every other entry of the checkout linked) with the system compilers, a simulator that builds nothing, and `STACK_DIR` a clone whose `include/wire.h` ends in `#error PIN-POISON`. Each must exit non-zero naming `include/wire.h` from the pin check, and `PIN-POISON` must never appear. At the head the derived targets are `run-cosim`, `obj_fw/libctrlfw.a`, `stack-pin`, `all` and `run-if2`; the pin target passes the unpoisoned clone; a planted copy of the Makefile with `run-if2: if2-gen` is refused by name.
- `pin_controls` moved from `ctrl_boundary.py` to `ctrl_pin.py:227` with its thirteen other controls unchanged; the derived bench arms replace its two hand-written bench controls.

### Item 3 — R585-2-S1: a mode written as two arguments

`ctrl_configs.py:155` `python_flags`: a bare `"-D"`/`"-U"` followed, in a list, a tuple or a call's arguments, by a literal macro is the one-argument flag; followed by an f-string, a computed value; followed by any other expression, a refusal. `:183` `makefile_flags`: two words of a logical line (continuations joined). Controls: a Python builder writing `("-D", "CTRL_SPLIT_MODE")` and a new Makefile builder writing `cc -D CTRL_SPLIT_MAKE`, each refused by name.

### Docs

`sw/firmware/ctrl/README.md:85-126` (units judged as builders compile them: language, modes, values, shapes and the builder they need, the SRP shape header, the contract; the deciding macros; `#error` configurations; 42 + 3 controls; the Makefile rule; twenty pin controls and the derived bench targets); `tb/verilator/mbx/README.md:12-20`; `docs/testing/CI_WORKFLOWS.md:58-66,197-201`; `.github/workflows/rtl-fast.yml:287-293`; the module docstrings of `ctrl_boundary.py`, `ctrl_configs.py` and `ctrl_pin.py`.

### Planted controls added in round 3 (`round3/boundary-selftest-head.log`)

| Control | Refused by |
|---|---|
| R584-2's probe: `test/rv32_image/image_main.c`, `#if IMAGE_SINKS > 1u` then the stack example's `adp_port.h` then `#error PROBE-REACHED` | `firmware [-DIMAGE_SINKS=2u -DIMAGE_SOURCES=1u]: test/rv32_image/image_main.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers` (and `firmware rv32 [...]`) |
| R585-2's n1: `acmp/acmp_mbx.h`, `#include "acmp_fake.hpp"` in its `#ifdef __cplusplus` region | `firmware c++: acmp/acmp_mbx.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers` (and the C++ units including it) |
| `test/ctrl_aecp_image.c`: a stack source under `AECP_ENTITY_MAPS > 8u`, which only the 8x8 shape's generated header gives | `firmware [shape=endstation_ax7101_8x8]: test/ctrl_aecp_image.c includes tsn-c-stack/src/acmp.c` |
| `maap/maap_mbx.c`: a stack source under `#ifdef CTRL_SRP_SOURCES` (the force-included SRP shape header) | `firmware [-include srp_entity_gen.h]: maap/maap_mbx.c includes tsn-c-stack/src/maap.c` |
| `adp/adp_mbx.c`: a stack source under `#if MBX_N_IF > 1u` | `firmware [interfaces=2]: adp/adp_mbx.c includes tsn-c-stack/src/adp.c` |
| `acmp/acmp_mbx.c`: a stack source under `#ifndef LWSRP_MILAN` (what the gate's old default hid) | `firmware: acmp/acmp_mbx.c includes tsn-c-stack/src/acmp.c, not one of the stack's public headers` |
| `aecp/aecp.c` tests `AECP_TEST_INTERFACES`, a value only the AECP arms compute | `firmware [-DAECP_TEST_INTERFACES]: aecp/aecp.c tests AECP_TEST_INTERFACES, a value sw/firmware/ctrl/test/aecp_arms.py computes at run time, which the boundary has none of` |
| `ctrl_arms.py` writes `("-D", "CTRL_SPLIT_MODE")`; `src/adp.c` includes `mbx_hal.h` under it | `host [-DCTRL_SPLIT_MODE]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| a new `planted.mk` writes `cc -D CTRL_SPLIT_MAKE`; `src/maap.c` includes `ctrl_loop.h` under it | `host [-DCTRL_SPLIT_MAKE]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h` |
| pin: `tb/verilator/mbx/Makefile` `make stack-pin`, the pinned clone | `exit 0: tsn-c-stack at 1a9f651c…` |
| pin: `make run-cosim`, `make obj_fw/libctrlfw.a`, `make stack-pin`, `make all`, `make run-if2`, each against the poisoned clone | each `exit 2: REFUSED: tsn-c-stack differs from the pinned 1a9f651c: include/wire.h`, no `PIN-POISON` |
| pin: a planted Makefile whose `run-if2` lacks `stack-pin` | `Makefile: run-if2 builds against tsn-c-stack without the pin check (stack-pin) as a prerequisite` |

The 36 boundary controls of round 2b are kept, each with its needle unchanged, and all `[ok]`; the 13 non-bench pin controls likewise. Totals: 45 boundary controls (42 refused by name, 3 passing) and 20 pin controls.

### Reviewers' probes at the head (`round3/probes/`)

Each published probe script was run unchanged from the reviewers' packets at `2d9b8d11`, against clean clones of `d1b22e804` with `tsn-c-stack`, `lwSRP`, `protocol-processor`, `verilog-axis` and `gptp-processor` initialised.

| Probe | At `386b8e69` (the reviews) | At `d1b22e804` |
|---|---|---|
| R584-2 `boundary_probes.py` (10 probes, the copy's own gate) | 8 CAUGHT; the `IMAGE_SINKS > 1u` and two-token probes passed the gate | 8 CAUGHT; both former gap probes refused (exit 1) by findings naming them: `firmware [-DIMAGE_SINKS=2u -DIMAGE_SOURCES=1u]: test/rv32_image/image_main.c includes tsn-c-stack/examples/adp_port.h, ...` and `host [-DCTRL_TWO_TOKEN_MODE]: the stack's src/maap.c includes sw/firmware/ctrl/mbx/mbx_hal.h` |
| R584-2 `shape_probe.sh` | gate rc 0 | gate rc 1, the same `[-DIMAGE_SINKS=2u -DIMAGE_SOURCES=1u]` finding for the stack example by its checkout path; `ctrl_image.py` still compiles the branch at both shapes (`PROBE-REACHED`) |
| R584-2 `pin_probes.sh` (S0 to S6) | 44 of 44 refused; S6 `make run-if2` compiled the poisoned `wire.h` | 44 of 44 refused; S6 rc 2, `REFUSED: tsn-c-stack differs from the pinned 1a9f651c: include/wire.h`; clone restored |
| R585-2 `boundary_probes.py all` (11 probes, the gate's own `planted`/`judge`) | n1, n2, n3, n4 ESCAPED | 11 of 11 CAUGHT: n1 `firmware c++: acmp/acmp_mbx.h includes tsn-c-stack/tests/acmp_fake.hpp`, n2 `firmware c++: adp/adp_mbx.h includes tsn-c-stack/src/adp.c`, n3 `firmware [-DIMAGE_SINKS=2u -DIMAGE_SOURCES=1u]: test/rv32_image/image_main.c includes tsn-c-stack/src/acmp.c`, n4 `host [-DCTRL_SPLIT_MODE]: ...` |
| R585-2 `pin_probes.sh` (EDIT, HIDE, UNTRACKED, WIRE) | 26 of 27 refused; `WIRE-mbx_run_if2` compiled the poisoned header | 27 of 27 refused, `WIRE-mbx_run_if2` rc 2 naming `include/wire.h`; clone restored |

### RV32 images, dev `aef7ac66` and the round-3 head

Built at `36699f6c9` (`ctrl_image.py` and `ctrl_srp_image.py` are unchanged in `d1b22e804`) with `round3/images3.sh` (round 2b's script): `ctrl_image.py` at five shapes; `ctrl_srp_image.py` at five shapes, one and two interfaces, without SRP, with SRP and with AECP; the same pinned SDK and runtime archives as round 2b (`libc.a` `6c93b7f6…7d51` and `libcompiler_rt.a` `dff1861b…653c`; for AECP the `-fno-stack-protector` pair `66ab3904…2413` and `caeddc04…26a7`). 35 of 35 ELF files are byte-identical to dev's; the manifest `round3/images-head.sha256` is byte-identical to round 2b's dev and head manifests (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`). `ctrl_image.py --base aef7ac66` at the head: `+0` in every section at both default shapes (`round3/ctrl-image-base-aef7ac66.log`).

| Image (fixture shape-interfaces-composition) | sha256 dev `aef7ac66` | sha256 head | |
|---|---|---|---|
| ctrl_image.py endstation_arty_4x4 | `5232e40ecbc0d0ed97c31d645b51b3b7c6a2b0c4c407be2f6c1663175bf8d071` | `5232e40ecbc0d0ed97c31d645b51b3b7c6a2b0c4c407be2f6c1663175bf8d071` | identical |
| ctrl_image.py endstation_arty_8ch | `6073714e3fe7dfb49b7c384b71777cb39d16fd1a642ebfbc300132e33d0bbaae` | `6073714e3fe7dfb49b7c384b71777cb39d16fd1a642ebfbc300132e33d0bbaae` | identical |
| ctrl_image.py endstation_arty_current | `604f16d207c01178b30519ea5e9f93a1fb40ff51106b80e1df95b60831291260` | `604f16d207c01178b30519ea5e9f93a1fb40ff51106b80e1df95b60831291260` | identical |
| ctrl_image.py endstation_ax7101_1x1_tdm8 | `c47a379013c3d2f518f11a09c46f42baf6c327038c97d5393c60ce4a7a863a6f` | `c47a379013c3d2f518f11a09c46f42baf6c327038c97d5393c60ce4a7a863a6f` | identical |
| ctrl_image.py endstation_ax7101_8x8 | `da74a7ead4a80cdabe3a8659ac6dc2bd90f950f06ec892301f9743b9c70ec5f6` | `da74a7ead4a80cdabe3a8659ac6dc2bd90f950f06ec892301f9743b9c70ec5f6` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if1-aecp | `7119c330a5a09e3fa10acdaea6fd489a8b637a3bddb370a2c9106ddaef31c402` | `7119c330a5a09e3fa10acdaea6fd489a8b637a3bddb370a2c9106ddaef31c402` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if1-nosrp | `2daabe0c1b4367b6979d4d1938e38b13553051a10d2a891b64c9468a5b3bf182` | `2daabe0c1b4367b6979d4d1938e38b13553051a10d2a891b64c9468a5b3bf182` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if1-srp | `2f735a17dd84b43d802b7bbfd48d3c4f08a4b26e222dae5b864ce944674b1a4d` | `2f735a17dd84b43d802b7bbfd48d3c4f08a4b26e222dae5b864ce944674b1a4d` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if2-aecp | `e7e54606634495b04680b9bbef7ebae86c45ceb1b6cb940fbdd7068da20a0cbd` | `e7e54606634495b04680b9bbef7ebae86c45ceb1b6cb940fbdd7068da20a0cbd` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if2-nosrp | `67cb0e1cc7f46a2c6d347983cd4305b3f97359555a7777738f02ae1da7699319` | `67cb0e1cc7f46a2c6d347983cd4305b3f97359555a7777738f02ae1da7699319` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if2-srp | `621c0703c34f27a981841df62c6ed24b1bf42500b4c7c86948dab225655e0814` | `621c0703c34f27a981841df62c6ed24b1bf42500b4c7c86948dab225655e0814` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if1-aecp | `c5c5800431ed4895baebe750f315c8de235de93cfc1ee80ce75bc5aa2245c3fd` | `c5c5800431ed4895baebe750f315c8de235de93cfc1ee80ce75bc5aa2245c3fd` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if1-nosrp | `18b67362d222ee4cff516e6e552c322bac94b7e851fd8a147881ab2ba9e651d3` | `18b67362d222ee4cff516e6e552c322bac94b7e851fd8a147881ab2ba9e651d3` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if1-srp | `935f86f68f4fcaaaddf20dc56e9088ef4a992210a522caca5a5aa581273ee05d` | `935f86f68f4fcaaaddf20dc56e9088ef4a992210a522caca5a5aa581273ee05d` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if2-aecp | `cd8c0b4d8f1921485a2e4a19251d0b8dab089212138169837791dc8aab39e8a4` | `cd8c0b4d8f1921485a2e4a19251d0b8dab089212138169837791dc8aab39e8a4` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if2-nosrp | `a5f36deb6c139f3783afd4c301e1a5f17d9d87345cbf4069cfd834ce2818e38a` | `a5f36deb6c139f3783afd4c301e1a5f17d9d87345cbf4069cfd834ce2818e38a` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if2-srp | `991374a26c691848c44f1d800fed328f2cdd1ae713989b0e98226792317c64fb` | `991374a26c691848c44f1d800fed328f2cdd1ae713989b0e98226792317c64fb` | identical |
| ctrl_srp_image.py endstation_arty_current-if1-aecp | `cbef444372c5b1ab51ea492bc44af83efa5811f9dbc4e9965002197aa254f1ec` | `cbef444372c5b1ab51ea492bc44af83efa5811f9dbc4e9965002197aa254f1ec` | identical |
| ctrl_srp_image.py endstation_arty_current-if1-nosrp | `39f5ed170bd43de4e0d8fc4132bad14a90f9a041a91582f36a73c41cd1d132de` | `39f5ed170bd43de4e0d8fc4132bad14a90f9a041a91582f36a73c41cd1d132de` | identical |
| ctrl_srp_image.py endstation_arty_current-if1-srp | `d0a54aa47af63e0f7e43da32ddd5f17d32a38532360037a3e3d86d7952570e78` | `d0a54aa47af63e0f7e43da32ddd5f17d32a38532360037a3e3d86d7952570e78` | identical |
| ctrl_srp_image.py endstation_arty_current-if2-aecp | `b4281f6edf66a6845c0589679a8c055d309a2e5c600318cf80c706a37c5ed13f` | `b4281f6edf66a6845c0589679a8c055d309a2e5c600318cf80c706a37c5ed13f` | identical |
| ctrl_srp_image.py endstation_arty_current-if2-nosrp | `1cb077c3c02ebe6b948cb20b28a0985730608e50d3edb5c384e71bb0010f1908` | `1cb077c3c02ebe6b948cb20b28a0985730608e50d3edb5c384e71bb0010f1908` | identical |
| ctrl_srp_image.py endstation_arty_current-if2-srp | `8a8b61f8f88ad0d636b565d7b5262df9a64d7867bfbb30f6184de7a4987ee938` | `8a8b61f8f88ad0d636b565d7b5262df9a64d7867bfbb30f6184de7a4987ee938` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if1-aecp | `ec1a28946369a724ff6aca045d23aaac8e0d9a882dc691923659203abc6343e2` | `ec1a28946369a724ff6aca045d23aaac8e0d9a882dc691923659203abc6343e2` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if1-nosrp | `3ed7fdc5d3fa36afc8fb63f45795b56d7caa0844f7b91d583fc853a29130995f` | `3ed7fdc5d3fa36afc8fb63f45795b56d7caa0844f7b91d583fc853a29130995f` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if1-srp | `ed04049b21806328b75701d6737c6b0c4ff4f88ae85438d7730a3285f0ac973e` | `ed04049b21806328b75701d6737c6b0c4ff4f88ae85438d7730a3285f0ac973e` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if2-aecp | `4786d47a3fab4e0e05572edeead86b972da6a1dc154d80fe679088877215879b` | `4786d47a3fab4e0e05572edeead86b972da6a1dc154d80fe679088877215879b` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if2-nosrp | `26039329ad2ed34cd83acfa8c39d0e2c0447bc6d2ccd97c22fa80ae9274578c5` | `26039329ad2ed34cd83acfa8c39d0e2c0447bc6d2ccd97c22fa80ae9274578c5` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if2-srp | `c1142f8d5a18564dbaa791247820939d39ecdf5704eb32216e1ee89833e197ea` | `c1142f8d5a18564dbaa791247820939d39ecdf5704eb32216e1ee89833e197ea` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if1-aecp | `e5e62290c8a77783fe03381d88e5333b33e6be5b732fa87ff521e98d7dd3789a` | `e5e62290c8a77783fe03381d88e5333b33e6be5b732fa87ff521e98d7dd3789a` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if1-nosrp | `b5f79fd932cb17d6090158827f626710fa6a27a6d45eddb4281f67c7577f6989` | `b5f79fd932cb17d6090158827f626710fa6a27a6d45eddb4281f67c7577f6989` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if1-srp | `4688e4c84ecc487a805126acefbdd5d4a9d7f8adf35cee0fd9775cad27521c21` | `4688e4c84ecc487a805126acefbdd5d4a9d7f8adf35cee0fd9775cad27521c21` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if2-aecp | `ac0658cad589c9735c7397f2055cecfa8983366fc532fdeda74c79f507c5af6d` | `ac0658cad589c9735c7397f2055cecfa8983366fc532fdeda74c79f507c5af6d` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if2-nosrp | `1503a953ad94e7863f516f11122b92e6151df59988f6deeccfbe054f77b5685a` | `1503a953ad94e7863f516f11122b92e6151df59988f6deeccfbe054f77b5685a` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if2-srp | `5cd36014ec1857c35c133138cddc55d519f70ada9b477910e461e791b47a13b6` | `5cd36014ec1857c35c133138cddc55d519f70ada9b477910e461e791b47a13b6` | identical |

### Coverage at the round-3 head

`fw_coverage.py --check --jobs 4` in the CI-parity container at `36699f6c9` (the coverage inputs are unchanged in `d1b22e804`): PASS (30 files); `--selftest` 29 of 29. Every raw row is identical to round 2b's head, whose rows equal dev's raw counts (see the [round 2b table](#coverage-dev-aef7ac66-and-the-merge-head)); `coverage.ratchet` is unchanged.

| File | Lines | Branches |
|---|---|---|
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 73/73 | 26/26 |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 | 10/10 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 |
| `sw/firmware/ctrl/aecp/aecp.c` | 357/357 | 308/308 |
| `sw/firmware/ctrl/aecp/aecp_commands.c` | 424/424 | 362/362 |
| `sw/firmware/ctrl/aecp/aecp_image.c` | 77/77 | 80/80 |
| `sw/firmware/ctrl/aecp/aecp_maps.c` | 222/222 | 290/290 |
| `sw/firmware/ctrl/aecp/aecp_mbx.c` | 101/101 | 40/40 |
| `sw/firmware/ctrl/aecp/aecp_nvm.c` | 102/102 | 86/86 |
| `sw/firmware/ctrl/aecp/aecp_state.c` | 63/63 | 69/69 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 | 40/44 |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | 107/107 | 64/64 |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 | 62/62 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 | 60/60 |
| `sw/firmware/ctrl/mbx/mbx.c` | 189/189 | 74/74 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 514/514 | 478/478 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 | 106/110 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 |
| `third_party/tsn-c-stack/include/wire.h` | 10/10 | 2/2 |
| `third_party/tsn-c-stack/src/acmp.c` | 742/742 | 348/348 |
| `third_party/tsn-c-stack/src/adp.c` | 204/206 | 95/102 |
| `third_party/tsn-c-stack/src/maap.c` | 209/209 | 140/140 |

### Mutation campaigns at the round-3 head

`test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`, CI-parity container (CPython 3.12.3, gcc/gcov 13.3.0, GoogleTest 1.14.0), tree `36699f6c9` (the gate reads nothing `d1b22e804` changes): PASS in 29 min 30 s. Its 843 verdict lines equal round 2b's head log line for line, and dev `aef7ac66`'s by name (log 310,992 bytes, sha256 `885357758f0b4ab8f055fa66cca76c82e0d593071c96cf8bd3bfa8b0a727c0ad`; `round3/container/fw-gate-summary.txt`).

| Campaign | dev `aef7ac66` | round 3 head |
|---|---|---|
| firmware gate arms | 59 | 59, all `[ok]` |
| control (`ctrl_mutants.py`, ACMP, ACMP review and MAAP tables) | 471 of 471 | 471 of 471 |
| AECP (`aecp_mutants.py`) | 74 of 74 | 74 of 74 |
| SRP, two interfaces | 169 caught, 0 escaped | 169 caught, 0 escaped |
| SRP, one-interface subset | 68 caught, 0 escaped | 68 caught, 0 escaped |
| lwSRP pin arms | 2 of 2 | 2 of 2 |
| MAAP differential (`maap_differential.py --self-test`, at `76c0e27c3`) | 16 of 16 | the pin first, then 16 of 16 |
| mailbox bench quick mutants (`make -C tb/verilator/mbx`, at `76c0e27c3`) | 5 of 5 | 5 of 5 |
| boundary gate (this lane) | — | 45 boundary (42 refused by name, 3 passing), 20 pin, the stack's own 12 |

### Gates at the round-3 head

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest` | host, clean clone of `d1b22e804` | PASS: `51 firmware units (24 also as C++) ... in every configuration of 18 build modes, 5 shapes and 2 mailbox contracts (942 preprocessings), and every Makefile builder's pin prerequisites; 0 finding(s), 45 boundary and 20 pin controls, 0 misbehaved`; the stack's own gate and self-test pass; 630 s (`round3/boundary-selftest-final.log`) |
| `ctrl_boundary.py --require-rv32` without `gptp-processor` | host, clone of `36699f6c9` with `ctrl_configs.py` of `d1b22e804` | exit 2, `REFUSED: the end-station builder refused endstation_arty_4x4.yaml, ... run git submodule update --init gptp-processor` |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | container | PASS, campaigns above |
| `fw_coverage.py --selftest`; `--check --jobs 4` | container | 29 of 29; PASS (30 files), rows above |
| `fw_rv32_selftest.py --require-rv32`; `tally_selftest.py`; `ctrl_image_selftest.py --require-rv32` | container | 17 checks PASS; 18 of 18; 33 checks PASS |
| images, 35; `ctrl_image.py --base aef7ac66` | host, pinned SDK | 35 of 35 identical to dev; `+0` everywhere |
| `make -C tb/verilator/mbx` (`all`), then `run-if2` and `run-cosim` alone | host, Verilator 5.050, clean clone of `76c0e27c3` (the bench is unchanged after it) | `all`: 382, 427, 32, 384, 429, 369 checks, 0 failures, `mbx mutants: 5 of 5 caught`, the pin line before the firmware build; `run-if2` alone and `run-cosim` alone each print `tsn-c-stack at 1a9f651c…` before compiling, then their tallies; rc 0 (`round3/mbx-*.log`) |
| `maap_differential.py --self-test` | same | the pin line, 12 checks 0 failures, `differential mutants: 16/16 caught` (`round3/maap-differential-summary.txt`) |
| the docs job's 54 repository commands | host (CPython 3.14), clean clones of `d1b22e804`: every submodule, and only the hosted docs job's three | all rc 0 both ways; `check_em_dash --base 386b8e69`: 0 findings over 40 added lines in 3 pages; `ci_events.py --check` OK (1757 items), `--selftest` PASS (2387 arms); `check_py_idiom.py` 0 over-long lines, no new ratchet entry (`round3/docsjob-*-final.txt`) |

Not run in round 3, their inputs unchanged since round 2b (`git diff 386b8e69 d1b22e804` is empty on them): `aecp_wire.py`, `test_ctrl_nvm.py` and `tally_selftest.py --mutants`, `act_ci.py --selftest`. Hosted CI and act: no push.

### Open risks and questions (round 3)

1. The boundary self-test does more work: 630 s here on a shared host (load average 13 to 45 during the run; about 14 s per judgement unloaded, 45 boundary controls each judging both sides). At `386b8e69` the hosted step took 2 min 51 s and `firmware-unit` 26 min of its 45-minute budget; expect the step to grow by several minutes. Not measured on a hosted runner.
2. The dimensions are explored independently, a superset of what the builders compile together, so a finding may name a combination no single builder compiles (an image stream count with the SRP shape header, say). Only the macros that decide what a unit reads trigger a dimension, so the cost stays per unit.
3. `-fdirectives-only` would have restricted `-dU` to directives, but GCC's `-dU` then drops tests after a file's last `#include` (seen with GCC 16 and the RV32 GCC 14); the gate uses plain `-dU` and keeps the macros the conditionals and `#include` lines of the files read name, read as text, which can only add a macro (an identifier in a comment on such a line), never drop one.
4. The interface counts are derived by counting up until `gen_mailbox.py` refuses (it refuses 3 on the register space, which only grows with the count).
5. The C++ units are found by following `#include` lines as text, every branch alike: a superset of what any configuration reaches.
6. The gate now needs `gptp-processor` initialised (the end-station builder loads every config); `firmware-unit` initialises it, and the gate refuses by name without it.
7. R585-2-S2 (`aecp_arms.py --stack` with another clone still builds the submodule's `tests/`) is optional and not addressed; the default invocation pins what it builds.
8. Hosted CI and act have not run at any round-3 head (no push).

## Round 4

Assignment: #697 comment 6096148471, answering [R585-3](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6096142856) (one MAJOR, F1: the hosted `firmware-unit` job timed out at 45 minutes inside the boundary step) and [R584-3](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6095873264) (one MINOR, F1: `test/test_maap_differential.cpp`, named relative to the firmware tree, was not followed), with R585-3-S1 required now. Earlier rulings: pin 6092176555, round 2 6092628778, round 2b 6093389868, round 3 6094873968.
Base of the round: `d1b22e804158cbcb33fa12116d60e982f9a4c55b` (PR #705's head). New commits only, no rebase or amend; not pushed.
Head: `e07b305458ed3520e4adfc55e9746144ce5cdc79` (tree `ec8f8fb21ee972f83bf14a535e07f3633bc9a35e`).
Status: REVIEW READY, posted on #697 as comment [6097154937](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097154937) (`round4/review-ready-round4.md`).

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `6d43e1978` | Resolve every C++ source a builder names or refuse it by name, and refuse a -D or -U flag that is neither a literal nor an f-string | `ctrl_boundary.py --require-rv32 --selftest` on that exact tree: PASS, 59 boundary and 20 pin controls, 0 misbehaved, 1547 s (no memo yet; `round4/logs/step1-selftest.log`); docs job 54 of 54 rc 0 |
| `d25ae924a` | Run each TSN stack boundary preprocessing once per run, share the controls' base and stop a refused control at its finding, so the step fits five minutes | the same, PASS, 60 and 20, 0 misbehaved, 81 s (`step2-selftest.log`) |
| `9453fcc10` | Hold each NOT_SOURCES entry to the C++ names its builder's parsed text holds, not to a substring of it | the same, PASS, 73 s (`step3-selftest.log`) |
| `e07b30545` | State the boundary step's measured worst case and margin against its five-minute budget | docs job 54 of 54 rc 0 on the same tree (`docsjob/docsjob-step4.txt`) |

One-line subjects, no body, no trailers, configured identity. `git diff --name-only d1b22e80 e07b30545`: `docs/testing/CI_WORKFLOWS.md`, `sw/firmware/ctrl/README.md`, `sw/firmware/ctrl/test/ctrl_boundary.py`, `sw/firmware/ctrl/test/ctrl_configs.py` and the new `sw/firmware/ctrl/test/ctrl_plants.py`. No firmware source or header, test, builder, mutation table, coverage row, build flag, Makefile or workflow changes; nothing that builds an image, runs a campaign or measures coverage imports a changed module (only comments in `ctrl_image.py`, `ctrl_build.py` and the bench Makefile name them).

### Item 1 — R585-3-F1: the boundary step within 5 minutes

Same configurations, modes and shapes, every control kept (and twelve added); the step's cost cut by doing each piece of work once. None of the changes drops a configuration, samples, or moves the gate.

| Change | Where | What it saves |
|---|---|---|
| Each preprocessing once per run (`Memo`, `Judgement`). A preprocessing is reused only for the same unit and the same arguments, every file it read byte-identical (sha256 per file, taken once per judgement), and every file the trees gained or lost since named in none of those files and none of its arguments, none of which computes an `#include` operand (a header is looked up by name; the computed-include test reads `#`, `%:` and `??=`, `include_next`, `import` and `__has_include`, comments where blanks may be, after joining line splices). A preprocessing that failed for any reason but an `#error` is never stored. | `ctrl_boundary.py:229-351` (`Facts`, `Entry`, `Judgement.lookup/unmoved/store`, `Memo`), `:389` `preprocess` | The 59 controls' judgements of copies at the same paths reuse the base's preprocessings except where the plant changed a file they read: 3359 preprocessings run for 60 judgements instead of about 56,000 |
| The controls share one prepared base: `BASE`, the unplanted copies, judged first, must pass (a control of its own). | `ctrl_plants.py:249`; `ctrl_boundary.py:817` `controls` | The base's 943 preprocessings serve every control |
| A control that must be refused stops at the finding it names: each side reports as it finishes, and once one holds the needle the judgement's `stop` is set; the rest raise `Stopped` before their next preprocessing. A judgement returns only when every preprocessing it started has finished (`wait` in `explore.visit` and `judged`), so nothing of it runs into the next control's trees. Pass controls and the checkout's own judgement never stop early. | `ctrl_boundary.py:732` `judge`, `:443` `visit`, `:491` `judged` | Broad plants (a stack public header, a firmware header) stop after the side that finds them |
| A unit's configurations go to the shared workers at once (`pool`, JOBS = 4 compilers), each unit coordinated by its own thread (`explorers`), every side of a judgement at once. | `ctrl_boundary.py:434-498`, `:732` | The 81-configuration units no longer run one compiler at a time |
| The stack's own gate and its self-test run in a thread beside everything else; its output prints at the end, as before. | `ctrl_boundary.py:774` `stack_gate`, `:853` `main` | About 20 s of mostly serial CMake work overlaps |
| Paths a compiler names are resolved once per run (`resolved`), prefix checks on resolved text (`within`), directive names read once per file content (`Facts.directives`, keyed by digest rather than mtime and size). | `ctrl_boundary.py:358-386` | A reused judgement takes 0.7 s, not 5 |
| The builders' texts, flags and C++ names are read once per run (`candidates`, `checkout_builders`, `builder_flags`, `names_of`, `checkout_sources`). | `ctrl_configs.py:257-315`, `:557-590` | Per-control derivation from 0.4 s to almost nothing |
| The planted controls' data moved to the new gate module `ctrl_plants.py` (in `GATE`, never a builder), keeping `ctrl_boundary.py` under the 1000-line module limit of `check_py_idiom.py`. | `ctrl_plants.py`; `ctrl_configs.py:78` | — |

`judge(trees, rv32, work, universe=None, computed=None, control=None)` keeps the positional form the reviewers' probe harnesses use (`judge(trees, rv32, work, modes(...))`); `modes` stays importable from `ctrl_boundary`.

Step timings, `ctrl_boundary.py --require-rv32 --selftest`, pinned to four CPUs with `taskset` on a shared host (the hosted runner has four):

| Tree | Total | Controls | Pin controls, checkout, Makefile check, stack gate | Load average |
|---|---|---|---|---|
| `d1b22e80` (before, `round4/logs/before-selftest.log`) | 807 s | 766 s (45 controls) | 35 s | 5 to 11 |
| `9453fcc10`, run 1 (`head-selftest-1.log`) | 82.0 s | 64.4 s (60 controls) | 9.4 s | 23 |
| `9453fcc10`, run 2 | 73.6 s | 58.2 s | 9.4 s | 23 |
| `9453fcc10`, run 3 | 81.2 s | 63.5 s | 11.7 s | 22 |
| `e07b30545` (`final-head-selftest.log`), with this lane's own container gate and image builds running beside it | 86.0 s | 69.2 s | 10.6 s | 8, the host's other lanes quieter |

Setup (deriving the builders and generating every shape's headers) takes 6 to 8 s of each. The stack's own gate runs beside the controls, so its time is hidden in the column "pin controls ...". `CI_WORKFLOWS.md` states the three runs at `9453fcc10` (74 to 82 s; the worst leaves 218 s of 300 s, 73 %); the run at the head, beside this lane's own heavy jobs, took 86 s (214 s left, 71 %). Budget is the assignment's 5 minutes; the job's other steps took 19 to 32 min (step 8) and 3.5 min (steps 10 and 11) hosted, so the job ends at about 25 to 38 min of its 45.

Per control at the head (`round4/logs/controls-timed-head.log`, scratch `controls_timed.py`): the base runs 943 preprocessings; most controls run 3 to 60 and reuse the rest; the widest (a stack public header for C++ only, the AECP image's SRP composition, the four mode-writing builders) run 250 to 400 before they stop at their finding; the twelve builder-only controls run none. Controls 63.7 s, the checkout's own judgement 7.1 s (942 configurations, 943 preprocessings, none reused: the checkout is judged at its own paths, never from a control's).

The 807 s run matches the hosted step at `d1b22e80`: its self-test phase took 736 s there (12:16, R585-3), so the pinned host is no faster than a hosted runner.

Memo equivalence (scratch `round4/scripts/memo_equivalence.py`): every control, the base included, judged in full twice (no early stop), once reusing the run's preprocessings and once with a fresh memo whose lookups all miss (no reuse at all, not even within one judgement); the sorted findings compared. At `9453fcc10`: 0 of 60 controls differ (`round4/logs/memo-equivalence-head.log`, rc 0); an earlier run on the work tree gave 0 of 58.

### Item 2 — R584-3-F1: every C++ source a builder names is resolved, or refused

`ctrl_configs.py:574-610` (`cxx_sources`, `named_sources`, `names_of`, `write_target`):

- A C++ name now resolves beside its builder, in `test/`, in the firmware tree (`CTRL`, new: `test/test_maap_differential.cpp`), in the stack (with or without `tsn-c-stack/`), the checkout's root, the protocol processor, and in every directory of the checkout the builder names as a literal (new: `aecp_wire.py`'s `"tb/pp_top"` resolves its `sim_main.cpp` to the processor's `tb/pp_top/sim_main.cpp`). Every file it resolves to is a source.
- Resolution is in the trees judged (`view`): a copy's file, so a control's edit of a test source is followed.
- A name the builder writes itself (`write_text`, `write_bytes`, `touch`, `open` for writing, a `shutil` copy's destination) is generated: it is followed through the builder's own literals (`aecp_wire.py` writes `reference.cpp`).
- A name that resolves to no file and is not written fails the gate by name: `firmware c++: <builder> names <name>, a C++ source that resolves to no file`. So does a name the builder computes (an f-string ending in a C++ suffix, a suffix joined to a value, `with_suffix`).
- `NOT_SOURCES` lists the two names that are no source: `fw_coverage_selftest.py`'s `sw/firmware/ctrl/test/t.cpp` and `tests/t.cpp`, paths written into a planted coverage report. Each is checked: its builder holds it (else a finding), it resolves to no file (else it is followed), and the builder does not write it (else it is generated). They are printed on every run.
- At the head: 57 C++ sources (55 before: `test_maap_differential.cpp` and the processor's `tb/pp_top/sim_main.cpp` added), one generated (`reference.cpp`), two `NOT_SOURCES`, no finding; still 24 firmware units judged as C++.

### Item 3 — R585-3-S1: a flag that is neither a literal nor an f-string

`ctrl_configs.py:183-255`: a Python builder's flag is a literal (`"-DNAME"`, or `"-D", "NAME"` adjacent) or an f-string whose literal holds `NAME=` (a value); any other string literal starting `-D` or `-U` is refused by name, a literal joined to a value by `+`, `%` or `str.format` among them (even `"-DNAME=" + x`), as is a bare `-D` alone. An f-string or literal whose macro name is computed (`f"-D{X}"`, `f"-DFOO{X}"`) is refused (the computed-macro reading now needs the `=`). A Makefile word starting `-D` or `-U` (or a bare one with the next word) that is not a literal flag, or that holds `$`, is refused by name: `-D$(MODE)`, `-DNAME=$(VALUE)`, `$(addprefix -D,$(MODES))`. No builder at the head uses any of these forms, so the derived modes (18) and values are unchanged.

### Docs (at the head)

`sw/firmware/ctrl/README.md:94-102` (C++ name resolution, generated sources, `NOT_SOURCES`, the flag forms refused) and `:114-118` (the memo, the shared base, early stop, 56 + 3 controls); `docs/testing/CI_WORKFLOWS.md:67-74` (the 5-minute budget, how the step fits it, the measured worst case and margin); the docstrings `ctrl_boundary.py:43-63` and `:90-113`, `ctrl_configs.py:17-24` and `:37-48`, and `ctrl_plants.py:1-11`.

### Planted controls added in round 4 (`ctrl_plants.py:191-238`, `:249`)

| Control | Refused by |
|---|---|
| BASE: the copies as they are, judged first | passes |
| R584-3's plant: a new `maap/maap_r584.h` with `#include "acmp_fake.hpp"` under `#ifdef __cplusplus`, included only from `test/test_maap_differential.cpp` | `firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers` |
| a builder names `planted_r4.cpp`, which is no file | `firmware c++: sw/firmware/ctrl/test/planted_arms.py names planted_r4.cpp, a C++ source that resolves to no file` |
| a builder computes a C++ name (`STEM + ".cpp"`) | `firmware c++: sw/firmware/ctrl/test/planted_arms.py computes the name of a C++ source, STEM + '.cpp', which the boundary cannot follow` |
| a builder writes `planted_r4.cpp` holding `#include "adp_r4.h"`, a new header with `#include "adp_port.h"` under `#ifdef __cplusplus` | `firmware c++: adp/adp_r4.h includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers` |
| `test/t.cpp`, a `NOT_SOURCES` name, made a file including a new header with a C++-only `acmp_fake.hpp` include | `firmware c++: maap/maap_r4.h includes tsn-c-stack/tests/acmp_fake.hpp, ...` |
| `fw_coverage_selftest.py` no longer naming `tests/t.cpp` | `firmware c++: NOT_SOURCES lists tests/t.cpp for sw/firmware/gtest/fw_coverage_selftest.py, which no longer names it` |
| Python `["-D" + MODE]` | `REFUSED: the builder sw/firmware/ctrl/test/planted_arms.py writes '-D', a -D or -U flag the boundary cannot read ...` |
| Python `["-D%s" % "CTRL_R4_FORMAT"]` | `... writes '-D%s', a -D or -U flag the boundary cannot read` |
| Python `["-DCTRL_R4_VALUE=" + str(N)]` | `... writes '-DCTRL_R4_VALUE=', a -D or -U flag the boundary cannot read` |
| Python `[f"-DCTRL_R4_{SUFFIX}"]` | `... computes a -D or -U flag's macro: the boundary cannot read it` |
| Python `["cc", "-D"] + NAMES` | `... writes '-D', a -D or -U flag the boundary cannot read` |
| Makefile `cc -D$(MODE)` | `the builder sw/firmware/ctrl/test/planted.mk writes '-D$(MODE)', ...` |
| Makefile `cc -DCTRL_R4_MAKE=$(VALUE)` | `... writes '-DCTRL_R4_MAKE=$(VALUE)', ...` |
| Makefile `cc $(addprefix -D,$(MODES))` | `... writes '-D,$(MODES))', ...` |

A control that refuses the gate (exit 2) is caught as `REFUSED: <reason>` and judged by its needle like a finding. The 45 controls of round 3 are kept with their needles unchanged (`Plant.mode` is renamed `words`, positionally the same) and all `[ok]`. Totals at the head: 60 boundary controls (the base, 56 refused by name, 3 passing) and 20 pin controls, 0 misbehaved.

### Reviewers' probes at the head (`round4/probes/`)

Each published script was run unchanged from the review packets on `697c-review-evidence` (`70bb2d21`), against a clean clone of `9453fcc10` (the gate is the same at `e07b30545`), with `python3 -I`.

| Probe set | At `d1b22e80` (the reviews) | At the head |
|---|---|---|
| R584-3 `boundary_probes.py`, 20 probes | `cplusplus-new-header-maap-differential` ESCAPED (R584-3-F1); the rest as below | `cplusplus-new-header-maap-differential` CAUGHT: `firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp`. Every other probe gives the verdict R584-3 recorded: 13 more CAUGHT; the stack-side plants refused first by the pin check (exit 2, as designed); `two-arg-U-tuple` derived (`R584_UNDEF (-UR584_UNDEF -DR584_UNDEF)`; the harness's needle lists the flags the other way round); `fw-multiword-string-flag` and `makefile-pin-errors-ignored` GAP-CONFIRMED, R584-3-S1's optional items, not addressed |
| R585-3 `boundary_probes3.py all`, 18 probes | f1 to f4 ESCAPED (R585-3-S1), f5 and f6 REFUSED, the rest CAUGHT | 12 CAUGHT; f1 to f6 REFUSED by name: f1 `writes '-D,$(MODES))'`, f2 `writes '-D$(MODE)'`, f3 `writes '-D'`, f4 `writes '-D%s'`, f5 `writes -D before a macro it computes`, f6 `computes a -D or -U flag's macro` |
| R585-3 `cxx_unfollowed_probe.py`, real path | includer `test/test_maap_differential.cpp` ESCAPED, `test/test_maap_mbx.cpp` CAUGHT | both CAUGHT: `firmware c++: maap/maap_probe.h includes tsn-c-stack/examples/adp_port.h` |
| R585-3 `boundary_probes_r585_2.py all`, 11 probes | 11 CAUGHT | 11 CAUGHT |

The pin probes were not rerun: `ctrl_pin.py`, `ctrl_build.py` and the bench Makefile are unchanged since round 3, and the 20 pin controls pass at the head.

### Images, coverage, kills

- Images: `round4/scripts/images3.sh` (round 3's) at `9453fcc10` (the image builders are unchanged at `e07b30545`), the pinned SDK and the same runtime archives: 35 of 35 ELF files; the manifest `round4/images-head.sha256` is byte-identical to round 3's (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`), which equals dev `aef7ac66`'s (round 2b). Every hash in the round-3 table above holds.
- Kills: `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` in the CI-parity container (CPython 3.12.3, gcc/gcov 13.3.0, GoogleTest 1.14.0) on a clean clone of `9453fcc10`: PASS in 28 min, rc 0; its 843 `[ok]` verdict lines are identical to round 3's line for line (`round4/container/fw-gate-verdicts.txt`), so to dev `aef7ac66`'s by name: 59 arms, control 471 of 471, AECP 74 of 74, SRP 169 and 68, lwSRP pin 2 of 2 (log 310,992 bytes, sha256 `eaf5d73f233f0de592d6ab1c3dac50f93c013cb250316dd8b28945ecd00052d1`, not copied: `round4/container/fw-gate-summary.txt`).
- Coverage: `fw_coverage.py --selftest` 29 of 29; `--check --jobs 4` PASS (30 files), every row identical to round 3's (`round4/container/coverage-check.log`), which equal dev's raw counts; `coverage.ratchet` is unchanged.

### Gates at the round-4 head

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest` | host, clean clone of `e07b30545`, four CPUs | PASS: `51 firmware units (24 also as C++) ... 18 build modes, 5 shapes and 2 mailbox contracts (942 configurations, 943 preprocessed), and every Makefile builder's pin prerequisites; 0 finding(s), 60 boundary and 20 pin controls, 0 misbehaved`; the stack's own gate and its twelve controls pass; 86.0 s (`round4/logs/final-head-selftest.log`); at `9453fcc10` three more runs, 82.0, 73.6 and 81.2 s |
| memo equivalence (scratch) | host, clean clone of `9453fcc10` | 0 of 60 controls differ |
| R584-3, R585-3 and R585-2 probes | host, clean clone of `9453fcc10` | as tabled above |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | container | PASS, 843 verdicts identical to round 3's |
| `fw_coverage.py --selftest`; `--check --jobs 4` | container | 29 of 29; PASS (30 files), rows identical |
| `fw_rv32_selftest.py --require-rv32`; `tally_selftest.py`; `ctrl_image_selftest.py --require-rv32` | container | 17 checks PASS; 18 of 18; 33 checks PASS |
| images, 35 | host, pinned SDK | 35 of 35 identical to round 3's manifest and dev's |
| the docs job's 54 repository commands (`round4/scripts/docsjob.sh`, the shared Markdown venv of round 3) | host (CPython 3.14), clean clones of `9453fcc10` with every submodule and with only the hosted docs job's three; and the tree of `e07b30545` | all rc 0 each way; `check_em_dash --base d1b22e80`: 0 findings over 18 added lines in 2 pages; `ci_events.py --check` OK (1757 items); `check_py_idiom.py`: no ratchet raised (`ctrl_boundary.py` 899 lines, under the 1000-line limit) |

Not run in round 4, their inputs unchanged since round 3 (`git diff d1b22e80 e07b30545` is empty on them): the mailbox bench, the MAAP differential, the AECP wire comparison, `test_ctrl_nvm.py`, `tally_selftest.py --mutants`, `act_ci.py --selftest`, the reviewers' pin probes. Hosted CI and act: no push.

### Open risks and questions (round 4)

1. The step's time is measured locally only: 74 to 86 s on four pinned CPUs of a shared host, where `d1b22e80` took 807 s and its hosted run 12 min 16 s before the job was cancelled; the manager's hosted run at the head is the confirmation the assignment names.
2. The memo's reuse rests on a preprocessing being a function of its arguments, the unit's path, the bytes of every file it read, and which files exist where it looks a header up. The two trees judged are listed per judgement; the gate adds no file anywhere else during a run (it writes only under its temporary directory, and plants only into the copies), and every file read, inside or outside the trees, is checked by digest. The scratch equivalence check found no difference over all 60 controls.
3. A refused control stops at its finding: its verdict is the same as a full judgement's by construction (findings only grow with more sides), but the finding it shows is the first side's to finish holding the needle.
4. `NOT_SOURCES` is a written list of two paths that are no files (a coverage self-test's report fixture). Each is checked on every run and printed; any other C++ name that resolves to no file fails the gate by name.
5. A C++ source a builder generates is followed through the builder's own literals; one generated from a template the builder does not name as a C++ source would not be. None exists: the only one, `reference.cpp`, is written from `sim_main.cpp`'s text, itself followed.
6. A name is resolved in every directory the builder names as well: a superset, which can follow a same-named file the builder never compiles, never fewer.
7. The first round-4 commit (`6d43e1978`) has no memo; its self-test takes about 25 minutes. Only the head runs in CI.
8. R584-3-S1 (optional) and R585-2-S2 (optional) are not addressed.
9. Hosted CI and act have not run at any round-4 commit (no push).

## Round 5

Assignment: #697 comment 6097800045, answering [R584-4](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6097725381) (two MINOR: F1, computed and written C++ sources pass silently; F2, `$(patsubst ...)` and `$(foreach ...)` flags pass silently) and [R585-4](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6097795358) (one MINOR, F1: patsubst, `VAR+=-D`, a mid-f-string `-D` and multi-word literals are neither derived nor refused). Ruling: judge the builders' actual compiler invocations, by construction. Earlier rulings: pin 6092176555, round 2 6092628778, round 2b 6093389868, round 3 6094873968, round 4 6096148471.
Base of the round: `e07b305458ed3520e4adfc55e9746144ce5cdc79` (PR #705's head). New commits only, no rebase or amend; not pushed.
Head: `92b5be18817659c1c9903a0544450d29ca7ab3fd`.
Status: REVIEW READY, comment [6100754030](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6100754030) (its text: `round5/review-ready-round5.md`). The gate judges a capture of the builders' compiler invocations (`ctrl_capture.py`, its C recorder in `ctrl_shim.py`). Against the container's capture of the hosted job's firmware steps at the head it passes, 89 boundary and 20 pin controls, 0 misbehaved, in 101 to 106 s on four idle pinned CPUs (`e07b3054`'s step: 80 to 82 s on the same CPUs), and under CPython 3.12.3 and GNU make 4.3 with `MAKEFLAGS=w`; standalone, with Verilator, it passes too. The 942 configurations judged are identical to `e07b3054`'s; the 35 images, built plainly and through the capture, equal round 4's manifest; the firmware gate's 845 verdict lines and the coverage table, through the capture, equal round 4's.

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `d6dd5936d` | Judge the firmware builders' compiler invocations as a capture records them around the hosted firmware steps, not their source text | `ctrl_boundary.py --require-rv32 --selftest --capture <full capture> --without verilator`: PASS, 86 boundary and 20 pin controls, 0 misbehaved (`round5/logs/timed-4.log`), and under CPython 3.12.3 and GNU make 4.3 with `MAKEFLAGS=w` (`gate-capfull-312.log`); `check_py_idiom.py` rc 0; `ci_events.py --check` OK (1757 items); `check_doc_style.py` OK |

| `133ee559c` | Name each recorded compile's builder from the command the capture ran, not from the process tree, and document the capture's helpers | the same self-test, PASS, 86 and 20, 0 misbehaved (`timed-5.log`); `check_baremetal_only.py --check` OK (the first commit's recorder read the process tree's pseudo-filesystem, which #259's bare-metal gate refuses in a tracked file: the docs-job replay at `d6dd5936d` found it, with three helpers the idiom check under CPython 3.12 counts as undocumented); `check_py_idiom.py` rc 0 under CPython 3.12.3 and 3.14 |
| `11529fadd` | Leave an installed tool's own C++ source unfollowed, and refuse by name a builder-written C++ source whose include a macro computes | the same self-test, PASS, 87 and 20, 0 misbehaved (`final-timed-1.log`); `check_py_idiom.py`, `check_baremetal_only.py --check`, `check_doc_style.py`, `ci_events.py --check` rc 0. Found by the standalone run at `133ee559c` (Verilator given): the recorder had kept Verilator's own runtime source `verilated.cpp`, which the bench's and the wire comparison's builds compile, and the headers beside it, and the gate refused `verilated.h includes VL_VERILATED_INCLUDE, which text cannot follow` (`round5/logs/standalone-133ee559c-tail.txt`) |
| `93540c3a8` | Hold a C++ source a builder copies outside its directories as its own by its inode change time against the capture's start, and pass an installed tool's source that predates it | the same self-test, PASS, 89 and 20, 0 misbehaved (`final2-timed-1.log` to `-3`), and under CPython 3.12.3 and GNU make 4.3 with `MAKEFLAGS=w` (`final2-parity.log`); pyflakes, `check_py_idiom.py` under 3.12.3 and 3.14, `check_baremetal_only.py --check`, `check_doc_style.py`, `ci_events.py --check` rc 0. Found by a capture of the Verilator builders at `11529fadd`: the AECP wire comparison copies the bench's `sim_main.cpp` into its output directory, outside the temporary and working directories, and `11529fadd`'s rule took the copy for an installed tool's and did not follow it |
| `92b5be188` | State the boundary step's time with the capture against e07b3054's on the same idle CPUs, and its slowest run on busy ones | `check_doc_style.py`, `ci_events.py --check`, `check_em_dash.py --base e07b30545`, `docs_check.py` rc 0; then the docs job's 54 commands at the head (below). Docs only (`docs/testing/CI_WORKFLOWS.md`): of the gates run at `93540c3a8`, only `ci_events.py` reads it, and it ran again at the head |

One-line subjects, no body, no trailers, configured identity. `git diff --stat e07b3054 92b5be188`: 11 files, 2008 insertions, 577 deletions. New: `sw/firmware/ctrl/test/ctrl_capture.py`, `ctrl_shim.py`, `ctrl_runs.py`. Changed: `ctrl_boundary.py`, `ctrl_configs.py`, `ctrl_pin.py`, `ctrl_plants.py`, `sw/firmware/ctrl/README.md`, `docs/testing/CI_WORKFLOWS.md`, `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py`. No firmware source or header, no test, no image builder, no mutation table, no coverage row, no Makefile, no build flag. Nothing that builds an image, runs a campaign or measures coverage imports a changed module; the capture runs every compiler unchanged (below).

### Item 1: capture

| What | Where (at `d6dd5936d`) |
|---|---|
| The capture driver: `ctrl_capture.py --out DIR -- COMMAND...` runs COMMAND with `DIR/bin` first on `PATH`, a wrapper for every C and C++ compiler name the `PATH` holds (prefixed and versioned too), for the RV32 compiler (`MILAN_RV32_CC` names the wrapper; its sibling tools are linked beside it), and for `CC`/`CXX` where set; appends each run to `DIR/manifest.jsonl` (command, directory, exit status); exit status the command's | `ctrl_capture.py:191` `install`, `:200` `installed`, `:151` `wrapper`, `:248` `run`, `:54` `COMPILER` |
| The recorder: C11, compiled into `DIR/bin` with the real `cc` when a capture is installed (`ctrl_capture.py:160` `recorder`). Per invocation it appends one JSON record (name, real compiler, arguments, working directory, every source with its language as `parse()` reads it, the `-include`/`-imacros` files as the compiler finds them, the builder files of `CTRL_CAPTURE_FROM`, and of `CTRL_CAPTURE_RUN`: the script or Makefile of the command the driver ran, which every process below it inherits) with one `write` to `records.jsonl`, then `execv`s the real compiler with the same arguments. It keeps, under `DIR/text/` by SHA-256, every C++ source, every file a C++ compile reads first outside the checkout, and every header outside the checkout a C++ source reaches in a builder's own directories (the temporary directory, the compile's, the source's), its `#include` lines read as text in every branch. A record it cannot write stops the compile (exit 2). (The first commit named the builder from the process tree; the second takes it from the driver, so the recorder reads no pseudo-filesystem.) | `ctrl_shim.py:102` `RECORDER` (`main` `:542`, `closure` `:373`, `chain` `:486`, SHA-256 per FIPS 180-4), `:61` `parse` (shared with the reader) |
| The audit hook: every Python process of a capture loads `DIR/hook/sitecustomize.py` (on `PYTHONPATH`; it chains to the `sitecustomize` it shadows). For each process it starts it sets `CTRL_CAPTURE_FROM` to the checkout files on its Python stack (after its parent's), so a record names `ctrl_arms.py`, `srp_mutants.py` and the like, not only the entry script; and it records a compiler a builder runs by a path no wrapper stands on (absolute, or bare on a `PATH` of its own) as a bypass | `ctrl_capture.py:58` `HOOK` |
| The reader: `load(DIR)` refuses a missing or unreadable capture, and an empty one; each invocation's builders are the hook's stack files and the script or Makefile of the command the driver ran (`script_of`, applied by `run` to the command); `-D`/`-U` flags and searched directories come from `parse()` of the recorded arguments | `ctrl_capture.py:370` `load`, `:318` `script_of`, `:282` `Capture` |
| The hosted job: steps 8 (`fw_rv32_selftest.py`, `test_ctrl_firmware.py --self-test`), 9 (`test_ctrl_nvm.py`) and 10 (`fw_coverage.py --selftest`, `--check`) each run under `ctrl_capture.py --out "$RUNNER_TEMP/ctrl-capture"`; the boundary step moves last (11) and judges that capture with `--capture "$RUNNER_TEMP/ctrl-capture" --without verilator`. Same ten steps | `.github/workflows/rtl-fast.yml:281-310`; `scripts/ci_events.py:710` `CAPTURE`, `:2374-2396` |
| The boundary's own runs under the capture, in every run: the stack's own gate's CMake build (gcc and clang, without its self-test, which then runs uncaptured beside the controls), `ctrl_image.py` at its shapes, `ctrl_image_selftest.py`, and `ctrl_srp_image.py` at `ctrl_image.SHAPES`, both interface counts and all three compositions (12 runs). `ctrl_srp_image.py` links against runtime archives built from sources outside the checkout, so it is given archives that do not exist: it compiles every object and must stop exactly at its link (`stopped_at_link`) | `ctrl_runs.py:44` `image_runs`, `:66`, `:75` `owned`; `ctrl_boundary.py:801` `stack_gate`, `:915` `main` |
| Standalone (no `--capture`): the gate runs every known builder's commands under a capture of its own first, Verilator from `VERILATOR` or `PATH`; a builder that does not exit 0 refuses the gate | `ctrl_runs.py:100` `standalone`, `:128` `captures` |
| The judgement takes everything from the capture: the build modes are every `-D`/`-U` of every invocation exactly as given (a reserved name excepted; the image's stream counts stay their own dimension, and a recorded one no shipped shape gives refuses); the C++ sources are every recorded C++ compile's source and `-include` files, read from the trees judged where they are the checkout's (so a control's plant is followed) and from the kept text otherwise, followed through the kept headers by the name they were reached at. Computed values and their guard dimensions are gone: every recorded value is concrete | `ctrl_configs.py:310` `derive`, `:323` `modes_of`, `:535` `cxx_sources`, `:515` `cxx_index`; `ctrl_boundary.py:664` `cxx_units`, `:758` `judge` |
| An installed tool's own C++ source (Verilator's runtime, which the bench's and the wire comparison's builds compile) is recorded with the digest `installed` and nothing of it is kept or followed: a C++ source outside the checkout, outside the temporary directory and outside the compile's working directory whose inode changed before the capture's start marker (`DIR/start`, written when the capture is first installed, named by `CTRL_CAPTURE_START`). A file a builder writes, copies (`shutil.copy2` keeps the modification time, never the change time), links or renames during the capture is its own wherever it lies (each sets the inode's change time; the link and the rename checked on this host's ext4). The reader skips `installed` sources and prints the installed files each run (`installed tools' own, not followed: ...`) | `ctrl_shim.py` `own` (in `RECORDER`), `ctrl_capture.py` `installed`; `ctrl_configs.py` `INSTALLED`, `sources_of`, `configurations` (at `93540c3a8`) |
| Removed: the text readers of round 2 to 4 (`python_flags`, `makefile_flags`, `builder_flags`, `python_names`, `makefile_names`, `names_of`, `named_sources`, `NOT_SOURCES`, `write_target`, the value guards); the builder discovery by text stays only as the cross-check of item 2 | `git show d6dd5936d -- sw/firmware/ctrl/test/ctrl_configs.py` |

Cost of the capture per compile, measured in the CI-parity container on a shared host (`round5/logs/bench3.txt`, 100 C and 20 C++ compiles of a one-line source each way): a C compile 10.8 ms bare and 11.9 ms through the recorder; a C++ compile 11.8 ms bare and 13.8 ms through it. The hosted job's firmware steps make 23,213 compiles (`cap-head`), so the recorder adds well under a minute of CPU to the job, spread over its four CPUs. A first Python recorder cost 23 ms per compile (about 9 minutes of CPU on this job) and was replaced before the commit.

### Item 2: fail closed

`ctrl_configs.py:262` `held`, run at the start of every judgement (the checkout's and each control's): refused by name are

- a missing capture or one with no records (`ctrl_capture.load`), and one whose builder run did not exit 0 (`ctrl_runs.captures`);
- a known builder (`BUILDERS`, `ctrl_configs.py:110`) the capture holds no invocation of, unless the run leaves it out (`--without verilator`: the mailbox bench, the MAAP differential, the AECP wire comparison, each printed `LEFT OUT` on every run);
- a builder found by text (every Python module and Makefile naming `sw/firmware/ctrl` or `ctrl_build`) that compiled nothing in the capture and is neither a known builder, nor part of one the run leaves out (`PART_OF`), nor listed in `OUTSIDE` with the reason its compiles are none of the firmware's (`ctrl_configs.py:136-161`: the CI model and scope, the diagram, the generators, the campaign tables, the processor cuts, the store campaign's defect table, the bare-metal runtime builder);
- a compiler a builder runs by a path no wrapper stands on: a Python builder's, which the audit hook records, and a Makefile builder's recipe, read from make's own dry run of every target under the capture's environment (`ctrl_pin.py:148` `named_compilers`; the checkout's Makefile builders on every run, a control's planted Makefile with it);
- a C++ compile of a source that was no file when it ran, or of standard input (`unkept`, `:284`);
- a `-D`/`-U` whose macro has no name, and a recorded stream count no shipped shape gives (`modes_of`).

The static derivation from source text is removed. What remains of reading builders' text is the discovery of item 2's third bullet, which can only refuse.

### Item 3: plants

`ctrl_plants.py`: 88 plants and the base (89 boundary controls: 83 refused by name and 5 passing beside the base; round 4 had 59 and the base). Every builder plant is now a builder that runs through the capture (`ctrl_boundary.py:847` `planted_run`) in a directory of its own with an empty `planted.c`, `PLANT_CTRL`/`PLANT_STACK`/`PLANT_WORK`/`PLANT_GCC` naming the copies, its directory and the real gcc; what it compiled joins the run's capture for that control alone. A planted builder that only compiles a mode (`shared`) runs once, before the base, and its invocations join the base every control shares, which must still pass. A planted builder's files beside it are written before its capture begins. Every control at the head (`round5/logs/final3-timed-1.log`):

| Control (new or changed in round 5) | Refused by |
|---|---|
| a Makefile's `$(patsubst %,-D%,$(MODES))` (R584-4 D1, R585-4 mk-patsubst) | `firmware [-DCTRL_R5_PATSUBST]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers` |
| a Makefile's `$(foreach m,...,-D$(m))` (R584-4 D2) | `firmware [-DCTRL_R5_FOREACH]: ...` |
| a Makefile's `CFLAGS+=-D...` with no space (R585-4 mk-append-nospace) | `firmware [-DCTRL_R5_APPEND]: ...` |
| a Makefile's bare `-D $(M)` (R584-4 D6) | `firmware [-DCTRL_R5_SPACED]: ...` |
| a Makefile's `-D$(MODE)` (round 4, refused by text then) | `firmware [-DCTRL_R4_MAKE]: ...` |
| a Makefile's `-DNAME=$(VALUE)` (round 4) | `firmware [-DCTRL_R4_MAKE_VALUE=2]: ...` |
| a Makefile's `$(addprefix -D,$(MODES))` (round 4) | `firmware [-DCTRL_R4_ADDPREFIX]: ...` |
| an f-string with `-D` after other text, run through a shell (R585-4 py-fstring-mid) | `firmware [-DCTRL_R5_FSTRING]: ...` |
| a multi-word literal split (R585-4 py-midstring, R584-3-S1) | `firmware [-DCTRL_R5_SPLIT]: ...` |
| a shell command's literal (R584-4 D3) | `firmware [-DCTRL_R5_SHELL]: ...` |
| `shlex.split` of a literal (R584-4 D7) | `firmware [-DCTRL_R5_SHLEX]: ...` |
| a bare `-D` then a conditional expression (R584-4 D4) | `firmware [-DCTRL_R5_CHOSEN]: ...` |
| `"-D{}".format(...)` (R584-4 D5) | `firmware [-DCTRL_R5_FORMAT]: ...` |
| `"-D" + MODE`, `"-D%s" % ...`, `"-DNAME=" + str(N)`, `f"-DCTRL_R4_{SUFFIX}"`, `["cc", "-D"] + NAMES` (round 4, refused by text then) | `firmware [-DCTRL_R4_JOINED]`, `[-DCTRL_R4_PERCENT]`, `[-DCTRL_R4_VALUE=2]`, `[-DCTRL_R4_MODE]`, `[-DCTRL_R4_BARE]`: `adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, ...` |
| a Makefile's `$(wildcard .../*.cpp)` names the C++ source (R584-4 B1) | `firmware c++: adp/adp_r5.h includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers` |
| a builder joins a C++ name (`STEM + ".cpp"`), a `glob` names it (B2), an `iterdir` names it (B3) | the same `firmware c++: adp/adp_r5.h ...` |
| a builder writes the C++ source from a literal (C0), its include from an f-string (C1), from a `.format` template (C2), copies it from a template file (C3), or reaches the header through a header it writes beside it | the same `firmware c++: adp/adp_r5.h ...` (the kept text, and the kept beside-header) |
| R584-3's `maap_r584.h` reached only through `test_maap_differential.cpp`, now compiled by a planted builder (the MAAP differential needs Verilator) | `firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers` |
| the AECP core reaches a stack source at a value only its arms compile with (was: tests a computed value) | `firmware [-DAECP_TEST_INTERFACES=2]: aecp/aecp.c includes tsn-c-stack/src/acmp.c, ...` |
| the four earlier mode-writing builders (one literal, a new builder, two arguments, a new Makefile's two words), now run | `host [-DCTRL_PLANTED_MODE]`, `[-DCTRL_PLANTED_BUILDER]`, `[-DCTRL_SPLIT_MODE]`, `[-DCTRL_SPLIT_MAKE]`: their stack-side findings |
| a builder writes a C++ source whose include a macro computes (`11529fadd`) | `firmware c++: .../builder/planted.cpp includes H, which text cannot follow` |
| a builder copies, with `shutil.copy2` after dating the template to 2000, such a source into a directory of its own outside its temporary and working directories, and compiles it from there (`93540c3a8`; the AECP wire comparison's shape, which `11529fadd`'s rule passed) | `firmware c++: .../builder/out/sim.cpp includes H, which text cannot follow` |
| a builder compiles a C++ source with a computed include that has existed since before the capture began, outside the checkout, its temporary and its working directories: an installed tool's (`93540c3a8`, passing) | passes |
| a builder compiles a C++ source that is no file; one from standard input | `REFUSED: a builder compiled C++ from .../planted_r5_absent.cpp, which was no file when it ran`; `... from its standard input` |
| the capture is missing; empty; holds nothing of a known builder (`test_ctrl_firmware.py`'s records dropped) | `REFUSED: no capture at ...`; `... is empty: it records no compiler invocation`; `the capture holds no invocation of sw/firmware/ctrl/test/test_ctrl_firmware.py, ...` |
| a builder runs a compiler by its own path; a Makefile recipe does; a builder runs one on a `PATH` of its own | `REFUSED: a builder ran /usr/bin/gcc, a compiler the capture does not wrap, ...`; `planted.mk (target planted) ran /usr/bin/gcc, ...` |
| a builder of the firmware that no capture holds (text only, never run) | `REFUSED: sw/firmware/ctrl/test/planted_unrun.py names the firmware's tree, compiled nothing in the capture, ...` |
| a recorded stream count no shipped shape gives; a flag whose macro has no name | `REFUSED: ... compiled with -DIMAGE_SINKS=99u, a stream count no shipped shape gives`; `... '-D=1', a -D or -U flag whose macro the boundary cannot name` |
| pass: a builder compiles a mode no unit tests | passes |

Removed with the text derivation, as their subject no longer exists: round 4's two `NOT_SOURCES` controls (a name the list holds made a file; the list naming a name its builder no longer holds) and its "names a C++ source that resolves to no file" (now: compiles one that is no file). Every other control of round 4 is kept with its plant and needle; the 30 file-only plants are unchanged.

Real builders (`round5/scripts/real_probes.sh`, a clean clone of `93540c3a8`, whose tree differs from the head's only in `docs/testing/CI_WORKFLOWS.md`; logs, patches and `summary.txt` in `round5/probes/`): each form planted into a builder that actually runs, then the hosted command judged end to end.

| Probe | Where planted | Result |
|---|---|---|
| unplanted | none | `ctrl_boundary: PASS` |
| `$(patsubst ...)`, `$(foreach ...)`, `VAR+=-D` with no space, `$(addprefix ...)` | the mailbox bench's firmware library recipe (`make -C tb/verilator/mbx obj_fw/libctrlfw.a`, which needs no Verilator), run under a capture of its own given beside the job's | rc 1, `[FAIL] firmware [-DCTRL_R5_PROBE]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers`, each |
| the recipe names the compiler by its path | the same recipe, `$(CC)` replaced by `/usr/bin/gcc` | rc 2, `REFUSED: tb/verilator/mbx/Makefile (target obj_fw/libctrlfw.a) ran /usr/bin/gcc, a compiler the capture does not wrap, ...` |
| a split multi-word literal, a mid-string f-string, `str.format`, a join | `ctrl_image.py`'s `IMAGE_FLAGS`, which the boundary runs itself | rc 1, the same finding, each |

The reviewers' round-4 probe scripts (`boundary_probes4.py`, `run_probes.sh`) plant text into builders that no compile executes (for example an unused `R585_FLAGS = [...]` in `ctrl_arms.py`) and call the removed derivation API. Under the ruling such text is no invocation and no configuration, so those scripts do not apply as written; every form they probe is a standing control above (run through the capture) and the Makefile and Python forms also a real-builder probe.

### Item 4: budget

The boundary step, `ctrl_boundary.py --require-rv32 --selftest --capture <capture> --without verilator`, pinned to four CPUs of a shared host (`taskset`), against a full capture (`round5/logs/timed-*.log`, `final2-*.log`, `final3-*.log`). Other jobs on the host pin themselves to CPUs 0 to 3 as well: sampled at 20:03, CPUs 0 to 3 were 100% busy and 4 to 15 idle, so the last runs moved to CPUs 8 to 11.

| Run | Total | Gate's own runs (images; the stack's build beside) | Base | Controls | Pin controls, checkout, stack self-test | Load average |
|---|---|---|---|---|---|---|
| work tree before the last cuts (`timed-1`) | 168.6 s | 52.2 s | 15.1 s | 90.4 s | 10.9 s | 25 to 41 |
| after running the image builders at their own shapes, the stack's self-test beside the controls, reading each capture part once (`timed-2`, `timed-3`) | 158.5, 106.6 s | 25.5, 26.4 s | 17.7, 14.2 s | 91, 53 s | 24, 12 s | 19 to 29 |
| `d6dd5936d`'s code (`timed-4`) | 115.9 s | 22.5 s | 14.7 s | 65.6 s | 13.1 s | 24 to 39 |
| clean clone of `93540c3a8`, CPUs 0 to 3 (busy), against `cap-head` (`final2-timed-1` to `-3`) | 113.5, 112.1, 214.8 s | 29.7, 23.9, 20.7 s | 12.8, 15.9, 21.3 s | 60.3, 61.8, 149.1 s | 10.7, 10.5, 23.7 s | 18 to 30 |
| the same, CPython 3.12.3 and GNU make 4.3, `MAKEFLAGS=w` (`final2-parity`) | 137.4 s | 33.5 s | 16.7 s | 74.0 s | 13.2 s | 24 to 28 |
| clean clone of `93540c3a8`, CPUs 8 to 11 (idle), against `cap-final`, the container's capture at that commit (`final3-timed-1` to `-3`) | 106.4, 101.0, 104.1 s | 22.3, 22.7, 21.4 s | 12.7, 10.6, 11.8 s | 59.3, 58.4, 60.6 s | 12.1, 9.3, 10.3 s | 50 to 64 |
| `e07b3054`'s step (no capture), its round-4 clean clone, CPUs 8 to 11 (`base-e07b-timed-1`, `-2`) | 82.2, 80.1 s | | | | | 46 to 49 |
| clean clone of the head, CPUs 8 to 11, CPython 3.12.3 and GNU make 4.3, `MAKEFLAGS=w`, against `cap-final` (`final3-parity`) | 111.5 s | | | | | 43 to 44 |

On the same idle CPUs the step went from 80 to 82 s at `e07b3054` to 101 to 106 s at the head, 20 to 26 s more (the image builders and the stack's build it now runs under its own capture, and 29 more controls). The hosted step took 93 s at `e07b3054` (job 114206016568); scaled by the same ratio the worst is about 124 s, 176 s inside the 5-minute budget (59%). The slowest local run, 214.8 s on CPUs other jobs held, left 85 s. `docs/testing/CI_WORKFLOWS.md` states these figures. The hosted figure at the head needs a hosted run (not pushed).

### Images, coverage, kills

- Images: `round5/scripts/images5.sh` (round 3's `images3.sh` with the RV32 compiler inherited, so a capture can wrap it) on a clean clone of the head, the pinned SDK and round 1's runtime archives: 35 of 35 ELF files, built once plainly and once through `ctrl_capture.py` (922 RV32 invocations recorded, no bypass). The two manifests are byte-identical to each other and to round 4's `round4/images-head.sha256` (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`, equal to dev `aef7ac66`'s): `round5/images-head.sha256`. Every hash in the round-3 table holds. (The same held at `d6dd5936d`.)
- Kills, through the capture: the hosted job's firmware steps as it runs them, each under `ctrl_capture.py --out <capture>` (`round5/scripts/fullcap.sh`; its rc and summary lines in `round5/logs/fullcap-final-summary.txt`), in the CI-parity container (CPython 3.12.3, gcc 13.3.0, GoogleTest 1.14.0) on a clean clone of `93540c3a8`: `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` PASS, rc 0, in 1831 s; its 845 verdict lines (843 `[ok]`, `mutants: 471 of 471 caught`, `test_ctrl_firmware: PASS`) are identical, line for line, to round 4's `round4/container/fw-gate-verdicts.txt` (sha256 `ad30597b...74ad3`, both; `round5/logs/fw-verdicts-final.txt`). The log is 324,434 bytes, sha256 `49459d1f9995bc2a80c10edf8930ccbcd3417d994d3d011d154142c3606986b5`, not copied. The capture (`cap-final`) holds 23,213 invocations, as `133ee559c`'s did.
- Coverage, through the capture: `fw_coverage.py --selftest` 29 of 29; `--check --jobs 4` PASS (30 files), its 32-line table byte-identical to round 4's (`round5/logs/cov-final.txt`); `coverage.ratchet` unchanged.
- The store suites, through the capture: `test_ctrl_nvm.py --require-rv32 --jobs 4` PASS, `saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests`.

### Configurations

Every configuration the checkout's judgement explores, recorded with a variant of R584-4's `record_configs.py` (`round5/scripts/record_configs5.py`) at `e07b3054` (round 4's clean clone) and at a clean clone of the head against `cap-final`: 942 configurations at each, 794 distinct (side, unit, label), 0 only at one, 0 whose files read, deciding macros or errors differ (`round5/logs/compare-configs-head.txt`; the same at `d6dd5936d`, `compare-configs.txt`). The seed flags differ as they must: round 4 seeded a computed value as a bare `-DNAME` guard, the head seeds the recorded values. The build modes: 22, round 4's 18 less `PP_TOP_IF2` and `PP_TOP_TIM_DEFAULTS` (only `aecp_wire.py` writes them; it needs Verilator, so the hosted run leaves it out by name) plus six that round 4 called computed values, now concrete (`AECP_TEST_INTERFACES` 1 and 2, `FW_GTEST_LABEL`, `NVM_TALLY_SHAPE`, `PP_ENTITY_CAPS`, `SRP_EXPECT_SINKS`, `SRP_EXPECT_SOURCES`). The firmware units judged as C++: 24, the same 24. Standalone, with Verilator, the capture holds the bench, the MAAP differential and the AECP wire comparison too: 33 build modes, the hosted 22 and eleven more: the wire comparison's `PP_TOP_TIM_DEFAULTS` and `AECP_WIRE_INTERFACES`, and Verilator's own `VERILATOR` and eight `VM_*` switches, 252 C++ sources (106 in the checkout), and three installed sources not followed, `verilated.cpp`, `verilated_dpi.cpp` and `verilated_threads.cpp`; still 942 configurations. `PP_TOP_IF2` is not among them: the wire comparison's one-interface command does not compile it.

### Gates at the round-5 head

The head `92b5be188` differs from `93540c3a8` only in `docs/testing/CI_WORKFLOWS.md`; the gate runs below on `93540c3a8` read nothing of it but `ci_events.py`, which ran again at the head.

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --capture <capture> --without verilator` (the hosted command) | host, clean clone of `93540c3a8`, four pinned CPUs, against `cap-final`, the container's capture of the job's firmware steps at `93540c3a8` | PASS three times, `51 firmware units (24 also as C++) ... in every configuration of 22 build modes from 23791 recorded invocations, 5 shapes and 2 mailbox contracts (942 configurations, 943 preprocessed) ...; 0 finding(s), 89 boundary and 20 pin controls, 0 misbehaved`, 101.0 to 106.4 s (`round5/logs/final3-timed-*.log`); also three times against `cap-head` (`final2-timed-*.log`) |
| the same | host, CPython 3.12.3 venv, GNU make 4.3 with `MAKEFLAGS=w`, a clean clone of the head itself, against `cap-final`, four idle pinned CPUs | PASS, the same line, 111.5 s (`final3-parity.log`); also at `93540c3a8` against `cap-head` on busy CPUs, 137.4 s (`final2-parity.log`) |
| `ctrl_boundary.py --require-rv32 --selftest` (standalone: every known builder under the gate's own capture, Verilator 5.050 given, host make 4.4.1 with `MAKEFLAGS=w`) | host, clean clone of `93540c3a8` | PASS in 2928 s: every builder exit 0 (the firmware gate 2158 s, the store suites 103 s, coverage 1 s and 278 s, the bench 46 s, the MAAP differential 158 s, the AECP wire comparison 65 s), `24097 compiler invocations from 23 builder runs; every known builder held`, 33 build modes, 252 C++ sources, `installed tools' own, not followed: verilated.cpp, verilated_dpi.cpp, verilated_threads.cpp`; `0 finding(s), 89 boundary and 20 pin controls, 0 misbehaved` (`standalone-93540c3a.log`). At `133ee559c` the same run refused (see Commits, `11529fadd`) |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`, `test_ctrl_nvm.py --require-rv32 --jobs 4`, `fw_coverage.py --selftest`, `--check --jobs 4`, each under `ctrl_capture.py` as the hosted job runs them (`round5/scripts/fullcap.sh`) | CI-parity container, clean clone of `93540c3a8` | all rc 0 (above); 23,213 invocations (`fullcap-final-summary.txt`) |
| real-builder probes (`round5/scripts/real_probes.sh`, ten) | host, clean clone of `93540c3a8`, against `cap-head` | unplanted PASS; the four Makefile and four Python forms each `[FAIL] firmware [-DCTRL_R5_PROBE]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, ...`; the compiler path `REFUSED: tb/verilator/mbx/Makefile (target obj_fw/libctrlfw.a) ran /usr/bin/gcc, ...` (`round5/probes/summary.txt`) |
| images, 35 (`round5/scripts/images5.sh`), plainly and under `ctrl_capture.py` | host, pinned SDK, clean clone of the head | 35 of 35 identical to each other and to round 4's manifest (`round5/images-head.sha256`, sha256 `de8ae063...0ebd0`); 922 RV32 invocations recorded, no bypass |
| configurations judged (`round5/scripts/record_configs5.py`) | host, `e07b3054`'s clean clone against a clean clone of the head with `cap-final` | 942 and 942, 794 distinct (side, unit, label) each, 0 differ (`round5/logs/compare-configs-head.txt`) |
| the docs job's 54 commands (`round5/scripts/docsjob.sh`, CPython 3.12.3 with the pinned Markdown renderer from `tools/markdown/requirements.txt`) | host, clean clones of the head with every submodule and with only the docs job's three | 54 of 54 rc 0 each way (`round5/docsjob/`); `check_em_dash --base e07b30545`: 0 findings over 44 added lines in 2 pages; `ci_events.py --check` OK (1757 items), `--selftest` PASS (2387 arms); `check_baremetal_only.py --check` OK (1239 files); `check_py_idiom.py` no ratchet raised (`ctrl_boundary.py` 992 lines); `check_hygiene.py --check` PASS; `docs_check.py` 0 findings. At `d6dd5936d` the same replay found two failures, fixed by `133ee559c` (see Commits) |
| pyflakes over the six gate modules; `check_py_idiom.py` under CPython 3.12.3 and 3.14 | host, the work tree of `93540c3a8` | rc 0 |
| the recorder's cost (`round5/logs/bench3.txt`) | CI-parity container | C 10.8 to 11.9 ms, C++ 11.8 to 13.8 ms per compile |

Not run in round 5: the mailbox bench, the MAAP differential and the AECP wire comparison on their own (the standalone run above runs them under the capture), `act_ci.py --selftest`, `tally_selftest.py --mutants`. Hosted CI and act: no push.

### Open risks and questions (round 5)

1. The hosted job has no Verilator, so its capture holds nothing of the mailbox bench, the MAAP differential or the AECP wire comparison; the hosted boundary names each `LEFT OUT` on every run and judges what the job compiles. A defect reached only through what those builders compile (for example a header only `test_maap_differential.cpp` reaches) is caught by the standalone run (Verilator given) and by the standing control that compiles it through a planted builder, not by the hosted step. Their two modes (`PP_TOP_IF2`, `PP_TOP_TIM_DEFAULTS`) were judged hosted in round 4 by text; no firmware unit tests them (the configuration sets above are identical). Adding Verilator to `firmware-unit`, or a boundary step to the Verilator job, is a decision for the maintainer.
2. The assignment's premise that the hosted build step "already runs every builder" holds for the arms, campaigns, store suites and coverage runs (steps 8 to 10, all now captured), not for the image builders (the boundary runs them itself, `ctrl_srp_image.py` stopping at its link) or the Verilator builders (item 1 above).
3. Bypass: a compiler a Python builder starts by a path is recorded by the audit hook, and one a Makefile builder's recipe names is read from make's dry run. A compiler run by path from a shell script, a CMake project of a builder's own, a recipe that sets its own `PATH` for a bare compiler name, or a compiled helper would not be seen; none exists. An exec-level guard (`LD_PRELOAD`) was weighed and not taken: it would load into the store suite's ASan binary, which refuses a preloaded library, and into `vfork`ed children where it could not safely allocate.
4. `ctrl_srp_image.py` and the image builders run at `ctrl_image.SHAPES` (the shipping shape and the largest), not every shipped shape: their `-D` and `-U` flags are the same at every shape, and every shape's generated headers come in through the shape dimension. The images themselves were rebuilt at all five shapes above.
5. The capture's audit hook attributes compiles by the Python stack; two threads of one process starting processes at once with no `env` of their own share one `os.environ`, so a compile's attribution can name the other thread's modules. Attribution decides only which known builders are held, never what is judged.
6. The C++ follow is a superset by design: every recorded C++ invocation's searched directories that exist, and every builder's, for every source.
7. Hosted CI and act have not run at the round-5 head (no push).
8. R584-3-S1's `FORCED` constant and ignored-error pin recipe, and R585-2-S2 (`--stack` in `aecp_arms.py`), optional, are not addressed. R584-4-S2 and R585-4-S1 (the job's own margin, about 211 s at `e07b3054`) are outside this lane; this round adds the capture's per-compile cost (well under a minute of CPU) and 20 to 26 s to the boundary step on the same idle CPUs (80 to 82 s at `e07b3054`, 101 to 106 s at the head).
9. The installed-tool rule reads inode change times against the capture's start marker. A file a builder did not write that lies outside the checkout, the temporary directory and the compile's directory, and that existed before the capture began, is taken for a tool's and not followed: in the hosted job, one written by a step before the first captured one. None exists: the hosted capture marks no source installed, and the standalone one only Verilator's three runtime sources. A host clock stepped backwards during a capture could date a builder's file before the marker; nothing guards against that.

## Round 6

Assignment: #697 comment [6102039501](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6102039501), answering [R584-5](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6101961588) (two MINOR: F1, five GCC driver spellings and a file read first define macros the boundary never judges; F2, the Verilator builders' configurations are judged by no required job, the two-interface AECP wire build by no run) and [R585-5](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6102035089) (one MINOR, F1: a `-D` in a response file). Ruling: the compiler interprets its own arguments; the Verilator-built configurations are judged in a required job of their own; R585-5-S2 and S1 now; residue R584-5-RS1 and R585-5-RS1 with their exact texts.
Base of the round: `92b5be18817659c1c9903a0544450d29ca7ab3fd` (PR #705's head). New commits only, no rebase or amend; not pushed.
Head: `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1`.
Status: REVIEW READY, comment [6103486693](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6103486693) (its text: `round6/review-ready-round6.md`). The compiler expands every recorded invocation itself; the hosted command passes against the CI-parity capture of the job's firmware steps at the exact head (101 boundary and 20 pin controls, 0 misbehaved); the new required `firmware-verilator` job's step passes in a replica on the runner's Ubuntu 24.04 toolchain (5 boundary, V1 to V3 among them, and 20 pin controls, 0 misbehaved); both captures together pass with 105 and 20; images, verdict lines, coverage and configurations are round 5's (the configurations plus `mmio_window.h`'s four).

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `715d9c9ee` | Take each recorded compile's modes, search path and files read first from the compiler's own expansion of its arguments, and refuse one it cannot expand | its own tree (`round6/c1`, every other file at `92b5be18`) in a clean clone: pyflakes, `check_py_idiom.py` (all ratchets held), and the hosted command `ctrl_boundary.py --require-rv32 --selftest --capture <cap-head> --without verilator` PASS, 101 boundary and 20 pin controls, 0 misbehaved, 123 s (`round6/logs/hgate-c1.log`) |
| `5471b0605` | Run the AECP wire comparison at every reference it pins from the processor submodule's objects, and link the MAAP differential's objects before GoogleTest | `aecp_wire.py --every` PASS at both references under a capture (142 and 294 observations); the MAAP differential PASS in the Ubuntu 24.04 container with its static GoogleTest 1.14.0, where `92b5be18`'s fails to link with R585-5's exact error (`round6/logs/maap-ubuntu-*.txt`); pyflakes; `docs_check.py` |
| `d4184ff60` | Include `<stdexcept>` in the AECP wire comparison's model, which the hosted runner's GCC 13 library does not bring in | `aecp_wire.py --every` in the Ubuntu 24.04 container (GCC 13.3): before, 13 `'runtime_error' is not a member of 'std'` errors; after, PASS at both references in 205 s (`round6/logs/aecp-ubuntu.txt`) |
| `50b3f4535` | Judge the mailbox bench's, the MAAP differential's and both AECP wire references' compiles in a required firmware-verilator job, with their controls | the job's step replicated in the Ubuntu image (below) PASS; the hosted command PASS (101 and 20, 0 misbehaved); the union of both captures PASS (105 and 20); `ci_events.py --check` OK (1848 items) and `--selftest` PASS; `act_ci.py --selftest` PASS (446 arms); `check_py_idiom.py`, `check_baremetal_only.py --check`, `check_doc_style.py`, `docs_check.py`, `check_em_dash.py --base 92b5be18` rc 0 |
| `5b4f6fbeb` | Prove the pinned Verilator in firmware-verilator under pipefail, as the physical job does, so its version check needs no waiver | found by the docs job's replay at `50b3f4535` (`measure_fail_fast.py --selftest`: a second unguarded `--version \| grep` site in `rtl-fast.yml`, which the waiver table holds once); after it `measure_fail_fast.py --selftest` 106 of 106, `ci_events.py --check` OK and `--selftest` PASS (2530 arms), `act_ci.py --selftest` PASS (446), the docs job's 54 commands rc 0 |

One-line subjects, no body, no trailers, configured identity. `git diff --stat 92b5be18 HEAD`: 15 files, 1550 insertions, 461 deletions. New: `sw/firmware/ctrl/test/ctrl_expand.py`. Changed: `ctrl_shim.py`, `ctrl_capture.py`, `ctrl_configs.py`, `ctrl_boundary.py`, `ctrl_runs.py`, `ctrl_plants.py`, `aecp_wire.py`, `aecp_wire_model.hpp` (one include), `maap_differential.py` (argument order), `sw/firmware/ctrl/README.md`, `sw/firmware/ctrl/aecp/README.md`, `docs/testing/CI_WORKFLOWS.md`, `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py`. No firmware source or header, no image builder, no mutation table, no coverage row, no Makefile, no build flag.

### Item 1: the compiler interprets its own arguments (R584-5-F1, R585-5-F1)

| What | Where (at the head) |
|---|---|
| The expansion: before it records, the recorder runs the real compiler with the invocation's own arguments, in its directory and environment, over empty read-only stand-ins of its inputs (`<capture>/expand/in/<n><suffix>`, same suffix so the driver treats each as it treats the input), its outputs and dependency options dropped (`-o`, `--output`, `-M` and its kind, `-P`, the `-d` letters), and `-E -dD -v -fpch-preprocess` added. Every other argument (a response file, `-Wp,`, `-Xpreprocessor`, the long options, `-include`, `-imacros`) is passed through for the compiler to read | `ctrl_shim.py:628` `main`; `:260` `SEPARATE` (long options added), `:271` `OUTPUTS`, `:273` `FORMATS`, `:300` `output`, `:361` `stand_in`, `:699` the added options |
| The helper (`ctrl_expand.py expand`, run with `-I -S` on a cache miss, `CTRL_CAPTURE_EXPAND`): runs the compiler (`LC_ALL=C`), keeps the report (output, messages, every entered file resolved with its SHA-256 and whether it is an installed tool's, every precompiled header it read) under `text/`, the baseline of each language (the same driver with no argument, a plain environment) once per compiler, and writes the entry the recorder reads back (each input's language, the directories searched, what must still hold for reuse). For a driver whose baseline defines `__clang__` it adds `-Qunused-arguments`: Clang makes `-c`, an object or a `-l` unused under `-E` an error under a builder's `-Werror` (found when the stack's CMake build with clang refused in the first Verilator-only run, `round6/logs/vgate-1-tail.txt`) | `ctrl_expand.py:296` `expand_main`, `:237` `preprocess`, `:251` `baseline`, `:272` `entry`, `:216` `installed` |
| Reuse: by SHA-256 over the compiler (path and file), the directory, the expansion's arguments and the environment (the capture's own two attribution variables aside), only while every file it entered and every directory it searched is unchanged and every directory it found absent is still absent, and only when every argument is a plain form (`PLAIN`, `PLAIN_PREFIX`) and none holds `@`. In the hosted job's firmware steps: 551 expansions for 23,178 expanded compiles | `ctrl_shim.py:452` `cache_key`, `:403` `load`, `:317` `plain` |
| The report, read (`units_of`, `read`): each translation unit (its main file, language from the driver's own built-ins: `__cplusplus`, `__ASSEMBLER__`), its built-ins, every definition and removal after them with the file it came from (the command line, a file read first; GCC's and Clang's markers both), every file it entered, every `pch_preprocess` pragma; from `-v` the quoted and bracketed search lists, the absent directories, and the count of compiler-proper runs. GCC's working-directory marker (`# 0 "/cwd//"`, under `-g`) is no file | `ctrl_expand.py:104`, `:149`; `:61` `RUN` |
| No expansion, refused by name (`refusal`): the compiler failed; definitions without line markers; fewer units printed than compiler-proper runs (the output went to a response file's `-o`); a unit that is no stand-in (an input a response file names, or one the recorder left in place); a stand-in entered as a file or listed as a directory (an option's value taken for an input). An invocation naming no input and no response file compiles nothing and is not expanded (`gcc --version`, `-print-file-name`) | `ctrl_expand.py:173`; `ctrl_shim.py` `expanded` in `main`; `ctrl_capture.py:425` `invocation` |
| Precompiled headers: a compile whose output is a `.gch` (or lies in a `.gch` directory, as GCC finds one) is expanded over its real inputs; a compile that reads one first (GCC reports it only as a pragma under `-E`) reads the header the capture's compile of it expanded, matched by the recorded output; one no recorded compile made refuses by name. Verilator 5.050 compiles every model object with `-include <model>__pch.h.fast`, so the Verilator jobs need this | `ctrl_shim.py:341` `produced`; `ctrl_capture.py:425-445` (`made_by`) |
| Modes (`flags_of`): per unit, every macro defined when its source begins (the driver's built-ins, the command line in any spelling, a file read first that is the checkout's or a builder's own), rendered `-DNAME` for value 1 and `-DNAME(p)=v` otherwise, and `-UNAME` for each the command line or such a file leaves undefined or the baseline predefines and the invocation does not; the C library's (files and directories of the baseline), an installed tool's (the recorder's inode rule) and a modeled header's (a shipped config's SRP shape header or a mailbox contract variant, by content) are not modes; reserved names are dropped as before. The stream-count check compares states, not spellings | `ctrl_configs.py:500` `flags_of`, `:520` `unit_flags`, `:493` `rendered`, `:538` `modes_of` |
| Files read first (`read_first`, `expanded`): every file the expansion entered, by kind; a file of the stack other than its public headers refuses by name, and so does a file of the checkout read into a compile of the stack's own sources; a tracked file of the checkout outside the stack is judged as a firmware unit (`read_first_units`: `test/mmio_window.h`, which the unit arm force-includes into `plat/mbx_plat_mmio.c`) | `ctrl_configs.py:381`, `:420`, `:446`; `ctrl_boundary.py:780` |
| The search path: the reported quoted and bracketed lists (the baseline's own left out) are the C++ follow's directories, and the recorder's header closure follows them | `ctrl_capture.py:410` `expansion`; `ctrl_shim.py:548` `closure` |
| Split: the helper and the reader moved to `ctrl_expand.py` (new, 329 lines) so `ctrl_shim.py` (804) stays under the idiom gate's 1000; `stack_gate`, `planted_run` and `control_capture` moved to `ctrl_runs.py` so `ctrl_boundary.py` (953) does; `firmware_side` takes one unit list (C++ read from the compiler's name) to stay at six parameters | `ctrl_runs.py:163`, `:180`, `:202`; `ctrl_boundary.py:731` |

The reviewers' spellings, each a standing control in `ctrl_plants.py:376-419` (all `[ok]` at the head, `round6/logs/hgate-head-1.log`):

| Control | Verdict |
|---|---|
| `-Wp,-DCTRL_R6_WP` | `firmware [-DCTRL_R6_WP]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers` |
| `-Xpreprocessor -DCTRL_R6_XP` | `firmware [-DCTRL_R6_XP]: ...` |
| `--define-macro=CTRL_R6_LONG` | `firmware [-DCTRL_R6_LONG]: ...` |
| `--define-macro CTRL_R6_LONG2` | `firmware [-DCTRL_R6_LONG2]: ...` |
| a response file `@planted.rsp` holding `-DCTRL_R6_RSP` | `firmware [-DCTRL_R6_RSP]: ...` |
| `-imacros modes.h` (a header the builder writes) | `firmware [-DCTRL_R6_IMACROS]: ...` (caught by its mode) |
| a precompiled `modes.h.gch` read first, its header then rewritten with `#error` | `firmware [-DCTRL_R6_PCH]: ...` |
| `--include-directory <work>/inc` naming where the C++ source's header is | `firmware c++: adp/adp_r5.h includes tsn-c-stack/examples/adp_port.h, ...` |
| a response file naming the source | `REFUSED: ... which the compiler could not expand: the compiler's own expansion of it compiles planted.c, an input it names where the recorder did not see it (a response file's)` |
| a response file naming the output | `REFUSED: ... the compiler preprocessed 1 translation unit(s) and printed 0: its expansion went to an output the recorder did not see (a response file's)` |
| a precompiled header whose making the recorder cannot see (its `-o` in a response file) | `REFUSED: ... which no compile the capture holds made` |
| a stack source read first (`-include <stack>/src/adp.c`) | `REFUSED: ... which reads .../tsn-c-stack/src/adp.c first, a file of the stack that is not one of its public headers` |
| `-D=1` (was: a nameless flag the reader refused) | `REFUSED: ... which the compiler could not expand: ... macro names must be identifiers` |

Reviewers' probes at the head, through the gate's own control path (`round6/probes/`):

- R584-5 `boundary_probes.py`, adapted only to the moved and renamed API (`round6/probes/boundary_probes_r6.diff`: `stack_gate`/`control_capture` from `ctrl_runs`, `without` as a `Scope`), hosted mode against the CI-parity capture: K0 CAUGHT; F1 to F6 CAUGHT by their modes (`firmware [-DCTRL_R584_WP]`, `[-DCTRL_R584_XP]`, `[-DCTRL_R584_LONG]`, `[-DCTRL_R584_LONG2]`, `[-DCTRL_R584_RSP]`, `[-DCTRL_R584_IMACROS]`); F7 (a compiler run by its path through a shell command, R584-5-S3, optional) ESCAPED, a limit the README now states (`probes-hosted-mode.log`).
- R585-5 `run_capture_probes.sh`, unchanged: `env` CAUGHT, `rsp` CAUGHT (`firmware [-DCTRL_R585_RSP]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h`, host and RV32); `abs` hooked REFUSED by name; `abs` under `python3 -I` passes, the limit R585-5-S1 asked the README to state (`r585/`, `r585-abs/`, `r585-absI/`).
- V1 to V3 (R584-5's `aecp()` plants): standing controls below, CAUGHT through the real wire-comparison capture.

### Item 2: the Verilator-built configurations in a required job (R584-5-F2)

| What | Where |
|---|---|
| `aecp_wire.py --every`: every configuration its own `REFERENCE` lists (one interface at `2ad2f845`, two at `c9f74b68`), each tree taken from the processor submodule's objects by `git archive` (the submodule is read, never changed; a revision it lacks refuses by name), each under `<output>/if<n>`; the documented `--reference/--interfaces` form stays | `aecp_wire.py:154` `reference`, `:171` `compare`, `:194` |
| The known builders run their own lists: `ctrl_configs.BUILDERS` runs `aecp_wire.py --every` (no hand-written `--interfaces 1`), the bench's default target, the differential's `--self-test` | `ctrl_configs.py` `BUILDERS` |
| `--only verilator` (`Scope`): judges the builders that need Verilator alone, under the gate's own capture (standalone), with the gate's own runs; names the firmware steps' builders and their controls left out; the text cross-check is the firmware run's | `ctrl_configs.py:293` `Scope`, `:311` `held`; `ctrl_boundary.py:842` `controls`, `:885`; `ctrl_runs.py:112`, `:140` |
| V1 to V3 and a dropped-builder control, `needs="verilator"` | `ctrl_plants.py:93` `wire_mode`, `:420-427` |
| The required job `firmware-verilator` (in `rtl-fast`'s aggregate `needs`): checkout, the five submodules, GoogleTest and GoogleMock, the pinned Verilator from the cache `verilator-lint` shares (built on a miss), on `PATH` under pipefail, the pinned RV32 SDK, then `ctrl_boundary.py --require-rv32 --selftest --only verilator`; `timeout-minutes: 40` | `.github/workflows/rtl-fast.yml:313-379`, `:386`, `:397`, `:407` |
| The CI model: the job's step list, its `$GITHUB_PATH` writer (the physical job's script), the aggregate's env | `scripts/ci_events.py:570`, `:595`, `:1263`, `:2406` |
| Two fixes the hosted runner needs, found by replicating it: the MAAP differential passed `-LDFLAGS "-lgmock -lgtest -pthread"` before its objects, and Verilator links in command-line order, so Ubuntu's static GoogleTest left `testing::InitGoogleMock` unresolved (R585-5's limits log); the wire comparison's model used `std::runtime_error` without `<stdexcept>`, which GCC 16's library brings in and GCC 13's does not | `maap_differential.py:32-38`; `aecp_wire_model.hpp:4` |

The two jobs split the builders, never an invocation: each recorded compile is judged whole, with every mode it was given, in the job that ran it. Only a run given both captures also tries a mode only one records beside one only the other does (no compile combines them); that run is below.

Controls of the Verilator run (`round6/logs/vgate-ctr2.log`, the job's step replicated):

| Control | Verdict |
|---|---|
| V1 `#if defined(PP_TOP_TIM_DEFAULTS)` in `aecp/aecp_image.h` | `firmware c++ [-DPP_TOP_TIM_DEFAULTS]: aecp/aecp_image.h includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers` |
| V2 `#if defined(PP_TOP_IF2)` | `firmware c++ [-DPP_TOP_IF2]: aecp/aecp_image.h includes tsn-c-stack/examples/adp_port.h, ...` |
| V3 `#if defined(AECP_WIRE_INTERFACES) && AECP_WIRE_INTERFACES > 1` | `firmware c++ [-DAECP_WIRE_INTERFACES=2]: aecp/aecp_image.h includes tsn-c-stack/examples/adp_port.h, ...` |
| the capture without the wire comparison's compiles | `REFUSED: the capture holds no invocation of sw/firmware/ctrl/test/aecp_wire.py, a builder of the firmware that compiles` |
| base | passes |

### Item 3: small items

- R585-5-S2: the recorder's closure fails closed: `add` and the queue stop the compile (exit 2, the reason on standard error) past `CLOSURE`, raised to 1024 headers per compile (`ctrl_shim.py:68`, `:251`, `:607`); no builder comes near it (the Verilator model compiles read Verilator's headers as an installed tool's).
- R585-5-S1: the README lists the three compilers the capture cannot see beside the bypass sentence: one a shell runs by its path (a script's, or a command run through a shell: R584-5-S3's F7), one a compiled helper runs by its path, one a Python builder started with `-I` or `-E` runs by its path (`sw/firmware/ctrl/README.md:114`).

### Item 4: residue

PR-BODY.md, exact texts: R584-5-RS1 (Status: the `92b5be18` hosted sentence replaces "Round 5 is not pushed, ..."; Round 5 item 4 and Known limitations: "the hosted step took 113 s at `92b5be18` (job 114282060753)") and R585-5-RS1 (Round 5 item 4: "Hosted at `92b5be18` (job 114282060753): the boundary step took 113 s; the store suites (108 s) and the coverage ratchet (263 s) ran; the job took 2450 s of its 2700 s."; Known limitations: "on a hosted runner at `92b5be18` it took 113 s (job 114282060753)."; Status: "Hosted checks at `92b5be18`: ..."). The two reviews give different exact texts for the same three places; both stand there verbatim. R585-5-S3 / R584-5-S1 (optional): `docs/testing/CI_WORKFLOWS.md:79` now states the hosted 113 s instead of the projection.

### Captures, configurations, images, kills

Two captures of the hosted job's firmware steps, each `fullcap.sh` (the five commands under `ctrl_capture.py`) in the CI-parity container (Ubuntu 24.04.5, CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0): `cap-head` from a tree equal to `50b3f4535`'s firmware and gate code before the `ctrl_expand.py` split (its records and reports are the same format), and `cap-exact` from a clean clone of `50b3f4535` (the gate code of the head: `5b4f6fbeb` changes only the workflow and the CI model, which neither the capture nor the gate reads). Both: 23,213 invocations (round 5: 23,213), 23,178 expanded, 35 naming no input, 551 distinct expansions (551 cache entries), 0 refusals; files read first other than the implementation's: `srp_entity_gen.h` 9,450 and `mbx_contract.h` 71 (modeled by content), `mmio_window.h` 28 (a file of the checkout, judged as a firmware unit). Step times (`logs/fullcap-head-summary.txt`, `logs/fullcap-exact-summary.txt`; the logs themselves are over 200 KB and not copied: 324,434 bytes each, sha256 `3a2b4107655db9b2425bd780e14f88e21721bf8e527f99e092a25891ab3718ec` and `87a539d91ce69a3a5184ee51f0d0fcf019f568bfe5350ac1946a4a3d84731c96`):

| Step | Round 5 (`92b5be18`'s code) | `cap-head` | `cap-exact` (host busier) |
|---|---|---|---|
| `fw_rv32_selftest.py --require-rv32` | 8 s | 8 s | 9 s |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | 1831 s | 1863 s | 2002 s |
| `test_ctrl_nvm.py --require-rv32 --jobs 4` | 86 s | 82 s | 95 s |
| `fw_coverage.py --selftest` | 0 s | 1 s | 1 s |
| `fw_coverage.py --check --jobs 4` | 263 s | 249 s | 245 s |

- Kills: the firmware gate's 845 verdict lines (843 `[ok]`, `mutants: 471 of 471 caught`, `test_ctrl_firmware: PASS`) through each capture are byte-identical to rounds 4's and 5's (sha256 `ad30597bedd62700f6947680059d962b0d97a664df4ad59cc7364448b1274ad3`, `logs/fw-verdicts-cap-head.txt`); the store gate `OK across 5 shape(s), 435 tests`; `fw_coverage.py --selftest` 29 of 29.
- Coverage: `fw_coverage.py --check` PASS (30 files), its 32-line table byte-identical to round 5's in both captures (`logs/cov-cap-head.txt`); `coverage.ratchet` unchanged.
- Images: `images6.sh` (round 5's script) on a clean clone of the head with the pinned SDK and round 1's runtime archives: 35 of 35 ELF files, built plainly and through the capture (922 RV32 invocations recorded as in round 5, 0 refusals), each manifest byte-identical to round 5's `images-head.sha256` (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`, equal to dev `aef7ac66`'s): `round6/images-head.sha256`. Every hash of the round-3 table holds.
- Configurations (`round6/scripts/record_configs6.py`, round 5's recorder, against `cap-exact`; `compare_configs.py` with value 1 written `-DX` alike): round 5's 942 configurations (794 keys) all present, none reading differently; added: `test/mmio_window.h` at host and RV32, default and with its guard defined (4 keys, 6 configurations): 948 (`logs/compare-configs-exact.txt`). Build modes 26: round 5's 22 (the same names), plus `MMIO_WINDOW_H` and `CTRL_TEST_WINDOW_WORDS` (defined by `mmio_window.h`, which the unit arm reads first) and two names the driver predefines (`unix` and its sibling), which the GNU-mode compiles define and the strict ones undefine; no unit tests either pair's, so they add no configuration but `mmio_window.h`'s own guard.
- The Verilator builders' capture (in `firmware-verilator`'s replica): 916 invocations from 18 builder runs, 28 build modes (the wire comparison's `PP_TOP_TIM_DEFAULTS`, `PP_TOP_IF2`, `AECP_WIRE_INTERFACES` 1 and 2, Verilator's `VERILATOR` and `VM_*`, its generated headers' guards), 594 configurations; Verilator's own headers read first are an installed tool's.

### Gates at the round-6 head

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --capture <cap-exact> --without verilator` (the hosted `firmware-unit` step) | host, clean clone of the head, four pinned CPUs | PASS: `51 firmware units (24 also as C++) ... 26 build modes from 23791 recorded invocations ... (948 configurations, 949 preprocessed) ...; 0 finding(s), 101 boundary and 20 pin controls, 0 misbehaved`, 123.6 s (`logs/hgate-head-1.log`) |
| the same, CPython 3.12.3, GNU make 4.3, `MAKEFLAGS=w` | the same | PASS, the same line, 134.5 s (`logs/hgate-head-parity.log`) |
| the same step, round 5's head against round 5's capture, then this round's against `cap-head`, one after the other on the same four CPUs | host | 100.5 s and 117.6 s (`logs/hgate-r5-same.log`, `logs/hgate-r6-same.log`); scaled to round 5's hosted 113 s, about 132 s of the 300 s budget |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (the `firmware-verilator` step) | Ubuntu 24.04 image (`round6/scripts/Containerfile.697c-r6-ci`: the CI-parity image with Ubuntu's cmake 3.28 and clang 18), pinned Verilator 5.050 and RV32 SDK mounted, clean clone of the head, four pinned CPUs | PASS: builders 57, 139 and 212 s; `5 boundary and 20 pin controls, 0 misbehaved`; V1 to V3 caught by name; 452 s (`logs/vgate-ctr-head.log`; 440 s at `50b3f4535`'s code, `logs/vgate-ctr2.log`) |
| the same on the host (gcc 16, CPython 3.14) | host clone | PASS, 430 s with the container capture loading the host (`logs/vgate-2.log`) |
| both captures given, nothing left out (`--capture cap-head --capture <Verilator builders' capture> --capture <wire comparison --every capture>`) | host clone | PASS: `48 build modes from 24152 recorded invocations ... (948 configurations ...) ...; 0 finding(s), 105 boundary and 20 pin controls, 0 misbehaved`, 150 s (`logs/union.log`) |
| commit `715d9c9ee`'s tree alone, the hosted step | host clone of `92b5be18` with that commit's files | PASS, 101 and 20, 0 misbehaved, 123 s (`logs/hgate-c1.log`) |
| `aecp_wire.py --every` | Ubuntu image, four CPUs | PASS at both references, 142 and 294 observations, 205 s; at `5471b0605` 13 `runtime_error` errors (`logs/aecp-ubuntu.txt`) |
| `maap_differential.py` | Ubuntu image | PASS, 12 tests; `92b5be18`'s fails to link (`undefined reference to testing::InitGoogleMock`, exit 2) (`logs/maap-ubuntu-*.log`) |
| the docs job's 54 commands (`round6/scripts/docsjob.sh`, CPython 3.12.3 with the locked renderer) | clean clone of the head with the docs job's three submodules | 54 of 54 rc 0 (`logs/docsjob-three.txt`): `ci_events.py --check` OK (1848 items), `--selftest` PASS (2530 arms); `check_em_dash --base 92b5be18` 0 findings over 69 added lines in 3 pages; `check_py_idiom.py` every ratchet held; `check_baremetal_only.py --check` OK (1240 files); `docs_check.py` 0 findings; `measure_fail_fast.py --selftest` 106 of 106. At `50b3f4535` 53 of 54 (`logs/docsjob-head.txt`): the fail-fast waiver, fixed by `5b4f6fbeb` |
| `act_ci.py --selftest --worktree <head>` (installed 0555 outside the tree, sha256 `797f123b…d22d1`, unchanged by this round) | host, CPython 3.12.3 | PASS, 446 arms (`logs/act-selftest-2.log`) |
| pyflakes over the gate modules; `check_py_idiom.py` under CPython 3.12.3 and 3.14 | host | rc 0 |
| R584-5 probes (`round6/probes/boundary_probes_r6.py`), R585-5 probes (unchanged) | host clones, against `cap-head` | as in Item 1 (`round6/probes/`) |

Not run in round 6: the standalone gate with no capture (every builder, firmware steps included, under the gate's own capture, about 50 minutes; the union run judges the same captures and controls, and the Verilator-only standalone runs those builders by their own commands); `tally_selftest.py --mutants`; act and hosted CI (no push).

### Open risks and questions (round 6)

1. The hosted figures of `firmware-verilator` and of `firmware-unit` at this head need a push; the local replica of the new step took 440 s on four CPUs (setup excluded), against a 40-minute timeout. A Verilator cache miss adds its source build (about 10 to 15 minutes) to that job, as it does to `verilator-lint`.
2. The capture's path to a file of the checkout is the capture's checkout: judged from another tree (a reviewer's clone given this round's capture), `mmio_window.h` is the builders' own file there (macros as modes, not judged as a unit). Hosted, the capture and the judgement share one checkout.
3. Three compilers the capture cannot see (README:114): a shell's by path, a compiled helper's by path, a Python builder's under `-I`/`-E` by path. No builder has one.
4. The cache trusts what the report lists: a file a compile reads that the report does not show (a specs file, a plugin) makes its argument non-plain, so it is not reused; a precompiled header changed under the same name, path and arguments while its header's stat holds would be the one case left, and no builder rewrites one.
5. Built-in non-reserved macros (`unix` and the like) become modes from the builders that define them (the GNU-mode compiles) and are undefined in the gate's strict preprocessing; no unit tests them, so they add no configuration (948 configurations, the same reads as round 5's 942 plus `mmio_window.h`'s).
6. The Verilator-generated model headers a model object reads first through its precompiled header are the builders' own files: their include guards become modes in the Verilator run (no firmware unit tests them).
7. `firmware-unit`'s own headroom (2450 s of 2700 at `92b5be18`) is the manager's separate issue; this round adds no step to it and its steps' time under the capture changed by under 1% (2203 s against 2188 s in the container).
8. R584-3-S1 (the `FORCED` constant now only names the dimension's header; forced files are the compiler's report) and R585-2-S2 (`--stack` in `aecp_arms.py`): optional, not addressed.
