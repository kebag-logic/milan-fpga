# SPDX-License-Identifier: Apache-2.0
"""Independent faults use the upstream build/check driver on disposable copies."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--packet',type=Path,required=True)
p.add_argument('--profile',choices=['OFF','ON'],required=True)
a=p.parse_args();source=a.source.resolve();packet=a.packet.resolve()
spec=importlib.util.spec_from_file_location('reversal_driver',source/'tests/check_reversals.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.CASES=[
 ('own-domain-byte-order',m.MSRP,
  'be16_put(buf + 2, d->vid);',
  'buf[2] = (uint8_t)d->vid; buf[3] = (uint8_t)(d->vid >> 8);', 'unit'),
 ('own-destination-increment',m.MSRP,
  'increment_stream(t->dest_mac, 6, offset)',
  'increment_stream(t->dest_mac, 6, 0)', 'unit'),
 ('own-missing-destination-replay',m.MAD,
  'static void map_replay(struct mrp_app *app, uint8_t port_id)\n{',
  'static void map_replay(struct mrp_app *app, uint8_t port_id)\n{\n    if (port_id == 1) { return; }', 'unit'),
]
m.REQUIRED_FAILURES={
 'own-domain-byte-order':['domain'],
 'own-destination-increment':['stream_vectors_cannot_wrap_identity_or_destination'],
 'own-missing-destination-replay':['retained_ports_replay_propagated_join_and_timer_leave_in_order'],
}
work=packet/'scratch'/('own-plants-'+a.profile)
sys.argv=['check_reversals.py','--work-dir',str(work),'--prefix',str(packet/'scratch/deps'),'--milan',a.profile]
rc=m.main()
out=packet/'receipts'/('own-plants-'+a.profile);out.mkdir(exist_ok=True)
for f in work.iterdir():
    if f.is_file() and f.suffix in ['.log','.json']:
        (out/f.name).write_text(f.read_text().replace(str(source),'$SOURCE').replace(str(packet),'$PACKET'))
(out/'campaign.rc').write_text(str(rc)+'\n')
raise SystemExit(rc)
