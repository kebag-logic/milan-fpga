#!/usr/bin/env python3
"""Run a page's documented ctrl_plat_image.py command exactly as the page writes it, then read the flash port's code.

usage: page_probe.py <clone> <page> <build-dir> <out> [<flash-map>]

The sh fence holding `ctrl_plat_image.py` is taken from the page in the clone and run with bash, unedited, given only
the variables the page names: SOC, the build's product split export; RUNTIME, its archives; OUT; and FLASH_MAP. With
the page's own generator line FLASH_MAP is a new directory; a page whose fence has no generator line is given
<flash-map>, written by this script with the plat page's generator line. `--disasm ELF` alone reads an ELF.
Exit 0 when the fence exits 0 and no ls_* or nvm_flash_litespi* function holds a stand-in address.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

#: The flash port's RV32 stand-ins, as the compiler loads them: timer0 at 0xf0003800 and the window at 0x20000000.
STAND_INS = {'lui 0xf0004': 'the stand-in timer0, 0xf0003800', 'lui 0x20000': 'the stand-in window, 0x20000000'}
#: The generated map's banks, as the compiler loads them.
GENERATED = ('lui 0xf0003', 'lui 0x1000')


def fence(page: Path) -> str:
    """The page's one sh fence that runs ctrl_plat_image.py."""
    found = [f for f in re.findall(r'^```sh\n(.*?)^```', page.read_text(), re.M | re.S) if 'ctrl_plat_image.py' in f]
    assert len(found) == 1, f'{page}: {len(found)} fences run ctrl_plat_image.py'
    return found[0]


def port_code(elf: Path) -> dict:
    """Each flash port function's lui operands, from the ELF's disassembly."""
    text = subprocess.run(['riscv32-linux-objdump', '-d', str(elf)], capture_output=True, text=True, check=True).stdout
    functions, name = {}, None
    for line in text.splitlines():
        head = re.fullmatch(r'[0-9a-f]+ <([^>]+)>:', line)
        if head:
            name = head.group(1) if re.match(r'ls_|nvm_flash_litespi', head.group(1)) else None
            if name:
                functions[name] = []
        elif name:
            lui = re.search(r'\blui\s+\w+,(0x[0-9a-f]+)', line)
            if lui:
                functions[name].append(f'lui {lui.group(1)}')
    return functions


def report(elf: Path) -> int:
    """Print the port's loads; the number of stand-in loads."""
    functions = port_code(elf)
    loads = [lui for luis in functions.values() for lui in luis]
    print(f'{elf.name}: {len(functions)} flash port functions, {len(loads)} lui')
    for lui, what in STAND_INS.items():
        hits = sorted(n for n, luis in functions.items() if lui in luis)
        print(f'  {lui} ({what}): {loads.count(lui)} in {hits}')
    for lui in GENERATED:
        print(f'  {lui} (generated): {loads.count(lui)}')
    assert functions, 'no flash port function found: the probe read nothing'
    return sum(loads.count(lui) for lui in STAND_INS)


def main() -> int:
    """Run the page's fence and read its image."""
    if sys.argv[1] == '--disasm':
        return 1 if report(Path(sys.argv[2])) else 0
    clone, page, build, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
    text = fence(clone / page)
    env = dict(os.environ, SOC=str(build / 'split-soc/mapped/soc'), RUNTIME=str(build / 'runtime'),
               OUT=str(out / 'image'), FLASH_MAP=sys.argv[5] if len(sys.argv) > 5 else str(out / 'flash-map'))
    print(f'--- the page\'s fence, {page}\n{text}---')
    done = subprocess.run(['bash', '-eu', '-c', text], cwd=clone, env=env, capture_output=True, text=True, check=False)
    (out).mkdir(parents=True, exist_ok=True)
    (out / 'fence.log').write_text(done.stdout + done.stderr)
    print(f'fence exit {done.returncode}')
    if done.returncode:
        print((done.stdout + done.stderr)[-800:])
        return 1
    size = json.loads((out / 'image/size.json').read_text())
    print(f"plan: {size['split']}" [:300])
    if 'gen_flash_port.py' in text:
        strip = lambda p: {k: v for k, v in json.loads(p.read_text()).items() if k != 'source'}
        same = strip(out / 'flash-map/flash_port.json') == strip(build / 'split-soc/flash-map/flash_port.json')
        print(f'page generator map equals the run\'s split-soc/flash-map: {same}')
        if not same:
            return 1
    return 1 if report(out / 'image/ctrl_app.elf') else 0


if __name__ == '__main__':
    raise SystemExit(main())
