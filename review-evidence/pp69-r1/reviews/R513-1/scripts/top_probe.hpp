// Reviewer-owned legal byte-stream probe; included only in a disposable test copy.
static void reviewer_queued_ports(InterfacePhase& p) {
  auto check=[&](bool ok,const char* label) {
    ++p.h.checks; if (!ok) { ++p.h.fails; printf("FAIL: reviewer queued %s\n",label); }
  };
  const std::vector<uint8_t> flags(4,0);
  const uint64_t macs[2]={0x020200513001ull,0x020200513002ull};
  const uint64_t eids[2]={0x5130000000000001ull,0x5130000000000002ull};
  const size_t start=p.seen.size();
  for (unsigned n=0;n<4;++n)
    p.feed_on(n&1,aecp_frame(OWN_MAC,macs[n/2],0,0,EID,eids[n/2],0x5130+n,0x24,flags));
  p.run_ms(100);
  unsigned replies=0;
  for (size_t i=start;i<p.seen.size();++i) {
    const auto& f=p.seen[i].f;
    if (!p.unsolicited(f) && p.seq_of(f)>=0x5130 && p.seq_of(f)<0x5134 && p.succeeds(f)) ++replies;
  }
  check(replies==4,"four registrations complete");
  const size_t before=p.seen.size();
  auto answer=p.ask_on(0,p.D_MAC,p.D_EID,p.OP_LOCK,LockPhase::lockpld(0,0,0));
  p.run_ms(100);
  check(p.succeeds(answer),"lock response");
  check(p.lock_pushes(macs[0],before)==std::vector<unsigned>({0,0}),"first controller both ports");
  check(p.lock_pushes(macs[1],before)==std::vector<unsigned>({0,0}),"second controller both ports");
  printf("REVIEWER queued ports: four requests without response waits, %u successful replies\n",replies);
}
