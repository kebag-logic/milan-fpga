import runpy,sys
from pathlib import Path
root=Path(__file__).resolve().parent
sys.argv=[str(root/"public-probes/r226_mutants.py"),str(Path.cwd()/"scripts"),str(root/"maintenance")]
m=runpy.run_path(sys.argv[0],run_name="r226_mutants_lib")
T="gen_toc_closer_cases.py"
target="I440-T-other-name pre/div "+repr("\n")
fixture="<pre>\n</style>\n## Probe\n"
m["MUTANTS"][:]=[
("M01-empty-new-population",[(T,'_OTHER_NAMES = ("div", "title", "xmp")','_OTHER_NAMES = ()')]),
("M02-drop-one-new-arm",[(T,'    return arms',f'    return [arm for arm in arms if arm[0] != {target!r}]')]),
("M03-add-valid-cross-name-arm",[(T,'    return arms',f'    arms.append(("maintenance positive cross-name", {fixture!r}, _probe_kind(TEXT)))\n    return arms')]),
]
m["main"]()
