#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Observe every program a CI step runs inside the image, and judge each invocation.

This is the execution authority for issue #737. The static inventory derives
which programs the workflows *should* run; this audit records which programs a
step *does* run. A seccomp filter on the step's process tree turns every `execve`
and `execveat` into a notification the audit reads before letting the call
continue, so a static binary is observed like any other, and no process is
ptraced. Steps run with the container network disabled; a step that needs the
network fails and its exit status is a finding.

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
  earlier in the same traced job, or a byte copy of one. A script needs to be
  in the checkout when the job starts, or written during the job.

`--selftest` runs the controls; `--audit SPEC --output RECEIPT` runs a step spec.
"""

from __future__ import annotations

import argparse
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import select
import socket
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ALLOWLIST = HERE / "exec-audit.json"

#: A seccomp filter turns every `execve` and `execveat` of the step's process tree into a
#: user notification. The audit reads what each call names, then lets it continue. No
#: process is ptraced, so tools that trace themselves, such as LeakSanitizer, still run.
SYS_SECCOMP, PR_SET_NO_NEW_PRIVS = 317, 38
SET_MODE_FILTER, GET_NOTIF_SIZES, FLAG_NEW_LISTENER = 1, 3, 1 << 3
NR_EXECVE, NR_EXECVEAT, ARCH_X86_64 = 59, 322, 0xC000003E
RET_ALLOW, RET_USER_NOTIF, CONTINUE = 0x7FFF0000, 0x7FC00000, 1
NOTIF_RECV, NOTIF_SEND = 0xC0502100, 0xC0182101
AT_FDCWD, AT_EMPTY_PATH = -100, 0x1000
#: Load the arch, allow a foreign one; load the call number; notify on the two exec calls.
FILTER = ((0x20, 0, 0, 4), (0x15, 0, 4, ARCH_X86_64), (0x20, 0, 0, 0), (0x15, 1, 0, NR_EXECVE),
          (0x15, 0, 1, NR_EXECVEAT), (0x06, 0, 0, RET_USER_NOTIF), (0x06, 0, 0, RET_ALLOW))

_libc = ctypes.CDLL(None, use_errno=True)
_libc.syscall.restype = ctypes.c_long

#: The image's own program directories: a program or script there must be named.
SYSTEM_ROOTS = ("/usr/", "/bin/", "/sbin/", "/lib/", "/lib64/", "/opt/", "/etc/")
#: A toolchain program carries an `<arch>-[<vendor>-]<os>-gnu-` prefix, and a cross toolchain's
#: wrapper runs its real binary under a `.br_real` suffix; the plain tool is named.
MULTIARCH = re.compile(r"^[a-z0-9_]+(?:-[a-z0-9]+){1,2}-gnu-|\.br_real$")
SHELLS = {"bash", "sh", "dash"}
PYTHONS = {"python", "python3", "python3.12"}
#: Programs whose `-o` operand is a program the step built.
BUILDERS = re.compile(r"^(?:[a-z0-9_]+-[a-z0-9]+-[a-z]+-)?(?:cc|c\+\+|gcc|g\+\+|clang|clang\+\+|ld|ld\.bfd|"
                      r"ld\.gold|collect2)(?:-\d+)?$")
#: Programs that fetch: an interpreter reading its program from their output fetches and executes.
FETCHERS = {"curl", "wget", "fetch", "aria2c"}


def _record(pid: int, name: str) -> Path:
    """One entry of a traced process's process record."""
    return Path(f"/proc/{pid}/{name}")


def _proc(pid: int, name: str) -> str:
    """Read one link of a traced process's record; a vanished process reads empty."""
    try:
        return os.readlink(_record(pid, name))
    except OSError:
        return ""


class _Filter(ctypes.Structure):
    _fields_ = [("code", ctypes.c_uint16), ("jt", ctypes.c_uint8), ("jf", ctypes.c_uint8), ("k", ctypes.c_uint32)]


class _Program(ctypes.Structure):
    _fields_ = [("len", ctypes.c_uint16), ("filter", ctypes.POINTER(_Filter))]


