#!/usr/bin/env python3
"""Independent doc-delta checks; no synthesis or repository modifications."""
import os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
import cmarkgfm,html5lib
root=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve()
scratch=Path(tempfile.mkdtemp(prefix="independent-probe-",dir=out/"scratch"))
def git(*args): return subprocess.check_output(["git","-C",str(root),*args])
head="173362fc21c33078b7feed42a24a3636907010f5"; parent="7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783"
path="docs/design/MARK_II_AREA_PLAN.md"
old=git("show",f"{parent}:{path}").decode(); new=(root/path).read_text()
assert new==old.replace("rtk proxy ","").replace("| AECP dispatch queue | 421 | 40 percent |\nThat", "| AECP dispatch queue | 421 | 40 percent |\n\nThat")
assert git("diff","--name-only",parent,head).decode().splitlines()==[path]
assert git("rev-list","--count",parent+".."+head).strip()==b"1"
print("PASS exact one-commit delta: two prefix removals, one table separator, no other bytes changed")
r=subprocess.run(["git","-C",str(root),"grep","-I","-n","-i","-w","rtk",head],capture_output=True)
assert r.returncode==1,(r.returncode,r.stdout.decode())
print("PASS no prefix token in tracked repository text, case-insensitive whole-word search")
for label,md,want in [("head",new,4),("pre-fix control",old,14)]:
    section=md.split("Its basis uses these shares:\n",1)[1].split("### Cumulative",1)[0]
    html=cmarkgfm.github_flavored_markdown_to_html(section)
    doc=html5lib.parseFragment(html,namespaceHTMLElements=False)
    rows=doc.findall(".//tbody/tr")
    if label=="head":
        assert len(rows)==want,len(rows)
        assert list(doc)[0].tag=="table" and list(doc)[1].tag=="p"
        para="".join(list(doc)[1].itertext())
        assert para.startswith("That displaces about 3,380 LUTs.") and "Neither lane receives credit" in para
        (out/"receipts"/"m3-head.html").write_text(html)
    else:
        assert len(rows)>4 and doc.findall(".//p")==[]
    print(f"PASS {label} render: {len(rows)} data rows; {len(doc.findall('.//p'))} prose paragraphs")
blocks=re.findall(r"```sh\n(.*?)\n```",new.split("### Reproduce L11b core pricing",1)[1],re.S)
assert len(blocks)==2
binpath=scratch/"bin"; binpath.mkdir(exist_ok=True)
for tool in ("bash","cat","mkdir"):
    target=binpath/tool
    if not target.exists(): target.symlink_to(shutil.which(tool))
# Redirect only the real lock path into this disposable probe, retaining real flock.
lock=binpath/"flock"
lock.write_text('#!/bin/bash\nset -eu\ntest "$1" = $VIVADO_LOCK\nshift\nexec /usr/bin/flock "$WORK/probe.lock" "$@"\n')
lock.chmod(0o755)
# Command stub records only invocation and simulates declared exit codes.
stub=binpath/"vivado"
stub.write_text('#!/bin/bash\nprintf "%s\\n" "$*" >> "$TRACE"\nif test "${FAIL_CORE:-}" = "${@: -1}"; then exit 23; fi\nexit 0\n')
stub.chmod(0o755)
for fail,expected_calls in [("",3),("vexii",1),("vexmin",2),("pico",3)]:
    work=scratch/("success" if not fail else "failure-"+fail)
    work.mkdir(exist_ok=True)
    trace=work/"calls.txt"
    if trace.exists(): trace.unlink()
    env={"PATH":str(binpath),"WORK":str(work),"TRACE":str(trace),"FAIL_CORE":fail,
         "CPU_VEXII_DIR":"/source/vexii","CPU_VEXMIN_DIR":"/source/vexmin","CPU_PICO_DIR":"/source/pico"}
    for i,block in enumerate(blocks):
        r=subprocess.run(["/bin/sh","-c",block],env=env,capture_output=True,text=True,timeout=30)
        assert r.returncode==(23 if fail and i==1 else 0),(fail,i,r.returncode,r.stderr)
    lines=trace.read_text().splitlines(); assert len(lines)==expected_calls
    for core in ["vexii","vexmin","pico"][:expected_calls]:
        assert (work/core/(core+".rc")).read_text().strip()==("23" if core==fail else "0")
    assert (work/"price_core.tcl").read_text().endswith('puts "PRICED $name"\n')
    print(f"PASS literal /bin/sh blocks: failure={fail or 'none'}, invocations={len(lines)}, exit/rc propagation correct")
# Restore only the removed prefix in the disposable copy; ordinary PATH must refuse it.
control=blocks[0].replace("bash -c", "rtk proxy bash -c",1)
r=subprocess.run(["/bin/sh","-c",control],env=env,capture_output=True,text=True,timeout=30)
assert r.returncode==127
print("PASS prefix-restored negative control: exit 127; production command stub never invoked")
print("LIMIT: lock path redirected to scratch; command stub tests shell behavior; no area, timing, physical or full synthesis evidence")
