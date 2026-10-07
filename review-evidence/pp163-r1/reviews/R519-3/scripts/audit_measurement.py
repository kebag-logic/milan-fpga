#!/usr/bin/env python3
"""Audit the published record; refuse an aggregate when any component is absent.
Run after fetch_measurement.py and recover_public_inputs.py:
  python3 scripts/audit_measurement.py --repo /path/to/exact/processor
This does not invoke synthesis, modify source, or substitute missing input bytes.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
M=P/'receipts/public-measurement/measurement-m3final'
PREFIX='$VALIDATION_STORAGE/pp163-a553/parent/'
READS=re.compile(r'^(?:read_verilog(?: -v)?|read_xdc|source) \{?([^{}\s]+)\}?[ \t]*$',re.M)
GEN=re.compile(r' -generic \{([^}]*)\}')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args()
    head=subprocess.check_output(['git','-C',str(a.repo),'rev-parse','HEAD'],text=True).strip()
    assert head=='c4539ff107a6a4c7d2e4a4844182b00a2bf33c82'
    script=(M/'ooc-m3final/baseline_ooc.tcl').read_text()
    refs=READS.findall(script); rows=[]; absent=[]; h=hashlib.sha256(); prefix_open=True; path_map={}
    for n,ref in enumerate(refs):
        if ref.startswith(PREFIX+'protocol-processor/'):
            origin='processor exact head';path=a.repo/ref[len(PREFIX+'protocol-processor/'):]
        elif ref.startswith(PREFIX):
            origin='immutable public parent or dependency';path=P/'scratch/public-inputs'/ref[len(PREFIX):]
        elif ref=='clock.xdc':
            origin='published constraint';path=M/'ooc-m3final/clock.xdc'
        else:
            origin='unpublished generated or external source';path=None
        row={'order':n,'recipe_reference':ref,'origin':origin,'available':path is not None and path.is_file()}
        if row['available']:
            data=path.read_bytes();row['bytes']=len(data);row['sha256']=sha(data);path_map[ref]=str(path.resolve())
            if origin=='processor exact head':
                rel=str(path.relative_to(a.repo))
                blob=subprocess.check_output(['git','-C',str(a.repo),'rev-parse',f'{head}:{rel}'],text=True).strip()
                row['git_blob']=blob
                assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
            if prefix_open:h.update(Path(ref).name.encode()+b'\0'+hashlib.sha256(data).digest())
        else:
            absent.append(ref);prefix_open=False
        rows.append(row)
    params=json.loads((M/'ooc-m3final/baseline_parameters.json').read_text())
    generics=dict(x.split('=',1) for x in GEN.findall(script))
    assert len(generics)==len(params)==21
    assert all(generics[k]==(str(v) if isinstance(v,int) else '"'+v+'"') for k,v in params.items())
    ch=(M/'ooc-m3final/baseline_chparam.txt').read_text().split()
    assert {k:int(v) for k,v in (x.split('=',1) for x in ch)}=={k:v for k,v in params.items() if isinstance(v,int)}
    assert params['CLK_HZ_P']==50000000 and params['N_STREAM_IN_P']==params['N_STREAM_OUT_P']==2
    assert params['TIM_DIV_US_P']==50 and params['TIM_DIV_MS_P']==1000
    assert (M/'ooc-m3final/clock.xdc').read_text().strip()=='create_clock -period 20.000 -name clk [get_ports clk_i]'
    integrated=(M/'rtl-m3final/baseline_integrated.tcl').read_text()
    assert [x for x in refs if x!='clock.xdc']==[x for x in READS.findall(integrated) if not x.endswith('.xdc')]
    conc=json.loads((M/'ooc-m3final/baseline_concurrency.json').read_text())
    assert conc['general.maxThreads']==2 and 'set_param general.maxThreads 2\n' in script
    record=json.loads((M/'record-m3final.stdout').read_text())
    assert 'set_param general.maxThreads 2' in record['identity']['flow']
    assert record['identity']['standalone_clock_ns']==['20.000']
    assert record['kind']=='ooc' and record['identity']['state']=='Synthesized'
    imgs=json.loads((M/'ooc-m3final/baseline_images.json').read_text())
    audit=json.loads((M/'image-audit-m3final.json').read_text())
    assert not audit['diag'] and len(imgs)==len(audit['images'])==6
    image_results=[]
    for img,observed in zip(imgs,audit['images']):
        assert all(img[k]==observed[k] for k in ['path','bytes','sha256'])
        name=Path(img['path']).name;out=P/'scratch'/name
        data=None;reason='manifest and publisher audit agree; source bytes not independently recovered'
        if name in ('ltn_rom.hex','ucode.hex'):
            generator=a.repo/('hdl/acmp/rom/gen_ltn_rom.py' if name=='ltn_rom.hex' else 'hdl/aecp/ucode/gen_ucode.py')
            r=subprocess.run(['python3',str(generator),'-o',str(out)],capture_output=True,text=True)
            (P/'receipts'/f'{name}-generation.log').write_text(r.stdout+r.stderr)
            assert r.returncode==0;data=out.read_bytes();reason='regenerated from exact processor head'
        elif name=='alinx_ax7101_sram.init':data=b'';reason='published empty SRAM shape independently hashed'
        if data is not None:assert sha(data)==img['sha256'] and len(data)==img['bytes']
        image_results.append({'name':name,'independently_hashed':data is not None,'sha256':img['sha256'],'evidence':reason})
    summary=json.loads((P/'receipts/public-measurement/evidence/measurement-m3final.json').read_text())
    cone=summary['cone'];hist={int(k):v for k,v in cone['histogram'].items()}
    assert record['figures']['WNS_ns']==summary['timing']['setup']['worst_slack_ns']==3.337
    assert record['figures']['WHS_ns']==summary['timing']['hold']['worst_slack_ns']==0.159
    assert sum(hist.values())==cone['pairs']==17990
    assert max(hist)==cone['max_levels']==16 and sum(v for k,v in hist.items() if k>20)==cone['above_20']==0
    transcript=(M/'cone-m3final.stdout').read_text()
    assert 'arbiter cells 187 endpoint pins 561 startpoints 328' in transcript and 'cone paths written: 17990' in transcript
    assert '-nworst 1 -max_paths 1000' in transcript
    assert 'paths written: 7034' in (M/'paths-m3final.stdout').read_text()
    assert 'RESULT: PASS' in (M/'gate-m3final.stdout').read_text()
    rcs={f.name:int(f.read_text()) for f in sorted(M.glob('*.rc'))};assert rcs and set(rcs.values())=={0}
    directories={}
    for group in re.findall(r' -include_dirs \{([^}]*)\}',script):
        for ref in group.split():
            assert ref.startswith(PREFIX)
            folder=P/'scratch/public-inputs'/ref[len(PREFIX):]
            folder.mkdir(parents=True,exist_ok=True)
            directories[ref]=str(folder.resolve())
    (P/'scratch/input-map.json').write_text(json.dumps({'files':path_map,'directories':directories,'note':'Include directories reconstructed from the pinned public tree only; measured extra generated headers are not inventoried.'},indent=2)+'\n')
    result={'head':head,'recorded_inputs_sha256':record['inputs_sha256'],
      'aggregate_recomputed':False,'aggregate_matches':None,
      'result':'REFUSED: complete inputs unavailable; no substitute aggregate claimed',
      'read_count':len(rows),'processor_sources_hashed':sum(r['origin']=='processor exact head' for r in rows),
      'available_reads':sum(r['available'] for r in rows),'unavailable_reads':absent,
      'contiguous_source_prefix_sha256_not_full_digest':h.hexdigest(),
      'sources':rows,'parameters':params,'generic_parameter_and_chparam_agreement':True,
      'source_order_agrees_between_ooc_and_integrated':True,'clock_ns':20.0,'concurrency':2,
      'published_concurrency_recipe_hashes':conc,
      'published_recipe_sha256':sha(script.encode()),
      'recipe_hash_limit':'Published paths are normalized; original raw recipe hashes cannot be reproduced by hashing this normalized text.',
      'images':image_results,'include_directory_limit':'Pinned tracked headers recovered; the measured generated directory inventories are not published.',
      'published_figures_reconciled':{'WNS_ns':3.337,'max_levels':16,'above_20':0,'pairs':17990},
      'measurement_return_codes':rcs,
      'cone_limit':'Figures reconcile with final summary and executed transcript; full pair table and checkpoint absent, so no fresh path derivation claimed.'}
    (P/'receipts/measurement-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sources','parameters','published_concurrency_recipe_hashes','images')},indent=2))
    return 2 if absent else 0
if __name__=='__main__':raise SystemExit(main())
