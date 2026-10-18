"""Plant the two controls of the round-4 phase-list split, each in its own
archive copy of the head: `swap` inverts run_suite's dispatch, so the
shipping passes run only the self-publication phases and the fourth pass runs
every phase; `drop` removes one phase call from run_every_phase.
Usage: plant_split_controls.py <ctl_dir>  (holds swap/ and drop/)"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
rel = "tb/verilator/engine/sim_main.cpp"
plants = (
    ("swap", "    if (self_present == 0)\n      run_the_self_publication_phases();",
     "    if (self_present != 0)\n      run_the_self_publication_phases();"),
    ("drop", "    return_to_thisclock_around_a_winning_peer();\n", ""),
)
for tag, old, new in plants:
    path = root / tag / rel
    text = path.read_text()
    if text.count(old) != 1:
        sys.exit(f"{tag}: pattern appears {text.count(old)} time(s)")
    path.write_text(text.replace(old, new))
    print(f"{tag}: planted")
