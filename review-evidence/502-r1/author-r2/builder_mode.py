import json, pathlib, runpy, subprocess, sys
from unittest.mock import patch
root=pathlib.Path.cwd()
sys.path.insert(0,str(root/"sw/builder"))
sys.path.insert(0,str(root/"scripts"))
from test_firmware_compiler import CompilerAudit
import ci_rv32_sdk
mode=sys.argv[1]
destination=pathlib.Path(sys.argv[2]) if mode=="sdk" else None
out=pathlib.Path(__file__).resolve().parent
if destination: ci_rv32_sdk.verify(destination)
with (out/("builder-"+mode+"-audit.jsonl")).open("w") as stream:
    audit=CompilerAudit(stream,destination)
    original=subprocess.run
    def invoke(argv, **kwargs):
        if isinstance(argv,(list,tuple)) and str(argv[0]) in audit.cross:
            return audit.invoke(argv,**kwargs)
        return original(argv,**kwargs)
    argv=[str(root/"sw/builder/test_builder.py")]+(["--require-rv32"] if destination else [])
    print("FULL BUILDER MODE:",mode,"argv:",argv,flush=True)
    with patch.object(subprocess,"run",side_effect=invoke),patch.object(sys,"argv",argv):
        runpy.run_path(str(root/"sw/builder/test_builder.py"),run_name="__main__")
    if destination:
        assert audit.compiles>0, "No pinned compiler invocation"
    else:
        assert audit.hidden==audit.cross, audit.hidden
        assert audit.compiles==0, "Absent mode compiled firmware"
    print("FULL BUILDER AUDIT:",audit.compiles,"actual compiler calls;",len(audit.hidden),"hidden candidates",flush=True)
