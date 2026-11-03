"""Instrument a copy of starved_cleanup: per listing, the in-grace passes that list a descendant new since pass 1."""
import sys
from pathlib import Path
root = Path(sys.argv[1]) / "scripts"
p = root / "process_test_support.py"; s = p.read_text()
old = ('        assert clock[0] < 100, "cleanup never reached a verdict on the owner\'s clock"\n'
       '        return listing(clock[0])\n')
new = ('        assert clock[0] < 100, "cleanup never reached a verdict on the owner\'s clock"\n'
       '        listed = listing(clock[0])\n'
       '        first = census.__dict__.setdefault("first", set(listed))\n'
       '        if set(listed) - first and clock[0] < 2:\n'
       '            census.__dict__.setdefault("new_in_grace", []).append(clock[0])\n'
       '        return listed\n')
assert s.count(old) == 1; s = s.replace(old, new)
old2 = '        owner._cleanup()\n        events.append((clock[0], "no verdict"))'
new2 = ('        try:\n            owner._cleanup()\n        finally:\n'
        '            print("AUDIT", stated, "new-in-grace passes:", census.__dict__.get("new_in_grace", []), flush=True)\n'
        '        events.append((clock[0], "no verdict"))')
assert s.count(old2) == 1; s = s.replace(old2, new2); p.write_text(s)
