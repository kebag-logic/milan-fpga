#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Observe every program a CI step runs inside the image, and judge each invocation.

This is the execution authority for issue #737. The static inventory derives
which programs the workflows *should* run; this audit records which programs a
step *does* run. Its threat model is accidental drift in reviewed source, and
each guard is closed by construction: an allowlist, or a check that fails closed.

A seccomp filter on the step's process tree turns every `execve`, `execveat` and
`exit_group` into a notification the audit reads before the call continues, so a
static binary is observed like any other and no process is ptraced. Steps run
with the container network disabled; a step that needs the network fails and its
exit status is a finding.

- **Exec ABI.** A call from any architecture other than x86-64, or through the
  x32 entry, is refused before it runs and named.
- **Exec target.** An exec runs only a regular file reached by a path. Its path is
  resolved component by component as the exec's own lookup resolves it; a target through the
  process filesystem or `/dev`, a memfd, a deleted file, or a descriptor that is
  not a path is refused before it runs and named.
- **Invocations.** Every exec instance is kept with its full argument vector and
  directory, and judged by what it runs, not by the loaded interpreter binary.
  Installers are refused by name, as a program, a script or a module.
- **Interpreter programs.** The program text of `bash`, `python3`, `perl`, `node`
  and `tclsh`, whether inline (`-c`, `-e`), streamed (stdin, `-`, `/dev/fd/N`) or
  a file, runs code in-process, so it is accepted only by the digest of its text:
  a file in the checkout as the job started, a byte copy of one, the step's own
  text, or a program in the reviewed lists of `exec-audit.json`. Any other is
  refused by name. `dash` runs nothing in-process (it imports no dynamic loader
  and has no loadable builtins), so a `dash` program is judged by its execs.
- **Programs.** A program inside the image's own directories must be named in
  `exec-audit.json`. Any other program is accepted only with positive provenance:
  its bytes are the declared output of a toolchain invocation the job traced
  (`-o`, or `a.out` without one), digested when that invocation ends, so a
  renamed or installed copy of a build output keeps it; or it is in the reviewed
  list of generated programs.
- **The checkout.** A file present when the job starts is digested then. A script
  whose bytes differ at its exec, and any such file changed during the job, is a
  finding: what the static walker read is what ran.

`--selftest` runs the controls; `--audit SPEC --output RECEIPT` runs a step spec.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import select
import signal
import socket
import stat
import struct
import sys
import time

from exec_files import Watch, key_of, lkey, snapshot
from exec_operands import EXEC_ONLY, PINNABLE, interpreter, operands

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ALLOWLIST = HERE / "exec-audit.json"

#: A seccomp filter turns the step's exec and exit calls, and every call it cannot audit, into
#: a user notification. No process is ptraced, so tools that trace themselves, such as
#: LeakSanitizer, still run.
SYS_SECCOMP, PR_SET_NO_NEW_PRIVS = 317, 38
#: A notified call waits killably once read, so a stop sent to it stays pending until the call returns.
SET_MODE_FILTER, FLAG_NEW_LISTENER, FLAG_WAIT_KILLABLE_RECV = 1, 1 << 3, 1 << 5
NR_EXECVE, NR_EXECVEAT, NR_EXIT_GROUP = 59, 322, 231
ARCH_X86_64, X32_BIT = 0xC000003E, 0x40000000
ARCHES = {0x40000003: "i386", ARCH_X86_64: "x86-64"}
RET_ALLOW, RET_USER_NOTIF, CONTINUE = 0x7FFF0000, 0x7FC00000, 1
NOTIF_RECV, NOTIF_SEND = 0xC0502100, 0xC0182101
AT_FDCWD, AT_SYMLINK_NOFOLLOW, AT_EMPTY_PATH = -100, 0x100, 0x1000
#: Load the architecture: any other than x86-64 is notified, and refused. Load the call
#: number: an x32 call is notified, and refused; exec and exit calls are notified and
#: continued once read; everything else is allowed.
FILTER = ((0x20, 0, 0, 4), (0x15, 0, 6, ARCH_X86_64), (0x20, 0, 0, 0), (0x45, 4, 0, X32_BIT),
          (0x15, 3, 0, NR_EXECVE), (0x15, 2, 0, NR_EXECVEAT), (0x15, 1, 0, NR_EXIT_GROUP),
          (0x06, 0, 0, RET_ALLOW), (0x06, 0, 0, RET_USER_NOTIF))
F_SETPIPE_SZ, F_GETPIPE_SZ, SPLICE_F_NONBLOCK = 1031, 1032, 2

_libc = ctypes.CDLL(None, use_errno=True)
_libc.syscall.restype = ctypes.c_long
_libc.tee.restype = ctypes.c_ssize_t
_libc.tee.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_size_t, ctypes.c_uint)

