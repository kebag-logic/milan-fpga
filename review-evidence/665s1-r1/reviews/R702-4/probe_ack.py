#!/usr/bin/env python3
"""Exercise acknowledgement failure through the real AECP mailbox adapter."""
import pathlib,shutil,sys
root=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(__file__).resolve().parent
work=packet/'scratch/ack-probe'; work.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(root/'sw/firmware/ctrl/test'))
import ctrl_build, aecp_arms, fw_gtest
tests=work/'tests'
shutil.copytree(root/'sw/firmware/ctrl/test',tests,ignore=shutil.ignore_patterns('__pycache__'),dirs_exist_ok=True)
src=tests/'test_aecp.cpp'
text=src.read_text()
anchor='TEST_F(Face, ALateCommitIsOwedAndPublishedAgainWhole)'
probe=r'''
TEST_F(Face, ReviewHeldSettingMustNotPromiseUnwrittenValue)
{
    far.ack=false;
    Bytes identify=target(26,0,5);identify[4]=255;
    receive(24,identify);
    ASSERT_TRUE(mbx_face_busy(0));
    const auto commits_before=far.commits.size();
    identify[4]=0;
    auto response=receive(24,identify);
    const auto visible=mbx_model_read(&fabric,MBX_FACE_BASE+MBX_FACE_REG_F_ENTITY);
    const auto actual=(visible>>MBX_F_ENTITY_IDENTIFY_LSB)&255u;
    const auto status=get(response,16,2)>>11;
    std::printf("REVIEW held update: response_status=%llu core_identify=%u mailbox_identify=%u commits_before=%zu commits_after=%zu busy=%u owed=%u\n",
      (unsigned long long)status,adapter.core.identify,actual,commits_before,far.commits.size(),mbx_face_busy(0),face.owed[0]);
    EXPECT_TRUE(status!=0 || actual==0u)<<"successful response must not promise an unwritten F value";
}

'''
assert text.count(anchor)==1
src.write_text(text.replace(anchor,probe+anchor))
aecp_arms.HERE=tests
tree=ctrl_build.Tree(root/'sw/firmware/ctrl',work/'build',work/'reuse',fw_gtest.Build(jobs=4))
result=aecp_arms.core_arm(tree,root/'configs/endstation_ax7101_1x1_tdm8.yaml',2,'mailbox',
 'Face.EachSettingIsCommittedBeforeTheResponseThatPromisesIt:Face.ALateCommitIsOwedAndPublishedAgainWhole:Face.ReviewHeldSettingMustNotPromiseUnwrittenValue')
(packet/'ack-probe.log').write_text(result.log)
print(result.log)
print('probe return code:',result.rc)
sys.exit(0 if result.rc==1 and 'successful response must not promise an unwritten F value' in result.log else 1)
