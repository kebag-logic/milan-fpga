#!/usr/bin/env python3
"""Run independent failure/recovery checks on a disposable test copy.
Usage: delta_probes.py CHECKOUT PACKET
Production source is read from CHECKOUT and never edited.
"""
import concurrent.futures
import pathlib
import shutil
import sys

root, packet = (pathlib.Path(s).resolve() for s in sys.argv[1:3])
work = packet / 'scratch/delta-probes'
tests = work / 'tests'
shutil.copytree(root / 'sw/firmware/ctrl/test', tests,
                ignore=shutil.ignore_patterns('__pycache__'), dirs_exist_ok=True)
src = tests / 'test_aecp.cpp'
text = src.read_text()
anchor = 'TEST_F(Face, ALateCommitIsOwedAndPublishedAgainWhole)'
probe = r'''
TEST_F(Face, ReviewGetterMustNotPromiseUnacknowledgedIdentify)
{
    const auto applied_identify=adapter.core.identify;
    far.ack=false;
    Bytes identify=target(26,0,5);identify[4]=255;
    receive(24,identify,AECP_ENTITY_MISBEHAVING);
    ASSERT_TRUE(mbx_face_busy(0));ASSERT_TRUE(face.owed[0]);
    const auto before=fabric.tx_sent;
    auto frame=command(25,target(26,0));
    ASSERT_TRUE(mbx_model_rx(&fabric,frame.data(),frame.size(),0));service();
    ASSERT_GT(fabric.tx_sent,before);
    const auto reply=mbx_model_tx_frame(&fabric,before);
    Bytes response(reply->bytes,reply->bytes+reply->len);
    const auto status=get(response,16,2)>>11;
    std::printf("REVIEW getter: status=%llu returned=%u last_acknowledged=%u busy=%u owed=%u\n",
        (unsigned long long)status,response[42],applied_identify,mbx_face_busy(0),face.owed[0]);
    EXPECT_TRUE(status!=AECP_SUCCESS || response[42]==applied_identify)
        <<"a successful getter must not promise the unacknowledged F value";
}

TEST_F(Face, ReviewStreamNotificationMustNotPromiseUnacknowledgedOffset)
{
    receive(36,{},0,CTLR+1);
    far.ack=false;
    Bytes info=target(6,0,84);put(info,4,0x20000000,4);put(info,24,4321,4);
    receive(14,info,AECP_ENTITY_MISBEHAVING);
    ASSERT_TRUE(mbx_face_busy(home(6,0)));
    const auto before=fabric.tx_sent;
    aecp_changed(&adapter.core,6,0,1u);
    service(20);
    unsigned promises=0;
    for(uint32_t k=before;k<fabric.tx_sent;++k){
        auto f=mbx_model_tx_frame(&fabric,k);
        if(f!=nullptr && f->bytes[14]==0xfb && get(f->bytes+36,2)==0x800fu){
            const auto status=get(f->bytes+16,2)>>11;
            const auto latency=get(f->bytes+62,4);
            std::printf("REVIEW notification: status=%llu offset=%llu busy=%u owed=%u\n",
                (unsigned long long)status,(unsigned long long)latency,
                mbx_face_busy(home(6,0)),face.owed[home(6,0)]);
            if(status==AECP_SUCCESS && latency==4321u)++promises;
        }
    }
    EXPECT_EQ(promises,0u)<<"no notification may promise an unacknowledged F offset";
}

TEST_F(Face, ReviewAutomaticUnlockMustBeNotifiedAfterRecovery)
{
    receive(36,{},0,CTLR+1);receive(1,Bytes(16));
    ASSERT_TRUE(adapter.core.locked);
    far.ack=false;
    const auto before=fabric.tx_sent;
    mbx_model_advance_ms(&fabric,60000);service(20);
    ASSERT_FALSE(adapter.core.locked);
    auto unlocks=[&](){unsigned n=0;
        for(uint32_t k=before;k<fabric.tx_sent;++k){
            auto f=mbx_model_tx_frame(&fabric,k);
            if(f!=nullptr && f->bytes[14]==0xfb && get(f->bytes+36,2)==0x8001u)++n;
        }
        return n;
    };
    EXPECT_EQ(unlocks(),0u)<<"no premature unlock notification";
    far.ack=true;
    for(unsigned i=0;i<MBX_N_IF;++i)mbx_model_face_ack(&fabric,i);
    service(100);
    ASSERT_TRUE(face.ports.applied(&face));
    for(unsigned i=0;i<MBX_N_IF;++i)
        EXPECT_EQ(at(taken(i),MBX_FACE_REG_F_AECP,MBX_F_AECP_LOCK_HELD_LSB,1),0u);
    std::printf("REVIEW unlock recovery: applied=%u notifications=%u registered=%u\n",
        face.ports.applied(&face),unlocks(),adapter.core.registry[0][0].used);
    ASSERT_TRUE(adapter.core.registry[0][0].used);
    EXPECT_EQ(unlocks(),1u)<<"automatic unlock remains owed until its required notification is sent";
}

'''
assert text.count(anchor) == 1
src.write_text(text.replace(anchor, probe + anchor))
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import aecp_arms
import ctrl_build
import fw_gtest
aecp_arms.HERE = tests

def run(interfaces):
    tree = ctrl_build.Tree(root / 'sw/firmware/ctrl', work / f'build{interfaces}',
                          work / f'reuse{interfaces}', fw_gtest.Build(jobs=4))
    result = aecp_arms.core_arm(tree, root / 'configs/endstation_ax7101_1x1_tdm8.yaml',
                              interfaces, 'app',
                              'Face.*:FaceLatency.*:AppFace.*:AppFaceUnacknowledged.*:'
                              'Core.AChangeThePlatformHasNotAppliedPromisesNothing')
    (work / f'if{interfaces}.log').write_text(result.log)
    (work / f'if{interfaces}.rc').write_text(str(result.rc) + '\n')
    return interfaces, result.rc

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(run, (1, 2)))
print(results)
sys.exit(max(rc for _, rc in results))
