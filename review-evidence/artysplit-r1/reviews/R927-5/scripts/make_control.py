"""Build the no-srp-bound control from a census extract: a hard-linked copy whose census.json omits one case.

Usage: python3 -I make_control.py <census-extract> <new copy dir> [case=none/srp-bound]
Every case file is kept (hard links, so no byte is copied or changed); only the copy's census.json is rewritten,
without the named case's entry. The source extract is not modified.
"""
import json
import os
import pathlib
import shutil
import sys

src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
case = sys.argv[3] if len(sys.argv) > 3 else 'none/srp-bound'
shutil.copytree(src, dst, copy_function=os.link)
census = json.loads((src / 'census.json').read_text())
before = len(census['cases'])
census['cases'] = [row for row in census['cases'] if row['case'] != case]
assert len(census['cases']) == before - 1, 'case not found exactly once'
(dst / 'census.json').unlink()  # break the hard link before writing
(dst / 'census.json').write_text(json.dumps(census, indent=1) + '\n')
print(f'control: {dst} cases {before} -> {len(census["cases"])}, removed {case}; '
      f'{case} files kept: {(dst / "census" / case).is_dir()}')
