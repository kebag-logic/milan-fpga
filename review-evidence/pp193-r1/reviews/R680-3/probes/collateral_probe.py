#!/usr/bin/env python3
"""Add a public-input check that a re-walk serves unrelated streams once too."""
import pathlib,sys
p=pathlib.Path(sys.argv[1]);s=p.read_text()
decl='  void ready_with_asking_failed_declares_ready_failed();\n'
assert s.count(decl)==1
s=s.replace(decl,decl+'  void probe_other_applicants();\n')
body=r'''
void SrpStreamFsmsSuite::probe_other_applicants() {
  constexpr uint64_t OTHER1=0x02AABBCCDDEE0041ull;
  constexpr uint64_t OTHER3=0x02AABBCCDDEE0043ull;
  for (bool la : {false,true}) for (int holder : {5,7}) for (int at : {1,2,3}) {
    h.reset();
    h.ctl(true,0,SID0,DA0,3);
    h.ctl(true,holder,SID0,DA0,VID0);
    h.ctl(true,1,OTHER1,DAP,VID0);
    h.ctl(true,3,OTHER3,DAP,VID0);
    for (uint64_t sid : {SID0,OTHER1,OTHER3})
      h.inject(true,1,sid,sid==SID0?DA0:DAP,VID0,3,0,500);
    int m=app_next(VO,eNew,false,true);
    for (int k=0;k<(la?3:1);++k) { h.tick();m=app_next(m,eTx,false,true); }
    if (la) h.la_own();
    const bool done=tick_with_input_at(at,-1,SID0,DA0,3);
    const std::string want=model_words(app_msg(m,la,false),2);
    const bool same=listener_words(h.l_push,SID0)==want
      && listener_words(h.l_push,OTHER1)==want
      && listener_words(h.l_push,OTHER3)==want && h.l_push.size()==3;
    m=app_next(m,la?eTxLA:eTx,false,true);
    const bool state=h.l_app(0)==m && h.l_app(holder)==VO && h.l_app(1)==m && h.l_app(3)==m;
    printf("COLLATERAL holder=%d kind=%s clock=%d done=%d pushes=%zu state=%d -> %s\n",
      holder,la?"txLA!":"tx!",at,done,h.l_push.size(),state,done&&same&&state?"MATCH":"DIFF");
    CHECK(done&&same&&state,"each unrelated applicant transmits once before the re-walk finishes");
  }
}
'''
anchor='int SrpStreamFsmsSuite::run() {'
assert s.count(anchor)==1;s=s.replace(anchor,body+'\n'+anchor)
call='  ready_with_asking_failed_declares_ready_failed();\n'
assert s.count(call)==1;s=s.replace(call,call+'  probe_other_applicants();\n')
p.write_text(s)
