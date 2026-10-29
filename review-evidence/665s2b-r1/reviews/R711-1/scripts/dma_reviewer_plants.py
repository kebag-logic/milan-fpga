#!/usr/bin/env python3
"""Reviewer-planted defects in KL_mbx_dma.sv, run against the tree's own bench (tb/verilator/mbx/dma_main.cpp).

Each arm copies the mover and its package to a scratch directory, writes one substitution (which must
occur exactly once), builds dma_main.cpp with the Makefile's own recipe (make print-dma-vflags), runs it
and reports caught (exit 1 with a [FAIL] line) or ESCAPED. The checkout is never written.
usage: dma_reviewer_plants.py CHECKOUT SCRATCH [--jobs N]
"""
import shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ARMS = (
    ("error-burst-continues", "            if (last_chunk_w || rerr_r || (beat_w && axi_rresp_i[1])) begin\n",
     "            if (last_chunk_w || (beat_w && axi_rresp_i[1])) begin\n"),
    ("held-partial-write-widened", "        pend_be_r    <= cpu_be_i;\n", "        pend_be_r    <= 4'hF;\n"),
    ("rerr-not-cleared", "              rerr_r      <= 1'b0;\n", ""),
    ("fill-during-cpu-answer", "assign fill_req_w  = (state_r == FILL_S) && !hold_r && !ack_cpu_r && (count_r != chunk_r);",
     "assign fill_req_w  = (state_r == FILL_S) && !hold_r && (count_r != chunk_r);"),
    ("rready-during-hold", "assign axi_rready_o  = (state_r == R_S) && !hold_r && !ack_cpu_r;",
     "assign axi_rready_o  = (state_r == R_S);"),
    ("tail-strobe-off-by-one", "4'((5'd1 << len_bytes_i[1:0]) - 5'd1);", "4'((5'd1 << len_bytes_i[1:0]));"),
    ("held-write-data-dropped", "        pend_wdata_r <= cpu_wdata_i;\n", "        pend_wdata_r <= '0;\n"),
    ("held-address-dropped", "        pend_addr_r  <= cpu_addr_i;\n", "        pend_addr_r  <= '0;\n"),
    ("receive-buffer-skew", "      buf_r[count_r[3:0]] <= host_rdata_i;", "      buf_r[count_r[3:0] + 4'd1] <= host_rdata_i;"),
    ("awlen-one-long", "assign axi_awlen_o   = 8'(chunk_r - 5'd1);", "assign axi_awlen_o   = 8'(chunk_r);"),
)


def main() -> int:
    checkout, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 4
    here = checkout / 'tb/verilator/mbx'
    rtl_dir = checkout / 'hdl/milan/mailbox'
    flags = [l for l in subprocess.run(['make', '-s', '-C', str(here), 'print-dma-vflags'], check=True,
                                       capture_output=True, text=True).stdout.splitlines() if l]
    def arm(spec):
        name, old, new = spec
        work = scratch / name
        if work.exists():
            shutil.rmtree(work)
        (work / 'rtl').mkdir(parents=True)
        for f in ('KL_mbx_pkg.sv', 'KL_mbx_dma.sv'):
            shutil.copy(rtl_dir / f, work / 'rtl' / f)
        t = work / 'rtl/KL_mbx_dma.sv'
        text = t.read_text()
        if text.count(old) != 1:
            return name, 'FIXTURE', f'{text.count(old)} occurrences'
        t.write_text(text.replace(old, new))
        b = subprocess.run([*flags, '--Mdir', str(work / 'obj'), str(work / 'rtl/KL_mbx_pkg.sv'), str(t),
                            str(here / 'dma_main.cpp'), '-o', 'Vmbx_dma'], cwd=here, capture_output=True, text=True)
        if b.returncode:
            return name, 'BUILD', b.stderr[-300:]
        try:
            r = subprocess.run([str(work / 'obj/Vmbx_dma')], capture_output=True, text=True, timeout=600)
        except subprocess.TimeoutExpired:
            return name, 'caught (timeout: the bench hung)', ''
        fails = [l.strip() for l in r.stdout.splitlines() if '[FAIL]' in l]
        return name, ('caught' if r.returncode != 0 and fails else f'ESCAPED rc {r.returncode}'), '; '.join(fails[:2])
    with ThreadPoolExecutor(jobs) as pool:
        results = list(pool.map(arm, ARMS))
    for n, v, d in results:
        print(f'{n}: {v}: {d[:300]}')
    print(f'reviewer plants: {sum(v.startswith("caught") for _, v, _ in results)} of {len(ARMS)} caught')
    return 0


if __name__ == '__main__':
    sys.exit(main())
