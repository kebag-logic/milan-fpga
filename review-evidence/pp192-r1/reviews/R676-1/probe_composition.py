#!/usr/bin/env python3
"""Disposable test-only extension: both type swaps plus STOP, and repeated STOP."""
import json, os, pathlib, subprocess
p=pathlib.Path(__file__).resolve().parent
tree=p/'scratch/focused-source'
f=tree/'tb/pp_top/gsi_internal.hpp'
s=f.read_text(); original=s
s=s.replace('void started_with_registration() {','void started_with_registration(uint8_t code = 7, uint64_t bridge = BRIDGE0) {')
start=s.index('  void started_with_registration('); end=s.index('  void started_notify()',start)
part=s[start:end].replace('attribute(0, 7, BRIDGE0, true);','attribute(0, code, bridge, code != 0);').replace('true, 7,\n             BRIDGE0','true, code,\n             bridge').replace('true, 7, BRIDGE0','true, code, bridge')
s=s[:start]+part+s[end:]
needle='    started_with_registration();\n    io.run_ms(100);'
assert s.count(needle)==1
probe=r'''    started_with_registration();
    for (const bool failed : {false, true}) {
      streaming(0x0022, 0);
      auto start_frames = drain_aecp(150);
      auto start_a = unsolicited_to(start_frames, CTLR_MAC, unsolicited_sequence);
      auto start_b = unsolicited_to(start_frames, B_MAC, b_unsolicited);
      CHECK(start_frames.size() == 4 && stream_info_of(start_a, 0).size() == 1
            && stream_info_of(start_b, 0).size() == 1,
            "COMPOSITION: START restores state and notifies both once");
      started_with_registration(failed ? 7 : 0, failed ? BRIDGE0 : 0);
      CHECK((io.snap(12) & 3u) == (failed ? 2u : 1u),
            "COMPOSITION: registrar premise is type %d", failed ? 2 : 1);
      io.q_acmp.clear();
      const uint16_t seq = sequence++;
      io.feed(acmp_frame(CTLR_MAC, 10, 0, 0, CTLR_EID, 0, EID, 0, 0,
                         0, 0, seq, 0, 0));
      const auto rx = io.wait_frame(io.q_acmp, 500,
          [seq](const std::vector<uint8_t>& r) {
            return r.size() == 70 && (r[15] & 15) == 11
                && fv_u64(r, 62, 2) == seq;
          });
      CHECK(!rx.empty() && ((fv_u64(rx, 64, 2) & 0x0040) != 0) == failed,
            "COMPOSITION: GET_RX_STATE REGISTERING_FAILED follows final type %d", failed);
      const uint16_t repeated = sequence;
      streaming(0x0023, 0);
      const auto noop = drain_aecp(150);
      CHECK(noop.size() == 1 && answered(noop, repeated, 1) == 1,
            "COMPOSITION: repeated STOP succeeds without either unsolicited kind");
    }
    io.run_ms(100);'''
s=s.replace(needle,probe)
try:
    f.write_text(s)
    subprocess.run(['git','diff','--no-index','--',str(p/'scratch/original-gsi.hpp'),str(f)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL) if False else None
    import difflib
    (p/'composition-probe.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='a/tb/pp_top/gsi_internal.hpp',tofile='b/tb/pp_top/gsi_internal.hpp')))
    for name,cmd in [('composition-build',['make','-j16','gsi-build','VERILATOR='+str(p/'bounded_frontend.py')]),('composition-run',['./obj_dir/Vpp_top_sim','--gsi-internal-only'])]:
        with (p/(name+'.log')).open('w') as log:
            log.write('COMMAND '+json.dumps(cmd)+'\n');log.flush()
            rc=subprocess.run(cmd,cwd=tree/'tb/pp_top',stdout=log,stderr=subprocess.STDOUT).returncode
        (p/(name+'.rc')).write_text(str(rc)+'\n')
        print(name,rc,flush=True)
        if rc: break
finally: f.write_text(original)
