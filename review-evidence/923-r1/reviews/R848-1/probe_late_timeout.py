#!/usr/bin/env python3
"""Add store-agreement assertions to a disposable copy of the exact-head tests."""
import os
from pathlib import Path
import sys
repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch" / "late-timeout"
scratch.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(packet / "scratch")
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms
from ctrl_build import Tree, CTRL, STACK
import fw_gtest
extra = r'''
TEST_F(Face, ReviewLateTimeoutControlCommand)
{
    receive(44,mappings(14,{{0,1,1,0},{0,2,2,0}}));
    agree(14);
    EXPECT_EQ(maps[0].count,2u);
}
TEST_F(Face, ReviewLateTimeoutControlRestore)
{
    std::array<aecp_mapping,2> defaults{{{0,0,0,0},{0,1,1,0}}};
    auto &m=maps[0];m.defaults=defaults.data();m.default_count=2;
    adapter.core.open=false;ASSERT_TRUE(aecp_restore_defaults(&adapter.core));
    far.live[{14u,0u}]={defaults.begin(),defaults.end()};
    ASSERT_EQ(aecp_map_restore(&adapter.core,&m,nullptr,0),0u);
    aecp_restore_commit(&adapter.core);
    adapter.core.open=true;agree(14);
    EXPECT_EQ(m.count,0u);
}
TEST_F(Face, ReviewLateTimeoutLeavesPartialStore)
{
    far.mute=[](const Far::Beat &b){return b.phase==5u&&b.rec==1u?2u:0u;};
    auto out=receive(44,mappings(14,{{0,1,1,0},{0,2,2,0}}));
    std::printf("REVIEW command status=%u core rows=%zu store rows=%zu unanswered=%u\n",
        unsigned(get(out,16,2)>>11),maps[0].count,far.live[{14u,0u}].size(),face.unanswered);
    far.mute=nullptr;
    agree(14);
}
TEST_F(Face, ReviewLateTimeoutDuringBootRestore)
{
    std::array<aecp_mapping,2> defaults{{{0,0,0,0},{0,1,1,0}}};
    auto &m=maps[0];m.defaults=defaults.data();m.default_count=2;
    adapter.core.open=false;ASSERT_TRUE(aecp_restore_defaults(&adapter.core));
    far.live[{14u,0u}]={defaults.begin(),defaults.end()};
    ASSERT_EQ(aecp_map_restore(&adapter.core,&m,nullptr,0),0u);
    far.mute=[](const Far::Beat &b){return b.phase==5u&&b.rec==1u?2u:0u;};
    aecp_restore_commit(&adapter.core);
    std::printf("REVIEW boot core rows=%zu store rows=%zu unanswered=%u\n",
        m.count,far.live[{14u,0u}].size(),face.unanswered);
    far.mute=nullptr;adapter.core.open=true;agree(14);
}
'''
(scratch / "test_aecp.cpp").write_text((aecp_arms.HERE / "test_aecp.cpp").read_text() + extra)
aecp_arms.HERE = scratch
tree = Tree(CTRL, scratch / "build", scratch / "reuse", fw_gtest.Build(jobs=4), STACK)
result = aecp_arms.core_arm(tree, repo / "configs/endstation_ax7101_1x1_tdm8.yaml", 2,
                           "mailbox", "Face.ReviewLateTimeout*")
print(result.log)
sys.exit(result.rc)
