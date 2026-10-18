#!/usr/bin/env python3
"""Run bounded command-engine checks in disposable exported source trees."""
import argparse
import concurrent.futures
import io
import os
from pathlib import Path
import subprocess
import tarfile

BASE = "22c139a4323bc96c779d13e3f6774480c5fb9b75"
HEAD = "29f58ad30a97327d92b50f17f49d085cd97066a5"

PROBE = r'''
  int checks = 0, failures = 0;
  for (int cdl = 12; cdl <= 140; ++cdl) {
    Stim s; s.ct = 0x000E; s.cdl = cdl;
    put16(s.bytes, 24, 6); put32(s.bytes, 28, 0x20000000u);
    put32(s.bytes, 48, 750000); put16(s.bytes, 70, 0xA5A5);
    const Result r = run(s);
    const int want = (cdl == 60 || cdl == 96) ? 0 : 7;
    const bool pass = !r.timeout && r.resp && r.status == want && r.cdl == 96;
    ++checks; failures += !pass;
    printf("LENGTH cdl=%d body=%d status=%d response_cdl=%d expected_status=%d %s\n",
           cdl, cdl-12, r.status, r.cdl, want, pass ? "PASS" : "FAIL");
  }
  for (int cdl : {60, 96}) {
    for (int scenario = 0; scenario < 7; ++scenario) {
      Stim s; s.ct = 0x000E; s.cdl = cdl;
      put16(s.bytes, 24, scenario == 5 ? 5 : 6);
      put16(s.bytes, 26, scenario == 6 ? 5 : 0);
      put32(s.bytes, 28, scenario == 1 ? 0 : scenario == 2 ? 0x20000008u : 0x20000000u);
      put32(s.bytes, 48, scenario == 3 ? 0x80000001u : 750000);
      put16(s.bytes, 70, 0xA5A5); s.running = scenario == 4;
      const int statuses[] = {0, 11, 11, 7, 12, 11, 2};
      const Result r = run(s);
      bool bytes = true;
      for (int off = 24; off < 108; ++off) {
        int want = (cdl == 60 && off >= 70) ? 0 : s.bytes[off];
        bytes = bytes && frame[14+off] == want;
      }
      bool pass = !r.timeout && r.resp && r.status == statuses[scenario] && r.cdl == 96 && bytes;
      ++checks; failures += !pass;
      printf("SEMANTICS cdl=%d scenario=%d status=%d response_cdl=%d bytes=%d %s\n",
             cdl, scenario, r.status, r.cdl, bytes, pass ? "PASS" : "FAIL");
    }
  }
  printf("REVIEW_PROBE %d checks, %d failures\n", checks, failures);
  return failures ? 1 : 0;
}
'''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--verilator", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=3, choices=range(1, 4))
    args = ap.parse_args()
    packet = Path(__file__).resolve().parents[1]
    receipt = packet / "receipts"
    scratch = packet / "scratch"
    version = subprocess.check_output([str(args.verilator), "--version"], text=True)
    assert "Verilator 5.050" in version, version
    (receipt / "compiler-identity.txt").write_text(version)

    def campaign(name, rev, probe):
        root = scratch / name
        root.mkdir(parents=True, exist_ok=True)
        data = subprocess.check_output(["git", "-C", str(args.repo), "archive", rev])
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            tf.extractall(root, filter="data")
        if probe:
            src = root / "tb/aecp_cmds/sim_main.cpp"
            text = src.read_text()
            src.write_text(text[:text.index("  const std::vector<Tpl> tpls = templates();")] + PROBE)
        wrapper = root / "bounded-compiler"
        wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i]=='-j': a[i+1]='4'\nos.execv(" + repr(str(args.verilator)) + ", [" + repr(str(args.verilator)) + "]+a)\n")
        wrapper.chmod(0o755)
        command = ["make", "-j16", "-C", "tb/aecp_cmds", "build" if probe else "run", "VERILATOR="+str(wrapper)]
        with (receipt / (name+".log")).open("w") as log:
            log.write("revision="+rev+"\n"); log.flush()
            rc = subprocess.run(command, cwd=root, stdout=log, stderr=subprocess.STDOUT).returncode
            if rc == 0 and probe:
                rc = subprocess.run(["./obj_dir/Vaecp_cmds"], cwd=root/"tb/aecp_cmds", stdout=log, stderr=subprocess.STDOUT).returncode
        (receipt/(name+".rc")).write_text(str(rc)+"\n")
        if not probe and rc == 0:
            (receipt/"head-observed.json").write_bytes((root/"tb/aecp_cmds/obj_dir/observed.json").read_bytes())
        return name, rc

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(campaign, *job) for job in [("head-engine-suite", HEAD, False), ("head-length-probe", HEAD, True), ("base-length-probe", BASE, True)]]
        for future in concurrent.futures.as_completed(futures):
            print(*future.result(), flush=True)

if __name__ == "__main__":
    main()
