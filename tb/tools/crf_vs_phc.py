#!/usr/bin/env python3
"""Compare the AVTP timestamps our board puts on the wire (CRF, 64-bit gPTP ns)
against the domain gPTP time as held by this bench host's disciplined PHC.

Read-only: sniffs, reads /dev/ptpN.  Nothing is transmitted."""
import socket, struct, sys, time, os, argparse

ETH_P_ALL = 0x0003
ETHERTYPE_AVTP = 0x22F0


def phc_clockid(fd: int) -> int:
    """The POSIX clock id for an already-open PHC character device."""
    return (~fd << 3) | 3


def strip_vlan(pkt: bytes) -> tuple[bytes, bytes, int, bytes]:
    """(dst, src, ethertype, payload) with any stack of VLAN tags peeled off."""
    et = struct.unpack('!H', pkt[12:14])[0]
    off = 14
    while et in (0x8100, 0x88A8):
        et = struct.unpack('!H', pkt[off + 2:off + 4])[0]
        off += 4
    return pkt[0:6], pkt[6:12], et, pkt[off:]


def main() -> None:
    """Print each CRF frame's timestamp beside the PHC reading and their gap."""
    ap = argparse.ArgumentParser()
    ap.add_argument('--iface', default='enp6s0')
    ap.add_argument('--phc', default='/dev/ptp0')
    ap.add_argument('--src', default='02:00:00:00:00:01')
    ap.add_argument('--n', type=int, default=13)
    ap.add_argument('--gap', type=float, default=5.0)
    a = ap.parse_args()

    src = bytes.fromhex(a.src.replace(':', ''))
    fd = os.open(a.phc, os.O_RDWR)
    cid = phc_clockid(fd)

    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
    s.bind((a.iface, 0))
    # PACKET_MR_PROMISC so the NIC delivers the stream multicast groups too
    idx = socket.if_nametoindex(a.iface)
    s.setsockopt(263, 1, struct.pack('IHH8s', idx, 1, 0, b''))
    s.settimeout(3.0)

    print('# iso  phc_ns  crf_ts_ns  (crf-phc)_ns  seq  base_freq  ts_interval')
    prev = None
    for i in range(a.n):
        # 1) drain the whole socket backlog so we are not reading stale frames
        s.setblocking(False)
        while True:
            try:
                s.recv(2048)
            except BlockingIOError:
                break
            except socket.timeout:
                break
        # 2) now block for the NEXT (freshest) CRF frame
        s.setblocking(True)
        s.settimeout(3.0)
        got = None
        end = time.time() + 3.0
        while time.time() < end:
            try:
                pkt = s.recv(2048)
            except socket.timeout:
                break
            d, sr, et, p = strip_vlan(pkt)
            if et != ETHERTYPE_AVTP or sr != src or len(p) < 28:
                continue
            if p[0] != 0x04:            # CRF
                continue
            got = p
            break
        # read the PHC as close to the frame as possible
        phc = time.clock_gettime_ns(cid)
        if got is None:
            print('%s  no CRF frame seen' % time.strftime('%H:%M:%S'))
        else:
            seq = got[2]
            sid = struct.unpack('!Q', got[4:12])[0]
            bf = struct.unpack('!I', got[12:16])[0] & 0x1FFFFFFF
            cdl = struct.unpack('!H', got[16:18])[0]
            ti = struct.unpack('!H', got[18:20])[0]
            ts = struct.unpack('!Q', got[20:28])[0]
            delta = ts - phc
            print('%s  phc=%d  crf=%d  delta=%+d ns (%+0.6f s)  seq=%d sid=%016X '
                  'bf=%d int=%d cdl=%d'
                  % (time.strftime('%H:%M:%S'), phc, ts, delta, delta / 1e9,
                     seq, sid, bf, ti, cdl))
            if prev is not None:
                print('        d(delta)=%+d ns over %0.1f s' % (delta - prev, a.gap))
            prev = delta
        sys.stdout.flush()
        if i < a.n - 1:
            time.sleep(a.gap)
    os.close(fd)


if __name__ == '__main__':
    main()
