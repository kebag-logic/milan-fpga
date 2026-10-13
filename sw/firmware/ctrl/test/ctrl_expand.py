# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_expand.py - the compiler's own expansion of a recorded invocation, and how its report reads (#697).

THE EXPANSION. Before it records, the recorder (ctrl_shim.RECORDER) runs the
real compiler with the invocation's own arguments, in its directory and
environment, as a preprocessing of empty translation units: each argument it
takes for an input (a source or a linker input) is replaced, in its place, by
an empty file of the same suffix (<capture>/expand/in/<n><suffix>, standard
input by an empty one), the output and dependency options (-o, -M and its
kind, -P and the -d letters) are dropped, and -E -dD -v -fpch-preprocess are
added. Every other argument is the compiler's to read: a response file,
-Wp, -Xpreprocessor, a long option, a file read first. A compile whose output
is a precompiled header (.gch, as GCC finds one) is expanded over its real
inputs, which the compiles that read the header first read.

THE REPORT says what the compiler made of them: the -dD line markers say which
file each translation unit is, where each definition came from (the driver's
built-ins, the command line, a file read first) and which files it read, and
-v the directories it searches; GCC's -fpch-preprocess pragma names a
precompiled header it read first. The same driver run with no argument (the
baseline) says what is the implementation's own. Both are kept under the
capture's text/ (expand_main, the helper the recorder runs on a miss). A
report in which the compiler failed, printed fewer translation units than it
ran (its output went where an argument the recorder did not see says), ran a
translation unit that is no stand-in (an input a response file names), or
read a stand-in as an option's value, is no expansion: the reader refuses it
by name (refusal).

Clang makes an argument -E leaves unused an error under a builder's -Werror:
for a driver whose baseline defines __clang__, -Qunused-arguments is added,
and the entry says so ("driver clang"), for the recorder's dependency pass.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

#: A line marker of a preprocessing: its file as printed (escaped) and its flags.
MARKER = re.compile(r'^# \d+ "((?:[^"\\]|\\.)*)"((?: \d+)*)$')
#: A definition -dD prints: its macro, a function-like macro's parameters, its replacement list.
DEFINE = re.compile(r"^#define ([A-Za-z_]\w*)(\([^)]*\))?(?:[ \t](.*))?$")
#: A removal -dD prints.
UNDEF = re.compile(r"^#undef ([A-Za-z_]\w*)\s*$")
#: Where GCC read a precompiled header, under -fpch-preprocess.
PCH = re.compile(r'^#pragma GCC pch_preprocess "((?:[^"\\]|\\.)*)"$')
#: The pseudo-files a preprocessing's line markers name: the driver's built-ins and the command line.
BUILTIN, COMMAND_LINE = "<built-in>", ("<command-line>", "<command line>")
#: The file standard input is read as.
STDIN = "<stdin>"
#: Where -v lists the directories searched, and the directories it names as left out.
QUOTE, BRACKET, END = '#include "..." search starts here:', "#include <...> search starts here:", "End of search list."
LEFT_OUT = re.compile(r'^ignoring (nonexistent|duplicate) directory "(.*)"$')
#: A preprocessing run of the compiler proper that -v reports (GCC's cc1, Clang's -cc1), one per translation unit.
RUN = re.compile(r'^ (?:\S*/cc1\w*|"[^"]*" -cc1) .*?(?<= )-E(?: |$)')
NOT_A_DIRECTORY = re.compile(r"^\S+: warning: (.*): not a directory$")
#: The suffix the baseline's empty translation unit takes, by language.
BASE_SUFFIX = {"c": ".c", "c++": ".cpp", "assembler": ".S"}


@dataclass(frozen=True)
class Unit:
    """One translation unit of a preprocessing: its main file as the compiler printed it, its language (from the
    driver's own built-ins: c, c++ or assembler), the built-in definitions (name, parameters, replacement), every
    definition or removal after them in order with the file it came from (a removal's replacement is None),
    every file it entered, and every precompiled header it read first (GCC's -fpch-preprocess pragma), as
    printed."""

    main: str
    language: str
    builtins: tuple[tuple[str, str, str], ...]
    ops: tuple[tuple[str, str, str, str | None], ...]
    entered: tuple[str, ...]
    pch: tuple[str, ...] = ()


