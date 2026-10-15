#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Read an interpreter's command line as the interpreter does: what program it runs.

The execution audit (exec_audit.py) judges an interpreter by its program: a
script file, a `-m` module, an inline program (`-c`, `-e`) or a streamed one
(stdin, `-`). Each reader follows its interpreter's own option rules, so the
program text it finds is the text the interpreter runs.
"""

from __future__ import annotations


SHELLS = {"bash", "sh", "dash"}
PYTHONS = {"python", "python3", "python3.12"}
#: An interpreter that runs nothing in-process: no dynamic loader import, no loadable builtins.
EXEC_ONLY = {"dash"}
#: Interpreters whose inline and streamed program texts can be pinned in the reviewed list.
PINNABLE = {"shell", "python"}


def interpreter(base: str) -> str | None:
    """The interpreter family of a loaded program, if it is one."""
    if base in SHELLS:
        return "shell"
    if base in PYTHONS:
        return "python"
    return base if base in ("perl", "node", "tclsh") else None


def shell_operands(words: list[str]) -> dict[str, object]:
    """Read a shell's options as bash and dash do: `-c` takes the first operand after every option."""
    index, inline, stream = 1, False, False
    while index < len(words):
        word = words[index]
        if word in ("--", "-"):
            index += 1
            break
        if word.startswith("--"):
            index += 2 if word in ("--rcfile", "--init-file") else 1
            continue
        if word[:1] not in ("-", "+") or len(word) < 2:
            break
        consumed = 0
        for letter in word[1:]:
            inline = inline or letter == "c"
            stream = stream or letter == "s"
            consumed += letter in "oO"
        index += 1 + consumed
    rest = words[index:]
    if inline:
        return {"kind": "inline", "text": rest[0] if rest else None, "rest": rest[1:]}
    return {"kind": "script" if rest and not stream else "stream", "rest": rest}


def python_operands(words: list[str]) -> dict[str, object]:
    """Read CPython's options as it does: `-c` and `-m` end them, `-W` and `-X` take a value."""
    index = 1
    while index < len(words):
        word = words[index]
        if word == "-":
            return {"kind": "stream", "rest": words[index + 1:]}
        if word == "--":
            index += 1
            break
        if word.startswith("--"):
            index += 2 if word == "--check-hash-based-pycs" else 1
            continue
        if not word.startswith("-") or len(word) < 2:
            break
        consumed = 0
        for position, letter in enumerate(word[1:]):
            if letter in "cmWX":
                rest = word[2 + position:]
                value = rest or (words[index + 1] if index + 1 < len(words) else None)
                consumed = 0 if rest else 1
                if letter == "c":
                    return {"kind": "inline", "text": value, "rest": words[index + 1 + consumed:]}
                if letter == "m":
                    return {"kind": "module", "module": value, "rest": words[index + 1 + consumed:]}
                break
        index += 1 + consumed
    rest = words[index:]
    return {"kind": "script" if rest else "stream", "rest": rest}


def other_operands(family: str, words: list[str]) -> dict[str, object]:
    """perl, node and tclsh: an inline program is found by its option; none of theirs is pinned."""
    index = 1
    while index < len(words):
        word = words[index]
        if word == "-":
            return {"kind": "stream", "rest": words[index + 1:]}
        if word == "--":
            index += 1
            break
        if word in ("--eval", "--print") or family in ("perl", "node") and word[:1] == "-" and \
                set(word[1:2]) & set("eEp" if family == "perl" else "ep"):
            return {"kind": "inline", "text": None, "rest": []}
        if not word.startswith("-") or len(word) < 2:
            break
        index += 2 if word in ("-I", "-M", "-m", "-r", "--require", "--import", "-encoding") else 1
    rest = words[index:]
    return {"kind": "script" if rest else "stream", "rest": rest}


def operands(family: str, words: list[str]) -> dict[str, object]:
    """What an interpreter runs: `script`, `inline`, `module` or `stream`, with its text, module and operands."""
    if family == "shell":
        return shell_operands(words)
    if family == "python":
        return python_operands(words)
    return other_operands(family, words)
