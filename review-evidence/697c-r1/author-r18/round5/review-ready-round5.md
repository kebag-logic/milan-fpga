[A583] REVIEW READY (round 5)
Commit: 92b5be18817659c1c9903a0544450d29ca7ab3fd (tree 33de4dc3c3be34efea3d50128211bd14a72ac510), five new commits on e07b3054: d6dd5936d, 133ee559c, 11529fadd, 93540c3a8, 92b5be188. No rebase or amend, not pushed (PR #705 still shows e07b3054).

Changed (the boundary gate, its capture, the `firmware-unit` job's steps and their docs; no firmware source, header, test, image builder, mutation table, coverage row, Makefile or build flag):
- Capture (item 1). `ctrl_capture.py --out DIR -- COMMAND` runs a builder with a recording wrapper first on PATH for every C and C++ compiler name, the RV32 compiler (MILAN_RV32_CC) and CC/CXX.
  - The wrapper runs a C recorder (`ctrl_shim.RECORDER`, compiled into DIR when the capture starts). It appends one record per invocation (arguments, directory, each source and its language, the -include files, the builder files) and then execv's the real compiler with the same arguments.
  - It keeps the text of every C++ source, and of every header outside the checkout a C++ source reaches in a builder's own directories, so a source a builder writes and deletes is still read.
  - An installed tool's own C++ source is recorded as such and not followed: one outside the checkout, the temporary directory and the compile's directory whose inode changed before the capture's start marker. Standalone, that is Verilator's verilated.cpp, verilated_dpi.cpp and verilated_threads.cpp; hosted, nothing. A source a builder writes or copies anywhere is its own.
  - A Python audit hook names the builder modules on the stack of each compile; the driver names the command's script or Makefile.
  - `firmware-unit`'s firmware suites, store suites and coverage steps run under one capture; the boundary step moves last and judges it (`--capture "$RUNNER_TEMP/ctrl-capture" --without verilator`). The boundary runs the stack's own CMake build and the image builders under the capture itself.
  - The judgement takes every mode and C++ source from the capture. The static derivation from builder text is removed.
- Fail closed (item 2), each refused by name:
  - a missing or empty capture, or one whose builder run failed;
  - a known builder (`ctrl_configs.BUILDERS`) it holds no invocation of;
  - a builder found by text that compiled nothing and is listed nowhere (the old discovery, kept only as this cross-check);
  - a compiler a builder runs by a path no wrapper stands on (the hook for Python, make's dry run for a Makefile recipe);
  - a C++ compile of a source that was no file, or of standard input; a nameless -D; a stream count no shipped shape gives.
  - Standalone, the gate runs every known builder under its own capture first. `--without verilator` leaves out the bench, the MAAP differential and the AECP wire comparison, named on every run.
- Plants (item 3): 88 plants and the base, 89 controls (round 4: 60): 83 refused by name, 5 passing beside the base. Every builder plant runs through the capture. Each form listed in rounds 2 to 4 is caught by name:
  - Makefile forms: patsubst, foreach, `VAR+=-D` with no space, `-D $(M)`, `-D$(MODE)`, `-DNAME=$(VALUE)`, addprefix;
  - Python forms: a mid-string f-string, a split multi-word literal, a shell literal, shlex, a bare -D before a conditional, str.format, +, %, an f-string macro, a bare -D before a list;
  - C++ names: wildcard, a join, glob, iterdir;
  - written sources: a literal, an f-string include, a formatted template, a copied template, a header written beside the source; a written source whose include a macro computes, and one copied out of the builder's directories with its old modification time kept;
  - the fail-closed cases of item 2;
  - passing: an installed tool's source with a computed include, there before the capture began.
- Docs: `sw/firmware/ctrl/README.md` (the boundary passage, Run); `docs/testing/CI_WORKFLOWS.md` (the job, the budget); module docstrings.

Two of the five commits fix what this round's own runs found. The standalone run at 133ee559c failed, its base and four passing controls misbehaving: the recorder had kept Verilator's runtime source, and the gate followed `verilated.h`'s computed include (fixed by 11529fadd). A capture of the Verilator builders at 11529fadd then showed that rule leaving the AECP wire comparison's copy of `sim_main.cpp`, in its output directory, unread (fixed by 93540c3a8). Each has a standing control.

Validation (clean clones; the head differs from 93540c3a8 only in `docs/testing/CI_WORKFLOWS.md`, which of the gates below only `ci_events.py` reads, and that ran again at the head; host for the boundary, probes, images and docs; the CI-parity container, CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0, for the firmware steps):
- Hosted command, against the container's capture of the job's firmware steps at 93540c3a8 (23,213 invocations): PASS three times, `(942 configurations, 943 preprocessed) ... 0 finding(s), 89 boundary and 20 pin controls, 0 misbehaved`. Same under CPython 3.12.3 with GNU make 4.3 and MAKEFLAGS=w, on a clean clone of the head itself.
- Standalone (no capture; every known builder run under the gate's own, Verilator 5.050 given): PASS in 49 min. Every builder exits 0; 24,097 invocations from 23 builder runs, 33 build modes, 252 C++ sources, three installed and not followed; 89 and 20 controls, 0 misbehaved.
- Budget (item 4), pinned to four otherwise idle CPUs of a shared host: 101.0, 104.1 and 106.4 s. e07b3054's step took 80.1 and 82.2 s on the same CPUs, and the hosted one 93 s (job 114206016568), so the same ratio puts the head near 124 s, 59% inside 300 s. The slowest local run, 214.8 s on CPUs other jobs held, left 85 s. Not measured hosted (not pushed).
- The judged configurations equal round 4's: 942 configurations, 794 distinct (side, unit, label), none on one side only and none read differently.
- Real builders, at 93540c3a8: each Makefile form planted into the mailbox bench's firmware recipe is caught end to end: `firmware [-DCTRL_R5_PROBE]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers`. So is each Python form planted into ctrl_image.py's flags. A recipe naming /usr/bin/gcc is refused by name.
- Images, at the head: 35 of 35, built plainly and through the capture (922 RV32 invocations, no bypass), byte-identical to round 4's manifest and dev aef7ac66's (sha256 de8ae063…).
- Kills and coverage, through the capture at 93540c3a8: the firmware gate's 845 verdict lines identical to round 4's (471/471 control, 74/74 AECP, 169 and 68 SRP, 2/2 lwSRP pin); coverage self-test 29 of 29, `--check` PASS (30 files), its table identical; store suites PASS (5 shapes, 435 tests).
- Recorder cost in the container, measured at d6dd5936d: +1.1 ms per C compile, +2.0 ms per C++ compile (the later rule adds one stat per C++ source).
- Docs job at the head, 54 of 54 rc 0, with every submodule and with the docs job's three. That includes `check_baremetal_only.py`, `check_py_idiom.py` under CPython 3.12.3, `ci_events.py --check` (1757 items) and `--selftest` (2387 arms), and em-dash (0 findings over 44 added lines).

Acceptance criteria: met at the head. Images are byte-identical; coverage and kills are unchanged. Round 5 items 1 to 3 are met as above; item 4's hosted figure is the manager's.
Open risks/questions:
- The hosted job has no Verilator, so its capture holds nothing of the mailbox bench, the MAAP differential or the AECP wire comparison. Each is named LEFT OUT on every hosted run; a standalone run with Verilator judges them. The modes only they compile (`PP_TOP_TIM_DEFAULTS`, `AECP_WIRE_INTERFACES` and Verilator's own) are judged only there; no firmware unit tests any of them, so the standalone run judges the same 942 configurations. Adding Verilator to `firmware-unit` is the maintainer's call.
- The installed-tool rule reads inode change times against the capture's start. A C++ source outside the checkout, the temporary directory and the compile's directory that a step before the first captured one wrote would be taken for a tool's; none is compiled. A clock stepped backwards during a capture is not guarded against.
- The image builders run in the boundary step at their own two shapes; `ctrl_srp_image.py` stops at its link for want of runtime archives. Every shape's headers come in through the shape dimension.
- A compiler a shell script, a recipe that sets its own PATH, or a compiled helper runs by a path would not be seen; none exists. An LD_PRELOAD guard was weighed and not taken: the store suite's ASan binary refuses a preloaded library.
- R584-3-S1's remaining parts and R585-2-S2 (optional) are not addressed. R584-4-S2 and R585-4-S1 (the job's own margin) are outside this lane; the boundary step adds 20 to 26 s on the same CPUs.
- Hosted CI and act have not run at the round-5 head.

Details are in the Round 5 sections of the lane packet's HANDOFF.md and PR-BODY.md.
