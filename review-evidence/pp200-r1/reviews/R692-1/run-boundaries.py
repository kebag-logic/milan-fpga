#!/usr/bin/env python3
"""Add reviewer-only boundary stimuli in a disposable tree, leaving RTL exact."""
import difflib,os,pathlib,shutil,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
source=pathlib.Path(sys.argv[1]).resolve()
tree=P/'scratch'/'boundaries'
tree.mkdir(exist_ok=True)
for d in ('hdl','scripts','tb'):
 shutil.copytree(source/d,tree/d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('obj*','*.hex','__pycache__'))
file=tree/'tb/pp_top/sim_main.cpp';original=file.read_text();text=original
needle='    v5_get_avb_info_on_any_other_type_is_not_supported();'
text=text.replace(needle,needle+'\n    review_boundaries();')
anchor='  //! the face\'s AVB_INTERFACE 0 answer (gsi_value kind 1)'
probe='''  void review_boundaries() {
    uint16_t seq = 0x7900;
    for (uint16_t ty : {uint16_t(0x0009), uint16_t(0xffff)}) {
      for (size_t bytes = 0; bytes < 4; ++bytes) {
        std::vector<uint8_t> p(bytes, 0xff);
        if (bytes) p[0] = uint8_t(ty >> 8);
        if (bytes > 1) p[1] = uint8_t(ty);
        h.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, seq, 0x0027, p));
        auto got = h.wait_any(h.q_aecp, 3000);
        auto want = aecp_frame(CTLR_MAC, OWN_MAC, 1, AECP_BAD_ARGUMENTS, EID, CTLR_EID, seq, 0x0027, p);
        CHECK(!got.empty() && got == want, "review short type %04X cdl %zu: BAD_ARGUMENTS echo", ty, bytes+12);
        ++seq;
      }
    }
    for (uint16_t ty : {uint16_t(0x0109), uint16_t(0xffff)}) {
      for (size_t cdl : {16u,17u,18u,19u,20u,100u,255u,256u,257u,511u,523u,524u}) {
        std::vector<uint8_t> p(cdl-12);
        for (size_t i=0;i<p.size();++i) p[i]=uint8_t(37*i+13);
        putbe(&p[0],ty,2);putbe(&p[2],0xffff,2);
        h.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, seq, 0x0027, p));
        auto got = h.wait_any(h.q_aecp, 3000);
        auto want = aecp_frame(CTLR_MAC, OWN_MAC, 1, AECP_NOT_SUPPORTED, EID, CTLR_EID, seq, 0x0027, p);
        CHECK(!got.empty() && got == want, "review wrong type %04X absent index cdl %zu: NOT_SUPPORTED echo", ty, cdl);
        if (!got.empty() && got != want) { dump("got",got);dump("expected",want); }
        ++seq;
      }
    }
  }

'''
assert text.count(anchor)==1
text=text.replace(anchor,probe+anchor);file.write_text(text)
(P/'boundary-probe.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),text.splitlines(True),fromfile='a/tb/pp_top/sim_main.cpp',tofile='b/tb/pp_top/sim_main.cpp')))
env=os.environ.copy();env.update(TMPDIR=str(P/'scratch'),PYTHONDONTWRITEBYTECODE='1')
args=['make','-j16','-C',str(tree/'tb/pp_top'),'aecp-dispatch','VERILATOR='+str(P/'scratch/bounded-simulator.py')]
with (P/'boundary-probe.log').open('w') as log:
 rc=subprocess.run(args,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(P/'boundary-probe.rc').write_text(str(rc)+'\n')
print('boundary-probe rc='+str(rc));sys.exit(rc)
