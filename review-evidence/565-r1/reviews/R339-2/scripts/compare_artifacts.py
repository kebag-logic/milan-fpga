#!/usr/bin/env python3
"""Compare reviewer-generated builder outputs (base vs head) and against the
author's published per-file hashes.

Usage: compare_artifacts.py <out-base> <out-head> <author-before.json> <author-after.json>
Each out-* directory holds one subdirectory per configuration; a file named
fragment-sweep_opts_<board>.sh is the per-config copy of the generated sweep
fragment (the author's records call it sweep_opts.sh).
"""
import hashlib
import json
import sys
from pathlib import Path


def digest(root: Path) -> dict:
    res = {}
    for cfg in sorted(p for p in root.iterdir() if p.is_dir()):
        files = {}
        for f in sorted(cfg.iterdir()):
            name = 'sweep_opts.sh' if f.name.startswith('fragment-') else f.name
            data = f.read_bytes()
            files[name] = {'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data)}
        res[cfg.name] = files
    return res


def main() -> int:
    base, head = digest(Path(sys.argv[1])), digest(Path(sys.argv[2]))
    auth = {'base': json.load(open(sys.argv[3])), 'head': json.load(open(sys.argv[4]))}
    rc = 0
    out = {'configs': {}}
    for cfg in sorted(base):
        changed = sorted(f for f in base[cfg] if base[cfg][f] != head[cfg].get(f))
        row = {'files': len(base[cfg]), 'changed_base_to_head': changed}
        for side, mine in (('base', base), ('head', head)):
            theirs = auth[side].get(cfg, {})
            mism = sorted(f for f in set(mine[cfg]) | set(theirs)
                          if mine[cfg].get(f) != theirs.get(f))
            row[f'author_{side}_mismatch'] = mism
            if mism:
                rc = 1
        out['configs'][cfg] = row
    out['result'] = 'match' if rc == 0 else 'MISMATCH'
    print(json.dumps(out, indent=2))
    return rc


if __name__ == '__main__':
    sys.exit(main())
