#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Design-parameter sweep (issue #649): price every plan point with Yosys, and
write the matching Vivado calibration point.

The plan is syn/resmap/sweep_plan.json. Every point is the shipping AX7101 1x1
TDM8 shape with the changes the point names: parameter values, an entity shape
generated from a variant of the shipping configuration, or a package or module
default in a scratch copy of one source. Nothing in the checkout is written;
every artifact lands under the work directory the caller names.

THE INSTRUMENT is the recipe's hierarchy-preserving Yosys mapping
(`synth_xilinx -family xc7 -top <top>`, no `-flatten`), because it keeps every
block's cells inside its own module: a point's per-block figures are read off
`stat -json` by expanding each module with its multiplicity. A point marked
`anchor` is also mapped with `-flatten`, the instrument syn/yosys/ooc.sh
publishes. The column taxonomy is ooc.sh's: LUT is LUT1 to LUT6, LUTRAM is the
LUT6 equivalent of each distributed-RAM cell (UG474), FF is FD*. INV cells are
counted apart, as ooc.sh leaves them out of every column.

SOURCES are never listed here. A top's read set, include path and defines are
the record syn/ooc/dp_srcs.py derives from syn/yosys/run.sh; the shape
directory replaces the record's first include directory, which is the
elaboration-shape slot. A `milan_datapath` point is shaped by rewriting the
DEFAULTS of a scratch copy of the top, because `chparam` cannot re-derive that
top (syn/yosys/ooc.sh says why); the other tops take `chparam`. ROM images come
from syn/yosys/ooc.sh, which generates and validates them against
syn/yosys/rom_digests.tsv, and every copy a run reads is re-hashed against the
ledger row for the current gitlinks.

Subcommands, each taking --work DIR:

    shapes        export HEAD and its pinned submodules, write every variant
                  configuration and run the builder on it
    roms          generate and validate the three ROM images
    run [NAME..]  price the points (all by default), --jobs at a time
    guards [NAME..]
                  lint each point that ran with --verilator, which evaluates the
                  RTL's elaboration guards (`$error` in a generate block) that the
                  sv2v conversion leaves unenforced; a firing guard marks the
                  point as a shape the product refuses
    vivado-point NAME
                  write the point file syn/resmap/datapath_ooc.tcl reads
    summary       write summary.json: per point, totals and per-block figures
                  at --depth levels ("blocks") and at one level ("blocks1"),
                  each set tied to Yosys's own design totals

--selftest proves the parameter rewrite, the module expansion, its tie and the
plan validation on synthetic inputs.
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PLAN = HERE / "sweep_plan.json"
LEDGER = REPO / "syn" / "yosys" / "rom_digests.tsv"
ROMS = ("ltn_rom.hex", "ucode.hex", "gptp_ucode.hex")
#: The ROM image each submodule pin owns in the ledger.
ROM_OWNER = {"ltn_rom.hex": "protocol-processor", "ucode.hex": "protocol-processor",
             "gptp_ucode.hex": "gptp-processor"}
SUBMODULES = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
BASE_CONFIG = "endstation_ax7101_1x1_tdm8"
#: Shipping stream lines the variants rewrite; each must occur exactly once.
LISTENER = '    - { name: "Stream In 0", channels: 8, map_mode: dynamic }\n'
TALKER = '    - { name: "Stream Out 0", channels: 8, map_mode: dynamic }\n'
#: Distributed-RAM cells and their LUT6 cost: ooc.sh's table (UG474 SLICEM occupancy).
LUTRAM_COST = {**dict.fromkeys(("RAM256X1D", "RAM512X1S", "RAM32X8S", "RAM64X8SW", "RAM32X16DR8"), 8),
               **dict.fromkeys(("RAM32M", "RAM64M", "RAM128X1D", "RAM32M16", "RAM64M8", "RAM256X1S",
                                "RAM32X4S"), 4),
               **dict.fromkeys(("RAM32X1D", "RAM32X1D_1", "RAM64X1D", "RAM64X1D_1", "RAM128X1S",
                                "RAM128X1S_1", "RAM32X2S", "RAM64X2S"), 2),
               **dict.fromkeys(("RAM32X1S", "RAM32X1S_1", "RAM64X1S", "RAM64X1S_1"), 1)}
COLUMNS = ("LUT", "LUTRAM", "SRL", "LUT_TOT", "FF", "RAMB36", "RAMB18", "DSP", "CARRY4", "MUXF7", "MUXF8", "INV")


