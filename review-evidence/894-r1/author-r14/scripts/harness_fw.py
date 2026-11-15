#!/usr/bin/env python3
"""Link every harness leg's firmware again, the leg's own build parameters and flash map, from TREE, into OUT/<leg>,
and print each ELF's sha256. Only build.firmware runs: no SoC, no simulation, no leg.
usage: harness_fw.py TREE BUILDS OUT LEG...   (BUILDS: the legs' build directories, each with its build.json)"""
import concurrent.futures
import hashlib
import json
import sys
from pathlib import Path


def main(tree, builds, out, legs):
    sys.path.insert(0, str(Path(tree) / 'tb/verilator/ctrl_service_budget'))
    import build
    assert Path(build.ROOT).resolve() == Path(tree).resolve(), (build.ROOT, tree)

    def one(leg):
        spec = json.loads((Path(builds) / leg / 'build.json').read_text())
        elf = build.firmware(Path(out) / leg, spec['shape'], spec['interfaces'], spec['mutation'], spec['variant'],
                             Path(spec['flash_map']))
        return leg, spec, hashlib.sha256(elf.read_bytes()).hexdigest()

    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        for leg, spec, sha in pool.map(one, legs):
            print(leg, sha, spec['shape'], spec['interfaces'], spec['variant'], spec['mutation'])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
