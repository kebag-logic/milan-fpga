#!/usr/bin/env python3
"""Measured parent locales: production and exact b911 assertion restoration."""
import argparse, codecs, concurrent.futures, contextlib, hashlib, io, json, os, subprocess, sys, tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("checkout",type=Path);p.add_argument("output",type=Path);p.add_argument("--child",choices=["utf-8","iso8859-1"]);a=p.parse_args()
a.checkout=a.checkout.resolve();a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=True)
if a.child:
    actual=codecs.lookup(sys.getfilesystemencoding()).name
    assert actual==a.child,(actual,a.child)
    sys.path.insert(0,str(a.checkout/"scripts"))
    import check_merge_containment as mc
    import merge_containment_selftest_retention as retention
    from merge_containment_selftest_replay import _History
    from merge_containment_selftest_scratch import quiet_git
    from merge_containment_selftest import _Fixture
    rows=[];runs=[]
    def case(name,got,want,why): rows.append({"name":name,"got":got,"want":want,"pass":got==want})
    def run(args):
        output=io.StringIO()
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(io.StringIO()): rc=mc.main(["checker",*args])
        runs.append({"argv":args,"exit":rc,"output":output.getvalue()})
        return rc,output.getvalue()
    with quiet_git():
        history=_History();history._git("init","-q","-b","main")
        retention._path_and_format_cases(_Fixture(mc,case,run),history)
        tree=retention._tree({"raw-\udcff":("100644",b"oracle")})
        raw=subprocess.check_output(["git","ls-tree","-z",tree])
    name=raw.split(b"\t",1)[1].removesuffix(b"\0")
    assert name==b"raw-\xff",name
    bad=[r for r in rows if not r["pass"]]
    assert len(rows)==22,len(rows)
    record={"encoding":actual,"assertions":len(rows),"failures":bad,"rows":rows,"runs":runs,"fixture_name_hex":name.hex(),"raw_tree_record_hex":raw.hex(),"input_repr":repr("raw-\udcff"),"filesystem_repr":repr(os.fsdecode(name)),"roundtrip_hex":os.fsencode(os.fsdecode(name)).hex()}
    (a.output/"result.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps(record,ensure_ascii=True))
    raise SystemExit(bool(bad))
with tempfile.TemporaryDirectory(prefix="r251-r3-locale-") as td:
    work=Path(td);loc=work/"locales";loc.mkdir()
    cmd=["localedef","--no-archive","-i","en_US","-f","ISO-8859-1",str(loc/"en_US.ISO-8859-1")]
    r=subprocess.run(cmd,capture_output=True)
    (a.output/"localedef.stdout").write_bytes(r.stdout);(a.output/"localedef.stderr").write_bytes(r.stderr)
    assert r.returncode==0,("Latin-1 NOT RUN",r.stderr)
    old=work/"restored-b911";(old/"scripts").mkdir(parents=True)
    for f in (a.checkout/"scripts").glob("*containment*.py"): (old/"scripts"/f.name).write_bytes(f.read_bytes())
    path="scripts/merge_containment_selftest_retention.py"
    before=subprocess.check_output(["git","-C",str(a.checkout),"show","b911c11671cae329a99f5e413133b4bf6357fa7f:"+path])
    (old/path).write_bytes(before)
    (a.output/"restored-retention-blob.py").write_bytes(before)
    records=[]
    def one(item):
        label,source,encoding,locale=item
        dest=a.output/(label+"-"+encoding);dest.mkdir()
        cwd=work/(label+"-"+encoding);cwd.mkdir()
        env=dict(os.environ,LC_ALL=locale,LOCPATH=str(loc),PYTHONUTF8="0",PYTHONCOERCECLOCALE="0",PYTHONIOENCODING="utf-8:backslashreplace",PYTHONDONTWRITEBYTECODE="1",GIT_CONFIG_NOSYSTEM="1",GIT_CONFIG_GLOBAL=os.devnull)
        cmd=[sys.executable,"-B",str(Path(__file__).resolve()),str(source),str(dest),"--child",encoding]
        r=subprocess.run(cmd,env=env,cwd=cwd,capture_output=True)
        (dest/"focused.stdout").write_bytes(r.stdout);(dest/"focused.stderr").write_bytes(r.stderr)
        expected=1 if label=="restored-b911" and encoding=="iso8859-1" else 0
        row={"source":label,"encoding":encoding,"environment":{k:env[k] for k in ("LC_ALL","LOCPATH","PYTHONUTF8","PYTHONCOERCECLOCALE")},"focused_argv":cmd,"focused_exit":r.returncode,"expected_exit":expected}
        assert r.returncode==expected,(row,r.stderr)
        focused=json.loads((dest/"result.json").read_bytes())
        assert len(focused["failures"])==expected,focused["failures"]
        if expected: assert focused["failures"][0]["name"]=="retention-literal-revert-'raw-\\udcff'-path",focused["failures"]
        cmd=[sys.executable,"-B",str(source/"scripts/check_merge_containment.py"),"--selftest"]
        r=subprocess.run(cmd,env=env,cwd=cwd,capture_output=True)
        (dest/"full.stdout").write_bytes(r.stdout);(dest/"full.stderr").write_bytes(r.stderr)
        lines=r.stdout.decode("utf-8","backslashreplace").splitlines()
        assertions=[line for line in lines if line.startswith(("  ok  ","  FAIL"))]
        failures=[line for line in assertions if line.startswith("  FAIL")]
        row.update(full_argv=cmd,full_exit=r.returncode,full_assertions=len(assertions),failure_lines=failures)
        (dest/"process.json").write_text(json.dumps(row,indent=2)+"\n")
        assert r.returncode==expected,(row,r.stderr)
        assert len(assertions)==455 and len(failures)==expected,row
        print(label,encoding,"focused",len(focused["rows"])-len(focused["failures"]),"/22; full",len(assertions)-len(failures),"/455; exit",r.returncode,flush=True)
        return row
    items=[(label,source,encoding,locale) for label,source in [("current",a.checkout),("restored-b911",old)] for encoding,locale in [("utf-8","C.UTF-8"),("iso8859-1","en_US.ISO-8859-1")]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: records=list(pool.map(one,items))
    (a.output/"processes.json").write_text(json.dumps(records,indent=2)+"\n")
print("PASS: corrected parents pass; b911 assertion restoration detects precisely F3")
