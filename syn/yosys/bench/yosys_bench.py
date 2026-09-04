#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure what ONE Yosys process costs on one of the gate's own tops (#286).

Why this exists. The portability gate (syn/yosys/run.sh) cannot finish faster
than its single longest top, and that top is one single-threaded `yosys`
process. Every speed question about the gate - allocator, front end, rebuilt
binary, host tuning - comes down to one measurement: what that process spends
its time on and whether a lever moves it. A figure quoted without the machine,
the tool versions, the trial count and the concurrency it ran at is not
comparable with any other, and the first pass of these figures was taken by
hand. This harness is the reproducible form.

WHAT IT DOES, per top:

  1. STAGES the top exactly as the gate does. The define/incdir/src record
     comes from `run.sh --emit TOP` and from nowhere else - there is no second
     source list to drift - and `sv2v` lowers it into a work directory beside
     the same three ROM images run.sh generates for `$readmemh`. The sha256 of
     the staged Verilog is the INPUT DIGEST every record carries.
  2. RUNS the gate's own program, `yosys -d -p "read_verilog TOP.v; synth -top
     TOP; hierarchy -check; stat -top TOP; tee -q -o <run>.stat.json stat -top
     TOP -json"`, from that work directory, under a NAMED allocator, and
     records wall/user/system time and peak RSS (GNU time's `%e %U %S %M`, or
     wait4's rusage when /usr/bin/time is absent), the `-d` per-pass "Time
     spent" table, the `stat -json` cell and wire counts and, with `--rtlil`,
     the sha256 of a `write_rtlil` netlist for the invariance oracle.
  3. REFUSES to publish a number for a run that proved nothing. A non-zero
     exit, an `ERROR:` line, a log with no TOP-LEVEL `hierarchy` pass after
     `synth` or no `End of script.`, no per-pass table, or no readable design
     count is a record marked FAILED whose timing fields are null.

ALLOCATORS are resolved the way syn/yosys/malloc.sh resolves them: the library
is looked up on the loader's own path (`ldconfig -p`, then the same literal
fallbacks) and handed to malloc.sh's `select_malloc`, so an absent or
non-loadable library is REFUSED rather than measured as glibc under another
name. `glibc` means LD_PRELOAD actively unset for the child.

TRIALS AND BATCHES. `--trials N` repeats every cell N times (>= 3 for a
published figure). `--batch` starts all the allocator variants of one top at
once, so they share the machine's conditions, and every record states the
concurrency it ran at: a lone run and a batched run are different numbers.

Usage:

    python3 syn/yosys/bench/yosys_bench.py --top KL_crf_rx --trials 3 --batch
    python3 syn/yosys/bench/yosys_bench.py --top KL_crf_rx --alloc glibc,jemalloc --rtlil
    python3 syn/yosys/bench/yosys_bench.py --top KL_crf_rx --stage-only
    python3 syn/yosys/bench/yosys_bench.py --report [--markdown FILE]
    python3 syn/yosys/bench/yosys_bench.py --selftest

Records are one JSON file per trial under `<out>/records/` (default
`syn/yosys/bench/out/`, which is gitignored); `--report` aggregates them into
a Markdown table of median, min and max per cell, headed by the machine, the
tool versions, the trial count and the concurrency. Exit 0 = every run
measured; 1 = at least one run FAILED (its record says why); 2 = a refusal
before anything was measured.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import time
from collections.abc import Callable, Iterable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import BinaryIO

HERE = Path(__file__).resolve().parent
YOSYS_DIR = HERE.parent
REPO = YOSYS_DIR.parent.parent
RUN_SH = YOSYS_DIR / "run.sh"
MALLOC_SH = YOSYS_DIR / "malloc.sh"
SELFTEST = HERE / "bench_selftest.py"
DEFAULT_OUT = HERE / "out"
SCHEMA = 1
GLIBC = "glibc"
DEFAULT_ALLOCS = "glibc,jemalloc,mimalloc,tcmalloc"
#: variant name -> sonames looked up on the loader's path, preferred first.
SONAMES = {
    "jemalloc": ("libjemalloc.so.2",),
    "mimalloc": ("libmimalloc.so.3", "libmimalloc.so.2"),
    "tcmalloc": ("libtcmalloc.so.4",),
}
#: malloc.sh's literal fallback for a machine whose ldconfig a normal user
#: cannot run, plus Debian's multiarch directory for a hosted runner.
LITERAL_DIRS = ("/usr/lib", "/usr/lib64", "/usr/local/lib")
#: package names to ask the package manager about, pacman first, dpkg second.
PACKAGES = {
    "jemalloc": ("jemalloc", "libjemalloc2"),
    "mimalloc": ("mimalloc", "libmimalloc3", "libmimalloc2.0"),
    "tcmalloc": ("gperftools", "libgoogle-perftools4", "libtcmalloc-minimal4"),
}
#: the ROM images run.sh generates into yosys's working directory, because a
#: relative `$readmemh` resolves against it; generator paths from the root.
ROM_GENERATORS = (
    ("protocol-processor/hdl/acmp/rom/gen_ltn_rom.py", "ltn_rom.hex"),
    ("protocol-processor/hdl/aecp/ucode/gen_ucode.py", "ucode.hex"),
    ("gptp-processor/hdl/ucode/gen_gptp_ucode.py", "gptp_ucode.hex"),
)
TIME_BIN = Path("/usr/bin/time")
TIME_FORMAT = "%e %U %S %M"
END_OF_SCRIPT = "End of script."
TIME_SPENT = "Time spent:"
PASS_ROW_RE = re.compile(r"^\s*(\d+)%\s+(\d+) calls\s+(\d+\.\d+) sec (\S+)\s*$")
#: a TOP-LEVEL log header - `3. Executing HIERARCHY pass ...` or `4. Printing
#: statistics.`; a nested `2.1. Executing HIERARCHY pass` is synth's own.
TOP_HEADER_RE = re.compile(r"^(\d+)\. (?:Executing (\S+) pass|(Printing statistics))")
ERROR_RE = re.compile(r"ERROR:.*")
#: stands for the per-run file stem in a record's `program_shape`, so runs of
#: one cell compare equal however many trials and batches produced them.
RUN_TOKEN = "<run>"
PUBLISHABLE_TRIALS = 3