class PlanError(Exception):
    """The plan, a point or an input cannot be used as written."""


# ------------------------------------------------------------------ plan


def load_plan(path: Path) -> dict:
    """Read and validate the plan: unique names, known tops and shapes, typed values."""
    plan = json.loads(path.read_text())
    names = [point["name"] for point in plan["points"]]
    if len(names) != len(set(names)):
        raise PlanError("point names repeat")
    shapes = {plan["tops"]["milan_datapath"]["shape"], *plan.get("tracked_shapes", []), *plan["variants"]}
    for point in plan["points"]:
        if point["top"] not in plan["tops"]:
            raise PlanError(f"{point['name']}: unknown top {point['top']}")
        if point.get("shape", BASE_CONFIG) not in shapes:
            raise PlanError(f"{point['name']}: unknown shape {point['shape']}")
        values = [*point.get("params", {}).values()]
        values += [v for patch in point.get("patch", {}).values() for v in patch.values()]
        if not all(isinstance(value, int) for value in values):
            raise PlanError(f"{point['name']}: every value must be a decimal integer")
    return plan


def point_params(plan: dict, point: dict) -> dict[str, int]:
    """The top's base parameters with the point's own laid over them."""
    return {**plan["tops"][point["top"]]["params"], **point.get("params", {})}


# ---------------------------------------------------------- source rewrite


def patch_params(text: str, params: dict[str, int]) -> str:
    """Rewrite each named parameter or localparam default; each must occur exactly once."""
    for name, value in params.items():
        pattern = re.compile(r"(^\s*(?:parameter|localparam)\b[^=;\n]*?\b" + re.escape(name)
                             + r"\s*=\s*)([^,;\n/]+?)(?=\s*(?:,|;|//|\n|$))", re.M)
        text, count = pattern.subn(lambda match, v=value: match.group(1) + str(v), text)
        if count != 1:
            raise PlanError(f"parameter {name} is declared {count} times where exactly one was expected")
    return text


def find_declaring(srcs: list[str], declaration: str) -> str:
    """The one source declaring `module NAME` or `package NAME`."""
    kind, name = declaration.split()
    pattern = re.compile(rf"^\s*{kind}\s+(?:automatic\s+)?{re.escape(name)}\b", re.M)
    hits = [src for src in srcs if pattern.search(Path(src).read_text())]
    if len(hits) != 1:
        raise PlanError(f"{declaration}: declared in {len(hits)} sources, expected exactly one")
    return hits[0]


def record_of(top: str) -> dict:
    """The derived read set of a run.sh top: dp_srcs.py's record, parsed."""
    run = subprocess.run([sys.executable, str(REPO / "syn/ooc/dp_srcs.py"), "--top", top, "--record"],
                         capture_output=True, text=True, check=False)
    if run.returncode:
        raise PlanError(f"dp_srcs.py --top {top} --record exited {run.returncode}: {run.stderr.strip()}")
    record: dict[str, list[str]] = {"top": [], "define": [], "incdir": [], "src": []}
    for line in run.stdout.splitlines():
        key, _, value = line.partition("=")
        if key not in record or not value:
            raise PlanError(f"unrecognized record line {line!a}")
        record[key].append(value)
    return record


def shape_dir(work: Path, shape: str) -> Path:
    """A tracked generated shape, or one the shapes command generated under the work tree."""
    stem = shape if shape.startswith("endstation_") else f"endstation_{shape}"
    for root in (REPO, work / "tree"):
        candidate = root / "configs" / "generated" / stem
        header = candidate / "gen" / "adp_shape_defaults.svh"
        if header.is_file():
            if f"configs/{stem}.yaml" not in header.read_text():
                raise PlanError(f"{header} does not name {shape} as its source")
            return candidate
    raise PlanError(f"no generated shape {shape}; run the shapes command first")


def sha256(path: Path) -> str:
    """Hex SHA-256 of one file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ------------------------------------------------------------ ROM custody


def gitlink(path: str) -> str:
    """The superproject's recorded revision of one submodule."""
    run = subprocess.run(["git", "rev-parse", f"HEAD:{path}"], cwd=REPO, capture_output=True, text=True,
                         check=True)
    return run.stdout.strip()


def ledger_digests() -> dict[str, str]:
    """The ledger's digest of each ROM image at the current gitlinks."""
    pins = {name: gitlink(owner) for name, owner in ROM_OWNER.items()}
    rows = [line.split("\t") for line in LEDGER.read_text().splitlines() if line and not line.startswith("#")]
    found = {image: digest for pin, image, digest in rows if pins.get(image) == pin}
    if set(found) != set(ROMS):
        raise PlanError(f"the ROM ledger has no row for {sorted(set(ROMS) - set(found))} at the current pins")
    return found


