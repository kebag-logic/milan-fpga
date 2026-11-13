#!/usr/bin/env python3
"""Check map lookup work on colliding maximum-length REMOVE commands."""
from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root/'sw/firmware/ctrl/test'))
import aecp_arms
import ctrl_build
import fw_gtest

scratch = packet/'scratch/maps'
scratch.mkdir(parents=True, exist_ok=True)
source = scratch/'ctrl'
shutil.copytree(root/'sw/firmware/ctrl', source, dirs_exist_ok=True)
maps = source/'aecp/aecp_maps.c'
text = maps.read_text()
anchor = '\t\tsize_t v = e->slot[s];'
assert text.count(anchor) == 1
text = text.replace(anchor, '\t\t++review_match_probes;\n'+anchor)
text = text.replace('static size_t match(', 'unsigned review_match_probes;\nstatic size_t match(')
maps.write_text(text)
tests = source/'test/test_aecp.cpp'
tests.write_text(tests.read_text()+r'''
extern "C" unsigned review_match_probes;
TEST_F(Core, ReviewMaximumRemoveCollisionWork)
{
    for(unsigned count: {8u,16u,32u,63u}){
        Bytes body=target(14,0,8+8*count);put(body,4,count,2);
        for(unsigned n=0;n<count;++n){
            put(body,8+8*n,n,2); // distinct streams, identical input destination key
        }
        review_match_probes=0;
        ask(45,body,7);
        std::printf("COLLISION mappings=%u probes=%u\n",count,review_match_probes);
        EXPECT_GE(review_match_probes,count*(count+1)/2);
    }
}
''')
aecp_arms.HERE = source/'test'
tree = ctrl_build.Tree(source, scratch/'build', scratch/'reuse', fw_gtest.Build(jobs=8))
config = root/"configs/endstation_ax7101_1x1_tdm8.yaml"
result = aecp_arms.core_arm(tree, config, 1, 'core',
    'Core.MapEditsAreTheirDefinitionRowForRow:Core.RestoredOutputMapsHaveOneGlobalOwner:Core.ReviewMaximumRemoveCollisionWork')
print(result.log)
raise SystemExit(result.rc)
