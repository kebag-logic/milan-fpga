#!/usr/bin/env python3
"""Run real locale controls with locale/localedef absent from a restricted PATH."""
import argparse,contextlib,io,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("checkout",type=Path);p.add_argument("output",type=Path);p.add_argument("--child",action="store_true");a=p.parse_args();a.checkout=a.checkout.resolve();a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=True)
if not a.child:
    with tempfile.TemporaryDirectory(prefix="r251-unavailable-") as td:
        directory=Path(td);binpath=directory/"bin";binpath.mkdir();(binpath/"git").symlink_to(shutil.which("git"))
        env=dict(os.environ,PATH=str(binpath),LC_ALL="C",PYTHONUTF8="0",PYTHONCOERCECLOCALE="0",PYTHONIOENCODING="utf-8:backslashreplace",PYTHONDONTWRITEBYTECODE="1",GIT_CONFIG_NOSYSTEM="1",GIT_CONFIG_GLOBAL=os.devnull)
        cmd=[sys.executable,"-B",str(Path(__file__).resolve()),str(a.checkout),str(a.output),"--child"]
        r=subprocess.run(cmd,env=env,cwd=directory,capture_output=True)
        (a.output/"stdout").write_bytes(r.stdout);(a.output/"stderr").write_bytes(r.stderr)
        (a.output/"process.json").write_text(json.dumps({"argv":cmd,"restricted_path":str(binpath),"exit":r.returncode},indent=2)+"\n")
        assert r.returncode==0,r.stderr
        print(r.stdout.decode())
    raise SystemExit(0)
sys.path.insert(0,str(a.checkout/"scripts"))
import merge_containment_selftest_locale as loc
from merge_containment_selftest_scratch import quiet_git
assert shutil.which("locale") is None and shutil.which("localedef") is None
class Fixture:
    leftovers=[]
    rows=[]
    def case(self,name,got,want,why): self.rows.append({"name":name,"got":got,"want":want,"pass":got==want})
fx=Fixture();output=io.StringIO()
with quiet_git(),contextlib.redirect_stdout(output): loc.locale_cases(fx)
words=output.getvalue()
assert "NOT RUN locale-iso8859-1: localedef unavailable and no Latin-1 locale installed" in words,words
assert len(fx.rows)==86,len(fx.rows)
assert all(r["pass"] for r in fx.rows),fx.rows
assert not any("iso8859-1" in r["name"] for r in fx.rows),fx.rows
assert not fx.leftovers,fx.leftovers
record={"locale_found":shutil.which("locale"),"localedef_found":shutil.which("localedef"),"notice":words,"rows":fx.rows,"count":len(fx.rows),"latin1_checks":0,"leftovers":fx.leftovers}
(a.output/"result.json").write_text(json.dumps(record,indent=2)+"\n")
print(words,end="");print("PASS: 86 UTF-8/ASCII assertions; zero Latin-1 assertions; absence reported NOT RUN")
