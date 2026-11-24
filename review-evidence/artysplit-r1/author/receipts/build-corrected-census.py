"""Measure the Arty point from completed 80 MHz traces; no other point's costs enter this table."""
import sys,json,bisect,collections,os
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tb/verilator/ctrl_service_budget'))
sys.path.insert(0,str(Path(__file__).parent))
import grade,poll_grade,whole_grade,round_grade,record_classes,shape_costs,parts,eventcost,scenario
HZ=80_000_000
shape=shape_costs.Shape(1,1,2)
most,where,counts,rounds,groups={},{},collections.Counter(),{},[]
paces={}
def rule(c): return -(-c*105//(80*100*5))*5
def note(k,c,g,at=None):
    counts[k]+=1
    if c>most.get(k,-1): most[k]=c; where[k]=dict(group=g,start=at)
for arg in sys.argv[2:]:
    d=Path(arg); spec=json.loads((d.parent/'build.json').read_text())
    assert spec['sys_hz']==spec['cpu_hz']==HZ and spec['cpu_cd']=='sys'
    # Prepared bootstrap images used the explicit 9 ms measurement pace.
    # Final images must record the own pace compiled into their frozen inputs.
    pace=spec.get('measurement_pace_ms')
    if pace is None:
        if 'final-census' in d.parts or os.environ.get('CENSUS_REQUIRE_PACE'):
            raise SystemExit('Final census refuses an unrecorded compiled pace')
        pace=9
    paces[str(d)]=pace
    accepted=set()
    for path in sorted(d.glob('*.log')):
        text=path.read_text(errors='replace')
        if 'RESULT: PASS' not in text[-4000:] and not os.environ.get('CENSUS_INCLUDE_RUNNING'): continue
        accepted.add(path.stem)
        g=d.parent.name+'/'+path.stem; groups.append(g)
        parsed=grade.parse(text,HZ,HZ)
        spans=poll_grade.spans(parsed)
        # A LINK event can run reset_interface before the poll observes the
        # level change. Measure the same withdrawal function in either context;
        # an empty poll-only population must not become a zero cost. The LINK
        # event's complete cost is measured separately by eventcost.
        for _,cycles,at in spans.get('srp_mbx:reset_interface',[]):
            note('item.withdraw',cycles,g,at)
        aecp=[(at,frame) for at,ch,_,frame in parsed.tx if ch==scenario.CH['aecp']]
        tx_at=[at for at,_ in aecp]
        for cpu,cycles,at in spans.get('aecp:transmit',[]):
            frames=[frame for _,frame in aecp[bisect.bisect_left(tx_at,at):bisect.bisect_left(tx_at,at+cycles)]]
            if not frames:continue
            if any(len(f)>poll_grade.fan_bytes() and f[15]&15==1 and f[36]&128 for f in frames):kind='long'
            elif any(f[15]&15==1 and f[36]&128 for f in frames):kind='notice'
            elif all(f[15]&15==0 and int.from_bytes(f[36:38],'big')==3 for f in frames):kind='probe'
            else:kind='response'
            note('tx.aecp.'+kind,cycles,g,at)
        for ch,label in parts.HANDLERS.items():
            if ch=='aecp': continue
            for _,c,at in spans.get(label,[]): note('record.'+ch,c,g,at)
        for k,c in poll_grade.held(parsed,shape)['heaviest'].items(): note('base' if k=='base' else 'item.'+k,c,g)
        for k,c in whole_grade.held(parsed,shape)['heaviest'].items(): note({'build-one':'build_one'}.get(k,k),c,g)
        for _,c,at in spans.get('ctrl_loop:dispatch_ticks',[]):
            if c>1000: note('centisecond',c,g,at)
        for r in round_grade.rounds(parsed):
            k=f"{r['notices']}:{r['refused']}"
            if r['cycles']>rounds.get(k,{}).get('cycles',-1): rounds[k]=dict(r,group=g)
        for kind,c in eventcost.costs(path): note('event.'+kind,c,g)
        parts._KEYS.clear(); passes,calls,ss=parts.parse(path)
        for start,cycles in passes:
            rx=parts.inside(calls.get('ctrl_loop:service_rx',[]),start,start+cycles)
            if not rx: continue
            takes=parts.inside(calls.get('mbx_event_take',[]),start,rx[0])
            if len(takes)<=1:
                ticks=parts.spans_in(ss.get('ctrl_loop:dispatch_ticks',[]),start,rx[0])
                note('events_none',rx[0]-start-sum(c for _,c in ticks),g,start)
        note('share',max([p.cycles for p in parsed.passes]+[n for _,_,n in parsed.idle]),g)
    leg,_=record_classes.read_leg(d)
    for group in leg.groups:
        if group not in accepted: continue
        for kind,r,c,_,why in record_classes.classes(leg,group,dict(pace_ms=pace,long=0,paced=0,other=0)):
            if record_classes.held(leg,group,kind,r.command,r.completions):
                note('record.aecp.'+kind,r.cycles,d.parent.name+'/'+group,r.start)
            if kind=='paced': note('paced.'+str(r.command),r.cycles,d.parent.name+'/'+group,r.start)
result=dict(status='measurement census; missing groups remain unqualified',cpu_hz=HZ,shape=list(shape),groups=groups,pace_ms_by_input=paces,
            costs={k:dict(cycles=v,us=v/80,rule_us=rule(v),instances=counts[k],**where[k]) for k,v in sorted(most.items())},rounds=rounds)
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print('Completed groups',len(groups))
for k,c in result['costs'].items(): print(k,c['cycles'],c['rule_us'],c['group'])
print('Retry maxima:',rounds)
