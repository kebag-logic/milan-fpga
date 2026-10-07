#!/usr/bin/env python3
"""Reviewer probe: run ctrl_image.py from ROOT with the lwSRP pin guard set to REV.
usage: size_probe.py ROOT REV -- <ctrl_image.py arguments>"""
import sys
root, rev = sys.argv[1], sys.argv[2]
sys.path[:0] = [f"{root}/sw/firmware/ctrl/test", f"{root}/sw/firmware/gtest"]
import ctrl_arms
ctrl_arms.LWSRP_REV = rev
import ctrl_image
sys.argv = ["ctrl_image.py", *sys.argv[4:]]
raise SystemExit(ctrl_image.main())
