#!/usr/bin/env python3
"""Compare C sources token for token, independent of any comment.

Comments are removed by the C preprocessor in pre-processed mode
(gcc -fpreprocessed -dD -E -P), which strips comments without expanding
macros or includes. The remainder is split into C tokens by a regex lexer
and compared as (token) sequences. Usage:
  token_identity.py <milan-git-dir> <milan-rev> <stack-git-dir> <stack-rev>...
"""
import re, subprocess, sys, tempfile, os

PAIRS = [("sw/firmware/ctrl/adp/adp.c", "src/adp.c"),
         ("sw/firmware/ctrl/adp/adp.h", "include/adp.h"),
         ("sw/firmware/ctrl/acmp/acmp.c", "src/acmp.c"),
         ("sw/firmware/ctrl/acmp/acmp.h", "include/acmp.h"),
         ("sw/firmware/ctrl/maap/maap.c", "src/maap.c"),
         ("sw/firmware/ctrl/maap/maap.h", "include/maap.h"),
         ("sw/firmware/ctrl/wire/wire.h", "include/wire.h")]
TOK = re.compile(r'''
 [A-Za-z_][A-Za-z0-9_]* | \.?[0-9](?:[eEpP][+-]|[A-Za-z0-9_.])* |
 "(?:\\.|[^"\\\n])*" | '(?:\\.|[^'\\\n])*' |
 %:%:|\.\.\.|<<=|>>=|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[*/%+\-&^|]=|\#\#|<:|:>|<%|%>|%: |
 [][(){}.&*+\-~!/%<>^|?:;=,\#]
''', re.X)

def show(gitdir, rev, path):
    r = subprocess.run(["git", "-C", gitdir, "show", f"{rev}:{path}"], capture_output=True)
    if r.returncode: return None
    return r.stdout

def tokens(src):
    with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as f:
        f.write(src); name = f.name
    try:
        out = subprocess.run(["gcc", "-fpreprocessed", "-dD", "-E", "-P", "-x", "c", name],
                             capture_output=True, check=True).stdout.decode()
    finally:
        os.unlink(name)
    out = out.replace("\\\n", " ")
    toks, pos = [], 0
    for line in out.splitlines():
        line = line.strip()
        i = 0
        while i < len(line):
            if line[i].isspace(): i += 1; continue
            m = TOK.match(line, i)
            if not m: raise SystemExit(f"lex error at {line[i:i+20]!r}")
            toks.append(m.group(0).strip()); i = m.end()
    return toks

def main():
    mg, mrev, sg = sys.argv[1:4]; revs = sys.argv[4:]
    base = {m: tokens(show(mg, mrev, m)) for m, _ in PAIRS}
    rc = 0
    for rev in revs:
        full = subprocess.run(["git", "-C", sg, "rev-parse", rev], capture_output=True, text=True).stdout.strip()
        print(f"## stack {full}")
        for m, s in PAIRS:
            data = show(sg, rev, s)
            if data is None:
                print(f"ABSENT {s}"); continue
            t = tokens(data)
            same = t == base[m]
            print(f"{'SAME' if same else 'DIFFERENT'} {len(base[m])}/{len(t)} tokens {m} vs {s}")
    return rc

if __name__ == "__main__":
    sys.exit(main())
