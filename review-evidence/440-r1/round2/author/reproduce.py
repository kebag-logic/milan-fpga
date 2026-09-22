"""Replay the three exact R226-F1 mutants and selected real-Git CLI cases.
No renderer calls. Public scripts are loaded unchanged; case selection is explicit.
"""
import json,runpy,shutil,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parent
scripts=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve()
out.mkdir(parents=True,exist_ok=True)
sys.argv=[str(root/"public-probes/r226_mutants.py"),str(scripts),str(out/"mutants")]
m=runpy.run_path(sys.argv[0],run_name="r226_mutants_lib")
selected=[row for row in m["MUTANTS"] if row[0].startswith(("R15-","R16-"))]
close=m["CLOSE"]
selected.append(("X04-closer-add-xmp",[(m["T"],close,close.replace('"|".join(RAW_HTML_TAGS)', '"|".join(RAW_HTML_TAGS + ("xmp",))'))]))
m["MUTANTS"][:]=selected
m["main"]()
e=runpy.run_path(str(root/"public-probes/r226_e2e.py"),run_name="r226_e2e_lib")
e["CASES"][:]=[row for row in e["CASES"] if row[0].startswith(("E03-","E14-","E15-"))]
e["CASES"].append(("A164-xmp", "<pre>\n</xmp>\n"))
(out/"cli-cases.json").write_text(json.dumps(e["CASES"],indent=2)+"\n")
for label,edits in [("correct",[]),*selected]:
    with tempfile.TemporaryDirectory(prefix="a164.cli.") as tmp:
        dest=Path(tmp)/"scripts";shutil.copytree(scripts,dest,ignore=shutil.ignore_patterns("__pycache__"))
        for name,old,new in edits:
            p=dest/name; text=p.read_text();assert text.count(old)==1
            p.write_text(text.replace(old,new))
        sys.argv=[str(root/"public-probes/r226_e2e.py"),str(dest),label,str(out/"e2e")]
        e["main"]()
