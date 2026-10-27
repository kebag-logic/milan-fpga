// Reviewer probe (appended to a disposable copy of test_aecp.cpp, never committed).
// While a change of face state waits behind IN_PROGRESS, other changes are refused
// by the lock check. The authoritative text (MAILBOX_SPLIT.md "The firmware's
// writer", aecp/README.md) says each answers ENTITY_MISBEHAVING. This prints what
// SET_NAME, START_STREAMING and the MVU SET_SYSTEM_UNIQUE_ID actually answer.
TEST_F(Face, ReviewerProbeRefusalsWhileAChangeWaits)
{
    far.ack=false;Bytes identify=target(26,0,5);identify[4]=255;
    receive(24,identify,AECP_IN_PROGRESS);
    ASSERT_TRUE(adapter.core.waiting);
    // SET_NAME on the ENTITY descriptor's entity_name
    Bytes name=target(0,0,72);name[8]='x';
    auto n=receive(16,name,AECP_ENTITY_MISBEHAVING);
    std::printf("PROBE set_name status=%u\n",(unsigned)(get(n,16,2)>>11));
    // MVU SET_SYSTEM_UNIQUE_ID, value 0x0102030405060708
    Bytes body={0xc5,0x0a,0xc1,0,0,0,0,0};put(body,4,1,2);
    Bytes value={1,2,3,4,5,6,7,8};body.insert(body.end(),value.begin(),value.end());
    auto p=command(0x001b,body,CTLR,0,6);uint32_t before=fabric.tx_sent;
    ASSERT_TRUE(mbx_model_rx(&fabric,p.data(),p.size(),0));service();
    ASSERT_GT(fabric.tx_sent,before);
    auto f=mbx_model_tx_frame(&fabric,before);Bytes out(f->bytes,f->bytes+f->len);
    unsigned status=(unsigned)(get(out,16,2)>>11);
    std::printf("PROBE mvu_set_system_unique_id status=%u (ENTITY_MISBEHAVING=%u, NOT_IMPLEMENTED=1)\n",
                status,(unsigned)AECP_ENTITY_MISBEHAVING);
    EXPECT_EQ(status,(unsigned)AECP_ENTITY_MISBEHAVING)<<"MVU SET_SYSTEM_UNIQUE_ID refused while a change waits";
    mbx_model_advance_ms(&fabric,5);
    // and once the wait has failed and the face is still held (refusing, no wait)
    mbx_model_advance_ms(&fabric,AECP_WAIT_MS);service();
    ASSERT_FALSE(adapter.core.waiting);
    p=command(0x001b,body,CTLR,0,6);before=fabric.tx_sent;
    ASSERT_TRUE(mbx_model_rx(&fabric,p.data(),p.size(),0));service();
    ASSERT_GT(fabric.tx_sent,before);
    f=mbx_model_tx_frame(&fabric,before);out.assign(f->bytes,f->bytes+f->len);
    status=(unsigned)(get(out,16,2)>>11);
    std::printf("PROBE mvu_set_system_unique_id_after_failed_wait status=%u\n",status);
    EXPECT_EQ(status,(unsigned)AECP_ENTITY_MISBEHAVING)<<"MVU SET_SYSTEM_UNIQUE_ID refused while the face is held";
    far.ack=true;for(unsigned i=0;i<MBX_N_IF;++i)mbx_model_face_ack(&fabric,i);service();
}