def _listen() -> int:
    """In the step's first process: install the exec filter and return its notification fd."""
    if _libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0):
        raise OSError(ctypes.get_errno(), "no_new_privs")
    rows = (_Filter * len(FILTER))(*[_Filter(*row) for row in FILTER])
    program = _Program(len(FILTER), rows)
    listener = _libc.syscall(SYS_SECCOMP, SET_MODE_FILTER, FLAG_NEW_LISTENER, ctypes.byref(program))
    if listener < 0:
        raise OSError(ctypes.get_errno(), "seccomp listener")
    return listener


def _memory(pid: int, address: int, size: int) -> bytes:
    """Read a stopped caller's memory; a vanished caller reads empty."""
    try:
        descriptor = os.open(_record(pid, "mem"), os.O_RDONLY)
    except OSError:
        return b""
    try:
        return os.pread(descriptor, size, address)
    except OSError:
        return b""
    finally:
        os.close(descriptor)


def _string(pid: int, address: int) -> str:
    """One NUL-terminated string of the caller."""
    data = b""
    while address and b"\0" not in data and len(data) < 1 << 20:
        chunk = _memory(pid, address + len(data), 4096)
        if not chunk:
            break
        data += chunk
    return data.split(b"\0", 1)[0].decode("utf-8", "surrogateescape")


def _vector(pid: int, address: int) -> list[str]:
    """A NULL-terminated array of string pointers of the caller."""
    words, index = [], 0
    while address and index < 1 << 16:
        raw = _memory(pid, address + 8 * index, 8)
        if len(raw) < 8 or not (pointer := int.from_bytes(raw, "little")):
            break
        words.append(_string(pid, pointer))
        index += 1
    return words


def _executed(pid: int, number: int, arguments: list[int]) -> tuple[str, list[str]] | None:
    """The file an exec call names, resolved in the caller's directory, and its argument vector."""
    if number == NR_EXECVEAT:
        directory, name, vector, flags = arguments[0], _string(pid, arguments[1]), arguments[2], arguments[4]
        directory = ctypes.c_int(directory & 0xFFFFFFFF).value
        if not name and flags & AT_EMPTY_PATH:
            path = _proc(pid, f"fd/{directory}")
        else:
            base = _proc(pid, "cwd") if directory == AT_FDCWD or name.startswith("/") else \
                _proc(pid, f"fd/{directory}")
            path = lexical(base, name)
    else:
        path, vector = lexical(_proc(pid, "cwd"), _string(pid, arguments[0])), arguments[1]
    if not Path(path).is_file() or not os.access(path, os.X_OK):
        return None  # The call fails; a search through PATH tries several such names.
    return path, _vector(pid, vector)


def _loaded(path: str, words: list[str]) -> tuple[str, list[str]]:
    """What runs for an executable file: its interpreter line, with argv built as exec builds it."""
    for _ in range(4):
        try:
            with open(path, "rb") as stream:
                head = stream.read(256)
        except OSError:
            break
        if not head.startswith(b"#!"):
            break
        line = head[2:].split(b"\n", 1)[0].decode("utf-8", "surrogateescape").strip()
        interpreter, _, argument = line.partition(" ")
        words = [interpreter, *([argument.strip()] if argument.strip() else []), path, *words[1:]]
        path = interpreter
    return str(Path(path).resolve()), words


