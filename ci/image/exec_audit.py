#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Observe every program a CI step runs inside the image, and judge each invocation.

This is the execution authority for issue #737. The static inventory derives
which programs the workflows *should* run; this audit records which programs a
step *does* run, by following `execve` with `ptrace`, so a static binary is
observed like any other. Steps run with the container network disabled; a step
that needs the network fails and its exit status is a finding.

Every exec instance is kept with its full argument vector and directory. Each is
judged by what it runs, not by the loaded interpreter binary:

- an interpreter (`bash`, `sh`, `python3`, `perl`, `node`, `tclsh`) is judged by
  its script, its `-m` module, or its inline or streamed program;
- an installer is refused by name, as a program, a script or a module: package
  managers (`apt*`, `dpkg`, `pip*`, `npm`, `npx`, ...), the installing
  subcommands of `gem`, `cargo` and `go`, and an interpreter reading its program
  from a pipe a fetcher writes;
- a program or script inside the image's own directories must be named in
  `exec-audit.json`;
- any other program needs provenance: the output (`-o`) of a build program run
  earlier in the same traced step, or a byte copy of one. A script needs to be
  in the checkout when the step starts, or written during the step.

`--selftest` runs the controls; `--audit SPEC --output RECEIPT` runs a step spec.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ALLOWLIST = HERE / "exec-audit.json"

#: ptrace requests and the options that stop a tracee on exec and on each new
#: child; PTRACE_O_EXITKILL reaps the tree if the tracer dies.
TRACEME, CONT, GETEVENTMSG, SETOPTIONS = 0, 7, 0x4201, 0x4200
O_TRACEFORK, O_TRACEVFORK, O_TRACECLONE, O_TRACEEXEC, O_EXITKILL = 0x2, 0x4, 0x8, 0x10, 0x100000
OPTIONS = O_TRACEFORK | O_TRACEVFORK | O_TRACECLONE | O_TRACEEXEC | O_EXITKILL
EVENT_FORK, EVENT_VFORK, EVENT_CLONE, EVENT_EXEC = 1, 2, 3, 4
WALL = 0x40000000

_libc = ctypes.CDLL(None, use_errno=True)
_libc.ptrace.restype = ctypes.c_long
_libc.ptrace.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p]

#: The image's own program directories: a program or script there must be named.
SYSTEM_ROOTS = ("/usr/", "/bin/", "/sbin/", "/lib/", "/lib64/", "/opt/", "/etc/")
#: A toolchain program carries a `<arch>-<os>-gnu-` prefix; the plain tool is named.
MULTIARCH = re.compile(r"^[a-z0-9_]+-[a-z0-9]+-gnu-")
#: Interpreters, by the options that take a value and the option that names inline text.
SHELLS = {"bash", "sh", "dash"}
PYTHONS = {"python", "python3", "python3.12"}
VALUE_OPTIONS = {"shell": {"-o", "-O", "+O", "+o"}, "python": {"-X", "-W", "--check-hash-based-pycs"},
                 "perl": {"-I", "-M", "-m"}, "node": {"-r", "--require", "--import"}, "tclsh": set()}
INLINE = {"shell": {"-c"}, "python": {"-c"}, "perl": {"-e", "-E"}, "node": {"-e", "--eval", "-p", "--print"},
          "tclsh": set()}
#: Programs whose `-o` operand is a program the step built.
BUILDERS = re.compile(r"^(?:[a-z0-9_]+-[a-z0-9]+-[a-z]+-)?(?:cc|c\+\+|gcc|g\+\+|clang|clang\+\+|ld|ld\.bfd|"
                      r"ld\.gold|collect2)(?:-\d+)?$")
#: Programs that fetch: an interpreter reading its program from their output fetches and executes.
FETCHERS = {"curl", "wget", "fetch", "aria2c"}


def _ptrace(request: int, pid: int, data: int = 0) -> int:
    """Issue one ptrace request; a vanished tracee is not an error for the tracer."""
    return _libc.ptrace(request, pid, None, ctypes.c_void_p(data))


def _record(pid: int, name: str) -> Path:
    """One entry of a traced process's process record."""
    return Path(f"/proc/{pid}/{name}")


