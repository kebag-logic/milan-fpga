#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Read an exec's argument vector as the program does: what it runs, and what it declares.

The execution audit (exec_audit.py) judges an interpreter by its program: a
script file, a `-m` module, an inline program (`-c`, `-e`) or a streamed one
(stdin, `-`). Each reader follows its interpreter's own option rules, so the
program text it finds is the text the interpreter runs. An option a reader does
not model, or one that makes the interpreter read code from somewhere other
than its program (start files, preloaded modules, an interactive session after
the program), is refused by name: the reading never guesses.

`invocation` reads one exec instance: a program, or an image interpreter's own
program. `subcommand` and `built_output` read a tool's subcommand and a
toolchain invocation's declared output.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


#: A toolchain program carries an `<arch>-[<vendor>-]<os>-gnu-` prefix, and a cross toolchain's
#: wrapper runs its real binary under a `.br_real` suffix; the plain tool is named.
MULTIARCH = re.compile(r"^[a-z0-9_]+(?:-[a-z0-9]+){1,2}-gnu-|\.br_real$")
#: Programs whose declared output (`-o`, or `a.out` when linking without one) is a program the step built.
BUILDERS = re.compile(r"^(?:[a-z0-9_]+-[a-z0-9]+-[a-z]+-)?(?:cc|c\+\+|gcc|g\+\+|clang|clang\+\+|ld|ld\.bfd|"
                      r"ld\.gold|collect2)(?:-\d+)?$")
#: An image interpreter's family, by the name of its file in the image (exec_audit.py, `Origin`).
FAMILIES = (("shell", re.compile(r"^(?:ba|da|rba)?sh$")), ("python", re.compile(r"^python(?:3(?:\.\d+)?)?$")),
            ("perl", re.compile(r"^perl(?:5(?:\.\d+)*)?$")), ("node", re.compile(r"^node(?:js)?$")),
            ("tclsh", re.compile(r"^tclsh(?:\d+(?:\.\d+)*)?$")))
#: An interpreter that loads no further code: no dynamic loader import, no loadable builtins.
EXEC_ONLY = {"dash"}
#: CPython 3.12's short options; `-i` reads stdin as a program after the script, so it refuses.
PYTHON_LETTERS = set("bBcdEhIOPqRsSuvVWxX?m")


def interpreter(base: str) -> str | None:
    """The interpreter family a file name spells, if any."""
    return next((family for family, pattern in FAMILIES if pattern.match(base)), None)


def refused(reason: str) -> dict[str, object]:
    """An interpreter command line the readers do not model."""
    return {"kind": "refused", "reason": reason, "rest": []}


def shell_operands(words: list[str]) -> dict[str, object]:
    """Read a shell's options as bash and dash do: `-c` takes the first operand after every option.

    `-i` and `-l` make the shell read start files before its program, so they refuse.
    """
    index, inline, stream = 1, False, False
    while index < len(words):
        word = words[index]
        if word in ("--", "-"):
            index += 1
            break
        if word.startswith("--"):
            if word in ("--login", "--rcfile", "--init-file", "--debugger"):
                return refused(f"shell option {word} reads code from start files")
            index += 2 if word in ("--rcfile", "--init-file") else 1
            continue
        if word[:1] not in ("-", "+") or len(word) < 2:
            break
        consumed = 0
        for letter in word[1:]:
            if letter in "il":
                return refused(f"shell option -{letter} reads code from start files")
            inline = inline or letter == "c"
            stream = stream or letter == "s"
            consumed += letter in "oO"
        index += 1 + consumed
    rest = words[index:]
    if inline:
        if not rest:
            return refused("shell -c without its program")
        return {"kind": "inline", "text": rest[0], "rest": rest[1:]}
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
            if letter not in PYTHON_LETTERS:
                return refused(f"python option -{letter} is not modelled")
            if letter in "cmWX":
                rest = word[2 + position:]
                value = rest or (words[index + 1] if index + 1 < len(words) else None)
                consumed = 0 if rest else 1
                if letter in "cm" and value is None:
                    return refused(f"python -{letter} without its argument")
                if letter == "c":
                    return {"kind": "inline", "text": value, "rest": words[index + 1 + consumed:]}
                if letter == "m":
                    return {"kind": "module", "module": value, "rest": words[index + 1 + consumed:]}
                break
        index += 1 + consumed
    rest = words[index:]
    return {"kind": "script" if rest else "stream", "rest": rest}


def _octal(text: str, limit: int) -> int:
    """How many leading octal digits perl's grok_oct reads, up to a limit."""
    count = 0
    while count < min(limit, len(text)) and text[count] in "01234567":
        count += 1
    return count