def stage_roms(work: Path, destination: Path) -> dict[str, str]:
    """Copy the validated ROM images into a run directory, each re-hashed against the ledger."""
    expected = ledger_digests()
    for image in ROMS:
        target = destination / image
        shutil.copyfile(work / "roms" / image, target)
        if sha256(target) != expected[image]:
            raise PlanError(f"{image}: the staged copy does not hash to the ledger row")
    return expected


def command_roms(work: Path) -> int:
    """Generate and validate the three images with syn/yosys/ooc.sh on its smallest top."""
    roms = work / "roms"
    roms.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "OOC_TMP": str(roms)}
    with (roms / "ooc.sh.log").open("w") as log:
        run = subprocess.run(["bash", str(REPO / "syn/yosys/ooc.sh"), "tcam"], env=env, stdout=log,
                             stderr=subprocess.STDOUT, check=False)
    if run.returncode:
        print(f"roms: ooc.sh exited {run.returncode}; see {roms / 'ooc.sh.log'}")
        return run.returncode
    digests = ledger_digests()
    for image in ROMS:
        if sha256(roms / image) != digests[image]:
            print(f"roms: {image} does not hash to its ledger row")
            return 1
    print(f"roms: three images validated against the ledger at {gitlink('protocol-processor')[:8]} and "
          f"{gitlink('gptp-processor')[:8]}")
    return 0


# ---------------------------------------------------------------- shapes


def export_tree(work: Path) -> Path:
    """HEAD and its three pinned submodules, archived into work/tree (never a checkout).

    An existing export is reused only when its marker names this HEAD and these pins.
    """
    tree = work / "tree"
    marker = tree / ".resmap-export"
    identity = " ".join([_head(), *(gitlink(sub) for sub in SUBMODULES)]) + "\n"
    if tree.exists():
        if not marker.is_file() or marker.read_text() != identity:
            raise PlanError(f"{tree} exists and is not this checkout's export; use an empty work directory")
        return tree
    tree.mkdir(parents=True)
    _extract(["git", "archive", "HEAD"], REPO, tree)
    for sub in SUBMODULES:
        checkout = REPO / sub
        top = subprocess.run(["git", "-C", str(checkout), "rev-parse", "--show-toplevel"], capture_output=True,
                             text=True, check=True).stdout.strip()
        head = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"], capture_output=True, text=True,
                              check=True).stdout.strip()
        if Path(top) != checkout or head != gitlink(sub):
            raise PlanError(f"{sub}: the checkout is not the superproject's pin ({head} against {gitlink(sub)})")
        (tree / sub).mkdir(parents=True, exist_ok=True)
        _extract(["git", "archive", "HEAD"], checkout, tree / sub)
    marker.write_text(identity)
    return tree


def _head() -> str:
    """The superproject's HEAD revision."""
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True,
                          check=True).stdout.strip()


def _extract(argv: list[str], cwd: Path, destination: Path) -> None:
    """Run an archive command into a temporary tar file and unpack it."""
    with tempfile.TemporaryFile() as handle:
        subprocess.run(argv, cwd=cwd, stdout=handle, check=True)
        handle.seek(0)
        with tarfile.open(fileobj=handle) as archive:
            archive.extractall(destination, filter="tar")


def variant_text(base: str, spec: dict) -> str:
    """The shipping configuration with its stream section and named lines rewritten."""
    if base.count(LISTENER) != 1 or base.count(TALKER) != 1:
        raise PlanError("the shipping configuration's stream lines are not where the variants expect them")
    channels, streams = spec["channels"], spec["streams"]
    listeners = "".join(LISTENER.replace("In 0", f"In {k}").replace("channels: 8", f"channels: {channels}")
                        for k in range(streams))
    talkers = "".join(TALKER.replace("Out 0", f"Out {k}").replace("channels: 8", f"channels: {channels}")
                      for k in range(streams))
    text = base.replace(LISTENER, listeners).replace(TALKER, talkers)
    for old, new in spec.get("replace", []):
        if text.count(old) != 1:
            raise PlanError(f"variant line {old!a} does not occur exactly once")
        text = text.replace(old, new)
    return text


