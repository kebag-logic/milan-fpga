#!/usr/bin/env python3
"""Build all five endstation configurations from one tree and hash every output.

Usage: builder_outputs.py <repo-root> <work-dir> <out.json>
Mirrors the public round-1 artifact method: builder output directory plus the
AEM image, map and JSON from avdecc/gen_aemi_image.py at 576-byte lines.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root, work, out = (Path(a).resolve() for a in sys.argv[1:4])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    result = {}
    for cfg in sorted((root / 'configs').glob('endstation_*.yaml')):
        dest = work / cfg.stem
        dest.mkdir(parents=True, exist_ok=False)
        subprocess.run([sys.executable, 'sw/builder/endstation_builder.py',
                        str(cfg.relative_to(root)), '-o', str(dest / 'builder')],
                       cwd=root, env=env, check=True, stdout=subprocess.DEVNULL)
        gen = dest / 'builder' / cfg.stem
        subprocess.run([sys.executable, 'avdecc/gen_aemi_image.py', '--overlay',
                        str(gen / 'aem_overlay.json'), '--line-bytes', '576',
                        '-o', str(dest / 'aem.bin'), '-m', str(dest / 'aem.map'),
                        '--json', str(dest / 'aem.json')],
                       cwd=root, env=env, check=True, stdout=subprocess.DEVNULL)
        result[cfg.stem] = {
            str(p.relative_to(dest)): {'bytes': p.stat().st_size,
                                       'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(dest.rglob('*')) if p.is_file()}
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(f'{sum(len(v) for v in result.values())} files over {len(result)} configurations')
    return 0


if __name__ == '__main__':
    sys.exit(main())