def _proc(pid: int, name: str) -> str:
    """Read one link of a traced process's record; a vanished process reads empty."""
    try:
        return os.readlink(_record(pid, name))
    except OSError:
        return ""


def _argv(pid: int) -> list[str]:
    """The exact argument vector of a traced process, read at its exec stop."""
    try:
        raw = _record(pid, "cmdline").read_bytes()
    except OSError:
        return []
    return [part.decode("utf-8", "surrogateescape") for part in raw.split(b"\0")[:-1]]


def trace(argv: list[str], cwd: Path, env: dict[str, str]) -> dict[str, object]:
    """Run one command, following its whole process tree, and keep every exec instance.

    Each instance records the process, the program it loaded, the full
    argument vector, the directory and the stream links an interpreter may read.
    """
    instances: list[dict[str, object]] = []
    pid = os.fork()
    if pid == 0:
        try:
            _ptrace(TRACEME, 0)
            os.chdir(cwd)
            signal.raise_signal(signal.SIGSTOP)
            os.execvpe(argv[0], argv, env)
        except BaseException:  # noqa: BLE001 - the child must never return to the tracer
            os._exit(127)
    os.waitpid(pid, 0)
    _ptrace(SETOPTIONS, pid, OPTIONS)
    _ptrace(CONT, pid)
    alive = {pid}
    exit_status = None
    while alive:
        try:
            waited, status = os.waitpid(-1, WALL)
        except ChildProcessError:
            break
        if os.WIFEXITED(status) or os.WIFSIGNALED(status):
            alive.discard(waited)
            if waited == pid:
                exit_status = os.waitstatus_to_exitcode(status)
            continue
        signal_number, event = os.WSTOPSIG(status), status >> 16
        deliver = 0
        if signal_number == signal.SIGTRAP and event in (EVENT_FORK, EVENT_VFORK, EVENT_CLONE):
            child = ctypes.c_ulong()
            _libc.ptrace(GETEVENTMSG, waited, None, ctypes.addressof(child))
            alive.add(child.value)
        elif signal_number == signal.SIGTRAP and event == EVENT_EXEC:
            words = _argv(waited)
            streams = {str(n): _proc(waited, f"fd/{n}") for n in (0, 1)}
            for word in words:
                if word.startswith("/dev/fd/") and word[8:].isdigit():
                    streams[word[8:]] = _proc(waited, f"fd/{word[8:]}")
            instances.append({"pid": waited, "program": _proc(waited, "exe") or "<gone>", "argv": words,
                              "directory": _proc(waited, "cwd"), "streams": streams})
        elif signal_number not in (signal.SIGTRAP, signal.SIGSTOP, signal.SIGCONT):
            deliver = signal_number  # pass a real signal through, never the trap stops
        _ptrace(CONT, waited, deliver)
    return {"exit_status": 0 if exit_status is None else exit_status, "instances": instances}


def lexical(directory: str, word: str) -> str:
    """Join a word to a directory and fold `.` and `..` textually, as the exec saw the path."""
    parts: list[str] = []
    for part in (word if word.startswith("/") else f"{directory}/{word}").split("/"):
        if part == "..":
            parts = parts[:-1]
        elif part not in ("", "."):
            parts.append(part)
    return "/" + "/".join(parts)


def allowlist() -> dict[str, object]:
    """The reviewed program, script and module allowlists and the installer denylists."""
    return json.loads(ALLOWLIST.read_text())


def interpreter(base: str) -> str | None:
    """The interpreter family of a loaded program, if it is one."""
    if base in SHELLS:
        return "shell"
    if base in PYTHONS:
        return "python"
    return base if base in ("perl", "node", "tclsh") else None