def command_shapes(work: Path, plan: dict) -> int:
    """Export the tree, write each variant configuration and generate its shape with the builder."""
    tree = export_tree(work)
    base = (tree / "configs" / f"{BASE_CONFIG}.yaml").read_text()
    failures = 0
    for name, spec in plan["variants"].items():
        config = tree / "configs" / f"endstation_{name}.yaml"
        config.write_text(variant_text(base, spec))
        log = work / "shapes" / f"{name}.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open("w") as handle:
            run = subprocess.run([sys.executable, str(tree / "sw/builder/endstation_builder.py"), "-o",
                                  str(work / "builder-out"), str(config)], cwd=tree, stdout=handle,
                                 stderr=subprocess.STDOUT, check=False)
        print(f"shape {name}: builder rc={run.returncode}")
        failures += run.returncode != 0
    return 1 if failures else 0


# ------------------------------------------------------------- one point


def prepare_sources(work: Path, plan: dict, point: dict, directory: Path) -> dict:
    """The point's record with its shape include and its rewritten sources in place."""
    top = point["top"]
    record = record_of(plan["tops"][top].get("record", top))
    srcs = list(record["src"])
    rewrites = dict(point.get("patch", {}))
    if top == "milan_datapath":
        rewrites[f"module {top}"] = point_params(plan, point)
        if "configs/generated/" not in record["incdir"][0]:
            raise PlanError("the record's first include directory is not the elaboration-shape slot")
        record["incdir"][0] = str(shape_dir(work, point.get("shape", plan["tops"][top]["shape"])))
    for declaration, params in rewrites.items():
        original = find_declaring(srcs, declaration)
        copy = directory / "src" / Path(original).name
        copy.parent.mkdir(exist_ok=True)
        copy.write_text(patch_params(Path(original).read_text(), params))
        srcs[srcs.index(original)] = str(copy)
    record["src"] = srcs
    return record


def yosys_script(top: str, chparams: dict[str, int], flatten: bool, stat: str) -> str:
    """The recipe's mapping, hierarchical unless flatten, with stat -json captured to a file."""
    lines = ["read_verilog design.v"]
    lines += [f"chparam -set {name} {value} {top}" for name, value in chparams.items()]
    lines.append(f"synth_xilinx -family xc7 -top {top}" + (" -flatten" if flatten else ""))
    lines.append(f"tee -q -o {stat} stat -json")
    return "; ".join(lines)


def run_point(work: Path, plan: dict, point: dict, malloc: str) -> dict:
    """Convert, map and record one point; the receipt is returned and written beside it."""
    directory = work / "points" / point["name"]
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True)
    start = time.time()
    receipt = {"point": point, "rc": {}, "seconds": {}}
    record = prepare_sources(work, plan, point, directory)
    top = point["top"]
    argv = ["sv2v", f"--top={top}", *(f"-D{d}" for d in record["define"]), *(f"-I{i}" for i in record["incdir"]),
            *record["src"]]
    with (directory / "design.v").open("w") as out, (directory / "sv2v.err").open("w") as err:
        receipt["rc"]["sv2v"] = subprocess.run(argv, cwd=directory, stdout=out, stderr=err, check=False).returncode
    receipt["roms"] = stage_roms(work, directory)
    chparams = {} if top == "milan_datapath" else point_params(plan, point)
    runs = [("hierarchical", False, "stat.json")]
    if point.get("anchor"):
        runs.append(("flat", True, "stat_flat.json"))
    env = {**os.environ, **({"LD_PRELOAD": malloc} if malloc else {})}
    for label, flatten, stat in runs:
        if receipt["rc"]["sv2v"]:
            break
        began = time.time()
        with (directory / f"yosys_{label}.log").open("w") as log:
            run = subprocess.run(["nice", "-n", "10", "yosys", "-q", "-p", yosys_script(top, chparams, flatten, stat)],
                                 cwd=directory, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
        receipt["rc"][label] = run.returncode
        receipt["seconds"][label] = round(time.time() - began, 1)
    receipt["seconds"]["total"] = round(time.time() - start, 1)
    receipt["inputs"] = {"record_sources": len(record["src"]), "incdir": record["incdir"], "define": record["define"],
                         "rewritten": {p.name: sha256(p) for p in sorted((directory / "src").glob("*"))}
                         if (directory / "src").is_dir() else {},
                         "design.v": sha256(directory / "design.v"),
                         "shape_header": _shape_digest(record, top)}
    receipt["outputs"] = {p.name: {"sha256": sha256(p), "bytes": p.stat().st_size}
                          for p in sorted(directory.glob("*")) if p.suffix in (".json", ".log", ".err")}
    (directory / "receipt.json").write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    (directory / "design.v").unlink()
    return receipt


def _shape_digest(record: dict, top: str) -> str:
    """The digest of the shape header a datapath point elaborated, or a dash."""
    if top != "milan_datapath":
        return "-"
    return sha256(Path(record["incdir"][0]) / "gen" / "adp_shape_defaults.svh")


def select_malloc() -> str:
    """The allocator syn/yosys/malloc.sh selects for Yosys; speed only, never results."""
    run = subprocess.run(["bash", "-c", '. "$0"; select_malloc', str(REPO / "syn/yosys/malloc.sh")],
                         capture_output=True, text=True, check=False)
    return run.stdout.strip() if run.returncode == 0 else ""


def command_run(work: Path, plan: dict, names: list[str], jobs: int) -> int:
    """Price the named points (every point when none is named), `jobs` at a time."""
    chosen = [p for p in plan["points"] if not names or p["name"] in names]
    missing = sorted(set(names) - {p["name"] for p in chosen})
    if missing:
        print(f"run: no such point {missing}")
        return 2
    malloc = select_malloc()
    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(run_point, work, plan, point, malloc): point["name"] for point in chosen}
        for future in concurrent.futures.as_completed(futures):
            try:
                receipt = future.result()
            except (PlanError, OSError, subprocess.SubprocessError) as failure:
                print(f"point {futures[future]}: refused: {failure}", flush=True)
                failures += 1
                continue
            bad = {k: v for k, v in receipt["rc"].items() if v}
            failures += bool(bad)
            print(f"point {futures[future]}: rc {receipt['rc']} in {receipt['seconds']['total']} s", flush=True)
    return 1 if failures else 0


