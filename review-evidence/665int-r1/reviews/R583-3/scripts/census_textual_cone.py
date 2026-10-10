#!/usr/bin/env python3
"""census_textual_cone.py - a fail-closed, purely textual cone for every
status and processor read the publication census accepts.

Usage: python3 -I census_textual_cone.py <tree>

For each (wire, consumer) row the census classifies as `status` or
`processor`, follow the consumer through EVERY statement of
milan_datapath.sv (comments and strings blanked by the census's own
strip_comments) that names it anywhere, whatever the form:
  - an instance statement: every port of a CSR instance is `csr`, every port of
    the wrapper is `processor`, any other instance is `wire`;
  - any other statement: every signal it or its enclosing always block
    assigns becomes a cone node; a module output is `wire`;
  - a statement that names a cone node but assigns nothing and is no
    instance is reported UNPARSED (counted as reaching the wire).
The result is compared with the census's own classification. Exit 0 when
every status read reaches CSR only and every processor read the wrapper only.
"""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/mailbox"))
import publication_census as pc  # noqa: E402


def main() -> int:
    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    net = pc.netlist(src.datapath)
    code, stmts = net.code, net.stmts
    blocks = pc.always_blocks(code, stmts)
    kinds = {i: k for i, k in net.instances.items()}

    def targets_of(s, e):
        """Signals the statement (or its always block) assigns, or None for an instance."""
        text = code[s:e]
        op = pc.assignment(text)
        blk = next((b for b in blocks if b[0] <= s < b[1]), None)
        tg = set()
        if op is not None:
            tg |= set(pc.lvalues(text[:op[0]])[0])
        if blk:
            for s2, e2 in stmts:
                if blk[0] <= s2 < blk[1] or (s2 < blk[0] < e2):
                    t2 = code[s2:e2]
                    o2 = pc.assignment(t2)
                    if o2:
                        tg |= set(pc.lvalues(t2[:o2[0]])[0])
        return tg

    def ends(start):
        seen, stack, out = set(), [start], set()
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            if node in net.outputs:
                out.add(("wire", node))
            pat = re.compile(r"(?<![A-Za-z0-9_$.])" + re.escape(node) + r"(?![A-Za-z0-9_$])")
            for s, e in stmts:
                text = code[s:e]
                if not pat.search(text):
                    continue
                # an instance naming the node: classify by instance kind
                hit_inst = None
                for inst, (off, body) in net.bodies.items():
                    if off <= s + len(text) and s <= off + len(body) and pat.search(body) and s <= off < e:
                        hit_inst = inst
                if hit_inst:
                    k = kinds[hit_inst]
                    out.add(("csr" if k == {pc.CSR} else "processor" if k == {pc.WRAPPER} else "wire",
                             hit_inst))
                    continue
                op = pc.assignment(text)
                if op is not None:
                    lv, lstart = pc.lvalues(text[:op[0]])
                    # occurrences other than the driven name itself at the lvalue
                    occ = [m.start() for m in pat.finditer(text)]
                    lv_at = {lstart + text[:op[0]][lstart:].find(node)} if node in lv else set()
                    if all(o in lv_at for o in occ):
                        continue              # this statement drives the node: not a read of it
                tg = targets_of(s, e)
                tg.discard(node)
                if not tg:
                    first = pat.search(text)
                    # its own declaration without initialiser is not a read
                    if pc.DECL.match(text, pc.lead_of(text)) and op is None:
                        continue
                    out.add(("UNPARSED", f"line {net.line(s + first.start())}: " + " ".join(
                        text[max(0, first.start() - 60):first.end() + 40].split())))
                    continue
                stack.extend(tg)
        return out

    bad = 0
    for (wire, consumer), row in sorted(pc.CENSUS.items()):
        if row.kind not in ("status", "processor"):
            continue
        if "." in consumer:
            continue
        got = ends(consumer)
        kinds_got = {k for k, _ in got}
        want = {"csr"} if row.kind == "status" else {"processor"}
        ok = kinds_got <= want and kinds_got
        bad += not ok
        print(f"[{'ok' if ok else 'DIFF'}] {row.kind:9} {wire} -> {consumer}: reaches {sorted(kinds_got)}"
              + ("" if ok else f" {sorted(got)[:4]}"))
    print(f"textual cone: {bad} status/processor read(s) whose fail-closed cone leaves their class")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
