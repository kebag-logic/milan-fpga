#!/usr/bin/env python3
"""Compare a reviewer build's service_spec build_hashes with a published receipt."""
import json, sys
spec = json.load(open(sys.argv[1]))['build_hashes']
rec = json.load(open(sys.argv[2]))['build_hashes']
same = sorted(k for k in rec if spec.get(k) == rec[k])
diff = sorted(k for k in rec if k in spec and spec[k] != rec[k])
only = sorted(set(rec) ^ set(spec))
print(f'equal {len(same)} differ {len(diff)} key-set-diff {len(only)}')
for k in diff: print('  DIFFER', k)
for k in only: print('  ONLY-ONE-SIDE', k)