# ---------------------------------------------------------------- guards


#: An elaboration-time `$error`/`$fatal` Verilator evaluated, and any other hard error.
USER_GUARD = re.compile(r"^%(?:Warning|Error)-USER(?:ERROR|FATAL): (.*)$")
HARD_ERROR = re.compile(r"^%Error(?!-USER)(?!: Exiting due to)")


def guard_point(work: Path, plan: dict, point: dict, verilator: str) -> dict:
    """Lint one point with Verilator, which evaluates the RTL's elaboration guards that the
    conversion for Yosys does not: a guard that fires means the shape is one the product refuses."""
    directory = work / "points" / point["name"] / "guards"
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True)
    record = prepare_sources(work, plan, point, directory)
    top = point["top"]
    params = {} if top == "milan_datapath" else point_params(plan, point)
    argv = [verilator, "--lint-only", "--sv", "-Wno-fatal", "--top-module", top,
            *(f"-D{d}" for d in record["define"]), *(f"-I{i}" for i in record["incdir"]),
            *(f"-G{name}={value}" for name, value in params.items()), *record["src"]]
    run = subprocess.run(argv, cwd=directory, capture_output=True, text=True, check=False)
    refusals, errors = guard_lines((run.stdout + run.stderr).splitlines())
    result = {"rc": run.returncode, "verilator": subprocess.run([verilator, "--version"], capture_output=True,
                                                                   text=True, check=False).stdout.strip(),
              "refusals": refusals, "errors": errors}
    (directory.parent / "guards.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    shutil.rmtree(directory)
    return result


def guard_lines(lines: list[str]) -> tuple[list[str], list[str]]:
    """The distinct elaboration-guard messages and the hard errors in one Verilator output."""
    refusals = sorted({match.group(1) for match in map(USER_GUARD.match, lines) if match})
    return refusals, [line for line in lines if HARD_ERROR.match(line)]


def command_guards(work: Path, plan: dict, names: list[str], jobs: int, verilator: str) -> int:
    """Run the guard lint over the named points (every point that ran when none is named)."""
    chosen = [p for p in plan["points"] if (not names or p["name"] in names)
              and (work / "points" / p["name"]).is_dir()]
    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(guard_point, work, plan, point, verilator): point["name"] for point in chosen}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            failures += result["rc"] != 0 or bool(result["errors"])
            print(f"guards {futures[future]}: rc {result['rc']}, {len(result['refusals'])} refusal(s) "
                  f"{result['refusals'][:1]}", flush=True)
    return 1 if failures else 0


# --------------------------------------------------------------- results


def base_name(module: str) -> str:
    """The source module name of a Yosys module, its parameterization stripped."""
    name = module.lstrip("\\")
    if name.startswith("$paramod"):
        return name.split("\\")[1]
    return name


