#!/usr/bin/env python3
"""Recompute the source gate input digest from a relocated published recipe.
--map is JSON with `files` (recipe reference -> local file), `directories`
(include reference -> local directory), and optionally `original_roots`
(the original generated, parent, and measurement directory strings in that order).
Only the designated input files and immediate include-directory headers are read.
Missing input bytes cause exit 2; a complete digest mismatch causes exit 1.
"""
import argparse,hashlib,json,re
from pathlib import Path
READS=re.compile(r'^(?:read_verilog(?: -v)?|read_xdc|source) \{?([^{}\s]+)\}?[ \t]*$',re.M)
INCLUDES=re.compile(r' -include_dirs \{([^}]*)\}')
GENERICS=re.compile(r' -generic \{([^}]*)\}')
def main():
    a=argparse.ArgumentParser();a.add_argument('--measurement',type=Path,required=True);a.add_argument('--map',type=Path,required=True);a.add_argument('--record',type=Path,required=True);o=a.parse_args()
    m=json.loads(o.map.read_text()); script=(o.measurement/'baseline_ooc.tcl').read_text();refs=READS.findall(script)
    generated=[str(Path(x).parent) for x in refs if Path(x).name=='alinx_ax7101.v']
    parent=[str(Path(x).parents[2]) for x in refs if Path(x).name=='KL_pp_shadow.sv']
    assert len(generated)==len(parent)==1
    roots=m.get('original_roots',[generated[0],parent[0],str(o.measurement)])
    assert len(roots)==3
    files=[];missing=[]
    for ref in refs:
        path=Path(m['files'][ref]) if ref in m.get('files',{}) else o.measurement/ref
        if not path.is_file():missing.append({'kind':'source','reference':ref});continue
        files.append((ref,path))
    for group in INCLUDES.findall(script):
        for ref in group.split():
            folder=Path(m['directories'][ref]) if ref in m.get('directories',{}) else Path(ref)
            if not folder.is_dir():missing.append({'kind':'include directory','reference':ref});continue
            for path in sorted(folder.iterdir()):
                if path.suffix in ('.svh','.vh'):files.append((ref+'/'+path.name,path))
    if missing:
        print(json.dumps({'result':'REFUSED','missing':missing,'expected_inputs_sha256':json.loads(o.record.read_text())['inputs_sha256']},indent=2));return 2
    h=hashlib.sha256();components=[]
    for ref,path in files:
        data=path.read_bytes()
        if ref.startswith(generated[0]+'/'):
            text=re.sub(r'//[^\n]*','',data.decode(errors='replace'))
            for n,root in enumerate(roots):text=text.replace(root,f'$ROOT{n}')
            data=text.encode()
        digest=hashlib.sha256(data).digest();h.update(Path(ref).name.encode()+b'\0'+digest)
        components.append({'reference':ref,'digest_component':digest.hex()})
    for generic in GENERICS.findall(script):h.update(re.sub(r'"[^"]*/([^/"]+)"',r'"\1"',generic).encode()+b'\0')
    images=json.loads((o.measurement/'baseline_images.json').read_text())
    for im in sorted(images,key=lambda row:Path(row['path']).name):h.update(f"{Path(im['path']).name}\0{im['sha256']}\0".encode())
    actual=h.hexdigest();expected=json.loads(o.record.read_text())['inputs_sha256']
    print(json.dumps({'result':'MATCH' if actual==expected else 'MISMATCH','actual':actual,'expected':expected,'components':components},indent=2));return 0 if actual==expected else 1
if __name__=='__main__':raise SystemExit(main())
