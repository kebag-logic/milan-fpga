#!/bin/bash
# The new recorder on small compiles, under a real capture (round 7 smoke test).
set -u
L=$LANES/697-consume
W=$1
PY=$VALIDATION_STORAGE/697c-a583/r5/venv312/bin/python
mkdir -p "$W/src/inc" "$W/sys"
cd "$W/src" || exit 1
printf '#include "h1.h"\n#include <stdbool.h>\nint a;\n' > a.c
printf '#include "h2.h"\n#define H1 1\n' > inc/h1.h
printf '#pragma once\n#define H2 2\n' > inc/h2.h
printf '#include "g.h"\nint x;\n' > f.h
printf '#define G 1\n' > g.h
printf '#include "nope.h"\n' > m.c
printf '#include "inc/h2.h"\n#error stop here\n' > e.c
cap="$W/cap"
run() { "$PY" "$L/sw/firmware/ctrl/test/ctrl_capture.py" --out "$cap" -- "$@"; echo "rc=$?"; }
run gcc -Iinc -include f.h -c a.c -o a.o
run gcc -c m.c -o m.o
run gcc -c e.c -o e.o
run gcc -Wp,-MD,wp.d -Iinc -c a.c -o a2.o
run bash -c 'echo "int y;" | gcc -x c -c - -o s.o'
run gcc -Iinc -c a.c f.h -o a3.o
run clang -Iinc -Werror -include f.h -c a.c -o a4.o
"$PY" -I - "$cap" <<'EOF'
import json, sys
from pathlib import Path
cap = Path(sys.argv[1])
for line in (cap / "records.jsonl").read_text().splitlines():
    r = json.loads(line)
    print(r["tool"], " ".join(r["args"]))
    for path, lang, digest, error in r["sources"]:
        print("   ", path, lang, error or "")
        if digest:
            d = json.loads((cap / "text" / digest).read_text())
            print("      deps:", d["deps"])
            print("      tree:", d["tree"])
EOF