@dataclass(frozen=True)
class Report:
    """What a preprocessing's output and messages say: its translation units, the directories searched for a
    quoted and for a bracketed name, those it left out as nonexistent, the paths it warned are no directory,
    whether it printed a definition outside any translation unit (its line markers suppressed), and how many
    preprocessing runs of the compiler proper -v reports."""

    units: tuple[Unit, ...]
    quote: tuple[str, ...]
    bracket: tuple[str, ...]
    absent: tuple[str, ...]
    notdir: tuple[str, ...]
    unmarked: bool
    runs: int


def unescaped(text: str) -> str:
    """A path as a line marker escapes it, plain."""
    return re.sub(r"\\(.)", r"\1", text)


def units_of(out: str) -> tuple[tuple[Unit, ...], bool]:
    """The translation units of a preprocessing's -dD output, and whether a definition fell outside any."""
    found: list[dict] = []
    current = ""
    unmarked = False
    for line in out.splitlines():
        if (m := MARKER.match(line)) is not None:
            path, flags = unescaped(m[1]), m[2].split()
            unit = found[-1] if found else None
            if path.endswith("//"):
                continue  # the working directory a debug build records (-fworking-directory): no file
            if path == BUILTIN or path in COMMAND_LINE:
                current = path
            elif "1" in flags and unit is not None:
                unit["entered"].append(path)
                current = path
            elif unit is not None and (path == unit["main"] or path in unit["entered"]):
                current = path
            else:
                found.append({"main": path, "builtins": [], "ops": [], "entered": [], "pch": []})
                current = path
            continue
        if (m := PCH.match(line)) is not None and found:
            found[-1]["pch"].append(unescaped(m[1]))
            continue
        m = DEFINE.match(line) or UNDEF.match(line)
        if m is None:
            continue
        if not found:
            unmarked = True
            continue
        params, value = (m[2] or "", m[3] or "") if m.re is DEFINE else ("", None)
        if current == BUILTIN:
            found[-1]["builtins"].append((m[1], params, value))
        else:
            found[-1]["ops"].append((current, m[1], params, value))
    units = []
    for unit in found:
        names = {name for name, _, _ in unit["builtins"]}
        language = "c++" if "__cplusplus" in names else "assembler" if "__ASSEMBLER__" in names else "c"
        units.append(Unit(unit["main"], language, tuple(unit["builtins"]), tuple(unit["ops"]),
                          tuple(dict.fromkeys(unit["entered"])), tuple(unit["pch"])))
    return tuple(units), unmarked


def read(out: str, err: str) -> Report:
    """A preprocessing's report: its units from its -dD output, the directories from its -v messages."""
    units, unmarked = units_of(out)
    lists: dict[str, list[str]] = {"quote": [], "bracket": []}
    absent, notdir = [], []
    into, runs = None, 0
    for line in err.splitlines():
        runs += bool(RUN.match(line))
        if line.startswith(QUOTE):
            into = "quote"
        elif line.startswith(BRACKET):
            into = "bracket"
        elif line.startswith(END):
            into = None
        elif into is not None and line.startswith(" "):
            lists[into].append(line.strip().removesuffix(" (framework directory)"))
        elif (m := LEFT_OUT.match(line)) is not None and m[1] == "nonexistent":
            absent.append(m[2])
        elif (m := NOT_A_DIRECTORY.match(line)) is not None:
            notdir.append(m[1])
    return Report(units, tuple(dict.fromkeys(lists["quote"])), tuple(dict.fromkeys(lists["bracket"])),
                  tuple(dict.fromkeys(absent)), tuple(dict.fromkeys(notdir)), unmarked, runs)


