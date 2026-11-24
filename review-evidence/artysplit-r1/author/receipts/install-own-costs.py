"""Install a measured Arty model, leaving every existing shape's row untouched.

The input remains a candidate until its changed image passes the full census.
This helper is intentionally not run while prepared measurement arms are queued.
"""
import ast,json,math,sys
from pathlib import Path
root=Path.cwd()
model=json.loads(Path(sys.argv[1]).read_text())
assert model['status']=='CANDIDATE MODEL' and model['cpu_hz']==80_000_000 and model['shape']==[1,1,2]
assert model['choices']
choice=model['choices'][0]; c=model['costs']
assert not choice['owner_findings']
def edit(name,old,new):
    path=root/name; text=path.read_text()
    assert text.count(old)==1,(name,old)
    path.write_text(text.replace(old,new))
def add_entry(name,variable,key,value):
    path=root/name; text=path.read_text()
    tree=ast.parse(text)
    node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==variable for t in n.targets))
    assert isinstance(node.value,ast.Dict)
    assert key not in [ast.literal_eval(k) for k in node.value.keys]
    lines=text.splitlines(keepends=True)
    offset=sum(map(len,lines[:node.value.lineno-1]))+node.value.col_offset+1
    row=f'\n    {key!r}: {value!r},'
    path.write_text(text[:offset]+row+text[offset:])
base='tb/verilator/ctrl_service_budget/'
header='sw/firmware/ctrl/loop/ctrl_loop.h'
text=(root/header).read_text()
start=text.index('#elif CTRL_LOOP_SHAPE(1u, 1u, 2u)')
end=text.index('#else',start)
values=dict(CTRL_LOOP_SLICE_US=choice['slice_us'],CTRL_LOOP_BUILD_PASS_US=c['build'],
            CTRL_LOOP_BUILD_ONE_PASS_US=c['build_one'],CTRL_LOOP_SRP_UNIT_US=c['record.srp'],
            CTRL_LOOP_RETRY_COLD_US=model['retry_us'][0],CTRL_LOOP_RETRY_ATTEMPT_US=model['retry_us'][1],
            CTRL_LOOP_QUEUED_MS=choice['queued_ms'],CTRL_LOOP_TX_MS=math.ceil(choice['rows_ms']['tx']-1e-9),
            CTRL_LOOP_STEP_PASS_US=c['step'],CTRL_LOOP_TICK_US=c['centisecond'],
            AECP_NOTICE_US=model['retry_us'][2],AECP_PACE_MS=choice['pace_ms'])
block='#elif CTRL_LOOP_SHAPE(1u, 1u, 2u)      // Arty FPGA: one interface, AAF talker, AAF and CRF sinks, 80 MHz\n'
block+=''.join(f'#define {name} {number}u\n' for name,number in values.items())
(root/header).write_text(text[:start]+block+text[end:])
for name,path in (('CTRL_LOOP_STEP_PASS_US',header),('CTRL_LOOP_TICK_US',header),
                  ('AECP_NOTICE_US','sw/firmware/ctrl/aecp/aecp_mbx.h'),
                  ('AECP_PACE_MS','sw/firmware/ctrl/aecp/aecp_mbx.h')):
    text=(root/path).read_text(); lines=[x for x in text.splitlines() if x.startswith('#define '+name+' ')]
    # The last definition is the existing default, not the new Arty literal.
    line=lines[-1]
    edit(path,line+'\n','#ifndef '+name+'\n'+line+'\n#endif\n')
edit(base+'shape_costs.py','QUEUED, TX = BOUNDS\n',
     "QUEUED, TX = BOUNDS\n#: Arty's 80 MHz FPGA point states these additional measured costs and its own pace.\n"
     "ARTY_NAMES = ('CTRL_LOOP_STEP_PASS_US', 'CTRL_LOOP_TICK_US', 'AECP_NOTICE_US', 'AECP_PACE_MS')\n")
edit(base+'shape_costs.py','        costs: dict[str, int] = {}\n',
     '        names = NAMES + BOUNDS + (ARTY_NAMES if shape == Shape(1, 1, 2) else ())\n'
     '        costs: dict[str, int] = {}\n')
edit(base+'shape_costs.py','define[1] not in NAMES + BOUNDS','define[1] not in names')
edit(base+'shape_costs.py','if tuple(costs) != NAMES + BOUNDS:','if tuple(costs) != names:')
edit(base+'shape_costs.py','join(NAMES + BOUNDS)','join(names)')
poll=dict(base=c['base'],withdraw=c['item.withdraw'],rebuild=c['item.rebuild'],walk=c['item.walk'],
          reclaim=c['item.reclaim'],retained=c['record.srp'],mrpdu=0,acmp=c['item.acmp'],aecp=c['item.aecp'],
          aecp_long=c['item.aecp_long'],acmp_declined=c['item.acmp_declined'])
edit(base+'poll_grade.py',
     '# Unqualified bootstrap: zero statements expose every measurement as a finding.\n'
     'STATED_US[shape_costs.Shape(1, 1, 2)] = {name: 0 for name in ONE}',
     '# Arty FPGA measurements at exactly 80 MHz; no interface-count fallback.\n'
     'STATED_US[shape_costs.Shape(1, 1, 2)] = '+repr(poll))
