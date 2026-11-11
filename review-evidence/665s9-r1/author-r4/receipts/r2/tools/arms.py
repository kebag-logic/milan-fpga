"""arms.py <name-prefix>...: run the named arms of the dev clone's mbx mutants table (iteration only)."""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, "<scratch>/dev/tb/verilator/mbx")
import mutants  # noqa: E402
names = sys.argv[1:]
arms = [a for a in mutants.ARMS if any(a.name == n for n in names)]
root = Path("<scratch>/arms"); root.mkdir(exist_ok=True)
import shutil
for a in arms:
    shutil.rmtree(root / a.name, ignore_errors=True)
with ThreadPoolExecutor(max_workers=8) as pool:
    for arm, caught, detail in pool.map(lambda a: mutants.run_arm(a, root), arms):
        print(f"[{'ok' if caught else 'ESCAPED'}] {arm.name}: {detail}", flush=True)
