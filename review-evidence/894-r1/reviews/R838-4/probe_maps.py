#!/usr/bin/env python3
"""Run exact-source map work probes with generated descriptors; no source edits."""
import copy
import sys
from pathlib import Path
import yaml

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch' / 'maps'
scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_build
import aecp_arms

raw = yaml.safe_load((root / 'configs/endstation_ax7101_8x8.yaml').read_text())
template = raw['streams']['talkers'][0]
raw['streams']['talkers'] = [dict(copy.deepcopy(template), name=f'Output {k}', channels=4) for k in range(16)]
config = scratch / 'sixteen-outputs.yaml'
config.write_text(yaml.safe_dump(raw))
tests = scratch / 'tests'
tests.mkdir(exist_ok=True)
original = (ctrl_build.HERE / 'test_aecp.cpp').read_text()
extra = r'''
#ifdef AECP_MAP_WORK
TEST_F(Core, ReviewLegalHashCollisionWork)
{
    for (unsigned n : {8u,16u,32u,63u}) {
        maps[1].count=0;
        Bytes body=target(15,0,8+8*n); put(body,4,n,2);
        for(unsigned k=0;k<n;++k) {
            // All coordinates come from generated descriptors: 16 outputs,
            // four channels each, routed to port zero's first cluster.
            put(body,8+8*k,k%16,2); put(body,10+8*k,k/16,2);
        }
        aecp_map_work=0; ask(44,body,0);
        EXPECT_EQ(maps[1].count,n);
        unsigned visits=aecp_map_work;
        std::printf("LEGAL ADD n=%u visits=%u stated_bound=%u\n",n,visits,2*n);
        EXPECT_LE(visits,2*n) << "legal distinct keys exceed the stated linear-work bound";
        aecp_map_work=0; ask(45,body,0);
        EXPECT_EQ(maps[1].count,0u);
        std::printf("LEGAL REMOVE n=%u visits=%u stated_bound=%u\n",n,aecp_map_work,6*n);
        EXPECT_LE(aecp_map_work,6*n);
    }
}
#endif
'''
(tests / 'test_aecp.cpp').write_text(original + extra)
aecp_arms.HERE = tests
tree = ctrl_build.Tree(ctrl_build.CTRL, scratch / 'build', scratch / 'reuse',
                       ctrl_build.fw_gtest.Build(jobs=8))
result = aecp_arms.core_arm(tree, config, 1, 'work', 'Core.ReviewLegalHashCollisionWork')
print('Builder and entity generation accepted 16 outputs x 4 channels.')
print(result.log)
raise SystemExit(result.rc)

