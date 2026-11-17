import sys, pathlib, math
root=pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import rows_tiers as rt
import shape_costs as sc
import load_grade as lg
import rows_grade as rg
import poll_grade as pg
from unittest.mock import patch
point='8x8/1if'
rg.ROW_COSTS[point] = dict(rg.ROW_COSTS['8x8/2if'])
rt.DATAPATH_US[point] = dict(rt.DATAPATH_US['8x8/2if'])
polls=pg.stated_us(sc.of_point(point,root))
rt.LONG_NOTICE_US[point]=polls[pg.LONG]
i=rt.point_inputs(root,point)
notices=sc.notices_most(root/'configs/endstation_ax7101_8x8.yaml',1,root)
i=i._replace(c={**i.c,**{f'item.{k}':polls[k] for k in ('withdraw','rebuild','aecp')}},s={**i.s,'notices':notices},h={**i.h,'AECP_NOTICES_MOST':notices})
w=rt.solve('tx',i,rt.BUILT)[0]
print('Head:', __import__('subprocess').check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip())
with patch.object(rt,'point_inputs',return_value=i):
 print('tx_statements with the published shape input recipe:',rt.tx_statements(root,(point,)))
print('tx row ms:',format(w,'.9f'),'stated ms:',i.tx_stated,'required ceiling ms:',math.ceil(w-1e-9))
join=19
hold_cs=2000+join+(i.tx_stated+9)//10
fixed_cs=2000+join+(math.ceil(w-1e-9)+9)//10
print('Current hold-off cs:',hold_cs,'hold-off if statement covers model:',fixed_cs)
print('Minimum remaining hold after latest modelled Leave, ms:',hold_cs*10-join*10-w)
print('Required after Leave: 20000 ms (IEEE 802.1Q-2018 35.2.2.8, source contract srp_mbx.c:30-36)')
print('MODEL ENVELOPE CHECK:', 'FAIL' if hold_cs*10-join*10-w<20000 else 'PASS')
print('Default tx_statements:',rt.tx_statements(root))
print('\nCurrent model table:')
for row,(val,terms) in rt.rows(root,point,rt.BUILT,i).items():
 print(row,format(val,'.5f'))
print('\nThis probe does not claim an observed early wire departure; it checks the declared timing envelope.')
