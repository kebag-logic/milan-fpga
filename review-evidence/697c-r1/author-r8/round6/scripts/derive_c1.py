"""Scratch: commit 1's files, from the final ones with item 2 (the Verilator job) taken back out."""
import subprocess
import sys
from pathlib import Path
F, C = Path(sys.argv[1]), Path(sys.argv[2])
LANE = "$LANES/697-consume"
T = "sw/firmware/ctrl/test/"


def derive(rel, pairs):
    t = (F / rel).read_text(encoding="utf-8")
    for old, new in pairs:
        assert t.count(old) == 1, (rel, old[:100], t.count(old))
        t = t.replace(old, new)
    (C / rel).parent.mkdir(parents=True, exist_ok=True)
    (C / rel).write_text(t, encoding="utf-8")


for name in ("ctrl_shim.py", "ctrl_capture.py", "ctrl_expand.py"):
    (C / T).mkdir(parents=True, exist_ok=True)
    (C / T / name).write_text((F / T / name).read_text(encoding="utf-8"), encoding="utf-8")

head = subprocess.run(["git", "-C", LANE, "show", "HEAD:" + T + "ctrl_configs.py"], capture_output=True, text=True,
                      check=True).stdout
fin = (F / T / "ctrl_configs.py").read_text(encoding="utf-8")
a, e = fin.index("THE BUILDERS."), fin.index("\n\nTHE BUILD MODES")
ha, he = head.index("THE BUILDERS."), head.index("\n\nTHE BUILD MODES")
(F / T / "ctrl_configs.c1tmp").write_text(fin[:a] + head[ha:he] + fin[e:], encoding="utf-8")
cfg = (F / T / "ctrl_configs.c1tmp").read_text(encoding="utf-8")
(F / T / "ctrl_configs.c1tmp").unlink()
(C / T / "ctrl_configs.py").write_text(cfg, encoding="utf-8")
F2 = F
F = C  # the rest of ctrl_configs is derived from the paragraph-restored copy
derive(T + "ctrl_configs.py", [
('''#: The known set: every builder of the firmware that compiles. The hosted firmware-unit job runs the first four
#: under the capture (rtl-fast.yml); the gate runs the stack's gate and the image builders itself on every run
#: (ctrl_runs.owned); the last three need Verilator, and the hosted firmware-verilator job runs them through the
#: gate's own capture (--only verilator). Each runs every configuration its own list holds: the bench's default
#: target, the differential with its self-test, the wire comparison at every reference it pins (--every).''',
'''#: The known set: every builder of the firmware that compiles. The hosted firmware-unit job runs the first four
#: under the capture (rtl-fast.yml); the gate runs the stack's gate and the image builders itself on every run
#: (ctrl_runs.owned); the last three need Verilator, which the hosted job has none of.'''),
('''    Builder("sw/firmware/ctrl/test/aecp_wire.py",
            (("{python}", "sw/firmware/ctrl/test/aecp_wire.py", "--every", "--output", "{work}/aecp-wire",
              "--verilator", "{verilator}"),), "verilator"),''',
'''    Builder("sw/firmware/ctrl/test/aecp_wire.py",
            (("{python}", "sw/firmware/ctrl/test/aecp_wire.py", "--reference", "protocol-processor", "--interfaces",
              "1", "--output", "{work}/aecp-wire", "--verilator", "{verilator}"),), "verilator"),'''),
('''@dataclass(frozen=True)
class Scope:
    """Which known builders a run judges: every one but those needing what it has none of (`without`), or, with
    `only`, those that need it alone (the gate's own runs beside them, which need nothing)."""

    without: frozenset[str] = frozenset()
    only: str = ""

    def left_out(self) -> list[Builder]:
        """The known builders the run leaves out."""
        return [b for b in BUILDERS if (b.needs and b.needs in self.without) or
                (self.only and b.runs and b.needs != self.only)]

    def judges(self, needs: str) -> bool:
        """Whether a control that needs this ("" for nothing) is the run's: its plant needs a builder the run
        holds."""
        return needs == self.only if self.only else needs not in self.without


def held(capture: Capture, scope: Scope, planted: dict[Path, str] | None = None,
         trees: tuple[Path, Path] = (CTRL, STACK)) -> None:''',
'''def left_out(without: frozenset[str]) -> list[Builder]:
    """The known builders a run leaves out: those needing what it says it has none of."""
    return [b for b in BUILDERS if b.needs and b.needs in without]


def held(capture: Capture, without: frozenset[str], planted: dict[Path, str] | None = None,
         trees: tuple[Path, Path] = (CTRL, STACK)) -> None:'''),
('''    out = {b.path for b in scope.left_out()}
    known = {b.path for b in BUILDERS}
    reasons = [f"the capture holds no invocation of {b.path}, a builder of the firmware that compiles"
               for b in BUILDERS if b.path not in out and b.path not in capture.builders]
    for path in builder_texts(planted) if not scope.only else ():''',
'''    out = {b.path for b in left_out(without)}
    known = {b.path for b in BUILDERS}
    reasons = [f"the capture holds no invocation of {b.path}, a builder of the firmware that compiles"
               for b in BUILDERS if b.path not in out and b.path not in capture.builders]
    for path in builder_texts(planted):'''),
('''def configurations(universe: dict[str, tuple[str, ...]], capture: Capture, scope: Scope, ran: list[str]) -> None:''',
'''def configurations(universe: dict[str, tuple[str, ...]], capture: Capture, without: frozenset[str],
                   ran: list[str]) -> None:'''),
('''    for b in scope.left_out():
        print(f"  LEFT OUT: {b.path}, which needs {NEEDS[b.needs]}, which this run has none of (--without {b.needs})"
              if b.needs else f"  LEFT OUT: {b.path}, which the run that holds the firmware steps judges (--only "
              f"{scope.only})")
    if scope.only:
        print("  the builders found by text are cross-checked by the run that holds the firmware steps")''',
'''    for b in left_out(without):
        print(f"  LEFT OUT: {b.path}, which needs {NEEDS[b.needs]}, which this run has none of (--without {b.needs})")'''),
])
F = F2
derive(T + "ctrl_runs.py", [
('''ctrl_configs.BUILDERS, by its own commands, from the checkout's root, but the
ones the run leaves out (ctrl_configs.Scope). Each must exit 0: a builder
that fails may have compiled less than it does.''',
'''ctrl_configs.BUILDERS, by its own commands, from the checkout's root, but the
ones needing what the run says it has none of. Each must exit 0: a builder
that fails may have compiled less than it does.'''),
('''from ctrl_configs import BUILDERS, CONFIGS, Scope, run''', '''from ctrl_configs import BUILDERS, CONFIGS, left_out, run'''),
('''def standalone(capture: Path, work: Path, scope: Scope, verilator: str | None) -> list[str]:
    """Every builder of BUILDERS with commands, but those the run leaves out, run under the capture; one line
    each. A builder that does not exit 0 refuses the gate."""
    out = {b.path for b in scope.left_out()}''',
'''def standalone(capture: Path, work: Path, without: frozenset[str], verilator: str | None) -> list[str]:
    """Every builder of BUILDERS with commands, but those the run leaves out, run under the capture; one line
    each. A builder that does not exit 0 refuses the gate."""
    out = {b.path for b in left_out(without)}'''),
('''def captures(given: list[Path] | None, work: Path, scope: Scope) -> list[ctrl_capture.Capture]:
    """The captures the gate judges beside its own: the ones given, each of whose builder runs exited 0, or one
    it makes by running every known builder the run judges under it."""
    if not given:
        mine = work / "standalone"
        print("no capture given: running every known builder the run judges under one", flush=True)
        standalone(mine, work / "builders", scope, verilator_of())''',
'''def captures(given: list[Path] | None, work: Path, without: frozenset[str]) -> list[ctrl_capture.Capture]:
    """The captures the gate judges beside its own: the ones given, each of whose builder runs exited 0, or one
    it makes by running every known builder under it."""
    if not given:
        mine = work / "standalone"
        print("no capture given: running every known builder under one", flush=True)
        standalone(mine, work / "builders", without, verilator_of())'''),
])
derive(T + "ctrl_boundary.py", [
('''hook sees, or one a Makefile builder's recipe names, read from make's own dry
run under the capture's PATH) all refuse the gate by name. --without
verilator leaves out the builders that need Verilator, and --only verilator
judges them alone, as the hosted firmware-verilator job does; each builder
and control left out is named on the run.''',
'''hook sees, or one a Makefile builder's recipe names, read from make's own dry
run under the capture's PATH) all refuse the gate by name; --without
verilator leaves out the builders that need Verilator, each named on the
run.'''),
('''alone (ctrl_plants.py); a control that needs a builder the run leaves out is
named, not planted. Then the pin controls (ctrl_pin.pin_controls: the''',
'''alone (ctrl_plants.py). Then the pin controls (ctrl_pin.pin_controls: the'''),
('''    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture DIR --without verilator
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
''', '''    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture DIR --without verilator
'''),
('''from ctrl_configs import (FLAG, FORCED, NEEDS, Read, Scope, Space, configurations, cxx_index, derive,  # noqa: E402
                          held, makefiles, mode_dims, read_first_units, run, spaces, variants)''',
'''from ctrl_configs import (FLAG, FORCED, NEEDS, Read, Space, configurations, cxx_index, derive, held,  # noqa: E402
                          makefiles, mode_dims, read_first_units, run, spaces, variants)'''),
('''          scope: Scope = Scope()) -> list[str]:''', '''          without: frozenset[str] = frozenset()) -> list[str]:'''),
('''    capture must hold every known builder's invocations but those the run's `scope` leaves out
    (ctrl_configs.held, with a `control`'s builder texts added to the checkout's). A control that must be refused
    is judged until the finding it names is found."""
    texts, needle = ({HERE / name: text for name, text in control.texts}, control.needle) if control else (None, "")
    held(capture, scope, texts, (trees.ctrl, trees.stack))''',
'''    capture must hold every known builder's invocations but those `without` leaves out (ctrl_configs.held,
    with a `control`'s builder texts added to the checkout's). A control that must be refused is judged until
    the finding it names is found."""
    texts, needle = ({HERE / name: text for name, text in control.texts}, control.needle) if control else (None, "")
    held(capture, without, texts, (trees.ctrl, trees.stack))'''),
('''def controls(rv32: str | None, work: Path, run: Capture, scope: Scope) -> tuple[int, int]:
    """The base the controls share passing (the run's capture, with what every shared planted builder compiled),
    every plant of the run's scope refused by the finding it names (judged until it is found), every pass control
    passing, each other plant named as left out; the misbehaving count and the controls run."""
    plants = [plant for plant in PLANTS if scope.judges(plant.needs)]
    for plant in PLANTS:
        if not scope.judges(plant.needs):
            print(f"  LEFT OUT: boundary control {plant.name}, judged where its builders' capture is (needs "
                  f"{plant.needs or 'the firmware steps'})")
    shared''',
'''def controls(rv32: str | None, work: Path, run: Capture, without: frozenset[str]) -> tuple[int, int]:
    """The base the controls share passing (the run's capture, with what every shared planted builder compiled),
    every plant refused by the finding it names (judged until it is found), every pass control passing; the
    misbehaving count and the controls run."""
    plants = list(PLANTS)
    shared'''),
('''            findings = judge(trees, rv32, work / "plants-build", capture, control=plant, scope=scope)''',
'''            findings = judge(trees, rv32, work / "plants-build", capture, control=plant, without=without)'''),
('''    ap.add_argument("--only", choices=sorted(NEEDS), default="",
                    help="judge only the builders that need this, and the controls that need them (each other one "
                         "is named)")
    args = ap.parse_args(argv)
    if args.only in args.without:
        ap.error("--only and --without name the same builders")
    scope = Scope(frozenset(args.without), args.only)''',
'''    args = ap.parse_args(argv)
    without = frozenset(args.without)'''),
('''            given = captures(args.capture, work, scope)''', '''            given = captures(args.capture, work, without)'''),
('''            held(capture, scope)
            universe = derive(capture)
            configurations(universe, capture, scope, ran)
            bad = pins = planted_count = 0
            if args.selftest:
                bad, planted_count = controls(rv32, work / "controls", capture, scope)''',
'''            held(capture, without)
            universe = derive(capture)
            configurations(universe, capture, without, ran)
            bad = pins = planted_count = 0
            if args.selftest:
                bad, planted_count = controls(rv32, work / "controls", capture, without)'''),
('''            findings = judge(Trees(CTRL, STACK), rv32, work / "checkout", capture, scope=scope)''',
'''            findings = judge(Trees(CTRL, STACK), rv32, work / "checkout", capture, without=without)'''),
])
derive(T + "ctrl_plants.py", [
('''    against: "missing", "empty", or "drop " and a builder whose invocations it loses. `needs` names the builders
    whose capture the control needs ("verilator": the run that judges the builders that need Verilator; ""
    the firmware steps' run): a run judges the controls of its scope and names every other one."""''',
'''    against: "missing", "empty", or "drop " and a builder whose invocations it loses."""'''),
('''    shared: bool = False
    needs: str = ""
''', '''    shared: bool = False
'''),
('''def wire_mode(name: str, condition: str, label: str) -> Plant:
    """A control only the AECP wire comparison's capture catches (R584-5 V1 to V3): the AECP image header, which
    its C++ compile reaches, reaches a stack example's header only under `condition`, a mode only that
    builder's configurations give (its one- and two-interface references)."""
    anchor = '#include "aecp_model.h"\\n'
    return Plant(name, "ctrl", "aecp/aecp_image.h", anchor,
                 anchor + f"#if {condition}\\n#include \\"adp_port.h\\"\\n#endif\\n",
                 f"[{label}]: aecp/aecp_image.h includes tsn-c-stack/examples/adp_port.h", needs="verilator")


''', ''),
('''    # R584-5-F2: the configurations only the AECP wire comparison compiles, judged where its capture is.
    wire_mode("V1 a mode only the AECP wire comparison gives", "defined(PP_TOP_TIM_DEFAULTS)", "-DPP_TOP_TIM_DEFAULTS"),
    wire_mode("V2 a mode only its two-interface reference gives", "defined(PP_TOP_IF2)", "-DPP_TOP_IF2"),
    wire_mode("V3 a value only its two-interface reference gives",
              "defined(AECP_WIRE_INTERFACES) && AECP_WIRE_INTERFACES > 1", "-DAECP_WIRE_INTERFACES=2"),
    Plant("the capture holds nothing of the AECP wire comparison", "ctrl", "", "", "",
          "the capture holds no invocation of sw/firmware/ctrl/test/aecp_wire.py",
          alter="drop sw/firmware/ctrl/test/aecp_wire.py", needs="verilator"),
''', ''),
])
derive("sw/firmware/ctrl/README.md", [
('''`--without verilator` leaves out the builders that need Verilator (the mailbox bench, the MAAP differential and the AECP wire comparison) and names each; `firmware-unit` has no Verilator.
`--only verilator` judges those three alone, under the gate's own capture, and names the others.
Each runs every configuration its own list holds: the bench's default target, the differential with its self-test, and the wire comparison at each processor reference it pins (`--every`, one and two interfaces).
The required `firmware-verilator` job runs it with the pinned Verilator from the cache.
The two jobs split the builders, never an invocation: each recorded compile is judged whole, with every mode it was given, in the job that ran it.
Only a run given both captures also tries a mode only one job records beside a mode only the other does, which no compile combines.
The builders are also found by text, as a cross-check that can only refuse: every Python module and Makefile that names `sw/firmware/ctrl` or `ctrl_build`.
Each must have compiled in the capture, be a known builder, or be listed in `OUTSIDE` with the reason its compiles are none of the firmware's; the run that holds the firmware steps checks this.''',
'''`--without verilator` leaves out the builders that need Verilator (the mailbox bench, the MAAP differential and the AECP wire comparison) and names each; the hosted job has no Verilator.
The builders are also found by text, as a cross-check that can only refuse: every Python module and Makefile that names `sw/firmware/ctrl` or `ctrl_build`.
Each must have compiled in the capture, be a known builder, or be listed in `OUTSIDE` with the reason its compiles are none of the firmware's.'''),
('''The build modes are the macros each recorded invocation's expansion has when its source begins, with each value the builds gave them (`NDEBUG`, `CTRL_REENTRY_ASSERT`, the re-entry tests', the SRP builds' and the AECP arms' switches, the arms' interface counts, the AECP wire comparison's).''',
'''The build modes are the macros each recorded invocation's expansion has when its source begins, with each value the builds gave them (`NDEBUG`, `CTRL_REENTRY_ASSERT`, the re-entry tests', the SRP builds' and the AECP arms' switches, the arms' interface counts).'''),
('''It then plants 95 defects, each refused by name, and five passing controls, where the firmware steps' capture is.
Among them is each spelling the reviewers gave a mode, a directory or a file read first in, each form a builder can write a mode or a C++ source's name in, and each way the capture can be missing, empty or incomplete.
Where the Verilator builders' capture is, it plants four more: a header the wire comparison reaches includes a stack example only under a mode its one-interface or its two-interface reference gives (`PP_TOP_TIM_DEFAULTS`, `PP_TOP_IF2`, `AECP_WIRE_INTERFACES=2`), and that capture without the wire comparison's compiles.
A run names each control of the other run as left out.
''', '''It then plants 95 defects, each refused by name, and five passing controls.
Among them is each spelling the reviewers gave a mode, a directory or a file read first in, each form a builder can write a mode or a C++ source's name in, and each way the capture can be missing, empty or incomplete.
'''),
])
print("c1 derived")
