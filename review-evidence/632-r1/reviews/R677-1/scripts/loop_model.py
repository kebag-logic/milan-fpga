#!/usr/bin/env python3
"""Linear per-window model of the KL_mmcm_drp_servo rate + phase loop (review probe).

Units: ns per 512 ms window for e, u and the integrator (1 unit = 1/512 ppm);
phase in ns. Per window n:
  e[n]     = f0 - u[n-1]                    (the trim applies over the next window)
  phi[n+1] = phi[n] + e[n]                  (a slow domain falls behind)
  Theta[n] = mean phase over window n ~ (phi[n] + phi[n+1]) / 2
  integ[n] = integ[n-1] + e[n]/2^KI + k * clamp(Theta[n-1])   (one window late)
  u[n]     = integ[n] + e[n]/2^KP
with k = 3 * 2^PH_GAIN_LSH_P / 256 (Theta in 1/3 ns, the integrator in 1/256).
Prints the closed-loop poles of the unclamped loop and a pull-in from Ps/2.
"""
import cmath
import sys

KI, KP, LSH = 1, 2, 1
k = 3 * (2 ** LSH) / 256.0
PS = 1e9 / 48000
CLAMP_NS = (256 * 128 >> LSH) / 3.0


def poly_roots(c):
    """Durand-Kerner roots of a monic polynomial given high-to-low coefficients."""
    n = len(c) - 1
    c = [x / c[0] for x in c]
    r = [complex(0.4, 0.9) ** i for i in range(n)]
    for _ in range(2000):
        nr = []
        for i in range(n):
            num = sum(c[j] * r[i] ** (n - j) for j in range(n + 1))
            den = 1
            for j in range(n):
                if j != i:
                    den *= (r[i] - r[j])
            nr.append(r[i] - num / den)
        r = nr
    return r


def poles():
    # z-domain: E = -z^-1 U ; Phi(z-1) = E ; Th = (1+z)/2 Phi ; I(1-z^-1) = E/2 + k z^-1 Th
    # U = I + E/4. Solve characteristic numerically by building the state machine
    # and computing its companion polynomial via impulse response (Berlekamp-free: use states).
    # States: phi, integ, u_prev, phi_prev. Simulate the linear map's matrix.
    import itertools
    def step(s):
        phi, integ, uprev, th_prev = s
        e = -uprev
        phi_n = phi + e
        th = 0.5 * (phi + phi_n)
        integ_n = integ + e / 2 ** KI + k * th_prev
        u = integ_n + e / 2 ** KP
        return (phi_n, integ_n, u, th)
    basis = [tuple(1.0 if i == j else 0.0 for i in range(4)) for j in range(4)]
    cols = [step(b) for b in basis]
    A = [[cols[j][i] for j in range(4)] for i in range(4)]
    # characteristic polynomial by Faddeev-LeVerrier
    n = 4
    import copy
    M = [[0.0] * n for _ in range(n)]
    coeffs = [1.0]
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for kk in range(1, n + 1):
        AM = [[sum(A[i][l] * M[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        M = [[AM[i][j] + coeffs[-1] * I[i][j] for j in range(n)] for i in range(n)]
        AM = [[sum(A[i][l] * M[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        ck = -sum(AM[i][i] for i in range(n)) / kk
        coeffs.append(ck)
    return poly_roots(coeffs), A


def pullin(phi0, f0=0.0, clamp=True, n=200):
    phi, integ, u, thp = phi0, f0, f0, phi0
    out = []
    for i in range(n):
        e = f0 - u
        phin = phi + e
        th = 0.5 * (phi + phin)
        thc = max(-CLAMP_NS, min(CLAMP_NS, thp)) if clamp else thp
        integ = integ + e / 2 ** KI + k * thc
        u = integ + e / 2 ** KP
        out.append((i, phin, e))
        phi, thp = phin, th
    return out


if __name__ == "__main__":
    r, A = poles()
    print("closed-loop poles (per 512 ms window):")
    for p in sorted(r, key=lambda z: -abs(z)):
        print(f"  {p.real:+.4f}{p.imag:+.4f}j  |p|={abs(p):.4f}")
    tr = pullin(PS / 2 * 0.98)
    for lim in (0.05 * PS,):
        first = next((i for i, ph, e in tr if all(abs(x[1]) < lim for x in tr[i:])), None)
        print(f"pull-in from 0.49 Ps: inside +/-5 % of Ps from window {first} ({first*0.512 if first is not None else float('nan'):.1f} s)")
    maxstep = max(abs(e) for i, ph, e in tr[6:])
    print(f"largest phase move per window after window 6: {maxstep:.1f} ns (slew target 256 ns)")
    over = min(ph for i, ph, e in tr)
    print(f"undershoot past zero: {over:.1f} ns")