def invocation(instance: dict[str, object]) -> dict[str, str]:
    """What one exec runs: a program, or an interpreter's script, module, inline or streamed program."""
    program = str(instance["program"])
    base = MULTIARCH.sub("", Path(program).name)
    family = interpreter(base)
    words = list(instance["argv"])
    if family is None:
        return {"kind": "program", "name": base, "path": program, "args": words[1:]}
    index = 1
    while index < len(words):
        word = words[index]
        if word in INLINE[family]:
            return {"kind": "inline", "name": base, "path": program}
        if family == "python" and word == "-m" and index + 1 < len(words):
            return {"kind": "module", "name": words[index + 1].split(".")[0], "path": words[index + 1]}
        if family == "python" and word.startswith("-m") and len(word) > 2:
            return {"kind": "module", "name": word[2:].split(".")[0], "path": word[2:]}
        if word in VALUE_OPTIONS[family]:
            index += 2
            continue
        if word == "-" or (family == "shell" and word == "-s"):
            break
        if word.startswith(("-", "+")) and word != "--":
            index += 1
            continue
        if word == "--":
            index += 1
            if index >= len(words):
                break
            word = words[index]
        path = lexical(str(instance["directory"]), word)
        if word.startswith("/dev/fd/"):
            return {"kind": "stream", "name": base, "path": word, "stream": instance["streams"].get(word[8:], "")}
        return {"kind": "script", "name": Path(word).name, "path": path, "args": words[index + 1:]}
    return {"kind": "stream", "name": base, "path": "<stdin>", "stream": instance["streams"].get("0", "")}


def built_output(words: list[str], directory: str) -> str | None:
    """The `-o` operand of a build program, resolved in its directory."""
    for index, word in enumerate(words):
        operand = words[index + 1] if word == "-o" and index + 1 < len(words) else (
            word[2:] if word.startswith("-o") and len(word) > 2 and not word.startswith("-o-") else None)
        if operand:
            return lexical(directory, operand)
    return None


def digest(path: str) -> str | None:
    """Content identity of a program file."""
    try:
        with open(path, "rb") as stream:
            return hashlib.file_digest(stream, "sha256").hexdigest()
    except OSError:
        return None


def judge(result: dict[str, object], names: dict[str, object], root: Path, started: float,
          present: set[str]) -> tuple[list[dict], list[dict]]:
    """Classify every exec instance; return the invocation population and its findings."""
    programs = set(names["programs"])
    scripts = set(names["scripts"])
    modules = set(names["modules"])
    installers = set(names["installers"])
    subcommands = {key: set(value) for key, value in names["installer_subcommands"].items()}
    fetched = {i["streams"].get("1") for i in result["instances"]
               if Path(str(i["program"])).name in FETCHERS and str(i["streams"].get("1", "")).startswith("pipe:")}
    outputs: dict[str, str] = {}
    population: dict[tuple, dict] = {}
    findings = []

    def finding(instance: dict, what: dict, reason: str) -> None:
        """Name one forbidden or unprovenanced invocation."""
        findings.append({"invocation": what["name"], "path": what["path"], "argv": instance["argv"], "reason": reason})

    for instance in result["instances"]:
        what = invocation(instance)
        words = list(instance["argv"])
        base = MULTIARCH.sub("", Path(str(instance["program"])).name)
        provenance = "named"
        if what["kind"] in ("program", "script") and what["name"] in installers:
            finding(instance, what, f"installer executed: {what['name']}")
        elif what["kind"] == "module" and what["name"] in names["installer_modules"]:
            finding(instance, what, f"installer module executed: {what['name']}")
        elif what["kind"] == "stream" and what.get("stream") in fetched:
            finding(instance, what, f"fetched program executed by {what['name']}")
        elif what.get("args") and what["args"][0] in subcommands.get(what["name"], ()):
            finding(instance, what, f"installer subcommand executed: {what['name']} {what['args'][0]}")
        if interpreter(base) and base not in programs:
            finding(instance, what, f"interpreter not in the allowlist: {base}")
        if what["kind"] == "program":
            if what["path"].startswith(SYSTEM_ROOTS):
                if what["name"] not in programs:
                    finding(instance, what, f"system program not in the allowlist: {what['name']}")
            elif what["path"] in outputs:
                provenance = f"built by {outputs[what['path']]}"
            elif (copy := digest(what["path"])) and copy in {digest(p) for p in outputs}:
                provenance = "copy of a program the step built"
            else:
                provenance = "none"
                finding(instance, what, f"program without provenance: {what['name']}")
        elif what["kind"] == "script":
            path = what["path"]
            if path.startswith(SYSTEM_ROOTS):
                if what["name"] not in scripts:
                    finding(instance, what, f"system script not in the allowlist: {what['name']}")
            elif Path(path).is_relative_to(root) and Path(path).relative_to(root).as_posix() in present:
                provenance = "checkout"
            elif Path(path).exists() and Path(path).stat().st_mtime >= started:
                provenance = "written during the step"
            else:
                provenance = "none"
                finding(instance, what, f"script without provenance: {what['name']}")
        elif what["kind"] == "module" and what["name"] not in modules:
            finding(instance, what, f"module not in the allowlist: {what['name']}")
        if BUILDERS.match(base) and (output := built_output(words, str(instance["directory"]))):
            outputs[output] = base
        key = (what["kind"], what["name"], what["path"] if what["kind"] != "program" or
               what["path"].startswith(SYSTEM_ROOTS) else "<built>", provenance)
        population.setdefault(key, {"kind": key[0], "invocation": key[1], "path": key[2], "provenance": key[3],
                                    "count": 0})["count"] += 1
    if result["exit_status"] != 0:
        findings.append({"invocation": "<step>", "path": "", "argv": [],
                         "reason": f"step exited {result['exit_status']} (network disabled)"})
    return sorted(population.values(), key=lambda row: (row["kind"], row["invocation"], row["path"])), findings


