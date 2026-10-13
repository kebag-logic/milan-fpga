[A583] REVIEW READY

Round 7 for PR #705 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6104711137), answering [R584-6](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6104503651) and [R585-6](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6104708471)). Four new commits on `5b4f6fbe`, no rebase or amend; not pushed.

Commit: `8436dfc0bd5e0f3c592dd1faa0a4ced1841a2651`

Changed:
- `1bcf60e12` (items 1 and 2). The compile's own dependency list decides; the gate's own resolution is gone (its preprocessing, search path, exploration of modes, shapes and contracts, C++ text follow, unit lists and memo).
  - The recorder runs a dependency pass for each source an invocation compiles: the real compiler with the invocation's own arguments, directory and environment, its outputs and other inputs left out, `-M -MF <file> -MT dependencies -H -fpch-preprocess` added. `-M` lists every file the compile reads; `-H` gives the tree of what the source's own `#include` lines read. `-fpch-preprocess` reads a precompiled header as the compile does (Verilator's model objects need it), and that header's reads come from the compile that made it. The recorder then runs the compile, waits for it and records its exit status.
  - The population on each side is exactly the sources the capture recorded as compiled. Each file a compile read is classified by where it lives: the stack's (public under `include/`), the C implementation's, the firmware's, the rest of the checkout, outside.
  - Refused by name: a firmware compile reading a stack file outside `include/`; a firmware file including one in any compile; a stack compile reading, through its own `#include` lines, anything but stack and C implementation files; a stack file including anything else; a file of the checkout outside the stack read first into a stack compile; a source a passing compile compiled whose dependency output failed or is incomplete; a capture made in another checkout, or by an earlier recorder.
  - Controls: every earlier one restated so a real compile of a planted copy reaches the defect (the image builder's `compile_all`, the arms' compile functions, a spelling of the planted builder's own, or a replay of a recorded compile). Standing N1 (`ctrl_nvm/nvm_store.c` reaches `examples/`, as the image builder compiles it) and Q7 (`ctrl_nvm/plat/stdbool.h` shadows the C library header in the same build), each refused by name. Firmware run: 103 boundary controls (94 refused, 8 passing, the base); Verilator run: 6; pin: 20 each.
- `c34ca24a3`. The expansion helper's baseline stand-in is made race-free: two helpers at once failed with a permission error in the first N1 replay (round 6's code).
- `dfe36f668` (item 3). The README's stack section, the CI page and the workflow's comments say exactly this; the CI page cites the hosted figures at `5b4f6fbe` (R585-6-S1). `8436dfc0b`: three comments in `ctrl_plants.py`.
- Item 4: R584-6-RS1 and R585-6-RS1 applied verbatim in the PR body; where they overlap they make the same edit, once.

Validation (exact head; CI-parity means Ubuntu 24.04, CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0, four CPUs):
- The hosted job's five firmware steps under the round's recorder: all rc 0. 23,213 invocations, 22,031 compiled sources, 22,030 with a dependency list, 1 failed compile without one (the RV32 self-test's planted header defect), 551 expansions.
  - The firmware gate's 845 verdict lines are byte-identical to rounds 4 to 6 (`mutants: 471 of 471 caught`). The coverage table is identical (30 files). The store gate passed 435 tests.
- `ctrl_boundary.py --require-rv32 --selftest --capture <capture> --without verilator`, under GNU make 4.3 with `MAKEFLAGS=w`: PASS, `22528 compiled sources of 23795 recorded invocations (3337 the firmware's, 1688 the stack's, ...)`, 0 findings, 103 boundary and 20 pin controls, 0 misbehaved.
- `ctrl_boundary.py --require-rv32 --selftest --only verilator` on the runner's Ubuntu 24.04 toolchain (plus cmake 3.28 and clang 18): PASS, 816 compiled sources, 0 findings, 6 boundary and 20 pin controls, 0 misbehaved; V1 to V3 and the MAAP differential's replay caught by name.
- Reviewers' probes, their plants and gate commands unchanged:
  - R584-6 N1: rc 1, `firmware: sw/firmware/ctrl_nvm/nvm_store.c reads tsn-c-stack/examples/adp_port.h, not one of the stack's public headers [sw/firmware/ctrl/test/ctrl_image.py]`. N1C names both files.
  - R585-6 Q7: rc 1, `stack: tsn-c-stack/src/acmp.c reads sw/firmware/ctrl_nvm/plat/stdbool.h (included by tsn-c-stack/include/acmp.h), which is neither the stack's nor the C implementation's`, and `adp.c`, `maap.c` alike. Q8 rc 1. Q9 PASS.
- 35 RV32 images byte-identical to round 6 and dev `aef7ac66` (manifest sha256 `de8ae063…0ebd0`).
- Repository gates: the docs job's 54 commands rc 0; `ci_events.py --check` OK (1848 items), `--selftest` PASS (2530 arms); `act_ci.py --selftest` PASS (446 arms); `check_py_idiom.py` every ratchet held; `check_em_dash.py --base 5b4f6fbe` 0 findings.

Local timings (four pinned CPUs of a shared host):
- `firmware-unit`'s boundary step: 80 s, where `5b4f6fbe`'s took 132 s, one after the other in the same container; exact head 73 s.
- `firmware-verilator`'s step (Ubuntu replica): 472 s. The bench took 53 s, the MAAP differential 149 s and the wire comparison at both references 206 s.
- The firmware steps under the capture: 2497 s, where round 6's took 2203 s (13% more, the dependency passes).

Acceptance criteria: #697 acceptance 1 to 5 hold unchanged: pin `1a9f651c`, lwSRP `9197193e`, images byte-identical, coverage and kills identical, README. Round 7 items 1 to 4 are met as above.

Open risks/questions:
- Eight readings of the assignment are mine, each needed for the clean tree to pass or a resolved finding to stay resolved (PR body, Round 7):
  1. what a stack compile reads through its command line is the builder's (the SRP and two-interface builds force their generated headers into every unit, the stack's sources among them);
  2. the C implementation's headers are the compiler's baseline and the RV32 builds' freestanding C library (`rv32_include`);
  3. test equipment is held only through the firmware and stack files it reads (the tests use the stack's `acmp_fake.hpp`);
  4. the include tree is judged in every compile, which keeps the C++-only findings resolved;
  5. a stack test may read the host's libraries (GoogleTest);
  6. a compile that failed compiled nothing, and is named, not refused, where its pass failed with it;
  7. a POSIX header is the host C implementation's; the RV32 image builders refuse it;
  8. a mode reaches only the compiles a builder gives it.
- `firmware-unit`'s headroom: scaled from the hosted run at `5b4f6fbe` (1861 s of 2700) the job lands near 2050 s; a run as slow as `92b5be18`'s (2450 s) would land near 2750 s, past its 45 minutes. Both jobs' hosted figures need the push.
- R584-6-S2, R584-3-S1's remainder and R585-2-S2 are optional and not addressed.