class BenchRefusal(Exception):
    """A condition under which no number may be produced, with its reason."""


# --- records ---------------------------------------------------------------

@dataclass(frozen=True)
class EmitRecord:
    """One top's inventory record as `run.sh --emit` prints it."""
    top: str
    defines: tuple[str, ...]
    incdirs: tuple[str, ...]
    srcs: tuple[str, ...]


@dataclass(frozen=True)
class Staged:
    """One top lowered by sv2v into the work directory, with its input digest."""
    top: str
    workdir: Path
    digest: str
    nbytes: int
    sv2v_s: float
    sv2v_argv: tuple[str, ...]


@dataclass(frozen=True)
class Variant:
    """A named allocator: `lib` is the absolute preload, None for glibc."""
    name: str
    lib: str | None
    package: str


@dataclass(frozen=True)
class Measure:
    """What GNU time (or wait4) reports for one child."""
    wall_s: float
    user_s: float
    sys_s: float
    max_rss_kib: int


@dataclass(frozen=True)
class PassTime:
    """One row of yosys -d's end-of-log "Time spent" table."""
    name: str
    percent: int
    calls: int
    seconds: float


@dataclass(frozen=True)
class Verdict:
    """Whether a run may publish a number and, if not, the first reason why."""
    ok: bool
    reason: str


@dataclass(frozen=True)
class Context:
    """The machine and the tool versions every record of one session carries."""
    machine: dict[str, object]
    tools: dict[str, str]


@dataclass(frozen=True)
class RunSpec:
    """One trial of one variant on one staged top."""
    staged: Staged
    variant: Variant
    trial: int
    batch_id: str
    concurrency: int
    rtlil: bool
    synth: str

    @property
    def stem(self) -> str:
        """The per-run file stem: `<variant>.<batch>.t<trial>` in the work dir."""
        return f"{self.variant.name}.{self.batch_id}.t{self.trial}"


@dataclass(frozen=True)
class Launch:
    """Everything needed to start one measured yosys child."""
    argv: tuple[str, ...]
    cwd: Path
    preload: str | None
    log: Path
    time_file: Path


@dataclass
class Running:
    """A started child and what `finish` needs to close it out."""
    launch: Launch
    proc: subprocess.Popen[bytes]
    log_handle: BinaryIO
    started: float
    load1: float


@dataclass(frozen=True)
class Outcome:
    """How one child ended: its exit code and its resource measurement."""
    exit_code: int
    measure: Measure | None
    error: str
    load1: float


@dataclass(frozen=True)
class Options:
    """The command line, validated."""
    tops: tuple[str, ...]
    allocs: tuple[str, ...]
    trials: int
    batch: bool
    rtlil: bool
    out: Path
    stage_only: bool
    synth: str


@dataclass(frozen=True)
class Session:
    """One invocation's resolved state, shared by every run it starts."""
    opts: Options
    variants: tuple[Variant, ...]
    ctx: Context
    yosys: str
    sv2v: str
    batch_id: str


# --- staging ---------------------------------------------------------------

