"""Which audit events the clean pin decision raises (after the proof modules are imported)."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "$LANES/697-consume/sw/firmware/ctrl/test")
import ctrl_build  # noqa
import ctrl_pin  # noqa
seen = {}
inside = [False]
armed = [False]
def hook(event, args):
    if not armed[0] or inside[0]:
        return
    inside[0] = True
    try:
        f = sys._getframe(1)
        key = (event, f"{f.f_code.co_filename.rsplit('/', 1)[-1]}:{f.f_code.co_name}")
        seen[key] = seen.get(key, 0) + 1
    finally:
        inside[0] = False
sys.addaudithook(hook)
import re
armed[0] = True
re.compile(r"x+y*z?neverseen")
armed[0] = False
print("re.compile events:", seen); seen.clear()
armed[0] = True
rc = ctrl_build.main(["--stack-pin"])
armed[0] = False
print("main rc", rc)
for k, v in sorted(seen.items()):
    print("  ", v, *k)
print("settrace event?")
seen.clear(); armed[0] = True
sys.settrace(None); sys.setprofile(None)
import gc; gc.get_referrers(ctrl_build)
armed[0] = False
print(sorted(seen))
