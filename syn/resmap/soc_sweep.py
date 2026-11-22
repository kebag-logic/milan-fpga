#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""SoC-side options (issue #649): export each LiteX option variant, record the
recipe's refusals, and price the CPU core and the SoC top in Yosys.

The variants are the `soc` section of syn/resmap/sweep_plan.json. Each one is
the shipping configuration's own SoC argument list (the builder's
soc_params.json, at the placement the section names) with the named flags
changed, run through sw/litex/milan_soc.py WITHOUT --build, from the scratch
export syn/resmap/yosys_sweep.py `shapes` wrote. The section names the
all-fabric placement, the one the recorded figures were taken at; the AX7101
configurations ship the split since #665. An argument list that names a
platform image (the split's --ctrl-firmware) is refused before any export
unless that image is in the export tree: no export leans on an earlier,
unrelated firmware build. A variant the script refuses is recorded here with its refusal line, and
this script prices only what the recipe accepts. The refused CPU, cache and L2
variants were priced separately, from a scratch-only copy of the recipe with the
refusal removed (never committed; issue #649's round-2 ruling): the findings page
docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md gives those figures and where
their driver and receipts are published.

Two figures per accepted variant, both `synth_xilinx -family xc7 -flatten`:

  cpu   the VexiiRiscv netlist the export names, alone
  top   the LiteX top with every non-LiteX module (milan_datapath, the CPU and
        the parent's own SystemVerilog blocks) replaced by a black box whose
        ports are 1024 bits wide, so no connected net is truncated away

Usage, each with --work DIR (the same one yosys_sweep.py used):

    soc_sweep.py export --litex-python PY --sdk DIR [NAME..]
    soc_sweep.py price [NAME..]
    soc_sweep.py --selftest
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import yosys_sweep  # noqa: E402

#: migen writes one instance per block, opened by this banner.
INSTANCE = re.compile(r"^// Instance (\S+) of (\S+) Module\.$", re.M)
#: A named connection or parameter: `.name (expr)`.
NAMED = re.compile(r"^\s*\.(\w+)\s*\(", re.M)
#: migen's direction sections inside an instance.
SECTIONS = {"// Inputs.": "input", "// Outputs.": "output", "// InOuts.": "inout"}
STUB_WIDTH = 1024


def plan_variants(plan: dict) -> dict:
    """The soc section of the plan."""
    return plan["soc"]["variants"]


def plan_placement(plan: dict) -> str:
    """The control placement the soc section prices; the plan must name it (#665)."""
    placement = plan["soc"].get("placement")
    if not isinstance(placement, str) or not placement:
        raise yosys_sweep.PlanError("the soc section names no control placement")
    return placement


def missing_images(argv: list[str], tree: Path) -> list[str]:
    """Each platform image the SoC arguments name (--ctrl-firmware) that is not a file, a relative path read
    against the export tree as milan_soc.py reads it against its repository."""
    named = [argv[i + 1] for i, flag in enumerate(argv[:-1]) if flag == "--ctrl-firmware"]
    named += ["(no value)"] if argv[-1:] == ["--ctrl-firmware"] else []
    return [path for path in named if not (tree / path).is_file()]


def variant_argv(base: list[str], spec: dict) -> list[str]:
    """The shipping SoC arguments with each `set` flag's value replaced or appended, and `add` flags appended."""
    argv = list(base)
    for flag, value in spec.get("set", {}).items():
        if flag in argv:
            argv[argv.index(flag) + 1] = value
        else:
            argv += [flag, value]
    return argv + list(spec.get("add", []))


def git_listable(tree: Path) -> None:
    """Give each exported processor a scratch commit: milan_soc.py derives its sources with git ls-files."""
    for sub in ("protocol-processor", "gptp-processor"):
        checkout = tree / sub
        if (checkout / ".git").exists():
            continue
        for argv in (["git", "init", "-q"], ["git", "add", "-A"],
                     ["git", "-c", "user.name=scratch", "-c", "user.email=scratch@invalid", "commit", "-q", "-m",
                      "scratch export of the pinned tree"]):
            subprocess.run(argv, cwd=checkout, check=True)


def prepare(work: Path, placement: str) -> list[str]:
    """The export tree made usable for milan_soc.py, and the shipping configuration's SoC arguments at
    `placement`; refused when they name a platform image the tree does not hold."""
    tree = work / "tree"
    git_listable(tree)
    out = work / "builder-out"
    config = tree / "configs" / f"{yosys_sweep.BASE_CONFIG}.yaml"
    subprocess.run([sys.executable, str(tree / "sw/builder/endstation_builder.py"), "-o", str(out), str(config),
                    "--placement", placement], cwd=tree, capture_output=True, check=True)
    link = tree / "sw" / "builder" / "out"
    if not link.exists():
        link.symlink_to(out)
    params = json.loads((out / yosys_sweep.BASE_CONFIG / "soc_params.json").read_text())
    missing = missing_images(params["argv"], tree)
    if missing:
        raise yosys_sweep.PlanError(f"the {placement} SoC arguments name platform image(s) {missing} that the "
                                    "export tree does not hold; the sweep builds none (#665)")
    return [*params["argv"], "--entity-gen-dir", str(tree / "configs/generated" / yosys_sweep.BASE_CONFIG)]


def compiler_triple() -> str:
    """The SDK compiler's triple, derived as the baseline recipe derives it, from the SDK installer's COMPILER."""
    sys.path.insert(0, str(yosys_sweep.REPO / "scripts"))
    from ci_rv32_sdk import COMPILER  # noqa: E402,PLC0415 - the installer is the one source of the triple
    return COMPILER.removeprefix("bin/").removesuffix("-gcc")


def command_export(work: Path, plan: dict, names: list[str], tools: argparse.Namespace) -> int:
    """Run milan_soc.py without --build for each variant and record its outcome."""
    base = prepare(work, plan_placement(plan))
    env = {**os.environ, "PYTHONHASHSEED": "0", "LITEX_ENV_CC_TRIPLE": compiler_triple(),
           "PATH": f"{tools.sdk / 'bin'}:{Path(tools.litex_python).parent}:{os.environ['PATH']}"}
    records = {}
    for name, spec in plan_variants(plan).items():
        if names and name not in names:
            continue
        directory = work / "soc" / name
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True)
        argv = variant_argv(base, spec) + ["--output-dir", str(directory / "export")]
        log = directory / "export.log"
        with log.open("w") as handle:
            rc = subprocess.run([tools.litex_python, "milan_soc.py", *argv], cwd=work / "tree/sw/litex", env=env,
                                stdout=handle, stderr=subprocess.STDOUT, check=False).returncode
        text = log.read_text()
        refusal = next((line for line in text.splitlines() if "milan_soc.py: error:" in line), "")
        netlist = re.search(r"VexiiRiscv netlist : (\S+)", text)
        records[name] = {"argv": argv, "rc": rc, "refusal": refusal, "cpu_netlist": netlist.group(1) if netlist else "",
                         "log_sha256": yosys_sweep.sha256(log), "expected": spec.get("expect", "accepted")}
        print(f"soc {name}: rc={rc} {refusal or records[name]['cpu_netlist']}")
    (work / "soc" / "exports.json").write_text(json.dumps(records, indent=1, sort_keys=True) + "\n")
    surprises = [n for n, r in records.items() if (r["rc"] == 0) != (r["expected"] == "accepted")]
    if surprises:
        print(f"soc: outcome differs from the plan's expectation for {surprises}")
    return 1 if surprises else 0


def stubs(top_text: str, modules: set[str]) -> str:
    """Black-box declarations for each named module, from migen's instance blocks."""
    out = []
    for match in INSTANCE.finditer(top_text):
        module = match.group(2)
        if module not in modules:
            continue
        body = top_text[match.end():top_text.index(");", match.end())]
        params, ports, direction = [], [], ""
        for line in body.splitlines():
            stripped = line.strip()
            if stripped == "// Parameters.":
                direction = "parameter"
            elif stripped in SECTIONS:
                direction = SECTIONS[stripped]
            elif NAMED.match(line) and direction:
                (params if direction == "parameter" else ports).append((NAMED.match(line).group(1), direction))
        decl = [f"  parameter {name} = 0;" for name, _ in params]
        decl += [f"  {kind} [{STUB_WIDTH - 1}:0] {name};" for name, kind in ports]
        out.append(f"(* blackbox *)\nmodule {module}({', '.join(name for name, _ in ports)});\n"
                   + "\n".join(decl) + "\nendmodule\n")
        modules = modules - {module}
    if modules:
        raise yosys_sweep.PlanError(f"no instance of {sorted(modules)} in the top")
    return "\n".join(out)


def foreign_modules(top_text: str) -> set[str]:
    """Every instantiated module the top does not define and Yosys's Xilinx library does not know."""
    defined = set(re.findall(r"^module (\w+)", top_text, re.M))
    used = {match.group(2) for match in INSTANCE.finditer(top_text)}
    return {name for name in used - defined if not re.fullmatch(r"[A-Z0-9_]+", name)}


def yosys_flat(directory: Path, sources: list[Path], top: str, label: str) -> dict:
    """One flattened mapping; returns rc, seconds and the ooc.sh-taxonomy totals."""
    script = "; ".join([*(f"read_verilog {s}" for s in sources),
                        f"synth_xilinx -family xc7 -top {top} -flatten", f"tee -q -o {label}_stat.json stat -json"])
    with (directory / f"{label}.log").open("w") as log:
        rc = subprocess.run(["nice", "-n", "10", "yosys", "-q", "-p", script], cwd=directory, stdout=log,
                            stderr=subprocess.STDOUT, check=False).returncode
    if rc:
        return {"rc": rc}
    stat = json.loads((directory / f"{label}_stat.json").read_text())
    top_key, tree = yosys_sweep.expand(stat)
    return {"rc": 0, "top": top_key, "totals": tree["inclusive"][top_key]}


def cpu_sources(tcl_text: str, name: str) -> list[Path]:
    """The CPU netlist and its helper RAM files, as the export's own Tcl reads them: every
    read_verilog entry in the netlist's directory."""
    read = [Path(path) for path in re.findall(r"read_verilog\s+(?:-sv\s+)?\{([^}]+)\}", tcl_text)]
    netlist = [path for path in read if path.name == f"{name}.v"]
    if len(netlist) != 1:
        raise yosys_sweep.PlanError(f"the export Tcl reads {len(netlist)} copies of {name}.v")
    return [path for path in read if path.parent == netlist[0].parent]


def command_price(work: Path, names: list[str]) -> int:
    """Price the CPU core and the stubbed SoC top of every accepted export."""
    exports = json.loads((work / "soc" / "exports.json").read_text())
    results, failures = {}, 0
    for name, record in exports.items():
        if record["rc"] or (names and name not in names):
            continue
        directory = work / "soc" / name / "price"
        if directory.exists():
            shutil.rmtree(directory)
        shutil.copytree(work / "soc" / name / "export" / "gateware", directory)
        top_text = (directory / "alinx_ax7101.v").read_text()
        (directory / "stubs.v").write_text(stubs(top_text, foreign_modules(top_text)))
        cpu = cpu_sources((directory / "alinx_ax7101.tcl").read_text(), record["cpu_netlist"])
        results[name] = {
            "cpu_sources_sha256": {path.name: yosys_sweep.sha256(path) for path in cpu},
            "top_sha256": yosys_sweep.sha256(directory / "alinx_ax7101.v"),
            "stubbed": sorted(foreign_modules(top_text)),
            "cpu": yosys_flat(directory, cpu, record["cpu_netlist"], "cpu"),
            "top": yosys_flat(directory, [directory / "alinx_ax7101.v", directory / "stubs.v"], "alinx_ax7101", "top"),
        }
        failures += bool(results[name]["cpu"]["rc"] or results[name]["top"]["rc"])
        print(f"soc {name}: cpu {results[name]['cpu'].get('totals', results[name]['cpu'])}")
        print(f"soc {name}: top {results[name]['top'].get('totals', results[name]['top'])}")
    (work / "soc" / "prices.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
    return 1 if failures else 0


class _Exported(Exception):
    """Raised by the self-test's stand-in for prepare(), carrying the placement command_export asked for."""


def wiring_problems(plan: dict) -> list[str]:
    """prepare() and command_export() with the builder and the export stubbed (#665): the builder is asked for the
    placement given, and a builder run without one gives the config's own, the split; an argument list naming an
    absent platform image is refused before any export; an all-fabric one comes back with the shape's include;
    command_export asks prepare() for the plan's placement."""
    problems, calls = [], []
    module = sys.modules[__name__]

    def builder(argv: list[str], **_kwargs: object) -> subprocess.CompletedProcess:
        """The builder's stand-in: soc_params.json for the placement asked for (the split when none is)."""
        calls.append(list(argv))
        placement = argv[argv.index("--placement") + 1] if "--placement" in argv else "split"
        image = [] if placement == "all-fabric" else ["--ctrl-mailbox", "--ctrl-firmware", "sw/builder/out/c/x.elf"]
        out = Path(argv[argv.index("-o") + 1]) / yosys_sweep.BASE_CONFIG
        out.mkdir(parents=True, exist_ok=True)
        (out / "soc_params.json").write_text(json.dumps({"argv": ["--xlen", "32", *image]}))
        return subprocess.CompletedProcess(argv, 0)

    def stand_in(work: Path, placement: str) -> list[str]:
        """prepare()'s stand-in: stops command_export, carrying the placement it was asked for."""
        raise _Exported(placement)

    with tempfile.TemporaryDirectory(prefix="resmap-wiring-") as tmp:
        work = Path(tmp)
        (work / "tree/sw/builder").mkdir(parents=True)
        with mock.patch.object(module, "git_listable", lambda tree: None), mock.patch("subprocess.run", builder):
            try:
                argv = prepare(work, "all-fabric")
                if argv[-2:-1] != ["--entity-gen-dir"]:
                    problems.append(f"prepare(all-fabric) returned {argv}")
            except yosys_sweep.PlanError as refusal:
                problems.append(f"prepare(all-fabric) was refused: {refusal}")
            if not calls or calls[-1][-2:] != ["--placement", "all-fabric"]:
                problems.append(f"prepare(all-fabric) did not ask the builder for all-fabric: ...{calls[-1][-3:]}")
            try:
                prepare(work, "split")
                problems.append("prepare(split) returned an argument list naming an absent platform image")
            except yosys_sweep.PlanError as refusal:
                if "x.elf" not in str(refusal):
                    problems.append(f"prepare(split) refused without naming the image: {refusal}")
        with mock.patch.object(module, "prepare", stand_in):
            try:
                command_export(work, plan, [], argparse.Namespace(sdk=work, litex_python=sys.executable))
                problems.append("command_export ran past a refusing prepare()")
            except _Exported as asked:
                if str(asked) != plan_placement(plan):
                    problems.append(f"command_export asked prepare() for {asked}, the plan names "
                                    f"{plan_placement(plan)}")
            except yosys_sweep.PlanError as refusal:
                problems.append(f"command_export refused the plan: {refusal}")
        if (work / "soc").exists():
            problems.append("command_export wrote under soc/ before prepare() returned")
    return problems


SELFTEST_TOP = """module top(input a);
//------------------------------------------------------------------------------
// Instance core of core Module.
//------------------------------------------------------------------------------
core #(
\t// Parameters.
\t.WIDTH (4'd8)
) core (
\t// Inputs.
\t.clk (a),

\t// Outputs.
\t.q   (b)
);
BUFG BUFG(.I(a), .O(c));
endmodule
"""


def selftest() -> int:
    """The stub carries the parameter and both directions; a missing instance is refused; argv edits land."""
    problems = []
    text = stubs(SELFTEST_TOP, {"core"})
    for want in ("parameter WIDTH = 0;", "input [1023:0] clk;", "output [1023:0] q;", "module core(clk, q);"):
        if want not in text:
            problems.append(f"stub lacks {want!a}: {text!a}")
    if foreign_modules(SELFTEST_TOP) != {"core"}:
        problems.append(f"foreign modules wrong: {foreign_modules(SELFTEST_TOP)}")
    try:
        stubs(SELFTEST_TOP, {"absent"})
        problems.append("a module with no instance was stubbed silently")
    except yosys_sweep.PlanError:
        pass
    argv = variant_argv(["--xlen", "32", "--full"], {"set": {"--xlen": "64", "--l2-bytes": "8192"}, "add": ["--x"]})
    if argv != ["--xlen", "64", "--full", "--l2-bytes", "8192", "--x"]:
        problems.append(f"argv edit wrong: {argv}")
    with tempfile.TemporaryDirectory(prefix="resmap-soc-") as tmp:
        plan = yosys_sweep.load_plan(yosys_sweep.PLAN)
        (Path(tmp) / "names.txt").write_text("\n".join(plan_variants(plan)))
        if "ship" not in plan_variants(plan):
            problems.append("the plan has no shipping SoC variant")
        try:
            if plan_placement(plan) != "all-fabric":
                problems.append(f"the plan prices the {plan_placement(plan)} SoC, not the all-fabric one its "
                                "recorded figures were taken at")
        except yosys_sweep.PlanError as refusal:
            problems.append(f"the plan: {refusal}")
        try:
            plan_placement({"soc": {"variants": {}}})
            problems.append("a soc section that names no placement was accepted")
        except yosys_sweep.PlanError:
            pass
        image = Path(tmp) / "sw/builder/out/cfg/ctrl_app.elf"
        split = ["--ctrl-mailbox", "--ctrl-firmware", "sw/builder/out/cfg/ctrl_app.elf"]
        for label, argv, want in (("an absent platform image", split, ["sw/builder/out/cfg/ctrl_app.elf"]),
                                  ("a platform image flag with no value", split[:2], ["(no value)"]),
                                  ("an all-fabric argument list", ["--xlen", "32"], [])):
            if missing_images(argv, Path(tmp)) != want:
                problems.append(f"{label}: missing images {missing_images(argv, Path(tmp))}, want {want}")
        image.parent.mkdir(parents=True)
        image.write_bytes(b"\x7fELF")
        if missing_images(split, Path(tmp)):
            problems.append("a platform image present in the tree was reported missing")
        problems += wiring_problems(plan)
    for problem in problems:
        print(f"SELF-TEST FAILED: {problem}")
    print(f"soc_sweep self-test: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


def main() -> int:
    """The CLI; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work", type=Path)
    parser.add_argument("--plan", type=Path, default=yosys_sweep.PLAN)
    parser.add_argument("--litex-python", default=sys.executable)
    parser.add_argument("--sdk", type=Path)
    parser.add_argument("command", nargs="?", choices=("export", "price"))
    parser.add_argument("names", nargs="*")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.command is None or args.work is None:
        parser.print_help()
        return 2
    work = args.work.resolve()
    if args.command == "export":
        if args.sdk is None:
            print("export needs --sdk")
            return 2
        try:
            return command_export(work, yosys_sweep.load_plan(args.plan), args.names, args)
        except yosys_sweep.PlanError as refusal:
            print(f"soc_sweep: export refused: {refusal}")
            return 2
    return command_price(work, args.names)


if __name__ == "__main__":
    sys.exit(main())
