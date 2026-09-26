"""Compare wrapper parameters parsed from an integrated synthesis log with the
published input manifest, using the head's own parser.

usage: compare_params.py <repo> <integrated-log> <manifest-json> <config-name>
"""
import importlib.util
import json
from pathlib import Path
import re
import sys

repo, log, manifest, config = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("baseline", repo / "syn/ooc/pp_baseline.py")
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
wrapper = (repo / "hdl/milan/KL_pp_shadow.sv").read_text()
values = baseline.wrapper_parameters(log.read_text(), wrapper)
published = json.loads(manifest.read_text())["configurations"][config]["wrapper_parameters"]
root = str(repo) + "/"
normalised = {k: (v.removeprefix(root) if isinstance(v, str) else v) for k, v in values.items()}
print(f"reproduced parameters: {len(values)}; published: {len(published)}")
bad = 0
for key in sorted(set(normalised) | set(published)):
    a, b = normalised.get(key), published.get(key)
    flag = "ok" if a == b else "MISMATCH"
    bad += a != b
    print(f"{flag:8} {key} reproduced={a!r} published={b!r}")
decl = re.findall(r"^\s*parameter\s+[^=]*?\b(\w+)\s*=", re.sub(r"/\*.*?\*/|//[^\n]*", "", wrapper, flags=re.S), re.M)
print(f"independent declaration scan of KL_pp_shadow.sv: {len(decl)} parameters: {sorted(decl) == sorted(values)}")
sys.exit(1 if bad else 0)
