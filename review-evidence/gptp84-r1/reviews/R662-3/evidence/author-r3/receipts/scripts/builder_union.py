#!/usr/bin/env python3
"""Judge one parent tree's two builder legs with that tree's own union().

usage: builder_union.py <parent-tree> <receipt-b.json> <receipt-r.json>

Wraps the two driver receipts (leg 0 = the isolated baremetal gate, leg 1 =
every other gate, the parent's own measured partition) in the schema
scripts/ci_builder_legs.py run writes, with the tree's source identity now,
and asks that script's union() for "every gate exactly once, each a pass",
judging the requirement flags of the manager's command, which carries none.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(tree / "scripts"))
    os.chdir(tree)
    import ci_builder_legs as legs  # noqa: E402
    from ci_case_receipts import source_identity  # noqa: E402
    head, ident = source_identity(tree)
    receipts = []
    for leg, path in enumerate(sys.argv[2:4]):
        driver = json.loads(Path(path).read_text())
        receipts.append({"schema": legs.SCHEMA, "head": head, "tree": ident,
                         "leg": leg, "legs": legs.LEGS, "driver": driver})
    result = legs.union(receipts, head, ident, [])
    print(f"builder: {len(result['inventory'])} gates exactly once, union "
          f"{result['union']}, legs {[leg['shard'] for leg in result['legs']]}, "
          f"head {head}")
    print(f"NOT RUN rows: {result['not_run']}")
    print(f"verdicts_sha256 {result['verdicts_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