edit(base+'poll_grade.py',
     "        # Until qualification supplies the row, expose the measurement against zero.\n"
     "        return load_grade.STATED_US.get('arty-1x1', {}).get('record.acmp', 0)",
     "        return load_grade.STATED_US['arty-1x1']['record.acmp']")
keys=['record.srp','record.aecp','record.acmp','record.adp','record.maap',
      'event.ADP','event.ACMP','event.MAAP','event.AECP','event.TICK','event.GM','centisecond','events_none',
      'item.retained','item.aecp.notice','item.aecp.response','item.aecp.probe']
row={k:c[k] for k in keys}
add_entry(base+'load_grade.py','STATED_US','arty-1x1',row)
add_entry(base+'load_grade.py','STATED_US_DONOR','arty-1x1',row)
add_entry(base+'load_grade.py','POINTS','arty-1x1',dict(n_if=1,sources=1,sinks_per_if=2,registrations=16,counter_descriptors=5))
add_entry(base+'load_grade.py','CEILING','arty-1x1',0.70)
edit(base+'load_grade.py',"CEILING != {'1x1/1if': 0.70}","CEILING != {'1x1/1if': 0.70, 'arty-1x1': 0.70}")
edit(base+'load_grade.py',"SRP_UNIT_POINTS = ('1x1/1if', '8x8/2if', '8x8/1if')",
     "SRP_UNIT_POINTS = ('1x1/1if', '8x8/2if', '8x8/1if', 'arty-1x1')")
edit('sw/firmware/ctrl/loop/ctrl_loop.c',
     '_Static_assert(!CTRL_LOOP_SHAPE(1u, 2u, 2u) || CTRL_LOOP_TX_MS <= CTRL_LOOP_TX_BOUND_MS,',
     '_Static_assert(!(CTRL_LOOP_SHAPE(1u, 2u, 2u) || CTRL_LOOP_SHAPE(1u, 1u, 2u)) ||\n'
     '\t       CTRL_LOOP_TX_MS <= CTRL_LOOP_TX_BOUND_MS,')
add_entry(base+'rows_grade.py','ROW_COSTS','arty-1x1',{'event.LINK':c['event.LINK']})
add_entry(base+'rows_tiers.py','DATAPATH_US','arty-1x1',
          {k:c['event.'+k] for k in ('AVB_INFO_CHANGED','AS_PATH_CHANGED','AMAP_LIVE_WRITE')})
add_entry(base+'rows_tiers.py','LONG_RECORD_US','arty-1x1',c['record.aecp.long'])
edit(base+'rows_tiers.py',"for p in (*POINTS, '8x8/1if')}","for p in (*POINTS, '8x8/1if', 'arty-1x1')}")
add_entry(base+'edit_rows.py','PACED','arty-1x1',
          {'a one-row edit':max(c['paced.44'],c['paced.45']),'an accepted SET_CONFIGURATION':c['paced.6']})
phy='sw/firmware/ctrl/plat/ctrl_plat_phy.h'
edit(phy,'#define CTRL_PLAT_PHY_STEP_US 155u',
     '// Arty MII at 80 MHz: 14,487 cycles, 181.0875 us; plus 5 %, rounded up to 5 us.\n'
     '#define CTRL_PLAT_PHY_MII_STEP_US 195u\n'
     '#ifdef CTRL_PLAT_PHY_100_ONLY\n#define CTRL_PLAT_PHY_STEP_US CTRL_PLAT_PHY_MII_STEP_US\n#else\n'
     '#define CTRL_PLAT_PHY_STEP_US 155u\n#endif')
boot='tb/verilator/ctrl_split_boot/run.py'
edit(boot,'def phy_constants() -> tuple[float, float]:','def phy_constants(mii: bool = False) -> tuple[float, float]:')
edit(boot,"    step = re.search(r'^#define CTRL_PLAT_PHY_STEP_US (\\d+)u$', header, re.M)",
     "    name = 'CTRL_PLAT_PHY_MII_STEP_US' if mii else 'CTRL_PLAT_PHY_STEP_US'\n"
     "    step = re.search(rf'^#define {name} (\\d+)u$', header, re.M)")
edit(boot,'    poll_us, step_us = phy_constants()','    poll_us, step_us = phy_constants(mii)')
print(json.dumps(dict(status='INSTALLED CANDIDATE; full image qualification required',constants=values),indent=2))

# The measured FPGA point stays separate from #983's host-only header.
edit(header, '// own clock, the 100 MHz bus clock\n',
     '// own clock, the bus clock: 100 MHz at AX7101, exactly 80 MHz at Arty\n')
edit(header, '#ifdef CTRL_SRP_SOURCES\n',
     '// Arty FPGA (1,1,2), #878: every cost is measured at 80 MHz. The row also\n'
     '// states its own aged step, centisecond work, notice cost and AECP pace;\n'
     '// the defaults below remain the existing AX7101 statements. This is not\n'
     '// a Linux-host scheduling profile. Section 15 of SPLIT_CONTROL_MEMORY.md\n'
     '// records the cost basis, rules, owner bounds and held-egress ledger.\n'
     '#ifdef CTRL_SRP_SOURCES\n')
edit(base+'run.py',
     "#: arty-1x1 is #878's exact-clock measurement point, not a qualified scheduler row.",
     "#: arty-1x1 is #878's FPGA point: one AAF source, AAF/CRF sinks, CPU/sys exactly 80 MHz.")
