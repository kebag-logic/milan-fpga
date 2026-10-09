#!/usr/bin/env python3
"""Focus both synthesis flows on the datapath at the five shipping shapes.

Source defaults are changed only in disposable inputs, following ooc.sh's
required recipe for interface-bearing tops. The builder emits the shape header
and CLI options; parameter translation follows add_milan_datapath.
"""
import concurrent.futures, json, os, pathlib, shlex, subprocess, sys, time
root=pathlib.Path.cwd()
packet=pathlib.Path(__file__).resolve().parents[1]
work=packet/'scratch/shipping-flows'; work.mkdir(exist_ok=True)
sys.path[:0]=[str(root/'sw/builder'),str(root/'syn/resmap')]
import endstation_builder as eb
import yosys_sweep as sweep
names=('arty_current','arty_4x4','arty_8ch','ax7101_8x8','ax7101_1x1_tdm8')

def one(name):
    directory=work/name; directory.mkdir(exist_ok=True)
    art=eb._derive_artifacts(str(root/'configs'/('endstation_'+name+'.yaml')))
    argv=art.argv
    def opt(key, default):
        return argv[argv.index(key)+1] if key in argv else default
    slots=int(str(opt('--audio-interface','tdm0')).removeprefix('tdm'))
    params=dict(MILAN_CLK_FREQ_HZ=int(float(opt('--milan-clk-freq','50e6'))),
                N_STREAMS=int(opt('--num-streams','1')), AUDIO_IF_SLOTS_P=slots,
                TALKER_WIRE_CHANS_P=int(opt('--talker-wire-chans','2')),
                AUDIO_IF_MASTER_P=int('--audio-interface-master' in argv),
                AUDIO_IF_RENDER_SLOTS_P=int(opt('--audio-interface-render','0')),
                GPTP_PLANE_EN_P=int('--fabric-gptp' in argv),
                LOOPBACK_P=int('--loopback-lane' in argv),
                GPTP_INGRESS_LAT_NS_P=int(opt('--gptp-ingress-lat-ns','0')),
                GPTP_EGRESS_LAT_NS_P=int(opt('--gptp-egress-lat-ns','0')))
    if params['AUDIO_IF_MASTER_P']:
        params['AUDIO_IF_CLK_HZ_P']=2*slots*32*48000
    for option,param in (('--no-i2s-playback','I2SPB_P'),('--no-render-lpf','LPF_P'),
                         ('--no-latency-taps','LTAP_P'),('--no-datapath-probes','DPROBES_P')):
        if option in argv: params[param]=0
    gen=directory/'shape/gen'; gen.mkdir(parents=True,exist_ok=True)
    (gen/'adp_shape_defaults.svh').write_text(art.adp_svh)
    record=sweep.record_of('milan_datapath')
    assert 'configs/generated/' in record['incdir'][0]
    record['incdir'][0]=str(directory/'shape')
    source=sweep.find_declaring(record['src'],'module milan_datapath')
    altered=directory/'milan_datapath.sv'
    altered.write_text(sweep.patch_params(pathlib.Path(source).read_text(),params))
    record['src'][record['src'].index(source)]=str(altered)
    conversion=['sv2v','--top=milan_datapath', *['-D'+v for v in record['define']],
                *['-I'+v for v in record['incdir']],*record['src']]
    rows=[]
    for flow in ('run.sh','ooc.sh'):
        text=(root/'syn/yosys'/flow).read_text()
        replacements={'R="$(cd "$(dirname "$0")/../.." && pwd)"':'R='+shlex.quote(str(root)),
                      '. "$(dirname "$0")/malloc.sh"':'. '+shlex.quote(str(root/'syn/yosys/malloc.sh'))}
        for before,after in replacements.items():
            assert text.count(before)==1,(flow,before)
            text=text.replace(before,after)
        before='sv2v --top="$top" '+('$inc' if flow=='run.sh' else '$INC')+' $srcs'
        assert text.count(before)==1,(flow,before)
        text=text.replace(before,shlex.join(conversion))
        script=directory/flow; script.write_text(text)
        cli=['--top','milan_datapath','--no-structural'] if flow=='run.sh' else ['milan_datapath']
        env=dict(os.environ,TMPDIR=str(directory),OOC_TMP=str(directory/'ooc'),OOC_CHPARAM='')
        label='shipping-'+name+'-'+flow.removesuffix('.sh')
        start=time.monotonic()
        with (packet/'receipts'/(label+'.log')).open('w') as log:
            done=subprocess.run(['bash',str(script),*cli],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1200)
        result=dict(shape=name,flow=flow,rc=done.returncode,seconds=round(time.monotonic()-start,3),params=params,argv=argv)
        (packet/'receipts'/(label+'.json')).write_text(json.dumps(result,indent=2)+'\n')
        (packet/'receipts'/(label+'.rc')).write_text(str(done.returncode)+'\n')
        print(json.dumps(result),flush=True); rows.append(result)
    return rows
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    results=[r for rows in executor.map(one,names) for r in rows]
(packet/'receipts/shipping-flows-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['rc']==0 for r in results),results
