#!/usr/bin/env python3
"""Disposable probe: does the end-station builder's gptp loader refuse an
asymmetry key (the GPTP_PLANE record's "Can a configuration set it? No")?
Imports the builder read-only from the review clone given as argv[1]; writes
nothing (run with python3 -B). Each case prints ACCEPTED or REFUSED."""
import sys
sys.path.insert(0, sys.argv[1] + "/sw/builder")
import endstation_builder as eb  # noqa: E402

BASE = {"ingress_latency_ns": 0, "egress_latency_ns": 0}
cases = {
    "control: only the two REQ-PTP-06 keys": dict(BASE),
    "delay_asymmetry_ns": dict(BASE, delay_asymmetry_ns=256),
    "delayAsymmetry": dict(BASE, delayAsymmetry=256),
    "asymmetry_ns": dict(BASE, asymmetry_ns=-256),
}
for name, gp in cases.items():
    try:
        eb._load_gptp({"gptp": gp})
        print(f"{name}: ACCEPTED")
    except eb.ConfigError as e:
        print(f"{name}: REFUSED ({str(e)[:110]})")
    except Exception as e:  # anything past the key check is not a refusal
        print(f"{name}: PAST-KEY-CHECK {type(e).__name__}: {str(e)[:110]}")
