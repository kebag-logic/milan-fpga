#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""One parser for SystemVerilog module headers - ports, parameters, comments.

Two code-quality gates read module port lists: the Rule 4 unit-in-the-name
ratchet (scripts/measure_naming.py) and the Rule 5 port-contract gate
(scripts/check_port_contracts.py). Their first versions each carried a private
regex, and review found the same defect in both: a header of the form
`module X import pkg::*; #(...) (...)` ended at the import's `;`, so every
port of every module written that way - 23 of them, all three top-level
integration modules and most of both processors - was invisible. Rule 3 says a
production fact has one definition; the parse of "what ports does this module
declare" is that kind of fact, so it lives here and both gates import it.

What is parsed. For every `module` in a source: the header text from the
keyword to the `;` that closes its port list, with block and ordinary line
comments blanked and `//!` documentation kept. Inside it, each declaration
chunk - starting at `input`/`output`/`inout`, `parameter`/`localparam`, or an
`interface.modport name` port - yields every name it declares, across lines
and shared declarations, with its documentation and whether it is a quantity
(any packed or unpacked dimension, an unsized type such as `int`, a package or
interface type, or a parameter).

Documentation attribution is the bundle rule: a `//!` on a name's own line
documents every name declared on that line; a run of standalone `//!` lines
documents the undocumented names that follow until one carries its own
comment, which ends the bundle. Function and task arguments inside module
bodies are not boundaries and are never returned.

    from sv_ports import declarations
    for module, name, doc, multibit, kind in declarations(text): ...
    kind in {"port", "param", "iface"}; doc == "" when undocumented
