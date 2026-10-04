#!/usr/bin/env python3
"""Independent recompute of the #653 B11 per-cycle table from the published evidence packet.
Sources: the provided decoder's per-capture text (its time column is LE64 of the tap's two
32-bit words, so the low (nanosecond) word is recovered as round(dX / 2**32) between lines,
modulo 2**32), the lane grade JSON, and the probe logs. Compares with the page's table.
usage: recompute.py <page.md> <packet author dir>"""
import json, re, sys, os
page, au = sys.argv[1], sys.argv[2]
P32 = 2 ** 32
fails = []
def chk(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    if not cond: fails.append(msg)

def parse_decode(path):
    out, lo, prev = [], 0, None
    for ln in open(path):
        m = re.match(r'\s*(-?[\d.]+) ms (\S+)\s+(.*)$', ln.rstrip('\n'))
        if not m: continue
        x = round(float(m.group(1)) * 1e6)          # X - X0 in decoder units (hi + lo*2^32)
        lo_abs = (x / P32)                           # lo - lo0 (ns), may be negative after wrap
        if prev is None: ns = 0.0
        else: ns = out[-1]['ns'] + ((lo_abs - prev) % P32)
        prev = lo_abs
        rest = m.group(3)
        d = dict(ns=ns, port=m.group(2), text=rest)
        mm = re.search(r'desc=0x5/(\d+)', rest); d['desc'] = int(mm.group(1)) if mm else None
        d['ML'] = int(re.search(r'MLOCK=(\d+)', rest).group(1)) if 'MLOCK=' in rest else 0
        d['MU'] = int(re.search(r'MUNLOCK=(\d+)', rest).group(1)) if 'MUNLOCK=' in rest else 0
        d['INTR'] = int(re.search(r'INTR=(\d+)', rest).group(1)) if 'INTR=' in rest else 0
        mm = re.search(r'ctl=(\w+)', rest); d['ctl'] = mm.group(1) if mm else None
        out.append(d)
    return out

g = json.load(open(os.path.join(au, 'summary/o653-grade.json')))
txt = open(page, encoding='utf-8').read()
rows = {}
for ln in txt.splitlines():
    m = re.match(r'^\| (C0 \(control\)|A\d\d|R\d\d) \|', ln)
    if m:
        c = [x.strip() for x in ln.strip('|').split('|')]
        rows['C0' if c[0].startswith('C0') else c[0]] = c
chk(len(rows) == 23, f'page per-cycle rows = {len(rows)}')
summary = {}
for key, v in g.items():
    if key.endswith('_session'): continue
    s, tag = key.split('/')
    L = v['library']['listener']
    dec = parse_decode(os.path.join(au, f'summary/decode/b11-a535-{s}-{tag}.decode.txt'))
    cmd = next(i for i, d in enumerate(dec) if 'ACMP UNBIND_RX_CMD' in d['text'])
    rsp = next(i for i, d in enumerate(dec) if 'ACMP UNBIND_RX_RESP' in d['text'] and i > cmd)
    chk(dec[cmd]['port'] == 'sw->DUT' and dec[rsp]['port'] == 'DUT->sw', f'{tag} cmd/rsp ports {dec[cmd]["port"]}/{dec[rsp]["port"]}')
    chk(' status=0 ' in dec[rsp]['text'] + ' ', f'{tag} UNBIND_RX_RESP status 0 (SUCCESS)')
    pushes = [i for i, d in enumerate(dec) if 'UNSOL GET_COUNTERS' in d['text'] and d['desc'] == L and d['port'] == 'DUT->sw']
    mub = max([dec[i]['MU'] for i in pushes if i < cmd], default=0)
    unl = next(i for i in pushes if dec[i]['MU'] > mub)
    order = 'RESPONSE_FIRST' if rsp < unl else 'COUNTERS_FIRST'
    c2r = (dec[rsp]['ns'] - dec[cmd]['ns']) / 1e3
    r2p = (dec[unl]['ns'] - dec[rsp]['ns']) / 1e3
    between = [dec[i]['text'].split(' tgt=')[0] for i in range(rsp + 1, unl)]
    push_ctls = sorted({dec[i]['ctl'] for i in pushes})
    w = v['wire']
    chk(order == w['order'] == 'RESPONSE_FIRST', f'{tag} order indep={order} grader={w["order"]} decoder_order={w["decoder_order"]}')
    chk(abs(c2r - w['cmd_to_rsp_us']) < 0.06, f'{tag} cmd->rsp indep={c2r:.3f}us grader={w["cmd_to_rsp_us"]}')
    chk(abs(r2p - w['rsp_to_push_us']) < 0.06, f'{tag} rsp->push indep={r2p:.3f}us grader={w["rsp_to_push_us"]}')
    pushed = f'{dec[unl]["ML"]}/{dec[unl]["MU"]}/{dec[unl]["INTR"]}'
    up = w['unlock_push']
    chk(pushed == f'{up["ML"]}/{up["MU"]}/{up["SI"]}', f'{tag} pushed indep={pushed} grader={up}')
    r = rows[tag]
    lib = v['library']
    post = lib['post']['counters']
    exp = [None, ('AAF, 0' if L == 0 else 'CRF, 1'), str(lib['lock_ms']), str(lib['hold_ms']), f'{w["cmd_to_rsp_us"]}',
           f'{w["rsp_to_push_us"]:,}', w['order'], f'{up["ML"]}/{up["MU"]}/{up["SI"]}', f'{w["stream_frames_after_cmd"]:,}',
           lib['lib_unlock_update']['lib_conn'], 'none' if not lib['library_flagged'] else 'yes',
           f'{post["ML"]}/{post["MU"]}/{post["SI"]}', f'`{w["sha256"][:12]}`']
    for k in range(1, 13):
        chk(r[k] == exp[k], f'{tag} page col{k} page="{r[k]}" evidence="{exp[k]}"')
    chk(w['talker_streaming_at_cmd'] and w['stream_frames_after_cmd'] > 0, f'{tag} talker streaming at cmd: after={w["stream_frames_after_cmd"]} last={w["last_stream_frame_after_cmd_ms"]}ms')
    chk(w['tap_time_monotonic_in_file_order'], f'{tag} tap time monotonic (grader)')
    chk(w['stream_sub'] == ('AAF' if L == 0 else 'CRF'), f'{tag} stream subtype {w["stream_sub"]}')
    chk(lib['bind'] == 'Success' or lib['bind'].startswith('Success'), f'{tag} bind {lib["bind"]}')
    chk(lib['formats']['equal'] and 'set_listener_format' not in lib, f'{tag} formats equal, none set')
    chk(lib['lib_order'] == 'RESPONSE_FIRST', f'{tag} library NotConnected before unlock update')
    gap_us = (lib['lib_unlock_update']['t'] - lib['t_lib_notconnected'])
    summary[tag] = dict(L=L, c2r=c2r, r2p=r2p, between=between, push_ctls=push_ctls, last_ms=w['last_stream_frame_after_cmd_ms'],
                        frames=w['stream_frames_after_cmd'], nc_to_upd_us=gap_us, unbind_to_upd_ms=lib['lib_unlock_after_unbind_ms'],
                        held10=lib['lib_held_1_0_after_unbind_ms'], ctl=w.get('control'))
print()
for t, s in summary.items():
    print(t, {k: (round(x, 3) if isinstance(x, float) else x) for k, x in s.items()})
aaf = [s for t, s in summary.items() if s['L'] == 0]
crf = [s for t, s in summary.items() if s['L'] == 1]
print('AAF rsp->push range', min(s['r2p'] for s in aaf), max(s['r2p'] for s in aaf))
print('AAF frames after cmd range', min(s['frames'] for s in aaf), max(s['frames'] for s in aaf))
print('AAF last frame ms range', min(s['last_ms'] for s in aaf), max(s['last_ms'] for s in aaf))
print('CRF last frame ms', [s['last_ms'] for s in crf])
print('AAF NotConnected->update us range', min(s['nc_to_upd_us'] for s in aaf), max(s['nc_to_upd_us'] for s in aaf))
print('AAF unbind->update ms range', min(s['unbind_to_upd_ms'] for s in aaf), max(s['unbind_to_upd_ms'] for s in aaf))
print('CRF held 1/0 ms', [s['held10'] for s in crf])
print('cmd->rsp all', sorted({round(s['c2r'], 1) for s in summary.values()}))
print('shapes', sorted({tuple(s['between']) for s in summary.values()}))
print('push ctls', sorted({tuple(s['push_ctls']) for s in summary.values()}))
print('FAILS', len(fails))
for f in fails: print('  ', f)
sys.exit(1 if fails else 0)
