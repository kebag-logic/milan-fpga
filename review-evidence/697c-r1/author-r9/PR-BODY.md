[A583]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — What R584-1 and R585-1 asked for, and how each gap is closed by construction.
- **[Round 2b](#round-2b)** — The merge of dev after F5 (AECP), and how the boundary, the pin check and the mode derivation cover what F5 added.
- **[Round 3](#round-3)** — How R584-2's and R585-2's two gaps and R585-2-S1 are closed by derivation.
- **[Round 4](#round-4)** — How the boundary step fits five minutes with every configuration kept, and how R584-3-F1 and R585-3-S1 are closed.
- **[Round 5](#round-5)** — How the gate judges the builders' recorded compiler invocations, by construction, and fails closed on a missing, empty or incomplete capture.
- **[Round 6](#round-6)** — How the compiler reads each recorded invocation's arguments itself, and how a required job judges what only the Verilator builders compile.
- **[Round 7](#round-7)** — How each compile's own dependency list decides both sides, with the gate's own resolution removed.
- **[Round 8](#round-8)** — How the boundary moves to its own job, which runs the gate's known builders by their builds, and what each job's budget is.
- **[Round 9](#round-9)** — How the stack pin proof reads only the real objects through one Git helper that a census holds, over the whole tree, and how the README's figures are checked against the self-test.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/CONTRIBUTING.md).

## Status

GREEN locally at `feed95bbb6429e5af0ee3f0a24c531777279e9de` (round 9, three commits on `4cab445a`): the stack pin proof starts Git only through one helper, run with `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE` naming a path that cannot exist, so Git reads the real objects only; it compares the submodule's whole checkout with the pinned tree (every path, type, mode and blob, hashed from the files' own bytes); a census refuses any Git command the proof's modules start outside the helper; the firmware README gives the boundary self-test's own figures (96 defects, 8 passing, 5 in the Verilator run, 30 pin controls), which the self-test now checks. In the runner's Ubuntu 24.04 replica on four CPUs at the head: `firmware-boundary`'s step PASS in 677 s (38 % of 30 minutes; 105 boundary, 30 pin and 4 figure controls, 0 misbehaved), `firmware-verilator`'s PASS in 492 s (21 % of 40); `firmware-unit`'s steps every one rc 0 in 2051 s at `107aab30` (no module they load changed after it); both reviewers' probes print a refusal for every replacement case, and every entry point refuses each disguise by name (85 of 85); the firmware gate's 845 verdict lines, the coverage table and 35 of 35 RV32 images are identical to round 8's — `697-consume` -> `dev`, not pushed; REVIEW READY in #697 comment [6108314179](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6108314179).

Round 8: GREEN locally at `4cab445aa2475903b6cf8b87566d2c8a1e15e391` (round 8, six commits on `8436dfc0`): the boundary leaves `firmware-unit` for a new required job, `firmware-boundary`, which runs `ctrl_boundary.py --require-rv32 --selftest --without verilator` with no capture given, so the gate reads its builders from its own known set and runs each by its builds, not its suites (the suite gates' new `--build-only`: every binary built and linked, none run, nothing planted); `firmware-unit` runs dev's steps with no capture; the `rtl-fast` aggregate requires the new job and `scripts/ci_events.py` pins it; a known builder is held by a run of its own, and a builder dropped from the known set refuses by name even where another builder still runs it. In the runner's Ubuntu 24.04 replica on four CPUs at the head: `firmware-boundary`'s step PASS in 682 s (38 % of its 30 minutes; 105 boundary and 20 pin controls, 0 misbehaved), `firmware-verilator`'s PASS in 494 s (21 % of 40), `firmware-unit`'s steps every one rc 0 in 1986 s (74 % of 45, its suites alone); the firmware gate's 845 verdict lines, the coverage table and 35 of 35 RV32 images are identical to round 7's — `697-consume` -> `dev`, published; REVIEW READY in #697 comment [6106923767](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6106923767). Hosted at `8436dfc0` (the manager's check): `firmware-unit` cancelled at its 45 minutes (job 114392589133), the firmware step after 39 min 43 s; `firmware-verilator` passed in 11 min 22 s (job 114392589175).

Round 7: GREEN locally at `8436dfc0bd5e0f3c592dd1faa0a4ced1841a2651` (round 7, four commits on `5b4f6fbe`): the gate judges exactly the sources the capture recorded as compiled, each by the compiler's own dependency output for that invocation, and classifies every file a compile read by where it lives, building no include path and listing no source; the hosted command passes against a CI-parity capture made with the round's recorder (22,528 compiled sources of 23,795 invocations, 0 findings, 103 boundary and 20 pin controls, 0 misbehaved, 73 s on four CPUs, where `5b4f6fbe`'s step took 132 s on the same CPUs); the `firmware-verilator` step passes in the runner's Ubuntu 24.04 replica in 472 s (6 boundary and 20 pin controls); R584-6's N1 and R585-6's Q7 are standing controls refused by name, and both probes fail the gate on the real path; 35 of 35 RV32 images, the firmware gate's 845 verdict lines and the coverage table are identical to round 6's; the firmware steps take 13% longer under the capture (2497 s against 2203 s in the container) — `697-consume` -> `dev`.

Round 6: GREEN locally at `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1` (round 6, five commits on `92b5be18`): each recorded compile's modes, search path and files read first are the compiler's own expansion of its arguments, so `-Wp,`, `-Xpreprocessor`, `--define-macro`, `--include-directory`, a response file, `-imacros` and a precompiled header each give the mode they give the compile, and an invocation the compiler cannot expand refuses the gate by name; the hosted command passes against the CI-parity capture of the job's firmware steps at this head with 101 boundary and 20 pin controls, 0 misbehaved (117.6 s on four CPUs where `92b5be18`'s took 100.5 s on the same CPUs); the new required `firmware-verilator` job's step, replicated on the runner's Ubuntu 24.04 toolchain, passes in 440 s with V1 to V3 caught by name; both captures judged together pass with 105 and 20; round 5's 942 configurations are judged unchanged, with the four of `mmio_window.h` (read first by the unit arm) added; 35 of 35 RV32 images, the firmware gate's 845 verdict lines and the coverage table are identical to round 5's — `697-consume` -> `dev`. Hosted checks at `e07b3054`: `rtl-fast` success; `firmware-unit` passed in 41 min 29 s of its 45 (job 114206016568), its boundary step in 93 s, with the store suites and the coverage ratchet run. Hosted checks at `92b5be18`: `rtl-fast` success; `firmware-unit` success in 2450 s, its boundary step in 113 s; `verilator-suites` and `yosys-portability` success. `firmware-unit` succeeded in 31 min (job 114344992704), its boundary step in 93 s; `firmware-verilator` succeeded (job 114344992708), its step in 438 s; `rtl-fast`, `verilator-suites` and `yosys-portability` succeeded at `5b4f6fbe`.

## Linked Issue / roles

Relates to #697

Executor: `[A583]`
Internal cleared-context reviewer: `[R584]`
External reviewer: `[R585]`

## Description

milan-fpga now takes its ADP, ACMP and MAAP cores and the wire layer from the
[tsn-c-stack](https://github.com/kebag-logic/tsn-c-stack) submodule at
`third_party/tsn-c-stack`, and no longer holds copies. No firmware behaviour
changes: both linked RV32 images are byte-identical at every shape.

| Piece | Change |
|---|---|
| Submodule | `third_party/tsn-c-stack` pinned at `1a9f651cdf7846b8e10ac246a6ef6916960fbb92`, the newest tsn-c-stack commit whose cores are milan-fpga's code token for token and line for line. `.gitmodules`, `scripts/act_ci.py` `TRUSTED_SUBMODULES` (with four new refusal arms), the submodule map, its diagram and `THIRD_PARTY.md` (MIT). |
| Copies removed | `git rm` of `adp.{c,h}`, `acmp.{c,h}`, `maap.{c,h}`, `wire/wire.h` and the core-test copies `test_acmp.cpp`, `acmp_fake.hpp`, `test_adp_reentry.cpp`, `test_maap_debug.cpp`; the core cases of `test_adp.cpp` and `test_maap.cpp` go too, their adapter and CSR cases stay. |
| Build | `ctrl_build.py` names the cores `tsn-c-stack/src/*.c` in the same link order and includes only the stack's `include/`; the arms build the stack's own core tests into the same binaries under the same tally labels (`fw_gtest_label.cpp` for a binary whose test files name no label). The `mbx` bench Makefile, the SRP arms, the MAAP differential and both image fixtures build from the stack. |
| Evidence readers | `ctrl_image.py --base` and `ctrl_srp_image.py --ctrl-source` measure a pre-move tree with its own cores and a later one with its recorded stack. |
| Coverage | `fw_coverage.py` measures the stack's `src/` and `include/` (never its tests or examples), with a new planted case; the ratchet is regenerated: same counts on the new paths, and `srp_mbx.c` moves from a stale 515 to the 514 lines dev already measures. |
| Mutation tables | Core plants name the stack's files; 43 plants whose anchor was a comment the stack removed take the stack's own re-anchored text; every planted program is token-identical to dev's. Two killers take the stack's words, see below. |
| Boundary | New `ctrl_boundary.py`, judging exactly the sources a capture of the firmware's builders' compiler invocations recorded as compiled (`ctrl_capture.py`, round 5), each by the compiler's own dependency output for that invocation (`-M` and `-H` with its own arguments, directory and environment, round 7), every file a compile read classified by where it lives. A compile of a firmware source (the saved-state store's and the images' own included) reads no stack file outside `include/`, and no firmware file includes one in any compile; a compile of a stack source reads, through its own `#include` lines, only the stack's files and the C implementation's headers, and no stack file includes anything else; the stack's tests reach nothing of this repository outside the submodule; no file under `sw/firmware` is named as a stack source or header; and the stack's own `scripts/check_boundary.py` runs. |
| Pin check | One shared check, `ctrl_build.stack_pin` (`ctrl_build.py --stack-pin` for the Makefile), proves the stack's content: every file of its sources, headers, tests, examples, scripts and CMake files must hash to the gitlink's tree, with nothing added, read from the files rather than the index. The host test (with coverage), the boundary gate, the MAAP differential in both modes, the mailbox bench and both image fixtures with the submodule as their stack run it first; in a Makefile, every target whose recipe builds against the stack has it as a prerequisite (`ctrl_pin.py`, round 3). |
| CI | `firmware-unit` and the Verilator shards fetch the submodule; two new required jobs judge the boundary: `firmware-boundary` (round 8) runs every known builder but the Verilator ones by its builds under the gate's own capture, and `firmware-verilator` (round 6) the Verilator ones; `firmware-unit` runs its suites with no capture; `scripts/ci_events.py` pins all of it. |
| Docs | A "TSN stack submodule" section in `sw/firmware/ctrl/README.md` (what it provides, what it must not depend on, its tests, MIT inside this CERN-OHL-W platform), and every reference to the old paths; `README.md`, `QUICKSTART.md` and `CONTRIBUTING.md` initialise the submodule wherever every Verilator suite runs. Links into the stack use pinned URLs, since the docs gates run without submodules. |

Two killers changed words, not kills: the stack's two A29 tests now assert the
admission and withdrawal counts first, so `acmp-admit-ignores-another-talker`
and `acmp-reset-forgets-the-admitted` fail the same tests on the stack's words.
Its own table uses those words.

## Round 2

[R584-1](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6092573026) and
[R585-1](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6092623741) were NEGATIVE on
MINOR gaps in the boundary and pin gates. Round 2
([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6092628778)) adds three
commits on `60e7b57c` and changes no firmware source, test, mutation table or build flag.

| Finding | Closed by |
|---|---|
| R585-1-F1: the boundary was judged in one configuration | The gate reads the build modes from the builders themselves (every `-D`/`-U` flag literal in `ctrl_build.py`, `ctrl_arms.py`, `srp_arms.py`, both image fixtures, the MAAP differential and the bench's Makefile), never from a list of its own. GCC's `-dU` reports the macros each unit's preprocessing tests; the gate preprocesses every combination of their modes, with every other mode defined, until none is new. Both directions run on the host and for RV32. A finding names its configuration, e.g. `host [-DCTRL_REENTRY_ASSERT]: ...`. R585-1's three escaped probes are each refused by name. |
| R585-1-F2 = R584-1-F1: two gates built an unpinned stack | The MAAP differential (both modes; new `--stack`, default the submodule) and the mailbox bench (a phony `stack-pin` prerequisite of its firmware library) run the same `stack_pin` first. Planted controls: the bench accepts a pinned clone; the bench and both differential modes refuse an edited one before building. |
| R584-1-S1: the pin trusted `git status` | `stack_pin` hashes every file of `src/`, `include/`, `tests/`, `examples/`, `scripts/`, `cmake/` and `CMakeLists.txt` and compares it with the gitlink's tree; added files are refused; the index is never read. An `assume-unchanged` edit, an edited script or CMake file and an added header are refused. |
| R584-1-S2: the stack's tests were outside the boundary | The stack's `tests/*.cpp` and `*.hpp` are preprocessed as C++ with the arms' test include path in every configuration; a dependency inside this repository outside the submodule is refused. The real-path `#include "mbx_hal.h"` plant in `tests/test_maap_debug.cpp` fails the gate by name. |
| R585-1 residue | R1 to R4 in this body; R5 in the five `adp.c` coverage rows of `sw/firmware/gtest/README.md`. |

At round 2's head the boundary self-test plants 25 defects refused by name, 3 passing controls and 12 pin
controls, all as expected. A real-path run in a disposable clone, editing the clone's own submodule, is
refused by the bench, both differential modes, the host test, the pin check (an `assume-unchanged` edit) and
the boundary gate (an edited script), each by name. The images (25 of 25), coverage (22 files, same counts), the firmware gate's
verdicts and the MAAP and bench tallies are unchanged from round 1.

## Round 2b

F5 (#700, the AECP core under `sw/firmware/ctrl/aecp/`) merged into dev as `aef7ac66` and conflicted
with this branch. Round 2b ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6093389868))
merges dev in as one merge commit, `386b8e69`, with no rebase. AECP is not part of tsn-c-stack: it stays
this firmware's, and every F5 source, test, coverage row and mutation entry is kept.

| What | Resolution |
|---|---|
| Conflicts | `sw/firmware/ctrl/README.md` keeps both layout rows; `ctrl_srp_image.py` keeps the stack's `source_tree` and F5's `--with-aecp` composition, with the cores from the stack. |
| F5's builders | `aecp_arms.py` and `aecp_wire.py` named the removed `wire/`: they now take the stack's `include/`, the application arm builds the cores from the stack, and the AECP tests find `acmp_fake.hpp` in the stack's `tests/` (token-identical to dev's copy). |
| Pin check | `aecp_arms.py`, `aecp_mutants.py` and `aecp_wire.py` take `--stack` (the submodule by default) and run the shared pin check first when run alone; in the firmware gate they run after its pin check. Three pin controls refuse an edited clone in each. |
| Boundary units | The firmware's units are every directory of `sw/firmware/ctrl` but `host/` and `test/`, and every C source under `test/`: F5's core, adapters, application bridge and AECP image are judged (51 units, 34 before). The include path adds every firmware directory, and the entity generators' headers (`aecp_entity_gen.h` among them) are generated, not stood in for. |
| Mode derivation | The builders are found, not listed: every Python module and Makefile of the checkout that names `sw/firmware/ctrl` or `ctrl_build`. F5's `AECP_TEST_APP`, `AECP_TEST_MAILBOX` and `AECP_TEST_NVM` come from `aecp_arms.py` with nothing added to the gate; names the C implementation reserves (the runtime builder's `_LIBC`) are not modes. |
| Controls | Eight new boundary controls, each refused by name: a stack include under F5's `AECP_TEST_APP`; a mode written only in a new builder file; the stack including `aecp.h`; a stack test including `aecp_mbx.h`; the AECP core, its application bridge and the AECP image's SRP composition reaching the stack outside `include/`; a copy named `aecp/acmp.h`. |

The merge alone did not pass: F5's arms could not build, and the round-2 boundary gate refused
`app/ctrl_app_aecp.c` for RV32. So the merge commit carries the resolution, and every gate passes at it.
Real-path probes in a disposable clone: an edited `src/acmp.c` is refused by the three AECP tools, the AECP
image and the firmware gate, and three boundary plants fail the gate by name.

## Round 3

[R584-2](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6094643793) and
[R585-2](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6094869698) were NEGATIVE on the
same two MINOR gaps; R585-2-S1 is required now. Round 3
([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6094873968)) adds three
commits on `386b8e69`, with no rebase, and changes no firmware source, header, test, mutation table, coverage
row or build flag. `ctrl_image.py` only moves its shape's flags and headers into `shape_build`, which
`measure` calls, so the gate can take the same. The third commit makes the gate refuse by name (exit 2), not
crash, when the end-station builder it now loads every shape through lacks `gptp-processor`, which
`firmware-unit` initialises.

| Finding | Closed by |
|---|---|
| R584-2-F1 = R585-2-F1: firmware headers judged only as C, and the image only at a hand-listed 1/1 | Each unit is judged as its builders compile it, read from them by the new [`ctrl_configs.py`](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/sw/firmware/ctrl/test/ctrl_configs.py); the gate lists no flag, and its `FIRMWARE_DEFINES` and `SRP_ENTITY` are gone. Language: every unit is C, and a firmware unit that a C++ source a builder names reaches is C++ too, with the arms' test flags and include path (every `#include` followed as text; 24 of 51 units). Values: the image's stream counts come from `ctrl_image.shape_build` at every shipped config (5/5, 2/1, 2/2 and 9/9, or undefined, as every other builder leaves them); a judged unit whose includes depend on any other value a builder computes is refused. Shapes: every shipped config's generated headers, from the builders' own generators; the SRP shape header force-included, as the SRP builds compile, or not. The mailbox contract: tracked, or the variant its generator writes for every other interface count it admits (2). A configuration that stops on an `#error` is one no builder compiles; what it reads is still judged. R584-2's `IMAGE_SINKS > 1u` stack-example include and R585-2's C++-only `acmp_fake.hpp` include are controls, each refused by name, with five more for the derived dimensions. |
| R584-2-F2 = R585-2-F2: `run-if2` compiled against the stack unpinned | `run-if2` and `run-cosim` take `stack-pin` as a prerequisite, as the firmware library does. The new [`ctrl_pin.py`](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/sw/firmware/ctrl/test/ctrl_pin.py) reads every Makefile builder's targets from make's own database and dry run: a target whose recipe names the stack without the pin check as a prerequisite is a finding. Self-test: every target whose dry run reaches the stack (`all`, `run-cosim`, `run-if2`, the firmware library and `stack-pin`) runs for real in a scratch copy against a clone with a poisoned `wire.h` and a simulator that builds nothing; each refuses on the pin check, naming `include/wire.h`, and never compiles the poisoned header. A planted Makefile without the prerequisite is refused by name. |
| R585-2-S1: a mode written as two arguments | `-D NAME` and `-U NAME` (two literals of a list, a tuple or a call, or two words of a Makefile line) are derived like `-DNAME`; a bare flag before an expression the gate cannot read refuses the gate. A Python and a Makefile control, each refused by name. |
| R584-2-R1; R585-2-RS1 to RS3 | This body: links at the head, Status, Known limitations, How to validate. |

At `d1b22e80` the boundary self-test passes: 45 boundary controls (42 refused by name, 3 passing) and 20 pin controls. Every probe the two reviews published, rerun unchanged against a clean clone of the head, is refused by name: R584-2's ten boundary probes and its shape probe; its pin probes S0 to S6, where S6 (`make run-if2` on a poisoned `wire.h`) now exits 2 on the pin check; R585-2's eleven boundary probes, n1 to n4 among them; and its 27 pin arms, `WIRE-mbx_run_if2` among them. The images (35 of 35), coverage (30 files, the same counts), the firmware gate's 843 verdicts, the bench's tallies and the MAAP differential are unchanged.

## Round 4

[R585-3](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6096142856) (one MAJOR) and
[R584-3](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6095873264) (one MINOR) were
NEGATIVE; R585-3-S1 is required now. Round 4
([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6096148471)) adds four
commits on `d1b22e80`, with no rebase, and changes only the boundary gate, its new controls module and their
docs: no firmware source, header, test, builder, mutation table, coverage row, build flag or workflow.

| Finding | Closed by |
|---|---|
| R585-3-F1: `firmware-unit` timed out at 45 minutes inside the boundary step | The step judges the same configurations, modes and shapes, every control kept, but does each piece of work once. Each preprocessing runs once per run and is reused only for the same unit and arguments, every file it read byte-identical (by digest), and no file added or removed since that it could look up by name. The controls share one prepared base, the unplanted copies, judged first and required to pass. A control that must be refused stops at the finding it names. A unit's configurations go to four compilers at once and every side runs at once; the stack's own gate runs beside the rest. Pinned to four CPUs on a loaded shared host, the step took 75 s, against 807 s at `d1b22e80` on the same host (the hosted step then passed 12 minutes). A scratch check judged every control in full with and without reuse: 0 of 60 differ. The budget (5 of the job's 45 minutes) and the measurement are in [`CI_WORKFLOWS.md`](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/docs/testing/CI_WORKFLOWS.md). |
| R584-3-F1: `test/test_maap_differential.cpp`, named relative to the firmware tree, was not followed | A builder's C++ name now resolves in the firmware tree too, and in every directory of the checkout the builder names (so `aecp_wire.py`'s `sim_main.cpp` resolves to the processor's `tb/pp_top/`). A name the builder writes (`reference.cpp`) is followed through the builder's literals. A name that resolves to no file, or that a builder computes, fails the gate by name; `NOT_SOURCES` lists the two paths a coverage self-test writes into a planted report, each checked. R584-3's `maap_r584.h` plant, through the differential's source, is a control refused by name. |
| R585-3-S1: a flag that is neither a literal nor an f-string | Refused by name, in Python (`"-D" + NAME`, `"-DNAME=" + value`, `"-D%s" % NAME`, a bare `-D` alone, a computed macro name in an f-string) and in Makefiles (`-D$(NAME)`, `-DNAME=$(VALUE)`, `$(addprefix -D,...)`). No builder uses these forms, so the derived modes are unchanged. |
| R585-3-RS1 | This body: Status and Known limitations. |

At the head the boundary self-test passes with 60 boundary controls (the base, 56 refused by name and 3
passing) and 20 pin controls; fourteen controls are new in this round (59 plants against 45 at `d1b22e80`, beside the shared base). R584-3's and R585-3's published probes,
rerun unchanged: R584-3's `cplusplus-new-header-maap-differential` and R585-3's real-path differential probe,
both escaped at `d1b22e80`, are refused by name, and R585-3's f1 to f4 are refused by name; every other probe
gives the verdict it gave at `d1b22e80`. The images (35 of 35), coverage (30 files, the same counts) and the firmware gate's 843 verdicts are unchanged.

## Round 5

[R584-4](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6097725381) and
[R585-4](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6097795358) confirmed the hosted
timeout resolved and were NEGATIVE on one class, for the third round: configurations read from builder text
miss forms. Round 5 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097800045))
rules it by construction: the gate judges the builders' actual compiler invocations. Five commits on `e07b3054`,
no rebase; no firmware source, header, test, image builder, mutation table, coverage row, Makefile or build
flag changes.

| Item | How |
|---|---|
| 1. Capture | `ctrl_capture.py --out DIR -- COMMAND` runs a builder with a recording wrapper first on `PATH` for every C and C++ compiler name, the RV32 compiler (`MILAN_RV32_CC`) and `CC`/`CXX`. The wrapper runs a small C recorder (`ctrl_shim.py`, compiled into the capture when it starts): it appends one record per invocation (arguments, directory, each source and its language, the files read first, the builder files) and then runs the real compiler with the same arguments. It keeps the text of every C++ source, and of the headers outside the checkout a C++ source reaches in a builder's own directories, so a written and deleted source is still read. A C++ source outside the checkout, the temporary directory and the compile's directory that existed before the capture began (its inode changed before the capture's start marker) is an installed tool's, Verilator's runtime: it is recorded as such and not followed; a source a builder writes or copies anywhere is its own. A Python audit hook names the builder modules on the stack of each compile. `firmware-unit` runs its firmware suites, store suites and coverage steps under one capture and judges it in the boundary step, now last; the boundary runs the stack's own CMake build and the image builders under it itself. The recorder adds a millisecond or two to each of the job's 23,213 compiles. |
| 2. Fail closed | Refused by name: a missing capture, an empty one, one whose builder run failed; a known builder (`ctrl_configs.BUILDERS`) it holds no invocation of; a builder found by text (the round-2 discovery, kept only as this cross-check) that compiled nothing and is listed nowhere; a compiler a builder runs by a path no wrapper stands on (the audit hook for Python, make's own dry run for a Makefile recipe); a C++ compile of a source that was no file, or of standard input; a nameless `-D`; a stream count no shipped shape gives. Run standalone, the gate runs every known builder under its own capture first. The builders that need Verilator (the mailbox bench, the MAAP differential, the AECP wire comparison) are left out only by `--without verilator`, named on every run; the hosted job has no Verilator. The static derivation of modes and C++ names from source text is removed. |
| 3. Plants | 88 plants and the base (89 controls: 83 refused by name, 5 passing beside the base; round 4: 60). Every builder plant is a builder that runs through the capture. Each form R584-4 and R585-4 listed, and round 4's: `$(patsubst ...)`, `$(foreach ...)`, `VAR+=-D` with no space, `-D $(M)`, `-D$(MODE)`, `-DNAME=$(VALUE)`, `$(addprefix ...)`, a mid-string f-string, a split multi-word literal, a shell command's literal, `shlex.split`, a bare `-D` before a conditional, `str.format`, `+`, `%`, an f-string macro, a bare `-D` before a list; a C++ source named by `$(wildcard ...)`, a join, `glob`, `iterdir`; one written from a literal, an f-string include, a formatted template, a copied template file, or through a header written beside it; one written, or copied out of the builder's directories, whose include a macro computes. Each is caught by the finding it names, and so are the fail-closed cases of item 2; an installed tool's source with such an include passes. Through real builders too: the four Makefile forms planted into the mailbox bench's firmware recipe and four Python forms into `ctrl_image.py`'s flags are each caught end to end, and a recipe naming its compiler by an absolute path is refused. |
| 4. Budget | On four otherwise idle pinned CPUs of a shared host the step took 101 to 106 s, where `e07b3054`'s took 80 to 82 s on the same CPUs; the hosted step took 93 s at `e07b3054`, so the same ratio puts the worst near 124 s, 59% inside the 5 minutes. The slowest local run, 215 s on CPUs other jobs held, left 85 s. The job's other steps change only by the recorder's per-compile cost; the hosted step took 113 s at `92b5be18` (job 114282060753). Hosted at `92b5be18` (job 114282060753): the boundary step took 113 s; the store suites (108 s) and the coverage ratchet (263 s) ran; the job took 2450 s of its 2700 s. |
| R584-4-RS1, R585-4-RS1 | This body: Status, Round 4 (60, fourteen) and Known limitations. |

The judged configurations are the same as round 4's: 942, with 794 distinct (side, unit, label), none on
one side only and none read differently. The build modes are 22. They are round 4's 18, less the two that only
the Verilator-needing `aecp_wire.py` writes, plus six that round 4 called computed values, now concrete
recorded values. The firmware units judged as C++ are the same 24. Standalone, with Verilator, the capture adds the bench, the MAAP
differential and the AECP wire comparison: 33 build modes, the same 942 configurations. The images (35 of 35), the firmware gate's 845
verdict lines and the coverage table, all taken through the capture, are byte-identical to round 4's.

## Round 6

[R584-5](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6101961588) and
[R585-5](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6102035089) were NEGATIVE on MINORs
only: the capture's own reader decided what an argument meant, so a spelling it did not parse escaped (F1 of both),
and what only the Verilator builders compile, the AECP wire comparison's two-interface build included, was judged by
no required job (R584-5-F2). Round 6 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6102039501))
rules both by construction. Five commits on `92b5be18`, no rebase; no firmware source, header, image builder,
mutation table, coverage row or build flag changes. Replicating the new job on the runner's toolchain found two test
fixes it needs: the MAAP differential's link order, and one missing include in the AECP wire comparison's model.

| Item | How |
|---|---|
| 1. The compiler interprets its own arguments | Before it records, the recorder runs the real compiler with the invocation's own arguments, in its directory and environment, over empty stand-ins of its inputs (same suffix), its outputs dropped, with `-E -dD -v -fpch-preprocess` added. The line markers give each translation unit, where every macro came from and the files read first; `-v` gives the search path; the same driver with no argument gives what is the implementation's. Modes are the macros each unit has when its source begins (built-ins, command line, a file of the checkout or a builder's read first), not the C library's, an installed tool's or a modeled shape header's. A file of the stack's other than its public headers read first refuses, a file of the checkout read first is judged as a firmware unit (`mmio_window.h`), a precompiled header resolves to the recorded compile that made it. An invocation the compiler could not expand refuses by name: a failure, a translation unit the recorder did not see (a response file's), output sent elsewhere (a response file's `-o`), a stand-in taken as an option's value. Expansions are reused only for plain arguments with every reported file and directory unchanged: 551 for the job's 23,178 compiles. Standing controls: `-Wp,-D`, `-Xpreprocessor -D`, `--define-macro=X`, `--define-macro X`, `--include-directory`, a response file, `-imacros`, a precompiled header, each caught by its mode; a response file naming a source or an output, an unmade precompiled header, a stack source read first, `-D=1`, each refused by name. |
| 2. A required job for the Verilator builders | `aecp_wire.py --every` runs each reference its own list pins (one and two interfaces, trees from the processor submodule's objects); `ctrl_configs.BUILDERS` runs the builders' own lists; `ctrl_boundary.py --only verilator` judges those builders alone, under the gate's own capture, with their controls (V1 to V3, and the capture without the wire comparison). The required `firmware-verilator` job runs it with the pinned Verilator from the cache `verilator-lint` shares, inside `rtl-fast`'s aggregate, `timeout-minutes: 40`. Replicated on Ubuntu 24.04 (GCC 13.3, static GoogleTest 1.14.0, clang 18, CPython 3.12.3) on four CPUs: 440 s, V1 to V3 caught by name. `firmware-unit` is unchanged. |
| 3. R585-5-S2, S1 | The recorder stops a compile (exit 2) whose C++ source reaches more headers than one compile keeps (now 1024). The README lists the three compilers the capture cannot see beside the bypass sentence (a shell's by path, a compiled helper's, a Python builder's under `-I`/`-E`). |
| 4. Residue | R584-5-RS1 and R585-5-RS1 applied verbatim (Status, Round 5 item 4, Known limitations); both texts stand where they overlap. R585-5-S3 / R584-5-S1: the CI page states the hosted 113 s. |

Reviewers' probes at the head: R584-5's F1 to F6 CAUGHT by their modes, K0 CAUGHT, F7 (a shell command, optional
S3) a stated limit; R585-5's `env` and `rsp` CAUGHT, `abs` hooked REFUSED, `abs` under `-I` a stated limit; V1 to V3
CAUGHT in the Verilator run. The configurations judged are round 5's 942, unchanged in what each reads, plus
`mmio_window.h`'s four; the build modes are 26 (round 5's 22, with the two `mmio_window.h` defines and two names the
driver predefines, `unix` and its sibling, which no unit tests).

## Round 7

[R584-6](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6104503651) and
[R585-6](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6104708471) were NEGATIVE on MINORs
only: the firmware side's population came from directory listings, so the saved-state store's sources, which both
images compile, escaped it (F1 of both, probe N1), and the stack side resolved headers on a fixed search path, so a
platform header in a directory only a builder searches could stand in for a C library header (R585-6-F2, probe
Q7). Round 7 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6104711137)) removes
the gate's own resolution: the compile's own dependency list decides. Four commits on `5b4f6fbe`, no rebase; no
firmware source, header, image builder, mutation table, coverage row or build flag changes.

| Item | How |
|---|---|
| 1. The compile's own dependency list decides | The recorder now runs, for each source an invocation compiles, a dependency pass: the real compiler with the invocation's own arguments, in its directory and environment, its outputs and other inputs left out, and `-M -MF <file> -MT dependencies -H -fpch-preprocess` added. `-M` lists every file the compile reads; `-H` gives the tree of what the source's own `#include` lines read; `-fpch-preprocess` reads a precompiled header as the compile does (Verilator's model objects need it), and what that header read comes from the compile that made it. The gate judges exactly the sources the capture recorded as compiled, by those lists; it builds no include path and lists no source. It classifies each file by where it lives: the stack's (public under `include/`), the C implementation's (the compiler's own baseline, and the RV32 builds' freestanding C library under `-nostdinc`), the firmware's (under `sw/firmware` but the test equipment, plus every file an RV32 compile reads), the rest of the checkout, outside. Refused, by name: a firmware compile reading a stack file outside `include/`; a firmware file including one in any compile; a stack compile reading, through its own `#include` lines, anything but stack and C implementation files (a stack test also the host's libraries); a stack file including anything else; a file of the checkout outside the stack read first into a stack compile; a source a passing compile compiled whose dependency output failed or is incomplete. Gone: the gate's preprocessing, search path, exploration of modes, shapes and contracts, C++ text follow, unit lists and memo. |
| 2. Standing controls | N1 (`ctrl_nvm/nvm_store.c` reaches the stack's `examples/`, compiled by the image builder's own `compile_all`) and Q7 (`ctrl_nvm/plat/stdbool.h` shadows the C library header for the stack, in the same image compile), each refused by name; a shadow of a C library internal header (`bits/libc-header-start.h`) the stack reaches through `<stdint.h>` too. Every earlier control is restated so that a real compile of a planted copy (the image builder's, the arms', a spelling of the planted builder's own, or a replay of a recorded compile) reaches the defect; the firmware run holds 103 boundary controls (the base, 94 refused by name, 8 passing) and the Verilator run 6 (the base and 5 refused), beside the 20 pin controls. Q9 (nothing planted) and the clean controls pass. |
| 3. Docs | The README's stack section, the CI page and the gate's docstring claim exactly this; the CI page cites the hosted figures at `5b4f6fbe` (R585-6-S1). |
| 4. Residue | R584-6-RS1 and R585-6-RS1 applied verbatim (Status, Known limitations); where they overlap they make the same edit once. |

Reviewers' probes, their plants and gate commands unchanged: R584-6's N1 now fails the gate, rc 1, `firmware: sw/firmware/ctrl_nvm/nvm_store.c reads tsn-c-stack/examples/adp_port.h, not one of the stack's public headers [sw/firmware/ctrl/test/ctrl_image.py]` (it passed at `5b4f6fbe`), and N1C names both files; R585-6's Q7 fails, rc 1, `stack: tsn-c-stack/src/acmp.c reads sw/firmware/ctrl_nvm/plat/stdbool.h (included by tsn-c-stack/include/acmp.h), which is neither the stack's nor the C implementation's [sw/firmware/ctrl/test/ctrl_image.py]` and `adp.c`, `maap.c` alike; Q8 fails the same way; Q9 passes.

Eight readings of the assignment are this round's own, each needed for the clean tree to pass or a resolved finding to stay resolved, and each open to a decision: (1) what a stack compile reads through its command line is the builder's (the SRP and two-interface builds force their generated headers into every unit, the stack's sources among them), judged by the read-first rule; (2) the C implementation's headers are the compiler's baseline and the RV32 builds' freestanding C library (`rv32_include`); (3) test equipment is held only through the firmware and stack files it reads (the tests use the stack's `acmp_fake.hpp`); (4) the include tree also holds every firmware and stack file's own `#include` lines in every compile, which keeps the C++-only findings resolved; (5) a stack test may read the host's libraries (GoogleTest); (6) a compile that failed compiled nothing, and is named, not refused, where its pass failed with it (the RV32 self-test's planted header defect); (7) a POSIX header is the host C implementation's, which the RV32 image builders then refuse; (8) a mode reaches only the compiles a builder gives it. Two fixes came with the round: the expansion helper's baseline stand-in is made race-free (two helpers at once failed with a permission error), and a capture made in another checkout is refused by name.

## Round 8

The manager's hosted check at `8436dfc0` ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105928035), not a review) found `firmware-unit` cancelled at its 45-minute timeout: every compile of its firmware steps also ran its dependency pass under the capture, the step took 39 min 43 s, and the coverage ratchet and the boundary step never ran. Six commits on `8436dfc0`, no rebase; no firmware source, header, image builder, mutation table, coverage row or build flag changes.

| Item | How |
|---|---|
| 1. The boundary capture leaves `firmware-unit` | New required job `firmware-boundary` (30 minutes): the five submodules, GoogleTest, the RV32 SDK, then `ctrl_boundary.py --require-rv32 --selftest --without verilator` with no capture given. The gate reads its builders from its own known set (`ctrl_configs.BUILDERS`) and runs each by its builds under its own capture: `fw_rv32_selftest.py` as it was (it compiles its planted cases and runs no binary), and the three suite gates by a new `--build-only` (`fw_gtest.Execution`: every binary their suites build is built and linked as before, none is run, no defect is planted, nothing is measured, and each ends `BUILT`, never `PASS`; `--build-only` with `--self-test` or `--check` is refused). The stack's gate and the image builders run under the capture as before. A builder dropped from the known set is still found by text and refused by name. A probe of that first passed: the coverage gate runs the control and store gates as programs of its own, so a dropped one still compiled in the capture. Two rules close it: a known builder must hold an invocation from a run of its own (the capture's record of the command it came from), and a program found by text (a Makefile, or a module with a `__main__` block) must be known or listed; two standing controls plant each case, and the probe now refuses by name. The four modules that compile only inside a suite (the control, AECP and SRP campaigns, the coverage reader's planted cases) are listed in `ctrl_configs.SUITES` with what they compile there, since the first run refused them by name. `firmware-unit` is dev's nine steps with the stack fetched. The aggregate needs `firmware-boundary`; `ci_events.py` pins its six steps, its result binding, its RV32 refusal, cache and installation arms, and `firmware-unit`'s steps back as dev's. |
| 2. Budget | At the head, in the runner's Ubuntu 24.04 replica on four CPUs: `firmware-boundary`'s step 682 s, 38 % of 1800 s (the builds 614 s: the control gate 299 s, coverage 226 s, the store 80 s, the RV32 self-test 9 s); `firmware-verilator`'s 494 s, 21 % of 2400 s (hosted at `8436dfc0`: 682 s, 28 %); `firmware-unit`'s steps 1986 s, 74 % of 2700 s, the control gate's campaigns most of it. `firmware-unit` cannot meet 60 % of 45 minutes by dropping the capture: its suites are dev's own (the lane adds the stack's eight ADP and six ACMP tests), and with no capture the job took 1963 s hosted at this lane's base `8b61b709` and 1484 to 2462 s on other branches' twenty most recent runs (55 to 91 %). Meeting it needs a longer timeout or the campaigns sharded across jobs; neither is this round's to take. |
| 3. Nothing else | The gate's judgement and every control are round 7's; every standing control refuses by name (105 boundary, the two new ones among them, and 20 pin in `firmware-boundary`; 6 and 20 in `firmware-verilator`; 0 misbehaved). The capture now holds the builds: the compiles of the arms', the store's, the coverage and the RV32 self-test's builds are the same as in round 7's capture of the suites, phase by phase, and every judged fact of the builds is among the suites'; the suites' capture held 5 facts and 20 include edges more, each a test file reading a campaign's planted copy outside the checkout, which every rule admits. |

Open: `firmware-unit`'s budget (Item 2); the campaigns' compiles of planted copies no longer reach the boundary, measured to add no fact a rule can refuse.

## Round 9

R584-7 and R585-7 ([R584-7](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6107725598), [R585-7](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6107554012); [assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6107732413)) found the stack pin check following replacement objects, and the README's 95 where the self-test plants 96. Three commits on `4cab445a`, no rebase; no firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin changes.

| Item | How |
|---|---|
| 1. The pin proof reads the real objects (R584-7-F1, R585-7-F1) | Every Git call of the pin proof (`ctrl_build.py`, `ctrl_pin.py`) goes through `ctrl_build.git`, whose environment (`git_env`) sets `GIT_NO_REPLACE_OBJECTS=1` and gives `GIT_GRAFT_FILE` a path under `/dev/null`, which cannot exist; `GIT_NO_REPLACE_OBJECTS` alone does not stop a graft file. Disk bytes are hashed from the files themselves (`blob <len>\0<bytes>`), through no attribute or filter. `stack_pin` reads the pinned commit's whole tree, trees included, and the checkout's every entry but its own `.git`: the same paths, the same type and mode at each (a directory, a symbolic link, a file executable or not), the same blob for every file and link, each differing path named; this settles R584-6-S2. A census (`ctrl_pin.census`) runs on every boundary run: a string of either module, outside the helper and the docstrings, that names the Git program is refused, and so is a helper environment without either setting (a name assembled at run time is not seen). Ten new pin controls, each refused by name before any build: with `src/adp.c` edited on disk, a replacement of the pinned `src/` tree, a replacement commit for the pin, a graft file, and a clean filter given through attributes that turns the edit back into the pinned blob (checked first); the stack's `LICENSE` edited (the whole tree); a symbolic link standing in for a source (type); a script made executable (mode); and the census planted with the round-8 form of a Git call, and with the helper's environment without each setting. The clean clone still passes. Six mutants of the proof each make their own control escape, but the graft setting, which only the census holds (a graft changes only parents, which the proof never reads). R584-7's `pin_replace_probe.sh` step 3 and R585-7's `pin_probe.py` print `ACCEPTED`/`ESCAPED` at `4cab445a` and `REFUSED` at the head; in a full clone with the edit disguised each way, all 17 entry points (the pin check's command line, the host test, coverage, both image fixtures, the boundary gate, the MAAP differential in both modes, the three AECP tools, and five bench targets) refuse by the changed file's name, 85 of 85. |
| 2. The README's figures (R584-7-F2, R585-7-F2) | The README gives 96 defects and 8 passing controls in the firmware run, 5 in the Verilator run and 30 pin controls. No figure check existed in the repository (R585-7's `structure_check.py` is the reviewer's), so the boundary self-test gets one: it counts `ctrl_plants.PLANTS` and its pin controls, refuses the page where one of the four figures differs or is not given once, and refuses a copy of the page with each figure one more (4 figure controls). Against the README at `4cab445a` it names the 95. |
| RES1 / RS1, S1 | RES1 is the manager's at merge; the two stale lines of this body are corrected with the reviewers' exact wording. S1 is not applied: this round changes what `firmware-boundary` runs, so `4cab445a`'s hosted figures are no longer the head's. |

Open: none new; `firmware-unit`'s headroom stays #716's.

## Authoritative references

- [#697](https://github.com/kebag-logic/milan-fpga/issues/697) acceptance 1 to 5, the [pin ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6092176555), owner decisions [6074086970](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074086970), [6074093506](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074093506) and [6074191062](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074191062), and the [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6091228902).
- F5: [#700](https://github.com/kebag-logic/milan-fpga/pull/700), [AECP core and adapters](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/sw/firmware/ctrl/aecp/README.md).
- tsn-c-stack at the pin: [README](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/README.md), [import record](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/docs/IMPORT.md), [porting guide](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/docs/PORTING.md), [boundary gate](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/scripts/check_boundary.py).
- [Control firmware](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/sw/firmware/ctrl/README.md), [firmware harness](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/sw/firmware/gtest/README.md), [submodule map](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/docs/reference/SUBMODULES.md), [CI workflow policy](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/docs/testing/CI_WORKFLOWS.md), [mailbox bench](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/tb/verilator/mbx/README.md).

## How to get into the same state

```sh
git fetch origin 697-consume
git checkout 697-consume
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
python3 scripts/ci_rv32_sdk.py --destination <new SDK directory>
export MILAN_RV32_CC=<new SDK directory>/bin/riscv32-linux-gcc
```

The firmware gates need GoogleTest and GoogleMock 1.14.0, PyYAML, the pinned
RV32 SDK, CMake and Clang (the stack's own boundary gate), and the pinned
Verilator 5.050 for the two local Verilator gates.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_image.py --base aef7ac66605c4404900ce04cbaaeff88e41bb880
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
make -C tb/verilator/mbx
python3 sw/firmware/ctrl/test/aecp_wire.py --every --output <scratch directory> --verilator <Verilator 5.050>
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/firmware/ctrl/test/ctrl_build.py --stack-pin
python3 scripts/act_ci.py --selftest  # inside a disposable container or the CI job only, never on the host
python3 scripts/ci_events.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/docs_check.py
```

For the image bytes, link both fixtures at dev and at this head with the same
SDK and runtime archives and compare the ELF hashes: `ctrl_image.py --shape
<shape> --out <dir>` for each shipped shape, and `ctrl_srp_image.py --config
<config> --interfaces <1|2> [--without-srp | --with-aecp] --output <dir> --libc <libc.a>
--compiler-runtime <libcompiler_rt.a>` for each shipped config. The `--with-aecp`
composition links compiler-rt's `__umoddi3`, so its runtime archives must be built
with `-fno-stack-protector` (the pinned SDK defaults to `-fstack-protector-strong`).

Expected result / pass criteria:

- the firmware gate prints `tsn-c-stack at 1a9f651cdf7846b8e10ac246a6ef6916960fbb92`, all 59 arms `[ok]`, `mutants: 471 of 471 caught`, every AECP defect `[ok]` (74), every SRP defect `[ok]` (169 at two interfaces, 68 in the one-interface subset), both lwSRP pin arms `[ok]` and `test_ctrl_firmware: PASS`;
- coverage: `29 of 29 planted cases`, then `firmware coverage: PASS (30 files)`, every file at 100 %; the store: `OK across 5 shape(s), 435 tests`;
- each `--build-only`: every binary `built, not run (--build-only)` and `test_ctrl_firmware: BUILT`, `saved-state store gate (#665 F1): BUILT across 5 shape(s), nothing run (--build-only)`, `firmware coverage: BUILT (...)`; with `--self-test` (or the coverage gate's `--check`) each is refused, rc 2;
- boundary, the first form (every known builder, give it `VERILATOR`) or the second (the `firmware-boundary` job's), each running every known builder it judges by its builds under its own capture first: `no capture given: running every known builder the run judges under one`, one line per builder, `capture: ... every known builder held: ...`, `1 compile(s) failed, each with its dependency pass, and compiled nothing: ...` (the RV32 self-test's planted header defect), every control `[ok]`, then `<N> compiled sources of <M> recorded invocations (... the firmware's, ... the stack's, ... test equipment's and builders' own), each judged by what its dependency output lists, host and RV32, every Makefile builder's pin prerequisites and the pin proof's census; 0 finding(s), 105 boundary, 30 pin and 4 figure controls, 0 misbehaved` and `ctrl_boundary: PASS` for the second, in about 11 minutes on four CPUs over 2822 compiled sources of 3053 invocations (the first plants the Verilator run's five controls too; `--only verilator`: 6 boundary, 30 pin and 4 figure controls, V1 to V3 and the MAAP differential's replay among them, in about 8 minutes on four CPUs with its builders; it needs `gptp-processor` initialised, for the end-station builder, and refuses without it); a capture made by an earlier recorder is refused: `a recorder that lists no dependencies made it: capture again`;
- `--base aef7ac66`: `+0` in every section at both shapes;
- the MAAP differential prints `tsn-c-stack at 1a9f651cdf7846b8e10ac246a6ef6916960fbb92` first, then `16/16 caught`; the bench prints the same line before its firmware build, then its six tallies with 0 failures and `mbx mutants: 5 of 5 caught`, and `make -C tb/verilator/mbx run-if2` alone prints it before compiling; the AECP wire comparison prints the same line, then `wire comparison PASS: 1 ingress paths, 142 observations` and, with `--every`, `wire comparison PASS: 2 ingress paths, 294 observations`; the pin check alone prints the same line;
- the pin controls: the clean clone `accepted 1a9f651c...`; each of the other 29 refused by name, among them the stack's `LICENSE` edited, a symbolic link standing in for `src/adp.c`, `scripts/check_boundary.py` made executable, and `src/adp.c` edited under a replacement of the pinned `src/` tree, under a replacement commit for the pin, beside a graft file and under a clean filter given through attributes (each `tsn-c-stack differs from the pinned 1a9f651c: src/adp.c`), and the three census controls; the four figure controls each `gives the ... as <n+1>, where the self-test has <n>`;
- act self-test `selftest: PASS`; the rest exit 0;
- all 35 image hashes equal between dev and the head.

Local evidence at the head (CI-parity Ubuntu 24.04 container with gcc 13.3 and
GoogleTest 1.14.0 for the firmware gates): all of the above hold. The
detailed tables (image hashes, coverage before and after, campaign counts,
plant equivalence, pin proof) are in
[`review-evidence/697c-r1/author/HANDOFF.md`](https://github.com/kebag-logic/milan-fpga/blob/ec6854f6fefbfa2954d6907d5cf457afac92377c/review-evidence/697c-r1/author/HANDOFF.md)
at `ec6854f6`. Round 2's, round 2b's, round 3's and round 4's evidence is not published yet; until it is, their REVIEW READY comments ([6093383132](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6093383132), [6094033396](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6094033396), [6095730057](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6095730057) and [6097154937](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097154937)) carry their results.

## Known limitations / out of scope

- The pin is the newest tsn-c-stack commit with milan-fpga's code, not byte-identical files: every tsn-c-stack commit carries the MIT SPDX line, and from `18d7378` its comments are reduced; #697 comment 6092176555 confirms the pin on that reading. Moving to tsn-c-stack main (the ADP change of tsn-c-stack #19 and the YAML generator, #703) is a later PR.
- The lwSRP pin check (`ctrl_arms.lwsrp_pin`) still reads `git status`; R584-1-S1 marks that part optional, and lwSRP is not #697's submodule.
- act has not run: this PR changes `scripts/act_ci.py`'s trusted manifest, so the first act run needs the audited-install bootstrap by an independent reviewer.
- The hosted `firmware-unit` step needs CMake and Clang for the stack's own gate; both ship on the hosted Ubuntu image; the boundary step passed in `firmware-unit` at `386b8e69`.
- The MAAP differential runs in CI in `firmware-verilator` (round 6), under the boundary's capture. The mailbox bench also runs in CI as the `mbx` Verilator suite.
- The AECP wire comparison runs in CI in `firmware-verilator` at both references (`--every`); its two-interface reference is the processor revision `c9f74b68`, taken from the processor submodule's objects, not the submodule's gitlink.
- The repository's runtime builder (`ctrl_image_runtime.py`, unchanged here) compiles compiler-rt with the pinned SDK's default stack protector, so its archives cannot link `ctrl_srp_image.py --with-aecp`; the AECP images were compared with `-fno-stack-protector` archives at dev and here alike.
- Rounds 3 to 6: the boundary self-test judged every shape, contract and language. At `d1b22e80`, measured on a hosted runner: the step ran more than 12 min and the job exceeded 45 min (job 114173809799). Round 4 runs each preprocessing once and judged the same configurations in 74 to 86 s here, on four pinned CPUs of a shared host where `d1b22e80` took 807 s; on a hosted runner at `e07b3054` the step took 93 s (job 114206016568). Round 5's step took 101 to 106 s on four idle pinned CPUs, where `e07b3054`'s took 80 to 82 s on the same CPUs; on a hosted runner at `92b5be18` it took 113 s (job 114282060753). A preprocessing is reused only for the same unit and arguments with every file it read byte-identical and no file added or removed that it could look up by name; judging every control with and without reuse gave the same findings, 0 of 60 differing.
- R584-3-S1's multi-word literal is closed by construction in round 5 (the capture records the flag the compiler is given); its force-included SRP header named as a constant, and a pin recipe that ignores its exit status, are optional and not addressed; the bench arms of the pin self-test already catch the last.
- `firmware-boundary` has no Verilator; `firmware-verilator` judges the mailbox bench, the MAAP differential and the AECP wire comparison (`--only verilator`). The two jobs split the builders, never an invocation: each recorded compile is judged whole in the job that ran it, and only a run given both captures also tries a mode only one records beside one only the other does (no compile combines them; that run passes locally with 105 and 20 controls). A Verilator cache miss adds its source build to `firmware-verilator`, as it does to `verilator-lint`.
- The image builders run in the boundary step at `ctrl_image.SHAPES`, and the gate judges exactly the compiles they make there; `ctrl_srp_image.py` is given no runtime archives there, so it compiles every object and must stop exactly at its link.
- A compiler a Python builder starts by a path is recorded by the audit hook, and one a Makefile builder's recipe names is read from make's dry run; one a shell runs by a path (a script's, or a command a builder runs through a shell), one a compiled helper runs by a path, and one a Python builder started with `-I` or `-E` runs by a path would not be, and none exists (README, beside the bypass sentence). An exec-level guard (`LD_PRELOAD`) was weighed and not taken: it would load into the store suite's ASan binary, which refuses a preloaded library.
- Round 7: a compile is judged by where the files it read live. A builder's own file outside the checkout (a source it writes or copies, a mutant's tree) is held only by the `#include` lines of the firmware and stack files it reads, not by its own; the firmware the images compile is the checkout's.
- Round 7: a mode reaches only the compiles a builder gives it. Rounds 3 to 6 explored every combination of the modes, shapes and contracts any builder gave, a superset of what any builder compiles; round 7 judges exactly the recorded compiles, as the assignment's population rule says, so a defect under a mode no builder gives the file it is in is not found.
- R585-2-S2 (an explicit `--stack` for `aecp_arms.py` still builds the submodule's `tests/`) is optional and not addressed; the default invocation pins the stack it builds.

- A capture given must have been made in the checkout judged: a builder run of it that ran in another checkout refuses the gate (round 7), since that checkout's files are none of this one's. Hosted, no capture is given: each boundary job makes its own.
- An expansion is reused only while every file and directory it reported is unchanged and every argument is plain; a file a compile reads that the report does not show (a specs file, a plugin) makes its argument non-plain, so it is never reused. The dependency pass is never reused: it runs for every compiled source.
- Round 7 reads the assignment in eight places of its own (the Round 7 section): command-line reads into stack compiles judged as the builder's, the C implementation's headers as the compiler's baseline and the RV32 builds' freestanding C library, test equipment held only through the firmware and stack files it reads, the include tree judged in every compile, stack tests admitted the host's libraries, failed compiles named rather than refused, POSIX headers admitted on the host, and modes not explored across units. Each is a decision the manager may confirm or reverse.
- Round 8: `firmware-unit` runs no capture, and is over 60 % of its 45 minutes on its suites alone: dev's own job took 1963 s hosted at `8b61b709` and 1484 to 2462 s on other branches' twenty most recent runs; a longer timeout or sharded campaigns would meet 60 %, and neither is taken here.
- Round 8: the boundary judges the builds, not the suites, so the campaigns' compiles of planted copies leave its capture; measured against round 7's capture of the suites, they add no fact a rule can refuse. `ctrl_configs.SUITES` lists the four modules that compile only inside a suite.
- Round 8: `firmware-boundary`'s 30-minute timeout is chosen for a new job (38 % locally); its hosted figures at `4cab445a` are in the manager's ruling on #697 ([6107349992](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6107349992)).
- Round 9: the census reads the pin proof's text, so a Git program name assembled at run time is not seen, nor a Git command a function of another module would start for it (the proof calls none).
- Round 9: a graft rewrites only a commit's parents, which the pin proof never reads; its control shows a graft carries no altered stack past the proof, and the helper's graft setting is held by the census's environment check.
- Round 9: the pin check compares the submodule's whole checkout but its `.git`, so a file left inside it (a build directory made there) refuses every gate by name until it is removed.
- Round 9: the figure check reads the four sentences of the firmware README that give the self-test's population; a figure written elsewhere is not checked.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (all met locally; pin confirmed in #697 comment 6092176555)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