def classify(cells: dict[str, int]) -> dict[str, int]:
    """Primitive counts in the ooc.sh taxonomy; an unpriced distributed RAM is refused."""
    out = dict.fromkeys(COLUMNS, 0)
    for kind, count in cells.items():
        if re.fullmatch(r"LUT[1-6]", kind):
            out["LUT"] += count
        elif kind.startswith("RAM") and not kind.startswith("RAMB"):
            if kind not in LUTRAM_COST:
                raise PlanError(f"distributed-RAM cell {kind} has no LUT6 cost")
            out["LUTRAM"] += count * LUTRAM_COST[kind]
        elif kind in ("SRL16E", "SRLC32E"):
            out["SRL"] += count
        elif re.fullmatch(r"FD[CPRS]E?", kind):
            out["FF"] += count
        else:
            column = {"RAMB36E1": "RAMB36", "RAMB18E1": "RAMB18", "DSP48E1": "DSP"}.get(kind, kind)
            if column in out:
                out[column] += count
    out["LUT_TOT"] = out["LUT"] + out["LUTRAM"] + out["SRL"]
    return out


def expand(stat: dict) -> tuple[str, dict[str, dict]]:
    """The top module and every module's own and inclusive figures, from one stat -json."""
    modules = {name.lstrip("\\"): body["num_cells_by_type"] for name, body in stat["modules"].items()}
    children = {name: {k.lstrip("\\"): v for k, v in cells.items() if k.lstrip("\\") in modules}
                for name, cells in modules.items()}
    instantiated = {child for kids in children.values() for child in kids}
    tops = [name for name in modules if name not in instantiated]
    if len(tops) != 1:
        raise PlanError(f"expected one top module in the stat output, found {len(tops)}")
    inclusive: dict[str, dict[str, int]] = {}

    def total(name: str) -> dict[str, int]:
        """A module's own primitives plus each child's inclusive figures times its count."""
        if name not in inclusive:
            figures = classify({k: v for k, v in modules[name].items() if k.lstrip("\\") not in modules})
            for child, count in children[name].items():
                for column, value in total(child).items():
                    figures[column] += count * value
            inclusive[name] = figures
        return inclusive[name]

    total(tops[0])
    own = {name: classify({k: v for k, v in cells.items() if k.lstrip("\\") not in modules})
           for name, cells in modules.items()}
    return tops[0], {"own": own, "inclusive": inclusive, "children": children}


def blocks(top: str, tree: dict, depth: int) -> dict[str, dict]:
    """Per-block figures to `depth` levels, keyed by source module path, multiplicities applied."""
    out: dict[str, dict] = {}

    def walk(name: str, path: str, multiple: int, level: int) -> None:
        """Record one node; recurse while levels remain, else record the subtree whole."""
        kids = tree["children"][name]
        if level == depth or not kids:
            _add(out, path, tree["inclusive"][name], multiple)
            return
        _add(out, f"{path}/@own", tree["own"][name], multiple)
        for child, count in kids.items():
            walk(child, f"{path}/{base_name(child)}", multiple * count, level + 1)

    walk(top, base_name(top), 1, 0)
    return out


def _add(out: dict, path: str, figures: dict[str, int], multiple: int) -> None:
    """Accumulate `multiple` copies of one block's figures under its path, counting instances."""
    entry = out.setdefault(path, {"instances": 0, **dict.fromkeys(COLUMNS, 0)})
    entry["instances"] += multiple
    for column in COLUMNS:
        entry[column] += multiple * figures[column]


def tie(stat: dict, top: str, tree: dict, parts: dict[str, dict]) -> list[str]:
    """The expansion's sums against Yosys's own design totals, and the blocks against the top."""
    failures = []
    design = classify({k: v for k, v in stat["design"]["num_cells_by_type"].items()
                       if not k.startswith("$paramod") and k.lstrip("\\") not in
                       {name.lstrip("\\") for name in stat["modules"]}})
    for column in COLUMNS:
        if tree["inclusive"][top][column] != design[column]:
            failures.append(f"{column}: the expansion gives {tree['inclusive'][top][column]}, Yosys {design[column]}")
        if sum(entry[column] for entry in parts.values()) != design[column]:
            failures.append(f"{column}: the blocks sum to {sum(e[column] for e in parts.values())}, Yosys "
                            f"{design[column]}")
    return failures


