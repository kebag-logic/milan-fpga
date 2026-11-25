"""Usage: rv32_controls.py TREE WORK. Runs the smoke image on mutated cores, with the head control length and with 1024."""
import subprocess, sys, pathlib, shutil, concurrent.futures as cf
tree, work = map(lambda p: pathlib.Path(p).resolve(), sys.argv[1:3])
CMP = "(wire_be16(frame + ADP_HEADER_BYTES + 2u) & 0x07FFu) < ADP_CONTROL_DATA_LENGTH ||"
M = {'head': CMP, 'exact': CMP.replace('<', '!='), 'removed': 'false ||', **{f'mask-0x{m}': CMP.replace('0x07FF', '0x' + m) for m in ('03FF', '01FF', '00FF', '007F')}}
def one(a):
    n, c, l = a
    d = work / f'{n}-{l}'
    shutil.copytree(tree, d / 't', dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
    s = d / 't/src/adp.c'; t = s.read_text(); assert t.count(CMP) == 1; s.write_text(t.replace(CMP, c))
    s = d / 't/examples/rv32/smoke.c'; t = s.read_text(); assert t.count('0, 256}') == 1; s.write_text(t.replace('0, 256}', f'0, {l}}}'))
    out = ''
    for k in ('Debug', 'Release'):
        b = d / k
        for cmd in (['cmake', '-S', d/'t', '-B', b, f'-DCMAKE_TOOLCHAIN_FILE={d}/t/cmake/rv32.cmake', f'-DCMAKE_BUILD_TYPE={k}'], ['cmake', '--build', b, '-j2']):
            r = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if r.returncode: return n + ' build failed ' + r.stdout[-800:]
        elf = next(b.rglob('rv32_smoke.elf'))
        r = subprocess.run(['qemu-system-riscv32', '-machine', 'virt', '-nographic', '-bios', 'none', '-kernel', elf], timeout=60, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out += f' {k}={r.returncode}'
    return f'length {l} core {n}:{out}'
with cf.ThreadPoolExecutor(6) as p:
    for line in p.map(one, [(n, c, l) for l in (256, 1024) for n, c in M.items()]): print(line, flush=True)
