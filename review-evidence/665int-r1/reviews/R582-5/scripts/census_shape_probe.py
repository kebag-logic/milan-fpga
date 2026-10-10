#!/usr/bin/env python3
"""census_shape_probe.py - run the publication census over other build shapes.

The census elaborates milan_datapath once: the include directory of
``syn/yosys/run.sh --emit milan_datapath`` (configs/generated/endstation_arty_current)
and the datapath's default parameters. A shipped image is built from another
shape header and the builder's parameter overrides. This probe re-runs the
census's own findings() with (a) a shape's generated header directory in place
of the recipe's first include directory and (b) the datapath's parameter
defaults rewritten to that shape's values, then prints every read the census
classifies and every finding, so a reviewer can compare the read set across shapes.

Usage: census_shape_probe.py <checkout> <shape> [NAME=VALUE ...]
The checkout is not modified: the rewritten datapath is passed as the census's
own in-memory overlay (a planted copy), exactly as its self-test plants.
"""
import re
import sys
from dataclasses import replace
from pathlib import Path


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    shape = sys.argv[2]
    params = dict(a.split("=", 1) for a in sys.argv[3:])
    sys.path.insert(0, str(repo / "sw/mailbox"))
    import census_elab as ce
    import publication_census as pc
    import mailbox_model

    base = ce.recipe()
    inc = list(base.incdirs)
    if shape != "default":
        new = repo / "configs/generated" / shape
        assert new.is_dir(), new
        assert inc[0].name == "endstation_arty_current", inc[0]
        inc[0] = new
    rcp = ce.Recipe(base.defines, tuple(inc), base.sources)
    ce.recipe = lambda: rcp          # census_elab's own global lookups
    pc.recipe = lambda: rcp
    ce.tracked_openers.cache_clear()

    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    text = src.datapath
    for name, value in params.items():
        pat = re.compile(rf"(\n\s*parameter\s+(?:int(?:\s+unsigned)?|bit|logic(?:\s*\[[^\]]*\])?)\s+{name}\s*=\s*)([^,\n]+?)(\s*(?:,|\n\s*\)))")
        n = len(pat.findall(text))
        assert n == 1, (name, n)
        text = pat.sub(lambda m: m.group(1) + value + m.group(3), text, count=1)
    src = replace(src, datapath=text)
    known = pc.fields(mailbox_model.load())
    out, sv = pc.findings(src, pc.CENSUS, known)
    print(f"shape={shape} params={params}")
    print(f"population={len(sv.population)} unread={len(sv.unread)} reads={len(sv.reads)} netlist={sv.size}")
    for r in sv.reads:
        row = pc.CENSUS.get((r.wire, r.consumer))
        kinds = ",".join(sorted({k for k, _ in r.ends}))
        print(f"READ {r.wire} -> {r.consumer} ends={kinds} row={row.kind if row else 'UNMAPPED'}")
    for f in out:
        print(f"FINDING {f}")
    print(f"RESULT {'PASS' if not out else 'FAIL'} findings={len(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