#: The image's own program directories: a program or script there must be named.
SYSTEM_ROOTS = ("/usr/", "/bin/", "/sbin/", "/lib/", "/lib64/", "/opt/", "/etc/")
#: A toolchain program carries an `<arch>-[<vendor>-]<os>-gnu-` prefix, and a cross toolchain's
#: wrapper runs its real binary under a `.br_real` suffix; the plain tool is named.
MULTIARCH = re.compile(r"^[a-z0-9_]+(?:-[a-z0-9]+){1,2}-gnu-|\.br_real$")
#: Programs whose declared output (`-o`, or `a.out` when linking without one) is a program the step built.
BUILDERS = re.compile(r"^(?:[a-z0-9_]+-[a-z0-9]+-[a-z]+-)?(?:cc|c\+\+|gcc|g\+\+|clang|clang\+\+|ld|ld\.bfd|"
                      r"ld\.gold|collect2)(?:-\d+)?$")
#: Programs that fetch: an interpreter reading its program from their output fetches and executes.
FETCHERS = {"curl", "wget", "fetch", "aria2c"}
#: How long a streamed program's writer may keep its pipe open after the interpreter's exec.
STREAM_WAIT = 60


def _record(pid: int | str, name: str) -> Path:
    """One entry of a traced process's process record."""
    return Path(f"/proc/{pid}/{name}")


#: The process filesystem's root and the device directory: no exec target is reached through them.
PROCESS_ROOT = str(_record(0, "x").parents[1])
NON_PATH_ROOTS = (PROCESS_ROOT, "/dev")


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
    """In the step's first process: install the filter and return its notification fd."""
    if _libc.prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0):
        raise OSError(ctypes.get_errno(), "no_new_privs")
    rows = (_Filter * len(FILTER))(*[_Filter(*row) for row in FILTER])
    program = _Program(len(FILTER), rows)
    listener = _libc.syscall(SYS_SECCOMP, SET_MODE_FILTER, FLAG_NEW_LISTENER | FLAG_WAIT_KILLABLE_RECV,
                             ctypes.byref(program))
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


def _non_path(path: str) -> bool:
    """Whether a path is the process filesystem or the device directory, or under them."""
    return any(path == root or path.startswith(root + "/") for root in NON_PATH_ROOTS)


def resolve(base: str, name: str, nofollow: bool = False) -> tuple[str, object]:
    """Resolve a path component by component, as an exec's own lookup resolves its file.

    Returns ("path", physical path), ("errno", code) when the lookup fails as the
    exec's would, or ("refuse", reason) when the path passes through the process
    filesystem or `/dev`, where a name can stand for a descriptor and not a file.
    """
    pending = name.split("/") if name.startswith("/") else [*base.split("/"), *name.split("/")]
    current, links = "/", 0
    while pending:
        part = pending.pop(0)
        if part in ("", "."):
            continue
        if part == "..":
            current = str(PurePosixPath(current).parent)
            continue
        candidate = str(PurePosixPath(current) / part)
        if _non_path(candidate):
            return "refuse", f"exec through {candidate}: not a file on a path"
        try:
            status = os.lstat(candidate)
        except OSError as error:
            return "errno", error.errno
        if stat.S_ISLNK(status.st_mode):
            if nofollow and not any(p not in ("", ".") for p in pending):
                return "errno", errno.ELOOP
            links += 1
            if links > 40:
                return "errno", errno.ELOOP
            target = os.readlink(candidate)
            pending = [*target.split("/"), *pending]
            current = "/" if target.startswith("/") else current
            continue
        if pending and not stat.S_ISDIR(status.st_mode):
            return "errno", errno.ENOTDIR
        current = candidate
    return "path", current


def _same_file(path: str, view: Path) -> bool:
    """Whether a resolved path and the caller's own view of the target are one file."""
    try:
        mine, theirs = os.stat(path), os.stat(view)
    except OSError:
        return False
    return (mine.st_dev, mine.st_ino) == (theirs.st_dev, theirs.st_ino)


