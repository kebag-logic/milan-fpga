#!/usr/bin/env python3
"""Show that a SystemVerilog file changed only in comments between two revisions.

Usage: comment_only.py GITDIR OLD NEW PATH
Strips // and /* */ comments (outside string literals) from both blobs, splits the rest into
tokens, and compares the token streams. Also lists every changed comment line that carries a
tool directive keyword, since a directive inside a comment is not inert. Prints JSON; exit 0
only when the token streams are equal and no changed line carries a directive.
"""
import difflib
import json
import re
import subprocess
import sys

DIRECTIVE = re.compile(r"\b(synthesis|synopsys|pragma|translate_(on|off)|verilator|lint_(on|off)|"
                       r"full_case|parallel_case|keep|dont_touch|mark_debug|ram_style|rom_style)\b"
                       r"|^\s*`", re.I)
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\w+|\S')


def strip(text):
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1])
            i = j + 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            out.append(" ")
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def blob(gitdir, rev, path):
    return subprocess.run(["git", "-C", gitdir, "show", f"{rev}:{path}"], capture_output=True,
                          check=True, text=True).stdout


def main():
    gitdir, old, new, path = sys.argv[1:5]
    a, b = blob(gitdir, old, path), blob(gitdir, new, path)
    ta, tb = TOKEN.findall(strip(a)), TOKEN.findall(strip(b))
    changed = [line[1:] for line in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0)
               if line[:1] in "+-" and not line.startswith(("+++", "---"))]
    non_comment = [line for line in changed if line.strip() and not line.strip().startswith("//")]
    directives = [line for line in changed if DIRECTIVE.search(line)]
    result = {"path": path, "old": old, "new": new, "old_tokens": len(ta), "new_tokens": len(tb),
              "token_streams_equal": ta == tb, "changed_lines": len(changed),
              "changed_lines_not_starting_with_comment": non_comment,
              "changed_lines_with_directive_keyword": directives}
    print(json.dumps(result, indent=1))
    sys.exit(0 if ta == tb and not directives and not non_comment else 1)


if __name__ == "__main__":
    main()
