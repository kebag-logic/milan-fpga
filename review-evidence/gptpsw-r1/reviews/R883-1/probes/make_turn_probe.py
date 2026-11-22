"""Reviewer probe builder (R883-1): a scratch copy of test_gptp.cpp whose simulated peer answers a
Pdelay_Req after a stated turnaround (Pdelay_Resp and its Follow_Up leave g_turn_ns later), plus the
step probes. Usage: make_turn_probe.py <test_gptp.cpp> <probe.inc> <out.cpp>"""
import sys
src, inc, out = sys.argv[1:4]
text = open(src).read()
old = "\t\tlong double t_tx = n.true_ns + 1000.0L * (n.wire.size() + 1);   // distinct instants inside the tick\n\t\tBytes b(f, f + len);\n\t\tunsigned type = b[14] & 0x0F;\n"
new = "\t\tBytes b(f, f + len);\n\t\tunsigned type = b[14] & 0x0F;\n\t\tlong double t_tx = n.true_ns + 1000.0L * (n.wire.size() + 1) + ((type == 3 || type == 0xA) ? g_turn_ns : 0.0L);\n"
assert text.count(old) == 1, "send() anchor"
text = text.replace(old, new)
anchor = "struct Net : ::testing::Test {"
assert text.count(anchor) == 1
text = text.replace(anchor, "long double g_turn_ns = 0.0L;   // probe: the responder's turnaround\n" + anchor)
end = "}  // namespace\n"
assert text.endswith(end)
text = text[: -len(end)] + open(inc).read() + end
open(out, "w").write(text)
