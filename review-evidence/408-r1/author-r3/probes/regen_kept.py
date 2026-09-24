import sys, re, subprocess, tempfile, os
from pathlib import Path
sys.path.insert(0, "$LANES/408-409-boot-gate-retire/sw/builder")
import test_builder as tb
GCC = os.path.expanduser("~/milan-fpga-management/2026-09-23/408-a248/sdk-home/br-milan-rv32/host/bin/riscv32-linux-gcc")
DRIVER = []  # empty driver (rv32 native); matches rv32_drivers[0]
corpus = tb._lexer_generated_corpus()
outcomes = tb._LEXER_OUTCOMES
rev = {v: k for k, v in outcomes.items()}
texts = [fw for _l, fw, _r in corpus]
line_marker_re = re.compile(r'# \d+ "([^"]*)"')
def measure(texts):
    with tempfile.TemporaryDirectory() as tmp:
        files = []
        for i, t in enumerate(texts):
            p = Path(tmp) / f"lex{i:05d}.c"
            p.write_bytes(t.encode("utf-8"))
            files.append(p)
        batches = [files[a:a+50] for a in range(0, len(files), 50)]
        lines = {}
        refused = set()
        for batch in batches:
            r = subprocess.run([GCC, *DRIVER, "-std=gnu99", "-E", *map(str, batch)],
                               capture_output=True)
            named = set(re.findall(r"(?m)(lex\d{5}\.c):\d+(?::\d+)?: (?:fatal )?error:",
                                   r.stderr.decode("utf-8", errors="replace")))
            assert named or not r.returncode, r.stderr.decode()[:500]
            refused |= named
            name = None
            for line in r.stdout.decode("utf-8", errors="replace").split("\n"):
                m = line_marker_re.match(line)
                if m:
                    name = Path(m.group(1)).name
                    continue
                lines.setdefault(name, []).append(line)
        out = []
        for f in files:
            if f.name in refused:
                out.append(None)
            else:
                out.append(tuple(re.findall(r"\bint\s+(\w+)\s*;", "\n".join(lines.get(f.name, [])))))
        return out
kept = measure(texts)
letters = []
for (label, fw, reader), k in zip(corpus, kept):
    if k not in rev:
        print("UNMAPPED outcome", repr(k), "for", label[:60], file=sys.stderr)
        sys.exit(2)
    letters.append(rev[k])
s = "".join(letters)
print("COUNT", len(s))
# emit as python string literal wrapped at 66 chars like the original
import textwrap
chunks = [s[i:i+66] for i in range(0, len(s), 66)]
print("_LEXER_GENERATED_KEPT = (")
for c in chunks:
    print(f'    "{c}"')
print(")")
open("kept_new.txt","w").write(s)
