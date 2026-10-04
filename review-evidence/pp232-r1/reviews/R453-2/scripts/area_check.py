#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Internal-consistency check of the Vivado figures QUOTED in the published PR body
and handoff (milan-fpga review-evidence/pp232-r1 at ed9f5f46). The raw Vivado
reports are not published, so this re-derives only what the quoted numbers imply;
it cannot confirm the numbers themselves.
"""
ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok &= good
    print(f"{'OK  ' if good else 'BAD '} {label}: derived {got}, quoted {want}")


# round 1b integrated route, main 5c71928a vs head 6e950fea (HANDOFF R1b.6)
main = dict(lut=51434, lut_logic=49158, lut_mem=2276, ff=59691, slice=15847, carry=3526, wns=0.079, whs=0.014)
head = dict(lut=50671, lut_logic=47533, lut_mem=3138, ff=57660, slice=15841, carry=3376, wns=0.274, whs=0.023)
check("main LUT = logic + memory", main["lut_logic"] + main["lut_mem"], main["lut"])
check("head LUT = logic + memory", head["lut_logic"] + head["lut_mem"], head["lut"])
check("route LUT delta", head["lut"] - main["lut"], -763)
check("route FF delta", head["ff"] - main["ff"], -2031)
check("route slice delta", head["slice"] - main["slice"], -6)
check("route CARRY4 delta", head["carry"] - main["carry"], -150)
check("route WNS delta (ps)", round((head["wns"] - main["wns"]) * 1000), 195)
check("route logic/memory delta", (head["lut_logic"] - main["lut_logic"], head["lut_mem"] - main["lut_mem"]), (-1625, 862))
# u_notify in the routed hierarchy
check("u_notify LUT delta", 2343 - 3270, -927)
check("u_notify FF delta", 1287 - 3299, -2012)
check("u_notify LUTRAM delta", 960 - 96, 864)
# head u_notify LUTRAM composition (HANDOFF section 4, 1x1 cells)
check("LUTRAM = 288 RAM64X1D*2 + 16 RAM32X1D*2 + 88 RAM32M*4", 288 * 2 + 16 * 2 + 88 * 4, 960)
check("RAM32M = rows_r 64 + cmdq 24", 64 + 24, 88)
check("rows_r RAM32M count = 128 bits / 2 bits per RAM32M", 128 // 2, 64)
check("main u_notify LUTRAM = cmdq 24 RAM32M * 4", 24 * 4, 96)
check("index memories = 16 rows x 19 chunks", 16 * 19, 288 + 16)
check("rows_r flops at main = 16 x 128", 16 * 128, 2048)
# #638 gate cross-figures
check("head vs A = main vs A + head vs main (LUT)", 1306 + (-763), 543)
check("u_notify vs A = main vs A + delta (LUT)", 135 + (-927), -792)
# round 1 and standalone
check("round 1 route LUT delta", 50090 - 50740, -650)
check("round 1 route FF delta", 57681 - 59631, -1950)
check("1x1 LUT delta", 23600 - 24494, -894)
check("1x1 FF delta", 23429 - 25471, -2042)
check("8x8 LUT delta", 30458 - 31383, -925)
check("8x8 FF delta", 31793 - 33968, -2175)
check("1x1 u_notify LUT delta", 2261 - 3194, -933)
check("1x1 u_notify FF delta", 1253 - 3299, -2046)
check("8x8 u_notify FF delta", 1753 - 3799, -2046)
check("stamps 1x1 = (2+2+2) x 32", 6 * 32, 192)
check("stamps 8x8 figure = 20 x 32 (9+9+2 descriptors)", 20 * 32, 640)
print("ALL CONSISTENT" if ok else "INCONSISTENT")
raise SystemExit(0 if ok else 1)
