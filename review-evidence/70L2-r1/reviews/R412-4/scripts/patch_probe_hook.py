#!/usr/bin/env python3
"""Insert a reviewer probe hook into a DISPOSABLE copy of sw/builder/test_builder.py.

Usage: patch_probe_hook.py <tree>

The hook runs inside gate 1b, right after the AEM-first base is accepted with
the slot kept and refused under forget-on-call, and before the planted-break
loop. When R412_PROBES names a JSON file it grades every probe there through
the same census_take() + assert_resolved_boot_flow(source=...) path the planted
breaks use, prints one PROBE line per probe with the resolver's outcome and the
relocations the -no-pie image places on aem_loaded's bytes, and exits.

Probe entry forms:
  ["name", "nvm", macro, statement]      in_nvm_boot(macro, statement)
  ["name", "sub", [[old, new], ...]]     replace_once() pairs on the base
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
path = tree / "sw/builder/test_builder.py"
text = path.read_text(encoding="utf-8")
anchor = "        for what, pins, planted, units in verdict_pin_breaks:\n"
assert text.count(anchor) == 1, "anchor not unique"
hook = '''        import json as _r412_json, os as _r412_os
        if _r412_os.environ.get("R412_PROBES"):
            for _probe in _r412_json.load(open(_r412_os.environ["R412_PROBES"])):
                _pname, _pkind = _probe[0], _probe[1]
                if _pkind == "nvm":
                    _planted = in_nvm_boot(_probe[2], _probe[3], _pname)
                else:
                    _planted = aem_first_source
                    for _old, _new in _probe[2]:
                        _planted = replace_once(_planted, _old, _new, _pname)
                try:
                    _pimage = verdict_image_take(_planted, _pname)
                    _pv = [s for s in _pimage["symbols"]
                           if s["name"] == "aem_loaded" and s["defined"]]
                    _pbytes = sorted(
                        (target - _pv[0]["value"], rv32_image_where(_pimage, site),
                         RV32_RELOCATION_NAMES.get(kind, str(kind)))
                        for site, kind, target in _pimage["relocations"]
                        if target is not None and len(_pv) == 1 and
                        0 <= target - _pv[0]["value"] < _pv[0]["size"])
                except BaseException as _pexc:  # noqa: BLE001
                    _pbytes = f"image not taken: {_pexc}"
                try:
                    _ptaken = census_take(_planted, _pname)
                    _pres = assert_resolved_boot_flow(
                        _ptaken["text"], source_model, _pname, source=_planted)
                except AssertionError as _pexc:
                    _msg = " ".join(str(_pexc).split())
                    print(f"PROBE {_pname}: REFUSED :: {_msg[:1600]}")
                except BaseException as _pexc:  # noqa: BLE001
                    print(f"PROBE {_pname}: ERROR :: {type(_pexc).__name__}: {_pexc}")
                else:
                    print(f"PROBE {_pname}: ACCEPTED kept={_pres.get('kept')}")
                try:
                    _playout = sorted((s["value"], s["size"], s["name"])
                                      for s in _pimage["symbols"]
                                      if s["name"] in ("aem_loaded", "milan_pre",
                                                       "milan_nbr", "milan_pre_i",
                                                       "milan_verdict_next", "r412_line", "r412_pad") and s["defined"])
                except BaseException as _pexc:  # noqa: BLE001
                    _playout = f"no layout: {_pexc}"
                print(f"PROBE {_pname}: layout (addr, size, name): "
                      f"{[(hex(a), z, n) for a, z, n in _playout] if isinstance(_playout, list) else _playout}")
                print(f"PROBE {_pname}: image relocations on aem_loaded "
                      f"(offset, where, kind): {_pbytes}")
                sys.stdout.flush()
            raise SystemExit(0)
'''
path.write_text(text.replace(anchor, hook + anchor), encoding="utf-8")
print(f"hook inserted into {path}")