def _target(pid: int, number: int, arguments: list[int]) -> tuple[str, object, list[str]]:
    """What an exec call names: ("run", (lexical name, physical file), argv), ("errno", code, []) for a
    call that fails as the exec itself would, or ("refuse", reason, argv) for a target that is not a
    file on a path. The caller's own view of the target, through its record, must be the same file."""
    directory = _proc(pid, "cwd")
    if number == NR_EXECVEAT:
        handle = ctypes.c_int(arguments[0] & 0xFFFFFFFF).value
        name, vector, flags = _string(pid, arguments[1]), arguments[2], arguments[4]
    else:
        handle, flags = AT_FDCWD, 0
        name, vector = _string(pid, arguments[0]), arguments[1]
    words = _vector(pid, vector)
    if not name and number == NR_EXECVEAT and flags & AT_EMPTY_PATH:
        link = _proc(pid, f"fd/{handle}")
        located = resolve("/", link) if link.startswith("/") else ("refuse", "")
        if located[0] != "path" or not _same_file(located[1], _record(pid, f"fd/{handle}")):
            return "refuse", f"exec of a descriptor that is not a file on a path: {link or '<closed>'}", words
        lexical_name, view = link, _record(pid, f"fd/{handle}")
    elif not name:
        return "errno", errno.ENOENT, []
    else:
        if name.startswith("/"):
            base, view = "/", _record(pid, f"root{name}")
        elif handle == AT_FDCWD:
            base, view = directory, _record(pid, f"cwd/{name}")
        else:
            base, view = _proc(pid, f"fd/{handle}"), _record(pid, f"fd/{handle}/{name}")
        if not base.startswith("/") or not Path(base).is_dir():
            return "refuse", f"exec relative to a directory that is not a path: {base or '<closed>'}", words
        located = resolve(base, name, bool(flags & AT_SYMLINK_NOFOLLOW))
        if located[0] == "refuse":
            return "refuse", located[1], words
        if located[0] == "errno":
            return "errno", located[1], []
        lexical_name = lexical(base, name)
    status = os.stat(located[1])
    if not stat.S_ISREG(status.st_mode) or not os.access(located[1], os.X_OK):
        return "errno", errno.EACCES, []
    if not _same_file(located[1], view):
        return "refuse", f"exec target resolves differently in the caller: {lexical_name}", words
    return "run", (lexical_name, located[1]), words


def _loaded(name: str, path: str, words: list[str], directory: str) -> tuple[str, object, list[str]]:
    """What runs for an executable file: an ELF program, or its interpreter line, with argv built
    as exec builds it, the file passed by the name the exec gave it.

    ("run", program, argv), ("errno", code, []) or ("refuse", reason, argv).
    """
    for _ in range(5):
        try:
            with open(path, "rb") as stream:
                head = stream.read(256)
        except OSError as error:
            return "errno", error.errno, []
        if head.startswith(b"\x7fELF"):
            return "run", path, words
        if not head.startswith(b"#!"):
            return "errno", errno.ENOEXEC, []  # No handler: nothing runs.
        line = head[2:].split(b"\n", 1)[0].decode("utf-8", "surrogateescape").strip()
        interpreter, _, argument = line.partition(" ")
        located = resolve(directory, interpreter)
        if located[0] == "refuse":
            return "refuse", located[1], words
        if located[0] == "errno":
            return "errno", located[1], []
        if not stat.S_ISREG(os.stat(located[1]).st_mode) or not os.access(located[1], os.X_OK):
            return "errno", errno.EACCES, []
        words = [interpreter, *([argument.strip()] if argument.strip() else []), name, *words[1:]]
        name, path = interpreter, located[1]
    return "errno", errno.ELOOP, []


