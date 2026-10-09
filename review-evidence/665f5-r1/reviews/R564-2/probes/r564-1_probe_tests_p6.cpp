TEST_F(Core, P6_OneFailingObservationDoesNotStarveOtherDescriptorNotices)
{
    register_controller();sent.clear();
    // Only STREAM_INPUT counters are unavailable; every other observation answers.
    ON_CALL(mock,Counters).WillByDefault([](unsigned,uint16_t t,uint16_t,aecp_counters*v){
        v->valid=1;for(unsigned n=0;n<32;++n)v->value[n]=n;return t!=5;});
    aecp_changed(&a,5,0,8);aecp_changed(&a,9,0,8);aecp_changed(&a,36,0,8);
    unsigned busy=0;for(unsigned n=0;n<50;++n){if(aecp_poll(&a))++busy;}
    ms+=5000;for(unsigned n=0;n<50;++n){if(aecp_poll(&a))++busy;}
    unsigned avb=0,domain=0;for(auto&v:sent){if(get(v.second,36,2)==0x8029){
        unsigned t=unsigned(get(v.second,38,2));avb+=t==9;domain+=t==36;}}
    printf("PROBE P6 sent=%zu avb_counter_notices=%u clock_domain_counter_notices=%u busy_polls=%u/100\n",
           sent.size(),avb,domain,busy);
    EXPECT_EQ(avb,1u)<<"Milan 5.4.5.2 Table 5.22: an unrelated descriptor's notice is still sent";
    EXPECT_EQ(domain,1u)<<"Milan 5.4.5.2 Table 5.22: an unrelated descriptor's notice is still sent";
}
