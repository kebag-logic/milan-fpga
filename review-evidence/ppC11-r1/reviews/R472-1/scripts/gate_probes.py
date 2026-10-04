#!/usr/bin/env python3
"""Fault plants against `make ids` / `make figures` and mutants of both gate scripts.

usage: gate_probes.py <disposable clone at the head under review>
Each plant edits the disposable clone, runs the gate, records rc and the FAIL lines,
then restores the clone (git checkout + clean). Each mutant is a copy of the gate
script with one behaviour removed; its own --selftest must fail (rc 1) to be killed.
"""
import re
import subprocess
import sys
from pathlib import Path

C = Path(sys.argv[1]).resolve()
HEAD = "91cef52b3c56cc69f66966b004782a69d2940a46"


def sh(*cmd, **kw):
    return subprocess.run(cmd, cwd=C, capture_output=True, text=True, **kw)


def restore():
    sh("git", "reset", "-q", "--hard", HEAD)
    sh("git", "clean", "-fdxq")
    assert sh("git", "status", "--porcelain", "--ignored").stdout == "", "clone not clean"


def append(rel, text):
    p = C / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(text)


def replace(rel, old, new, count=1):
    p = C / rel
    body = p.read_text(encoding="utf-8")
    assert old in body, f"{rel}: anchor text not found: {old!r}"
    p.write_text(body.replace(old, new, count), encoding="utf-8")


def base_files(*rels):
    for rel in rels:
        sh("git", "checkout", "-q", "c050d97153dd0480ae741102c1647eeda9b7f273", "--", rel)


