#!/usr/bin/env python3
"""Plant one fault into a copied tree for the Yosys gate probes.

usage: plant.py <tree> <kind> <arg>
  kinds:
    absent <Module>        an instance of an undeclared module before <Module>'s endmodule
    badport <Module>       an instance of KL_pp_prng with a port it does not have, same place
    fatal <Module>         an unconditional elaboration-time $fatal, same place
    drop-top <Name>        delete <Name> from syn/yosys/run.sh's tops array
    add-top <Name>         add <Name> to the tops array
    allv-syntax <Module>   make run.sh write a syntax fault into all.v inside <Module>
"""
import re
import sys
from pathlib import Path

tree, kind, arg = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
run = tree / "syn" / "yosys" / "run.sh"


def module_file(name: str) -> Path:
    for f in sorted((tree / "hdl").rglob("*.sv")):
        if re.search(rf"^\s*module\s+{name}\b", f.read_text(), re.M):
            return f
    raise SystemExit(f"no module {name}")


def insert_before_endmodule(name: str, text: str) -> None:
    f = module_file(name)
    src = f.read_text()
    m = re.search(rf"^\s*module\s+{name}\b", src, re.M)
    e = re.search(r"^\s*endmodule\b", src[m.end():], re.M)
    at = m.end() + e.start()
    f.write_text(src[:at] + "\n" + text + "\n" + src[at:])
    print(f"planted in {f.relative_to(tree)} before offset {at}")


if kind == "absent":
    insert_before_endmodule(arg, "  r448_absent_module u_r448_planted ();")
elif kind == "badport":
    insert_before_endmodule(arg, "  KL_pp_prng u_r448_badport (.r448_no_such_port_i(1'b0));")
elif kind == "fatal":
    insert_before_endmodule(arg, '  if (1) begin : g_r448_planted\n    $fatal(1, "r448 planted elaboration fault");\n  end')
elif kind == "drop-top":
    s = run.read_text()
    s2 = re.sub(rf"(tops=\([^)]*?)\b{arg}\b", r"\1", s, count=1, flags=re.S)
    assert s2 != s
    run.write_text(s2)
elif kind == "add-top":
    s = run.read_text()
    s2 = s.replace("protocol_processor_top)", f"protocol_processor_top {arg})", 1)
    assert s2 != s
    run.write_text(s2)
elif kind == "allv-syntax":
    s = run.read_text()
    hook = 'cd "$work"\n'
    inj = (hook + "python3 - <<'PY'\nimport re\np='all.v'\ns=open(p).read()\n"
           f"m=re.search(r'^module {arg}\\b', s, re.M)\ne=s.index('endmodule', m.end())\n"
           "s=s[:e]+'  this is not verilog ;\\n'+s[e:]\nopen(p,'w').write(s)\nPY\n")
    assert s.count(hook) == 1
    run.write_text(s.replace(hook, inj, 1))
else:
    raise SystemExit("unknown kind")
