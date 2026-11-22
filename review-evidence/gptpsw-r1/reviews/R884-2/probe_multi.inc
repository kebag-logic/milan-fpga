// Multiple responders whose Follow_Up never arrives (Milan v1.2 4.2.6.2.5; IEEE 802.1AS-2020 10.2.5.1 c).
TEST_F(Scripted, MultipleResponsesWithoutFollowUpCannotKeepAsCapable) {
 start(); exchanges(2);
 ASSERT_TRUE(port.pd.as_capable);
 for (unsigned i=0;i<3;i++) {
  auto seq=last_seq();
  uint64_t t1=10000000000ull+1000000000ull*i;
  gptp_port_ts(&port,true,0x2,seq,t1,true);
  rx(pdelay_resp(kClockB,seq,t1+500,kClockA,false),true,t1+31000);
  rx(pdelay_resp(0x1234ull,seq,t1+600,kClockA,false),true,t1+32000);
  std::printf("[MULTI] exchange %u: multi=%d run=%u ceased=%d asCapable=%d lost=%u\n",i+1,port.pd.multi,port.pd.multi_run,port.pd.ceased,port.pd.as_capable,port.pd.lost);
  if(i<2)tick(1000);
 }
 EXPECT_TRUE(port.pd.ceased);
 tick(10000);
 std::printf("[MULTI] 10 seconds after cease: ceased=%d asCapable=%d lost=%u\n",port.pd.ceased,port.pd.as_capable,port.pd.lost);
 EXPECT_FALSE(port.pd.as_capable) << "multiple responses without Follow_Up preserved asCapable during cease";
}
TEST_F(Scripted, MultipleResponsesWithFollowUpClearAsCapableControl) {
 start(); exchanges(2);
 ASSERT_TRUE(port.pd.as_capable);
 auto seq=last_seq();
 uint64_t t1=10000000000ull;
 gptp_port_ts(&port,true,0x2,seq,t1,true);
 rx(pdelay_resp(kClockB,seq,t1+500,kClockA,false),true,t1+31000);
 rx(pdelay_resp(0x1234ull,seq,t1+600,kClockA,false),true,t1+32000);
 rx(pdelay_resp(kClockB,seq,t1+30500,kClockA,true));
 EXPECT_FALSE(port.pd.as_capable);
 std::printf("[MULTI CONTROL] completed multi-response exchange asCapable=%d\n",port.pd.as_capable);
}
