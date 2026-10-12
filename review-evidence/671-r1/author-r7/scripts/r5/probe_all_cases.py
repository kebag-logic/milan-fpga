"""R603-4's probe_refusal_digest.py, graded on all four cases rather than
stopping at its first defect assertion. Its two assertions of the defect are
replaced, as text, by a record of each case; nothing else in it changes.
Exit 0 only when every faulty case keeps the change and every saved record
and its clean control passes. With a control's label, that #671 control is
planted into a scratch copy of the firmware first, and exit 0 then means the
defect returned in all four cases:
python3 -I probe_all_cases.py PROBE REPO [LABEL SCRATCH]"""
import json
import runpy
import sys
from pathlib import Path

probe, repo = Path(sys.argv[1]).resolve(), sys.argv[2]
old = ("        assert state.get(\"acks\") == 1 and \"the writer is HELD until reset\" not in out\n"
       "        assert lost > 0 if slot == \"a\" else got != fr.want[1][fr.key]\n")
new = ("        RESULTS.append((name, slot, state.get(\"acks\") == 1, \"the writer is HELD until reset\" in out,\n"
       "                        got == fr.want[1][fr.key], lost))\n")
text = probe.read_text()
assert text.count(old) == 1, "the probe's defect assertions moved"
derived = probe.with_name("probe_refusal_digest_all.py")
derived.write_text(text.replace(old, new).replace(
    'print("REPRODUCED: all four faulty cases', 'print("PROBE TEXT ENDS: all four faulty cases'))
plant = sys.argv[3] if len(sys.argv) > 4 else None
if plant:
    sys.path.insert(0, str(Path(repo).resolve() / "sw/firmware/nvm_hosttest"))
    import read_fault_cases
    import test_nvm_firmware
    planted = test_nvm_firmware.FIRMWARE.read_text()
    for before, after in read_fault_cases.READ_FAULT_MUTATIONS[plant][0]:
        assert planted.count(before) == 1, plant
        planted = planted.replace(before, after)
    copy = Path(sys.argv[4]).resolve() / "milan_baremetal.c"
    copy.parent.mkdir(parents=True, exist_ok=True)
    copy.write_text(planted)
    test_nvm_firmware.FIRMWARE = copy
results = []
sys.argv = [str(derived), repo]
try:
    runpy.run_path(str(derived), init_globals={"RESULTS": results}, run_name="__main__")
finally:
    derived.unlink()
bad = 0
for name, slot, acked, held, survived, lost in results:
    ok = (acked and not held and survived and lost == 0) or (held and not acked)
    bad += not ok
    print(json.dumps({"shape": name, "slot": slot, "acknowledged": acked, "held": held,
                      "change_survived": survived, "other_records_lost": lost,
                      "verdict": "DEFECT GONE" if ok else "DEFECT PRESENT"}))
print(f"{len(results)} case(s), {bad} with the defect" + (f" (planted {plant})" if plant else ""))
sys.exit(0 if len(results) == 4 and bad == (4 if plant else 0) else 1)