F015 = "docs/architecture/01_overview.md"
PLANTS = [
    # (id, gate script, description, action, expected rc)
    ("I1", "ids", "stray P-ID in an architecture page",
     lambda: append("docs/architecture/03_packet_engine.md", "\nP-R472-STRAY\n"), 1),
    ("I2", "ids", "stray T-ID in an RTL comment",
     lambda: replace("hdl/packet_engine/KL_pp_tx_slots.sv", "F01.5\n//                rows.",
                     "F01.5\n//                rows T-R472-STRAY."), 1),
    ("I3", "ids", "stray P-ID in a new untracked tb/ file",
     lambda: append("tb/r472_probe/NOTE.txt", "P-R472-NEW\n"), 1),
    ("I4", "ids", "stray in an ignored file (tb/x.log): out of scope by design",
     lambda: append("tb/r472_probe.log", "P-R472-IGNORED\n"), 0),
    ("I5", "ids", "braced list whose member has a hyphen: T-NVM-{RS-DEADLINE, RS-TYPO}",
     lambda: append("docs/architecture/08_timing.md", "\nT-NVM-{RS-DEADLINE, RS-TYPO}\n"), 1),
    ("I6", "ids", "braced list, hyphen-free members: T-MRP-{JOIN, TYPO}",
     lambda: append("docs/architecture/08_timing.md", "\nT-MRP-{JOIN, TYPO}\n"), 1),
    ("I7", "ids", "the old stray P-TX written as a hyphenated adjective: P-TX-shaped",
     lambda: append("tb/tx_slots/README.md", "\nthe P-TX-shaped pool\n"), 0),
    ("I8", "ids", "F01.5 row P-MAAP-RSP-MS deleted",
     lambda: replace(F015, "| P-MAAP-RSP-MS |", "| X-MAAP-RSP-MS |"), 1),
    ("I9", "ids", "a P-ID used only as a T- name (T-CLK-HZ)",
     lambda: append("docs/architecture/02_interfaces.md", "\nT-CLK-HZ\n"), 1),
    ("I10", "ids", "stray in a hand-authored SVG",
     lambda: replace("docs/diagrams/24-adp-acmp-states.svg", "</svg>", "<!-- P-R472-SVG --></svg>"), 1),
    ("I11", "ids", "stray in the history page",
     lambda: append("docs/history/02-class-a-word-stream.md", "\nT-R472-HIST\n"), 1),
    ("I12", "ids", "duplicate F01.5 row",
     lambda: replace(F015, "| P-CLK-HZ |", "| P-CLK-HZ | x | x | x |\n| P-CLK-HZ |"), 1),
    ("I13", "ids", "the five fixed files at base content (the real strays)",
     lambda: base_files("docs/architecture/01_overview.md", "docs/architecture/02_interfaces.md",
                        "hdl/packet_engine/KL_pp_tx_slots.sv", "tb/tx_slots/README.md",
                        "tb/tx_slots/sim_main.cpp"), 1),
    ("I14", "ids", "F08.1 anchor removed (table unfindable)",
     lambda: replace("docs/architecture/08_timing.md", '<a id="fig-08-constants"></a>', ""), 1),
    ("I15", "ids", "F01.5 table present but with no P- row (first column emptied)",
     lambda: (C / F015).write_text(re.sub(r"(?m)^\| P-[A-Z0-9-]+", "| x", (C / F015).read_text(encoding="utf-8")), encoding="utf-8"), 1),
    ("I16", "ids", "a P-ID with a non-numeric tail after a real stem: P-RX-SLOTS-X",
     lambda: append("tb/tx_slots/README.md", "\nP-RX-SLOTS-X\n"), 1),
    ("G1", "figures", "a PNG restored from base",
     lambda: base_files("docs/diagrams/21-integration-faces.png"), 1),
    ("G2", "figures", "<foreignObject> inside a hand-authored SVG",
     lambda: replace("docs/diagrams/22-aecp-descriptor-fetch.svg", "</svg>",
                     "<foreignObject width='1' height='1'/></svg>"), 1),
    ("G3", "figures", "hand-authored SVG root without the SVG namespace",
     lambda: replace("docs/diagrams/23-bringup-decision.svg", 'xmlns="http://www.w3.org/2000/svg"', ""), 1),
    ("G4", "figures", "an extra file in src/ (an SVG beside the .drawio)",
     lambda: append("docs/diagrams/src/r472.svg", "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1 1'/>"), 1),
    ("G5", "figures", "a nested directory under docs/diagrams",
     lambda: append("docs/diagrams/wavedrom/sub/x.svg", "<svg/>"), 1),
    ("G6", "figures", "the hand-authored inventory section heading renamed",
     lambda: replace("docs/diagrams/README.md", "## Inventory (hand-authored SVG)", "## Inventory (hand SVG)"), 1),
    ("G7", "figures", "a draw.io export deleted",
     lambda: (C / "docs/diagrams/03-shared-datapath.svg").unlink(), 1),
    ("G8", "figures", "a hand-authored SVG whose only link is removed from every page",
     lambda: [replace(str(p.relative_to(C)), "23-bringup-decision.svg", "23-bringup-decision.svgX", 99)
              for p in C.rglob("*.md") if "23-bringup-decision.svg" in p.read_text(encoding="utf-8")
              and ".git" not in p.parts and p.relative_to(C).as_posix() != "docs/diagrams/README.md"], 1),
    ("G9", "figures", "an untracked stray file in docs/diagrams",
     lambda: append("docs/diagrams/notes.txt", "x\n"), 1),
]

