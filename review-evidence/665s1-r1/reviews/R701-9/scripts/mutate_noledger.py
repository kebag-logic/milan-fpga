"""Mutant: build.build no longer holds split_soc.build under the ledgered plan. Usage: mutate_noledger.py BUILD_PY"""
import sys

path = sys.argv[1]
src = open(path).read()
old = ("    with split_soc.ledgered_plan(ledgered_point(shape, n_if)):\n"
       "        spec = split_soc.build(build_dir, shape, rom_elf, n_if, core.cpu_regions, core.fetch_l1)\n")
new = "    spec = split_soc.build(build_dir, shape, rom_elf, n_if, core.cpu_regions, core.fetch_l1)\n"
assert src.count(old) == 1, 'anchor not found once'
open(path, 'w').write(src.replace(old, new))
print('mutated', path)
