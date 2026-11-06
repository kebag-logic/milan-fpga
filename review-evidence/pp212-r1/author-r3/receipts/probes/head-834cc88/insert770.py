"""insert770.py <sim_main.cpp> <inc>: add r770_probes() (declared, defined before run(), called last)."""
import sys
f, inc = sys.argv[1], sys.argv[2]
s = open(f).read()
d = "  void a_settled_sinks_registration_ends_at_a_link_change();\n"
assert s.count(d) == 1
s = s.replace(d, d + "  void r770_probes();\n")
r = "int SrpStreamFsmsSuite::run() {\n"
assert s.count(r) == 1
s = s.replace(r, open(inc).read() + "\n" + r)
c = "  a_settled_sinks_registration_ends_at_a_link_change();\n\n  printf("
assert s.count(c) == 1
s = s.replace(c, "  a_settled_sinks_registration_ends_at_a_link_change();\n  r770_probes();\n\n  printf(")
open(f, "w").write(s)
