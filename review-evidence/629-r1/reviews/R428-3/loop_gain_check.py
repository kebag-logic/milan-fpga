#!/usr/bin/env python3
"""Reviewer check of the #629 design's E8 closed-loop bound (PR #631, head a463a1de).

Independent of the author's model. Derives, from KL_mmcm_drp_servo.sv's PI as
written (integ += e >>> 1; u = integ + e >>> 2; e = locerr - rate; the trim u
moves locerr one window later with plant gain g), the transfer from the
per-snapshot pick error eps_k (|eps_k| <= J) to the servo's window error e_k
for an N-window two-point estimator rate_k = true + (eps_k - eps_{k-N}) / N.

  S(z)   = (1 - z^-1) / (1 - (1 - 3g/4) z^-1 - (g/4) z^-2)   (sensitivity)
  H_N(z) = -S(z) (1 - z^-N) / N

The worst |e| over every eps sequence bounded by J is J * ||H_N||_1, attained
by eps_k = J * sign of the time-reversed impulse response. The script also
checks the indistinguishability bound: any rate estimator over a span T sees
the same data for (rate r, phase ramp -J..+J) and (rate r + 2J/T, no error).
Standard library only. Usage: python3 loop_gain_check.py
"""


def impulse(n_est, g=1.0, taps=4000, est=True):
    integ = u = 0.0
    hist = [0.0] * (n_est + 1)
    out = []
    for k in range(taps):
        x = 1.0 if k == 0 else 0.0
        if est:
            hist = hist[1:] + [x]
            d = (hist[-1] - hist[0]) / n_est
        else:
            d = x
        e = -g * u - d
        integ += e / 2
        u = integ + e / 4
        out.append(e)
    return out


def poles(g):
    # 1 - a z^-1 - b z^-2, a = 1 - 3g/4, b = -g/4 -> z^2 - a z - b
    import cmath
    a, b = 1 - 0.75 * g, -0.25 * g
    disc = cmath.sqrt(a * a + 4 * b)
    return [(a + disc) / 2, (a - disc) / 2]


def main():
    s = impulse(1, est=False)
    print(f"sensitivity S impulse first taps (g=1): "
          f"{[round(x, 5) for x in s[:6]]}")
    print(f"||S||_1 (g=1) = {sum(abs(x) for x in s):.4f}")
    for g in (0.5, 0.8, 1.0, 1.2, 1.5):
        p = poles(g)
        print(f"g={g:3.1f} poles |z| = {abs(p[0]):.4f}, {abs(p[1]):.4f}; "
              f"||S||_1 = {sum(abs(x) for x in impulse(1, g, est=False)):.4f}")
    print()
    print("N  g    open 2/N  closed ||H_N||_1  J=1042   J=1426   J=1748")
    for g in (0.8, 1.0, 1.2):
        for n in (1, 2, 4, 6, 8, 16):
            h = impulse(n, g)
            l1 = sum(abs(x) for x in h)
            print(f"{n:<2d} {g:3.1f}  {2 / n:7.4f}  {l1:14.4f}   "
                  f"{1042 * l1:6.0f}   {1426 * l1:6.0f}   {1748 * l1:6.0f}")
    print()
    for j in (1042, 1426):
        for t_ms in (512, 2048, 4096):
            print(f"ramp bound 2J/T: J={j} T={t_ms} ms -> "
                  f"{2 * j / (t_ms * 1e-3) / 1e3:.3f} ppm = "
                  f"{2 * j / (t_ms / 512):.0f} ns per 512 ms window "
                  f"(lock threshold 1,024 ns = 2 ppm)")
    # The interval of rates consistent with error-free data of slope s is
    # [s - 2J/T, s + 2J/T]: any estimator is off by >= 2J/T somewhere.
    print("indistinguishability: for every estimator the worst case over a "
          "span T is >= 2J/T (half the width 4J/T of the consistent set)")


if __name__ == "__main__":
    main()