class Origin:
    """Provenance within one traced job, from what existed as it started and what its toolchain declared."""

    def __init__(self, root: Path, names: dict[str, object] | None = None, watch: bool = True,
                 scratch: tuple[str, ...] = ()) -> None:
        self.root = Path(root)
        names = names or allowlist()
        # A job-temporary path: under /tmp or the job's own scratch roots, made only of name characters.
        roots = "|".join(re.escape(root) for root in ("/tmp", *scratch))
        self.temporary = re.compile(rf"(?:{roots})(?![A-Za-z0-9_.-])(?:/[A-Za-z0-9_.-]+)*".encode())
        self.pinned = dict(names.get("inline_programs", {}))
        self.generated = dict(names.get("generated_programs", {}))
        self.started = snapshot(str(self.root), executable=False)
        self.checkout = {path: digest(path) for path in self.started}
        self.copies = {value: path for path, value in sorted(self.checkout.items(), reverse=True) if value}
        self.system: dict[str, tuple] = {}
        for top in SYSTEM_ROOTS:
            self.system.update(snapshot(top, executable=True))
        self.system_sizes: dict[int, list[str]] = {}
        for path, key in sorted(self.system.items()):
            self.system_sizes.setdefault(key[2], []).append(path)
        self.pending: dict[int, list[tuple[str, str]]] = {}
        self.built: dict[str, tuple[str, str]] = {}
        self.texts: set[str] = set()
        self.digests: dict[tuple, str | None] = {}
        self.changed: dict[str, str] = {}
        # What the static walker read: the inventory's recorded inputs, or, without an inventory, every file.
        inventory = self.root / "ci/image/tool-inventory.json"
        followed = json.loads(inventory.read_text())["inputs"] if inventory.is_file() else None
        self.followed = {path for path in self.started
                         if followed is None or Path(path).relative_to(self.root).as_posix() in followed}
        self.writable = {str(self.root / path) for path in names.get("checkout_writes", {})}
        self.rewritten: dict[str, str] = {}
        self.watch = Watch(self.root) if watch else None

    def close(self) -> None:
        """End the job: stop watching its checkout."""
        if self.watch is not None:
            self.watch.close()
            self.watch = None

    def digest(self, path: str) -> str | None:
        """Content identity of a file, cached by its identity and change time."""
        try:
            key = (path, *key_of(os.stat(path)))
        except OSError:
            return None
        if key not in self.digests:
            self.digests[key] = digest(path)
        return self.digests[key]

    def relative(self, path: str) -> str:
        """A checkout path as the receipt names it."""
        return Path(path).relative_to(self.root).as_posix()

    def sweep(self, final: bool = False) -> None:
        """Record every file the walker read whose bytes are no longer those the job started with.

        A file in the reviewed `checkout_writes` list is recorded apart: a step rewrites it on purpose.
        """
        candidates, lost = self.watch.drain() if self.watch else (set(), False)
        if lost or final:
            candidates |= {path for path, key in self.started.items() if lkey(path) != key}
        for path in sorted(candidates & self.followed):
            if path in self.changed or path in self.rewritten:
                continue
            now = self.digest(path) if Path(path).is_file() and not Path(path).is_symlink() else None
            if now != self.checkout[path]:
                change = "removed or replaced" if now is None else f"sha256 {now}"
                (self.rewritten if path in self.writable else self.changed)[path] = change

    def image_copy(self, path: str, own: str) -> str | None:
        """The image executable present as the job started that holds this file's bytes."""
        size = os.stat(path).st_size
        for candidate in self.system_sizes.get(size, []):
            if lkey(candidate) == self.system[candidate] and self.digest(candidate) == own:
                return candidate
        return None

    def started_exec(self, pid: int, instance: dict[str, object]) -> None:
        """Record a toolchain invocation's declared output, and that file as it stood, to digest when it ends."""
        base = MULTIARCH.sub("", Path(str(instance["program"])).name)
        if BUILDERS.match(base) and (output := built_output(list(instance["argv"]), str(instance["directory"]))):
            try:
                before = key_of(os.stat(output))
            except OSError:
                before = None
            self.pending.setdefault(_group(pid), []).append((output, base, before))

    def ended(self, pid: int, status: int) -> None:
        """A process ends: a successful invocation's declared outputs that it wrote are build outputs."""
        if not self.pending:
            return
        for output, builder, before in self.pending.pop(pid if pid in self.pending else _group(pid), []):
            try:
                now = os.stat(output)
            except OSError:
                continue
            if status == 0 and key_of(now) != before and stat.S_ISREG(now.st_mode) and now.st_mode & 0o111 and \
                    (own := self.digest(output)):
                self.built.setdefault(own, (builder, output))

    def judge(self, instance: dict[str, object]) -> str:
        """Where what this exec runs came from."""
        what = invocation(instance)
        kind, path = what["kind"], str(what["path"])
        if kind == "module":
            return "named"
        if kind in ("inline", "stream"):
            family = what["family"]
            if what["name"] in EXEC_ONLY:
                return "exec-only interpreter"
            text = what.get("sha256")
            if not text:
                return "unreadable"
            if text in self.texts:
                return "step text"
            entry = self.pinned.get(text)
            return "pinned" if family in PINNABLE and entry and entry.get("interpreter") == family else "none"
        if kind == "script":
            # The interpreter opens its operand from its own directory; a link names the file it runs.
            located = resolve(str(instance["directory"]), str(what["operand"]))
            if located[0] == "refuse":
                return "not a file on a path"
            if located[0] == "errno":
                return "absent"  # The interpreter cannot open it, so no code runs from it.
            path = str(located[1])
            instance["script"] = path
        if path.startswith(SYSTEM_ROOTS):
            return "named"
        if not Path(path).exists():
            return "absent"
        own = self.digest(path)
        instance["sha256"] = own
        if path in self.started:
            return "checkout" if own == self.checkout[path] else "checkout file changed before it ran"
        if kind == "program":
            if own in self.built:
                builder, output = self.built[own]
                return f"built by {builder}" if output == path else f"copy of a program built by {builder}"
            entry = self.generated.get(own, {})
            return "generated" if entry.get("kind") == "program" else "none"
        if own in self.texts:
            return "step text"
        # A copy of an image executable runs that executable's code, so it is judged as that file, by its name.
        if own and (original := self.image_copy(path, own)):
            instance["copy"] = original
            return f"copy of {original}"
        if own in self.copies:
            return f"copy of {self.relative(self.copies[own])}"
        if Path(str(instance["program"])).name in EXEC_ONLY:
            return "exec-only interpreter"
        with open(path, "rb") as stream:
            data = stream.read()
        instance["text"] = data[:1 << 20].decode("utf-8", "surrogateescape")  # The step log keeps it for review.
        # A generated program is identified with its job-temporary paths masked: such a path is made only of
        # name characters, so it carries no command, and every other byte is exact.
        instance["sha256_masked"] = masked = hashlib.sha256(self.temporary.sub(b"/tmp/<job>", data)).hexdigest()
        entry = self.generated.get(masked, {})
        return "generated" if entry.get("kind") == "script" and entry.get("interpreter") == what["family"] else "none"


