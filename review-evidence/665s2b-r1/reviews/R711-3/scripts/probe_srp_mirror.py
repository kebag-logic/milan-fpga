#!/usr/bin/env python3
"""Probe: SRP's one-build-a-pass rule in the mirrored orientation (#665, srp_bounds.h).

The lane's test JointLinkChangeBuildsOneInterfaceAPass checks that interface 0, due while interface 1 (whose
turn it is) withdraws, builds at once. This probe adds the mirror: interface 0 has the turn and withdraws in
the pass interface 1 is due. It patches a disposable copy (argv[1], an export of the head's sw/ with
third_party linked) and runs the two-interface srp_app.cpp arm filtered to the probe.

usage: probe_srp_mirror.py <probe copy root> <work dir>
"""
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
test = root / 'sw/firmware/ctrl/test/srp_app.cpp'
text = test.read_text()
anchor = '        << "the other is built on the next pass";\n}\n#endif\n'
assert text.count('EXPECT_TRUE(built(0) && built(1)) << "the other is built on the next pass";\n}\n#endif\n') == 1
probe = '''
TEST_F(Srp, ProbeMirrorJointLinkChange) {
    settle();
    auto built=[this](unsigned n) { return adapter.ifs[n].msrp!=nullptr && adapter.ifs[n].mvrp!=nullptr; };
    // interface 1 rebuilt alone last, so interface 0 has the turn
    mbx_model_set_link(&model,1,false); ctrl_loop_service(&loop); ctrl_loop_service(&loop);
    ASSERT_TRUE(built(0) && built(1)) << "(interface 1 rebuilt alone)";
    ASSERT_EQ(adapter.build_turn,0u) << "(interface 0 has the turn)";
    settle();
    // interface 0 has the turn and withdraws in the pass interface 1 is due
    mbx_model_set_link(&model,1,true); ctrl_loop_service(&loop);
    ASSERT_TRUE(built(0) && !built(1)) << "(interface 1 withdrew and is due)";
    mbx_model_set_link(&model,0,false); ctrl_loop_service(&loop);
    unsigned passes=1;
    EXPECT_TRUE(built(1) && !built(0)) << "PROBE an interface due beside one still withdrawing is built at once";
    while(!built(1) && passes<6) { ctrl_loop_service(&loop); ++passes; }
    std::printf("PROBE interface 1 built after %u pass(es) from interface 0's withdrawal; interface 0 built %d\\n",
                passes, built(0) ? 1 : 0);
}
'''
text = text.replace('EXPECT_TRUE(built(0) && built(1)) << "the other is built on the next pass";\n}\n#endif\n',
                    'EXPECT_TRUE(built(0) && built(1)) << "the other is built on the next pass";\n}\n' + probe +
                    '#endif\n')
test.write_text(text)
sys.path[:0] = [str(root / 'sw/firmware/ctrl/test'), str(root / 'sw/firmware/gtest')]
import ctrl_build
import fw_gtest
import srp_arms
tree = ctrl_build.Tree(root / 'sw/firmware/ctrl', work / 'out', work / 'reuse', fw_gtest.Build(jobs=8))
for f in ('*JointLinkChange*', '*ProbeMirror*'):
    out = srp_arms.arm_srp(tree, root / 'third_party/lwSRP', 2, test=('srp_app.cpp', f))
    print(f'== filter {f} rc={out.rc}')
    print('\n'.join(l for l in out.log.splitlines()
                    if 'PROBE' in l or '[  ' in l or 'Failure' in l or 'srp_app.cpp' in l))
