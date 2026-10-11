#!/usr/bin/env python3
"""Compare removed milan-fpga core copies (at a base commit) with tsn-c-stack files at
given revisions, token for token (comments stripped by the C preprocessor's lexer rules,
whitespace collapsed). Usage: pin_tokens.py <milan-repo> <base> <stack-repo> <rev>..."""
import re, subprocess, sys, hashlib
repo, base, stack, revs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
PAIRS = [("sw/firmware/ctrl/adp/adp.c", "src/adp.c"), ("sw/firmware/ctrl/adp/adp.h", "include/adp.h"),
         ("sw/firmware/ctrl/acmp/acmp.c", "src/acmp.c"), ("sw/firmware/ctrl/acmp/acmp.h", "include/acmp.h"),
         ("sw/firmware/ctrl/maap/maap.c", "src/maap.c"), ("sw/firmware/ctrl/maap/maap.h", "include/maap.h"),
         ("sw/firmware/ctrl/wire/wire.h", "include/wire.h"),
         ("sw/firmware/ctrl/test/acmp_fake.hpp", "tests/acmp_fake.hpp"),
         ("sw/firmware/ctrl/test/test_acmp.cpp", "tests/test_acmp.cpp"),
         ("sw/firmware/ctrl/test/test_adp_reentry.cpp", "tests/test_adp_reentry.cpp"),
         ("sw/firmware/ctrl/test/test_maap_debug.cpp", "tests/test_maap_debug.cpp")]
TOK = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|\S', re.S)
def show(r, ref, path):
    p = subprocess.run(["git", "-C", r, "show", f"{ref}:{path}"], capture_output=True)
    return p.stdout.decode() if p.returncode == 0 else None
def toks(src):
    out=[]; 
    for m in TOK.finditer(src):
        t=m.group(0)
        if t.startswith('//') or t.startswith('/*'): continue
        out.append(t)
    # join single chars back into words to be robust: compare the stream of non-space chars + literals
    return out
def lines_nc(src):
    s = re.sub(r'/\*.*?\*/', lambda m: '\n'*m.group(0).count('\n'), src, flags=re.S)
    s = re.sub(r'//[^\n]*', '', s)
    return [l.rstrip() for l in s.split('\n')]
rc = 0
for rev in revs:
    print(f"== stack {rev}")
    for a, b in PAIRS:
        x, y = show(repo, base, a), show(stack, rev, b)
        if x is None or y is None:
            print(f"  MISSING {a if x is None else ''} {b if y is None else ''}"); rc = 1; continue
        tx, ty = toks(x), toks(y)
        same = tx == ty
        ln = [l for l in lines_nc(x) if l.strip()] == [l for l in lines_nc(y) if l.strip()]
        print(f"  {'TOKEN-SAME' if same else 'TOKEN-DIFF'} {'LINES-SAME' if ln else 'LINES-DIFF'} {a} ~ {b} "
              f"sha(base)={hashlib.sha256(x.encode()).hexdigest()[:12]} sha(stack)={hashlib.sha256(y.encode()).hexdigest()[:12]}")
        if not same:
            import difflib
            for d in list(difflib.unified_diff(tx, ty, lineterm='', n=2))[:20]: print('     ', d)
sys.exit(rc)