def _group(pid: int) -> int:
    """The process a thread belongs to."""
    try:
        for line in _record(pid, "status").read_text().splitlines():
            if line.startswith("Tgid:"):
                return int(line.split()[1])
    except (OSError, ValueError):
        pass
    return pid


def _stream_source(pid: int, descriptor: int) -> tuple[str, int | None]:
    """How to read a streamed program: ("pipe", reopened read end), ("file", offset) or ("none", None)."""
    link = _proc(pid, f"fd/{descriptor}")
    if link.startswith("pipe:["):
        try:
            reopened = os.open(_record(pid, f"fd/{descriptor}"), os.O_RDONLY | os.O_NONBLOCK | os.O_CLOEXEC)
        except OSError:
            return "none", None
        try:
            fcntl.fcntl(reopened, F_SETPIPE_SZ, 1 << 20)  # Room for a program of up to 1 MiB.
        except OSError:
            pass
        return "pipe", reopened
    try:
        status = os.stat(_record(pid, f"fd/{descriptor}"))
    except OSError:
        return "none", None
    if stat.S_ISREG(status.st_mode) or stat.S_ISCHR(status.st_mode) and link == "/dev/null":
        for line in _record(pid, f"fdinfo/{descriptor}").read_text().splitlines():
            if line.startswith("pos:"):
                return "file", int(line.split()[1])
    return "none", None


def _pipe_text(reopened: int) -> bytes:
    """Duplicate what a pipe holds without consuming it, once its writers have closed it."""
    size = fcntl.fcntl(reopened, F_GETPIPE_SZ)
    reader, writer = os.pipe()
    try:
        fcntl.fcntl(writer, F_SETPIPE_SZ, size)
        copied = _libc.tee(reopened, writer, size, SPLICE_F_NONBLOCK)
        if copied < 0 and ctypes.get_errno() != errno.EAGAIN:
            raise OSError(ctypes.get_errno(), "tee")
        os.close(writer)
        writer = -1
        data = b""
        while chunk := os.read(reader, 1 << 16):
            data += chunk
        return data
    finally:
        os.close(reader)
        if writer >= 0:
            os.close(writer)


def _file_text(pid: int, descriptor: int, offset: int) -> bytes:
    """A streamed program read from a file, from where the interpreter will start reading."""
    with open(_record(pid, f"fd/{descriptor}"), "rb") as stream:
        stream.seek(offset)
        return stream.read(1 << 24)


def _respond(listener: int, serial: int, error: int = 0) -> None:
    """Let a notified call continue, or fail it with an errno before it runs."""
    response = struct.pack("<QqiI", serial, 0, -error if error else 0, 0 if error else CONTINUE)
    try:
        fcntl.ioctl(listener, NOTIF_SEND, bytearray(response), True)
    except OSError:
        pass  # The caller died after its notification was read.


def _start(argv: list[str], cwd: Path, env: dict[str, str]) -> tuple[int, int]:
    """Fork the step under the filter; return its process and the filter's notification descriptor."""
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
    return pid, descriptors[0]


