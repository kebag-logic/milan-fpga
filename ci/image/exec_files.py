#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""File state the execution audit compares: snapshots of directories, and a watch on the checkout.

A snapshot keeps each file's identity and change time, which any write changes,
so an unchanged key proves unchanged bytes. The watch reports every change to a
file in a directory of the checkout as it started (exec_audit.py, `Origin`).
"""

from __future__ import annotations

import ctypes
import os
from pathlib import Path
import stat
import struct


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
