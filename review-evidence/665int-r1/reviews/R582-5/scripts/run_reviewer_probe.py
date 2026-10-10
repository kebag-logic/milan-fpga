#!/usr/bin/env python3
"""run_reviewer_probe.py - run an earlier reviewer's census probe against the head, optionally with its probe modules defined.

The earlier rounds' probes (public review evidence of #665) plant copies of the
datapath that instantiate KL_probe_buf / KL_probe_sink / KL_probe_* without
defining them. Run as they are, the elaborating census refuses each such copy
at `hierarchy -check` (an undefined module), which says nothing about the
dataflow. With --define-modules this runner wraps the census's findings() so
that every planted datapath that instantiates an undefined KL_probe_* module
gets that module defined after the datapath's closing `default_nettype wire`
(the same place the census's own plants put theirs): every port the copy
connects by name, and a, y_o for positional use, each 512 bits wide so no
connection is truncated, the outputs driven from the OR of all inputs. The
probe script itself is not modified; it is run with runpy.

Usage: run_reviewer_probe.py <checkout> <probe.py> [--define-modules]
"""
import re
import runpy
import sys
from dataclasses import replace
from pathlib import Path

TAIL = "\n`default_nettype wire\n"
INST = re.compile(r"\b(KL_probe_\w+)\s+(\w+)\s*\((.*?)\)\s*;", re.S)


def modules(text: str) -> str:
    out = []
    by_mod: dict[str, set[str]] = {}
    for mod, _, body in INST.findall(text):
        if re.search(rf"^\s*module\s+{mod}\b", text, re.M):
            continue
        ports = by_mod.setdefault(mod, set())
        ports |= set(re.findall(r"\.(\w+)\s*(?=[(,)]|$)", body))
        if not re.search(r"\.\w", body):
            ports |= {"a", "y_o"}
    for mod, ports in sorted(by_mod.items()):
        ports |= {"y_o"}
        ins = sorted(p for p in ports if p != "y_o")
        order = (["a", "y_o"] if "a" in ins else ["y_o"]) + [p for p in ins if p != "a"]
        decl = ", ".join(f"{'output' if p == 'y_o' else 'input'} logic [511:0] {p}" for p in order)
        body = f"  assign y_o = {{511'd0, |{{{', '.join(ins)}}}}};\n" if ins else "  assign y_o = '0;\n"
        out.append(f"module {mod} ({decl});\n{body}endmodule\n")
    return "".join(out)


def main() -> int:
    tree, probe = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    define = "--define-modules" in sys.argv[3:]
    sys.path.insert(0, str(tree / "sw/mailbox"))
    import publication_census as pc
    if define:
        real = pc.findings

        def findings(src, table, known):
            extra = modules(src.datapath)
            if extra:
                assert src.datapath.count(TAIL) == 1
                src = replace(src, datapath=src.datapath.replace(TAIL, TAIL + extra, 1))
            return real(src, table, known)

        pc.findings = findings
    sys.argv = [str(probe), str(tree)]
    runpy.run_path(str(probe), run_name="__main__")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as exc:
        raise
