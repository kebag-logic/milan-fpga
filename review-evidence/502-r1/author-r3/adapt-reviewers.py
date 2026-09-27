"""Rebind only the old anchor; preserve every published replacement body.
This is a separately reported author replay, not an unchanged reviewer run.
"""
from pathlib import Path
import runpy, sys
script=Path(sys.argv[1])
ns=runpy.run_path(str(script))
old=ns["LIVE"]
new="  assign aecp_live_wr_w = aecp_name_wr_w\n                        | amap_live_wr_i;"
for name,spec in ns["MUTANTS"].items():
    if spec is not None:
        anchor,replacement=spec
        if anchor == old:
            ns["MUTANTS"][name]=(new,replacement)
sys.argv=sys.argv[1:]
ns["main"]()
