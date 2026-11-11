# Reviewer mutants of the wire-timing grader and model-facing checks (#868 round 3): each replaces one
# line of wire_grade.py in a DISPOSABLE checkout, runs the self-test, and restores the exact bytes.
# A mutant is killed when the self-test exits non-zero. Usage: python3 -I -B grader_mutants.py <checkout>
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
src = root / 'tb/verilator/ctrl_wire_timing/wire_grade.py'
MUTANTS = (
    ('pairing reverted to any later PROBE_TX',
     "own = [p for p in probes if p.first > resp[0].last and (until is None or p.first < until)]",
     "own = [p for p in probes if p.first > cmd.last]"),
    ('PROBE_TX count check dropped', "if len(probe.cycles) != draws:", "if False:"),
    ('BIND_RX_RESPONSE status ignored', "if resp[0].status != SUCCESS:", "if False:"),
    ('AEM final status ignored', "if final[0].status != statuses[name]:", "if False:"),
    ('missing advertise period accepted', "if announces > 1 and not period.cycles:", "if False:"),
    ('stopped advertising accepted', "if quiet >= high:", "if False:"),
    ('frame equation dropped', "if delivered + FRAMES_PER_DRAW * draws != received:", "if False:"),
    ('skip after ANNOUNCE accepted', "if skipped and interface in offer.announced:", "if False:"),
    ('delivered counted as queued', "t['delivered_frames'] += got", "t['delivered_frames'] += offer.frames"),
)
original = src.read_bytes()
try:
    for name, old, new in MUTANTS:
        text = original.decode()
        assert text.count(old) == 1, name
        src.write_text(text.replace(old, new))
        r = subprocess.run([sys.executable, '-B', str(src.parent / 'wire_selftest.py')], capture_output=True, text=True)
        fails = [ln for ln in r.stdout.splitlines() if 'FAIL' in ln or ln.startswith('ctrl_wire_timing self-test')]
        print(f"{'KILLED' if r.returncode else 'SURVIVED'} rc={r.returncode} {name}: {fails[:2]}"[:300])
        src.write_bytes(original)
finally:
    src.write_bytes(original)
print('restored:', src.read_bytes() == original)
