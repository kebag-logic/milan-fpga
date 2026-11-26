"""lastframe_range.py SUMMARY...: per graded cut, the DUT's last frame minus the outlet's power-off instant
(both seconds after the bind's response, as the summary's 'sink' lines give them); prints each and the range."""
import re, sys
for path in sys.argv[1:]:
    d = [(float(a), float(b)) for a, b in re.findall(
        r"power off ([\d.]+) s after the response;.*?the DUT's last frame ([\d.]+) s", open(path).read())]
    gaps = [round(b - a, 3) for a, b in d]
    print(f"{path}: graded cuts {len(d)}; last frame after power-off min {min(gaps):.3f} max {max(gaps):.3f}")
    print("  " + " ".join(f"{g:.3f}" for g in gaps))