def summarize(directory: Path, depth: int) -> dict:
    """One point's totals and blocks, every figure tied to Yosys's design totals."""
    result: dict = {"receipt": json.loads((directory / "receipt.json").read_text())}
    if (directory / "guards.json").is_file():
        result["guards"] = json.loads((directory / "guards.json").read_text())
    for label, name in (("hierarchical", "stat.json"), ("flat", "stat_flat.json")):
        path = directory / name
        if not path.is_file():
            continue
        stat = json.loads(path.read_text())
        top, tree = expand(stat)
        result[label] = {"totals": tree["inclusive"][top]}
        for key, levels in (("blocks", depth), ("blocks1", 1)):
            parts = blocks(top, tree, levels)
            failures = tie(stat, top, tree, parts)
            if failures:
                raise PlanError(f"{directory.name} {label} depth {levels}: " + "; ".join(failures))
            result[label][key] = parts
    return result


def command_summary(work: Path, plan: dict, depth: int) -> int:
    """Summarize every point that ran, refusing any whose figures do not tie."""
    summary, failures = {}, 0
    for point in plan["points"]:
        directory = work / "points" / point["name"]
        if not (directory / "receipt.json").is_file():
            continue
        try:
            summary[point["name"]] = summarize(directory, depth)
        except PlanError as failure:
            print(f"summary: {failure}")
            failures += 1
    (work / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n")
    print(f"summary: {len(summary)} points tied, {failures} refused")
    return 1 if failures else 0


# ----------------------------------------------------------- Vivado point


def command_vivado_point(work: Path, plan: dict, name: str) -> int:
    """Write the point file datapath_ooc.tcl reads, its rewritten sources and its ROM copies."""
    point = next((p for p in plan["points"] if p["name"] == name), None)
    if point is None:
        print(f"vivado-point: no such point {name}")
        return 2
    directory = work / "vivado" / name
    directory.mkdir(parents=True, exist_ok=True)
    record = prepare_sources(work, plan, point, directory)
    stage_roms(work, directory)
    generics = [f"{k}={v}" for k, v in point_params(plan, point).items()]
    if point["top"] == "milan_datapath":
        generics += [f'{param}="{directory / image}"' for param, image in
                     (("PP_TROM_HEX_P", "ltn_rom.hex"), ("PP_UCODE_HEX_P", "ucode.hex"),
                      ("GPTP_UCODE_HEX_P", "gptp_ucode.hex"))]
    lines = [f"top={point['top']}", f"part={plan['part']}", f"clock_ns={plan['clock_ns']}"]
    lines += [f"incdir={d}" for d in record["incdir"]] + [f"define={d}" for d in record["define"]]
    lines += [f"src={s}" for s in record["src"]] + [f"generic={g}" for g in generics]
    (directory / "point.txt").write_text("\n".join(lines) + "\n")
    print(f"vivado-point {name}: {directory / 'point.txt'}")
    return 0


# -------------------------------------------------------------- self-test


SELFTEST_MODULE = """module m #(
  parameter int A = 1,
  parameter bit B = 1'b1,
  parameter logic [31:0] C  = 32'h2000_0000,
  parameter int unsigned D = A / 2, // derived
  parameter int E = 3
)();
endmodule
package p;
  localparam int unsigned F       = 16;  // note
endpackage
"""


def _selftest_patch() -> list[str]:
    """The rewrite changes exactly the named defaults and refuses an absent name."""
    problems = []
    text = patch_params(SELFTEST_MODULE, {"A": 4, "B": 0, "C": 7, "E": 9, "F": 32})
    wanted = ("parameter int A = 4,", "parameter bit B = 0,", "C  = 7,", "D = A / 2, // derived",
              "parameter int E = 9\n", "F       = 32;  // note")
    problems += [f"patch: {want!a} missing after the rewrite" for want in wanted if want not in text]
    try:
        patch_params(SELFTEST_MODULE, {"G": 1})
        problems.append("patch: an absent parameter was accepted")
    except PlanError:
        pass
    return problems


def _selftest_stat() -> dict:
    """A two-level design: top owns a LUT6 and two copies of mid; mid owns a leaf; leaf owns cells."""
    return {"modules": {
        "\\top": {"num_cells_by_type": {"LUT6": 1, "$paramod$ab\\mid": 2}},
        "$paramod$ab\\mid": {"num_cells_by_type": {"FDRE": 3, "leaf": 1, "INV": 1}},
        "\\leaf": {"num_cells_by_type": {"RAM32M": 1, "CARRY4": 2, "RAMB36E1": 1}}},
        "design": {"num_cells_by_type": {"LUT6": 1, "FDRE": 6, "RAM32M": 2, "CARRY4": 4, "RAMB36E1": 2, "INV": 2,
                                         "$paramod$ab\\mid": 2, "leaf": 2}}}


def _selftest_expand() -> list[str]:
    """Expansion multiplies, the blocks tie, and a planted wrong count is caught."""
    problems = []
    stat = _selftest_stat()
    top, tree = expand(stat)
    parts = blocks(top, tree, 2)
    if top != "top" or parts.get("top/mid/leaf", {}).get("LUTRAM") != 8 or parts["top/mid/@own"]["FF"] != 6:
        problems.append(f"expand: wrong expansion {parts}")
    if tie(stat, top, tree, parts):
        problems.append(f"expand: the consistent design does not tie: {tie(stat, top, tree, parts)}")
    stat["modules"]["\\leaf"]["num_cells_by_type"]["CARRY4"] = 3
    top, tree = expand(stat)
    if not tie(stat, top, tree, blocks(top, tree, 2)):
        problems.append("expand: a planted wrong CARRY4 count tied clean")
    try:
        classify({"RAM16X1S": 1})
        problems.append("classify: an unpriced distributed RAM was counted as free")
    except PlanError:
        pass
    return problems


def _selftest_plan() -> list[str]:
    """The tracked plan loads; a repeated name and a non-integer value are refused."""
    problems = []
    plan = load_plan(PLAN)
    with tempfile.TemporaryDirectory(prefix="resmap-plan-") as tmp:
        for label, mutate in (("repeated name", lambda p: p["points"].append(dict(p["points"][0]))),
                              ("non-integer value", lambda p: p["points"][0].update(params={"N_STREAMS": "2"}))):
            broken = json.loads(json.dumps(plan))
            mutate(broken)
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(broken))
            try:
                load_plan(path)
                problems.append(f"plan: a {label} was accepted")
            except PlanError:
                pass
    base = (REPO / "configs" / f"{BASE_CONFIG}.yaml").read_text()
    text = variant_text(base, {"streams": 2, "channels": 4})
    if text.count('channels: 4, map_mode: dynamic') != 4:
        problems.append("plan: the 2x2 four-channel variant does not declare four four-channel streams")
    return problems


