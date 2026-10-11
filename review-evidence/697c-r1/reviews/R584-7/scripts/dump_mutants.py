#!/usr/bin/env python3
"""usage: dump_mutants.py <tree> -> JSON list of the control campaign's planted defects (ctrl_mutants.MUTANTS)
and the AECP campaign's (aecp_mutants.DEFECTS fields), as that tree's own tables define them."""
import dataclasses, json, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / "sw/firmware/ctrl/test"), str(tree / "sw/firmware/gtest")]
import ctrl_mutants  # noqa: E402
out = {"ctrl": [dict(name=m.name, path=m.path, old=m.old, new=m.new, kills=[list(k) for k in m.kills()])
                for m in ctrl_mutants.MUTANTS]}
try:
    import aecp_mutants  # noqa: E402
    out["aecp"] = [dataclasses.asdict(d) if dataclasses.is_dataclass(d) else repr(d) for d in aecp_mutants.DEFECTS]
except Exception as exc:  # noqa: BLE001
    out["aecp_error"] = repr(exc)
json.dump(out, sys.stdout, indent=1, default=repr)
