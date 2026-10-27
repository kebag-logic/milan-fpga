"""Module shares of a group's composed (or worst) pass in an archived arm.
usage: pass_shares.py RUNS_DIR ARM GROUP [worst|composed]"""
import json
import sys
from pathlib import Path
d = json.loads((Path(sys.argv[1]) / sys.argv[2] / f'{sys.argv[3]}.json').read_text())
p = d['passes'][sys.argv[4] if len(sys.argv) > 4 else 'composed']
m, c = p['modules'], p['cycles']
cats = {
    'memset+memcpy': ['rt_memset', 'rt_memcpy'],
    'aecp+acmp+mrp_mad': ['aecp', 'aecp_commands', 'acmp', 'mrp_mad'],
    'aecp+acmp+mrp_mad (aecp only)': ['aecp', 'acmp', 'mrp_mad'],
    'mailbox driver (mbx)': ['mbx'],
    'mailbox driver (mbx+mmio)': ['mbx', 'mbx_plat_mmio'],
    'soft arithmetic (rt_ not mem)': [k for k in m if k.startswith('rt_') and k not in ('rt_memset', 'rt_memcpy', 'rt_memcmp')],
}
print(f"{sys.argv[2]} {sys.argv[3]} {sys.argv[4] if len(sys.argv) > 4 else 'composed'}: {c:,} cycles; sum of modules {sum(m.values()):,}")
for name, keys in cats.items():
    v = sum(m.get(k, 0) for k in keys)
    print(f'  {name}: {v:,} ({100*v/c:.1f} %)')
for k, v in sorted(m.items(), key=lambda kv: -kv[1])[:8]:
    print(f'    {k} {v:,} ({100*v/c:.1f} %)')
