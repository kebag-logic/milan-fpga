#!/usr/bin/env python3
"""Replay public probes and current port phases in disposable exact-head trees."""
import argparse, concurrent.futures, io, pathlib, subprocess, tarfile, time

HEAD = '409c3075a6c5525d283de5a93584ad87a4528137'
p = argparse.ArgumentParser()
p.add_argument('--repo', type=pathlib.Path, required=True)
p.add_argument('--compiler', default='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
p.add_argument('--jobs', type=int, default=16)
a = p.parse_args()
assert 4 <= a.jobs <= 16
root = pathlib.Path(__file__).resolve().parent
assert subprocess.check_output(['git','-C',str(a.repo),'rev-parse','HEAD'],text=True).strip() == HEAD
version = subprocess.check_output([a.compiler,'--version'],text=True)
assert 'Verilator 5.050' in version
(root/'compiler-identity.txt').write_text(version)
archive = subprocess.check_output(['git','-C',str(a.repo),'archive',HEAD])
sources = ['ucpu/gptp_ucpu_pkg.sv','ucpu/KL_gptp_ucpu.sv','wire/KL_gptp_rx_parser.sv','wire/KL_gptp_tx_slot.sv','common/KL_gptp_timer.sv','top/KL_gptp_engine.sv']

def run(case):
    tree = root/'scratch'/case
    tree.mkdir(parents=True,exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar: tar.extractall(tree,filter='data')
    src = tree/'tb/verilator/engine/sim_main.cpp'
    s = src.read_text()
    if case.startswith('r730') or case == 'permanent':
        start=s.index('  int run_suite() {'); end=s.index('\n private:',start)
        calls='    independent_port_probes();'
        if case != 'r730-probe':
            calls='''    bring_the_engine_out_of_reset();
    settle_as_capable_master("focused setup");
    boot_watch = false;
    end_the_cease_on_a_port_toggle();
    drop_ascapable_at_a_link_loss();
    drop_a_frame_built_across_the_fall();
    keep_the_countdown_exit();'''
        if case == 'permanent':
            calls+='''
    complete_no_exchange_across_the_fall();
    withdraw_a_frame_stalled_at_its_first_byte();
    finish_a_frame_started_before_the_fall();
    end_a_retained_cease_at_the_first_rise();'''
        s=s[:start]+'  int run_suite() {\n'+calls+'\n    printf("%d checks: %d PASS, %d FAIL\\n", checks, checks-fails, fails);\n    return fails ? 1 : 0;\n  }\n'+s[end:]
        s=s.replace('\n private:','\n private:\n'+(root/'public/reviews/R730-1/probe.cpp.inc').read_text(),1)
    else:
        pub=root/'public/reviews/R729-1/scripts'
        probe=(pub/'probe_phases.cpp').read_text()+(pub/'probe_phases2.cpp').read_text()
        needle='    raise_ascapable_on_the_second_exchange();\n'
        j=s.index(needle,s.index('  void run_every_phase() {'))+len(needle)
        calls='''    r729_probe_warm_reset_port_low(true, "R729 D low-at-release");
    r729_probe_warm_reset_port_low(false, "R729 D fall-after-release");
    r729_probe_fu_after_fall();
    r729_probe_glitch(1, "R729 B1");
    r729_probe_glitch(3, "R729 B3");
    return;
'''
        if case=='r729-sweep': calls='    r729_probe_rise_near_the_beat();\n    return;\n'
        s=s[:j]+calls+s[j:]
        anchor='  // ---- 41: #89, sync receipt ageing needs gmPresent'
        assert s.count(anchor)==1
        s=s.replace(anchor,probe+'\n'+anchor)
    src.write_text(s)
    work=src.parent
    cmd=[a.compiler,'--cc','--exe','--build','-j',str(a.jobs//4),'--top-module','KL_gptp_engine','-Wno-fatal','-Wno-DECLFILENAME','-Wno-UNUSEDSIGNAL','-Wno-WIDTHEXPAND','-Wno-WIDTHTRUNC','-Wno-UNUSEDPARAM','-GUCODE_HEX_P="gptp_ucode.hex"','-GCLK_HZ_P=2000000','-CFLAGS','-std=c++17 -O2',*[str(tree/'hdl'/x) for x in sources],'sim_main.cpp','-o','Vprobe']
    for step,command in [('build',cmd),('run',['./obj_dir/Vprobe'])]:
        t=time.monotonic()
        with (root/(case+'-'+step+'.log')).open('w') as f:
            r=subprocess.run(command,cwd=work,stdout=f,stderr=subprocess.STDOUT,timeout=540)
        (root/(case+'-'+step+'.rc')).write_text(str(r.returncode)+'\n')
        print(case,step,'rc',r.returncode,'seconds',round(time.monotonic()-t,2),flush=True)
        if r.returncode: return False
    return True

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,['r730-probe','r730-focused','r729-probes','r729-sweep','permanent']))
raise SystemExit(0 if all(results) else 1)
