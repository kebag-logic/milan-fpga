"""The 32x32/2if point's backlog-owed script from a tree: its owed frames and its transmit waits. usage: TREE"""
import re, sys
from pathlib import Path
tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget')); sys.path.insert(0, str(tree / 'sw/mailbox'))
import scenario, gen_mailbox
layout = gen_mailbox.shape_variant(scenario.CONTRACT, tree / 'configs/endstation_ax7101_32x32.yaml', 2)[0]
p = scenario.Point('32x32', 'endstation_ax7101_32x32', 2, 0x0102030405060708, 0x020304050607, 33, 33, layout)
g = next(g for g in scenario.backlog_groups(p) if g.name == 'backlog-owed')
s = g.script()
head = s[:s.index('mark composed')]
print('owed frames before the window:', len(re.findall(r'^frame 0 ', head, re.M)))
print('transmit waits:', re.findall(r'^wait tx 1 \d+ within \d+', head, re.M))
