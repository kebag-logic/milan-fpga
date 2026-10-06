#!/usr/bin/env python3
"""Recompute the DN timing observations from raw trace lines."""
import json,pathlib,re
p=pathlib.Path(__file__).resolve().parents[1];s=(p/'receipts/trace.log').read_text()
last=[int(x) for x in re.findall(r'TRACE_RX_LAST t=(\d+) ethertype=22ea',s)]
returns=[int(x) for x in re.findall(r'TRACE_FEED_RETURN t=(\d+) ethertype=22ea',s)]
tx=[(int(t),bytes.fromhex(f)) for t,f in re.findall(r'TRACE_TX t=(\d+) bytes=([0-9a-f]+)',s)]
notifications=[(t,f) for t,f in tx if f[36]&128]
assert len(tx)==5 and len(notifications)==4
assert last==[340030,460064,580098,700132]
assert returns==[340034,460068,580102,700136]
assert [b-a for a,b in zip(last,returns)]==[4]*4
assert [t for t,f in notifications]==[100466,220466,340529,580597]
assert [int.from_bytes(f[34:36],'big') for t,f in notifications]==[0,1,2,3]
assert all((int.from_bytes(f[36:38],'big')==0x8027 and f[38:42]==bytes.fromhex('00090000') and len(f)==66 and (int.from_bytes(f[16:18],'big')&2047)==40) for t,f in notifications)
reg=tx[0][0];down=int(re.search(r'TRACE_LINK_DOWN t=(\d+)',s)[1]);up=int(re.search(r'TRACE_LINK_UP t=(\d+)',s)[1])
rows=[{'event':'adoption','rx_last':last[0],'feed_return':returns[0],'tx_last':notifications[2][0]},{'event':'return-to-default-values','rx_last':last[2],'feed_return':returns[2],'tx_last':notifications[3][0]}]
for row in rows:
 row.update(from_last_byte=row['tx_last']-row['rx_last'],from_feed_return=row['tx_last']-row['feed_return'])
 assert row['from_last_byte']==499 and row['from_feed_return']==495
assert down-reg==96536 and notifications[0][0]-down==466 and notifications[1][0]-up==466
assert 'DN: 15 checks, 0 failures' in s
print(json.dumps({'domain':rows,'register_response':reg,'link_down':down,'link_up':up,'first_spacing_clocks':down-reg,'wire_frames':len(tx),'notifications':len(notifications),'verdict':'PASS'},indent=2))
