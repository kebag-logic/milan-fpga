#!/usr/bin/env python3
"""Independent model of the ADP first draw at the reviewed head.

Re-implements, from the source text (not by importing it), the adapter's seed
port (sw/firmware/ctrl/adp/adp_mbx.c port_seed, mix) and the stack core's
init, seed fold, xorshift32 step and draw (third_party/tsn-c-stack/src/adp.c
adp_init, adp_set_enable, rng_next, draw_ms), then measures the first draw's
spread over scenarios the host tests do not use:

  S1 EUI-64 entity IDs derived from consecutive MAC addresses (FR-DISC-05),
     all started at one clock sample (several entities powered up together);
  S2 the same with a small per-host boot jitter (0 to 63 us);
  S3 consecutive MAC addresses with a stride of 2 and of 256;
  S4 one entity, boots whose sample differs by 1 us, 1024 boots;
  S5 two interfaces of one entity at one sample (independence of the pair);
  S6 neighbouring pairs drawing within 5 ms of each other (the ruling's case).

Each spread is graded by Pearson's chi-square over 16 equal bins (99 %: 30.58
for 15 degrees of freedom), the same bound the host tests use, and by a
Kolmogorov-Smirnov distance against the continuous uniform law.
Usage: python3 -I draw_model.py  (stdlib only; exit 0 when every scenario passes)
"""
import sys

M32 = 0xFFFFFFFF
G = 0x9E3779B9
STARTUP_MAX = 2000
LINK_UP_MAX = 4000
CHI99 = 30.58


def mix(x):
    x = ((~x) + (x << 15)) & M32
    x ^= x >> 12
    x = (x + (x << 2)) & M32
    x ^= x >> 4
    x = (x + (x << 3) + (x << 11)) & M32
    return x ^ (x >> 16)


def port_seed(mac, entity_id, sample, interface):
    s = sample & M32
    total = ((mac & M32) + s) & M32
    total = (total + (1 if total < s else 0)) & M32
    return mix(mix(total) ^ (entity_id & M32) ^ ((entity_id >> 32) & M32) ^ ((interface << 24) & M32))


def core_rng(mac, entity_id, sample, interface):
    rng = (entity_id & M32) ^ ((entity_id >> 32) & M32) ^ G
    if rng == 0:
        rng = 1
    rng ^= port_seed(mac, entity_id, sample, interface)
    if rng == 0:
        rng = 1
    return rng


def step(x):
    x ^= (x << 13) & M32
    x ^= x >> 17
    x ^= (x << 5) & M32
    return x & M32


def draw(rng, max_ms):
    r16 = step(rng) >> 16
    return (r16 * (max_ms + 1)) >> 16


def chi(values, max_ms):
    bins = [0] * 16
    for v in values:
        bins[min(15, v * 16 // (max_ms + 1))] += 1
    e = len(values) / 16
    return sum((b - e) ** 2 / e for b in bins)


def ks(values, max_ms):
    xs = sorted(v / (max_ms + 1) for v in values)
    n = len(xs)
    return max(max((i + 1) / n - x, x - i / n) for i, x in enumerate(xs))


def eui64(mac):
    return ((mac >> 24) << 40) | (0xFFFE << 24) | (mac & 0xFFFFFF)


def grade(name, values, max_ms, out):
    c = chi(values, max_ms)
    d = ks(values, max_ms)
    ks99 = 1.628 / len(values) ** 0.5
    ok = c <= CHI99 and d <= ks99
    out.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} {name}: n={len(values)} chi2={c:.1f} (<= {CHI99}) "
          f"KS={d:.4f} (<= {ks99:.4f}) min={min(values)} max={max(values)} distinct={len(set(values))}")


def main():
    out = []
    base_mac = 0x001B21A40000
    sample = 1_853_117  # a boot-time microsecond reading; any fixed value
    for max_ms, kind in ((STARTUP_MAX, "startup"), (LINK_UP_MAX, "LINK_UP")):
        hosts = [(base_mac + k, eui64(base_mac + k)) for k in range(1024)]
        grade(f"S1 EUI-64 neighbours, one sample, {kind}",
              [draw(core_rng(m, e, sample, 0), max_ms) for m, e in hosts], max_ms, out)
        grade(f"S2 EUI-64 neighbours, jitter 0..63 us, {kind}",
              [draw(core_rng(m, e, sample + (k * 37) % 64, 0), max_ms) for k, (m, e) in enumerate(hosts)],
              max_ms, out)
        for stride in (2, 256):
            hs = [(base_mac + k * stride, eui64(base_mac + k * stride)) for k in range(1024)]
            grade(f"S3 stride {stride} neighbours, {kind}",
                  [draw(core_rng(m, e, sample, 0), max_ms) for m, e in hs], max_ms, out)
        grade(f"S4 one entity, boots 1 us apart, {kind}",
              [draw(core_rng(base_mac, eui64(base_mac), sample + k, 0), max_ms) for k in range(1024)], max_ms, out)
        # S5: interface 1 minus interface 0 for the same host, folded into the range: uniform if independent
        diffs = []
        for m, e in hosts:
            a = draw(core_rng(m, e, sample, 0), max_ms)
            b = draw(core_rng(m, e, sample, 1), max_ms)
            diffs.append((b - a) % (max_ms + 1))
        grade(f"S5 interface 1 against interface 0 (difference mod range), {kind}", diffs, max_ms, out)
        # S6: consecutive neighbours within 5 ms of each other
        vals = [draw(core_rng(m, e, sample, 0), max_ms) for m, e in hosts]
        close = sum(1 for a, b in zip(vals, vals[1:]) if abs(a - b) <= 5)
        expect = 1023 * 11 / (max_ms + 1)
        ok = close <= max(8, 3 * expect)
        out.append(ok)
        print(f"{'PASS' if ok else 'FAIL'} S6 consecutive neighbours within 5 ms, {kind}: {close} of 1023 "
              f"(independent draws expect about {expect:.1f})")
    # The pre-change seed, for contrast (NOW_MS alone, no host terms): neighbours at one ms reading.
    old = []
    for k in range(16):
        e = eui64(base_mac + k)
        rng = (e & M32) ^ (e >> 32) ^ G
        rng ^= 900
        old.append(draw(rng, LINK_UP_MAX))
    print(f"INFO contrast, the base seed (NOW_MS=900) for 16 EUI-64 neighbours: min {min(old)} max {max(old)} ms")
    print("RESULT:", "PASS" if all(out) else "FAIL", f"({sum(out)} of {len(out)})")
    return 0 if all(out) else 1


if __name__ == "__main__":
    sys.exit(main())
