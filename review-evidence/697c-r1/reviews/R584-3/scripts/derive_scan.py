#!/usr/bin/env python3
"""R584-3: the gate's derived builders, modes, values, Makefiles and C++ sources, compared with a raw text scan of
every -D/-U token in every builder; then every .cpp/.cc/.cxx name a builder writes that the gate cannot resolve.
Run from <checkout>/sw/firmware/ctrl/test:  python3 -B <this> """
import ast, re, sys
sys.path.insert(0, "../../gtest")
import ctrl_configs as c
texts = c.builder_texts()
print("BUILDERS", len(texts)); [print("  ", c.rel(p)) for p in sorted(texts)]
u, comp = c.derive()
print("MODES", u); print("COMPUTED", comp); print("MAKEFILES", [c.rel(p) for p in c.makefiles()])
cx = c.cxx_sources(); print("CXX", len(cx)); [print("  ", c.rel(p)) for p in sorted(cx)]
pat = re.compile(r"(?<![\w-])-([DU])\s*([A-Za-z_]\w*)")
raw = {}
for p, t in texts.items():
    for m in pat.finditer(t):
        raw.setdefault(m[2], set()).add(c.rel(p))
print("RAW-NOT-DERIVED")
for k, v in sorted(raw.items()):
    if k not in u and k not in comp and not c.RESERVED.match(k):
        print("  ", k, sorted(v))
print("UNRESOLVED C++ NAMES")
for path, text in texts.items():
    names = ([n.value for n in ast.walk(ast.parse(text)) if isinstance(n, ast.Constant) and isinstance(n.value, str)
              and n.value.endswith(c.CXX_SUFFIXES)] if path.suffix == ".py"
             else [w for w in text.replace("\\\n", " ").split() if w.endswith(c.CXX_SUFFIXES)])
    for name in names:
        bases = (path.parent, c.HERE, c.STACK, c.ROOT, c.PP)
        if not any((b / name.removeprefix(c.STACK_PREFIX) if b == c.STACK else b / name).is_file() for b in bases):
            print("  ", c.rel(path), repr(name)[:120])
