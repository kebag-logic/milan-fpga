from pathlib import Path
import subprocess
import sys

root = Path('/tmp/502-a345')
tb = root / 'export/tb/verilator/pp_shadow'
s = (tb / 'sim_main.cpp').read_text()
s = s.replace('    PendingObs pending;', '    unsigned key_in_cycles=0, key_out_cycles=0, key_overlap_cycles=0;\n    PendingObs pending;')
anchor = '        const auto* rp = dut->rootp;\n        const bool name ='
replacement = '''        const auto* rp = dut->rootp;
        const bool in_key = rp->milan_datapath__DOT__amap_edit_in_key_v_w;
        const bool out_key = rp->milan_datapath__DOT__amap_edit_out_key_v_w;
        key_in_cycles += in_key;
        key_out_cycles += out_key;
        key_overlap_cycles += in_key && out_key;
        const bool name ='''
assert s.count(anchor) == 1
s = s.replace(anchor, replacement)
anchor = '        printf("pp_shadow: %ld checks, %ld failures\\n", checks, fails);'
replacement = '''        ck("PRIORITY key-valid overlap cycles", key_overlap_cycles, 0);
        ck("PRIORITY input key witnessed", key_in_cycles != 0, 1);
        if (PRIORITY_DYNAMIC) ck("PRIORITY output key witnessed", key_out_cycles != 0, 1);
        printf("PRIORITY input cycles %u, output cycles %u, overlap cycles %u\\n",
               key_in_cycles, key_out_cycles, key_overlap_cycles);
'''
assert s.count(anchor) == 1
s = s.replace(anchor, replacement + anchor)
(tb / 'priority_probe_main.cpp').write_text('#ifndef PRIORITY_DYNAMIC\n#define PRIORITY_DYNAMIC 0\n#endif\n' + s)
(root / 'priority_probes.vlt').write_text('`verilator_config\npublic_flat_rd -module "milan_datapath" -var "amap_edit_in_key_v_w"\npublic_flat_rd -module "milan_datapath" -var "amap_edit_out_key_v_w"\n')
for leg in ('static', 'dynamic'):
    cmd = ['make', 'run-pending' if leg == 'dynamic' else 'run-base', 'CPP=priority_probe_main.cpp', f'VERILATOR=verilator {root}/priority_probes.vlt']
    if leg == 'static':
        cmd += ['SIM_ARGS=--pending-only', f'BUILD_DIR={root}/priority-static']
    else:
        cmd += [f'PENDING_BUILD_DIR={root}/priority-dynamic', 'CXXFLAGS=-DPRIORITY_DYNAMIC=1']
    subprocess.run([sys.executable, str(root / 'gate.py'), 'priority-' + leg, *cmd], cwd=tb, check=True, timeout=43200)
