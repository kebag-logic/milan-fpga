#!/usr/bin/env python3
"""usage: direct_increment_variant.py TREE OUT -- copy TREE's src and include to OUT and apply R812-1 S1 there:
transmit increments the released sink's change_owed directly and drops its loop over every sink."""
import shutil, sys
from pathlib import Path
tree, out = Path(sys.argv[1]), Path(sys.argv[2])
shutil.rmtree(out, ignore_errors=True)
for d in ('src', 'include', 'examples'):
    shutil.copytree(tree / d, out / d)
p = out / 'src/acmp.c'; t = p.read_text()
old_set = "\t\to->release[(release - 1u) / 32u] = UINT32_C(1) << ((release - 1u) % 32u);\n\t}\n"
new_set = ("\t\to->release[(release - 1u) / 32u] = UINT32_C(1) << ((release - 1u) % 32u);\n"
           "\t\ta->sinks[release - 1u].change_owed = (uint8_t)(a->sinks[release - 1u].change_owed + 1u);\n\t}\n")
old_loop = ("\tfor (unsigned k = 0; k < a->cfg.n_sinks; ++k) {\n\t\ta->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed + "
            "((o->release[k / 32u] >> (k % 32u)) & 1u));\n\t}\n")
assert t.count(old_set) == 1 and t.count(old_loop) == 1
p.write_text(t.replace(old_set, new_set).replace(old_loop, ''))
print('variant written:', p)
