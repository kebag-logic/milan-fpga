#!/usr/bin/env python3
"""Focused independent review probes; source checkout is read-only.
Usage: python3 run_probes.py CHECKOUT PACKET PINNED_SIMULATOR
All disposable inputs and builds live under PACKET/scratch.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys

root, packet, simulator = map(lambda x: Path(x).resolve(), sys.argv[1:])
scratch = packet / 'scratch'
scratch.mkdir(exist_ok=True)
receipts = packet / 'probes'
receipts.mkdir(exist_ok=True)
wrapper = scratch / 'bounded_simulator.py'
wrapper.write_text('#!/usr/bin/env python3\nimport os, sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i] in ("-j", "--build-jobs"): a[i+1]="1"\nos.execv(' + repr(str(simulator)) + ', [' + repr(str(simulator)) + ']+a)\n')
wrapper.chmod(0o755)
env = dict(os.environ, VERILATOR=str(wrapper), TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
aaf = 'hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv'
crf = 'hdl/ieee1722/crf/KL_crf_rx.sv'
src = {k: (root / k).read_text() for k in (aaf, crf)}
def replace(text, anchor, value):
    assert text.count(anchor) == 1, (anchor, text.count(anchor))
    return text.replace(anchor, value)
cases = []
def case(name, kind, rtl=None, harness=None, expected=None):
    cases.append((name, kind, rtl, harness, expected))
case('aaf_clean', 'aaf')
case('crf_clean', 'crf')
case('aaf_no_advance', 'aaf', replace(src[aaf], 'monst_r <= {ram_q_r[31:8], cur_w.seq};', 'monst_r <= ram_q_r;'), expected='[SQ2c]')
case('aaf_whole_state', 'aaf', replace(src[aaf], 'monst_r <= {ram_q_r[31:8], cur_w.seq};', 'monst_r <= monst_next_w;'), expected='[SQ2d]')
case('aaf_timestamp_walk', 'aaf', replace(src[aaf], 'mst_r   <= M_PSEQ_S;', 'mst_r   <= M_PWR_S;'), expected='[SQ1d]')
anchor = "          exp_seq_r <= seq_i + 8'd1;\n        end else begin"
case('crf_no_advance', 'crf', replace(src[crf], anchor, '        end else begin'), expected='[SQ-b2]')
case('crf_reject_seeds', 'crf', replace(src[crf], anchor, "          exp_seq_r <= seq_i + 8'd1;\n          have_seq_r <= 1'b1;\n        end else begin"), expected='[SQ-d1]')
for kind, path, expected in [('aaf', aaf, '[SQ2c]'), ('crf', crf, '[SQ-b2]')]:
    base = subprocess.check_output(['git', 'show', 'a032c6d6:'+path], cwd=root, text=True)
    case(kind+'_base', kind, base, expected=expected)
h = (root / 'tb/verilator/avtp_rxmon/sim_main_nx.cpp').read_text()
h = replace(h, 'uint8_t q = 40;', 'uint8_t q = 246;')
h = replace(h, 'lctx_rd(3, 8) & 0xFF, q - 1);', 'lctx_rd(3, 8) & 0xFF, static_cast<uint8_t>(q - 1));')
h = replace(h, 'const long tsd0 = lctx_rd(3, 10);', 'const long tsd0 = lctx_rd(3, 10);\n        const long state0 = lctx_rd(3, 8);\n        const long stamp0 = lctx_rd(3, 9);\n        const long other0 = lctx_rd(0, 8);')
h = replace(h, 'off_format(0xA55AC33CUL + 1000);', 'off_format(0xA55AC33CUL + 1000);\n        ck("[EXTRA] upper state preserved", lctx_rd(3, 8) >> 8, state0 >> 8);\n        ck("[EXTRA] LAST_TS preserved", lctx_rd(3, 9), stamp0);\n        ck("[EXTRA] other stream preserved", lctx_rd(0, 8), other0);')
case('aaf_wrap_state', 'aaf', harness=h)
h = (root / 'tb/verilator/crf_rx/sim_main.cpp').read_text()
h = replace(h, '        send_in_order_then_commit(10);', '        seq = 245;\n        send_in_order_then_commit(10);')
case('crf_wrap', 'crf', harness=h)

def run(item):
    name, kind, rtl, harness, expected = item
    work = scratch / name
    work.mkdir(exist_ok=True)
    suite = root / 'tb/verilator' / ('avtp_rxmon' if kind == 'aaf' else 'crf_rx')
    rtlpath = root / (aaf if kind == 'aaf' else crf)
    if rtl is not None:
        rtlpath = work / 'input.sv'
        rtlpath.write_text(rtl)
    cmd = ['make', '-j16', '-C', str(suite), 'nx-build' if kind == 'aaf' else 'unit-build', 'VERILATOR='+str(wrapper)]
    cmd += [('RXMON_SRC=' if kind == 'aaf' else 'RX_RTL=')+str(rtlpath), ('NX_MDIR=' if kind == 'aaf' else 'UNIT_MDIR=')+str(work / 'obj')]
    if harness is not None:
        hp = work / 'harness.cpp'
        hp.write_text(harness)
        if kind == 'crf':
            cmd.append('UNIT_CPP='+str(hp))
        else:
            # Keep the repository recipe and add the original include directory.
            mf = work / 'Makefile'
            mf.write_text((suite / 'Makefile').read_text().replace(' sim_main_nx.cpp ', ' '+str(hp)+' ').replace('-std=c++17 -O2 -Wall', '-I'+str(suite)+' -std=c++17 -O2 -Wall'))
            cmd += ['-f', str(mf)]
    with (receipts / (name+'.build.log')).open('w') as log:
        log.write('command: '+repr(cmd)+'\n'); log.flush()
        built = subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT)
    (receipts / (name+'.build.rc')).write_text(str(built.returncode)+'\n')
    result = {'case': name, 'build_rc': built.returncode, 'expected_failure': expected}
    if built.returncode == 0:
        exe = work / 'obj' / ('Vavtp_rxmon_nx_sim' if kind == 'aaf' else 'Vcrf_rx_sim')
        ran = subprocess.run([str(exe)], cwd=suite, env=env, capture_output=True, text=True)
        output = ran.stdout+ran.stderr
        (receipts / (name+'.run.log')).write_text(output)
        (receipts / (name+'.run.rc')).write_text(str(ran.returncode)+'\n')
        failures = [line for line in output.splitlines() if '[FAIL]' in line]
        passed = ran.returncode == 0 if expected is None else ran.returncode == 1 and any(expected in line for line in failures)
        result.update(run_rc=ran.returncode, pass_=passed, failures=failures)
    else:
        result['pass_'] = False
    print(name, 'PASS' if result['pass_'] else 'FAIL', flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, cases))
(packet / 'probe_results.json').write_text(json.dumps(results, indent=2)+'\n')
raise SystemExit(0 if all(r['pass_'] for r in results) else 1)
