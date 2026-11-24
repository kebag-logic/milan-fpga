"""Prepare missing 80 MHz measurement arms without running an extra simulation leg."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"tb/verilator/ctrl_service_budget"))
import build
root=Path("$VALIDATION_STORAGE/artysplit-a829/r4")
for name,variant in (("arm-valid","valid-destinations"),("arm-later","answering-later"),("arm-declaring","declaring-outputs")):
    spec=build.build(root/name,"endstation_arty_current",1,variant=variant)
    assert spec["cpu_hz"]==spec["sys_hz"]==80_000_000
    print("PREPARED",name,spec["executable_sha256"],flush=True)
# An explicitly labelled measurement fixture reaches the two-MRPDU path, which the
# conservative bootstrap row otherwise never admits. Its numbers are not a qualified row.
text=(Path.cwd()/"sw/firmware/ctrl/loop/ctrl_loop.h").read_text()
start=text.index("#elif CTRL_LOOP_SHAPE(1u, 1u, 2u)")
end=text.index("#else",start)
old=text[start:end]
new=old.replace("#define CTRL_LOOP_BUILD_PASS_US 2000u", "#define CTRL_LOOP_BUILD_PASS_US 1300u")
plant=build.Plant("arty-measure-two-mrpdus","ctrl/loop/ctrl_loop.h",old,new)
spec=build.build(root/"arm-two","endstation_arty_current",1,mutation=plant,variant="valid-destinations")
assert spec["cpu_hz"]==spec["sys_hz"]==80_000_000
print("PREPARED arm-two (measurement only)",spec["executable_sha256"],flush=True)