def refusal(report: dict, seen: Report) -> str:
    """Why an expansion's report is no expansion of its invocation, or "": the compiler failed, a definition came
    without line markers, the compiler preprocessed more translation units than it printed (its output went to a
    file an argument the recorder did not see names, as a response file's -o), a translation unit is no stand-in
    (an input the recorder did not see, as a response file names one), or a stand-in was read as an option's
    value (a file entered or a directory)."""
    stand_in, real = report["placeholders"], set(report.get("inputs", {}).values())
    if report["rc"]:
        tail = " ".join(report["err"].strip().splitlines()[-2:])[-300:]
        return f"the compiler's own expansion of it failed (exit {report['rc']}: {tail})"
    if seen.unmarked:
        return "the compiler's own expansion of it printed definitions without line markers"
    if len(seen.units) < seen.runs:
        return f"the compiler preprocessed {seen.runs} translation unit(s) and printed {len(seen.units)}: its " \
               "expansion went to an output the recorder did not see (a response file's)"
    for unit in seen.units:
        if unit.main != STDIN and not unit.main.startswith(stand_in) and unit.main not in real:
            return f"the compiler's own expansion of it compiles {unit.main}, an input it names where the " \
                   "recorder did not see it (a response file's)"
        if any(path.startswith(stand_in) for path in unit.entered):
            return "the compiler read a stand-in of an input as a file: an argument the recorder took for an " \
                   "input is an option's value"
    if any(d.startswith(stand_in) for d in (*seen.quote, *seen.bracket, *seen.absent, *seen.notdir)):
        return "the compiler read a stand-in of an input as a directory: an argument the recorder took for an " \
               "input is an option's value"
    return ""


# ---- the helper the recorder runs (on a cache miss) --------------------------------------------


def keep(capture: Path, text: str) -> str:
    """A text kept under the capture's text/ by its SHA-256, written once; its digest."""
    data = text.encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    path = capture / "text" / digest
    if not path.is_file():
        part = path.with_name(f"{digest}.{os.getpid()}")
        part.write_bytes(data)
        part.replace(path)
    return digest


def installed(where: Path, cwd: Path) -> bool:
    """Whether a file is an installed tool's own: outside the checkout, the temporary directory and the compile's,
    and its inode changed before the capture began (CTRL_CAPTURE_START), so a file a builder writes or copies
    anywhere is the builder's."""
    tops = [Path(os.environ.get("TMPDIR") or "/tmp").resolve(), cwd.resolve()]
    tops += [Path(os.environ["CTRL_CAPTURE_ROOT"]).resolve()] if os.environ.get("CTRL_CAPTURE_ROOT") else []
    start = os.environ.get("CTRL_CAPTURE_START", "")
    if any(where.is_relative_to(top) for top in tops) or not start or not Path(start).is_file():
        return False
    return where.stat().st_ctime_ns < Path(start).stat().st_ctime_ns


def files(printed: list[str], cwd: Path) -> dict[str, list]:
    """Files a preprocessing printed, each resolved, with its digest and whether it is an installed tool's."""
    found = {}
    for name in printed:
        where = (cwd / name).resolve()
        if where.is_file():
            found[name] = [str(where), hashlib.sha256(where.read_bytes()).hexdigest(), installed(where, cwd)]
    return found


def preprocess(argv: list[str], cwd: Path, env: dict[str, str], stand_in: Path, inputs: dict[str, str]) -> dict:
    """One expansion run: its report as kept, every file it entered and every real input it read (a precompiled
    header's maker's) resolved, with its digest, and every precompiled header it read first, resolved."""
    res = subprocess.run(argv, cwd=cwd, env={**env, "LC_ALL": "C"}, stdin=subprocess.DEVNULL, capture_output=True,
                         check=False)
    out, err = res.stdout.decode("utf-8", "replace"), res.stderr.decode("utf-8", "replace")
    units = read(out, err).units
    return {"argv": argv, "cwd": str(cwd), "rc": res.returncode, "out": out, "err": err,
            "placeholders": f"{stand_in}/", "inputs": inputs,
            "entered": files([name for unit in units for name in unit.entered], cwd),
            "mains": files([unit.main for unit in units if unit.main in inputs.values()], cwd),
            "pch": {name: str((cwd / name).resolve()) for unit in units for name in unit.pch}}


def baseline(capture: Path, real: str, language: str) -> str:
    """The digest of the same driver's expansion with no argument, in this language and a plain environment:
    what the implementation predefines, reads and searches on its own. Made once per compiler and language."""
    st = Path(real).stat()
    key = hashlib.sha256(f"{real}\0{st.st_dev}\0{st.st_ino}\0{st.st_size}\0{st.st_mtime_ns}\0{language}".encode())
    marker = capture / "expand" / f"base-{key.hexdigest()}"
    if marker.is_file():
        return marker.read_text(encoding="utf-8").strip()
    stand_in = capture / "expand" / "in"
    empty = stand_in / f"base{BASE_SUFFIX.get(language, '.c')}"
    # made once, read-only, by whichever helper of the capture comes first: another may be making it at once
    try:
        empty.touch(mode=0o444, exist_ok=False)
    except FileExistsError:
        pass
    env = {"PATH": os.environ.get("PATH", ""), "TMPDIR": os.environ.get("TMPDIR", "/tmp")}
    report = preprocess([real, "-E", "-dD", "-v", str(empty)], capture, env, stand_in, {})
    digest = keep(capture, json.dumps({**report, "stdin": -1, "baseline": {}}, sort_keys=True))
    part = marker.with_name(f"{marker.name}.{os.getpid()}")
    part.write_text(digest + "\n", encoding="utf-8")
    part.replace(marker)
    return digest


