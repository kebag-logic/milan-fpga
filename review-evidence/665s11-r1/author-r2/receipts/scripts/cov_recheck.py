#!/usr/bin/env python3
"""cov_recheck.py CHECKOUT KEEP_DIR README: the coverage gate's own exclusion and ratchet judgement (fw_coverage.py's
apply_exclusions, compare) over a measurement CHECKOUT kept (--keep), with README's exclusion table."""
import sys
from pathlib import Path
root, keep, readme = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import fw_coverage as fc  # noqa: E402
merged = fc.collect([keep])
kept_lines, found = fc.apply_exclusions(merged, fc.exclusions(readme.read_text(encoding='utf-8')))
kept = fc.tally(kept_lines)
drops = fc.compare(kept, fc.read_ratchet(fc.RATCHET.read_text(encoding='utf-8')))
for x in found + drops:
    print(f'FINDING: {x}')
print(f"firmware coverage (recheck of a kept measurement): {'FAIL' if found or drops else 'PASS'} ({len(kept)} files)")
sys.exit(1 if found or drops else 0)
