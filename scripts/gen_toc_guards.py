#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The DECISION SITES of `gen_toc.py`'s walk, enumerated from its source.

WHICH MODULE IS WHICH. `gen_toc.py` owns block classification: the walk,
every rule that decides what a line is, and the runner. `gen_toc_cases.py`
holds the case tables. THIS module holds neither. It reads a Python syntax
tree and answers a question about SOURCE, not about Markdown: which
positions of the walk read a character class, and whether each reads it
from `CLASSES` or refuses the page instead. No rule moved here, and
`gen_toc._owner_guards` is applied to this module exactly as it is to the
case tables, so the promise is checked and not asserted: this file imports
no expression engine and holds no compiled expression.

Split off in round 10 of PR #428, for the reason the case tables were split
off in round 6: the module had reached rule 12's long-module ratchet
(docs/development/CODE_QUALITY.md) and the statements two reviews required
would not fit beside it. The constants below come from the walk, so this
module is imported only after `gen_toc` is loaded; `gen_toc._sites()` and
`gen_toc_cases` both do that.
"""
import ast
from collections.abc import Iterator

from gen_toc import CLASSES, REFUSED, WALK_ROOTS, _PYTHON_CLASSES, _STRIPS


def _pattern_texts(node: ast.AST, assign: dict,
                   seen: frozenset = frozenset()) -> Iterator[str]:
    """Every string an expression reaches, `_cc()`'s own argument apart:
    that call IS the named source, read by name."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id == "_cc":
        return
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node.value
    elif isinstance(node, ast.Name) and node.id in assign \
            and node.id not in seen:
        yield from _pattern_texts(assign[node.id], assign, seen | {node.id})
    for child in ast.iter_child_nodes(node):
        yield from _pattern_texts(child, assign, seen)


def _class_guards(source: str) -> tuple[list[str], list[str]]:
    r"""Every DECISION SITE of the walk, classified, and what is wrong with
    one that is neither honest kind.

    A site is a position that reads a character class: a compiled
    expression of this module, or a call inside the walk that hands a
    string to a scanner. They are ENUMERATED from the syntax tree, out
    from `WALK_ROOTS`, not from a list kept by hand, so a decision added
    later is in the enumeration whether or not anyone remembers it. Each
    is one of two things, and `--sites` prints which. SINGLE SOURCE: every
    class it reads comes from `CLASSES`, whose bodies the case tables spell
    again, so narrowing or widening one fails an arm. REFUSAL: it spells
    Python's own whitespace, whose excess over the renderer's BLANK is
    exactly `REFUSED`, so a page that could tell the two apart is refused
    before the site is asked -- which holds the site only where the
    renderer's class AT THAT POSITION is the blank, and
    `gen_toc._type_1_end` says at the site why it is not held there.
    Anything else is a note and the self-test fails: a class inline, Python's
    `\d`, `\w`, `\W` or `\D`, a `str.is*()` test, or a strip with a class
    of its own ([R85] F1 and F2, [R86] F1 and F2, round 9 on PR #428).

    WHAT IT CANNOT SEE, measured and not supposed ([R85] F3, [R86] F3,
    round 10): a binding that is no `ast.Assign`; `from re import compile`;
    a call through an alias or a lambda; a membership test; a `str` method
    other than the strips; a class respelled as escapes, reached through
    `getattr`, built at run time or imported; a rule the walk never calls;
    and the FLAGS of a match, `ASCII_FOLD` included. A site LOST to any of
    those moves the number `--sites` prints, which the case tables spell
    and hold, so the loss fails an arm although this guard is silent. It is
    a structural proxy; the arms and the refusal hold the rest.
    """
    tree = ast.parse(source)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assign = {t.id: n.value for n in tree.body if isinstance(n, ast.Assign)
              for t in n.targets if isinstance(t, ast.Name)}
    notes = [f"the walk root {root!r} is no function of this module"
             for root in WALK_ROOTS if root not in funcs]
    walk, queue = set(), [root for root in WALK_ROOTS if root in funcs]
    while queue:                        # the calls out of the roots
        name = queue.pop()
        if name not in walk:
            walk.add(name)
            queue += [c.func.id for c in ast.walk(funcs[name])
                      if isinstance(c, ast.Call)
                      and isinstance(c.func, ast.Name) and c.func.id in funcs]

    def judge(where: str, node: ast.AST) -> str:
        """One site, classified; a class of its own is a note."""
        kind = "single source"
        for text in _pattern_texts(node, assign):
            kind = "refusal" if r"\s" in text or r"\S" in text else kind
            notes.extend(
                f"{where} spells {own}, which is Python's class and not "
                "the renderer's"
                for own in (r"\d", r"\w", r"\W", r"\D") if own in text)
            for i, char in enumerate(text):
                if char in REFUSED or (char in CLASSES["blank"] and not (
                        text[i - 1:i].isalnum()
                        and text[i + 1:i + 2].isalnum())):
                    notes.append(f"{where} spells a blank of its own; every "
                                 "class the walk reads is in CLASSES")
                    break
        return f"{where}: {kind}"

    sites = [judge(name, node) for name, node in assign.items()
             if any(isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Attribute)
                    and c.func.attr == "compile" for c in ast.walk(node))]
    for name in walk:
        for call in ast.walk(funcs[name]):
            if not isinstance(call, ast.Call) \
                    or not isinstance(call.func, ast.Attribute):
                continue
            attr, where = call.func.attr, f"{name}() {call.func.attr}()"
            if attr in _PYTHON_CLASSES:
                notes.append(f"{where} asks Python what a character is; the "
                             "renderer's answer is in CLASSES")
            elif (attr in _STRIPS or attr == "split") and not call.args:
                sites.append(f"{where}: refusal")
            elif attr in _STRIPS:
                arg = call.args[0]
                if isinstance(arg, ast.Subscript) \
                        and isinstance(arg.value, ast.Name) \
                        and arg.value.id == "CLASSES":
                    sites.append(f"{where}: single source")
                else:
                    notes.append(f"{where} strips a class of its own")
            elif isinstance(call.func.value, ast.Name) \
                    and call.func.value.id == "re" and call.args:
                sites.append(judge(where, call.args[0]))
    return sorted(sites), notes
