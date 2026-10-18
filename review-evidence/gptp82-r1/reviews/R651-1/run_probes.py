#!/usr/bin/env python3
"""Focused review reproduction; all changed files/builds stay in PACKET/scratch.
Usage: python3 run_probes.py SOURCE PACKET --jobs 16
"""
import argparse, concurrent.futures, importlib.util, json, os, pathlib, shutil, subprocess, sys
ap=argparse.ArgumentParser()
ap.add_argument('source',type=pathlib.Path); ap.add_argument('packet',type=pathlib.Path)
ap.add_argument('--jobs',type=int,default=16); a=ap.parse_args()
assert 1 <= a.jobs <= 16
src=a.source.resolve(); out=a.packet.resolve(); work=out/'scratch/probes'; work.mkdir(parents=True,exist_ok=True)
ver='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
identity=subprocess.check_output([ver,'--version'],text=True); assert '5.050' in identity
(out/'tool-identity.txt').write_text(identity)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=src,text=True).strip()=='85373de08a5c35487f260087ac8ceaf7a3789cdc'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('engine_mutants',src/'tb/verilator/engine/mutants.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
original=(src/'tb/verilator/engine/sim_main.cpp').read_text()
start=original.index('    bring_the_engine_out_of_reset();',original.index('  int run_suite()'))
end=original.index('    printf("%d checks:',start)
body=r'''
    const std::string mode = std::getenv("PROBE_MODE") ? std::getenv("PROBE_MODE") : "named";
    auto_txts = true;
    if (mode == "cold") {
      dut->rst_n=0; dut->rx_valid_i=0; dut->rx_sof_i=0; dut->rx_eof_i=0;
      dut->rx_err_i=0; dut->rx_data_i=0; dut->rx_ts_i=0;
      dut->tx_ready_i=1; dut->tx_credit_i=1;
      for (int i=0;i<8;i++) tick();
      dut->rst_n=1;
      run(2);
      expect("cold release GM is thisClock",dut->pub_gm_id_o,OUR_CID);
      expect("cold release path has one entry",dut->pub_path_count_o,1);
      run(1999998);
      printf("COLD at 1s: gm=%016llx count=%u commits=%zu\n",(unsigned long long)dut->pub_gm_id_o,unsigned(dut->pub_path_count_o),commit_snaps.size());
      expect("cold publication exists by 1s",!commit_snaps.empty(),1);
      run(500000);
      if (!commit_snaps.empty()) printf("FIRST_COMMIT release_delta=%llu gm=%016llx count=%u\n",(unsigned long long)(commit_snaps[0].cyc-8),(unsigned long long)commit_snaps[0].gm,commit_snaps[0].count);
    } else {
      bring_the_engine_out_of_reset();
      check_the_boot_pdelay_request();
      publish_thisclock_before_any_peer();
      if (mode == "named") return_to_thisclock_around_a_winning_peer();
      else {
        pd_mode=PD_NORMAL; pd_seen=txf.size();
        expect("setup capability",wait_flags(FL_ASCAP,FL_ASCAP,10000000),1);
        const uint64_t gm=0x0082A0FFFE000001ull, hop=0x0082A0FFFE000002ull, peer=0x0082A0FFFE000003ull;
        send_announce(0x8201,1,gm,2,peer,{gm,hop,peer},phc()+100);
        expect("setup elected peer",dut->pub_gm_id_o,gm);
        if (mode == "gone") {
          pd_mode=PD_SKIP;
          // Keep Announce alive while Pdelay is lost; then silence the link.
          for (unsigned i=0;i<10;i++) {
            run_svc(1000000);
            send_announce(0x8210+i,1,gm,2,peer,{gm,hop,peer},phc()+100);
          }
          expect("departure lost capability",dut->pub_flags_o & FL_ASCAP,0);
          const size_t mark=commit_snaps.size();
          run_svc(14000000);
          printf("DEPARTED after 7s: gm=%016llx count=%u flags=%x commits=%zu\n",(unsigned long long)dut->pub_gm_id_o,unsigned(dut->pub_path_count_o),unsigned(dut->pub_flags_o),commit_snaps.size()-mark);
          expect("departed peer returns thisClock",dut->pub_gm_id_o,OUR_CID);
          expect("departed peer returns self path",dut->pub_path_count_o,1);
        } else if (mode == "warm") {
          warm_reset();
          expect("warm initial self",dut->pub_gm_id_o,OUR_CID);
          expect("warm capability",wait_flags(FL_ASCAP,FL_ASCAP,10000000),1);
          const uint64_t next=0x0082B0FFFE000001ull;
          send_announce(0x8301,2,next,0,next,{next},phc()+100);
          printf("WARM successor: gm=%016llx count=%u\n",(unsigned long long)dut->pub_gm_id_o,unsigned(dut->pub_path_count_o));
          expect("warm better-than-local peer wins",dut->pub_gm_id_o,next);
        }
      }
    }
'''
text=original[:start]+body+'    expect("all consumer-edge tuples coherent", torn_edges, 0);\n    expect("commit pulses one cycle", wide_pulses, 0);\n    printf("CONSUMER_EDGES %llu\\n", (unsigned long long)consumer_edges);\n'+original[end:]
text=text.replace('  void tick() {', '  uint64_t consumer_edges=0, torn_edges=0, wide_pulses=0; bool prev_commit=false;\n  void tick() {')
text=text.replace('    dut->clk_i = 1; dut->eval();',r'''
    // Sample on the receiving sequential block's edge, before model updates.
    if (dut->rst_n && dut->pub_commit_o) {
      consumer_edges++;
      if (prev_commit) wide_pulses++;
      const uint64_t gm=dut->pub_gm_id_o;
      bool coherent=true;
      if (gm==OUR_CID || gm==0x0082B0FFFE000001ull) coherent=dut->pub_path_count_o==1;
      else if (gm==0x0082A0FFFE000001ull) coherent=dut->pub_path_count_o==3;
      else coherent=false;
      for (unsigned k=0;k<PATH_TAIL_SLOTS;k++) {
        uint64_t want=(gm==0x0082A0FFFE000001ull && k<2) ? 0x0082A0FFFE000002ull+k : 0;
        uint64_t got=static_cast<uint64_t>(dut->pub_path_o[2*k]) | (static_cast<uint64_t>(dut->pub_path_o[2*k+1])<<32);
        coherent &= got==want;
      }
      if (!coherent) torn_edges++;
    }
    prev_commit=dut->rst_n && dut->pub_commit_o;
    dut->clk_i = 1; dut->eval();''')
def command(cmd,cwd,log,env=None):
    with open(out/log,'w') as f:
        r=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=540)
    (out/(log+'.rc')).write_text(str(r.returncode)+'\n'); return r.returncode
