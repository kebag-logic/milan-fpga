#!/usr/bin/env python3
"""Re-derive the issue 117 step 3 per-cycle record from the published A202 packet.

usage: step3_rederive.py <archive-root: .../review-evidence/117-r1> [--json out.json]
Reads, per cycle: powerstrip.txt, clock-before/after.jsonl, console.txt, tap-cN.pcap,
pw1-cN.pcap and pw1-watch.jsonl. Times are seconds after the outlet-off command on the
build-box clock (power-strip host time minus its measured offset). Written independently of
the packet's own analysis scripts; imports only tapdec.py beside it.
"""
import datetime as dt
import json
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tapdec  # noqa: E402

ROOT = sys.argv[1]
A202 = os.path.join(ROOT, 'bench-a202', 'bench')
DUT = '020000fffe000001'
SW = '3cc0c6fffefe0210'
DUT_SPI = DUT + ':0001'


def iso(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()


def offsets(cdir):
    o = {}
    for fn in ('clock-before.jsonl', 'clock-after.jsonl'):
        for ln in open(os.path.join(cdir, fn)):
            j = json.loads(ln)
            host = j['host'].split('>')[-1]
            o.setdefault(host, []).append(j['offset_s_median_best5'])
    return {h: sum(v) / len(v) for h, v in o.items()}


def powerstrip(cdir):
    t = {}
    for ln in open(os.path.join(cdir, 'powerstrip.txt')):
        m = re.match(r'(?:\w+=\d+ )?(T_\w+) ([0-9.]+)', ln.strip())
        if m:
            t[m.group(1)] = float(m.group(2))
    return t


def console(cdir):
    txt = open(os.path.join(cdir, 'console.txt'), encoding='latin-1').read()
    blocks = re.split(r'^### ', txt, flags=re.M)[1:]
    samples, cmds = [], []
    cur = None
    for b in blocks:
        hdr = b.split('\n', 1)[0]
        m = re.match(r"(\S+) cmd='([^']*)'", hdr)
        if not m:
            continue
        t, cmd = iso(m.group(1)), m.group(2)
        cmds.append(cmd.split()[0])
        if cmd == 'milan_status':
            kv = dict(re.findall(r'(\w+)=([0-9A-Za-z_x]+)', b))
            if 'CLKV_STAT' not in kv:
                continue
            cur = dict(t=t, gm=kv.get('GPTP_GM'), parent=kv.get('GPTP_PARENT'),
                       pc=kv.get('AS_PATH_COUNT'), pg=kv.get('AS_PATH_GEN'),
                       clkv=int(kv['CLKV_STAT'], 16), sync=kv.get('SYNC'), asc=kv.get('ASCAPABLE'),
                       tu=kv.get('TU'), pdelay=int(kv.get('PDELAY_NS', '0')),
                       tai=int(kv['TAI_NS'], 16) if 'TAI_NS' in kv else None)
            samples.append(cur)
        elif cmd.startswith('mem_read') and cur is not None:
            addr = int(cmd.split()[1], 16)
            cur.setdefault('t_mem', {})[addr] = t
            m2 = re.search(r'0x%08x\s+((?:[0-9a-f]{2} ){4})' % addr, b)
            if m2:
                v = int.from_bytes(bytes.fromhex(m2.group(1).replace(' ', '')), 'little')
                cur[{0x90000780: 'tucnt', 0x90000774: 'linkg', 0x90000720: 'rst',
                     0x90000750: 'crft_ctrl', 0x90000764: 'crft_count'}.get(addr, hex(addr))] = v
    return samples, cmds


def first(samples, t0, pred):
    for s in samples:
        if s['t'] >= t0 and pred(s):
            return s
    return None


def analyse(n):
    cdir = os.path.join(A202, f'cycle{n}')
    off = offsets(cdir)
    ps = powerstrip(cdir)
    off_pi, off_srv, off_pw1 = off['pi'], off['ubuntu-server'], off['pw1']
    T0 = ps['T_OFF_CMD'] - off_pi
    rel = lambda t: round(t - T0, 3)
    S, cmds = console(cdir)
    R = dict(cycle=n, off_for=round(ps['T_ON_CMD'] - ps['T_OFF_CMD'], 2))
    R['console_samples'] = len(S)
    gaps = [b['t'] - a['t'] for a, b in zip(S, S[1:])]
    R['console_max_gap'] = round(max(gaps), 3)
    R['console_cmd_kinds'] = sorted(set(cmds))
    R['rst_epoch_values'] = sorted({s.get('rst') for s in S if 'rst' in s})
    s_sync0 = first(S, T0, lambda s: s['sync'] == '0')
    s_gmself = first(S, T0, lambda s: s['gm'] == DUT)
    s_asc0 = first(S, T0, lambda s: s['asc'] == '0')
    s_asc1 = first(S, s_asc0['t'], lambda s: s['asc'] == '1')
    s_gmsw = first(S, s_gmself['t'], lambda s: s['gm'] == SW)
    good = lambda s: s['gm'] == SW and s['sync'] == '1' and s['asc'] == '1' and s['tu'] == '0'
    idx = len(S)
    while idx > 0 and good(S[idx - 1]):
        idx -= 1
    s_all = S[idx]
    R.update(sync0=rel(s_sync0['t']), sync0_tu=s_sync0['tu'], gm_self=rel(s_gmself['t']),
             asc0=rel(s_asc0['t']), asc1=rel(s_asc1['t']), gm_switch=rel(s_gmsw['t']),
             all_good=rel(s_all['t']), all_good_prev_good=good(S[idx - 1]))
    R['asc1_pdelay_ns'] = s_asc1['pdelay']
    R['pdelay_after_return_range'] = [min(s['pdelay'] for s in S if s['t'] >= s_asc1['t']),
                                      max(s['pdelay'] for s in S if s['t'] >= s_asc1['t'])]
    # holdover (CLKV_STAT bit 3) episodes after the off command
    eps, cur = [], None
    for s in S:
        if s['t'] < T0:
            continue
        h = (s['clkv'] >> 3) & 1
        if h and cur is None:
            cur = [s['t'], None, 0, s['gm']]
        if h:
            cur[2] += 1
        if not h and cur is not None:
            cur[1] = s['t']
            eps.append(cur)
            cur = None
    R['holdover_episodes'] = [dict(first_set=rel(e[0]), first_clear=rel(e[1]) if e[1] else None,
                                   samples=e[2], span=round(e[1] - e[0], 3) if e[1] else None, gm_at_set=e[3])
                              for e in eps]
    sync1 = first(S, s_gmsw['t'], lambda s: s['sync'] == '1')
    tu0 = first(S, s_gmsw['t'], lambda s: s['tu'] == '0')
    R['sync1_after_adoption'] = round(sync1['t'] - s_gmsw['t'], 3)
    R['tu0_after_adoption'] = round(tu0['t'] - s_gmsw['t'], 3)
    tuc = [s.get('tucnt') for s in S if 'tucnt' in s]
    tu_on = [s for s in S if s['tu'] == '1' and s['t'] >= T0]
    R['tu1_span'] = round(tu_on[-1]['t'] - tu_on[0]['t'], 3) if tu_on else None
    pre = [s.get('tucnt') for s in S if s['t'] < s_sync0['t'] and 'tucnt' in s]
    post = [s.get('tucnt') for s in S if s['t'] >= s_all['t'] and 'tucnt' in s]
    R['tucnt_delta'] = (post[-1] - pre[-1]) if pre and post else None
    R['path_gen'] = [s_sync0['pg'], s_gmself['pg'], s_gmsw['pg']]
    R['path_count_values'] = sorted({s['pc'] for s in S})
    lk = [(rel(s['t']), s.get('linkg')) for s in S if 'linkg' in s and s['t'] >= T0]
    trans = []
    for (t1, v1), (t2, v2) in zip(lk, lk[1:]):
        if v1 != v2:
            trans.append((t2, v2))
    R['linkg_transitions'] = trans[:4]
    lkm = [(rel(s['t_mem'][0x90000774]), s.get('linkg')) for s in S if 'linkg' in s and s['t'] >= T0]
    R['linkg_transitions_by_mem_read_time'] = [(b[0], b[1], a[0]) for a, b in zip(lkm, lkm[1:]) if a[1] != b[1]][:4]
    # PHC step: TAI_NS minus the build-box time at the command
    steps = []
    prev = None
    for s in S:
        if s['tai'] is None:
            continue
        d = s['tai'] / 1e9 - s['t']
        if prev is not None and abs(d - prev[1]) > 0.05:
            steps.append((rel(s['t']), round(d - prev[1], 3)))
        prev = (s['t'], d)
    R['phc_steps'] = steps
    if any('crft_ctrl' in s for s in S):
        cr = [(rel(s['t']), s['crft_ctrl']) for s in S if 'crft_ctrl' in s]
        drops = [t for (t1, v1), (t, v) in zip(cr, cr[1:]) if v1 != 0x3 and v == 0x3 and t > 0]
        relic = [t for (t1, v1), (t, v) in zip(cr, cr[1:]) if v1 == 0x3 and v != 0x3 and t > 0]
        R['crf_licence_drop'] = drops[:1]
        R['crf_relicensed'] = relic[:1]
        R['crf_relicensed_after_all_good'] = round(relic[0] - R['all_good'], 3) if relic else None
        R['clkv_tu_rise_interval'] = [rel(S[S.index(s_sync0) - 1]['t']), rel(s_sync0['t'])]

    # ---------------- tap on the DUT link
    recs, noenv = tapdec.tap_records(os.path.join(cdir, f'tap-c{n}.pcap'))
    fit = tapdec.fit_consensus(recs)
    R['tap_records'] = len(recs)
    R['tap_envelope_less'] = noenv
    R['tap_fit_windows'] = [fit[2], fit[3]]
    R['tap_fit_resid_max_ms'] = round(fit[4], 3)
    ev = []
    for r in recs:
        d = tapdec.decode(r['frame'])
        t = (tapdec.tap_to_host(r, fit) / 1e9) - off_srv
        ev.append((t - T0, r['port'], d))
    ev.sort(key=lambda e: e[0])
    sw_ev = [e for e in ev if e[1] == 2]
    dut_ev = [e for e in ev if e[1] == 3]
    # dark window: the largest gap between consecutive records of either port
    gi = max(range(len(ev) - 1), key=lambda i: ev[i + 1][0] - ev[i][0])
    R['dark_from'] = round(ev[gi][0], 3)
    R['dark_from_port'] = ev[gi][1]
    R['dark_from_kind'] = ev[gi][2].get('kind')
    R['dark_to'] = round(ev[gi + 1][0], 3)
    sgi = max(range(len(sw_ev) - 1), key=lambda i: sw_ev[i + 1][0] - sw_ev[i][0])
    R['switch_last_frame'] = round(sw_ev[sgi][0], 3)
    R['switch_first_frame'] = round(sw_ev[sgi + 1][0], 3)
    t_ret = sw_ev[sgi + 1][0]
    t_lost = sw_ev[sgi][0]
    k = lambda e, kind: e[2].get('kind') == kind
    last_sync = max(e[0] for e in sw_ev if k(e, 'gPTP Sync') and e[0] <= t_lost)
    last_ann = max(e[0] for e in sw_ev if k(e, 'gPTP Announce') and e[0] <= t_lost)
    last_presp = max(e[0] for e in sw_ev if k(e, 'gPTP Pdelay_Resp') and e[0] <= t_lost
                     and e[2].get('req_spi') == DUT_SPI)
    first_ann = min(e for e in sw_ev if k(e, 'gPTP Announce') and e[0] >= t_ret)
    first_sync = min(e[0] for e in sw_ev if k(e, 'gPTP Sync') and e[0] >= t_ret)
    R['switch_last_sync'] = round(last_sync, 3)
    R['switch_last_announce'] = round(last_ann, 3)
    R['switch_last_presp_to_dut'] = round(last_presp, 3)
    R['switch_first_announce'] = round(first_ann[0], 3)
    R['switch_first_sync'] = round(first_sync, 3)
    fa = first_ann[2]
    R['first_announce_fields'] = dict(gm=fa['gm'], prio1=fa['prio1'], cclass=fa['cclass'], cacc=hex(fa['cacc']),
                                      cvar=hex(fa['cvar']), prio2=fa['prio2'], steps=fa['steps'],
                                      tsrc=hex(fa['tsrc']), path=fa['path'])
    R['recovery'] = round(R['all_good'] - min(first_ann[0], first_sync), 3)
    R['recovery_from_sync'] = round(R['all_good'] - first_sync, 3)
    R['sync0_after_last_sync'] = round(R['sync0'] - last_sync, 3)
    R['gmself_after_last_announce'] = round(R['gm_self'] - last_ann, 3)
    R['asc0_after_last_presp'] = round(R['asc0'] - last_presp, 3)
    R['on_to_all_good'] = round(R['all_good'] - (ps['T_ON_CMD'] - ps['T_OFF_CMD']), 3)
    R['first_frame_to_all_good'] = round(R['all_good'] - t_ret, 3)
    # the DUT's completed Pdelay exchanges after the return (its Req, the switch's Resp and Resp_FU)
    reqs = [e for e in dut_ev if k(e, 'gPTP Pdelay_Req') and e[0] >= t_ret - 1.5]
    done = []
    for rq in reqs:
        seq = rq[2]['seq']
        rs = [e for e in sw_ev if k(e, 'gPTP Pdelay_Resp') and e[2].get('seq') == seq and e[2].get('req_spi') == DUT_SPI and e[0] >= rq[0]]
        fu = [e for e in sw_ev if k(e, 'gPTP Pdelay_Resp_Follow_Up') and e[2].get('seq') == seq and e[2].get('req_spi') == DUT_SPI and e[0] >= rq[0]]
        if rs and fu:
            done.append(round(fu[0][0], 3))
    R['dut_completed_pdelay_after_return'] = done[:3]
    R['asc1_minus_2nd_pdelay'] = round(R['asc1'] - done[1], 3) if len(done) > 1 else None
    R['2nd_pdelay_after_first_frame'] = round(done[1] - t_ret, 3) if len(done) > 1 else None
    R['switch_ann_after_first'] = [round(e[0], 3) for e in sw_ev if k(e, 'gPTP Announce') and e[0] >= t_ret][:3]
    R['on_cmd'] = round(ps['T_ON_CMD'] - off_pi, 3)
    # DUT acting as master between the link's return and adoption
    msync = [e for e in dut_ev if k(e, 'gPTP Sync') and t_ret <= e[0] <= R['gm_switch'] + 0.2]
    mann = [e for e in dut_ev if k(e, 'gPTP Announce') and t_ret <= e[0] <= R['gm_switch'] + 0.2]
    R['dut_master_syncs'] = len(msync)
    R['dut_master_sync_window'] = [round(msync[0][0], 3), round(msync[-1][0], 3)] if msync else None
    R['dut_master_announces'] = [(round(e[0], 3), e[2]['gm'], e[2]['prio1']) for e in mann]
    R['dut_sync_or_announce_before_off'] = sum(1 for e in dut_ev if e[0] < 0 and (k(e, 'gPTP Sync') or k(e, 'gPTP Announce')))
    # DUT ADPDUs
    adp = [e for e in dut_ev if k(e, 'ADP') and e[0] >= 0]
    R['dut_adp_during_absence'] = [round(e[0], 3) for e in adp if e[0] < R['gm_switch']]
    first_adp = next((e for e in adp if e[0] >= R['gm_switch']), None)
    R['dut_first_adp_after_adoption'] = (round(first_adp[0] - R['gm_switch'], 3), first_adp[2].get('adp_gm')) if first_adp else None
    R['dut_adp_gm_values'] = sorted({e[2].get('adp_gm') for e in dut_ev if k(e, 'ADP')})
    # CRF
    crf = [e for e in dut_ev if k(e, 'CRF')]
    if crf:
        loss = [e for e in crf if 0 <= e[0] <= R['dark_to']]
        tu1 = [e for e in loss if e[2]['tu'] == 1]
        R['crf_first_tu1'] = round(tu1[0][0], 3) if tu1 else None
        R['crf_tu1_count'] = len(tu1)
        R['crf_emission_end'] = round(loss[-1][0], 3) if loss else None
        after = [e for e in crf if e[0] > R['dark_to']]
        R['crf_first_after_return'] = round(after[0][0], 3) if after else None
        R['crf_after_return_tu_values'] = sorted({e[2]['tu'] for e in after})
        R['crf_before_off_tu_values'] = sorted({e[2]['tu'] for e in crf if e[0] < 0})
    # ACMP CONNECT_TX commands addressed to the DUT as talker
    ctx = [e for e in ev if k(e, 'ACMP') and e[2]['acmp_mt'] == 0 and e[2].get('talker') == DUT]
    mts = {}
    for e in ev:
        if k(e, 'AECP') and e[2].get('target') == DUT and e[1] == 2:
            mts[e[2].get('aecp_mt')] = mts.get(e[2].get('aecp_mt'), 0) + 1
    R['aecp_msg_types_to_dut'] = mts
    am = {}
    for e in ev:
        if k(e, 'ACMP') and e[1] == 2:
            am[e[2].get('acmp_mt')] = am.get(e[2].get('acmp_mt'), 0) + 1
    R['acmp_msg_types_from_far_end'] = am
    R['connect_tx_between_off_and_all_good'] = [round(e[0], 3) for e in ctx if 0 <= e[0] <= R['all_good']]
    fct = next((e for e in ctx if e[0] > R['all_good']), None)
    R['first_connect_tx_after_all_good'] = round(fct[0], 3) if fct else None
    # AECP commands to the DUT: command codes by message type (0 = AEM_COMMAND)
    codes = {}
    for e in ev:
        if k(e, 'AECP') and e[2].get('target') == DUT and e[2].get('aecp_mt') == 0 and 'cmd' in e[2]:
            codes[e[2]['cmd']] = codes.get(e[2]['cmd'], 0) + 1
    R['aecp_cmd_codes_to_dut'] = sorted('0x%04x' % c for c in codes)
    # ---------------- controller-host port capture and watcher
    wat = [json.loads(l) for l in open(os.path.join(cdir, 'pw1-watch.jsonl'))]
    car = [(round(w['t'] - off_pw1 - T0, 3), w['value']) for w in wat if w.get('type') == 'carrier']
    R['carrier'] = car
    return R, ev, cdir


def main():
    out = []
    for n in range(1, 7):
        R, ev, cdir = analyse(n)
        out.append(R)
    if '--json' in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
    cols = ['cycle', 'off_for', 'sync0', 'gm_self', 'asc0', 'switch_first_frame', 'switch_first_announce',
            'asc1', 'gm_switch', 'all_good', 'recovery']
    print('\t'.join(cols))
    for R in out:
        print('\t'.join(str(R[c]) for c in cols))
    for R in out:
        print(json.dumps({k: v for k, v in R.items()}, default=str))


if __name__ == '__main__':
    main()
