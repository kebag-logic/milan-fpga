#!/usr/bin/env python3
"""Each published budget table's paths, instances, refused probes, groups and composed figures."""
import re, sys
from pathlib import Path
ev = Path(sys.argv[1])
for f in sorted(ev.glob('budget-*-table.md')):
    t = f.read_text()
    head = re.search(r'(\d+) of (\d+) paths and (\d+) of (\d+) probe instances', t).groups()
    refused = sorted(set(re.findall(r'\| `([^`]+)` \| - \| - \| - \| - \| no start', t)))
    groups = set(re.findall(r'\(([a-z0-9-]+)\) \|', t))
    comp = re.search(r'Composed maximum[^:]*: (at least )?[\d,]+ CPU cycles \(([\d.]+) ms\)', t)
    rel = re.search(r'Over the windows that released their whole load only: (.*)', t)
    print(f"{f.name[:-9]:28} paths {head[0]}/{head[1]} inst {head[2]}/{head[3]} groups {len(groups)} refused {len(refused)} "
          f"composed {comp.group(2) if comp else '?'} released {rel.group(1)[:32] if rel else 'none'} {refused[:3]}")
