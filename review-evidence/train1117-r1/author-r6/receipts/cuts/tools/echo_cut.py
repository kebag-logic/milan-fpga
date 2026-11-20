"""echo_cut.py TREE: attempt 2's paced-record cut in TREE's aecp_maps.c: an edit of one or two mappings echoes them a
byte at a time, as the fixed fields are, not by memcpy's call; a longer one keeps memcpy's word moves. Scratch writer."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'sw/firmware/ctrl/aecp/aecp_maps.c'; t = p.read_text()
a = "\taecp_put16(out + 4, count);\n\tmemcpy(out + 8, in + 8, count * 8u);\n"
b = ("\taecp_put16(out + 4, count);\n"
     "\t// the mappings echoed: one or two a byte at a time, as the fixed fields are, not by a call, which cost a one-row\n"
     "\t// edit more than its bytes did (#665); more by memcpy's word moves\n"
     "\tif (count <= 2u) {\n"
     "\t\tfor (size_t k = 0; k < count * 8u; ++k) {\n"
     "\t\t\tout[8u + k] = in[8u + k];\n"
     "\t\t}\n"
     "\t} else {\n"
     "\t\tmemcpy(out + 8, in + 8, count * 8u);\n"
     "\t}\n")
assert t.count(a) == 1
p.write_text(t.replace(a, b))
print('echo cut written')
