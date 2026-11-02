#!/usr/bin/env python3
"""usage: emit_table.py COLLECTED_JSON NAMES_JSON EXPECT_JSON > table.py

Print the MUTANTS literal for scripts/process_test_support.py: one entry per
distinct mutated text, named by NAMES_JSON (text_sha -> name) and expecting
EXPECT_JSON (name -> [control or null, words or reason])."""
import json, sys

groups = json.load(open(sys.argv[1]))
names = json.load(open(sys.argv[2]))
expect = json.load(open(sys.argv[3]))
WIDTH = 118


def pieces(text: str, indent: int) -> list[str]:
    """json.dumps() of text, split at newlines into concatenated literals that fit."""
    whole = json.dumps(text)
    if indent + len(whole) <= WIDTH - 2:
        return [whole]
    parts, current = [], ""
    for line in text.splitlines(keepends=True):
        if current and indent + len(json.dumps(current + line)) > WIDTH - 2:
            parts.append(current)
            current = ""
        current += line
    parts.append(current)
    out = []
    for part in parts:
        r = json.dumps(part)
        while indent + len(r) > WIDTH - 2:
            # split long single lines at a space
            cut = part.rfind(" ", 0, WIDTH - indent - 10)
            out.append(json.dumps(part[:cut]))
            part = part[cut:]
            r = json.dumps(part)
        out.append(r)
    return out


order = sorted(groups, key=lambda g: list(names).index(g["text_sha"]))
print("MUTANTS: dict[str, tuple] = {")
for g in order:
    name = names[g["text_sha"]]
    control, words = expect.get(name, [None, "PENDING"])
    head = f'    "{name}": ({json.dumps(control) if control else "None"}, '
    lines = []
    w = pieces(words, len(head))
    lines.append(head + w[0] + ("" if len(w) == 1 else ""))
    for extra in w[1:]:
        lines.append(" " * len(head) + extra)
    lines[-1] += ","
    for old, new in g["edits"]:
        ind = 8
        o, n = pieces(old, ind + 1), pieces(new, ind + 1)
        if len(o) == 1 and len(n) == 1 and ind + 1 + len(o[0]) + 2 + len(n[0]) + 2 <= WIDTH:
            lines.append(" " * ind + f"({o[0]}, {n[0]}),")
        else:
            lines.append(" " * ind + "(" + o[0])
            for extra in o[1:]:
                lines.append(" " * (ind + 1) + extra)
            lines[-1] += ","
            lines.append(" " * (ind + 1) + n[0])
            for extra in n[1:]:
                lines.append(" " * (ind + 1) + extra)
            lines[-1] += "),"
    lines[-1] = lines[-1][:-1] + "),"
    print("\n".join(lines))
print("}")
