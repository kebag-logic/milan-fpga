#!/usr/bin/env python3
"""Check KL_mmcm_drp_servo's tracking unwrap (head 2ff30f0d) against its spec.

Model of the RTL at hdl/ieee1722/crf/KL_mmcm_drp_servo.sv (ph_ref_up_w,
ph_edge_w, ph_wrap_w, ph_unw_w) in exact integers with the RTL widths:
PH_TW_C = 16 (signed), edge PH_TW_C+1 bits, unwrapped PH_UW_C = 18 bits.
Spec: for every reference r and folded sample f in [-H, H), the unwrapped u
satisfies u == f (mod Ps) and r - H <= u < r + H. Also checks the window
re-fold (ph_wmean_w) maps any raw mean in [-(33/32)Ps, (33/32)Ps] into [-H, H)
congruently. Exhaustive over f for every r (vectorised).
"""
import sys
import numpy as np

PS = 62500
H = PS // 2

def wrap(v, bits):
    m = 1 << bits
    v = np.asarray(v, dtype=np.int64) & (m - 1)
    return np.where(v >= m // 2, v - m, v)

f = np.arange(-H, H, dtype=np.int64)
bad = 0
for r in range(-H, H):
    up = r >= 0
    edge = wrap(r - H if up else r + H, 17)
    fw = wrap(f, 17)
    wr = (fw < edge) if up else (fw >= edge)
    u = np.where(~wr, wrap(f, 18), wrap(wrap(f, 18) + (PS if up else -PS), 18))
    ok = ((u - f) % PS == 0) & (u >= r - H) & (u < r + H)
    bad += int((~ok).sum())
print(f"unwrap: refs {2*H} samples {2*H} violations {bad}")

raw = np.arange(-(33 * PS) // 32 - 1, (33 * PS) // 32 + 2, dtype=np.int64)
rw = wrap(raw, 18)
m = np.where(rw >= H, wrap(rw - PS, 16), np.where(rw < -H, wrap(rw + PS, 16), wrap(rw, 16)))
ok2 = ((m - raw) % PS == 0) & (m >= -H) & (m < H)
bad2 = int((~ok2).sum())
print(f"refold: raw means {raw.size} violations {bad2}")
sys.exit(1 if bad or bad2 else 0)
