[A583] REVIEW READY

Round 6 for PR #705 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6102039501), answering [R584-5](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6101961588) and [R585-5](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6102035089)). Five new commits on `92b5be18`, no rebase or amend; not pushed.

Commit: `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1`

Changed:
- `715d9c9ee` (items 1 and 3). Before it records, the recorder has the real compiler expand each invocation: its own arguments, directory and environment, over empty stand-ins of its inputs, outputs dropped, `-E -dD -v -fpch-preprocess` added (`ctrl_expand.py`, new; `ctrl_shim.py`, `ctrl_capture.py`, `ctrl_configs.py`). The gate takes each compile's modes, search path and files read first from that report. A response file, `-Wp,`, `-Xpreprocessor`, the long options, `-imacros` and a precompiled header are the compiler's to read.
  - Refused by name: an expansion that fails; one that prints fewer translation units than it ran (a response file's `-o`); one that compiles an input the recorder never saw (a response file's); one that reads a stand-in as an option's value. Also refused: a precompiled header no recorded compile made, and a stack file other than a public header read first.
  - A file of the checkout read first is judged as a firmware unit (`mmio_window.h`, which the unit arm force-includes).
  - R585-5-S2: the header closure fails closed (exit 2) past 1024 headers per compile.
  - R585-5-S1: the README lists the three compilers the capture cannot see, beside the bypass sentence.
  - 13 standing controls, one for each reviewer spelling and refusal case.
- `5471b0605`, `d4184ff60`. `aecp_wire.py --every` runs each reference its own list pins: one interface and two, each tree taken from the processor submodule's objects. Two fixes the hosted runner needs:
  - the MAAP differential passes its objects before `-LDFLAGS`, because Ubuntu's static GoogleTest failed to link (R585-5's limits log);
  - `<stdexcept>` in the wire comparison's model, which GCC 13 did not compile without.
- `50b3f4535`, `5b4f6fbeb` (item 2). `ctrl_boundary.py --only verilator` judges the bench, the MAAP differential and the wire comparison at both references, each run by its own commands under the gate's capture. Its controls are V1 to V3 and a dropped-builder control.
  - A required `firmware-verilator` job in `rtl-fast`'s aggregate runs it, with the pinned Verilator from the cache `verilator-lint` shares, under `timeout-minutes: 40`.
  - `firmware-unit` is unchanged. The CI model and the CI page are updated.
- Item 4: R584-5-RS1 and R585-5-RS1 are applied verbatim in the PR body; where they overlap, both texts stand. R585-5-S3: the CI page states the hosted 113 s.

Validation (exact head; CI-parity means Ubuntu 24.04, CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0):
- The hosted job's five firmware steps under the new capture, in the CI-parity container: all rc 0.
  - 23,213 invocations, 551 distinct expansions, 0 refusals.
  - The firmware gate's 845 verdict lines are byte-identical to rounds 4 and 5 (`mutants: 471 of 471 caught`).
  - The coverage table is identical (30 files). The store gate passed 435 tests.
- `ctrl_boundary.py --require-rv32 --selftest --capture <capture> --without verilator`: PASS, 101 boundary and 20 pin controls, 0 misbehaved.
  - It judges 948 configurations: round 5's 942, each reading the same files, plus 6 for `mmio_window.h`.
  - Under CPython 3.12.3 and GNU make 4.3 with `MAKEFLAGS=w`: PASS.
- `ctrl_boundary.py --require-rv32 --selftest --only verilator` on the runner's Ubuntu 24.04 toolchain (plus cmake 3.28 and clang 18): PASS, 5 boundary and 20 pin controls, 0 misbehaved. V1 to V3 are caught by name:
  - `firmware c++ [-DPP_TOP_TIM_DEFAULTS]`, `[-DPP_TOP_IF2]` and `[-DAECP_WIRE_INTERFACES=2]`, each `: aecp/aecp_image.h includes tsn-c-stack/examples/adp_port.h`.
- Both captures given together, nothing left out: PASS, 105 boundary and 20 pin controls, 0 misbehaved.
- Reviewers' probes:
  - R584-5: K0 and F1 to F6 CAUGHT by their modes. F7 (optional S3, a compiler run by path through a shell) is a stated limit.
  - R585-5: `env` and `rsp` CAUGHT; `abs` with the hook REFUSED by name; `abs` under `python3 -I` is a stated limit.
- 35 RV32 images are byte-identical to round 5 and dev `aef7ac66` (manifest sha256 `de8ae063…0ebd0`), built plainly and through the capture.
- Repository gates:
  - The docs job's 54 commands: rc 0, with the docs job's three submodules.
  - `ci_events.py --check` OK (1848 items); `--selftest` PASS (2530 arms).
  - `act_ci.py --selftest` PASS (446 arms).
  - `check_py_idiom.py`, `check_baremetal_only.py --check`, `check_em_dash.py --base 92b5be18`, `docs_check.py` and `measure_fail_fast.py --selftest`: rc 0.

Local timings (four pinned CPUs of a shared host):
- `firmware-unit`'s boundary step: 117.6 s, where `92b5be18`'s took 100.5 s, run one after the other on the same CPUs. Scaled to the hosted 113 s at `92b5be18`, that is about 132 s, leaving 56% of the 300 s budget. Exact head: 123.6 s; parity run: 134.5 s.
- `firmware-verilator`'s step (Ubuntu replica): 452 s. The bench took 57 s, the MAAP differential 139 s and the wire comparison at both references 212 s; the judgement took the rest. With setup that is under a third of the 40 minutes.
- The firmware steps under the capture: 2203 s, where round 5's took 2188 s (CI-parity container).

Acceptance criteria: #697 acceptance 1 to 5 hold unchanged: pin `1a9f651c`, lwSRP `9197193e`, images byte-identical, coverage and kills identical, README. Round 6 items 1 to 4 are met as above.

Open risks/questions:
- Both jobs' hosted figures need the push. A Verilator cache miss adds its source build to `firmware-verilator`, as it does to `verilator-lint`.
- The capture cannot see three compilers (README): one a shell runs by path, one a compiled helper runs by path, and one a Python builder runs by path under `-I` or `-E`. No builder has one.
- A capture judged from another clone reads that checkout's files as a builder's own. For example, `mmio_window.h`'s macros become modes and the header is not judged as a unit. Hosted, the capture and the judgement share one checkout.
- R584-3-S1's remainder and R585-2-S2 are optional and not addressed. `firmware-unit`'s headroom is the separate issue.