class _Trace:
    """One step's notifications: each exec instance kept and judged, each refused call kept apart.

    A streamed program read from a pipe whose writers are still open is held: its
    exec completes with a stop pending, so the interpreter stops before its first
    instruction, and a parent waiting for the exec (a vfork) can write the program.
    Once every writer has closed the pipe, its whole text is read without consuming
    it, and the interpreter continues.
    """

    def __init__(self, listener: int, origin: Origin) -> None:
        self.listener, self.origin = listener, origin
        self.instances: list[dict[str, object]] = []
        self.refused: list[dict[str, object]] = []
        self.waiting: dict[int, tuple[int, dict, float]] = {}
        self.poller = select.poll()
        self.poller.register(listener, select.POLLIN)

    def admit(self, serial: int | None, caller: int, instance: dict, text: bytes | None) -> None:
        """Judge one exec instance, keep it, and let its call continue unless it already has."""
        if text is not None:
            instance["sha256_text"] = hashlib.sha256(text).hexdigest()
            instance["text"] = text.decode("utf-8", "surrogateescape")  # The step log keeps it for review.
        instance["provenance"] = self.origin.judge(instance)
        self.origin.started_exec(caller, instance)
        self.instances.append(instance)
        if serial is not None:
            _respond(self.listener, serial)

    def finish(self, reopened: int) -> None:
        """A held stream's writers are done, or its wait is over: read it and let the interpreter run."""
        caller, instance, _ = self.waiting.pop(reopened)
        self.poller.unregister(reopened)
        complete = poll_hangup(reopened)
        text = _pipe_text(reopened) if complete else None
        os.close(reopened)
        if not complete:
            instance["stream_open"] = True
        self.admit(None, caller, instance, text)
        try:
            os.kill(caller, signal.SIGCONT)
        except ProcessLookupError:
            pass

    def refuse(self, serial: int, entry: dict[str, object], error: int) -> None:
        """Fail a call before it runs, and keep why."""
        if entry not in self.refused:
            self.refused.append(entry)
        _respond(self.listener, serial, error)

    def notified(self) -> None:
        """Read one notification and answer it."""
        request = bytearray(80)
        try:
            fcntl.ioctl(self.listener, NOTIF_RECV, request, True)
        except OSError:
            return  # The caller died before its notification was read.
        serial, caller = int.from_bytes(request[0:8], "little"), int.from_bytes(request[8:12], "little")
        number, arch = int.from_bytes(request[16:20], "little"), int.from_bytes(request[20:24], "little")
        arguments = [int.from_bytes(request[32 + 8 * i:40 + 8 * i], "little") for i in range(6)]
        self.origin.sweep()
        if arch != ARCH_X86_64 or number & X32_BIT:
            abi = "x32" if arch == ARCH_X86_64 else ARCHES.get(arch, hex(arch))
            self.refuse(serial, {"pid": caller, "program": _proc(caller, "exe"),
                                 "reason": f"{abi} system call refused: {number & ~X32_BIT}"}, errno.EPERM)
        elif number == NR_EXIT_GROUP:
            self.origin.ended(caller, arguments[0] & 0xFF)
            _respond(self.listener, serial)
        else:
            self.executed(serial, caller, number, arguments)

    def executed(self, serial: int, caller: int, number: int, arguments: list[int]) -> None:
        """An exec: refuse a target that is not a file on a path, fail what cannot run, keep what runs."""
        outcome, value, words = _target(caller, number, arguments)
        directory = _proc(caller, "cwd")
        program = None
        if outcome == "run":
            outcome, program, words = _loaded(value[0], value[1], words, directory)
        if outcome == "errno":
            _respond(self.listener, serial, int(value))
            return
        if outcome == "refuse":
            self.refuse(serial, {"pid": caller, "argv": words, "reason": f"exec refused: {value}"}, errno.EACCES)
            return
        streams = {str(n): _proc(caller, f"fd/{n}") for n in (0, 1)}
        for word in words:
            if word.startswith("/dev/fd/") and word[8:].isdigit():
                streams[word[8:]] = _proc(caller, f"fd/{word[8:]}")
        instance = {"pid": caller, "file": value[0], "program": program, "argv": words,
                    "directory": directory, "streams": streams}
        what = invocation(instance)
        if what["kind"] != "stream" or what["family"] not in PINNABLE or what["name"] in EXEC_ONLY:
            self.admit(serial, caller, instance, None)
            return
        source, handle = _stream_source(caller, int(what["descriptor"]))
        if source == "pipe" and not poll_hangup(handle):
            # The stop stays pending through the exec, which completes: nothing of the program runs yet.
            os.kill(caller, signal.SIGSTOP)
            _respond(self.listener, serial)
            self.waiting[handle] = (caller, instance, time.monotonic() + STREAM_WAIT)
            self.poller.register(handle, 0)
            return
        if source == "pipe":
            text = _pipe_text(handle)
            os.close(handle)
        else:
            text = _file_text(caller, int(what["descriptor"]), handle) if source == "file" else None
        self.admit(serial, caller, instance, text)

    def run(self, pid: int) -> int:
        """Answer notifications until the step and every process it left have ended; return its status."""
        exit_status, deadline = None, None
        while True:
            if exit_status is None:
                waited, status = os.waitpid(pid, os.WNOHANG)
                if waited:
                    exit_status = os.waitstatus_to_exitcode(status)
                    deadline = time.monotonic() + 30  # Processes the step left behind may still exec.
            events = dict(self.poller.poll(10 if self.waiting else 100))
            for reopened in [r for r in self.waiting if events.get(r, 0) & (select.POLLHUP | select.POLLERR) or
                             time.monotonic() > self.waiting[r][2]]:
                self.finish(reopened)
            flags = events.get(self.listener, 0)
            if not self.waiting and (flags & (select.POLLHUP | select.POLLERR) and exit_status is not None or
                                     deadline is not None and time.monotonic() > deadline):
                break
            if flags & select.POLLIN:
                self.notified()
        if exit_status is None:
            _, status = os.waitpid(pid, 0)
            exit_status = os.waitstatus_to_exitcode(status)
        return exit_status


