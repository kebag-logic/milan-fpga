#!/usr/bin/env python3
"""Print-only probe of accepted RX final bytes, feed returns, stimuli and TX frames."""
import difflib,os,pathlib,subprocess,sys,tarfile
packet=pathlib.Path(__file__).resolve().parents[1];scratch=packet/"scratch";tree=scratch/"trace";receipt=packet/"receipts"
assert not tree.exists();tree.mkdir()
with tarfile.open(scratch/"source.tar") as f:f.extractall(tree,filter="data")
f=tree/"tb/pp_top/notify_phases.hpp";old=f.read_text();s=old
edits=[
("      seen.push_back({io.q_aecp.front(), io.t});\n", """      printf("TRACE_TX t=%llu bytes=", (unsigned long long)io.t);
      for (auto b : io.q_aecp.front()) printf("%02x", b);
      printf("\\n");
      seen.push_back({io.q_aecp.front(), io.t});
"""),
("""      tick();
    }
    io.d->rx_valid_i = 0;
""", """      tick();
      if (i + 1 == f.size()) printf("TRACE_RX_LAST t=%llu ethertype=%02x%02x\\n", (unsigned long long)io.t, f[12], f[13]);
    }
    io.d->rx_valid_i = 0;
"""),
("""    for (int i = 0; i < 4; ++i) tick();
  }
""", """    for (int i = 0; i < 4; ++i) tick();
    printf("TRACE_FEED_RETURN t=%llu ethertype=%02x%02x\\n", (unsigned long long)io.t, f[12], f[13]);
  }
"""),
("""    io.d->link_up_i = 0;
    one_notification""", """    printf("TRACE_LINK_DOWN t=%llu\\n", (unsigned long long)io.t);
    io.d->link_up_i = 0;
    one_notification"""),
("""    io.d->link_up_i = 1;
    one_notification""", """    printf("TRACE_LINK_UP t=%llu\\n", (unsigned long long)io.t);
    io.d->link_up_i = 1;
    one_notification""")]
for a,b in edits:
 assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b)
f.write_text(s)
(receipt/"trace-instrumentation.patch").write_text("".join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile="a/tb/pp_top/notify_phases.hpp",tofile="b/tb/pp_top/notify_phases.hpp")))
env=os.environ.copy();env.update(TMPDIR=str(scratch),REVIEW_LOCKDIR=str(scratch/"build-locks"),MAKEFLAGS="-j16")
for name,cmd in [("trace-build",["make","-j16","gsi-build","VERILATOR="+str(packet/"scripts/bounded-verilator.py")]),("trace",["./obj_dir/Vpp_top_sim","--domain-notify-only"])]:
 with (receipt/(name+".log")).open("w") as f:r=subprocess.run(cmd,cwd=tree/"tb/pp_top",env=env,stdout=f,stderr=subprocess.STDOUT)
 (receipt/(name+".rc")).write_text(str(r.returncode)+"\n");print(name,r.returncode,flush=True)
 if r.returncode:sys.exit(r.returncode)
