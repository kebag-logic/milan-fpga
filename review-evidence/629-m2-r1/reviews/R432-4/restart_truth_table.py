#!/usr/bin/env python3
"""Reviewer probe: the restart request's truth table, clean and both veto forms.

Evaluates mcr_restart_p_w (hdl/milan/milan_datapath.sv at the head) over all
2^7 input combinations with SystemVerilog precedence (& binds tighter than |):
  clean   = (sel & ((tkd & ~lk) | ct)) | ad | at
  r4      = (sel & ((tkd & ~lk) | ct)) | ad | at & ~rb        (round 4's control)
  fixed   = (sel & ((tkd & ~lk) | ct) & ~rb) | ad | at        (round 4b's control)
and counts, on re-base cycles (rb = 1), which requests each veto suppresses.
"""
from itertools import product

crf_only = aaf_only = 0
sup_r4_crf = sup_r4_aaf = sup_fx_crf = sup_fx_aaf = 0
for sel, tkd, lk, ct, ad, at, rb in product((0, 1), repeat=7):
    crf = sel & ((tkd & (1 - lk)) | ct)
    aaf = ad | at
    clean = crf | aaf
    r4 = crf | ad | (at & (1 - rb))
    fixed = (crf & (1 - rb)) | aaf
    if not rb:
        assert r4 == clean and fixed == clean, "a veto changed a non-re-base cycle"
        continue
    if crf and not aaf:
        crf_only += 1
        sup_r4_crf += clean and not r4
        sup_fx_crf += clean and not fixed
    if aaf and not crf:
        aaf_only += 1
        sup_r4_aaf += clean and not r4
        sup_fx_aaf += clean and not fixed
print(f"re-base cycles: selected-CRF-only requests {crf_only}, AAF-only requests {aaf_only}")
print(f"round-4 form suppresses: CRF-only {sup_r4_crf}, AAF-only {sup_r4_aaf}")
print(f"round-4b form suppresses: CRF-only {sup_fx_crf}, AAF-only {sup_fx_aaf}")
ok = (crf_only, aaf_only, sup_r4_crf, sup_r4_aaf, sup_fx_crf, sup_fx_aaf) == (5, 33, 0, 11, 5, 0)
print("matches the PR body's 5 / 33 / 11 figures" if ok else "DOES NOT match the PR body")
raise SystemExit(0 if ok else 1)