def entry(capture: Path, report: dict, digest: str, fresh: bool) -> list[str]:
    """The lines the recorder reads back: the report's digest and status, each input's language by its index, the
    directories searched, and what must still hold for the expansion to be reused (every file it entered, every
    directory it searched, every directory it found absent)."""
    seen = read(report["out"], report["err"])
    cwd = Path(report["cwd"])
    lines = [f"report {digest}", f"rc {report['rc']}"]
    stand_in, real = report["placeholders"], {path: int(k) for k, path in report["inputs"].items()}
    for unit in seen.units:
        index = report["stdin"] if unit.main == STDIN else real[unit.main] if unit.main in real else \
            int(m[0]) if unit.main.startswith(stand_in) and (m := re.match(r"\d+", unit.main[len(stand_in):])) else -1
        if index >= 0:
            lines.append(f"lang {index} {unit.language}")
    for found in (*seen.quote, *seen.bracket):
        lines.append(f"dir {(cwd / found).resolve()}")
    lines += [f"nodir {Path(cwd / gone).absolute()}" for gone in seen.absent]
    for where, _, _ in (*report["entered"].values(), *report["mains"].values()):
        st = Path(where).stat()
        lines.append(f"file {st.st_dev} {st.st_ino} {st.st_size} {st.st_mtime_ns} {st.st_ctime_ns} {where}")
    if fresh or any("\n" in line for line in lines):
        lines = [line.replace("\n", " ") for line in lines] + ["fresh"]
    return lines


def expand_main(argv: list[str]) -> int:
    """The recorder's helper: `expand <capture> <entry> <fresh|reuse> <stdin index> [<index>=<input>]... --
    <compiler> <argument>...` (the inputs the expansion keeps as they are, a precompiled header's maker's). Run
    the expansion and the baseline of each language it holds, keep both reports, and write the entry the recorder
    reads; a failure of its own is written there too, for the reader to refuse by name."""
    capture, target, fresh, stdin = Path(argv[0]), Path(argv[1]), argv[2] == "fresh", int(argv[3])
    split = argv.index("--")
    inputs = dict(word.split("=", 1) for word in argv[4:split])
    command = argv[split + 1:]
    try:
        # Clang makes an argument -E leaves unused (-c, a linker input) an error under a builder's -Werror; its
        # own baseline says it is Clang, and -Qunused-arguments (which GCC refuses) keeps those arguments quiet
        base = json.loads((capture / "text" / baseline(capture, command[0], "c")).read_text(encoding="utf-8"))
        units = read(base["out"], base["err"]).units
        clang = any(name == "__clang__" for unit in units for name, _, _ in unit.builtins)
        if clang:
            command = [*command, "-Qunused-arguments"]
        report = preprocess(command, Path.cwd(), dict(os.environ), capture / "expand" / "in", inputs)
        report["stdin"] = stdin
        languages = sorted({unit.language for unit in read(report["out"], report["err"]).units})
        report["baseline"] = {language: baseline(capture, command[0], language) for language in languages}
        lines = entry(capture, report, keep(capture, json.dumps(report, sort_keys=True)), fresh)
        # the dependency pass adds what the expansion adds for Clang (ctrl_shim, THE DEPENDENCY PASS)
        lines[2:2] = ["driver clang"] if clang else []
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        lines = [f"error the capture's expansion helper failed: {type(exc).__name__}: {exc}".replace("\n", " "),
                 "fresh"]
    part = target.with_name(f"{target.name}.{os.getpid()}")
    part.write_text("\n".join(lines) + "\n", encoding="utf-8")
    part.replace(target)
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] != ["expand"]:
        sys.exit("usage: ctrl_expand.py expand <capture> <entry> <fresh|reuse> <stdin index> [<index>=<input>]... -- "
                 "<compiler> <argument>...")
    sys.exit(expand_main(sys.argv[2:]))
