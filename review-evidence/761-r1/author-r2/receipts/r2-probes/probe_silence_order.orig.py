#!/usr/bin/env python3
"""Observe a committed silence unlock, then unbind at each following cycle.

Usage: python3 probe_silence_order.py SOURCE_ROOT PINNED_SIMULATOR
The DUT is unchanged. Only a disposable copy of the existing harness gains
an independent count oracle, based on its public counter interface.
"""
import concurrent.futures
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile

packet = Path(__file__).resolve().parent
source = Path(sys.argv[1]).resolve()
simulator = Path(sys.argv[2]).resolve()
work = packet / "scratch" / "silence-order"
work.mkdir(parents=True, exist_ok=True)
archive = subprocess.check_output(["git", "-C", str(source), "archive", "HEAD", "hdl", "tb"])
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
    tf.extractall(work, filter="data")
harness = work / "tb/verilator/avtp_rxmon/sim_lockstep.cpp"
text = harness.read_text()
text = text.replace("    void si_causes();", "    void committed_silence_then_unbind();\n    void si_causes();")
addition = r'''
void Lockstep::committed_silence_then_unbind() {
    const int s = kN - 1;
    for (int delay = 0; delay <= 8; ++delay) {
        lock_and_settle(s);
        const uint32_t mu0 = gc_read(s, kColMu);
        const uint32_t si0 = gc_read(s, kColSi);
        int waited = 0;
        while (gc_read(s, kColMu) == mu0 && waited < 1400) {
            step(); ++waited;
        }
        const bool silence_committed = gc_read(s, kColMu) == mu0 + 1;
        c_.that("[ORDER] silence committed MEDIA_UNLOCKED while still bound", silence_committed);
        cycles(delay);
        bind(s, false);
        cycles(60);
        const uint32_t si = gc_read(s, kColSi) - si0;
        std::printf("ORDER N=%d delay=%d waited=%d prior_silence_unlock=%u interruption=%u\n",
                    kN, delay, waited, silence_committed, si);
        c_.dec("[ORDER] later unbind preserves the already committed silence interruption", si, 1);
        cycles(kUnlockCycles + 100);
        c_.dec("[ORDER] no further interruption after unbind", gc_read(s, kColSi) - si0, 1);
    }
}
'''
text = text.replace("void Lockstep::si_causes() {", addition + "\nvoid Lockstep::si_causes() {")
text = text.replace("    si_causes();\n    si_unbind_across_the_silence();", "    si_causes();\n    si_unbind_across_the_silence();\n    committed_silence_then_unbind();")
harness.write_text(text)
wrapper = work / "bounded-simulator"
wrapper.write_text("#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\n"
                   "for i,x in enumerate(a[:-1]):\n    if x == '-j': a[i+1]='4'\n"
                   f"os.execv({str(simulator)!r}, [{str(simulator)!r}]+a)\n")
wrapper.chmod(0o755)
env = dict(os.environ, VERILATOR=str(wrapper))
suite = work / "tb/verilator/avtp_rxmon"
with (packet / "silence-order-build.log").open("w") as log:
    rc = subprocess.run(["make", "-j16", "lockstep-build"], cwd=suite, env=env,
                        stdout=log, stderr=subprocess.STDOUT).returncode
(packet / "silence-order-build.rc").write_text(str(rc) + "\n")
if rc:
    sys.exit(rc)

def run(n):
    with (packet / f"silence-order-{n}.log").open("w") as log:
        rc = subprocess.run([str(suite / f"obj_ls{n}/Vavtp_rxmon_lockstep")],
                            cwd=suite, stdout=log, stderr=subprocess.STDOUT).returncode
    (packet / f"silence-order-{n}.rc").write_text(str(rc) + "\n")
    print("silence-order", n, "rc", rc, flush=True)
    return rc

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, (1, 8)))
sys.exit(any(results))
