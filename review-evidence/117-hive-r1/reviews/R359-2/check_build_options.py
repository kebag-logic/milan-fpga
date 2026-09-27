#!/usr/bin/env python3
"""Compare the page's probe-define and library-option sentence with the public
build-provenance.txt BUILD_FLAGS and the library's CMake option defaults.

Usage: check_build_options.py <page.md> <build-provenance.txt> <upstream CMakeLists.txt> <upstream src/CMakeLists.txt>
"""
import json, re, sys
page, prov, cm, srccm = (open(p).read() for p in sys.argv[1:5])
flags = json.loads(prov.splitlines()[0][len("BUILD_FLAGS "):])
defines = sorted(f[2:] for f in flags if f.startswith("-D"))
incs = [f[2:] for f in flags if f.startswith("-I")]
para = page.split("The probe defines", 1)[1].split("It links", 1)[0]
probe_part, lib_part = para.split("the library's enabled options are", 1)
page_probe = sorted(re.findall(r"`([A-Z0-9_]+)`", probe_part))
enabled_part, disabled_part = lib_part.split(", with", 1)
page_enabled = sorted(re.findall(r"`([A-Z0-9_]+)`", enabled_part))
page_disabled = re.findall(r"`([A-Z0-9_]+)` disabled", disabled_part)
opts = dict(re.findall(r'^option\((\w+) "[^"]*" (TRUE|FALSE)\)', cm, re.M))
behav = {k: v for k, v in opts.items() if not k.startswith(("BUILD_", "INSTALL_", "ENABLE_CODE"))}
dflt_on = sorted(k for k, v in behav.items() if v == "TRUE")
dflt_off = sorted(k for k, v in behav.items() if v == "FALSE")
private = sorted(set(re.findall(r'ADD_PRIVATE_COMPILE_OPTIONS "-D(\w+)"', srccm)))
public = sorted(set(re.findall(r'ADD_PUBLIC_COMPILE_OPTIONS "-D(\w+)"', srccm)))
res = []
def chk(name, ok): res.append(ok); print(("PASS " if ok else "FAIL ") + name)
print("BUILD_FLAGS defines:", defines); print("page probe defines:", page_probe)
chk("page probe defines == BUILD_FLAGS -D set", page_probe == defines)
print("upstream behaviour options default TRUE:", dflt_on); print("default FALSE:", dflt_off)
print("page enabled:", page_enabled); print("page disabled:", page_disabled)
chk("page enabled list == upstream default-TRUE behaviour options", page_enabled == dflt_on)
chk("page disabled list == upstream default-FALSE behaviour options", sorted(page_disabled) == dflt_off)
chk("'no warnings' conditioned on the default set incl. IGNORE_INVALID_CONTROL_DATA_LENGTH",
    bool(re.search(r'"no warnings" result is conditioned on\s+that default option set, including `IGNORE_INVALID_CONTROL_DATA_LENGTH`', para)))
print("library src/CMakeLists PRIVATE-only defines (not observable from the probe build):", private)
print("library src/CMakeLists PUBLIC defines:", public)
print("include order in BUILD_FLAGS:", incs)
print("RESULT", "PASS" if all(res) else "FAIL")
sys.exit(0 if all(res) else 1)
