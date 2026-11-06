#!/usr/bin/env python3
"""Force and drop every pass-through bit of the PHY init, and prove the start values matter.

Usage: phy_keep_matrix.py <clone root> <scratch dir> <json receipt>. The clone is only read.
"""
import json, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root, scratch, receipt = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
hosttest = root / "sw/firmware/nvm_hosttest"
sys.path.insert(0, str(hosttest))
sys.dont_write_bytecode = True
import test_phy_firmware as t
nvm = t.nvm

source = nvm.FENCE_RE.sub("(void)0;", nvm.FIRMWARE.read_text())
driver = (hosttest / "phy_host.c").read_text()
base = scratch / "base"
base.mkdir(parents=True)  # must be fresh: a kept generated/csr.h breaks the bench link
nvm.make_bench(root / "configs/endstation_ax7101_1x1_tdm8.yaml", base, nvm.FIRMWARE.read_text())
t.phy_csr(base)

def build_run(name, firmware, host):
    work = scratch / "v" / name
    work.mkdir(parents=True, exist_ok=True)
    (work / "milan_baremetal.c").write_text(firmware)
    (work / "phy_host.c").write_text(host)
    shutil.copy(hosttest / "phy_peer.h", work / "phy_peer.h")
    cmd = ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", "-Wno-format",
           "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
           f"-I{work}", f"-I{base}", f"-I{nvm.STUBS}", str(work / "phy_host.c"), "-o", str(work / "phy")]
    subprocess.run(cmd, check=True, timeout=180)
    r = subprocess.run([str(work / "phy")], capture_output=True, text=True, timeout=120)
    m = re.search(r"Assertion `(.+?)' failed", r.stderr)
    return {"name": name, "rc": r.returncode, "ok": "PHY_OK" in r.stdout,
            "assertion": m.group(1) if m else None}

def force(reg, bit):
    mask = f"0x{1 << bit:04x}u"
    if reg == 9:
        return source.replace(t.REGISTER_9_KEEP, f"{t.REGISTER_9_KEEP} {mask} |")
    value = t.REGISTER_4_VALUE if reg == 4 else t.REGISTER_0_VALUE
    assert source.count(value) == 1
    return source.replace(value, f"{mask} | ({value})")

def drop(reg, bit):
    mask = f"0x{1 << bit:04x}u"
    if reg == 9:
        return source.replace(t.REGISTER_9_KEEP, t.REGISTER_9_KEEP.replace("MASTER_SLAVE)", f"MASTER_SLAVE & ~{mask})"))
    value = t.REGISTER_4_VALUE if reg == 4 else t.REGISTER_0_VALUE
    return source.replace(value, value.replace("~(", f"~({mask} | "))

PASS_THROUGH = {4: [*range(0, 5), 10, 11, 12, 13, 15], 9: [10, 11, 12],
                0: [14, 13, 11, *range(0, 9)]}
GRADED = {4: {0, 1, 2, 3, 4, 10, 11}, 9: {10, 11, 12}, 0: {11, 14}}
jobs = [("baseline", source, driver)]
for reg, bits in PASS_THROUGH.items():
    for bit in bits:
        jobs.append((f"force-{reg}.{bit}", force(reg, bit), driver))
        jobs.append((f"drop-{reg}.{bit}", drop(reg, bit), driver))

def start(old, new):
    assert driver.count(old) == 1, old
    return driver.replace(old, new)

# Each start value undone in turn: the one mutant it alone exposes must then escape.
A1, A2 = "registers[0] = 0x9c00;", "registers[0] = 0x6100;"
necessity = [("arm1-power-down-clear", drop(0, 11), start(A1, "registers[0] = 0x9400;")),
             ("arm2-power-down-set", force(0, 11), start(A2, "registers[0] = 0x6900;")),
             ("arm1-loopback-set", force(0, 14), start(A1, "registers[0] = 0xdc00;")),
             ("arm2-loopback-clear", drop(0, 14), start(A2, "registers[0] = 0x2100;"))]
for name in ("power_down_kept", "loopback_kept"):
    bit = 11 if name == "power_down_kept" else 14
    gone = start(f"\tassert({name});\n", "")
    gone = gone.replace(f"const int {name} =", f"const int {name} __attribute__((unused)) =")
    necessity.append((f"no-assert-force-{name}", force(0, bit), gone))
    necessity.append((f"no-assert-drop-{name}", drop(0, bit), gone))
# A defect conditional on auto-negotiation enable: each bit's one informative state sits in one arm.
V0 = t.REGISTER_0_VALUE
AN = "(control & PHY_BMCR_AN_ENABLE)"
def conditional(on_value, off_value):
    return source.replace(V0, f"{AN} ? ({on_value}) : ({off_value})")
necessity += [("cond-drop-0.11-when-an-off", conditional(V0, f"({V0}) & ~0x0800u"), driver),
              ("cond-force-0.11-when-an-on", conditional(f"({V0}) | 0x0800u", V0), driver),
              ("cond-force-0.14-when-an-off", conditional(V0, f"({V0}) | 0x4000u"), driver),
              ("cond-drop-0.14-when-an-on", conditional(f"({V0}) & ~0x4000u", V0), driver)]
jobs += necessity

with ThreadPoolExecutor(16) as pool:
    results = list(pool.map(lambda j: build_run(*j), jobs))
by = {r["name"]: r for r in results}
assert by["baseline"]["ok"], by["baseline"]

escaped, caught, wrong = [], [], []
for reg, bits in PASS_THROUGH.items():
    for bit in bits:
        for kind in ("force", "drop"):
            r = by[f"{kind}-{reg}.{bit}"]
            (caught if r["rc"] else escaped).append(r["name"])
            if (bit in GRADED[reg]) != bool(r["rc"]):
                wrong.append(r)
summary = {"rows": len(caught) + len(escaped), "caught": len(caught), "escaped": len(escaped),
           "escaped_names": escaped, "disagrees_with_stated_bits": wrong,
           "caught_by": {n: by[n]["assertion"] for n in caught},
           "necessity": {j[0]: by[j[0]] for j in necessity}}
receipt.write_text(json.dumps(summary, indent=1) + "\n")
print(json.dumps({k: summary[k] for k in ("rows", "caught", "escaped", "escaped_names", "disagrees_with_stated_bits")}))
for name, r in summary["necessity"].items():
    print(name, "ESCAPED" if r["ok"] else f"caught by {r['assertion']}")
