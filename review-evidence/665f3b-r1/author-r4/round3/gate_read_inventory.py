"""Audit the CI classifier's complete gate-read page inventory."""
import argparse
import json
from pathlib import Path
import runpy

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
root = args.repo.resolve()
scope = runpy.run_path(str(root / "scripts/ci_scope.py"))
named = scope["docs_named_by_gated_code"](root)
registered = set(scope["GATE_READ_DOCS"])
rows = [dict(page=page, reader=reader, registered=page in registered,
             relevant=scope["is_rtl_relevant"]([page]))
        for page, reader in sorted(named.items())]
missing = sorted(set(named) - registered)
stale = sorted(registered - set(named))
result = dict(gated_files=len(scope["gated_files"](root)),
              documentation_files=len(scope["documentation_files"](root)),
              pages=rows, missing=missing, stale=stale)
print(json.dumps(result, indent=2))
raise SystemExit(bool(missing or stale or any(not row["relevant"] for row in rows)))