def _selftest_guards() -> list[str]:
    """A guard message and a hard error are read; the exit summary and other warnings are not."""
    lines = ["%Warning-USERERROR: a.sv:1:5: N_NAME_P=235 outside 1..128", "%Warning-WIDTH: a.sv:2:1: width",
             "%Error: b.sv:3:1: syntax error", "%Error: Exiting due to 1 error(s)",
             "%Warning-USERERROR: a.sv:1:5: N_NAME_P=235 outside 1..128"]
    refusals, errors = guard_lines(lines)
    if refusals != ["a.sv:1:5: N_NAME_P=235 outside 1..128"] or errors != ["%Error: b.sv:3:1: syntax error"]:
        return [f"guards: wrong reading {refusals} {errors}"]
    return []


def selftest() -> int:
    """Every arm on synthetic inputs; exit 0 only when all pass."""
    problems = _selftest_patch() + _selftest_expand() + _selftest_plan() + _selftest_guards()
    for problem in problems:
        print(f"SELF-TEST FAILED: {problem}")
    print(f"yosys_sweep self-test: {'PASS' if not problems else 'FAIL'} ({len(problems)} problems)")
    return 1 if problems else 0


def main() -> int:
    """The CLI; see the module docstring."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--plan", type=Path, default=PLAN)
    parser.add_argument("--work", type=Path)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--depth", type=int, default=3, help="block levels below the top in the summary")
    parser.add_argument("--verilator", default="verilator", help="the Verilator the guards command runs")
    parser.add_argument("command", nargs="?",
                        choices=("shapes", "roms", "run", "guards", "vivado-point", "summary"))
    parser.add_argument("names", nargs="*")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.command is None or args.work is None:
        parser.print_help()
        return 2
    plan = load_plan(args.plan)
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    if args.command == "shapes":
        return command_shapes(work, plan)
    if args.command == "roms":
        return command_roms(work)
    if args.command == "run":
        return command_run(work, plan, args.names, args.jobs)
    if args.command == "guards":
        return command_guards(work, plan, args.names, args.jobs, args.verilator)
    if args.command == "summary":
        return command_summary(work, plan, args.depth)
    return command_vivado_point(work, plan, args.names[0] if args.names else "")


if __name__ == "__main__":
    sys.exit(main())
