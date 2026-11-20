#!/usr/bin/env python3
"""sweep_classify.py REPO BASE HEAD: every file BASE..HEAD changes, with its comments removed and its string literals
masked, must be the same code at both commits (R865-4-R1/R2: a comment-only commit). Per file type:

  .py              tokenize: COMMENT tokens dropped, each STRING token replaced by one placeholder, the rest compared
                   token for token (so a docstring, a check's text or a message may change, and nothing else);
  .c .h .cpp .hpp  comments (// and /* */, outside string and character literals) removed and each string literal
                   masked, then the remaining text compared with whitespace collapsed;
  .txt             the hot list: every line not starting with '#' compared;
  .md              documentation, listed and not compared.

For each string literal that changed (Python) it prints both values, so a reader sees which message texts moved.
Exit 0 when every compared file is the same code, 1 when one is not, 2 when a file type is not covered."""
import io
import re
import subprocess
import sys
import tokenize

repo, base, head = sys.argv[1:4]


def show(rev: str, path: str) -> str:
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True, text=True,
                          check=True).stdout


def py_code(text: str) -> tuple[list[tuple[int, str]], list[str]]:
    code, strings = [], []
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type == tokenize.COMMENT or tok.type in (tokenize.NL, tokenize.NEWLINE):
            continue
        if tok.type == tokenize.STRING:
            strings.append(tok.string)
            code.append((tok.type, '<STRING>'))
        else:
            code.append((tok.type, tok.string))
    return code, strings


C_TOKENS = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|\s+|.', re.S)


def c_code(text: str) -> str:
    out = []
    for m in C_TOKENS.finditer(text):
        t = m.group(0)
        if t.startswith('//') or t.startswith('/*'):
            out.append(' ')
        elif t.startswith('"'):
            out.append('"<STRING>"')
        elif t.isspace():
            out.append(' ')
        else:
            out.append(t)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


files = subprocess.run(['git', '-C', repo, 'diff', '--name-only', base, head], capture_output=True, text=True,
                       check=True).stdout.split()
rc = 0
print(f'sweep_classify.py {base}..{head}: {len(files)} files')
for f in files:
    old, new = show(base, f), show(head, f)
    lines = f'{old.count(chr(10))} -> {new.count(chr(10))} lines'
    if f.endswith('.py'):
        (co, so), (cn, sn) = py_code(old), py_code(new)
        same = co == cn
        moved = [(a, b) for a, b in zip(so, sn) if a != b]
        print(f'{"SAME CODE" if same else "CODE DIFFERS"} {f} ({lines}; python tokens with comments dropped and '
              f'{len(so)} string literals masked; {len(moved)} literal(s) changed)')
        for a, b in moved:
            print(f'    string: {a!r}\n        -> {b!r}')
    elif f.endswith(('.c', '.h', '.cpp', '.hpp')):
        same = c_code(old) == c_code(new)
        print(f'{"SAME CODE" if same else "CODE DIFFERS"} {f} ({lines}; C/C++ with comments removed and string '
              f'literals masked)')
    elif f.endswith('.txt'):
        same = [l for l in old.splitlines() if not l.startswith('#')] == \
               [l for l in new.splitlines() if not l.startswith('#')]
        print(f'{"SAME CODE" if same else "CODE DIFFERS"} {f} ({lines}; every line not starting with #)')
    elif f.endswith('.md'):
        print(f'DOCUMENTATION {f} ({lines}; not compared)')
        continue
    else:
        print(f'NOT COVERED {f}')
        rc = max(rc, 2)
        continue
    if not same:
        rc = max(rc, 1)
print(f'RESULT: {"PASS: every compared file is the same code" if rc == 0 else "FAIL"}')
sys.exit(rc)
