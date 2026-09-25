#!/usr/bin/env python3
"""Reviewer probe: non-integer / boolean / boundary declaration values.
usage: probe-robustness.py <tree>. Prints accept/refuse and, when accepted,
the generated VID/offset header lines, for each case."""
import copy, pathlib, re, sys, tempfile, yaml
tree = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
base = yaml.safe_load((tree / "configs/endstation_arty_current.yaml").read_text())
def srp(**kv):
    return lambda c: c.setdefault("srp", {}).update(kv)
def talker(v):
    return lambda c: c["streams"]["talkers"][0].update(presentation_time_offset_ns=v)
cases = [
    ("srp.vid 2.0 (float)", srp(vid=2.0)),
    ("srp.vid True", srp(vid=True)),
    ("srp.vid '2' (string)", srp(vid="2")),
    ("srp.vid 0x002 (int 2)", srp(vid=0x002)),
    ("srp.bandwidth_limit_pct 75.0", srp(bandwidth_limit_pct=75.0)),
    ("srp.bandwidth_limit_pct 75", srp(bandwidth_limit_pct=75)),
    ("srp.bandwidth_limit_pct 1", srp(bandwidth_limit_pct=1)),
    ("srp.timers_ms.leave 5000.0", lambda c: c["srp"].setdefault("timers_ms", {}).update(leave=5000.0)),
    ("srp.tspec.max_frame_bytes True", lambda c: c["srp"].setdefault("tspec", {}).update(max_frame_bytes=True)),
    ("srp.class_queue True", srp(class_queue=True)),
    ("talker offset 2000000.0", talker(2000000.0)),
    ("talker offset '2000000'", talker("2000000")),
    ("talker offset None", talker(None)),
    ("crf_output offset with enabled false, 1000000",
     lambda c: c.setdefault("clocking", {}).setdefault("crf_output", {}).update(enabled=False, presentation_time_offset_ns=1000000)),
    ("platform.rx_address_filter 'PROMISCUOUS'", lambda c: c["platform"].update(rx_address_filter="PROMISCUOUS")),
]
with tempfile.TemporaryDirectory() as tmp:
    for label, change in cases:
        raw = copy.deepcopy(base); change(raw)
        path = pathlib.Path(tmp) / "case.yaml"; path.write_text(yaml.safe_dump(raw))
        try:
            cfg = eb.load_config(path)
        except eb.ConfigError as exc:
            print(f"REFUSE  {label}: {str(exc)[:150]}")
            continue
        except Exception as exc:
            print(f"CRASH   {label}: {type(exc).__name__}: {exc}")
            continue
        hdr = eb.emit_adp_shape_svh(cfg)
        lines = [l.strip() for l in hdr.splitlines() if re.search(r"ADP_SRP_DOM_DEF_VID_C|ADP_STROUT_PRES_NS_C", l)]
        csr = [l.strip() for l in eb.emit_csr_defaults_svh(cfg).splitlines() if "LWSRP_VID_RST_C" in l and "localparam" in l]
        print(f"ACCEPT  {label}: {lines} {csr}")
