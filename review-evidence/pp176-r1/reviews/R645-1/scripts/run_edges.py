#!/usr/bin/env python3
"""Run boundary, short-slot and poisoned-tail cases, plus a published mutant."""
import argparse
import concurrent.futures
import io
from pathlib import Path
import subprocess
import tarfile
from run_focus import HEAD

EDGE = r'''
  int checks = 0, failures = 0;
  for (int cdl : {60, 96}) {
    for (uint32_t lat : {0u, 0x7FFFFFFFu, 0x80000000u, 0xFFFFFFFFu}) {
      for (int trunc : {0, 1}) {
        Stim s; s.ct = 0x000E; s.cdl = cdl; s.actual_slot = 12 + cdl - trunc;
        for (int k = 24; k < 12+cdl; ++k) s.bytes[k] = uint8_t(k*7);
        put16(s.bytes, 24, 6); put16(s.bytes, 26, 0);
        put32(s.bytes, 28, 0x20000000u); put32(s.bytes, 48, lat);
        put16(s.bytes, 70, 0xA5A5);
        const Result r = run(s);
        int want = trunc || (lat >> 31) ? 7 : 0;
        bool bytes = true;
        for (int off = 24; off < 108; ++off) {
          int expected = trunc ? (off == 25 ? 6 : 0) :
                         (cdl == 60 && off >= 70 ? 0 : s.bytes[off]);
          bytes = bytes && frame[14+off] == expected;
        }
        bool pass = !r.timeout && r.resp && r.status == want && r.cdl == 96 && bytes;
        ++checks; failures += !pass;
        printf("EDGE cdl=%d latency=%08x short_by=%d status=%d response_cdl=%d bytes=%d %s\n",
               cdl, lat, trunc, r.status, r.cdl, bytes, pass ? "PASS" : "FAIL");
      }
    }
  }
  printf("REVIEW_EDGES %d checks, %d failures\n", checks, failures);
  return failures ? 1 : 0;
}
'''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--verilator', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=2, choices=[1, 2])
    a = ap.parse_args()
    packet = Path(__file__).resolve().parents[1]
    def run(name, mutant):
        root = packet/'scratch'/name
        root.mkdir(parents=True, exist_ok=True)
        data = subprocess.check_output(['git','-C',str(a.repo),'archive',HEAD])
        with tarfile.open(fileobj=io.BytesIO(data)) as tf: tf.extractall(root, filter='data')
        src=root/'tb/aecp_cmds/sim_main.cpp'
        text=src.read_text()
        text=text.replace('  int cdl = 12;', '  int cdl = 12;\n  int actual_slot = -1;')
        text=text.replace('  dut->rxs_slot_len_i = len > 576 ? 576 : len;', '  for (int n = len; n < int(slot.size()); ++n) slot[n] = 0xD7;\n  dut->rxs_slot_len_i = s.actual_slot < 0 ? len : s.actual_slot;')
        src.write_text(text[:text.index('  const std::vector<Tpl> tpls = templates();')]+EDGE)
        if mutant:
            patch=packet/'receipts/public/author/mutants/patches/sinfo13-reserved-echoed.patch'
            subprocess.run(['git','apply',str(patch)],cwd=root,check=True)
        wrapper=root/'bounded-compiler'
        wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=='-j': a[i+1]='4'\nos.execv("+repr(str(a.verilator))+", ["+repr(str(a.verilator))+"]+a)\n")
        wrapper.chmod(0o755)
        with (packet/'receipts'/(name+'.log')).open('w') as log:
            rc=subprocess.run(['make','-j16','-C','tb/aecp_cmds','build','VERILATOR='+str(wrapper)],cwd=root,stdout=log,stderr=subprocess.STDOUT).returncode
            if rc==0:rc=subprocess.run(['./obj_dir/Vaecp_cmds'],cwd=root/'tb/aecp_cmds',stdout=log,stderr=subprocess.STDOUT).returncode
        (packet/'receipts'/(name+'.rc')).write_text(str(rc)+'\n')
        return name,rc
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        for result in pool.map(lambda t:run(*t), [('head-edge-control',False),('reserved-word-mutant',True)]):print(*result,flush=True)

if __name__=='__main__':main()