"""

import re

_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_LINE_COMMENT = re.compile(r"//(?!!)[^\n]*")      # ordinary comments; `//!` kept
_MODULE = re.compile(r"^\s*module\s+([A-Za-z_]\w*)", re.M)
_DIRECTION = re.compile(r"\b(input|output|inout)\b")
_PARAM_KW = re.compile(r"\b(?:parameter|localparam)\b")
_TYPE_WORDS = {"wire", "logic", "reg", "var", "bit", "int", "integer", "byte",
               "shortint", "longint", "signed", "unsigned", "tri", "real",
               "shortreal", "time", "supply0", "supply1", "type"}
_UNSIZED_TYPES = {"int", "integer", "byte", "shortint", "longint", "real",
                  "shortreal", "time"}
_IDENT = re.compile(r"^[A-Za-z_]\w*$")


def _blank_keep_newlines(m):
    return "".join(c if c == "\n" else " " for c in m.group(0))


def module_headers(text):
    """[(module_name, header_text, first_line_no)] for each module in `text`.

    The header runs from `module` to the `;` that ends the port list, with
    block and ordinary line comments blanked and `//!` comments kept."""
    code = _BLOCK_COMMENT.sub(_blank_keep_newlines, text)
    code = _LINE_COMMENT.sub(_blank_keep_newlines, code)
    out = []
    for m in _MODULE.finditer(code):
        i, depth, seen_paren = m.end(), 0, False
        while i < len(code):
            ch = code[i]
            if ch == "(":
                depth += 1; seen_paren = True
            elif ch == ")":
                depth -= 1
            elif ch == ";" and depth == 0:
                # `module X import pkg::*;` - the import's `;` is not the end
                # of the header; the port list follows it
                if not seen_paren and re.search(r"\bimport\b[^;]*$", code[m.end():i]):
                    i += 1
                    continue
                break
            elif ch == "/" and code.startswith("//!", i):
                j = code.find("\n", i)
                i = len(code) if j < 0 else j
                continue
            i += 1
        out.append((m.group(1), code[m.start():i], code[:m.start()].count("\n") + 1))
    return out


_IFACE_PORT = re.compile(r"^[ \t]*([A-Za-z_]\w*\.[A-Za-z_]\w*)[ \t]+[A-Za-z_]\w*", re.M)


def _split_decls(header):
    """Split a header into declaration chunks: each starts at a direction or
    parameter keyword, or at an `interface.modport name` port, and runs to the
    next such start. Returns (preamble, [(kind, chunk)]) with kind in
    {'port', 'param', 'iface'}; the preamble is the text before the first
    declaration, where a group `//!` comment may already be in force."""
    marks = [(m.start(), "port") for m in _DIRECTION.finditer(header)]
    marks += [(m.start(), "param") for m in _PARAM_KW.finditer(header)]
    marks += [(m.start(1), "iface") for m in _IFACE_PORT.finditer(header)]
    marks.sort()
    chunks = []
    for k, (pos, kind) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(header)
        chunks.append((kind, header[pos:end]))
    preamble = header[:marks[0][0]] if marks else header
    return preamble, chunks


def _group_comment_in(text):
    """The last run of consecutive standalone `//!` lines in `text`, joined,
    or None."""
    found, run = None, []
    for line in text.split("\n"):
        if "//!" in line and not line.split("//!", 1)[0].strip():
            run.append(line.split("//!", 1)[1].strip())
            found = " ".join(run)
        elif line.strip():
            run = []
    return found


def _parse_chunk(kind, chunk, carried_doc):
    """Parse one declaration chunk into [(name, doc, multibit)].

    `carried_doc` is a standalone `//!` group comment still in force; the
    return also carries the group comment this chunk leaves in force."""
    lines = chunk.split("\n")
    # standalone `//!` lines inside the chunk are group comments for what follows
    docs_by_line, group_after = {}, None
    code_lines = []
    run = []
    for ln, line in enumerate(lines):
        if "//!" in line:
            code, doc = line.split("//!", 1)
            if not code.strip():
                run.append(doc.strip())            # standalone: applies to what follows
                group_after = " ".join(run)
                code_lines.append("")
                continue
            run = []
            docs_by_line[ln] = doc.strip()
            code_lines.append(code)
        else:
            if line.strip():
                run = []
            code_lines.append(line)
    # the declaration's own line is the line of its first name; a same-line
    # `//!` documents every name declared on that line
    joined = "\n".join(code_lines)
    # strip the closing `)` of a port list and any default value
    joined = joined.replace(")", " ").replace("(", " ")
    if kind != "iface":
        kw = _DIRECTION if kind == "port" else _PARAM_KW
        joined = kw.sub(" ", joined, count=1)
    # dimensions: packed before the name, unpacked after it; record presence
    has_dims = bool(re.search(r"\[[^\]]*\]", joined))
    joined_nodims = re.sub(r"\[[^\]]*\]", " ", joined)
    # split names by comma, keep track of which line each piece starts on
    names, line_of = [], {}
    pos = 0
    pieces = joined_nodims.split(",")
    offset = 0
    first_piece_typed = None
    for idx, piece in enumerate(pieces):
        piece_line = joined_nodims[:offset].count("\n")
        offset += len(piece) + 1
        piece = piece.split("=")[0]                       # default value
        toks = [t for t in piece.replace("\n", " ").split() if t]
        if not toks:
            continue
        if idx == 0:
            ident_toks = [t for t in toks if _IDENT.match(t) or "::" in t or "." in t]
            if not ident_toks:
                continue
            name = ident_toks[-1]
            typ = [t for t in ident_toks[:-1] if t not in _TYPE_WORDS]
            first_piece_typed = (bool(typ) or any(t in _UNSIZED_TYPES for t in ident_toks[:-1]))
        else:
            ident_toks = [t for t in toks if _IDENT.match(t)]
            if not ident_toks:
                continue
            name = ident_toks[-1]
        if not _IDENT.match(name):
            continue
        # the name's own line: the line on which the name token sits
        name_line = piece_line + piece[:piece.rfind(name)].count("\n") if name in piece else piece_line
        names.append(name)
        line_of[name] = name_line
    multibit = has_dims or bool(first_piece_typed) or kind in ("param", "iface")
    rows, any_own = [], False
    for name in names:
        ln = line_of[name]
        doc = docs_by_line.get(ln)
        if doc is None and docs_by_line and len(names) == 1:
            # one name, one declaration: its trailing comment may sit on the
            # last line of a declaration split across lines
            doc = docs_by_line.get(max(docs_by_line))
        own = doc is not None
        any_own |= own
        rows.append((name, (doc if own else carried_doc) or "", multibit, own))
    # what stays in force for the next declaration: a standalone `//!` after
    # this one starts a new bundle; a declaration with its own comment ends
    # the bundle; otherwise the group comment carries on
    if group_after is not None:
        nxt = group_after
    elif any_own:
        nxt = None
    else:
        nxt = carried_doc
    return rows, nxt


def declarations(text):
    """[(module, name, doc, multibit, kind)] for every port/parameter in `text`."""
    out = []
    for module, header, _ in module_headers(text):
        preamble, chunks = _split_decls(header)
        carried = _group_comment_in(preamble)
        for kind, chunk in chunks:
            rows, carried = _parse_chunk(kind, chunk, carried)
            for name, doc, multibit, _own in rows:
                out.append((module, name, doc, multibit, kind))
    return out