class Origin:
    """Provenance within one traced job: build outputs, job-created scripts and program copies."""

    def __init__(self, root: Path, present: set[str]) -> None:
        self.root, self.present = root, present
        self.started = time.time() - 1
        self.outputs: dict[str, str] = {}
        self.digests: dict[tuple, str | None] = {}

    def digest(self, path: str) -> str | None:
        """Content identity of a program file, cached by its size and modification time."""
        try:
            status = os.stat(path)
        except OSError:
            return None
        key = (path, status.st_size, status.st_mtime_ns)
        if key not in self.digests:
            self.digests[key] = digest(path)
        return self.digests[key]

    def judge(self, instance: dict[str, object]) -> str:
        """Where what this exec runs came from; record a build program's output."""
        what = invocation(instance)
        base = MULTIARCH.sub("", Path(str(instance["program"])).name)
        if BUILDERS.match(base) and (output := built_output(list(instance["argv"]), str(instance["directory"]))):
            self.outputs[output] = base
        path = what["path"]
        if what["kind"] == "script":
            # A script reached through a link is the file the link names.
            path = str(Path(path).resolve())
            instance["script"] = path
        if what["kind"] not in ("program", "script") or path.startswith(SYSTEM_ROOTS):
            return "named"
        if what["kind"] == "program":
            if path in self.outputs:
                return f"built by {self.outputs[path]}"
            own = self.digest(path)
            built = {self.digest(output) for output in self.outputs}
            return "copy of a program the step built" if own and own in built else "none"
        if not Path(path).exists():
            return "absent"  # The interpreter cannot open it, so no code runs from it.
        if Path(path).is_relative_to(self.root) and Path(path).relative_to(self.root).as_posix() in self.present:
            return "checkout"
        try:
            created = os.stat(path).st_ctime >= self.started  # Created or copied during the job.
        except OSError:
            created = False
        return "written during the job" if created else "none"


def trace(argv: list[str], cwd: Path, env: dict[str, str], origin: Origin | None = None) -> dict[str, object]:
    """Run one command and keep every exec instance of its whole process tree.

    Each instance records the process, the file the exec named and the program the
    exec loads for it, the full argument vector as that program receives it, the
    directory and the stream links an interpreter may read. Provenance is judged at
    the exec itself, while the file it runs still exists.
    """
    origin = origin or Origin(cwd, set())
    instances: list[dict[str, object]] = []
    parent, child = socket.socketpair()
    pid = os.fork()
    if pid == 0:
        try:
            parent.close()
            listener = _listen()
            socket.send_fds(child, [b"x"], [listener])
            # The step never holds the descriptor, so it cannot answer its own notifications.
            os.close(listener)
            child.close()
            os.chdir(cwd)
            os.execvpe(argv[0], argv, env)
        except BaseException:  # noqa: BLE001 - the child must never return to the auditor
            os._exit(127)
    child.close()
    _, descriptors, _, _ = socket.recv_fds(parent, 1, 1)
    parent.close()
    if not descriptors:
        os.waitpid(pid, 0)
        raise OSError("the step could not install the exec filter")
    listener = descriptors[0]
    poller = select.poll()
    poller.register(listener, select.POLLIN)
    exit_status, deadline = None, None
    try:
        while True:
            if exit_status is None:
                waited, status = os.waitpid(pid, os.WNOHANG)
                if waited:
                    exit_status = os.waitstatus_to_exitcode(status)
                    deadline = time.monotonic() + 30  # Processes the step left behind may still exec.
            events = poller.poll(100)
            if any(flags & (select.POLLHUP | select.POLLERR) for _, flags in events) and exit_status is not None:
                break
            if deadline is not None and time.monotonic() > deadline:
                break
            if not any(flags & select.POLLIN for _, flags in events):
                continue
            request = bytearray(80)
            try:
                fcntl.ioctl(listener, NOTIF_RECV, request, True)
            except OSError:
                continue  # The caller died before its notification was read.
            serial, caller = int.from_bytes(request[0:8], "little"), int.from_bytes(request[8:12], "little")
            number = int.from_bytes(request[16:20], "little")
            arguments = [int.from_bytes(request[32 + 8 * i:40 + 8 * i], "little") for i in range(6)]
            named = _executed(caller, number, arguments)
            if named is not None:
                program, words = _loaded(*named)
                streams = {str(n): _proc(caller, f"fd/{n}") for n in (0, 1)}
                for word in words:
                    if word.startswith("/dev/fd/") and word[8:].isdigit():
                        streams[word[8:]] = _proc(caller, f"fd/{word[8:]}")
                instance = {"pid": caller, "file": named[0], "program": program, "argv": words,
                            "directory": _proc(caller, "cwd"), "streams": streams}
                instance["provenance"] = origin.judge(instance)
                instances.append(instance)
            response = serial.to_bytes(8, "little") + bytes(12) + CONTINUE.to_bytes(4, "little")
            try:
                fcntl.ioctl(listener, NOTIF_SEND, bytearray(response), True)
            except OSError:
                pass  # The caller died after its notification was read.
    finally:
        os.close(listener)
    if exit_status is None:
        _, status = os.waitpid(pid, 0)
        exit_status = os.waitstatus_to_exitcode(status)
    return {"exit_status": exit_status, "instances": instances}


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


