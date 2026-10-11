"""tokens.py BASE STACK : compare milan-fpga's removed core copies (BASE tree) with tsn-c-stack (STACK) as
token streams. Comments are removed by the C preprocessor in -fpreprocessed mode (no macro expansion);
the remaining text is split into C tokens (identifiers, numbers, strings, chars, punctuators)."""
import re, subprocess, sys
from pathlib import Path
PAIRS = [("sw/firmware/ctrl/adp/adp.c", "src/adp.c"), ("sw/firmware/ctrl/adp/adp.h", "include/adp.h"),
         ("sw/firmware/ctrl/acmp/acmp.c", "src/acmp.c"), ("sw/firmware/ctrl/acmp/acmp.h", "include/acmp.h"),
         ("sw/firmware/ctrl/maap/maap.c", "src/maap.c"), ("sw/firmware/ctrl/maap/maap.h", "include/maap.h"),
         ("sw/firmware/ctrl/wire/wire.h", "include/wire.h")]
TOK = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_]\w*|\.?\d(?:[\w.]|[eEpP][+-])*|'
                 r'<<=|>>=|\.\.\.|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%&|^!=<>]=|##|\S')
def toks(path):
    out = subprocess.run(["gcc", "-x", "c", "-fpreprocessed", "-dD", "-E", "-P", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return TOK.findall(out)
base, stack = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
for a, b in PAIRS:
    ta, tb = toks(base / a), toks(stack / b)
    same = ta == tb
    bad += not same
    print(f"{'SAME' if same else 'DIFFERENT'} {len(ta)}/{len(tb)} tokens: {a} vs {b}")
print("rc", 1 if bad else 0)
sys.exit(1 if bad else 0)
