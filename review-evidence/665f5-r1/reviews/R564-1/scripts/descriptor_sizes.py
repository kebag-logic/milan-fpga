"""Per-shape descriptor census from generated aecp_entity_gen.h files."""
import collections
import re
import struct
import sys

for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read().split("aecp_entity_image[] = {", 1)[1]
    blob = bytes(int(x, 16) for x in re.findall(r"0x([0-9a-f]{2})", text))
    rows, directory = struct.unpack_from(">H", blob, 8)[0], struct.unpack_from(">I", blob, 12)[0]
    types, longest, total = collections.Counter(), 0, 0
    for row in range(rows):
        _, kind, number, length, _, _, _ = struct.unpack_from(">HHHHIHH", blob, directory + 16 * row)
        types[kind] += number
        total += number
        longest = max(longest, length)
    shape = path.split("/")[-2]
    print(f"{shape}: configurations {struct.unpack_from('>H', blob, 6)[0]}, descriptors {total}, "
          f"longest {longest} B (READ_DESCRIPTOR limit 1472 B: {'ok' if longest <= 1472 else 'EXCEEDED'}), "
          f"types {dict(sorted(types.items()))}")
