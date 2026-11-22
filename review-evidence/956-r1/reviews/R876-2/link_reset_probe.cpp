// Reviewer probe (#957): a STREAM_OUTPUT's Listener registration notice across a link reset of its interface.
// Appended to a disposable copy of sw/firmware/ctrl/test/test_aecp.cpp; never part of the reviewed tree.
TEST_F(AppOutputs, ReviewerProbeListenerReturnAfterLinkReset)
{
    aem(36);aem(36,{},CTLR+1);
    unsigned cursor=fabric.tx_sent;
    struct Seen { unsigned count[2]{};uint32_t flags=0;uint32_t flags_ex=~0u; };
    auto take=[&]{
        std::vector<Seen> seen(OUTPUTS);
        for(;cursor<fabric.tx_sent;++cursor){auto p=mbx_model_tx_frame(&fabric,cursor);
            if(p==nullptr||p->bytes[14]!=0xfb||get(p->bytes+36,2)!=0x800fu||get(p->bytes+38,2)!=6u)continue;
            const unsigned n=unsigned(get(p->bytes+40,2));
            const uint64_t controller=get(p->bytes+26,8);
            if(n>=OUTPUTS||(controller!=CTLR&&controller!=CTLR+1))continue;
            ++seen[n].count[controller==CTLR?0:1];
            seen[n].flags=uint32_t(get(p->bytes+42,4));seen[n].flags_ex=uint32_t(get(p->bytes+86,4));
        }
        return seen;
    };
    auto probe=[&]{
        for(unsigned m=0;m<OUTPUTS;++m){
            acmp_test::Pdu p{};p.msg=0;p.controller=CTLR;p.talker=ENTITY;p.listener=0x0303cafef00d0001;
            p.talker_uid=uint16_t(m);p.seq=uint16_t(0x700+m);
            auto bytes=acmp_test::acmpdu(p);
            ASSERT_TRUE(mbx_model_rx(&fabric,bytes.data(),bytes.size(),connection.source_interface[m]));settle(2);
        }
    };
    auto valid=[&]{
        for(unsigned k=0;k<200u;++k){
            bool held=true;
            for(unsigned i=0;i<MBX_N_IF;++i)held=held&&application.maap.ifs[i].core.valid;
            if(held)return true;
            settle(100);
        }
        return false;
    };
    const unsigned n=0,interface=connection.source_interface[0];
    auto gate=[&]{return (reservation.ifs[interface].gate>>n&1u)!=0u;};
    ASSERT_TRUE(valid());
    probe();settle(400);take();
    ASSERT_TRUE(gate())<<"output 0's DA gate is open";
    declaring[n]=true;  // the face reports the output declaring while its DA gate is open
    listener(interface,sid(n),1u,2u);
    auto s=take();
    printf("PROBE step1 Ready appears: notices %u/%u flags_ex %u\n",s[n].count[0],s[n].count[1],s[n].flags_ex);
    EXPECT_EQ(s[n].count[0],1u);
    EXPECT_EQ(info(n).flags_ex,1u)<<"REGISTERING with the Listener Ready";
    take();
    // the link goes down and comes back up: SRP resets the interface (reset_interface destroys its participants)
    mbx_model_set_link(&fabric,interface,false);settle(50);
    declaring[n]=gate();
    s=take();
    printf("PROBE step2 link down: gate %d notices %u/%u\n",int(gate()),s[n].count[0],s[n].count[1]);
    mbx_model_set_link(&fabric,interface,true);settle(50);
    ASSERT_TRUE(valid());
    probe();settle(400);
    declaring[n]=gate();
    s=take();
    printf("PROBE step3 link up, MAAP valid, probed: gate %d talkers %u notices %u/%u flags_ex %u\n",int(gate()),
           unsigned(reservation.ifs[interface].talkers>>n&1u),s[n].count[0],s[n].count[1],s[n].flags_ex);
    ASSERT_TRUE(gate())<<"output 0's DA gate is open again";
    for(unsigned k=0;k<450u&&(reservation.ifs[interface].talkers>>n&1u)==0u;++k){probe();settle(100);}
    s=take();
    printf("PROBE step3b base %llx readdressed %u held_cs %u\n",(unsigned long long)application.maap.ifs[interface].core.base,unsigned(reservation.ifs[interface].readdressed),unsigned(reservation.held_cs[n]));
    printf("PROBE step3b Talker declared again: talkers %u notices %u/%u flags_ex %u\n",
           unsigned(reservation.ifs[interface].talkers>>n&1u),s[n].count[0],s[n].count[1],s[n].flags_ex);
    ASSERT_NE(reservation.ifs[interface].talkers>>n&1u,0u)<<"output 0's Talker is declared again";
    const Info before=info(n);take();
    printf("PROBE step4 answer before the Listener returns: flags_ex %u listener_present %d declaration %u\n",
           before.flags_ex,int(reservation.ifs[interface].listener_present[n]),
           unsigned(reservation.ifs[interface].declaration[n]));
    // the Listener Ready returns (the bridge declares it again once it registers the Talker)
    listener(interface,sid(n),1u,2u);
    settle(3000);
    s=take();
    const Info after=info(n);take();
    printf("PROBE step5 Listener Ready returns: notices %u/%u answer flags_ex %u\n",s[n].count[0],s[n].count[1],
           after.flags_ex);
    EXPECT_EQ(before.flags_ex,0u)<<"the answer showed no REGISTERING before the Listener returned";
    EXPECT_EQ(after.flags_ex,1u)<<"the answer shows REGISTERING once it returned";
    EXPECT_EQ(s[n].count[0],1u)<<"PROBE: the Listener registration's return is one notice to the first controller";
    EXPECT_EQ(s[n].count[1],1u)<<"PROBE: the Listener registration's return is one notice to the second controller";
}