def perl_operands(words: list[str]) -> dict[str, object]:
    """Read perl 5.38's switches as perl does (perl.c, `S_parse_body` and `moreswitches`).

    Switches bundle: `-le CODE` is `-l` then `-e CODE`. Each `-e` or `-E` adds its
    text and a newline to the program; `-I` takes the rest of its word or the next
    one; `-i` and `-F` take the rest of their word; `-l` and `-0` take octal digits;
    `-C` takes the rest of its word. `-M`, `-m`, `-d`, `-x` and `-S` load or find
    code other than the program, and every other switch is unmodelled: both refuse.
    """
    index, text = 1, None
    while index < len(words):
        word = words[index]
        if word[:1] != "-" or word == "-":
            break
        if word == "--":
            index += 1
            break
        letters, position, consumed = word[1:], 0, 0
        while position < len(letters):
            letter, rest = letters[position], letters[position + 1:]
            if letter in "eE":
                if not rest and index + 1 >= len(words):
                    return refused("perl -e without its program")
                text = (text or "") + (rest or words[index + 1]) + "\n"
                consumed = 0 if rest else 1
                break
            if letter == "I":
                if not rest and index + 1 >= len(words):
                    return refused("perl -I without its directory")
                consumed = 0 if rest else 1
                break
            if letter in "iF":
                if any(c.isspace() for c in rest):
                    return refused(f"perl switch -{letter} with a blank is not modelled")
                break
            if letter == "C":
                if rest and not (rest.isdigit() or set(rest) <= set("IOEioSDALa")):
                    return refused(f"perl switch -C{rest} is not modelled")
                break
            if letter == "l":
                count = _octal(rest, 4 if rest[:1] == "0" else 3)
                if rest[:1].isdigit() and not count:
                    return refused(f"perl switch -l{rest} is not modelled")
                position += 1 + count
                continue
            if letter == "0":
                if rest[:1] == "x":
                    return refused("perl switch -0x is not modelled")
                position += _octal(letters[position:], 4)
                continue
            if letter not in "acnpstTUuwWXf":
                return refused(f"perl switch -{letter} is not modelled")
            position += 1
        index += 1 + consumed
    if text is not None:
        return {"kind": "inline", "text": text, "rest": words[index:]}
    rest = words[index:]
    return {"kind": "script" if rest and rest[0] != "-" else "stream", "rest": rest[1:] if rest[:1] == ["-"] else rest}


def node_operands(words: list[str]) -> dict[str, object]:
    """Read node 22's options for its program: `-e`, `--eval` and `-pe` take the next word, which may
    not start with `-`, and the last program given wins; `--eval=TEXT` too. `-p` and `--print` take
    the next word as the program unless it starts with `-`. The first other word ends the options: the
    script, or with a program its first argument. `-` reads stdin. Every other option refuses, since
    node's preload, loader and interactive options run code other than the program."""
    index, text = 1, None
    while index < len(words):
        word = words[index]
        if word == "-":
            return {"kind": "stream", "rest": words[index + 1:]}
        if word == "--":
            index += 1
            break
        following = words[index + 1] if index + 1 < len(words) else None
        if word in ("-p", "--print"):
            if following is not None and not following.startswith("-"):
                text = following
                index += 1
            index += 1
            continue
        if word in ("-e", "--eval", "-pe"):
            if following is None or following.startswith("-"):
                return refused(f"node {word} without its program")
            text = following
            index += 2
            continue
        if word.startswith("--eval="):
            if word == "--eval=":
                return refused("node --eval= without its program")
            text = word[len("--eval="):]
            index += 1
            continue
        if word.startswith("-"):
            return refused(f"node option {word.split('=', 1)[0]} is not modelled")
        break
    rest = words[index:]
    if text is not None:
        return {"kind": "inline", "text": text, "rest": rest}
    return {"kind": "script" if rest else "stream", "rest": rest}


def tcl_operands(words: list[str]) -> dict[str, object]:
    """Read tclsh 8.6 as `Tcl_Main` does: `-encoding NAME FILE`, or a first word without a leading
    `-`, is the script; otherwise the program is read from stdin."""
    if len(words) > 3 and words[1] == "-encoding" and not words[3].startswith("-"):
        return {"kind": "script", "rest": words[3:]}
    if len(words) > 1 and not words[1].startswith("-"):
        return {"kind": "script", "rest": words[1:]}
    return {"kind": "stream", "rest": []}


READERS = {"shell": shell_operands, "python": python_operands, "perl": perl_operands, "node": node_operands,
           "tclsh": tcl_operands}


def operands(family: str, words: list[str]) -> dict[str, object]:
    """What an interpreter runs: `script`, `inline`, `module`, `stream` or `refused`, with its text, module
    and operands."""
    return READERS[family](words)


def lexical(directory: str, word: str) -> str:
    """Join a word to a directory and fold `.` and `..` textually, as the exec saw the path."""
    parts: list[str] = []
    for part in (word if word.startswith("/") else f"{directory}/{word}").split("/"):
        if part == "..":
            parts = parts[:-1]
        elif part not in ("", "."):
            parts.append(part)
    return "/" + "/".join(parts)


def invocation(instance: dict[str, object]) -> dict[str, object]:
    """What one exec runs: a program, or an image interpreter's script, module, inline or streamed program.

    The interpreter family is the one `Origin.identify` found for the program's own file; a program
    that is not an image interpreter is judged as a program, whatever its name.
    """
    program = str(instance["program"])
    base = MULTIARCH.sub("", Path(program).name)
    family = instance.get("family")
    words = list(instance["argv"])
    if family is None:
        return {"kind": "program", "name": base, "path": program, "args": words[1:]}
    read = operands(str(family), words)
    kind, rest = read["kind"], list(read["rest"])
    if kind == "refused":
        return {"kind": "refused", "name": base, "path": program, "family": family, "reason": read["reason"]}
    if kind == "module":
        return {"kind": "module", "name": str(read["module"]).split(".")[0], "path": str(read["module"]),
                "family": family}
    if kind == "inline":
        return {"kind": "inline", "name": base, "path": program, "family": family,
                "sha256": hashlib.sha256(str(read["text"]).encode("utf-8", "surrogateescape")).hexdigest()}
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
