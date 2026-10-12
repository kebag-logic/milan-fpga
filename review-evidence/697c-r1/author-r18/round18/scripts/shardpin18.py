"""Scratch (round 18): each hosted firmware job's form, test_ctrl_firmware.py --self-test --shard i/4, run in a
disposable clone whose tsn-c-stack has include/adp.h edited, must refuse (rc 2) naming the file before any build;
then with the pin check taken out of the driver's main (the plant), the same form must not refuse in that way
within the time limit. The clone is restored afterwards.
usage: python3 -I -B shardpin18.py <disposable clone> <seconds>"""
import subprocess, sys
from pathlib import Path
clone, limit = Path(sys.argv[1]).resolve(), int(sys.argv[2])
driver = clone / "sw/firmware/ctrl/test/test_ctrl_firmware.py"
header = clone / "third_party/tsn-c-stack/include/adp.h"
assert subprocess.run(["git", "-C", str(header.parent.parent), "rev-parse", "--show-toplevel"], capture_output=True,
                      text=True).stdout.strip() == str(header.parent.parent)
OLD, NEW = b"#define ADP_ADVERTISE_MS 5000u", b"#define ADP_ADVERTISE_MS 9000u"
PIN = '            print(f"tsn-c-stack at {stack_pin()}")\n            cut_reuse(tree.reuse)\n            failed = run_selected'
text, data = driver.read_text(), header.read_bytes()
assert text.count(PIN) == 1 and data.count(OLD) == 1

def run(label):
    bad = 0
    for i in range(4):
        argv = [sys.executable, "-B", str(driver), "--require-rv32", "--self-test", "--jobs", "4", "--shard", f"{i}/4"]
        try:
            r = subprocess.run(argv, cwd=clone, capture_output=True, text=True, timeout=limit)
            out, rc = r.stdout + r.stderr, r.returncode
        except subprocess.TimeoutExpired as exc:
            out, rc = (exc.stdout or b"").decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""), None
        said = [ln for ln in out.splitlines() if "differs from the pinned" in ln]
        refused = rc == 2 and any("include/adp.h" in ln for ln in said)
        print(f"  {label} --shard {i}/4: {'REFUSED' if refused else 'NOT REFUSED'} "
              f"(rc {rc if rc is not None else f'none: still running at {limit} s'}): "
              f"{(said[-1] if said else (out.strip().splitlines() or [''])[-1])[:150]}", flush=True)
        bad += refused
    return bad

try:
    header.write_bytes(data.replace(OLD, NEW))
    head = run("head")
    driver.write_text(text.replace(PIN, PIN.replace('            print(f"tsn-c-stack at {stack_pin()}")\n', ""), 1))
    planted = run("plant: no pin check in main")
finally:
    header.write_bytes(data)
    driver.write_text(text)
ok = head == 4 and planted == 0
print(f"head refused {head} of 4; with the plant refused {planted} of 4: {'CONTROL HOLDS' if ok else 'CONTROL FAILS'}")
sys.exit(0 if ok else 1)
