// #920: a SET_NAME of every user-settable name, each acknowledged, is saved and restored after a power cycle
// (Milan v1.2 5.3.13). Each name's record id is layout 3's (nvm_layout3.h): the names follow every other block, so
// at 1x1/1if the ordinals from 34 on have ids from 256 on, and every one must reach the store, once.
TEST_F(Nvm, EveryAcknowledgedNameSurvivesTheRealStorePowerCycle)
{
    boot();ASSERT_EQ(nvm_store_status()->terminal,NVM_T_BLANK);
    ON_CALL(mock,Changed).WillByDefault([this](aecp_change k,uint16_t t,uint16_t i){aecp_nvm_changed(&owner,k,t,i);});
    aecp_open(&a);
    ASSERT_GT(nvm_rec_id_of(NVM_G_NAME,AECP_ENTITY_NAMES-1),255)<<"the shape has names past the first 256 ids";
    auto value=[](unsigned k){Bytes v(64,0);v[0]='n';v[1]=uint8_t('A'+k%26);v[2]=uint8_t('0'+k/26);return v;};
    for(unsigned k=0;k<AECP_ENTITY_NAMES;++k){
        auto body=target(names[k].type,names[k].index,72),name=value(k);put(body,4,names[k].name,2);
        std::copy(name.begin(),name.end(),body.begin()+8);ask(16,body);
    }
    unsigned delivered=0;while(aecp_nvm_poll(&owner))++delivered;
    EXPECT_EQ(delivered,AECP_ENTITY_NAMES)<<"every name's mark reaches the store, once";
    EXPECT_EQ(nvm_store_status()->n_dirty,AECP_ENTITY_NAMES)<<"the store holds every name dirty";
    EXPECT_TRUE(owner.released);
    save();
    a.open=false;ASSERT_TRUE(aecp_restore_defaults(&a));owner.released=false;nvm_fmodel_power_on();boot();
    ASSERT_EQ(nvm_store_status()->terminal,NVM_T_COMPLETE);
    for(unsigned k=0;k<AECP_ENTITY_NAMES;++k)
        EXPECT_EQ(latch(NVM_G_NAME,k,64),value(k))<<"name "<<k<<" (descriptor "<<names[k].type<<" "
                                                   <<names[k].index<<") survives the power cycle";
}
