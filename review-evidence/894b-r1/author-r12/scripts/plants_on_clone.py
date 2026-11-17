"""Plant named SRP defects (srp_mutants.DEFECTS, exact names) from a clean clone's own tree, each into a copy of that
clone's sw/firmware/ctrl, at one interface count, and require each caught by its own test's words (srp_mutants.campaign).
usage: python3 -B plants_on_clone.py CLONE OUT INTERFACES NAME..."""
import subprocess
import sys
from pathlib import Path

clone, out, n_if, names = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3]), sys.argv[4:]
head = subprocess.run(['git', '-C', str(clone), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(['git', '-C', str(clone), 'status', '--porcelain'], capture_output=True, text=True).stdout
print(f'clone at {head}, {len(dirty.splitlines())} changed path(s)', flush=True)
sys.path.insert(0, str(clone / 'sw/firmware/gtest'))
sys.path.insert(0, str(clone / 'sw/firmware/ctrl/test'))
import srp_mutants  # noqa: E402
assert Path(srp_mutants.__file__).resolve().is_relative_to(clone), srp_mutants.__file__
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in names)
assert sorted(d.name for d in srp_mutants.DEFECTS) == sorted(names), [d.name for d in srp_mutants.DEFECTS]
for d in srp_mutants.DEFECTS:
    print(f'defect {d.name}: {d.path} {d.old!r} -> {d.new!r}; test {d.test}, words {d.needle!r}', flush=True)
failed = srp_mutants.campaign(out, clone / 'third_party/lwSRP', 8, n_if)
print('FAILED' if failed else 'ALL CAUGHT')
sys.exit(1 if failed else 0)
