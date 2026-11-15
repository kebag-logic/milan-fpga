# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The self-test's checks of a record its channel's bucket held (#917, held.py), on synthetic logs.

Among them a frame refused behind a held one, its last byte 11 cycles before the held record's commit, which the
attribution before #917 credited with that commit (selftest_mutants.py plants that rule again).
"""
from __future__ import annotations

import types

import grade
import scenario

AECP, ACMP = scenario.CH['aecp'], scenario.CH['acmp']


def refused_by(st: types.ModuleType, lines: list[str], probe: scenario.Probe) -> str:
    """The grader's refusal of a synthetic log, '' when it grades it."""
    try:
        st.one(st.synthetic(lines), probe)
    except grade.Refusal as error:
        return str(error)
    return ''


def held_checks(st: types.ModuleType) -> list[tuple[str, bool, str]]:
    """A record its channel's bucket held (#917): its hold in its commit's place (RXH), its commit at the
    channel's next refill (RXR) credited to its own frame, not to a frame ended since that the filter or the
    bucket refused, and measured from its last byte with its ingress delay; a commit with no held frame, a
    second hold on one channel and a commit past the held allowance (FR_NFR.md 3.4.1) are refused."""
    probe = scenario.Probe('s.held.if0', 'READ_DESCRIPTOR held', 'aecp', f'rxh:{AECP}', [f'resp:{AECP}:7d00'])
    response = st.tx_record(AECP, 0, st.aem_response(scenario.CTL1, 0x7D00, 0x0004), 0, 700_000)
    # the held frame ends at 1059; a frame behind it, refused, ends 11 cycles before the refill's commit
    lines = ['MARK 1000 s.held.if0', 'RXS 1000 0 60 s.held.if0', 'RXE 1059', f'RXH 1070 {AECP}',
             'RXS 500030 0 60 -', 'RXE 500089', f'RXR 500100 {AECP}', *response]
    r = st.one(st.synthetic(lines), probe)
    out = [("a held record's commit belongs to its own held frame, measured from its last byte",
            r.get('start_sys') == 1059 and r.get('ingress_sys') == 500_100 - 1059 and r.get('end_sys') == 700_000,
            str(r))]
    log = grade.parse(st.synthetic(lines), st.SYS_HZ, st.CPU_HZ)
    out.append(('the frame refused behind a held one is not credited with its commit',
                [tag for _, _, _, tag, _ in log.rxc] == ['s.held.if0'] and [x[2] for x in log.refused] == ['-'],
                f'{log.rxc} {log.refused}'))
    out.append(("a held record's ingress is held to one refill period and T_ingress",
                r.get('ingress_allowance_ms') == scenario.CONTRACT.channels[AECP].refill_ms + 1.0, str(r)))
    other = [ln.replace(f'RXR 500100 {AECP}', f'RXR 500100 {ACMP}') for ln in lines]
    out.append(("a held record's commit on another channel is refused",
                'follows no held frame' in refused_by(st, other, probe), refused_by(st, other, probe)))
    orphan = ['MARK 1000 s.held.if0', 'RXS 1000 0 60 s.held.if0', 'RXE 1059', f'RXR 500100 {AECP}']
    out.append(('a held-record commit with no hold is refused',
                'follows no held frame' in refused_by(st, orphan, probe),
                refused_by(st, orphan, probe)))
    twice = lines[:4] + ['RXS 2000 0 60 -', 'RXE 2059', f'RXH 2070 {AECP}'] + lines[4:]
    out.append(('a second hold on a channel holding one is refused',
                'a second record held' in refused_by(st, twice, probe), refused_by(st, twice, probe)))
    late = [ln.replace(f'RXR 500100 {AECP}', f'RXR 701059 {AECP}') for ln in lines]
    out.append(('a held record committed past its allowance is refused', 'outside its allowance' in
                refused_by(st, late, probe), refused_by(st, late, probe)))
    unserved = grade.parse(st.synthetic(lines[:4]), st.SYS_HZ, st.CPU_HZ)
    out.append(('a held record never committed is not served', [x[2] for x in unserved.refused] == ['s.held.if0']
                and unserved.held[0][2] == -1, f'{unserved.refused} {unserved.held}'))
    at_once = ['MARK 1000 s.held.if0', 'RXS 1000 0 60 s.held.if0', 'RXE 1059', f'RXC 1063 {AECP}', *response]
    out.append(('a probe frame that was not held starts no held path',
                st.one(st.synthetic(at_once), probe).get('status')
                == 'no start', ''))
    return out