ID_MUTANTS = [
    ("MI1", "resolves() always true", "def resolves(token: str, kind: str, rows: set) -> bool:\n",
     "def resolves(token: str, kind: str, rows: set) -> bool:\n    return True\n"),
    ("MI2", "family accepted without a row", "        return token in rows or any(r.startswith(token + \"-\") for r in rows)",
     "        return True"),
    ("MI3", "braced members not expanded", "        braces = BRACES.match(text, end)", "        braces = None"),
    ("MI4", "untracked files not scanned", '"--cached", "--others",', '"--cached",'),
    ("MI5", "minus-n rule accepts any tail", "    return tail.isdigit() and stem in rows", "    return stem in rows"),
    ("MI6", "sibling shorthand not expanded", "            names += [f\"{stem}-{tail}\" for tail in SIBLING.findall(cell)]", "            pass"),
    ("MI7", "lookbehind dropped", 'ID = re.compile(r"(?<![A-Za-z0-9_-])(', 'ID = re.compile(r"('),
    ("MI8", "empty master table accepted", '        problems.append(f"{what}: no {prefix} rows parsed")', "        pass"),
    ("MI9", "duplicate row accepted", '            problems.append(f"{what}: {name} has two rows")', "            pass"),
    ("MI10", "check() always rc 0", "    return 1 if problems else 0\n\n\nSELFTEST_PARAMS", "    return 0\n\n\nSELFTEST_PARAMS"),
    ("MI11", "registry words not skipped in uses", "        if token in REGISTRY_WORDS:\n            continue\n        braces", "        braces"),
]
FIG_MUTANTS = [
    ("MF1", "svg_problems() never reports", "    out = []\n    if svg.tag", "    return []\n    out = []\n    if svg.tag"),
    ("MF2", "unlinked figure accepted", "            if rel not in linked:", "            if False:"),
    ("MF3", "unknown format accepted", '            problems.append(f"{rel}: not a figure format docs/README.md section 3 lists")', "            pass"),
    ("MF4", "orphan WaveDrom accepted", "            if name[9:-4] not in anchors:", "            if False:"),
    ("MF5", "draw.io without export accepted", "            if export not in names:", "            if False:"),
    ("MF6", "listed-but-missing accepted", "    for name in sorted(set(hand) - names):", "    for name in []:"),
    ("MF7", "unlisted SVG accepted", "            if name not in hand:", "            if False:"),
    ("MF8", "foreignObject not checked", 'for tag in ("image", "foreignObject"):', 'for tag in ("image",):'),
    ("MF9", "non-SVG root accepted", '    if svg.tag != f"{SVG_NS}svg":', "    if False:"),
    ("MF10", "empty inventory accepted", "    if not names:\n        raise ValueError", "    if False:\n        raise ValueError"),
    ("MF11", "viewBox not checked", '    if "viewBox" not in svg.attrib:', "    if False:"),
]


def run_gate(gate):
    proc = sh(sys.executable, f"scripts/check-{gate}.py")
    fails = [l for l in proc.stdout.splitlines() if " FAIL" in l]
    summary = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr.strip()[-200:]
    return proc.returncode, fails, summary


def main():
    restore()
    assert sh("git", "rev-parse", "HEAD").stdout.strip() == HEAD
    bad = 0
    print("== plants (expected rc: 1 = must be caught, 0 = passes by design)")
    for pid, gate, what, act, want in PLANTS:
        act()
        rc, fails, summary = run_gate(gate)
        verdict = "AS-EXPECTED" if rc == want else "UNEXPECTED"
        if rc != want:
            bad += 1
        print(f"{pid} [{gate}] {what}: rc {rc} (want {want}) {verdict}; {summary}")
        for l in fails[:4]:
            print(f"    {l}")
        if len(fails) > 4:
            print(f"    ... {len(fails)} FAIL lines")
        restore()
    for gate, mutants in (("ids", ID_MUTANTS), ("figures", FIG_MUTANTS)):
        print(f"== mutants of scripts/check-{gate}.py (killed = its --selftest rc 1)")
        src = (C / f"scripts/check-{gate}.py").read_text(encoding="utf-8")
        for mid, what, old, new in mutants:
            assert old in src, f"{mid}: anchor not found"
            mpath = C / f"scripts/check-{gate}-{mid}.py"
            mpath.write_text(src.replace(old, new, 1), encoding="utf-8")
            st = sh(sys.executable, str(mpath), "--selftest")
            tree = sh(sys.executable, str(mpath))
            mpath.unlink()
            state = "KILLED" if st.returncode == 1 else "SURVIVED"
            print(f"{mid} {what}: selftest rc {st.returncode} {state}; head tree rc {tree.returncode}")
        restore()
    restore()
    print(f"plants not as expected: {bad}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