def checkout_files(root: Path) -> set[str]:
    """Every file present in the checkout when a step starts."""
    present = set()
    for base, children, files in os.walk(root):
        children[:] = [c for c in children if c != ".git"]
        present.update((Path(base) / f).relative_to(root).as_posix() for f in files)
    return present


def audit_step(entry: dict[str, object], names: dict[str, object], root: Path, environment: dict[str, str],
               log: Path | None = None) -> dict[str, object]:
    """Trace one step, keep its instances, and attach the population and findings."""
    present = checkout_files(root)
    started = time.time() - 1
    directory = root / str(entry.get("working-directory", "."))
    result = trace(list(entry["argv"]), directory, {**environment, **entry.get("env", {})})
    population, findings = judge(result, names, root, started, present)
    lines = "".join(json.dumps(i, sort_keys=True) + "\n" for i in result["instances"]).encode()
    if log is not None:
        log.write_bytes(lines)
    return {"job": entry["job"], "label": entry["label"], "argv": entry["argv"],
            "working-directory": str(entry.get("working-directory", ".")), "exit_status": result["exit_status"],
            "instances": len(result["instances"]), "instances_sha256": hashlib.sha256(lines).hexdigest(),
            "population": population, "findings": findings, "clean": not findings}


def receipt(spec: list[dict[str, object]], names: dict[str, object], root: Path,
            logs: Path | None = None) -> dict[str, object]:
    """Run every step in a spec; return each step's population and findings (the follow-up interface)."""
    environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/root"),
                   "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    steps = []
    for number, entry in enumerate(spec):
        log = logs / f"step-{number:03d}.jsonl" if logs else None
        steps.append(audit_step(entry, names, root, environment, log))
        print(f"{'CLEAN' if steps[-1]['clean'] else 'FINDINGS'}: {entry['job']}: {entry['label']} "
              f"(exit {steps[-1]['exit_status']}, {steps[-1]['instances']} execs)", flush=True)
    return {"steps": steps, "clean": all(step["clean"] for step in steps)}