def sha256_of(path: Path) -> str:
    """The hex sha256 of a file, read in chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_emit(text: str) -> EmitRecord:
    """Parse `run.sh --emit` output; only define=/incdir=/src= feed sv2v.

    `derived=` names the generated half of the source list for a consumer that
    wants to assert it survived; it is already contained in `src=`, so it is
    accepted and not used. Any other key is a record shape this harness does
    not know, and guessing at it would be the second source list.
    """
    top = ""
    fields: dict[str, list[str]] = {"define": [], "incdir": [], "src": []}
    for line in text.splitlines():
        key, sep, value = line.partition("=")
        if not sep or not value:
            raise BenchRefusal(f"malformed --emit line: {line!r}")
        if key == "top":
            top = value
        elif key in fields:
            fields[key].append(value)
        elif key != "derived":
            raise BenchRefusal(f"unknown --emit key: {key!r}")
    if not top or not fields["src"]:
        raise BenchRefusal("--emit record names no top or no src= line")
    return EmitRecord(top, tuple(fields["define"]), tuple(fields["incdir"]), tuple(fields["src"]))


def emit_record(top: str) -> EmitRecord:
    """Ask run.sh for the top's record; its refusal (an unknown top) is ours."""
    proc = subprocess.run([str(RUN_SH), "--emit", top], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise BenchRefusal(f"run.sh --emit {top}: {proc.stderr.strip() or proc.returncode}")
    record = parse_emit(proc.stdout)
    if record.top != top:
        raise BenchRefusal(f"run.sh --emit answered for {record.top!r}, not {top!r}")
    return record


def generate_roms(workdir: Path) -> None:
    """Generate the three ROM images run.sh puts beside yosys, or refuse."""
    for rel, image in ROM_GENERATORS:
        generator = REPO / rel
        if not generator.is_file():
            raise BenchRefusal(f"ROM generator is missing: {generator}")
        out = workdir / image
        proc = subprocess.run([sys.executable, str(generator), "-o", str(out)],
                              capture_output=True, text=True, check=False)
        if proc.returncode != 0 or not out.is_file() or out.stat().st_size == 0:
            raise BenchRefusal(f"ROM generation failed: {rel}: {proc.stderr.strip()[:200]}")


def sv2v_argv(sv2v: str, record: EmitRecord) -> list[str]:
    """sv2v's argument list, word for word what run.sh's `$inc $srcs` expands to."""
    argv = [sv2v, f"--top={record.top}"]
    argv += [f"-D{define}" for define in record.defines]
    for incdir in record.incdirs:
        argv += ["-I", incdir]
    return argv + list(record.srcs)


def stage(top: str, workdir: Path, sv2v: str) -> Staged:
    """Lower one top exactly as the gate does and digest the result."""
    record = emit_record(top)
    workdir.mkdir(parents=True, exist_ok=True)
    generate_roms(workdir)
    argv = sv2v_argv(sv2v, record)
    verilog = workdir / f"{top}.v"
    err_path = workdir / f"{top}.sv2v.err"
    started = time.monotonic()
    with verilog.open("wb") as out, err_path.open("wb") as err:
        proc = subprocess.run(argv, stdout=out, stderr=err, check=False)
    elapsed = time.monotonic() - started
    if proc.returncode != 0:
        first = err_path.read_text(errors="replace").splitlines()[:1]
        raise BenchRefusal(f"sv2v failed on {top}: {first[0] if first else proc.returncode}")
    nbytes = verilog.stat().st_size
    if nbytes == 0:
        raise BenchRefusal(f"sv2v produced an empty {verilog.name}")
    return Staged(top, workdir, sha256_of(verilog), nbytes, round(elapsed, 3), tuple(argv))


# --- allocators ------------------------------------------------------------

def ldconfig_candidates(soname: str) -> list[str]:
    """Existing paths the loader's cache maps `soname` to, then the literal fallbacks."""
    found: list[str] = []
    ldconfig = next((p for p in ("ldconfig", "/usr/sbin/ldconfig", "/sbin/ldconfig") if shutil.which(p)), None)
    if ldconfig:
        proc = subprocess.run([ldconfig, "-p"], capture_output=True, text=True, check=False)
        for line in proc.stdout.splitlines():
            name, sep, path = line.strip().partition(" => ")
            if sep and name.split(" ")[0] == soname:
                found.append(path.strip())
    found += [str(Path(directory) / soname) for directory in LITERAL_DIRS]
    return [p for p in dict.fromkeys(found) if Path(p).exists()]


def select_malloc(request: str) -> str:
    """Run malloc.sh's own `select_malloc` on `request` (a path, or `none`).

    The answer is the absolute library, or "" for the system allocator. A
    refusal - absent, unresolvable, or a file the loader will not preload - is
    malloc.sh's own message, raised: the same rule the gate applies.
    """
    env = dict(os.environ, YOSYS_MALLOC=request)
    proc = subprocess.run(["bash", "-c", '. "$1" && select_malloc', "select_malloc", str(MALLOC_SH)],
                          env=env, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise BenchRefusal(proc.stderr.strip() or f"malloc.sh refused {request!r}")
    return proc.stdout.strip()


def package_version(name: str, lib: str) -> str:
    """The allocator's package and version, with the real file the soname resolves to."""
    real = str(Path(lib).resolve())
    for pkg in PACKAGES.get(name, ()):
        for argv in (["pacman", "-Q", pkg], ["dpkg-query", "-W", "-f=${Package} ${Version}", pkg]):
            if not shutil.which(argv[0]):
                continue
            proc = subprocess.run(argv, capture_output=True, text=True, check=False)
            if proc.returncode == 0 and proc.stdout.strip():
                return f"{proc.stdout.strip()} ({real})"
    return f"unpackaged ({real})"


def resolve_variant(spec: str) -> Variant:
    """`glibc`, a known name (jemalloc, mimalloc, tcmalloc), or `name=/path/to/lib.so`."""
    name, sep, explicit = spec.partition("=")
    if not name:
        raise BenchRefusal(f"empty allocator name in {spec!r}")
    if name == GLIBC:
        if sep:
            raise BenchRefusal("glibc names the system allocator and takes no library")
        if select_malloc("none"):
            raise BenchRefusal("malloc.sh selected a library for YOSYS_MALLOC=none")
        return Variant(GLIBC, None, " ".join(platform.libc_ver()))
    if sep:
        candidates = [explicit]
    elif name in SONAMES:
        candidates = [c for soname in SONAMES[name] for c in ldconfig_candidates(soname)]
        if not candidates:
            raise BenchRefusal(f"{name}: no {' or '.join(SONAMES[name])} on the loader's path; "
                               f"install it or pass {name}=/path/to/lib.so")
    else:
        raise BenchRefusal(f"unknown allocator {name!r}: use glibc, {', '.join(SONAMES)} or name=/path/to/lib.so")
    lib = select_malloc(candidates[0])
    if not lib:
        raise BenchRefusal(f"{name}: malloc.sh selected no library for {candidates[0]}")
    return Variant(name, lib, package_version(name, lib))


def child_env(preload: str | None) -> dict[str, str]:
    """The child's environment: LD_PRELOAD set to the library, or actively unset."""
    env = {key: value for key, value in os.environ.items() if key != "LD_PRELOAD"}
    if preload:
        env["LD_PRELOAD"] = preload
    return env


# --- the measured cell -----------------------------------------------------

def program_for(top: str, stem: str, rtlil: bool, synth: str = "synth") -> str:
    """The gate's Yosys program for `top`, spelled for a run from the work directory.

    run.sh issues `read_verilog $TMP/$top.v; $SYNTH -top $top; hierarchy
    -check; stat -top $top; tee -q -o $TMP/$top.stat.json stat -top $top -json`
    with $TMP as its working directory. The same program is issued here with
    the paths relative to that directory, so the `\\src` attributes a
    `write_rtlil` netlist carries do not spell the checkout's location and one
    digest is comparable between two machines. The self-test holds this text
    against run.sh's own line.
    """
    program = (f"read_verilog {top}.v; {synth} -top {top}; hierarchy -check; stat -top {top}; "
               f"tee -q -o {stem}.stat.json stat -top {top} -json")
    if rtlil:
        program += f"; write_rtlil {stem}.il"
    return program


def parse_time_line(text: str) -> Measure:
    """The last line of GNU time's `-o` file in TIME_FORMAT: wall, user, system, max RSS KiB.

    `Command exited with non-zero status N` precedes it on a failed child, so
    the last non-empty line is the one read; anything but four numbers there
    is a measurement that did not happen.
    """
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        raise BenchRefusal("time output is empty")
    fields = lines[-1].split()
    if len(fields) != 4:
        raise BenchRefusal(f"unexpected time line: {lines[-1]!r}")
    try:
        return Measure(float(fields[0]), float(fields[1]), float(fields[2]), int(fields[3]))
    except ValueError as exc:
        raise BenchRefusal(f"unparseable time line: {lines[-1]!r}") from exc


def parse_time_spent(log: str) -> list[PassTime]:
    """Rows of the `Time spent:` table `yosys -d` prints after `End of script.`.

    Without `-d` yosys prints one line (`Time spent: 59% 1x abc (0 sec), ...`)
    and no table; that yields no rows, and the verdict refuses the run rather
    than publish a timing with no breakdown behind it.
    """
    rows: list[PassTime] = []
    lines = log.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == TIME_SPENT]
    if not starts:
        return rows
    for line in lines[starts[-1] + 1:]:
        match = PASS_ROW_RE.match(line)
        if not match:
            break
        rows.append(PassTime(match.group(4), int(match.group(1)), int(match.group(2)), float(match.group(3))))
    return rows


def hierarchy_check_passed(log: str) -> bool:
    """A TOP-LEVEL hierarchy pass ran after synth, and statistics printed after it.

    `synth` runs its own hierarchy pass, numbered `2.1.`; the gate's criterion
    is the separate `hierarchy -check` command, which yosys numbers at the top
    level (`3.`). A log that died inside it has no later `Printing statistics.`
    header, and a log where it was never issued has no top-level HIERARCHY
    header at all. Neither may publish a number.
    """
    synth_no: int | None = None
    hier_no: int | None = None
    for line in log.splitlines():
        match = TOP_HEADER_RE.match(line)
        if not match:
            continue
        number, pass_name = int(match.group(1)), (match.group(2) or "")
        if synth_no is None and pass_name.upper().startswith("SYNTH"):
            synth_no = number
        elif hier_no is None and synth_no is not None and pass_name == "HIERARCHY":
            hier_no = number
        elif match.group(3) and hier_no is not None and number > hier_no:
            return True
    return False


def judge(log: str, exit_code: int, passes: Sequence[PassTime]) -> Verdict:
    """Decide whether a run may publish a number; the first failing rule names why."""
    if exit_code != 0:
        return Verdict(False, f"yosys exited {exit_code}")
    error = ERROR_RE.search(log)
    if error:
        return Verdict(False, error.group(0)[:200])
    if END_OF_SCRIPT not in log:
        return Verdict(False, "log has no 'End of script.'")
    if not hierarchy_check_passed(log):
        return Verdict(False, "no top-level hierarchy -check completed after synth")
    if not passes:
        return Verdict(False, "no per-pass 'Time spent' table (yosys -d)")
    return Verdict(True, "")


def stat_counts(path: Path) -> tuple[int, int]:
    """(cells, wires) from `stat -json`'s design roll-up - the gate's own count - or refuse."""
    try:
        design = json.loads(path.read_text())["design"]
        cells, wires = design["num_cells"], design["num_wires"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise BenchRefusal(f"no design counts in {path.name}: {exc}") from exc
    if not all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in (cells, wires)):
        raise BenchRefusal(f"non-numeric design counts in {path.name}")
    return cells, wires


def start(launch: Launch) -> Running:
    """Start one child, under GNU time when it is installed, log to its file."""
    argv = list(launch.argv)
    if TIME_BIN.is_file():
        argv = [str(TIME_BIN), "-f", TIME_FORMAT, "-o", str(launch.time_file)] + argv
    handle = launch.log.open("wb")
    load1 = os.getloadavg()[0]
    proc = subprocess.Popen(argv, cwd=launch.cwd, env=child_env(launch.preload),
                            stdout=handle, stderr=subprocess.STDOUT)
    return Running(launch, proc, handle, time.monotonic(), load1)


def finish(run: Running) -> Outcome:
    """Wait for one child and collect its exit code and resource measurement."""
    if TIME_BIN.is_file():
        code = run.proc.wait()
        run.log_handle.close()
        try:
            return Outcome(code, parse_time_line(run.launch.time_file.read_text()), "", run.load1)
        except (OSError, BenchRefusal) as exc:
            return Outcome(code, None, str(exc), run.load1)
    _pid, status, usage = os.wait4(run.proc.pid, 0)
    wall = time.monotonic() - run.started
    run.proc.returncode = os.waitstatus_to_exitcode(status)
    run.log_handle.close()
    measure = Measure(round(wall, 2), usage.ru_utime, usage.ru_stime, usage.ru_maxrss)
    return Outcome(run.proc.returncode, measure, "", run.load1)


def evaluate(spec: RunSpec, outcome: Outcome) -> tuple[Verdict, dict[str, object]]:
    """Judge one finished run and gather what an OK record publishes; a refusal publishes nothing."""
    work = spec.staged.workdir
    log_path = work / f"{spec.stem}.yosys.log"
    log = log_path.read_text(errors="replace") if log_path.is_file() else ""
    passes = parse_time_spent(log)
    verdict = judge(log, outcome.exit_code, passes)
    if verdict.ok and outcome.measure is None:
        verdict = Verdict(False, outcome.error or "no resource measurement")
    facts: dict[str, object] = {}
    if not verdict.ok:
        return verdict, facts
    try:
        cells, wires = stat_counts(work / f"{spec.stem}.stat.json")
        facts.update(asdict(outcome.measure), cells=cells, wires=wires, passes=[asdict(p) for p in passes])
        if spec.rtlil:
            netlist = work / f"{spec.stem}.il"
            facts["rtlil"] = {"sha256": sha256_of(netlist), "bytes": netlist.stat().st_size}
    except (BenchRefusal, OSError) as exc:
        return Verdict(False, str(exc)), {}
    return verdict, facts


def build_record(spec: RunSpec, program: str, outcome: Outcome, ctx: Context) -> dict[str, object]:
    """One trial's machine-readable record; a failed run carries null in every number."""
    verdict, facts = evaluate(spec, outcome)
    staged, variant = spec.staged, spec.variant
    rec: dict[str, object] = {
        "schema": SCHEMA, "top": staged.top, "variant": variant.name,
        "alloc_lib": variant.lib, "alloc_package": variant.package,
        "trial": spec.trial, "batch_id": spec.batch_id, "concurrency": spec.concurrency,
        "load1_before": round(outcome.load1, 2),
        "program": program, "program_shape": program_for(staged.top, RUN_TOKEN, spec.rtlil, spec.synth),
        "input": {"sha256": staged.digest, "bytes": staged.nbytes, "sv2v_s": staged.sv2v_s,
                  "sv2v_argv": list(staged.sv2v_argv)},
        "tools": ctx.tools, "machine": ctx.machine,
        "status": "ok" if verdict.ok else "failed", "reason": verdict.reason, "exit_code": outcome.exit_code,
        "wall_s": None, "user_s": None, "sys_s": None, "max_rss_kib": None,
        "cells": None, "wires": None, "passes": [], "rtlil": None,
        "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }
    rec.update(facts)
    return rec


def write_record(out: Path, rec: dict[str, object]) -> Path:
    """Write one trial's JSON atomically under `<out>/records/` and return its path."""
    records = out / "records"
    records.mkdir(parents=True, exist_ok=True)
    path = records / f"{rec['top']}.{rec['variant']}.{rec['batch_id']}.t{rec['trial']}.json"
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    tmp.replace(path)
    return path


def summary_line(rec: dict[str, object]) -> str:
    """One console line per finished run."""
    head = f"  [{'OK  ' if rec['status'] == 'ok' else 'FAIL'}] {rec['top']:<22} {rec['variant']:<10} " \
           f"t{rec['trial']} conc={rec['concurrency']}"
    if rec["status"] != "ok":
        return f"{head} {rec['reason']}"
    cpu = float(rec["user_s"]) + float(rec["sys_s"])
    rss = int(rec["max_rss_kib"]) / 1024
    tail = f" wall={rec['wall_s']}s cpu={cpu:.2f}s rss={rss:.0f}MiB cells={rec['cells']}"
    if rec["rtlil"]:
        tail += f" rtlil={rec['rtlil']['sha256'][:16]}"
    return head + tail


# --- the session -----------------------------------------------------------

def lscpu_fields() -> dict[str, str]:
    """`lscpu`'s `Key: value` lines as a dict; empty when the tool is absent."""
    if shutil.which("lscpu") is None:
        return {}
    proc = subprocess.run(["lscpu"], capture_output=True, text=True, check=False)
    pairs = (line.partition(":") for line in proc.stdout.splitlines() if ":" in line)
    return {key.strip(): value.strip() for key, _, value in pairs}


def machine_facts() -> dict[str, object]:
    """CPU model, vCPU count, virtualisation, RAM and OS release, from `lscpu`,
    `os.sysconf` and `platform`; a missing source reads `unknown`, never a guess."""
    fields = lscpu_fields()
    virt = fields.get("Hypervisor vendor", "").lower() or (
        "none" if fields else "unknown")
    try:
        mem_kib = os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE") // 1024
    except (ValueError, OSError):
        mem_kib = 0
    return {"cpu": fields.get("Model name", "unknown"), "vcpus": os.cpu_count() or 0, "virt": virt,
            "mem_total_kib": mem_kib, "os_release": platform.release()}


def first_line(argv: Sequence[str]) -> str:
    """The first stdout line of a version query, or its failure spelled out."""
    proc = subprocess.run(list(argv), capture_output=True, text=True, check=False)
    lines = (proc.stdout or proc.stderr).splitlines()
    return lines[0].strip() if lines else f"{argv[0]}: no version output (exit {proc.returncode})"


def find_tool(name: str) -> str:
    """Resolve a tool the way run.sh does: `$HOME/.local/bin` first, then PATH."""
    search = f"{Path.home() / '.local' / 'bin'}{os.pathsep}{os.environ.get('PATH', '')}"
    found = shutil.which(name, path=search)
    if not found:
        raise BenchRefusal(f"missing tool: {name} (see syn/yosys/README.md)")
    return found


def batch_id() -> str:
    """A stem unique to this invocation: UTC time plus pid."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-{os.getpid()}"


def plan(session: Session, staged: Staged) -> list[list[RunSpec]]:
    """The runs as waves: every variant at once per trial in batch mode, one run per wave otherwise."""
    conc = len(session.variants) if session.opts.batch else 1
    waves: list[list[RunSpec]] = []
    for trial in range(1, session.opts.trials + 1):
        specs = [RunSpec(staged, v, trial, session.batch_id, conc, session.opts.rtlil, session.opts.synth)
                 for v in session.variants]
        waves += [specs] if session.opts.batch else [[spec] for spec in specs]
    return waves


def launch_for(session: Session, spec: RunSpec) -> tuple[Launch, str]:
    """The child to start for one spec, and the exact program it is handed."""
    program = program_for(spec.staged.top, spec.stem, spec.rtlil, spec.synth)
    work = spec.staged.workdir
    launch = Launch((session.yosys, "-d", "-p", program), work, spec.variant.lib,
                    work / f"{spec.stem}.yosys.log", work / f"{spec.stem}.time")
    return launch, program


def run_wave(session: Session, specs: Sequence[RunSpec]) -> int:
    """Start every spec of the wave at once, finish each, write its record; count the failures."""
    pairs = [launch_for(session, spec) for spec in specs]
    running = [start(launch) for launch, _ in pairs]
    failed = 0
    for spec, (_, program), run in zip(specs, pairs, running):
        rec = build_record(spec, program, finish(run), session.ctx)
        write_record(session.opts.out, rec)
        failed += rec["status"] != "ok"
        print(summary_line(rec), flush=True)
    return failed


def measure_top(session: Session, top: str) -> int:
    """Stage one top and run every (variant, trial) cell on it; return the failed-run count."""
    staged = stage(top, session.opts.out / "work" / top, session.sv2v)
    print(f"staged {top}: {staged.nbytes} bytes, sha256 {staged.digest[:16]}, sv2v {staged.sv2v_s}s", flush=True)
    if session.opts.stage_only:
        return 0
    return sum(run_wave(session, wave) for wave in plan(session, staged))


# --- the report ------------------------------------------------------------

@dataclass(frozen=True)
class Spread:
    """Median with min and max over one cell's OK trials."""
    median: float
    lo: float
    hi: float

    def text(self, digits: int = 1) -> str:
        """`median (min-max)` at the given precision."""
        return f"{self.median:.{digits}f} ({self.lo:.{digits}f}-{self.hi:.{digits}f})"


@dataclass(frozen=True)
class Cell:
    """One (variant, concurrency) cell of a top aggregated over its trials."""
    variant: str
    concurrency: int
    trials: int
    ok: int
    wall: Spread | None
    cpu: Spread | None
    rss_mib: Spread | None
    cells: str
    wires: str
    netlist: str


def spread(values: Sequence[float]) -> Spread:
    """Median, min and max; the caller guarantees at least one value."""
    return Spread(statistics.median(values), min(values), max(values))


def agree(values: Iterable[str]) -> str:
    """One value when every trial agrees, MISMATCH naming them all when not, a dash when none."""
    distinct = sorted(set(values))
    if not distinct:
        return "-"
    return distinct[0] if len(distinct) == 1 else "MISMATCH(" + ", ".join(distinct) + ")"


def summarise(recs: Sequence[dict[str, object]]) -> Cell:
    """Aggregate the records of one cell; no OK trial means no number at all."""
    first = recs[0]
    ok = [r for r in recs if r["status"] == "ok"]
    variant, conc = str(first["variant"]), int(first["concurrency"])
    if not ok:
        return Cell(variant, conc, len(recs), 0, None, None, None, "-", "-", "-")
    wall = spread([float(r["wall_s"]) for r in ok])
    cpu = spread([float(r["user_s"]) + float(r["sys_s"]) for r in ok])
    rss = spread([int(r["max_rss_kib"]) / 1024 for r in ok])
    netlists = [str(r["rtlil"]["sha256"])[:16] for r in ok if r["rtlil"]]
    return Cell(variant, conc, len(recs), len(ok), wall, cpu, rss,
                agree(str(r["cells"]) for r in ok), agree(str(r["wires"]) for r in ok), agree(netlists))


def group_by(recs: Iterable[dict[str, object]], key: Callable[[dict[str, object]], object]) \
        -> dict[object, list[dict[str, object]]]:
    """Records bucketed by `key`, buckets in first-seen order."""
    buckets: dict[object, list[dict[str, object]]] = {}
    for rec in recs:
        buckets.setdefault(key(rec), []).append(rec)
    return buckets


def load_records(out: Path) -> list[dict[str, object]]:
    """Every record under `<out>/records/`, refusing an unreadable or foreign-schema one."""
    recs: list[dict[str, object]] = []
    for path in sorted((out / "records").glob("*.json")):
        try:
            rec = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise BenchRefusal(f"unreadable record {path}: {exc}") from exc
        if rec.get("schema") != SCHEMA:
            raise BenchRefusal(f"{path.name}: schema {rec.get('schema')!r} is not {SCHEMA}")
        recs.append(rec)
    if not recs:
        raise BenchRefusal(f"no records under {out / 'records'}")
    return recs


def context_lines(recs: Sequence[dict[str, object]]) -> list[str]:
    """The machine, tools and allocator packages one set of records was taken with."""
    machine = recs[0]["machine"]
    tools = recs[0]["tools"]
    gib = int(machine["mem_total_kib"]) / (1024 * 1024)
    lines = ["## Machine and tools", "",
             f"- machine: {machine['cpu']}, {machine['vcpus']} vCPU, virt={machine['virt']}, "
             f"{gib:.1f} GiB RAM, OS release {machine.get('os_release', 'unknown')}"]
    lines += [f"- {name}: {version}" for name, version in tools.items()]
    packages = {str(r["variant"]): str(r["alloc_package"]) for r in recs}
    lines += [f"- {name}: {pkg}" for name, pkg in packages.items() if name != GLIBC]
    ok = sum(1 for r in recs if r["status"] == "ok")
    lines += [f"- records: {len(recs)} ({ok} ok, {len(recs) - ok} failed); "
              f"a `*` marks a cell below {PUBLISHABLE_TRIALS} trials", ""]
    return lines


def cell_row(cell: Cell, baseline: Cell | None) -> str:
    """One Markdown table row; `baseline` is the glibc cell at the same concurrency, when any."""
    star = "*" if cell.ok < PUBLISHABLE_TRIALS else ""
    if cell.wall is None or cell.cpu is None or cell.rss_mib is None:
        return (f"| {cell.variant} | {cell.ok}/{cell.trials}{star} | {cell.concurrency} | failed "
                "| - | - | - | - | - | - |")
    versus = "-"
    if baseline is not None and baseline.wall is not None and baseline is not cell:
        versus = f"{(cell.wall.median / baseline.wall.median - 1) * 100:+.1f}%"
    return (f"| {cell.variant} | {cell.ok}/{cell.trials}{star} | {cell.concurrency} | {cell.wall.text(2)} | "
            f"{cell.cpu.text(2)} | {cell.rss_mib.text(0)} | {versus} | {cell.cells} | {cell.wires} | {cell.netlist} |")


def group_lines(top: str, digest: str, shape: str, recs: Sequence[dict[str, object]]) -> list[str]:
    """One top's section: its input digest, its program, and one row per cell."""
    cells = [summarise(bucket) for bucket in group_by(recs, lambda r: (r["variant"], r["concurrency"])).values()]
    cells.sort(key=lambda c: (c.variant != GLIBC, c.concurrency))
    baselines = {c.concurrency: c for c in cells if c.variant == GLIBC}
    lines = [f"## {top}", "", f"- input sha256: `{digest}`", f"- program: `{shape}`",
             f"- sv2v: {recs[0]['input']['sv2v_s']} s, {recs[0]['input']['bytes']} bytes", "",
             "| variant | trials ok/run | concurrency | wall s median (min-max) | CPU s median (min-max) | "
             "peak RSS MiB median (min-max) | vs glibc | cells | wires | rtlil sha256[:16] |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    lines += [cell_row(cell, baselines.get(cell.concurrency)) for cell in cells]
    return lines + [""]


def render_report(recs: Sequence[dict[str, object]]) -> str:
    """The Markdown report over a set of records, one section per machine/tool context."""
    lines = ["# Yosys single-process bench", ""]
    contexts = group_by(recs, lambda r: json.dumps([r["machine"], r["tools"]], sort_keys=True))
    if len(contexts) > 1:
        lines += [f"WARNING: {len(contexts)} distinct machine/tool contexts; each is reported on its own "
                  "and their numbers are not comparable.", ""]
    for ctx_recs in contexts.values():
        lines += context_lines(ctx_recs)
        groups = group_by(ctx_recs, lambda r: (r["top"], r["input"]["sha256"], r["program_shape"]))
        for (top, digest, shape), group_recs in groups.items():
            lines += group_lines(str(top), str(digest), str(shape), group_recs)
    return "\n".join(lines).rstrip("\n") + "\n"


# --- the command line ------------------------------------------------------

def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """The command line; `--top` measures, `--report` aggregates, `--selftest` proves the parsers."""
    parser = argparse.ArgumentParser(description="Measure one Yosys process on one top of the portability gate.")
    parser.add_argument("--top", action="append", default=None, help="top to stage and measure; may be repeated")
    parser.add_argument("--alloc", default=DEFAULT_ALLOCS,
                        help="comma list of glibc, jemalloc, mimalloc, tcmalloc or name=/path/to/lib.so "
                             f"(default {DEFAULT_ALLOCS})")
    parser.add_argument("--trials", type=int, default=1, help=f"trials per cell (>= {PUBLISHABLE_TRIALS} to publish)")
    parser.add_argument("--batch", action="store_true", help="run all variants of a top at once, as one matched batch")
    parser.add_argument("--rtlil", action="store_true", help="append write_rtlil and record the netlist's sha256")
    parser.add_argument("--stage-only", action="store_true", help="stage and digest the top; run nothing")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output directory (default {DEFAULT_OUT})")
    parser.add_argument("--report", action="store_true", help="aggregate <out>/records into a Markdown report")
    parser.add_argument("--markdown", type=Path, default=None, help="with --report: also write the report here")
    parser.add_argument("--selftest", action="store_true", help="run the fixture arms and exit")
    return parser.parse_args(argv)


def options_from(args: argparse.Namespace) -> Options:
    """Validate the measuring half of the command line."""
    tops = tuple(args.top or ())
    if not tops:
        raise BenchRefusal("--top is required (or --report / --selftest)")
    if args.trials < 1:
        raise BenchRefusal("--trials must be at least 1")
    allocs = tuple(spec.strip() for spec in str(args.alloc).split(",") if spec.strip())
    if not allocs:
        raise BenchRefusal("--alloc names no allocator")
    names = [spec.partition("=")[0] for spec in allocs]
    if len(set(names)) != len(names):
        raise BenchRefusal(f"--alloc repeats a variant name: {args.alloc}")
    return Options(tops, allocs, args.trials, args.batch, args.rtlil, args.out.resolve(), args.stage_only,
                   os.environ.get("YOSYS_SYNTH", "synth"))


def measure_main(args: argparse.Namespace) -> int:
    """Resolve tools and allocators once, then stage and measure every requested top."""
    opts = options_from(args)
    sv2v, yosys = find_tool("sv2v"), find_tool("yosys")
    variants = tuple(resolve_variant(spec) for spec in opts.allocs)
    session = Session(opts, variants, Context(machine_facts(), tool_versions(yosys, sv2v)), yosys, sv2v, batch_id())
    mode = f"batch of {len(variants)}" if opts.batch else "sequential"
    print(f"== yosys single-process bench: {mode}, {opts.trials} trial(s), batch {session.batch_id} ==")
    for name, version in session.ctx.tools.items():
        print(f"   {name}: {version}")
    for variant in variants:
        print(f"   allocator {variant.name}: {variant.lib or 'LD_PRELOAD unset'} ({variant.package})")
    failed = sum(measure_top(session, top) for top in opts.tops)
    print(f"records: {opts.out / 'records'}   failed runs: {failed}")
    return 1 if failed else 0


def tool_versions(yosys: str, sv2v: str) -> dict[str, str]:
    """`yosys -V`, `sv2v --version` and the C library, as the records state them."""
    return {"yosys": first_line([yosys, "-V"]), "sv2v": first_line([sv2v, "--version"]),
            "libc": " ".join(platform.libc_ver())}


def report_main(args: argparse.Namespace) -> int:
    """Render the report over `<out>/records/` to stdout and, when asked, to a file."""
    text = render_report(load_records(args.out.resolve()))
    sys.stdout.write(text)
    if args.markdown is not None:
        args.markdown.write_text(text)
        print(f"(written to {args.markdown})", file=sys.stderr)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point: dispatch to the self-test, the report, or a measuring session."""
    args = parse_args(argv)
    if args.selftest:
        return subprocess.run([sys.executable, str(SELFTEST)], check=False).returncode
    try:
        return report_main(args) if args.report else measure_main(args)
    except BenchRefusal as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
