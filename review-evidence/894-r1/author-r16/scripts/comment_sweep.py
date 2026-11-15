#!/usr/bin/env python3
"""Every hit of a figure the round 12 to 15 moves superseded, at any pace or slice, in every comment and docstring
under sw/ and tb/ (C, C++, headers, assembly and SystemVerilog: // and /* */ text; Python: # comments and module,
class and function docstrings; shell: # comments; Markdown under sw/ and tb/: every line, tables included).
Tokens: argv[1], one a line (the decimal figures: rows, loads, paces, at either point), and the cost figures, each
only on a line naming what it costs (TOKENS_IN_CONTEXT below). Run from the tree's top.
usage: comment_sweep.py TOKENS_FILE"""
import ast
import io
import re
import subprocess
import sys
import tokenize

TOKENS_IN_CONTEXT = [  # (token, the pattern, the line must name)
    ('725', r'(?<![\d.,])725(?![\d])', r'(?i)build|us\b'),
    ('900', r'(?<![\d.,])900 ?(?:us|u)\b', r'.'),
    ('65', r'(?<![\d.,])65(?: ?(?:us|u)\b|\b)', r'(?i)aecp.*(timer|slot)|(timer|slot).*aecp'),
    ('150', r'(?<![\d.,])150(?: ?(?:us|u)\b|\b)', r'LINK'),
    ('250', r'(?<![\d.,])250(?: ?(?:us|u)\b|\b)', r'(?i)SRP_UNIT|srp drain|the drain'),
    ('50', r'(?<![\d.,])50(?: ?(?:us|u)\b|\b)', r'TICK'),
    ('98', r'(?<![\d.,])98(?: ?(?:ms|u)\b|\b)', r'TX_MS|TRANSMIT|tx row'),
    ('30', r'(?<![\d.,])30(?: ?(?:ms|u)\b|\b)', r'TX_MS'),
    ('44', r'(?<![\d.,])44(?: ?(?:ms|u)\b|\b)', r'TX_MS'),
]
C_EXT = ('.c', '.h', '.cpp', '.hpp', '.cc', '.S', '.sv', '.svh', '.v')


def c_comments(text):
    """(line, text) of every // and /* */ comment, strings and character literals skipped."""
    out, i, line, n = [], 0, 1, len(text)
    while i < n:
        ch = text[i]
        if ch == '\n':
            line += 1
        elif ch in '"\'':
            j = i + 1
            while j < n and text[j] != ch and text[j] != '\n':
                j += 2 if text[j] == '\\' else 1
            i = j
        elif text.startswith('//', i):
            j = text.find('\n', i)
            j = n if j < 0 else j
            out.append((line, text[i:j]))
            i = j
            continue
        elif text.startswith('/*', i):
            j = text.find('*/', i + 2)
            j = n if j < 0 else j + 2
            for k, part in enumerate(text[i:j].split('\n')):
                out.append((line + k, part))
            line += text[i:j].count('\n')
            i = j
            continue
        i += 1
    return out


def py_comments(text):
    """(line, text) of every # comment and every module, class and function docstring line."""
    out = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                out.append((tok.start[0], tok.string))
        tree = ast.parse(text)
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return [(i, s) for i, s in enumerate(text.split('\n'), 1)]
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                lines = text.split('\n')[first.lineno - 1:first.end_lineno]
                out.extend((first.lineno + k, s) for k, s in enumerate(lines))
    return out


def sh_comments(text):
    out = []
    for i, s in enumerate(text.split('\n'), 1):
        m = re.search(r'(^|\s)#.*$', s)
        if m:
            out.append((i, m.group(0)))
    return out


def main(argv):
    decimals = [l.split()[0] for l in open(argv[1], encoding='utf-8') if l.strip() and not l.startswith('#')]
    pats = [(t, re.compile(r'(?<![\d.])' + re.escape(t) + r'(?![\d])'), None) for t in decimals]
    pats += [(t, re.compile(p), re.compile(c)) for t, p, c in TOKENS_IN_CONTEXT]
    files = subprocess.run(['git', 'ls-files', 'sw', 'tb'], capture_output=True, text=True, check=True).stdout.split()
    scanned = 0
    for f in files:
        try:
            text = open(f, encoding='utf-8').read()
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        if f.endswith(C_EXT):
            parts = c_comments(text)
        elif f.endswith('.py'):
            parts = py_comments(text)
        elif f.endswith('.sh'):
            parts = sh_comments(text)
        elif f.endswith('.md'):
            parts = list(enumerate(text.split('\n'), 1))
        else:
            continue
        scanned += 1
        for line, s in parts:
            for t, pat, ctx in pats:
                for m in pat.finditer(s):
                    if ctx is None or ctx.search(s):
                        print(f'{t}\t{f}:{line}\t{s[max(0, m.start() - 140):m.end() + 60].strip()}')
    print(f'# scanned {scanned} files under sw/ and tb/', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
