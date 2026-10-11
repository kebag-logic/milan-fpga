<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# ctrl: the bare-metal control-plane firmware (#665)

Portable C11 for the on-chip RISC-V, and for a hard core, behind the packet
mailbox ([design](../../../docs/design/MAILBOX_SPLIT.md),
[contract](../../../docs/reference/MAILBOX_CONTRACT.md)). No OS, no heap, no
threads: one event loop, static state, and a static pool behind lwSRP's
allocation port. Lane F0 carries the mailbox driver, the HAL, lwSRP's port
layer, the loop and the ADP slice; F2 adds the opt-in [MAAP owner](maap/README.md),
F3 the ACMP module, F4 the [SRP adapter](srp/README.md) on pinned lwSRP,
and F5 the opt-in [AECP owner](aecp/README.md).
Each protocol has its own core and mailbox adapter.
The ADP, ACMP and MAAP cores and the wire layer are the
[TSN stack](#the-tsn-stack-submodule)'s, from a pinned submodule (#697).

`python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`
is the gate: exit 0 = every arm passed and every planted defect was caught.

The [split verification contract](../../../docs/ARCHITECTURE_HW_SW_SPLIT.md#6-verification-boundary)
requires FT before F2 to F5.
FT ports these checks to GoogleTest/GoogleMock and adds coverage gates.
Existing mutation arms remain required.
The [service budget](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)
is an integration obligation, not a target-time result established here.

## Contents

- **[Layout](#layout)** -- One directory per layer: driver and HAL, lwSRP's port layer, loop, the ADP, MAAP and ACMP adapters, the app, the MMIO platform, the host model, the tests.
- **[The TSN stack submodule](#the-tsn-stack-submodule)** -- The cores the firmware builds from tsn-c-stack: what it provides, what it must not depend on, its tests and its licence.
- **[The ACMP module](#the-acmp-module)** -- The core, its mailbox adapter with the ADP channel's tap, and the binding owner on the saved-state store; per-interface keying, the response before its notification, the adp filter's bound-talker term, TMR_NO_RESP from the accepted send, and the boot order.
- **[The composition](#the-composition)** -- ADP, ACMP and MAAP in one app: the attach order, the channels the open enables, the timer slots, the refusals and the pass bound.
- **[The host test](#the-host-test)** -- The sixteen arms and lwSRP's, how the processor's ADP and ACMP stimulus is cut from the pinned submodule and walked, and the planted defects.
- **[Run](#run)** -- The four invocations and what each needs.
- **[Linked size](#linked-size)** -- The composed app linked with the pinned SDK and no library, audited as RV32I, at the shipping and the largest shape, against the block-RAM budget and dev.

## Layout

| Directory | What it holds |
|---|---|
| [`mbx/`](mbx) | the generated contract header, the three-function bus port (`mbx_hal.h`), the ring lanes and the driver |
| [`port/`](port) | lwSRP's port layer: `shlan_malloc`/`calloc`/`free` on the static block pool, `shlan_printf` on the debug sink |
| [`loop/`](loop) | the event loop: events first, bounded passes, the TICK fan-out in slices, sleep only when nothing is owed, the bring-up order, and the latency bound's assumptions |
| [`adp/`](adp) | the ADP mailbox adapter with the latency bounds, and `adp_entity.py` |
| [`maap/`](maap) | the Annex B core's per-interface mailbox adapter, allocation CSR output and H-MAAP evidence |
| [`srp/`](srp) | per-interface MSRP/MVRP adapter, generated static shape, admission and the binding port |
| [`acmp/`](acmp) | the ACMP mailbox adapter with the latency bounds and the ADP channel's tap, and the binding owner on lane F1's store |
| [`aecp/`](aecp) | the AECP core, image and saved-state adapters, mailbox completion tracking and opt-in application bridge |
| [`app/`](app) | the static composition a platform starts: compose, then open, then `ctrl_app_attach_srp` for SRP |
| [`plat/`](plat) | `mbx_hal.h` on a memory-mapped window (`CTRL_MBX_BASE`, from the SoC's generated `mem.h`) |
| [`host/`](host) | the mailbox model and `mbx_hal.h` on it |
| [`test/`](test) | the host tests and their driver |

The cores (ADP, ACMP, MAAP) and the big-endian wire layer every protocol
shares are the [TSN stack](#the-tsn-stack-submodule)'s, outside this tree.

## The TSN stack submodule

[`third_party/tsn-c-stack`](../../../third_party/tsn-c-stack) is the pinned
[tsn-c-stack](https://github.com/kebag-logic/tsn-c-stack) repository (#697).
It provides the portable C11 cores this firmware composes, with their
core-only unit tests:

| Header | What it is |
|---|---|
| [`adp.h`](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/include/adp.h) | ADP advertising (Milan v1.2 5.6.3) |
| [`acmp.h`](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/include/acmp.h) | Milan ACMP: the listener, the talker's answers and discovery |
| [`maap.h`](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/include/maap.h) | MAAP allocation (IEEE 1722-2016 Annex B) |
| [`wire.h`](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/include/wire.h) | the big-endian wire layer |

The stack depends on nothing in this repository.
It includes only its own headers and the C library.
It must never include the mailbox driver or its HAL, the generated register-map contract,
the MMIO platform, the app, the loop, the AECP core or the measured images.
This firmware uses it the other way round, through its public headers (`include/`) only.
AECP is not part of the stack: its core, adapters and application bridge ([`aecp/`](aecp), F5) are this firmware's.
The adapters, the app, the loop, the HAL and both images compile its `src/*.c` unchanged.
Its callback and timing obligations are in its
[porting guide](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/docs/PORTING.md).

[`ctrl_boundary.py`](test/ctrl_boundary.py) holds both directions, in the builders' own compiles.
It judges exactly the sources a capture of the builders' compiler invocations recorded as compiled; it lists no source of its own.
What each of those compiles read is the compiler's own dependency output for that invocation, made as it ran.
That is the rule `-M` writes with the invocation's own arguments, in its directory and environment: every file the compile reads, system headers included.
Beside it, `-H` prints the tree of what the source's own `#include` lines read, each file under the one whose `#include` read it.
The gate builds no include path and resolves no header: it classifies every file a compile read by where it lives.
The stack's files are those under `third_party/tsn-c-stack`, and its public headers are its `include/`.
The C implementation's headers are those the compiler reads and searches when run with no argument.
For the RV32 builds they are also the freestanding C library headers those builds supply ([`rv32_include`](../gtest/rv32_include)), which `-nostdinc` leaves as the only C library there.
The firmware's files are those under `sw/firmware` but its test equipment, which is the harness (`sw/firmware/gtest`), `sw/firmware/nvm_hosttest`, and every `host/` and `test/` directory.
Every file of the checkout that an RV32 compile compiles or reads is the firmware's too, wherever it lives: the images' own sources under `test/` and lwSRP's.
So the saved-state store's sources ([`ctrl_nvm`](../ctrl_nvm)), which both images compile, are judged as every other firmware source is.
A compile of a firmware source may read no stack file outside `include/`.
No firmware file may include one, in any compile, a test's C++ compile of a firmware header included.
A compile of a stack source may read, through the source's own `#include` lines, only the stack's files and the C implementation's headers.
A source or header of the stack's `tests/` may also read the host's libraries outside the checkout (GoogleTest).
No stack file may include anything else, in any compile.
So a platform header on a builder's include path that is named like a C library header (`ctrl_nvm/plat/stdbool.h`) is refused when the stack reads it.
What a compile reads first through its command line (`-include`, `-imacros`) is the builder's, not the source's.
A stack file outside `include/` read so refuses the gate, and so does a file of the checkout outside the stack read so into a compile of a stack source.
The SRP builds force-include their generated shape header, and the two-interface builds their generated mailbox contract, into every unit they compile, the stack's sources among them.
Those generated files lie outside the checkout, and what they read must be no file of the checkout outside the stack.
Test equipment, and a builder's own files, are held by the `#include` lines of the firmware and stack files they read, not by their own.
This repository's tests use the stack's test fakes (`tests/acmp_fake.hpp`), so a rename among them in the stack breaks those tests.
A mode reaches only the compiles a builder gives it: a defect under a mode is found in every compile given that mode, and in no other.
A source a compile compiled whose dependency output fails or is incomplete refuses the gate by name.
That is a pass that failed, but on `#error` or `#warning` alone, after which the compiler still lists every file it read.
It is also one that wrote no rule, named first a file that is not the source, named a file that does not exist, or printed a tree entry the rule does not hold, and a source read from standard input, which a pass cannot read again.
A compile that itself failed compiled nothing, so nothing it read is in an object: where its pass failed with it, the run names it and does not refuse it.
The RV32 self-test compiles planted header defects that must fail so, and a builder's failed probe would be named the same way.
A file under `sw/firmware` named as a stack source or header is refused too.
[`ctrl_capture.py`](test/ctrl_capture.py) runs a builder with a recording wrapper first on `PATH` for every C and C++ compiler name, for the RV32 compiler (`MILAN_RV32_CC`), and for `CC` and `CXX` where they are set.
The wrapper's recorder ([`ctrl_shim.py`](test/ctrl_shim.py), compiled into the capture when it starts) has the real compiler expand each invocation ([`ctrl_expand.py`](test/ctrl_expand.py)) and list what each source's compile reads, records it, and then runs the real compiler with the same arguments, so every object, binary and image is what it would be without it.
The expansion is the real compiler run with the invocation's own arguments, in its directory and environment, over empty stand-ins of its inputs, with its output and dependency options dropped and `-E -dD -v -fpch-preprocess` added.
So the compiler reads every other argument itself: a response file (`@f`), `-Wp,`, `-Xpreprocessor`, `--define-macro`, `--include-directory` and the other long options, `-include` and `-imacros`.
It says which language each input is compiled in and which files the command line reads first, and the same driver run with no argument is the baseline: what it reads and searches on its own is the implementation's.
A compile whose output is a precompiled header (`.gch`) is expanded over its real header, and a compile that reads one first reads what that compile's expansion reported.
An expansion is reused for the same arguments, directory, environment and compiler while every file and directory it reported is unchanged, and only when every argument is a plain form.
The dependency pass is the real compiler run once more for each source the expansion says it compiles, with the invocation's own arguments, in its directory and environment.
Its output and dependency options are dropped as the expansion drops them, its other inputs are left out, and `-M -MF <file> -MT dependencies -H -fpch-preprocess` is added, with `-Qunused-arguments` for Clang as the expansion adds it.
`-fpch-preprocess` has the pass read a precompiled header the compile reads first, as the compile does, and what that header read is taken from the compile that made it.
The recorder resolves every file the pass names while it is there, and keeps the list and the tree in the capture.
It then runs the compile itself, waits for it, and records its exit status with the invocation.
Python builders load an audit hook that names, for each compile, the builder files on the stack that started it, and records any compiler a builder runs by a path no wrapper stands on.
Run without `--capture`, as the hosted `firmware-boundary` and `firmware-verilator` jobs run it, the gate first runs every known builder it judges under a capture of its own, by that builder's own build commands: its builds, not its suites.
A suite builder's builds are its `--build-only` (`test_ctrl_firmware.py`, `test_ctrl_nvm.py` and `fw_coverage.py`): every binary and image its suites build, built and linked, none run and no defect planted.
The RV32 self-test runs as it is: it compiles its planted cases and runs no binary.
`firmware-unit` runs the suites, the store suites and the coverage ratchet with no capture.
A capture given (`--capture`) is judged instead, and must have been made in this checkout, its builders run here: one run in another checkout refuses the gate, since that checkout's files are none of this one's.
Either way it runs the stack's own gate and the image builders under the capture itself ([`ctrl_runs.py`](test/ctrl_runs.py)).
`ctrl_srp_image.py` compiles every object there and stops at its link, which needs runtime archives built from sources outside the checkout.
The image builders take each shape through the end-station builder, so the gate needs `gptp-processor` initialised, as `firmware-boundary` has it, and refuses without it.
[`ctrl_configs.py`](test/ctrl_configs.py) lists the known builders that compile (`BUILDERS`).
A missing or empty capture refuses the gate by name.
So does a known builder the capture holds no invocation of from a run of its own: a compile it makes only under another builder's run, as the coverage gate runs the control and store gates, holds that other one.
So does an invocation the compiler could not expand: the expansion failed, printed fewer translation units than it ran (its output went to a response file's `-o`), compiled an input the recorder never saw (a response file's), or read a stand-in as an option's value.
So does a precompiled header read first that no compile in the capture made.
So does a compiler run by a path no wrapper stands on: one a Python builder starts, which the audit hook sees, or one a Makefile builder's recipe names, which make's own dry run shows under the capture's `PATH`.
Three such compilers are not seen, and no builder has one: one a shell runs by its path (a shell script's, or a command a builder runs through a shell), one a compiled helper runs by its path, and one a Python builder started with `-I` or `-E` runs by its path, since that process loads no audit hook.
`--without verilator` leaves out the builders that need Verilator (the mailbox bench, the MAAP differential and the AECP wire comparison) and names each; `firmware-boundary` has no Verilator.
`--only verilator` judges those three alone, under the gate's own capture, and names the others.
Each runs every configuration its own list holds: the bench's default target, the differential with its self-test, and the wire comparison at each processor reference it pins (`--every`, one and two interfaces).
The required `firmware-verilator` job runs it with the pinned Verilator from the cache.
The two jobs split the builders, never an invocation: each recorded compile is judged whole, in the job that ran it.
The builders are also found by text, as a cross-check that can only refuse: every Python module and Makefile that names `sw/firmware/ctrl` or `ctrl_build`.
Each must be a known builder, be listed in `PART_OF` with the builder it runs under, in `OUTSIDE` with the reason its compiles are none of the firmware's, or in `SUITES` with what it compiles only inside a suite; one that is no program (a Makefile, or a Python module with a `__main__` block, is one) may instead have compiled in the capture.
So a builder dropped from the known set refuses the gate by name, even where another builder still runs it.
The run that holds the firmware builders checks this.
It also runs the stack's own boundary gate, beside the rest.
`--selftest` first compiles an unplanted copy of the firmware's tree and the stack, laid out as in the checkout, the ways the controls compile it; that base must pass.
Those ways are the image builder's compile of every image source at both of its shapes, the arms' C compile of every firmware and stack source, and their C++ compile of the stack's tests and of the firmware's headers.
It then plants 96 defects, each refused by name, and 8 passing controls, where the firmware builders' capture is.
Two of them are a known builder whose own run compiles nothing and a builder dropped from the known set, each one the coverage gate still runs.
A control's planted builder compiles the planted copy through a capture of its own, and what it compiled is judged.
It compiles the copy as the builders do (the image builder's and the arms' own compile functions), in a spelling of its own, or as a replay: a compile of the run's capture run again with the copy's trees in its arguments (the SRP image builder's).
Among them are R584-6's N1 (a store source reaching the stack's `examples/`, as the image builder compiles it) and R585-6's Q7 (a store platform header that shadows `stdbool.h` for the stack in the image build).
Among them too are each spelling a compiler takes a mode or a file read first in (`-Wp,`, `-Xpreprocessor`, the long options, a response file, `-imacros`, `-include`, a precompiled header), each form a builder can write a mode or a C++ source's name in, and each way the capture can be missing, empty or incomplete.
A passing compile whose pass gives no list is refused (its standard input; a builder's own `-Wp,-MD`, which overrides the pass's rule), and a compile that fails passes (a header nobody supplies; a source that is no file).
Where the Verilator builders' capture is, it plants 5 more, each a replay or an alteration of that capture.
In three, a header the wire comparison reaches includes a stack file only under a mode its one-interface or its two-interface reference gives (`PP_TOP_TIM_DEFAULTS`, `PP_TOP_IF2`, `AECP_WIRE_INTERFACES=2`).
The fourth is a header only the MAAP differential's C++ source reaches, and the fifth is that capture without the wire comparison's compiles.
A run names each control of the other run as left out.
The self-test refuses this section where one of these figures, or the pin controls' below, is not its own count of its controls.
A copy of this page with each figure one more is refused by name.

Every gate that builds the stack first runs the same pin check (`ctrl_build.py --stack-pin`).
The submodule must be at its gitlink.
Its checkout, all but its own `.git`, must be the gitlink's whole tree: the same paths, each of the same type and mode, every file and symbolic link hashing to the tree's blob.
The hashes are taken from the files' own bytes, never from the index and through no Git attribute or filter, so an edit hidden from `git status` is refused too.
The pin proof's modules are [`ctrl_build.py`](test/ctrl_build.py) and [`ctrl_pin.py`](test/ctrl_pin.py), and in them only one helper names a process-launch facility: it runs Git.
The helper sets `GIT_NO_REPLACE_OBJECTS=1` and gives `GIT_GRAFT_FILE` a path that does not exist, so Git reads the real objects only.
So a replacement object (`refs/replace`) or a graft cannot make another tree read as the pin's.
What decides the pin is `stack_gitlink`, `stack_pin` and the command line's `main`.
Before the proof's first Git call, where `ctrl_build.py` defines the helper, the proof installs a PEP 578 audit hook, which stays for the life of the process.
An audit hook cannot be removed, and this one binds all it judges by as it is installed: the helper's code, the module's namespace, the Git program, and every function, builtin and constant it uses.
So no later rebinding of a name switches it off.
While the proof runs (a function that decides the pin, in any thread, or the top level of one of the two modules), the hook refuses every process start the interpreter audits but the helper's, and every thread start, since a thread could change a start's arguments after the hook has read them.
The helper's is the `subprocess` module starting, for the helper's own code, the Git program that `PATH` named when the proof was loaded, with both settings.
The hook refuses `exec`, `compile` and an import of `importlib` while a function that decides the pin runs, and wherever the proof's own code asks for them, the helper's included.
In the same places it refuses the reaches into its own state: the collector's lists of objects, and a trace or profile function.
At any time it refuses a replacement of what a function of the proof runs, its code or its defaults.
Each refusal names the line of the proof that asked, and is written to the standard error before it is raised, so a refusal that is caught is still read.
The guarantee covers launches through the interpreter's audited interfaces.
Native code is the remaining limit: `ctypes`, an extension module, and before CPython 3.14 `_posixsubprocess.fork_exec`, which `multiprocessing` calls to spawn, start a process no audit event names.
So is what Git itself starts, and code that runs before the hook is installed, at the top of `ctrl_build.py`.
An import of a module already loaded raises no audit event, so `import importlib`, `__import__` or `pkgutil.importlib` alone is refused by the census below, not at run time; nothing it reaches can start a process or run dynamic code in the proof without an event the hook refuses.
A function of the two modules that starts a process while the proof is not running is not judged.
`ctrl_build.py`'s build functions and `run`, and `ctrl_pin.py`'s runs of `make` and of the gates its controls run, start their processes that way, through `fw_gtest.run`.
`ctrl_boundary.py` also holds a census of the proof on every run: a fast lint of both modules' syntax trees, beside the hook.
Outside the helper it refuses any reference to a process-launch facility, by import, alias or attribute: the `subprocess`, `pty` and `asyncio.subprocess` modules and their members, `os.system`, `os.popen`, `os.exec*`, `os.spawn*`, `os.posix_spawn*`, `os.fork`, `os.forkpty`, `os.startfile`, and asyncio's `create_subprocess_exec` and `create_subprocess_shell`.
An attribute with one of those names is refused on any object, so `os` reached through another module is refused too.
Anywhere, the helper included, it refuses `eval`, `exec`, `compile`, `__import__`, `importlib`, `builtins` and a wildcard import, by name or as an attribute of any object (but `re.compile`).
Outside the hook it refuses the reflection that reaches an object without naming it: `getattr`, `setattr`, `delattr`, `vars`, `globals`, `locals`, an attribute that begins with an underscore (but `__name__`), a frame's attributes and `sys.modules`.
What decides the pin, and every function, class and constant of `ctrl_build.py` it names, may name only the proof's vocabulary.
That is a few names of `os`, `hashlib`, `stat`, `pathlib` and `argparse`, and builtins and attributes of the proof's own values.
The census also refuses a helper environment without either setting, and `ctrl_build.py` without the helper or with its name bound again.
It reads the modules as written, so it does not see a rebinding by assignment or code built at run time: the guarantee is the hook's.
So the census also runs the proof from the modules it reads, under the hook in a fresh interpreter, and names each refusal at its line.
The gates are the host test (with its coverage), `ctrl_boundary.py`, the MAAP differential in both modes, the mailbox bench ([`tb/verilator/mbx`](../../../tb/verilator/mbx)) and both image fixtures with the submodule as their stack.
The AECP arms, campaign and wire comparison run it too when run alone (`--stack`, the submodule by default).
In a Makefile builder, every target whose recipe builds against the stack has the pin check as a prerequisite, so no target run alone reaches it unpinned.
[`ctrl_pin.py`](test/ctrl_pin.py) reads those targets from make's own dry run and refuses one without it.
52 pin controls follow the boundary controls.
A clean clone passes the check.
An edited source, test, script, CMake file or the stack's `LICENSE` is refused, and so are an edit hidden by `assume-unchanged`, an added header, a symbolic link standing in for a source, a script made executable and another revision.
An edited source is refused by its name when the pinned `src/` tree or the pinned commit is replaced by one holding the edit, and beside a graft file.
So it is when a clean filter given through the clone's attributes turns it back into the pinned blob, as `git status` would read it.
A graft changes only a commit's parents, which the check never reads; the hook holds the helper's graft setting.
The proof as the checkout holds it runs to its verdict under the hook.
Each of 24 bypasses planted in the proof, which is then run under the hook, ends in the hook's refusal before any build.
Twenty are refused at the plant's line.
They are a Git command run by the harness's runner, under a computed name (`git.__name__`) and as a dashed program (`git-ls-tree`); an aliased import (`from subprocess import run as r`); `os.system`; and `exec` of a string.
They are also the helper's name rebound by attribute assignment, in either module; `os.walk` rebound to start Git; `inspect.builtins.exec`, `eval` and `compile`; `pkgutil.importlib.import_module`; and `exec`, `eval` and `compile` inside the helper.
The rest are a thread started, the decision's code replaced (`stack_pin.__code__`), the collector's list of objects (`gc.get_objects`) and a trace function (`sys.settrace`).
The Git program rebound is refused for the program the helper would start.
The helper's environment without each of its two settings, and also with the builtins a hook could look up rebound, is refused by the setting's name.
Both modes of the MAAP differential and the three AECP tools refuse an edited clone before building it.
Every mailbox bench target whose dry run reaches the stack runs for real, in a scratch copy, against a clone whose `wire.h` is poisoned.
At this head those are `all`, `run-cosim`, `run-if2`, the firmware library and the pin target itself.
Each refuses on the pin check and never compiles the poisoned header, and the pin target passes the clean clone.
A planted copy of the bench's Makefile whose `run-if2` lacks the pin prerequisite is refused by name.

Its tests run two ways.
The gate [below](#the-host-test) builds the stack's own core tests into the
`adp`, `reentry_debug`, `reentry_release`, `acmp`, `maap` and `maap_debug` binaries.
The coverage gate measures the stack's sources, and the campaign plants core defects into a copy of them.
The stack's own suite runs from the submodule, as its
[CI](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/.github/workflows/quality.yml)
runs it, with GoogleTest and GoogleMock 1.14.0:

```sh
cmake -S third_party/tsn-c-stack -B <build directory> -DCMAKE_BUILD_TYPE=Debug
cmake --build <build directory> -j16
ctest --test-dir <build directory> --output-on-failure -j16
```

The stack is [MIT](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/LICENSE) (Kebag Logic).
Its files keep their MIT identifiers inside this platform.
The platform's own files stay [CERN-OHL-W-2.0](../../../LICENSE).
lwSRP stays a separate Apache-2.0 component.
The gitlink is the only record of the stack's revision; moving it is a reviewed change.

## The ACMP module

Milan v1.2 5.5 (connection management) and 5.6.4 (the listener's discovery
machine), in three units, each stating its clauses in its header:

| Unit | What it is |
|---|---|
| [`acmp.h`](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/include/acmp.h), [`acmp.c`](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/src/acmp.c) (the TSN stack's) | the core, with no mailbox: every listener transition of Table 5.30, the talker's answers of 5.5.4, the discovery machine of Table 5.54, the timers of Tables 5.26 and 5.29, the lock, the saved binding record, and the no-callback guard of #678 |
| [`acmp_mbx.h`](acmp/acmp_mbx.h), [`acmp_mbx.c`](acmp/acmp_mbx.c) | the mailbox adapter: the acmp channel, one fabric timer slot per AVB interface armed at the earliest deadline of its sinks, the tap that hands the adp channel's ENTITY_AVAILABLE and ENTITY_DEPARTING to discovery and everything else to ADP, the adp channel's bound-talker table kept equal to the bindings, and the service-latency figures per path |
| [`acmp_nvm.h`](acmp/acmp_nvm.h), [`acmp_nvm.c`](acmp/acmp_nvm.c) | the binding group on lane F1's state port (`ctrl_nvm/nvm_state.h`), every other group forwarded to the integrator's owners |

The protocol state is keyed per AVB interface: a sink's probes leave on its
interface, a source answers only probes that arrived on its own, and a sink
takes ADPDUs only from its own interface. A change of a sink's Table 5.22
items is reported through the env's `changed` port only once the response of
the command that caused it has been taken by the transmit ring (#653).

The adp channel's term is decided on #665 (6029368753): ENTITY_AVAILABLE and
ENTITY_DEPARTING of a talker bound on the receiving interface; F3 round 2 adds
the term. The contract's `eq_bound` term reads a per-interface bound-talker
table in the mailbox block, which the core's `admit` port keeps equal to each
bound sink's talker (sink k is entry k), and which `ctrl_app_open()` fills
with the bindings the store restored
([design page](../../../docs/design/MAILBOX_SPLIT.md#discovery-and-the-adp-channels-filter)).
Only AVTP version 0 is read: the core discards an ACMPDU or ADPDU of another
version before decoding it (IEEE 1722-2016 4.4.3.4). TMR_NO_RESP runs from
the send the transmit ring accepts, so a probe owed behind other frames
holds its timer until it leaves, and its deadline comes from a clock read
after that send returns, never from one read before it.

A platform that restores bindings boots in this order: `ctrl_app_compose()`,
`acmp_nvm_init()` on the app's ACMP core, `nvm_store_boot()` with its port,
`nvm_store_service()` added as a centisecond consumer, then `ctrl_app_open()`;
the ACMP env's `persist` port calls `nvm_store_changed(NVM_G_BIND, sink)`.

## The composition

`ctrl_app` composes ADP always, and ACMP and lane F2's
[MAAP owner](maap/README.md) when the configuration supplies them: `acmp`
and `acmp_env` for ACMP; `maap_allocation`, the stream-address port
(`maap_csr_allocation` on the datapath CSR window), with `maap_ctx` and
`maap_preferred` for MAAP. Lane F2's `ctrl_app_start_maap()` is
`ctrl_app_start()` with those three fields given, and refuses a missing port.

- **The attach order.** `ctrl_app_compose()` attaches ADP, then ACMP (its
  tap stands in front of ADP's handler of the adp channel), then MAAP, and
  touches no mailbox register. `ctrl_app_open()` then opens every bound
  channel at the filter and enables each one's receive interrupt with the
  events' (`ctrl_loop_open()`): with all three, the adp, acmp and maap
  channels and no other. ACMP writes the restored bindings, ADP is enabled,
  and MAAP reads each interface's link and begins.
- **The timer slots.** ADP holds slots 0 to `MBX_N_IF` - 1, ACMP the next
  `MBX_N_IF` and MAAP the next: three disjoint runs, which a
  `_Static_assert` keeps inside the fabric's bank of `MBX_N_TIMERS` (16).
- **The refusals.** The composition is refused, with nothing opened, for a
  pool that cannot be carved, a configuration its module refuses (MAAP
  refuses an entity with no talker source), and a preferred MAAP range
  that starts outside the B.4 pool (IEEE 1722-2016 Table B.9) or runs past
  its end. A refusal stops the composition before the later modules attach.
- **The pass bound.** A pass of the three costs at most `CTRL_APP_THREE_PASS_MAX`
  mailbox accesses: the pass of ADP and ACMP (`ACMP_MBX_PASS_MAX`, 1,012 at
  one interface) plus MAAP's share of 568, its costliest action on each of
  the 8 events (48), its 2 records of the maap channel (20 + 48) and its
  poll on each interface (48). That is 1,580 at one interface and 1,659 at
  two. It is also the two modules' own pass bounds less what both count:
  `ACMP_MBX_PASS_MAX` plus `MAAP_MBX_PASS_MAX` (616 at one interface, 664
  at two) less the 6 accesses of each of the 8 event records. Every pass
  count of `acmp_mbx.h` and of the MAAP page holds in the composed loop
  with this pass in place of its own
  ([design page](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)).

After the open, initialize SRP on the application's static pool and call
`ctrl_app_attach_srp()` before entering the loop. This fourth attachment retains
ADP, ACMP and MAAP receive/filter bits, adds SRP's receive interrupt, and enables
the centisecond tick. SRP uses no one-shot timer slot. Its participant timers
share the tick; the three runs of fabric slots above remain disjoint.
A failed attachment preserves the running three-module composition.
With ACMP present, attachment also installs a composition-owned request per sink.
The ACMP callback copies the latest bind or unbind, preserving its sink index.
A fifth poll delivers requests after SRP service returns, using each sink's
configured interface. Transient refusal keeps the request pending and the loop awake.
VID 0 or VID >= 4095 sets the readable per-request `parked` state.
A parked request permits sleep until ACMP replaces or withdraws it.
Unbind and replacement supersede the prior request; no callback enters SRP.
The supplied ACMP SRP callback observes intent; it must not deliver it itself.
After SRP returns, that poll delivers retained Talker feedback.
Feedback belongs to each accepted sink binding and configured interface.
Advertise or Failed enters SETTLED_RSV_OK; withdrawal stops SRP and reprobes.
A continuous kind change calls `acmp_tk_kind_changed`, updating REGISTERING_FAILED.
This view-only entry is allowed solely in SETTLED_RSV_OK.
It neither reprobes nor replays Table 5.30's EVT_TK_REGISTERED.
Milan Table 5.23 defines the current kind's reported flag.
[The round-11 decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6049530812)
authorizes this ACMP interface extension.
Unchanged registration is idempotent; pending replacement blocks obsolete feedback.
SRP retains the first withdrawal despite subsequent re-registration.
Registration precedes withdrawal when both await delivery.
Accepted replacement retires feedback, including identical stream identities.
The [adapter contract](srp/README.md) explains event observation.
Both directions obey #678: no protocol entry occurs inside a port callback.
Other environment callbacks retain their original context.
Keep application and adapter storage alive until loop service stops.

`CTRL_APP_PASS_MAX` bounds all four modules: `ACMP_MBX_PASS_MAX` already
includes ADP, then add `MAAP_MBX_PASS_MAX` and `SRP_MBX_PASS_MAX`, subtracting
two copies of the shared event reads, then adding `CTRL_APP_SRP_FEEDBACK_MAX`.
Feedback costs at most six accesses per sink.
Registration and withdrawal can each stop or re-arm a timer.
Withdrawal can also read the clock and initial random seed.
The static maximum of 16 sinks contributes 96 accesses.
The result is 3,224 accesses at one interface and 4,073 at two. The SRP bound counts one maximum-size frame per
library transmit call, at most two calls per interface, receive readiness and
retry clocks, plus link/reset work. Binding delivery itself adds no mailbox access.
The feedback allowance covers the same poll's ACMP registration entries.
It excludes CPU work and external ports.
The SRP arm also builds U6/F6 with all four modules at each interface count:
exact interrupt mask, an idle HAL awakened by SRP alone, ordered attachment,
disjoint timer slots, full receive backlogs and the algebraic pass bound.
The exact-mask, SRP-only wake and algebraic-bound checks have named planted defects.

MAAP's allocation reaches ACMP's talker only through the integrator's
`source` port (`acmp.h`): the port reports `dest_mac_valid` and the stream's
destination, and the app does not connect it to the stream-address port.

`test_acmp_mbx.cpp` holds the composition's checks, in both ACMP arms: U6
(the attach order, every channel and its interrupt, disjoint slots each
holding its own module's arm, MAAP acquiring its range beside the other
two over four seconds, every MAAP frame sent from its interface's own
unicast MAC, where the maap row admits a DEFEND (IEEE 1722-2016 B.2.1)),
U7 (the refusals) and F6 (events and the acmp and maap rings backlogged:
the worst pass 231 accesses at one interface and 233 at two, and the bound
against the two modules' own).

## The host test

The driver compiles the firmware for the host exactly as the target
compiles it (`-std=c11 -Wall -Wextra -Werror -pedantic`), into a temporary
directory, and runs these arms. Every arm but `rv32` is a GoogleTest binary
graded by the tally it prints; the harness, its mocks, the port from the
hand-rolled checks and the coverage ratchet are described in
[the harness page](../gtest/README.md).

| Arm | Source | What it shows |
|---|---|---|
| `model` | `model_suite.cpp` | the mailbox suite's checks, which the RTL passes through both adapters, pass on the model too |
| `port` | `test_port_loop.cpp` | the pool, the debug sink, the driver on the model (TX commit order across channels included, and the own MAC the filter matches with the FILTER_MISMATCH it counts), the loop's order (every interface's own MAC before a channel opens), bounds, owed work and tick slices, and a TICK record taken while centiseconds are carried |
| `unit` | `test_unit_seams.cpp`, `test_unit_driver.cpp`, `test_mmio.cpp` | the firmware's own seams on GoogleMock: the app's composition order over the mailbox window (`mbx_hal.h`) and lwSRP's port layer (`shlan_port.h`), the entity's MAC as every interface's own MAC, the contract check field by field, the driver's refusals and bounds, each interface's own MAC block and the FILTER_MISMATCH read, the adapter's slot, interface and loop-room refusals, and the MMIO platform over a host window |
| `adp` | the stack's `tests/test_adp.cpp`, `test_adp.cpp` | the ADP core over fake ports (deferred sends, strays, discards, the two draw kinds, the available_index every DEPARTING and restart carries on the wire, an owed DEPARTING across a restart and a second SHUTDOWN, owed frames across a link loss, a GM change, a DISCOVER and a stray expiry, and the bound of two owed DEPARTINGs with the SHUTDOWNs beyond it coalesced and counted), the tag race, the latency bound of every path, an owed frame behind a full transmit ring under a HAL that sleeps, the owed DEPARTING across a restart through the mailbox, the pass an AVAILABLE behind owed DEPARTINGs is committed in, and the bound with both rings full and ticks coalesced |
| `reentry_debug`, `reentry_release` | the stack's `tests/test_adp_reentry.cpp` | Every port/core entry pair, same and cross instance; both inline-expiry regressions. Assertions in debug, counted refusal in release. |
| `walk` | `adp_walk.cpp` | the processor's own ADP walk, reused: 36 cells of its Table 5.51 transcription and its frame builder, on the firmware and the model |
| `acmp` | the stack's `tests/test_acmp.cpp`, `test_acmp_mbx.cpp` | the ACMP core over fake ports (every listener command, response, timer and SRP event in every state Table 5.30 gives it, each response field by field; the talker's answers; the lock; responses keyed on the consumer's unique ID; sequence IDs; one timer per interface; owed frames and the response before its notification; the discovery machine cell by cell; the saved record; the no-callback guard), then the adapter on the model: the channel and its filter, the timer slot and the tag rule, the ADP channel's tap, the gPTP pair, the adapter's refusals, every path's service cost (the H-ACMP and H-DISC hooks), an owed response behind a full ring under a HAL that sleeps, full backlogs and the composition, with ADP, ACMP and MAAP composed together ([The composition](#the-composition)) |
| `acmpwalk` | `acmp_walk.cpp` | the processor's own ACMP expectations, reused: its F05.3 matrix model of Table 5.30 in lock step with the firmware (88 cells), its Table 5.54 transcription (33 cells) and its talker suite's F05.11 constants, each difference between the two asserted to be what it is |
| `acmpnvm` | `test_acmp_nvm.cpp` | the core and its binding owner on lane F1's store over the host flash model, at the shipping 1x1 shape: a bind saved and fast-connected after a power cycle, an unbind saved, the started flags, an unread slot refusing persistence, a refused record, the roll-back and every other group forwarded, and a D3 roll-back (at the port and at a boot) leaving the bindings applied |
| `acmpif2` | `test_acmp_mbx.cpp`, `acmp_if2.cpp` | the adapter's tests again with the firmware and the model compiled against the contract elaborated for two AVB interfaces (written into the build by `gen_mailbox.py`): each interface's timer slot, tag, gPTP pair, bound-talker table and every latency path, and the three-way composition |
| `entity` | `entity_fields.cpp` | every shipped config's ADPDU fields, against the fabric's own sources |
| `maap`, `maap_if2`, `maap_debug` | the stack's `tests/test_maap.cpp`, `test_maap.cpp`, `test_maap_mbx.cpp`, the stack's `tests/test_maap_debug.cpp` | Annex B, stream CSR output, H-MAAP at one/two interfaces, and synchronous reentry refusal |
| `rv32` | the portable set | a freestanding RV32I build whose only open symbols are C-library string, format and assertion functions and libgcc helpers |
| `lwsrp` | `lwsrp_port.cpp` | the pinned submodule, or `--lwsrp DIR`: lwSRP's own MRP core on the port layer, through the SRP channel, timed by the fabric's ticks; DIR must be lwSRP at the pinned revision with `src/` unmodified |

The [SRP evidence](srp/README.md#evidence) adds declaration, lifecycle, latency,
debug, shape and processor-wire arms at one and two interfaces.

### Reusing the processor's stimulus

`ctrl_reuse.py` cuts three things out of the pinned
`protocol-processor/tb/adp_engine/sim_main.cpp` at build time: the fixed
entity configuration, the independent 82-byte `model_frame` builder and the
`ADV` table of Milan v1.2 Table 5.51. It first proves the submodule is one
stage-0 gitlink, checked out at that commit, and that the file's bytes are the
blob the pin records; a marker that is missing or repeated refuses the run.

`adp_walk.cpp` drives the firmware into each cell's state through the
mailbox, applies the row's event as the fabric delivers it, and grades the
cell's end state, draws, arms, cancel rule, frame (byte for byte against
`model_frame`) and available_index. The processor's "DELAY, draw in flight"
column has no firmware counterpart (the firmware draws and arms in one call)
and is reported as not applicable. A stray ('S') is an expiry posted with a
tag the firmware did not issue.

For ACMP the same module cuts three more slices, each from its pinned file:
`tb/acmp_listener/sim_main.cpp`'s constants, ACMPDU builder, stimulus and
independent F05.3 matrix model (`pp_acmp_reuse.inc`),
`tb/adp_engine/sim_main.cpp`'s Table 5.54 transcription (`pp_disc_reuse.inc`)
and `tb/acmp_talker/sim_main.cpp`'s F05.11 constants
(`pp_talker_reuse.inc`). `acmp_walk.cpp` runs the processor's model and the
firmware's core in lock step through every Table 5.30 cell a stimulus can
reach, and grades the frames byte for byte, the sink's timer, its record, the
SRP start and stop, discovery, the store's mark and the notification. Three
differences are asserted, field for field, to be exactly what they are:
UNBIND_RX_RESPONSE's talker fields (the processor echoes them; Milan Table
5.36 gives 0), the ACMP status after a TMR_RETRY with the talker discovered
(the processor zeroes it; 5.5.3.5.30 step 2 sets none), and the lock's refusal
status (the processor sends 13, TALKER_MISBEHAVING in IEEE 1722.1-2021 Table
8-3; the firmware 16, CONTROLLER_NOT_AUTHORIZED). A fourth, DISCONNECT_TX of
an unknown source, is asserted on the firmware's half only (TALKER_UNKNOWN_ID,
Milan 5.5.4.2 step 1); the processor's SUCCESS is read from source
(`KL_acmp_talker.sv:1301-1306`), not walked. Milan 5.5.2.7 says DISCONNECT_TX
"always returns SUCCESS"; 5.5.4.2 governs, since 5.5.2.7 is an overview that
defers to 5.5.4 and 5.5.4.2 is the "shall" procedure. The four are processor
issue #168.

### Planted defects

`--self-test` writes each defect of `ctrl_mutants.py` (with lane F3's
`acmp_mutants.py` and lane F2's `maap_mutants.py` appended) into a copy of
this tree, or of the TSN stack's sources and headers for a defect in a core
(a `tsn-c-stack/` path), and requires the arm it
names to exit 1 with a `[FAIL]` line naming the
GoogleTest test and carrying the check's own words; a defect that breaks the
build, or reddens only other tests, is an escape. The arms: ADP clause defects caught by the walk (one per walked
Table 5.51 row but the foreign DISCOVER, which the fabric filter drops and
`adp`'s A4 catches), adapter, latency, owed-output (an owed DEPARTING
replaced, passed or dropped, an owed AVAILABLE dropped or kept wrongly, and
the bound on owed DEPARTINGs included), events-first and available_index
defects by `adp`, pool, sink, loop, tick-slice, tick-carry and driver
defects (TX commit order included) by `port`, lane, model and model
commit-order defects by `model`, a wrong ADPDU field source by `entity`, a
heap call by `rv32`, and a defect in each seam the `unit` arm mocks (the
composition order, the contract fields, the driver's refusals, the
adapter's bounds and the MMIO platform) by `unit`; each check written for
branch coverage (P5 to P9, S3, L9, A22 to A24) has a defect of its own; P9's
free list cut short, followed to its end, is caught by the crash report
that names P9. Each rule of the full-tuple filter (lane FC) has a defect in
the model caught by `model` (a tag stripped or taken for an EtherType, a
destination, EtherType or subtype ignored, any unicast or interface 0's MAC
taken for own, the AECP response term dropped, FILTER_MISMATCH never, wrongly
or ERR-less counted; for the MAAP DEFEND to own unicast, the message_type read
a byte early, a tuple's message types ignored, a message_type refusal left
uncounted, a DEFEND taken to any unicast), and the firmware's side has its
own: the own MAC unguarded or halved, FILTER_MISMATCH read from another register (`unit` and
`port`), the own MACs written after the channels open (`port`) and the app's
own MAC not the entity's (`unit`). Lane F3 adds 273 defects for the
`acmp`, `acmpwalk`, `acmpnvm` and `acmpif2` arms (with the driver's and the
model's for the bound-talker table in `unit` and `model`): a defect in each clause step, each
response field, each guard term, each timer, the owed queue and the #653
release, discovery's every guard, each port's re-entry flag, the saved
record, the adapter's slot, tag and tap, extra mailbox accesses on each
measured path, each backlog figure understated, and the binding owner's
forwarding; round 2's AVTP version check, TMR_NO_RESP from the accepted send,
the slot range, the per-interface wiring at two interfaces, the binding
record's flags and length, the D3 roll-back, each timer across the
millisecond wrap and the bound-talker table; round 4's TMR_NO_RESP from a
clock read before the probe's send; round 6's for the composition with
MAAP: each overlap of MAAP's slots with ACMP's or ADP's, MAAP attached after
the open, before ACMP, started in the compose or never, its channel left
unbound, each refusal dropped or moved off its boundary, lane F2's entry
taking no port or dropping its range, and a MAAP handler overrunning the
three-way pass bound; round 7's: MAAP's source MAC or the filter's own MAC
keyed by interface (`acmpif2`), and the three-way bound without MAAP's
share or with MAAP's poll on one interface only; and eight wrong numbers in
`acmp.h` itself, which the tests
catch because they spell the standards' values (the stack's `tests/acmp_fake.hpp`, `spec`),
never the header's. They are `acmp_mutants.py`'s table, rounds 2, 4, 6 and 7's
in `acmp_review_mutants.py`. Round 6 re-plants four defects whose text the
composition moved, each with its test and words: the pool bound after the
mailbox (F0) and ACMP never composed read the compose's ACMP block, and lane
F2's MAAP receive interrupt and filter bit, which the app no longer writes,
are dropped where `ctrl_loop_open()` writes them. Lane F2's own defects
(96, `maap_mutants.py`) grade the `maap`, `maap_if2` and `maap_debug` arms;
its README lists them. Every test of those
arms is named by at least one defect, which `unnamed_tests` proves before any is planted, as lane F1's
store suite does; a test of the stack's may instead be named by the stack's own defect table
(its `tests/mutations.json`, which its CI plants). Some FC filter defects in the host model also name
lane F3's own-unicast and FILTER_MISMATCH checks. With
`--lwsrp` it also requires the pin to refuse a
scratch clone with one compiled source edited, and the same clone at
another revision. `--slice K/N` plants slice K of N of the table, so the
campaign runs as N commands.

## Run

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --slice 1/6
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --lwsrp <lwSRP checkout>
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture <capture> --without verilator
```

`--build-only` builds and links every arm's binaries and runs none; it plants nothing and ends `BUILT`, never `PASS`.
The first boundary command runs every known builder by its builds under a capture of its own first (Verilator from `VERILATOR` or `PATH`).
The second is the `firmware-boundary` job's: every known builder but those that need Verilator (see [CI workflows](../../../docs/testing/CI_WORKFLOWS.md)).
The third judges a capture made of any builder's commands, each run as `ctrl_capture.py --out <capture> -- <command>`.

Needs host C/C++ compilers, GoogleTest, GoogleMock, and PyYAML (the
`acmpnvm` arm also runs the builder for its shape, as lane F1's gate does).
RV32 checks use the SDK from `scripts/ci_rv32_sdk.py`.
Both firmware gates require RV32 in `firmware-unit`, and the boundary gate in `firmware-boundary`.
The boundary gate also needs GoogleTest's headers for the stack's tests, and CMake and Clang for the stack's own gate.
Freestanding declarations avoid the SDK's hosted C headers.
GCC supplies its own freestanding integer and varargs headers.
`MILAN_RV32_CC` selects an explicit compiler for local validation.
See [the harness](../gtest/README.md#rv32-object-builds) for evidence limits.
The SDK distribution is `ilp32d`; the core uses RV32I/ILP32.
The CI firmware step also requires the control mutation campaign.

Initialize `third_party/lwSRP` and `third_party/tsn-c-stack` at their recorded gitlinks before running the gate.
An alternate `--lwsrp` checkout must match `ctrl_arms.LWSRP_REV`, currently
`9197193e47a6bb1c45a56d90a18c1784123aba44`, with every compiled source unchanged.
Moving either pin requires a reviewed change.
The pin is published on public lwSRP `main`, including PR #12 and PR #15.
Anonymous HTTPS checkout needs no repository credentials.

## Linked size

Two independent measurement fixtures survive the F3/F4 merge.
`ctrl_image.py` retains F3's ADP/ACMP/MAAP and saved-state composition below.
`ctrl_srp_image.py` measures ADP/ACMP/MAAP/SRP with the entity-sized pool,
verified bare-metal runtime archives and an 8192-byte stack reservation;
see the [SRP recipe](srp/README.md#evidence).
Neither fixture is a shipping or booted image, and neither connects the
integrator's live stream, persistence and media owners completely.


`ctrl_image.py` links the firmware as a Mark II platform composes it
([`rv32_image/image_main.c`](test/rv32_image/image_main.c)): the app with
ADP, ACMP and MAAP, the binding owner, MAAP's allocation output on the
datapath CSR window, and lane F1's store on the LiteSPI port at the shape's
container, booted in the order above, every source compiled with its gate's
RV32I flags plus `-DNDEBUG`, one section per function and object, and linked
at `--gc-sections` into one 128 KB block-RAM region
([`image.ld`](test/rv32_image/image.ld)), so only what the composition
reaches counts (#665, acceptance addition 6030870481). The integrator's
owners (the lock, the sources, SRP, the notifier, every other saved group,
the CSR window's two accesses) are stubs; the C runtime the SoC's libbase supplies is linked from byte-loop
stand-ins, reported apart (64 bytes: `memset` and `memcpy`, the only ones the
composition reaches); lwSRP's pool is the host tests' 256 bytes in this fixture; `ctrl_srp_image.py` measures the entity-sized pool; the stack is not counted. `--base REV` measures another revision's
firmware with the same harness, with its own copies of the cores for a revision
from before #697 and tsn-c-stack at its recorded gitlink after.

No library is linked. The pinned SDK's `libgcc.a` is built for its one
multilib, `rv32imafd` with the `ilp32d` ABI, so it cannot link into a
soft-float RV32I image. The arithmetic helpers GCC calls on RV32I come from
[`rv32_image/image_arith.c`](test/rv32_image/image_arith.c) instead: every
helper the `rv32` arm admits (none is a floating-point one), each a
shift-and-add or shift-and-subtract loop that must be a leaf. A helpers
object that leaves a symbol open or calls a helper is refused, since GCC
lowers a `*` inside `__mulsi3` into a call to `__mulsi3`. In the SoC image
LiteX's `libcompiler_rt` supplies them. They are reported apart: 508 bytes,
`__lshrdi3`, `__muldi3`, `__mulsi3`, `__udivdi3`, `__umoddi3` and
`__umodsi3` (the only ones the composition reaches; MAAP's code brings
`__umodsi3`) and their two divide loops.

Before any figure is read, the linked ELF is audited, and any finding
refuses the measurement:

- a little-endian ELF32 RISC-V executable whose `e_flags` are 0: no RVC, the
  soft-float ILP32 ABI, not RVE or Ztso;
- one architecture attribute, `rv32i` and its version alone;
- every word of every executable section an RV32I base instruction (no M,
  A, F, D, C, Zicsr, Zifencei or privileged instruction);
- no symbol the linked objects reference and none defines. A weak one links
  to address 0 and leaves no trace in the image, so the inputs are read.

```sh
python3 sw/firmware/ctrl/test/ctrl_image.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
```

The self-test holds the controls, 33 checks: the helpers against the host's
own arithmetic (the edges, every shift count and 200,000 random pairs), the
leaf rule and two helpers it refuses, a probe linked as the image is and
every RV32I instruction form passing, eleven foreign instruction words, an
RV32IM attribute, ten foreign header fields and a weak symbol refused, and
the measurement itself at the shipping shape: passing, and refusing a helper
library built for RV32IM with the soft-float ABI (by the audit), one built
for the pinned SDK's own multilib (at the link) and a helper that calls
itself.

`ctrl_image.py` prints the compiler's identity first: its version line and
the sha256 of its `libgcc.a`, which is not linked. That is what names the
toolchain of a table. Another build at the SDK's path prints another
identity.

At lane F3 round 6, with the pinned SDK of `scripts/ci_rv32_sdk.py`
(`riscv32-ilp32d--glibc--stable-2025.08-1`, archive sha256
`d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`), whose
compiler's version line reports GCC 14.3.0 from the SDK build
`2021.11-18033-g83947c7bb6` (`ctrl_image.py` prints the line in full) and
whose `libgcc.a` has sha256
`d8ebca8cf6ad31cd50695f79e91e86a716d3b1761fbbefd5ee7b0627a2d0af58`, against
dev `e21c1ca0` (the app with ADP and MAAP through `ctrl_app_start_maap()`,
no ACMP, the same store):

| Shape | STREAM_INPUTs / OUTPUTs | text | rodata | data | bss | total | of 128 KB |
|---|---:|---:|---:|---:|---:|---:|---:|
| `endstation_ax7101_1x1_tdm8` (shipping) | 2 / 2 | 33,444 (+10,768) | 748 (+32) | 0 (+0) | 12,416 (+4,848) | 46,608 (+15,648) | 35.6 % |
| `endstation_ax7101_8x8` (largest) | 9 / 9 | 33,448 (+10,768) | 748 (+32) | 0 (+0) | 22,784 (+4,848) | 56,980 (+15,648) | 43.5 % |

Every image passes the audit (`rv32i2p1`, 8,361 and 8,362 words at the
head, 5,669 and 5,670 at the base). The text includes the 64 bytes of
runtime stand-ins and the 508 bytes of helpers, at the head and the base.

The static objects: the app, 7,904 bytes at every shape (ACMP's state 4,720
at its maxima of 16 sinks, 16 sources and four interfaces, the loop 1,748,
MAAP's 1,104, the pool's header 204, ADP's 124), the store's stage (3,344 at the shipping
shape, 13,264 at the largest), its payload buffer (136, 576), chunk (256)
and state (288), and the pool's arena (256). ACMP's state does not follow
the shape: the sinks and sources it serves are a run-time configuration
within those maxima, so the shape moves only the store's buffers and a few
bytes of code.
