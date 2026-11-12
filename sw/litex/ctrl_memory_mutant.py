# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""How test_ctrl_memory.py plants a mutant: one definition of ctrl_memory.py or milan_soc.py rebuilt from its
own source with one edit (`mutated`), put in place for the duration of one arm (`patched`)."""

from __future__ import annotations

import __future__
import ast
import contextlib
import inspect
import textwrap
import types
from collections.abc import Iterator
from typing import Any


def mutated(owner: types.ModuleType, name: str, old: str, new: str) -> Any:
    """`owner.name` rebuilt from its own source with `old` replaced by `new`, which must match once.

    The text compiled is the module's own definition of `name` and nothing else:
    it must parse to exactly that one definition, and it runs in the module's
    own namespace, so the rebuilt object sees every other name as it was.
    """
    source = textwrap.dedent(inspect.getsource(getattr(owner, name)))
    if source.count(old) != 1:
        raise LookupError(f"{owner.__name__}.{name}: the edit matches {source.count(old)} times, not once")
    edited_source = source.replace(old, new)
    tree = ast.parse(edited_source)
    if [getattr(node, "name", None) for node in tree.body] != [name]:
        raise LookupError(f"{owner.__name__}.{name}: the edited source is not one definition of {name}")
    scope: dict[str, Any] = {}
    exec(compile(edited_source, f"<mutant of {owner.__name__}.{name}>", "exec",
                 flags=__future__.annotations.compiler_flag, dont_inherit=True), vars(owner), scope)
    return scope[name]


@contextlib.contextmanager
def patched(owner: object, name: str, value: object) -> Iterator[None]:
    """Replace `owner.name` for the duration of one mutant."""
    original = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield
    finally:
        setattr(owner, name, original)