def operands(family: str, words: list[str]) -> tuple[str, str | None, list[str]]:
    """Read an interpreter's options as it does: what it runs (`script`, `inline`, `module`
    or `stream`), a module name, and the words from its program operand on."""
    index = 1
    while index < len(words):
        word = words[index]
        if word == "-":
            return "stream", None, words[index + 1:]
        if word == "--":
            index += 1
            break
        if word.startswith("--"):
            index += 2 if word in ("--rcfile", "--init-file", "--check-hash-based-pycs", "--require", "--import") \
                else 1
            if word in ("--eval", "--print"):
                return "inline", None, words[index:]
            continue
        if not (word.startswith("-") or (family == "shell" and word.startswith("+"))) or len(word) < 2:
            break
        letters, consumed = word[1:], 0
        for position, letter in enumerate(letters):
            rest = letters[position + 1:]
            if family == "shell":
                if letter == "c":
                    return "inline", None, words[index + 1 + consumed:]
                if letter == "s":
                    return "stream", None, words[index + 1:]
                consumed += letter in "oO"
            elif family == "python" and letter in "cmWX":
                value = rest or (words[index + 1] if index + 1 < len(words) else "")
                if letter == "c":
                    return "inline", None, []
                if letter == "m":
                    return "module", value, []
                consumed = 0 if rest else 1
                break
            elif family in ("perl", "node") and letter in ("eEp" if family == "perl" else "ep"):
                return "inline", None, []
            elif family in ("perl", "node") and letter in ("IMmr" if family == "perl" else "r"):
                consumed = 0 if rest else 1
                break
        index += 1 + consumed
    return ("script" if index < len(words) else "stream"), None, words[index:]


def invocation(instance: dict[str, object]) -> dict[str, str]:
    """What one exec runs: a program, or an interpreter's script, module, inline or streamed program."""
    program = str(instance["program"])
    base = MULTIARCH.sub("", Path(program).name)
    family = interpreter(base)
    words = list(instance["argv"])
    if family is None:
        return {"kind": "program", "name": base, "path": program, "args": words[1:]}
    kind, module, rest = operands(family, words)
    if kind == "module":
        return {"kind": "module", "name": str(module).split(".")[0], "path": str(module)}
    if kind == "inline":
        return {"kind": "inline", "name": base, "path": program}
    if kind == "stream" or rest[0].startswith("/dev/fd/"):
        link = rest[0][8:] if rest and rest[0].startswith("/dev/fd/") and kind == "script" else "0"
        return {"kind": "stream", "name": base, "path": rest[0] if link != "0" else "<stdin>",
                "stream": instance["streams"].get(link, "")}
    return {"kind": "script", "name": Path(rest[0]).name, "path": lexical(str(instance["directory"]), rest[0]),
            "args": rest[1:]}


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


