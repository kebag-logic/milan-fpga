"""Dev: a subset of the SRP defect table, by name prefix or exact name, at one interface count and entity.
usage: dev_mut.py OUT INTERFACES ENTITY_STEM_OR_- NAME..."""
import sys
from pathlib import Path
LANE = Path('/data-2/milan/lanes/894-8x8')
sys.path.insert(0, str(LANE / 'sw/firmware/gtest'))
sys.path.insert(0, str(LANE / 'sw/firmware/ctrl/test'))
import srp_mutants  # noqa: E402
out, n_if, entity, names = Path(sys.argv[1]).resolve(), int(sys.argv[2]), sys.argv[3], sys.argv[4:]
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if any(d.name == n or (n.endswith('*') and d.name.startswith(n[:-1])) for n in names))
print('defects:', [d.name for d in srp_mutants.DEFECTS], flush=True)
failed = srp_mutants.campaign(out, LANE / 'third_party/lwSRP', 8, n_if, '' if entity == '-' else entity)
print('FAILED' if failed else 'ALL CAUGHT')
