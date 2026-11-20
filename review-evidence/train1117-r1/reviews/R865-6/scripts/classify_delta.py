#!/usr/bin/env python3
"""classify_delta.py REPO OLD NEW [--plant]

For every file OLD..NEW changes: the file's code with comments removed and every string
literal masked must be identical at both commits.  Python is compared by its token stream
(tokenize: COMMENT, NL and NEWLINE dropped, STRING tokens masked as one placeholder, f-strings
masked as a whole), C/C++ by a lexer that drops // and /* */ comments and masks "..." and
'...' literals, and the hot list (*.txt) by its non-'#' lines.  Each changed string literal is
printed old -> new.  Exit 0 when every file is equal code, 1 otherwise.

--plant: also run the same comparison against a planted copy of NEW in which one executable
token of each Python/C file is altered (a number incremented), and require it to be refused.
"""
import io, re, subprocess, sys, tokenize

def show(repo, rev, path):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], check=True,
                          capture_output=True).stdout.decode()

def py_code(text):
    code, strings = [], []
    toks = tokenize.generate_tokens(io.StringIO(text).readline)
    depth = 0
    for t in toks:
        name = tokenize.tok_name[t.type]
        if name in ('COMMENT', 'NL', 'NEWLINE', 'INDENT', 'DEDENT', 'ENCODING', 'ENDMARKER'):
            if name in ('INDENT', 'DEDENT'):
                code.append(name)
            continue
        if name == 'FSTRING_START':
            depth += 1; strings.append(t.string); continue
        if depth:
            strings.append(t.string)
            if name == 'FSTRING_END':
                depth -= 1
                if depth == 0:
                    code.append('<STR>')
            continue
        if name == 'STRING':
            strings.append(t.string); code.append('<STR>'); continue
        code.append(t.string)
    # adjacent literals concatenate: collapse runs so a split string compares equal
    out = []
    for c in code:
        if c == '<STR>' and out and out[-1] == '<STR>':
            continue
        out.append(c)
    return out, strings

C_TOK = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|\s+|.', re.S)

def c_code(text):
    code, strings = [], []
    for m in C_TOK.finditer(text):
        s = m.group(0)
        if s.startswith('//') or s.startswith('/*'):
            code.append(' '); continue
        if s[0] in '"\'':
            strings.append(s); code.append('<STR>'); continue
        code.append(' ' if s.isspace() else s)
    joined = re.sub(r'\s+', ' ', ''.join(code)).strip()
    joined = re.sub(r'(<STR>\s*)+', '<STR> ', joined)
    return joined.split(' '), strings

def txt_code(text):
    return [l for l in text.splitlines() if not l.lstrip().startswith('#')], []

def code_of(path, text):
    if path.endswith('.py'):
        return py_code(text)
    if re.search(r'\.(c|h|cpp|hpp|cc)$', path):
        return c_code(text)
    if path.endswith('.txt'):
        return txt_code(text)
    raise SystemExit(f'unclassified file type: {path}')

def plant_number(path, text):
    """Increment the first number that is an executable token (not in a comment or string)."""
    if path.endswith('.py'):
        lines = text.splitlines(keepends=True)
        for t in tokenize.generate_tokens(io.StringIO(text).readline):
            if t.type == tokenize.NUMBER and t.string.isdigit():
                (r, c) = t.start
                off = sum(len(l) for l in lines[:r - 1]) + c
                return text[:off] + str(int(t.string) + 1) + text[off + len(t.string):], f'number {t.string} at line {r}'
        return None, None
    prev = ''
    for m in C_TOK.finditer(text):
        s = m.group(0)
        if s.isdigit() and not re.match(r'[A-Za-z0-9_]', prev):
            off = m.start()
            line = text.count('\n', 0, off) + 1
            return text[:off] + str((int(s) + 1) % 10) + text[off + 1:], f'digit {s} at line {line}'
        prev = s[-1:] if s else prev
    return None, None

def main():
    repo, old, new = sys.argv[1:4]
    plant = '--plant' in sys.argv
    files = subprocess.run(['git', '-C', repo, 'diff', '--name-only', old, new], check=True,
                           capture_output=True, text=True).stdout.split()
    rc = 0
    for f in files:
        a, b = show(repo, old, f), show(repo, new, f)
        (ca, sa), (cb, sb) = code_of(f, a), code_of(f, b)
        same = ca == cb
        lines_a, lines_b = a.count('\n'), b.count('\n')
        print(f'{"EQUAL-CODE" if same else "CODE DIFFERS"} {f} lines {lines_a}->{lines_b} '
              f'strings {len(sa)}->{len(sb)}')
        if not same:
            rc = 1
        if not f.endswith('.txt'):
            changed = [(x, y) for x, y in zip(sa, sb) if x != y] if len(sa) == len(sb) else None
            if changed is None:
                print(f'  string count changed: {len(sa)} -> {len(sb)} (split or joined literals)')
            else:
                for x, y in changed:
                    print(f'  STRING {x!r}\n      -> {y!r}')
        if plant and not f.endswith('.txt'):
            planted, what = plant_number(f, b)
            if planted is not None:
                cp, _ = code_of(f, planted)
                print(f'  PLANT {f}: executable {what}: {"refused" if cp != ca else "ESCAPED"}')
                if cp == ca:
                    rc = 1
    print(f'END rc={rc}')
    return rc

if __name__ == '__main__':
    sys.exit(main())
