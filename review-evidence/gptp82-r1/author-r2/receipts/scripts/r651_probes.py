#!/usr/bin/env python3
"""Re-run the R651-1 reproducer probes (cold, gone, warm) against a source
tree. The probe body and the consumer-edge monitor are R651-1's run_probes.py
text, reproduced here verbatim; only its pinned-revision assertion and its
mutant campaigns are left out. Usage: r651_probes.py <source> <outdir>"""
import os, subprocess, sys, pathlib
src = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
original = (src / 'tb/verilator/engine/sim_main.cpp').read_text()
start = original.index('    bring_the_engine_out_of_reset();', original.index('  int run_suite()'))
end = original.index('    printf("%d checks:', start)
body = r'''
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
text = original[:start] + body + '    expect("all consumer-edge tuples coherent", torn_edges, 0);\n    expect("commit pulses one cycle", wide_pulses, 0);\n    printf("CONSUMER_EDGES %llu\\n", (unsigned long long)consumer_edges);\n' + original[end:]
assert text.count('  void tick() {') == 1 and text.count('    dut->clk_i = 1; dut->eval();') == 1
text = text.replace('  void tick() {', '  uint64_t consumer_edges=0, torn_edges=0, wide_pulses=0; bool prev_commit=false;\n  void tick() {')
text = text.replace('    dut->clk_i = 1; dut->eval();', r'''
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
here = out / 'build'; here.mkdir(exist_ok=True)
(here / 'sim_main.cpp').write_text(text)
subprocess.run([sys.executable, str(src / 'hdl/ucode/gen_gptp_ucode.py'), '--clk-hz', '2000000', '--cease-ms', '3000', '-o', str(here / 'gptp_ucode.hex')], check=True, stdout=subprocess.DEVNULL)
rtl = ['ucpu/gptp_ucpu_pkg.sv', 'ucpu/KL_gptp_ucpu.sv', 'wire/KL_gptp_rx_parser.sv', 'wire/KL_gptp_tx_slot.sv', 'common/KL_gptp_timer.sv', 'top/KL_gptp_engine.sv']
cmd = ['verilator', '--cc', '--exe', '--build', '-j', '8', '--top-module', 'KL_gptp_engine', '-Wall', '-Wno-fatal', '-Wno-DECLFILENAME', '-Wno-UNUSEDSIGNAL', '-Wno-WIDTHEXPAND', '-Wno-WIDTHTRUNC', '-Wno-UNUSEDPARAM', '-GUCODE_HEX_P="gptp_ucode.hex"', '-GCLK_HZ_P=2000000', '--Mdir', str(here / 'obj'), '-CFLAGS', f'-std=c++17 -O2 -I{src}/tb/verilator/engine'] + [str(src / 'hdl' / r) for r in rtl] + [str(here / 'sim_main.cpp'), '-o', 'probe']
with open(out / 'build.log', 'w') as f:
    subprocess.run(cmd, cwd=here, stdout=f, stderr=subprocess.STDOUT, check=True)
for mode in ('cold', 'gone', 'warm'):
    env = dict(os.environ, PROBE_MODE=mode)
    with open(out / f'probe-{mode}.log', 'w') as f:
        r = subprocess.run([str(here / 'obj/probe')], cwd=here, stdout=f, stderr=subprocess.STDOUT, env=env)
    (out / f'probe-{mode}.log.rc').write_text(f'{r.returncode}\n')
    print(mode, r.returncode)
