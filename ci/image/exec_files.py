#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""File state the execution audit compares: snapshots of directories, and a watch on the checkout.

A snapshot keeps each file's identity and change time, which any write changes,
so an unchanged key proves unchanged bytes. The watch reports every change to a
file in a directory of the checkout as it started (exec_audit.py, `Origin`). The
image snapshot keeps the image's own executables, and its interpreters by the
identity of their files.
"""

from __future__ import annotations

import ctypes
import hashlib
import os
from pathlib import Path
import stat
import struct

from exec_operands import EXEC_ONLY, interpreter


LIBC = ctypes.CDLL(None, use_errno=True)
#: Inotify events that change a checkout file: written, attributes, moved, deleted.
CHANGES = 0x2 | 0x4 | 0x8 | 0x40 | 0x80 | 0x100 | 0x200 | 0x400 | 0x800
IN_Q_OVERFLOW, IN_ISDIR = 0x4000, 0x40000000


def snapshot(top: str, executable: bool) -> dict[str, tuple]:
    """Each regular file under a directory, with the status that proves it unchanged since."""
    found = {}
    for base, children, files in Path(top).walk():
        children[:] = [c for c in children if c != ".git"]
        for name in files:
            path = str(base / name)
            try:
                status = os.lstat(path)
            except OSError:
                continue
            if stat.S_ISREG(status.st_mode) and (not executable or status.st_mode & 0o111):
                found[path] = key_of(status)
    return found


def key_of(status: os.stat_result) -> tuple:
    """A file's identity and change time: any write to it changes this key."""
    return status.st_dev, status.st_ino, status.st_size, status.st_mtime_ns, status.st_ctime_ns


def lkey(path: str) -> tuple | None:
    """The key of a path itself, not what a link names; None once it is gone."""
    try:
        return key_of(os.lstat(path))
    except OSError:
        return None


class Watch:
    """Inotify on every checkout directory: any change to a file present at the job's start."""

    def __init__(self, root: Path) -> None:
        self.descriptor = LIBC.inotify_init1(os.O_NONBLOCK | os.O_CLOEXEC)
        self.directories: dict[int, str] = {}
        if self.descriptor < 0:
            raise OSError(ctypes.get_errno(), "inotify")
        for base, children, _ in Path(root).walk():
            children[:] = [c for c in children if c != ".git"]
            watch = LIBC.inotify_add_watch(self.descriptor, bytes(base), CHANGES)
            if watch < 0:
                raise OSError(ctypes.get_errno(), f"inotify watch on {base}")
            self.directories[watch] = str(base)

    def drain(self) -> tuple[set[str], bool]:
        """The paths changed since the last drain, and whether events were lost."""
        changed, lost = set(), False
        while True:
            try:
                data = os.read(self.descriptor, 1 << 16)
            except BlockingIOError:
                return changed, lost
            offset = 0
            while offset < len(data):
                watch, mask, _, length = struct.unpack_from("iIII", data, offset)
                name = data[offset + 16:offset + 16 + length].split(b"\0", 1)[0].decode("utf-8", "surrogateescape")
                offset += 16 + length
                if mask & IN_Q_OVERFLOW:
                    lost = True
                elif watch in self.directories and name and not mask & IN_ISDIR:
                    changed.add(str(Path(self.directories[watch]) / name))

    def close(self) -> None:
        """Stop watching."""
        os.close(self.descriptor)


def digest(path: str) -> str | None:
    """Content identity of a file."""
    try:
        with open(path, "rb") as stream:
            return hashlib.file_digest(stream, "sha256").hexdigest()
    except OSError:
        return None


def _elf(path: str) -> bool:
    """Whether a file is an ELF program."""
    try:
        with open(path, "rb") as stream:
            return stream.read(4) == b"\x7fELF"
    except OSError:
        return False


class Image:
    """The image's own executables as a job starts, and its interpreters by the identity of their files."""

    def __init__(self, roots: tuple[str, ...]) -> None:
        self.files: dict[str, tuple] = {}
        for top in roots:
            self.files.update(snapshot(top, executable=True))
        self.sizes: dict[int, list[str]] = {}
        for path, key in sorted(self.files.items()):
            self.sizes.setdefault(key[2], []).append(path)
        self.digests: dict[tuple, str | None] = {}
        # An interpreter is a file the image names for its family; a file named `dash` loads no further code.
        self.families: dict[tuple, tuple[str, bool]] = {}
        for path, key in sorted(self.files.items()):
            name = Path(path).name
            if (family := interpreter(name)) and _elf(path):
                known = self.families.get(key[:2], (family, False))
                self.families[key[:2]] = (known[0], known[1] or name in EXEC_ONLY)
        # Any other image file holding an interpreter's bytes is that interpreter, whatever its name.
        seeds = {key[:2]: path for path, key in sorted(self.files.items()) if key[:2] in self.families}
        for identity, seed in sorted(seeds.items()):
            for candidate in self.sizes.get(self.files[seed][2], []):
                other = self.files[candidate][:2]
                if other not in self.families and self.digest(candidate) == self.digest(seed):
                    self.families[other] = self.families[identity]

    def digest(self, path: str) -> str | None:
        """Content identity of an image file, cached by its key."""
        key = (path, self.files.get(path))
        if key not in self.digests:
            self.digests[key] = digest(path)
        return self.digests[key]

    def held(self, path: str) -> tuple | None:
        """The job-start key of a path the image held, if the file there is still that file."""
        key = self.files.get(path)
        return key if key is not None and lkey(path) == key else None
