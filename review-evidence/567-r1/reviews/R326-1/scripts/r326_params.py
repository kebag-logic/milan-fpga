#!/usr/bin/env python3
"""[R326] independent check: every parameter the parent binds on
protocol_processor_top is in the processor's documented inventory, and the
product values the parent supplies agree with that inventory's guidance.

Usage: r326_params.py <clone>
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
top_src = (root / "protocol-processor/hdl/top/protocol_processor_top.sv").read_text()
guide = (root / "protocol-processor/docs/guides/integrator.md").read_text()
shadow = (root / "hdl/milan/KL_pp_shadow.sv").read_text()
dp = (root / "hdl/milan/milan_datapath.sv").read_text()
shape = (root / "hdl/common/gen/adp_shape_defaults.svh").read_text()


def strip(text):
    return re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*.*?\*/', " ", text, flags=re.S)


def header(text, module):
    body = strip(text)
    m = re.search(r"\bmodule\s+%s\b.*?#\s*\(" % module, body, re.S)
    out, depth, buf = [], 0, []
    for ch in body[m.end():]:
        if ch == ")" and depth == 0:
            out.append("".join(buf))
            break
        if ch == "," and depth == 0:
            out.append("".join(buf)); buf = []; continue
        depth += ch in "([{"
        depth -= ch in ")]}"
        buf.append(ch)
    params, kind = {}, None
    for d in out:
        k = re.match(r"\s*(parameter|localparam)\b", d)
        if k:
            kind = k[1]
        n = re.search(r"\b([A-Za-z_]\w*)\s*=\s*(.*)$", d, re.S)
        if kind == "parameter" and n:
            params[n[1]] = " ".join(n[2].split())
    return params


def bindings(text, module):
    body = strip(text)
    m = re.search(r"^\s*%s\s*#\s*\((.*?)\)\s*\w+\s*\(\s*\.clk_i" % module, body, re.S | re.M)
    return dict(re.findall(r"\.(\w+)\s*\(\s*([^()]*?)\s*\)", m[1]))


top = header(top_src, "protocol_processor_top")
sec = re.search(r"^## 2\. Parameters\b.*?(?=^## |\Z)", guide, re.M | re.S)[0]
inv = []
for col in re.findall(r"^\|([^|]+)\|", sec, re.M):
    inv += re.findall(r"`([A-Za-z_]\w*)`", col)
pp_bind = bindings(shadow, "protocol_processor_top")
shadow_params = header(shadow, "KL_pp_shadow")
dp_bind = bindings(dp, "KL_pp_shadow")
dp_params = header(dp, "milan_datapath")

fail = 0
print(f"top parameters: {len(top)}; guide inventory rows: {len(inv)}")
if list(top) != inv:
    print("FAIL: guide inventory != top declaration order/set"); fail = 1
print(f"parent bindings on protocol_processor_top: {len(pp_bind)}")
for name, expr in pp_bind.items():
    ok = name in top and name in inv
    print(f"  {name:22s} <- {expr:22s} {'in-inventory' if ok else 'NOT IN INVENTORY'}")
    fail |= not ok
unbound = [n for n in top if n not in pp_bind]
print(f"unbound (processor default applies): {unbound}")

# product-value agreement for guidance-bearing parameters
def resolve(name):
    """Value the datapath hands KL_pp_shadow for `name`, else the shadow default."""
    if name in dp_bind:
        e = dp_bind[name]
        return e, dp_params.get(e, None)
    return None, shadow_params.get(name)

checks = []
e, v = resolve("SRP_DOM_DEF_VID_P")
m = re.search(r"%s\s*=\s*([^;]+);" % re.escape(e), shape)
checks.append(("SRP_DOM_DEF_VID_P keeps Milan value 2", m and m[1].strip() == "16'd2", f"{e} = {m and m[1].strip()}"))
e, v = resolve("TIM_DIV_US_P")
checks.append(("TIM_DIV_US_P is clock-derived in product", v == "MILAN_CLK_FREQ_HZ / 1_000_000", f"{e} = {v}"))
e, v = resolve("TIM_DIV_MS_P")
checks.append(("TIM_DIV_MS_P is 1000 in product", v == "1000", f"{e} = {v}"))
for n in ("REG_TL_TIMEOUT_MS_P", "LOCK_TIMEOUT_MS_P", "NVM_RS_TMO_CYC_P"):
    checks.append((f"{n} not shortened by parent", n not in pp_bind, f"default {top[n]}"))
for n in ("N_AUDIO_UNIT_P", "N_CLK_DOMAIN_P", "N_CONTROL_P"):
    checks.append((f"{n} unbound; default 1", n not in pp_bind and top[n] == "1", f"default {top[n]}"))
for lp in ("AEM_N_AUDIO_UNIT_C", "AEM_N_CLKDOM_C"):
    m = re.search(r"%s\s*=\s*([^;]+);" % lp, shape)
    checks.append((f"entity model {lp} equals processor default 1", m and m[1].strip() == "1", f"{lp} = {m and m[1].strip()}"))
for label, ok, detail in checks:
    print(f"  [{'OK' if ok else 'FAIL'}] {label}: {detail}")
    fail |= not ok
print("RESULT", "FAIL" if fail else "OK")
sys.exit(1 if fail else 0)