def selftest(names: dict[str, object]) -> int:
    """Each control is judged as the audit must judge it, by name."""
    import shutil
    import tempfile
    import zipfile
    environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/root"),
                   "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    system = Path("/usr/local/bin")
    with tempfile.TemporaryDirectory(prefix="exec-audit-") as directory:
        base = Path(directory)

        def step(label: str, command: str, expect: str | None) -> dict:
            """Audit one control step and require its expected judgment."""
            report = audit_step({"job": "selftest", "label": label, "argv": ["bash", "-e", "-c", command]},
                                names, base, environment)
            reasons = [f["reason"] for f in report["findings"]]
            if expect is None:
                assert not reasons, (label, reasons, report["population"])
            else:
                assert any(expect in reason for reason in reasons), (label, expect, reasons)
            print(f"PASS: {label}: " + (f"caught ({expect})" if expect else "clean"))
            return report

        (base / "static.c").write_text("int main(void) { return 0; }\n")
        report = step("a static binary the step builds is observed and has provenance",
                      f"gcc -static -o {base}/static {base}/static.c && {base}/static", None)
        assert any(row["provenance"].startswith("built by") for row in report["population"]), report["population"]
        shutil.copy(base / "static", system / "zz_static_probe")
        step("a static binary planted in a system directory", f"{system}/zz_static_probe",
             "system program not in the allowlist: zz_static_probe")
        (system / "zz_static_probe").unlink()
        step("a scripted installer run by name", "pip3 --version", "installer executed: pip3")
        step("a scripted package manager run by name", "npm --version", "installer executed: npm")
        wheel = base / "zz_probe_pkg-0.1-py3-none-any.whl"
        with zipfile.ZipFile(wheel, "w") as archive:
            archive.writestr("zz_probe_pkg/__init__.py", "")
            archive.writestr("zz_probe_pkg-0.1.dist-info/METADATA",
                             "Metadata-Version: 2.1\nName: zz-probe-pkg\nVersion: 0.1\n")
            archive.writestr("zz_probe_pkg-0.1.dist-info/WHEEL",
                             "Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
            archive.writestr("zz_probe_pkg-0.1.dist-info/RECORD", "")
        report = step("a real offline install of a local wheel",
                      f"python3 -m pip install --no-index --no-deps --disable-pip-version-check --target "
                      f"{base}/installed {wheel} && test -f {base}/installed/zz_probe_pkg/__init__.py",
                      "installer module executed: pip")
        (system / "zz_shebang_probe").write_text("#!/bin/sh\nexit 0\n")
        (system / "zz_shebang_probe").chmod(0o755)
        step("an unlisted shebang script in a system directory", "zz_shebang_probe",
             "system script not in the allowlist: zz_shebang_probe")
        (system / "zz_shebang_probe").unlink()
        (base / "bin").mkdir()
        (base / "bin/apt-get").write_text("#!/bin/sh\nexit 0\n")
        (base / "bin/apt-get").chmod(0o755)
        step("a shebang apt-get outside the system directories", f"{base}/bin/apt-get update",
             "installer executed: apt-get")
        shutil.copy("/bin/true", base / "bin/zz_copied_program")
        step("a copied unlisted program", f"{base}/bin/zz_copied_program",
             "program without provenance: zz_copied_program")
        (base / "fetched.sh").write_text("exit 0\n")
        step("a fetched program piped to a shell", f"curl -fsS file://{base}/fetched.sh | sh",
             "fetched program executed by dash")
        (base / "bin/gem").write_text("#!/bin/sh\nexit 0\n")
        (base / "bin/gem").chmod(0o755)
        step("an installing subcommand", f"{base}/bin/gem install zz-probe",
             "installer subcommand executed: gem install")
        (base / "tool.py").write_text("print('ok')\n")
        step("a permitted interpreter call and a step-written script",
             f"python3 -c 'print(1)' && python3 {base}/tool.py", None)
        (base / "built.c").write_text("int main(void) { return 0; }\n")
        step("a program the step built, and an installed copy of it",
             f"cc -o {base}/built {base}/built.c && {base}/built && install -m 755 {base}/built {base}/copy && "
             f"{base}/copy", None)
        step("a step that fails under the disabled network", "exit 7", "step exited 7")
    return 0


def main() -> int:
    """Self-test the audit, or run a step spec and write its receipt."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--audit", type=Path, help="a JSON step spec to run")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="where to write the receipt")
    parser.add_argument("--logs", type=Path, help="where to keep every step's exec instances")
    args = parser.parse_args()
    names = allowlist()
    if args.selftest:
        return selftest(names)
    report = receipt(json.loads(args.audit.read_text()), names, args.root, args.logs)
    text = json.dumps(report, indent=1, sort_keys=True) + "\n"
    (args.output.write_text(text) if args.output else sys.stdout.write(text))
    if not report["clean"]:
        print("REJECTED: an audited step executed a forbidden or unprovenanced invocation", file=sys.stderr)
        return 2
    print(f"PASS: {len(report['steps'])} audited steps executed only allowlisted, provenanced invocations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
