#!/usr/bin/env python3
"""Disposable, real-tree gate probes and self-test mutation controls."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument('tree', type=Path)
    p.add_argument('receipts', type=Path)
    a = p.parse_args()
    root = a.tree.resolve()
    originals = {}
    results = []
    def change(rel, body):
        path = root / rel
        if rel not in originals:
            originals[rel] = path.read_bytes() if path.exists() else None
        path.parent.mkdir(parents=True, exist_ok=True)
        if body is None:
            path.unlink(missing_ok=True)
        else:
            path.write_bytes(body.encode() if isinstance(body, str) else body)
    def restore():
        for rel, data in originals.items():
            path = root / rel
            if data is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(data)
        originals.clear()
    def run(label, script, expected, required=(), selftest=False):
        args = [sys.executable, str(root/'scripts'/script)]
        args += ['--selftest'] if selftest else ['--root',str(root)]
        r = subprocess.run(args, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (a.receipts / (label+'.log')).write_text(r.stdout)
        (a.receipts / (label+'.rc')).write_text(str(r.returncode)+'\n')
        ok = r.returncode == expected and all(s in r.stdout for s in required)
        results.append(dict(probe=label, expected_rc=expected, actual_rc=r.returncode, required=list(required), expectation_met=ok))
        print(label, 'rc',r.returncode,'expected',expected,'PASS' if ok else 'SURVIVED_OR_UNEXPECTED')
        return r
    ids='check-ids.py'
    figures='check-figures.py'
    try:
        run('ids-clean',ids,0,['531 files, 91 distinct IDs used'])
        run('ids-selftest',ids,0,['25 cases, OK'],True)
        run('figures-clean',figures,0,['3 draw.io, 18 WaveDrom, 5 hand-authored, OK'])
        run('figures-selftest',figures,0,['17 cases, OK'],True)
        timing='docs/architecture/08_timing.md'
        params='docs/architecture/01_overview.md'
        for label, page, token, required in [
            ('row-braced-deadline',timing,'T-NVM-RS-DEADLINE',['docs/README.md:89: T-NVM-RS-DEADLINE has no F08.1 row']),
            ('row-braced-aggregate',timing,'T-NVM-RS-AGGREGATE',['docs/README.md:89: T-NVM-RS-AGGREGATE has no F08.1 row']),
            ('row-linebreak-and-optional',timing,'T-ADP-DELAY-START',[
                'tb/adp_engine/tb_adp_top.sv:10: T-ADP-DELAY-START has no F08.1 row',
                'tb/pp_top/pp_top_wrap.sv:15: T-ADP-DELAY-START has no F08.1 row',
                'hdl/adp/KL_adp_engine.sv:625: T-ADP-DELAY-START has no F08.1 row']),
            ('row-optional-base',timing,'T-ADP-DELAY',['tb/pp_top/pp_top_wrap.sv:15: T-ADP-DELAY has no F08.1 row']),
            ('row-minus-one-rx',params,'P-RX-SLOTS',['hdl/common/pp_pkg.sv:72: P-RX-SLOTS-1 has no F01.5 row']),
            ('row-minus-one-tx',params,'P-TX-STD-SLOTS',['hdl/common/pp_pkg.sv:73: P-TX-STD-SLOTS-1 has no F01.5 row']),
        ]:
            data=(root/page).read_text()
            lines=data.splitlines(keepends=True)
            selected=[x for x in lines if x.startswith('| '+token+' ') or x.startswith('| '+token+' |')]
            assert len(selected)==1,(label,selected)
            change(page,data.replace(selected[0],''))
            run(label,ids,1,required)
            restore()
        cases=[
          ('braced-hyphenated','T-NVM-{RS-DEADLINE, RS-TYPO}',1,'T-NVM-RS-TYPO'),
          ('braced-simple','T-MRP-{JOIN, NOPE}',1,'T-MRP-NOPE'),
          ('linebreak','T-ADP-\n// DELAY-MISSING',1,'T-ADP-DELAY-MISSING'),
          ('optional-inline','T-ADP-DELAY(-MISSING)',1,'T-ADP-DELAY-MISSING'),
          ('optional-linebreak','T-ADP-DELAY(-\n// MISSING)',1,'T-ADP-DELAY-MISSING'),
          ('minus-one-missing','P-R472-MISSING-1',1,'P-R472-MISSING-1'),
          ('minus-other','P-RX-SLOTS-2',1,'P-RX-SLOTS-2'),
          ('prose-suffix','P-TX-shaped',1,'P-TX has no'),
          ('family-missing','T-R472-MISSING-*',1,'T-R472-MISSING-*'),
          ('sibling-missing','T-BUDGET-AECP-TYP / -MISSING',1,'T-BUDGET-AECP-MISSING'),
          ('combined-linebreak-optional','T-ADP-\n// DELAY(-MISSING)',1,'T-ADP-DELAY-MISSING'),
        ]
        for label, token, rc, required in cases:
            change('tb/r472-probe.txt',token+'\n')
            run('use-'+label,ids,rc,[required])
            restore()
        svg='docs/diagrams/20-rtl-dataflow.svg'
        data=(root/svg).read_text()
        for tag in ['image','feImage','foreignObject']:
            change(svg,data.replace('</svg>',f'<{tag}/></svg>'))
            run('figure-'+tag,figures,1,[f'carries <{tag}>'])
            restore()
        for label,source,replacement,required in [
          ('root-namespace','http://www.w3.org/2000/svg','urn:r472','not an SVG-namespace'),
          ('no-viewbox','viewBox=','unusedBox=','no viewBox'),
        ]:
            change(svg,data.replace(source,replacement))
            run('figure-'+label,figures,1,[required]); restore()
        for label,rel,body,required in [
          ('bad-xml',svg,'<svg','not well-formed'),
          ('png','docs/diagrams/r472.png',b'\x89PNG\0','not a figure format'),
          ('nested','docs/diagrams/nested/r472.svg',data,'not a figure format'),
          ('missing-inventory','docs/diagrams/README.md',None,'inventory unreadable'),
          ('empty-inventory','docs/diagrams/README.md','## Inventory (hand-authored SVG)\n','lists no SVG'),
        ]:
            change(rel,body); run('figure-'+label,figures,1,[required]); restore()
        code=(root/'scripts'/ids).read_text()
        mutations=[
          ('skip-brace-check','for member in members:', 'for member in []:'),
          ('skip-linebreak','broken = LINE_BREAK.match(text, end)','broken = None'),
          ('skip-sibling','sibling = SIBLING.match(text, end)','sibling = None'),
          ('any-minus-one','return token in rows or (token.endswith("-1") and token[:-2] in rows)',
           'return token in rows or token.endswith("-1")'),
          ('skip-optional-linebreak','if optional:\n                yield line, f"{token}-{optional.group(1)}", "id"',
           'if optional:\n                if "\\n" not in optional.group(0):\n                    yield line, f"{token}-{optional.group(1)}", "id"'),
        ]
        for label,old,new in mutations:
            assert old in code,label
            change('scripts/'+ids,code.replace(old,new))
            run('mutant-'+label,ids,1,selftest=True)
            if label=='any-minus-one':
                change('tb/r472-probe.txt','P-R472-MISSING-1\n')
                run('mutant-any-minus-one-real-tree',ids,1,['P-R472-MISSING-1'])
            if label=='skip-optional-linebreak':
                change('tb/r472-probe.txt','T-ADP-DELAY(-\n// MISSING)\n')
                run('mutant-skip-optional-linebreak-real-tree',ids,1,['T-ADP-DELAY-MISSING'])
            restore()
        figurecode=(root/'scripts'/figures).read_text()
        fm=[
          ('foreignObject','("image", "feImage", "foreignObject")','("image", "feImage")'),
          ('namespace','if svg.tag != f"{SVG_NS}svg":','if svg.tag.split("}")[-1] != "svg":'),
          ('root','if svg.tag != f"{SVG_NS}svg":','if False:'),
          ('empty-inventory','if not names:','if False:'),
        ]
        for label,old,new in fm:
            assert old in figurecode,label
            change('scripts/'+figures,figurecode.replace(old,new))
            run('figure-mutant-'+label,figures,1,selftest=True)
            restore()
    finally:
        restore()
        (a.receipts/'gate-probes.json').write_text(json.dumps(results,indent=2)+'\n')
    print('SUMMARY',len(results),'probes;',sum(not x['expectation_met'] for x in results),'unexpected survivors')

if __name__ == '__main__':
    main()
