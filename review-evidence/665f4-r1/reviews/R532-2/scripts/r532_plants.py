#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned planted defects in srp_mbx.c (lifecycle and shared-binding
reconciliation), each run against the lane's own srp_mbx.cpp suite at two
interfaces, in a copied tree. usage: r532_plants.py REPO OUT [--jobs N]"""
import shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
probe = Path(__file__).resolve().parent / "srp_probe.py"
PLANTS = [
 # lifecycle
 ("L1-reset-keeps-owed-domain", "i->msrp = NULL; i->mvrp = NULL; i->domain_owed = false;\n    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {\n        i->sinks[k].desired = 0; i->sinks[k].declared = 0;",
  "i->msrp = NULL; i->mvrp = NULL;\n    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {\n        i->sinks[k].desired = 0; i->sinks[k].declared = 0;"),
 ("L2-reset-keeps-sink-declared", "i->sinks[k].desired = 0; i->sinks[k].declared = 0;\n        i->sinks[k].vlan_requested", "i->sinks[k].desired = 0;\n        i->sinks[k].vlan_requested"),
 ("L3-reset-keeps-sink-vlan", "i->sinks[k].vlan_requested = false; i->sinks[k].vlan_sent = false;\n    }\n    if (!open_interface(i)) {\n        ++m->refused;\n    }\n}",
  "(void)k;\n    }\n    if (!open_interface(i)) {\n        ++m->refused;\n    }\n}"),
 ("L4-down-event-keeps-link", "i->link = event->link_up;", "i->link = event->link_up || i->link;"),
 ("L5-link-seen-never-set", "i->link_seen = true;\n        i->link = event->link_up;", "i->link = event->link_up;"),
 ("L6-reset-silent-licence", "++m->stops;\n            m->config.licence(m->config.ctx,i->index,k,false);\n        }\n        i->stop_owed[k] = false;",
  "++m->stops;\n        }\n        i->stop_owed[k] = false;"),
 ("L7-reset-keeps-stop-owed", "        i->stop_owed[k] = false;\n    }\n    msrp_app_destroy", "    }\n    msrp_app_destroy"),
 ("L8-fence-mark-is-tail", "i->rx_mark = mbx_rx_mark(MBX_CH_SRP);", "i->rx_mark = (uint16_t)(mbx_rx_mark(MBX_CH_SRP) - 0x4000u);"),
 ("L9-stale-vlan-sent-across-reset", "    i->vlan_sent = false;\n    i->domain = (struct msrp_domain){6,3,2};", "    i->domain = (struct msrp_domain){6,3,2};"),
 # Milan / stop path
 ("M1-stop-owed-ignored", "            if (!i->registered[n] && i->active[n]) {\n                i->stop_owed[n] = true;", "            if (false) {\n                i->stop_owed[n] = true;"),
 ("M2-left-ignores-listener", "    if (type == MSRP_ATTR_TYPE_LISTENER) {\n        listener(ctx,port,value,MSRP_LISTENER_DECL_IGNORE,false);", "    if (type == 0xffu) {\n        listener(ctx,port,value,MSRP_LISTENER_DECL_IGNORE,false);"),
 # shared-binding reconciliation
 ("S1-each-binding-declares-alone", "handled = handled || other < k;", "handled = false;"),
 ("S2-handler-vlan-gates-all", "if (r->desired != 2 || r->vlan_sent)", "if (r->desired != 2 || s->vlan_sent)"),
 ("S3-only-handler-updated", "for (unsigned other = k; other < CTRL_SRP_SINKS; ++other) {\n                struct srp_sink *r = &i->sinks[other];\n                if (r->bound && memcmp(r->stream_id.bytes,s->stream_id.bytes,8) == 0) {\n                    r->declared = desired;",
  "for (unsigned other = k; other <= k; ++other) {\n                struct srp_sink *r = &i->sinks[other];\n                if (r->bound && memcmp(r->stream_id.bytes,s->stream_id.bytes,8) == 0) {\n                    r->declared = desired;"),
 ("S4-unbind-shares-by-vid", "if (!another_sink(i,sink,s,true)) {", "if (!another_sink(i,sink,s,false)) {"),
 ("S5-failed-does-not-dominate", "                    sink->desired = 1;\n                } else if (sink->desired != 1) {", "                    sink->desired |= 1;\n                } else {"),
 ("S6-rebind-same-stream-keeps-old-vid", "        if (s->vlan_requested && s->vid != i->domain.vid && !another_sink(i,sink,s,false)) {", "        if (false) {"),
]
def run(p):
    name, old, new = p
    w = out / name; src = w / "ctrl"
    shutil.rmtree(w, ignore_errors=True); shutil.copytree(repo / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__"))
    f = src / "srp/srp_mbx.c"; t = f.read_text()
    if t.count(old) != 1:
        return name, "BAD-SITE", t.count(old)
    f.write_text(t.replace(old, new))
    r = subprocess.run([sys.executable, str(probe), "--repo", str(repo), "--src", str(src), "--interfaces", "2",
                        "--test", str(repo / "sw/firmware/ctrl/test/srp_mbx.cpp"), "--out", str(w / "run")],
                       capture_output=True, text=True)
    (w / "run.log").write_text(r.stdout + r.stderr)
    failed = sorted({l.split()[3] for l in r.stdout.splitlines() if l.startswith("[  FAILED  ] Srp.")})
    if "error:" in r.stdout + r.stderr and not failed:
        return name, "BUILD-FAIL", []
    return name, "caught" if r.returncode else "ESCAPED", failed
with ThreadPoolExecutor(jobs) as ex:
    res = list(ex.map(run, PLANTS))
for n, v, f in res:
    print(f"{v:9s} {n}  {f}")
print(f"caught {sum(v=='caught' for _,v,_ in res)} / {len(res)}; escaped {sum(v=='ESCAPED' for _,v,_ in res)}")
