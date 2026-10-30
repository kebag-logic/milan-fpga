#!/usr/bin/env python3
"""Reproduce focused controls and observation-only probes in an isolated tree."""
import os, pathlib, subprocess, sys, tarfile, io, difflib, json
P = pathlib.Path(__file__).resolve().parent
S = pathlib.Path(sys.argv[1]).resolve()
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip() == 'ec1ff275a72d885f0908fd213d8009e9e4dda4d9'
T = P / 'scratch' / 'probe-tree'
V = os.environ.get('REVIEW_VERILATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
def run(args, name, cwd):
    with (P / (name+'.log')).open('w') as f:
        r = subprocess.run(args, cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
    (P / (name+'.rc')).write_text(str(r.returncode)+'\n')
    print(name, r.returncode, flush=True)
    return r.returncode
T.mkdir(parents=True, exist_ok=True)
archive = subprocess.check_output(['git','archive','HEAD'],cwd=S)
with tarfile.open(fileobj=io.BytesIO(archive)) as a: a.extractall(T, filter='data')
wrapper = P / 'scratch' / 'bounded-simulator.py'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i,x in enumerate(a[:-1]):\n if x=="-j": a[i+1]="8"\nos.execv('+repr(V)+', ['+repr(V)+']+a)\n')
wrapper.chmod(0o755)
run([V,'--version'], 'simulator-identity', S)
bench = T / 'tb' / 'pp_top'
make = ['make','-j16','gsi-build','VERILATOR='+str(wrapper)]
assert run(make, 'control-build', bench)==0
assert run(['./obj_dir/Vpp_top_sim','--reboot-only'], 'reboot-control', bench)==0
f = bench / 'sim_main.cpp'
original = f.read_text()
assert run(['git','apply',str(P/'post-departure-probe.patch')], 'prior-probe-apply', T)==0
assert run(make, 'prior-probe-build', bench)==0
run(['./obj_dir/Vpp_top_sim','--reboot-only'], 'post-departure-probe', bench)
f.write_text(original)
method = '''
  void nonadvertising_pending_frame_probe() {
    boot(false, "PROBE_NO_ADV");
    io.d->link_up_i = 1;
    io.idle(50);
    register_ctlr(C2_MAC, CTLR2_EID, "PROBE_NO_ADV");
    lock(CTLR_MAC, CTLR_EID, true, "PROBE_NO_ADV");
    for (uint16_t k = 0; k < 8; ++k)
      io.feed(acmp_frame(CTLR_MAC, 6, 0, 0, CTLR_EID, T1_EID, EID, k, k, 0, 0,
                         uint16_t(0x4A00 + k), 0, 0));
    io.feed(adp_frame(0, T1_MAC, T1_EID, 31, 1, GM0, DOM0, 0xBBB0000000000001ULL, 8,
                      TKCAP, 0, 0, 0x0000C588u, 0, 0));
    io.run_ms(20);
    io.tx_log.clear();
    io.stall_rbt_ntf_at_eof = true;
    send(CTLR_MAC, CTLR_EID, AEM_REBOOT, ti(DT_ENTITY, 0));
    for (long c=0; c<2000L*MS_CYC && !io.tx_eof_stalled; ++c) io.step();
    CHECK(io.tx_eof_stalled, "PROBE_NO_ADV required notification held at EOF");
    io.run_ms(5000);
    printf("PROBE_NO_ADV free standard slots=%u\\n", unsigned(io.d->dbg_txs_free_o - io.d->dbg_txs_slot4_free_o));
    io.stall_rbt_ntf_at_eof = false;
    io.mac_tx_ready = true;
    for (long c=0; c<3000L*MS_CYC && io.reboot_rise_t<0; ++c) io.step();
    printf("PROBE_NO_ADV request=%ld in_frame=%u bytes=%zu valid=%u\\n",io.reboot_rise_t, unsigned(io.in_frame), io.cur.size(), unsigned(io.d->tx_valid_o));
    io.run_ms(2000);
    int late=0, deps=0, success=0, notifications=0;
    for (const auto& e: io.tx_log) {
      if (departing(e.second)) ++deps;
      if (aecp(e.second) && ct(e.second)==AEM_REBOOT) {
        if (e.second[36]&0x80) ++notifications;
        else if (st(e.second)==AECP_SUCCESS) ++success;
      }
      if (long(e.first)>=io.reboot_rise_t) {
        ++late;
        printf("PROBE_NO_ADV late frame cycle=%llu request=%ld ethertype=%02x%02x subtype=%02x mt=%02x\\n", (unsigned long long)e.first, io.reboot_rise_t,e.second[12],e.second[13],e.second[14],e.second[15]);
      }
    }
    CHECK(deps==0 && success==1 && notifications==1 && io.reboot_rise_t>=0,
      "PROBE_NO_ADV legitimate no-advertising shutdown (%d departures %d success %d notifications)",deps,success,notifications);
    CHECK(io.tx_offer_t < io.reboot_rise_t && late==0,
      "PROBE_NO_ADV no byte offered after reset request (%d frames, last offer %ld request %ld)",late,io.tx_offer_t,io.reboot_rise_t);
    CHECK(io.d->reboot_req_o && !io.reboot_fell, "PROBE_NO_ADV request remains held");
  }
'''
anchor='  // ---- RBT9: nothing on tx_* from the final DEPARTING to a delayed reset -----'
changed=original.replace(anchor,method+'\n'+anchor)
changed=changed.replace('    every_slot_taken_at_the_shutdown();','    every_slot_taken_at_the_shutdown();\n    nonadvertising_pending_frame_probe();',1)
assert changed != original
f.write_text(changed)
(P/'nonadvertising-probe.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),changed.splitlines(True),fromfile='a/tb/pp_top/sim_main.cpp',tofile='b/tb/pp_top/sim_main.cpp')))
assert run(make, 'nonadvertising-probe-build', bench)==0
run(['./obj_dir/Vpp_top_sim','--reboot-only'], 'nonadvertising-probe', bench)