controls=[x for x in m.MUTATIONS if x[4].startswith('#82 ')]
workers=min(4,a.jobs); buildjobs=max(1,a.jobs//workers)
def campaign(item):
    tag,mutation=item; tree=work/tag; tree.mkdir(exist_ok=True)
    shutil.copytree(src/'hdl',tree/'hdl',dirs_exist_ok=True)
    shutil.copytree(src/'tb/common',tree/'tb/common',dirs_exist_ok=True)
    here=tree/'tb/verilator/engine'; here.mkdir(parents=True,exist_ok=True); (here/'sim_main.cpp').write_text(text)
    if mutation:
        f=tree/'hdl'/mutation[1]; s=f.read_text(); assert mutation[2] in s
        f.write_text(s.replace(mutation[2],mutation[3]))
    assert command([sys.executable,str(tree/'hdl/ucode/gen_gptp_ucode.py'),*m.GENARGS,'-o',str(here/'gptp_ucode.hex')],here,tag+'-generate.log')==0
    flags=list(m.VFLAGS); flags[flags.index('-j')+1]=str(buildjobs)
    cmd=[ver,*flags,'--Mdir',str(tree/'obj'),'-CFLAGS',f'-std=c++17 -O2 -I{here}',*[str(tree/'hdl'/s) for s in m.RTL_SOURCES],str(here/'sim_main.cpp'),'-o','probe']
    assert command(cmd,here,tag+'-build.log')==0
    modes=['named','cold','gone','warm'] if mutation is None else ['named']
    results={}
    for mode in modes:
        env=os.environ.copy();env['PROBE_MODE']=mode
        results[mode]=command([str(tree/'obj/probe')],here,tag+'-'+mode+'.log',env)
    if mutation:
        failed=[l for l in (out/(tag+'-named.log')).read_text().splitlines() if l.startswith('FAIL ')]
        results['named_checks']={n:any(n in l for l in failed) for n in mutation[4].split(' | ')}
        results['name']=mutation[0]
    return tag,results
with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
    results=dict(ex.map(campaign,[('control',None)]+[(f'mutant{i+1}',x) for i,x in enumerate(controls)]))
(out/'probe-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
