#!/usr/bin/env python3
import argparse,json,pathlib,subprocess,base64,hashlib
p=argparse.ArgumentParser();p.add_argument("packet",type=pathlib.Path);p.add_argument("--verilator",required=True);a=p.parse_args();root=a.packet/"scratch/fabric";repo="Mister-M-alt/protocol-processor-control-plane-avb-milan";rev="2ad2f845dd583f8310075fa2380cb60a04fd091a"
paths=["hdl/common/pp_pkg.sv","hdl/srp/srp_pkg.sv","hdl/acmp/KL_acmp_talker.sv","tb/acmp_talker/Makefile","tb/acmp_talker/sim_main.cpp","tb/acmp_talker/retry_cases.hpp","tb/common/verilator_harness.hpp"]
for path in paths:
 out=root/path
 if not out.exists():
  d=json.loads(subprocess.check_output(["gh","api",f"repos/{repo}/contents/{path}?ref={rev}"]));b=base64.b64decode(d["content"]);assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==d["sha"];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
version=subprocess.check_output([a.verilator,"--version"],text=True);assert "Verilator 5.050" in version
(a.packet/"receipts/rtl-version.txt").write_text(version)
work=root/"tb/acmp_talker";original=(work/"sim_main.cpp").read_text();flags="--cc --exe --build -j 4 --top-module KL_acmp_talker -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS -std=c++17"
def run(name):
 with (a.packet/"receipts"/(name+".log")).open("w") as f:r=subprocess.run(["make","-j16","run","VERILATOR="+a.verilator,"VFLAGS="+flags],cwd=work,stdout=f,stderr=subprocess.STDOUT)
 (a.packet/"receipts"/(name+".rc")).write_text(str(r.returncode)+"\n");print(name,r.returncode,flush=True);return r.returncode
rc=run("rtl-original")
replacement=r"""int rc = 0;
  for (uint32_t start : {uint32_t(50000), UINT32_MAX - 999u}) {
    Hn h;
    h.configure_the_talker_and_release_reset();
    h.check_the_boot_walk_allocates_every_source_da();
    auto check = [&](bool ok, const char* what) {
      ++h.checks;
      if (!ok) { ++h.fails; printf("FAIL: reviewer %s start=%u\n", what, start); }
    };
    check(h.decl_mask() == 0, "no answer and no Listener");
    h.set_lsn(0, LSN_ASKING_FAILED);
    check(h.decl_mask() == 1, "Asking Failed counts as registration");
    h.set_lsn(0, LSN_NONE);
    check(h.decl_mask() == 0, "last unprobed Listener withdrawal");
    h.d->now_ms_i = start;
    check(h.send(MT_PROBE, 3, C1, 0x222, L1, 7, FL_FC), "accepted probe");
    h.run(12);
    for (uint32_t age : {0u, 14999u, 15000u, 15001u}) {
      h.d->now_ms_i = start + age;
      h.fire_expiry(3);
      h.run(12);
      check(h.decl_mask() == (age < 15000u ? 8u : 0u), "half-open window and source isolation");
    }
    rc |= h.report();
  }
  return rc;"""
assert original.count("Hn h;\n  return h.run_suite();")==1
try:
 (work/"sim_main.cpp").write_text(original.replace("Hn h;\n  return h.run_suite();",replacement))
 rc|=run("rtl-edges")
finally:(work/"sim_main.cpp").write_text(original)
raise SystemExit(rc)
