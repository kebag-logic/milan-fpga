#!/usr/bin/env python3
"""Build the base-vs-head ACMP differential test from the head's walk test.
The 'full' side runs the base core (old_ prefixed); the 'walked' side runs the core under test.
After every entry it requires identical callback traces, saved records, reported views, acmp_view and
acmp_binding_latch outputs for every sink. Usage: diff_gen.py TREE OUTDIR"""
import re, sys
from pathlib import Path
tree, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
hdr = (tree / "include/acmp.h").read_text()
names = sorted(set(re.findall(r"^(?:bool|void|enum acmp_restore) (acmp_\w+)\(", hdr, re.M)))
(out / "old_rename.h").write_text("".join(f"#define {n} old_{n}\n" for n in names))
protos = re.findall(r"^((?:bool|void|enum acmp_restore) acmp_\w+\([^;]*\);)", hdr, re.M)
api = 'extern "C" {\n' + "".join(re.sub(r" (acmp_\w+)\(", r" old_\1(", p, count=1) + "\n" for p in protos) + "}\n"
t = (tree / "tests/test_acmp_walk.cpp").read_text()
def sub(old, new, count=1):
    global t
    assert t.count(old) == count, old
    t = t.replace(old, new)
sub('using namespace acmp_test;\n', 'using namespace acmp_test;\n' + api +
    '#define CALL(fn) (s.old ? old_##fn : fn)\n')
sub('    std::vector<std::vector<std::uint64_t>> trace;\n', '    std::vector<std::vector<std::uint64_t>> trace;\n    bool old = false;\n')
sub('ASSERT_TRUE(acmp_init(&sides[n]->a, &cfg, &ports[n], &env[n]))',
    'sides[n]->old = n == 1u;\n            ASSERT_TRUE((n ? old_acmp_init : acmp_init)(&sides[n]->a, &cfg, &ports[n], &env[n]))')
sub('        every_sink_marked();\n        entry(walked);', '        entry(walked);')
t, k = re.subn(r"\b(acmp_\w+)\(&s\.a", r"CALL(\1)(&s.a", t)
assert k >= 10, k
sub('    Rng rng{0x9E3779B9u};', '    Rng rng{0x9E3779B9u};\n    std::uint32_t seed = 0x9E3779B9u;')
sub('        start(sinks);\n', '        start(sinks);\n        rng.x = seed;\n')
check = r'''
            for (unsigned k = 0; k < sinks; ++k) {
                const acmp_sink& x = walked.a.sinks[k];
                const acmp_sink& y = full.a.sinks[k];
                ASSERT_EQ(std::memcmp(x.saved, y.saved, sizeof x.saved), 0) << "saved record, sink " << k << " step " << n;
                const acmp_sink_view& u = x.reported;
                const acmp_sink_view& v = y.reported;
                ASSERT_TRUE(same_view(u, v)) << "reported view, sink " << k << " step " << n;
                acmp_sink_view p{}, q{};
                ASSERT_TRUE(acmp_view(&walked.a, k, &p) && old_acmp_view(&full.a, k, &q));
                ASSERT_TRUE(same_view(p, q)) << "acmp_view, sink " << k << " step " << n;
                std::uint8_t r1[ACMP_BINDING_BYTES], r2[ACMP_BINDING_BYTES];
                ASSERT_TRUE(acmp_binding_latch(&walked.a, k, r1) && old_acmp_binding_latch(&full.a, k, r2));
                ASSERT_EQ(std::memcmp(r1, r2, sizeof r1), 0) << "binding latch, sink " << k << " step " << n;
                ASSERT_EQ(x.change_owed, y.change_owed) << "change owed, sink " << k << " step " << n;
            }
'''
sub('            walked.trace.clear();\n', check + '            walked.trace.clear();\n')
same = r'''
bool same_view(const acmp_sink_view& u, const acmp_sink_view& v) {
    return u.state == v.state && u.bound == v.bound && u.binding.talker_entity_id == v.binding.talker_entity_id &&
           u.binding.controller_entity_id == v.binding.controller_entity_id &&
           u.binding.talker_unique_id == v.binding.talker_unique_id && u.binding.streaming_wait == v.binding.streaming_wait &&
           u.started == v.started && u.probing_status == v.probing_status && u.acmp_status == v.acmp_status &&
           u.settled == v.settled && u.stream.stream_id == v.stream.stream_id && u.stream.dest_mac == v.stream.dest_mac &&
           u.stream.vlan_id == v.stream.vlan_id && u.talker_registered == v.talker_registered &&
           u.registering_failed == v.registering_failed && u.talker_discovered == v.talker_discovered;
}
'''
sub('struct Rng {', same + '\nstruct Rng {')
# Replace the four fixed tests with seeded sweeps.
t = t[:t.index('// REQ: ACMP-13, ACMP-10, ACMP-09, ACMP-05\nTEST_F(AcmpWalk, OneSink')]
for sinks, steps in ((1, 4000), (2, 6000), (8, 8000), (9, 8000), (16, 8000), (32, 8000), (33, 10000)):
    t += f'''TEST_F(AcmpWalk, BaseAndHeadAgreeAt{sinks}Sinks) {{
    if ({sinks}u > ACMP_MAX_SINKS) GTEST_SKIP();
    for (std::uint32_t s = 1; s <= 12u; ++s) {{
        seed = 0x9E3779B9u * s + 7u;
        walk({sinks}u, {steps}u);
        if (HasFatalFailure()) return;
    }}
}}
'''
t += '}\n'
(out / "diff_old_new.cpp").write_text(t)
print("ok", len(names), "renamed")