def judge(result: dict[str, object], names: dict[str, object]) -> tuple[list[dict], list[dict]]:
    """Classify every exec instance; return the invocation population and its findings."""
    programs = set(names["programs"])
    scripts = set(names["scripts"])
    modules = set(names["modules"])
    installers = set(names["installers"])
    subcommands = {key: set(value) for key, value in names["installer_subcommands"].items()}
    fetched = {i["streams"].get("1") for i in result["instances"]
               if Path(str(i["program"])).name in FETCHERS and str(i["streams"].get("1", "")).startswith("pipe:")}
    population: dict[tuple, dict] = {}
    findings = []

    def finding(instance: dict, what: dict, reason: str) -> None:
        """Name one forbidden or unprovenanced invocation."""
        findings.append({"invocation": what["name"], "path": what["path"], "argv": instance["argv"], "reason": reason})

    for instance in result["instances"]:
        what = invocation(instance)
        if what["kind"] == "script" and instance.get("script"):
            # Judge the file a link names, and its name, alongside the name it was run by.
            what = {**what, "path": instance["script"], "alias": what["name"],
                    "name": Path(instance["script"]).name}
        base = MULTIARCH.sub("", Path(str(instance["program"])).name)
        provenance = str(instance.get("provenance", "none"))
        if what["kind"] in ("program", "script") and {what["name"], what.get("alias")} & installers:
            finding(instance, what, f"installer executed: {(({what['name'], what.get('alias')} & installers)).pop()}")
        elif what["kind"] == "module" and what["name"] in names["installer_modules"]:
            finding(instance, what, f"installer module executed: {what['name']}")
        elif what["kind"] == "stream" and what.get("stream") in fetched:
            finding(instance, what, f"fetched program executed by {what['name']}")
        elif what.get("args") and what["args"][0] in subcommands.get(what["name"], ()):
            finding(instance, what, f"installer subcommand executed: {what['name']} {what['args'][0]}")
        if interpreter(base) and base not in programs:
            finding(instance, what, f"interpreter not in the allowlist: {base}")
        system = what["path"].startswith(SYSTEM_ROOTS)
        if what["kind"] == "program" and system and what["name"] not in programs:
            finding(instance, what, f"system program not in the allowlist: {what['name']}")
        elif what["kind"] == "script" and system and what["name"] not in scripts:
            finding(instance, what, f"system script not in the allowlist: {what['name']}")
        elif what["kind"] in ("program", "script") and provenance == "none":
            finding(instance, what, f"{what['kind']} without provenance: {what['name']}")
        elif what["kind"] == "module" and what["name"] not in modules:
            finding(instance, what, f"module not in the allowlist: {what['name']}")
        key = (what["kind"], what["name"], what["path"] if what["kind"] != "program" or system else "<built>",
               provenance)
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
               log: Path | None = None, origin: Origin | None = None) -> dict[str, object]:
    """Trace one step, keep its instances, and attach the population and findings.

    A job's steps share one origin, so provenance spans the traced job.
    """
    origin = origin or Origin(root, checkout_files(root))
    directory = root / str(entry.get("working-directory", "."))
    result = trace(list(entry["argv"]), directory, {**environment, **entry.get("env", {})}, origin)
    population, findings = judge(result, names)
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
        (base / "checkout.sh").write_text("exit 0\n")
        step("a link the step makes to a checkout script is judged as that script",
             f"mkdir -p {base}/shadow && ln -s {base}/checkout.sh {base}/shadow/run.sh && "
             f"bash {base}/shadow/run.sh", None)
        step("a link named as an installer is caught by that name",
             f"ln -s {base}/checkout.sh {base}/shadow/apt-get && bash {base}/shadow/apt-get",
             "installer executed: apt-get")
        (base / "tool.py").write_text("print('ok')\n")
        step("an interpreter given a missing script runs nothing from it",
             f"python3 {base}/missing.py 2>/dev/null || true", None)
        step("a permitted interpreter call and a checkout script",
             f"python3 -c 'print(1)' && python3 {base}/tool.py", None)
        (base / "built.c").write_text("int main(void) { return 0; }\n")
        step("a program the step built, and an installed copy of it",
             f"cc -o {base}/built {base}/built.c && {base}/built && install -m 755 {base}/built {base}/copy && "
             f"{base}/copy", None)
        (base / "leak.c").write_text("#include <stdlib.h>\nint main(void) { return malloc(1) == 0; }\n")
        step("a LeakSanitizer build runs its leak check under the audit",
             f"cc -fsanitize=address -o {base}/leak {base}/leak.c && ! {base}/leak 2>{base}/leak.log && "
             f"grep -q 'detected memory leaks' {base}/leak.log", None)
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
