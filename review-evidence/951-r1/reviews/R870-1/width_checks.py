#!/usr/bin/env python3
"""Compile actual SRP sources at all four shapes and at count boundaries."""
from pathlib import Path
import re
import shutil
import subprocess
import sys

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
from ctrl_build import CTRL, Tree, C_FLAGS, SPLIT_RV32_FLAGS
import fw_rv32
import srp_arms

out = packet / 'scratch/width'
out.mkdir(parents=True, exist_ok=True)
src = out / 'ctrl'
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
original = (src / 'srp/srp_mbx.c').read_text()
header = (src / 'srp/srp_mbx.h').read_text()
compilers = [('host', 'gcc', list(C_FLAGS))]
rv = fw_rv32.compiler()
if rv:
    compilers.append(('target', rv, [*SPLIT_RV32_FLAGS, *fw_rv32.includes(rv)]))
else:
    print('Target compiler NOT RUN: unavailable')
failed = False
for entity, config in [('1x1', srp_arms.DEFAULT_ENTITY), ('8x8', srp_arms.ENTITY_8X8)]:
    for interfaces in (1, 2):
        tag = f'{entity}-if{interfaces}'
        tree = Tree(src, out / tag, out / 'reuse')
        variant, inc = srp_arms.prepared(tree, interfaces, out / tag, config)
        lw = root / 'third_party/lwSRP/src'
        inc += ['-DLWSRP_MILAN=1', f'-I{lw / "include"}', f'-I{lw}']
        expected = 3030 if interfaces == 2 else 3023 if entity == '1x1' else 3027
        for case, value, narrow, passed in [('normal', None, False, True), ('max16', 65535, False, True),
                                            ('overflow16', 65536, False, False), ('narrow8', None, True, False)]:
            code = original
            if value is not None:
                code = re.sub(r'^#define SRP_REDECLARE_CS .*$', f'#define SRP_REDECLARE_CS {value}u', code, flags=re.M)
            else:
                code += f'\n_Static_assert(SRP_REDECLARE_CS == {expected}u, "shape value");\n'
            (src / 'srp/srp_mbx.c').write_text(code)
            text = header.replace('uint16_t held_cs[', 'uint8_t held_cs[') if narrow else header
            (src / 'srp/srp_mbx.h').write_text(text)
            if variant != src:
                (variant / 'srp/srp_mbx.h').write_text(text)
            for label, cc, flags in compilers:
                result = subprocess.run([cc, *flags, *inc, '-fsyntax-only', str(src / 'srp/srp_mbx.c')],
                                        cwd=out, capture_output=True, text=True)
                correct = result.returncode == 0 if passed else result.returncode != 0 and 'held_cs holds the hold-off' in result.stderr
                print(tag, case, label, 'rc', result.returncode, 'PASS' if correct else 'FAIL')
                if not passed or not correct:
                    print(result.stderr.replace(str(packet), '<packet>').replace(str(root), '<checkout>'))
                failed |= not correct
        (src / 'srp/srp_mbx.h').write_text(header)
print('RESULT', 'FAIL' if failed else 'PASS')
sys.exit(failed)
