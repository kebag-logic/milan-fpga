# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Scratch repositories cannot leave automatic maintenance racing their removal."""

from __future__ import annotations

import errno
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

from ctrl_build import Refusal
from ctrl_pin_env import Scene, answer, create
from ctrl_pin_store import loose

if TYPE_CHECKING:
    from ctrl_pin import Clone


def settings(directory: Path, scope: str) -> bool:
    """Both independent maintenance switches are present in the requested configuration scope."""
    lines = answer(directory, "config", "--show-scope", "--list").splitlines()
    return all(f"{scope}\t{setting}" in lines for setting in ("gc.auto=0", "maintenance.auto=false"))


def configured_clones(clone: Clone) -> bool:
    """The ordinary clone and both other construction paths persist the disabled settings."""
    clone.fresh()
    own = clone.work / "lifecycle-config"
    own.mkdir()
    try:
        create(own / "empty")
        create(own / "second", clone.path)
        return all(settings(path, "local") for path in (clone.path, own / "empty", own / "second"))
    finally:
        shutil.rmtree(own)


def command_settings(clone: Clone) -> bool:
    """Every helper command overrides enabled settings in the repository it reads."""
    clone.fresh()
    clone.answer("config", "gc.auto", "1")
    clone.answer("config", "maintenance.auto", "true")
    accepted, detail = clone.direct()
    return not accepted and "gc.auto (local)" in detail and "maintenance.auto (local)" in detail and \
        settings(clone.path, "command") and all(
        clone.answer("config", "--get", key).strip() == value
        for key, value in (("gc.auto", "0"), ("maintenance.auto", "false")))


def loose_fetch(clone: Clone) -> bool:
    """The hosted failure's loose-object fetch stays unpacked and permits the next fresh clone."""
    clone.fresh()
    own = clone.work / "lifecycle-fetch"
    own.mkdir()
    try:
        loose(Scene(clone.path, clone.pin, own))
        safe = settings(clone.path, "local") and settings(clone.path, "command")
        clone.fresh()
        return safe and clone.direct()[0]
    finally:
        shutil.rmtree(own)


def deletion(clone: Clone, error: int) -> bool:
    """Race an unlink after directory enumeration, or inject another error at that same operation."""
    clone.fresh()
    victim = clone.path / ".git/maintenance.lock"
    victim.write_text("transient\n", encoding="utf-8")
    unlink = os.unlink
    seen = False

    def raced(path: str, *, dir_fd: int | None = None) -> None:
        """Inject the selected race or error on the actual removal call."""
        nonlocal seen
        if Path(path).name == victim.name:
            seen = True
            if error == errno.ENOENT:
                unlink(path, dir_fd=dir_fd)
            else:
                raise OSError(error, "planted scratch removal failure", path)
        unlink(path, dir_fd=dir_fd)

    try:
        with patch("os.unlink", raced):
            clone.fresh()
    except OSError as exc:
        return seen and error != errno.ENOENT and exc.errno == error
    return seen and error == errno.ENOENT and clone.direct()[0]


def controls(clone: Clone) -> tuple[int, int]:
    """Exercise real scratch construction, fetch and removal; never turn another deletion error green."""
    cases = (("clone, init and secondary clone disable maintenance", lambda: configured_clones(clone)),
             ("every Git call overrides enabled local maintenance", lambda: command_settings(clone)),
             ("loose fetch then fresh clone", lambda: loose_fetch(clone)),
             ("file vanishing after enumeration", lambda: deletion(clone, errno.ENOENT)),
             ("permission error is propagated", lambda: deletion(clone, errno.EACCES)),
             ("I/O error is propagated", lambda: deletion(clone, errno.EIO)))
    bad = 0
    for name, check in cases:
        try:
            ok, detail = check(), ""
        except (OSError, Refusal) as exc:
            ok, detail = False, str(exc)
        print(f"[{'ok' if ok else 'ESCAPED'}] scratch lifecycle, {name}: {detail or str(ok)}", flush=True)
        bad += not ok
    return bad, len(cases)
