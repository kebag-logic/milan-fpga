#!/usr/bin/env python3
"""R273-7: the round-five named reader refusal can fail. Loads the gate's
own closure check (as new_cells_probe.py does; RV32 re-measure stubbed off)
and runs assert_character_closure() four ways:
  intact; `_CLOSURE_READERS_REFUSE` emptied; an extra name added to it (a
  cell the readers read as GCC does); and a directive-set closure patched,
  in a disposable copy, to admit a directive with no name.
Each but the first must FAIL.
usage: named_refusal_controls.py <repo-root> <work-dir> <out.json>"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util
spec = importlib.util.spec_from_file_location("ncp", Path(__file__).resolve().parent / "new_cells_probe.py")
src = (Path(__file__).resolve().parent / "new_cells_probe.py").read_text()
ncp = {"__name__": "ncp", "__file__": str(Path(__file__).resolve().parent / "new_cells_probe.py")}
exec(compile(src.replace("\nmain()\n", "\n"), "new_cells_probe.py", "exec"), ncp)
root, work, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
res = {}
ns = ncp["load"](root)
named = ns["_CLOSURE_READERS_REFUSE"]
res["intact"] = ncp["run"](ns["assert_character_closure"])
ns["_CLOSURE_READERS_REFUSE"] = ()
res["named-emptied"] = ncp["run"](ns["assert_character_closure"])
ns["_CLOSURE_READERS_REFUSE"] = named + ("byte 0x61 at the end of the file, in code",)
res["extra-name"] = ncp["run"](ns["assert_character_closure"])
text = (root / "sw/builder/test_builder.py").read_text(encoding="utf-8")
old = "            assert kind in firmware_directives, \\\n"
assert text.count(old) == 1
copy = work / "nameless-admitted"
(copy / "sw/builder").mkdir(parents=True, exist_ok=True)
(copy / "sw/builder/test_builder.py").write_text(text.replace(old, "            assert kind is None or kind in firmware_directives, \\\n"), encoding="utf-8")
ns2 = ncp["load"](copy)
res["closure-admits-nameless"] = ncp["run"](ns2["assert_character_closure"])
for k, v in res.items():
    print(f"{k:26} {'PASS' if v['ok'] else 'FAIL'}  {v['said'][:230]}")
out.write_text(json.dumps(res, indent=1, ensure_ascii=False))
