# Reviewer probes of the wire-timing grader (#868) on the author's published real logs.
# Usage: python3 -I grader_probes.py <checkout> <ci-1x1-none wire.log> <ci-1x1-none results.json>
#                                     <8x8-none wire.log> <8x8-none results.json>
# Each probe changes one thing in a real log, as a firmware regression would leave it, and
# prints the grade's outcome. Nothing in the checkout is written.
import json
import sys

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + '/tb/verilator/ctrl_wire_timing')
sys.path.insert(0, ROOT + '/tb/verilator/ctrl_service_budget')
import wire_grade as g  # noqa: E402

SYS_HZ = 100_000_000


def outcome(text, draws=16, interfaces=1, announces=1):
    try:
        result, findings = g.grade(text, SYS_HZ, draws, interfaces, announces)
    except g.Refused as why:
        return None, [f'REFUSED: {why}']
    return result, findings


def frame(line):
    w = line.split()
    return bytes.fromhex(w[5] if w[0] == 'RXW' else w[4])


def is_acmp(line, kind, prefix):
    if not line.startswith(prefix):
        return False
    d = frame(line)
    return d[12:14] == b'\x22\xf0' and d[14] == 0xFC and (d[15] & 0x0F) == kind


def acmp_seq(line):
    return int.from_bytes(frame(line)[62:64], 'big')


def drop_probes(lines, keep):
    """Remove the PROBE_TX frames whose index (in TXW order) is not in `keep`, with the n-th ACMP commit
    (TXC ch 1) and the n-th ACMP KL_mbx egress (MTX ... 1) of each, and the talker's answer to each:
    the log a firmware that sent no PROBE_TX for those binds leaves."""
    acmp_tx = [i for i, ln in enumerate(lines) if ln.startswith('TXW') and frame(ln)[14:15] == b'\xfc'
               and frame(ln)[12:14] == b'\x22\xf0']
    txc = [i for i, ln in enumerate(lines) if ln.startswith('TXC') and ln.split()[2] == '1']
    mtx = [i for i, ln in enumerate(lines) if ln.startswith('MTX') and ln.split()[3] == '1']
    assert len(acmp_tx) == len(txc) == len(mtx), (len(acmp_tx), len(txc), len(mtx))
    gone, seqs, k = set(), set(), 0
    for n, i in enumerate(acmp_tx):
        if is_acmp(lines[i], g.PROBE_TX, 'TXW'):
            if k not in keep:
                gone |= {i, txc[n], mtx[n]}
                seqs.add(acmp_seq(lines[i]))
            k += 1
    for i, ln in enumerate(lines):
        if is_acmp(ln, g.PROBE_TX_RESPONSE, 'RXW') and acmp_seq(ln) in seqs:
            gone.add(i)
    return [ln for i, ln in enumerate(lines) if i not in gone], k


def patch_status(lines, pick, status):
    """The selected TX frame with its AVTP control status set (byte 16, bits 7:3)."""
    out, done = [], 0
    for ln in lines:
        if not done and pick(ln):
            w = ln.split()
            d = bytearray(bytes.fromhex(w[4]))
            d[16] = (d[16] & 0x07) | (status << 3)
            w[4] = d.hex()
            ln = ' '.join(w)
            done = 1
        out.append(ln)
    assert done
    return out


def main():
    real = open(sys.argv[2]).read()
    published = json.load(open(sys.argv[3]))
    real8 = open(sys.argv[4]).read()
    published8 = json.load(open(sys.argv[5]))
    lines = real.splitlines()

    r, f = outcome(real)
    print('R0 regrade ci-1x1-none at head:', len(f), 'finding(s);',
          'results identical to published' if dict(r, findings=f) == published else 'RESULTS DIFFER')
    r, f = outcome(real8, interfaces=2)
    print('R0 regrade 8x8-none at head:', len(f), 'finding(s);',
          'results identical to published' if dict(r, findings=f) == published8 else 'RESULTS DIFFER')

    mutated, total = drop_probes(lines, keep=set(range(16)) - {5})
    r, f = outcome('\n'.join(mutated) + '\n')
    n = {row['path']: row['n'] for row in r['rows']} if r else {}
    print(f'R1 one of {total} PROBE_TXs (draw 5) never sent, nor answered: {len(f)} finding(s) {f[:2]}; '
          f"acmp.probe_tx N={n.get('acmp.probe_tx')}, acmp.bind_rx N={n.get('acmp.bind_rx')}")

    mutated, total = drop_probes(lines, keep={total - 1 if total else 15})
    r, f = outcome('\n'.join(mutated) + '\n')
    n = {row['path']: row['n'] for row in r['rows']} if r else {}
    print(f'R2 only the last of {total} PROBE_TXs sent (15 binds cause none): {len(f)} finding(s) {f[:2]}; '
          f"acmp.probe_tx N={n.get('acmp.probe_tx')}")

    mutated, total = drop_probes(lines, keep=set())
    r, f = outcome('\n'.join(mutated) + '\n')
    print(f'R3 control: no PROBE_TX at all: {len(f)} finding(s), first {f[:1]}')

    mutated = patch_status(lines, lambda ln: is_acmp(ln, g.BIND_RX_RESPONSE, 'TXW'), 1)
    r, f = outcome('\n'.join(mutated) + '\n')
    print(f'R4 first BIND_RX_RESPONSE with status 1 (LISTENER_UNKNOWN_ID): {len(f)} finding(s) {f[:2]}')

    def aecp_resp(ln):
        if not ln.startswith('TXW'):
            return False
        d = frame(ln)
        return d[12:14] == b'\x22\xf0' and d[14] == 0xFB and (d[15] & 0x0F) in (1, 7)
    mutated = patch_status(lines, aecp_resp, 1)
    r, f = outcome('\n'.join(mutated) + '\n')
    print(f'R5 first AECP response with status 1 (NOT_IMPLEMENTED): {len(f)} finding(s) {f[:2]}')


if __name__ == '__main__':
    main()