def trace(argv: list[str], cwd: Path, env: dict[str, str], origin: Origin) -> dict[str, object]:
    """Run one command and keep every exec instance of its whole process tree.

    Each instance records the process, the file the exec named and the program the
    exec loads for it, the full argument vector as that program receives it, the
    directory, the stream links an interpreter may read, and the digest of a
    streamed program's text. Provenance is judged at the exec itself, while the
    file it runs still exists. Refused calls are kept apart and never run.
    """
    pid, listener = _start(argv, cwd, env)
    tracer = _Trace(listener, origin)
    try:
        exit_status = tracer.run(pid)
    finally:
        for reopened, (caller, _, _) in tracer.waiting.items():
            os.close(reopened)
            try:
                os.kill(caller, signal.SIGCONT)
            except ProcessLookupError:
                pass
        os.close(listener)
    return {"exit_status": exit_status, "instances": tracer.instances, "refused": tracer.refused}


def poll_hangup(descriptor: int) -> bool:
    """Whether a pipe's every writer has closed it."""
    once = select.poll()
    once.register(descriptor, 0)
    return any(flags & select.POLLHUP for _, flags in once.poll(0))


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
    """The reviewed program, script, module and program-text allowlists and the installer denylists."""
    return json.loads(ALLOWLIST.read_text())


def invocation(instance: dict[str, object]) -> dict[str, object]:
    """What one exec runs: a program, or an interpreter's script, module, inline or streamed program."""
    program = str(instance["program"])
    base = MULTIARCH.sub("", Path(program).name)
    family = interpreter(base)
    words = list(instance["argv"])
    if family is None:
        return {"kind": "program", "name": base, "path": program, "args": words[1:]}
    read = operands(family, words)
    kind, rest = read["kind"], list(read["rest"])
    if kind == "module":
        return {"kind": "module", "name": str(read["module"]).split(".")[0], "path": str(read["module"]),
                "family": family}
    if kind == "inline":
        text = read.get("text")
        return {"kind": "inline", "name": base, "path": program, "family": family,
                "sha256": hashlib.sha256(text.encode("utf-8", "surrogateescape")).hexdigest()
                if isinstance(text, str) and family in PINNABLE else None}
    if kind == "stream" or rest[0].startswith("/dev/fd/") and rest[0][8:].isdigit():
        descriptor = rest[0][8:] if kind == "script" else "0"
        return {"kind": "stream", "name": base, "path": rest[0] if descriptor != "0" else "<stdin>",
                "family": family, "descriptor": descriptor, "stream": instance["streams"].get(descriptor, ""),
                "sha256": instance.get("sha256_text")}
    return {"kind": "script", "name": Path(rest[0]).name, "path": lexical(str(instance["directory"]), rest[0]),
            "operand": rest[0], "args": rest[1:], "family": family}


def subcommand(args: list[str]) -> str | None:
    """A tool's subcommand: its first operand after options, `+toolchain` and option values."""
    index = 0
    while index < len(args) and args[index][:1] in ("-", "+"):
        index += 2 if args[index] in ("-C", "--config", "-Z", "--color", "--manifest-path") else 1
    return args[index] if index < len(args) else None


def built_output(words: list[str], directory: str) -> str | None:
    """The declared output of a build program, resolved in its directory: `-o`, `--output`, or `a.out`
    when a driver links (no `-c`, `-S` or `-E`) or `ld` runs without one."""
    for index, word in enumerate(words):
        operand = words[index + 1] if word in ("-o", "--output") and index + 1 < len(words) else (
            word[2:] if word.startswith("-o") and len(word) > 2 and not word.startswith("-o-") else
            word[9:] if word.startswith("--output=") else None)
        if operand:
            return lexical(directory, operand)
    if len(words) > 1 and not {"-c", "-S", "-E", "-M", "-MM", "--version", "-v", "--help", "-dumpversion",
                               "-dumpmachine", "-print-prog-name", "-###"} & set(words[1:]) and \
            not any(w.startswith(("-print-", "-dump", "--print")) for w in words[1:]):
        return lexical(directory, "a.out")
    return None


