#!/usr/bin/env python3
"""#773 item 1: the AAF talker's capture-to-wire latency per shape, from the
stamped media instant M (the PDU's first frame's start at the media
interface, milan_datapath aaf_tbase_w) to the PDU's hand-over at the
datapath's MAC TX port (m_axis_mac_tx), each term named after the RTL that
sets it. Formulas restate the RTL at dev a032c6d6; shape parameters are the
builder's (configs/endstation_ax7101_*.yaml, the generated adp_shape_defaults).

Prints a markdown table per shape and the CRF output's path for item 4."""
from fractions import Fraction as F

NS = 10**9
FS = 48_000
PS = F(NS, FS)                      # one media clock period, 62500/3 ns


def cyc_ns(n, hz):                  # KL_media_if_latency_pkg::cyc_ns
    return (n * NS + hz // 2) // hz


def half_cyc_ns(h, hz):             # KL_media_if_latency_pkg::half_cyc_ns
    return (h * NS + hz) // (2 * hz)


def pair_end_bits(k, word_bits, dd):  # KL_media_if_latency_pkg::pair_end_bits
    return 2 * (k + 1) * word_bits + dd - 1


SHAPES = {
    # name: axis clock, TDM slots, front-end write clock (TDM master: clk_tdm_i),
    # streams, wire channels, loopback lane (LOOPBACK_P), rx wire chans (8)
    "1x1 (TDM8 master, 50 MHz)": dict(axis=50_000_000, slots=8, wr_hz=24_576_000,
                                      streams=1, chans=8, loopback=1),
    "8x8 (TDM32 master on 98.304 MHz, 50 MHz)": dict(axis=50_000_000, slots=32, wr_hz=98_304_000,
                                                     streams=8, chans=8, loopback=0),
}

SAMPLES_PER_PDU = 6                 # KL_aaf_packetizer SAMPLES_PER_FRAME_C
WORD_BITS = 32
DATA_DELAY = 1                      # every capture front end of the root
GAP_CYC = 24                        # KL_chan_map_capture GAP_CYC_P (default, not overridden)
RX_WIRE_CHANS = 8                   # milan_datapath RX_WIRE_CHANS_C
CMAP_TDM_SLOTS = 8                  # milan_datapath CMAP_TDM_SLOTS_C
KEEPOFF_CAP = 256                   # milan_datapath MGA_KEEPOFF_CYC_C cap


def shape_terms(p):
    axis = p["axis"]
    cyc = F(NS, axis)
    aif_pairs = p["slots"] // 2
    frame_pairs = min(aif_pairs, CMAP_TDM_SLOTS // 2)            # CMAP_TDM_FRAME_PAIRS_C
    close_pair = frame_pairs - 1                                  # close_pair()
    bclk = p["slots"] * WORD_BITS * FS                            # AIF_BCLK_HZ_C
    bits = pair_end_bits(close_pair, WORD_BITS, DATA_DELAY)
    mark = cyc_ns(bits, bclk) + cyc_ns(1, p["wr_hz"]) + half_cyc_ns(9, axis)  # DOM_MARK_LAT_NS_C
    div = axis // FS                                              # MGA_SAMPLE_CYC_C
    keep = min(div // 4, KEEPOFF_CAP)                             # MGA_KEEPOFF_CYC_C
    age_lo, age_hi = keep, div - keep                             # settled lock band, cycles
    lb_streams = p["streams"] if p["loopback"] else 1             # LB_STREAMS_C
    lb_ch = RX_WIRE_CHANS if p["loopback"] else 2                 # LB_CH_C
    lb_pairs = lb_streams * max(1, lb_ch // 2)                    # LB_PAIRS_C
    pairs_per_talker = p["chans"] // 2
    np = SAMPLES_PER_PDU * pairs_per_talker                       # packetizer np_w
    ebeats = np + 6                                               # ebeats_w
    rows = []
    for t in range(p["streams"]):
        slot = (t + 1) * pairs_per_talker - 1                     # talker t's last pair slot
        walk = 4 + lb_pairs + slot * (GAP_CYC + 2)                # tick -> that pair at the packetizer
        crd = 0 if t == 0 else 3                                  # E_CRD_S for t > 0
        first = 4 + crd + np                                      # pend, grant, fetch .. first SEND beat
        last = first + ebeats - 1
        rows.append((t, slot, walk, first, last))
    return dict(cyc=cyc, frame_pairs=frame_pairs, close_pair=close_pair, bclk=bclk, bits=bits,
                mark=mark, div=div, keep=keep, age=(age_lo, age_hi), lb_pairs=lb_pairs, np=np,
                ebeats=ebeats, rows=rows)


def fmt(x):
    return f"{float(x):,.1f}"


def main():
    later = (SAMPLES_PER_PDU - 1) * PS
    print("# #773 item 1: AAF capture-to-wire latency per shape (derived)\n")
    print(f"Ps = 1e9/{FS} = {fmt(PS)} ns. Term A, the PDU's later frames: "
          f"(SAMPLES_PER_FRAME_C - 1) x Ps = {SAMPLES_PER_PDU - 1} x Ps = {fmt(later)} ns.\n")
    for name, p in SHAPES.items():
        d = shape_terms(p)
        c = d["cyc"]
        print(f"## {name}\n")
        print(f"- B, marker latency (DOM_MARK_LAT_NS_C): closing pair {d['close_pair']} of {d['frame_pairs']}, "
              f"{d['bits']} bit periods at {d['bclk']:,} Hz = {cyc_ns(d['bits'], d['bclk']):,} ns, + 1 write cycle at "
              f"{p['wr_hz']:,} Hz = {cyc_ns(1, p['wr_hz'])} ns, + 4.5 read cycles = {half_cyc_ns(9, p['axis'])} ns: "
              f"**{d['mark']:,} ns**")
        print(f"- C, capture age (close -> the walk's snapshot tick): aligner lock band "
              f"[{d['age'][0]}, {d['age'][1]}] cycles (keep-off {d['keep']} of a {d['div']}-cycle tick) = "
              f"{fmt(d['age'][0] * c)}..{fmt(d['age'][1] * c)} ns at a settled lock; 0..{d['div'] + 1} cycles "
              f"before one")
        print(f"- D, walk: tick -> talker t's last pair = 4 + LB_PAIRS_C ({d['lb_pairs']}) + slot x "
              f"(GAP_CYC_P + 2 = {GAP_CYC + 2}) cycles")
        print(f"- E, packetizer: last pair -> first SEND beat = 4 (+3 CRD for t > 0) + np ({d['np']}) cycles; "
              f"{d['ebeats']} beats to tlast")
        print("- F, arbiters (crf_dp_mux, adp_tx_mux): combinational, 0 cycles when no other frame is in flight "
              "and the MAC is ready\n")
        print("| talker | last slot | A + B ns | D walk cyc | E first/last beat cyc | "
              "hand-over (last beat) - M, age min .. max ns | first beat - M, age min ns |")
        print("|---:|---:|---:|---:|---:|---:|---:|")
        lo_all, hi_all = None, None
        for t, slot, walk, first, last in d["rows"]:
            ab = later + d["mark"]
            lo = ab + (d["age"][0] + walk + last) * c
            hi = ab + (d["age"][1] + walk + last) * c
            fl = ab + (d["age"][0] + walk + first) * c
            lo_all = lo if lo_all is None else min(lo_all, lo)
            hi_all = hi if hi_all is None else max(hi_all, hi)
            print(f"| {t} | {slot} | {fmt(ab)} | {walk} | {first} / {last} | {fmt(lo)} .. {fmt(hi)} | {fmt(fl)} |")
        unlocked = later + d["mark"] + (d["div"] + 1 + d["rows"][-1][2] + d["rows"][-1][4]) * c
        print(f"\nShape range at a settled lock, no interference: **{fmt(lo_all)} .. {fmt(hi_all)} ns**; "
              f"before a lock (age up to {d['div'] + 1} cycles), last talker: {fmt(unlocked)} ns. "
              f"Over 125,000 ns by {fmt(lo_all - 125000)} .. {fmt(hi_all - 125000)} ns.\n")
        k = -(-hi_all // PS)
        print(f"Whole media periods covering the settled-lock maximum: ceil({fmt(hi_all)} / Ps) = {k} periods = "
              f"{fmt(k * PS)} ns.\n")
        # item 4: the CRF output's own path, from its stamped event (KL_crf_tx)
        crf_first, crf_last = d["mark"] + 3 * c, d["mark"] + 10 * c
        print(f"CRF output: hand-over - its stamped event = marker latency + 3 (first beat) .. 10 (last beat) "
              f"cycles = {fmt(crf_first)} .. {fmt(crf_last)} ns, plus any AAF PDU in flight at crf_dp_mux "
              f"(up to {d['ebeats']} beats = {fmt(d['ebeats'] * c)} ns) and any control frame at adp_tx_mux.\n")
    print("## CRF Equation (14) at the two offsets\n")
    for off in (125_000, 2_000_000):
        per = -(-(off * 3) // 62_500)
        rnd = -(-(per * 62_500) // 3)
        print(f"- TTmax = {off:,} ns: ceil(TTmax / Ps) = {per} periods, applied {rnd:,} ns: round-up "
              f"{rnd - off} ns")


if __name__ == "__main__":
    main()
