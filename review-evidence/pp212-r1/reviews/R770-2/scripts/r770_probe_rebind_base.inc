// Reviewer probe for the base and the head: a sink settled and registered, then an
// A8 and an A15 on the same triple (no link change; the base has no link input).
void SrpStreamFsmsSuite::r770_rebind_base() {
  h.reset();
  h.ctl(true, 0, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  const int before = h.l_tkreg(0);
  h.ctl(false, 0, SID0, DA0, VID0);
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  printf("XPINFO XPB: settled+registered %d, then A8 and A15 same: reg %d tk %d\n",
         before, h.l_reg[0], h.l_tkreg(0));
}
