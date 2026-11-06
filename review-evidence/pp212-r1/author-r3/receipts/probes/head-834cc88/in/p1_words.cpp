  // round-3 author probe: R769-2 P1's steps, printing what its nothing_applied() reads
  for (const bool lv_out : {false, true}) {
    h.reset();
    fill_port_registrars();
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
    d->link_up_i = 0; h.idle(3);
    d->link_up_i = 1; h.idle(3);
    h.ctl(false, 0, SID0, DA0, VID0);
    if (lv_out) h.tick();
    h.clear_logs();
    h.ctl(true, 0, SID0, DA0, VID0);
    const int reg = h.l_reg[0], tk = h.l_tkreg(0), st = h.l_regst(0);
    const size_t ops = h.l_arm.size();
    h.clear_logs();
    h.tick();
    printf("PROBE-INFO P1-words (lv_out %d): settle reg %d tk %d state %d ops %zu; next tx! pushes [%s] (code/fp@sid), decl %d\n",
           lv_out, reg, tk, st, ops, push_words(h.l_push).c_str(), h.l_decl(0));
  }
