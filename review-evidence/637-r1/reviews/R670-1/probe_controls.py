#!/usr/bin/env python3
"""Run two focused fault controls concurrently, at six build jobs each."""
import concurrent.futures
import os
from pathlib import Path
import subprocess

p = Path(__file__).resolve().parent
work = p / 'scratch/probe'
original = (work / 'hdl/milan/milan_datapath.sv').read_text()
controls = {
    'hole-control': ("amr_malformed_r <= 1'b1;", "amr_malformed_r <= 1'b0;"),
    'putback-control': ("amr_step_r <= 2'd2;                  //! refused: the reset set back",
                        "amr_step_r <= 2'd2;                  //! control: no put-back"),
}
env = dict(os.environ, TMPDIR=str(p / 'scratch'), PYTHONDONTWRITEBYTECODE='1')
compiler = env.get('REVIEW_VERILATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
def run(name):
    if name == 'hole-control':
        a, b = controls[name]
        assert original.count(a) == 1
        text = original.replace(a, b)
    else:
        a = """          end else if ((amr_step_r == 2'd1) && !amr_ok_r) begin
            amr_step_r <= 2'd2;                  //! refused: the reset set back
            amr_src_r  <= 1'b1;
            amr_st_r   <= AS_ECNT;"""
        b = """          end else if ((amr_step_r == 2'd1) && !amr_ok_r) begin
            amr_r_r <= amr_r_r + AMR_RW_C'(1);
            amr_st_r <= AS_RNEXT;"""
        assert original.count(a) == 1
        text = original.replace(a, b)
    rtl = p / 'scratch' / (name + '.sv')
    rtl.write_text(text)
    mdir = p / 'scratch' / ('obj-' + name)
    cmd = ['make', '-j16', '-C', 'tb/verilator/milan_dp', '-o', 'ltn_rom.hex',
           '-o', 'ucode.hex', 'dynmap-build', 'VERILATOR=' + compiler,
           'VERILATOR_JOBS=6', 'DP_SRC=' + str(rtl), 'DYNMAP_MDIR=' + str(mdir)]
    with (p / 'receipts' / (name + '-build.log')).open('w') as f:
        rc = subprocess.run(cmd, cwd=work, env=env, stdout=f,
                            stderr=subprocess.STDOUT, check=False).returncode
    (p / 'receipts' / (name + '-build.rc')).write_text(str(rc) + '\n')
    if rc:
        print(name, 'BUILD FAILED', rc, flush=True)
        return
    with (p / 'receipts' / (name + '-run.log')).open('w') as f:
        rc = subprocess.run([str(mdir / 'Vmilan_dp_dynmap')],
                            cwd=work / 'tb/verilator/milan_dp', env=env, stdout=f,
                            stderr=subprocess.STDOUT, check=False).returncode
    (p / 'receipts' / (name + '-run.rc')).write_text(str(rc) + '\n')
    print(name, 'run rc', rc, flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(run, controls))