def digest(path: str) -> str | None:
    """Content identity of a file."""
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
        """Name one forbidden or unprovenanced invocation, with the digest of what it ran."""
        findings.append({"invocation": what["name"], "path": what["path"], "argv": instance["argv"], "reason": reason,
                         "sha256": what.get("sha256") or instance.get("sha256_masked") or instance.get("sha256")})

    for instance in result["instances"]:
        what = invocation(instance)
        if what["kind"] == "script" and instance.get("script"):
            # Judge the file a link names, or the image file a copy reproduces, alongside the name it was run by.
            judged = str(instance.get("copy") or instance["script"])
            what = {**what, "path": judged, "alias": what["name"], "name": Path(judged).name}
        base = MULTIARCH.sub("", Path(str(instance["program"])).name)
        provenance = str(instance.get("provenance", "none"))
        if what["kind"] in ("program", "script") and {what["name"], what.get("alias")} & installers:
            finding(instance, what, f"installer executed: {(({what['name'], what.get('alias')} & installers)).pop()}")
        elif what["kind"] == "module" and what["name"] in names["installer_modules"]:
            finding(instance, what, f"installer module executed: {what['name']}")
        elif what["kind"] == "stream" and what.get("stream") in fetched:
            finding(instance, what, f"fetched program executed by {what['name']}")
        elif (command := subcommand(what.get("args", []))) in subcommands.get(what["name"], ()):
            finding(instance, what, f"installer subcommand executed: {what['name']} {command}")
        if interpreter(base) and base not in programs:
            finding(instance, what, f"interpreter not in the allowlist: {base}")
        system = str(what["path"]).startswith(SYSTEM_ROOTS)
        if what["kind"] == "program" and system and what["name"] not in programs:
            finding(instance, what, f"system program not in the allowlist: {what['name']}")
        elif what["kind"] == "script" and system and what["name"] not in scripts:
            finding(instance, what, f"system script not in the allowlist: {what['name']}")
        elif what["kind"] in ("inline", "stream") and provenance == "none":
            finding(instance, what, f"unpinned {'inline' if what['kind'] == 'inline' else 'streamed'} program: "
                                    f"{what['name']} {what.get('sha256') or '(text not read)'}")
        elif what["kind"] == "stream" and provenance == "unreadable":
            finding(instance, what, f"streamed program not readable at its exec: {what['name']} "
                                    f"({what.get('stream') or 'no stream'})")
        elif what["kind"] in ("program", "script") and provenance == "none":
            finding(instance, what, f"{what['kind']} without provenance: {what['name']}")
        elif provenance == "not a file on a path":
            finding(instance, what, f"script that is not a file on a path: {what['name']}")
        elif provenance == "checkout file changed before it ran":
            finding(instance, what, f"checkout file changed before it ran: {what['name']}")
        elif what["kind"] == "module" and what["name"] not in modules:
            finding(instance, what, f"module not in the allowlist: {what['name']}")
        texts = what["kind"] in ("inline", "stream") and base not in EXEC_ONLY
        key = (what["kind"], what["name"], what["path"] if what["kind"] != "program" or system else "<built>",
               provenance, what.get("sha256") if texts else instance.get("sha256") if provenance == "checkout"
               else None)
        row = population.setdefault(key, {"kind": key[0], "invocation": key[1], "path": key[2],
                                          "provenance": key[3], "count": 0})
        if key[4]:
            row["sha256"] = key[4]
        row["count"] += 1
    for refusal in result.get("refused", []):
        findings.append({"invocation": "<refused>", "path": refusal.get("program", ""),
                         "argv": refusal.get("argv", []), "reason": refusal["reason"]})
    for path, change in sorted(result.get("changed", {}).items()):
        findings.append({"invocation": "<checkout>", "path": path, "argv": [],
                         "reason": f"checkout file changed during the job: {path} ({change})"})
    if result["exit_status"] != 0:
        findings.append({"invocation": "<step>", "path": "", "argv": [],
                         "reason": f"step exited {result['exit_status']} (network disabled)"})
    return sorted(population.values(), key=lambda row: (row["kind"], row["invocation"], row["path"],
                                                        row.get("sha256", ""))), findings


def audit_step(entry: dict[str, object], names: dict[str, object], root: Path, environment: dict[str, str],
               log: Path | None = None, origin: Origin | None = None) -> dict[str, object]:
    """Trace one step, keep its instances, and attach the population and findings.

    A job's steps share one origin, so provenance spans the traced job. The step's
    own text (`entry["text"]`) is reviewed source: its program is accepted by digest.
    """
    own = origin is None
    origin = origin or Origin(root, names)
    try:
        if entry.get("text") is not None:
            origin.texts.add(hashlib.sha256(str(entry["text"]).encode()).hexdigest())
        directory = root / str(entry.get("working-directory", "."))
        reported, rewritten = set(origin.changed), set(origin.rewritten)
        result = trace(list(entry["argv"]), directory, {**environment, **entry.get("env", {})}, origin)
        origin.sweep(final=True)
        result["changed"] = {origin.relative(p): c for p, c in origin.changed.items() if p not in reported}
        result["rewritten"] = sorted(origin.relative(p) for p in origin.rewritten if p not in rewritten)
    finally:
        if own:
            origin.close()
    population, findings = judge(result, names)
    lines = "".join(json.dumps(i, sort_keys=True) + "\n" for i in result["instances"]).encode()
    if log is not None:
        log.write_bytes(lines)
    return {"job": entry["job"], "label": entry["label"], "argv": entry["argv"],
            "working-directory": str(entry.get("working-directory", ".")), "exit_status": result["exit_status"],
            "instances": len(result["instances"]), "instances_sha256": hashlib.sha256(lines).hexdigest(),
            "population": population, "findings": findings, "clean": not findings,
            **({"checkout_writes": result["rewritten"]} if result["rewritten"] else {})}


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
        import exec_audit_selftest  # noqa: PLC0415 - the controls load only when they run
        return exec_audit_selftest.selftest(names)
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
