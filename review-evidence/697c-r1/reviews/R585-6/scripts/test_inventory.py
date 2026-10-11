"""test_inventory.py BASE HEAD : GoogleTest case names (TEST/TEST_F/TEST_P first two arguments) of the
ADP, ACMP and MAAP binaries' sources at dev BASE (its sw/firmware/ctrl/test copies) and at HEAD (the
remaining sw/firmware/ctrl/test files plus third_party/tsn-c-stack/tests). Prints cases lost and gained."""
import re, sys
from pathlib import Path
RX = re.compile(r'\b(TEST|TEST_F|TEST_P)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)')
def cases(files):
    out = {}
    for f in files:
        if f.is_file():
            for m in RX.finditer(f.read_text(errors="replace")):
                out[f"{m.group(2)}.{m.group(3)}"] = f.name
    return out
B, H = Path(sys.argv[1]), Path(sys.argv[2])
names = ["test_adp.cpp", "test_adp_reentry.cpp", "test_acmp.cpp", "test_maap.cpp", "test_maap_debug.cpp"]
base = cases([B / "sw/firmware/ctrl/test" / n for n in names])
head = cases([H / "sw/firmware/ctrl/test" / n for n in names] + [H / "third_party/tsn-c-stack/tests" / n for n in names])
lost = sorted(set(base) - set(head)); gained = sorted(set(head) - set(base))
print(f"base cases {len(base)}  head cases {len(head)}  lost {len(lost)}  gained {len(gained)}")
for n in lost: print("LOST", n, base[n])
for n in gained: print("GAINED", n, head[n])
